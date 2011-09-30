# encoding: utf-8
"""
indexer.py
Created by Christopher Bess
Copyright 2011
"""

import os
from whoosh.index import create_in, open_dir
from whoosh.fields import *
import settings
from core.sherlock import logger as log
from core.utils import read_file, debug
from core.sherlock import searcher


# Text index schema
text_schema = Schema(
    filename=TEXT(stored=True), 
    path=ID(stored=True),
    content=TEXT
)


def get_indexer(name='main'):
    """Returns an indexer with the specified name. Provides an indexer
    using the default settings.
    """
    idxr = Indexer(name, recursive=settings.INDEX_RECURSIVE)
    path = settings.INDEX_PATH % { 'sherlock_dir' : os.path.abspath('.') }
    idxr.create(path)
    return idxr
    

class Indexer(object):
    def __init__(self, name='main', *args, **kwargs):
        """Initializes this instance with the given arguments.
        @param kwargs {
            rebuild_index = True
        }
        """
        self._index = None
        self._writer = None
        # path of the indexed content (directory)
        self._path = None
        self._name = name
        self._rebuild_index = kwargs.get('rebuild_index', True)
        self._is_recursive = kwargs.get('recursive', False)
        pass
        
    def doc_count(self):
        """ Returns the count of all documents indexed """
        return self.index().doc_count_all()
        
    def get_index(self):
        """Returns a Sherlock index of for this indexer
        """
        return Index(self)
        
    def index(self):
        """Returns the internal Whoosh index
        """
        return self._index
        
    def name(self):
        """Returns the name of this indexer
        """
        return self._name
        
    def remove_index(self):
        """Removes the indexed contents
        """
        if self._path and self._path.startswith(settings.INDEX_PATH):
            os.system('rm -rf %s' % self._path)
            log.warning('removed index at %s' % self._path)
        pass
        
    def create(self, index_path):
        """Creates an index at specified path.
        """
        if not os.path.isdir(index_path):
            msg = "Directory `%s` is not a valid index directory." % index_path
            log.warning(msg)
            raise Exception(msg)
        # create the dir, if needed
        path = os.path.join(index_path, self._name)
        log.debug('creating index at %s' % path)
        if not os.path.isdir(path):
            os.mkdir(path)
            log.warning('created index directory at %s' % path)
        if self._rebuild_index:
            self._index = create_in(path, text_schema)
        else:
            self._index = open_dir(path)
        self._path = path
        pass
        
    def index_text(self, path, recursive=None):
        """Indexes the text at the specified path.
        """
        assert self._index is not None
        if recursive is not None:
            self._is_recursive = recursive
        # index items    
        self._writer = self._index.writer()
        self._index_path(path)
        self._writer.commit()
        pass
        
    def _index_path(self, path):
        """Indexes the items at the specified path.
        """
        log.debug('indexing item(s) at %s' % path)
        if os.path.isdir(path):
            self._index_dir(path)
        elif os.path.isfile(path):
            self._index_file(path)
        else:
            msg = 'Path %s is not valid' % path
            log.warning(msg)
            raise Exception(msg)
        pass
        
    def _index_dir(self, dpath):
        """Indexes the contents of the directory at the specified path.
        """
        log.debug('indexing directory: %s' % dpath)
        if not self._is_recursive:
            # just check the files in the target directory
            items = os.listdir(dpath)
            for item in items:
                path = os.path.join(dpath, item)
                self._index_file(path)
                pass
        else:
            # traverse the given path
            for dirpath, dirnames, filenames in os.walk(dpath):
                for name in filenames:
                    can_index = True
                    # ignore excluded files
                    for suffix in settings.EXCLUDE_FILE_SUFFIX:
                        if name.endswith(suffix):
                            can_index = False
                    # don't look at hidden files
                    if can_index:
                        can_index = not name.startswith(".")
                    if can_index:
                        path = os.path.join(dirpath, name)
                        self._index_file(path)
        pass
        
    def _index_file(self, filepath):
        """Indexes the contents of the file at the specified path.
        """
        log.debug('indexing file: %s' % filepath)
        contents = read_file(filepath)
        doc = dict(
            filename=unicode(os.path.basename(filepath)),
            path=unicode(filepath),
            content=contents
        )
        self._writer.add_document(**doc)
        pass
        
        
class Index(object):
    def __init__(self, indexer):
        """Initializes this Index instance
        """
        self._indexer = indexer
        self._searcher = searcher.Searcher(indexer)
        pass
        
    def name(self):
        """Returns the name of this index
        """
        return self._indexer.name()
        
    def search(self, text):
        """Searches the index for the specified text.
        @return list of results
        """
        return self._searcher.find_text(text)
        