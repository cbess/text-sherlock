import os

# `%(sherlock_dirs)s` resolves to the directory where sherlock is installed.

# A value indicating whether the app runs in debug mode.
# type: boolean
# default: True (set to False for production or in untrusted environments use)
DEBUG = True

# Should not be changed, this is the absolute path to the directory
# containing main.py, core/, etc.
# type: string
# default: os.path.abspath('.')
ROOT_DIR = os.path.abspath('.')

# An absolute path to the directory that will store all indexes
# for the search engine. Must have trailing slash.
# type: string
# default: '%(sherlock_dir)s/data/indexes/'
INDEXES_PATH = '%(sherlock_dir)s/data/indexes/'

# True if the target path will be indexed recursively (includes sub directories).
# type: boolean
# default: True
INDEX_RECURSIVE = True

# An absolute path to the directory path that will store the logs.
# Set to an empty string to disable logging.
# type: string
# default: ''
LOG_PATH = ''

# New line character value, may be '\n' or '\r\n'.
# type: character|string
# default: '\n'
NEW_LINE = '\n'

# During the indexing all items with the given suffix will be exclude from the index.
# Only checks filenames, for now.
# type: tuple
# default: None
EXCLUDE_FILE_SUFFIX = None

# The opposite of EXCLUDE_FILE_SUFFIX. This **only** includes files that match a given suffix.
# type: tuple
# default: None
INCLUDE_FILE_SUFFIX = None

# Number of lines used when displaying the results
# context per hit. This needs to be one (1) or greater.
# type: integer
# default: 1
NUM_CONTEXT_LINES = 1

# The absolute path to index when the indexing is performed.
# This is the index that has the original text to be indexed. This is also used when displaying
# the actual document from the search results. Must have trailing slash.
# The user running the app must have read access to the path.
# type: string
# default: '%(sherlock_dir)s/tests/text/'
INDEX_PATH = '%(sherlock_dir)s/tests/text/'

# The default index name that is used. This is an index created within the INDEXES_PATH.
# type: string
# default: 'main'
DEFAULT_INDEX_NAME = 'main'

# The name of the server type to use as the web server.
# CherryPy support is built-in, if production: 'cherrypy'.
# type: string
# default: None
SERVER_TYPE = None

# The local port to expose the web server.
# type: integer
# default: 7777
SERVER_PORT = 7777

# The local address to access the web server (the host name to listen on).
# Use '0.0.0.0' to make it available externally.
# type: string
# default: '127.0.0.1' or 'localhost'
SERVER_ADDRESS = '127.0.0.1'

# Default number of results per page.
# type: integer
# default: 10
RESULTS_PER_PAGE = 10

# Default number of sub results shown in each search result.
# type: integer
# default: 3
MAX_SUB_RESULTS = 3

# Default file indexer and searcher. Available indexers: whoosh and xapian
# They can be set to different values only if the two backends are compatible with each other.
# type: string
# default: 'whoosh'
DEFAULT_SEARCHER = DEFAULT_INDEXER = 'whoosh'

# Allows the indexer to ignore errors produced during file indexing. For example:
# any unicode or file read errors, it will skip indexing those files.
# Backends are not required to support this setting. Built-in backends (whoosh and xapian)
# honor this setting.
# default: not Debug (opposite of Debug value) = False
IGNORE_INDEXER_ERRORS = False

# The tag used to wrap the matched term in the search results. The first index is placed
# in the front of the matched term and the second index goes after the matched term.
# type: tuple
# default: ("<span class='match'>", "</span>")
MATCHED_TERM_WRAP = ("<span class='match'>", "</span>")

# The banner text displayed in the header of each page.
# type: string/html
# default: 'Sherlock Search'
SITE_BANNER_TEXT = 'Sherlock Search'

# The site title text (displayed in browser tab or title bar of window).
# This is appended to each auto-generated page title.
# type: string
# default: 'Text Sherlock'
SITE_TITLE = 'Text Sherlock'


# Customzie the settings per installation
try:
    # Try to import local settings, which override the above settings.
    # In local_settings.py (in this directory), set the values for any settings
    # you want to override.
    from local_settings import *
except ImportError:
    print 'No local_settings.py found. Using all default settings.'
    pass
