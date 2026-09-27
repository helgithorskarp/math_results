# Uniform Gaussian hinge reconstruction from finitely many moments

[PROOF.md](PROOF.md) gives an author proof of a positive polynomial
reconstruction with uniform error proportional to inverse degree. This
replaces the fourth-root rate in the team's earlier sufficient moment
certificate. Independent review of this new application is pending.

- Every bounded radius: `||J_p H-H|| <=6(R/sqrt(s)+2)^3/p`.
- For `R^2/s<=1/2`: `||J_p H-H|| <=6d L_epsilon/p`, with explicit L,
  and d the dimensionless mean squared-distance loss.
- The polynomial has degree `2p-2` and uses only the existing ordinary
  hinge moments. Its kernel is positive and its coefficients are rational.
- R3 paired cubature and the new rate give a sufficient
  `O_epsilon(zeta^-3)` atom budget for whole-curve error `d zeta`, improving
  the earlier sufficient `O_epsilon(zeta^-12)` composition.

This is uniform coverage of all thresholds, not a new local sign window.
It supplies no unknown positive margin. All-radius **loss-proportional**
coverage, unrestricted majorisation and a new Kneser--Poulsen consequence
remain unproved. Large constants and the cost of high-order exact moments
can still prevent a practical complete cover.

The Jackson operator and spherical addition formula are classical. The
new-to-team content is their explicit Gaussian angular estimate and
loss-proportional certification composition; no historical-priority claim
is made. [SOURCES.md](SOURCES.md) distinguishes analytic premises from
contextual team results.

Reproduce with CPython 3.11 or later, standard library only, in this directory:

```sh
python3 -B verify.py
python3 -B -O verify.py
sha256sum -c SHA256SUMS
```

[verify.py](verify.py) compares its deterministic result with
[EXPECTED.json](EXPECTED.json). Both modes print
`JACKSON_GAUSSIAN_CERTIFICATION_PASS`. Exact controls compare the Legendre
construction to direct azimuth integration, check rational remainder
budgets and malformed-input rejection, and enclose Gaussian moments for
two-atom contractions through `t=1-2^-60`. These controls do not prove the
universal analytic bounds or supply a new positive Gaussian class.

For R2, `reconstruct(p, moments)` constructs the rational polynomial;
`propagate(p, radii)` bounds moment enclosure error uniformly in threshold;
`certify_lower(poly,a,b,bound)` checks a proposed polynomial bound on a
whole interval by exact Bernstein subdivision. All numerical inputs to
these routines must be exact rationals. A failed subdivision returns
`None` and is inconclusive. To sign H on[a,b], its polynomial lower bound
must cover **both** reconstruction error and moment enclosure error.
Signs at the original law's remaining endpoints are a separate premise.

For R3, equations(10)--(15) of the proof give the retained-loss cubature
error and an explicit safe degree. At `p=16, epsilon=1/2`, the exact
reconstruction-only tolerance `2^-10` uses `q=47`, hence 294879 retained
pairs. The angular reconstruction error must still be added; this number
does not certify the whole curve to that tolerance or claim practical
cubature construction. Ordinary rounding of sites or weights is outside
the retained-loss guarantee.

Only the compact source and deterministic record are published. Exploratory
notes, node data and publication logs are private. The prior spherical
transfer is preserved and independently accepted, but is not a premise
of this different reconstruction theorem.
