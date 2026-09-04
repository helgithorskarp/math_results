# Two-clique persistence and a three-profile reduction at the Albertson `r=27` frontier

This note advances the sole surviving Albertson frontier row

```text
|V(G)|=53,  |E(G)|=713,  chi(G)=27.
```

It proves that the Gallai two-clique structure persists when the number `h`
of high vertices is `10`, `11`, or `12`, and combines that structure with a
reusable matching/routing dichotomy.  At `h=10`, three of the six exact
block/bridge profiles are impossible.  The remaining three receive stronger
incidence normal forms.  This is a structural reduction, not a proof of the
`h=10` case or of Albertson's conjecture for chromatic number 27.

## Setting and result

Let `G` be a hypothetical 27-critical counterexample on 53 vertices and 713
edges.  Put

```text
L={v:d_G(v)=26},   Q=V(G)-L,   h=|Q|,   H=complement(G).
```

The total degree excess is

```text
sum_v (d_G(v)-26) = 2*713-26*53 = 48.                 (1)
```

The preceding `h=8` and `h=9` closures imply `h>=10`.  The structural part
below does not use those closures: it classifies any one of the conditional
cases `h=10,11,12` directly from Gallai's low-vertex theorem and Stehlik's
colouring theorem.

For each `10<=h<=12`, `G[L]` consists of two vertex-disjoint clique blocks
`A=K_a` and `B=K_b`, together with at most one bridge between them.  There
are no other low-low edges.  Let

```text
t = number of A-B bridges (0 or 1),
r = e(H[Q]),
p = a+h-27,
q = b+h-27.
```

Thus `p+q=h-1`.  A non-bridge-endpoint row of `H[A,Q]` has size `p`, and one
of `H[B,Q]` has size `q`; a bridge endpoint has row size one larger.  Exact
use of (1) leaves the following table.  Each line represents the two profiles
`(t,r)=(0,D)` and `(1,D-1)`.

| `h` | `(a,b)` | `(p,q)` | `D=t+r` |
|---:|---:|---:|---:|
| 10 | (19,24) | (2,7) | 3 |
| 10 | (20,23) | (3,6) | 7 |
| 10 | (21,22) | (4,5) | 9 |
| 11 | (18,24) | (2,8) | 5 |
| 11 | (19,23) | (3,7) | 10 |
| 11 | (20,22) | (4,6) | 13 |
| 11 | (21,21) | (5,5) | 14 |
| 12 | (17,24) | (2,9) | 7 |
| 12 | (18,23) | (3,8) | 13 |
| 12 | (19,22) | (4,7) | 17 |
| 12 | (20,21) | (5,6) | 19 |

The matching/routing lemma proved below eliminates five of these exact
profiles:

```text
(h,a,b,t,r) = (10,19,24,0,3), (10,19,24,1,2),
                (10,20,23,1,6),
                (11,18,24,1,4),
                (12,17,24,1,6).                         (2)
```

In particular, if `h=10`, only

```text
(a,b,t,r) = (20,23,0,7), (21,22,0,9), (21,22,1,8)       (3)
```

can remain.  They satisfy the following additional necessary conditions.

* In `(20,23,0,7)`, all rows of `H[A,Q]` are one common 3-set, while
  `H[B,Q]` has a matching of size at least 7.
* In `(21,22,0,9)`, all rows on at least one side are common: either every
  `H[A,Q]` row is one 4-set or every `H[B,Q]` row is one 5-set.
* In `(21,22,1,8)`, write the bridge as `a0b0`.  There are disjoint sets
  `S_A,S_B` and a vertex `q*` partitioning `Q`, with sizes 4, 5, and 1,
  such that

  ```text
  N_H(a,Q)=S_A                 for a in A-{a0},
  N_H(a0,Q)=S_A union {q*},
  N_H(b,Q)=S_B                 for b in B-{b0},
  N_H(b0,Q)=S_B union {q*}.
  ```

These forms compress all low-to-high incidence matrices in the `h=10`
boundary to three structural families.

## Persistence of the two low cliques

Fix a low vertex `v`.  Stehlik's theorem supplies a 26-colouring of `G-v`
whose classes all have at least two vertices.  Since `|G-v|=52`, all 26
classes are pairs.  Vertex `v` has one neighbour in each class.  At least
`26-h` pair classes are fully low.

The rooted Kempe argument is short.  For two fully-low classes
`{y_i,x_i}` and `{y_j,x_j}`, where `y_i,y_j` are the neighbours of `v`,
the two distinguished vertices lie in one bichromatic component; otherwise
a Kempe swap frees a colour at `v`.  If `y_i y_j` is an edge, the two edges
from `v` lie in one clique block of `G[L]`.  If it is not an edge,
bichromatic connectivity forces the induced cycle

```text
v-y_i-x_j-x_i-y_j-v,
```

so those edges lie in one `C5` block.  Edges in different blocks through
`v` cannot participate in such a cycle.  Hence all fully-low classes use
one block through `v`; when there are at least three classes this block must
be a clique.  Every low vertex therefore lies in a clique block of order at
least

```text
s=27-h.                                                   (4)
```

For `10<=h<=12`, one has

```text
2(s-1)>26,        |L|=53-h>26,        3s>|L|.
```

No low vertex can lie in two of the large clique blocks, since its internal
degree would exceed 26.  No block has order 27, since that would itself be a
`K27`.  Thus the large blocks are disjoint, at least two are needed to cover
`L`, and three do not fit.  Exactly two blocks `A,B` partition `L`.

Any further block meets each of `A,B` in at most one vertex.  Since they
already cover `L`, the only possible further block is a bridge joining the
two cliques; two such bridges would lie on a common cycle and merge the
blocks.  Hence there is at most one.

For fixed `a+b=53-h`, the excess identity gives

```text
48 = 26(53-h)-a(a-1)-b(b-1)+h(h-1)-26h-2(t+r).          (5)
```

The table follows by exact integer evaluation of (4) and (5).

## Matching and routing lemmas

We use two elementary facts.

**Uniform-row lemma.**  Let a bipartite graph have left part `X`, with
`|X|>d`, and let every left degree be at least `d`.  Either it has a matching
of size `d+1`, or every left row has degree exactly `d` and all rows have one
common `d`-element neighbourhood.

Indeed, a Konig vertex cover of size at most `d` cannot contain a left
vertex: after using `s>0` left vertices, any uncovered left row of degree at
least `d` would have to fit among at most `d-s` right cover vertices.

**Boundary routing lemma.**  Suppose `t=0` and every row of `H[A,Q]` is a
common set `S` of size `d=p>=2`.  Put `T=Q-S` and `F=H[Q]`.  If
`e(F)<=d+1`, then `G` is 26-colourable or contains a subdivision of `K27`.

To prove this, first take `e(F)<=d`.  For each target edge `uv` of `F[T]`,
let its available internal vertices be the `s in S` for which neither `su`
nor `sv` lies in `F`.  If `k` target edges violate Hall, at least `d-k+1`
support vertices are blocked from every one of them.  Each blocked support
has an `F`-neighbourhood that covers those `k` target edges.  Counting the
targets and at least one blocking cross edge per blocked support gives at
least `d+1` edges of `F`, a contradiction.  The assignment routes every
missing branch edge through a distinct support vertex, so `A union T` is the
branch set of a `TK27`.

Now let `e(F)=d+1`.  Equality in the preceding Hall count is rigid unless
all `d+1` edges of `F` are targets in `T`: the obstructing target edges form
a star, and each blocked support has exactly one cross edge, to the star
centre.  Route all but one star edge through the free supports.  If the sole
target has blockers at both endpoints, it has a three-edge route through two
support vertices.  Otherwise, leave target `uv`, with centre `u` and a
blocked support `s0`, for the path

```text
u-b1-b2-s0-v
```

through two vertices of the opposite clique `B`.  Since high vertices of
`H` have degree at most 25, the centre has at least

```text
b-(25-(d+1))=b+d-24=2
```

neighbours in `G` inside `B`.  The blocker has all `a` vertices of `A` and
the centre as neighbours in `H`, so it has at least

```text
b-(24-a)=29-h>=17
```

neighbours in `G` inside `B`.  Distinct `b1,b2` therefore exist.

It remains when all `d+1` edges of `F` lie in `T`.  Put `q=b+h-27`, so
`|T|=q+1`.  Contract one edge of `F` to a two-vertex high colour class.  If
the resulting incidence graph from `B` to the `h-1` high classes has a
`q`-matching, attach `d` vertices of `A` to the singleton classes in `S`,
attach `q` vertices of `B` along the matching, and pair the remaining
`27-h` vertices on each low side.  This is a 26-colouring.

If no contracted edge permits such a matching, the uniform-row lemma makes
the contracted `B`-rows common for every edge of `F`.  Two distinct
contractions show that the original rows themselves are one common `q`-set
`R`: the symmetric difference of two rows is contained in each contracted
edge and has even size.  If `F[Q-R]` is empty, `B union (Q-R)` is a `K27`.
Otherwise route one edge of `F[Q-R]` through a vertex of `B`, and route the
other `d` target edges through the `d` vertices of `S`.  This again gives a
`TK27` and proves the lemma.

Consequently, an unbridged profile is impossible whenever

```text
r <= min(p,q)+1.                                         (6)
```

If the two incidence graphs have matchings of sizes `p+1,q+1`, nine or more
distinct high colours are extended and the residual low vertices are paired
across the complement-complete `A-B` cut, giving 26 colours.  Otherwise the
uniform-row lemma applies on a deficient side, and (6) invokes boundary
routing there.

## One-bridge lemma

Suppose the bridge is `a0b0`.  The nonendpoint rows on the two sides have
sizes `p,q`, while the endpoint rows have sizes `p+1,q+1`.  Each incidence
graph has a matching of size one above its ordinary row degree.  For example,
either the nonendpoint `A`-rows already have a `(p+1)`-matching, or the
uniform-row lemma makes them one common `p`-set; the extra endpoint neighbour
then augments a `p`-matching.

If the two matchings can be chosen without attaching both bridge endpoints
to the same high vertex, they extend the singleton colours of `Q`; residual
vertices pair across the `A-B` cut, avoiding the bridge if both endpoints are
residual.  This is a 26-colouring.

Otherwise every maximum matching covers its bridge endpoint, on both sides,
and both endpoints have one forced common partner `q*`.  Applying the
uniform-row lemma to the nonendpoint rows gives disjoint common sets
`S_A,S_B` of sizes `p,q`, with endpoint rows `S_A union {q*}` and
`S_B union {q*}`.  The sets are disjoint because a common member would have
at least `a+b>=41` low neighbours in `H`, contradicting the high-vertex
degree cap 25.  Since `p+q=h-1`, they and `q*` partition `Q`.

Choose the larger of `S_A,S_B` as internal support and the corresponding low
clique as branch vertices.  When

```text
r <= max(p,q),                                           (7)
```

the ordinary routing argument assigns all missing high-high branch edges to
distinct support vertices.  The sole missing endpoint/high edge has the
internally disjoint path, or its symmetric version,

```text
a0-b0-b1-q*.
```

Thus a bridged profile satisfying (7) is also impossible.  Conditions (6)
and (7), applied to the exact table, give (2) and the three survivors (3).
The matching restrictions following (3) are just the alternatives in the
same proof.

## Reproduction and trust boundary

Run with CPython 3.9 or later; there are no third-party dependencies:

```sh
python3 verify.py
```

The verifier independently reconstructs every `h=10,11,12` arithmetic
profile, applies the two closure thresholds, and exhausts all 14,190
three-edge high-complement graphs in the load-bearing `d=2` boundary-routing
case.  It checks Hall assignments and the rigid-star/all-target split using
exact set and integer arithmetic.  The executable check does not enumerate
critical graphs or replace Gallai's, Stehlik's, or Konig's theorems.

The mathematical trust boundary consists of Sadhu's September 2026
order-53 frontier, the classical Gallai low-vertex block theorem, Stehlik's
all-classes-size-at-least-two colouring theorem, and the previously published
`h>=10` closure.  The two-clique persistence proof, exact profiles, and
matching/routing deductions are deductive.

## Sources and novelty scope

* A. Sadhu, [*Albertson's Conjecture Holds for `r` at Most 26*](https://arxiv.org/abs/2609.01682v1),
  for the order-53 frontier, connected complement, and exclusion of a
  topological `K27` from a counterexample.
* M. Stehlik, [*Critical graphs with connected complements*](https://doi.org/10.1016/S0095-8956(03)00069-8),
  JCTB 89 (2003), 189--194.
* T. Gallai's low-vertex theorem, reproduced as Theorem 8 in A. Kostochka's
  [survey](https://kostochk.web.illinois.edu/docs/2008/book06.pdf).
* The preceding [Gallai-block reduction](../albertson_r27_gallai_blocks/README.md)
  and [`h=9` closure](../albertson_r27_order53_h9_closure/README.md).

The new content is the persistence and exact profile classification through
`h=12`, the boundary routing lemma at one edge beyond the basic Hall bound,
and its application eliminating five profiles and reducing `h=10` to three
incidence families.  Targeted primary-literature and committed-graph searches
through indexed height 1832 found no prior statement of this extension or
three-profile reduction.  This is a search-relative assessment, not a claim
of historical priority.
