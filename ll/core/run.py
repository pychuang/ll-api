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
    if query is None:
        raise LookupError("Query not found: site_qid = '%s'. Only rankings "
                          "for existing queries can be expected." % site_qid)
    if "runs" not in query or not query["runs"]:
        raise LookupError("No rankings available for query: site_qid = '%s'. "
                          "Participants will have to submit runs first. "
                          "Sites should be able to handle such errors."
                          % site_qid)
    userid, runid = random.choice(query["runs"].items())
    runs = db.run.find({"runid": runid,
                           "site_qid": site_qid,
                           "userid": userid}
                          ).hint("runid_1_site_qid_1_userid_1")
    run = runs[0]
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


def add_run(key, qid, runid, doclist):
    q = db.query.find_one({"_id": qid})
    if not q:
        raise LookupError("Query does not exist: qid = '%s'" % qid)
    sites = user.get_sites(key)
    if q["site_id"] not in sites:
        raise LookupError("First sign up for site %s." % q["site_id"])
    if len(doclist) == 0:
        raise ValueError("The doclist should contain documents.")
    for doc in doclist:
        doc_found = db.doc.find_one({"_id": doc["docid"]})
        if not doc_found:
            raise LookupError("Document not found: docid = '%s'. Only submit "
                              "runs with existing documents." % doc["docid"])
        doc["site_docid"] = doc_found["site_docid"]
    run = {
        "userid": key,
        "qid": qid,
        "site_qid": q["site_qid"],
        "runid": runid,
        "doclist": doclist,
        "creation_time": datetime.datetime.now(),
        }
    db.run.remove({"runid": runid,
                   "qid": qid,
                   "userid": key})
    db.run.save(run)
    if "runs" in q:
        runs = q["runs"]
    else:
        runs = {}
    runs[key] = runid
    q["runs"] = runs
    db.query.save(q)
    return run


def get_run(key, qid):
    q = db.query.find_one({"_id": qid})
    if not q:
        raise LookupError("Query does not exist: qid = '%s'" % qid)

    if "runs" not in q or key not in q["runs"]:
        raise LookupError("No run for this query: qid = '%s'" % qid)

    run = db.run.find_one({"userid": key,
                           "qid": qid,
                           "runid": q["runs"][key]})
    return run
