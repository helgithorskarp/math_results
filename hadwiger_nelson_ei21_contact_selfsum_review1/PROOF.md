# Independent proof architecture

## 1. Source reconstruction

The pinned Shibuya `ei21_vertices` routine labels

```text
(A,B,p0,p1,p2,p3,p4,p5,p6,q1,...,q6,r1,...,r6) = (0,...,20).
```

Each `cu(x,y)` call creates a point at unit distance from both parents.  The
fixed pair `A=0`, `B=-i` supplies one edge.  The three returned closure
conditions supply `(7,8)`, `(4,14)`, and `(3,20)`.  Reading only those
definition-level operations gives 38 sorted source edges, which agree exactly
with the geometry certificate.  The new contact is `(0,14)`.

## 2. Independent root isolation

Fix vertices 0 and 1 at `(0,0)` and `(0,-1)`.  The remaining 19 points supply
38 real coordinates.  The 39 complete edges other than the fixed edge give a
square system `F:R^38 -> R^38` of squared-unit equations.

The certificate contains a rational midpoint `m`, radius `r=10^-25`, and
rational matrix `A`.  Unlike the target's aggregate Jacobian perturbation
formula, the review gives every coordinate its exact rational interval,
evaluates each affine Jacobian entry over the whole box, and propagates those
intervals through every entry of

```text
I-AJ(X).
```

The resulting infinity row norm is below `10^-22`.  Direct exact evaluation
also gives

```text
||A F(m)||_infinity + 10^-22 r < 10^-47 < r.
```

Thus `T(x)=x-AF(x)` is a contraction mapping the closed box strictly into
itself.  Banach's theorem gives a unique fixed point.  At the midpoint,
`||I-AJ(m)||<1`, so `AJ(m)` and hence the square matrix `A` are invertible.
The fixed point therefore satisfies `F(x)=0`.

Direct endpoint interval evaluation of all 210 point pairs proves squared
separation greater than `38/1000`.  Every undeclared pair has squared-distance
gap from one greater than `9/1000`.  Consequently the root consists of 21
distinct plane points and its complete strict unit graph has exactly 39 edges.

## 3. Chromatic and structural checks

A fixed-label exhaustive search, rather than the target's DSATUR, proves the
38-edge source and 39-edge contact graph non-three-colourable after 479 and
339 recursive calls.  The target's blocked and surviving words are checked
directly.  A fresh reverse-palette search gives the different complete word

```text
013222231231103332231.
```

Deleting every vertex set of orders one and two leaves the contact graph
connected.  Exactly twelve three-vertex sets disconnect it; the first is
`{3,5,15}`.  Hence its vertex connectivity is exactly three, strengthening
the target's no-articulation/no-bridge statement.  The degree multiset has
nine vertices of degree three, nine of degree four, and three of degree five.

## 4. Conservative commutative self-sum

There are 231 canonical addresses `(i,j)` with `0<=i<=j<21`, representing
`p_i+p_j`.  The checker adds the source coordinate intervals endpoint by
endpoint.  Two addresses enter the possible-equality relation exactly when
their boxes overlap in both coordinates; connected components give 210
conservative classes.

For every one of the 26,565 address pairs, the checker subtracts interval
endpoints and squares the resulting coordinate intervals.  It proves:

- no same-class pair can be unit, with squared distance below `10^-48`;
- no different-class pair can collide, with squared separation greater than
  `36/1000000`; and
- every excluded possible-unit pair has squared-distance gap greater than
  `167/1000000`.

Joining class pairs whenever an address-pair interval contains one yields a
210-vertex, 731-edge supergraph containing every actual unit edge after every
possible collision.  The submitted 210-character word is proper on this
independently reconstructed graph.  Its complete component/edge serialization
hash agrees with the target.

For every fixed `j`, the canonical addresses for `p_i+p_j` form an injective
translated copy of the exact 39-edge source.  Hence the physical self-sum is
not three-colourable.  The conservative word proves it four-colourable, so its
chromatic number is exactly four.

The interval classes give at least 210 distinct physical points; 231 formal
addresses give the upper bound.  The calculation does not resolve equality
inside a nontrivial class, so it does not establish exact order 210.

## 5. Connectedness and bridges

The translated fibre for index `j` contains `p_j+p_k`, while the fibre for
index `k` contains that same physical point.  Therefore every pair of the 21
fibres intersects.  Since each fibre is a connected copy of the source, their
union is a connected spanning exact-unit-edge subgraph of the physical
self-sum.

The source has no bridge, so every fibre edge lies on a cycle.  Any additional
actual unit edge also lies on a cycle because its endpoints are already joined
in the spanning union.  Thus the actual complete self-sum graph is connected
and bridgeless.

## 6. Trust boundary

The proof trusts CPython integer and `Fraction` arithmetic, JSON parsing, the
two hash-pinned target certificates, and ordinary hardware.  It does not
trust the target verifier, target midpoint error formulas, floating-point root
finder, or SAT producer.  It is independently implemented evidence, not a
proof-assistant formalization.
