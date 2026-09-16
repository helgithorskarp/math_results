# Proof obligations and independent discharge

## 1. Exact EI19 source

Let the 34 free variables be the two coordinates of vertices 2 through 18;
vertices 0 and 1 are fixed at `(0,0)` and `(1,0)`. Let `F` consist of the 34
listed squared-unit equations other than the anchor equation. The certificate
provides a rational midpoint `m`, radius `r=10^-25`, and rational square
matrix `A`.

The checker constructs `F(m)` and `J(m)` directly from the 35-edge list and
computes exact induced infinity-norm bounds

```text
beta = ||I - A J(m)||,
eta  = beta + 16 r ||A||,
delta = ||A F(m)|| + eta r.
```

For one squared-distance row, changing every free coordinate by at most `r`
changes each endpoint-difference derivative by at most `4r`. There are at most
four nonzero derivative entries across the two coordinate directions, so
`||A(J(x)-J(m))|| <= 16r||A||` throughout the box. The exact certificate gives
`beta<1`, `eta<1`, and `delta<r`.

Thus `T(x)=x-AF(x)` is a strict contraction and a strict self-map of the
closed rational box. Banach's theorem gives a unique fixed point. Since
`||I-AJ(m)||<1`, the square matrix `AJ(m)` is invertible; hence `A` is
invertible and a fixed point of `T` is a zero of `F`. This establishes a
unique exact real EI19 realization in the box.

For every source pair, the checker bounds deviation of squared distance from
its midpoint value by

```text
4 r (|dx|+|dy|) + 8 r^2.
```

All 19 points are distinct. The 34 free equations and anchor equation give 35
unit pairs, and the other 136 pairs have a strict squared-unit gap. Hence the
complete source unit-distance graph is exactly the advertised 19-vertex,
35-edge graph.

## 2. Independent lens enclosures

For source points `a,b`, put `v=b-a` and `d2=|v|^2`. Exact rational interval
classification gives `0<d2<4` for 165 pairs and `d2>4` for the remaining six;
no interval meets 0 or 4. For each eligible pair, the exact intersections are

```text
(a+b)/2 +/- i(b-a) sqrt(1/d2 - 1/4).
```

Direct expansion proves that each is at unit distance from `a` and `b`. The
checker evaluates this formula by inclusion-isotonic rational interval
operations. It rounds only square roots. For a nonnegative rational `x=n/d`
and `S=2^192`, it sets

```text
k = floor(sqrt(floor(n S^2/d))),
lower = k/S,
upper = k/S if k^2 d = n S^2, otherwise (k+1)/S.
```

Because `floor(sqrt(floor y))=floor(sqrt y)`, these are rigorous outward
bounds for `sqrt(x)`. This gives 330 lens labels and 349 total formal labels.

## 3. Collision-safe four-colouring

The submitted word has length 349 and alphabet `{0,1,2,3}`. The independent
checker visits all `349 choose 2 = 60,726` label pairs.

- For each of 43,127 differently coloured pairs, at least one coordinate
  interval is strictly separated. Such labels cannot denote the same point.
- For each of 17,599 same-colour pairs, the interval for squared distance lies
  strictly on one side of one. Such labels cannot form a unit edge.

Therefore every physical collision involves labels of one colour, so colour
descends to the quotient. Every physical unit edge has differently coloured
endpoints, including contacts absent from the generating incidences. This is a
proper four-colouring of the complete physical unit-distance graph.

## 4. Chromatic lower bound and vertex-criticality

The full 19-vertex source graph is embedded in the closure. A deterministic
DSATUR traversal fixes the colours of one edge to 0 and 1, which is without
loss under colour permutation, and exhausts every remaining three-colour
assignment. It finds none after 152 search nodes.

The same checker deletes each source vertex in turn and generates a proper
three-colouring of the remaining graph. The 19 positive words appear in
`EXPECTED.json` and are rechecked edge by edge. Every proper induced subgraph
is contained in a one-vertex deletion, so the source is vertex-critical
four-chromatic. Consequently the physical first closure has chromatic number
exactly four.

## 5. Physical-order interval

Join two formal labels when their certified rectangles overlap in both
coordinates. There are 388 such pairs and 247 connected components. Equal
exact points must belong to intersecting rectangles, hence to the same
component. Distinct components therefore give distinct physical points, so
the physical order is at least 247. The 349 formal labels give the trivial
upper bound 349.

No converse is used: rectangle overlap does not establish exact equality.
Thus `[247,349]` is certified, while an exact physical order is not.

