#!/usr/bin/env python

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

import os
import base64
import hashlib
import xml.etree.ElementTree as et
import argparse
import requests
import json
import random
import time
import datetime
import codecs
from numpy import log2, mean

PCLICK = {0: 0.05,
          1: 0.5,
          2: 0.95}
PSTOP = {0: 0.2,
         1: 0.5,
         2: 0.9}


QUERYENDPOINT = "site/query"
DOCENDPOINT = "site/doc"
DOCLISTENDPOINT = "site/doclist"
RANKIGNENDPOINT = "site/ranking"
FEEDBACKENDPOINT = "site/feedback"

HEADERS = {'content-type': 'application/json'}


class Site():
    def __init__(self):
        path = os.path.dirname(os.path.realpath(__file__))
        description = "Living Labs Challenge's Site Client"
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument('--host', dest='host', default='127.0.0.1',
                        help='Host to listen on.')
        parser.add_argument('--port', dest='port', default=5000, type=int,
                        help='Port to listen on.')
        parser.add_argument('-k', '--key', type=str, required=True,
                            help='Provide a user key.')
        parser.add_argument('-q', '--store_queries', action="store_true",
                            default=False,
                            help='Store some queries (needs --query_file).')
        parser.add_argument('--delete_queries', action="store_true",
                            default=False,
                            help='Delete all queries for this site.')
        parser.add_argument('--query_file',
                            default=os.path.normpath(os.path.join(path,
                                                 "../../data/queries.xml")),
                            help='Path to TREC style query file '
                            '(default: %(default)s).')
        parser.add_argument('-d', '--store_doclist', action="store_true",
                            default=False,
                            help='Store a document list (needs --run_file)')
        parser.add_argument('--run_file', 
                            default=os.path.normpath(os.path.join(path,
                                                "../../data/run.txt")),
                            help='Path to TREC style run file '
                            '(default: %(default)s).')
        parser.add_argument('--wait_min', type=int, default=1,
                            help='Minimum simulation waiting time in seconds.')
        parser.add_argument('--wait_max', type=int, default=10,
                            help='Max simulation waiting time in seconds.')
        parser.add_argument('-s', '--simulate_clicks', action="store_true",
                            default=False,
                            help='Simulate clicks (needs --qrel_file).')
        parser.add_argument('--qrel_file',
                            default=os.path.normpath(os.path.join(path,
                                                    "../../data/qrel.txt")),
                            help='Path to TREC style qrel file '
                            '(default: %(default)s).')
        parser.add_argument('--docs_dir',
                            default=os.path.normpath(os.path.join(path,
                                                    "../../data/docs")),
                            help='Path to document directory '
                            '(default: %(default)s).')
        args = parser.parse_args()
        self.host = "%s:%s/api" % (args.host, args.port)

        if args.store_queries:
            self.store_queries(args.key, args.query_file)
        if args.delete_queries:
            self.delete_queries(args.key)
        if args.store_doclist:
            self.store_doclist(args.key, args.run_file, args.docs_dir)
        if args.simulate_clicks:
            self.simulate_clicks(args.key, args.qrel_file, args.wait_min, args.wait_max)

    def store_queries(self, key, query_file):
        tree = et.parse(query_file)
        topics = tree.getroot()
        queries = {"queries": []}
        for topic in topics.getiterator("topic"):
            qid = topic.attrib["number"]
            query = topic.find("query")
            qstr = query.text
            queries["queries"].append({
                "qstr": qstr,
                "site_qid": hashlib.sha1(qid).hexdigest(),
            })
        url = "/".join([self.host, QUERYENDPOINT, key])
        requests.put(url, data=json.dumps(queries), headers=HEADERS)

    def delete_queries(self, key):
        url = "/".join([self.host, QUERYENDPOINT, key])
        requests.delete(url, headers=HEADERS)

    def store_doc(self, key, docid, site_docid, docdir):
        fh = codecs.open(os.path.join(docdir, docid), "r", "utf-8")
        title = fh.readline().strip()
        content = fh.read().strip()
        fh.close()
        doc = {
            "site_docid": site_docid,
            "title": title,
            "content": {"text": content},
            }
        url = "/".join([self.host, DOCENDPOINT, key, site_docid])
        requests.put(url, data=json.dumps(doc), headers=HEADERS)

    def store_doclist(self, key, run_file, docdir):
        def put_doclist(doclist, current_qid):
            site_qid = hashlib.sha1(current_qid).hexdigest()
            doclist["site_qid"] = site_qid
            url = "/".join([self.host, DOCLISTENDPOINT, key, site_qid])
            requests.put(url, data=json.dumps(doclist), headers=HEADERS)

        doclist = {"doclist": []}
        current_qid = None
        for line in open(run_file, "r"):
            qid, _, docid, _, _, _ = line.split()
            if current_qid != None and current_qid != qid:
                put_doclist(doclist, current_qid)
                doclist = {"doclist": []}
            site_docid = hashlib.sha1(docid).hexdigest()
            self.store_doc(key, docid, site_docid, docdir)
            doclist["doclist"].append({"site_docid": site_docid})
            current_qid = qid
        put_doclist(doclist, current_qid)

    def get_ranking(self, key, qid):
        site_qid = hashlib.sha1(qid).hexdigest()
        url = "/".join([self.host, RANKIGNENDPOINT, key, site_qid])
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
        json = r.json()
        return json["sid"], json["doclist"]

    def store_feedback(self, key, qid, sid, ranking, clicks):
        site_qid = hashlib.sha1(qid).hexdigest()
        doclist = {"sid": sid,
                   "site_qid": site_qid,
                   "type": "clicks",
                   "doclist": []}
        for doc, click in zip(ranking, clicks):
            site_docid = doc["site_docid"]
            doclist["doclist"].append({"site_docid": site_docid,
                                       "clicked": click == 1})

        url = "/".join([self.host, FEEDBACKENDPOINT, key, sid])
        r = requests.put(url, data=json.dumps(doclist), headers=HEADERS)
        r.raise_for_status()

    def get_labels(self, qrel_file):
        labels = {}
        for line in open(qrel_file, "r"):
            qid, _, docid, label = line.split()
            if not qid in labels:
                labels[qid] = {}
            site_docid = hashlib.sha1(docid).hexdigest()
            labels[qid][site_docid] = int(label)
        return labels

    def get_clicks(self, ranking, labels):
        clicks = [0] * len(ranking)
        for pos, doc in enumerate(ranking):
            site_docid = doc["site_docid"]
            label = labels[site_docid]
            rand = random.random()
            if rand < PCLICK[label]:
                clicks[pos] = 1
                rand = random.random()
                if rand < PSTOP[label]:
                    break
        return clicks

    def evaluate_ranking(self, ranking, labels):
        def get_dcg(orderedlabels):
            dcg = 0.0
            for pos, label in enumerate(orderedlabels):
                dcg += (2. ** label - 1.) / log2(2. + pos)
            return dcg
        orderedlabels = [labels[doc["site_docid"]] for doc in ranking]
        idcg = get_dcg(sorted(orderedlabels, reverse=True))
        if idcg == 0.0:
            return 0.0
        return get_dcg(orderedlabels) / idcg

    def evaluate(self, rankings, labels):
        ndcgs = []
        for qid in rankings:
            ndcgs.append(self.evaluate_ranking(rankings[qid], labels[qid]))
        return mean(ndcgs)

    def simulate_clicks(self, key, qrel_file, wait_min, wait_max):
        labels = self.get_labels(qrel_file)
        rankings = {}
        while True:
            qid = random.choice(labels.keys())
            #try:
            sid, ranking = self.get_ranking(key, qid)
            rankings[qid] = ranking
            print "NDCG: %.3f" % self.evaluate(rankings, labels)
            #TODO: once in a while, drop a document before return.
            clicks = self.get_clicks(ranking, labels[qid])
            self.store_feedback(key, qid, sid, ranking, clicks)
            #except:
            #    print "ERROR, fall back to normal processing"
            time.sleep(wait_min + (random.random() * (wait_max - wait_min)))

if __name__ == '__main__':
    site = Site()
