# Exact triangle-isometry assembly of Haugland's heptagon graph

This is a construction of graphs drawn with unit edges in the Euclidean
plane. The word "plane" refers to the metric realization, not to graph
planarity or a requirement that edges do not cross.

## Source and complete construction family

Let t=exp(pi i/21), so t is a primitive 42nd root of unity, and put

```
P_j = t^(6j)/(t^24-t^(-24)),
Q_j = -t^(6j-7)/(t^6-t^(-6)),
R_j = -t^(6j+7)/(t^12-t^(-12)),       0<=j<7.
```

Let H be the set of these 21 points and let U(X) denote the strict
unit-distance graph of a point set X. These are precisely the coordinates
in Section 2 of [Haugland's paper](https://arxiv.org/html/2608.04542v1),
written in the complex plane. For example, 1/(2i sin theta)=-i/(2 sin theta)
turns the P formula into his trigonometric formula, and
i t^(-7)=exp(pi i/6), i t^7=exp(5pi i/6) give Q and R.
The graph U(H) has the P cycle of step 1, the Q cycle of step 2, the R cycle
of step 3, and all three edges of each triangle

```
Delta_j = {P_j,Q_j,R_j}.
```

All 210 seed distances are rechecked exactly; these are all 42 edges.

For each j, take all six Euclidean isometries which permute Delta_j.
Remove the identity, leaving five isometries per triangle. Label the
resulting collection of 35 choices by C. For J a subset of C define

```
X_J = H union union_{g in J} g(H).
```

Each g is an actual isometry of the plane, not a proposed realization of
an abstract graph. The family includes every subset of these 35 choices.
No recursive application to newly created triangles is included.

## Exact geometric lemma

The following finite statements are certified by complete exact arithmetic:

1. Each of the 35 nonidentity copies g(H) intersects H in exactly the
   three vertices of its designated triangle Delta_j.
2. The 18 points g(H) outside H are disjoint from the outside points of
   every other copy. Thus the 35 copies are distinct, and different subsets
   J give different point sets X_J.
3. Every unit edge of the full union X_C belongs to H or to some g(H).
   There are no additional unit edges joining different copies.

Consequently

```
|X_J| = 21 + 18 |J|,
|E(U(X_J))| = 42 + 39 |J|.
```

Each added copy has 42 edges and shares exactly its three triangle edges
with the existing union. The full union has 651 points and 1407 edges.

Here is the exact arithmetic behind the lemma. The producer uses the power
basis of t, with

```
Phi_42(t) = t^12+t^11-t^9-t^8+t^6-t^4-t^3+t+1 = 0.
```

It enumerates every permutation of each triangle and determines whether
the corresponding isometry preserves or reverses orientation. It constructs
every image of every seed point, merges exact coincidences, and enumerates
all pairs. A finite-field test only rejects impossible units; surviving
pairs receive full characteristic-zero norm checks.

The independent verifier imports none of this implementation. It uses
z=exp(2pi i/7), w=exp(pi i/3), with

```
1+z+z^2+z^3+z^4+z^5+z^6=0,    w^2=w-1,    t=z^6 w.
```

The twelve monomials z^a w^b, 0<=a<6, 0<=b<2 form a rational basis:
Q(zeta_7) and Q(zeta_6) have trivial intersection, for example because
their only possibly ramified rational primes are respectively 7 and 3.
Equivalently their compositum is Q(zeta_42), of degree phi(42)=12.
Physical complex conjugation sends z to z^6 and w to 1-w.

The verifier reconstructs the seed without a linear-system inverse, using
the exact geometric-series identity

```
(x-x^(-1)) * x * sum_{k=0}^6 k x^(2k) = 7
```

for each primitive seventh root x. All coordinates of the union have
denominator seven in the tensor basis and in the t basis.

For a triangle (a,b,c), the verifier generates its six isometries from
a rotation C sending a to b to c to a, and the reflection S fixing a and
swapping b,c. It constructs C^k S^e for 0<=k<3 and e in {0,1} and checks
that the induced permutations are exactly S_3. This differs from the
producer's permutation-first enumeration. If u=b-a and v=c-a are actual
unit complex numbers, the reflection is

```
S(x) = a + u v conjugate(x-a).
```

The coordinate integerization is handled by exact divisions, which must
have zero remainder. Every point and every image label is compared with
the producer after the basis change. All 211575 unordered pairs in the
651-point union receive complete characteristic-zero norm computations,
with no numerical approximation or modular filter. The resulting unit
edges agree both with the producer's edge list and with the union of the
36 seed/image edge lists. Exact set intersections verify statements 1 and 2.
This proves the finite geometric lemma, subject to the documented checker
and exact-arithmetic trust boundary.

## Every base colouring extends

Let c:H->{0,1,2,3} be any proper four-colouring. For each g associated to
Delta_j, choose the unique permutation sigma_g of the four colour names
such that

```
sigma_g(c(a)) = c(g(a))    for all a in Delta_j.
```

This is possible because the three vertices of the unit triangle have
three distinct colours and g permutes the same three vertices. The unused
fourth colour is fixed. Assign sigma_g(c(v)) to g(v) throughout that copy.
This agrees with c on the shared triangle and is proper on the whole copy.
The geometric lemma shows that all shared points have consistent colours
and that every unit edge is checked by one of these colourings. This gives
a proper colouring of the entire 651-point union extending c. Restriction
gives the same conclusion for every X_J.

This is the usual colour-permutation argument for gluing graphs on complete
subgraphs. The contribution here is the exact complete geometric incidence
calculation for the stated isometries; no priority is claimed for clique
gluing or for the Haugland seed.

## Exact chromatic number and target-sized family

`certificate.json` contains a proper four-colouring of H in the order
P_0,...,P_6,Q_0,...,Q_6,R_0,...,R_6. The verifier checks all 42 edges.
To exclude three colours, rename colours on Delta_0 to (0,1,2). Every
other Delta_j must be a permutation of (0,1,2). The verifier checks all
6^6=46656 assignments to the remaining six triangles, and none satisfies
the seed edges. This complete small search establishes chi(U(H))=4 without
trusting a SAT solver. Since every X_J contains H, the extension theorem
implies chi(U(X_J))=4 for all 2^35 subsets J.

The vertex formula gives the exact target gate:

```
|X_J| <= 508   if and only if   |J| <= 27.
```

There are exactly

```
sum_{k=0}^27 binomial(35,k) = 34351006520
```

distinct target-sized point sets in this family. Their orders range from
21 to 507 and their edge counts from 42 to 1095. All are four-chromatic.
This counts coordinate point sets, not graph isomorphism classes. Every
subgraph of the full 651-point union is also four-colourable.

The result makes no claim about recursive triangle closures, arbitrary
rotations or translations, maps anchored on different triples, Minkowski
sums, or the full Haugland-2131 graph. It supplies no five-chromatic
unit-distance graph on at most 508 vertices.
