""" 
__init__.py
Created by: Christopher Bess
Copyright: 2011
"""
__version__ = '0.7'

import logging
logger = logging.getLogger('core.sherlock')

# import needed core modules or packages for easy access
from core import whoosh
from core import pygments
from core import flask
from core import cherrypy_wsgiserver
from core import flaskext