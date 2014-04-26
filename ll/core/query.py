import random
import string
import datetime
from db import db
collection = db.queries

def add_query(user, qid, qstr):
    if collection.find({"user": user, "qid": qid}).count():
        return False
    query = collection.insert({
        "user" : user,
        "qid" : qid,
        "qstr" : qstr,
        "creation_time": datetime.datetime.now(), 
    }) 
    return query

def get_query(user, qid=None):
    if qid:
        return collection.find({"user": user, "qid": qid})
    else:
        return collection.find({"user": user})

if __name__ == '__main__':
    for query in collection.find():
        print query
