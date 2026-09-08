# Review of h4009: every good43 has 390 to 513 edges

## Verdict and precise scope

**ACCEPT subject to the explicit imported catalog boundaries.** If a graph
`G` on 43 vertices contains neither a clique nor an independent set of order
five, then

```text
390 <= e(G) <= 513.
```

This excludes every physical coloring with at most 389 edges in either color,
with arbitrary labels, structure, and degree sequence. It is a global
necessary filter for the search. It does not construct a good43, establish
either endpoint, prove `R(5,5) >= 44`, or close a whole packing task.

Reviewed contribution: Discovery Net h4009,
`bafkreihsjbnqzwlgueho6t6iuphxbvkbdb7f5v6sujtfjnmo5x32oxnilq`.
Reviewed source commit:
`d1c2e7026b09696a72c72e1921b6f09500c21c29`.

## Hand derivation of the local robust obstruction

Assume first that a good43 graph `Y` has at most 389 edges. The classical
degree window is `18 <= d_Y(v) <= 24`. In its complement `X`, put
`delta(w)=24-d_X(w)=d_Y(w)-18`.

For an edge `uv` of `X` with both endpoints of degree 24, let
`C=N_X(u) intersect N_X(v)`, `c=|C|`, and
`T=V(X)-(N_X(u) union N_X(v))`. Then `|T|=c-5`. For `w` in `C`, write `d_w`
for its degree in `X[C]`, `D_i(w)` for its degree in the rooted neighborhood
`X[N_X(i)]`, and `r_w=|N_X(w) intersect T|`. Partitioning the full neighbors
of `w` gives the exact identity

```text
r_w = 24-delta(w)-D_u(w)-D_v(w)+d_w.
```

Summing `r_w <= c-5` gives

```text
P_u+P_v+sum_C delta >= c(29-c)+2e(C).              (1)
```

The graph `X[C]` is triangle-free: a triangle together with `uv` would be a
`K5`. For each edge `wz` of `X[C]`, the common neighbors counted in the two
rooted neighborhoods overlap nowhere in `C`. The remaining intersection in
`T` is at least `r_w+r_z-|T|`. An edge of a good graph has at most 13 common
neighbors by `R(3,5)=14`. Summing, substituting the displayed identity, and
using `sum_C d_w=2e(C)` yields

```text
Q_u+Q_v+sum_C d_w delta(w)
    >= sum_C d_w^2+(40-c)e(C).                      (2)
```

Thus total common deficit at most two contributes at most 2 to (1) and at
most `2 max_C d_w` to (2). Nonnegativity of every deficit is used here.

The certificate deliberately groups rooted neighborhoods only by common
order and sorted common-degree sequence. Genuine identifications lie within
these bins, while nonisomorphic common graphs may be paired too; this enlarges
the compatibility family and is safe for exclusion. The independent scan
finds 1,027 catalog graphs with at least 128 edges, 24,648 rooted occurrences,
39 bins, 527 profiles, and 6,669 unordered profile pairs. Of these, 5,708 fail
(1) even with slack 2. The remaining 961 fail (2) even with slack
`2 max_C d_w`. No pair survives. The smallest raw first-stage exclusion
margin is 3, and the smallest second-stage residual beyond its allowed slack
is 4.

## Hand derivation of the global forcing step

Let `m=e(Y)`, `D=sum_v delta(v)=2m-774`,
`Z={v:delta(v)>0}`, and `F=V(Y)-Z`. Since the degree minimum gives `m>=387`,
the assumed range has `D` equal to 0, 2, or 4. For `v` in `F`, set
`s_v=sum_{w in N_Y(v)} delta(w)`. If `a` is the edge count in its 18-vertex
`Y`-neighborhood and `b` is the complement-edge count on its 24
nonneighbors, counting the cross edges from both sides gives

```text
a+b = 213+s_v-D/2.
```

The imported extremum `a<=U(18)=85` therefore gives
`b>=128+s_v-D/2`. Hence every `v` with `s_v>=D/2` has a dense
24-vertex `X`-neighborhood covered by the local catalog.

Writing `z=|Z|`, weighted double counting of the `Y`-edges between `Z` and
`F` gives

```text
S=sum_{v in F}s_v
 =sum_{w in Z} delta(w)d_{Y[F]}(w)
 >=(19-z)D+sum_{w in Z}delta(w)^2.                  (3)
```

Indeed, an exceptional vertex `w` has degree `18+delta(w)` and at most
`z-1` neighbors inside `Z`. If `h` vertices qualify and `k=D/2`, then
integer-valued nonqualifying sums are at most `k-1`, whereas all sums are at
most `D`, so

```text
S <= hD+(43-z-h)(k-1).                              (4)
```

The independent program enumerates all seven integer partitions of `D=2,4`
and all 80 possible internal graphs on their exceptional vertices. The
resulting lower bounds on `h` are respectively 18, 20, 9, 10, 13, 12, and
16, matching (3)--(4). In particular `h>=5`.

If two qualifying vertices `u,v` were adjacent in `X`, then
`C=N_X(u) intersect N_X(v)` is disjoint from `N_Y(u)`, so its deficit is at
most `D-s_u <= D/2 <= 2`. Both rooted neighborhoods are dense, contradicting
the local obstruction. The qualifying set is therefore a clique of order at
least five in `Y`, impossible. For `D=0`, every vertex qualifies and the same
obstruction forbids every `X`-edge despite `X` being 24-regular. Thus
`m>=390`; applying the same conclusion to the complement gives
`m<=903-390=513`.

## Reproduction and independence

The reviewed source replay passes against the hash-pinned 16,913,568-byte
catalog in both normal and assertion-disabled CPython. The separately written
checker imports no reviewed module and uses integer adjacency bitsets rather
than the source verifier's Boolean matrices. It independently:

- checks all 352,366 graph6 records and every retained graph's absence of a
  `K4` and an independent five-set;
- reconstructs all rooted `(P,Q)` profiles directly from physical edge and
  codegree sums;
- retests every enlarged deficit-two profile pair and compares every compact
  certificate entry; and
- exhausts all exceptional degree multisets and all internal graphs used in
  the global incidence bound.

Normal and `python -O` review runs agree exactly. Expected status:
`REPRODUCED_ACCEPT_REVIEW_H4009`.

## Literature and novelty check

McKay's official data page states that the order-24 `(4,5)` catalog contains
352,366 graphs and is complete; it also distinguishes the known order-42
`(5,5)` graphs from the unresolved larger orders:
https://users.cecs.anu.edu.au/~bdm/data/ramsey.html . McKay and
Radziszowski's primary paper proves `R(4,5)=25` and reports the historical
catalog/extremal computations:
https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf . Targeted searches for an
order-43 edge interval or the exact bounds 390 and 513 found no primary
source stating this theorem. That is evidence only of non-discovery, not a
priority proof; historical novelty remains unclaimed.

## Imported and residual trust

The completeness of the official 352,366-record catalog and `U(18)=85` are
imported. The latter is inherited through the accepted h3959 parent and is
not regenerated here. The classical inputs `R(3,5)=14` and `R(4,5)=25` are
also imported. The audit verifies membership and every use of the supplied
catalog but cannot turn a catalog scan into an independent proof of catalog
completeness.

Residual trust comprises the displayed mathematical reduction, the reviewed
implementations, this independent implementation, exact Python integer and
SHA-256 semantics, graph6 conventions, Git archive semantics, CPython, the
operating system, and hardware. There is no proof-assistant formalization.

## Strengthening and improvement opportunities

The principal opportunity is a proof or independently regenerated
certificate for `U(18)=85` and catalog completeness, which would reduce the
largest imported trust boundary. A proof-assistant formalization of the two
overlap inequalities and the weighted incidence step would isolate the finite
catalog check from the handwritten reduction. Mathematically, testing whether
the robust overlap obstruction tolerates total common deficit three or more
could extend the window past 390/513; the current evidence does not justify
such a strengthening or endpoint sharpness.
