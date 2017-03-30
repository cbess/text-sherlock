# Text Sherlock (or Sherlock or TS)

Provides a fast, easy to install and use search engine for text but, mostly for source code. [OpenGrok](https://github.com/OpenGrok/OpenGrok) requires too much time to install (though it may be worth it for some). Sherlock will give you a much easier setup, a text indexer, and a web app interface for searching.

## Basic Setup

Instructions:

1. Download [sherlock](https://github.com/cbess/text-sherlock) source from [GitHub](https://github.com/cbess/text-sherlock).
1. Extract/place the sherlock source code in the desired (install) directory. This will be where sherlock lives.
1. Run `sh setup/virtualenv-setup.sh` to setup an isolated environment and download core packages.
1. Configure settings. The defaults in [`settings.py`](settings.py) provide documentation for each setting.
	- Copy [`example.local_settings.yml`](example.local_settings.yml) to `local_settings.yml`.
	- Override/copy any setting from [`settings.py`](settings.py) to `local_settings.yml` (change the values as needed). All YAML keys/options must be lowercase.
1. Run `source sherlock_env/bin/activate` to enter the virtual environment.
1. Run `python main.py --index update` or `--index rebuild` to index the path specified in the settings. Watch indexing output.
1. Run `python main.py --runserver` to start the web server.
1. Go to `http://localhost:7777` to access the web interface. Uses the [twitter bootstrap](http://getbootstrap.com/) for its UI.

You may need to install some packages before a *Ubuntu* installation will run without error.

- Install curl: `sudo apt-get install curl`
- Install uuid libs: `sudo apt-get install uuid-dev`
- Install python dev: `sudo apt-get install python-dev`

---

Includes:

- Settings/Configuration
	- See [`settings.py`](settings.py) for details.
- Setup script (read contents of script for more information)
	- Run [`virtualenv-setup.sh`](setup/virtualenv-setup.sh) to perform an isolated installation.
- Main controller script
	- Run `main.py -h` for more information.
- End-to-end interface
	- Indexing and searching text (source code). Built-in support for [whoosh](https://whoosh.readthedocs.io) (fast searching) or [xapian](http://xapian.org/) (much faster searching).
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

In [`settings.py`](settings.py):

- Change the `default_indexer` and `default_searcher` values to match the name given to the backend.
    - Possible values:
        - `whoosh` the default, no extra work needed.
        - `xapian` must be installed separately using the included [`setup/install-xapian.sh`](setup/install-xapian.sh) setup script.

## Using other web servers

Text Sherlock has built-in support for [werkzeug](http://werkzeug.pocoo.org/) and [cherrypy](http://www.cherrypy.org/) WSGI compliant servers.

In [`settings.py`](settings.py):

- Change the `server_type` value to one of the available server types.
    - Possible values:
        - `default`, werkzeug web server (default).
        - `cherrypy`, production ready web server.

## Core packages

**Requires Python 2.6/3+**

* Whoosh - [whoosh](https://whoosh.readthedocs.io/en/latest/quickstart.html#a-quick-introduction)
* Flask - [flask](http://flask.pocoo.org)
* Jinja2 - [jinja2](http://jinja.pocoo.org/docs)
* Pygments - [pygments](http://pygments.org/docs/quickstart)
* peewee - [peewee](https://github.com/coleifer/peewee)
* Twitter Bootstrap v2.x - [twitter bootstrap](http://getbootstrap.com/2.3.2/)
* PyYAML - [pyyaml](http://pyyaml.org)

## Other References

* http://twitter.github.com/bootstrap/examples/container-app.html
* http://pygments.org/
* http://docs.peewee-orm.com/
* http://www.cherrypy.org/
* http://xapian.org/
* http://pyyaml.org/wiki/PyYAMLDocumentation

## Project Goals

1. Provide an easy to setup, fast, and adequate text search engine solution.
1. Be a respectable alternative to [OpenGrok](https://github.com/OpenGrok/OpenGrok).
1. Influence the authors of [OpenGrok](https://github.com/OpenGrok/OpenGrok) to provide a simpler setup process.
	- I successfully setup two installations on CentOS and Ubuntu 11.x and each time it took more than two hours. TS setup takes less than 10 minutes (excluding package download time).

## Contributors

- [Christopher Bess](https://github.com/cbess)
- [Raphael Boidol](https://github.com/boidolr)
- [And others](https://github.com/cbess/text-sherlock/contributors)...
