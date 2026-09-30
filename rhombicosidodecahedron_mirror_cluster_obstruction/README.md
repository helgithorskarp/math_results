# Rhombicosidodecahedron: local obstructions and adaptive receiver regions

**six-rupert-3 — researcher — updated 2026-09-30.**

[ADAPTIVE_RECEIVER_PROOF.md](ADAPTIVE_RECEIVER_PROOF.md) gives a sufficient
exclusion criterion depending only on the receiver, and certifies a whole
receiver polygon from exact corner inequalities. It excludes **every source
orientation** in the closed chord caps of radius **1/200** about the ten
unoriented threefold axes, enlarging the prior radius by 35. An explicit
two-dimensional receiver triangle extends beyond even the radius-1/190 cap.
Source roll, translation and scale at least one remain arbitrary.

The complete persistent contact pool has 36 endpoint probes. Its exact center
torque hull has sharp ball radius `phi-1`, verified by all 816 torque triples
and 15 supporting facets. A concave long-edge gap rejects the remote roll
branch: for one-sided shadow error `eta<=77/1000`, the roll chord modulo `C6`
is at most `eta`. Combined with axial coercivity and full frame transports,
this reduces a certified receiver patch from five passage parameters to two
receiver parameters. The complementary normal domain remains unresolved.

[LINEAR_ROLL_PROOF.md](LINEAR_ROLL_PROOF.md) excludes **every source orientation**
when the receiver normal is within chord distance **1/7000** of one of the ten
unoriented threefold axes. Source roll, translation and scale at least one are
arbitrary. The exact threefold shadow is a cyclic dodecagon. Its supporting
edges give a bound valid for **every planar rotation**: distance to the shadow's
six rotation symmetries is at most `20/3` times the one-sided containment error.
Sharper axial, frame-angle and actual torque estimates enlarge the previous
cap radius by `2000/7`. All edge ties and every original vertex are checked.

[GLOBAL_CAP_PROOF.md](GLOBAL_CAP_PROOF.md) supplies the earlier radius
`1/2,000,000`, the exact minimum squared shadow diameter `80/3+32phi`, and
its complete ten-axis optimizer classification. All 436 antipodal axial sign
regions are checked; the nonoptimal regions have a strict gap. These receiver
caps still leave a global unresolved frontier.

Exact analytic criteria exclude every strict translated passage with full
relative rotation angle at most **1/10^16 radians**, uniformly over all
target projections. RID is therefore **not locally Rupert**, including when
both projections vary independently.
**The global non-Rupert conjecture remains open.**

[LOCAL_PROOF.md](LOCAL_PROOF.md) closes the previously remaining critical
orbit. Five contacts force the relative rotation axis close to
`(1,phi,1-phi)`. A hidden supporting vertex and two zero-height radial
vertices give incompatible bounds, with exact rational error estimates.
The uniform angle is deliberately conservative; it is not a useful estimate
of an optimal local exclusion angle.

[CELL_PROOF.md](CELL_PROOF.md) proves that **every fixed RID projection has
a positive exclusion angle**. Five polynomial certificates cover a complete
symmetry chamber. More quantitatively, for `0<rho<=1/200`, target normals at
distance at least `rho` from the symmetry orbit of
`(1,phi,1+3phi)/sqrt(12+16phi)` exclude relative rotation angles at most
`rho/200000`, for every translation. Any sequence of passages with relative
rotation tending to zero must accumulate at this one orbit. That cell theorem
alone is pointwise. Its exact limiting contact separator explains the failure
of a uniform first-order argument, which the new quadratic proof resolves.

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
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/adaptive_receiver_certificate.py --self-test
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/linear_roll_certificate.py --self-test
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/global_cap_certificate.py --self-test
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/local_certificate.py --self-test
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/cell_certificate.py --self-test
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/torque_certificate.py --self-test
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/verify.py --self-test
```

The adaptive command rechecks and compares the entire linear-roll output and
its inherited diameter/sign-region/cell hypotheses. It regenerates all 120
standard edges, tests 43,200 corner gaps for both edge orientations, verifies
6,480 selected support gaps and all 14,688 torque-triple support comparisons,
and computes all 15 center facets. It checks ten roll-branch comparisons,
23 cap bounds, exact rational radical enclosures on a fixed denominator-`10^12`
grid, and every example-triangle corner hypothesis. Ten new malformed controls
and twelve inherited controls are rejected. Every byte must match
[adaptive_receiver_expected.json](adaptive_receiver_expected.json), SHA256
`53c852471e2d787b8958f01cc6f6e1b5c210ce3ee2b3a524ddbe1a59e9514e98`.
The first full replay took 45.98 seconds and 24,796 KiB peak child RSS, with
one CPU job. No floating-point or solver verdict is a proof input; continuous
polygon coverage and the source-elimination bridges are proved in prose.

The linear-roll command rechecks the entire global-cap output, then validates
the complete dodecagon against all sixty original vertices (720 inequalities),
both incident derivatives and all long-edge ties, six exact roll comparisons
and nineteen cap-error comparisons. Twelve malformed controls are rejected,
including six inherited controls. Every output field must match
[linear_roll_expected.json](linear_roll_expected.json), SHA256
`d030324507fc37fda1dd8c7bdda22b55422f8b7c5a1ccf011ffb7bdcdb5de309`.
The first exact replay took 27.15 seconds and 24 MiB peak child RSS with one
thread. Source and compact expected output are the only proof inputs.

The global-cap command generates 17,140 raw active-set directions and checks
all 140,430 dot products on their 4,681 distinct projective directions. It
reconstructs the ten optimizer axes, all 436 sign-region maxima, the active
threefold stress triangle, six valid and six invalid circle rolls, chamber
separations, four center torque facet distances and twelve rational error
bounds. It rechecks every inherited
cell-certificate field. Expected output: `global_cap_expected.json`. Six
malformed controls are rejected. The full Python 3.11.2 replay takes about
27 seconds and 24 MiB. The general equal-radius active-set
reduction is credited to
[six-rupert-2's J77 diameter proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_projection_diameter/PROOF.md).

The local command rechecks the complete prior cell and mirror hypotheses,
then adds 1080 corner support comparisons, 236 radial comparisons, critical
axis and hidden-vertex identities, a quadratic identity, and 15 rational
error audits. Expected output: `local_expected.json`. Reversed axes and
silhouettes, incorrect hidden vertices, missing radial directions and an
unsupported angle are rejected. Exact Cayley identities are also checked.
The recorded complete self-test takes 3.291 seconds and about 20 MiB.
The analytic proof is unformalized and independent review is not asserted.

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

Next: extend the adaptive criterion over a specified larger receiver domain,
using actual receiver torque facets or certified polygon subdivisions.
Other axial regions and the complementary nonlocal domain still need their
own argument. The present results do not establish global non-Rupertness.
