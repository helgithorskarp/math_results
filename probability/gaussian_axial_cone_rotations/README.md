# Axial cone rotations: Gaussian majorisation and ball volumes

This packet gives an explicit four-dimensional contracting motion for a
broad class of three-dimensional central reflections. It proves full
Gaussian majorisation at every variance and threshold, and Kneser--Poulsen
inequalities for unions and intersections of balls with arbitrary individual
radii. The general dimension-three conjecture remains open.

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

For circular cones `C_p = {(u,z): z >= 0, |u| <= p z}`, this becomes

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
sha256sum -c SHA256SUMS
```

Standard library only. Checked with CPython 3.11.2 and 3.12.14. Expected:

```text
AXIAL_CONE_EXACT_AUDITS_PASS 50ce427908f4f6e355ea7ed58996954bc2b5ebc72c2ac547417659be6b8196c4
AXIAL_CONE_SCOPE_AUDITS_PASS de6ff71916e4afddfce10a93b3d8e0d9a566c8d08660dd333ea12fdd3ad8da0a
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
