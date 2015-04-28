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
    stats = {"participants_verified":  len([u for u in participants
                                            if u["is_verified"]]),
             "participants":  len(participants)
             }
    return render_template("admin/admin.html", user=g.user, stats=stats)
