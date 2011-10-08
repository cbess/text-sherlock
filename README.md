# Text Sherlock (or Sherlock or TS)

Provides an easy to install and use search engine for text, but mostly for source code. [OpenGrok](http://hub.opensolaris.org/bin/view/Project+opengrok/) requires to much time to install (though it may be worth it for some). Sherlock will give you a much easier setup, a text indexer, and a web app interface for searching.

## Basic Setup

Instructions:

1. Download and place the sherlock source code in the desired (install) directory. This will be where sherlock lives.
1. Run one of the setup scripts in `/setup` to download core packages.
1. Update `settings.py`. It provides adequate documentation for each setting.
1. Run `main.py --index-path` to index target directory/content. Watch indexing output.
1. Run `main.py --run-webapp` to startup the web service.
1. Go to `http://localhost:5000` to access the web interface. Uses the [twitter bootstrap](http://twitter.github.com/bootstrap) for its UI.

---

Includes:

- Settings/Configuration
	- See `settings.py`
- Setup scripts (read contents of script for more information)
	- Run `manual-setup.sh` to perform an in directory install. Easiest setup.
	- Run `virtualenv-setup.sh` to perform an isolated installation. Preferred setup.
- Main controller script 
	- Run `main.py -h` for more information.
- End-to-end interface
	- Indexing and searching text (source code). Built-in support for [whoosh](http://packages.python.org/Whoosh) or [xapian](http://xapian.org/).
	    - Easily extend indexing or searching via custom backends.
	- Front end web app using [flask](http://flask.pocoo.org).
	- Settings and configuration using [Python](http://python.org).

### Web Interface

![screenshot](https://github.com/cbess/text-sherlock/raw/master/setup/web-example1.jpg)

![screenshot](https://github.com/cbess/text-sherlock/raw/master/setup/web-example2.jpg)

## Using other backends

settings.py

- Change the `DEFAULT_INDEXER` and `DEFAULT_SEARCHER` values to match the name given to the backend.
    - Available backends:
        - `whoosh` the default, no extra work needed.
        - `xapian` must be installed separately using the included `setup/install-xapian.sh` setup script.


## Core packages

**Requires Python 2.5 or later.**

* Whoosh - [whoosh](http://packages.python.org/Whoosh/quickstart.html#a-quick-introduction)
* Flask - [flask](http://flask.pocoo.org)
* Jinja2 - [jinja2](http://jinja.pocoo.org/docs)
* Pygments - [pygments](http://pygments.org/docs/quickstart)
* peewee - [peewee](https://github.com/coleifer/peewee) *(not used, yet)*
* Twitter Bootstrap - [twitter bootstrap](http://twitter.github.com/bootstrap)

## Other References

* http://twitter.github.com/bootstrap/examples/container-app.html
* http://pygments.org/
* http://charlesleifer.com/docs/peewee/

## Project Goals

1. Provide an easy to setup and adequate text search engine solution.
1. Be a respectable alternative to [OpenGrok](http://hub.opensolaris.org/bin/view/Project+opengrok/).
1. Influence the authors of [OpenGrok](http://hub.opensolaris.org/bin/view/Project+opengrok/) to provide a simpler setup process. 
	- I successfully setup two installations on CentOS and Ubuntu 11.x and each time it took more than two hours. TS setup takes less than 10 minutes (excluding package download time).