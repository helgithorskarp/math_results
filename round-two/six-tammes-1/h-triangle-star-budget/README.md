# Small-diagonal triangles and their original-point budget

**six-tammes-1, researcher, 2026-10-02.** Complete ordinary author proof,
with two separate exact auxiliary checks; independent review pending.

In any finite unit-sphere packing with pair products at most
**1/2<=c<=3/5**, select actual simple strictly convex hemispherical
quadrilateral contact faces. Join opposite corners whose angle is
strictly less than `phi=2*pi-4*acos(c/(1+c))`; call the resulting graph H.

Every H triangle has a unique original degree-three center, and its
corners have degree three or four. If k corners have degree four, the
patch uses at least **7+k distinct original points**. Explicit exact
packings attain every budget above the previously known threshold beta,
the root of `1+4*c+2*c^2-4*c^3-11*c^4-24*c^5` in `(119/200,3/5)`.
H is triangle-free for the **closed** interval `1/2<=c<=beta`.
If the remaining faces at the triangle corners are also simple strictly
convex cells, all three corners have degree four and at least ten
original points are required.

[PROOF.md](PROOF.md) supplies the geometry, closed endpoints, sharpness
family, and credits. [DEPENDENCIES.json](DEPENDENCIES.json) records the
exact committed graph references and primary sources. The five-contact
angle obstruction, Q identities, below-beta shared-neighbor observation,
and contact reflection are credited prior ingredients. This contribution
adds the full correspondence, distinct-original budget, and sharp local
examples. A bounded prior-art search does not establish historical priority.

The examples have degree-one or degree-two points elsewhere and an
unrestricted outer face. They are local packings, with no assertion of
a fifteen-point, nine-Q, globally convex T/Q contact map. No global
Tammes-15 bound, optimizer occurrence, or endpoint extension of a prior
global profile catalogue is proved.
The tabulated incumbent cosine is below beta, so the sharp local examples
lie outside the parameter range of a strictly better packing. This result
clarifies auxiliary contact structure without narrowing the present global gap.

## Reproduce

CPython 3.11 or newer; tested with **CPython 3.12.14**. Standard library
only, no external runtime inputs. From this directory:

```sh
python3 -B check.py > replay.json
cmp replay.json EXPECTED.json
python3 -B -O check.py > replay-optimized.json
cmp replay-optimized.json EXPECTED.json
python3 -B audit.py > audit-replay.json
cmp audit-replay.json EXPECTED.json
python3 -B -O audit.py > audit-optimized.json
cmp audit-optimized.json EXPECTED.json
```

The programs produce the entire small [EXPECTED.json](EXPECTED.json):
ten norm identities, all 45 pair products, nine strict packing gaps with
positive Bernstein coefficients, twelve Q turns, eight construction
subsets, all four original-alias domains, nineteen contact-link corner
choices, the sealed center cycles, and exact controls. The two algorithms
use Cartesian radical arithmetic versus latitude/phase Gram data, distinct
Bernstein transforms, recursive alias pruning versus raw bit incidences,
and cyclic permutations versus Hamiltonian edge subsets. They agree on
every output byte, including normal and optimized Python runs.

[VALIDATION.json](VALIDATION.json) gives actual run receipts and output
hashes; [MANIFEST.json](MANIFEST.json) gives source hashes. Explicit
exceptions remain active under `-O`. No numerical search, solver,
private certificate, or large proof corpus is required.

The ordinary face, contact-plane, angle-budget and faceness arguments
remain a written proof obligation; code checks their algebra and finite
encodings. Two algorithms by the same author do not provide independent
researcher review. The shared signing identity identifies committed
artifacts; this directory names the actual author and role.
