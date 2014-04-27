import random
import string
import datetime
import site
from db import db
collection = db.query

def add_query(site_id, site_qid, qstr):
    query = collection.find_one({"site_id": site_id, "site_qid": site_qid})
    if query:
        query["qstr"] = qstr
        collection.save(query)
        return query
    query = {
        "_id" : site.next_qid(site_id),
        "site_id" : site_id,
        "site_qid" : site_qid,
        "qstr" : qstr,
        "creation_time": datetime.datetime.now(), 
    }
    collection.insert(query)
    return query

def get_query(site_id=None, qid=None):
    q = {}
    if site_id:
        q["site_id"] = site_id
    if qid:
        q["_id"] = qid
    return collection.find(q)

if __name__ == '__main__':
    for query in collection.find():
        print query
