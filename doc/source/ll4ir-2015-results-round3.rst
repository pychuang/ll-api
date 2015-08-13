.. _ll4ir-results-round3:

LL4IR Round #3 Results
======================

This page presents the LL4IR Round #3 results. This round ran from July 15, 2015 till July 30, 2015.

#Impressions is the total number of times when rankings (for any of the test queries) from the given team/system have been displayed to users.
The number of wins, losses, and ties are calculated against the production system, where a win is defined as the experimental system having more clicks on results assigned to it by Team Draft Interleaving than clicks on results assigned to the production system.
Outcome is defined as #wins/(#wins+#losses). An outcome value below 0.5 means that the experimental system performed worse than the production system (i.e., in overall, it has more losses than wins).
(Note that we fixed the issue with the expected outcome that we encountered in the :ref:`LL4IR Official Results <ll4ir-results>`.) 

Participants can request the outcomes, for the entire query set (both test and train) as well as for each query individually, via :http:get:`/api/participant/outcome/(key)/(qid)`.

Product search
~~~~~~~~~~~~~~

============ ======= ===== ======= ===== ============
Teamname     Outcome #Wins #Losses #Ties #Impressions
============ ======= ===== ======= ===== ============
Peter Dekker 0.5429  19    16      76    111*
Expected     0.5
IRIT         0.4890  89    93      533   715
UiS-Mira     0.4507  64    78      527   669
Baseline     0.4430  66    83      498   647
GESIS        0.4134  74    105     513   692
UiS-Jern     0.3702  67    114     511   692
UiS-UiS      0.3459  55    104     521   680
============ ======= ===== ======= ===== ============

*This team did not submit runs for all queries.

Web search
~~~~~~~~~~

====================== ======= ===== ======= ===== ============
Teamname               Outcome #Wins #Losses #Ties #Impressions 
====================== ======= ===== ======= ===== ============
Exploitative Baseline  0.5203  2161  1992    13206 17359
Expected               0.5
UvA-LambdaMart         0.2405  2264  7148    7863  17275
Uniform Baseline       0.2157  313   1138    922   2373*
====================== ======= ===== ======= ===== ============

*This team did not submit runs for all queries.
