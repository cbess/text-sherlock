#!/bin/sh
# Created by: Christopher Bess
# This is for non virtualenv and non pip setups.
# This script should be run from the setup directory (ex: /my-app/setup) using the privileges of the user
# that will run the server.
#
# Warning: This setup type is deprecated and no longer fully supported, use virtual-setup.sh instead. But, it is left here as a starting point
# for anyone who desires to utilize this type of installation.

echo "Setting up core packages"

# create the default directories
mkdir -p ../data/indexes

# for the sherlock.webapp
echo "grabbing flask"
curl -o flask.zip https://github.com/pallets/flask/archive/0.11.1.zip
unzip flask.zip
cp -r mitsuhiko-flask-*/flask ../core

# flask peewee database layer
echo "grabbing flask-peewee"
curl -o flask-peewee.tar.gz http://pypi.python.org/packages/source/f/flask-peewee/flask-peewee-0.6.7.tar.gz
tar -xvzf flask-peewee.tar.gz
cp -r flask-peewee-*/flaskext ../core

# peewee database layer
curl -o peewee.py https://raw.github.com/coleifer/peewee/master/peewee.py
cp ./peewee.py ../core

# flask web server
echo "grabbing Werkzeug"
curl -o Werkzeug.tar.gz http://pypi.python.org/packages/source/W/Werkzeug/Werkzeug-0.11.11.tar.gz
tar -xvzf Werkzeug.tar.gz
cp -r Werkzeug-*/werkzeug ../core

# cherrypy web server
echo "grabbing cherrypy"
curl -o cherrypy.zip http://download.cherrypy.org/cherrypy/8.1.2/CherryPy-8.1.2.zip
unzip cherrypy.zip
cp -r CherryPy*/py2/cherrypy ../core

# required for sherlock.webapp
echo "grabbing Jinja2"
curl -o jinja2.tar.gz http://pypi.python.org/packages/source/J/Jinja2/Jinja2-2.8.tar.gz
tar -xvzf jinja2.tar.gz
cp -r Jinja2*/jinja2 ../core

# required for the sherlock indexer
echo "grabbing Whoosh"
curl -o whoosh.zip http://pypi.python.org/packages/source/W/Whoosh/Whoosh-2.5.7.zip
unzip whoosh.zip
cp -r Whoosh*/src/whoosh ../core

# dependency for sherlock.transformer
echo "grabbing Pygments"
# or the latest: https://bitbucket.org/birkenfeld/pygments-main/get/default.zip
curl -o pygments.zip https://bitbucket.org/birkenfeld/pygments-main/get/2.1.3.zip
unzip pygments.zip
cp -r *pygments*/src/pygments ../core

echo "done grabbing source sherlock dependencies"
