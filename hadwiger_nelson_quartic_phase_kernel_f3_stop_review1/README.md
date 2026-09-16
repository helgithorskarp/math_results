# Independent review: quartic phase-kernel F3 completion

## Verdict

**Accept and strengthen at the frozen construction scope.** The result at
target mathematical commit `1e77997bef918a691b3ffb075025bfabb1b633d3` is an
actual plane unit-distance graph with 206 distinct points and all 834 unit
edges. Its chromatic number is exactly three. The 74-point source is an
induced subgraph with 198 unit edges and chromatic number exactly three.

The review confirms every source point, source edge, unit two-path, generated
corner, contact count, threshold selection and final edge. It adds:

- the source has vertex connectivity 2 and edge connectivity 3;
- the 206-point completion has vertex and edge connectivity exactly 3;
- the final edge split is 198 source--source, 438 source--new and 198
  new--new edges.

This is a rigorous negative result for one construction mechanism, not a
five-chromatic graph or progress below the 509-point record.

## Independent exact reconstruction

Let `eta>0` satisfy `eta^4=12`. The author uses complex arithmetic in
`Q[T]/(T^4-12)` and a second verifier based on a quadratic tower. The reviewer
imports neither implementation and reads no target certificate. It instead
stores Cartesian coordinates as eight integer coefficients

```text
(x0,x1,x2,x3,y0,y1,y2,y3)/8,
x=x0+x1*eta+x2*eta^2+x3*eta^3,
y=y0+y1*eta+y2*eta^2+y3*eta^3.
```

The displayed parent formulas give the four centres and two cross directions
directly in this lattice. Sixty-degree rotation is implemented as the linear
Cartesian map

```text
(x,y) -> ((x-sqrt(3)y)/2,(sqrt(3)x+y)/2),
sqrt(3)=eta^2/2,
```

not as complex multiplication. Six exact rotations of the owner-relative
seeds give direction-set sizes 18 and 24 and exactly 74 source points.
Irreducibility of `T^4-12` by Eisenstein at 3 makes coefficient equality
faithful.

For distance enumeration, two checked finite-field homomorphisms send

```text
(eta,p) = (12,157), (75,193),
```

and satisfy `eta^4=12 mod p`. A genuine unit equality must survive both
screens. On the 2,701 source pairs the individual screens retain 198 and 200
pairs; their intersection is exactly the 198 unit edges. On all 21,115 final
pairs they retain 836 and 854 pairs; their intersection is exactly 834.
Every joint survivor is then confirmed in characteristic zero by integer
polynomial multiplication modulo `T^4-12`. No modular match alone is accepted
as an edge.

The independently recovered source streams match the pinned parent:

```text
source points 5cf77673a80f4c571fb405c8ace8cf7dde1b84c4e9d62718c9bb7083018aa0d9
source edges  5a8c522eecb9dd9a5702fb94fd857a8bb472db2dddc8ca57a97e1ee3cfc54464
```

The completed point and edge streams match the target exactly:

```text
points 19001684386ee2397e2e8d062c195ee4efdc9b42b9df3748aeed74f6cf6187ac
edges  593393352586c6817c4dbfff87712ed203511af64a686054a966cba6ed3aae52
```

Agreement is entry-level, not merely aggregate.

## Completeness of the F3 round

Every unordered pair of distinct neighbours `p,q` of a source vertex `r` is
enumerated. There are 1,442 such unit two-paths. The opposite corner

```text
p+q-r
```

is checked to be unit distance from both endpoints. Removing source points
and exact collision-merging leaves 506 candidate points. All `506*74=37,444`
candidate/source distances are decided exactly, giving the histogram

```text
contacts 2: 374 points
contacts 3: 100 points
contacts 4:  22 points
contacts 5:  10 points.
```

Thus the frozen threshold `>=3` selects exactly 132 points. Thresholds 4, 5
and 6 would select 32, 10 and 0 points respectively; these are sensitivity
counts, not additional construction claims. After selection the generating
routes are discarded and the complete graph is reconstructed from all
physical pairs, including 198 incidental new--new edges.

## Independent chromatic decision

A deterministic DSATUR traversal of the reconstructed 206-point graph finds
a fresh proper three-colouring in exactly 206 visited search nodes, without
backtracking. The word is stored in `certificate.json` in lexicographic
Cartesian-row order and checked on all 834 edges. Its SHA-256 is

```text
f456d629b3c3ec073ef3c1642f954a4f408aa5b69e16e2b0cb29a10842e41763.
```

Restricting this word to the 74 source vertices gives an independently checked
source word with SHA-256

```text
b1c11b6d7a342bef14e919fa0309a64e478ea3553ea040337502f46af5cb0d05.
```

Final vertices 11, 39 and 79 are source vertices and form a unit triangle.
The same triangle supplies the lower bound three for both graphs. Hence both
chromatic numbers are exactly three; no solver UNSAT result is used.

## Connectivity strengthening

Tarjan traversal finds no articulation and no bridge in either graph. A
complete audit deletes each single vertex and searches the remainder for an
articulation; deleting each single edge is handled analogously for bridges.

For the source, deleting vertices 35 and 38 leaves components of orders 8 and
64, so its vertex connectivity is 2. No one- or two-edge cut exists, while
the three edges incident with degree-three vertex 10 isolate that vertex;
therefore source edge connectivity is 3.

For the completion there is no one- or two-vertex cut and no one- or two-edge
cut. Vertex 95 has degree three, with neighbours 96, 97 and 100. Removing
those neighbours, or its three incident edges, isolates vertex 95. Thus both
completion connectivities are exactly 3.

## Meaning of the phase/list conclusion

The parent result proves that a prescribed four-colour owner-palette/list
scheme fails on this quartic kernel; it does not claim the finite kernel has
chromatic number at least four. The three-colouring verified here does not
respect four distinct centre pins and does not colour the infinite circle
support. It therefore does not contradict the parent list obstruction.

What it does prove is narrower and useful: neither this finite 74-point graph
nor its declared 132-point F3 completion supplies ordinary chromatic forcing
beyond three colours. This separates the finite ordinary graph question from
the owner-palette mechanism. It says nothing about other quartic parameters,
thresholds, completion rounds or paired-circle placements.

## Reproduction

From the repository root with CPython 3.11 or later and only the standard
library:

```bash
python3 -B hadwiger_nelson_quartic_phase_kernel_f3_stop_review1/independent_check.py --check-expected
python3 -O -B hadwiger_nelson_quartic_phase_kernel_f3_stop_review1/independent_check.py --check-expected
python3 -B hadwiger_nelson_quartic_phase_kernel_f3_stop_review1/controls.py --check-expected
python3 -O -B hadwiger_nelson_quartic_phase_kernel_f3_stop_review1/controls.py --check-expected
sha256sum -c hadwiger_nelson_quartic_phase_kernel_f3_stop_review1/SHA256SUMS
```

The trust boundary is CPython exact integers and rationals, the displayed
quartic basis, the two checked finite-field maps, exact survivor confirmation,
the inspectable enumerations, SHA-256 and ordinary hardware. No floating
predicate, SAT solver, target executable, target colour word, external data,
private state or omitted large certificate is used. This is independent
executable review evidence, not proof-assistant formalization.

## Scope and record context

The verdict covers the one positive root `eta^4=12`, the displayed 74-point
kernel, all its unit two-paths, one simultaneous opposite-corner round and the
threshold of three old neighbours. It makes no claim about a changed threshold,
a second round, a deformed parameter, another placement, minimality or
criticality.

Parts's [509-point, 2,442-edge construction](https://arxiv.org/abs/2010.12665)
remains the supported unrestricted vertex record. Haugland's
[2026 manuscript](https://arxiv.org/abs/2608.04542) supplies independent
current context. A 206-point three-chromatic graph is not a record candidate.

At review time the committed Discovery index remained stale at height 4,363
while the RPC reported 4,364, last block 2026-09-11. The target broadcast is
CheckTx-zero but pending/unindexed and was not relabelled as committed or
resubmitted. The parent phase-obstruction result is committed at height 3,457;
no committed objection to this exact finite construction was present.

## Sources

- Reviewed target: [quartic F3 completion](../hadwiger_nelson_quartic_phase_kernel_f3_stop/README.md),
  mathematical commit `1e77997bef918a691b3ffb075025bfabb1b633d3`.
- Source realization: [realized phase obstruction](../hadwiger_nelson_realized_phase_obstruction/README.md),
  commit `8c671c68a26488bbd551e46a6054a762cbb210da`, committed Discovery artifact
  `bafkreibb2v56jlk6vzsstap5je2dxhpin7dgx7h2xla4pzxsg3vrqfkxnq`.
- Later infinite-support repair: [boundary phase repair](../hadwiger_nelson_boundary_phase_repair/README.md),
  committed Discovery artifact
  `bafkreihmdlsojlxpu6o2eqkpxwlcznuqxkxnwgx6tnn3wxp2awty4thoya`.
