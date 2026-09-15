# Proof of the exact-507 H510 obstruction

## 1. Geometry of a source rhombus

Suppose source vertices `a,b` have exactly the two common neighbours `c,d`.
If `p(a) != p(b)` and `p(c) != p(d)`, then `p(c),p(d)` are the two distinct
intersections of the unit circles about `p(a),p(b)`. Reflection in the midpoint
of `p(a),p(b)` interchanges them, so

```text
p(a) + p(b) = p(c) + p(d).
```

Thus the row `e_a+e_b-e_c-e_d` is valid unless an opposite pair is identified.
Adjacent labels cannot be identified because their image distance must be one.

The checked H510 source has no `K2,3`, so each opposite source pair belongs to
at most one such row. It has 3,953 canonical rows and 7,906 opposite pairs.

## 2. The twenty-basis dichotomy

The accepted parent certificate contains 20 sets of 501 rows, each of rank
501. For each row, form a 20-bit mask recording the bases containing it. For a
collision partition `Pi`, let `M(Pi)` be the union of the masks of all rows
invalidated by an opposite pair lying in one fibre.

If `M(Pi)` is not the all-one mask, one certified rank-501 basis remains valid.
Both coordinate vectors of the proposed drawing therefore lie in the parent's
nine-dimensional kernel.

If `M(Pi)` is the all-one mask, `Pi` belongs to the finite rank-defect branch
enumerated in Section 4.

## 3. Full-rank branch

The parent orientation proof exhausts all 4,096 orientation words by 36
prefixes. Two complete words survive and the parent polynomial identities
give exactly four Galois-conjugate drawings, each with 510 distinct points.

Each of the other 34 prefixes supplies three forced equality pairs whose
equivalence closure loses at least three images. The new verifier confirms
that it loses exactly three in every prefix. Therefore a drawing with exactly
507 images following such a prefix can have no further equality: its fibre
partition is exactly the forced one. Eighteen forced partitions identify a
source edge. Each of the remaining sixteen quotient graphs contains a checked
`K2,3`.

An injective plane unit-distance graph cannot contain `K2,3`: two distinct
points have at most two common unit neighbours. Hence no full-rank exact-507
drawing exists.

## 4. Rank-defect branch

A partition of 510 labels into 507 fibres has non-singleton sizes `4`, `3+2`,
or `2+2+2`.

### Three pairs

At most three distinct rhombus rows fail. The verifier enumerates every
three-row mask cover, then both opposite-pair choices per row. If both opposite
pairs of one rhombus are identified, only two distinct rows fail; the two
possible two-row mask covers are supplied and checked by the parent. These
repeated-row cases are included separately.

For a two-row cover plus a third pair that invalidates no new row, first form
the two-pair quotient. It already has a checked `K2,3`. Any third identification
not merging two vertices of that witness leaves the witness intact. The only
four quotient-class choices are its centre pair and the three pairs among its
common neighbours. Testing their source representatives completes this branch.

### Triple and pair

Every relevant triple contains an opposite pair; otherwise its only possible
failed row comes from the separate pair and cannot hit all 20 bases. The
verifier enumerates each independent triple containing an opposite pair,
unions the masks of all its internal opposite pairs, and completes the mask by
each disjoint opposite pair whose row contains all missing bits.

Exactly four triples already have the full mask. Each partial quotient has a
literal `K2,3`, so the same four-class repair argument covers an arbitrary
separate pair.

### Quadruple

If at most three internal opposite rows cover all bases, the quadruple is
generated from the complete list of three-row covers, the two exceptional
two-row covers, or one of the four full-mask triples plus a fourth label.

Otherwise at least four of its six internal pairs are opposition edges. The
verifier enumerates all independent four-sets with at least four such edges.
For a sorted four-set `a<b<c<d`, at least one opposition edge lies among
`a,b,c`; otherwise only the three pairs incident with `d` could be edges. This
gives the complete bitset enumeration used by the checker. It examines
1,897,832 dense four-sets before retaining the full-mask cases.

## 5. Quotient obstruction check

The source H510 graph has no `K2,3`. Therefore any `K2,3` newly created by a
collision contains a merged quotient class. If that class is one of the two
degree-three vertices, the other centre can be arbitrary. If it is one of the
three common neighbours, both centres lie in its quotient neighbourhood. The
verifier checks exactly these candidate centre pairs; no all-pairs scan is
omitted.

Every enumerated rank-defect partition either collapses a source edge or has a
literal quotient `K2,3`, with the counts in `expected.json`. Sections 2--5
exhaust both sides of the dichotomy and all fibre shapes, proving the theorem.
