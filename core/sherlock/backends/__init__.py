# encoding: utf-8
"""
__init__.py
Created by Christopher Bess
Copyright 2011
"""
__author__ = 'C. Bess'

import indexer
import searcher

# Lists the indexer classes that can handle indexing operations
AVAILABLE_INDEXERS = {
    'whoosh' : indexer.WhooshIndexer
}

# Lists the searcher classes that can handle search operations
AVAILABLE_SEARCHERS = {
    'whoosh' : searcher.WhooshSearcher
}


try:
    import xapian
    AVAILABLE_INDEXERS['xapian'] = indexer.XapianIndexer
    AVAILABLE_SEARCHERS['xapian'] = None
except ImportError:
    pass