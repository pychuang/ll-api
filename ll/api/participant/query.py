from flask import jsonify
from flask.ext.restful import Resource
from .. import api

class Query(Resource):
    def get(self, queryid):
        return {'hello': 'world'}

api.add_resource(Query, '/query/<queryid>')
