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

from .. import core, requires_login

mod = Blueprint('site', __name__, url_prefix='/site')


@mod.route('/')
@requires_login
def home():
    sites = core.site.get_sites()
    return render_template("site/sites.html", user=g.user, sites=sites)


@mod.route('/<site_id>')
@requires_login
def site(site_id):
    site = core.site.get_site(site_id)
    feedbacks = core.db.db.feedback.find({"site_id": site_id})
    clicks = 0
    for feedback in feedbacks:
        if not "doclist" in feedback:
            continue
        clicks += len([d for d in feedback["doclist"] if d["clicked"]])

    stats = {
             "query": core.db.db.query.find({"site_id": site_id}).count(),
             "doc": core.db.db.doc.find({"site_id": site_id}).count(),
             "impression": feedbacks.count(),
             "click": clicks,
    }
    return render_template("site/site.html",
                           user=g.user,
                           site=site,
                           stats=stats)


@mod.route('/<site_id>/query')
@requires_login
def query(site_id):
    site = core.site.get_site(site_id)
    return render_template("site/query.html",
                           user=g.user,
                           site=site,
                           queries=core.db.db.query.find({"site_id": site_id}))


@mod.route('/<site_id>/doc')
@requires_login
def doc(site_id):
    site = core.site.get_site(site_id)
    return render_template("site/doc.html",
                           user=g.user,
                           site=site,
                           docs=core.db.db.doc.find({"site_id": site_id}))