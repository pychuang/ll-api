#!/usr/bin/env python

import argparse
import requests
import json
import hashlib
from urlparse import urlparse, parse_qsl
from collections import Counter
from bs4 import BeautifulSoup

from parser import logparser


def get_content(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    content = soup.find("div", id="main", role="main")
    if content is None:
        print soup

def get_top(query, topsize):
    url = "http://www.uva.nl/search?page=1&pageSize=%d&q=%s&type=subject" % (topsize, query)
    print url
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    return [link.get("href") for link in soup.find("ul", "searchlist").find_all("a")]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse uva.nl access logs for queries to send to the Living Labs API.')
    parser.add_argument("--api", "-a", type=str,
                        default="http://living-labs.net/api/",
                        help="Living labs API location (default: %(default)s).")
    parser.add_argument("--key", "-k", type=str,
                        default="KEY-123",
                        help="API key (default: %(default)s).")
    parser.add_argument("--upload", "-u", action="store_true",
                        default=False,
                        help="Actually upload to the API (default: %(default)s).")
    parser.add_argument("--size", "-s", type=int, default=5)
    parser.add_argument("--topsize", "-t", type=int, default=5)
    args = parser.parse_args()
    
    queries = Counter()
    for _, url, _ in logparser():
        if "/search?q=" in url:
            query = parse_qsl(urlparse(url)[4])[0][1]
            queries[query] += 1
    data = {"queries": []}
    tops = {} 
    for query, _ in queries.most_common(args.size):
        site_qid = hashlib.sha1(query).hexdigest()
        data["queries"].append({"qstr": query,
                                "site_qid": site_qid})    
        tops[query] = get_top(query, args.topsize)

    apiurl = "/".join([args.api.strip("/"), "query", args.key])
    if args.upload:
        requests.put(apiurl,
                     data=json.dumps(data),
                     headers={'content-type': 'application/json'})
    else:
        print apiurl
        print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        for q in tops:
            for url in tops[q]:
                print q, url
                get_content(url)
                print

