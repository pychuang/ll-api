API Reference for Participants
==============================

We will provide a basic API for participants of the challenge to perform several actions such as obtaining a key, queries, documents and feedback. The API can also be used to update runs. Everything is implemented as HTTP request, and we use the request types GET, HEAD and PUT. We try to throw appropriate 4XX errors where possible.

.. note:: Please be nice to our API and don’t flood it with multiple cores constantly sending multiple requests. We will place a decent machine behind the API, but we might not be able to match yours.

.. autoflask:: ll.api:app
   :undoc-static:
   :include-empty-docstring:
