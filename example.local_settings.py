# settings overrides
# Make a copy of this file and rename it to `local_settings.py`
# DO NOT import `settings.py` into this script, it will cause a circular import

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
