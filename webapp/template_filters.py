import six
from core import LONG_DATE_FORMAT, SHORT_DATE_FORMAT
from core.utils import datetime_to_phrase
from datetime import datetime
try:
    from urllib.parse import quote_plus
except ImportError:
    # python 2
    from urllib import quote_plus


def register_filters(app):
    """Registers jinja2 template filters"""

    @app.template_filter('dt_format')
    def dt_format_filter(value, format=LONG_DATE_FORMAT):
        """Returns a string of the value formated as a date string
        :param: value date time or string '2009-11-22 01:20:07'
        """
        if not value:
            return ''
        if isinstance(value, six.string_types):
            # make datetime
            value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return value.strftime(format)


    @app.template_filter('dt_ago')
    def dt_ago_filter(value):
        """Returns the datetime as a phrase
        """
        if not value:
            return ''
        if isinstance(value, six.string_types):
            # make datetime
            value = datetime.strptime(value, SHORT_DATE_FORMAT)
        return datetime_to_phrase(value)


    @app.template_filter('urlencode')
    def urlencode_filter(value):
        """Returns the urlencoded value of the specified value
        """
        if not value:
            return ''
        return quote_plus(value, '/')
