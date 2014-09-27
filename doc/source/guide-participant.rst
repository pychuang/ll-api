.. _guide:

Guide for CLEF Participants
===========================

This guide is meant to be a practical guide to participating in the CLEF Living
Lab.
Since we deviate significantly from the typical TREC style evaluation setup
that most participants are likely to be familiar with, we will focus primarily
on those differences.


Participating in the lab involves following these steps:

#.	Read the `lab description <http://living-labs.net/clef-lab/>`_ and  :ref:`key` below.
#.	Sign up:

	#.	`Register <http://living-labs.net:5001/user/register/>`_ starting 3 November 2014.
	#.	Sign and send the agreement form. You will receive a link to this form.
	#.	Sign up for individual sites (use-cases) you want to obtain data for. You will receive a link by email to do so.

#.	Implement your method as a client that can talk to the API. Examples are provided. See :ref:`method` below.
#.	Run your client:

	#. See :ref:`run` below.
	#. When the test phase starts, submit your test runs.

#.	Write up your findings. Publication details will become available.
#.	Come to and present your work at `CLEF 2014 in Toulouse <http://clef2015.clef-initiative.eu/CLEF2015/>`_ in September 2015.

We hope that all steps but 3. and 4. are self explanatory. Below we detail these two steps.


.. _key:

Key Concepts
------------
But, first some key concepts some of which may come as a surprise and that you
will need to be aware of.

-	Frequent queries and offline processing
	
	We use frequent queries because these allow participants of the lab to
	prepare their runs offline. Since these queries are frequent, users
	are likely to issue them again at which point a run from participants
	is presented.
	
-	Feedback is *not* immediate

	Feedback comes from real users. That means that real users have to enter
	a query that is part of the lab into the search box on the site. They
	then have to click a link and this click has to be fed back into the API.
	There is bound to be a significant delay between submitting a run and
	the feedback becoming available.
	
-	Feedback is noisy

	Feedback, such as clicks, can not be used as if it were relevance
	judgments. Users click for many reasons. For instance, if a ranking shown
	is really bad, users may start clicking on all links in the rank out of
	despair in which case a click actually signals negative relevance.

-	Interleaving

	Your ranking may not be shown to users directly, it can be interleaved with
	the current production system of the site. This means that only about half
	the documents shown to a users actually come from your ranking. This is 
	generally done for two reasons: it allows pairwise comparisons between your
	ranking and the sites ranking. But also, it reduces the risk of showing bad
	rankings to users.

.. _method:

Implement a Client
------------------

We advise you to first familiarize yourself with the :ref:`api-participants`. 



.. _run:

Run a Client
------------

