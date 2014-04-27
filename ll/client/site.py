import argparse
import requests, json

HOST = "http://127.0.0.1:5000/api"
QUERYENDPOINT = "site/query"

headers = {'content-type': 'application/json'}

def store_queries(key):
    queries = [ 
                {
                    "site_qid": "48474c1ab6d3541d2f881a9d4b3bed75",
                    "qstr": "jaguar"
                }, 
                {
                    "site_qid": "30c6677b833454ad2df762d3c98d2409",
                    "qstr": "apple"
                },
                {
                    "site_qid": "e30c6677b833454ad2df762d3c98d2409",
                    "qstr": "applepie"
                }
              ]
    url = "/".join([HOST, QUERYENDPOINT, key])
    r = requests.put(url, data=json.dumps(queries), headers=headers)
    print r.text

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Living Labs Challenge's API Server")
    parser.add_argument('--key', type=str, required=True,
                        help='Provide a user key.')
    parser.add_argument('-q', '--store_queries', action="store_true", default=False,
                        help='Store some queries.')
    args = parser.parse_args()
    if args.store_queries:
        store_queries(args.key)
