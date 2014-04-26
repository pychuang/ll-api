from flask import jsonify
from flask.ext.restful import Resource
from .. import api

class Feedback(Resource):
    def get(self, runid):
        return {'hello': 'world'}

api.add_resource(Feedback, '/feedback/<runid>')
