# encoding: utf-8
"""
docdb.py
Created by Christopher Bess
Copyright 2012

refs:
https://github.com/coleifer/peewee/blob/master/README.rst
http://charlesleifer.com/blog/peewee-a-lightweight-python-orm/
http://charlesleifer.com/docs/flask-peewee/
"""
import os
import stat  # index constants for os.stat()
import time
from datetime import datetime
from core import peewee
from core import settings, FULL_INDEXES_PATH
from core.utils import debug, resolve_path, is_doc_allowed
import flaskext
from werkzeug import secure_filename
import shutil
try:
    import sqlite3
except ImportError:
    from pysqlite2 import dbapi2 as sqlite3


__all__ = ['TSProject', 'TSDocument', 'create_doc_tables', 'app_doc_database']


DATABASE_PATH = os.path.join(FULL_INDEXES_PATH, '%s-docs.db' % settings.DEFAULT_INDEX_NAME)
app_doc_database = peewee.SqliteDatabase(DATABASE_PATH, check_same_thread=False)


class TSBaseModel(peewee.Model):
    class Meta:
        database = app_doc_database
        
        
class TSProject(TSBaseModel):
    """Represents a project that is stored
    """
    name = peewee.CharField(unique=True)
    description = peewee.TextField(null=True)
    date_added = peewee.DateTimeField()
    
    def __unicode__(self):
        return u'%d:%s' % (self.id, self.name)
    
    @classmethod
    def get_projects(cls):
        return TSProject.select().order_by(('date_added', 'DESC'))
        
    @classmethod
    def remove_project(cls, project):
        """Removes the specified project and all its associated files"""
        # delete all the project files
        for doc in project.all_documents():
            doc.remove()
        # delete the proj folder
        if os.path.isdir(project.dirpath()):
            shutil.rmtree(project.dirpath())
        # remove the proj db record
        project.delete_instance()
        pass
        
    def dirpath(self):
        """Returns the directory path for this project"""
        return os.path.join(resolve_path(settings.PROJECT_DOC_PATH), str(self.id))
        
    def __add_zipfile_contents(self, file_obj):
        """Adds the specified zip file contents to this project"""
        # use self.__add_file(fileobj) for each applicable file in the zip
        pass    
        
    def __add_file(self, file_obj):
        """Adds the specified file to this project
        @return tuple (success = True|False, 'message')
        """
        # create the project folder `/projects/$proj_id/`, if needed
        dirpath = self.dirpath()
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)
        # build the path and check the filepath
        filename = secure_filename(file_obj.filename)
        filepath = os.path.join(dirpath, filename)
        if not is_doc_allowed(filepath):
            return (False, 'document type for `%s` is not allowed' % filename)
        if os.path.isfile(filepath):
            return (False, 'file already exists')
        # create the document record
        doc = TSDocument.create(
            name=filename,
            path=filepath,
            file_size=file_obj.content_length,
            file_type=filename[len(filename) - 3:], # last three letters of the file
            date_added=datetime.now(),
            mod_date=datetime.now(),
            indexed=False,
            project=self
        )
        doc.save()
        # save the file to disk
        file_obj.save(filepath)
        # add to indexing queue
        return (True, None)
    
    def add_file(self, file_obj):
        """Adds the specified file to this project
        """
        # debug()
        isZipFile = False
        # determine the file action
        if isZipFile:
            return self.__add_zipfile_contents(file_obj)
        return self.__add_file(file_obj)
        
    def is_indexed(self):
        """Returns True if all documents for this project have been indexed"""
        return not TSDocument.filter(project=self, indexed=False).exists()
        
    def all_documents(self):
        """Returns all documents assigned to this project
        @remark This is here mostly because a random 'sqlite3.InterfaceError' occurs when using the peewee 
        generated ForeignKeyField property
        """
        try:
            query = peewee.RawQuery(TSDocument, 'SELECT * FROM tsdocument WHERE project_id = %s' % str(self.id))
            return query.execute()
        except sqlite3.InterfaceError, e:
            print 'fetch documents error'
            debug()
            return []


class TSDocument(TSBaseModel):
    """Represents a project document that is stored
    """
    name = peewee.CharField(max_length=255)
    path = peewee.CharField(unique=True, help_text='The absolute path of the document.')
    file_size = peewee.FloatField(help_text='The size of the document on disk')
    file_type = peewee.CharField(help_text='The file type (usually the file ext)')
    mod_date = peewee.DateTimeField(help_text='The date it was modified on the file system.')
    date_added = peewee.DateTimeField(help_text='The date this record was added to the index.')
    indexed = peewee.BooleanField(help_text='True if this file has been indexed.')
    # relationships
    project = peewee.ForeignKeyField(TSProject, null=False, cascade=True, related_name='documents') # ref to the project

    def __unicode__(self):
        return u'%d:%s' % (self.id, self.path)
        
    def remove(self):
        """Removes the db record and the associated file from the file system"""
        # remove the file
        if os.path.isfile(self.path):
            os.remove(self.path)
        # remove the db record
        self.delete_instance()
        pass
    

def create_doc_tables():
    TSDocument.create_table(fail_silently=True)
    TSProject.create_table(fail_silently=True)
    pass
    
