# This file is part of Living Labs Challenge, see http://living-labs.net.
#
# Living Labs Challenge is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Living Labs Challenge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Living Labs Challenge. If not, see <http://www.gnu.org/licenses/>.

import datetime
from db import db
import doc


def add_feedback(site_id, sid, feedback):
    existing_feedback = db.feedback.find_one({"site_id": site_id, "_id": sid})
    if existing_feedback is None:
        raise LookupError("Session not found: sid = '%s'." % sid)
    for doc in feedback["doclist"]:
        doc_found = db.doc.find_one({"site_id": site_id,
                                     "site_docid": doc["site_docid"]
                                     })
        if not doc_found:
            raise LookupError("Document not found: site_docid = '%s'. Please"
                            "only provide feedback for documents that are"
                            "allowed for a query." % doc["site_docid"])
        doc["docid"] = doc_found["_id"]

    for k in feedback:
        existing_feedback[k] = feedback[k]
    existing_feedback["modified_time"] = datetime.datetime.now()
    db.feedback.save(existing_feedback)
    return existing_feedback


def add_historical_feedback(site_id, site_qid, feedback):
    query = db.query.find_one({"site_id": site_id, "site_qid": site_qid})
    if query is None:
        raise LookupError("Query not found: site_qid = '%s'." % site_qid)

    for doc in feedback["doclist"]:
        doc_found = db.doc.find_one({"site_id": site_id,
                                     "site_docid": doc["site_docid"]
                                     })
        if not doc_found:
            raise LookupError("Document not found: site_docid = '%s'. Please"
                              "only provide historical feedback for documents"
                              "that are allowed for a query."
                              % doc["site_docid"])
        doc["docid"] = doc_found["_id"]


    feedback = {
        "site_id": site_id,
        "site_qid": site_qid,
        "qid": query["_id"],
        "creation_time": datetime.datetime.now(),
        "modified_time": datetime.datetime.now(),
    }

    db.historical.save(feedback)
    return feedback


def reset_feedback(userid=None, site_id=None, sid=None, qid=None):
    q = {}
    if userid:
        q["userid"] = userid
    if site_id:
        q["site_id"] = site_id
    if sid:
        q["sid"] = sid
    if qid:
        q["qid"] = qid
    db.feedback.remove(q)


def get_feedback(userid=None, site_id=None, sid=None, qid=None, runid=None):
    q = {}
    if userid:
        q["userid"] = userid
    if site_id:
        q["site_id"] = site_id
    if sid:
        q["sid"] = sid
    if qid and qid.lower() != "all":
        q["qid"] = qid
    if runid:
        q["runid"] = runid
    readyfeedback = []
    for feedback in db.feedback.find(q):
        if feedback.get("doclist") is not None:
            readyfeedback.append(feedback)
    return readyfeedback


def get_historical_feedback(userid=None, site_id=None,
                            qid=None, site_qid=None):
    q = {}
    if userid:
        q["userid"] = userid
    if site_id:
        q["site_id"] = site_id
    if site_qid:
        q["site_qid"] = site_qid
    if qid and qid.lower() != "all":
        q["qid"] = qid
    return db.historical.find(q)
