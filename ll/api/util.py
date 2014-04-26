
def wrap_user(user):
    rdict = {"user": 
        { "teamname": user["teamname"],
          "email": user["email"],
        }}

def wrap_queries(user, queries):
    rdict = wrap_user(user)
    rdict["queries"] = []
    for q in queries:
        rdict["queries"].append({
            "qid": q["qid"],
            "qstr": q["qstr"],
        })
    return rdict
