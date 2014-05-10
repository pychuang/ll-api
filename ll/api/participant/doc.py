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

from flask.ext.restful import Resource, fields, marshal
from .. import api
from .. import core
from .. import ApiResource

doclist_fields = {
    "docid": fields.String(attribute="_id"),
    "title": fields.String(),
}


class Doc(ApiResource):
    def get(self, key, docid):
        self.validate_participant(key)
        return {'hello': 'world'}


class DocList(ApiResource):
    def get(self, key, qid):
        self.validate_participant(key)
        doclist = self.trycall(core.doc.get_doclist, qid=qid)
        return {
            "qid": qid,
            "doclist": [marshal(d, doclist_fields) for d in doclist]
            }

api.add_resource(Doc, '/api/participant/doc/<key>/<docid>',
                 endpoint="participant/doc")
api.add_resource(DocList, '/api/participant/doclist/<key>/<qid>',
                 endpoint="participant/doclist")
