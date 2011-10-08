# encoding: utf-8

# try ipython first, fallback to standard pdb
try:
    from ipdb import set_trace
    debug = set_trace
except ImportError:
    from pdb import set_trace
    debug = set_trace
    pass

import cgi
import codecs
import settings
from core.sherlock import logger as log


def read_file(path, encoding='utf-8'):
    """Reads the file at the target path.
    """
    with codecs.open(path, "r", encoding=encoding) as f:
        try:
            contents = f.read()
        except UnicodeDecodeError, e:
            # re-raise with more information
            raise Exception('%s: %s' % (e, path))
    return contents


def safe_read_file(path, ignore_errors=settings.IGNORE_INDEXER_ERRORS, encoding='utf-8'):
    """Returns the contents of the file at the specified path. Ignores any
    errors that may occur
    """
    try:
        contents = read_file(path, encoding=encoding)
    except Exception, e:
        log.error('Skipped file: %s' % path)
        if not ignore_errors:
            raise e
        return None
    return contents


def fragment_text(token, text):
    """Returns the text for the specified token.
    :param token: The token or fragment that provides the start and end pos
    of the matched search term.
    :param text: The full text that was searched. The entire contents
    of the searched document.
    """
    max_lines = settings.NUM_CONTEXT_LINES
    new_line = settings.NEW_LINE
    assert max_lines > 0
    nl = new_line
    # add the formatted token
    bText = text[:token.startchar]
    eText = text[token.endchar:]
    # encapsulate some code
    def format_token(token, text):
        """Returns the formatted token text that is inserted as apart
        of the search result context
        """
        token_text = text[token.startchar:token.endchar]
        return "[ts[[%s]]ts]" % token_text
    # get text with formatted token
    text = u''.join((bText, format_token(token, text), eText))
    # get the position up to the previous new line
    prevIdx = text.rfind(nl, 0, token.startchar)
    # get the position of the next new line
    nextIdx = text.find(nl, token.endchar)
    # should we try to get more lines
    if max_lines > 1:
        idx = prevIdx
        line = 1
        # lines before token
        while idx >= 0 and line <= max_lines:
            prevIdx = idx
            idx = text.rfind(nl, 0, prevIdx)
            line += 1
        # lines after token
        idx = nextIdx
        line = 1
        while idx >= 0 and line <= max_lines:
            nextIdx = idx + 1
            idx = text.find(nl, nextIdx)
            line += 1
    # get token and context
    if prevIdx < 0:
        prevIdx = 0
    # escape html before adding our own html for highlighting
    token_text = cgi.escape(text[prevIdx:nextIdx])
    # replace html highlighter placeholders
    token_text = token_text.replace('[ts[[', "<span class='match'>")
    token_text = token_text.replace(']]ts]', '</span>')
    # truncate text
    return token_text[:777]

