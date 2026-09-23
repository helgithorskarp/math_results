# Tuza's conjecture for all two-neighborhood split graphs

Let `nu(G)` be the maximum number of pairwise edge-disjoint triangles of a
finite simple graph, and let `tau(G)` be the minimum number of edges meeting
every triangle. Fix a split partition `V(G)=C disjoint-union I`: `C` induces
a clique and `I` is independent. Call a vertex of `I` active if its degree
is at least two.

**Theorem (computer-assisted).** If the active vertices of `I` have at most
two distinct neighborhoods in `C`, then

    tau(G) <= 2 nu(G).

Clique order, graph order, the two neighborhood sizes, and their
multiplicities are unrestricted. The two neighborhoods need not be nested.
The theorem settles this two-type subclass, not unrestricted split graphs
or Tuza's conjecture in general. This is a complete author proof with exact
finite computation; independent peer review and formal verification remain
outstanding.

The new step is a finite closure using two compatible centered-packing
bounds and a residual-clique packing average. It joins the previous uniform
gap theorem to eliminate the whole remaining parameter range. The exact
cover normal form from the preceding research is motivation, not a logical
dependency: the simpler bipartite covers below suffice.

## 1. Finite reduction

Discard inactive vertices. Let the two neighborhoods be `S,T`, with original
multiplicities `M,N`, and put

    a=|S\T|, b=|T\S|, c=|S intersect T|, d=|C\(S union T)|,
    k=a+b+c+d, s=a+c, t=b+c, u=a+b+c.

An absent type may be represented by the empty set and multiplicity zero.
Exchange the types if necessary to obtain `a>=b`. All edges are determined,
up to isomorphism, by these counts and the two multiplicities.

### Multiplicity cap

A type of neighborhood size `s` may be capped at `max(0,s-1)` without
changing `tau`. Capping cannot increase `nu`.

Here is the cover argument, valid for any number of types. For `s>=2`,
consider a minimum cover in the graph with `s-1` copies of this type and let
`F` be its surviving triangle-free clique core. At each copy the retained
neighbors must be independent in `F[S]`. We may retain the same maximum
independent set `A` at all copies without increasing the cover. Every edge
of `F[S]` has an endpoint in `S\A`, so

    e(F[S]) <= (s-1)|S\A|.

Delete all edges of `F[S]` and restore all spokes of this type. The newly
deleted clique edges cost at most the restored spokes. This modification
preserves triangle-freeness, including at all other types. Extra copies can
now be added with all their spokes, at no extra cover cost. Repeat the
repair for each capped type. Monotonicity under taking subgraphs gives the
reverse inequality. Sizes zero and one are inactive and need no repair.

It therefore suffices to work with

    0 <= m <= max(0,s-1),  0 <= n <= max(0,t-1).             (1)

The previous uniform-gap theorem proves, for this whole class,

    2 nu(G)-tau(G) >= k^2/228-k/2-1/4.                      (2)

A self-contained restatement of its argument and attribution are in
[LARGE_ORDER.md](LARGE_ORDER.md). At `k=113` the right side is `-85/114>-1`
and is increasing thereafter. Integrality proves Tuza for `k>=113`.
For `k<=2` there is either no triangle or every triangle shares the single
clique edge, so the result is immediate.

Thus the remaining complete domain is

    3 <= k <= 112,
    a,b,c,d >= 0,  a>=b,  a+b+c+d=k,  and (1).              (3)

Allowing absent, inactive, or coincident labeled types introduces harmless
redundancy; it omits no graph. No assumption that `C` is a maximum clique is
made. In particular, independent vertices complete to `C` are included.

## 2. Two centered-packing bounds

Write `q(z)=binomial(z,2)` and define

    r(z)=1 for z=0,1;  r(z)=z-1 for even z>=2;
    r(z)=z for odd z>=3.

A complete graph of order `z` has an edge partition into `r(z)` matchings.
For even order this is the standard round-robin one-factorization; for odd
order remove one vertex from the next even order. For sizes zero and one
use a single empty matching. A matching within a neighborhood forms
edge-disjoint triangles when joined to one independent-side center.

First choose `m` colors uniformly from a fixed factorization of `K_S`, and
independently `n` colors from a factorization of `K_T`. Assign distinct
chosen colors to distinct centers. Every edge in `K_S` is chosen with
probability `m/r(s)`; every edge in `K_T` with probability `n/r(t)`.
The common edges are chosen twice with probability `mn/(r(s)r(t))`.
Delete one centered triangle for each repeated base edge. There are no
other conflicts: matchings avoid repeated spokes at a center, and different
centers have different spokes. The expected size of the resulting packing is

    H1 = m q(s)/r(s) + n q(t)/r(t) - mn q(c)/(r(s)r(t)).     (4)

Second factorize the complete graph on `S union T`. Choose `i` colors for
`S` and `j` disjoint colors for `T`, where

    0<=i<=m, 0<=j<=n, i+j<=r(u).

Restrict each chosen matching to its corresponding neighborhood. Because
the colors are disjoint, their base edges never conflict. Uniform disjoint
color choices have expected retained size

    (i q(s)+j q(t))/r(u).

Maximize over these choices to define

    H2 = max (i q(s)+j q(t))/r(u).                          (5)

The coefficients are nonnegative. For `s>=t`, first assign `i=m` colors,
then `j=min(n,r(u)-m)`; this maximizes (5). This is legitimate because
`m<=r(s)<=r(u)`. In the other order exchange the types. If `m+n<=r(u)`,
all centers receive distinct colors.

Consequently some centered packing has integer size `j0` with

    j0 >= h := ceil(max(H1,H2)).                            (6)

The independence in (4) and the deliberately disjoint palettes in (5) are
different valid constructions. We take the better existential bound; we
do not combine their triangles.

## 3. Completing the packing inside the clique

Let `p=p(k)=nu(K_k)`. We use the classical exact complete-graph packing
formula, stated in Bonamy et al., Lemma 6:

    p(k)=(q(k)-L(k))/3,
    L(k)=0                 if k=1,3 mod 6,
         4                 if k=5 mod 6,
         k/2               if k=0,2 mod 6,
         k/2+1             if k=4 mod 6.                  (7)

Formula (7) is used for `k>=3`. Its external mathematical provenance is
listed in [SOURCES.md](SOURCES.md); the finite checker does not prove the
packing-design existence theorem.

Delete the `j0` base edges of a centered packing from `K_C`, leaving `R`
with `e=q(k)-j0` edges. Every edge `vw` has at least `d(v)+d(w)-k` common
neighbors in `R`. Summing and applying Cauchy--Schwarz gives

    3 t(R) >= sum_v d(v)^2-ke >= 4e^2/k-ke,
    t(R) >= e(4e-k^2)/(3k).                                (8)

Take a fixed maximum triangle packing of `K_k` and permute its vertices
uniformly. Each of its `p` triangles is a uniformly distributed three-set,
so the expected number lying in `R` is `p t(R)/binomial(k,3)`. Some
permutation retains at least this many. Those retained triangles are
mutually edge-disjoint and share no edge with the centered packing: they
avoid all its base edges and use no independent-side spokes. Thus

    nu(G) >= f(j0),
    f(z)=z + p (q(k)-z)(4(q(k)-z)-k^2)/(3k binomial(k,3)).   (9)

We also have `nu(G)>=j0` and `nu(G)>=p`.

It is necessary to justify replacing `j0` by its lower bound `h`: `f` need
not be increasing near zero. The function `f` is a convex quadratic with
positive leading coefficient and `f(0)=p`. If `f(h)<=p`, its value supplies
no improvement on `p`. If `f(h)>p`, then `h>0` and convexity, or direct
quadratic subtraction, gives `f'(h)>0`; therefore `f(j0)>=f(h)` for
`j0>=h`. Integrality now yields the rigorously valid bound

    B(a,b,c,d,m,n) = max {p, h, ceil(f(h))} <= nu(G).        (10)

The ceiling is evaluated with signed integer division, including when the
residual triangle term in (9) is negative.

## 4. A cheap cover bound

Fix a subset `L` of the clique, of size `ell`. Keep only the crossing clique
edges between `L` and its complement. Put all centers of a type on one side
and keep only their crossing spokes. The graph left after deleting all
within-side edges is bipartite, so the deleted edges cover all triangles.

Up to complementing the whole cut, there are two relative placements of
the types. In the first, both types keep their neighbors in `L`. Assign
weights

    w(v)=m 1_S(v)+n 1_T(v),  constant E=ms+nt.

In the second, `S` keeps neighbors in `L` and `T` keeps neighbors outside:

    w(v)=m 1_S(v)-n 1_T(v),  constant E=ms.

For either placement the cover size is

    q(k)-ell(k-ell)+E-sum_(v in L) w(v).                    (11)

For fixed `ell`, choose the `ell` largest weights. There are only four
weight classes, on the four cells. On an interval in which the weight of
the newly included vertices is `w`, (11) is a quadratic with leading
coefficient one and linear coefficient `-(k+w)`. Its integer minimum is
attained by clamping `floor((k+w)/2)` to that interval. Minimize over all
four intervals and both placements. Denote the resulting integer by `U`.

Then `tau(G)<=U`. In fact `U` equals the minimum number of edges making the
whole capped graph bipartite: same-type independent vertices all have an
identical best side once the clique cut is fixed. We only use the upper
bound on `tau`, and do not equate the two parameters. The multiplicity-cap
repair may destroy whole-graph bipartiteness when lifting to the original
graph, while still preserving a triangle cover of no greater size.

## 5. Exact closure of (3)

The finite checker proves Tuza at every tuple of (3) by the bounds (10)
and (11). It may certify many tuples at once without evaluating their
individual bounds. For fixed cells, both true graph parameters `nu` and
`tau` are nondecreasing as `m,n` increase. Thus the rectangle

    ml<=m<=mh, nl<=n<=nh

is certified whenever

    2 B(a,b,c,d,ml,nl) >= U(a,b,c,d,mh,nh).                (12)

Indeed `2nu(m,n)>=2nu(ml,nl)>=2B(ml,nl)>=U(mh,nh)>=tau(mh,nh)>=tau(m,n)`.
No monotonicity assumption about either numerical formula is needed.
An uncertified rectangle is bisected into two disjoint integer rectangles
until (12) holds or a singleton fails. A failed singleton gives a nonzero
exit code. Since at least one nontrivial interval strictly shrinks, the
recursion terminates. Each initial rectangle is exactly (1).

`verify_rectangles.cpp` enumerates every shape by `k,a,b,c` and sets `d`
from their sum. It uses the four constant-weight intervals to compute `U`.
The full deterministic result is

    shapes                  3,642,650
    represented tuples      7,636,614,579
    certified rectangles    11,301,625
    visited rectangles      18,960,600
    failures                0.

`verify_literal.cpp` independently traverses shapes by `k,c,d,b`, uses a
different bisection rule, evaluates `U` by sorting individual vertex weights
and scanning **every** `ell=0,...,k`, and evaluates the common-palette
allocation at both feasible endpoints. It uses an expanded rational
numerator for (10). It closes the same domain with

    certified rectangles    12,157,453
    visited rectangles      20,672,256
    failures                0.

This is a second author implementation, not independent peer review. Both
implementations use the mathematical lemmas in Sections 1--4.

The domain count is also checked in independent coordinates. For
`0<=t<=s<=k`, the possible intersection sizes are exactly
`max(0,s+t-k)<=c<=t`. Each such shape has `max(1,s)max(1,t)` multiplicity
pairs. Summing this expression separately for each `k` agrees with every
reported row, as well as the final total.

The standard-library Python audit compares each of 3,402 tuples through
`k=8` against `Fraction` arithmetic and a literal examination of all clique
subsets for (11). It exhausts the actual palette choices / a disjoint-color
dynamic program on 876 tuples through `k=6`. On all 384 tuples through
`k=5`, a direct graph constructor and exact triangle-packing search produce
packings meeting (10), which are then checked edge by edge. Round-robin
palettes are checked through order 12, including empty cases. Invalid input
and tight `K4` controls check important conventions.

The two full exact closures establish the finite lemma for (3), subject to
the explicit execution trust boundary below. Combining it with (2), the
small clique cases, and the cap proves the theorem.

## 6. Arithmetic, reproducibility, and trust

All finite mathematical computations use integers or Python `Fraction`.
There are no floating-point comparisons, solver calls, graph catalogues,
random samples, or external datasets. The averaging arguments above are
universal counting arguments, not randomized evidence.

The C++ domain is explicitly restricted to `3<=k<=112`. Every multiplicity
is at most 111, `q(k)<=6216`, `p(k)<=2072`, `0<=h<=q(k)`, and
`0<=e<=6216`. The largest common denominator in (9) is
`3k binomial(k,3)<77,000,000`. Its numerator in the second implementation is
bounded in absolute value by

    6216*77,000,000 + 2072*6216*12544 < 10^12.

All other arithmetic intermediates are smaller; domain counters are below
`10^10`. Signed 64-bit arithmetic therefore suffices with ample room.
Negative rational ceilings use division toward zero correctly. Input
validation prevents accidentally extending the supported arithmetic domain.

The universal reductions are unformalized mathematics. The finite closure
trusts the published C++ source, the compiler/runtime, and the execution
hardware. The formula (7) trusts the cited classical packing theorem; (2)
is reproduced with attribution in the appendix. The author checks reduce
implementation risk but are not a proof-assistant certification or an
independent review. No bulky certificate or hidden run state is needed:
source plus the two small row reports reproduce the whole finite closure.
Exact commands, versions, measured cost, and output hashes are in
[README.md](README.md) and the manifest.
