# Four exact low-block forms contain the Albertson `r=27`, `h=19` frontier

This note advances the sole surviving Albertson frontier row

```text
|V(G)|=53,  |E(G)|=713,  chi(G)=27.
```

Put

```text
L={v:d_G(v)=26},  Q=V(G)-L,  h=|Q|,
H=complement(G).
```

The preceding committed results give `h>=19`.  This note classifies the
equality case.  If `h=19`, then `G[L]` has one of the following four forms,
where the displayed clique blocks have no other low--low edges:

| form | blocks of `G[L]` | `e(G[L])` | `e(G[Q])` |
|---|---|---:|---:|
| A0 | isolated `K18`, isolated `K8`, isolated `K8` | 209 | 38 |
| A1 | isolated `K18`, two `K8` blocks joined by one bridge | 210 | 39 |
| B | isolated `K19`, two `K8` blocks meeting in one cut vertex | 227 | 56 |
| C | isolated `K18`, a `K8` and `K9` meeting in one cut vertex | 217 | 46 |

Thus the two-large-block regime is closed, four or more large blocks are
excluded by the edge budget, and 107 arithmetically feasible three-block
signatures reduce to four exact obstruction forms.  These four forms are not
excluded here, so this is a structural reduction, not a proof of Albertson's
conjecture for chromatic number 27.

There is also a rigid colour-incidence conclusion.  Fix an optimal
`c`-colouring `phi` of `G[Q]`, using colours from a 26-colour palette, and let
`B` be the isolated `K18` or `K19` in the corresponding row.  There is a
common set `F` of `27-|B|` colours such that every vertex of `B` has exactly
one neighbour in each colour of `F` and no other neighbour in `Q`.  The
ranges allowed by the edge count are

```text
A0,A1: |B|=18, c=9,       |F|=9;
B:     |B|=19, 8<=c<=11,  |F|=8;
C:     |B|=18, 9<=c<=10,  |F|=9.
```

The assertion holds for every optimal colouring of `G[Q]`.

## Imported facts

We use the following established inputs.

1. Sadhu's September 2026 frontier and the subsequent committed closures
   leave only a 27-critical graph on 53 vertices and 713 edges whose
   complement is connected and which contains no subdivision of `K27`.
2. Gallai's theorem says that every block of `G[L]` is a clique or an odd
   cycle.
3. Stehlik's theorem makes `H` factor-critical.  A conformal triangle in `H`
   is impossible, since that triangle and a perfect matching of the other 50
   vertices would be a 26-colouring of `G`.
4. The independently reviewed rooted Gallai lemma puts every low vertex in a
   clique block of `G[L]` of order at least `27-h`.
5. Every high vertex has complement degree at most 25, since its graph degree
   is at least 27.
6. The committed matching/conformal-triangle argument closes the two-clique
   normal forms through `h=18`.  Its numerical boundary is checked afresh
   below at `h=19`.

Set `h=19`.  Then `|L|=34`, every low vertex belongs to a clique block of
order at least

```text
s=27-h=8,                                               (1)
```

and summing degree 26 over `L` gives

```text
e(L,Q)=26*34-2e(G[L]),
e(G[Q])=e(G[L])-171,
e(G[L])>=171.                                           (2)
```

Call the clique blocks supplied by (1) *large*.

## At most three large blocks

Restrict the block-cut forest to its large-block nodes and their common cut
vertices.  If there are `b` large blocks and this restricted forest has `c`
components, put `q=b-c`.  Repeated cut vertices give

```text
sum_i |B_i|=34+q.                                       (3)
```

Every other block uses at most one vertex from each direct large-block
component.  For at most four large blocks it is therefore a clique connector,
not an odd cycle of order at least five.  Connector blocks joining the `c`
direct components form a hyperforest and add at most `binom(c,2)` edges.

Five blocks have union order at least `5*8-4=36`, so there are at most four.
For four blocks, convexity in (3), including the connector bound, gives

| `q` | extremal orders | connector bound | upper bound on `e(G[L])` |
|---:|---|---:|---:|
| 0 | `(8,8,8,10)` | 6 | 135 |
| 1 | `(8,8,8,11)` | 3 | 142 |
| 2 | `(8,8,8,12)` | 1 | 151 |
| 3 | `(8,8,8,13)` | 0 | 162 |

Every value is below the floor 171 in (2).  One block cannot cover 34 low
vertices because a large block has order at most 26.  Hence only two or three
large blocks remain.

## The two-block regime is terminal

Two large blocks cannot meet: their orders would sum to 35, whereas a common
cut vertex and degree 26 force their order sum to be at most 28.  They are
therefore disjoint cliques `C=K_a,D=K_b`, with `a+b=34`, and at most one
bridge joins them.  Write

```text
a=8+p,  b=8+q,  p+q=18.
```

An ordinary row of `H[C,Q]` has size `p`, and an ordinary row of `H[D,Q]`
has size `q`; a bridge endpoint has one additional complement neighbour in
`Q`.  Exact accounting leaves nine rows.  In the final column
`D0=t+e(H[Q])`, with `t` the bridge indicator.

| `(a,b)` | `(p,q)` | `D0` |
|---|---|---:|
| `(9,25)` | `(1,17)` | 6 |
| `(10,24)` | `(2,16)` | 21 |
| `(11,23)` | `(3,15)` | 34 |
| `(12,22)` | `(4,14)` | 45 |
| `(13,21)` | `(5,13)` | 54 |
| `(14,20)` | `(6,12)` | 61 |
| `(15,19)` | `(7,11)` | 66 |
| `(16,18)` | `(8,10)` | 69 |
| `(17,17)` | `(9,9)` | 70 |

Both bridge variants are arithmetically possible in every row.

We record why the preceding parametric dichotomy crosses the new boundary.
The elementary uniform-row lemma says that a bipartite graph with left side
`X`, `|X|>r`, and every left degree at least `r` either has an `(r+1)`-
matching or all left rows are one common `r`-set.  This follows immediately
from Konig's matching-cover theorem: a cover of order at most `r` cannot
contain a left vertex, and hence lies on the right and contains every row.

Suppose first that there is no bridge.  If both low--high incidence graphs
have matchings of sizes `p+1,q+1`, give `Q` singleton colours, extend them
along the matchings, and pair the seven residual vertices on each low side
across the complement-complete `C,D` cut.  This is a 26-colouring.  Otherwise,
after relabelling, every `C`-row is one common `p`-set `S`.  Put `T=Q-S`.
The 27 vertices `C union T` form a clique in `G` apart from the target edges
of `H[T]`.

No target gives a `K27`.  If there is exactly one target `uv`, it has a path
outside the branch set.  A support adjacent in `G` to both ends gives a
two-edge path.  Otherwise supports split according to which endpoint they
meet in `H`.  Opposite one-end types give a path through the two supports;
if their mutual edge is in `H`, each has at least 11 graph neighbours in the
opposite clique, so two distinct clique vertices may be inserted.  If all
supports meet one endpoint, that endpoint has at least two graph neighbours
in the opposite clique.  A support meeting only that endpoint has at least
10; two distinct choices give the required path (if this lower bound exceeds
the opposite clique order, that support pattern is impossible).  If every support meets
both ends, choose distinct clique neighbours of the two endpoints.  The
counts are exact consequences of `d_H(x)<=25` and `|D|=26-p`.  Thus one
target gives a `TK27` even though the older common-neighbour inequality no
longer has slack.

If `H[T]` has two distinct edges, contract either one as a two-vertex high
colour class.  A `q`-matching in the contracted `D` incidence graph gives a
26-colouring: there are 18 high classes and eight residual cross-pairs.  If
both distinct contractions fail, their uniform contracted rows force all
original `D`-rows to be a common `q`-set `R`.  Indeed, the symmetric
difference of two equal-sized original rows lies in each target pair; two
distinct pairs intersect in at most one vertex, while a symmetric difference
has even order.

The degree cap makes `S,R` disjoint, and `p+q=18` gives

```text
Q=S disjoint-union R disjoint-union {z}.                 (4)
```

Factor-critical matching balance and the absence of conformal triangles give

```text
N_H(z) meets both S and R,
H[S]=H[R]=H[N_H(z) intersect S, N_H(z) intersect R]=empty. (5)
```

For completeness, deleting a vertex of `S` and balancing a perfect matching
shows that if `z` could only match into `S`, an edge inside `R` would be
forced; that edge and a low vertex form a conformal triangle.  The symmetric
argument makes both neighbour sets nonempty.  Any internal support edge or
edge between the two `z`-neighbour sets similarly completes an explicit
conformal triangle; after its deletion, attach the remaining supports to
their low sides and pair the nine residual low vertices on each side.

Inject the smaller of the two neighbour sets in (5) into the larger.  Using
distinct vertices of the opposite low clique, route every missing branch
edge by a path of the form

```text
z - c_x - y_x - x.
```

This gives a `TK27`, exactly as in the preceding parametric proof.

With one low bridge, the endpoint's extra complement neighbour augments any
uniform ordinary rows, so both incidence graphs have their one-larger
matching.  Compatible choices give the same 26-colouring; the seven residual
cross-pairs can avoid the single bridge edge.  If no compatible choices
exist, matching rigidity gives disjoint supports `S,R`, a unique `z`, and
endpoint rows `S+z,R+z`.  Absence of conformal triangles leaves only
`S`--`R` edges in `H[Q]`.  Then one 27-vertex branch set is complete except
for the endpoint--`z` edge, which is routed through the low bridge and one
additional vertex of the opposite clique.  Thus every two-block form is
26-colourable or contains a `TK27`.

## Three blocks and strict degree-list slack

For three blocks, `q` is 0, 1, or 2.  Connector-edge totals are respectively

```text
q=0: 0,1,2,3;   q=1: 0,1;   q=2: 0.                    (6)
```

Intersecting block orders `u,v` satisfy `u+v<=28`.  At `q=2`, one common cut
in all three blocks has 33 low neighbours, so the blocks instead form a path
with two distinct cuts.  Exact enumeration of (2), (3), and (6) leaves 56,
32, and 19 edge-budget signatures for `q=0,1,2`.

Every block is now a clique, so `chi(G[L])` is the largest block order.  A
graph with chromatic number `c` has at least `binom(c,2)` edges; hence the
edge count in (2) bounds `chi(G[Q])`.  Disjoint palettes close all but 14 of
the 107 signatures.

The remaining collapse uses the following elementary list observation.
Colour `G[Q]` optimally with `c` colours from a palette of 26.  For a low
vertex `v`, let

```text
A(v)=[26] minus the colours appearing on N_G(v) intersect Q.
```

Because `d_G(v)=26`,

```text
|A(v)| >= 26-d_Q(v)=d_{G[L]}(v).                        (7)
```

If a connected graph has lists of size at least its degrees, with strict
inequality at one vertex, it is list-colourable: root a spanning tree at the
strict vertex, order every other vertex before a later neighbour, and colour
greedily.  The root has one spare colour at the end.

All `26-c` colours unused on `Q` lie in every list `A(v)`.  Consequently, if
an endblock `K_t` of a low component has a noncut vertex and

```text
26-c > t-1,                                              (8)
```

that component is list-colourable by (7).

Each of the 14 exceptions has a unique largest block.  Using the edge-count
upper bound on `c`, inequality (8) holds for both smaller blocks.  A low
component containing at least two large blocks has a leaf large block; since
there is only one largest block, it has a smaller leaf and is colourable.
An isolated smaller block is colourable for the same reason.  Hence the only
possible obstruction is an isolated copy of the unique largest block.

Reading this condition back through the direct-intersection and connector
forest eliminates all `q=2` rows, every row where the largest block meets a
smaller one, and every connector that reaches the largest block.  Precisely
the four forms A0, A1, B, C in the opening table remain.

Finally, for an isolated clique `B`, its list-incidence graph has left side
of order `|B|` and every left list has size at least `|B|-1`.  The same
uniform-row lemma says that either it has a system of `|B|` distinct
representatives, extending the colouring, or every list is one common
`(|B|-1)`-set.  Since all other low components have already been coloured,
the latter alternative is forced.  Taking complements in the 26-colour
palette gives the common set `F` and the rigid colour-incidence statement at
the start of the note.

## Reproduction and trust boundary

Run under CPython 3.9 or later; there are no third-party dependencies:

```sh
python3 verify.py
python3 independent_check.py
```

With CPython 3.11.2, the expected final digests are

```text
primary:     fe776a297d8ec11cfd5716ad88ca835634b654b50f8467d2078d3c691a1a9983
independent: 3762983a8489bc7672658b009b377f510b5d208632ae5a956cd209897b46ee0e
```

SHA-256 of `verify.py`:
`3710730a1f70bd50e1e22d275b3546d8ac60d0a4f328b448f4e2eea6148a28c0`.
SHA-256 of `independent_check.py`:
`b8f31c20095dd5a7effd0b1538784e061fb4d45337b5a775b2e93709533c8b1d`.

The primary checker enumerates the four-block caps, all 107 three-block
edge signatures, their 14 palette exceptions, the four residual forms, all
nine two-clique profiles and 18 bridge variants, and the exact matching,
route, balance, and contraction counts.  The independently organized checker
reconstructs the bounds from closed formulas and a separate partition loop.

Both checkers use exact CPython integer, set, tuple, and hash arithmetic,
with no solver, randomness, floating point, generated input, external data,
or project import.  The scripts do not enumerate critical graphs.  The prose
supplies the graph-theoretic bridge from the imported theorems and arbitrary
incidence matrices to the finite arithmetic.

The mathematical trust boundary is Sadhu's connected-complement frontier,
Gallai's low-vertex block theorem, Stehlik's colouring theorem, Konig's
matching-cover theorem, the independently reviewed rooted Gallai lemma, and
the committed closures through `h=18`.  The new strict-list argument is
proved above.  This note does not exclude the four displayed forms and does
not prove Albertson `r=27`.

## Sources and novelty scope

* A. Sadhu, [*Albertson's Conjecture Holds for `r` at Most
  26*](https://arxiv.org/abs/2609.01682v1), for the order-53
  connected-complement frontier and exclusion of a topological `K27`.
* M. Stehlik, [*Critical graphs with connected
  complements*](https://doi.org/10.1016/S0095-8956(03)00069-8), JCTB 89
  (2003), 189--194.
* Gallai's low-vertex theorem, stated as Theorem 8 in A. Kostochka's
  [survey](https://kostochk.web.illinois.edu/docs/2008/book06.pdf).
* The preceding [`h=18`
  closure](../albertson_r27_order53_h18_closure/README.md) and the
  independently reviewed [rooted Gallai
  reduction](../albertson_r27_gallai_blocks_independent_review/README.md).

Targeted searches of the September 2026 Albertson paper, its cited critical-
graph sources, and the committed Discovery Net found no prior `h=19`
classification, strict-list collapse, or four-form reduction.  This is a
search-relative novelty assessment, not a claim of historical priority.
