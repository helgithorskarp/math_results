The independently reviewed opposed-B214 conditional core has 241 distinct
plane points and 991 complete unit edges.  Eight explicit proper
four-colourings give 241 distinct eight-symbol vertex signatures.  Hence for
every pair of distinct vertices, at least one checked proper four-colouring
assigns them different colours: the graph has no forced-equal pair.  The same
holds in every induced subgraph by restriction.

This closes a concrete record-scale route.  A forced-equal pair at distance at
least 1/2 would yield a non-four two-copy spindle on at most 2*241-1=481
physical points.  Exact comparison finds 27,010 pairs above that distance
threshold and no pair exactly on it, but the signature certificate separates
all 28,920 pairs.  No union or phase family is generated after the failed
premise.

The standard-library verifier reconstructs the core from the archived B214
table, collision-merges exact coordinates, tests every physical pair, checks
all eight words on all 991 edges, verifies the signature injection, and
rechecks exact four-chromaticity from the embedded Golomb graph.  Canonical
SHA-256 values are points
70c14dfaec7875038c0f3cc1b9f84f5469143f5227fbd49377340bb46e27d908,
edges 02e1fbb4c9f94cc5aca57945657706088e25560d3ca0c00217d0d17d647f55ab,
and word stream
0e88e2bf0d0c306238db2bdaee31224f89cf04c299f897f3d8b3694981fa3dd0.
Only positive colour words are trusted; no solver UNSAT result is used.

Scope is exactly this 241-point physical core and its induced subgraphs.  The
result does not classify higher-arity relations, other extractions or other
sources, and it is not a five-chromatic graph or record progress.  Reproducible
source at mathematical commit b1b1bf00c80b0524956a889ceb3a82920b3571dc:
https://github.com/helgithorskarp/math_results/tree/b1b1bf00c80b0524956a889ceb3a82920b3571dc/hadwiger_nelson_opposed241_equal_pair_gate
