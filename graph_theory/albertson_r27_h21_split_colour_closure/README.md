# Block/list and split-colour closure forces `h>=22` at Albertson `r=27`

This note advances the sole surviving Albertson frontier row

```text
|V(G)|=53,  |E(G)|=713,  chi(G)=27.
```

Put

```text
L={v:d_G(v)=26},  Q=V(G)-L,  h=|Q|.
```

The independently reviewed split-colour closure proves `h>=21`.  We prove
that equality is also impossible.  Consequently every hypothetical
counterexample in the surviving row has

```text
h>=22.                                                     (1)
```

This closes only the `h=21` equality boundary.  It does not exclude `h>=22`,
improve the universal crossing lower bound by itself, or prove Albertson's
conjecture for chromatic number 27.

## Imported facts

We use the following established inputs.

1. Sadhu's September 2026 frontier and the subsequent committed closures
   leave only a 27-critical graph on 53 vertices and 713 edges whose
   complement is connected and which contains no subdivision of `K27`.
2. Gallai's theorem says every block of `G[L]` is a clique or an odd cycle.
3. The reviewed rooted Gallai/Stehlik lemma puts every low vertex in a clique
   block of order at least `27-h`.
4. Stehlik's theorem makes the complement factor-critical.  A conformal
   triangle in the complement is therefore impossible: it and a perfect
   matching of the remaining 50 vertices would give a 26-colouring.
5. Every high vertex has complement degree at most 25, because its graph
   degree is at least 27.
6. The reviewed active-class recolouring lemma says the following.  If an
   incidence weight on a `c`-chromatic graph has, in every optimal colouring,
   exactly `f` colour classes of weight `b` and all other classes of weight
   zero, then a vertex of weight `b` has degree at least `f-1`.

Set `h=21`.  Then `|L|=32`, every low vertex belongs to a clique block of
order at least

```text
s=27-h=6,                                                (2)
```

and the fixed low degree sum gives

```text
e(L,Q)=26*32-2e(G[L]),
e(G[Q])=e(G[L])-119,
e(G[L])>=119.                                            (3)
```

Call the clique blocks supplied by (2) *large*.
A single large block would have to cover all 32 low vertices and would
contain `K27`, so there are at least two.

## Block-count and degree-list reduction

Restrict the block-cut forest to the large blocks and their shared cut
vertices.  If there are `b` large blocks in `c` direct components, put
`q=b-c`.  Since the large blocks cover `L`,

```text
sum_i |B_i|=32+q.                                        (4)
```

A block outside the large family meets each direct component at most once.
These connector blocks form a hyperforest.  If their orders are `t_j`, then
`sum_j(t_j-1)<=c-1`; whether they are cliques or odd cycles, their total edge
contribution is at most `binom(c,2)`.  This supplies a safe over-approximation
for every connector geometry.

Every connector clique has order at most the number of direct components,
and every connector odd cycle is 3-colourable.  Since a Gallai forest has
chromatic number equal to the maximum chromatic number of one of its blocks,
`chi(G[L])` is the largest large-block order in all counts below.

Seven large blocks would cover at least `7*6-6=36` vertices.  Six blocks have
convex edge caps 91 and 96 for `q=4,5`, both below (3).  For five blocks the
caps for `q=0,...,4` are

```text
98, 102, 108, 116, 126.
```

Only two rows reach (3): orders `(6,6,6,6,12)` and `(6,6,6,7,11)`, with
`e(G[Q])=7,2`.  Since a `c`-chromatic graph has at least `binom(c,2)` edges,
their respective bounds `chi(G[L])+chi(G[Q])<=16,13` give a 26-colouring.

For four blocks, the connector over-approximation contains respectively

```text
73, 72, 46, 27
```

edge-budget rows for `q=0,1,2,3`.  Their largest disjoint-palette bounds are
`21,23,26,28`.  The unique row above 26 is

```text
(|B_i|)=(6,6,6,17), q=3, e(G[Q])=62, chi(G[Q])<=11.     (5)
```

The large-block family in (5) is connected.  A smaller end block has a
noncut vertex of low degree 5, while all `26-11=15` colours unused on `Q`
belong to its available list.  Root a spanning tree there and greedily colour
toward the root; the strict list at the root colours last.  Thus (5) is also
26-colourable.

For clarity, the list argument just used has no hidden list theorem.  Fix a
`c`-colouring of `G[Q]` from a 26-colour palette and give each low vertex the
colours absent from its high neighbourhood.  A low vertex `v` has a list of
size at least

```text
26-d_Q(v)=d_L(v),                                       (6)
```

and every colour unused on `Q` lies in every list.  In a connected component,
one vertex with a list strictly larger than its low degree suffices for the
spanning-tree greedy order described above.

## Three blocks leave 31 isolated-clique rows

The three-block connector over-approximation has 96, 54, and 30 edge-budget
rows for `q=0,1,2`; respectively 36, 26, and 21 exceed the disjoint-palette
bound 26.  All but one of these exceptions has a unique largest block.  For
every smaller block `K_t`, with `c_Q` the edge bound on `chi(G[Q])`, exact
enumeration gives

```text
26-c_Q > t-1.                                           (7)
```

If the component of the largest block contains another large block, its
block-cut tree has a smaller end block: a connector block cannot be an end
block because every one of its vertices already lies in a large block.
Thus (6)--(7) colour that component.  All other components are coloured the
same way.  The sole tied exception is
`(6,14,14),q=2,e(G[Q])=78,c_Q=13`.  A common cut in all three blocks would
have 31 low neighbours, so the only potentially troublesome geometry has the
`K6` in the middle of a path.  It still has a noncut degree-5 vertex with all
13 unused colours in its list, and is colourable by (6).

It follows that the unique largest block `B=K_b` must be an isolated
component of `G[L]`.  This is possible only when the three large blocks are
disjoint with zero or one connector edge (the possible edge joins the two
smaller blocks), or when the two smaller blocks meet and there is no
connector.  Exactly 31 rows remain:

| relation | large-block orders | `e(G[Q])` |
|---|---|---|
| disjoint / zero or one small-block bridge | `(6,6,20)` | `101 / 102` |
| same | `(6,7,19)` | `88 / 89` |
| same | `(6,8,18)` | `77 / 78` |
| same | `(6,9,17)` | `68 / 69` |
| same | `(6,10,16)` | `61 / 62` |
| same | `(7,7,18)` | `76 / 77` |
| same | `(7,8,17)` | `66 / 67` |
| same | `(7,9,16)` | `58 / 59` |
| same | `(8,8,16)` | `57 / 58` |
| two smaller blocks meet | `(6,6,21)` | `121` |
| same | `(6,7,20)` | `107` |
| same | `(6,8,19)` | `95` |
| same | `(6,9,18)` | `85` |
| same | `(6,10,17)` | `77` |
| same | `(6,11,16)` | `71` |
| same | `(6,12,15)` | `67` |
| same | `(7,7,19)` | `94` |
| same | `(7,8,18)` | `83` |
| same | `(7,9,17)` | `74` |
| same | `(7,10,16)` | `67` |
| same | `(8,8,17)` | `73` |
| same | `(8,9,16)` | `65` |

The first nine lines each represent two rows and the last thirteen one each,
for `18+13=31` rows.

## Split-colour Hall closure of every isolated clique

Fix an optimal `c`-colouring of `X=G[Q]`.  The low components other than
`B` are list-colourable by (6)--(7).  If `B` were also list-colourable, this
would give a 26-colouring of `G`.  Each list on the clique `B` has size at
least `b-1`.  Hall can fail for `b` such lists only when all lists are one
common `(b-1)`-set.  Consequently every vertex of `B` sees the same

```text
f=27-b                                                     (8)
```

active colours, exactly once each, and no other colour on `Q`.  Define

```text
w(x)=|N_G(x) intersect B|.
```

Every active colour class has total weight `b`, every other class has weight
zero, and

```text
sum_{x in Q} w(x)=bf.                                    (9)
```

Suppose `0<w(x)<b`.  Its active class has total weight `b`, so it is not a
singleton.  Move `x` alone to a fresh colour.  On `B` this creates two list
types, both of order `b-1`, differing by exchanging the old and fresh
colours.  Both occur and their union has order `b`.  A proper subset of the
`b` clique vertices has at most `b-1` members and sees a union of at least
`b-1`; all of `B` sees the `b`-element union.  Hall therefore colours `B`.

In all 31 rows, even at the upper edge bound `c_Q`, the number
`26-(c_Q+1)` of colours absent from the split colouring is at least the order
of the largest smaller block.  These colours properly colour `L-B`; colours
used on `B` may be reused there because `B` is isolated.  This again gives a
26-colouring, so

```text
w(x) in {0,b} for every x in Q.                          (10)
```

Equations (9)--(10) force exactly `f` full columns and `21-f` zero columns.
The active-class recolouring lemma gives `d_X(x)>=f-1` at full weight.  At
zero weight, `x` has no neighbour in `B`; since `x` is high and there are
only `32-b` other low vertices,

```text
d_X(x)>=27-(32-b)=b-5.                                  (11)
```

The terminal degree certificates, grouped by isolated block order, are:

| `b` | `f` | degree-sum floor | maximum `2e(X)` | margin |
|---:|---:|---:|---:|---:|
| 15 | 12 | 222 | 134 | 88 |
| 16 | 11 | 220 | 142 | 78 |
| 17 | 10 | 222 | 154 | 68 |
| 18 | 9 | 228 | 170 | 58 |
| 19 | 8 | 238 | 190 | 48 |
| 20 | 7 | 252 | 214 | 38 |
| 21 | 6 | 270 | 242 | 28 |

Here the floor is

```text
f(f-1)+(21-f)(b-5).
```

Every row contradicts the handshake identity on `X`.

## The two-block regime remains terminal

Two large blocks cannot meet: their orders would sum to 33, whereas a common
cut vertex of degree 26 requires their sum to be at most 28.  Thus they are
disjoint cliques `C=K_a,D=K_b`, with `a+b=32`, joined by at most one bridge.
Write

```text
a=6+p,  b=6+q,  p+q=20.
```

Exact edge accounting leaves ten profiles:

```text
(a,b,p,q,D0) =
(7,25,1,19,8), (8,24,2,18,25), (9,23,3,17,40),
(10,22,4,16,53), (11,21,5,15,64), (12,20,6,14,73),
(13,19,7,13,80), (14,18,8,12,85), (15,17,9,11,88),
(16,16,10,10,89),
```

where `D0` is the bridge indicator plus `e(complement(G)[Q])`.  The
parametric matching/conformal-triangle proof used through `h=20` retains
slack at this boundary.  We include its alternatives and the new numerical
checks.

Without a bridge, simultaneous `(p+1)`- and `(q+1)`-matchings in the two
low--high complement incidence graphs attach low vertices to the 21 high
singleton colours.  Five residual vertices on each low side pair across the
complement-complete cut, giving 26 colours.  Otherwise the uniform-row
consequence of Konig's theorem makes all rows on one side a common `p`-set
`S`.  Then `C union (Q-S)` is a 27-vertex clique apart from the target edges
inside `complement(G)[Q-S]`.

No target gives `K27`.  One target `uv` has a path outside the branch set.  If
`p=1`, each endpoint has a graph neighbour in the opposite `K25`; use one
common neighbour or two distinct ones joined in that clique.  For `p>=2`, a
support adjacent in `G` to both endpoints gives a two-edge path.  Opposite
one-end support types give a path through the supports; if their mutual edge
is missing, insert two distinct vertices of the opposite clique.  The degree
cap gives such supports at least nine graph neighbours there.  If all
supports miss the same endpoint, that endpoint has at least two graph
neighbours in the opposite clique and a one-end support has at least eight;
two distinct choices give a path through a clique edge (and if a displayed
floor exceeds the clique order, that support pattern is impossible).  If
every support misses both endpoints, choose distinct opposite-clique
neighbours of the two endpoints.  Thus the one-target route remains valid at
the exact new floors `2,8,9`.

With two distinct targets, contract either one as a high colour class.  A
`q`-matching on the opposite side gives 20 high colour classes and six
residual cross-pairs, hence a 26-colouring.  Failure after both contractions
makes all opposite rows one common `q`-set `R`: the symmetric difference of
two equal-size original rows lies in both distinct endpoint pairs and has
even order.  The degree cap gives

```text
Q=S disjoint-union R disjoint-union {z}.
```

Factor-critical balance and exclusion of a conformal triangle imply that
`z` has complement neighbours in both supports, while the complement has no
edge inside `S`, inside `R`, or between the two `z`-neighbour sets.  Inject
the smaller neighbour set into the larger and route the missing branch edges
through distinct vertices of the opposite low clique, exactly as in the
preceding parametric proof.  There are seven residual low vertices in the
conformal-triangle matchings, so no endpoint case is lost.

With one low bridge, the endpoint's extra complement neighbour augments any
uniform nonendpoint rows.  Compatible one-larger matchings again give a
26-colouring; five residual cross-pairs can avoid the bridge.  Incompatible
choices force disjoint supports `S,R`, a unique `z`, and endpoint rows
`S+z,R+z`.  Conformal-triangle exclusion leaves only `S`--`R` complement
edges on `Q`, and the sole missing branch edge routes through the low bridge
and one further opposite-clique vertex.  Thus every two-block form is
26-colourable or contains a `TK27`.

All possible large-block counts are now closed, proving (1).

## Reproduction and trust boundary

Run under CPython 3.9 or later; there are no third-party dependencies:

```sh
python3 verify.py
python3 independent_check.py
```

Expected certificate digests:

```text
primary:     4b62aac4e48f69a547423ff7a4a6a373429cec3784a4e01b39385f1deb8e0fab
independent: f95916fc5a2a893822a64f33d52ce6498eda02a70d2cc2731e0b09ec0a5a598d
```

SHA-256 of the executable sources:

```text
verify.py            4fe04bf4db28fa6a2d3b77c4baec8b6f5fe5d6b26a9a1d966cbb5b507eceb6dd
independent_check.py 91dddef49537396df4b1d9ecdd75cf3b2036c55a5a4d107c21994eb50e4b8196
```

The primary checker recursively enumerates the block-order signatures,
connector-edge over-approximation, all list exceptions, every split weight,
all 31 endpoint certificates, ten two-clique profiles, and all 43,890 ordered
pairs of distinct target contractions.  The independently organized checker
uses combinations with replacement, constructs the two list types and finds
an explicit maximum matching for every split, and enumerates every labelled
zero/full endpoint vector for the seven isolated block orders.

Both programs use only exact CPython integer, set, tuple, matching, and hash
arithmetic.  They use no solver, randomness, floating point, generated input,
external data, or project import.  The scripts audit finite arithmetic; the
passage from the imported graph theorems through block/list structure,
split-colour Hall, and the parametric topological dichotomy is the deductive
proof above.

The mathematical trust boundary is Sadhu's connected-complement frontier and
the committed structural chain through the independently reviewed `h>=21`
lemma.  In particular, Gallai's theorem, Stehlik's theorem, the rooted
large-block lemma, and the preceding arbitrary-incidence two-clique
dichotomy are imported rather than reproved here.

## Sources and novelty scope

* A. Sadhu, [*Albertson's Conjecture Holds for `r` at Most
  26*](https://arxiv.org/abs/2609.01682v1), for the order-53/54
  connected-complement frontier.
* M. Stehlik, [*Critical graphs with connected
  complements*](https://doi.org/10.1016/S0095-8956(03)00069-8), JCTB 89
  (2003), 189--194.
* Gallai's low-vertex theorem, stated as Theorem 8 in A. Kostochka's
  [survey](https://kostochk.web.illinois.edu/docs/2008/book06.pdf).
* The preceding [`h=20` weighted
  reduction](../albertson_r27_h20_weighted_pruning/README.md) and reviewed
  [`h>=21` split-colour
  closure](../albertson_r27_h20_split_colour_closure/README.md).

The arXiv and committed-graph searches were refreshed on 2026-09-04.  Sadhu's
paper remained the latest directly relevant preprint, and Discovery Net
through indexed height 1938 contained no `h=21` classification or `h>=22`
consequence.  The split-Hall observation itself is elementary and already
committed; the potentially new content is its combination with the `h=21`
block/list reduction and the new endpoint certificates.  This is a
search-relative novelty statement, not a claim of historical priority.
