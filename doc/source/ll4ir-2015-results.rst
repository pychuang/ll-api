.. _ll4ir-results:

LL4IR Official Results
======================

This page presents the official results for the LL4IR CLEF 2015 Lab.

This round ran from May 1, 2015 till May 15, 2015.

#Impressions is the total number of times when rankings (for any of the test queries) from the given team/system have been displayed to users.
The number of wins, losses, and ties are calculated against the production system, where a win is defined as the experimental system having more clicks on results assigned to it by Team Draft Interleaving than clicks on results assigned to the production system.
Outcome is defined as #wins/(#wins+#losses). Typically, an outcome value below 0.5 means that the experimental system performed worse than the production system (i.e., in overall, it has more losses than wins).
For the Product search use case however, the expect outcomes was 0.28. Please see the Overview paper for details.
(Note that we fixed this issue with the expected outcome in the :ref:`LL4IR Round #2 Results <ll4ir-results-round2>`.) 

Participants can request the outcomes, for the entire query set (both test and train) as well as for each query individually, via :http:get:`/api/participant/outcome/(key)/(qid)`. 


Product search
~~~~~~~~~~~~~~

======== ======= ===== ======= ===== ============
Teamname Outcome #Wins #Losses #Ties #Impressions 
======== ======= ===== ======= ===== ============
Baseline 0.4691  91    103     467   661
UiS-Mira 0.3413  71    137     517   725
UiS-Jern 0.3277  58    119     488   665
UiS-UiS  0.2827  54    137     508   699
GESIS    0.2685  40    109     374   523
======== ======= ===== ======= ===== ============


Web search
~~~~~~~~~~

====================== ======= ===== ======= ===== ============
Teamname               Outcome #Wins #Losses #Ties #Impressions 
====================== ======= ===== ======= ===== ============
Exploitative Baseline  0.5527  3030  2452    19055 24537
Uniform Baseline       0.2161  430   1560    1346  3336
====================== ======= ===== ======= ===== ============
