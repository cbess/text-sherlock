from __future__ import absolute_import
# Cherrypy server add-on
# Install: pip install cherrypy
# refs:
# http://stackoverflow.com/questions/4884541/cherrypy-vs-flask-werkzeug
# https://github.com/radekstepan/Flask-Skeleton-App
# http://stackoverflow.com/questions/5982638/using-cherrypy-cherryd-to-launch-multiple-flask-instances
# http://flask.pocoo.org/snippets/24/
# http://docs.cherrypy.org/dev/refman/wsgiserver/init.html
from core import cherrypy_wsgiserver
from .server import app
from core import settings as core_settings

# setup cherrypy server
dispatcher = cherrypy_wsgiserver.WSGIPathInfoDispatcher({ '/' : app })
server = cherrypy_wsgiserver.CherryPyWSGIServer(
    (core_settings.SERVER_ADDRESS, core_settings.SERVER_PORT), 
    dispatcher,
    server_name='text.sherlock',
    numthreads=10 # default: 10
)

def run():
    """ Run the cherrypy server """
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()

      
if __name__ == '__main__':
    run()