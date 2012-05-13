# setup test env
import test_indexer
import test_searcher
import test_transformer
import logging
import os
import settings
import sys


# setup logger
sherlock_logger = logging.getLogger('core.sherlock')
sherlock_logger.setLevel(logging.DEBUG)
filename = 'sherlock.tests.log.txt'
hdlr = None
if settings.LOG_PATH:
    hdlr = logging.FileHandler(os.path.join(settings.LOG_PATH, filename, __name__))
else:
    hdlr = logging.StreamHandler(sys.__stdout__)
if hdlr:
    sherlock_logger.addHandler(hdlr)


def run_all():
    """Runs all unit tests
    """
    test_indexer.run()
    test_searcher.run()
    #test_transformer.run()
    pass