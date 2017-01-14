#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
indexer.py
Created by Christopher Bess
Copyright 2011
"""

from __future__ import absolute_import

import contextlib
import os
import settings
import shutil
from core import FULL_INDEXES_PATH, FORCE_INDEX_REBUILD
from core.sherlock import logger as log
from core.sherlock import searcher
from . import backends
from core.utils import debug

try:
    _ensure_unicode = unicode
except NameError:
    _ensure_unicode = str


def get_indexer(name=settings.DEFAULT_INDEX_NAME, rebuild_index=FORCE_INDEX_REBUILD, **kwargs):
    """Returns an indexer with the specified name. Provides an indexer
    using the default settings.
    :param rebuild_index: True to rebuild the index on open/create. Default is False.
    """
    idxr = Indexer(name, recursive=settings.INDEX_RECURSIVE, rebuild_index=rebuild_index, **kwargs)
    path = FULL_INDEXES_PATH
    idxr.open(path, **kwargs)
    return idxr


def index_paths(paths, name=settings.DEFAULT_INDEX_NAME):
    """Indexes the files at the given paths and places them in
    the specified index.
    :param paths: The absolute paths to the directories or files to index.
    :param name: The name of the index to add the documents from the
    target paths to.
    """
    # index files for the search
    with _get_indexer_with_cleanup(name) as idxr:
        for path in paths:
            idxr.index_text(_ensure_unicode(path))


def index_path(path, name=settings.DEFAULT_INDEX_NAME):
    """Indexes the files at the given path and places them in
    the specified index.
    :param path: The absolute path to the directory or file to index.
    :param name: The name of the index to add the documents from the
    target path to.
    """
    # index a file for the search
    with _get_indexer_with_cleanup(name) as idxr:
        idxr.index_text(_ensure_unicode(path))


@contextlib.contextmanager
def _get_indexer_with_cleanup(name=settings.DEFAULT_INDEX_NAME, rebuild_index=FORCE_INDEX_REBUILD, **kwargs):
    """Prepare an indexer for use and remove orphaned files if necessary.

    :param rebuild_index: True to rebuild the index on open/create. Default is False.
    """
    # get the indexer for use
    idxr = get_indexer(name=name, rebuild_index=rebuild_index, **kwargs)
    yield idxr
    # if not rebuilding the index, then cleanup orphaned files that
    # were previously indexed
    if not FORCE_INDEX_REBUILD:
        idxr.clean_index()


class Indexer(object):
    def __init__(self, name=settings.DEFAULT_INDEX_NAME, *args, **kwargs):
        """Initializes this instance with the given arguments.
        @param kwargs {
            rebuild_index = True
        }
        """
        IndexerBackend = backends.AVAILABLE_INDEXERS.get(settings.DEFAULT_INDEXER)
        if IndexerBackend is None:
            raise Exception('No available indexer for: %s' % settings.DEFAULT_INDEXER)

        self._index = IndexerBackend(name)
        # path of the index directory
        self._path = None
        self._name = name
        self._is_writable = kwargs.get('writable', True)
        self._rebuild_index = kwargs.get('rebuild_index', False)
        self._is_recursive = kwargs.get('recursive', False)

    def doc_count(self):
        """Returns the count of all documents indexed."""
        return self.index.doc_count()

    def get_index(self):
        """Returns a Sherlock index for this indexer."""
        return Index(self)

    @property
    def index(self):
        """Returns the internal FileIndexer index."""
        return self._index

    @property
    def name(self):
        """Returns the name of this indexer."""
        return self._name

    @property
    def path(self):
        """Returns the path of index."""
        return self._path

    def clear_index_directory(self):
        """Removes the indexed contents."""
        if self.path and self._path.startswith(settings.INDEXES_PATH):
            shutil.rmtree(self.path)
            log.warning('removed index at %s' % self.path)

    def clean_index(self):
        """Cleans the index by purging any documents that no longer exist."""
        log.info('Cleaning index')
        self._index.clean_index()

    def open(self, index_path, **kwargs):
        """Creates or opens an index at the specified path."""
        if not os.path.isdir(index_path):
            msg = 'Directory `%s` is not a valid index directory.' % index_path
            log.warning(msg)
            raise Exception(msg)
        # create the dir, if needed
        path = os.path.join(index_path, self._name)
        if not os.path.isdir(path):
            os.mkdir(path)
            log.warning('created index directory at %s' % path)
        # create or open the index
        if self._rebuild_index or not self._index.index_exists(path):
            log.debug('creating index at %s' % path)
            self._index.create_index(path)
        else:
            log.debug('opening index at %s' % path)
            self._index.open_index(path, writable=self._is_writable)
        # store indexes path
        self._path = path

    def index_text(self, path, recursive=None):
        """Indexes the text at the specified path."""
        assert self._index is not None
        if recursive is not None:
            self._is_recursive = recursive
        # index items
        self._index.begin_index_file(path)
        self.__index_path(path)
        self._index.end_index_file(path)

    def __index_path(self, path):
        """Indexes the items at the specified path."""
        if os.path.isdir(path):
            self.__index_dir(path)
        elif os.path.isfile(path):
            self.__index_file(path)
        else:
            msg = 'Path %s is not valid for indexing' % path
            log.warning(msg)
            raise Exception(msg)

    def __index_dir(self, dpath):
        """Indexes the contents of the directory at the specified path."""
        log.debug('Checking directory: %s' % dpath)
        # sanity checks
        if not isinstance(settings.EXCLUDE_FILE_SUFFIX, (tuple, list, type(None))):
            raise Exception('settings.EXCLUDE_FILE_SUFFIX must be a tuple or None, found: %s' %
                            type(settings.EXCLUDE_FILE_SUFFIX))
        if not isinstance(settings.INCLUDE_FILE_SUFFIX, (tuple, list, type(None))):
            raise Exception('settings.INCLUDE_FILE_SUFFIX must be a tuple or None, found: %s' %
                            type(settings.INCLUDE_FILE_SUFFIX))
        # nested, reused code block
        def check_name(name):
            """Returns True if the item with the specified name can be indexed."""
            can_index = True
            # ignore hidden files
            if name.startswith('.'):
                return False
            # ignore excluded files
            if settings.EXCLUDE_FILE_SUFFIX:
                for suffix in settings.EXCLUDE_FILE_SUFFIX:
                    can_index = True
                    if name.endswith(suffix):
                        return False
            # ignore files that do not have the given suffixes
            if settings.INCLUDE_FILE_SUFFIX:
                for suffix in settings.INCLUDE_FILE_SUFFIX:
                    can_index = False
                    if name.endswith(suffix):
                        return True
            return can_index
        # perform item indexing
        if not self._is_recursive:
            # just check the files in the target directory
            items = os.listdir(dpath)
            for item in items:
                if not check_name(item):
                    continue
                path = os.path.join(dpath, item)
                self.__index_file(path)
        else:
            # traverse the given path
            for dirpath, dirnames, filenames in os.walk(dpath):
                dirname = os.path.basename(dirpath)
                # ignore hidden dirs
                if dirname.startswith('.'):
                    continue
                for name in filenames:
                    can_index = check_name(name)
                    if can_index:
                        path = os.path.join(dirpath, name)
                        self.__index_file(path)

    def __index_file(self, filepath):
        """Indexes the contents of the file at the specified path."""
        has_file_changed, db_record = self._index.has_file_updated(filepath)
        if FORCE_INDEX_REBUILD and db_record is not None:
            has_file_changed = True
        if not has_file_changed:
            return
        log.debug('indexing file: %s' % filepath)
        self._index.index_file(filepath, document_id=db_record.id)


class Index(object):
    def __init__(self, indexer):
        """Initializes this Index instance."""
        self._indexer = indexer
        self._searcher = searcher.Searcher(indexer)

    def name(self):
        """Returns the name of this index."""
        return self._indexer.name

    def search(self, text, pagenum=1, limit=10):
        """Searches the index for the specified text.
        @return list of results
        """
        return self._searcher.find_text(text, pagenum=pagenum, limit=limit)

    def search_path(self, path):
        """Searches the index for the specified path.
        @return list of results
        """
        return self._searcher.find_path(path)

    def suggestions(self, text, limit=3):
        """Returns suggestions for the search term generated by the index"""
        return self._searcher.find_suggestions(text, limit)
