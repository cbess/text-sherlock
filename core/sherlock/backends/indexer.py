# encoding: utf-8
"""
indexer.py
Created by Christopher Bess
Copyright 2011

refs:
http://xapian.org/docs/bindings/python/
http://invisibleroads.com/tutorials/xapian-search-pylons.html#filter-documents-by-number-using-value
"""
__author__ = 'C. Bess'

import os
from whoosh.index import create_in, open_dir, exists_in
from whoosh.fields import *
from core.utils import read_file, debug
from base import FileIndexer


class WhooshIndexer(FileIndexer):
    # Text index schema
    schema = Schema(
        filename=TEXT(stored=True),
        path=ID(stored=True),
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
        contents = read_file(filepath)
        doc = dict(
            filename=unicode(os.path.basename(filepath)),
            path=unicode(filepath),
            content=contents
        )
        self._writer.add_document(**doc)
        return None

    def end_index_file(self, filepath):
        self._writer.commit()
        pass

    def index_exists(self, path):
        return exists_in(path)


class XapianIndexer(FileIndexer):
    DOC_VALUE_FILENAME = 0
    DOC_VALUE_FILEPATH = 1
    def __init__(self, *args, **kwargs):
        super(XapianIndexer, self).__init__(*args, **kwargs)
        import xapian
        self.xapian = xapian
        self._path = None
        pass

    @property
    def path(self):
        return self._path

    def doc_count(self):
        return self.index.get_doccount()

    def open_index(self, path, *args, **kwargs):
        self._path = path
        self.index = self.xapian.WritableDatabase(path, self.xapian.DB_OPEN)
        pass

    def create_index(self, path, *args, **kwargs):
        self._path = path
        self.index = self.xapian.WritableDatabase(path, self.xapian.DB_CREATE_OR_OVERWRITE)
        pass

    def begin_index_file(self, filepath):
        # Initialize indexer
        self.indexer = self.xapian.TermGenerator()
        # Set word stemmer to English
        self.indexer.set_stemmer(self.xapian.Stem('english'))
        pass

    def index_file(self, filepath, *args, **kwargs):
        # index file content
        content = read_file(filepath)
        document = self.xapian.Document()
        # store file meta
        filename = os.path.basename(filepath)
        document.add_value(self.DOC_VALUE_FILENAME, filename)
        document.add_value(self.DOC_VALUE_FILEPATH, filepath)
        document.add_term('P'+filepath)
        document.add_term('F'+filename)
        # index document
        self.indexer.set_document(document)
        self.indexer.index_text(content)
        self.index.add_document(document)
        
        # index the path to search against it
#        document = self.xapian.Document()
#        document.add_value(self.DOC_VALUE_FILENAME, filename)
#        document.add_value(self.DOC_VALUE_FILEPATH, filepath)
#        document.set_data(filepath)
#        # index it
#        self.indexer.set_document(document)
#        self.indexer.index_text(filepath)
#        self.index.add_document(document)
        pass

    def end_index_file(self, filepath):
        self.index.flush()
        pass

    def index_exists(self, path):
        return os.path.isdir(path)
