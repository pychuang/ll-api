from flask import jsonify
from flask.ext.restful import Resource
from .. import api


class Key(Resource):
    def get(self, teamname, email):
        """Obtain an API key.

        The first thing you, as a participant, will need to do is request a unique key from the API that you can then use for the rest of the challenge.
        You will only need to do this once.
        Also, an email will be send with an activation link. You will have to click this link in order to activate your key. Until you do this, all API calls with the unverified key will throw a 403 (Forbidden) error, as will all other API calls without a key, or with an invalid key.
        The email you receive will also provide you with a login to our leaderboard (described below).

        :param teamname: an alphanumeric unique name we will use on to refer to you
        :param email: a valid (and your) email address
        :status 200: when both arguments were valid
        :status 400: either the teamname or email address were not formatted correctly
        :status 409: your chosen name or if the email address already exist in our database
        :return: {"key" : "secret-value-key"}

        """
        return jsonify({"key":"secret-value-key"})

api.add_resource(Key, '/key/<teamname>/<email>')
