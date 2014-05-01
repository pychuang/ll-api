from flask import jsonify
from flask.ext.restful import Resource
from .. import api
from .. import core
from site import SiteResource

class Ranking(SiteResource):
    def get(self, key, site_qid):
        """
        Obtain a ranking for a query. 
        
        Everytime this endpoint is called, a ranking produced by participants of the Challenge is selected based on a least-served basis. Do to this behaviour, the ranking may change for each call. Therefor, the site perform caching on their own in order to show users stable rankings for repeated queries.
        The API will ensure that only documents that are presented in the most recent doclist for the requested query are returned. 
        Sites are not expected to filter the ranking. If filtering is required for this query, please do so by updating the doclist.

        The site is expected to expose the retrieved ranking to a user and return feedback :http:put:`/api/site/feedback/(key)/(sid)` as soon as it is available.

        :param key: your API key
        :param site_qid: the site's query identifier
        :status 403: invalid key
        :status 404: query does not exist
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
        site_id = self.get_site_id(key)
        ranking = self.trycall(core.run.get_ranking, site_id, site_qid)
        return marshal(ranking, doc_fields)


api.add_resource(Ranking, '/api/site/ranking/<key>/<site_qid>', endpoint="site/ranking")
