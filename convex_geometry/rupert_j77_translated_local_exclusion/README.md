# Exact translated local rigidity for Johnson solid J77

**six-rupert-2 — researcher — 2026-09-29.**

For the unit-edge paragyrate diminished rhombicosidodecahedron, let
`D=(0,-1,(7+sqrt(5))/2)`. If the receiver's unit normal is within Euclidean
distance **1/200** of `D/|D|` or one of its fivefold symmetry images, and
the relative full 3D rotation has angle at most **3/20 radians**, closed
containment of a unit or larger projected copy forces scale one, identical
orientation and zero translation. Thus no strict Rupert passage exists in
this region, with any planar translation. Either sign of the normal is allowed.
The angle condition includes in-plane alignment of the projection frames.

J77's global Rupert property remains unresolved. This certificate covers
five unoriented receiver caps and a neighborhood of relative rotation zero.
The earlier [global diameter and scale certificate](https://github.com/helgithorskarp/math_results/tree/main/convex_geometry/rupert_j77_projection_diameter)
already excludes the exact direction `D` for arbitrary inner orientations.
The present theorem supplies open receiver neighborhoods, with an additional
local restriction on the relative rotation.

Read [PROOF.md](PROOF.md) for the general criterion and its J77 application.
Thirty-four algebraic support probes have 1836 strictly positive support-gap
comparisons. Six exact positive combinations yield the signed rotation
coordinate vectors and zero translation coordinates. Projecting the probes
into nearby receiver planes preserves this cancellation. No central-symmetry
assumption is made for J77.

From the repository root, with Python 3.11+ and standard library only:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 -B convex_geometry/rupert_j77_translated_local_exclusion/verify.py --self-test
```

The output equals [expected.json](expected.json). `verify.py` reconstructs
all coefficients over `Q(sqrt(5))` from 28 column indices, checks every finite
hypothesis, and audits strict inequalities using separate rational enclosures
of `sqrt(5)`. It independently regenerates the named model by cupola
deletion/gyration and verifies its fivefold symmetry. Invalid probes and
positive-combination bases are rejected. The checker was tested on Python
3.11.2; its written analytic implication is not formalized or independently
reviewed.

`model.py` and `q5.py` are unchanged copies of the small model and field
source from the earlier J77 certificate. This directory is self-contained.
The published checker requires no solver, floating-point geometry package,
external data, large certificate or network access. Floating-point LP discovery
selected only the listed column bases; its encoding and versions are recorded
in the proof.

The proof cites the complementary contact methods of researchers
[six-rupert-1](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/proof.md)
and [six-rupert-3](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/TORQUE_PROOF.md).
No priority claim is made for the contact-gradient mechanism.
