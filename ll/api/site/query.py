import json
from flask import jsonify, request
from flask.ext.restful import Resource, reqparse, abort
from .. import api
from .. import core
from .. import util

class Query(Resource):
    #def __init__(self):
        #self.reqparse = reqparse.RequestParser()
        #self.reqparse.add_argument('title', type = str, required = True,
        #    help = 'No task title provided', location = 'json')
        #self.reqparse.add_argument('description', type = str, default = "", location = 'json')
        #super(Query, self).__init__()

    def get(self, key):
        """
        Obtain the query set.

        :param key: your API key
        :status 200: valid key
        :status 403: invalid key
        :return: 
            .. sourcecode:: javascript
            
                {   "S-q2" : "jaguar",
                    "S-q2" : "apple",
                    ... }

        """
        user = core.user.get_user(key)
        queries = core.query.get_query(user)
        return jsonify(util.wrap_queries(user, queries))

    def put(self, key):
        """
        :reqheader Content-Type: application/json
        :resheader Content-Type: application/json

        .. sourcecode:: javascript

            [
                {
                    "qid": "q0",
                    "qstr": "jaguar"
                }, 
                {
                    "qid": "q1",
                    "qstr": "apple"
                }
            ]

        """
        queries = request.get_json(force=True)
        user = core.user.get_user(key)
        for q in queries:
            core.query.add_query(user, q["qid"], q["qstr"])
            #abort(409, message="Duplicate qid %s." % q["qid"])

        queries = core.query.get_query(user)
        return jsonify(util.wrap_queries(user, queries))

    def delete(self, key):
        pass

api.add_resource(Query, '/api/site/query/<key>', endpoint="site/query")
