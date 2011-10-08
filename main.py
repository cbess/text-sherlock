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
import tests
import settings


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
    add_argument('--run-webapp', dest='run_webapp',
                 action='store_true',
                    help='Run the Sherlock webapp.')
    # not available, yet
#    add_argument("-q", "--quiet",
#                      action="store_false", dest="verbose", default=True,
#                      help="Don't print status messages to stdout.")
    add_argument("--index-path", dest="index_path",
                    action='store',
                      help="Indexes the files at the given path or use `default` "\
                            "to index the item(s) at settings.INDEX_PATH "\
                            "(replaces the index).")
    options = get_app_args()

    # determine app action
    if options.run_tests:
        tests.run_all()
    elif options.show_stats:
        # backend stats
        print 'Available indexer backends: %s' % backends.indexer_names()
        print 'Available searcher backends: %s' % backends.searcher_names()
        # indexer stats
        idxr = indexer.get_indexer()
        print 'Total documents indexed: %d' % idxr.doc_count()
    elif options.run_webapp:
        server.app.run(
            host=settings.SERVICE_ADDRESS,
            port=settings.SERVICE_PORT,
            debug=settings.DEBUG
        )
    elif options.index_path:
        path = options.index_path
        if path == 'default':
            path = settings.INDEX_PATH
        path = path % { 'sherlock_dir' : settings.ROOT_DIR }
        print 'Indexing path: %s' % path
        indexer.index_path(path)
    else:
        print 'Use -h to see options.'
    pass
    

if __name__ == '__main__':
    print 'sherlock started'
    run()
    print 'sherlock done.'