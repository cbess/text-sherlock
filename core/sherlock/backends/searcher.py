"""
searcher.py
Created by: Christopher Bess
Copyright: 2011
"""
__author__ = 'C. Bess'


from whoosh.qparser import QueryParser
# from whoosh.query import And, Term
from whoosh import highlight
from base import FileSearcher


class WhooshSearcher(FileSearcher):
    pass


class XapianSearcher(FileSearcher):
    pass