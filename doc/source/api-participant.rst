API Reference for Participants
==============================

We provide a basic API for participants of the Living Labs Challenge to perform 
several actions such as obtaining a key, queries, documents and feedback. The 
API can also be used to update runs. Everything is implemented as HTTP request,
and we use the request types GET, HEAD and PUT. We try to throw appropriate 4XX
errors where possible.

.. note:: Please be nice to our API and don't flood it with multiple cores 
	constantly sending multiple requests. We will place a decent machine behind 
	the API, but we might not be able to match yours.

Query
-----
.. autoflask:: ll.api.participant:app
   :endpoints: participant/query
   :undoc-static:
   :include-empty-docstring:


Doc
---
.. autoflask:: ll.api.participant:app
   :endpoints: participant/doc
   :undoc-static:
   :include-empty-docstring:


Feedback
--------
.. autoflask:: ll.api.participant:app
   :endpoints: participant/feedback
   :undoc-static:
   :include-empty-docstring:


Run
---
.. autoflask:: ll.api.participant:app
   :endpoints: participant/run
   :undoc-static:
   :include-empty-docstring:

