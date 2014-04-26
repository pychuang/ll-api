from flask import jsonify
from flask.ext.restful import Resource
from .. import api

class Ranking(Resource):
    def get(self, key):
        """
        :param key: your API key
        :status 200: valid key
        :status 403: invalid key
        :return: 
            .. sourcecode:: javascript
            

        """

        return queries


api.add_resource(Ranking, '/api/site/ranking/<key>', endpoint="site/ranking")
