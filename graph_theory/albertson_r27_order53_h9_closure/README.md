# Coloring/subdivision closure of the Albertson `r=27`, `h=9` frontier

## Result

Let `G` be a hypothetical 27-critical counterexample to Albertson's
conjecture on 53 vertices and 713 edges.  Put

```text
L = {v : d_G(v)=26},       Q = V(G)-L,       h=|Q|.
```

The preceding Gallai-block reduction and the already closed `h=8` boundary
show that `h>=9`.  This note proves that equality is also impossible:

```text
|V(G)|=53, |E(G)|=713  ==>  |Q|>=10.
```

More precisely, every `h=9` graph in the forced Gallai normal forms is
either 26-colorable or contains a subdivision of `K27`.  The alternatives
come with explicit coloring or path-certificate templates.  This materially
narrows the only surviving order/size row, but it does not settle the cases
with at least ten high vertices or Albertson's conjecture for `r=27`.

## The six exact `h=9` profiles

Write `H` for the complement of `G`.  The Gallai argument partitions the 44
low vertices into two clique blocks `A=K_a` and `B=K_b`, where

```text
18 <= a <= b <= 26,        a+b=44.
```

There is at most one additional low edge, a bridge between the two blocks.
Let `t` be 1 when that bridge is present and 0 otherwise, and let
`r=e(H[Q])`, the number of missing edges in `G[Q]`.  The excess cap from the
preceding reduction is

```text
C(a,b) = 26*44-a(a-1)-b(b-1)+9*8-26*9.
```

The total degree excess is 48, so `C(a,b)-48=2(t+r)`.  Exact evaluation
leaves precisely

```text
(a,b,t,r) = (20,24,0,1), (20,24,1,0),
              (21,23,0,4), (21,23,1,3),
              (22,22,0,5), (22,22,1,4).
```

Put

```text
p=a-18,        q=b-18,        p+q=8.
```

If there is no bridge, every row of `H[A,Q]` has size `p` and every row of
`H[B,Q]` has size `q`.  With a bridge `a0b0`, the endpoint rows have sizes
`p+1` and `q+1`, while all other rows retain sizes `p` and `q`.  Also
`H[A,B]` is complete bipartite except for `a0b0` in the bridge case.

## Two elementary matching lemmas

We repeatedly use the following uniform-row consequence of Konig's theorem.

**Uniform-row lemma.**  If a bipartite graph has left part `X`, every left
degree is at least `d`, and `|X|>d`, then either it has a matching of size
`d+1`, or every left degree is exactly `d` and all left neighborhoods are
the same `d`-set.

Indeed, a vertex cover of size at most `d` cannot contain a left vertex:
after using `s>0` left vertices, an uncovered row of degree at least `d`
would have to fit in at most `d-s` right vertices.  Thus a minimum cover is
entirely on the right, and degree forces equality and a common neighborhood.

The second lemma turns missing high-high edges into disjoint subdivision
paths.

**Routing lemma.**  Let `F` be a graph on `S union T`, with `|S|=d` and
`e(F)<=d`.  Every edge `uv` of `F[T]` can be assigned a distinct vertex
`s in S` such that neither `su` nor `sv` is in `F`.

For otherwise Hall gives `k` edges of `F[T]` whose available union has at
most `k-1` vertices of `S`.  Necessarily `k<=d`.  Each of the at least
`d-k+1` other support vertices needs a distinct cross edge to block all
`k` edges.  Together with the `k` edges already in `F[T]`, this gives at
least `d+1` edges of `F`, a contradiction.

When `e(F)=d+1`, the same proof says that a failure with
`k=|E(F[T])|<=d` has a rigid form.  Equality holds throughout: the `k`
edges form a star centered at a vertex `u in T` when `k>=2`, and there are
exactly `d-k+1` blocking cross edges, one from each blocked support vertex
to `u`.  The other `k-1` support vertices are available for all the star
edges.  When `k=1`, each support vertex has exactly one cross edge to either
endpoint of the sole target edge; choosing any blocker orients that edge so
the identical routing below applies.

## Profiles without a low bridge

Suppose first that `t=0`.  If `H[A,Q]` has a matching of size `p+1` and
`H[B,Q]` one of size `q+1`, give the nine vertices of `Q` distinct colors
and extend those colors along the two matchings.  An overlap at a high
vertex gives an independent triple because all `A-B` pairs are complement
edges.  There remain

```text
a-(p+1) = b-(q+1) = 17
```

low vertices on each side.  Pair them across `A-B` and use 17 new colors.
This is a proper 26-coloring.

Otherwise one of the incidence graphs is deficient.  Call its low block
`A`, its size `a`, and its row degree `d=a-18`; the letters can be swapped.
The uniform-row lemma gives a `d`-set `S in Q` with

```text
N_H(x) intersect Q = S        for every x in A.
```

Put `T=Q-S`.  The set `A union T` has order 27 and induces a `K27` except
for the edges of `F[T]`, where `F=H[Q]`.  If `e(F)<=d`, the routing lemma
replaces those missing edges by internally disjoint two-edge paths through
`S`.

The only remaining possibility has `e(F)=d+1`.  If the routing obstruction
uses at most `d` edges of `F[T]`, it is the star described above.  Route
all but one star edge through its `k-1` available support vertices.  When
`k=1` and blockers meet both endpoints, the sole edge `uv` instead has the
path `u-s_v-s_u-v`, where `s_v` is blocked only at `v` and `s_u` only at
`u`.

In every other case all blocking edges meet the common star center `u`.
Choose one blocking support vertex `s0`.  Now `d_F(u)=d+1`, so the
complement-degree cap `Delta(H)<=25` guarantees at least two vertices of the
opposite low block that are `G`-neighbors of `u`, and at least 20 that are
`G`-neighbors of `s0`.  Distinct choices `b1,b2` therefore give the last path

```text
u - b1 - b2 - s0 - v.
```

Here `b1b2` is an edge because the opposite low block is a clique, and
`s0v` is an edge by the rigid equality description.

It remains only when all `d+1` edges of `F` lie in `T`; this can occur in
the `(21,23)` and `(22,22)` profiles.  Merge the endpoints of one edge
`uv` of `F` into one high-vertex color class.  On the opposite block `B`,
contract the two corresponding columns of `H[B,Q]`: a row of original
size `q` has at least `q-1` available color classes: a row containing both
endpoints can use the merged pair, a row containing exactly one loses that
endpoint color, and a row containing neither keeps all `q` singleton
neighbors.  If this contracted incidence graph has a `q`-matching, use it,
match `d` vertices of `A` to the singleton colors in `S`, and pair the 18
residual vertices on each low side.  The eight high color classes plus 18
low pairs again give 26 colors.

Suppose no edge of `F` gives such a matching.  For every edge, the
uniform-row lemma makes all contracted `B`-row neighborhoods the same
`(q-1)`-set.  This forces all original `B`-rows to be one common `q`-set
`R`.  Indeed, if two original rows have the same contracted neighborhoods
for every edge `e`, then away from the two endpoints of `e` their vertex
memberships agree.  Using two distinct edges makes their symmetric
difference have size at most one; equal row sizes make it empty.

If `F[Q-R]` is empty, `B union (Q-R)` induces a `K27`.  Otherwise choose
an edge `xy` of `F[Q-R]`.  In the original branch set `A union T`, route
`xy` as `x-b-y` through any vertex of `B`: the common row `R` omits both
endpoints.  All other `d` edges of `F` route through the `d` vertices of
`S`, since every edge of `F` lies in `T`.  These paths are internally
disjoint.  This closes every unbridged profile.

## Profiles with one low bridge

Now let `t=1`, with bridge `a0b0`.  A matching of size `p+1` in `H[A,Q]`
always exists.  Indeed, either the nonendpoint rows already have such a
matching, or the uniform-row lemma makes them one common `p`-set; the
endpoint row has size `p+1`, so its extra neighbor plus the common set give
the matching.  Similarly `H[B,Q]` has a matching of size `q+1`.

The two matchings give the preceding coloring unless they both attach the
bridge endpoints to the same high vertex.  If both endpoints are residual,
the residual pairing can be permuted to keep them apart.  Suppose no
compatible pair of matchings exists.  Then every maximum matching covers
its bridge endpoint, and all possible endpoint partners on both sides form
one singleton `{q*}`.  Applying the uniform-row lemma to the nonendpoint
rows gives disjoint sets `S_A,S_B` of sizes `p,q` such that

```text
N_H(a,Q)=S_A                 for a != a0,
N_H(a0,Q)=S_A union {q*},
N_H(b,Q)=S_B                 for b != b0,
N_H(b0,Q)=S_B union {q*}.
```

The sets `S_A,S_B` are disjoint because a common vertex would have at least
44 complement neighbors among the low vertices.  Hence
`S_A,S_B,{q*}` partition `Q`.

Use `A union S_B union {q*}` as the 27 branch vertices.  Apart from the
edges of `H[S_B union {q*}]`, its only missing edge is `a0q*`.  In all
three bridge profiles

```text
e(H[Q]) = 0,3,4 <= p = 2,3,4,
```

where the first inequality is interpreted profile by profile.  The routing
lemma assigns all missing high-high edges to distinct internal vertices of
`S_A`.  Finally, any `b1 != b0` gives the internally disjoint path

```text
a0 - b0 - b1 - q*;
```

the last edge is present because only `b0` sees `q*` in the complement.
This is a `TK27`, completing the bridge case and the proof.

## Reproduction and trust boundary

Run with CPython 3.9 or later; there are no third-party dependencies.

```sh
python3 verify.py
python3 independent_check.py
```

The checker derives the six profiles from exact excess arithmetic, enumerates
every labeled high-complement graph for each routing regime, independently
checks Hall matchings and the equality obstruction, and validates every
constructed coloring and topological-clique template.  It also checks the
degree-cap choices in the long star route and the contracted-color escape.
Expected output includes

```text
unbridged high-complement graphs checked: 494874
rigid star TK27 templates checked: 900
all-target contraction cases checked: 1617
contracted row signatures checked: 92385
bridged high-complement graphs checked: 66046
certificate_sha256=83a0fa8716e6b185c6016e0dd832489625b9518c5ac43e8954408267ecf3cce7
```

The independent script uses Hall-subset inequalities instead of augmenting
paths and reproduces all five finite counts.  Its expected digest is
`21658c1d2105f62d79e072ba5756b40c3ddb135bab824307a45e69044d6144da`.

The passage from a deficient incidence matrix to a common row uses Konig's
theorem and is deductive; the script does not enumerate all `44 by 9`
incidence matrices.  The imported mathematical boundary is the published
order-53 frontier and the preceding Gallai normal forms.  The executable
boundary is CPython exact integer, set, and tuple arithmetic.  There is no
solver, randomness, floating point, generated dataset, or external project
import.

## Sources and novelty scope

* A. Sadhu, [*Albertson's Conjecture Holds for `r` at Most
  26*](https://arxiv.org/abs/2609.01682v1), for the order-53 frontier,
  connected complement, and the topological-clique exclusion.
* The preceding [Gallai-block
  reduction](../albertson_r27_gallai_blocks/README.md), for the two-block
  structure and exact excess cap.
* The preceding [`h=8` closure](../albertson_r27_order53_h8_closure/README.md),
  which leaves `h=9` as the next boundary.
* D. Konig's bipartite matching-cover theorem, used in the elementary form
  proved above.

The new contribution is the complete six-profile classification at
`(n,m,h)=(53,713,9)`, the Hall routing certificate, and the
coloring/subdivision closure of every profile.  A targeted search of the
current Albertson and sparse-critical literature and of the committed
Discovery Net found no prior statement of this exact reduction.  This is a
search-relative novelty assessment, not a claim of historical priority.
