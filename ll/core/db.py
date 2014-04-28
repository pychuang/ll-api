from pymongo import MongoClient

class CoreDatabase(object):
    def __init__(self):
        self.db = None
    
    def __getattr__(self, name):
        return self.db.__getattr__(name)

    def init_db(self, db_name, *args, **kwargs):
        if self.db == None:
            client = MongoClient(*args, **kwargs)
            self.db = client[db_name]

db = CoreDatabase()
