# encoding: utf-8

import codecs
# try ipython first, fallback to standard pdb
try:
    from ipdb import set_trace
    debug = set_trace
except ImportError:
    from pdb import set_trace
    debug = set_trace
    pass


def read_file(path, encoding='utf-8'):
    """Reads the file at the target path.
    """
    with codecs.open(path, "r", encoding=encoding) as f:
        contents = f.read()
    return contents
    