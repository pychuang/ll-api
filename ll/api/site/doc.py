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
        Retreive a single document.

        :param key: your API key
        :param site_docid: 
        :status 403: invalid key
        :status 404: document does not exist
        :return: 
            .. sourcecode:: javascript

                {
                     "content": "RHVtbXkgQ29udGVudA==", 
                     "content_encoding": "base64", 
                     "creation_time": "Sun, 27 Apr 2014 23:40:29 -0000", 
                     "site_docid": "b59b2e327493c4fdb24296a90a20bdd20e40e737", 
                     "title": "Document Title"
                } 

        """
        site_id = self.get_site_id(key)
        doc = self.trycall(core.doc.get_doc, site_id=site_id, site_docid=site_docid)
        return marshal(doc, doc_fields)

    def delete(self, key, site_docid):
        pass

    def put(self, key, site_docid):
        """
        Store a single document.
        
        :param key: your API key
        :param site_docid: the site's document identifier

        :reqheader Content-Type: application/json
        :content: 
            .. sourcecode:: javascript

                {
                     "content": "RHVtbXkgQ29udGVudA==", 
                     "content_encoding": "base64", 
                     "site_docid": "b59b2e327493c4fdb24296a90a20bdd20e40e737", 
                     "title": "Document Title"
                } 

        :status 200: stored the document
        :status 403: invalid key
        :status 400: bad request
        :return: see :http:get:`/api/site/doc/(key)/(site_docid)`
        """
        site_id = self.get_site_id(key)
        doc = request.get_json(force=True)
        self.check_fields(doc, ["title", "content", "content_encoding"])
        doc = self.trycall(core.doc.add_doc, site_id, site_docid, doc)
        return marshal(doc, doc_fields)
                

class DocList(SiteResource):
    def get(self, key, site_qid):
        """
        Update the document list for a query. 
        
        The doclist defines the set documents that are returnable for a query.

        :param key: your API key
        :param site_qid: the site's query identifier
        :status 403: invalid key
        :status 404: query does not exist
        :status 400: bad request
        :return: 
            .. sourcecode:: javascript

                {
                    "doclist": [
                        {"site_docid": "b59b2e327493c4fdb24296a90a20bdd20e40e737"}, 
                        {"site_docid": "b59b2e327493c4fdb24296a90a20bdd20e40e737"}, 
                        {"site_docid": "b59b2e327493c4fdb24296a90a20bdd20e40e737"}, 
                            ]
                }

        """
        site_id = self.get_site_id(key)
        doclist = self.trycall(core.doc.get_doclist, site_id=site_id, site_qid=site_qid)
        return {
            "site_qid" : site_qid,
            "doclist": [marshal(d, doclist_fields) for d in doclist]
            }

    def put(self, key, site_qid):
        """
        Update the document list for a query. 
        
        The doclist defines the set documents that are returnable for a query.

        :param key: your API key
        :param site_qid: the site's query identifier
        :reqheader Content-Type: application/json
        :content: 
            .. sourcecode:: javascript

                {
                    "doclist": [
                        {"site_docid": "b59b2e327493c4fdb24296a90a20bdd20e40e737"}, 
                        {"site_docid": "b59b2e327493c4fdb24296a90a20bdd20e40e737"}, 
                        {"site_docid": "b59b2e327493c4fdb24296a90a20bdd20e40e737"}, 
                            ]
                }
        
        :status 403: invalid key
        :status 404: query does not exist
        :status 400: bad request
        :return: see :http:get:`/api/site/doclist/(key)/(site_qid)`
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
