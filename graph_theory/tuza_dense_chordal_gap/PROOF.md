# A strict Tuza gap for dense chordal graphs

All graphs are finite, simple, and undirected. Write `nu(G)` for the maximum
number of edge-disjoint triangles, `tau(G)` for the minimum number of edges
meeting every triangle, and `nu*(G)=tau*(G)` for their common fractional LP
optimum. A chordal graph admits a perfect elimination ordering: the later
neighbors of every vertex form a clique. We use this standard equivalent
definition, including disconnected graphs.

## Statements

**Theorem 1 (finite fractional bound).** Every chordal graph with `n>=1`
vertices and `m` edges satisfies

    2nu*(G) - tau(G) >= m^2/(50 n^2) - 2n/3.             (1)

**Theorem 2 (integer bound at every fixed positive density).** For every
fixed `0<beta<1/2`, there is `N_beta` such that every chordal graph with
`n>=N_beta` and `m>=beta n^2` satisfies

    2nu(G) - tau(G) >= m^2/(100 n^2),                    (2)
    tau(G) <= (2 - 3beta/100) nu(G).                     (3)

Thus Tuza's inequality holds, with a strict quadratic margin, for all
sufficiently large chordal graphs in each fixed positive edge-density
class. Split graphs and interval graphs are included. Density here means
`m/n^2`, not `m/binom(n,2)` and not a minimum-degree hypothesis.

**Theorem 3 (bounded neighborhood types, arbitrary multiplicities).** Let
`V(G)=C disjoint-union I` be a split partition, `|C|=k`, with at most `r>=1`
distinct neighborhoods of size at least two among vertices of `I`. Then

    2nu*(G) - tau(G)
      >= [k^2 - 2k - 32(r+1)] / [8(8r+11)].             (4)

For each fixed `r`, there is `K_r` such that all such graphs with `k>=K_r`
satisfy

    2nu(G) - tau(G) >= k^2/[16(8r+11)].                 (5)

In particular, unrestricted three-type split graphs satisfy Tuza's
inequality for every sufficiently large clique order, with the margin
`k^2/560`. There is no bound on their original multiplicities or on the
number of inactive independent vertices.

The proofs below are ordinary mathematical proofs, not proofs by the
accompanying finite audit. The integer statements use the uniform
Haxell--Rodl approximation theorem. We specify the dependence on its
modulus but do not provide a usable numerical `N_beta` or `K_r`. No claim
is made for the remaining orders, for all chordal graphs, or for all
three-type split graphs. The proposed stronger factor `3/2` in the
fractional problem is not used or proved here.

## 1. Classical inputs and the zero/unit framework

We use two external theorems, with sources in [SOURCES.md](SOURCES.md):

* Krivelevich: `tau(H)<=2nu*(H)` for every finite simple graph `H`.
* Haxell--Rodl: for every fixed `eta>0` there is `N_HR(eta)` such that
  every graph `H` on `v>=N_HR(eta)` vertices satisfies
  `0<=nu*(H)-nu(H)<=eta v^2`.

The following zero/unit-edge framework is already used by Yuster (2012,
Section 2); it is not claimed as new. Choose an optimal fractional cover
`f:E(G)->[0,1]`. Truncation at one allows the indicated range. Let
`Z={e:f(e)=0}`, `z=|Z|`, and let `W` be any subset of edges with `f(e)=1`;
put `h=|W|` and `D=2nu*(G)-tau(G)`.

Deleting `W` and restricting `f` gives

    nu*(G-W) <= nu*(G)-h.

Every triangle cover of `G-W`, together with `W`, covers `G`. Apply
Krivelevich to `G-W` (which need not be chordal) to obtain

    tau(G) <= h + tau(G-W)
           <= h + 2nu*(G-W)
           <= 2nu*(G)-h.

Consequently

    D >= h.                                             (6)

Complementary slackness with an optimal fractional packing says that
every edge with positive cover weight has packing load one. Summing these
loads, and counting any triangle at most three times, gives

    3nu*(G) >= m-z.

A random two-coloring has at most `m/2` expected monochromatic edges;
deleting those edges gives a triangle cover. Therefore

    D >= m/6 - 2z/3.                                    (7)

These facts hold for arbitrary graphs. The new structural input below is
the bound on `z` afforded by a perfect elimination ordering.

## 2. Elimination forces unit-weight edges

Fix a perfect elimination ordering of a chordal graph. Take `W` to be all
unit-weight edges. For a vertex `v`, let `A_v` be its later neighbors
joined to `v` by zero-weight edges, and put `d_v=|A_v|`. The set `A_v` is
a clique. For any distinct `a,b` in `A_v`, the triangle `vab` forces

    f(ab) >= 1-f(va)-f(vb) = 1.

Thus every edge of `G[A_v]` is in `W`, and

    binom(d_v,2) <= h,
    d_v <= 1+sqrt(2h).

Every zero-weight edge is counted exactly once, at its earlier endpoint.
It follows that

    z <= n(1+sqrt(2h)).                                 (8)

The edges forced by different vertices may coincide. No disjointness of
these sets is assumed: each individual set has at most `h` edges, and we
sum the resulting degree bounds, not the forced-edge counts.

Combining (6)--(8),

    D >= h,
    D >= m/6 - (2n/3)(1+sqrt(2h)).                       (9)

Set `a=m^2/(50n^2)`. If `h>=a`, (1) follows from the first inequality.
Otherwise `sqrt(2h)<m/(5n)`, so the second gives

    D >= m/30 - 2n/3 >= a - 2n/3.

The last inequality follows from `m<=n^2/2`, since
`a<=m/100<=m/30`. This also treats `m=0` through the first case.
Theorem 1 follows.

## 3. Uniform integer rounding at fixed density

Fix `0<beta<1/2`, and choose

    eta = beta^2/400,
    N_beta = max(1, N_HR(eta), ceil(400/(3 beta^2))).     (10)

For `n>=N_beta`, Haxell--Rodl gives
`2(nu*-nu)<=beta^2 n^2/200`, while
`2n/3<=beta^2 n^2/200`. Hence (1) yields

    2nu-tau >= m^2/(50n^2) - beta^2 n^2/100
            >= m^2/(100n^2),

using `m>=beta n^2`. This proves (2). Finally `3nu<=m`, and so

    m^2/(100n^2) >= [3m/(100n^2)]nu >= (3beta/100)nu,

which proves (3).

The accuracy `eta` is fixed before sending `n` to infinity. We do not
substitute an accuracy tending to zero with `n` into an unspecified
asymptotic cutoff. This is an exact eventual integer inequality, rather
than only `tau<=2nu+o(n^2)`.

## 4. Multiplicity reduction for split graphs

This cap is reused from the earlier split-graph work; see
[the two-type proof](../tuza_two_type_complete/PROOF.md) and
[the independent review](../tuza_two_type_complete_review1/README.md).
We include its argument so that the present proof is self-contained.

Vertices of `I` with at most one neighbor lie in no triangle and can be
deleted. If a neighborhood `S` has size `s>=2`, cap its multiplicity at
`s-1`. This preserves `tau`, while neither `nu` nor `nu*` increases.

To prove cover preservation, begin with a minimum cover of the capped
graph and its surviving triangle-free clique core `F`. Copies of `S` may
all retain a common maximum independent set `A` of `F[S]`; this costs no
more than any previous choice of their retained spokes. Every edge of
`F[S]` has an endpoint in `S\A`, so

    e(F[S]) <= (s-1)|S\A|.

When a type was capped, there are `s-1` copies. Delete these surviving
core edges and restore all spokes of this type. The new core deletions
cost no more than the restored spokes, and now arbitrarily many copies
of the type can be added without creating a triangle. Repeat for all
capped types. Deleting additional core edges cannot spoil an earlier
repair. This produces a cover of the original graph of no greater size;
subgraph monotonicity supplies the reverse inequality. Packing
monotonicity, integral and fractional, follows from subgraph containment.

In the reduced graph let the nonzero multiplicities and neighborhood
sizes be `m_i,s_i`, for at most `r` types, and write

    p=sum_i m_i,  E=sum_i m_i s_i,  q=binom(k,2).

Then `m_i<=s_i-1`, `p<=r(k-1)`, and Cauchy--Schwarz gives

    p^2 <= r sum_i m_i^2 <= r E.                        (11)

## 5. A sharper gap with a fixed number of types

Work first in the reduced graph. In Section 1 take `W` to consist only
of the unit-weight edges within `C`, and again put `h=|W|` and
`L=1+sqrt(2h)`. Every vertex, whether in `C` or `I`, has at most `L`
zero-weight neighbors in `C`: those neighbors form a clique, whose
edges are forced to have weight one by the same triangle argument.

The zero clique edges are therefore at most `kL/2`, and the zero spokes
at most `pL`. By (11),

    z <= L(k/2+p) <= L(k/2+sqrt(rE)).

Apply (7), now with total edge count `q+E`:

    D >= (q+E)/6 - kL/3 - (2L/3)sqrt(rE)
      >= q/6 - kL/3 - (2r/3)L^2.                       (12)

The second line is the nonnegativity of
`(sqrt(E)-2L sqrt(r))^2/6`. Also `(k-4L)^2>=0` gives

    kL/3 <= k^2/24 + (2/3)L^2.

Since `(sqrt(2h)-1)^2>=0`, we have `L^2<=4h+2`. Substitute both bounds
into (12) to obtain

    D >= (k^2-2k)/24 - [8(r+1)/3]h - 4(r+1)/3.

Using `h<=D` from (6) and rearranging proves (4) in the reduced graph.
The cap preserves `tau` and can only decrease `nu*`, so (4) also holds
in the original graph.

For completeness, an exact choice of the eventual threshold in terms of
the Haxell--Rodl modulus is

    A_r = 8r+11,
    eta_r = 1/[64 A_r (r+1)^2],
    K_r = max(N_HR(eta_r),
              ceil(4+sqrt(16+128(r+1)))).               (13)

The reduced graph has order `v` between `k` and `(r+1)k`. For `k>=K_r`,
Haxell--Rodl implies

    2(nu*-nu) <= 2 eta_r v^2 <= k^2/(32 A_r).

The other part of (13) says `2k+32(r+1)<=k^2/4`. Applying (4) leaves

    2nu-tau >= 3k^2/(32 A_r) - k^2/(32 A_r)
             = k^2/(16 A_r).

Finally pass back to the original graph using the cap. This proves (5).
For `r=3`, (13) becomes

    K_3 = max(N_HR(1/35840), 27),

which is a dependence formula, not a claimed numerical cutoff.

## 6. Scope and remaining work

The chordal theorem permits arbitrarily many neighborhood types in a
split graph. The bounded-type theorem also permits arbitrary original
multiplicities, even when the original graph has very small edge density;
rounding is applied only after the exact cap.

For each fixed `r`, any split-graph counterexample can therefore be
reduced to bounded clique order and bounded multiplicities. This gives a
finite-exception reduction up to inactive vertices and cloning, but the
present proof does not make the finite search practically executable.
Effective rounding for the reduced class, or a direct integer packing
argument, is the next missing bridge. The previously certified all-order
two-type and co-sunflower theorems retain their stronger small-order
conclusions.

The dependence on fixed positive density in Theorem 2 matters: disjoint
copies of `K4` have `tau=2nu` at arbitrarily large order, and their density
tends to zero. Theorem 2 does not settle sparse chordal graphs.
