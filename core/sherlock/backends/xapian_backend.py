# encoding: utf-8
"""
xapian_backend.py
Created by Christopher Bess
Copyright 2011

refs:
http://xapian.org/docs/bindings/python/
http://xapian.org/docs/apidoc/html/annotated.html
https://github.com/notanumber/xapian-haystack/blob/master/xapian_backend.py
http://invisibleroads.com/tutorials/xapian-search-pylons.html#filter-documents-by-number-using-value
"""
__author__ = 'C. Bess'

import re
import os
import xapian
from core import settings
from core.sherlock import logger
from core.utils import debug, safe_read_file, fragment_text, read_file
from base import FileSearcher, FileIndexer, SearchResult, SearchResults


DEFAULT_SEARCH_FLAGS = (
    xapian.QueryParser.FLAG_BOOLEAN |
    xapian.QueryParser.FLAG_PHRASE |
    xapian.QueryParser.FLAG_LOVEHATE |
    xapian.QueryParser.FLAG_BOOLEAN_ANY_CASE |
    xapian.QueryParser.FLAG_WILDCARD
)

## Indexer

class XapianIndexer(FileIndexer):
    DOC_VALUE_FILENAME = 0
    DOC_VALUE_FILEPATH = 1
    def __init__(self, *args, **kwargs):
        super(XapianIndexer, self).__init__(*args, **kwargs)
        self._path = None
        pass

    @property
    def path(self):
        return self._path

    def doc_count(self):
        return self.index.get_doccount()

    def open_index(self, path, *args, **kwargs):
        self._path = path
        is_writable = kwargs.get('writable', True)
        if is_writable:
            self.index = xapian.WritableDatabase(path, xapian.DB_OPEN)
        else:
            self.index = xapian.Database(path)
        pass

    def create_index(self, path, *args, **kwargs):
        self._path = path
        self.index = xapian.WritableDatabase(path, xapian.DB_CREATE_OR_OVERWRITE)
        pass

    def begin_index_file(self, filepath):
        # Initialize indexer
        self.indexer = xapian.TermGenerator()
        # Set word stemmer to English
        self.indexer.set_stemmer(xapian.Stem('english'))
        pass

    def index_file(self, filepath, *args, **kwargs):
        # index file content
        contents = safe_read_file(filepath)
        if contents is None:
            return
        document = xapian.Document()
        # store file meta
        filename = os.path.basename(filepath)
        document.add_value(self.DOC_VALUE_FILENAME, filename)
        document.add_value(self.DOC_VALUE_FILEPATH, filepath)
        # index document and file path
        self.indexer.set_document(document)
        self.indexer.index_text(contents+' '+filepath)
        doc_id = kwargs.get('document_id')
        if doc_id:
            self.index.replace_document(doc_id, document)
        else:
            self.index.add_document(document)
        pass

    def end_index_file(self, filepath):
        self.index.flush()
        pass

    def index_exists(self, path):
        return os.path.isdir(path)

    def clean_index(self):
        """Cleans the index by purging any documents that no longer exist.
        """
        # iterate each record in the database
        # see if it exists on the file system
        for record in self.get_indexed_files():
            if not os.path.exists(record.path):
                try:
                    self.index.delete_document(record.id)
                except xapian.DocNotFoundError:
                    # it is safe to continue
                    pass
                record.delete_instance()
                logger.debug('removed indexed file: %s' % record)
        pass


## Searcher

class XapianSearcher(FileSearcher):
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
        self.parser.set_stemming_strategy(xapian.QueryParser.STEM_SOME)
        self.query = self.parser.parse_query(text, DEFAULT_SEARCH_FLAGS)
        # find using the parsed query
        enquire.set_query(self.query)
        offset = pagenum * limit - limit
        matches = enquire.get_mset(offset, limit)
        # build results
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
    max_sub_results = settings.MAX_SUB_RESULTS
    class Token:
        startchar = 0
        endchar = 0

    def __init__(self, match, searcher):
        self._searcher = searcher
        kwargs = {
            'path' : match.document.get_value(XapianIndexer.DOC_VALUE_FILEPATH),
            'filename' : match.document.get_value(XapianIndexer.DOC_VALUE_FILENAME)
        }
        super(XapianResult, self).__init__(match, None, **kwargs)
        pass

    def process_hit(self, hit):
        self.context = self._hit_context(hit)
        # the file path could have matched
        if not self.context:
            self.context = self.path
        pass
    
    def _hit_context(self, hit):
        qparser = self._searcher.parser
        query = self._searcher.query
        contents = read_file(self.path)
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
            for match in pattern.finditer(contents):
                token = self.Token()
                token.startchar = match.start()
                token.endchar = match.end()
                # get the context line
                context = fragment_text(token, contents)
                self.append_line(lines, context)
                if len(lines) >= self.max_sub_results:
                    break
        return u''.join(lines)
