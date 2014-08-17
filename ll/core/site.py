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

import argparse
from db import db
import user


def set_site(key, short, name, url, terms):
    if not key or not short or not name or not url:
        raise ValueError("Specify key, short, name, url")
    if db.site.find_one({"_id": short}):
        raise ValueError("Site with short name exists: shortname = '%s'"
                        % short)
    u = user.get_user(key)
    u["is_participant"] = False
    u["is_site"] = True
    site = db.site.insert({
        "_id": short,
        "name": name,
        "url": url,
        "terms": terms,
        "qid_counter": 0,
        "docid_counter": 0,
        "sid_counter": 0})
    u["site_id"] = site
    db.user.save(u)


def get_site(site_id):
    return db.site.find_one({"_id": site_id})


def get_sites():
    return db.site.find()


def next_qid(site_id):
    #TODO: make these thread save
    site = get_site(site_id)
    qid = site["qid_counter"]
    site["qid_counter"] += 1
    db.site.save(site)
    return "%s-q%d" % (site["_id"], qid)


def next_docid(site_id):
    #TODO: make these thread save
    site = get_site(site_id)
    docid = site["docid_counter"]
    site["docid_counter"] += 1
    db.site.save(site)
    return "%s-d%d" % (site["_id"], docid)


def next_sid(site_id):
    #TODO: make these thread save
    site = get_site(site_id)
    sid = site["sid_counter"]
    site["sid_counter"] += 1
    db.site.save(site)
    return "%s-s%d" % (site["_id"], sid)
