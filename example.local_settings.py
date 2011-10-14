# settings overrides
# Make a copy of this file and rename it to `local_settings.py`
# DO NOT import `settings.py` into this script, it will cause a circular import

# A value indicating whether the app runs in debug mode.
# type: boolean
# default: True (set to False for production or in untrusted environments use)
DEBUG = False

# During the indexing all items with the given suffix will be exclude from the index.
# Only checks filenames, for now.
# type: tuple
# default: None
EXCLUDE_FILE_SUFFIX = (
    '.pyc',
)

# The opposite of EXCLUDE_FILE_SUFFIX. This **only** includes files that match a given suffix.
# type: tuple
# default: None
INCLUDE_FILE_SUFFIX = (
    '.m',
    '.c',
)

# Allows the indexer to ignore errors produced during file indexing. For example:
# any unicode or file read errors, it will skip indexing those files.
# Backends are not required to support this setting. Built-in backends (whoosh and xapian)
# honor this setting.
# default: not Debug (opposite of Debug value) = False
IGNORE_INDEXER_ERRORS = not DEBUG

# The name of the server type to use as the web server.
# type: string
# default: None or 'cherrypy'
SERVER_TYPE = 'cherrypy'