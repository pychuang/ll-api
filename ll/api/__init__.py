from flask import Flask
from flask.ext.restful import Api

from .. import core

app = Flask(__name__)
api = Api(app)
