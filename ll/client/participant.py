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

import base64
import argparse
import requests
import json
import time
import datetime
import random
import os


QUERYENDPOINT = "participant/query"
DOCENDPOINT = "participant/doc"
DOCLISTENDPOINT = "participant/doclist"
RUNENDPOINT = "participant/run"
FEEDBACKENDPOINT = "participant/feedback"

HEADERS = {'content-type': 'application/json'}


class Participant():
    def __init__(self):
        path = os.path.dirname(os.path.realpath(__file__))
        description = "Living Labs Challenge's Participant Client"
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument('--host', dest='host', default='http://127.0.0.1',
                        help='Host to listen on.')
        parser.add_argument('--port', dest='port', default=5000, type=int,
                        help='Port to listen on.')
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
        parser.add_argument('--wait_min', type=int, default=1,
                            help='Minimum simulation waiting time in seconds.')
        parser.add_argument('--wait_max', type=int, default=10,
                            help='Max simulation waiting time in seconds.')

        args = parser.parse_args()

        self.host = "%s:%s/api" % (args.host, args.port)

        self.runid = 0

        if args.simulate_runs:
            self.simulate_runs(args.key, args.wait_min, args.wait_max)

        if args.store_run:
            self.store_run(args.key, args.run_file)

        if args.get_feedback:
            self.get_feedbacks(args.key)

    def get_queries(self, key):
        url = "/".join([self.host, QUERYENDPOINT, key])
        r = requests.get(url, headers=HEADERS)
        if r.status_code != requests.codes.ok:
            print r.text
            r.raise_for_status()
        return r.json()

    def get_doclist(self, key, qid):
        url = "/".join([self.host, DOCLISTENDPOINT, key, qid])
        r = requests.get(url, headers=HEADERS)
        if r.status_code != requests.codes.ok:
            print r.text
            r.raise_for_status()
        return r.json()

    def get_feedback(self, key, qid):
        url = "/".join([self.host, FEEDBACKENDPOINT, key, qid])
        r = requests.get(url, headers=HEADERS)
        if r.status_code != requests.codes.ok:
            print r.text
            r.raise_for_status()
        return r.json()

    def store_runs(self, key, runs):
        for qid in runs:
            run = runs[qid]
            run["runid"] = str(self.runid)
            url = "/".join([self.host, RUNENDPOINT, key, qid])
            r = requests.put(url, data=json.dumps(run), headers=HEADERS)
            if r.status_code != requests.codes.ok:
                print r.text
                r.raise_for_status()

    def update_runs(self, key, runs, feedbacks):
        for qid in runs:
            if qid in feedbacks and feedbacks[qid]['feedback']:
                clicks = dict([(doc['docid'], 0)
                               for doc in runs[qid]['doclist']])
                for feedback in feedbacks[qid]['feedback']:
                    for doc in feedback["doclist"]:
                        if doc["clicked"]:
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

    def simulate_runs(self, key, wait_min, wait_max):
        queries = self.get_queries(key)
        runs = {}
        for query in queries["queries"]:
            qid = query["qid"]
            runs[qid] = self.get_doclist(key, qid)
        while True:
            feedbacks = {}
            for query in queries["queries"]:
                qid = query["qid"]
                feedbacks[qid] = self.get_feedback(key, qid)
            runs = self.update_runs(key, runs, feedbacks)
            time.sleep(wait_min + (random.random() * (wait_max - wait_min)))

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
        queries = self.get_queries(key)
        for query in queries["queries"]:
            qid = query["qid"]
            feedbacks = self.get_feedback(key, qid)
            for feedback in feedbacks['feedback']:
                print qid, " ".join([doc["docid"]
                                     for doc in feedback["doclist"]
                                     if doc["clicked"]])

if __name__ == '__main__':
    participant = Participant()
