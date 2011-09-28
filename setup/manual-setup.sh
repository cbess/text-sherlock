#!/bin/sh
# Created by: Christopher Bess
# this is for non virtualenv and non pip setups
# this script should be run from the setup directory (ex: /my-app/setup)

echo "Setting up core packages"

# create the default directories
mkdir ../data
mkdir ../data/indexes

# for the webapp
echo "grabbing flask"
curl -o flask.zip https://nodeload.github.com/mitsuhiko/flask/zipball/0.7.2
unzip flask.zip
cp -r mitsuhiko-flask-*/flask ../core

# flask dependency
echo "grabbing Werkzeug"
curl -o Werkzeug.tar.gz http://pypi.python.org/packages/source/W/Werkzeug/Werkzeug-0.7.1.tar.gz
tar -xvzf Werkzeug.tar.gz
cp -r Werkzeug-*/werkzeug ../core

#required for sherlock.transformer
echo "grabbing Jinja2"
curl -o jinja2.tar.gz http://pypi.python.org/packages/source/J/Jinja2/Jinja2-2.5.tar.gz
tar -xvzf jinja2.tar.gz
cp -r Jinja2*/jinja2 ../core

# required for the sherlock indexer
echo "grabbing Whoosh"
curl -o whoosh.zip http://pypi.python.org/packages/source/W/Whoosh/Whoosh-2.2.2.zip
unzip whoosh.zip
cp -r Whoosh*/src/whoosh ../core

# dependency for sherlock.transformer
echo "grabbing Pygments"
# or the latest: https://bitbucket.org/birkenfeld/pygments-main/get/default.zip
curl -o pygments.zip https://bitbucket.org/birkenfeld/pygments-main/get/1.4.zip
unzip pygments.zip
cp -r *pygments*/src/pygments ../core

echo "done grabbing source sherlock dependencies"