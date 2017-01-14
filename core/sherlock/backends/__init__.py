#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__init__.py
Created by Christopher Bess
Copyright 2011
"""

from __future__ import print_function
from __future__ import absolute_import

from . import whoosh_backend

__author__ = 'C. Bess'


# Lists the indexer classes that can handle indexing operations
AVAILABLE_INDEXERS = {
    'whoosh' : whoosh_backend.WhooshIndexer
}

# Lists the searcher classes that can handle search operations
AVAILABLE_SEARCHERS = {
    'whoosh' : whoosh_backend.WhooshSearcher
}


try:
    from . import xapian_backend
    AVAILABLE_INDEXERS['xapian'] = xapian_backend.XapianIndexer
    AVAILABLE_SEARCHERS['xapian'] = xapian_backend.XapianSearcher
except ImportError:
    print('Xapian backend support unavailable')


# for stats output
def searcher_names(separator=', '):
    return separator.join(AVAILABLE_SEARCHERS.keys())

def indexer_names(separator=', '):
    return separator.join(AVAILABLE_INDEXERS.keys())
