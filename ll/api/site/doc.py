from flask import jsonify
from flask.ext.restful import Resource
from .. import api

class Doc(Resource):
    def get(self, key):
        """
        :param key: your API key
        :status 200: valid key
        :status 403: invalid key
        :return: 
            .. sourcecode:: javascript

        """

        return queries

    def put(self, key):
        pass

    def delete(self, key):
        pass

api.add_resource(Doc, '/api/site/doc/<key>', endpoint="site/doc")
