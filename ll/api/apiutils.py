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

from flask.ext.restful import Resource, abort, fields
from .. import core

DOCUMENTATION = "http://doc.living-labs.net/"


class ContentField(fields.Raw):
    def format(self, value):
        return value


class ApiResource(Resource):
    def check_fields(self, o, fields):
        notfound = [f for f in fields if f not in o]
        if notfound:
            abort(400, message="Please specify field(s): '%s'. See %s." %
                      (", ".join(notfound), DOCUMENTATION))

    def trycall(self, function, *args, **kwargs):
        #function(*args, **kwargs)
        try:
            return function(*args, **kwargs)
        except ValueError, e:
            abort(409, message=str(e).strip() + " See %s." % DOCUMENTATION)
        except LookupError, e:
            abort(404, message=str(e).strip() + " See %s." % DOCUMENTATION)
        except Exception, e:
            abort(400, message=str(e).strip() + " See %s." % DOCUMENTATION)

    def get_site_id(self, key):
        user = self.trycall(core.user.get_user, key)
        if not user:
            abort(403, message="No such key. See %s." % DOCUMENTATION)
        if not user["is_site"]:
            abort(403, message="Not a site. Please use the participant "
                  "API instead. See %s." % DOCUMENTATION)
        return user["site_id"]

    def validate_participant(self, key):
        user = self.trycall(core.user.get_user, key)
        if not user:
            abort(403, message="No such key. See %s." % DOCUMENTATION)
        if not user["is_participant"]:
            abort(403, message="Not a participant. Please use the site "
                  "API instead. See %s." % DOCUMENTATION)
        if not user["is_verified"]:
            abort(403, message="Not verified (yet). Please send the signed "
                  "registration form.")
        return True
