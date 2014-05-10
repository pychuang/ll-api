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
        print r.json()
        r.raise_for_status()
        return r.json()

    def get_doclist(self, key, qid):
        url = "/".join([HOST, DOCLISTENDPOINT, key, qid])
        r = requests.get(url, headers=HEADERS)
        print r.json()
        r.raise_for_status()
        return r.json()

    def get_feedback(self, key):
        url = "/".join([HOST, FEEDBACKENDPOINT, key])
        r = requests.get(url, headers=HEADERS)
        print r.json()
        r.raise_for_status()
        return r.json()

    def store_runs(self, key, runs):
        for qid in runs:
            run = runs[qid]
            run["runid"] = str(self.runid)
            url = "/".join([HOST, RUNENDPOINT, key, qid])
            r = requests.put(url, data=json.dumps(run), headers=HEADERS)
            print r.json()
            r.raise_for_status()

    def update_runs(self, key, runs, feedback):
        #TODO: Implement baseline
        if True:
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
            feedback = self.get_feedback(key)
            runs = self.update_runs(key, runs, feedback)
            time.sleep(5)

if __name__ == '__main__':
    participant = Participant()
