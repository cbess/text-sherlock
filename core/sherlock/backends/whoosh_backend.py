# encoding: utf-8
"""
whoosh_backend.py
Created by Christopher Bess
Copyright 2011

refs:
https://whoosh.readthedocs.io/en/latest/quickstart.html
https://whoosh.readthedocs.io/en/latest/indexing.html
"""

from __future__ import absolute_import

import os
from whoosh.index import create_in, open_dir, exists_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh import highlight
from core import settings
from core.sherlock import logger
from core.utils import debug, safe_read_file, fragment_text, read_file
from .base import FileSearcher, FileIndexer, SearchResult, SearchResults

__author__ = 'C. Bess'

## Indexer

class WhooshIndexer(FileIndexer):
    # Text index schema
    schema = Schema(
        filename=TEXT(stored=True, spelling=True),
        path=ID(stored=True, unique=True),
        content=TEXT
    )
    _index = None

    def __init__(self, *args, **kwargs):
        super(WhooshIndexer, self).__init__(*args, **kwargs)

    @property
    def index(self):
        return self._index

    def doc_count(self):
        if not self._index:
            return -1
        return self._index.doc_count_all()

    def open_index(self, path, *args, **kwargs):
        self._index = open_dir(path)

    def create_index(self, path, *args, **kwargs):
        self._index = create_in(path, self.schema)

    def begin_index_file(self, filepath):
        self._writer = self._index.writer()

    def index_file(self, filepath, *args, **kwargs):
        assert self._index is not None
        contents = safe_read_file(filepath)
        if contents is None:
            return
        path = filepath
        # build doc
        doc = dict(
            filename=os.path.basename(filepath),
            path=path,
            content=contents + path
        )
        self._writer.update_document(**doc)

    def end_index_file(self, filepath):
        self._writer.commit()

    def index_exists(self, path):
        return exists_in(path)

    def clean_index(self):
        """Cleans the index by purging any documents that no longer exist.
        """
        # iterate each record in the database
        # see if it exists on the file system
        for record in self.get_indexed_files():
            if not os.path.exists(record.path):
                self._index.delete_by_term('path', record.path)
                record.delete_instance()
                logger.debug('removed indexed file: %s' % record)
        # Docs says the index has this method, it doesn't
        # must find a way to 'purge' deleted documents.
        # It does remove them from the query, but the index info is stored until purged.
        # http://packages.python.org/Whoosh/indexing.html#deleting-documents
        #self.index.commit()

## Searcher

class WhooshSearcher(FileSearcher):
    def __init__(self, indexer):
        super(WhooshSearcher, self).__init__(indexer)
        self._index = indexer.index

    def find_path(self, path):
        parser = QueryParser('path', self._index.schema)
        query = parser.parse(path)
        return self._search(query, limit=1)

    def find_text(self, text, pagenum=1, limit=10):
        parser = QueryParser('content', self._index.schema)
        query = parser.parse(text)
        return self._search(query, pagenum, limit)

    def find_suggestions(self, text, limit=3):
        with self._index.index.searcher() as searcher:
            corrector = searcher.corrector('content')
            return [word for word in corrector.suggest(text, limit=limit) if word != text]

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


class WhooshResult(SearchResult):
    def process_hit(self, hit):
        contents = read_file(self.path)
        self.context = hit.highlights('content', text=contents)
        # the file path could have matched
        if not self.context:
            self.context = self.path


# refs:
# https://bitbucket.org/mchaput/whoosh/src/4470a8812c9e/src/whoosh/highlight.py
# http://whoosh.readthedocs.io/en/latest/api/highlight.html#manual-highlighting
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
