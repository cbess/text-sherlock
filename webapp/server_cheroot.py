# Cheroot server add-on
# Install: pip install cheroot
# refs:
# http://stackoverflow.com/questions/4884541/cherrypy-vs-flask-werkzeug
# https://github.com/radekstepan/Flask-Skeleton-App
# http://stackoverflow.com/questions/5982638/using-cherrypy-cherryd-to-launch-multiple-flask-instances
# http://flask.pocoo.org/snippets/24/
# https://docs.cherrypy.org/projects/cheroot/en/latest/pkg/cheroot.wsgi.html
from core import WSGIPathInfoDispatcher, WSGIServer
from .server import app
from core import settings as core_settings

# setup cheroot server
server = WSGIServer(
    (core_settings.SERVER_ADDRESS, core_settings.SERVER_PORT),
    WSGIPathInfoDispatcher({'/': app}),
    server_name='text.sherlock',
    numthreads=10  # default: 10
)


def run():
    """ Run the cherrypy server """
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()


if __name__ == '__main__':
    run()
