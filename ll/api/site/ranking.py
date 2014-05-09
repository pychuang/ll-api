from flask.ext.restful import fields, marshal
from .. import api
from .. import core
from site import SiteResource

doc_fields = {
    "site_docid": fields.String,
    "creation_time": fields.DateTime(),
    "content": fields.String(),
    "title": fields.String(),
    "content_encoding": fields.String(),
}


class Ranking(SiteResource):
    def get(self, key, site_qid):
        """
        Obtain a ranking for a query.

        Every time this endpoint is called, a ranking produced by participants
        of the Challenge is selected based on a least-served basis.
        Due to this behavior, the ranking is likely to change for each call.
        Therefor, the site should perform caching on their own in order to show
        users stable rankings for repeated queries.

        The API will ensure that only documents that are presented in the most
        recent doclist for the requested query are returned.
        Sites are not expected to filter the ranking.
        If filtering is required for this query, please do so by updating the
        doclist.
        While we should aim to prevent this, it may happen that the site needs
        to make a last minute decision not to include a certain document.
        Make sure to incorporate this decision in the feedback.

        The site is expected to expose the retrieved ranking to a user and
        return user feedback :http:put:`/api/site/feedback/(key)/(sid)` as soon
        as it is available.

        :param key: your API key
        :param site_qid: the site's query identifier
        :status 403: invalid key
        :status 404: query does not exist
        :return:
            .. sourcecode:: javascript

                {
                    "sid": "s1",
                    "doclist": [
                        {"site_docid": "4922d3c4fdb24296a90a20bdd20e"},
                        {"site_docid": "af1594296a90da20bdd20e40e737"},
                        {"site_docid": "b5ee9b2e327493c4fdb24296a94a"},
                            ]
                }

        """
        site_id = self.get_site_id(key)
        ranking = self.trycall(core.run.get_ranking, site_id, site_qid)
        return marshal(ranking, doc_fields)


api.add_resource(Ranking, '/api/site/ranking/<key>/<site_qid>', endpoint="site/ranking")
