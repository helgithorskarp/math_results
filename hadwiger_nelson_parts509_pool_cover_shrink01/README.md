# Smaller killing sets in the Parts sealed pool

**Exact positive certificate.** Recolouring gives strict subset
replacements for all sixteen killing sets in the
[previous cover extension](../hadwiger_nelson_parts509_pool_cover_residual30/README.md#sixteen-additional-irredundant-killing-sets).
The sum of their sizes decreases from 539 to 205.
This restores 334 vertex occurrences across the sixteen separately
coloured graphs. Every replacement has a directly checked proper
four-colouring of its complement. These are stronger positive clauses,
not a five-chromatic graph or an additional shape closure.

## Statement and proof

Use the committed labels L={0,...,373}, S={374,...,508}, and the
specified 168-point Q5 in
[pool_S.json](../hadwiger_nelson_parts509_s_replacement_budget/pool_S.json).
Write U=S union Q5, sorted by global label. All L vertices remain present.
Let D_i be row i of the previous
[refinements.json](../hadwiger_nelson_parts509_pool_cover_residual30/refinements.json).

[colourings.json](colourings.json) gives D'_i subset D_i, an explicit
374-character L-colouring `l`, and a 303-character pool colouring `c`,
with dots exactly on D'_i. The resulting colouring is proper on
G_i=L union (U minus D'_i). The original and new colourings are both
checked directly on every surviving unit edge. Indices and subset
relations are checked explicitly.

| Parent index | Original size | New size | New S part | New Q5 part |
| --- | ---: | ---: | ---: | ---: |
| 0 | 40 | 9 | 7 | 2 |
| 1 | 19 | 5 | 3 | 2 |
| 2 | 39 | 3 | 2 | 1 |
| 3 | 27 | 17 | 3 | 14 |
| 4 | 28 | 6 | 6 | 0 |
| 5 | 32 | 6 | 3 | 3 |
| 6 | 37 | 14 | 7 | 7 |
| 7 | 31 | 12 | 5 | 7 |
| 8 | 39 | 4 | 4 | 0 |
| 9 | 22 | 20 | 7 | 13 |
| 10 | 35 | 10 | 6 | 4 |
| 11 | 32 | 24 | 9 | 15 |
| 12 | 41 | 5 | 3 | 2 |
| 13 | 45 | 41 | 18 | 23 |
| 14 | 40 | 15 | 7 | 8 |
| 15 | 32 | 14 | 7 | 7 |

The smallest supplied set, `[413, 436, 853]`, is
certified by a proper four-colouring of all 674
remaining points and their 3370 strict unit edges.

For any X subset U whose graph L union X is not four-colourable,
X must meet each D'_i: otherwise G_i's colouring restricts to L union X.
Thus the positive clause `OR(x_v for v in D'_i)` is valid. Since D'_i is
a subset of D_i, the new clause implies the old one and preserves every
exclusion obtained from it. Strict subset inclusion makes it a strictly
stronger clause on unrestricted Boolean assignments; we do not assert
that it strictly reduces every already-constrained master domain.

The supplied family has 16 distinct sets.
`rows_surviving_family_subset_pruning` in [expected.json](expected.json)
describes only literal-set containment within these sixteen rows.
It is not a claim that any deletion set is minimal under recolouring.

The following certified sets lie entirely in S, so every such
non-four-colourable selection must retain at least one vertex from each:

- Row 4: `[384, 386, 412, 461, 474, 495]`.
- Row 8: `[385, 441, 456, 467]`.

The earlier irredundancy theorem remains a theorem about the earlier
family. No irredundancy claim for this new family is needed here.
Nor is any new lower bound on the total selected vertex count asserted.

## Solver-free reproduction

From a full repository checkout, using Python 3.11's standard library:

```sh
python3 hadwiger_nelson_parts509_pool_cover_shrink01/verify.py
```

Expected: `SUBSET KILLING CERTIFICATES VERIFIED`, with
`improved_rows: 16` and `final_total: 205`.
[manifest.json](manifest.json) pins every input, including the original
sixteen rows and the new colourings. The exact per-row counts are in
[expected.json](expected.json). No SAT solver, private input, network
access or negative proof trace is required.

The verifier uses the independently reviewed
[integer geometry reader](../hadwiger_nelson_parts509_pool_shape6_review1/independent_check.py).
It reconstructs all 228,826 pairs of 677 distinct points at common
denominator 288 in Q(sqrt(3),sqrt(5),sqrt(11)), recovering 3,400 exact unit
edges. A separate author audit rebuilt the points from the original
Mathematica source and checked the whole accepted transition chain and
final family with bitsets. This is a second implementation check by the
author, not external peer review or proof-assistant formalization.

## Discovery and limits

One bounded batch attempted to restore deleted vertices while allowing
all present colours to change. Queries used a full two-bit graph-colouring
CNF, with the exact L-triangle (0,149,152) pinned to colours (0,1,2).
Any proper colouring can be permuted to that normalization. Every SAT
model was decoded and checked directly. Fixed-colour greedy extension
then restored any further available vertices before the next probe.

The preset limits were 256 restoration probes, 1,200 cumulative solver
seconds, and five native seconds per probe. Each sweep tried one point
per active row, shorter sets first, choosing a least-total-degree
untried point (S first on ties, then global label). Each point was tried
at most once per row. Kissat 4.0.4 used seed 20610.

The completed run made 256 probes in 1183.84 cumulative solver
seconds and accepted 49 directly verified subset improvements.
Failed or timed-out probes supplied no negative certificate and are not
assumptions of this result. In particular, neither failure to restore a
vertex nor maximality with the final colours fixed proves deletion-set
minimality. No new shape stratum or global master was solved in this pass.

The trust boundary is the exact coordinate data, parsing and arithmetic,
the explicit colourings and restriction argument, and ordinary software
execution. All claims retain every L vertex and use only this specified
pool. Other planar graphs and geometric families are outside the result.

## Residual after the sixteen replacements

A further exact certificate shows that the enlarged published cover still
admits a four-colourable residual. The selection in
[postshrink_residual.json](postshrink_residual.json) deletes 28 S points and
adds 27 Q5 points, giving 508 vertices and 2404 strict unit edges. Its 134
selected pool points all have degree at least four. It meets every one of
the 24,821 rows (17,283 distinct sets) in the seven pinned public families:
the a=0,...,5 cover, S-only cover, a=6 cover, a=7 cover, first residual cut,
sixteen refinements, and sixteen subset replacements.

An explicit colouring extends this selection to 646 vertices and all 3102
surviving unit edges. Its complement D has 31 points (12 S and 19 Q5), and
is disjoint from the residual selection X. Thus every non-four-colourable
L union Y must meet D, while X meets every previous published clause and
misses D. The new positive clause strictly refines this specified public
cover even on the size/degree-constrained domain: X is the separating
witness. This does not assert minimality of D. The earlier rows and their
certificates are retained unchanged.

Reproduce from the repository root with Python 3.11 standard library:

```sh
python3 hadwiger_nelson_parts509_pool_cover_shrink01/verify_postshrink.py
```

Expected: `POST-SHRINK RESIDUAL AND NEW KILLING SET VERIFIED`,
`candidate_vertices=508`, `candidate_edges=2404`, `killing_size=31`,
`public_family_distinct_sets=17283`, and `missed_public_sets=0`.
[postshrink_manifest.json](postshrink_manifest.json) pins the public inputs;
[postshrink_expected.json](postshrink_expected.json) gives exact counts and
hashes. The compact certificate is 1074 bytes, SHA-256
`4df4c2cb87ef6d3ece25f72ecbba7aa6cad46ea6b6e98636f852a52b0c74b782`.
The explicit complement colouring also colours the candidate
by restriction. No SAT verdict is needed for these public claims.

Discovery used one bounded Kissat 4.0.4 call, seed 20609, on the exact
remaining-pool master augmented by the sixteen subset clauses. Its 36,520
local killing clauses were all directly rechecked before use. The
12,799-variable, 155,993-clause formula had SHA-256
`c50e974411286477f40afced4acd49de5c185472623c7649867b75ab4fbfcd1d`.
The 600-second-bounded call returned SAT in 52.181 seconds; all model
clauses and decoded conditions were checked. A full-graph two-bit colouring
formula, with triangle (0,149,152) pinned to colours (0,1,2), returned SAT
in 0.767 seconds within a 300-second bound. Every graph edge was checked
before greedy fixed-colour extension. One worker was used; full batch
wall time was 69.124 seconds and child peak RSS was 122652 KiB.

A second author implementation reconstructed the original Mathematica
coordinates, checked the candidate against all 36,520 local killing sets,
and directly checked the candidate and extension colourings in 4.610
seconds. The public checker separately uses the reviewed integer geometry
and verifies the witness against only the explicitly pinned public family.
The larger private local cover is not required for the public theorem;
no public reproducibility of the full local master is claimed here.
Solver traces from the two SAT calls are local search records, not UNSAT
certificates. No family closure, additional closed shape, cardinality
lower bound, or five-chromatic graph is established.
