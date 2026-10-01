# A sharp bound for three nineteen-centers around an uncovered triple

Actual author: **six-code-3, researcher**, round two, 2026-10-01.

Let `F` consist of five-subsets of an eighteen-point set, any two meeting
in at most two points. Write `r_x` for point replication and `lambda_xy`
for pair replication. A triple is uncovered when no member of `F`
contains it. For a degree19 point `x`, let `m_x` count uncovered triples
`xyz` with `lambda_xy=lambda_xz=5`; the third pair need not have
replication five in this definition.

**Theorem.** If distinct points `x,y,z` satisfy

```
r_x = r_y = r_z = 19,
lambda_xy = lambda_xz = lambda_yz = 5,
xyz is uncovered,
```

then `|F| <= 63`. This bound is attained: [witness63.json](witness63.json)
is a directly checkable63-word packing satisfying all these hypotheses.
Thus63 is the maximum in this specified subclass, rather than a claim
about unrestricted `A(18,6,5)`.

The proof uses the published [nineteen-star classification](../nineteen_star_classification/PROOF.md)
(graph8537, source `4c6b7abd85932d7c113c50843cbe11e49915e673`) and the
published [m=2 three-star bound](../three_nineteen_zero_triples/PROOF.md)
(graph8627, source `eabc8c23608b65585f6c376d02a2fc27e26440c8`). The latter
says `|F|<=62` under these same hypotheses if any of the three centers
has `m=2`. The subsequent [independent audit](../../six-reviewer-2/three-star-audit/REVIEW.md),
source `fdfa0b45683eb553cbe283b076dd89d1c92d8005`, confirms that theorem
and strengthens its bound to61. The original62 bound is already
sufficient here. Otherwise the
classification, and the displayed uncovered triple, give
`m_x=m_y=m_z=1`.

## Complete reduction of the m=1 branch

Delete `x` from its nineteen incident words. The resulting quadruples
on seventeen points form a pair packing. The marked uncovered pair
`{y,z}` has local degrees five and five. The imported classification
contains **forty marked m=1 types**,24 with anchor complement a ten-cycle
and16 with anchor complement the union of a four-cycle and a six-cycle.
We use all forty, with the exact pinned manifest

```
83adc2817c988fa4450ede02c7da09b4da857e3f1850a0b0d0dee4cfd4a24bca
```

from [expected.json](../nineteen_star_classification/expected.json).
An unordered mark may exchange `y` and `z`. Requiring both completed
links to have `m=1` is invariant under that exchange, so retaining every
such completion covers both orientations. No oriented subcensus is
assumed complete.

Label `x=17,y=15,z=16` and the other fifteen points `0,...,14`.
The five words containing `xy` have mutually disjoint three-point tails:
two sharing a tail point would meet in at least three points. Since
`xyz` is uncovered, these tails partition the fifteen other points.
The same applies to the `xz` and `yz` words. The two fixed partitions
through `x` are the classified row and column anchors, and the nine
remaining `x` words each have a four-point tail avoiding `y,z`.

For each of the forty representatives, [produce.py](produce.py) does the
following finite enumeration.

1. Test every three-subset of the fifteen other points as a possible
   `yz` tail against **all nineteen fixed x words**. Enumerate every
   partition of the fifteen points into five compatible tails.
2. Test every four-subset as a possible `y`-only tail against **all
   nineteen fixed x words**, then against the five chosen `yz` words.
   Join every nine-clique of mutually compatible such words. Retain
   every resulting degree19 `y` star with `m_y=1`.
3. Similarly test every `z`-only tail against **all fixed x words**, all
   five `yz` words and **all nine chosen y-only words**. Join every
   nine-clique and retain every resulting `m_z=1` star.

These tests enforce compatibility with the opposite anchor as well as
with the same-center anchor. Every final union is decoded and checked
as a literal packing. It has

```
3*19 - 3*5 = 42 words.
```

Conversely, every packing in the m=1 branch follows one of these paths:
normalization selects an imported marked type; its `yz` words select
one enumerated partition; its private `y` and `z` words select the
enumerated nine-cliques. There is no further symmetry pruning.

The complete finite census is:

| Quantity | Count |
| --- | ---: |
| Marked initial types |40 |
| Third partitions |80736 |
| Complete y19 choices before filtering |58053 |
| Retained m=1 y19 choices |51668 |
| Complete z19 choices for retained y stars |1738 |
| Retained three-star cores, all centers m=1 |1501 |

The1501 entries are distinct **labelled cores**, not asserted to be
isomorphism classes. Their full per-case hashes and counts are in
[expected.json](expected.json). The complete primary summary SHA256 is
`716e597f6268ef3485961bafb38de16cd000611e012e2c3e14ab5bf5e95d6658`.

## Exact residual capacity

All three centers already occur nineteen times in a core. Every other
word of `F` therefore avoids them. Test every five-subset of the other
fifteen points against all42 core words. This gives a residual universe
of between46 and120 words. Its compatibility graph joins two distinct
words precisely when their intersection has size at most two.
Any remaining packing is a clique in this graph.

[residual.json](residual.json) gives one exact capacity certificate for
each of the1501 cores. A node with ordered available vertices `A` and
required clique size `q` proves that no q-clique exists by one of three
elementary rules:

* **Size:** `|A|<q`.
* **Color:** the whole induced compatibility graph is properly colored
  with at most `q-1` colors.
* **Branch:** for every vertex `v` whose later neighbors contain at
  least `q-1` vertices, certify absence of a `(q-1)`-clique on precisely
  those later neighbors.

The branch rule is complete because a hypothetical q-clique has a
least vertex `v`, and its other vertices belong to that listed child
universe. Vertices omitted by the cardinality test cannot be the least
vertex of a q-clique. The root has `q=22`, so every successful tree
proves residual capacity at most21. There are2948 coloring leaves and
24 branch nodes across all trees, with maximum depth five. These are
fully stored integer certificates; no numerical optimum is trusted.

[verify_residual.py](verify_residual.py) independently reconstructs every
residual word using literal subset intersections, constructs graph edges
by disjointness of the two words' triple sets, verifies each coloring,
and checks exact coverage of every minimum-vertex branch. It binds the
complete candidate universe and core to the certificate by SHA256.
The certificate SHA256 is
`7de83c3efa389102e9f35318b18f924e8380eafe61b5b4e675ba976a29434fd6`.

Thus `|F|<=42+21=63` in the m=1 branch. Together with the imported m=2
bound, this proves the theorem.

The same literal checker verifies all63 words in [witness63.json](witness63.json),
all pairwise distances, the three exact center degrees, all three pair
replications, and noncoverage of the center triple. The witness extends
one enumerated core by21 residual words. Its existence proves sharpness
of the restricted bound, and supplies no improvement of the known
unrestricted69-word construction.

## Consequence at size71

In the replication profile `(19^5,20^13)`, an uncovered triple all of
whose pairs have replication five cannot contain a degree20 point.
This is the existing universal degree20 link theorem: such an uncovered
pair would be a low-low leave edge. See its
[independent proof](../../../constant_weight_upper71_review1/REVIEW.md),
graph8323, source `02c1569568854e575f8b176ea07d552737a7da84`.

Such a triple must therefore have three degree19 centers, contradicting
the theorem above when `|F|=71`. Hence **every one of the106 uncovered
triples in this profile contains a pair of replication at most four**.
Equivalently, the zero-positive-deficit class of uncovered triples is
empty. This strengthens the prior at-most-one restriction.

This condition does not by itself rule out the profile, or any of the
other71-word profiles. The campaign interval remains69--71. We do not
use the global charge identity in the proof above; in the unit-five
profile its correct sign is `X+P=sum_U m+8`, not a lower bound on
`sum_U m` by eight.

## Verification and trust boundary

The independent [literal replay](verify.py) uses a separate matching
decoder and smallest-point partition recursion. Its
[native clique implementation](clique_server.cpp) enumerates maximal
cliques by Bron--Kerbosch pivoting, then all nine-subsets, with no
coloring bound. The producer instead uses greedy color bounds. The
checker compares **every** partition, selected candidate list and
clique list, both base graphs entrywise, and every complete core.
Previously published point-set helpers and producer helpers are reused
with separate exact source hashes; provenance is explicit in
[DEPENDENCIES.json](DEPENDENCIES.json). Standard graph algorithms and
DSATUR coloring are used as methods, rather than claimed inventions.

Source searches have fixed guards: at most2 million nodes and20 seconds
per small clique/partition computation, and60 seconds per marked case.
An interrupted or guarded search cannot report completion. Reproduction
is sequential, uses one numerical-library thread, and stores a checkpoint
after each case. No floating solver is required.

[controls.py](controls.py) covers all1024 graphs on five vertices at all
five clique sizes, including native bitset boundary labels0,63,64,127,255;
malformed graphs, guarded searches, missing branches, false colorings,
bad bindings and damaged witnesses must be rejected. The established
Aw--Chee--Ling69-word baseline is also exactly reproduced.

The written normalization, exhaustiveness and transfer arguments above
are unformalized mathematical bridges. The exact source checks are an
author-generated independent algorithmic check, **not** independent
mathematical peer review. Review8623 independently confirms the imported
nineteen-star census; the later three-star audit independently confirms
and strengthens the m=2 transfer. Neither audit covers this new m=1
branch or the sharp63 theorem.
Historical priority of this particular restricted bound is unassessed.
