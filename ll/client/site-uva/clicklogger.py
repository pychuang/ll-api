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
import datetime
import hashlib
from urlparse import urlparse, parse_qsl

from parser import logparser, argparser

if __name__ == "__main__":
    args = argparser.parse_args()
   
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

