import requests, json

HOST = "http://127.0.0.1:5000/api"
QUERYENDPOINT = "site/query"
KEY = "6s4lwl4zpzu851hs"

headers = {'content-type': 'application/json'}

def store_queries():
    queries = [ 
                {
                    "qid": "q1011",
                    "qstr": "jaguar"
                }, 
                {
                    "qid": "q1112",
                    "qstr": "apple"
                }
              ]
    url = "/".join([HOST, QUERYENDPOINT, KEY])
    r = requests.put(url, data=json.dumps(queries), headers=headers)
    print r.text

if __name__ == '__main__':
    store_queries()
