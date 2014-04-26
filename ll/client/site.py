import requests, json

HOST = "http://127.0.0.1:5000/api"
QUERYENDPOINT = "site/query"
KEY = "6s4lwl4zpzu851hs"

headers = {'content-type': 'application/json'}

def store_queries():
    queries = {
        "queries": [
        (
            "q0", 
            "jaguar"
        ), 
        (
            "q1",
            "apple"
        ),
        ]
    }
    data = json.dumps(queries)
    url = "/".join([HOST, QUERYENDPOINT, KEY])
    r = requests.put(url, data, headers=headers)
    print str(r.json)

if __name__ == '__main__':
    store_queries()
