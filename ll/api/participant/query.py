from flask.ext.restful import Resource, abort, fields, marshal
from .. import api
from .. import core

query_fields = {
    "qid": fields.String(attribute="_id"),
    "qstr": fields.String,
    "creation_time": fields.DateTime(),
}


class Query(Resource):
    def get(self, key):
        """Obtain the query set.

        :param key: your API key
        :status 200: valid key
        :status 403: invalid key
        :return:
            .. sourcecode:: javascript

                {   "S-q2" : "jaguar",
                    "S-q2" : "apple",
                    ... }

        .. note:: We kindly ask you to not enter any of the provided queries
        into the search engines for testing purposes (unless, of course you
        have an actual information need that translates in any of the queries).
        As we are not aware of your the IP addresses you may use for these
        request, we have no means of filtering such queries out. In particular,
        for the smaller engines such test issues of queries might severely
        impact the usefulness of our challenge. We will, however, monitor for
        strange behaviour.

        """
        queries = core.query.get_query()
        return {"queries": [marshal(q, query_fields) for q in queries]}

api.add_resource(Query, '/api/participant/query/<key>',
                 endpoint="participant/query")
