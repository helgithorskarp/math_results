# Verdict

ACCEPT_AND_STRENGTHEN_EXACT_FOUR at the exact frozen scope. I independently
reviewed target commit `bcb699cc9890480c93c24716155a7fb5f4b5cea1`. The
selected support is a genuine plane unit-distance graph on 508 distinct points
with all 2,506 unit edges, and its chromatic number is exactly four. It is not
a five-chromatic candidate or a record improvement.

# Independent exact method

The standard-library checker imports neither target executable. It pins the
four original inputs and independently reconstructs all 632 archived points
as numerator rows over 96 in the basis
`1,sqrt(3),sqrt(5),sqrt(15),sqrt(11),sqrt(33),sqrt(55),sqrt(165)`.
Reviewer-owned Cartesian field multiplication decides all 199,396 pairs,
recovering 3,112 unit edges. The H516 source has 516 points and 2,538 complete
unit edges; its only degree-four vertices are exactly
`102,109,293,296,299,302,305,308,569,578`.

Deleting those vertices leaves 506 points and 2,498 unit edges. Among H632
unit pairs wholly outside H560, exactly 20 pairs have at least three contacts
from each endpoint to the retained support. The first is `(399,576)`. Its old
contacts are `399:{346,392,421,441}` and `576:{393,421,431}`, and the new
points are adjacent. Exact re-enumeration of all 128,778 final pairs gives the
edge split 2,498 old--old, seven old--new and one new--new. Point and edge
hashes match the target byte-for-byte.

The supplied four-word is checked on all edges. A fresh deterministic DSATUR
search, without the supplied word or a SAT solver, finds a different proper
four-word in 124,657 nodes; its SHA-256 is
`5311366138cdcd403fbf5979f7d3f83a9b59af1cb00ddbf77e86c7605a5745e8`.

# Strengthening

The seven Moser-witness vertices have original labels
`0,294,145,164,310,143,162`. All lie in the retained H506; neither added point
is used. The eleven checked edges give the elementary two-diamond Moser
lower bound. Restricting the checked four-word gives exact chromatic number
four for the complete retained H506 (506/2498), H506 plus 399 (507/2502),
H506 plus 576 (507/2501), and the full exchange (508/2506). Thus the added
coupled edge is geometrically valid but supplies no ordinary chromatic forcing.

Public review evidence:
https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_h516_coupled_edge_exchange_stop_review1

# Limitations and graph status

This is one frozen pair after one frozen deletion. It says nothing about the
other 19 eligible archived pairs, altered deletions, arbitrary two-point
placements, moved realizations or global sub-509 existence. The whole-plane
one-point closure h3999/h4003 is narrower and does not contain this support;
that scope distinction does not make the present graph positive.

Discovery was stale at indexed height 4,363 versus RPC 4,364. The target's
CheckTx-zero broadcast was absent from the committed graph and was not
resubmitted. Therefore this review cannot yet attach a committed VERIFIES
relation to it; the target reference is cited in the body only as pending.
