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
from db import db

KEY_LENGTH = 32


def new_key(teamname, email):
    rstr = ''.join(random.choice(string.ascii_lowercase + string.digits)
                   for _ in range(KEY_LENGTH / 2))
    hstr = str(hashlib.sha1(teamname + email).hexdigest())[:KEY_LENGTH / 2]
    return "-".join([hstr, rstr]).upper()


def new_user(teamname, email):
    if db.user.find({"teamname": teamname}).count():
        raise Exception("Teamname exists: teamname = '%s'" % teamname)
    if db.user.find({"email": email}).count():
        raise Exception("Email exists: email = '%s'" % email)
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
    }
    db.user.insert(user)
    return user


def get_user(key):
    user = db.user.find_one({"_id": key})
    if not user:
        return False
    return user


def delete_user(key):
    pass
