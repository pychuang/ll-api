.. _ll4ir-results-round2:

LL4IR Round #2 Results
======================

This page presents the LL4IR Round #2 results. This round ran from Jun 15, 2015 till Jun 30, 2015.

#Impressions is the total number of times when rankings (for any of the test queries) from the given team/system have been displayed to users.
The number of wins, losses, and ties are calculated against the production system, where a win is defined as the experimental system having more clicks on results assigned to it by Team Draft Interleaving than clicks on results assigned to the production system.
Outcome is defined as #wins/(#wins+#losses). An outcome value below 0.5 means that the experimental system performed worse than the production system (i.e., in overall, it has more losses than wins).
(Note that we fixed the issue with the expected outcome that we encountered in the :ref:`LL4IR Official Results <ll4ir-results>`.) 

Participants can request the outcomes, for the entire query set (both test and train) as well as for each query individually, via :http:get:`/api/participant/outcome/(key)/(qid)`.

Product search
~~~~~~~~~~~~~~

======== ======= ===== ======= ===== ============
Teamname Outcome #Wins #Losses #Ties #Impressions 
======== ======= ===== ======= ===== ============
Baseline 0.5284	 93    83      598   774
UiS-Jern 0.4795	 82    89      596   767
GESIS    0.4520	 80    97      639   816
UiS-Mira 0.4389  79    101     577   757
UiS-UiS	 0.4118  84    120     527   731
IRIT	 0.3990  79    119     593   791
======== ======= ===== ======= ===== ============


Web search
~~~~~~~~~~

====================== ======= ===== ======= ===== ============
Teamname               Outcome #Wins #Losses #Ties #Impressions 
====================== ======= ===== ======= ===== ============
Exploitative Baseline  
Uniform Baseline       
====================== ======= ===== ======= ===== ============
