import json
import sys
import pymongo

import ll.core
from ll.core.db import db

if len(sys.argv)>1:
    collection = sys.argv[1]
    filename = "dump/ll/" + sys.argv[1] + ".metadata.json"
    f=open(filename,"r")

    structure = json.load(f)
    attr_list = structure[u"indexes"]
    for item in attr_list:
        if u"key" in item:
            index = item[u"key"]
            print(item[u"key"])
            print(collection)
            if(collection==u"user"):
                db.user.create_index(index)
            if(collection==u"site"):
                db.site.create_index(index)
            if(collection==u"doc"):
                db.doc.create_index(index)
            if(collection==u"feedback"):
                db.feedback.create_index(index)
            if(collection==u"run"):
                db.run.create_index(index)
