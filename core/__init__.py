#!/usr/bin/env python

from __future__ import absolute_import

# import packages here to help support the two available setups
__all__ = [
    'whoosh', 'flask',
    'pygments', 'settings',
    'cherrypy_wsgiserver', 'flaskext',
    # settings
    'FULL_INDEXES_PATH', 'FORCE_INDEX_REBUILD',
    'FULL_INDEX_PATHS'
]

from cherrypy import wsgiserver as cherrypy_wsgiserver
import codecs
import flask
import os
import peewee
import pygments
import sys
import whoosh

try:
    import configparser
except ImportError:
    # python2
    import ConfigParser as configparser
import settings
from . import utils


class SherlockMeta(object):
    """Represents the sherlock meta data that is stored."""
    config = configparser.RawConfigParser()
    config_file_path = os.path.join(settings.ROOT_DIR, 'sherlock-meta.cfg')

    @classmethod
    def set(cls, key, value):
        """Sets the meta value for the target key."""
        if not cls.config.has_section('main'):
            cls.config.add_section('main')
        cls.config.set('main', key, value)
        # write config
        with codecs.open(cls.config_file_path, 'w', encoding='utf-8') as configfile:
            cls.config.write(configfile)

    @classmethod
    def get(cls, key):
        """Returns the meta value for the target key."""
        cls.config.read(cls.config_file_path)
        if cls.config.has_section('main'):
            return cls.config.get('main', key)
        return None


def get_version_info(module):
    """Returns the version information for the target core module.
    :return: string
    """
    module = module.lower()

    def cherrypy_ver():
        import cherrypy
        return cherrypy.__version__

    def sherlock_ver():
        from . import sherlock
        return sherlock.__version__

    return {
        'cherrypy': cherrypy_ver,
        'whoosh': whoosh.versionstring,
        'pygments': lambda: pygments.__version__,
        'flask': lambda: flask.__version__,
        'sherlock': sherlock_ver,
    }.get(module, lambda: '0.0')()


# determine actual index name
force_rebuild = False
if '--test' in sys.argv:
    settings.DEFAULT_INDEX_NAME = 'test'
    force_rebuild = True

if '--index' in sys.argv and 'rebuild' in sys.argv:
    force_rebuild = True

# build the full path
FULL_INDEX_PATHS = settings.INDEX_PATHS
FULL_INDEXES_PATH = settings.INDEXES_PATH

# force index rebuilding
FORCE_INDEX_REBUILD = force_rebuild

LONG_DATE_FORMAT = '%A, %B %d, %Y %I:%M%p'
SHORT_DATE_FORMAT = '%m/%d/%Y %H:%M'
