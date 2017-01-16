#!/usr/bin/env python

"""
transformer.py
Created by: Christopher Bess
Copyright: 2011

refs:
pygments/formatters/html.py
https://bitbucket.org/birkenfeld/pygments-main/src/72d5ec2c3be6/pygments/formatters/html.py
"""

import pygments
import six
from core.sherlock import logger
from pygments import highlight
from pygments.util import ClassNotFound
from pygments.lexers import get_lexer_for_filename, get_lexer_by_name
from pygments.formatters import HtmlFormatter


class Transformer(object):
    """Transform the result object to it's search result for various outputs."""
    def __init__(self, result=None):
        """Initializes this Transformer instance.

        :param result: sherlock.Result instance
        """
        self._result = result

    def get_lines(self, lines):
        """Returns the lines that were parsed out of the specified lines. Parses
        out ranges or line numbers.
        """
        if not lines:
            return []
        # convert string into lines, if needed
        if isinstance(lines, six.string_types):
            lines = lines.split(',')
        result = []
        for part in lines:
            try:
                if '-' in part:
                    nStart, nEnd = part.split('-')
                    nStart, nEnd = int(nStart), int(nEnd)
                    # prevent large ranges
                    if nEnd > 9999:
                        nEnd = 0
                    result.extend(range(nStart, nEnd + 1))
                else:
                    num = int(part)
                    result.append(num)
            except ValueError:
                pass
        return result

    def html(self, result=None):
        """Transform the internal or specified result object to HTML."""
        if not result:
            result = self._result
        assert result is not None
        return self.to_html(result.context, result.filename)

    def to_html(self, text, filename, **kwargs):
        """Return highlighted HTML for the given text, based on filename
        (file type).
        """
        # get the highlighted lines
        hl_lines = kwargs.get('highlight_lines', '')
        kwargs['hl_lines'] = self.get_lines(hl_lines)
        # get html syntax
        try:
            lexer = get_lexer_for_filename(filename)
        except ClassNotFound as e:
            logger.warn('Could not find lexer for filename=[%s], error=[%s]', filename, e)
            lexer = get_lexer_by_name('text')
        formatter = HtmlFormatter(
            linenos='table',
            cssclass='source',
            lineanchors='line',
            anchorlinenos=True,
            **kwargs
        )
        html = highlight(text, lexer, formatter)
        return html

    def transform_results(self, results, type='html'):
        """Returns a sequence of syntax hightlighted items.

        :param results: searcher.Results instance
        :param string type: The type of transform to perform.
            possible values: html (that's it for now) or None
        """
        for result in results:
            item = Item()
            item.context = result.context
            if type is not None:
                item.html = self.html(result)
            else:
                item.html = result.context
            item.result = result
            results.items.append(item)
        return results


class Item(object):
    """Represents a transformed item result."""
    def __str__(self):
        return '<transformer.Item %s>' % repr(self)
