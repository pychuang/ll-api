from flask import jsonify, request
from flask.ext.restful import Resource, abort, fields, marshal
from .. import api
from .. import core
from site import SiteResource

doclist_fields = {
    "site_docid" :  fields.String,
    "title" : fields.String(),
}

doc_fields = {
    "site_docid" :  fields.String,
    "creation_time" : fields.DateTime(),
    "content" : fields.String(),
    "title" : fields.String(),
    "content_encoding" : fields.String(),
}

class Doc(SiteResource):
    def get(self, key, site_docid):
        """
        :param key: your API key
        :status 200: valid key
        :status 403: invalid key
        :return: 
            .. sourcecode:: javascript

        """
        site_id = self.get_site_id(key)
        doc = self.trycall(core.doc.get_doc, site_id=site_id, site_docid=site_docid)
        return marshal(doc, doc_fields)

    def delete(self, key, site_docid):
        pass

    def put(self, key, site_docid):
        site_id = self.get_site_id(key)
        doc = request.get_json(force=True)
        self.check_fields(doc, ["title", "content", "content_encoding"])
        doc = self.trycall(core.doc.add_doc, site_id, site_docid, doc)
        return marshal(doc, doc_fields)
                

class DocList(SiteResource):
    def get(self, key, site_qid):
        site_id = self.get_site_id(key)
        doclist = self.trycall(core.doc.get_doclist, site_id=site_id, site_qid=site_qid)
        return {
            "site_qid" : site_qid,
            "doclist": [marshal(d, doclist_fields) for d in doclist]
            }

    def put(self, key, site_qid):
        """
        :reqheader Content-Type: application/json
        :content: 
            .. sourcecode:: javascript

                {
                    "doclist": [
                            "d171717d75",
                            "d171717d75",
                            ]
                }
        """
        site_id = self.get_site_id(key)
        documents = request.get_json(force=True)
        self.check_fields(documents, ["doclist"])
        doclist = self.trycall(core.doc.add_doclist, site_id, site_qid, documents["doclist"])
        return {
            "site_qid" : site_qid,
            "doclist": [marshal(d, doclist_fields) for d in doclist]
            }

api.add_resource(Doc, '/api/site/doc/<key>/<site_docid>', endpoint="site/doc")
api.add_resource(DocList, '/api/site/doclist/<key>/<site_qid>', endpoint="site/doclist")
