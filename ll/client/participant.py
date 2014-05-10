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


def get_queries(key):
    url = "/".join([HOST, QUERYENDPOINT, key])
    r = requests.get(url, headers=HEADERS)
    print r.json()
    r.raise_for_status()
    return r.json()


def get_doclist(key, qid):
    url = "/".join([HOST, DOCLISTENDPOINT, key])
    r = requests.get(url, headers=HEADERS)
    print r.json()
    r.raise_for_status()
    return r.json()


def get_feedback(key):
    url = "/".join([HOST, FEEDBACKENDPOINT, key])
    r = requests.get(url, headers=HEADERS)
    print r.json()
    r.raise_for_status()
    return r.json()


def update_runs(runs, feedback):
    #TODO: Implement baseline
    return runs


def store_runs(key, doclist):
    url = "/".join([HOST, RUNENDPOINT, key])
    r = requests.put(url, data=json.dumps(doclist), headers=HEADERS)
    print r.json()
    r.raise_for_status()


def simulate_runs(key):
    queries = get_queries(key)
    runs = {}
    for qid in queries:
        runs[qid] = get_doclist(key, qid)

    while True:
        feedback = get_feedback(key)
        runs = update_runs(runs, feedback)
        store_runs(key, runs)
        time.sleep(5)

if __name__ == '__main__':
    description = "Living Labs Challenge's Participant Client"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-k', '--key', type=str, required=True,
                        help='Provide a user key.')
    parser.add_argument('-s', '--simulate_runs', action="store_true",
                        default=False,
                        help='Simulate runs.')
    args = parser.parse_args()
    if args.simulate_runs:
        simulate_runs(args.key)
