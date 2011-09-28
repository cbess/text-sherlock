# Source Sherlock (or Sherlock or S2)

## Core packages

**Requires Python 2.5 or later.**

* Flask - [flask](http://flask.pocoo.org)
* Jinja2 - [jinja2](http://jinja.pocoo.org/docs)
* Whoosh - [whoosh](http://packages.python.org/Whoosh/quickstart.html#a-quick-introduction)
* Flask-peewee - [flask-peewee](https://github.com/coleifer/flask-peewee)
* Twitter Bootstrap - [twitter bootstrap](http://twitter.github.com/bootstrap)
* Pygments - [pygments](http://pygments.org/docs/quickstart)

## References

* http://twitter.github.com/bootstrap/examples/container-app.html
* http://pygments.org/
* http://charlesleifer.com/docs/peewee/

## Prototypes

### Index

Code:

	import sherlock

    # index the directory for code
    path = '/a/path/here/'
    indexer = sherlock.indexer.get_indexer(name='main')
    result = indexer.index_text(path, recursive=True)

  
### Search

Code:

    import sherlock

    # search and output results in html
    indexer = sherlock.indexer.get_indexer()
    index = indexer.index()
    result = index.search('int great')
    html = sherlock.transformer.result_to_html(result, template='some-results-template.tpl')
    webapp.response(html)
