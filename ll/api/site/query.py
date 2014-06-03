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
from flask.ext.restful import fields, marshal
from .. import api
from .. import core
from .. import ApiResource

query_fields = {
    "site_qid": fields.String(),
    "qstr": fields.String(),
    "creation_time": fields.DateTime(),
}


class Query(ApiResource):
    def get(self, key):
        """
        Obtain the query set.

        :param key: your API key
        :status 200: valid key
        :status 403: invalid key
        :return:
            .. sourcecode:: javascript

                {
                    "queries": [
                        {
                            "creation_time": "Sun, 27 Apr 2014 13:46:00 -0000",
                            "qstr": "jaguar",
                            "site_qid": "48474c1ab6d3541d2f881a9d4b3bed75"
                        },
                        {
                            "creation_time": "Sun, 27 Apr 2014 13:46:00 -0000",
                            "qstr": "apple",
                            "site_qid": "30c6677b833454ad2df762d3c98d2409"
                        }
                    ]
                }

        """
        site_id = self.get_site_id(key)
        queries = self.trycall(core.query.get_query, site_id=site_id)
        return {"queries": [marshal(q, query_fields) for q in queries]}

    def put(self, key):
        """
        Update the query set. This can only be done before the challenge
        started.

        :param key: your API key

        :reqheader Content-Type: application/json
        :content:
            .. sourcecode:: javascript

                {
                    "queries": [
                        {
                            "qstr": "jaguar",
                            "site_qid": "48474c1ab6d3541d2f881a9d4b3bed75"
                        },
                        {
                            "qstr": "apple",
                            "site_qid": "30c6677b833454ad2df762d3c98d2409"
                        }
                    ]
                }

        :status 403: invalid key.
        :status 400: bad request.
        :status 409: the query set is not updatable, the challenge is running.
        :return: see :http:get:`/api/site/query/(key)`.
        """

        site_id = self.get_site_id(key)
        queries = request.get_json(force=True)
        self.check_fields(queries, ["queries"])
        self.trycall(core.query.delete_query, site_id=site_id)
        for q in queries["queries"]:
            self.check_fields(q, ["site_qid", "qstr"])
            self.trycall(core.query.add_query, site_id, q["site_qid"],
                         q["qstr"])
        queries = self.trycall(core.query.get_query, site_id=site_id)
        return {"queries": [marshal(q, query_fields) for q in queries]}

    def delete(self, key):
        """
        Delete the query set. This can only be done before the challenge.
        started.

        :param key: your API key.

        :status 403: invalid key.
        :status 400: bad request.
        :status 409: the query set is not deletable, the challenge is running.
        :status 200: the query set is deleted.
        """

        site_id = self.get_site_id(key)
        self.trycall(core.query.delete_query, site_id=site_id)

api.add_resource(Query, '/api/site/query/<key>', endpoint="site/query")
