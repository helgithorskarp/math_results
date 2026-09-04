# A parametric two-clique dichotomy closes the Albertson `r=27` cases `h=11,12`

This note advances the sole surviving Albertson frontier row

```text
|V(G)|=53,  |E(G)|=713,  chi(G)=27.
```

Let

```text
L={v:d_G(v)=26},  Q=V(G)-L,  h=|Q|,  H=complement(G).
```

The preceding Gallai-block reduction proves that, conditionally for every
`10<=h<=12`, the graph `G[L]` is two disjoint clique blocks, with at most one
bridge between them.  The argument below proves a parameterized terminal
dichotomy for every one of those normal forms: `G` is 26-colourable or
contains a subdivision of `K27`.  Hence none can be a counterexample.
Together with the already proved `h>=10` bound, this gives

```text
             |Q| >= 13.                                  (1)
```

In particular, the argument independently re-closes `h=10` and newly closes
all eight exact profiles at each of `h=11` and `h=12`.  It does not treat
`h>=13`, where the two-large-block argument reaches an equality boundary,
and therefore does not prove Albertson's conjecture for chromatic number 27.

## The parametric normal form

For one of `10<=h<=12`, write the two low cliques as `C,D`.  There are
positive integers `d,e` such that

```text
|C|=27-h+d,  |D|=27-h+e,  d+e=h-1.                       (2)
```

If there is no bridge, every row of `H[C,Q]` has size `d` and every row of
`H[D,Q]` has size `e`.  If the bridge is `c0d0`, its two endpoint rows have
sizes `d+1,e+1`, while all other rows have sizes `d,e`.  Also `H[C,D]` is
complete bipartite, except for the one absent edge `c0d0` in the bridge
case.  The exact profile table has `d,e>=2`.

Two consequences of connected-complement criticality will be used throughout.
Stehlik's theorem makes `H` factor-critical, because every `G-v` has a
26-colouring into pairs.  Moreover, `H` has no conformal triangle: a triangle
whose deletion leaves a perfect matching would be one independent triple and
25 independent pairs in `G`, hence a 26-colouring.  Finally, every `q in Q`
satisfies

```text
d_H(q) <= 25,                                             (3)
```

because every vertex of `Q` has degree at least 27 in the 53-vertex graph
`G`.

## Two matching facts

We use the following elementary consequence of Konig's theorem.

**Uniform-row lemma.**  Let a bipartite graph have left part `X`, with
`|X|>s`, and suppose every left degree is at least `s`.  Either it has a
matching of size `s+1`, or every left row is the same `s`-set.

Indeed, a vertex cover of size at most `s` cannot contain a left vertex.  If
it contained `j>0` left vertices, any uncovered left row would have to fit
its at least `s` neighbours into at most `s-j` right cover vertices.  Thus a
minimum cover witnessing matching number at most `s` lies entirely on the
right, and equality forces all rows to be the same set.

We also need a small contraction observation.  Let `uv` be an edge of
`H[Q]`, viewed as a two-vertex colour class of `G`, with all other high
vertices singleton classes.  If a low row originally has size `e`, it is
compatible with at least `e-1` of these `h-1` classes.  If the resulting
incidence graph has no `e`-matching, the uniform-row lemma says all its rows
are the same `(e-1)`-set.

If this failure occurs for two distinct edges `uv` and `xy`, then all the
original low rows are equal.  For any two original rows, equality after the
first contraction makes their symmetric difference a subset of `{u,v}`;
equality after the second makes it a subset of `{x,y}`.  The intersection of
two distinct two-sets has order at most one, while the symmetric difference
of equal-sized rows has even order.  It is therefore empty.

## The case with no low bridge

Suppose first that `H[C,Q]` has a `(d+1)`-matching and `H[D,Q]` has an
`(e+1)`-matching.  Give the `h` high vertices distinct colours and extend
them along the two matchings.  When a high colour is extended on both sides,
its three vertices are independent because `H[C,D]` is complete.  By (2),
exactly `26-h` vertices remain on each low side.  Pair them across
`H[C,D]`.  The resulting number of colours is

```text
h+(26-h)=26.
```

Thus one incidence graph is deficient in any surviving case.  Relabel so it
is the `C` side.  The uniform-row lemma gives a common `d`-set `S` such that

```text
N_H(c) intersect Q = S  for every c in C.                (4)
```

Put `T=Q-S`.  The 27 vertices `C union T` induce a complete graph in `G`
apart from the edges of `H[T]`.

### Zero or one target edge

If `H[T]` is empty, this is a `K27`.  Suppose its only edge is `uv`.  A
vertex `s in S` adjacent in `G` to both ends gives the path `u-s-v`.
Assume no such `s` exists.

If there are support vertices `s_u,s_v` which meet only `u`, respectively
only `v`, in `H`, then

```text
u-s_v-s_u-v
```

works when `s_us_v` is an edge of `G`.  Otherwise each of `s_u,s_v` has at
least two high-complement incidences, including their mutual edge.  From
(2),(3), each then has at least `30-h>=18` neighbours in `G[D]`; since
`|D|<=24`, they have a common such neighbour, which can be inserted between
them.

In every remaining support pattern, one endpoint, say `u`, meets all `d`
supports in `H`.  Including `uv`, it has at least `d+1` high-complement
neighbours, and therefore at least

```text
|D|-(25-(d+1)) = 2
```

neighbours in `G[D]`.  If some support `s` meets `u` but not `v`, then `s`
has at least `29-h>=17` neighbours in `G[D]`; two distinct vertices of the
clique `D` give the path `u-d1-d2-s-v`.  If every support meets both ends,
both `u` and `v` have two neighbours in `G[D]`, and distinct choices give
`u-d1-d2-v`.  Thus one target edge always has an internally disjoint route,
and `C union T` is the branch set of a `TK27`.

### Two contractions force double uniformity

It remains that `H[T]` has two distinct edges.  Contract each edge in turn
as a high colour class.  If the contracted incidence graph on the `D` side
has an `e`-matching, use that matching, attach `d` vertices of `C` to the
singleton classes in `S`, and pair the remaining `27-h` vertices on each low
side.  The `h-1` high classes and `27-h` low pairs give 26 colours.

Otherwise the two-contraction observation forces a common `e`-set `R` with

```text
N_H(d') intersect Q = R  for every d' in D.              (5)
```

The sets `S,R` are disjoint: a vertex in their intersection would have all
`53-h>=41` low vertices as neighbours in `H`, contrary to (3).  Since
`d+e=h-1`, there is a unique vertex `z` with

```text
Q = S disjoint-union R disjoint-union {z}.               (6)
```

We now close this double-uniform form using only factor-criticality and the
absence of a conformal triangle.

Choose `s0 in S` and a perfect matching of `H-s0`.  If `s_M,r_M` count the
endpoints in `S,R` of its high-high matching edges, low-side balance gives

```text
r_M-s_M=1.                                               (7)
```

The vertex `z` has no low neighbour in `H`, so it is matched in `H[Q]`.  If
it were matched to `S`, (7) would force an edge inside `R`.  That edge,
together with any vertex of `D`, would be a conformal triangle: match `z` to
its `S` neighbour, attach the other support vertices to their low blocks,
and pair the equally many residual low vertices.  This is impossible.
Hence `z` has a neighbour in `R`.  The symmetric argument after deleting a
vertex of `R` shows that `z` also has a neighbour in `S`.

Put

```text
X=N_H(z) intersect S,   Y=N_H(z) intersect R.
```

Both sets are nonempty.  There is no edge of `H` between `X` and `Y`, since
such an edge, with `z`, is a high-vertex triangle; after deleting it, attach
the remaining `S` and `R` vertices to `C` and `D`, then pair the equal
residual low sets.  The triangle would be conformal.

There are also no edges inside `S` or inside `R`.  For example, after the
preceding argument choose `y in Y`.  An edge `s1s2` of `H[S]`, together with
any vertex of `C`, is a triangle.  After deleting that triangle, match `z`
to `y`, attach the other `d-2` vertices of `S` to `C`, attach the other
`e-1` vertices of `R` to `D`, and pair the two residual low sets, each of
order `28-h`.  This would make the triangle conformal.  The argument for
`H[R]` is symmetric, using a vertex of `X`.

If `|X|<=|Y|`, inject `X` into `Y`.  For each `x in X`, with image `y`,
choose a distinct `c_x in C` and replace the missing branch edge `zx` by

```text
z-c_x-y-x.                                               (8)
```

All three edges lie in `G`: (4) and (6) give the first two, and the absence
of `H[X,Y]` gives the third.  These internally disjoint paths turn
`D union S union {z}` into a `TK27`; its only missing branch edges were the
`zx` with `x in X`.  If `|Y|<=|X|`, the symmetric construction turns
`C union R union {z}` into a `TK27`.  One of the two inequalities always
holds, completing the unbridged case.

## The case with one low bridge

Let the bridge be `c0d0`.  The incidence graph on the `C` side always has a
`(d+1)`-matching.  If its nonendpoint rows do not already have one, the
uniform-row lemma makes them a common `d`-set, and the extra neighbour of
`c0` augments a matching of that set.  The same holds on the `D` side.

The two matchings give the preceding 26-colouring unless both bridge
endpoints receive the same high colour.  If both endpoints remain residual,
the residual cross-pairing can be permuted to avoid `c0d0`, since
`26-h>=14`.  Therefore, if no compatible pair of matchings exists, every
`(d+1)`-matching on the `C` side and every `(e+1)`-matching on the `D` side
covers its bridge endpoint, and the possible partners of the two endpoints
form one common singleton `{z}`.  Applying the uniform-row lemma to the
nonendpoint rows gives disjoint sets `S,R` of sizes `d,e` with

```text
N_H(c,Q)=S                 (c != c0),
N_H(c0,Q)=S union {z},
N_H(d',Q)=R                (d' != d0),
N_H(d0,Q)=R union {z}.                                  (9)
```

Again `S,R,{z}` partition `Q`.  Any edge of `H[S]`, `H[R]`, `H[z,S]`, or
`H[z,R]` creates an explicit conformal triangle.  For example, an edge of
`H[S]` forms a triangle with a nonendpoint of `C`; after deleting it, match
`z` to `c0`, attach the remaining supports to their low blocks, and pair the
residual lows.  An edge `zs` forms the triangle `{c0,z,s}`.  The other two
cases are symmetric.  Thus every edge of `H[Q]` lies between `S` and `R`.

Now `C union R union {z}` is a `K27` in `G` with only `c0z` missing.  For
any `d1 != d0`, the path

```text
c0-d0-d1-z                                               (10)
```

uses the low bridge, an edge of the clique `D`, and an edge present by (9).
It completes a `TK27`.  This closes the bridge case and proves (1).

## Reproduction and trust boundary

Run under CPython 3.9 or later; there are no third-party dependencies:

```sh
python3 verify.py
```

The checker reconstructs all 22 exact `h=10,11,12` profiles, exhaustively
checks the two-distinct-contractions row-rigidity statement, audits every
one-target support type pattern, checks all balance and residual-pair counts,
and decodes representative double-uniform and bridge `TK27` certificates for
every profile.  It uses exact integer, set, tuple, and bit-mask arithmetic,
without a solver, randomness, floating point, generated input, or external
package.

The proof, rather than an enumeration, bridges arbitrary incidence matrices
to the uniform forms.  The mathematical trust boundary is Sadhu's September
2026 two-order connected-complement frontier, Stehlik's colouring theorem,
the classical Gallai low-vertex block theorem as used in the preceding
two-clique reduction, Konig's matching-cover theorem, and the previously
proved `h>=10` starting point.  The present matching, contraction, conformal
triangle, and subdivision arguments are deductive.

## Sources and novelty scope

* A. Sadhu, [*Albertson's Conjecture Holds for `r` at Most 26*](https://arxiv.org/abs/2609.01682v1),
  for the order-53/order-54 connected-complement frontier and the exclusion of
  a topological `K27` from a counterexample.
* M. Stehlik, [*Critical graphs with connected complements*](https://doi.org/10.1016/S0095-8956(03)00069-8),
  JCTB 89 (2003), 189--194.
* T. Gallai's low-vertex theorem, reproduced as Theorem 8 in A. Kostochka's
  [survey](https://kostochk.web.illinois.edu/docs/2008/book06.pdf).
* The preceding [`h=10,11,12` two-clique reduction](../albertson_r27_order53_h10_reduction/README.md)
  and [`h=9` closure](../albertson_r27_order53_h9_closure/README.md).

The new contribution is the parameterized two-clique terminal dichotomy and
its closure of every `h=11,12` profile.  Targeted searches of the current
Albertson and critical-graph literature and of the committed Discovery Net
found no prior version of this dichotomy or the `h>=13` consequence.  This is
a search-relative novelty assessment, not a historical-priority claim.
