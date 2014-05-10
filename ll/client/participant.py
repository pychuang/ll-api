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

HOST = "http://127.0.0.1:5000/api"

QUERYENDPOINT = "participant/query"
DOCENDPOINT = "participant/doc"
DOCLISTENDPOINT = "participant/doclist"
RUNENDPOINT = "participant/run"
FEEDBACKENDPOINT = "participant/feedback"

HEADERS = {'content-type': 'application/json'}


class Participant():
    def __init__(self):
        description = "Living Labs Challenge's Participant Client"
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument('-k', '--key', type=str, required=True,
                            help='Provide a user key.')
        parser.add_argument('-s', '--simulate_runs', action="store_true",
                            default=False,
                            help='Simulate runs.')
        args = parser.parse_args()

        self.runid = 0

        if args.simulate_runs:
            self.simulate_runs(args.key)

    def get_queries(self, key):
        url = "/".join([HOST, QUERYENDPOINT, key])
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
        return r.json()

    def get_doclist(self, key, qid):
        url = "/".join([HOST, DOCLISTENDPOINT, key, qid])
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
        return r.json()

    def get_feedback(self, key, qid):
        url = "/".join([HOST, FEEDBACKENDPOINT, key, qid])
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
        return r.json()

    def store_runs(self, key, runs):
        for qid in runs:
            run = runs[qid]
            run["runid"] = str(self.runid)
            url = "/".join([HOST, RUNENDPOINT, key, qid])
            r = requests.put(url, data=json.dumps(run), headers=HEADERS)
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

    def simulate_runs(self, key):
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
            time.sleep(random.random())

if __name__ == '__main__':
    participant = Participant()
