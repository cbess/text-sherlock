import os
import stat  # index constants for os.stat()
import time
from datetime import datetime
from core import peewee
from core import settings
from core.utils import debug


db_path = os.path.join(settings.INDEXES_PATH % {'sherlock_dir' : settings.ROOT_DIR },
                       '%s-index.db' % settings.DEFAULT_INDEX_NAME)
print 'Index Database: '+db_path


class BaseModel(peewee.Model):
    class Meta:
        database = peewee.SqliteDatabase(db_path)


class IndexerMeta(BaseModel):
    """Represents the indexer meta data created during the indexing process.
    """
    path = peewee.CharField(unique=True, help_text='The absolute path of the item.')
    mod_date = peewee.DateTimeField(help_text='The date it was modified on the file system.')
    date_added = peewee.DateTimeField(help_text='The date this record was added to the index.')

IndexerMeta.create_table(fail_silently=True)


## Database Methods

def is_file_updated(filepath, check_file_exists=False, create=False):
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
        record = [q for q in query][0]
        # compare mod dates
        if last_mod_dt > record.mod_date:
            has_file_changed = True
    else:
        if create:
            record = IndexerMeta.create(
                path=filepath,
                mod_date=last_mod_dt,
                date_added=datetime.now()
            )
        return True, record
    return has_file_changed, record


def can_update_index(filepath, create=True):
    """Returns True if the target file should be updated or added to the index. Also, creates a DB entry if
    it can be updated.
    """
    is_updated, record = is_file_updated(filepath, create=create)
    return is_updated