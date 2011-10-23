# import packages here to help support the two available setups
__all__ = [
    'whoosh', 'flask',
    'pygments', 'settings',
    'cherrypy_wsgiserver', 'flaskext',
    # settings
    'FULL_INDEXES_PATH', 'FORCE_INDEX_REBUILD',
    'FULL_INDEX_PATH'
]
import os
import sys
import whoosh
import flask
import pygments
import settings
from cherrypy import wsgiserver as cherrypy_wsgiserver
import peewee
import utils
import ConfigParser


class SherlockMeta:
    """Represents the sherlock meta data that is stored.
    """
    config = ConfigParser.RawConfigParser()
    @classmethod
    def set(cls, key, value):
        """Sets the meta value for the target key
        """
        if not cls.config.has_section('main'):
            cls.config.add_section('main')
        cls.config.set('main', key, value)
        # write config
        with open(os.path.join(settings.ROOT_DIR, 'sherlock-meta.cfg'), 'wb') as configfile:
            cls.config.write(configfile)
        pass

    @classmethod
    def get(cls, key):
        """Returns the meta value for the target key
        """
        cls.config.read(os.path.join(settings.ROOT_DIR, 'sherlock-meta.cfg'))
        if not cls.config.has_section('main'):
            return None
        return cls.config.get('main', key)


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

LONG_DATE_FORMAT = '%A, %B %d, %Y %I:%M%p'
SHORT_DATE_FORMAT = '%m/%d/%Y %H:%M'
