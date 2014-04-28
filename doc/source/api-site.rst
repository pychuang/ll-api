API Reference for Sites
=======================

We provide a basic API for sites. We use the term 'sites' to refer to search engines that dedicate a (small) part of their traffic to evaluating runs from participants of the Living Labs Challenge.
This API can be used by sites to update the query set, the documents and to retreive rankings. For each retreived ranking, the site is expected to provide feedback.
Everything is implemented as HTTP request, and we use the request types GET, HEAD and PUT. We try to throw appropriate 4XX errors where possible.


.. autoflask:: ll.api.site:app
   :endpoints: site/query, site/doc, site/ranking, site/feedback, site/doclist
   :undoc-static:
   :include-empty-docstring:
