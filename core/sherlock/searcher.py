""" 
searcher.py
Created by: Christopher Bess
Copyright: 2011
"""

from whoosh.qparser import QueryParser
# from whoosh.query import And, Term
from whoosh import highlight
from core.sherlock import logger as log
from core.utils import debug, read_file
import settings


class Searcher(object):
    def __init__(self, indexer):
        self._indexer = indexer
        self._index = indexer.index
        pass

    @property
    def indexer(self):
        return self._indexer

    def find_text(self, text, pagenum=1, limit=10):
        """Finds the specified text by searching the internal index
        """
        log.debug('searching for: %s' % text)
        parser = QueryParser('content', self._index.schema)
        query = parser.parse(unicode(text))
        return self.search(query, pagenum, limit)

    def find_path(self, path):
        """Finds the document at the specified path
        """
        log.debug('search for path: %s' % path)
        parser = QueryParser('path', self._index.schema)
        query = parser.parse(unicode(path))
        return self.search(query, limit=1)
        
    def search(self, squery, pagenum=1, limit=10):
        """Searches the internal index using the specified query
        @param QueryParser squery
        """
        assert self._index is not None
        log.debug('search page %d, limit %d' % (pagenum, limit))
        results = None
        with self._index.searcher() as searcher:
            page = searcher.search_page(squery, pagenum, limit, terms=True)
            results = self._get_results(page, pagenum, limit)
        return results
        
    def _get_results(self, results_page, pagenum, limit):
        """Populates the results with normalized Sherlock result data
        @param whoosh.ResultsPage results_page
        @return tuple of sherlock.Result objects
        """
        hits = results_page.results
        hits.fragmenter = ResultFragmenter()
        hits.formatter = ResultFormatter()
        # create results wrapper
        results = Results(
            self,
            hits,
            total_count=hits.estimated_length(),
            pagenum=pagenum,
            limit=limit
        )
        return results


class Results(list):
    """Represents the search results
    """
    def __init__(self, searcher, hits, **kwargs):
        """Initializes this Results instance
        :param searcher: sherlock.Searcher instance that created the items
        :param hits: sequence of whoosh.Hit objects from the search
        :param kwargs: {
            total_count = Total number of results for the entire search
            pagenum = The page of the expected results
            limit = The maximum number of results to store
        }
        """
        super(list, self).__init__()
        self._total_count = kwargs.get('total_count', -1)
        self._pagenum = kwargs.get('pagenum', 0)
        self._limit = kwargs.get('limit', settings.RESULTS_PER_PAGE)
        self._searcher = searcher
        self._next_page = self._pagenum + 1
        self._prev_page = -1
        if self._pagenum > 1 and self._limit > 0:
            self._prev_page = self._pagenum - 1
        self._items = []
        self._process_hits(hits)
        pass

    def _process_hits(self, hits):
        count = len(hits)
        if hits:
            prev_count = self._limit * (self._pagenum - 1)
            # any more results
            if count - prev_count < self._limit:
                self._next_page = -1
            if count > self._limit:
                # get the next page items
                hits = hits[prev_count:]

        for hit in hits:
            result = Result(hit, self._searcher.indexer, **hit.fields())
            self.append(result)
        pass

    @property
    def next_pagenum(self):
        return self._next_page

    @property
    def prev_pagenum(self):
        return self._prev_page

    @property
    def items(self):
        """Returns the list of transformer.Item objects, processed by transformer.Transformer"""
        return self._items

    def __items(self):
        """Returns he actual results from the search query
        @return tuple of the results
        """
        return tuple(super(list, self))

    @property
    def total_count(self):
        """Results the total count of the results"""
        return self._total_count


class Result(object):
    """Represents a sherlock result
    """
    def __init__(self, hit, indexer, **kwargs):
        """Initializes this Result instance
        @param whoosh.Hit hit The hit this instance represents
        @param sherlock.Indexer indexer The Indexer that holds this search result
        @param kwargs {
            path = Path of the file this result represents
            filename = Filename of the file
        }
        """
        # the textual context of the hit
        self._context = ''
        self._path = kwargs['path']
        self._filename = kwargs['filename']
        # build index path
        path = settings.INDEX_PATH % { 'sherlock_dir' : settings.ROOT_DIR }
        self._index_path = self._path.replace(path, '')
        self._process_hit(hit)
        pass
        
    def _process_hit(self, hit):
        """Process the result data, reads the original file to produce
        the context
        @remark For now it only processes to get the context for the result
        """
        contents = read_file(self.path)
        self._context = hit.highlights('content', text=contents)
        pass

    @property
    def index_path(self):
        """Returns the path within the index path.
        @remark The full file path without the index path prepended.
        """
        return self._index_path
        
    @property
    def path(self):
        """path
        """
        return self._path
        
    @property
    def filename(self):
        """filename
        """
        return self._filename
        
    @property
    def context(self):
        """context
        """
        return self._context


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

        