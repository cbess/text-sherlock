# import packages here to help support the two available setups
__all__ = [
    'whoosh', 'flask',
    'pygments', 'settings',
    'cherrypy_wsgiserver', 'peewee',
    'flaskext',
    # settings
    'FULL_INDEXES_PATH', 'FORCE_INDEX_REBUILD',
    'FULL_INDEX_PATH'
]
import sys
import whoosh
import flask
import pygments
import settings
import peewee
import utils
import flaskext


def get_version_info(module):
    """Returns the version information for the target core module
    :return: string
    """
    module = module.lower()
    if module == 'cherrypy':
        import cherrypy
        return cherrypy.__version__
    elif module == 'whoosh':
        return whoosh.versionstring()
    elif module == 'pygments':
        return pygments.__version__
    elif module == 'flask':
        return flask.__version__
    elif module == 'sherlock':
        import sherlock
        return sherlock.__version__
    return '0.0'


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