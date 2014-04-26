import random
import string
import datetime
from db import db
collection = db.users

def new_user(teamname, email):
    if collection.find({"teamname": teamname}).count():
        return False
    if collection.find({"email": email}).count():
        return False
    key = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16))
    collection.insert({
        "teamname" : teamname,
        "email" : email,
        "key" : key,
        "is_participant": True,
        "is_site": False,
        "creation_time": datetime.datetime.now(), 
    }) 
    return User(key)

class User(object):
    def __init__(self, key):
        user = collection.find_one({"key": key})
        if not user:
            raise Exception
        self.user = user
    
    def __repr__(self):
        return self.user

    def __str__(self):
        return str(self.user)
    
    def get(self, k):
        return self.user[k]

if __name__ == '__main__':
    key = "6s4lwl4zpzu851hs"
    print User(key)

    for user in collection.find():
        print user
