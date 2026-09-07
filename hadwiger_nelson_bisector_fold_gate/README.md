# A complete reflection-contraction gate for the nine-move seed

Every edge-preserving map obtained by independently retaining or reflecting
each point of the [nine-move 509-point seed](../hadwiger_nelson_neutral_mutation_candidate)
across one common line is injective. Thus this entire family of simultaneous
patch moves cannot reduce the seed to 508 or fewer points. The line is
arbitrary in the real plane, and any number of vertices may move.

The mechanism was chosen to produce a smaller graph directly: a collision
under an edge-preserving fold would give a unit-distance image on fewer
vertices, and a four-colouring of that image would pull back to the
five-chromatic seed. The implementation includes a general exact fold
constructor. The completed test finds no collision for this seed.

## The transferable criterion

Let `G` be a finite graph with distinct planar vertex positions and unit
edges. For a line `L`, let `R_L` be reflection in `L` and let `B_L` be the
vertices lying on `L`. Consider any map sending each vertex either to its
original position or to its reflection.

Such a map preserves every edge exactly when the reflection choice is
constant on each connected component of `G-B_L`. To see this, put `L` on
the horizontal axis. Reflecting just one endpoint of an edge changes its
squared length by `4 y_u y_v`. This vanishes exactly when an endpoint lies
on the axis. Reflecting both endpoints preserves distance. Hence the choices
must agree across every edge whose endpoints are off the axis, and this
condition is sufficient.

A collision of distinct vertices `p,q` requires opposite choices and
`R_L(p)=q`. The axis is therefore the perpendicular bisector `L_pq` of
`p,q`. In particular neither endpoint lies on the axis. Conversely, if
`p,q` belong to different components of `G-B_Lpq`, reflecting the component
of `p` and fixing every other component preserves all edges and identifies
`p` with `q`.

It follows that an edge-preserving one-axis reflection contraction exists
**if and only if** some pair `p,q` is disconnected after removing the
vertices on its perpendicular bisector. This reduces the entire continuum
of axes and all reflection assignments to `n(n-1)/2` connectivity decisions.
The condition is constructive in either direction: paths exclude collisions;
a separating pair supplies an exact fold. The criterion does not require
vertex-criticality or any chromatic assumption.

## Exact application to the seed

The seed has 509 distinct points and 2447 unit edges. Its coordinates are
integer vectors divided by 96 in the basis

```text
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165).
```

The program reconstructs the hash-bound sibling coordinates and tests all
129286 pairs for unit distance by exact integer monomial multiplication.

To obtain conservative sets of vertices on a bisector, evaluate the three
radicals modulo 1000081 at `964569,816716,970601`. Their square identities
are checked directly. Since all coordinate denominators are the same,
use the coordinate numerators: their common scale cancels from equal-distance
equations. This is a ring homomorphism on the integer radical coefficient
ring; no numerical tolerance or probabilistic modular-equality assumption is
used.

For a pair `p,q`, every vertex on its actual bisector satisfies

```text
2 (q-p) dot v = |q|^2 - |p|^2.
```

It therefore satisfies the same equation in the modular image. Let `Z_pq`
be the vertices passing this modular equality, excluding `p,q` themselves.
The exclusions are valid even for degenerate modular images: distinct
Euclidean points are not on their own bisector. The actual on-axis set is
contained in `Z_pq`. Any `p`-to-`q` path in `G-Z_pq` consequently avoids the
actual axis and certifies that this pair cannot collide.

Every pair has such a path. There are 11278 distinct removed sets, the
largest containing 14 vertices. All 129286 decisions are resolved by the
conservative modular test, with no exact fallback needed. The SHA256 of
the ordered 64-byte little-endian removed-set masks is

```text
78231c370da5167bf5cb1421c46fd4d44e830f631c370527cfcc5b6dbe685954
```

This hash is a regression check; it is not the proof. The public program
regenerates the sets and verifies connectivity. When a modular test does
fail on another input, the implementation refines the on-axis set by exact
field coefficient comparison before constructing a fold. A modular false
positive is never treated as a real separator.

## Reproduction and validation

From the repository root, using Python 3.11+ and its standard library:

```sh
python3 hadwiger_nelson_bisector_fold_gate/reproduce.py --output /tmp/hn-fold-gate
python3 hadwiger_nelson_bisector_fold_gate/controls.py
```

Expected output includes `pairs:129286`, `modular_paths:129286`,
`exact_fallback_paths:0`, `all_pairs_checked:true`, and
`every_one_axis_fold_injective:true`. The complete source needs no SAT solver,
proof trace, floating-point arithmetic or imported chromatic theorem.

The discovery implementation used equal-distance buckets and bitset graph
components. A separate reference implementation checked a path for each pair
using the affine bisector equation and ordinary queue traversal. The public
implementation uses the affine equation and memoized queue components. Its
entire sequence of 129286 removed sets was compared entry by entry with the
discovery route. Normal and optimized Python runs agree.

A four-point diamond is a positive construction control: the program folds
one apex onto the other, yielding an exact three-point triangle and directly
checks preservation of all five source edges. A seven-point control graph
is tested modulo 2, deliberately collapsing its modular coordinate images;
all ten nonedge pairs then require successful exact refinement. Malformed
coordinate and edge inputs are rejected. Details and environment information
are recorded in `validation.json` and `provenance.json`.

The trust boundary consists of the elementary, unformalized fold/bisector
proof, exact Python arithmetic, the imported coordinate and field routines,
and reconstructed sibling coordinate inputs. No external peer review,
formalization, or priority for the general folding criterion is claimed.
The result is a complete construction-family gate for this source, rather
than a new 509-vertex variant.

The baseline remains Parts's [509-vertex construction](https://arxiv.org/abs/2010.12665),
also identified as the record by [Haugland in August 2026](https://arxiv.org/html/2608.04542v4).
No smaller five-chromatic graph was produced here. The theorem does not cover
maps that lose source edges and gain replacements, successive folds across
different axes, or arbitrary geometric deformations. Those broader spaces
remain unclassified. This bounded reflection probe is complete; no axis-count
or edge-repair ladder is part of this result.
