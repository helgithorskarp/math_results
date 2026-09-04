# Implicit-edge contraction leaves two Albertson `r=27`, `h=19` subcases

This note advances the sole surviving Albertson frontier row

```text
|V(G)|=53,  |E(G)|=713,  chi(G)=27.
```

Put

```text
L={v:d_G(v)=26},  Q=V(G)-L,  h=|Q|.
```

The preceding four-form reduction and chromatic-core incidence pruning leave
four cases at `h=19`: form B with `chi(G[Q])` in `{8,9,10}`, and form C with
`chi(G[Q])=9`.  We prove the following strict refinement.

## Lemma

If `h=19`, form C is impossible and form B satisfies

```text
                         chi(G[Q]) in {8,9}.              (1)
```

Consequently every remaining `h=19` counterexample candidate has

```text
G[L] = an isolated K19 together with two K8 blocks
       meeting in one cut vertex,
e(G[Q])=56,
chi(G[Q]) in {8,9}.                                      (2)
```

This eliminates two of the four subcases at the preceding frontier.  It does
not assert that either case in (2) exists, does not exclude `h>=20`, and does
not prove Albertson's conjecture for chromatic number 27.

## Imported incidence conclusion

For either remaining low form, let `B` be its isolated large clique.  The
four-form reduction proves that for every optimal `c`-colouring of `G[Q]`
there is one common set `F` of `27-|B|` colours such that, for every `b in B`,

```text
N_G(b) intersect Q
```

contains exactly one vertex in every colour of `F` and no other vertex.
Thus `S_b=N_G(b) intersect Q` receives pairwise distinct colours in every
optimal colouring.  We call such a set *c-rainbow*.

The two cases addressed here are:

| form | `|B|` | `|L-B|` | `c` | `e(G[Q])` | `|S_b|` |
|---|---:|---:|---:|---:|---:|
| B | 19 | 15 | 10 | 56 | 8 |
| C | 18 | 16 | 9 | 46 | 9 |

Every vertex of `Q` has degree at least 27 because `G` is 27-critical.

## A one-edge implicit-edge lemma

We use the following elementary observation.

**Rainbow contraction lemma.**  Let `c in {9,10}`, let `X` be `c`-chromatic,
let `S` be a `c`-rainbow set of order at least seven, and suppose

```text
e(X) <= binom(c+1,2)+1.                                  (3)
```

Then `S` is a clique.

To prove it, suppose that `x,y in S` are nonadjacent and contract them to one
vertex `z`.  A `c`-colouring after contraction would pull back to a
`c`-colouring of `X` in which `x,y` have the same colour.  Hence

```text
chi(X/xy) >= c+1.                                        (4)
```

Take a `(c+1)`-critical subgraph `J` of `X/xy`.  If it has more than `c+1`
vertices, minimum degree `c` gives

```text
e(J) >= ceil(c(c+2)/2) > binom(c+1,2)+1                 (5)
```

for the values `c=9,10` used here.  Thus `X/xy` contains a `K_(c+1)`.
This clique must contain `z`, since otherwise `X` itself contains
`K_(c+1)`.  Its other vertices form a `K_c`, say `W`, and every vertex of
`W` is adjacent to at least one of `x,y`.

Contracting `x,y` deletes one edge for each common neighbour.  Equations
(3)--(4) therefore allow at most one common neighbour.  The edges of `W`
and the edges from `W` to `{x,y}` already use `binom(c+1,2)` edges, plus one
more for every common neighbour in `W`.  At most one edge remains outside
this scaffold.

Neither `x` nor `y` is complete to `W`, since `X` is only `c`-chromatic.
The sets of their nonneighbours in `W` are nonempty and disjoint.  Colour
`W` with all `c` colours and give `x,y` colours of respective nonneighbours.
The at-most-one residual edge causes no extension problem.  If a vertex
`s in S-{x,y}` lies in `W` and is not a common neighbour of `x,y`, choose the
colouring so that `s` agrees with the endpoint missing it, contradicting the
rainbow property.  Thus at most one further vertex of `S` lies in `W`.

At least `|S|-3>=4` vertices of `S` lie outside `W union {x,y}`.  At most two
of them meet the sole residual edge, so two are isolated and may receive the
same colour.  This is the final contradiction and proves the lemma.  This is
the standard implicit-edge contraction mechanism; the content needed here is
the sharp one-residual-edge count.

## Form C with `c=9`

The rainbow contraction lemma makes every `S_b` a `K9`.  Fix one of them,
`R=K9`.  It consumes 36 of the 46 edges in `G[Q]`.

Any other `K9`, say `T`, must meet `R` in at least eight vertices, because

```text
e(R union T) >= 2 binom(9,2)-binom(|R intersect T|,2),
```

and the right side exceeds 46 when the intersection has order at most seven.
If `T` is distinct, it therefore has the form

```text
T=(R-{u}) union {x},                                     (6)
```

where `x` lies outside `R` and is adjacent to the other eight vertices of
`R`.

There is at most one distinct alternative (6).  Two alternatives using
different outside vertices require 16 of the ten edges outside `R`.  Two
using the same outside vertex but omitting different vertices make that
outside vertex complete to `R`, producing a `K10`, contrary to `c=9`.

If no alternative occurs, all `B`--`Q` edges end in `R`.  Any vertex outside
`R` then has no neighbour in `B`, high-graph degree at most ten, and at most
16 neighbours in `L-B`; hence its total degree is at most 26, a contradiction.

If one alternative occurs, the union of the two `K9` rows uses 44 high
edges.  All `B`--`Q` edges end in its ten vertices, while each of the nine
remaining high vertices has high-graph degree at most two.  Its total degree
is then at most 18, again impossible.  This eliminates form C.

## Form B with `c=10`

First `G[Q]` contains a `K10`.  Indeed, take a 10-critical subgraph `R`.  If
`|R|=10` this is immediate.  Order 11 is impossible: minimum degree nine
makes the complement a matching, and the only 10-chromatic possibility is
`K11` minus one edge, which contains a proper 10-chromatic `K10`.  At order
12, Gallai's critical edge bound gives

```text
2e(R) >= 9*12 + 2*8 - 2 = 122 > 112,
```

while at every order at least 13 the minimum-degree handshake bound gives
`e(R)>=59>56`.

Fix a core `C=K10`; only 11 high edges lie outside it.  The rainbow
contraction lemma makes every row `S_b` a `K8`.  If such a clique uses `t`
vertices outside `C`, it requires at least

```text
t(8-t)+binom(t,2)                                       (7)
```

edges outside the core.  This is 13 already at `t=2`, so every row uses at
most one outside vertex.  An outside vertex occurring in a row requires
seven edges to `C`; hence two distinct outside vertices cannot occur among
the rows, since they would require 14 of the available 11 edges.

At least eight of the nine vertices in `Q-C` consequently have no neighbour
in `B`.  Each needs at least 12 high-graph neighbours in order to reach total
degree 27, because `|L-B|=15`.  Their high-degree sum is therefore at least
96.  On the other hand, summing high degrees over all nine vertices outside
`C` counts the 11 residual edges at most twice, and is at most 22.  This
contradiction eliminates form B with `c=10` and proves (1)--(2).

## Reproduction and trust boundary

Run under CPython 3.9 or later; there are no third-party dependencies:

```sh
python3 verify.py
python3 independent_check.py
```

The primary checker audits the contraction thresholds, every scaffold
budget, the `K9` intersection alternatives, the `K10` critical-core bounds,
the `K8` outside-core costs, and both degree contradictions.  The independent
checker enumerates all 92,378 nine-subsets and all 75,582 eight-subsets of a
labelled 19-set, reconstructing exactly the clique-row candidates allowed by
the two edge budgets; it separately enumerates all contraction-scaffold type
patterns.

Both scripts use exact CPython integer, set, tuple, and hash arithmetic, with
no solver, randomness, floating point, generated input, external data, or
project import.  They do not enumerate critical graphs.  The prose supplies
the graph-theoretic bridge from arbitrary colourings and incidence rows to
the finite edge budgets.

Expected final digests under CPython 3.9 or later are

```text
primary:     c6e88e1017638c5e4170c730cb6a3fe42f28dfcd51e30312b1d362ff2c7ac935
independent: 44c7cc33fbf10947b91cdaf9621f27ec86d16b4f66b2fea8bc9f79d022e4792f
```

The mathematical trust boundary is Sadhu's connected-complement frontier,
Gallai's published critical-edge bound, and the committed four-form and
incidence-pruning lemmas.  In particular, the rigid rainbow-row conclusion
is imported rather than recomputed here.

## Sources and novelty scope

* A. Sadhu, [*Albertson's Conjecture Holds for `r` at Most
  26*](https://arxiv.org/abs/2609.01682v1), especially Lemma 2.3 and
  Theorem 1.3.
* The preceding [four-form
  reduction](../albertson_r27_order53_h19_reduction/README.md) and
  [chromatic-core incidence
  pruning](../albertson_r27_h19_incidence_pruning/README.md).

The implication from a forced colour inequality to contraction is commonly
called an implicit-edge argument.  Targeted literature and committed-graph
searches found no prior application giving the two closures above.  This is
a search-relative novelty statement, not a claim of historical priority.
