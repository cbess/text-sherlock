""" 
base.py
Created by: Christopher Bess
Copyright: 2011
"""

## Indexer Base Classes

class FileIndexer(object):
    """Represents the base file indexer object. All methods are required to be implemented.
    """
    def __init__(self, *args, **kwargs):
        pass

    def doc_count(self):
        """Returns the total document count
        """
        raise NotImplemented

    def open_index(self, path, *args, **kwargs):
        """Opens the index at the specified path
        """
        raise NotImplemented

    def create_index(self, path, *args, **kwargs):
        """Creates the index at the specified path
        """
        raise NotImplemented

    def index_file(self, filepath, *args, **kwargs):
        """Indexes and stores the file at the specified path
        """
        raise NotImplemented

    def index_exists(self, path):
        """Returns True if an index exist at the specified path, False otherwise
        """
        raise NotImplemented

    
## Searcher Base Classes

class FileSearcher(object):
    def __init__(self):
        pass


class SearchResult(object):
    pass


class SearchResults(object):
    pass
