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
import hashlib
import datetime
import smtplib
from email.mime.text import MIMEText
from werkzeug import generate_password_hash
from db import db

KEY_LENGTH = 32
PASSWORD_LENGHT = 8
EMAIL_FROM = 'anne.schuth@uva.nl'


def send_email(user, password, subject="New Account"):
    txt = "Hi %s,\n\n" % user["teamname"]
    txt += "These are your Living Labs account details:\n"
    txt += "teamname: %s\n" % user["teamname"]
    txt += "email: %s\n" % user["email"]
    txt += "password: %s\n" % password
    txt += "\n\n"
    txt += "Some relevant urls:\n"
    txt += "API: http://living.labs.net:5000/api\n"
    txt += "Dashboard: http://living.labs.net:5001/\n"
    txt += "Documentation: http://doc.living.labs.net\n"
    txt += "Code: http://git.living.labs.net\n"
    msg = MIMEText(txt)
    msg['subject'] = "[Living Labs] %s" % subject
    email_from = EMAIL_FROM
    email_to = user['email']
    msg['From'] = email_from
    msg['To'] = email_to
    s = smtplib.SMTP('localhost')
    s.sendmail(email_from, [email_to], msg.as_string())
    s.quit()

def random_string(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits)
                   for _ in range(length))


def new_key(teamname, email):
    rstr = random_string(KEY_LENGTH / 2)
    hstr = str(hashlib.sha1(teamname + email).hexdigest())[:KEY_LENGTH / 2]
    return "-".join([hstr, rstr]).upper()


def new_user(teamname, email, password=None):
    if db.user.find({"teamname": teamname}).count():
        raise Exception("Teamname already exists: teamname = '%s'. "
                        "Please choose another name." % teamname)
    if db.user.find({"email": email}).count():
        raise Exception("Email already exists: email = '%s'. "
                        "Please choose another email address." % email)

    if password == None:
        password = random_string(PASSWORD_LENGHT)

    #TODO: check valid email
    #TODO: send email with validation

    user = {
        "_id": new_key(teamname, email),
        "teamname": teamname,
        "email": email,
        "is_participant": True,
        "is_site": False,
        "is_verified": False,
        "creation_time": datetime.datetime.now(),
        "password": generate_password_hash(password),
    }
    send_email(user, password)
    db.user.insert(user)
    return user


def reset_password(email):
    user = get_user_by_email(email)
    password = random_string(PASSWORD_LENGHT)
    user["password"] = generate_password_hash(password)
    send_email(user, password, subject="Password Reset")
    db.user.save(user)


def get_user(key):
    user = db.user.find_one({"_id": key})
    if not user:
        raise Exception("No such user.")
    return user


def get_user_by_email(email):
    user = db.user.find_one({"email": email})
    if not user:
        raise Exception("No such user.")
    return user


def get_users():
    return db.user.find()


def delete_user(key):
    pass
