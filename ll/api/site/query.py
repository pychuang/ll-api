import json
from flask import jsonify, request
from flask.ext.restful import Resource, reqparse, abort, fields, marshal
from .. import api
from .. import core

query_fields = {
    "site_qid" : fields.String,
    "qstr" : fields.String,
    "creation_time" : fields.DateTime(),
}


class Query(Resource):
    def get_site_id(self, key):
        user = core.user.get_user(key)
        if not user:
            abort(403, message="No such key.")
        if not user["is_site"]:
            abort(403, message="Not a site.")
        return user["site_id"]

    def get(self, key):
        """
        Obtain the query set.

        :param key: your API key
        :status 200: valid key
        :status 403: invalid key
        :return: 
            .. sourcecode:: javascript
           
                {
                    "queries": [
                        {
                            "creation_time": "Sun, 27 Apr 2014 11:08:15 -0000", 
                            "qid": "q1011", 
                            "qstr": "jaguar"
                        }, 
                        {
                            "creation_time": "Sun, 27 Apr 2014 11:08:15 -0000", 
                            "qid": "q1112", 
                            "qstr": "apple"
                        }
                    ]
                } 

        """
        site_id = self.get_site_id(key)
        queries = core.query.get_query(site_id=site_id)
        return {"queries": [marshal(q, query_fields) for q in queries]}

    def put(self, key):
        """
        :reqheader Content-Type: application/json
        :body: 
            .. sourcecode:: javascript

                [
                    {
                        "site-qid": "48474c1ab6d3541d2f881a9d4b3bed75", 
                        "qstr": "jaguar"
                    }, 
                    {
                        "site_qid": "30c6677b833454ad2df762d3c98d2409", 
                        "qstr": "apple"
                    }
                ]
        :return: see GET

        """
        site_id = self.get_site_id(key)
        queries = request.get_json(force=True)
        for q in queries:
            core.query.add_query(site_id, q["site_qid"], q["qstr"])
        queries = core.query.get_query(site_id=site_id)
        return {"queries": [marshal(q, query_fields) for q in queries]}

    def delete(self, key):
        pass

api.add_resource(Query, '/api/site/query/<key>', endpoint="site/query")
