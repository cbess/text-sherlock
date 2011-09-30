""" 
transformer.py
Created by: Christopher Bess
Copyright: 2011
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
        @param sherlock.Result result
        """
        self._result = result
        pass
        
    def html(self, result=None):
        """Transforms the internal or specified result object to HTML
        """
        if not result:
            result = self._result
        assert result is not None
        return self.to_html(result.context, result.filename)

    def to_html(self, text, filename):
        """Returns the HTML for the given text, highlighting it based on the
        specified filename (file type)
        """
        lexer = get_lexer_for_filename(filename)
        formatter = HtmlFormatter(linenos=False, cssclass="source")
        html = highlight(text, lexer, formatter)
        return html
        
    def transform_results(self, results, type='html'):
        """Returns a sequence of syntax hightlighted items
        @param string type: The type of transform to perform.
            possible values: html (that's it for now) or None
        """
        items = []
        for result in results:
            item = Item()
            item.context = result.context
            if type is not None:
                item.html = self.html(result)
            else:
                item.html = result.context
            item.result = result
            items.append(item)
            pass
        return items


class Item(object):
    """Represents a transformed item result
    """
    pass
