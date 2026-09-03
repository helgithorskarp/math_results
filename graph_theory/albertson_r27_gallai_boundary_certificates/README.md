# Coloring/subdivision certificates for two Albertson `r=27` Gallai boundary profiles

This note closes two minimum-high-vertex profiles supplied by
the Gallai-block reduction for the remaining order-53 Albertson frontier.  It
does **not** prove Albertson's conjecture for chromatic number 27.

## Result

Let `G` be a 27-critical graph on 53 vertices, let

```text
L = {v : d_G(v)=26},       Q = V(G)-L,
```

and suppose that the complement of `G` is connected.  The preceding
Gallai-block theorem gives the following normal forms when `|Q|=8`.

1. If `|E(G)|=714`, then `G[L]` is the disjoint union of `K22` and
   `K23`, while `G[Q]=K8`.  This profile is always 26-colorable and hence
   cannot occur.
2. If `|E(G)|=713`, `G[L]` consists of `K22` and `K23` joined by one
   bridge, and `G[Q]=K8`, then either `G` is 26-colorable or it contains a
   subdivision of `K27`.  Thus this profile also cannot be an Albertson
   counterexample.

Consequently a hypothetical counterexample satisfies

```text
m=714  ==>  |Q| >= 9,
```

and, at `(m,|Q|)=(713,8)`, only the other Gallai profile remains: there is
no bridge between the low cliques and `G[Q]` is `K8` minus one edge.

The proof gives an independently checkable terminal certificate in every
case: either an explicit 26-coloring or a `TK27` branch/path witness.

## Complement setup

Write `H` for the complement of `G`, and let the two low cliques be `A`
and `B`, of orders 22 and 23.  At order `2k-1`, Stehlik's coloring theorem
implies that `H-v` has a perfect matching for every vertex `v`; thus `H` is
factor-critical.

In the bridge profile denote the bridge by `a0 b0`.  Degree 26 at every low
vertex gives

```text
d_H(a,Q)=3  for a in A-a0,       d_H(a0,Q)=4,
d_H(b,Q)=4  for b in B-b0,       d_H(b0,Q)=5.
```

There are no edges of `H` inside `A`, `B`, or `Q`, and `H[A,B]` is complete
bipartite except for `a0 b0`.

In the 714-edge profile there is no bridge, so every `A`-row has complement
degree 3 into `Q`, every `B`-row has complement degree 4 into `Q`, and
`H[A,B]` is complete bipartite.

## The two required matchings

Factor-criticality supplies precisely the small matchings needed for a
coloring.  Delete any vertex of `B` and consider a perfect matching of the
remaining graph.  If `x,y,z` count its `A-Q`, `B-Q`, and `A-B` edges, then

```text
x+y=8,       x+z=22,       y+z=22,
```

so `x=y=4`.  In particular `H[A,Q]` has a matching of size 4.  Similarly,
after deleting a vertex of `A`, the part sizes give

```text
x+y=8,       x+z=21,       y+z=23,
```

and hence `x=3,y=5`; therefore `H[B,Q]` has a matching of size 5.

Choose such matchings `M_A` and `M_B`.  Give the eight vertices of `Q`
eight distinct colors.  For every edge `aq` of `M_A`, give `a` the color
of `q`; do the analogous thing for `M_B`.  There remain 18 uncolored
vertices in each of `A` and `B`.  Pair them and give the 18 pairs 18 new
colors.  This uses 26 colors.

When there is no low bridge, every such pairing is valid, even when the two
small matchings use the same `q`: the resulting color class `{a,b,q}` is
independent.  This proves the first assertion.

In the bridge profile the construction fails only if `M_A` matches `a0` to
some `q` and `M_B` matches `b0` to that same `q`.  If both bridge endpoints
remain among the 18 residual vertices, simply permute their pairing; there
are 18 pairs, so they need not receive the same color.

## The unique obstruction to compatible matchings

Assume now that **no** choice of a size-4 matching in `H[A,Q]` and a size-5
matching in `H[B,Q]` is compatible.  Then every size-4 matching covers
`a0`, every size-5 matching covers `b0`, and the possible partners of both
endpoints must be the same singleton, say `{q*}`.  Otherwise two matchings
with distinct endpoint partners would be compatible.

It follows that

```text
nu(H[A-a0,Q]) <= 3,       nu(H[B-b0,Q]) <= 4.
```

König's theorem now makes the incidence matrices rigid.  We use the
following elementary consequence.  If a bipartite graph has at least
`d+1` vertices on its left, every left degree is exactly `d`, and its
matching number is at most `d`, then all left vertices have the same
`d`-element neighborhood.  Indeed, a vertex cover of size at most `d`
cannot contain a left vertex: if it contained `s>0`, an uncovered left
vertex would have its `d` neighbors in at most `d-s<d` right vertices.
Thus a minimum cover consists of `d` right vertices, and equality of the
left degrees forces the claim.

Apply this with `d=3` and `d=4`.  There are sets `S_A,S_B` in `Q`, of
orders 3 and 4, such that

```text
N_H(a) intersect Q = S_A             for a in A-a0,
N_H(a0) intersect Q = S_A union {q*},

N_H(b) intersect Q = S_B             for b in B-b0,
N_H(b0) intersect Q = S_B union {q*}.
```

The endpoint formulas follow because an endpoint needs a neighbor outside
the common set to raise the matching number, and every such outside neighbor
can be its partner in a maximum matching.  The partner was assumed unique.

The sets `S_A` and `S_B` are disjoint.  Otherwise a vertex in their
intersection would have at least `21+22=43` neighbors in `H`, whereas every
high vertex has `d_H(q)<=25` because `d_G(q)>=27`.  Also `q*` lies outside
both sets.  Since `3+4+1=8`, these three sets partition `Q`.

## The terminal `TK27` certificate

In the rigid case take

```text
A union S_B union {q*}
```

as the 27 branch vertices.  They induce a `K27` with only the edge
`a0 q*` missing.  Choose any `s` in `S_A` and route that edge by

```text
a0 - b0 - s - q*.
```

Both internal vertices lie outside the branch set.  The first edge is the
unique low bridge; `b0s` is present because `s` is outside
`S_B union {q*}`; and `sq*` is present because `G[Q]=K8`.  This is a
subdivision of `K27`, completing the dichotomy.

## Reproduction

Run with CPython 3.9 or later:

```sh
python3 verify.py
```

Expected output ends with

```text
labelled rigid TK27 certificates checked: 280
rigid_certificate_sha256=66ddfd8f90a79b3eb7b04534d0fa55df97652990e6c859571410e24da3dfebde
conclusion: (714,h=8) and the bridged (713,h=8) profile are closed
```

The dependency-free verifier exhausts all endpoint-compatibility cases for
the two matching certificates, checks every produced 26-coloring against all
adjacency facts used by the construction, checks the König-cover
arithmetic, and constructs and verifies all 280 labelled rigid partitions
`(S_A,S_B,{q*})` and their topological-`K27` paths.  It also checks the exact
orders, sizes, low degrees, high-degree condition, and connected complement
of every rigid graph.

The structural bridge from arbitrary incidence matrices to the matching
dichotomy is the displayed deductive proof; the script does not enumerate
all `45 by 8` matrices.  Its executable trust boundary is CPython integer and
set arithmetic.  It uses no solver, randomness, floating point, generated
data, or external project code.

## Sources and novelty scope

* A. Sadhu, [*Albertson's Conjecture Holds for `r` at Most
  26*](https://arxiv.org/abs/2609.01682v1), for the surviving order-53 rows,
  connected complement, and exclusion of a `TK27` from a counterexample.
* M. Stehlik, [*Critical graphs with connected
  complements*](https://doi.org/10.1016/S0095-8956(03)00069-8), JCTB 89
  (2003), 189--194, for the factor-critical complement consequence.
* The preceding [Gallai-block
  reduction](../albertson_r27_gallai_blocks/README.md), for the two boundary
  profiles and their exact incidence row sums.
* The earlier [Kempe-state certificate
  note](../albertson_r27_kempe_states/README.md), for the same
  coloring-or-`TK27` terminal-certificate semantics.

König's matching-cover theorem is classical.  The contribution is the exact
matching compatibility dichotomy, its rigid polarized obstruction, and the
one-path `TK27` certificate specialized to these two Gallai boundary
profiles.  Targeted searches of the current Albertson and sparse-critical
literature and of the committed Discovery Net found no prior statement of
this reduction.  This is a search-relative assessment, not a claim of
historical priority.
