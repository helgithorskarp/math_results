# Matching-or-subdivision closure of the last order-53 `h=8` profile

## Result

Let `G` be a hypothetical 27-critical counterexample to Albertson's
conjecture on 53 vertices, and put

```text
L = {v : d_G(v)=26},       Q = V(G)-L,       h=|Q|.
```

The preceding Gallai-block and boundary-certificate reductions left one
possibility with `h=8`: at `|E(G)|=713`, the low graph is the disjoint union
of cliques `A=K22` and `B=K23`, while `G[Q]=K8-e`.  This profile is
impossible.  More precisely, every graph with this displayed structure and
the forced low degrees is either 26-colorable or contains a subdivision of
`K27`.

Consequently, all three surviving order-53 edge rows now satisfy

```text
|E(G)| in {713,714,715}  ==>  |Q| >= 9.
```

A concurrent recursive-sampling theorem independently eliminates the
714- and 715-edge rows.  Combining it with the result here and the earlier
order-54 closure, every remaining counterexample must therefore satisfy

```text
|V(G)|=53,  |E(G)|=713,  |Q|>=9,
```

and have connected complement.  This is a structural narrowing, not a proof
of the full `r=27` case.

## Abstract matching dichotomy

Write `H` for the complement of `G`.  The exact profile gives

```text
G[A]=K22,  G[B]=K23,  E_G(A,B)=empty,
G[Q]=K8-q0q1,
d_H(a,Q)=3 for every a in A,
d_H(b,Q)=4 for every b in B.
```

We use the following elementary consequence of König's matching-cover
theorem.  Let `F` be bipartite with left side `X`, suppose every vertex of
`X` has degree `d`, and suppose `|X|>=d+1`.  Then either `F` has a matching
of size `d+1`, or all vertices of `X` have the same `d`-element
neighborhood.

Indeed, if the matching number is at most `d`, a minimum vertex cover `C`
has size at most `d`.  If `C` contains `s>0` left vertices, some left vertex
lies outside `C`, and all of its `d` neighbors must lie among the at most
`d-s` right vertices of `C`, a contradiction.  Thus `C` lies entirely on
the right.  Since it contains every degree-`d` neighborhood and has size at
most `d`, all those neighborhoods equal `C`.

Apply the lemma to `H[A,Q]` with `d=3` and to `H[B,Q]` with `d=4`.

### If both large matchings exist: a 26-coloring

Suppose `H[A,Q]` has a matching `M_A` of size 4 and `H[B,Q]` has a matching
`M_B` of size 5.  Give the eight vertices of `Q` eight distinct colors.  For
each edge `aq` of `M_A`, give `a` the color of `q`; do the same for each edge
`bq` of `M_B`.  If both matchings use the same `q`, then `{a,b,q}` is an
independent color class: `aq,bq` are complement edges and there are no
`G`-edges from `A` to `B`.

There remain 18 uncolored vertices in each of `A` and `B`.  Pair them
arbitrarily across the empty `A`--`B` cut and give the 18 pairs new colors.
This is a proper coloring with `8+18=26` colors.

### If either matching is deficient: a topological `K27`

Suppose first that `H[A,Q]` has no matching of size 4.  The lemma gives a
3-set `S` in `Q` such that `N_H(a) intersect Q=S` for every `a` in `A`.
Put `T=Q-S`, so `|T|=5`.  All edges from `A` to `T` are present in `G`.
Thus `A union T` induces `K27`, unless both endpoints `q0,q1` of the sole
missing edge of `G[Q]` lie in `T`.  In that exceptional case choose any
`s in S` and replace the missing branch edge by

```text
q0 - s - q1.
```

Both path edges are present because `G[Q]=K8-q0q1`, and the internal vertex
`s` is outside the branch set.  This is a subdivision of `K27`.

If instead `H[B,Q]` has no matching of size 5, all `B`-rows have one common
4-set `S`.  Its complement `T` has size 4, and the identical construction
uses branch set `B union T`, again of order 27.  The only possible missing
branch edge is routed through any vertex of the nonempty set `S`.

This exhausts all cases and proves the dichotomy.

## Reproduction

Run with CPython 3.9 or later; there are no third-party dependencies.

```sh
python3 verify.py
```

The checker enumerates every normalized overlap pattern for the two coloring
matchings and every common-neighborhood/missing-edge position in both
subdivision branches.  It validates proper color classes and complete
topological-clique certificates directly.  It also checks the exact frontier
degree arithmetic and the finite cover-capacity implications used in the
uniform-neighborhood lemma.

The structural passage from a deficient matching to a vertex cover uses
Konig's theorem and is deductive; the script does not enumerate all `22 by 8`
or `23 by 8` incidence matrices.  The executable trust boundary is CPython
integer and set arithmetic.  There is no solver, randomness, floating point,
generated data, or external project import.

## Sources and novelty scope

* A. Sadhu, [*Albertson's Conjecture Holds for `r` at Most
  26*](https://arxiv.org/abs/2609.01682v1), for the two-order frontier and
  the reduction of a counterexample to a 27-critical graph with connected
  complement.
* The preceding [Gallai-block
  reduction](../albertson_r27_gallai_blocks/README.md), for the three lower
  bounds on `h` and the exact `h=8` profiles.
* The preceding [boundary-certificate
  reduction](../albertson_r27_gallai_boundary_certificates/README.md), which
  closes the `m=714` profile and the bridged `m=713` profile, leaving exactly
  the profile treated here.
* The concurrent [recursive convex-sampling
  theorem](../albertson_r27_recursive_convex_sampling/README.md), which
  independently eliminates the 714- and 715-edge rows and leaves only the
  713-edge row treated structurally here.
* Discovery Net review
  `bafkreicr7cvjrlka2k7w3yipplr2nxmce37p4wodp66immde3d5pfekfda`, which
  independently verifies that preceding reduction, records the general
  uniform-row consequence of König duality, and explicitly identifies this
  unbridged profile as the highest-value next case.  It does not close it.
* D. König's bipartite matching-cover theorem, used only in the elementary
  form proved above.

The new contribution is the matching-or-uniformity dichotomy and its explicit
coloring/topological-clique certificates for the last `h=8` profile.  A
targeted search of the current Albertson and sparse-critical literature and
of the committed Discovery Net found no prior statement of this exact
closure.  This is a search-relative novelty assessment, not a claim of
historical priority.
