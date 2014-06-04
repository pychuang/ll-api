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

from .. import core
from flask import Flask, render_template
app = Flask(__name__)

app.config['ADMINS'] = frozenset(['anne.schuth@uva.nl'])
app.config['CSRF_ENABLED'] = True
app.config['CSRF_SESSION_KEY'] = "csrfsecrettoken"
app.config['SECRET_KEY'] = "test1234"
app.config['RECAPTCHA_PUBLIC_KEY'] = "6LdJm_QSAAAAAGJcrrPk9NI7hnYdOR_eMA1WAUci"
app.config['RECAPTCHA_PRIVATE_KEY'] = "6LdJm_QSAAAAAISK9G2S0-aJZYR-zpDphHrj8ZNH"


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from user.views import mod as usersModule
app.register_blueprint(usersModule)
