# Gaussian majorisation: paired rank and a half-order obstruction

This package advances the dimension-three frontier in
[Aishwarya–Li, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
It does **not** prove or disprove the full conjecture and does not claim a new
Kneser–Poulsen case. The written arguments are complete proof attempts awaiting
external review.

[PROOF.md](PROOF.md) establishes three linked results:

1. Full Gaussian majorisation holds when the paired support `(x,T(x))` has
   affine dimension at most five. This includes every measure on at most six
   atoms. Any failure has a finite rational witness with strict pair contractions,
   at least seven atoms, and paired rank six.
2. In full rank six, retaining exactly three auxiliary Gaussian coordinates
   gives all Gamma(3/2) density-value comparisons. Equivalently, a half-order
   smoothing of every hinge deficit is nonnegative. These tests include convex
   energies outside the source's integer pressure class `PC_2`.
3. This half-order smoothing cannot be cancelled for arbitrary probability
   densities. An explicit normalized pair satisfies all the smoothed tests and
   all positive-order Rényi comparisons, but its hinge deficit at threshold 2
   is exactly `-1/40`.

The negative example consists of step densities, not a Gaussian-contraction
pair. It rules out an inference from the lifted comparisons alone. The missing
bridge must use additional structure of the related Gaussian mixtures.

The concurrent [Team B bridge-barrier result](../gaussian_majorisation_bridge_barrier/PROOF.md)
already supplies entropy-only and `PC_2` obstructions. The present package adds
the paired-rank reduction and an obstruction after retaining the stronger exact
three-coordinate marginal comparison. The results have complementary scopes.

## Reproduce

Run from this directory with Python 3.11 or later, standard library only:

```sh
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

Both Python modes produce [EXPECTED.json](EXPECTED.json) exactly. Tested with
CPython 3.11.2 and 3.12.14. The checks cover:

- all 120 distances of the 16-label simplex-flap fixture, including its 42
  strict deficits and paired rank six;
- a 27-point rank-five contraction and 127 subsets of an absolute-value fold;
- exact mass normalization, the `-1/40` hinge gap, and the polynomial certificate
  for every positive Rényi order;
- 32 validated Gamma comparisons at thresholds `2^(k/4)`, `-20 <= k <= 11`.

The Gamma calculations use rational arithmetic throughout. The logarithm is
enclosed with 96 terms of the positive `atanh(1/3)` series and a geometric tail.
Square roots use 200-bit rational brackets. Degree-100 and degree-101 Taylor
polynomials for `exp(-u)` are integrated exactly against `sqrt(u)`; the
Lagrange remainder fixes their directions for all nonnegative `u`. Each sampled
gap enclosure has width below `10^-40`. The common positive Gamma normalizing
factor is omitted because the checks only compare signs.

Canonical rounded sample-enclosure SHA256:
`bbb25b2474511d86acfcbb512a4f36e512677032a05f691184800c4443593cd4`.
The universal all-threshold obstruction is proved by four analytic regimes in
PROOF.md; it is not inferred from these samples.

## Handoff for geometric and experimental work

[flap_fixture.json](flap_fixture.json) contains exact integer input/output
coordinates, labels, and uniform weights for the classical simplex-flap
contraction at depth one. All weights may be varied while keeping the same
pairwise contraction; coincident output labels must retain their total mass.
The construction and its nonliftability theorem are due to prior work described
in [Cheng–Tan–Zheng, Theorem 2.1](https://arxiv.org/abs/1107.0140).
The fixture is an input for further research, not a counterexample or a claim
that majorisation has been settled on that family.

Paired rank six is only a necessary condition for a counterexample. The checker
includes a rank-six map built from ordinary hyperplane folds, for which another
low-dimensional continuous motion is available. Do not reject a positive
result or infer nonliftability merely from the paired-rank test.

The rank-five geometric union-volume consequence follows from established
continuous-lifting results. The open campaign objective remains a full
three-dimensional theorem or counterexample, or a broad class with a genuinely
new Kneser–Poulsen consequence.

## Dependencies and trust

The mathematical input is Aishwarya–Li's continuous-contraction theorem. The
rank interpolation, Gamma identities, rational-witness approximation and
noncancellation proof are written out. The global-map version of the finite
witness reduction uses Kirszbraun extension. The cited simplex-flap
nonliftability theorem is not reproved by the finite checker.

This is not a proof-assistant formalization or independent peer review. Exact
computation validates the stated finite identities and enclosures. It does not
prove the continuum theorem, demonstrate publication priority, or establish
the full conjecture. No downloaded papers, binary tools, private graph state,
raw search logs, or large generated artifacts are included.
