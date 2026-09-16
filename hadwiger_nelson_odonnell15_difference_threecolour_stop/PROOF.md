# Proof and certificate structure

## 1. Exact source

Write `q=sqrt(5)` and

`R=sqrt((5+q)/10)`, `r=sqrt(1-2q/5)`,

`T=r(1+q)/4 + sqrt(1-r^2(5-q)/8)`.

The source is the union, for `0 <= k < 5`, of the three pentagonal rings

- `R exp(i(-3+4k)pi/10)`,
- `r exp(i(7+4k)pi/10)`, and
- `T exp(i(5+4k)pi/10)`.

This is the 15-point O'Donnell pentagonal core.  Taking `t=R+T` gives the
degree-eight coordinate representation used by the package.  The verifier
reconstructs exactly 25 unit pairs among these 15 points.

## 2. Collision quotient and complete unit graph

There are 225 ordered formal differences.  All 15 diagonal differences are
zero, and additional exact equalities reduce the physical order to 171.  The
verifier recreates every difference from the 15 coordinate rows, groups equal
coefficient pairs, and compares the resulting quotient with the certificate.

For the physical points `x_i`, every one of the 14,535 quantities
`||x_i-x_j||^2-1` is reduced in the quotient ring.  Identically zero values
give the 560 edges.  Every nonzero value is evaluated using rational interval
arithmetic on the isolating interval for `t`; none contains zero.  The same
interval method proves that every pair of serialized physical points is
distinct.  Hence the edge set is the complete strict unit-distance graph.

## 3. Nonseparability

Ordinary depth-first low-link recomputation finds one component, no
articulation vertex and no bridge.  Iteratively deleting vertices of degree
less than four deletes nothing, so the degree-4 core contains all 171
vertices.  These are structural checks only; a nonempty degree core is not a
chromatic lower bound.

## 4. Chromatic number

The certificate's 171-entry word over `{0,1,2}` is checked on all 560 unit
edges, proving `chi(D) <= 3`.  The five distinct vertices

`0, 4, 14, 21, 38`

form the checked unit cycle

`0-4-14-21-38-0`.

An odd cycle is not bipartite, so `chi(D) >= 3`.  Therefore `chi(D)=3`.
In particular the graph has a proper four-colouring and cannot satisfy the
campaign's required ordinary non-four condition.

