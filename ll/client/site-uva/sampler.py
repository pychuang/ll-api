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

import requests
import json
import hashlib
from urlparse import urlparse, parse_qsl
from collections import Counter
from bs4 import BeautifulSoup

from parser import logparser, argparser


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
    argparser.add_argument("--size", "-s", type=int, default=20)
    argparser.add_argument("--topsize", "-t", type=int, default=5)
    args = argparser.parse_args()
    
    queries = Counter()
    for _, url, _ in logparser():
        if "/search?q=" in url:
            try:
                query = parse_qsl(urlparse(url)[4])[0][1]
            except:
                continue
            queries[query] += 1
#    data = {"queries": []}
#    tops = {} 
    for query, count in queries.most_common(args.size):
        print query, count
#        site_qid = hashlib.sha1(query).hexdigest()
#        data["queries"].append({"qstr": query,
#                                "site_qid": site_qid})    
#        tops[query] = get_top(query, args.topsize)
#
#    apiurl = "/".join([args.api.strip("/"), "query", args.key])
#    if args.upload:
#        requests.put(apiurl,
#                     data=json.dumps(data),
#                     headers={'content-type': 'application/json'})
#    else:
#        print apiurl
#        print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
#        for q in tops:
#            for url in tops[q]:
#                print q, url
#                get_content(url)
#                print
