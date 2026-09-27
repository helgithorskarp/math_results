# Norm-preserving contractions: all Gaussian variances and thresholds

This author proof gives full Gaussian majorisation for every bounded law
in R3 whenever the contraction preserves each point's distance to a
supplied anchor, allowing independent source and target anchors. It also
gives both Kneser--Poulsen volume inequalities for arbitrary individual
ball radii in that class and claims both area inequalities for arbitrary
spherical caps on S2. Independent review and historical priority are pending.
The unrestricted non-norm-preserving Gaussian question remains open.

[PROOF.md](PROOF.md) proves a stronger statement: at each spatial radius,
the angular source density is below the angular target density in convex
order, at every Gaussian variance. Equal anchored norms cancel the diagonal
Gram terms in [R1's positive spherical difference](../gaussian_spherical_sinc_comparison/PROOF.md).
The off-diagonal terms then sign every convex function of a sum of
exponentials, including smoothed hinges. No contracting motion is assumed.

The spherical-cap consequence is not a citation to a known unrestricted
cap theorem. Its complete author derivation is in Section 5 of the proof.
[SOURCES.md](SOURCES.md) distinguishes it from the restricted primary results
we checked. R1's identity is an essential dependency, independently accepted
at graph6506 during preparation. That review does not review our new claims.

## Reproduce the exact finite evidence

Run in this directory with CPython 3.11.2, standard library only:

```sh
python3 -B verify.py
python3 -B -O verify.py
python3 -B verify.py --input INPUT.json
sha256sum -c SHA256SUMS
```

The first two commands must match [EXPECTED.json](EXPECTED.json), status
`EXACT_NORM_PRESERVING_CHECKS_PASSED`, record SHA256
`90d3be5cdebcc8d3231e2ed04e6916674615a136e8a4d81e7793d503ea33186d`.
The suite checks six exact geometries and 112 unordered pairs, including
paired affine rank six, independent isometries, unequal radial scales,
a fixed anchor in the support, congruent data and one point. It also checks
54 Gram/Hessian identities, 336 Boolean mixed-derivative identities and
nine rejected inputs. The run takes below one second here.

The input fixture is a coordinate fold of seven rational unit vectors
with unequal positive weights. It is a calibration, not a newly discovered
hard instance or an exclusion from prior positive classes. No sampled
Gaussian hinge, cap area or Euclidean volume is used as proof evidence.

## Minimal R2/R3/R8 handoff

R2 can call `verify.py --input file.json` on the schema in
[INPUT.json](INPUT.json). Integer values and exact rational strings are
accepted; floating-point values are rejected. Success certifies the finite
hypotheses for all variances and thresholds under the analytic author
theorem, not the theorem's formal correctness. Failure decides no other
class. Supplied real anchors are allowed by the theorem; the checker uses
rational witnesses and does not search for anchors.

R3 can apply the theorem to bounded diffuse laws when the anchor equality
holds on the original support. Approximations chosen on that support keep
the condition exactly. Moment-matching cubature alone is not asserted to
preserve it. The old R3/R8 effective cutoffs stay consolidated and unchanged.

R8 owns this functional passage from the spherical operator to actual
fixed-variance hinge signs. The positive operator itself is R1's work.
The exact code verifies finite algebra and hypotheses; smooth approximation,
the operator identity, bounded-law limits and polar integration are written
mathematics, not proof-assistant output or independent peer review.
