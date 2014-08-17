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

from db import db
import random
import pymongo
import datetime
import site
import user

def get_ranking(site_id, site_qid):
    query = db.query.find_one({"site_id": site_id, "site_qid": site_qid})
    if query == None:
        raise LookupError("Query not found: site_qid = '%s'. Only rankings for"
                        "existing queries can be expected." % site_qid)
    run = get_next_run(query["_id"])
    sid = site.next_sid(site_id)
    feedback = {
        "_id": sid,
        "site_qid": site_qid,
        "site_id": site_id,
        "qid": query["_id"],
        "runid": run["runid"],
        "userid": run["userid"],
        "creation_time": datetime.datetime.now(),
    }
    db.feedback.save(feedback)
    run["sid"] = sid
    return run


def get_next_run(qid):
    runs = db.run.find({"qid": qid})
    if not runs.count():
        raise LookupError("No runs available for query.")
    participants = set()
    for run in runs:
        participants.add(run["userid"])
    participant = random.choice(list(participants))
    return get_run(participant, qid)


def get_run(key, qid):
    return db.run.find_one({"qid": qid, "userid": key},
                           sort=[('creation_time', pymongo.DESCENDING)])


def add_run(key, qid, runid, doclist):
    q = db.query.find_one({"_id": qid})
    if not q:
        raise Exception("Query does not exist: qid = '%s'" % qid)
    sites = user.get_sites(key)
    if not q["site_id"] in sites:
        raise Exception("First signup for site %s." % q["site_id"])

    for doc in doclist:
        doc_found = db.doc.find_one({"_id": doc["docid"]})
        if not doc_found:
            raise LookupError("Document not found: docid = '%s'. Add "
                            "only submit runs with existing documents."
                            % doc["docid"])
        doc["site_docid"] = doc_found["site_docid"]
    run = {
        "userid": key,
        "qid": qid,
        "site_qid": q["site_qid"],
        "runid": runid,
        "doclist": doclist,
        "creation_time": datetime.datetime.now(),
        }
    db.run.save(run)
    return run
