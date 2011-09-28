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
        lexer = get_lexer_for_filename(result.filename)
        formatter = HtmlFormatter(linenos=False, cssclass="source")
        html = highlight(result.context, lexer, formatter)
        return html
        
    def transform_results(self, results, type='html'):
        """Returns a sequence of syntax hightlighted items
        @param string type: The type of transform to perform.
            possible values: html (that's it for now)
        """
        items = []
        for result in results:
            item = Item()
            item.html = self.html(result)
            item.context = result.context
            item.result = result
            items.append(item)
            pass
        return items


class Item(object):
    """Represents a transformed item result
    """
    pass
