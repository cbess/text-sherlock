# -*- coding: utf-8 -*-
import os
from server import app
from flask import render_template, request, url_for, session
from core.sherlock import indexer, searcher, transformer
from core import settings as core_settings
from core.utils import debug, read_file


def items_from_search_text(text, isPath=False, type=None):
    """Returns the result items from the search using the given text.
    """
    idxr = indexer.get_indexer()
    if isPath:
        results = idxr.get_index().search_path(text)
    else:
        # find something in the file
        results = idxr.get_index().search(text)
    # transform the results
    trns = transformer.Transformer()
    items = trns.transform_results(results, type=type)
    return items
    

@app.route('/')
def index():
    """Handles index requests
    """
    response = {
        "title" : u"Welcome"
    }
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
    items = items_from_search_text(search_text)
    # build response
    response = {
        'title' : 'Search',
        'search_text' : search_text,
        'results' : items
    }
    return render_template('index.html', **response)


@app.route('/document', methods=['GET'])
def document():
    """Handles document display requests
    """
    path_text = request.args.get('path')
    search_text = request.args.get('q')
    doc = items_from_search_text(path_text, isPath=True)
    if not doc:
        # respond with 404 error
        return None
    else:
        doc = doc[0]
    doc_contents = read_file(path_text)
    trn = transformer.Transformer()
    doc_html = trn.to_html(doc_contents, doc.result.filename)
    response = {
        "title" : doc.result.filename,
        'doc' : doc,
        'contents' : doc_html,
        'search_text' : search_text
    }
    return render_template('document.html', **response)