from flask import jsonify
from flask.ext.restful import Resource
from .. import api

class Ranking(Resource):
    def get(self, key, site_qid):
        """
        Obtain a ranking for a query. 
        
        The site is expected to expose this ranking to a user and return feedback :http:put:`/api/site/feedback/(key)/(sid)` as soon as it is available.

        :param key: your API key
        :param site_qid: the site's query identifier
        :status 200: valid key
        :status 404: query does not exist
        :status 403: invalid key
        :return: 
            .. sourcecode:: javascript
            
                {
                    "sid": "s1",
                    "doclist": [
                        {"site_docid": "b59b2e327493c4fdb24296a90a20bdd20e40e737"}, 
                        {"site_docid": "b59b2e327493c4fdb24296a90a20bdd20e40e737"}, 
                        {"site_docid": "b59b2e327493c4fdb24296a90a20bdd20e40e737"}, 
                            ]
                }

        """

        return queries


api.add_resource(Ranking, '/api/site/ranking/<key>/<site_qid>', endpoint="site/ranking")
