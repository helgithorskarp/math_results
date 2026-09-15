# Proof architecture for the restricted-family exclusion

Let `H` be the retained 373-point Parts host and let `B` be its 23 marked
receiver pins.  Define

```
C(B) = {x in R^2 : x is at unit distance from at least two distinct points of B}.
```

The target support is `W = H union C(B)`, with physical coincidences merged.
The independently checked finite computation proves that `W` has 488 points,
2,200 strict unit edges, and chromatic number four.

## Completeness of the circle-intersection enumeration

Fix two distinct pins `a,b`, put `d=b-a` and `s=|d|^2`.  A common unit
neighbour `x` lies at the intersection of the two unit circles centred at
`a` and `b`.  Subtracting their equations shows that `x` lies on the
perpendicular bisector of `ab`.  Consequently:

- if `s>4`, the circles are disjoint;
- if `s=4`, their sole intersection is `(a+b)/2`; and
- if `0<s<4`, their intersections are exactly

```
(a+b)/2 +/- i(b-a)/2 * sqrt((4-s)/s).
```

The 23 pins are physically distinct, so `s=0` never occurs.  The independent
checker classifies all `binom(23,2)=253` pairs as 81 secants, 24 tangents,
and 148 disjoint pairs, then includes every displayed root.  This gives 186
formal occurrences before collision merging.

Every `x in C(B)` has two distinct witnessing pins.  Applying the preceding
two-circle classification to that pair puts `x` in the enumerated support.
Conversely, each enumerated occurrence is checked to have its two defining
unit contacts.  Thus the enumeration equals `C(B)` over the entire real
plane; it is not restricted to a preselected algebraic pool.

## Exact physical reconstruction

The base field is represented independently as the tower
`Q(sqrt(3))(sqrt(11))`.  Each occurrence has the form

```
A + U sqrt(r),  with A,U in Q(sqrt(3),sqrt(11))^2 and r>0 in that field,
```

with tangencies handled separately at `r=0`.  The review makes no
independence assumption about different square roots.

Outward rational intervals first identify possible coordinate coincidences.
SymPy 1.14.0 then simplifies every surviving equality as an exact real
algebraic expression.  All 141 overlapping occurrence pairs are exact
equalities.  Their equivalence classes have size distribution

```
451 x 1, 24 x 2, 10 x 4, 1 x 6, 2 x 7.
```

Hence 559 host-plus-lens occurrences merge to 488 physical points, or 115 new
points.  The 71 count in the target is the number of redundant occurrences
`559-488`; it is not the number of pairwise equalities.  This distinction is
only a bookkeeping refinement, not a correction to the target theorem.

At each of 96, 128, and 192 interval bits, rational distance intervals exclude
116,628 of the 118,828 merged pairs from unit distance.  Exact tower arithmetic
handles host pairs, and exact symbolic simplification verifies the 344
surviving pairs involving a new radical point.  This recovers exactly 2,200
unit edges and leaves no unresolved or refined candidate.  The ordered point,
route, representative-origin, and edge hashes agree entry-for-entry with the
target.

## Chromatic and universal consequences

The supplied 488-symbol word is proper on every one of the 2,200 reconstructed
unit edges and restricts to the stated full host word and receiver boundary
word.  Thus `chi(W)<=4`.

The seven retained host labels `[0,149,152,312,151,154,314]` induce eleven
unit edges.  Directly exhausting all `3^7=2187` assignments finds no proper
three-colouring, so `chi(W)>=4`.  Therefore `chi(W)=4`.

Now let `X` be any set of new plane points such that every `x in X` is at
unit distance from at least two marked pins.  Circle-intersection completeness
gives `X subseteq C(B)`, hence the complete strict unit graph on `H union X`
is an induced subgraph of the checked graph on `W`.  Restricting the displayed
four-colouring proves that `H union X` is four-colourable.

Contrapositively, every successful non-four-colourable replacement for this
host must contain at least one new point with at most one marked-`B` contact.
This is the exact global quantifier justified by the package.

It says nothing about a replacement after even one such low-contact point is
allowed, about iterative or second-layer closures, or about other hosts and
boundaries.  The fact that the complete lens support uses only 115 of the
135-point allowance does not license filling the remaining budget while
retaining the theorem.
