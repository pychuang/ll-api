import random
import string
import datetime
import site
from db import db

def add_query(site_id, site_qid, qstr):
    query = db.query.find_one({"site_id": site_id, "site_qid": site_qid})
    if query:
        query["qstr"] = qstr
        query["creation_time"] = datetime.datetime.now()
        db.query.save(query)
        return query
    query = {
        "_id" : site.next_qid(site_id),
        "site_id" : site_id,
        "site_qid" : site_qid,
        "qstr" : qstr,
        "creation_time": datetime.datetime.now(), 
    }
    db.query.insert(query)
    return query

def get_query(site_id=None, qid=None):
    q = {}
    if site_id:
        q["site_id"] = site_id
    if qid:
        q["_id"] = qid
    return db.query.find(q)

if __name__ == '__main__':
    for query in db.query.find():
        print query
