import random
import string
import datetime
from db import db
user_collection = db.user

def new_user(teamname, email):
    if user_collection.find({"teamname": teamname}).count():
        return False
    if user_collection.find({"email": email}).count():
        return False
    key = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16))
    while user_collection.find_one({"_id":key}):
        key = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16))
    user = {
        "_id" : key,
        "teamname" : teamname,
        "email" : email,
        "is_participant": True,
        "is_site": False,
        "creation_time": datetime.datetime.now(), 
    }
    user_collection.insert(user)
    return user

def get_user(key):
     user = user_collection.find_one({"_id": key})
     if not user:
         return False
     return user

if __name__ == '__main__':
    for user in user_collection.find():
        print user
