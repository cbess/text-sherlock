import os
# should not be changed, this is the absolute path to the directory
# containing main.py, core/, etc.
# type: string
# default: os.path.abspath('.')
ROOT_DIR = os.path.abspath('.')

# An absolute path to the directory that will store all indexes
# for the search engine
# type: string
# default: %(sherlock_dir)s/data/indexes
INDEX_PATH = '%(sherlock_dir)s/data/indexes'

# True if the target path will be indexed recursively 
# (includes sub directories)
# type: boolean
# default: True
INDEX_RECURSIVE = True

# An absolute path to the directory path that will store the logs
# Set to an empty string to disable logging
# type: string
# default: ''
LOG_PATH = ''

# new line character value, maybe '\n' or '\r\n'
# default: \n
NEW_LINE = '\n'