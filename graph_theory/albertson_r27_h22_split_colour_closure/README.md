# Block/list and topological closure of the Albertson `r=27`, `h=22` boundary

This note advances the sole surviving Albertson frontier row

```text
|V(G)|=53,  |E(G)|=713,  chi(G)=27.
```

Put

```text
L={v:d_G(v)=26},  Q=V(G)-L,  h=|Q|,  H=complement(G).
```

We prove that no graph in the frontier with `h=22` exists.  Combined with
the preceding committed `h>=22` lemma, this gives the conditional campaign
advance

```text
                         h >= 23.                         (1)
```

The new result closes only the equality boundary `h=22`.  It does not
exclude `h>=23`, improve the crossing estimate by itself, or prove
Albertson's conjecture for chromatic number 27.  The preceding `h>=22`
lemma was committed and source-reproduced when this note was written but
had not yet received an independent graph review; the equality exclusion
proved here remains meaningful even if that imported lower bound is audited
separately.

## Imported facts and exact parameters

We use the following established inputs.

1. Sadhu's September 2026 frontier and the subsequent committed reductions
   leave only a 27-critical graph on 53 vertices and 713 edges, with
   connected complement and no subdivision of `K27`.
2. Gallai's theorem says every block of `G[L]` is a clique or an odd cycle.
3. The reviewed rooted Gallai/Stehlik lemma puts every low vertex in a clique
   block of order at least `27-h`.
4. Stehlik's theorem makes `H` factor-critical.  Hence `H` has no conformal
   triangle: such a triangle together with a perfect matching after its
   deletion would be one independent triple and 25 independent pairs in
   `G`, giving a 26-colouring.
5. Every high vertex has complement degree at most 25, because it has graph
   degree at least 27.
6. The reviewed active-class recolouring lemma says: if every optimal
   colouring of a graph has exactly `f` incidence-weight classes of weight
   `b` and all remaining classes have weight zero, then a vertex of weight
   `b` has degree at least `f-1`.

Set `h=22`.  Then

```text
|L|=31,  s=27-h=5.                                      (2)
```

Writing `e_L=e(G[L])` and `e_Q=e(G[Q])`, the degree sum over `L` gives

```text
e(L,Q)=26*31-2e_L,
e_Q=e_L-93,
e_L>=93.                                                 (3)
```

Call every clique block of order at least five *large*.  By input 3 these
blocks cover `L`.  There are at least two: one would have to cover
all 31 low vertices, whereas a clique block has order at most 26 because a
`K27` is forbidden.  There are at most seven, because eight order-five
blocks in a block forest cover at least `8*5-7=33` vertices.

## Complete block-count census

Suppose there are `b` large blocks in `c` direct components and put

```text
q=b-c.
```

Repeated cut vertices give

```text
sum_i |B_i|=31+q.                                       (4)
```

A block outside the large family meets each direct component at most once.
These connector blocks form a hyperforest.  If their orders are `t_j`, then
`sum_j(t_j-1)<=c-1`; whether a connector is a clique or an odd cycle, its
edge contribution is at most `binom(t_j,2)`.  Convexity therefore bounds the
total connector contribution by

```text
binom(c,2).                                              (5)
```

This is intentionally an over-approximation: the certificate enumerates
every integer connector contribution from zero through (5), including
values and geometries that need not be realizable.  Closing this larger set
is sufficient.

Every connector clique has order below five, or it would itself be a large
block; connector odd cycles are 3-colourable.  Thus

```text
chi(G[L])=max_i |B_i|.                                  (6)
```

The convex edge caps for seven large blocks are `73,76,81` for
`q=4,5,6`, all below (3).  For six and five blocks the exact over-counted
census is:

| large blocks | admissible edge-budget rows | largest `max |B_i|+chi(G[Q])` |
|---:|---:|---:|
| 6 | 10 | 16 |
| 5 | 247 | 25 |

Here `chi(G[Q])<=c_Q` is obtained from
`binom(c_Q,2)<=e_Q<binom(c_Q+1,2)`.  By (6), disjoint palettes colour every
six- and five-block row with at most 26 colours.

For four blocks there are respectively

```text
189,136,78,47
```

edge-budget rows for `q=0,1,2,3`.  Only `7,8,8,8` of them exceed the
disjoint-palette bound, for 31 exceptions in total.  Every exception has a
unique largest large block.  If that block is not an isolated component of
`G[L]`, the component containing it also has a smaller large block at an end
of its block-cut tree.  A connector block cannot be an end block because
every low vertex lies in a large block.

Fix an optimal `c`-colouring of `G[Q]` from a 26-colour palette and give a
low vertex the colours absent from its high neighbourhood.  Every low
vertex `v` has a list of size at least

```text
26-d_Q(v)=d_L(v).                                       (7)
```

All `26-c` colours unused on `Q` lie in every low list.  In all 31
four-block exceptions, for every smaller large block `K_t`,

```text
26-c_Q > t-1.                                           (8)
```

A noncut vertex of a smaller end block therefore has a list strictly larger
than its low degree.  Order a spanning tree toward that strict vertex and
greedily colour it last: all other vertices see an uncoloured parent and the
root has a strict list.  This colours its entire component.  The same
argument colours every other low component.  Hence the unique largest block
must be isolated.  Allowing every numeric connector overcount leaves 12
four-block rows.

For three blocks there are `120,66,37` edge-budget rows for `q=0,1,2`, of
which `64,44,30` exceed the palette bound.  The only tied-largest row is

```text
(5,14,14), q=2, e_Q=99, c_Q=14.                         (9)
```

The only unique-largest rows in which (8) fails for some smaller block are

```text
(5,13,15), q=2, e_Q=100, c_Q=14,
(6,13,14), q=2, e_Q= 91, c_Q=14.                        (10)
```

All three blocks are directly connected in (9)--(10), and a noncut vertex
of the `K5` or `K6` has degree at most five while twelve colours are unused
on `Q`.  The same strict-root greedy argument closes these rows.  All other
non-isolated unique-largest rows satisfy (8).  The only remaining numeric
overcount consists of 54 rows in which the unique largest block is isolated.

## Split-Hall closure of the 66 isolated-block rows

Let `B=K_b` be the isolated largest block in one of the 12+54 residual rows,
and put `X=G[Q]`.  The other low components are list-colourable by the strict
argument above.  If `B` were also list-colourable, `G` would be
26-colourable.  Each list on `B` has size at least `b-1`.  Hall can fail for
`b` such lists only when they are all the same `(b-1)`-set.  It follows that,
in every optimal colouring of `X`, every vertex of `B` sees exactly once
each of a common set of

```text
f=27-b                                                   (11)
```

active colours and sees no other colour on `Q`.

Define the colouring-independent column weight

```text
w(x)=|N_G(x) intersect B|, x in Q.
```

Every active colour class has total weight `b`, every other class has weight
zero, and

```text
sum_{x in Q} w(x)=bf.                                   (12)
```

If `0<w(x)<b`, move `x` alone from its active colour to a fresh colour.  Its
old class remains nonempty because it had total weight `b`.  On `B`, this
creates two list types of order `b-1`, obtained by exchanging the old and
fresh colours; both types occur and their union has order `b`.  Every proper
subset of the `b` clique vertices sees at least `b-1` colours, while the full
set sees `b`.  Hall now colours `B`.

After this split the other low components still satisfy (7).  In all but
one residual row, the colours unused on the split colouring already supply
a disjoint palette at least as large as the largest smaller block.  The sole
exception is

```text
(5,13,14), q=1, e_Q=86, c_Q=13.                         (13)
```

Here the `K5` and `K13` meet, and after the split twelve colours remain
unused; a noncut vertex of the `K5` again supplies the strict root.  Thus an
intermediate-weight column always yields a 26-colouring, and consequently

```text
w(x) in {0,b} for every x in Q.                         (14)
```

Equations (12)--(14) force exactly `f` full columns and `22-f` zero columns.
The active-class recolouring lemma gives degree at least `f-1` in `X` at a
full column.  A zero column has no graph neighbour in `B`; since its vertex
is high and there are only `31-b` other low vertices,

```text
w(x)=0 implies d_X(x)>=27-(31-b)=b-4.                  (15)
```

The exact endpoint certificates, grouped by isolated block order, are:

| `b` | rows | degree-sum floor | maximum `2e_Q` | minimum margin |
|---:|---:|---:|---:|---:|
| 14 | 2 | 246 | 172 | 74 |
| 15 | 12 | 242 | 176 | 66 |
| 16 | 18 | 242 | 184 | 58 |
| 17 | 12 | 246 | 196 | 50 |
| 18 | 8 | 254 | 212 | 42 |
| 19 | 6 | 266 | 232 | 34 |
| 20 | 4 | 282 | 256 | 26 |
| 21 | 3 | 302 | 284 | 18 |
| 22 | 1 | 326 | 316 | 10 |

The floor in each row is

```text
f(f-1)+(22-f)(b-4).
```

It is strictly larger than the handshake identity `sum_x d_X(x)=2e_Q` in
every one of the 66 rows.  This closes every case with at least three large
blocks.

## Exact two-clique profiles

It remains to consider two large blocks.  They cannot meet: their orders
would sum to 32 by (4), giving their common cut vertex 30 low neighbours.
Thus they are disjoint cliques `C=K_a,D=K_b`, with `a+b=31`, and every
additional low block is either absent or the single bridge `c0d0`.

Write

```text
a=5+p, b=5+q, p+q=21.                                  (16)
```

An ordinary row in the complement incidence graphs `H[C,Q]` and `H[D,Q]`
has size `p` and `q`; a bridge endpoint has one additional complement
neighbour.  If `t` is the bridge indicator, exact edge accounting gives the
following ten profiles, where `D0=t+e(H[Q])`:

```text
(a,b,p,q,D0) =
(6,25,1,20,9), (7,24,2,19,27), (8,23,3,18,43),
(9,22,4,17,57), (10,21,5,16,69), (11,20,6,15,79),
(12,19,7,14,87), (13,18,8,13,93),
(14,17,9,12,97), (15,16,10,11,99).                    (17)
```

Each admits the variants `(t,e(H[Q]))=(0,D0),(1,D0-1)`.

We use the elementary uniform-row consequence of Koenig's theorem: if more
than `r` left vertices of a bipartite graph have degree at least `r`, then
either there is an `(r+1)`-matching or all left rows are the same `r`-set.
A vertex cover of size at most `r` cannot contain a left vertex, so a
deficient cover lies wholly on the right and forces the claimed equality.

### No low bridge: simultaneous matchings and one target

If the two incidence graphs have matchings of orders `p+1` and `q+1`, give
the 22 high vertices singleton colours and attach low vertices along the
matchings.  A high class used by both sides remains independent because the
`C,D` cut lies in `H`.  Four vertices remain on each low side, since

```text
a-(p+1)=b-(q+1)=4.
```

Pair them across the complement-complete cut.  The result has `22+4=26`
colour classes.

Otherwise relabel a deficient side `C`.  The uniform-row lemma makes all
its rows one common `p`-set `S`.  With `T=Q-S`, the 27 vertices `C union T`
induce a clique in `G` apart from the target edges of `H[T]`.  No target
gives a `K27`.

Suppose first that the unique target is `uv`.  If `p=1`, then `D=K25`; each
endpoint has a graph neighbour in `D` under the complement-degree cap.
One common neighbour, or two distinct neighbours joined inside `D`, routes
the missing edge.

Let `p>=2`.  A support vertex adjacent in `G` to both endpoints gives the
two-edge path immediately.  Otherwise every support meets `u`, `v`, or both
in `H`.

* Opposite one-end support types give a path through the two supports.  If
  their mutual edge lies in `H`, the degree cap gives each at least eight
  graph neighbours in `D`; either the pattern is numerically impossible
  because `|D|<8`, or two distinct clique vertices complete the path.
* If all supports meet one endpoint, say `u`, and some support misses `v` in
  `H`, then `u` has at least two and that support at least seven graph
  neighbours in `D`.  Two distinct choices give
  `u-d1-d2-s-v`.
* If every support meets both endpoints in `H`, both endpoints have at least
  two graph neighbours in `D`; distinct choices joined inside `D` give the
  path.

The finite checker exhausts all four support types.  The exact graph-neighbour
floors in the last two bullets and the mutual-edge case are `2,7,8`.  Hence
the unique target always has an internally external path and produces a
`TK27`.

### No low bridge: two targets

If `H[T]` has two distinct edges, contract either target into one high colour
class.  Every original `q`-row is compatible with at least `q-1` of the 21
resulting high classes.  A `q`-matching in the contracted opposite incidence
graph gives a 26-colouring: use the 21 high classes, attach `p` low vertices
to `S`, attach `q` opposite low vertices along the matching, and pair the
five residual vertices on each low side.

If both contractions are deficient, their uniform contracted rows imply
that the symmetric difference of any two original rows lies in both target
pairs.  Distinct pairs intersect in at most one vertex, whereas an
equal-size-row symmetric difference has even order.  Thus all opposite rows
are one common `q`-set `R`.

The supports are disjoint: a vertex in `S intersect R` would have all 31 low
vertices as complement neighbours, contradicting the cap 25.  Equation
(16) therefore gives a unique vertex `z` with

```text
Q=S disjoint-union R disjoint-union {z}.                (18)
```

The vertex `z` has no low complement neighbour.  Factor-critical matching
balance after deleting a vertex of `S` forces a complement neighbour of `z`
in `R`; otherwise `z` must match into `S` and the balance forces an edge
inside `R`, which together with a vertex of `D` is a conformal triangle.  If
`p=1`, deleting the sole vertex of `S` makes the conclusion immediate.  The
symmetric argument gives a neighbour in `S`.

Put

```text
X=N_H(z) intersect S, Y=N_H(z) intersect R.
```

Both sets are nonempty.  Explicit perfect matchings after deleting the
candidate triangles, with six residual vertices on each low side, show

```text
H[S]=H[R]=H[X,Y]=empty.                                 (19)
```

For example, an edge `s1s2` of `H[S]` forms a triangle with any vertex of
`C`.  After deleting it, match `z` to a fixed vertex of `Y`, attach the
remaining vertices of `S` and `R` to their low sides, and cross-pair the six
unused vertices of `C` and `D`.  An edge of `H[X,Y]` forms a triangle with
`z`; attaching `S-{x}` and `R-{y}` leaves the same six cross-pairs.  The
`H[R]` case is symmetric.

If `|X|<=|Y|`, inject `X` into `Y`, choose distinct `c_x in C`, and replace
each missing branch edge `zx` in the branch set `D union S union {z}` by

```text
z-c_x-y_x-x.
```

Equations (18)--(19) make these paths internally disjoint and all their
edges graph edges.  The branch set has `b+p+1=27` vertices.  If
`|Y|<=|X|`, use the symmetric construction on `C union R union {z}`.  This
gives a `TK27` in every double-uniform case.

### One low bridge

Let the bridge be `c0d0`.  The nonendpoint rows on either side either have a
one-larger matching or are uniform; in the latter case the endpoint's extra
neighbour augments the common support.  Thus both incidence graphs have
one-larger matchings.  Compatible choices give the 26-colouring above, and
the four residual cross-pairs can avoid the one forbidden pair `c0d0`.

If all choices are incompatible, every matching covers its endpoint and the
two possible endpoint-partner sets must be the same singleton `{z}`.
Applying the uniform-row lemma to the nonendpoint rows gives disjoint common
supports `S,R` and

```text
N_H(c,Q)=S                 (c != c0),
N_H(c0,Q)=S union {z},
N_H(d,Q)=R                 (d != d0),
N_H(d0,Q)=R union {z},
Q=S disjoint-union R disjoint-union {z}.                (20)
```

An edge `s1s2` of `H[S]` makes a triangle with a nonendpoint of `C`: match
`z` to `c0`, attach `S-{s1,s2}` and all of `R` to their low sides, and
cross-pair the five unused vertices on each side.  An edge `zs` with
`s in S` makes a triangle with `c0`; attaching `S-{s}` and `R` again leaves
five cross-pairs.  The forbidden bridge pair is absent because `c0` is
already used or deleted.  The two symmetric constructions exclude `H[R]`
and `H[z,R]`.  Hence all edges of `H[Q]` run between `S` and `R`.

The 27 vertices `C union R union {z}` now induce a clique in `G` except for
`c0z`.  Choose `d1 != d0`; then

```text
c0-d0-d1-z
```

is a graph path whose internal vertices lie outside the branch set.  This
is a `TK27`.  Every two-block form is therefore 26-colourable or contains a
subdivision of `K27`, completing the `h=22` equality exclusion.

## Reproduction and trust boundary

Run under CPython 3.9 or later; there are no third-party dependencies:

```sh
python3 verify.py
python3 independent_check.py
```

The primary checker recursively enumerates the block-order signatures and
connector overcount, all palette exceptions, the exact isolation filter,
every split-Hall subset size, all 66 endpoint rows, all support-type counts,
the ten two-clique profiles, and 53,130 ordered target-contraction pairs.

The independently organized checker uses combinations with replacement,
constructs the actual two list types and finds a maximum matching for every
split, enumerates all 3,584,825 labelled zero/full endpoint vectors, rebuilds
the two-clique table from the complement-edge formula, and checks 26,565
unordered target pairs.  It does not import the primary checker.

Both programs use exact CPython integer, set, tuple, matching, and SHA-256
operations.  They use no solver, randomness, floating point, generated
input, external data, or project import.  They certify the finite census and
arithmetic; the passage from the imported graph theorems through block-cut
geometry, list colouring, factor-critical matchings, and internally disjoint
paths is the deductive proof above.

The mathematical trust boundary is Sadhu's connected-complement frontier,
the committed reduction to the 713-edge row, Gallai's low-vertex theorem,
Stehlik's factor-critical theorem, the reviewed rooted large-block lemma,
the reviewed active-class recolouring lemma, and the preceding committed
`h>=22` equality closure.  No critical graphs are enumerated.

Expected certificate digests are

```text
primary:     955a618a706aecd280080a15149dc0e738412e9ec9964adf01354d720d093b2c
independent: 199ce4fa3f393cece0fddcc0c240fc66966381e25e5941e7895fc0a34edbde80
```

SHA-256 of the executable sources:

```text
verify.py            8ec81ed55e3458d392ee6cfd2638fa7a3efc2783c1780f8d8ebe723d7a4b7c6d
independent_check.py 7fd24bb7129b92e5615a2452c0e42ab80be9f1db05f669b9ee5aaccbfff501e5
```

## Sources and novelty scope

* A. Sadhu, [*Albertson's Conjecture Holds for `r` at Most
  26*](https://arxiv.org/abs/2609.01682v1), for the order-53/54
  connected-complement frontier and the topological-clique reduction.
* M. Stehlik, [*Critical graphs with connected
  complements*](https://doi.org/10.1016/S0095-8956(03)00069-8), JCTB 89
  (2003), 189--194.
* Gallai's low-vertex theorem, stated as Theorem 8 in A. Kostochka's
  [survey](https://kostochk.web.illinois.edu/docs/2008/book06.pdf).
* The preceding [`h=21` equality
  closure](../albertson_r27_h21_split_colour_closure/README.md) and reviewed
  [`h>=21` split-colour
  closure](../albertson_r27_h20_split_colour_closure/README.md).

The arXiv and committed-graph searches were refreshed on 2026-09-04.
Sadhu's paper remained the latest directly relevant preprint, and Discovery
Net through indexed height 1948 contained no `h=22` classification or
`h>=23` consequence.  The split-Hall and two-clique kernels were already
present in the campaign; the potentially new content is the exhaustive
`h=22` block/list reduction, its 66 endpoint certificates, and the checked
extension of every topological construction to the new floors `2,7,8`.
This is a search-relative novelty statement, not a claim of historical
priority.
