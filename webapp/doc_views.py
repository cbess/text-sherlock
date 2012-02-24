# -*- coding: utf-8 -*-
# refs: http://flask.pocoo.org/docs/quickstart/#redirects-and-errors

import os
from server import app
from core.sherlock.db import TSProject, TSDocument
from core.sherlock import indexer, searcher, transformer, db
from core import settings as core_settings
from core import SherlockMeta
from flask import render_template, request, abort, Response
from flask import send_from_directory
from core import utils
from datetime import datetime
from core import peewee


def results_from_search_text(project, text, pagenum=1, isPath=False, type=None):
    """Returns the results from the search using the given text, populated with the transformed items
    """
    idx = indexer.get_project_indexer(project, writable=False).get_index()
    # find something in the index
    try:
        results = idx.search('*%s*' % text, pagenum, core_settings.RESULTS_PER_PAGE)
    except ValueError, e:
        # This assumes the value error resulted from a page count issue
        app.logger.error('Out of page bounds: %s' % e)
        return []
    # transform the results
    trns = transformer.Transformer()
    return trns.transform_results(results, type)


def add_default_response(response):
    """Adds the default response parameters to the response.
    """
    response['site_banner_text'] = core_settings.SITE_BANNER_TEXT
    response['site_title'] = core_settings.SITE_TITLE
    response['site_banner_color'] = core_settings.SITE_BANNER_COLOR
    response['last_indexed'] = SherlockMeta.get('last_indexed') or 'Never'
    if not response.get('errors'):
        response['errors'] = {}
    pass


@app.route('/docs')
def doc_index():
    """Handles index requests
    """
    projects = TSProject.get_projects()
    response = {
        "title" : u"Docs",
        "type" : 'docs',
        'projects' : tuple(projects)
    }
    add_default_response(response)
    return render_template('index.html', **response)


@app.route('/docs/search')
def doc_search():
    """Handles search requests
    """
    form = request.args
    search_text = form.get('q')
    pagenum = int(form.get('p', 1))
    proj_id = form.get('project')
    app.logger.debug('page %d, searching for: %s' % (pagenum, search_text))
    try:
        project = TSProject.get(id=proj_id)
        results = results_from_search_text(project, search_text, pagenum)
    except TSProject.DoesNotExist:
        abort(500)
    projects = TSProject.get_projects()
    
    # build response
    response = {
        'title' : search_text or 'Document Search',
        'type' : 'docs',
        'projects' : tuple(projects),
        'html_css_class' : 'search',
        'search_text' : search_text,
        'search_proj' : proj_id,
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


@app.route('/docs/manage', methods=['POST', 'GET'])
def doc_manage():
    projects = TSProject.get_projects()    
    response = {
        'title' : 'Manage Docs',
        'projects' : projects
    }
    add_default_response(response)
    
    # reused functions
    def render(resp):
        add_default_response(resp)
        return render_template('docs-manage.html', **resp)
    def render_error(errors):
        response['errors'] = errors
        return render(response)

    if request.method == 'POST':
        form = request.form
        # determine the action
        if form.get('btn_add_project'):
            proj_name = form.get('proj_add_name', '')
            # validate
            # no name
            if not proj_name.strip():
                err = {
                    "proj_add_name" : "no name"
                }
                return render_error(err)
            # try to find a project with that name
            # if projects.where(peewee.R('LOWER(name) = %s', proj_name)).exists():
            if projects.where(name=proj_name).exists():
                err = {
                   "proj_add_name" : "already exists"
                }
                return render_error(err)
            # create the project
            project = TSProject.create(
                name=proj_name,
                description='',
                date_added=datetime.now()
            )
            project.save()
            pass
        elif form.get('btn_add_file'):
            fileobj = request.files['file']
            if not fileobj:
                return render_error({'file' : 'no file'})
            # get the associated proj
            try:
                project = TSProject.get(id=form.get('proj_id'))
            except TSProject.DoesNotExist:
                return render_error({'file' : 'project does not exist'})
            result = project.add_file(fileobj)
            if not result[0]:
                return render_error({'btn_add_file' : result[1]})
        elif form.get('btn_delete_proj'):
            try:
                project = TSProject.get(id=form.get('proj_id'))
            except TSProject.DoesNotExist:
                return render_error({'btn_delete_proj' : 'project does not exist'})
            TSProject.remove_project(project)
        elif form.get('btn_delete_file'):
            docid = form.get('btn_delete_file')
            doc = TSDocument.get(id=docid)
            doc.remove()
        elif form.get('btn_index_proj'):
            try:
                project = TSProject.get(id=form.get('proj_id'))
            except TSProject.DoesNotExist:
                return render_error({'btn_delete_proj' : 'project does not exist'})
            # index the project
            indexer.index_project(project, rebuild_index=True)
        pass
    return render(response)
