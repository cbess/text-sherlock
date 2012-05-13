# encoding: utf-8
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

try:
    import sqlite3
except ImportError:
    from pysqlite2 import dbapi2 as sqlite3


DATABASE_PATH = os.path.join(FULL_INDEXES_PATH, '%s-index.db' % settings.DEFAULT_INDEX_NAME)
app_database = peewee.SqliteDatabase(DATABASE_PATH)


class BaseModel(peewee.Model):
    class Meta:
        database = app_database


class IndexerMeta(BaseModel):
    """Represents the indexer meta data created during the indexing process.
    """
    path = peewee.CharField(unique=True, help_text='The absolute path of the item.')
    mod_date = peewee.DateTimeField(help_text='The date it was modified on the file system.')
    date_added = peewee.DateTimeField(help_text='The date this record was added to the index.')

    def __unicode__(self):
        return u'<IndexerMeta: %d:%s>' % (self.id, self.path)

IndexerMeta.create_table(fail_silently=True)


## Database Methods

def is_file_updated(filepath, check_file_exists=False, update_db=False):
    """Determines if the target filepath is new or updated. Attempts to find the
    record by file path then compares the file stats.
    :return: tuple has_changed, db_record
    """
    if check_file_exists:
        if not os.path.isfile(filepath):
            return False

    has_file_changed = False

    # get file info
    file_stats = os.stat(filepath)
    last_mod = time.localtime(file_stats[stat.ST_MTIME])
    last_mod_dt = datetime(*last_mod[:6]) # time_struct -> datetime

    # get db record
    record = None
    query = IndexerMeta.select().where(path=filepath)
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
            record = IndexerMeta.create(
                path=filepath,
                mod_date=last_mod_dt,
                date_added=datetime.now()
            )
        return True, record
    return has_file_changed, record


def can_update_index(filepath, update_db=True):
    """Returns True if the target file should be updated or added to the index. Also, creates a DB entry if
    it can be updated.
    """
    is_updated, record = is_file_updated(filepath, update_db=update_db)
    return is_updated


def get_file_record(filepath):
    """Returns the database record for the target filepath.
    """
    record = IndexerMeta.select().get(path=filepath)
    return record


def file_record_exists(filepath):
    """Returns True if a record with the specified file path exists in the database
    """
    return IndexerMeta.select().where(path=filepath).exists()


def get_raw_file_record(filepath):
    """Returns the raw file record, connecting to the database at a lower level (without peewee).
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
