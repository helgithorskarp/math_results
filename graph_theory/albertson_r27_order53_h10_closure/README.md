# Coloring-or-subdivision closure of the Albertson `r=27`, `h=10` frontier

This note closes all three incidence profiles left by the preceding `h=10`
structural reduction.  Consequently, conditional on the published order-53
frontier and the preceding `h>=10` result, every hypothetical counterexample
in the sole surviving row

```text
|V(G)|=53,  |E(G)|=713,  chi(G)=27
```

has at least eleven vertices of degree greater than 26.  This does not settle
the `h>=11` cases and therefore does not prove Albertson's conjecture for
chromatic number 27.

## Setting and imported reduction

Let `G` be a hypothetical 27-critical counterexample, let

```text
L={v:d_G(v)=26},  Q=V(G)-L,  h=|Q|,  H=complement(G),  F=H[Q].
```

Stehlik's theorem makes `H` factor-critical: for every vertex `v`, a
26-colouring of `G-v` into pairs is a perfect matching of `H-v`.  Also `H`
has no conformal triangle, meaning a triangle whose deletion leaves a perfect
matching.  Such a triangle and matching would be one independent triple and
25 independent pairs in `G`, hence a 26-colouring.

The preceding reduction proves that when `h=10`, `G[L]` consists of two
cliques `A,B`, possibly with one bridge, and leaves only

```text
(|A|,|B|,bridge,e(F)) = (20,23,0,7),
                         (21,22,0,9),
                         (21,22,1,8).                    (1)
```

In the first profile all rows of `H[A,Q]` are one 3-set and the opposite
incidence graph has matching number at least 7.  In the second, at least one
side has common rows: a 4-set on `A` or a 5-set on `B`.  In the third, if the
bridge is `a0b0`, there is a partition

```text
Q = S disjoint-union R disjoint-union {z},  |S|=4, |R|=5,
```

such that the nonendpoint `A`-rows are `S`, the `a0`-row is `S union {z}`,
the nonendpoint `B`-rows are `R`, and the `b0`-row is `R union {z}`.

We eliminate (1) one row at a time.

## Two reusable finite lemmas

Suppose first that there is no bridge.  Let `C` be a low clique of order
`17+d` whose rows into `Q` are one common `d`-set `S`.  Put `T=Q-S`.
The opposite clique `D` has order `26-d`; each of its complement-incidence
rows into `Q` has size `q=9-d`.

### One-target routing

If `F[T]` has at most one edge, then `C union T` is a `K27` or the branch set
of a `TK27`.  Only the one-edge case needs proof.  Write its edge as `uv`.
A support `s in S` with neither `su` nor `sv` in `F` gives the path `u-s-v`.
Assume no such support exists and classify each support according as it is
joined in `F` to only `u`, only `v`, or both.

If both one-sided types occur, choose `s_u,s_v` of opposite types.  The path
is `u-s_v-s_u-v` if `s_us_v` is in `G`; otherwise insert a common neighbour
of `s_u,s_v` from `D`.  Such a common neighbour exists because every support
has at least `18+d_F(s)` neighbours in `G[D]`, while `|D|>=21`.

If all supports meet, say, `v` in `F`, then `d_F(v)>=d+1`; the high-vertex
degree cap `d_H(v)<=25` gives at least two neighbours of `v` in `G[D]`.
If some support is joined only to `v`, use it at the other end of a path
through two distinct vertices of the clique `D`.  If every support meets both
ends, each of `u,v` has at least two neighbours in `D`, and `u-d_1-d_2-v`
works.  The case with `u,v` exchanged is identical.

### Contraction rigidity

Let `e` be an edge of `F[T]` and merge its ends into one high colour class.
The resulting nine classes are cliques of `H`.  A `D`-row of original size
`q` is compatible with at least `q-1` of them.  If the contracted incidence
graph has a `q`-matching, attach `q` vertices of `D` along it, attach `d`
vertices of `C` to the singleton classes in `S`, and pair the 17 residual
vertices of each low clique across the complete `H[C,D]` cut.  This is a
26-colouring.  Attachments from the two low sides may use the same high
class; the low vertices are adjacent in `H`, so this causes no conflict.

If there is no `q`-matching, Konig's theorem and the uniform-row lemma imply
that all contracted rows are the same `(q-1)`-set.  If this failure occurs
for two distinct edges `e,f` of `F[T]`, all original `D`-rows are one common
`q`-set `R`.  Indeed, two rows with the same `e`-contraction differ only on
the ends of `e`, and similarly their symmetric difference is contained in
`f`.  Distinct edges meet in at most one vertex, while a symmetric difference
of equal-sized sets has even size.  Hence the rows are equal.

Finally `R` is disjoint from `S`: a vertex in their intersection would have
all 43 low vertices as neighbours in `H`, contradicting `d_H<=25` on `Q`.
Since `d+q=9`, the two supports leave one vertex `z` of `Q`.

The verifier exhausts the one-target type patterns and checks the complete
row-signature assertion for every relevant pair of contractions.

## The `(20,23,0,7)` profile

Write the common `A`-row as `S`, with `|S|=3`, and put `T=Q-S`.  If
`e(F[T])<=1`, one-target routing applies.  Otherwise contract two distinct
edges of `F[T]`.  A successful contraction gives a 26-colouring; if both
fail, contraction rigidity makes every `B`-row one common 6-set `R`, and
`R` is a subset of `T`.

Now use `B union (Q-R)` as the 27 branch vertices and `R` as six internal
supports.  For every missing high-high branch edge `xy`, a support `r` is
available when neither `rx` nor `ry` is in `F`.  Hall either assigns all
target edges to distinct supports, or an obstructing set of `k` target edges
blocks at least `7-k` supports.  The `k` targets and at least one blocking
edge at each of those supports already account for all seven edges of `F`.
Thus equality is rigid: the targets form a star (with the usual two-centre
choice when `k=1`), every blocked support has exactly one edge to its centre,
and there are no other complement edges.

Route `k-1` star edges through the available supports.  If blockers occur at
both ends in the `k=1` case, the remaining edge has a three-edge route through
two supports.  Otherwise route it as

```text
centre - c1 - c2 - r0 - leaf
```

through the opposite clique `A`.  The centre has `F`-degree 7 and hence at
least two `G[A]` neighbours; the blocker `r0` already sees all 23 vertices of
`B` in `H` and therefore has at least 19 `G[A]` neighbours.  Distinct
`c1,c2` exist.  The alternative that all seven complement edges are targets
is impossible because `Q-R` has only four vertices.  Hence this profile
always gives a 26-colouring or a `TK27`.

## The `(21,22,0,9)` profile

At least one side has common rows.  Apply the two finite lemmas to that side.
Unless the graph is already 26-colourable or contains a `TK27`, contraction
rigidity forces both incidence matrices to have common rows.  Relabel so that

```text
N_H(a,Q)=S for every a in A,  |S|=4,
N_H(b,Q)=R for every b in B,  |R|=5,
Q=S disjoint-union R disjoint-union {z}.                 (2)
```

We now use factor-criticality.  Fix `s0 in S` and a perfect matching of
`H-s0`.  Let `s_M,r_M` count the endpoints in `S,R` of its high-high edges.
Every unmatched `S` vertex must match into `A`, every unmatched `R` vertex
into `B`, and the residual low vertices match across `H[A,B]`.  Balance gives

```text
r_M-s_M=1.                                               (3)
```

The vertex `z`, which has no low neighbour in `H`, is matched in `F`.  If it
is matched to `S`, equation (3) forces an `R-R` matching edge.  That edge,
together with any vertex of `B`, is a conformal triangle: match `z` to its
`S` partner, the remaining `S` vertices into `A`, the remaining `R` vertices
into `B`, and pair the residual lows.  Therefore, in the absence of a
26-colouring, `F` has a `z-R` edge.  The symmetric argument from a perfect
matching of `H-r0` shows that `F` has a `z-S` edge.

These two edges make every edge inside `S` or inside `R` conformal by the
same explicit matching count.  Hence, if there is still no 26-colouring,

```text
F[S]=F[R]=empty, and every edge of F is in S-R, z-S, or z-R.       (4)
```

Use `B union S union {z}` as branch vertices.  Its only missing edges are
the `z-s` edges of `F`.  Assign each such `s` a distinct `r in R` for which
`rs` is in `G`.  Hall always permits this assignment.  A target `s` has at
most three `F`-neighbours in `R`, because `d_H(s)<=25` and it already has 21
low complement neighbours and the edge `zs`.  For a Hall obstruction on
`k>=2` targets, at least `6-k` vertices of `R` would meet all `k` targets in
`F`, contributing `k(6-k)` cross edges.  Together with all target `z-S`
edges and the already proved `z-R` edge, this exceeds `e(F)=9` for
`k=2,3,4`.  The case `k=1` is excluded by the degree cap.

For the resulting matching, route every missing `zs` as

```text
z - a_s - r_s - s,
```

using distinct internal vertices `a_s in A` and the assigned distinct
`r_s in R`.  All required edges are present by (2), (4), and the assignment.
This is a `TK27`.

## The `(21,22,1,8)` profile

Use the notation `S,R,z,a0,b0` from the imported bridge normal form.  Four
types of high-complement edge immediately give a conformal triangle:

* an edge in `S` forms a triangle with any `a != a0`; after deleting it,
  match `z-a0`, the remaining `S` into `A`, and all of `R` into `B`;
* an edge in `R` is symmetric, using `z-b0`;
* an edge `zs` forms the triangle `{a0,z,s}`;
* an edge `zr` forms the triangle `{b0,z,r}`.

The residual low vertices pair across the complete cut, and the only absent
cut edge has had one endpoint removed in each construction.  Therefore a
non-26-colourable graph has all eight edges of `F` between `S` and `R`.

Then `A union R union {z}` is a 27-vertex branch set with just one missing
edge, `a0z`.  For any `b1 != b0`, route it as

```text
a0 - b0 - b1 - z.
```

The first edge is the low bridge, the second lies in the clique `B`, and the
last is present because every nonendpoint `B`-row is exactly `R`.  Thus this
profile also contains a `TK27`.

## Reproduction and trust boundary

Run with CPython 3.9 or later; there are no third-party dependencies:

```sh
python3 verify.py
python3 independent_check.py
```

`verify.py` checks all profile arithmetic, exhausts every support pattern in
the one-target lemma, every pair of contracted row signatures, every
seven-edge Hall obstruction up to permutation of the six supports, and every
final `S`-to-`R` routing row allowed by the degree and edge budgets.  It also
decodes representative 26-colourings and `TK27` certificates against explicit
graphs.  `independent_check.py` uses direct Hall-subset tests and separately
reconstructs the balance and edge-budget arguments.

Expected primary output includes

```text
two-contraction row signatures: 53835
seven-edge Hall states: 23732 (routed=23674, rigid=58)
final double-uniform routing rows: 11654
certificate_sha256=599c8397dc65ecbbc67572929856eb63a564a95441750dfe624a5184ce17a7e4
```

The independent digest is
`b1db4fa1ba5248f4e4f85cba4fc6c4e65d4e32bb955038956a63159ed389e5d1`.
SHA-256 of `verify.py` is
`06440edd08421f6fcebd72566906a29d1b908f1bae59495120ccea504cfb01ae`;
SHA-256 of `independent_check.py` is
`9026a31ca164c3eb4c7b60aa7f693e7513f1b4eb1e77cd6db8842ae379b85984`.

The executable trust boundary is CPython exact integer, set, tuple, and
bit-mask arithmetic.  There is no solver, randomness, floating point,
generated input, or external package.  The code does not enumerate critical
graphs.  The mathematical trust boundary consists of Sadhu's September 2026
order-53 frontier, Gallai's low-vertex theorem, Stehlik's colouring theorem,
and the preceding `h=10` three-profile reduction.  Everything after (1),
including the factor-critical balance and all colouring/subdivision
certificates, is proved here.

## Sources and novelty scope

* A. Sadhu, [*Albertson's Conjecture Holds for `r` at Most 26*](https://arxiv.org/abs/2609.01682v1),
  for the order-53 frontier, connected complement, and exclusion of a
  topological `K27` from a counterexample.
* M. Stehlik, [*Critical graphs with connected complements*](https://doi.org/10.1016/S0095-8956(03)00069-8),
  JCTB 89 (2003), 189--194.
* The preceding [`h=10` structural reduction](../albertson_r27_order53_h10_reduction/README.md)
  and [`h=9` closure](../albertson_r27_order53_h9_closure/README.md).

Targeted searches of the current Albertson and critical-graph literature and
of the committed Discovery Net found no prior version of this exact `h=10`
closure.  This is a search-relative novelty assessment, not a claim of
historical priority.
