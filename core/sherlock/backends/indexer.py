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


class FileIndexer(object):
    """Represents the base file indexer object. All methods are required to be implemented.
    """
    def __init__(self, *args, **kwargs):
        pass

    def doc_count(self):
        """Returns the total document count
        """
        raise NotImplemented

    def open_index(self, path, *args, **kwargs):
        """Opens the index at the specified path
        """
        raise NotImplemented

    def create_index(self, path, *args, **kwargs):
        """Creates the index at the specified path
        """
        raise NotImplemented

    def index_file(self, filepath, *args, **kwargs):
        """Indexes and stores the file at the specified path
        """
        raise NotImplemented

    def index_exists(self, path):
        """Returns True if an index exist at the specified path, False otherwise
        """
        raise NotImplemented


class WhooshIndexer(FileIndexer):
    # Text index schema
    text_schema = Schema(
        filename=TEXT(stored=True),
        path=ID(stored=True),
        content=TEXT
    )
    _index = None
    
    def __init__(self, *args, **kwargs):
        super(FileIndexer, self).__init__()
        pass

    def doc_count(self):
        if not self._index:
            return -1
        return self._index.doc_count_all()

    def open_index(self, path, *args, **kwargs):
        self._index = open_dir(path)
        pass

    def create_index(self, path, *args, **kwargs):
        self._index = create_in(path, self.text_schema)
        pass

    def index_file(self, filepath, *args, **kwargs):
        assert self._index is not None
        writer = self._index.writer()
        contents = read_file(filepath)
        doc = dict(
            filename=unicode(os.path.basename(filepath)),
            path=unicode(filepath),
            content=contents
        )
        writer.add_document(**doc)
        writer.commit()
        return None

    def index_exists(self, path):
        return exists_in(path)


class XapianIndexer(FileIndexer):
    pass