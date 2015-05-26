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


outcome_fields = {"site_id": fields.String(),
                  "qid": fields.String(),
                  "outcome": fields.Float(),
                  "wins": fields.Integer(),
                  "losses": fields.Integer(),
                  "ties": fields.Integer(),
                  "impressions": fields.Integer()
                  }


class Outcome(ApiResource):
    def get(self, key, qid=None):
        """
        Obtain outcome (optionally for a query).

        You may omit or specify "all" as the query identifier to obtain
        feedback for all queries.

        Note that you may receive multiple feedbacks for a single query as
        it may have been shown to a user more than once. And even if you
        specify a runid, then the rankings for this runid may have been
        presented to users multiple times.


        :param key: your API key
        :param qid: *optional*, the query identifier, can be "all"
        :status 403: invalid key
        :status 404: query does not exist
        :status 400: bad request
        :return:
            .. sourcecode:: javascript

                {
                    "outcomes": [
                        {"site_id": "S",
                         "qid": "S-q1",
                         "outcome": 0.4,
                         "wins": 2
                         "losses": 3
                         "ties": 5
                         "impressions": 10
                        },
                        ...
                }

        """

        self.validate_participant(key)
        outcomes = self.trycall(core.feedback.get_comparison,
                                key,
                                qid=qid)

        return {"outcomes": [marshal(outcomes[site_id], outcome_fields)
                             for site_id in outcomes]}


api.add_resource(Outcome, '/api/participant/outcome/<key>/<qid>',
                           '/api/participant/outcome/<key>',
                 endpoint="participant/outcome")
