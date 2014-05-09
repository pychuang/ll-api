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
from db import db


def add_query(site_id, site_qid, qstr):
    query = db.query.find_one({"site_id": site_id, "site_qid": site_qid})
    if query:
        query["qstr"] = qstr
        query["creation_time"] = datetime.datetime.now()
        db.query.save(query)
        return query
    query = {
        "_id": site.next_qid(site_id),
        "site_id": site_id,
        "site_qid": site_qid,
        "qstr": qstr,
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
