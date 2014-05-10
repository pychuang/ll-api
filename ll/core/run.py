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
import site


def get_ranking(site_id, site_qid):
    query = db.query.find_one({"site_id": site_id, "site_qid": site_qid})
    if query == None:
        raise LookupError("Query not found: site_qid = '%s'. Only rankings for"
                        "existing queries can be expected." % site_qid)
    run = get_run(site_qid)
    feedback = {
        "_id": site.next_sid(site_id),
        "site_qid": site_qid,
        "qid": query["_id"],
        "rid": run["_id"],
    }
    db.feedback.save(feedback)
    return run


def get_run(site_qid):
    runs = db.run.find(site_qid=site_qid)
    if not runs.count():
        raise LookupError("No runs available for query: site_qid = '%s'."
                        % site_qid)
    participants = set()
    for run in runs:
        participants.add(run["participants_id"])
    participant = random.choice(list(participants))
    last = 0
    selectedrun = None
    for run in runs:
        if run["participants_id"] != participant:
            continue
        if run["creation_time"] > last:
            last = run["creation_time"]
            selectedrun = run
    return selectedrun
