from flask import jsonify
from flask.ext.restful import Resource
from .. import api

class Feedback(Resource):
    def put(self, key, sid):
        """
        Return feedback for a session.

        Store user feedback for a session obtained through :http:get:`/api/site/ranking/(key)/(site_qid)`. 
        This can be store multiple times if more feedback comes availaible. 
        In that case, the old feedback would be overwritten.

        :param key: your API key
        :param sid: the session's identifier
        :reqheader Content-Type: application/json
        :content: 
            .. sourcecode:: javascript
            
                {
                    "sid": "s1",
                    "type": "clicks",
                    "doclist": [
                        {
                            "site_docid": "b59b2e327493c4fdb24296a90a20bdd20e40e737"
                            "clicked": true,
                        }, 
                        {"site_docid": "b59b2e327493c4fdb24296a90a20bdd20e40e737"}, 
                        {"site_docid": "b59b2e327493c4fdb24296a90a20bdd20e40e737"}, 
                        ]
                }

        In case Team Draft Interleaving was performed, this should be encoded as follows.

        :content: 
            .. sourcecode:: javascript
            
                {
                    "sid": "s1",
                    "type": "tid",
                    "doclist": [
                        {
                            "site_docid": "b59b2e327493c4fdb24296a90a20bdd20e40e737"
                            "clicked": true,
                            "team": "site",
                        }, 
                        {
                            "site_docid": "b59b2e327493c4fdb24296a90a20bdd20e40e737"
                            "clicked": true,
                            "team": "participant",
                        }, 
                        ]
                }

        :status 200: stored the feedback
        :status 403: invalid key
        """

        return queries


api.add_resource(Feedback, '/api/site/feedback/<key>/<sid>', endpoint="site/feedback")
