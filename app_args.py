# provides app argument parsing values

__all__ = ['get_options']

try:
    # optparse is deprecated, but I wanted broader compatibility
    from optparse import OptionParser
    parser = OptionParser(description=__doc__)
    add_argument = parser.add_option
except ImportError:
    # this is here to help any future upgrades
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    add_argument = parser.add_argument


def get_app_args():
    """Returns the application arguments from stdin
    @return Object optparse.Values or argparse.Namespace
    """
    arguments = parser.parse_args()
    if isinstance(arguments, tuple):
        # assume its optparse return value
        (opts, args) = arguments
        return opts
    return arguments
    
    
def add_app_args():
    """Add app arguments"""
    add_argument('-r', '--runserver', dest='run_server',
                 action='store_true',
                 help='Run the Sherlock web server.')
    add_argument('-c', '--config', dest='config',
                 action='store',
                 help='Sherlock config settings absolute path.')
    add_argument('-v', '--version', dest='show_version',
                 action='store_true',
                 help='Show sherlock version information.')
    # TODO: not available, yet
#    add_argument('-q', '--quiet',
#                action='store_false', dest='verbose', default=True,
#                help='Don\'t print status messages to stdout.')
    add_argument('--test', dest='run_tests',
                 action='store_true',
                 help='Run tests to ensure everything works correctly.')
    add_argument('--stats', dest='show_stats',
                 action='store_true',
                 help='Show sherlock statistics.')
    add_argument('--index', dest='reindex',
                 action='store',
                 help=('Indexes the in the path specified by '
                       'settings.INDEX_PATHS. Use `update` or '
                       '`rebuild` to replace the entire index.'))
add_app_args()


def get_options():
    """ Returns the options from the script """
    options = get_app_args()
    return options
