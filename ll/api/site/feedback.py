from flask import jsonify
from flask.ext.restful import Resource
from .. import api

class Feedback(Resource):
    def put(self, key, sid):
        """
        Return feedback for a session.

        Store user feedback for a session obtained through :http:get:`/api/site/ranking/(key)/(site_qid)`. 
        The feedback can be stored multiple times for the same session if more feedback comes availaible. 
        In that case, the old feedback will be overwritten.

        :param key: your API key
        :param sid: the session's identifier
        :reqheader Content-Type: application/json
        :content: 
            .. sourcecode:: javascript
            
                {
                    "sid": "s1",
                    "site_qid": "48474c1ab6d3541d2f881a9d4b3bed75",
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
                    "site_qid": "48474c1ab6d3541d2f881a9d4b3bed75",
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
        
        Historical feedback can be added as follows.

        .. warning:: #TODO: need another endpoint, no sid available here.

        :content: 
            .. sourcecode:: javascript
            
                {
                    "site_qid": "48474c1ab6d3541d2f881a9d4b3bed75",
                    "type": "ctr",
                    "doclist": [
                        {
                            "site_docid": "b59b2e327493c4fdb24296a90a20bdd20e40e737"
                            "clicked": 0.7,
                        }, 
                        {
                            "site_docid": "b59b2e327493c4fdb24296a90a20bdd20e40e737"
                            "clicked": 0.4,
                        }, 
                        ]
                }



        :status 200: stored the feedback
        :status 403: invalid key
        """

        return queries


api.add_resource(Feedback, '/api/site/feedback/<key>/<sid>', endpoint="site/feedback")
