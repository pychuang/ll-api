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

from functools import wraps
from flask import Flask, render_template,  g, flash, redirect, url_for, \
                    request, session
from .. import core
app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', user=g.user), 404


@app.errorhandler(500)
def not_found(error):
    return render_template('500.html', user=g.user), 500


@app.before_request
def before_request():
    """
    pull user's profile from the database before every request are treated
    """
    g.user = None
    if 'key' in session:
        g.user = core.user.get_user(session['key'])


@app.route('/')
def home():
    return render_template("base.html", user=g.user)


def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash(u'You need to be signed in for this page.', 'alert-warning')
            return redirect(url_for('user.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function

from user.views import mod as userModule
app.register_blueprint(userModule)
from site.views import mod as siteModule
app.register_blueprint(siteModule)
from participant.views import mod as participantModule
app.register_blueprint(participantModule)
