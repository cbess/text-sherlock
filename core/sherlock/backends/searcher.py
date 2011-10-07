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
            self._next_page = -1
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


class XapianSearcher(FileSearcher):
    pass