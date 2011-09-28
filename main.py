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
from core import sherlock
import tests


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
    add_argument('-t', "--test", dest="run_tests",
                      help="run tests to ensure everything works correctly.")
    add_argument('-r', '--run-webapp', dest='run_webapp',
                    help='run the Source Sherlock webapp')
    add_argument("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")
    options = get_app_args()

    # determine app action
    if options.run_tests == 'all':
        tests.run_all()
    elif options.run_webapp != '':
        server.app.run()
    pass
    

if __name__ == '__main__':
    print 'sherlock started'
    run()
    print 'sherlock done.'