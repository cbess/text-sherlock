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
# default: %(sherlock_dir)s/data/indexes/
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

# New line character value, maybe '\n' or '\r\n'.
# type: character|string
# default: \n
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

# The absolute path to index when the indexing is ran with the 'default' option.
# This is the index that has the original text to be indexed. This is also used when displaying
# the actual document from the search results. Must have trailing slash.
# The user running the app must have read access to the path.
# type: string
# default: '%(sherlock_dir)s/tests/text/'
INDEX_PATH = '%(sherlock_dir)s/tests/text/'

# The local port to expose the web service.
# type: integer
# default: 7777
SERVICE_PORT = 7777

# The local address to access the web service (the host name to listen on).
# Use '0.0.0.0' to make it available externally.
# type: string
# default: '127.0.0.1' or 'localhost'
SERVICE_ADDRESS = '127.0.0.1'

# Default number of results per page
# type: integer
# default: 10
RESULTS_PER_PAGE = 10

# Default file indexer. Available indexers: whoosh and xapian
# type: string
# default: whoosh
DEFAULT_INDEXER = 'whoosh'

# Default file searcher. Available searchers: whoosh and xapian
# type: string
# default: whoosh
DEFAULT_SEARCHER = 'whoosh'


# Customzie the settings per installation
try:
    # Try to import local settings, which override the above settings.
    # In local_settings.py (in this directory), set the values for any settings
    # you want to override.
    from local_settings import *
except ImportError:
    print 'No local_settings.py found. Using all default settings.'
    pass
