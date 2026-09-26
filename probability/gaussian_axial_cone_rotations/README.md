# Axial cone rotations: Gaussian majorisation and ball volumes

This packet gives explicit four- and five-dimensional contracting motions
for a broad class of three-dimensional central reflections. It proves full
Gaussian majorisation at every variance and threshold, and Kneser--Poulsen
inequalities for unions and intersections of balls with arbitrary individual
radii. The general dimension-three conjecture remains open.

The latest [matrix-path extension](MATRIX_PATHS.md) keeps the original
undamped endpoints and extends the circular range to

```text
p q <= 1/(1+cos(1)) = 0.649223...    (angle in radians).
```

It supplies a support-cost principle for general compact cone sections.
A transverse operator-norm boundary path has an explicit isometric lift
in R5; its optimal circular cost is `2(1+cos(1))`, below the old rotation
cost `pi`. This is the exact boundary for block-diagonal relative Gram
motions, including arbitrary continuous time parametrizations. Arbitrary
R5 motions and the full majorisation question remain open. The numerical
range extension is modest; the matrix-path principle is the new mechanism.

For centrally symmetric planar convex bodies `P,Q` containing zero in their
interiors, put

```text
C(P) = {(z u,z): z >= 0, u in P},
W(P,Q) = convex hull {conjugate(u) v: u in P, v in Q}   (complex products).
```

If `perimeter(W(P,Q)) <= 4`, the map fixing `C(P)` and sending `-b` to `b`
for `b in C(Q)` has the claimed motion and comparisons. Probability weights,
atom counts, and bounded nonatomic laws are unrestricted. The perimeter
criterion is sharp within the specified axial rotation form, not claimed
necessary for arbitrary motions or majorisation.

For circular cones `C_p = {(u,z): z >= 0, |u| <= p z}`, the original R4
rotation criterion becomes

```text
p q <= 2/pi.
```

Writing `a=(a_perp,a_z)` for a fixed point, the moving image of `-b` is

```text
F_t(b) = (R_theta(t) b_perp, -cos(pi t) b_z, sin(pi t) b_z),
theta(t) = (pi/2)(1 + cos(pi t)),       0 <= t <= 1.
```

Each cluster is rigid; the cross inner products increase. The interval
`1/2 < pq <= 2/pi` lies beyond every simplicial separator for the full
circular cones. A rational 25-point example with `p=3/4,q=4/5` demonstrates
this additional scope even for a finite configuration. It has paired affine
rank six, admits no motion in three dimensions, and is not a strong
coordinatewise contraction, even after independent rigid alignments.

[COMPOSITIONS.md](COMPOSITIONS.md) strengthens the last comparison to
**every finite composition** of strong contractions in three dimensions,
allowing different rigid alignments at each step. It also excludes arbitrary
successive one-sided hyperplane folds. A general rank-one matrix obstruction
proves this throughout the circular range above `1/2`; the existing finite
fixture has the strict certificate `diag(-8,-8,15)`, with trace `-1` and
minimum dual-generator value `5/27`. This is a limitation of those methods,
compatible with the positive four-dimensional motion.

[ROBUSTNESS.md](ROBUSTNESS.md) extends the motion to controlled nonlinear
changes of the whole source and target domains, with a reserved target
scaling factor. Its explicit finite consequence allows every endpoint of
the existing fixture to move freely within radius `1/2000` about
`(X,(19/20)Y)`. Throughout this full neighborhood, all weights, variances,
thresholds and individual radii are allowed. Four dimensions remain
necessary even after independent endpoint alignments; paired rank six
and the scalar-defect obstruction also persist. This is a quantitative
closure consequence of the axial theorem, using classical contracting
segments, with independent review pending.

Read [SCOPE.md](SCOPE.md) for the consolidated correctness boundary,
breadth, comparison with the current Team B classes, and precise
Kneser--Poulsen claim. The axial and simplicial criteria are not nested;
the standard orthant proves the reverse noncontainment under every common
axis. The existing 25-point fixture also fails the later scalar-defect
criterion. These are comparisons of sufficient methods, not negative
Gaussian inequalities.

Read [PROOF.md](PROOF.md) for the full proof and qualifications, and
[SOURCES.md](SOURCES.md) for primary inputs, team dependencies, and novelty
scope. The Gaussian lifting implication is due to Aishwarya--Li; the
arbitrary-radius volume implication is due to Bezdek--Connelly. The new work
is the motion, its perimeter criterion, and the resulting geometric class.

## Reproduction

From this directory:

```sh
python3 verify.py --check
python3 -O verify.py --check
python3 scope_audit.py --check
python3 -O scope_audit.py --check
python3 composition_audit.py --check
python3 -O composition_audit.py --check
python3 robustness_audit.py --check
python3 -O robustness_audit.py --check
python3 matrix_path_audit.py --check
python3 -O matrix_path_audit.py --check
sha256sum -c SHA256SUMS
```

Standard library only. Checked with CPython 3.11.2 and 3.12.14. Expected:

```text
AXIAL_CONE_EXACT_AUDITS_PASS 50ce427908f4f6e355ea7ed58996954bc2b5ebc72c2ac547417659be6b8196c4
AXIAL_CONE_SCOPE_AUDITS_PASS de6ff71916e4afddfce10a93b3d8e0d9a566c8d08660dd333ea12fdd3ad8da0a
AXIAL_STRONG_COMPOSITION_AUDITS_PASS 754bfdbc1cb7ad7a884003dadc90ddeac33e4b2554d7fd7d2b4a385e24cf66ab
AXIAL_UNIFORM_ROBUSTNESS_AUDITS_PASS 4004b3eb13fc1e1089966da5d33859c607ce0b159e2dba379b3ed3c6b5c640a6
AXIAL_MATRIX_PATH_AUDITS_PASS 148015152cbb1c3a22a75cee680510d272d511a2de841e8f37e4fc7d499aef32
```

Running `python3 verify.py` prints the exact [EXPECTED.json](EXPECTED.json).
The checker audits eight polynomial identities, all 300 fixture pairs,
rank determinants, the polygon and dual polygon defining the separator
obstruction, the noncircular product hexagon, a rational proof of the
`pi < 22/7` bound, and invalid controls. It uses integers and fractions only.
It does not sample Gaussian integrals or infer a universal inequality from
finite numerical checks. The analytic proof and the two primary lifting
theorems are the mathematical trust boundary. No external dataset, solver,
large certificate, or proof assistant is needed for these supplementary
checks. Independent mathematical review is pending.

The consolidation leaves the original `verify.py` and `EXPECTED.json`
unchanged. The new [scope_audit.py](scope_audit.py) and
[EXPECTED_SCOPE.json](EXPECTED_SCOPE.json) record the scalar-obstruction
matrix (rank six, determinant `-288/25`), an identity-map positive control,
and a distinct positive weight certificate for the common-target comparison.
The all-axis orthant exclusion is a written proof in Section 4.1, not an
axis search. These are supplementary author audits, not independent review.

The new [composition_audit.py](composition_audit.py) checks the dual polygons
by all boundary-line pairs, every one of the 144 generator tests, and a
rotated-orthant positive control with independent frames and a moving origin.
Two invalid matrix certificates are rejected. Its compact output is
[EXPECTED_COMPOSITIONS.json](EXPECTED_COMPOSITIONS.json). The exclusion of
every finite chain length follows from the written telescoping proof, not
from a bounded search over possible factorizations.

The [robustness_audit.py](robustness_audit.py) checks the uniform nonlinear
reserve, all reference separations, seven free-polynomial identities,
the orientation and rank margins, and the scalar contradiction. A separate
enclosure verifies all 128 corners of the two tetrahedral squared-edge
boxes by exact principal minors. [EXPECTED_ROBUSTNESS.json](EXPECTED_ROBUSTNESS.json)
records the compact evidence. No grid of endpoint perturbations is used;
all such perturbations are covered by the written uniform inequalities.

The [matrix-path audit](matrix_path_audit.py) verifies fourteen polynomial
identities and 150 direct rational isometric frames, including rank drops
and the endpoints. Its new 25-site certificate has paired minor
`209952/15625`, product perimeter lower bound `253379/62500`, and dual
certificate margin `935/729`. These support the universal proof in
[MATRIX_PATHS.md](MATRIX_PATHS.md); neither a path grid nor a Gaussian
quadrature is a premise. The four earlier checkers and expected outputs
are unchanged. All verification is author work, not independent review.
