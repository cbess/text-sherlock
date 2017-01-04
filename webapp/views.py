# -*- coding: utf-8 -*-
# refs: http://flask.pocoo.org/docs/quickstart/#redirects-and-errors

from __future__ import absolute_import

import os
from .server import app
from flask import render_template, request, abort, Response
from core.sherlock import indexer, searcher, transformer, db
from core import settings as core_settings
from core import SherlockMeta
from core.utils import debug, read_file
from .template_filters import register_filters

# register template filters
register_filters(app)


def results_from_search_text(text, pagenum=1, isPath=False, type=None):
    """Returns the results from the search using the given text, populated with the transformed items
    """
    idx = indexer.get_indexer(writable=False).get_index()
    # find something in the index
    if isPath:
        results = idx.search_path(text)
    else:
        try:
            results = idx.search(text, pagenum, core_settings.RESULTS_PER_PAGE)
        except ValueError as e:
            # This assumes the value error resulted from an page count issue
            app.logger.error('Out of page bounds: %s' % e)
            return []
    # transform the results
    trns = transformer.Transformer()
    return trns.transform_results(results, type)


def suggestion_from_search_text(text):
    idx = indexer.get_indexer(writable=False).get_index()
    return idx.suggestions(text)


def add_default_response(response):
    """Adds the default response parameters to the response.
    """
    response['site_banner_text'] = core_settings.SITE_BANNER_TEXT
    response['site_title'] = core_settings.SITE_TITLE
    response['site_banner_color'] = core_settings.SITE_BANNER_COLOR
    response['last_indexed'] = SherlockMeta.get('last_indexed') or 'Never'


@app.route('/')
def index():
    """Handles index requests
    """
    response = {
        "title" : u"Welcome"
    }
    add_default_response(response)
    return render_template('index.html', **response)


@app.route('/search', methods=['POST', 'GET'])
def search():
    """Handles search requests
    """
    # get form vars
    if request.method == 'POST':
        form = request.form
    else:
        form = request.args
    search_text = form.get('q')
    pagenum = int(form.get('p', 1))
    app.logger.debug('page %d, searching for: %s' % (pagenum, search_text))
    results = results_from_search_text(search_text, pagenum)
    suggestions = suggestion_from_search_text(search_text)

    # build response
    response = {
        'title' : search_text or 'Search',
        'html_css_class' : 'search',
        'search_text' : search_text,
        'suggestions' : suggestions,
        'results' : results.items,
        'total_count' : results.total_count,
        'page' : {
            'current' : pagenum,
            'previous' : results.prev_pagenum,
            'next' : results.next_pagenum,
            'count' : len(results)
        }
    }
    add_default_response(response)
    return render_template('index.html', **response)


@app.route('/document', methods=['GET'])
def document():
    """Handles document display requests
    """
    http_status = 200
    full_path = request.args.get('path')
    is_raw = (request.args.get('raw') == 'true')
    # allow `lines` or `hl` to highlight the target lines
    hl_str = request.args.get('lines') or request.args.get('hl', '')
    search_text = request.args.get('q')
    pagenum = request.args.get('p')

    # perform the text search, get wrapped results
    results = results_from_search_text(full_path, isPath=True)
    if not results:
        app.logger.error('Unable to find document: %s' % full_path)
        abort(404)
    doc = results.items[0]

    # grab contents, if file gone, then send 404 error message
    try:
        doc_contents = read_file(full_path)
    except IOError:
        app.logger.error('Document no longer exists: %s' % full_path)
        doc_contents = "Document does not exist"
        http_status = 404

    if is_raw:
        # dump the document text
        return Response(doc_contents, mimetype='text/plain')
    db_record = db.get_raw_file_record(full_path)

    if http_status == 200:
        # get syntax highlighted html
        trn = transformer.Transformer()
        doc_html = trn.to_html(doc_contents, doc.result.filename, highlight_lines=hl_str)
    else:
        doc_html = doc_contents

    # build response
    response = {
        "title" : doc.result.filename,
        'html_css_class' : 'document',
        'doc' : doc,
        'contents' : doc_html,
        'search_text' : search_text,
        'page_number' : pagenum,
        'last_modified' : db_record.get('mod_date'),
        'http_status' : http_status
    }
    add_default_response(response)
    return render_template('document.html', **response), http_status
