# Text Sherlock (or Sherlock or TS)

Provides an easy to install and use search engine for text but, mostly for source code. [OpenGrok](http://hub.opensolaris.org/bin/view/Project+opengrok/) requires to much time to install (though it may be worth it for some). Sherlock will give you a much easier setup, a text indexer, and a web app interface for searching.

## Basic Setup

Instructions:

1. Download [sherlock](https://github.com/cbess/text-sherlock) source from [GitHub](https://github.com/cbess/text-sherlock).
1. Extract/place the sherlock source code in the desired (install) directory. This will be where sherlock lives.
1. Run `setup/virtualenv-setup.sh` to setup an isolated environment and download core packages.
1. Configure settings. The defaults in `settings.py` provide documentation for each setting.
	- Copy `example.local_settings.py` to `local_settings.py`.
 	- Override/copy any setting from `settings.py` to `local_settings.py` (change the values as needed).
1. Run `source sherlock_env/bin/activate` to enter the virtual environment.
1. Run `python main.py --index update` or `--index rebuild` to index the path specified in the settings. Watch indexing output.
1. Run `python main.py --runserver` to start the web server.
1. Go to `http://localhost:7777` to access the web interface. Uses the [twitter bootstrap](http://twitter.github.com/bootstrap) for its UI.

You may need to install some packages before a *Ubuntu* installations will run without error.

- Install curl: `sudo apt-get install curl`
- Install uuid libs: `sudo apt-get install uuid-dev`
- Install python dev: `sudo apt-get install python-dev`

---

Includes:

- Settings/Configuration
	- See `settings.py` for details.
- Setup script (read contents of script for more information)
	- Run `virtualenv-setup.sh` to perform an isolated installation.
- Main controller script 
	- Run `main.py -h` for more information.
- End-to-end interface
	- Indexing and searching text (source code). Built-in support for [whoosh](http://packages.python.org/Whoosh) or [xapian](http://xapian.org/).
	    - Easily extend indexing or searching via custom backends.
	- Front end web app served using [werkzeug](http://werkzeug.pocoo.org/) or [cherrypy](http://www.cherrypy.org/).
	    - `werkzeug` is for development to small traffic.
	    - `cherrypy` is a high-speed, production ready, thread pooled, generic HTTP server.
	- Settings and configuration using [Python](http://python.org).

### Web Interface

Features:

Append to document URL.

- To highlight lines, append to URL: `&hl=3,7,12-14,21`
- To jump to a line, append to end of URL: `#line-3`

![screenshot](https://github.com/cbess/text-sherlock/raw/master/setup/web-example1.jpg)

![screenshot](https://github.com/cbess/text-sherlock/raw/master/setup/web-example2.jpg)

## Using other backends

settings.py

- Change the `DEFAULT_INDEXER` and `DEFAULT_SEARCHER` values to match the name given to the backend.
    - Possbile values:
        - `whoosh` the default, no extra work needed.
        - `xapian` must be installed separately using the included `setup/install-xapian.sh` setup script.
        
## Using other web servers

settings.py

- Text Sherlock has built-in support for [werkzeug](http://werkzeug.pocoo.org/) and [cherrypy](http://www.cherrypy.org/) WSGI compliant servers.
- Change the `SERVER_TYPE` value to one of the available server types.
    - Possible values:
        - `default`, werkzeug web server (default).
        - `cherrypy`, production ready web server.

## Core packages

**Requires Python 2.5 or later.**

* Whoosh - [whoosh](http://packages.python.org/Whoosh/quickstart.html#a-quick-introduction)
* Flask - [flask](http://flask.pocoo.org)
* Jinja2 - [jinja2](http://jinja.pocoo.org/docs)
* Pygments - [pygments](http://pygments.org/docs/quickstart)
* peewee - [peewee](https://github.com/coleifer/peewee)
* Twitter Bootstrap - [twitter bootstrap](http://twitter.github.com/bootstrap)

## Other References

* http://twitter.github.com/bootstrap/examples/container-app.html
* http://pygments.org/
* http://charlesleifer.com/docs/peewee/
* http://www.cherrypy.org/
* http://xapian.org/

## Project Goals

1. Provide an easy to setup and adequate text search engine solution.
1. Be a respectable alternative to [OpenGrok](http://hub.opensolaris.org/bin/view/Project+opengrok/).
1. Influence the authors of [OpenGrok](http://hub.opensolaris.org/bin/view/Project+opengrok/) to provide a simpler setup process. 
	- I successfully setup two installations on CentOS and Ubuntu 11.x and each time it took more than two hours. TS setup takes less than 10 minutes (excluding package download time).