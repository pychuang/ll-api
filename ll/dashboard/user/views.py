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
from werkzeug import check_password_hash, generate_password_hash

from .. import app, core, requires_login
from forms import LoginForm, RegisterForm

mod = Blueprint('user', __name__, url_prefix='/user')
app.register_blueprint(mod)

@mod.route('/me/')
@requires_login
def home():
    return render_template("user/profile.html", user=g.user)

@mod.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Login form
    """
    form = LoginForm(request.form)
    # make sure data are valid, but doesn't validate password is right
    if form.validate_on_submit():
        user = core.user.get_user_by_email(form.email.data)
        # we use werzeug to validate user's password
        if user and check_password_hash(user["password"], form.password.data):
            # the session can't be modified as it's signed,
            # it's a safe place to store the user id
            session['key'] = user["_id"]
            flash('Welcome %s' % user["teamname"], 'alert-success')
            return redirect(url_for('user.home'))
        flash('Wrong email or password', 'alert-info')
    return render_template("user/login.html", form=form, user=g.user)


@mod.route('/logout/', methods=['GET'])
def logout():
    """
    Logout
    """
    g.user = None
    del session['key']
    return redirect(url_for('user.home'))


@mod.route('/register/', methods=['GET', 'POST'])
def register():
    """
    Registration Form
    """
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        try:
            user = core.user.new_user(form.teamname.data, form.email.data,
                                  generate_password_hash(form.password.data))
        except Exception, e:
            flash(e, 'alert-warning')
            return render_template("user/register.html", form=form, user=g.user)

        key = user["_id"]
        session['key'] = key
        flash('Thanks for registering. Your key is: %s' % key, 'alert-success')
        # redirect user to the 'home' method of the user module.
        return redirect(url_for('user.home'))
    return render_template("user/register.html", form=form, user=g.user)