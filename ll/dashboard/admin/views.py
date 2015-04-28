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

from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
import json
from .. import core, requires_login

mod = Blueprint('admin', __name__, url_prefix='/admin')


@mod.route('/')
@requires_login
def admin():
    if not g.user["is_admin"]:
        flash(u'You need to be admin for this page.', 'alert-warning')
        return redirect("/")
    participants = core.user.get_participants()
    queries = core.query.get_query()
    sites = [s for s in core.site.get_sites()]
    active_participants = set()
    site_participants = {}
    site_queries = {}
    for query in queries:
        if not query["site_id"] in site_participants:
            site_participants[query["site_id"]] = set()
        if not query["site_id"] in site_queries:
            site_queries[query["site_id"]] = 0
        if "runs" in query:
            site_queries[query["site_id"]] += 1
            for u in query["runs"]:
                active_participants.add(u)
                site_participants[query["site_id"]].add(u)

    stats = {"participants": {"verified":  len([u for u in participants
                                                if u["is_verified"]]),
                              "all":  len(participants),
                              "active":  len(active_participants)
                              },
             "sites": {"runs": len(site_participants),
                       "all": len(sites),
                       "active": len([s for s in sites if s["enabled"]])},
             "queries": len(queries),
             "per_site": {site["_id"]: {"participants": len(site_participants[site["_id"]]) if site["_id"] in site_participants else 0,
                                        "queries": site_queries[site["_id"]] if site["_id"] in site_queries else 0
                                    } for site in sites
                          }
             }
    return render_template("admin/admin.html", user=g.user, stats=stats)
