# Rhombicosidodecahedron: exact local obstructions

**six-rupert-3 — researcher — 2026-09-29.**

Exact analytic criteria exclude small relative rotations and reduce the
varying-target local frontier to one orbit of **30 unoriented axes**.
**The global non-Rupert conjecture remains open.**

[CELL_PROOF.md](CELL_PROOF.md) proves that **every fixed RID projection has
a positive exclusion angle**. Five polynomial certificates cover a complete
symmetry chamber. More quantitatively, for `0<rho<=1/200`, target normals at
distance at least `rho` from the symmetry orbit of
`(1,phi,1+3phi)/sqrt(12+16phi)` exclude relative rotation angles at most
`rho/200000`, for every translation. Any sequence of passages with relative
rotation tending to zero must accumulate at this one orbit. This is not a
uniform local exclusion over all target normals. An exact separator for the
limiting normalized contact torques identifies why a second-order argument
is still needed there.

[TORQUE_PROOF.md](TORQUE_PROOF.md) excludes a passage when the target normal is
within **1/1000** of `(10,1,3)/sqrt(110)` and the relative source rotation has
angle at most **1/100 radians**, for any translation. Four non-radial support
probes give torques whose tetrahedron contains the unit ball. The same exact
checker proves that the positive radial maxima at this direction cannot span
its normal: the published radial criterion does not apply here.

A complementary class-based criterion excludes strict containment between two
rhombicosidodecahedron projections whose orthonormal row frames are within
operator norm **1/100** of the standard xy projection. Translations are
arbitrary, and small in-plane rotations are included in the frame condition.
An exactly checked 60-rotation symmetry group transports this neighborhood to
15 unoriented axes and to independently symmetry-equivalent frames.
Both criteria transport under independently chosen verified vertex symmetries.

[PROOF.md](PROOF.md) gives a general criterion for centrally symmetric,
sphere-inscribed vertex sets with paired off-plane vertices and singleton
equatorial vertices. It explains how coincident projected vertices can be
handled by a radial support class, rather than individually. It then combines
absolute axial inequalities with a positive quadratic stress.

The top-view region was already identified as amenable to a polynomial
exclusion by [Steininger--Yurkevich, Section 9.1](https://arxiv.org/html/2508.18475#S9.SS1).
The contribution there is the explicit analytic criterion, rational neighborhood,
and compact exact verification, with no priority claim for top-view exclusion.
The support-torque criterion supplies a separate local certificate beyond this
top-view region. Neither floating-point exploration nor failure to find a
passage enters any of the final proofs.

Related team work by **six-rupert-1** gives
[all-direction fixed-outer contact certificates for the deltoidal hexecontahedron](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/orientation_proof.md).
The shared first-order contact-gradient mechanism is acknowledged. The RID
results include stable unique-support probes on a cap and explicit polynomial
support probes on whole direction cells.

## Reproduce

Python **3.11.2** was used; Python 3.11 or later and its standard library suffice.
From the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/cell_certificate.py --self-test
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/torque_certificate.py --self-test
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/verify.py --self-test
```

The cell command checks 200 cubic coefficients, 3,600 corner support
comparisons, the symmetry chamber's coverage, and the complete limiting
16-vertex silhouette with another 2,880 corner support comparisons. Expected
output: `cell_expected.json`. All fields and coefficients are exact. Its
self-tests reject reversed probes, stress signs and silhouettes, and a missing
cell. The complete run with self-tests takes about ten seconds and 16 MiB.

The torque command's deterministic JSON output checks all 236 unique-support
inequalities for four exact probes, a positive torque equilibrium, and the
four exact facet-distance bounds proving inclusion of the unit ball. It checks
the scalar errors `1/4<27/100` and `3/4<1`, and the six radial maxima and their
tangent separator `(-1,-5,5)`. Expected output: `torque_expected.json`.
Its self-tests reject a reversed probe, a degenerate repeated-probe certificate,
and a missing probe.

The mirror command's deterministic JSON output checks:

- 60 standard vertices, all with squared radius `7+8phi`, and central symmetry;
- 12 selected projected classes: 8 doubletons and 4 singletons;
- all 700 radial gap comparisons, with exact minimum 1;
- support error less than `201/250` and support gap greater than `49/250`;
- the two positive quadratic stress coefficients and all scalar proof bounds.
- 60 proper vertex-preserving rotations and 15 unoriented axes in the orbit.

Every number is represented exactly in `Q(phi)`, with `phi^2=phi+1`; signs
are reduced to rational comparisons against the square of `sqrt(5)`.
`expected.json` is the mirror command's compact expected output. Self-tests check the field
relation, algebraic signs, inversion, and rejection of missing vertices and an
unsupported neighborhood. The analytic theorem is not formalized in a proof
assistant; the code checks its finite hypotheses, not every possible rotation.
On the recorded host the complete command takes a few seconds.

## Current named frontier

Primary literature searched on 2026-09-29 leaves these named cases unresolved:

| Family | Named solids |
| --- | --- |
| Archimedean | snub cube, rhombicosidodecahedron, snub dodecahedron |
| Catalan | deltoidal hexecontahedron, pentagonal hexecontahedron |
| Johnson | gyrate rhombicosidodecahedron J72; parabigyrate rhombicosidodecahedron J73; metabigyrate rhombicosidodecahedron J74; trigyrate rhombicosidodecahedron J75; paragyrate diminished rhombicosidodecahedron J77 |

The named list comes from [Fredriksson](https://arxiv.org/html/2210.00601),
with later status checked against [Gosain--Grimmer](https://arxiv.org/html/2509.08190)
and its [May 2026 journal article](https://doi.org/10.1080/00029890.2026.2662830).
[Zeng's April 2026 paper](https://arxiv.org/html/2604.26531) explicitly retains
the rhombicosidodecahedron non-Rupert conjecture. The universal convex-polyhedron
conjecture is already disproved by the Noperthedron; wording in older numerical
papers that it remains open does not change that result.

Next: develop a second-order or support-class exclusion around
`(1,phi,1+3phi)`, paying attention to the limiting rotation axis
`(1,phi,1-phi)`. A full non-Rupert proof also requires global exclusion.
