# Finite-atomic low-noise exclusion

For **every fixed noncongruent finite contraction in R3**, every fixed
complete Gaussian endpoint Hankel matrix is positive definite at all
sufficiently small variances. Tight nearest pairs and target collisions
are included. The polynomial coefficients may vary with variance.

This excludes bounded-degree globally convex polynomial counterexamples
on explicit uniform regions. It does **not** prove full Gaussian
majorisation at a fixed variance or a new Kneser--Poulsen consequence.
The author proof is complete; independent review and priority are pending.

With minimum mass at least `2^-b` and curvature-square root degree D:

* For distinct targets, put `beta=min min(target squared distance, positive
  squared loss)`, over the shortened pairs. It suffices that
  `beta/s>=8D(D+1)(2D+1)[(2D+2)b+ceil(log2(2D))]`.
* With a target collision, let delta be the smallest positive squared
  distance in either cloud. It suffices that `delta/s>=108bD`.

The new step controls the **least active replica scatter** when nearest
pairs are tight. A third site can dominate only through two preserved
legs; the parallelogram identity then gives the required exponent
curvature. A separate merger-limit argument handles every collision
pattern. Both routes end in full finite-matrix positivity.

Read [PROOF.md](PROOF.md) for exact margins and quantifiers, and
[SOURCES.md](SOURCES.md) for dependencies and comparison with prior work.

Reproduce with Python 3.11+ and its standard library:

```sh
python3 -B verify.py --check
python3 -B -O verify.py --check
sha256sum -c SHA256SUMS
```

Expected marker: `FINITE_ATOMIC_LOW_NOISE_EXCLUSION_EXACT_PASS`.
[EXPECTED.json](EXPECTED.json) contains the exact inputs, boundary cutoffs,
finite control counts and hashes. The checker verifies rational algebra,
finite replica minima and independent Gram-inversion identities. It does
not numerically integrate Gaussian energies or formally verify the
universal written proof. No external dataset or private computation is
required.
