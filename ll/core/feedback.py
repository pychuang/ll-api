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
    if existing_feedback == None:
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
    return feedback


def get_feedback(userid=None, site_id=None, sid=None, qid=None):
    q = {}
    if userid:
        q["userid"] = userid
    if site_id:
        q["site_id"] = site_id
    if sid:
        q["sid"] = sid
    if qid:
        q["qid"] = qid
    readyfeedback = []
    for feedback in db.feedback.find(q):
        if feedback.get("doclist") != None:
            readyfeedback.append(feedback)
    return readyfeedback

