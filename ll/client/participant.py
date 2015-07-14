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

import argparse
import requests
import json
import time
import random
import os


QUERYENDPOINT    = "participant/query"
DOCENDPOINT      = "participant/doc"
DOCLISTENDPOINT  = "participant/doclist"
RUNENDPOINT      = "participant/run"
FEEDBACKENDPOINT = "participant/feedback"

HEADERS = {'content-type': 'application/json'}


class Participant():
    def __init__(self):
        path = os.path.dirname(os.path.realpath(__file__))
        description = "Living Labs Challenge's Participant Client"
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument('--host', dest='host',
                            default='http://living-labs.net',
                            help='Host to listen on.')
        parser.add_argument('--port', dest='port', default=5000, type=int,
                            help='Port to connect to.')
        parser.add_argument('-k', '--key', type=str, required=True,
                            help='Provide a user key.')
        parser.add_argument('-s', '--simulate_runs', action="store_true",
                            default=False,
                            help='Simulate runs.')
        parser.add_argument('--store_run', action="store_true",
                            default=False,
                            help='Store TREC run (needs --run_file).')
        parser.add_argument('--run_file',
                            default=os.path.normpath(os.path.join(path,
                                                     "../../data/run.txt")),
                            help='Path to TREC style run file '
                            '(default: %(default)s).')
        parser.add_argument('--get_feedback', action="store_true",
                            default=False,
                            help="Get feedback, if any")
        parser.add_argument('--get_train', action="store_true",
                            default=False,
                            help="Get training data")
        parser.add_argument('--get_test', action="store_true",
                            default=False,
                            help="Get test data")
        parser.add_argument('--reset_feedback', action="store_true",
                            default=False,
                            help="Get feedback, if any")
        parser.add_argument('--wait_min', type=int, default=1,
                            help='Minimum simulation waiting time in seconds.')
        parser.add_argument('--wait_max', type=int, default=10,
                            help='Max simulation waiting time in seconds.')

        args = parser.parse_args()

        self.host = "%s:%s/api" % (args.host, args.port)
        if not self.host.startswith("http://"):
            self.host = "http://" + self.host

        self.runid = 0

        if args.store_run:
            self.store_run(args.key, args.run_file)

        if args.get_feedback:
            self.get_feedbacks(args.key)

        if args.get_train:
            self.get_train(args.key)

        if args.get_test:
            self.get_test(args.key)

        if args.reset_feedback:
            self.reset_feedback(args.key)

        if args.simulate_runs:
            self.simulate_runs(args.key, args.wait_min, args.wait_max)

    def get_queries(self, key):
        url = "/".join([self.host, QUERYENDPOINT, key])
        r = requests.get(url, headers=HEADERS)
        time.sleep(random.random())
        if r.status_code != requests.codes.ok:
            print r.text
            r.raise_for_status()
        return r.json()

    def get_doclist(self, key, qid):
        url = "/".join([self.host, DOCLISTENDPOINT, key, qid])
        r = requests.get(url, headers=HEADERS)
        time.sleep(random.random())
        if r.status_code != requests.codes.ok:
            print r.text
            r.raise_for_status()
        return r.json()

    # if qid == "all" returns feedback for all queries
    def get_feedback(self, key, qid, runid=None):
        urlList = [self.host, FEEDBACKENDPOINT, key, qid]
        if runid:
            urlList.append(str(runid))
        url = "/".join(urlList)
        r = requests.get(url, headers=HEADERS)
        time.sleep(random.random())
        if r.status_code != requests.codes.ok:
            print r.text
            r.raise_for_status()
        return r.json()

    def reset_feedback(self, key):
        queries = self.get_queries(key)
        for query in queries["queries"]:
            qid = query["qid"]
            url = "/".join([self.host, FEEDBACKENDPOINT, key, qid])
            r = requests.delete(url, headers=HEADERS)
            time.sleep(random.random())
            if r.status_code != requests.codes.ok:
                print r.text
                r.raise_for_status()

    def store_runs(self, key, runs):
        for qid in runs:
            run = runs[qid]
            run["runid"] = str(self.runid)
            url = "/".join([self.host, RUNENDPOINT, key, qid])
            r = requests.put(url, data=json.dumps(run), headers=HEADERS)
            time.sleep(random.random())
            if r.status_code != requests.codes.ok:
                print r.text
                r.raise_for_status()

    def update_runs(self, key, runs, feedbacks):
        for qid in runs:
            if qid in feedbacks and feedbacks[qid]:
                clicks = dict([(doc['docid'], 0) for doc in runs[qid]['doclist']])
                for feedback in feedbacks[qid]:
                    for doc in feedback["doclist"]:
                        if doc["clicked"] and doc["docid"] in clicks:
                            clicks[doc["docid"]] += 1
                runs[qid]['doclist'] = [{'docid': docid}
                                        for docid, _ in
                                        sorted(clicks.items(),
                                               key=lambda x: x[1],
                                               reverse=True)]
                print clicks
        self.runid += 1
        self.store_runs(key, runs)
        return runs

    def update_runid(self, old_runid):
        try:
            while int(old_runid) >= self.runid:
                self.runid += 1
        except ValueError:
            pass

    def simulate_runs(self, key, wait_min, wait_max):
        queries = self.get_queries(key)
        runs = {}
        for query in queries["queries"]:
            qid = query["qid"]
            runs[qid] = self.get_doclist(key, qid)
        feedbacks = {}
        feedback_update = self.get_feedback(key, "all")
        for elem in feedback_update['feedback']:
            self.update_runid(elem["runid"])
        while True:
            for elem in feedback_update['feedback']:
                qid = elem["qid"]
                if qid in feedbacks:
                    feedbacks[qid].append(elem)
                else:
                    feedbacks[qid] = [elem]
            runs = self.update_runs(key, runs, feedbacks)
            time.sleep(wait_min + (random.random() * (wait_max - wait_min)))
            feedback_update = self.get_feedback(key, "all", self.runid)

    def get_train(self, key):
        feedbacks = {}
        feedback_update = self.get_feedback(key, "all")
        for elem in feedback_update['feedback']:
            qid = elem["qid"]
            if qid in feedbacks:
                feedbacks[qid].append(elem)
            else:
                feedbacks[qid] = [elem]

        current_q = None
        nqid = 0
        queries = self.get_queries(key)
        for query in queries["queries"]:
            if "type" in query and query["type"] == "test":
                continue
            qid = query["qid"]
            if current_q is not None or current_q != qid:
                nqid += 1
            run = self.get_doclist(key, qid)
            skip = True
            clicks = dict([(doc['docid'], 0) for doc in run['doclist']])
            for fb in feedbacks[qid]:
                for doc in fb["doclist"]:
                    if doc["clicked"] and doc["docid"] in clicks:
                        clicks[doc["docid"]] += 1
                        skip = False
            if skip:
                continue
            for doc in run['doclist']:
                if "relevance_signals" not in doc:
                    continue
                docid = doc['docid']
                features = " ".join(["%d:%.4f" % tuple(fv)
                                     for fv in doc["relevance_signals"]])
                print "%d qid:%d %s # %s" % (clicks[docid],
                                             nqid,
                                             features,
                                             docid)

    def get_test(self, key):
        current_q = None
        nqid = 0
        queries = self.get_queries(key)
        for query in queries["queries"]:
            if "type" not in query or query["type"] != "test":
                continue
            qid = query["qid"]
            if current_q is not None or current_q != qid:
                nqid += 1
            run = self.get_doclist(key, qid)
            for doc in run['doclist']:
                if "relevance_signals" not in doc:
                    continue
                docid = doc['docid']
                features = " ".join(["%d:%.4f" % tuple(fv)
                                     for fv in doc["relevance_signals"]])
                print "-1 qid:%d %s # %s" % (nqid,
                                             features,
                                             docid)

    def store_run(self, key, run_file):
        runs = {}
        current_qid = None
        for line in open(run_file, "r"):
            qid, _, docid, _, _, _ = line.split()
            if current_qid is None or current_qid != qid:
                runs[qid] = {"doclist": []}
            runs[qid]["doclist"].append({"docid": docid})
            current_qid = qid
        self.store_runs(key, runs)

    def get_feedbacks(self, key):
        feedbacks = {}
        for elem in self.get_feedback(key, "all")['feedback']:
            qid = elem["qid"]
            if qid in feedbacks:
                feedbacks[qid].append(elem["doclist"])
            else:
                feedbacks[qid] = [elem["doclist"]]
        for qid, doclists in feedbacks.items():
            for doclist in doclists:
                print qid, " ".join([doc["docid"]
                                     for doc in doclist
                                     if doc["clicked"]])

if __name__ == '__main__':
    participant = Participant()
