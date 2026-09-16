# Proof obligations and independent discharge

## 1. Source identity

The archived H510 certificate identifies 510 coordinate rows by provenance.
Appending the 122 pinned fresh centres gives 632 distinct points in
`Q(sqrt(3),sqrt(5),sqrt(11))`, all at common denominator 96. Recursive
quadratic-tower multiplication tests every pair and gives 3,112 unit edges.
Deleting nonadjacent labels 399 and 462, each of degree seven, removes exactly
14 edges and gives the reviewed 630-point, 3,098-edge H630 seed.

The H632 and H630 canonical edge hashes agree with the prior independent
review. Its five-colour word is also checked directly. The final theorem below
does not otherwise require the source four-colour UNSAT certificate: its own
upper and lower chromatic bounds are positive witnesses.

## 2. Whole-block replacement and physical order

The retention predicate removes exactly those 212 H630 points with any
nonzero coefficient on a basis monomial containing `sqrt(5)`. The 418 retained
points lie in `Q(sqrt(3),sqrt(11))`.

For integers `(m,n)` in the radius-five hexagonal address set, put

```text
x = m/2 - (m+2n)sqrt(6)/6,
y = msqrt(2)/2 + (m+2n)sqrt(3)/6.
```

There are 91 distinct address points. The square classes of `2,3,5,11` are
independent over `Q`, so their sixteen products are linearly independent. A
disk point has no `sqrt(2)`-containing coefficient precisely when
`m=0` and `m+2n=0`, hence precisely at `(0,0)`. Consequently no nonzero disk
point can equal any old point, while the origin is shared. The physical order
is therefore

```text
418 + 91 - 1 = 508.
```

This is an exact collision proof, not a numerical merge tolerance.

## 3. Complete unit-distance graph

An element of a three-stage quadratic tower is represented recursively as
`a+b sqrt(p)`. Multiplication applies

```text
(a+b sqrt(p))(c+d sqrt(p))
  = (ac+pbd) + (ad+bc)sqrt(p)
```

at every stage. Independence of the square-class basis makes equality of the
eight integer coefficients faithful. For each physical pair the checker
squares both coordinate differences and compares the resulting coefficient
vector with `(96^2,0,...,0)`.

All 128,778 pairs are exhausted, giving exactly 2,341 edges. Canonical point
and edge bytes agree entry-for-entry with the target. Partitioning by physical
origin yields 2,095 retained--retained, 12 mixed and 234 private-disk edges.
Thus the result concerns an actual plane unit-distance realization and its
complete strict graph, not an abstract selected-edge graph.

## 4. Chromatic number

The submitted word has length 508, alphabet `{0,1,2,3}`, and different
symbols on every one of the 2,341 edges. Hence `chi <= 4`.

The submitted seven vertices induce two diamonds sharing one origin role,
with their opposite tips adjacent. In any three-colouring, the nonadjacent
tips of a diamond receive the same colour. The two diamonds therefore force
the two adjacent outer tips to share a colour, a contradiction. Hence
`chi >= 4`, and the full graph has chromatic number four.

## 5. Structural strengthening

The checker constructs every diamond `(o,t,a,b)` from the complete adjacency
relation: `o,t` are nonadjacent and `a,b` are adjacent common neighbours. It
then joins two vertex-disjoint diamonds at the same `o` when their tips are
adjacent. Every resulting seven-set has exactly the eleven Moser edges.

There are 572 role embeddings and 286 distinct induced vertex sets; exchanging
the two diamonds accounts for the factor two. Every set is a subset of the
418 retained vertices. The submitted witness is one of them. Thus the retained
graph is not three-colourable; restriction of the full four-word proves its
chromatic number is four.

For each private disk address colour by `(m-n) mod 3`. Every unit lattice step
changes this residue, and direct edge checking confirms propriety on all 234
private edges. A checked private triangle proves the private graph has
chromatic number three.

Tarjan traversals prove that the full graph, retained graph and private disk
graph are each connected and have no articulation vertex or bridge. These are
structural facts, not evidence of five-chromaticity.

## 6. Containment boundary

Independent outward rational bounds at scale `2^80` put every archived H632
coordinate strictly between -3 and 3. Hence every pair in H632 and its H560
and H516 subgraphs has squared distance below 72. The final support contains
three disjoint opposite disk pairs at distance ten. No registered old graph
can contain even one such pair isometrically, and H516 plus one arbitrary
point cannot accommodate all three disjoint pairs. This validates only the
declared containment distinction.

