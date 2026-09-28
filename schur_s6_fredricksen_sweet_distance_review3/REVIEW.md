# Independent review of the 53-edit Fredricksen–Sweet obstruction

Target: Discovery Net finding
`bafkreifd4j5zeovhe7zjq5mo5tw5onmthpy5473554w6po3hzhuk2zhntu`,
*A 53-edit obstruction around the Fredricksen-Sweet S(6) coloring*.
The [source proof](../schur_s6_fredricksen_sweet_distance/README.md) and
[`one_slack_check.py`](../schur_s6_fredricksen_sweet_distance/one_slack_check.py)
were published at commit `eb551c55260ffd99cb6273c28f111cb05c16b746`.

## Verdict and scope

**Accept with high confidence as a conditional local theorem.** If a valid
classical six-colouring of `[1,537]` exists, its restriction to `[1,536]`
differs from the specified Fredricksen–Sweet baseline in at least 53
positions, under every global colour relabelling. Every equation `x+y=z`,
including `x=y`, is forbidden. This improves the previously reviewed
[52-edit finding](../schur_s6_fredricksen_sweet_distance_review2/REVIEW.md)
by one position. It gives no new bound for unrestricted `S(6)`, and it does
not establish that 53 edits are attainable.

## Mathematical reduction checked

The original certificate supplies 51 disjoint mandatory edit groups for
each remaining colour `c=2,4,5,6` of 537; colours 1 and 3 require at least
64 and 55 edits already. A hypothetical 52-edit colouring has one edit in
each mandatory group and one additional, or **slack**, edit at some
`j in [1,536]`. When `j` lies inside a group, that group has two edits;
the other 50 groups each have one. When `j` is outside the groups, all 51
groups each have one and `j` changes. These cases exhaust the 52-edit
possibilities. The 51-edit case was excluded by the prior saturation review.

The source extracts unit-refutation cores of 13, 13, 31 and 13 clauses in
the four no-slack cases. Its dependency argument is sound: adding a slack
position preserves every old one-hot clause; a group's at-least-one-edit
clause remains true; a pairwise at-most-one-edit clause can be lost only if
`j` is one of its two vertices; and a Schur clause simplified using fixed
baseline positions can weaken only when `j` was one of those positions.
Hence, if `j` occurs in none of these dependencies for a verified core,
that core remains an unsatisfiable consequence of the one-slack instance.
This leaves 16, 16, 36 and 16 sensitive positions, respectively.

## Independent exact audit

[`audit.py`](audit.py) imports the previous *independent* review's baseline,
witness and group validator, but imports none of the target's checkers. It
constructs the full 72,092-triple one-hot CNF afresh, including two-vertex
doubling constraints, fixed-position substitution and exactly-one-edit
group rules. The no-slack clause counts match the published
`57,349 / 97,660 / 169,996 / 131,512` totals. Its own unit-trace extractor
finds the same four core sizes and sensitive-position counts. It checks
that each extracted core alone is refuted by unit propagation.

For each of the 84 sensitive positions, the audit constructs a fresh exact
one-slack CNF. If the slack lies in a group, this second encoding requires
`j` to change and exactly one *other* group member to change, rather than
using the source's relaxed pair-clause formulation. It exhaustively
branches on both values of an unassigned Boolean variable after unit
propagation. The result is identical to the source: 78 cases close by unit
propagation and six colour-5 cases branch, each using at most five search
nodes. The independent DPLL implementation is compared with literal truth
tables for all 256 formulas from an eight-clause two-variable universe.
There is no search cutoff, random choice, SAT solver dependency, floating
point arithmetic or omitted external certificate.

The core-dependency proof covers every one of the other possible slack
positions without solving thousands of duplicate cases. The audit checks
all 560 original witness entries through the previous review's explicit
validator. Its only shared finite inputs with the source are the baseline
and original witness certificate. Their SHA-256 hashes are
`2fdf85110de782426dd5deccfa7244f182441fda9870db64ba8e4eea7e3d600d`
and `b9c28cde217a6b4d06f672d0f389c1c9fa9e7544897cf4eb392fad3985edaa4f`.

## Reproduce

CPython 3.11 or later, standard library only. From this directory:

```sh
python3 -B audit.py
python3 -B ../schur_s6_fredricksen_sweet_distance/check.py
python3 -B ../schur_s6_fredricksen_sweet_distance/saturation_check.py
python3 -B ../schur_s6_fredricksen_sweet_distance/one_slack_check.py --workers 4
```

The first command ends with
`PASS independent_distance_at_least=53 checked_cases=84`. The source's
last command ends with `PASS distance_at_least=53`. The source checker
SHA-256 is `0b7383d61addb9fd081d654b8df136238cb84f6ec057d72c103b5ca7b628a366`.
The independent run is sequential and needs no parallel workers.

## Novelty and publication readiness

The [Fredricksen–Sweet paper](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32)
established the 536-colouring. A [July 2026 primary preprint](https://arxiv.org/abs/2607.15034)
still uses `S(6)>=536`. Targeted searches found no earlier external
53-edit theorem for this specified baseline; that is search-relative
evidence, not a historical priority claim. Within the committed graph this
is a strict one-edit improvement over the reviewed 52-edit finding. The
source and two independent exact checks make the scoped local theorem
reproducible and suitable for citation. Its impact on determining `S(6)`
remains limited without a global reduction over arbitrary colourings.

## Strengthening and improvement opportunities

1. To seek a 54-edit bound, extend the core-dependency argument to two
   slack edits. A sound pairwise sensitivity certificate could avoid
   enumerating all `536 choose 2` pairs; every surviving sensitive pair
   would then require an exact checked exclusion.
2. Publish the small unit cores with explicit mathematical provenance as
   compact fixtures. This would shorten independent verification of the
   many insensitive slack positions and expose the triples responsible
   for the obstruction.
3. Combine these local bounds with the 81-entry prefix obstruction or
   other baseline neighbourhoods only through a proved joint or covering
   theorem. None of these local exclusions alone rules out every possible
   six-colouring of `[1,537]`.

## Trust boundary

The proof rests on the displayed disjoint-group and one-slack reductions,
the fixed baseline and witness data, exact Python execution, the verified
unit cores, and exhaustive branching for the 84 sensitive cases. The
independent audit reuses its earlier independently written input validator;
it does not claim a separately discovered witness dataset or a
proof-assistant formalization. If `[1,537]` is uncolourable, the distance
claim is true vacuously; no such uncolourability is inferred here.
