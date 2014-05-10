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

from flask.ext.restful import Resource, abort, fields, marshal
from .. import api
from .. import core
from .. import ApiResource

user_fields = {
    "key": fields.String(attribute="_id"),
    "creation_time": fields.DateTime(),
    "teamname": fields.String(),
    "is_verified": fields.Boolean(),
}


class Key(ApiResource):
    def get(self, teamname, email):
        """Obtain an API key.

        The first thing you, as a participant or site owner, will need to do is
        request a unique key from the API that you can then use for the rest of
        the challenge.
        You will only need to do this once.
        Also, an email will be send with an activation link. You will have to
        click this link in order to activate your key. Until you do this, all
        API calls with the unverified key will throw a 403 (Forbidden) error,
        as will all other API calls without a key, or with an invalid key.
        The email you receive will also provide you with a login to our
        leaderboard.

        :param teamname: an alphanumeric unique name we will use on to refer to
        you
        :param email: a valid (and your) email address
        :status 200: when both arguments were valid
        :status 400: either the teamname or email address were not formatted
        correctly
        :status 409: the teamname or the email address already exists in our
        database
        :return:
            .. sourcecode:: javascript

                { "key" : "secret-value-key" }

        .. note:: If you are a site owner, please send us an email mentioning
        your key, we will set a flag that will allow you to perfrom actions
        only sites can perform.

        """
        user = core.user.new_user(teamname, email)
        if not user:
            abort(409, message="The teamname or the email address already "
                  "exists in our database. If you requested it before, then "
                  "check your email.")
        return marshal(user, user_fields)

api.add_resource(Key, '/key/<teamname>/<email>')
