# Exact mixed-box classification

## The family

Let `H` be the ordered 29-point Snail set `p,q,v1,...,v27` represented in
`seed.json`.  For every squared distance occurring for at least two unordered
pairs of `H`, choose the first pair in lexicographic order.  Map that pair to
each pair in its distance class, with either endpoint order and either
orientation.  After exact deduplication, the nonidentity maps form a set `T`
of 925 Euclidean isometries.

Rank `T` first by decreasing `|H intersect t(H)|` and then by the deterministic
canonical representation used in `geometry.py`.  Let `A` be its first 20
maps.  Their intersection counts are

```text
18,18,17,16,15,14,13,12,12,12,12,12,12,11,11,11,11,11,11,11.
```

The paper identifies exactly two nontrivial pair-congruence classes introduced
by the augmentation:

```text
{p,v11} congruent to {v6,v13}, {v21,v26}, {v8,v18};
{q,v24} congruent to {v6,v3}.
```

Applying the same endpoint and orientation choices to these two classes gives
22 distinct nonidentity isometries; call their set `U`.  Unit-edge congruences
are excluded because an edge has aggregate weight zero in every fractional
colouring, so equality between two such weights is automatic.

For `a in A`, `u in U`, an order bit `o`, and `2 <= s <= 6`, form the two
families of transformation boxes

```text
o=0: {a^i u^j : 0 <= i < l, 0 <= j < s},
o=1: {u^j a^i : 0 <= i < l, 0 <= j < s}.
```

Duplicate transformations are identified.  Beginning with `l=2`, increase
`l` through 30 while the union of the transformed copies has at most 508
distinct physical points.  Retain the last admissible prefix; if adding a row
does not enlarge the transformation set, retain that first stable prefix and
stop.  The 20 by 22 by 2 by 5 choices give 4,400 labelled graphs.  The
certificate covers them in precisely this order.

## Exact coordinates and isometries

Put `w=(1+i sqrt(3))/2`, `b=i sqrt(11)`, `c=sqrt(5)`, and let `e=8 eta`, where
`eta` is the radical in the source paper.  The coordinate field has basis
`w^i b^j c^k e^l`, with every exponent zero or one, and relations

```text
w^2=w-1,  b^2=-11,  c^2=5,
e^2=-3320-632b+1264wb.
```

The basis is linearly independent.  The square classes `-3,-11,5` are
independent over the rationals, giving degree eight before adjoining `e`.
If `e` belonged to that multiquadratic field, complex conjugation would make
all conjugates of `e^2` nonpositive; changing the sign of `sqrt(33)` instead
gives `-3320+632 sqrt(33)>0`.  Thus adjoining `e` doubles the degree to 16.
Consequently equality of the 16 rational coefficients is exact equality in
the displayed complex embedding.

For congruent ordered pairs `(x0,x1)` and `(y0,y1)`, `geometry.py` constructs

```text
z -> y0 + (y1-y0)/(x1-x0) (z-x0)
```

or its conjugate-input version.  Division is exact 16 by 16 rational Gaussian
elimination.  The checker verifies both endpoint images and that the
multiplier has norm one.  Composition therefore preserves every physical
unit distance.

## Modular supergraphs

All source coordinates are scaled by 384.  The certificate evaluates the
field into `Z/1000000411 Z` at the four stored roots in `field_base.py`.
The checker first verifies the defining equations, and it rejects any
denominator not invertible modulo the modulus.  Hence this evaluation is a
ring homomorphism on every coordinate used here.

For each box, join two distinct exact points whenever

```text
(E(x)-E(y)) (E(conjugate(x))-E(conjugate(y))) = 384^2 (mod 1000000411).
```

Every physical unit edge satisfies this congruence, so the modular graph is a
supergraph of the strict unit-distance graph.  False-positive modular edges
would only make the certificate stronger.  The stored two-bit word properly
four-colours every modular edge.  Restricting that word to the physical unit
edges proves that every one of the 4,400 geometric graphs is four-colourable.

The proof boundary is the elementary degree and isometry argument above,
CPython exact integers and rational arithmetic, and the explicit source table.
The certificate proves a complete result for this declared family only.
