#!/usr/bin/env python
# encoding: utf-8
"""
test_indexer.py
"""

import os
import testcase
from core.sherlock import indexer


class TestIndexer(testcase.BaseTestCase):
    def setUp(self):
        """ Called before each test """
        testcase.BaseTestCase.setUp(self)
        pass

    def tearDown(self):
        """ Called after each test """
        pass

    def test_indexer_creation(self):
        """Test indexer creation logic
        """
        # the below call provides and sets up a default indexer environment
        # based on the settings.py script values
        # the index name (usually 'main') has been overriden for testing
        idx = indexer.get_indexer(name='test', rebuild_index=True)
        # test values
        self.assertFalse(idx is None, 'unable to create an indexer')
        pass
        
    def test_index_file(self):
        """Tests file indexing logic
        """
        path = os.path.join(self.test_dir, 'text/objc_example.m')
        idx = indexer.get_indexer(name='test', rebuild_index=True)
        idx.index_text(path)
        # test values
        self.assertTrue(idx.doc_count() == 1, 'bad doc count')
        pass
        
    def test_index_directory(self):
        """Tests directory content indexing logic
        """
        path = os.path.join(self.test_dir, 'text')
        idx = indexer.get_indexer(name='test', rebuild_index=True)
        idx.index_text(path)
        # test values
        self.assertTrue(idx.doc_count() == 7, 'bad doc count, expected 7 but, indexed %d' % idx.doc_count())
        pass

    def test_doc_indexing(self):
        """Tests document indexing
        """
        path = os.path.join(self.test_dir, 'docs')
        idx = indexer.get_indexer(name='test', rebuild_index=True)
        idx.index_text(path)
        # test values
        self.assertTrue(idx.doc_count() == 2, 'bad doc count, expected 2 but, indexed %d' % idx.doc_count())
        pass
        

def run():
    testcase.run_all(TestIndexer)
    pass
