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

from flask import request
from flask.ext.restful import Resource, fields, marshal
from .. import api
from .. import core
from .. import ApiResource

doclist_fields = {
    "docid": fields.String(attribute="_id"),
    "title": fields.String(),
}


class Run(ApiResource):
    def get(self, key, qid):
        self.validate_participant(key)
        return {'hello': 'world'}

    def put(self, key, qid):
        self.validate_participant(key)
        run = request.get_json(force=True)
        self.check_fields(run, ["doclist", "runid"])
        self.trycall(core.run.add_run, key, qid, run["runid"], run["doclist"])
        return {
            "runid": run["runid"],
            "qid": qid,
            "doclist": run["doclist"]
            }

api.add_resource(Run, '/api/participant/run/<key>/<qid>',
                 endpoint="participant/run")
