from flask import request
from flask.ext.restful import Resource, abort, fields, marshal
from .. import api
from .. import core
from site import SiteResource

doclist_fields = {
    "site_docid": fields.String,
    "title": fields.String(),
}


class Feedback(SiteResource):
    def put(self, key, sid):
        """
        Return feedback for a session.

        Store user feedback for a session obtained through
        :http:get:`/api/site/ranking/(key)/(site_qid)`.
        The feedback can be stored multiple times for the same session if more
        feedback comes availaible.
        In that case, the old feedback will be overwritten, it is not additive.
        So if multiple clicks come in one by one, make sure to include all of 
        them each time you update the feedback.

        .. note::

            It is expected that the doclist is the actual doclist that was
            shown to the user.
            This is important because the site may have had to make a last
            minute decisions not to include a certain document.
            It not obtaining a click is valuable information for a participant.

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
                            "site_docid": "af1594296a90da20bdd20e40e737"
                            "clicked": true,
                        }, 
                        {"site_docid": "b5ee9b2e327493c4fdb24296a94a"},
                        {"site_docid": "4922d3c4fdb24296a90a20bdd20e"},
                        ]
                }

        In case Team Draft Interleaving was performed, this should be encoded 
        as follows.

        :content:
            .. sourcecode:: javascript

                {
                    "sid": "s1",
                    "site_qid": "4922d3c4fdb24296a90a20bdd20e",
                    "type": "tdi",
                    "doclist": [
                        {
                            "site_docid": "b5ee9b2e327493c4fdb24296a94a"
                            "clicked": true,
                            "team": "site",
                        },
                        {
                            "site_docid": "af1594296a90da20bdd20e40e737"
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
                    "site_qid": "af1594296a90da20bdd20e40e737",
                    "type": "ctr",
                    "doclist": [
                        {
                            "site_docid": "b5ee9b2e327493c4fdb24296a94a"
                            "clicked": 0.7,
                        },
                        {
                            "site_docid": "4922d3c4fdb24296a90a20bdd20e"
                            "clicked": 0.4,
                        },
                        ]
                }

        :status 200: stored the feedback
        :status 403: invalid key
        """
        site_id = self.get_site_id(key)
        json = request.get_json(force=True)
        self.check_fields(json, ["doclist", "sid", "type"])
        feedback = self.trycall(core.feedback.add_feedback, site_id, sid, json)
        return {
            "sid": sid,
            "site_qid": feedback["site_qid"],
            "type": feedback["type"],
            "doclist": [marshal(d, doclist_fields)
                        for d in feedback["doclist"]]
            }

        return feedback

api.add_resource(Feedback, '/api/site/feedback/<key>/<sid>',
                 endpoint="site/feedback")
