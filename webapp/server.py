# http://werkzeug.pocoo.org/docs/serving/#werkzeug.serving.run_simple
from flask import Flask
from core import settings as core_settings
import webapp.settings

app = Flask('webapp')
app.config.from_object('webapp.settings')

import views


def run():
    """Runs the flask server
    """
    app.run(
        host=core_settings.SERVER_ADDRESS,
        port=core_settings.SERVER_PORT,
        debug=core_settings.DEBUG,
        # support multi-thread requests outside of DEBUG mode
        threaded=core_settings.SERVER_IS_THREADED,
        processes=core_settings.SERVER_PROCESSES
    )
    pass