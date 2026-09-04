# The equality-boundary Gallai classification closes Albertson `r=27`, `h=13`

This note advances the sole surviving Albertson frontier row

```text
|V(G)|=53,  |E(G)|=713,  chi(G)=27.
```

Let

```text
L={v:d_G(v)=26},  Q=V(G)-L,  h=|Q|,  H=complement(G).
```

The preceding coloring-or-subdivision theorem proves `h>=13`.  Here the
equality case `h=13` is classified and eliminated.  Consequently every
hypothetical counterexample in the final order/size row satisfies

```text
                         |Q| >= 14.                       (1)
```

The new issue at `h=13` is structural.  The earlier two-large-block proof
used a strict degree inequality which becomes equality here.  The only new
Gallai-block possibility is a path of three `K14` blocks.  Exact low-degree
accounting rules it out immediately.  The remaining two-clique profiles are
closed by extending the preceding matching/conformal-triangle dichotomy to
this boundary.  This is a conditional advance within Sadhu's September 2026
frontier, not a proof of Albertson's conjecture for chromatic number 27.

## Imported facts and notation

We use four established inputs.

1. Sadhu's frontier permits us to take a 27-critical graph on 53 vertices
   and 713 edges whose complement is connected.  A counterexample contains
   no subdivision of `K27`.
2. Gallai's theorem says that every block of `G[L]` is a clique or an odd
   cycle.
3. Stehlik's theorem supplies, for each vertex `v`, a 26-colouring of `G-v`
   whose classes all have at least two vertices.  At order 53 all classes
   are pairs, so `H` is factor-critical.
4. The preceding rooted Kempe argument shows that, when `h=13`, every low
   vertex lies in a clique block of `G[L]` of order at least

   ```text
   s=27-h=14.                                             (2)
   ```

A triangle of `H` whose deletion leaves a perfect matching is called
conformal.  No such triangle exists here: it would be one independent
triple and 25 independent pairs in `G`, hence a 26-colouring.  Connectedness
of `H` and criticality also give

```text
d_H(q) <= 25  for every q in Q.                           (3)
```

The total degree excess is

```text
sum_v(d_G(v)-26)=2*713-26*53=48.                         (4)
```

## Exact equality-boundary block classification

Call the clique blocks supplied by (2) large.  Distinct blocks meet in at
most one cut vertex, and their block-cut incidence graph is a forest.  If a
low vertex lies in two large blocks of orders `u,v`, then

```text
(u-1)+(v-1) <= d_G(x)=26.
```

Since `u,v>=14`, equality is forced: both blocks are `K14`, the shared
vertex has all 26 neighbours inside them, and it belongs to no further
block.  In particular, no vertex lies in three large blocks.

The large blocks cover all `|L|=40` vertices.  One block cannot do so because
a counterexample has no `K27`.  Four blocks would have union of order at
least

```text
4*14-3=53>40,
```

even after every possible forest intersection.  With two blocks, an
intersection would force two `K14`s and a union of only 27 vertices, so the
blocks must be disjoint and their orders sum to 40.  With three blocks, the
minimum union is `3*14-2=40`; equality forces three `K14`s joined through
two distinct cut vertices, that is, a path in the block-cut tree.  These are
the only alternatives:

```text
(A) two vertex-disjoint cliques K_a,K_b, a+b=40;
(B) three K14 blocks in a path, covering all 40 low vertices.
```

No further low block is possible in (B), since all vertices are already in
large blocks and another block meeting two of them would create a cycle in
the block-cut tree.  Thus (B) has exactly

```text
e(G[L])=3*C(14,2)=273.
```

The fixed low degree sum then forces

```text
e(L,Q)=26*40-2*273=494.
```

Already `273+494=767>713`, before counting an edge of `G[Q]`.  Alternative
(B) is impossible.

In (A), any additional nontrivial low block can meet each of `A,B` in at
most one vertex.  It is therefore a single `A`--`B` bridge, and there is at
most one.  Put

```text
t = bridge indicator,
r = e(H[Q]),
d = a-14,
e = b-14.
```

Thus `d+e=12`.  Exact use of (4), or equivalently of the low degree sum and
`|E(G)|=713`, gives the complete table below.  `D=t+r`, so a row with `D>0`
represents the two variants `(t,r)=(0,D),(1,D-1)`.

| `(a,b)` | `(d,e)` | `D=t+r` |
|---:|---:|---:|
| `(15,25)` | `(1,11)` | `0` |
| `(16,24)` | `(2,10)` | `9` |
| `(17,23)` | `(3,9)` | `16` |
| `(18,22)` | `(4,8)` | `21` |
| `(19,21)` | `(5,7)` | `24` |
| `(20,20)` | `(6,6)` | `25` |

The formally possible block pair `(14,26)` would require `D=-11` and is
excluded.  Hence the table contains six arithmetic rows and eleven exact
bridge variants.

For a non-bridge vertex of `A`, its row in `H[A,Q]` has size `d`; a bridge
endpoint has size `d+1`.  The analogous row sizes on `B` are `e,e+1`.
Moreover, `H[A,B]` is complete bipartite apart from the missing edge which
corresponds to the possible low bridge.

## The row `(15,25,1,11,0)`

Here `H[Q]` is empty.  If `H[A,Q]` has a 2-matching and `H[B,Q]` has a
12-matching, extend the 13 singleton high colours along those matchings and
pair the 13 residual vertices on each low side across `H[A,B]`.  This is a
26-colouring of `G`.

Otherwise one incidence graph is deficient.  The elementary uniform-row
lemma (Konig duality) says that a bipartite graph with more than `s` left
vertices, all of degree at least `s`, either has an `(s+1)`-matching or all
left rows are one common `s`-set.  On the deficient side all rows are
therefore common.  If the common support is `S`, the low clique on that side
together with `Q-S` has order 27 and is complete in `G`, because `H[Q]` is
empty.  This gives a `K27`.  Thus the first row is terminal.

## Unbridged rows with `d,e>=2`

We give the full parametric argument at `h=13`; it is the equality-boundary
extension of the preceding `h=10,11,12` dichotomy.

If `H[A,Q]` and `H[B,Q]` have matchings of sizes `d+1,e+1`, extend the 13
high colours along them.  Exactly 13 vertices remain on each low side, and
pairing them across `H[A,B]` gives 26 colours.  Hence one side is deficient;
relabel so that every `A`-row is a common `d`-set `S`.  Put `T=Q-S`.  The 27
vertices `A union T` induce a complete graph in `G` except for the target
edges of `H[T]`.

If there is no target, this is `K27`.  If the only target is `uv`, it always
has a path with internal vertices outside `A union T`.  A support vertex
adjacent to both ends in `G` gives `u-s-v`.  Otherwise classify each support
by whether it meets only `u`, only `v`, or both in `H`.

* Opposite one-end types give `u-s_v-s_u-v` if `s_us_v` lies in `G`.  If it
  lies in `H`, both supports have at least 17 neighbours in `G[B]`, by (3),
  and `|B|<=24`; a common such neighbour completes the path.
* If all supports meet one end, say `u`, then `u` has at least two neighbours
  in `G[B]`.  If some support `s` misses `v` in `H`, it has at least 16
  neighbours in `G[B]`, and distinct `b1,b2` give
  `u-b1-b2-s-v`.  If every support meets both ends, choose distinct
  neighbours of `u,v` in `B` and use `u-b1-b2-v`.

The numerical estimates are exactly the boundary values

```text
B-side centre degree >= |B|-(25-(d+1))=2,
support degree in B >= 29-h=16,
two opposite supports each have >=30-h=17 neighbours in B,
2*17>|B|.
```

Suppose now that `H[T]` has two distinct edges.  Treat either edge in turn
as a two-vertex high colour class.  If the contracted incidence graph on the
`B` side has an `e`-matching, attach `d` vertices of `A` to the singleton
classes in `S`, attach `e` vertices of `B` along that matching, and pair the
14 residual vertices on each low side.  The 12 high classes and 14 pairs
give a 26-colouring.

If both contractions fail, the uniform-row lemma makes all contracted
`B`-rows common `(e-1)`-sets.  Equality after contraction on `uv` says that
the symmetric difference of two original equal-sized rows lies in `{u,v}`.
Doing this for a distinct edge leaves an even set of order at most one, so
the original rows are equal.  Write their common support as `R`.  Equation
(3) makes `S,R` disjoint (a common vertex would see all 40 lows in `H`), and

```text
Q = S disjoint-union R disjoint-union {z}.               (5)
```

Use factor-criticality after deleting `s0 in S`.  If `s_M,r_M` are the
numbers of `S,R` endpoints in high--high matching edges, equality of the
residual low sides gives `r_M-s_M=1`.  The vertex `z` has no low neighbour
in `H`, hence is matched within `Q`.  If it is matched into `S`, the balance
forces an edge in `H[R]`; that edge together with any vertex of `B` is a
conformal triangle (after deleting it, match `z` to its `S` neighbour,
attach the other supports to their low sides, and pair the 15 residual lows
on each side).  This is impossible.  Thus `z` has an `H`-neighbour in `R`.
Deleting a vertex of `R` gives symmetrically an `H`-neighbour in `S`.

Put `X=N_H(z) intersect S` and `Y=N_H(z) intersect R`; both are nonempty.
The absence of conformal triangles gives

```text
H[S]=H[R]=H[X,Y]=empty.                                  (6)
```

For example, an edge of `H[S]` forms a triangle with a vertex of `A`; match
`z` to a member of `Y`, attach all other supports, and pair the 15 residual
lows on each side.  An `X-Y` edge forms the same forbidden structure with
`z`.  The other case is symmetric.

If `|X|<=|Y|`, inject `X` into `Y`.  For distinct vertices `a_x in A`, route
every missing branch edge `zx` as

```text
z-a_x-y_x-x.
```

By (5)--(6) these paths lie in `G`, are internally disjoint, and turn
`B union S union {z}` into a `TK27`.  If `|Y|<=|X|`, use the symmetric
construction on `A union R union {z}`.  Every unbridged row is terminal.

## Bridged rows

Let the low bridge be `a0b0`.  Each incidence graph has a matching one above
its ordinary row size.  If the nonendpoint rows do not already supply it,
the uniform-row lemma makes them common and the endpoint's extra neighbour
augments the matching.

Two such matchings give the same 26-colouring unless they attach both bridge
endpoints to the same high vertex; the 13 residual cross-pairs can be chosen
to avoid `a0b0`.  If no compatible pair exists, every maximum matching must
cover its endpoint, and the possible endpoint partners on both sides are the
same singleton `{z}`.  Otherwise choosing two different possible partners
would itself make the matchings compatible.  Applying the uniform-row lemma
to the nonendpoint rows now yields disjoint sets `S,R`, of sizes `d,e`, with

```text
N_H(a,Q)=S                  (a != a0),
N_H(a0,Q)=S union {z},
N_H(b,Q)=R                  (b != b0),
N_H(b0,Q)=R union {z}.
```

They partition `Q`.  An edge of `H[S]`, `H[R]`, `H[z,S]`, or `H[z,R]`
creates an explicit conformal triangle: delete it, attach `z` or the
remaining supports to the appropriate low side, and pair the 14 residual
lows across the complement-complete cut.  Therefore every edge of `H[Q]`
lies between `S,R`.

Now `A union R union {z}` has 27 vertices and induces `K27` in `G` except
for `a0z`.  For any `b1 != b0`, the path

```text
a0-b0-b1-z
```

uses the low bridge, an edge of the clique `B`, and an edge present by the
displayed rows.  It completes a `TK27`.  Thus all bridged rows are terminal,
proving (1).

## Reproduction and trust boundary

Run under CPython 3.9 or later; there are no third-party dependencies:

```sh
python3 verify.py
python3 independent_check.py
```

The primary checker enumerates every large-block forest allowed by the
degree equality, reconstructs all six arithmetic rows and eleven bridge
variants, exhaustively checks the two-contraction row-rigidity statement,
audits every one-target support type, verifies every balance identity, and
decodes representative `TK27` certificates for all ten nondegenerate
variants.  The independent checker reconstructs the block classification
and edge table with a separately organized labelled-forest enumeration and
checks the terminal colour/balance counts.

Both scripts use exact integer, set, tuple, and bit-mask arithmetic, with no
solver, randomness, floating point, generated input, external data, or
project imports.  The prose proof, rather than an enumeration, bridges
arbitrary incidence matrices to the uniform forms.  The mathematical trust
boundary is Sadhu's September 2026 connected-complement frontier, Gallai's
low-vertex block theorem, Stehlik's colouring theorem, Konig's theorem, and
the preceding `h>=13` result.  This note proves the equality-boundary block
classification and all new colouring/subdivision deductions.

The expected certificate digests are

```text
primary:     fef106dc3e87a360fd45d2a07c50733c91294df7891b64ae48b68d5a371c45b9
independent: 65505cc3121ef845287c1f3d39480d27cdcd1eae0d15a1d2ef334326c0d46ba6
```

The primary audit covers 12,300,288 two-contraction row comparisons,
1,402,192 one-target support patterns, 20 matching-balance identities, and
ten explicit nondegenerate terminal templates.

SHA-256 of `verify.py`:
`62352a6edaa7c5ad5e3068f02124e725c13fe85178fd7c140d4dbc4df97fb250`.
SHA-256 of `independent_check.py`:
`0d9f403d061be76ed834999dee39c41e85347d20da0e9676ef5bccb341c2adb6`.

## Sources and novelty scope

* A. Sadhu, [*Albertson's Conjecture Holds for `r` at Most
  26*](https://arxiv.org/abs/2609.01682v1), for the order-53/order-54 frontier
  and the exclusion of a topological `K27` from a counterexample.
* M. Stehlik, [*Critical graphs with connected
  complements*](https://doi.org/10.1016/S0095-8956(03)00069-8), JCTB 89
  (2003), 189--194.
* T. Gallai's low-vertex theorem, stated as Theorem 8 in A. Kostochka's
  [survey](https://kostochk.web.illinois.edu/docs/2008/book06.pdf).
* The preceding [`h>=13` two-clique
  dichotomy](../albertson_r27_order53_h11_h12_closure/README.md).

Targeted searches of the current Albertson and critical-graph literature and
the committed Discovery Net found no prior equality-boundary three-`K14`
classification or `h>=14` consequence.  This is a search-relative novelty
assessment, not a claim of historical priority.
