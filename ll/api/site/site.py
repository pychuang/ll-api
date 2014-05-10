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

from flask.ext.restful import Resource, abort
from .. import core

DOCUMENTATION = "http://doc.living-labs.net/"


class SiteResource(Resource):
    def check_fields(self, o, fields):
        for f in fields:
            if f not in o:
                abort(400, message="Please specify field '%s'. See %s." %
                      (f, DOCUMENTATION))

    def trycall(self, function, *args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception, e:
            abort(400, message=str(e).strip() + " See %s." % DOCUMENTATION)

    def get_site_id(self, key):
        user = self.trycall(core.user.get_user, key)
        if not user:
            abort(403, message="No such key. See %s." % DOCUMENTATION)
        if not user["is_site"]:
            abort(403, message="Not a site. Please use the participant"
                  "API instead. See %s." % DOCUMENTATION)
        return user["site_id"]
