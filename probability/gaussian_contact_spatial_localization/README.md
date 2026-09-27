# Law-independent finite witnesses from adverse Gaussian contacts

[PROOF.md](PROOF.md) gives a spatial posterior cover for R7's accepted
two-rigid-body contact transfer. A certified adverse joint-level volume
gap yields an actual finite common-variance Gaussian counterexample with
an explicit atom bound depending only on radius, variance range, threshold
floor and volume margin. It has no dependence on the input atom count or
minimum weight, and applies to diffuse laws and critical levels. An
optional output construction has rational centres, images, variance and
priors when the bodies have rational convex-hull presentations.

**Status:** complete author proof, independent review pending. No adverse
contact is supplied. No new positive sign class or Kneser--Poulsen theorem
is proved. The full R3 majorisation conjecture and its accepted global
adverse-defect cap remain unchanged.

For source bodies in B(0,R), variances in [1,S] and normalized levels at
least 2^-J, put U=ceil sqrt(2SJ), B=R+U. If a source joint contact remains
adverse after logarithmic threshold tightening eta, the cover uses at most

    2(2Bm+1)^3 centres,    m=ceil sqrt(3R^2/(8eta)).

A critical-level strip estimate chooses eta explicitly from an untightened
adverse margin delta. At fixed R,S,J, the resulting atom bound is polynomial
in inverse delta, with exponent O(R^2+J). This replaces the earlier
posterior-simplex grid's dependence on all original atom weights and count.
The new Gaussian witness changes priors, centres within the bodies and
variance; it does not assert an adverse hinge for the original priors.

The classical Gaussian ball envelope and its posterior centres are credited
to the primary literature. The added information is the uniform cover and
the effective, contraction-preserving finite-witness budgets. See
[SOURCES.md](SOURCES.md) and [HANDOFF.md](HANDOFF.md).

## Reproduction

From this directory, with CPython 3.11 or later, standard library only:

~~~sh
python3 -B verify.py
python3 -B -O verify.py
sha256sum -c SHA256SUMS
~~~

Expected status: SPATIAL_CONTACT_LOCALIZATION_CONTROLS_PASS.
[EXPECTED.json](EXPECTED.json) has SHA256
f82526dec9a4e74e45181a9bd4070d9f4983b9a1fa379b8d594a1a1128c1d473.
The exact controls check logarithmic and square-root ceilings, grid
coverage, posterior covariance algebra, barycentric contraction, rational
rounding, shell volumes, strip remainders and five symbolic schedules.
Thirteen invalid inputs are rejected and four dependency files are pinned.
The analytic proof is unformalized; this program is not a contact-volume
oracle or independent review.

The callable functions in [verify.py](verify.py) distinguish an already
tightened adverse datum from an untightened one. No adverse premise is
inferred merely by passing parameters to them. No enormous grid or
denominator is allocated.

For illustration only, R=1,S=4,J=3,eta=1/16 gives at most 101306 centres.
An already tightened adverse gap 1/100 would permit variance 2^-32.
Without supplied tightening, the conservative critical-level schedule at
the same R,S,J and delta gives eta=2^-20780 and atom cap 2^31185.
These are conditional cardinality bounds, not found counterexamples or
practical search sizes. An arbitrary diffuse law still needs a certified
representation or integration oracle to implement the posterior choices.
