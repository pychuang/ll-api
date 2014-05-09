from db import db
import random
import site


def get_ranking(site_id, site_qid):
    query = db.query.find_one({"site_id": site_id, "site_qid": site_qid})
    if query == None:
        raise Exception("Query not found: site_qid = '%s'. Only rankings for"
                        "existing queries can be expected." % site_qid)
    run = get_run(site_qid)
    feedback = {
        "_id": site.next_sid(site_id),
        "site_qid": site_qid,
        "qid": query["_id"],
        "rid": run["_id"],
    }
    db.feedback.save(feedback)
    return run


def get_run(site_qid):
    runs = db.run.find(site_qid=site_qid)
    if not runs.count():
        raise Exception("No runs avaliable")
    participants = set()
    for run in runs:
        participants.add(run["participants_id"])
    participant = random.choice(list(participants))
    last = 0
    selectedrun = None
    for run in runs:
        if run["participants_id"] != participant:
            continue
        if run["creation_time"] > last:
            last = run["creation_time"]
            selectedrun = run
    return selectedrun
