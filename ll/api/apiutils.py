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

import traceback
from flask.ext.restful import Resource, abort, fields
from .. import core


class ContentField(fields.Raw):
    def format(self, value):
        return value


class ApiResource(Resource):
    def abort(self, status, message, tb=None):
        if tb is None:
            abort(status,
                  message=str(message).strip().strip("."),
                  status=status,
                  documentaton=core.config.config["URL_DOC"])
        else:
            abort(status,
                  message=str(message).strip().strip("."),
                  status=status,
                  documentaton=core.config.config["URL_DOC"],
                  traceback=[l for l in tb.split("\n") if l])

    def check_fields(self, o, fields):
        notfound = [f for f in fields if f not in o]
        if notfound:
            self.abort(400, "Please specify field(s): '%s'" %
                       ", ".join(notfound))

    def trycall(self, function, *args, **kwargs):
        try:
            return function(*args, **kwargs)
        except ValueError, e:
            self.abort(409, e, traceback.format_exc())
        except LookupError, e:
            self.abort(404, e, traceback.format_exc())
        except Exception, e:
            self.abort(400, e, traceback.format_exc())

    def get_site_id(self, key):
        user = self.trycall(core.user.get_user, key)
        if not user:
            self.abort(403, "No such key")
        if not user["is_site"]:
            self.abort(403, "Not a site. Please use the participant "
                       "API instead")
        return user["site_id"]

    def validate_participant(self, key):
        user = self.trycall(core.user.get_user, key)
        if not user:
            self.abort(403, "No such key")
        if not user["is_participant"]:
            self.abort(403, "Not a participant. Please use the site "
                       "API instead")
        if not user["is_verified"]:
            self.abort(403, "Not verified (yet). Please send the signed "
                       "registration form.")
        return True
