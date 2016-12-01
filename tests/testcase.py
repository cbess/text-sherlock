#!/usr/bin/env python
# encoding: utf-8
"""
testcase.py

Created by Christopher Bess on 2008-05-18.
Copyright (c) 2008 Christopher Bess. All rights reserved.
"""

import unittest
import sys
import os
import time
import settings


def run_all(testCase):
    """Runs all the tests for the specified test case
    """
    suite = unittest.TestLoader().loadTestsFromTestCase(testCase)
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


class BaseTestCase(unittest.TestCase):
    """ The base class for all Sherlock test cases """

    def setUp(self):
        self.test_dir = '%s/tests' % settings.ROOT_DIR
        settings.DEFAULT_INDEX_NAME = 'test'

    def get_test_string(self):
        """
        Gets a string time tuple

        Used to ensure the text generated is 'unique'

        @return: a string of the current time
        """
        return "current time tuple: %s" % time.localtime()
