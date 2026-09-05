# Cross four-cycles force four-colorability of two connected E-gadgets

**Theorem.** Let `P,Q` be subsets of
`E=Q(i sqrt(3),i sqrt(11))`, each with a connected unit-distance graph.
If an isometric placement `P union g(Q)` has a cross four-cycle on four
distinct points, its strict unit-distance graph is four-colorable.
A cross four-cycle means two distinct points of each component with all
four distances between the components equal to one. Other overlaps are
allowed. There is no vertex-count or denominator bound.

The four-cycle fixes the two diagonal midpoints and forces the rotation
multiplier to have its square in `E`. Outside the already four-colorable
base-field case, every cross edge then satisfies a sum-of-squared-radii
identity. Two explicit congruence colorings, according to whether the
local diagonals are even or units, color every such edge.

[PROOF.md](PROOF.md) gives the uniform argument and exact coloring recipe.
It uses only the prior field embedding and arithmetic modulo two and four;
it does not require a coloring of the entire quadratic extension.

For the fixed 292-vertex inner union `B=A union ((5+i sqrt(11))/6)A` of the
Parts 159-vertex gadget and the Parts 214-vertex gadget `V`, the theorem
closes **every placement with a cross four-cycle**, including all disjoint
506-vertex placements of that kind. Any non-four-colorable remaining
composition must have a four-cycle-free cross graph. Combined with the
[previous single-hub reduction](../hadwiger_nelson_mixed506_single_hub_reduction/README.md),
a disjoint remaining placement has at most one vertex of cross degree
at least three, and that degree is at most ten.

No five-chromatic graph or record improvement is produced. The family with
no cross four-cycle remains open. Neither the teammate's sealed Parts pool
nor the parked Parts two-overlap family is enumerated here.

## Reproduce

Use Python 3.11 or later, standard library only, from this directory in a
complete repository checkout:

```bash
python3 verify.py --cases-out /tmp/cross-four-cases.json > /tmp/cross-four-summary.json
cmp expected.json /tmp/cross-four-summary.json
cmp calibration.json /tmp/cross-four-cases.json
python3 audit.py --cases /tmp/cross-four-cases.json > /tmp/cross-four-audit.json
cmp expected_audit.json /tmp/cross-four-audit.json
sha256sum -c SHA256SUMS
```

The diagonal-length census processes all component pairs. It finds 77
complementary squared-length pairs: 26 with rotation roots in `E`, and
51 with roots outside `E`. They account for 2,551,052 and 1,748,914 unordered
component-diagonal pair choices respectively. These are labeled seed
counts, not numbers of distinct graphs or placements.

The generator checks one exact placement for each of the 51 outside-field
length types. The unit-diagonal coloring applies in 43 cases and the
even-diagonal coloring in eight. All selected cases are disjoint, with
506 vertices, and their complete cross graphs have four through ten edges.
It verifies every component and cross edge and supplies compact hashes in
[calibration.json](calibration.json).

The separate audit constructs the input union by generic real-radical
multiplication, classifies the square condition with rational arithmetic,
and reconstructs the colors through exact auxiliary `E` coordinates.
It then traverses all 6,516,015 point pairs in the 51 selected geometries,
using the full quadratic algebra `E[u]`, and matches every edge stream and
coloring. The identities cover both roots without approximating them.

The auditor also exhausts the finite congruence claims: six relevant ordered
pairs modulo two and 216 relevant choices modulo four. The generator checks
a midpoint-overlap control for the more general local-coset coloring lemma
and rejects a nonintegral residue request. The control's tiny source graphs
are not asserted to be connected.

These computations validate the implementation and its exact sample graphs.
**The uniform theorem follows from the proof, not an assumption that the
51 examples exhaust all placements.** No SAT solver is used.

On the producing host with CPython 3.11.2, the generator took under one
second and the full audit took 34.11 seconds with 17.9 MiB peak RSS.

## Input and certificate conventions

The source order is the archived 159-point table followed by previously
unseen points of its rotated copy; `V` retains its archived order.
A seed `[i,j,k,l]` selects the two unordered component diagonals.
`colors_sha256` hashes the concatenation of the `B` and `V` color digits
followed by a newline. `cross_sha256` hashes ascending source pairs
`b,v` with a newline each. `union_edges_sha256` uses first-component labels
then second-component labels offset by 292, identifying a shared midpoint
with its first-component label if present. The selected cases have no
identification. These conventions are explicit in both implementations.

The archived [coordinate provenance](../hadwiger_nelson_nonmono159_214_lowden2/SOURCE.md),
[fixed inner union](../hadwiger_nelson_nonmono159_moser_triple/PROOF.md) and
[whole-field coloring](../hadwiger_nelson_nonmono_field_obstruction/PROOF.md)
are reused with hashes. The independent coordinate constructor and rational
square test are also pinned. No generated graph dump, angle census or
large proof artifact is required.

The geometric and local-arithmetic arguments remain unformalized. Finite
trust rests in pinned coordinates and dependencies, exact Python arithmetic,
and ordinary execution. The checks use different representations and are
author cross-checks, not external peer review. No priority claim is made
for the modular coloring method.
