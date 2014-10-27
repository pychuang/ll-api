.. _api-participants:

API Reference for Participants
==============================

.. note:: Please refer the :ref:`guide` before reading this.


We provide a basic API for participants of the CLEF Living Labs  to perform
several actions such as obtaining a key, queries, documents and feedback. The
API can also be used to update runs. Everything is implemented as HTTP request,
and we use the request types GET, HEAD and PUT. We try to throw appropriate 4XX
errors where possible.
Note that participants are free to implement their own client to communicate
with this API. However, example clients are provided by the organization.


For all operations, an API key is required. Also, we require you to sign an
agreement. Details on that process will be shared once you sign up.
The dashboard that you can use to obtain an API key is here:
http://living-labs.net:5001/

Our API is located at this location: http://living-labs.net:5000/api/.

.. note:: We have rate limited the API to 300 calls per minute or 10 calls per 
	second, whichever hits first. Please do let us know if this is causing you
	any problems.


Query
-----
From each site that a participant signed up for (see 
http://living-labs.net:5001/user/sites/), a sample of (N=100) queries is made
available. This endpoint allows for downloading these queries.

.. autoflask:: ll.api.participant:app
   :endpoints: participant/query
   :undoc-static:
   :include-empty-docstring:


Doclist
-------
For each query, there is a fixed set of documents available. These documents
are selected by the site. And this selection may change over time. Therefore,
participants should update the doclist for a query on a regular (daily?) 
basis.

For some use cases, the doclist will contain relevance signals (also referred
to as features, or ranking signals). These are always sparse representations, 
missing values can be assumed to be zeros. The relevance signals can be query
only, document only, or query document dependent. 
For these uses cases, the actual query and document content are generally not
provided.
The use cases that do not have relevance signals, will need to provide query
and document content.

.. autoflask:: ll.api.participant:app
   :endpoints: participant/doclist
   :undoc-static:
   :include-empty-docstring:


Doc
---
When a use case does not define relevance signals for each query document pair
then this is where the content of documents is made available.

.. autoflask:: ll.api.participant:app
   :endpoints: participant/doc
   :undoc-static:
   :include-empty-docstring:


Run
---
Runs (TREC terminology) are just rankings of document ids as shown to actual
users. Participants can keep updating their runs. They also have the option
of updating an identifier for the run. This identifier is then used in the
feedback that is returned.

.. autoflask:: ll.api.participant:app
   :endpoints: participant/run
   :undoc-static:
   :include-empty-docstring:

Feedback
--------
.. autoflask:: ll.api.participant:app
   :endpoints: participant/feedback
   :undoc-static:
   :include-empty-docstring:
