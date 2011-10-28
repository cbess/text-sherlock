""" 
transformer.py
Created by: Christopher Bess
Copyright: 2011

refs:
pygments/formatters/html.py
https://bitbucket.org/birkenfeld/pygments-main/src/72d5ec2c3be6/pygments/formatters/html.py
"""

import pygments
from core.utils import debug
from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import HtmlFormatter


class Transformer(object):
    """
    This transforms the result object to it's search result for various output.
    """
    def __init__(self, result=None):
        """Initializes this Transformer instance
        :param result: sherlock.Result instance
        """
        self._result = result
        pass

    def get_lines(self, lines):
        """Returns the lines that were parsed out of the specified lines. Parses
        out ranges or line numbers
        """
        if not lines:
            return []
        # convert string into lines, if needed
        if isinstance(lines, (str, unicode)):
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
        """Transforms the internal or specified result object to HTML
        """
        if not result:
            result = self._result
        assert result is not None
        return self.to_html(result.context, result.filename)

    def to_html(self, text, filename, **kwargs):
        """Returns the HTML for the given text, highlighting it based on the
        specified filename (file type)
        """
        # get the highlighted lines
        hl_lines = kwargs.get('highlight_lines', '')
        kwargs['hl_lines'] = self.get_lines(hl_lines)
        # get html syntax
        lexer = get_lexer_for_filename(filename)
        formatter = HtmlFormatter(
            linenos='table',
            cssclass="source",
            lineanchors='line',
            anchorlinenos=True,
            **kwargs
        )
        html = highlight(text, lexer, formatter)
        return html
        
    def transform_results(self, results, type='html'):
        """Returns a sequence of syntax hightlighted items
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
            pass
        return results


class Item(object):
    """Represents a transformed item result
    """
    def __str__(self):
        return "<transformer.Item %s>" % repr(self)
