from db import db
import doc


def add_feedback(site_id, sid, feedback):
    existing_feedback = db.feedback.find_one({"site_id": site_id, "sid": sid})
    if existing_feedback == None:
        raise Exception("Session not found: sid = '%s'." % sid)
    for doc in feedback["doclist"]:
        doc_found = doc.get_doc(site_id=site_id, site_docid=doc["site_docid"])
        if not doc_found:
            raise Exception("Document not found: site_docid = '%s'. Please"
                            "only provide feedback for documents that are"
                            "allowed for a query." % doc["site_docid"])
        doc["docid"] = doc_found["_id"]
    for k in feedback:
        existing_feedback[k] = feedback[k]
    db.feedback.save(existing_feedback)
    return feedback


def get_feedback(participant_id=None, site_id=None, sid=None):
    q = {}
    if participant_id:
        q["participant_id"] = site_id
    if site_id:
        q["site_id"] = site_id
    if sid:
        q["sid"] = qid
    feedback = db.feedback.find_one(q)
    if not feedback:
        raise Exception("Feedback not found:  sid = '%s'" % site_qid)
    return feedback
