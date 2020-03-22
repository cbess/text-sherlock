"""
__init__.py
Created by: Christopher Bess
Copyright: 2011

refs:
http://docs.python.org/3/library/logging.html
"""
__version__ = '0.8.1'

import logging
logger = logging.getLogger('core.sherlock')

# import needed core modules or packages for easy access
from core import whoosh
from core import pygments
from core import flask
