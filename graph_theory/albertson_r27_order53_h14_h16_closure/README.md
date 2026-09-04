# Gallai-block persistence closes Albertson `r=27` through `h=16`

This note advances the sole surviving Albertson frontier row

```text
|V(G)|=53,  |E(G)|=713,  chi(G)=27.
```

Put

```text
L={v:d_G(v)=26},  Q=V(G)-L,  h=|Q|,  H=complement(G).
```

The preceding equality-boundary theorem proves `h>=14`.  Here the low-block
geometry is classified for `h=14,15,16`, and every resulting graph is shown
to be 26-colourable or to contain a subdivision of `K27`.  Consequently every
hypothetical counterexample in the final order/size row satisfies

```text
                         |Q| >= 17.                       (1)
```

At the new boundary `h=17`, the same argument eliminates every two-large-
block form, and exact edge accounting classifies the remaining three-block
families.  These families are recorded below as the next structural frontier.

The new structural point is an edge-budget persistence lemma.  Although low
vertices may now lie in two large Gallai clique blocks, three large blocks
cannot contain enough low--low edges to coexist with only 713 total edges.
Thus the two-clique normal form persists for three more support levels.  The
matching/conformal-triangle dichotomy used at `h<=13` then extends through
every two-clique form at `h<=17`, with a new direct argument for a common
incidence row of size one.  This is a conditional advance within Sadhu's
September 2026 frontier, not a proof of
Albertson's conjecture for chromatic number 27.

## Imported facts

We use the following established inputs.

1. Sadhu's frontier permits us to take a 27-critical graph on 53 vertices
   and 713 edges whose complement is connected.  A counterexample has no
   subdivision of `K27`.
2. Gallai's theorem says that every block of `G[L]` is a clique or an odd
   cycle.
3. Stehlik's theorem gives, for every vertex `v`, a 26-colouring of `G-v`
   whose colour classes all have order at least two.  At order 53 all classes
   are pairs, so `H` is factor-critical.
4. The rooted Kempe/Gallai lemma proved and independently reviewed earlier
   says that every low vertex belongs to a clique block of `G[L]` of order at
   least

   ```text
   s=27-h.                                                (2)
   ```
5. The committed equality-boundary closure excludes `h=13`, giving the
   starting condition `h>=14`.

A triangle of `H` whose deletion leaves a perfect matching is called
conformal.  No conformal triangle exists: it would be one independent triple
and 25 independent pairs in `G`, hence a 26-colouring.  Also

```text
d_H(q)<=25 for every q in Q,                              (3)
```

because vertices in `Q` have degree at least 27 in the 53-vertex graph `G`.

## Edge-budget persistence of two large blocks

Fix `14<=h<=16`, put `ell=53-h`, and call the clique blocks supplied by (2)
large.  A low vertex lies in at most two large blocks, since three would give
it at least

```text
3(s-1)>=30>26
```

low neighbours.  If two large blocks of orders `u,v` meet, their common cut
vertex gives

```text
(u-1)+(v-1)<=26,  hence u+v<=28.                          (4)
```

The direct-intersection graph of the large blocks is a forest.  If there
were four large blocks, their union would have order at least

```text
4s-3 > ell
```

for each `h=14,15,16`.  One large block cannot cover `L`, since its order is
at most 26.  Hence there are two or three.

Suppose there are three, and let `q in {0,1,2}` be the number of direct
intersections.  Their orders sum to `ell+q`.  Every other block contains at
most one vertex from each large block and hence has order at most three.
Gallai's theorem makes it a `K2` or `K3`.  The block-cut forest allows such
connector blocks to add at most 3, 1, or 0 edges as `q=0,1,2`, respectively.
Convexity of `binom(x,2)` then gives the following upper bounds on `e(G[L])`:

| `h` | `ell` | `s` | upper bounds for `q=0,1,2` | forced lower bound |
|---:|---:|---:|---:|---:|
| 14 | 39 | 13 | `237,248,261` | `301` |
| 15 | 38 | 12 | `226,238,252` | `275` |
| 16 | 37 | 11 | `218,231,246` | `249` |

For the last column, summing the fixed degree 26 over `L` gives

```text
e(L,Q)=26 ell-2e(G[L]).
```

Thus the number of graph edges incident with `L` is `26 ell-e(G[L])`, and
the total edge count 713 forces

```text
e(G[L]) >= 26 ell-713.                                   (5)
```

Every three-block upper bound contradicts (5).  Therefore exactly two large
blocks remain.  They cannot meet, because their orders would sum to
`ell+1>=38`, contradicting (4).  Call the two disjoint cliques `C=K_a` and
`D=K_b`, where `a+b=ell`.  Every additional low block can use only one
vertex of each clique, so there is at most one `C`--`D` bridge and no other
edge of `G[L]`.

## Exact two-clique profiles

Write

```text
d=a-(27-h),  e=b-(27-h),  so d+e=h-1.
```

A non-bridge row of `H[C,Q]` has size `d`, and a bridge endpoint row has size
`d+1`; the analogous row sizes on `D` are `e,e+1`.  Let `t` be the bridge
indicator and `r=e(H[Q])`.  Exact edge accounting gives the following table,
where `D0=t+r`.  Each row has both variants `(t,r)=(0,D0),(1,D0-1)`.

| `h` | `(a,b,d,e,D0)` |
|---:|---|
| 14 | `(14,25,1,12,1)`, `(15,24,2,11,11)`, `(16,23,3,10,19)`, `(17,22,4,9,25)`, `(18,21,5,8,29)`, `(19,20,6,7,31)` |
| 15 | `(13,25,1,13,2)`, `(14,24,2,12,13)`, `(15,23,3,11,22)`, `(16,22,4,10,29)`, `(17,21,5,9,34)`, `(18,20,6,8,37)`, `(19,19,7,7,38)` |
| 16 | `(12,25,1,14,3)`, `(13,24,2,13,15)`, `(14,23,3,12,25)`, `(15,22,4,11,33)`, `(16,21,5,10,39)`, `(17,20,6,9,43)`, `(18,19,7,8,45)` |

The arithmetically possible pair with `d=0` always has a `K26` side and
would require `D0=-11`, so every actual row has `d,e>=1`.

## Two matching facts

We use the following elementary consequence of Konig's theorem.

**Uniform-row lemma.**  In a bipartite graph with left part `X`, suppose
`|X|>p` and every left degree is at least `p`.  Either there is a matching of
size `p+1`, or all left rows are the same `p`-set.

Indeed, a vertex cover of size at most `p` cannot contain a left vertex: an
uncovered left row could not fit its `p` neighbours into the at most `p-1`
right vertices left in the cover.  Hence a minimum cover witnessing matching
number at most `p` lies on the right, and equality makes every row common.

We also use the following contraction consequence.  Let `uv` be an edge of
`H[Q]`, treated as a two-vertex high colour class.  A fixed-size `q` row is
compatible with at least `q-1` of the resulting high classes.  If the
contracted incidence graph has no `q`-matching, the uniform-row lemma makes
all contracted rows common.  If this happens for two distinct edges, all
original rows are equal: the symmetric difference of two original rows is
contained in both endpoint pairs, whose intersection has order at most one,
and an equal-size-row symmetric difference has even order.

## Terminal dichotomy for two low cliques

The argument in this and the next section applies to every two-clique normal
form for `14<=h<=17`.  For the `h=17` application, the edge calculation gives
eight rows with `1<=d<=e`, just as the displayed `h<=16` tables do.

### No low bridge

Suppose first that both incidence graphs have matchings of sizes `d+1` and
`e+1`.  Give the `h` high vertices distinct colours and extend colours along
the matchings.  Pair the `26-h` residual vertices on each low side across the
complement-complete `C,D` cut.  This is a 26-colouring.  Hence one side is
deficient; relabel it `C`, write its ordinary row size as `p` and the other
row size as `q`, and let all `C`-rows have the common support `S`, `|S|=p`.
Put `T=Q-S`.  The 27 vertices `C union T` induce a complete graph in `G`
apart from the target edges of `H[T]`.

### Zero or one target

Zero targets give a `K27`.  Suppose the unique target is `uv`.

If `p=1`, the opposite clique has order 25.  Each of `u,v` has a neighbour
in that clique in `G`: it has no complement neighbour in `C`, it has at least
the edge `uv` within `Q`, and (3) leaves at most 24 complement neighbours in
the opposite clique.  A common graph neighbour gives a two-edge `u,v` path;
otherwise their two chosen neighbours are distinct and the clique edge
between them gives a three-edge path.

Now let `p>=2`.  A support vertex adjacent in `G` to both ends gives the path
`u-s-v`.  Otherwise every support is adjacent in `H` to `u`, to `v`, or to
both.  Opposite one-end types give a path through the two supports; if their
mutual edge lies in `H`, (3) gives each at least `30-h` graph neighbours in
the opposite clique.  Since

```text
2(30-h)>26-p,
```

they have a common such neighbour to insert in the path.  In the remaining
patterns all supports meet one endpoint, say `u`, in `H`.  That endpoint has
at least two graph neighbours in the opposite clique.  If some support meets
only `u`, it has at least `29-h>=12` such neighbours, and two distinct clique
vertices give `u-d1-d2-s-v`.  If every support meets both endpoints, choose
distinct clique neighbours of `u,v`.  Thus the unique target always has a
route whose internal vertices lie outside the branch set, giving a `TK27`.

### Two targets force double uniformity

If `H[T]` has two distinct edges, contract each in turn.  A `q`-matching in
the opposite incidence graph gives a 26-colouring: use the contracted high
pair, attach `p` low vertices to the singleton classes in `S`, attach `q`
opposite lows along the matching, and pair the `27-h` residual lows on each
side.  If both contractions fail, the contraction fact makes all opposite
rows a common `q`-set `R`.

The sets `S,R` are disjoint, since a common high vertex would have all
`53-h>=37` low vertices as complement neighbours, contradicting (3).  As
`p+q=h-1`, there is a unique `z` with

```text
Q=S disjoint-union R disjoint-union {z}.                 (6)
```

Delete a vertex of `S` and take a perfect matching of the remaining
factor-critical complement.  If `s_M,r_M` count the `S,R` endpoints used in
high--high matching edges, balance of the two residual low sides gives
`r_M-s_M=1`.  The vertex `z` has no low complement neighbour.  If it were
matched to `S`, that edge contributes one more `S` than `R` endpoint, while
`S,R` matching edges contribute equally and internal edges contribute two
endpoints on their own side.  The balance would therefore force an edge
inside `R`.  That edge with a vertex of `D` would be a conformal triangle:
match `z` to its `S` neighbour, attach the other supports to their low sides,
and pair the equal residual low sets.  Hence `z` has a complement neighbour
in `R`.  The symmetric deletion of a vertex of `R` gives one in `S`.

Put `X=N_H(z) intersect S` and `Y=N_H(z) intersect R`.  Both are nonempty.
The absence of conformal triangles gives

```text
H[S]=H[R]=H[X,Y]=empty.                                  (7)
```

For example, an edge of `H[S]` forms a triangle with a vertex of `C`; match
`z` into `Y`, attach all remaining support vertices to their low sides, and
pair the equal residual low sets.  An `X,Y` edge forms the same forbidden
structure with `z`.  The other internal case is symmetric.

If `|X|<=|Y|`, inject `X` into `Y` and, using distinct `c_x in C`, route each
missing branch edge `zx` as

```text
z-c_x-y_x-x.
```

Equations (6)--(7) make these paths internally disjoint and turn
`D union S union {z}` into a `TK27`.  If `|Y|<=|X|`, use the symmetric
construction on `C union R union {z}`.  This closes every unbridged profile.

### One low bridge

Let the bridge be `c0d0`.  Each incidence graph has a matching one larger
than its ordinary row size.  Indeed, if the nonendpoint rows do not already
supply such a matching, the uniform-row lemma makes them common and the
endpoint's extra neighbour augments them.

The two matchings give the same 26-colouring unless both endpoints are
attached to the same high vertex.  If both endpoints remain residual, the
residual cross-pairing can avoid the single bridge.  Therefore failure of
all compatible choices forces disjoint sets `S,R` and a vertex `z` with

```text
N_H(c,Q)=S                 (c != c0),
N_H(c0,Q)=S union {z},
N_H(d,Q)=R                 (d != d0),
N_H(d0,Q)=R union {z},
Q=S disjoint-union R disjoint-union {z}.                 (8)
```

To see the rigidity, every one-larger matching must cover its endpoint, and
the possible endpoint partners on the two sides must form the same singleton
`{z}`.  Otherwise two choices are compatible.  The nonendpoint rows cannot
have a one-larger matching, so the uniform-row lemma makes them common; the
endpoint row has precisely their support plus its unique possible partner.

An edge of `H[S]`, `H[R]`, `H[z,S]`, or `H[z,R]` creates a conformal triangle
using a low nonendpoint or the appropriate bridge endpoint.  Consequently
all edges of `H[Q]` run between `S` and `R`.  The 27 vertices
`C union R union {z}` therefore induce a `K27` in `G` except for `c0z`.
For any `d1 != d0`, the path

```text
c0-d0-d1-z
```

completes a `TK27`.  Thus every bridged profile is also terminal, proving
(1).

## The exact `h=17` three-block frontier

At `h=17`, there are 36 low vertices and every low vertex lies in a clique
block of order at least 10.  Four large blocks would cover at least
`4*10-3=37` vertices, so there are again at most three.  The preceding
terminal dichotomy eliminates the two-block case.  In a three-block case the
edge budget requires

```text
e(G[L])>=26*36-713=223.                                  (9)
```

Let `q` be the number of direct intersections of the three large blocks.
When `q=0`, the convex upper bound, including a possible connector `K3`, is
only 213.  When `q=1`, (9) forces block orders `(10,10,17)`.  The intersecting
pair and the isolated block may additionally be joined by one connector
`K2`; according as it is absent or present,

```text
e(G[L])=226 or 227,        e(G[Q])=3 or 4.
```

When `q=2`, the direct-intersection graph is a path, there is no additional
low block, and the complete list is

| large-block orders | `e(G[L])` | `e(G[Q])` |
|---|---:|---:|
| `(10,10,18)` | 243 | 20 |
| `(10,11,17)` | 236 | 13 |
| `(10,12,16)` | 231 | 8 |
| `(10,13,15)` | 228 | 5 |
| `(10,14,14)` | 227 | 4 |
| `(11,11,16)` | 230 | 7 |
| `(11,12,15)` | 226 | 3 |
| `(11,13,14)` | 224 | 1 |
| `(12,12,14)` | 223 | 0 |

Here `e(G[Q])=e(G[L])-223` follows from the fixed low degree sum.  These are
necessary block/edge signatures, not existence claims; incidence constraints,
factor-criticality, complement connectivity, and criticality may eliminate
some or all of them.  In particular, any `h=17` counterexample must have one
of these three-large-block signatures.

## Reproduction and trust boundary

Run under CPython 3.9 or later; there are no third-party dependencies:

```sh
python3 verify.py
python3 independent_check.py
```

With CPython 3.11.2, the expected final digests are

```text
primary:     9a1e12fe2382d454f7d4ab1afeeaa7be3c3bd7df4204d0977fbc135750f06751
independent: b7a08354ee2af58c3dc078ed432f415039811fb403e0107a3aa601ab659adc79
```

SHA-256 of `verify.py`:
`cfec057ff3442f76019a1eeea4ae688ff5a5da6a17930b9ca1c95bad0b07b07b`.
SHA-256 of `independent_check.py`:
`66618d8516f5c8b010f164cb807ddaf4760b3753eaaa5b95d6a8f92fc60f4a3c`.

The primary checker enumerates all admissible three-large-block forests,
checks the connector bounds and low-edge contradiction, reconstructs every
exact two-clique profile and bridge variant, verifies the contraction parity
lemma, exhausts the one-target support-type split by type counts, and checks
all colouring, balance, conformal, and subdivision vertex identities.  It
also classifies the eleven exact `h=17` three-block signatures.  The
independent checker reconstructs the block bounds, profile rows, and new
frontier from closed formulas and separately audits the terminal counts.

Both scripts use exact CPython integer/set arithmetic without a solver,
randomness, floating point, generated input, external data, or project
imports.  The prose proof supplies the bridge from Gallai, Stehlik, and
arbitrary incidence matrices to the finite arithmetic.

The mathematical trust boundary is Sadhu's September 2026 connected-
complement frontier, Gallai's low-vertex block theorem, Stehlik's colouring
theorem, Konig's theorem, the independently reviewed rooted Gallai lemma,
and the preceding `h=13` closure.  This note proves the new edge-budget
persistence, the `h=14,15,16` terminal deductions, and the necessary
three-block classification at `h=17`.

## Sources and novelty scope

* A. Sadhu, [*Albertson's Conjecture Holds for `r` at Most
  26*](https://arxiv.org/abs/2609.01682v1), for the order-53 connected-
  complement frontier and exclusion of a topological `K27`.
* M. Stehlik, [*Critical graphs with connected
  complements*](https://doi.org/10.1016/S0095-8956(03)00069-8), JCTB 89
  (2003), 189--194.
* Gallai's low-vertex theorem, stated as Theorem 8 in A. Kostochka's
  [survey](https://kostochk.web.illinois.edu/docs/2008/book06.pdf).
* The preceding [`h=13` closure](../albertson_r27_order53_h13_closure/README.md)
  and the independently reviewed [rooted Gallai
  reduction](../albertson_r27_gallai_blocks_independent_review/README.md).

Targeted searches of the current Albertson and sparse-critical literature
and of the committed Discovery Net found no prior three-level edge-budget
persistence lemma, `h>=17` consequence, or `h=17` three-block classification.
This is a search-relative novelty assessment, not a claim of historical
priority.
