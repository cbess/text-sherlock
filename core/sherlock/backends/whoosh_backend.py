# encoding: utf-8
"""
whoosh_backend.py
Created by Christopher Bess
Copyright 2011

refs:
http://packages.python.org/Whoosh/quickstart.html
http://packages.python.org/Whoosh/indexing.html
"""
__author__ = 'C. Bess'

import os
from whoosh.index import create_in, open_dir, exists_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh import highlight
from core import settings
from core.utils import debug, safe_read_file, fragment_text, read_file
from base import FileSearcher, FileIndexer, SearchResult, SearchResults

## Indexer

class WhooshIndexer(FileIndexer):
    # Text index schema
    schema = Schema(
        filename=TEXT(stored=True),
        path=ID(stored=True, unique=True),
        content=TEXT
    )
    _index = None
    
    def __init__(self, *args, **kwargs):
        super(WhooshIndexer, self).__init__(*args, **kwargs)
        pass

    @property
    def index(self):
        return self._index

    def doc_count(self):
        if not self._index:
            return -1
        return self._index.doc_count_all()

    def open_index(self, path, *args, **kwargs):
        self._index = open_dir(path)
        pass

    def create_index(self, path, *args, **kwargs):
        self._index = create_in(path, self.schema)
        pass

    def begin_index_file(self, filepath):
        self._writer = self._index.writer()
        pass

    def index_file(self, filepath, *args, **kwargs):
        assert self._index is not None
        contents = safe_read_file(filepath)
        if contents is None:
            return
        path = unicode(filepath)
        # build doc
        doc = dict(
            filename=unicode(os.path.basename(filepath)),
            path=path,
            content=contents + path
        )
        self._writer.update_document(**doc)
        pass

    def end_index_file(self, filepath):
        self._writer.commit()
        pass

    def index_exists(self, path):
        return exists_in(path)


## Searcher

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
        # the file path could have matched
        if not self.context:
            self.context = self.path
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
    max_sub_results = settings.MAX_SUB_RESULTS
    
    def format(self, fragments, replace=False):
        lines = []
        for fragment in fragments:
            context = fragment_text(fragment, fragment.text)
            lines.append(context)
            if len(lines) >= self.max_sub_results:
                break
        final_text = u''.join(lines)
        return final_text
