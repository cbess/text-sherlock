#!/usr/bin/env python
# encoding: utf-8
""" 
main.py
Created by Christopher Bess
Copyright 2011
"""

script_description = 'Runs the main application.'
try:
    # optparse is deprecated, but I wanted broader compatibility
    from optparse import OptionParser
    parser = OptionParser(description=script_description)
    add_argument = parser.add_option
except ImportError:
    # this is here to help any future upgrades
    from argparse import ArgumentParser
    parser = ArgumentParser(description=script_description)
    add_argument = parser.add_argument
    pass

from pdb import set_trace
from webapp import server
from core.sherlock import indexer, backends
from core.utils import resolve_path
from core.sherlock import db
import tests
import settings
import os

def get_app_args():
    """Returns the application arguments from stdin
    @return Object optparse.Values or argparse.Namespace
    """
    arguments = parser.parse_args()
    if isinstance(arguments, tuple):
        # assume its optparse return value
        (opts, args) = arguments
        return opts
    return arguments
    
    
def run():
    add_argument("--test", dest="run_tests",
                    action='store_true',
                      help="Run tests to ensure everything works correctly.")
    add_argument("--stats", dest="show_stats",
                    action='store_true',
                      help="Show sherlock statistics.")
    add_argument('--runserver', dest='run_server',
                 action='store_true',
                    help='Run the Sherlock web server.')
    # not available, yet
#    add_argument("-q", "--quiet",
#                      action="store_false", dest="verbose", default=True,
#                      help="Don't print status messages to stdout.")
    add_argument("--index", dest="reindex",
                    action='store',
                      help="Indexes the in the path specified by settings.INDEX_PATH. "\
                            "Use `update` (default) or `rebuild` to replace the entire index.")
    options = get_app_args()

    # determine app action
    if options.run_tests:
        tests.run_all()
    elif options.show_stats:
        # backend stats
        print 'Available indexer backends: %s' % backends.indexer_names()
        print 'Available searcher backends: %s' % backends.searcher_names()
        print 'Current backend: %s' % settings.DEFAULT_SEARCHER
        # indexer stats
        idxr = indexer.get_indexer()
        print 'Total documents indexed: %d' % idxr.doc_count()
        # database stats
        print 'Index Database: %s' % db.DATABASE_PATH
    elif options.run_server:
        print 'Backend: %s' % settings.DEFAULT_SEARCHER
        print 'Server: %s' % settings.SERVER_TYPE
        # launch web server
        server.run()
    elif options.reindex:
        path = resolve_path(settings.INDEX_PATH)
        # check path
        if not path.endswith('/'):
            raise Exception('INDEX_PATH must end with a trailing slash. %s' % path)
        if not os.path.exists(path):
            raise Exception('Check INDEX_PATH. Does it exist? %s' % path)
        print 'Indexing path: %s' % path
        indexer.index_path(path)
    else:
        print 'Use -h to see options.'
    pass
    

if __name__ == '__main__':
    print 'sherlock started'
    run()
    print 'sherlock done.'