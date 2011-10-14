# http://werkzeug.pocoo.org/docs/serving/#werkzeug.serving.run_simple
from flask import Flask
from core import settings as core_settings
import webapp.settings

app = Flask('webapp')
app.config.from_object('webapp.settings')

import views


def get_server_type():
    stype = core_settings.SERVER_TYPE
    if not stype:
        return 'flask/werkzeug (built-in)'
    return stype

def run():
    """Runs the flask server
    """
    server_type = core_settings.SERVER_TYPE
    if server_type == 'cherrypy':
        # near-production level server (small to medium traffic)
        import server_cherrypy
        server_cherrypy.run()
    else: # default server (flask/werkzeug)
        # dev or low traffic
        app.run(
            host=core_settings.SERVER_ADDRESS,
            port=core_settings.SERVER_PORT,
            debug=core_settings.DEBUG,
            # support multi-thread requests outside of DEBUG mode
            threaded=core_settings.SERVER_IS_THREADED,
            processes=core_settings.SERVER_PROCESSES
        )
    pass