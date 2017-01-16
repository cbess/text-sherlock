#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

import cgi
import codecs
from datetime import datetime
from core.sherlock import logger as log
import settings

# Try ipython first, fallback to standard pdb.
try:
    from ipdb import set_trace
    debug = set_trace
except ImportError:
    from pdb import set_trace
    debug = set_trace


def read_file(path, encoding='utf-8'):
    """Reads the file at the target path."""
    with codecs.open(path, 'r', encoding=encoding) as f:
        try:
            contents = f.read()
        except UnicodeDecodeError as e:
            # re-raise with more information
            raise Exception('%s: %s' % (e, path))
    return contents


def safe_read_file(path, ignore_errors=settings.IGNORE_INDEXER_ERRORS,
                   encoding='utf-8'):
    """Returns the contents of the file at the specified path. Ignores any
    errors that may occur."""
    try:
        contents = read_file(path, encoding=encoding)
        return contents
    except Exception as e:
        log.error('Skipped file: %s' % path)
        if not ignore_errors:
            raise e


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
    if (not isinstance(settings.MATCHED_TERM_WRAP, (tuple, list))
        # must have start and end tag elements/indexes
        or len(settings.MATCHED_TERM_WRAP) != 2):
        raise Exception(
            'Invalid matched term wrap. Please set MATCHED_TERM_WRAP setting.')
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
        return '[ts[[%s]]ts]' % token_text
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
    token_text = token_text.replace('[ts[[', settings.MATCHED_TERM_WRAP[0])
    token_text = token_text.replace(']]ts]', settings.MATCHED_TERM_WRAP[1])
    # truncate text
    return token_text[:777]


def datetime_to_phrase(date_time):
    """Converts a python datetime object to the format "X days, Y hours ago"

    @param date_time: Python datetime object

    @return:
        fancy datetime:: string

    @author:
        Copyright 2009 Jai Vikram Singh Verma (jaivikram[dot]verma[at]gmail[dot]com)
        http://code.activestate.com/recipes/576880-convert-datetime-in-python-to-user-friendly-repres/
    """
    current_datetime = datetime.now()
    delta = str(current_datetime - date_time)
    if delta.find(',') > 0:
        days, hours = delta.split(',')
        days = int(days.split()[0].strip())
        hours, minutes = hours.split(':')[0:2]
    else:
        hours, minutes = delta.split(':')[0:2]
        days = 0
    days, hours, minutes = int(days), int(hours), int(minutes)
    datelets =[]
    years, months, xdays = None, None, None
    plural = lambda x: 's' if x != 1 else ''
    if days >= 365:
        years = days // 365
        datelets.append('%d year%s' % (years, plural(years)))
        days = days % 365
    if days >= 30 and days < 365:
        months = days // 30
        datelets.append('%d month%s' % (months, plural(months)))
        days = days % 30
    if not years and days > 0 and days < 30:
        xdays = days
        datelets.append('%d day%s' % (xdays, plural(xdays)))
    if not (months or years) and hours != 0:
        datelets.append('%d hour%s' % (hours, plural(hours)))
    if not (xdays or months or years):
        datelets.append('%d minute%s' % (minutes, plural(minutes)))
    return ', '.join(datelets) + ' ago.'
