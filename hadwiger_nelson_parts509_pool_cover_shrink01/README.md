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
