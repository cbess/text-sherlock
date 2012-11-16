# settings overrides
# Make a copy of this file and rename it to `local_settings.py`
# DO NOT import `settings.py` into this script, it will cause a circular import

# A value indicating whether the app runs in debug mode.
# type: boolean
# default: True (set to False for production or in untrusted environments use)
DEBUG = False

# The opposite of EXCLUDE_FILE_SUFFIX. This **only** includes files that match a given suffix.
# type: tuple
# default: None
INCLUDE_FILE_SUFFIX = (
    '.m',
    '.c',
)

# The name of the server type to use as the web server.
# type: string
# default: None or 'cherrypy'
SERVER_TYPE = 'cherrypy'
