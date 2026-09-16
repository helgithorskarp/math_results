# Proof and exact scope

## 1. Frozen construction

Work in `K = Q(zeta_546)`. The embeddings

```text
zeta_13 = zeta_546^42,
zeta_14 = zeta_546^39
```

put both clouds in one exact field. Define

```text
A_13(i,j) = (zeta_13^i - zeta_13^j) / (1 - zeta_13),
A_14(i,j) = (zeta_14^i - zeta_14^j) / (1 - zeta_14^2).
```

The denominators are nonzero. These similarities send the chosen oriented
source-shell edges to `0--1`. Their images have 157 and 99 distinct points.
The relative placement is completely fixed by these formulas.

The declared completion rule is: for each complete-graph unit edge whose two
endpoints are private to different clouds, add both equilateral third points.
This is fixed before the chromatic query.

## 2. Exact equality and distance decisions

The checker represents a coordinate as a fraction `p(zeta)/q(zeta)` with
integral polynomials. For two such fractions, equality is equivalent to

```text
p1*q2 - p2*q1 = 0 mod Phi_546.
```

Writing `D = p1*q2 - p2*q1` and `Q = q1*q2`, their distance is one exactly
when

```text
D(zeta) D(zeta^-1) - Q(zeta) Q(zeta^-1) = 0 mod Phi_546.
```

`verify.py` constructs `Phi_546` from the exact factorization of `X^546-1`
and performs these reductions with integer arithmetic. It compares all
unordered pairs after exact collision merging; no tolerance, supplied edge
list, or floating coordinate is used.

The two label sets merge at exactly three physical points:

```text
0:  P13(0,0) = P14(0,0)
1:  P13(0,1) = P14(0,2)
13: P13(1,0) = P14(2,0)
```

There are 492 unit pairs. Exactly 312 lie in the `P13` image and 182 in the
`P14` image; two edges lie in both. No unit edge joins a `P13`-private point
to a `P14`-private point. Therefore the declared completion has empty input
and adds no point.

## 3. Chromatic decision

`expected.json` contains a ternary word in physical-vertex order. The checker
verifies its length, alphabet, and every one of the 492 edge inequalities.
This proves `chi <= 3`.

The 13 distinct vertices

```text
6,5,4,3,2,1,0,12,11,10,9,8,7
```

form a cycle in the reconstructed complete graph. The checker validates all
13 closing edges, so the graph is nonbipartite and `chi >= 3`. Hence its
ordinary chromatic number is exactly three.

The complete graph has components of orders 197, 28, and 28. Its 3-core has
197 vertices and its 4-core is empty. Consequently it fails the predeclared
gate requiring both clouds in one nonseparable 4-core, independently of the
stronger exact three-colouring stop.

## 4. Limitation

This proves only the outcome of the displayed edge-normalized placement and
its displayed private-cross equilateral completion. It is not a theorem about
all `P13`--`P14` placements or all heterogeneous polygon difference-cloud
unions, and it is not progress on the global 509-vertex lower boundary.
