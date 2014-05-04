import argparse
from db import db
import user

def set_site(key, short, name, url):
    if not key or not short or not name or not url:
        raise Exception("Specify key, short, name, url")
    if db.site.find_one({"_id": short}):
        raise Exception("Site with short name exists: shortname = '%s'" % short)
    u = user.get_user(key)
    u["is_participant"] = False
    u["is_site"] = True
    site = db.site.insert({
        "_id": short,
        "name": name,
        "url": url,
        "qid_counter": 0,
        "docid_counter": 0,
        "sid_counter": 0})
    u["site_id"] = site
    db.user.save(u)

def get_site(site_id):
    return db.site.find_one({"_id" : site_id})

def next_qid(site_id):
    site = get_site(site_id)
    qid = site["qid_counter"]
    site["qid_counter"] += 1
    db.site.save(site)
    return "%s-q%d" % (site["_id"], qid)

def next_docid(site_id):
    site = get_site(site_id)
    docid = site["docid_counter"]
    site["docid_counter"] += 1
    db.site.save(site)
    return "%s-d%d" % (site["_id"], docid)

def next_sid(site_id):
    site = get_site(site_id)
    sid = site["sid_counter"]
    site["sid_counter"] += 1
    db.site.save(site)
    return "%s-s%d" % (site["_id"], sid)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Living Labs Challenge's API Server")
    parser.add_argument('--key', type=str,
                        help='Make this key a site')
    args = parser.parse_args()
    if args.key:
        set_site(args.key, "U", "UvA", "uva.nl")
