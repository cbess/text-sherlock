from __future__ import print_function
from __future__ import absolute_import
# setup test env
import logging
import os
import settings
import sys


# setup logger
sherlock_logger = logging.getLogger('core.sherlock')
sherlock_logger.setLevel(logging.DEBUG)
filename = 'sherlock.tests.log.txt'

if settings.LOG_PATH:
    hdlr = logging.FileHandler(os.path.join(settings.LOG_PATH, filename))
else:
    hdlr = logging.StreamHandler(sys.__stdout__)

if hdlr:
    sherlock_logger.addHandler(hdlr)


def adjust_test_settings():
    """Adjusts the settings to support the unit tests"""
    # include the file suffixes available in the '/tests/text' dir
    settings.INCLUDE_FILE_SUFFIX = (
        '.h',
        '.m',
        '.c',
        '.cpp',
        '.py',
    )


def run_all():
    """Runs all unit tests
    """
    from operator import methodcaller
    from . import test_indexer
    from . import test_searcher
    from . import test_transformer

    print('Logging to "%s"' % (settings.LOG_PATH if settings.LOG_PATH else 'stdout'))

    adjust_test_settings()
    test_results = [
        test_indexer.run(),
        test_searcher.run(),
        # no HTML transform support added to results, yet
        #test_transformer.run(),
    ]
    return all(map(methodcaller('wasSuccessful'), test_results))
