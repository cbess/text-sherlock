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
from core.utils import debug
import flaskext

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
        return u'<TSProject: %d:%s>' % (self.id, self.name)
    
    @classmethod
    def get_projects(cls):
        return TSProject.select().order_by(('date_added', 'DESC'))


class TSDocument(TSBaseModel):
    """Represents a project document that is stored
    """
    name = peewee.CharField(max_length=255)
    path = peewee.CharField(unique=True, help_text='The absolute path of the document.')
    file_size = peewee.FloatField(help_text='The size of the document on disk')
    file_type = peewee.CharField(help_text='The file type (usually the file ext)')
    mod_date = peewee.DateTimeField(help_text='The date it was modified on the file system.')
    date_added = peewee.DateTimeField(help_text='The date this record was added to the index.')
    # relationships
    project = peewee.ForeignKeyField(TSProject, null=False, cascade=True, related_name='documents') # ref to the project

    def __unicode__(self):
        return u'<TSDocument: %d:%s>' % (self.id, self.path)
    

def create_doc_tables():
    TSDocument.create_table(fail_silently=True)
    TSProject.create_table(fail_silently=True)
    pass
    
