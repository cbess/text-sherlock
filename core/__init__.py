# import packages here to help support the two available setups
__all__ = [
    'whoosh', 'flask',
    'pygments', 'settings',
    'cherrypy_wsgiserver', 'peewee',
    'FULL_INDEXES_PATH', 'FORCE_INDEX_REBUILD',
    'FULL_INDEX_PATH'
]
import sys
import whoosh
import flask
import pygments
import settings
from cherrypy import wsgiserver as cherrypy_wsgiserver
import peewee
import utils

# determine actual index name
force_rebuild = False
if '--test' in sys.argv:
    settings.DEFAULT_INDEX_NAME = 'test'
    force_rebuild = True

if '--index' in sys.argv and 'rebuild' in sys.argv:
    force_rebuild = True

# build the full path
FULL_INDEX_PATH = utils.resolve_path(settings.INDEX_PATH)
FULL_INDEXES_PATH = utils.resolve_path(settings.INDEXES_PATH)

# force index rebuilding
FORCE_INDEX_REBUILD = force_rebuild