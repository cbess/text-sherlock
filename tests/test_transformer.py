#!/usr/bin/env python
# encoding: utf-8
"""
test_transformer.py
Created by Christopher Bess
"""
from __future__ import absolute_import
from __future__ import unicode_literals

import os
from . import testcase
from core.sherlock import indexer, searcher, transformer
from core.utils import debug


class TestTransformer(testcase.BaseTestCase):
    def setUp(self):
        """ Called before each test """
        testcase.BaseTestCase.setUp(self)

    def tearDown(self):
        """ Called after each test """

    def _test_html_transform(self):
        """Tests the HTML transform operation
        """
        # index a file for the search
        path = os.path.join(self.test_dir, 'text/objc_example.m')
        idxr = indexer.get_indexer(name='test', rebuild_index=True)
        idxr.index_text(path)
        idx = idxr.get_index()
        # find something in the file
        results = idx.search('nsstring')
        self.assertTrue(len(results) == 1, 'bad results count')
        result = results[0]
        # transform the results
        trns = transformer.Transformer()
        items = trns.transform_results(results)
        self.assertTrue(len(items) == 1, 'no transformed items')
        html = items[0].html
        # debug()
        self.assertTrue(len(html) > 0, 'no HTML returned')


def run():
    return testcase.run_all(TestTransformer)
