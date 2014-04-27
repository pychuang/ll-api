import argparse
from db import db
import user
site_collection = db.site
user_collection = db.user

def set_site(key, short, name, url):
    if site_collection.find_one({"_id": short}):
        raise Exception
    u = user.get_user(key)
    u["is_participant"] = False
    u["is_site"] = True
    site = site_collection.insert({
        "_id": short,
        "name": name,
        "url": url,
        "qid_counter": 0,
        "docid_counter": 0})
    u["site_id"] = site
    user_collection.save(u)

def get_site(site_id):
    return site_collection.find_one({"_id" : site_id})

def next_qid(site_id):
    site = get_site(site_id)
    qid = site["qid_counter"]
    site["qid_counter"] += 1
    site_collection.save(site)
    return "%s-q%d" % (site["_id"], qid)

def next_docid(site_id):
    site = get_site(site_id)
    docid = site["docid_counter"]
    site["docid_counter"] += 1
    site_collection.save(site)
    return "%s-d%d" % (site["_id"], docid)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Living Labs Challenge's API Server")
    parser.add_argument('--key', type=str,
                        help='Make this key a site')
    args = parser.parse_args()
    if args.key:
        set_site(args.key, "U", "UvA", "uva.nl")
