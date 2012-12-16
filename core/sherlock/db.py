# -*- coding: utf-8 -*-

"""
indexer.py
Created by Christopher Bess
Copyright 2011

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
from core.sherlock import logger

try:
    import sqlite3
except ImportError:
    from pysqlite2 import dbapi2 as sqlite3


def create_db(path=FULL_INDEXES_PATH, index=settings.DEFAULT_INDEX_NAME):
    try:
        os.makedirs(path)
    except OSError, e:
        if os.path.exists(path):
            pass  # The directory already existed.
        else:  # The directory couldn't be created.
             raise e
    db_path = os.path.join(path, '%s-index.db' % index)
    db = peewee.SqliteDatabase(db_path)
    return db, db_path

app_database, DATABASE_PATH = create_db()


class BaseModel(peewee.Model):
    class Meta:
        database = app_database


class IndexerMeta(BaseModel):
    """Represents the indexer meta data created during the indexing process."""
    path = peewee.CharField(unique=True,
                            help_text='The absolute path of the item.')
    mod_date = peewee.DateTimeField(
        help_text='The date it was modified on the file system.')
    date_added = peewee.DateTimeField(
        help_text='The date this record was added to the index.')

    def __unicode__(self):
        return u'<IndexerMeta: %d:%s>' % (self.id, self.path)

IndexerMeta.create_table(fail_silently=True)


## Database Methods

def is_file_updated(filepath, check_file_exists=False, update_db=False):
    """Determines if the target filepath is new or updated. Attempts to find the
    record by file path then compares the file stats.
    :return: tuple has_changed, db_record
    """
    has_file_changed = False
    record = None
    
    if check_file_exists:
        if not os.path.isfile(filepath):
            return has_file_changed, record

    # get file info
    try:
        file_stats = os.stat(filepath)
    except OSError:
        # file may not exist
        return has_file_changed, record
    last_mod = time.localtime(file_stats[stat.ST_MTIME])
    last_mod_dt = datetime(*last_mod[:6]) # time_struct -> datetime

    # get db record
    query = IndexerMeta.select().where(IndexerMeta.path == filepath)
    if query.exists():
        # get the one record
        record = [q for q in query][0]
        # compare mod dates
        if last_mod_dt > record.mod_date:
            # file on disk has changes after db record changed
            has_file_changed = True
        if update_db:
            record.mod_date = last_mod_dt
            record.save()
    else:
        if update_db:
            try:
                record = IndexerMeta.create(
                    path=filepath,
                    mod_date=last_mod_dt,
                    date_added=datetime.now()
                )
                return True, record
            except sqlite3.IntegrityError, e:
                # column path may not be unique
                logger.error('%s - filepath: %s' % (e, filepath))
                pass
    return has_file_changed, record


def can_update_index(filepath, update_db=True):
    """Returns True if the target file should be updated or added to the index. 
    Also, creates a DB entry if it can be updated.
    """
    is_updated, record = is_file_updated(filepath, update_db=update_db)
    return is_updated


def get_file_record(filepath):
    """Returns the database record for the target filepath.
    """
    record = IndexerMeta.select().get(IndexerMeta.path == filepath)
    return record


def file_record_exists(filepath):
    """Returns True if a record with the specified file path 
    exists in the database
    """
    return IndexerMeta.select().where(IndexerMeta.path == filepath).exists()


def get_raw_file_record(filepath):
    """Returns the raw file record, connecting to the database at a 
    lower level (without peewee).
    """
    database = sqlite3.connect(DATABASE_PATH)
    cursor = database.cursor()
    # get the results
    try:
        record = { }
        records = cursor.execute("""
        SELECT * FROM indexermeta WHERE path = ? LIMIT 1
        """, (filepath,))
        # get the record data
        col_data = records.next()
        for idx, data in enumerate(col_data):
            col = records.description[idx][0] # column name
            record[col] = col_data[idx] # column value
    except Exception, e:
        print 'Raw sql error: %s' % e
        return record
    # close the connection
    cursor.close()
    database.close()
    return record


def register_database_handlers(app):
    def connect_db():
       app_database.connect()

    def close_db(resp):
       app_database.close()
       return resp

    app.before_request(connect_db)
    app.after_request(close_db)
