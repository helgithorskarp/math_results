# Proof: an open four-colourable collar for dominating triples

For a plane point `c`, write

```text
C(c)={x: |x-c|=1}.
```

All graph edges below mean Euclidean distance exactly one.  Put

```text
delta=(sqrt(3)+sqrt(15))/2,
T=delta^2=(9+3*sqrt(5))/2.
```

## Theorem

Let `a0,a1,b` be three distinct plane points whose three mutual distances
are all greater than two.  If

```text
max(|a0-a1|,|a0-b|,|a1-b|)>delta,
```

then the full strict unit-distance graph on

```text
Y={a0,a1,b} union C(a0) union C(a1) union C(b)
```

is four-colourable.

In particular this excludes the nonempty open parameter region

```text
2 < every centre separation < 3,
delta < the largest centre separation < 3.
```

This is a region with interior in the three side-length parameters, not a
single equality locus.

## 1. Six-cycle orbits on one circle

Let `omega=exp(i*pi/3)`.  Two points of a unit circle are at unit distance
exactly when their directions differ by multiplication by `omega` or
`omega^-1`.  Rotation by 60 degrees therefore partitions the complete unit
circle into disjoint six-vertex orbits, and the strict graph on each orbit is
a six-cycle.

For an explicit global convention, choose the unique orbit representative
whose angle lies in the half-open sector `[0,pi/3)`.  Alternating two colours
around each orbit gives a proper bipartition.  The squared chord lengths for
rotation steps zero through five are

```text
0,1,3,4,3,1.                                      (1)
```

In particular, two distinct points in the same orbit are at distance at
least one.

## 2. Cross-active points lie in a cap of diameter below one

Choose a pair attaining a separation `d>delta` and relabel it `a0,a1`.
First suppose `d<=3`; if `d>3`, the triangle inequality gives no unit edges
between their unit circles and the conclusion of this section is immediate.

Normalize `a0=(0,0)` and `a1=(d,0)`.  Call `x in C(a0)` *cross-active* if
it has a unit neighbour `y in C(a1)`.  Because `|x-y|=|y-a1|=1`,

```text
|x-a1|<=2.
```

Writing `x=(X,Y)` and using `X^2+Y^2=1` gives

```text
d^2+1-2*d*X <= 4,
X >= (d^2-3)/(2*d).                               (2)
```

The threshold was chosen so that

```text
T^2-9*T+9=0,
delta^2=T.
```

Since `d>delta>2`, squaring the positive sides shows

```text
((d^2-3)/(2*d))^2 > 3/4.                          (3)
```

Indeed, after multiplying by `4*d^2`, (3) is

```text
d^4-9*d^2+9>0,
```

and `T` is the larger root of `q^2-9q+9`.  Thus every cross-active point on
`C(a0)` has `X>sqrt(3)/2` and `|Y|<1/2`.

If `x=(X,Y)` and `x'=(X',Y')` are two such points, then

```text
x dot x' >= X*X'-|Y|*|Y'| > 3/4-1/4=1/2,
|x-x'|^2=2-2*(x dot x')<1.                        (4)
```

By (1), no six-cycle orbit on `C(a0)` can therefore contain two distinct
cross-active points.  The identical argument with the centres exchanged
applies to `C(a1)`.

This is the key continuum statement: it bounds every possible cross-circle
unit edge at once.  It is not a finite sample of angles.

## 3. Bipartition of the full two-circle leaf support

For every six-cycle orbit on `C(a0)` that contains a cross-active point,
choose its alternating phase so that its unique active point has colour 0.
For every active orbit on `C(a1)`, choose the phase so that its unique active
point has colour 1.  Colour inactive orbits by the fixed half-open-sector
convention from Section 1.

Every same-circle unit edge is proper because its endpoints are consecutive
in a six-cycle.  Every cross-circle unit edge joins two cross-active points,
one on each circle, and hence joins colours 0 and 1.  Therefore the complete
strict graph

```text
A=U(C(a0) union C(a1))
```

is bipartite.  Notice that one active point may have two cross-circle
neighbours; both lie on the other leaf and receive the other colour, so no
degree or matching assumption is being made.

## 4. Four-colouring all three complete circles and the centres

All three centre separations exceed two, so the three unit circles are
pairwise disjoint.  Keep the colours `{0,1}` on `A`.  Independently
bipartition `C(b)` by its six-cycle orbits using the disjoint palette
`{2,3}`.

Give both leaf centres `a0,a1` colour 2, and give `b` colour 0.  The centres
are pairwise nonadjacent because their distances exceed two.  A centre has
no neighbour on another centre's circle: such a point would belong to the
intersection of two unit circles whose centres are more than two apart.
Thus each centre is adjacent, within `Y`, only to points of its own circle.
The leaf centres use a colour outside `{0,1}`, and `b` uses a colour outside
`{2,3}`, so all centre spokes are proper.

Edges between `C(b)` and either leaf circle join disjoint palettes.  Edges
inside the leaf union are proper by Section 3, and edges inside `C(b)` are
proper by its bipartition.  These classes exhaust all unit pairs in `Y`,
proving `chi(Y)<=4`.

## 5. Domination consequence

If a plane unit-distance graph `G` is dominated by the three embedded
centres, every noncentre vertex of `G` belongs to at least one of their unit
circles.  Hence `G` is a subgraph of the strict graph on `Y`; no induced-graph
assumption is needed.

It follows that a non-four-colourable plane unit-distance graph with a
dominating triple whose mutual distances all exceed two must satisfy

```text
diameter of the triple <= delta.                  (5)
```

The independently reviewed unit-edge theorem says that a five-chromatic
dominating triple is independent.  Equation (5) is a further restriction on
the subregion in which all three distances exceed two; it does not claim
that independence by itself forces the distances above two.

## 6. Exact nonempty interior fixture

Take the three centres

```text
(0,0), (2*sqrt(2),0), (sqrt(2),sqrt(6)).
```

They form an equilateral triangle of side `2*sqrt(2)`, so all three squared
distances equal 8.  They lie strictly inside the requested region because

```text
4 < 8 < 9,
T < 8  iff  3*sqrt(5)<7  iff 45<49.
```

All inequalities are strict, so a neighbourhood of this realized triangle
also lies in the theorem's region.  At this fixture, the squared lower bound
in (2) is `25/32`, and the squared diameter of the closed comparison cap is

```text
4*(1-25/32)=7/8<1.
```

The certificate verifies these identities, the exact three pair distances,
the threshold polynomial and isolation, and the six orbit chords in the
multiquadratic basis
`1,sqrt(2),sqrt(3),sqrt(6),sqrt(5),sqrt(10),sqrt(15),sqrt(30)`.

## 7. Scope and stop boundary

The proof supplies a sufficient open collar, not an optimal threshold.  At
`d<=delta`, estimate (4) no longer ensures at most one cross-active point per
six-cycle orbit.  At a centre separation at most two, two owner circles can
intersect, so the disjoint-palette lift in Section 4 no longer applies.  The
failure of either argument is not evidence of a non-four-colourable graph.

Accordingly, the remaining domination frontier is the union of:

1. triples with some centre-pair distance at most two; and
2. triples with all three distances above two but diameter at most `delta`.

Further work should replace the cap uniqueness argument by a region-level
analysis of linked active orbits, or pivot to another geometry architecture.
It should not merely test successive scalar values of `d` or interpret an
abstract phase conflict as a realized construction.
