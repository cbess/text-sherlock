""" 
searcher.py
Created by: Christopher Bess
Copyright: 2011
"""

from whoosh.qparser import QueryParser
from core.sherlock import logger as log
import settings
import backends
from datetime import datetime


class Searcher(object):
    def __init__(self, indexer):
        SearcherBackend = backends.AVAILABLE_SEARCHERS[settings.DEFAULT_SEARCHER]
        self._searcher = SearcherBackend(indexer)
        pass

    @property
    def indexer(self):
        return self._searcher.indexer

    def find_text(self, text, pagenum=1, limit=10):
        """Finds the specified text by searching the internal index
        """
        log.debug('[%s] searching for: %s' % (datetime.now(), text))
        return self._searcher.find_text(text, pagenum, limit)

    def find_path(self, path):
        """Finds the document at the specified path
        """
        log.debug('search for path: %s' % path)
        return self._searcher.find_path(path)

