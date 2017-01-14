# -*- coding: utf-8 -*-
"""
Created by Christopher Bess (https://github.com/cbess/text-sherlock)
Copyright 2013
"""

from __future__ import print_function
from __future__ import unicode_literals

import os
import six

# Should not be changed, this is the absolute path to the directory
# containing main.py, settings.py, core/, etc.
# type: string
# default: os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(__file__)

config = {}
from app_args import get_options
try:
    import yaml

    # Try to load local settings (given path first, then relative/local), which override the default settings.
    # In local_settings.yml, set the values for any settings you want to override.
    default_yaml_path = os.path.join(ROOT_DIR, 'local_settings.yml')
    yaml_path = get_options().config or default_yaml_path

    if not yaml_path or not os.path.isfile(yaml_path):
        if yaml_path:
            print('No config at %s' % yaml_path)
        else:
            print('No yaml config')
        print('Setup the local_settings.yml config.')

    # try to load the config
    if yaml_path and os.path.isfile(yaml_path):
        config = yaml.load(open(yaml_path, 'r'))

    if config:
        print('Loaded Sherlock config settings from %s' % yaml_path)
except ImportError:
    print('No yaml lib: pip install pyyaml')

# `%(sherlock_dir)s` resolves to the directory where sherlock is installed.

# A value indicating whether the app runs in debug mode.
# type: boolean
# default: True (set to False for production or in untrusted environments)
DEBUG = config.get('debug', True)

# An absolute path to the directory that will store all indexes
# for the search engine. Must have trailing slash.
# type: string
# default: '%(sherlock_dir)s/data/indexes/'
INDEXES_PATH = config.get('indexes_path', '%(sherlock_dir)s/data/indexes/' % {'sherlock_dir': ROOT_DIR})

# True if the target path will be indexed recursively (includes sub directories).
# type: boolean
# default: True
INDEX_RECURSIVE = config.get('index_recursive', True)

# An absolute path to the directory path that will store the logs.
# Set to an empty string to disable logging.
# type: string
# default: ''
LOG_PATH = config.get('log_path', '')

# New line character value, may be '\n' or '\r\n'.
# type: character|string
# default: '\n'
NEW_LINE = config.get('new_line', '\n')

# During the indexing all items with the given suffix will be exclude from the
# index. Only checks filenames, for now.
# type: tuple
# default: None
EXCLUDE_FILE_SUFFIX = config.get('exclude_file_suffix')

# The opposite of EXCLUDE_FILE_SUFFIX. This **only** includes files that match
# a given suffix.
# type: tuple
# default: None
INCLUDE_FILE_SUFFIX = config.get('include_file_suffix')

# Number of lines used when displaying the results
# context per hit. This needs to be one (1) or greater.
# type: integer
# default: 1
NUM_CONTEXT_LINES = config.get('num_context_lines', 1)

# The absolute path to index when the indexing is performed.
# This is the index that has the original text to be indexed. This is also used
# when displaying the actual document from the search results. Must have
# trailing slash. The user running the app must have read access to the path.
# type: string | tuple
# default: '%(sherlock_dir)s/tests/text/'
INDEX_PATHS = config.get('index_path', '%(sherlock_dir)s/tests/text/' % {'sherlock_dir': ROOT_DIR})
if isinstance(INDEX_PATHS, six.string_types):
    INDEX_PATHS = (INDEX_PATHS,)

# The default index name that is used for an index created within INDEXES_PATH.
# type: string
# default: 'main'
DEFAULT_INDEX_NAME = config.get('default_index_name', 'main')

# The name of the server type to use as the web server.
# CherryPy support is built-in, if production: 'cherrypy'.
# type: string
# default: None
SERVER_TYPE = config.get('server_type')

# The local port to expose the web server.
# type: integer
# default: 7777
SERVER_PORT = config.get('server_port', 7777)

# The local address to access the web server (the host name to listen on).
# Use '0.0.0.0' to make it available externally.
# type: string
# default: '127.0.0.1' or 'localhost'
SERVER_ADDRESS = config.get('server_address', '127.0.0.1')

# Default number of results per page.
# type: integer
# default: 10
RESULTS_PER_PAGE = config.get('results_per_page', 10)

# Default number of sub results shown in each search result.
# type: integer
# default: 3
MAX_SUB_RESULTS = config.get('max_sub_results', 3)

# Default file indexer and searcher. Available indexers: whoosh and xapian
# They can be set to different values only if the two backends are compatible
# with each other.
# type: string
# default: 'whoosh'
DEFAULT_SEARCHER = DEFAULT_INDEXER = config.get('default_indexer', 'whoosh')

# Allows the indexer to ignore errors produced during file indexing.
# For example: any unicode or file read errors, it will skip indexing those files.
# Backends are not required to support this setting.
# Built-in backends (whoosh and xapian) honor this setting.
# default: not Debug (opposite of Debug value) = False
IGNORE_INDEXER_ERRORS = not DEBUG

# The tag used to wrap the matched term in the search results. The first index
# is placed in the front of the matched term and the second index goes after
# the matched term.
# type: tuple
# default: ("<span class='match'>", "</span>")
MATCHED_TERM_WRAP = config.get('matched_term_wrap', ("<span class='match'>", "</span>"))

# The banner text displayed in the header of each page.
# type: string/html
# default: 'Sherlock Search'
SITE_BANNER_TEXT = config.get('site_banner_text', 'Sherlock Search')

# The site title text (displayed in browser tab or title bar of window).
# This is appended to each auto-generated page title.
# type: string
# default: 'Text Sherlock'
SITE_TITLE = config.get('site_title', 'Text Sherlock')

# The site banner background color.
# This banner is shown at the top of each page.
# Possible values: black, blue, skyblue, silver, orange, white
# More colors can be added to 'bg-gradients.css'
# The banner text styles must be changed in the stylesheet:
#   main.css (#top-banner #banner-text)
# type: string
# default: black
SITE_BANNER_COLOR = config.get('site_banner_color', 'black')


# Use the local_settings.yml instead, noted at the top of file
try:
    from local_settings import *
    print('!!!Deprecated local_settings.py|pyc file found: Use local_settings.yml instead.')
except ImportError:
    # ignore import error, because it's deprecated
    pass
