#!/usr/bin/env python

import argparse
import requests
import json
import datetime
import hashlib
from urlparse import urlparse, parse_qsl
from parser import logparser

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse uva.nl access logs for clicks to send to the Living Labs API.')
    parser.add_argument("--api", "-a", type=str,
                        default="http://living-labs.net/api/",
                        help="Living labs API location (default: %(default)s).")
    parser.add_argument("--key", "-k", type=str,
                        default="KEY-123",
                        help="API key (default: %(default)s).")
    parser.add_argument("--upload", "-u", action="store_true",
                        default=False,
                        help="Actually upload to the API (default: %(default)s).")
    args = parser.parse_args()
   
    feedbacks = {}
    for tm, url, ref in logparser():
        if "/search?q=" in ref and not url.startswith("http://static"):
            tm = datetime.datetime.strptime(tm, "%Y/%m/%d %H:%M:%S").strftime("%s")
            query = parse_qsl(urlparse(ref)[4])[0][1]
            site_qid = hashlib.sha1(query).hexdigest()
            site_docid = hashlib.sha1(url).hexdigest()
            apiurl = "/".join([args.api.strip("/"), "feedback", args.key, site_qid])
            if site_qid in feedbacks:
                data = feedbacks[site_qid]
                found = False
                for d in data["doclist"]:
                    if d["site_docid"] == site_docid:
                        d["clicked"].append(tm)
                        found = True
                        break
                if not found:
                    data["doclist"].append(
                        {"site_docid": site_docid,
                         "clicked": [tm],
                        })
            else:
                data = {"site_qid": site_qid,
                    "doclist": [
                    {   "site_docid": site_docid,
                        "clicked": [tm],
                    },
                    ]}
            feedbacks[site_qid] = data
            if args.upload:
                requests.put(apiurl,
                             data=json.dumps(data),
                             headers={'content-type': 'application/json'})
            else:
                print apiurl
                print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

