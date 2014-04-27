import base64
import hashlib
import xml.etree.ElementTree as et
import argparse
import requests
import json

HOST = "http://127.0.0.1:5000/api"
QUERYENDPOINT = "site/query"
DOCENDPOINT = "site/doc"
DOCLISTENDPOINT = "site/doclist"

headers = {'content-type': 'application/json'}

def put(url, data):
    r = requests.put(url, data=data, headers=headers)
    return r.text

def store_queries(key, query_file):
    tree = et.parse(query_file)
    topics = tree.getroot()
    queries = {"queries": []}
    for topic in topics.iter("topic"):
        qid = topic.attrib["number"]
        query = topic.find("query")
        qstr = query.text
        queries["queries"].append({
            "qstr" : qstr,
            "site_qid" : hashlib.sha1(qid).hexdigest(),
        })
    url = "/".join([HOST, QUERYENDPOINT, key])
    print put(url, json.dumps(queries))

def store_doc(key, doc, site_docid):
    title = "Dummy Title"
    content = "Dummy Content"
    doc = { 
        "site_docid": site_docid,
        "title": title,
        "content": base64.b64encode(content),
        "content_encoding": "base64",
        }
    url = "/".join([HOST, DOCENDPOINT, key, site_docid])
    print put(url, json.dumps(doc))

def store_doclist(key, run_file):
    def put_doclist(doclist, current_qid):
        site_qid = hashlib.sha1(current_qid).hexdigest()
        doclist["site_qid"] = site_qid
        url = "/".join([HOST, DOCLISTENDPOINT, key, site_qid])
        return put(url, json.dumps(doclist))

    doclist = {"doclist": []}
    current_qid = None
    for line in open(run_file, "r"):
        qid, _, docid, _, _, _ = line.split()
        if current_qid != None and current_qid != qid: 
            print put_doclist(doclist, current_qid)
            doclist = {"doclist": []}
        site_docid = hashlib.sha1(docid).hexdigest()
        store_doc(key, docid, site_docid)
        doclist["doclist"].append({"site_docid": site_docid})
        current_qid = qid
    print put_doclist(doclist, current_qid)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Living Labs Challenge's API Server")
    parser.add_argument('--key', type=str, required=True,
                        help='Provide a user key.')
    parser.add_argument('-q', '--store_queries', action="store_true", default=False,
                        help='Store some queries.')
    parser.add_argument('--query_file', default="data/queries.xml",
                        help='Path to TREC style query file.')
    parser.add_argument('-d', '--store_doclist', action="store_true", default=False,
                        help='Store a document list.')
    parser.add_argument('--run_file', default="data/run.txt",
                        help='Path to TREC style run file.')
    args = parser.parse_args()
    if args.store_queries:
        store_queries(args.key, args.query_file)
    if args.store_doclist:
        store_doclist(args.key, args.run_file)
