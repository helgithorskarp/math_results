# Gallai-block classification closes Albertson `r=27` at `h=18`

This note advances the sole surviving Albertson frontier row

```text
|V(G)|=53,  |E(G)|=713,  chi(G)=27.
```

Put

```text
L={v:d_G(v)=26},  Q=V(G)-L,  h=|Q|,  H=complement(G).
```

The preceding committed lemma proves `h>=18`.  Here every possible Gallai
block configuration at equality is classified and eliminated.  Therefore
every hypothetical counterexample in this row satisfies

```text
                         |Q| >= 19.                       (1)
```

This is a conditional advance within Sadhu's September 2026 frontier, not a
proof of Albertson's conjecture for chromatic number 27.

## Imported facts

We use the following established inputs.

1. Sadhu's frontier and subsequent committed reductions leave only a
   27-critical graph on 53 vertices and 713 edges, with connected complement
   and no subdivision of `K27`.
2. Gallai's theorem says that every block of `G[L]` is a clique or an odd
   cycle.
3. Stehlik's theorem makes `H` factor-critical.  Equivalently, deleting any
   vertex leaves a perfect matching.  A conformal triangle in `H` is
   impossible, since it and a perfect matching of the remaining 50 vertices
   would give a 26-colouring of `G`.
4. The reviewed rooted Gallai lemma puts every low vertex in a clique block
   of `G[L]` of order at least

   ```text
   s=27-h.                                                (2)
   ```

5. Every high vertex satisfies

   ```text
   d_H(q)<=25,                                            (3)
   ```

   because its degree in `G` is at least 27.
6. The preceding edge-budget and chromatic-palette closures give `h>=18` and
   supply the parametric two-clique matching dichotomy through `h=17`.

For the rest of the proof set `h=18`.  Thus `|L|=35`, `s=9`, and summing the
fixed degree 26 over `L` gives

```text
e(L,Q)=26*35-2e(G[L]),
e(G[Q])=e(G[L])-197,
e(G[L])>=197.                                             (4)
```

## Large-block incidence and connector bound

Call the clique blocks guaranteed by (2) *large*.  The block-cut incidence
graph is a forest.  If there are `B` large blocks and their direct-incidence
forest has `c` components, put `q=B-c`.  Counting repeated cut vertices gives

```text
sum |B_i| = 35+q.                                         (5)
```

Every low vertex is in a large block.  A different block can therefore use
at most one vertex from each large block.  With at most four large blocks it
cannot be an odd cycle of order at least five, so every remaining block is a
clique connector.  Connector blocks joining the `c` direct components form a
hyperforest.  If their orders are `k_1,...,k_t`, then

```text
sum (k_i-1) <= c-1.
```

Convexity, or repeatedly merging two connectors, now gives the sharp upper
bound

```text
sum binom(k_i,2) <= binom(c,2).                            (6)
```

One large block cannot cover 35 vertices; moreover every large block has
order at most 26 because a `K27` is already terminal.  Five large blocks
would cover at least
`5*9-4=41` vertices.  Hence `2<=B<=4`.

If `B=4`, equation (5), convexity, and (6) give the following complete upper
bounds.  The `q=0` order sum is already impossible.

| `q` | extremal block orders | connector bound | `e(G[L])` upper bound |
|---:|---|---:|---:|
| 1 | `(9,9,9,9)` | 3 | 147 |
| 2 | `(9,9,9,10)` | 1 | 154 |
| 3 | `(9,9,9,11)` | 0 | 163 |

All contradict (4).  Thus only two or three large blocks remain.

## Exact three-block certificate

For three blocks, `q` is 0, 1, or 2 and the possible connector-edge totals
are respectively

```text
q=0: 0,1,2,3;       q=1: 0,1;       q=2: 0.              (7)
```

If two blocks of orders `u,v` meet, their common cut vertex has at least
`u+v-2` low neighbours, so `u+v<=28`.  When `q=2`, a common cut vertex in all
three blocks would have

```text
sum_i (|B_i|-1)=(35+2)-3=34
```

low neighbours, which is impossible.  Hence the blocks form a path with two
distinct cuts.

The exact enumeration of (4)--(7) has 13, 24, and 14 edge-budget survivors
for `q=0,1,2`.  Since every block is a clique,

```text
chi(G[L]) = max_i |B_i|.                                  (8)
```

Also, any graph of chromatic number `c` has at least `binom(c,2)` edges: take
a `c`-critical subgraph and sum its minimum degrees.  Applying this to
`G[Q]`, whose edge count is fixed by (4), gives maximum disjoint-palette
bounds 22, 26, and 29 in the three rows of `q`.  Every configuration closes
except the following two path signatures.

| block orders | `e(G[L])` | `e(G[Q])` | disjoint-palette bound |
|---|---:|---:|---:|
| `(9,10,18)` | 234 | 37 | 27 |
| `(9,9,19)` | 243 | 46 | 29 |

Both exceptions have a short exact colour-class certificate.

### The `(9,10,18)` path

A cut vertex `y` of the `K18` lies also in a block of order 9 or 10.  Its
number of complement neighbours in `Q` is respectively

```text
(18-1)+(9-1)-8=17,    or    (18-1)+(10-1)-8=18.           (9)
```

Here the subtraction by 8 uses `d_G(y)=26` and `|Q|=18`.  If
`chi(G[Q])<=8`, disjoint palettes already give 26 colours.  Otherwise take a
9-colouring of `G[Q]`.  At most one high vertex lies outside `N_H(y)`, so at
most one of the nine colour classes is contaminated; some entire colour
class lies in `N_H(y)`.  Give `y` that colour.  Rooting the low block tree at
`K18`, extend its 18-colouring while avoiding this marked colour away from
`y`.  Thus `chi(G)<=18+9-1=26`.

### The `(9,9,19)` path

A `K19` cut vertex `y` has all 18 high vertices as complement neighbours.
Every non-cut vertex `v` of `K19` has a complement row of order 10 in `Q`.
In a `c`-colouring of `G[Q]`, its eight bad high vertices contaminate at most
eight colour classes.  Hence at least `c-8` classes lie wholly in
`N_H(v)`.

For `c<=7`, disjoint palettes suffice.  For `c=8`, reuse any class on the
universal cut vertex `y`.  For `c=9`, reuse one further compatible class on
an internal `K19` vertex.  For `c=10`, each of two internal vertices has at
least two compatible classes, so Hall's condition gives two distinct such
classes; reuse a third class on `y`.  For `c=8,9,10` respectively, this gives

```text
19+c-(c-7)=26.
```

At most three `K19` colours are marked.  The remaining at least 16 colours
are more than enough to colour the two attached `K9` blocks outward through
their cut vertices without reusing a marked colour on an incompatible
vertex.  This eliminates every three-block form.

## Two large blocks

Two large blocks cannot meet: their orders would sum to 36, while a common
cut vertex would force their sum to be at most 28.  Thus they are disjoint
cliques `C=K_a,D=K_b`, with `a+b=35`, and there is at most one bridge between
them.  Write

```text
p=a-9,  q=b-9,  p+q=17.
```

An ordinary row of the complement incidence graph `H[C,Q]` has order `p`,
and a bridge-end row has order `p+1`; the analogous orders on `D` are `q` and
`q+1`.  Exact edge accounting gives eight profiles.  In the last column
`D_0=t+e(H[Q])`, where `t` is the bridge indicator.

| `(a,b)` | `(p,q)` | `D_0` |
|---|---|---:|
| `(10,25)` | `(1,16)` | 5 |
| `(11,24)` | `(2,15)` | 19 |
| `(12,23)` | `(3,14)` | 31 |
| `(13,22)` | `(4,13)` | 41 |
| `(14,21)` | `(5,12)` | 49 |
| `(15,20)` | `(6,11)` | 55 |
| `(16,19)` | `(7,10)` | 59 |
| `(17,18)` | `(8,9)` | 61 |

Both bridge variants are arithmetically possible in every row.

The parametric matching proof from the preceding edge-budget lemma extends
to all these rows.  For completeness, its finite alternatives are recalled
here.  Without a bridge, simultaneous matchings of orders `p+1,q+1` attach
low vertices to the 18 singleton high colours; the eight residual vertices
on each low side pair across the complement-complete cut, giving 26 colours.
If a matching is deficient, Konig's theorem makes every row on that side a
common `p`-set `S`.  Then `C union (Q-S)` is a 27-vertex clique apart from the
target edges of `H[Q-S]`.

Zero targets give `K27`.  One target `uv` has an external path.  For `p=1`,
both endpoints have a graph neighbour in the opposite `K25`; use one common
neighbour or two distinct neighbours joined inside that clique.  For
`p>=2`, either a support vertex is adjacent in `G` to both ends, or support
types yield a path through two supports and one or two vertices of the
opposite clique.  In the remaining one-centre patterns, (3) gives each target
endpoint at least two graph neighbours in that clique and every one-end
support at least eleven.  This two-clique-vertex route is the only new
boundary check needed at `h=18`; it also repairs the equality case where a
common-neighbour pigeonhole would be insufficient.

With two target edges, contract either target.  A `q`-matching in the
contracted opposite incidence graph gives 17 high colour classes plus nine
residual low pairs, hence a 26-colouring.  Failure for two distinct targets
makes all opposite rows common: their equal-size symmetric difference lies
in both endpoint pairs and is even, hence empty.  Calling the opposite
support `R`, the degree cap gives

```text
Q = S disjoint-union R disjoint-union {z}.
```

The factor-critical balance and absence of conformal triangles then give the
same terminal certificate as in the preceding lemma: `z` meets both supports
in `H`, while `H[S]`, `H[R]`, and the cross graph between its two support
neighbour sets are empty.  Inject the smaller neighbour set into the larger
and route all missing `z` edges through distinct vertices of the opposite
low clique, producing a `TK27`.

With one low bridge, the non-endpoint uniform-row alternative always augments
through the endpoint's extra neighbour, so both incidence graphs have the
one-larger matching.  Compatible choices give a 26-colouring.  Incompatible
choices force common supports `S,R`, a unique `z`, and endpoint rows
`S+z,R+z`.  Conformal-triangle exclusion leaves only `S`--`R` edges in
`H[Q]`; the sole missing branch edge is routed through the low bridge and one
additional vertex of the opposite clique.  Thus every two-block form is
26-colourable or contains `TK27`.

This closes `h=18` and proves (1).

## Reproduction and trust boundary

Run under CPython 3.9 or later; there are no third-party dependencies:

```sh
python3 verify.py
python3 independent_check.py
```

With CPython 3.11.2, the expected final digests are

```text
primary:     2dffc22593f4f95fb39a33e2d425a57f454f5924d8b6ca073d60f36f3ea8d5c3
independent: 398d584969e26306e462fdb27c53eb43333e627cc40b0b0e2af4efa456af88e3
```

SHA-256 of `verify.py`:
`0ad425b4e91bac6a65215588d2e7308d8fc4f8e3d0985785451b01c4f86c7dbf`.
SHA-256 of `independent_check.py`:
`96a6b0f5ee86e0135bac9265d2c09615c5fcf8a200aacfc40a65d57a517da85e`.

The primary checker enumerates labelled direct-intersection geometries, all
51 surviving three-block edge signatures, 2,025 worst-case two-row Hall
patterns, all eight two-clique profiles and 16 bridge variants, 192 terminal
identities, and 23,256 ordered two-contraction comparisons.  The separately
organized checker reconstructs the block bounds from convex formulas and
audits 11,628 unordered contraction pairs.

Both scripts use exact CPython integer/set arithmetic without a solver,
randomness, floating point, generated input, external data, or project
imports.  They do not enumerate critical graphs.  The prose proof is the
bridge from the imported graph theorems and arbitrary incidence matrices to
the finite certificate.

The mathematical trust boundary is Sadhu's September 2026 connected-
complement frontier, Gallai's low-vertex block theorem, Stehlik's colouring
theorem, Konig's theorem, the independently reviewed rooted Gallai lemma, and
the preceding committed closures through `h=17`.  This note proves only the
new `h=18` classification and `h>=19` consequence.

## Sources and novelty scope

* A. Sadhu, [*Albertson's Conjecture Holds for `r` at Most
  26*](https://arxiv.org/abs/2609.01682v1), for the order-53
  connected-complement frontier and exclusion of a topological `K27`.
* M. Stehlik, [*Critical graphs with connected
  complements*](https://doi.org/10.1016/S0095-8956(03)00069-8), JCTB 89
  (2003), 189--194.
* Gallai's low-vertex theorem, stated as Theorem 8 in A. Kostochka's
  [survey](https://kostochk.web.illinois.edu/docs/2008/book06.pdf).
* The preceding [`h=14`--`17`
  closure](../albertson_r27_order53_h14_h16_closure/README.md) and the
  independently reviewed [rooted Gallai
  reduction](../albertson_r27_gallai_blocks_independent_review/README.md).

Targeted searches of the current Albertson and sparse-critical literature
and of the committed Discovery Net found no prior four-block exclusion,
three-block certificate, or `h>=19` consequence at this frontier.  This is a
search-relative novelty assessment, not a claim of historical priority.
