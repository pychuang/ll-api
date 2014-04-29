API Reference for Sites
=======================

We provide a basic API for sites. We use the term 'sites' to refer to search engines that dedicate a (small) part of their traffic to evaluating runs from participants of the Living Labs Challenge.
This API can be used by sites to update the query set, the documents and to retreive rankings. For each retreived ranking, the site is expected to provide feedback.
Everything is implemented as HTTP request, and we use the request types GET, HEAD and PUT. We try to throw appropriate 4XX errors where possible.

.. toctree::
    :maxdepth: 2

Query
-----
.. autoflask:: ll.api.site:app
   :endpoints: site/query
   :undoc-static:
   :include-empty-docstring:

Doc
---
.. autoflask:: ll.api.site:app
   :endpoints: site/doclist
   :undoc-static:
   :include-empty-docstring:

Doclist
-------
.. autoflask:: ll.api.site:app
   :endpoints: site/doclist
   :undoc-static:
   :include-empty-docstring:


Feedback
--------
.. autoflask:: ll.api.site:app
   :endpoints: site/feedback
   :undoc-static:
   :include-empty-docstring:

Ranking
-------
.. autoflask:: ll.api.site:app
   :endpoints: site/ranking
   :undoc-static:
   :include-empty-docstring:
