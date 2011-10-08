"""
searcher.py
Created by: Christopher Bess
Copyright: 2011
"""
__author__ = 'C. Bess'


from whoosh.qparser import QueryParser
from whoosh import highlight
from base import FileSearcher, SearchResult, SearchResults
from core.utils import debug, read_file
from core import settings
import indexer
import re


class WhooshSearcher(FileSearcher):
    def __init__(self, indexer):
        super(WhooshSearcher, self).__init__(indexer)
        self._index = indexer.index
        pass

    def find_path(self, path):
        parser = QueryParser('path', self._index.schema)
        query = parser.parse(unicode(path))
        return self._search(query, limit=1)

    def find_text(self, text, pagenum=1, limit=10):
        parser = QueryParser('content', self._index.schema)
        query = parser.parse(unicode(text))
        return self._search(query, pagenum, limit)
    
    def _search(self, squery, pagenum=1, limit=10):
        assert self._index is not None
        with self._index.index.searcher() as searcher:
            page = searcher.search_page(squery, pagenum, limit)
            results = self._get_results(page, pagenum, limit)
        return results

    def _get_results(self, results_page, pagenum, limit):
        """Populates the results with normalized Sherlock result data
        :param results_page: whoosh.ResultsPage instance
        @return tuple of sherlock.Result objects
        """
        hits = results_page.results
        hits.fragmenter = ResultFragmenter()
        hits.formatter = ResultFormatter()
        # create results wrapper
        results = WhooshResults(
            self,
            hits,
            total_count=hits.estimated_length(),
            pagenum=pagenum,
            limit=limit
        )
        return results


class WhooshResults(SearchResults):
    def process_hits(self, hits):
        count = len(hits)
        if hits:
            prev_count = self.limit * (self.pagenum - 1)
            # any more results
            if count - prev_count < self.limit:
                self.next_pagenum = -1
            if count > self.limit:
                # get the next page items
                hits = hits[prev_count:]
        else:
            self.next_pagenum = -1
        # get the results
        for hit in hits:
            result = WhooshResult(hit, self.searcher.indexer, **hit.fields())
            self.append(result)
        pass


class WhooshResult(SearchResult):
    def process_hit(self, hit):
        contents = read_file(self.path)
        self.context = hit.highlights('content', text=contents)
        pass


# refs:
# https://bitbucket.org/mchaput/whoosh/src/4470a8812c9e/src/whoosh/highlight.py
# http://packages.python.org/Whoosh/api/highlight.html?highlight=hit#manual-highlighting
class ResultFragmenter(highlight.Fragmenter):
    def fragment_tokens(self, text, all_tokens):
        tokens = []
        for tk in all_tokens:
            tokens.append(tk.copy())
            if tk.matched:
                yield highlight.mkfrag(text, tokens, startchar=tk.startchar, endchar=tk.endchar)


class ResultFormatter(highlight.Formatter):
    max_lines = settings.NUM_CONTEXT_LINES # fragment context
    new_line = settings.NEW_LINE

    def format_token(self, text, token, replace=False):
        token_text = text[token.startchar:token.endchar]
        return "<span class='match'>%s</span>" % token_text

    def fragement_text(self, fragment):
        """Returns the text for the specified fragment
        """
        assert self.max_lines > 0
        token = fragment # alias
        text = token.text
        nl = self.new_line
        # add the formatted token
        bText = text[:token.startchar]
        eText = text[token.endchar:]
        text = u''.join((bText, self.format_token(text, token), eText))
        # get the position up to the previous new line
        prevIdx = text.rfind(nl, 0, token.startchar)
        # get the position of the next new line
        nextIdx = text.find(nl, token.endchar)
        # should we try to get more lines
        if self.max_lines > 1:
            idx = prevIdx
            line = 1
            # lines before token
            while idx >= 0 and line <= self.max_lines:
                prevIdx = idx
                idx = text.rfind(nl, 0, prevIdx)
                line += 1
            # lines after token
            idx = nextIdx
            line = 1
            while idx >= 0 and line <= self.max_lines:
                nextIdx = idx + 1
                idx = text.find(nl, nextIdx)
                line += 1
        # get token and context
        if prevIdx < 0:
            prevIdx = 0
        token_text = text[prevIdx:nextIdx]
        return token_text

    def format(self, fragments, replace=False):
        lines = []
        for fragment in fragments:
            context = self.fragement_text(fragment)
            lines.append(context)
        final_text = u''.join(lines)
        return final_text

import xapian
DEFAULT_SEARCH_FLAGS = (
        xapian.QueryParser.FLAG_BOOLEAN |
        xapian.QueryParser.FLAG_PHRASE |
        xapian.QueryParser.FLAG_LOVEHATE |
        xapian.QueryParser.FLAG_BOOLEAN_ANY_CASE
        )

class XapianSearcher(FileSearcher):
    class MatchDecider(xapian.MatchDecider):
        def __init__(self, path, value):
            xapian.MatchDecider.__init__(self)
            self.path = path
            self.doc_value = value
            pass

        def __call__(self, document):
            path = xapian.sortable_unserialise(document.get_value(self.doc_value))
            return path == self.path

    def __init__(self, indexer):
        super(XapianSearcher, self).__init__(indexer)
        self._index = indexer.index
        self.parser = None
        self.query = None
        pass

    def find_path(self, path):
        return self._search(path, limit=1, isPath=True)

    def find_text(self, text, pagenum=1, limit=10):
        return self._search(text, pagenum, limit)

    def _search(self, text, pagenum=1, limit=10, isPath=False):
        database = self._index.index
        # Start an enquire session.
        enquire = xapian.Enquire(database)
        # Parse the query string to produce a Xapian::Query object.
        self.parser = xapian.QueryParser()
        self.parser.set_stemmer(xapian.Stem("english"))
        self.parser.set_database(database)
        self.parser.add_prefix("path", "P")
        self.parser.add_prefix("filename", "F")
        self.parser.set_stemming_strategy(xapian.QueryParser.STEM_SOME)
        self.query = self.parser.parse_query(text, DEFAULT_SEARCH_FLAGS)
        # find using the parsed query
        enquire.set_query(self.query)
        offset = pagenum * limit - limit
        if isPath:
            decider = self.MatchDecider(text, self._index.DOC_VALUE_FILENAME)
            matches = enquire.get_mset(offset, limit)#, None, decider)
        else:
            matches = enquire.get_mset(offset, limit)
        return self._get_results(matches, pagenum, limit)

    def _get_results(self, matches, pagenum, limit):
        results = XapianResults(
            self,
            matches,
            total_count=matches.get_matches_estimated(),
            pagenum=pagenum,
            limit=limit
        )
        return results


class XapianResults(SearchResults):
    def process_hits(self, matches):
        for match in matches:
            result = XapianResult(
                match,
                self.searcher
            )
            self.append(result)
            pass
        pass


class XapianResult(SearchResult):
    max_lines = settings.NUM_CONTEXT_LINES # fragment context
    new_line = settings.NEW_LINE
    class Token:
        startchar = 0
        endchar = 0

    def __init__(self, match, searcher):
        self._searcher = searcher
        kwargs = {
            'path' : match.document.get_value(indexer.XapianIndexer.DOC_VALUE_FILEPATH),
            'filename' : match.document.get_value(indexer.XapianIndexer.DOC_VALUE_FILENAME)
        }
        super(XapianResult, self).__init__(match, None, **kwargs)
        pass

    def process_hit(self, hit):
        qparser = self._searcher.parser
        query = self._searcher.query
        content = read_file(self.path)
        lines = []
        # For each query word,
        for queryWord in set(query):
            # Reverse map query words to document words
            documentWords = list(qparser.unstemlist(queryWord))
            # If the query word is not in the document, skip it
            if not documentWords:
                continue
            # Prepare regular expression using matching document words
            searchExpression = r'|'.join(documentWords)
            pattern = re.compile(searchExpression, re.IGNORECASE)
            for match in pattern.finditer(content):
                token = self.Token()
                token.startchar = match.start()
                token.endchar = match.end()
                # get the context line
                context = self.fragement_text(token, content)
                lines.append(context)
        self.context = u''.join(lines)
        pass

    def format_token(self, text, token):
        token_text = text[token.startchar:token.endchar]
        return "<span class='match'>%s</span>" % token_text

    def fragement_text(self, token, text):
        """Returns the text for the specified fragment
        """
        assert self.max_lines > 0
        nl = self.new_line
        # add the formatted token
        bText = text[:token.startchar]
        eText = text[token.endchar:]
        text = u''.join((bText, self.format_token(text, token), eText))
        # get the position up to the previous new line
        prevIdx = text.rfind(nl, 0, token.startchar)
        # get the position of the next new line
        nextIdx = text.find(nl, token.endchar)
        # should we try to get more lines
        if self.max_lines > 1:
            idx = prevIdx
            line = 1
            # lines before token
            while idx >= 0 and line <= self.max_lines:
                prevIdx = idx
                idx = text.rfind(nl, 0, prevIdx)
                line += 1
            # lines after token
            idx = nextIdx
            line = 1
            while idx >= 0 and line <= self.max_lines:
                nextIdx = idx + 1
                idx = text.find(nl, nextIdx)
                line += 1
        # get token and context
        if prevIdx < 0:
            prevIdx = 0
        token_text = text[prevIdx:nextIdx]
        return token_text

