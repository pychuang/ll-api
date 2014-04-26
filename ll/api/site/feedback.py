from flask import jsonify
from flask.ext.restful import Resource
from .. import api

class Feedback(Resource):
    def put(self, key):
        """
        :param key: your API key
        :status 200: valid key
        :status 403: invalid key
        :return: 
            .. sourcecode:: javascript
            
                {   "S-q2" : "jaguar",
                    "S-q2" : "apple",
                    ... }

        """

        return queries


api.add_resource(Feedback, '/api/site/feedback/<key>', endpoint="site/feedback")
