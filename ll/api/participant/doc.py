from flask import jsonify
from flask.ext.restful import Resource
from .. import api

class Doc(Resource):
    def get(self, docid):
        return {'hello': 'world'}

api.add_resource(Doc, '/doc/<docid>')
