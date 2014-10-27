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
        "sid_counter": 0,
        "enabled": False,
        "is_robot": False})
    u["site_id"] = site
    db.user.save(u)


def get_site(site_id):
    return db.site.find_one({"_id": site_id})


def get_sites():
    return db.site.find()


def next_qid(site_id):
    ret = db.site.find_and_modify({"_id": site_id},
                                  update={"$inc": {"qid_counter": 1}},
                                  new=True)
    return "%s-q%d" % (site_id, ret["qid_counter"])


def next_docid(site_id):
    ret = db.site.find_and_modify({"_id": site_id},
                                  update={"$inc": {"docid_counter": 1}},
                                  new=True)
    return "%s-d%d" % (site_id, ret["docid_counter"])


def next_sid(site_id):
    ret = db.site.find_and_modify({"_id": site_id},
                                  update={"$inc": {"sid_counter": 1}},
                                  new=True)
    return "%s-s%d" % (site_id, ret["sid_counter"])


def enable(site_id):
    site = db.site.find_one({"_id": site_id})
    site["enabled"] = True
    db.site.save(site)


def disable(site_id):
    site = db.site.find_one({"_id": site_id})
    site["enabled"] = False
    db.site.save(site)


def unset_robot(site_id):
    site = db.site.find_one({"_id": site_id})
    site["is_robot"] = False
    db.site.save(site)


def set_robot(site_id):
    site = db.site.find_one({"_id": site_id})
    site["is_robot"] = True
    db.site.save(site)
