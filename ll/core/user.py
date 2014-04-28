import random
import string
import hashlib
import datetime
from db import db

KEY_LENGTH = 32

def new_key(teamname, email):
    rstr = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(KEY_LENGTH/2))
    hstr = str(hashlib.sha1(teamname + email).hexdigest())[:KEY_LENGTH/2]
    return "-".join([hstr, rstr]).upper()

def new_user(teamname, email):
    if db.user.find({"teamname": teamname}).count():
        raise Exception("Teamname exists: teamname = '%s'" % teamname)
    if db.user.find({"email": email}).count():
        raise Exception("Email exists: email = '%s'" % email)
    #TODO: check valid email
    #TODO: send email with validation
    user = {
        "_id" : new_key(teamname, email),
        "teamname" : teamname,
        "email" : email,
        "is_participant": True,
        "is_site": False,
        "is_verified" : False,
        "creation_time": datetime.datetime.now(), 
    }
    db.user.insert(user)
    return user

def get_user(key):
     user = db.user.find_one({"_id": key})
     if not user:
         return False
     return user

if __name__ == '__main__':
    for user in db.user.find():
        print user
