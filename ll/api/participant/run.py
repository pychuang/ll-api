from flask import jsonify
from flask.ext.restful import Resource
from .. import api

class Run(Resource):
    def get(self, runid):
        return {'hello': 'world'}
    def put(self, runid):
        return {'hello': 'world'}

api.add_resource(Run, '/api/participant/run/<runid>', endpoint="participant/run")
