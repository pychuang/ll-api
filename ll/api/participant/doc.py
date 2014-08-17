# This file is part of Living Labs Challenge, see http://living-labs.net.
#
# Living Labs Challenge is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Living Labs Challenge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Living Labs Challenge. If not, see <http://www.gnu.org/licenses/>.

from flask.ext.restful import Resource, fields, marshal
from .. import api
from .. import core
from .. import ApiResource, ContentField

doclist_fields = {
    "docid": fields.String(attribute="_id"),
    "title": fields.String(),
}

doclist_fields_szn = {
    "docid": fields.String(attribute="_id"),
    "title": fields.String(),
    "relevance_signals": fields.List(fields.List(fields.Float)),
}

doc_fields = {
    "docid": fields.String(attribute="_id"),
    "creation_time": fields.DateTime(),
    "content": ContentField(),
    "title": fields.String(),
}


class Doc(ApiResource):
    def get(self, key, docid):
        """
        Retrieve a single document.

        :param key: your API key
        :param docid: the document identifier
        :status 403: invalid key
        :status 404: document does not exist
        :return:
            .. sourcecode:: javascript

                {
                     "content": {"description": "Lorem ipsum dolor sit amet",
                                 "short_description" : "Lorem ipsum",
                                 ...}
                     "creation_time": "Sun, 27 Apr 2014 23:40:29 -0000",
                     "docid": "S-d1",
                     "title": "Document Title"
                }

        """
        self.validate_participant(key)
        doc = self.trycall(core.doc.get_doc, docid=docid, key=key)
        return marshal(doc, doc_fields)


class DocList(ApiResource):
    def get(self, key, qid):
        """
        Retrieve the document list for a query.

        This doclist defines the set documents that are returnable for a query.
        You are free to update this list when the set of documents changes over
        time.

        :param key: your API key
        :param qid: the query identifier
        :status 403: invalid key
        :status 404: query does not exist
        :status 400: bad request
        :return:
            .. sourcecode:: javascript

                {
                    "qid": "S-q22",
                    "doclist": [
                        {"docid": "S-d3"},
                        {"docid": "S-d5"},
                        {"docid": "S-d10"},
                        ...
                            ]
                }

        """
        self.validate_participant(key)
        doclist = self.trycall(core.doc.get_doclist, qid=qid, key=key)
        return {
            "qid": qid,
            "doclist": [marshal(d, doclist_fields_szn)
                if "relevance_signals" in d else marshal(d, doclist_fields)
                for d in doclist]
            }

api.add_resource(Doc, '/api/participant/doc/<key>/<docid>',
                 endpoint="participant/doc")
api.add_resource(DocList, '/api/participant/doclist/<key>/<qid>',
                 endpoint="participant/doclist")
