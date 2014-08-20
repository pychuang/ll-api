API Reference for Participants
==============================

We provide a basic API for participants of the Living Labs Challenge to perform
several actions such as obtaining a key, queries, documents and feedback. The
API can also be used to update runs. Everything is implemented as HTTP request,
and we use the request types GET, HEAD and PUT. We try to throw appropriate 4XX
errors where possible.


For all operations, an API key is required. Also, we require you to sign an
agreement. Details on that process will be shared once you sign up.
The dashboard that you can use to obtain an API key is here:
http://living-labs.net:5001/

Our API is located at this location: http://living-labs.net:5000/api/.

.. note:: Please be nice to our API and don't flood it with multiple cores 
	constantly sending multiple requests. We will place a decent machine behind 
	the API, but we might not be able to match yours.
	To enforce this a little bit, we have rate limited the API to 300 calls 
	per minute or 10 calls per second, whichever hits first. Please do let us 
	know if this is causing you any problems.


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


Doclist
-------
.. autoflask:: ll.api.participant:app
   :endpoints: participant/doclist
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

