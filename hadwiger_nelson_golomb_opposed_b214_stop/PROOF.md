# Proof outline

Let `G` be the ten-point Golomb graph, and let `B` be the archived 214-point
strict unit graph with marked terminals `+3/2,-3/2`.  Put

```text
S = G union L(B) union R(B),
L(x,y)=(x-1/2,y),  R(x,y)=(-x+1/2,y).
```

The exact coordinate calculation in `verify.py` proves that each transformed
copy contains `G`, that their collision-merged union has 343 vertices, and
that its complete strict unit graph has 1,782 edges.  Exactly 108 of these
edges are absent from the union of the three labelled component edge sets.

Fix the colours on a unit triangle of `G` to `0,1,2`.  Direct enumeration of
the remaining seven vertices gives 95 proper normalized patterns.  For 66 of
them, `certificate.json` supplies proper colourings of `S`.  For the other 29,
the CNF encoded by `colouring_cnf` is the disjunction of all possible
extensions.  Every proper colouring choosing an excluded pattern satisfies
that CNF, and conversely a CNF model decodes to such a colouring.  The checked
RUP derivation of the empty clause proves that no model exists.  Hence the
complete normalized relation of `S` has exactly 66 patterns.

The pattern `0121212203` has explicit proper extensions through `L(B)` and
through `R(B)` separately.  It belongs to the 29-pattern RUP-excluded set for
`S`.  Therefore the complete physical cross contacts give a strict relation
loss beyond what either isolated component imposes.

Finally put `T=S union A`, where `A` is the archived A159 support in its native
frame.  Exact merging and all-pairs reconstruction give 359 vertices and
1,893 edges.  Restriction to `S` shows that `T` can admit no Golomb pattern
outside the 66-pattern relation.  The 66 checked colour words in
`certificate.json` show that every one of those patterns does extend to `T`.
Thus `T` has exactly the same relation.  Since `G` is not three-colourable and
both `S` and `T` have displayed proper four-colourings, both graphs have
chromatic number exactly four.

Every geometric equality and unit-distance predicate in this argument is an
integer coefficient comparison in a linearly independent multiquadratic
basis.  Remaining trust lies in Python integer arithmetic, the basis
interpretation, exhaustive finite loops, the literal certificates, and the
RUP checker implementation; this is not a proof-assistant formalization.

