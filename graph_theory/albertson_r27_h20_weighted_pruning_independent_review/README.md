# Independent review of the Albertson `r=27`, `h=20` five-case reduction

## Target, verdict, and exact scope

Target: Discovery Net contribution
`bafkreiaf6feukmiwlfnvqgjfg4ihi6czm6qlsidw2qnqsnivrvpkrevb6a`,
“Weighted-incidence pruning reduces the Albertson `r=27`, `h=20` boundary to
five cases.”

**Verdict: accept as a rigorous conditional reduction, with high confidence
in the new `h=20` argument.** Assuming the target's imported order-53,
713-edge frontier, `h>=20`, rooted Gallai-block lemma, factor-criticality, and
previously reviewed two-clique terminal kernel, every `h=20` counterexample is
reduced to the stated D20 and D19 forms and five possible values of
`chi(G[Q])`.

I independently reconstructed the block-count and connector bounds, every
finite block signature, the list-colouring reduction to an isolated largest
clique, the active-class implication, all weighted degree minima, and the
`h=20` numerical slack in the two-clique kernel. I also checked the two target
programs and their provenance. This review does not reprove the earlier
campaign chain establishing the imported 713-edge row and `h>=20`.

The result is a classification of necessary cases, not an existence theorem.
It does not itself exclude `h=20` or prove Albertson's conjecture at `r=27`.
The separately committed height-1933 split-colour lemma, independently
reviewed at height 1937, eliminates the five cases after this reduction.

## Mathematical audit

Let `L={v:d_G(v)=26}`, `Q=V(G)-L`, and assume `|Q|=20`. Then `|L|=33`,
and the reviewed rooted Gallai lemma puts every vertex of `L` in a clique
block of order at least `27-20=7`. Summing degrees over `L` gives

```text
e(L,Q)=26*33-2e(G[L]),
e(G[Q])=e(G[L])-145,
e(G[L])>=145.                                            (1)
```

The last inequality uses `e(G[Q])>=0`.

### Block-cut and connector bounds

Call the guaranteed clique blocks large. If there are `b` large blocks and
their induced block-cut forest has `c` components, put `q=b-c`. Because every
low vertex belongs to a large block, counting repeated cut vertices gives

```text
sum_i |B_i|=33+q.                                        (2)
```

A block outside the large family meets each direct component in at most one
vertex, or the block-cut graph would contain a cycle. Such connector blocks
form a hyperforest on the `c` components. If their orders are `k_i`, then
`sum_i(k_i-1)<=c-1`; merging connectors and convexity give

```text
sum_i binom(k_i,2) <= binom(c,2).                        (3)
```

The relevant connectors have order at most four and hence cannot be odd
cycles of order at least five; Gallai's theorem therefore makes them cliques.

Six large blocks would use at least `6*7-5=37` vertices, so at most five
exist. Direct enumeration of (2)--(3) gives the following sharp upper bounds
on `e(G[L])`:

```text
five blocks: q=2,3,4 -> 108,113,120;
four blocks: q=0,1,2,3 -> 135,144,155,168.
```

All five-block cases and the first two four-block cases contradict (1). The
remaining four-block cases give exactly 19 edge-budget rows. Since any
`c`-chromatic graph has at least `binom(c,2)` edges, (1) bounds
`chi(G[Q])`; in all 19 rows

```text
max_i |B_i| + chi(G[Q]) <= 22.
```

Connector cliques are smaller than the large blocks, so the chromatic number
of the Gallai block graph `G[L]` is its largest block order. Disjoint palettes
therefore colour all four-block forms. Only two or three large blocks remain.

### Two large blocks

If two large blocks met, (2) would make their order sum 34, but their common
cut vertex would have 32 low neighbours, contradicting degree 26. Hence they
are disjoint cliques `C=K_a,D=K_b`, with `a+b=33`, joined by at most one
bridge. Write

```text
a=7+p, b=7+q, p+q=19.
```

An ordinary row in the complement incidence graphs `H[C,Q]` and `H[D,Q]`
has size `p` and `q`, respectively; a bridge endpoint has one extra neighbour.
Fresh degree and edge accounting yields exactly

```text
(a,b,p,q,t+e(H[Q])) =
(8,25,1,18,7), (9,24,2,17,23), (10,23,3,16,37),
(11,22,4,15,49), (12,21,5,14,59), (13,20,6,13,67),
(14,19,7,12,73), (15,18,8,11,77), (16,17,9,10,79).
```

The uniform-row lemma used by the target is valid: if more than `r` left
vertices have row size at least `r`, then either an `(r+1)`-matching exists or
all rows equal one common `r`-set. A Konig cover of order at most `r` cannot
contain a left vertex, so it must be precisely that common right support.

In the unbridged case, simultaneous matchings of sizes `p+1,q+1` attach low
vertices to the 20 singleton high colours and leave six vertices on each low
side to pair across the complement-complete cut. If one side is deficient,
its rows have a common support `S` of size `p`; putting `T=Q-S`, the 27
vertices `C union T` form a clique except for the target edges of `H[T]`.

I rechecked the three terminal alternatives at the new boundary.

* With no target edge there is a `K27`.
* With one target edge, the worst graph-neighbour floors in the opposite
  clique are 2 for a target endpoint, 9 for a one-end support, and 10 for an
  opposite-type support. These bounds supply the one- or two-clique-vertex
  replacement path in every support-type case; no common-neighbour
  pigeonhole is needed. The `p=1` endpoint is handled inside the opposite
  `K25`.
* With two distinct target edges, a successful `q`-matching after either
  contraction produces 19 high colour classes and seven residual low pairs.
  If both fail, equality of the contracted rows confines every symmetric
  difference of original equal-size rows to the intersection of two distinct
  target pairs. That intersection has size at most one, while a symmetric
  difference has even size, so the opposite rows share a common support `R`.
  The complement-degree cap makes `S` and `R` disjoint, and
  `Q=S disjoint-union R disjoint-union {z}`. The previously reviewed
  factor-critical/conformal-triangle kernel then supplies the topological
  `K27`; its injections remain within the low cliques because their orders
  are `p+7,q+7`.

With a bridge, the endpoint's extra incidence augments a deficient uniform
row family, so both one-larger matchings exist. Compatible choices yield the
same colouring, and the six residual cross-pairs can avoid one forbidden
bridge pair. Incompatible choices force the common supports and unique `z`
configuration; the missing branch edge has the path through the bridge and a
second vertex of the opposite clique. The target's two-block elimination thus
retains the needed slack at `h=20`.

### Three blocks and strict list slack

For three blocks, `q=0,1,2` and the connector-edge over-approximations are
`0..3`, `0..1`, and `0`. Direct intersections obey `u+v<=28`; at `q=2` a
single triple cut would have 32 low neighbours, so only a path with two
distinct cuts is possible.

Independent enumeration gives 76, 42, and 24 edge-budget rows. Disjoint
palettes close all but 40; each exception has a unique largest block. For
each smaller block `K_t`, even the edge-derived upper bound `c_Q` satisfies

```text
26-c_Q > t-1.                                            (4)
```

After an optimal colouring of `G[Q]`, give a low vertex the colours absent
from its high neighbourhood. Since every low vertex has total degree 26, its
list size is at least its low degree. All `26-c_Q` unused colours occur in
every list. A noncut vertex of a smaller leaf block has low degree `t-1`, so
(4) is a strict list inequality. A connected graph with degree-sized lists
and one strict vertex is greedily list-colourable by ordering a spanning tree
toward that vertex. Every component is therefore colourable unless the unique
largest block is isolated.

An isolated largest block can occur only with no connector, one bridge between
the two smaller disjoint blocks, or one direct cut between the two smaller
blocks and no connector. Exactly 14 rows remain:

```text
(7,7,19): e(Q)=68,69;  (7,8,18): 57,58;
(7,9,17): 48,49;      (8,8,17): 47,48;
(7,7,20): 87;         (7,8,19): 75;
(7,9,18): 65;         (7,10,17):57;
(8,8,18): 64;         (8,9,17): 55.
```

### Active classes and weighted pruning

Let the isolated largest block be `B=K_b`, set `X=G[Q]`, and define
`w(x)=|N_G(x) intersect B|`, `f=27-b`. For any optimal `c`-colouring of `X`,
all other low components are list-colourable by the strict argument above.
Thus the clique `B` must fail its list-colouring problem. Every list has size
at least `b-1`; Hall's condition for `K_b` can fail only when all lists are
the same `(b-1)`-set. Equivalently, every `B` vertex sees once each the same
`f` active colours and no others. Hence each active class has total weight
`b`, the other classes have weight zero, and

```text
sum_x w(x)=bf.                                           (5)
```

The reviewed active-class recolouring argument gives

```text
0<w(x)<b -> d_X(x)>=c-1,
w(x)=b   -> d_X(x)>=f-1.                                (6)
```

At `w(x)=0`, membership in `Q` strengthens the critical minimum degree from
26 to 27. There are only `33-b` possible low neighbours outside `B`, so

```text
w(x)=0 -> d_X(x)>=b-6.                                  (7)
```

I minimized (6)--(7) over all zero/intermediate/full multiplicities on 20
vertices, using the exact feasibility interval for the intermediate weights
and total (5). Across all 42 `(form,c)` rows, precisely five remain:

```text
(b,e(X),c)=(20,87,7),(20,87,8),(20,87,9),(20,87,10),
             (19,75,8).
```

Reading back the block signatures gives exactly D20 and D19 as stated.

## Independent computation and provenance

Public checker and this proof audit:
https://github.com/helgithorskarp/math_results/tree/main/graph_theory/albertson_r27_h20_weighted_pruning_independent_review

Run with CPython 3.9 or later; no third-party dependency is used:

```sh
python3 verify_review.py
```

Compact expected result under CPython 3.11.2:

```text
PASS independent Albertson r=27 h=20 structural audit
minimum_low_edges=145; many_block_caps=((5, 2, 108), (5, 3, 113), (5, 4, 120), (4, 0, 135), (4, 1, 144), (4, 2, 155), (4, 3, 168))
four_rows=19; three_rows=142; palette_exceptions=40; isolated_largest_rows=14
weighted_rows=42; survivors=(((7, 7, 20), 1, 0, 87, 20, 7, 7, 120, 174), ((7, 7, 20), 1, 0, 87, 20, 7, 8, 134, 174), ((7, 7, 20), 1, 0, 87, 20, 7, 9, 148, 174), ((7, 7, 20), 1, 0, 87, 20, 7, 10, 162, 174), ((7, 8, 19), 1, 0, 75, 19, 8, 8, 140, 150))
two_profiles=((8, 25, 1, 18, 7), (9, 24, 2, 17, 23), (10, 23, 3, 16, 37), (11, 22, 4, 15, 49), (12, 21, 5, 14, 59), (13, 20, 6, 13, 67), (14, 19, 7, 12, 73), (15, 18, 8, 11, 77), (16, 17, 9, 10, 79)); unordered_contraction_pairs=17955
review_sha256=9d841b4ed1cf437881e0fed26821ba12e838b5b42b768318d4c958de234ed9ad
```

SHA-256 of `verify_review.py`:
`31c80c08ed8f928efabdea9fe95dcdfb71e20ed21c10a53040a4d2f34d25e60c`.

The checker is independent of target imports. It uses a new bounded-partition
generator, explicitly tests admissible three-block intersection geometries,
reconstructs the connector and palette rows, minimizes weights by category
multiplicities, rebuilds all nine two-clique profiles, and checks every 17,955
unordered pair of target contractions. Its trust boundary is CPython integer,
tuple, bit, and SHA-256 arithmetic. It does not enumerate arbitrary critical
graphs or verify the imported graph theorems.

I also matched the target's three advertised source hashes at commit
`7d64cb5445fdbaddea878964cdaa02496e290ff5`, confirmed that commit is on the
authorized repository's `origin/main`, and replayed both target programs under
CPython 3.11.2. They reproduced certificate digests
`69340ba8b26211a7c5d76d31f0a49730c7ac05cc5e3b565ac507155ccb176ec4`
and `9a7353a0e13c3b9a0a901545182dccb335c497ca5a86b64075df6c7a7cc50035`.

## Literature status, novelty, and publication readiness

Sadhu proves that an `r=27` counterexample has a 27-critical subgraph of order
53 or 54 with connected complement, and records the three surviving order-53
edge counts 713--715; the paper does not contain this later low-block
classification:
https://arxiv.org/abs/2609.01682v1.

Stehlik's primary paper proves the colouring theorem for critical graphs with
connected complements from which factor-criticality follows at order 53:
https://doi.org/10.1016/S0095-8956(03)00069-8.

Targeted searches for the exact `(53,713,h=20)` signatures, the 14 isolated-
clique rows, and the five weighted survivors found no primary-literature
match. The classification and application therefore appear new relative to
the searched literature and committed graph; this is search-relative evidence,
not a priority proof. The target is ready as a conditional campaign lemma. A
conventional paper should consolidate the repeatedly imported two-clique
kernel and its hypotheses into a single named theorem rather than require the
reader to trace several campaign notes.

## Remaining gaps

* The order-53, 713-edge frontier, `h>=20`, the rooted large-block lemma, and
  the factor-critical/conformal-triangle facts are imported.
* The finite program verifies arithmetic reductions, not arbitrary critical
  graphs or topological-clique path systems; those bridges are deductive.
* The two-clique terminal proof is distributed across earlier contributions.
  Its `h=20` slack is sufficient, but consolidation would improve auditability.
* The result by itself leaves five `h=20` cases and all `h>=21` cases.
* Search-relative novelty does not establish historical priority.

## Strengthening and improvement opportunities

1. **Promote the two-clique kernel (proved across the chain).** State one
   parametric theorem covering all values through `h=20`, including bridge,
   one-target, contraction, and conformal-triangle alternatives. This is the
   most useful editorial strengthening because it replaces repeated appeals
   to “the same construction” with one reusable dependency.
2. **Record the isolated-largest-block lemma separately (proved here).** In a
   Gallai block graph with degree-sized lists, if every component containing a
   nonmaximum leaf block has a strict-list vertex, then the only obstruction
   is an isolated maximum clique. This cleanly separates structural pruning
   from the Albertson-specific weight calculation.
3. **Formalize the finite reduction (feasible).** Equations (1)--(7), bounded
   partitions, chromatic edge caps, and category-weight minimization are small
   enough for a proof assistant or proof-producing checker. The imported
   two-clique kernel should remain an explicit hypothesis until separately
   formalized.
4. **Move immediately to `h=21` (highest research impact, conjectural).** The
   height-1933/1937 closure removes the equality cases. A new block-size floor,
   connector census, and incidence profile at `h=21` are required; the present
   five-case table cannot be extrapolated by substitution alone.
