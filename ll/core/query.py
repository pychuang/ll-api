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

import random
import string
import datetime
import site
import user
from db import db


def add_query(site_id, site_qid, qstr, query_type, qid=None):
    query = db.query.find_one({"site_id": site_id, "site_qid": site_qid})
    if query:
        query["qstr"] = qstr
        query["type"] = query_type
        query["creation_time"] = datetime.datetime.now()
        query["deleted"] = False
        if qid is not None:
            query["_id"] = qid
        db.query.save(query)
    else:
        query = {
            "_id": site.next_qid(site_id),
            "site_id": site_id,
            "site_qid": site_qid,
            "qstr": qstr,
            "type": query_type,
            "creation_time": datetime.datetime.now(),
            "deleted": False,
        }
        if qid is not None:
            query["_id"] = qid
        db.query.insert(query)
    return query


def get_query(site_id=None, qid=None, key=None):
    q = {"deleted": {"$ne": True}}
    if key is not None:
        sites = user.get_sites(key)
        if not sites:
            raise Exception("First signup for sites.")
        q["$or"] = [{"site_id": s} for s in sites]
    if site_id:
        if key is not None and site_id not in sites:
            raise Exception("First signup for site %s." % site_id)
        q["site_id"] = site_id
    if qid is not None:
        q["_id"] = qid

    return [query for query in db.query.find(q)]  # if "doclist" in query]


def delete_query(site_id=None, qid=None):
    q = {}
    if site_id:
        q["site_id"] = site_id
    if qid:
        q["_id"] = qid

    existing_query = db.query.find_one(q)

    if existing_query:
        existing_query["deleted"] = True
        db.query.save(existing_query)
        return True
    return False
