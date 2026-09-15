# Native Heule610 horizontal reflection cannot meet the 508-point cap

Let `P` be the exact 610-point set in the pinned native `610.vtx` file, and
let `r(x,y)=(x,-y)`. Every map selecting either `p` or `r(p)` independently
for every `p` in `P` has **at least 547 distinct images**. Thus no such map
preserving all source unit edges can produce an at-most-508-point graph.

This is a cardinality obstruction for one source and one fixed reflection.
It is not a new five-chromatic construction, a global HN bound, or a theorem
about other axes, preliminary frame changes, deleted source points or general
deformations. The edge-preserving minimum is not determined; only its lower
bound 547 is proved. Without edge constraints the minimum is exactly 547.

## Proof and exact accounting

The reflection-closed set `P union r(P)` has 1,086 points. Exactly eight are
fixed by reflection. Its reflection orbits therefore number

```text
(1086 + 8)/2 = 547.
```

Every orbit meets the original source. Images of source points in different
orbits cannot coincide, so every permitted map must retain at least one
point per orbit. Conversely, choosing a common representative in each orbit
attains 547 when edge preservation is not required.

An equivalent count finds exactly 63 nontrivial mirror pairs already present
in `P`: only such pairs can merge, giving `610-63=547`. The two calculations
agree. Reaching 508 would require 102 merges, exceeding the available 63.

The eight axis-point labels, in the native zero-based file order, are
`0,1,4,96,99,244,469,470`. Coordinates use the independent radical basis
`1,sqrt3,sqrt5,sqrt15,sqrt11,sqrt33,sqrt55,sqrt165`, separately for x and y,
with denominator 288. Exact coefficient equality decides all coincidences;
there is no proximity threshold.

## Reproduction

From the repository root, CPython 3.11 or later and its standard library:

```sh
python3 -B hadwiger_nelson_heule610_horizontal_reflection_gate/verify.py \
  --input /scratch/hn-heule610/610.vtx --download
python3 -O -B hadwiger_nelson_heule610_horizontal_reflection_gate/verify.py \
  --input /scratch/hn-heule610/610.vtx
python3 -B hadwiger_nelson_heule610_horizontal_reflection_gate/controls.py
sha256sum -c hadwiger_nelson_heule610_horizontal_reflection_gate/SHA256SUMS
```

The verifier reuses two existing, hash-pinned coordinate parsers and compares
their full ordered point lists entry by entry. One uses dense field vectors
and conjugate inversion; the other expands sparse radical numerators and
denominators and rationalizes their monomial denominators. The count check
then compares direct source pairs with Burnside counting on the closed set.
Small fixtures exhaust every pointwise reflection assignment and test that
the minimum-image formula is attained. This is author-run checking, not an
independent-author review or formalization.

The input is downloaded into scratch, not redistributed here. Its immutable
source is `vtx/610.vtx` at Heule's CNP-SAT commit
`bb414955a6ef5f49f7df2b245b1e778aa67c068a`. The file is 34,446 bytes with
SHA-256 `a385b4599ed5863546d39b3017c811aa144725d253db79afb2c9d0654164ba5e`.
[inputs.json](inputs.json) pins the URL and all imported code.

## Research boundary

The earlier [bisector-fold gate](../hadwiger_nelson_bisector_fold_gate/README.md)
gave a general component criterion for edge-preserving partial reflections
and closed every axis for a different, nine-move 509-point seed. Here the
source is native Heule610 and the axis is fixed; the weaker cardinality
obstruction already suffices. No new folding principle is claimed.

The positive-parent motivation is Heule's published 610-point five-chromatic
graph in [Section 4.2 of his primary paper](https://arxiv.org/html/1805.12181v1).
The selected operation was intended to preserve all unit edges while merging
mirror-related source points. Its cardinality gate failed before edge
compatibility, so no connectivity census, unit-edge reconstruction, colour
solver, parent refutation replay or five-colouring computation followed.
The chromatic premise is unnecessary for the theorem above.

The fixed source/reflection operation is retired. This result does not
justify another axis, extra reflections, deletion scheme or a nearby source
sweep. No record candidate or positive capped obstruction was obtained.
