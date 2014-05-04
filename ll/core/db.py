from pymongo import MongoClient

class CoreDatabase(object):
    def __init__(self):
        self.db = None
    
    def __getattr__(self, name):
        return self.db.__getattr__(name)

    def init_db(self, db_name, user=None, password=None):
        if self.db == None:
            client = MongoClient()
            self.db = client[db_name]
            if user or password:
                self.db.authenticate(user, password)

db = CoreDatabase()
