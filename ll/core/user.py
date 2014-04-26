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
    user = collection.insert({
        "teamname" : teamname,
        "email" : email,
        "key" : key,
        "is_participant": True,
        "is_site": False,
        "creation_time": datetime.datetime.now(), 
    }) 
    return user

def get_user(key):
     user = collection.find_one({"key": key})
     if not user:
         raise False
     return user

if __name__ == '__main__':
    key = "6s4lwl4zpzu851hs"

    for user in collection.find():
        print user
