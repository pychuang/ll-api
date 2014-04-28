from db import db
import datetime
import site

def add_doclist(site_id, site_qid, doclist):
    query = db.query.find_one({"site_id": site_id, "site_qid": site_qid})
    if query == None:
        raise Exception("Query not found: site_qid = '%s'. Add queries before adding a doclist" % site_qid)
    store_doclist = []
    for doc in doclist:
        doc_found = get_doc(site_id=site_id, site_docid=doc["site_docid"])
        if not doc_found:
            raise Exception("Document not found: site_docid = '%s'. Add documents before adding a doclist." % doc["site_docid"])
        store_doclist.append(doc_found["_id"])

    query["doclist"] = store_doclist
    db.query.save(query)
    return get_doclist(site_id=site_id, site_qid=site_qid)

def get_doclist(site_id=None, site_qid=None, qid=None):
    q = {}
    if site_id:
        q["site_id"] = site_id
    if site_qid:
        q["site_qid"] = site_qid
    if qid:
        q["qid"] = qid
    query = db.query.find_one(q)
    if not query:
        if site_qid:
            raise Exception("Query not found:  site_qid = '%s'" % site_qid)
        else:
            raise Exception("Query not found:  qid = '%s'" % qid)
    return [db.doc.find_one({"_id": d}) for d in query["doclist"]]

def add_doc(site_id, site_docid, doc):
    existing_doc = db.doc.find_one({"site_id": site_id, "site_docid": site_docid})
    if existing_doc:
        for k in doc:
            existing_doc[k] = doc[k]
        existing_doc["creation_time"] = datetime.datetime.now()
        db.doc.save(existing_doc)
        return existing_doc
    doc["_id"] = site.next_docid(site_id)
    doc["site_id"] =  site_id
    doc["site_docid"] = site_docid
    doc["creation_time"] = datetime.datetime.now()
    db.doc.insert(doc)
    return doc

def get_doc(site_id=None, site_docid=None, docid=None):
    q = {}
    if site_id:
        q["site_id"] = site_id
    if site_docid:
        q["site_docid"] = site_docid
    if docid:
        q["docid"] = docid
    return db.doc.find_one(q)
