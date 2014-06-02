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

doc_fields = {
    "docid": fields.String(),
    "clicked": fields.Boolean(default=False),
}

feedback_fields = {
    "qid": fields.String(),
    "modified_time": fields.DateTime(),
    "doclist": fields.Nested(doc_fields)
}


class Feedback(ApiResource):
    def get(self, key, qid):
        self.validate_participant(key)
        feedbacks = self.trycall(core.feedback.get_feedback, userid=key,
                                qid=qid)
        return {"feedback": [marshal(feedback, feedback_fields)
                             for feedback in feedbacks]}

api.add_resource(Feedback, '/api/participant/feedback/<key>/<qid>',
                 endpoint="participant/feedback")
