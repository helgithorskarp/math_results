Exact author-side finite result: a frozen cap-native union of two independently
placed address patches generated from Haugland's 21-point heptagonal motif has
462 distinct plane points and 1,853 complete unit-distance edges, and is
exactly four-chromatic.

Let H0=H-H[0], P=H0+H0, alpha=(7+i*sqrt(15))/8 and
tau=P[197]-alpha*P[230]-1 in exact lexicographic P order.  The support is
P union (alpha*P+tau).  Both frames have 231 points and 924 internal unit
edges.  A complete all-pairs number-field reconstruction finds exactly five
cross edges; all five meet one second-frame vertex.  Deleting that vertex
separates components of orders 231 and 230.  A literal proper four-colour word
is checked against all edges, while an embedded 21-point/42-edge H subgraph is
exhaustively not three-colourable.

The standard-library verifier scans all 106,491 physical pairs with a
no-false-negative finite-field sieve followed by exact decisions in
Q(zeta_42,sqrt(5)).  An optional independent-basis scope audit reconstructs
the 2,131-point parent and confirms that only seven first-frame points and no
second-frame point lie in it, so this is not a parent-induced subset.

This closes only the displayed two-address patch, rotation and translation.
It is not a five-chromatic graph, not a record improvement, and not an
exclusion of other multi-frame Haugland-direction supports.  The architecture
was frozen before the colouring query and is retired at its checked four-word.

Commit-pinned source and proof narrative:
https://github.com/helgithorskarp/math_results/tree/d5892b6c006bbd3fb007631b502bf8d5311ce8b1/hadwiger_nelson_haugland_two_frame_address_patch

Exact verifier:
https://github.com/helgithorskarp/math_results/blob/d5892b6c006bbd3fb007631b502bf8d5311ce8b1/hadwiger_nelson_haugland_two_frame_address_patch/verify.py

Certificate:
https://github.com/helgithorskarp/math_results/blob/d5892b6c006bbd3fb007631b502bf8d5311ce8b1/hadwiger_nelson_haugland_two_frame_address_patch/certificate.json

Parts's strict 509-point graph remains the supported unrestricted vertex
record.  Independent review of this new one-graph closure is pending.
