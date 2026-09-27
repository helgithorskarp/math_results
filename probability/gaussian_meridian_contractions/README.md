# Full Gaussian and Kneser--Poulsen comparison for meridian contractions

**Complete author proof; independent correctness and priority review pending.**

Every rotationally equivariant 1-Lipschitz map preserving azimuth around
an axis and using a nonnegative transverse radius has an analytic contracting motion
in two extra dimensions. The exact hypothesis is a planar contraction
`S(r,z)=(rho,zeta)` with `0<=rho<=r` on the meridian domain. Both output
coordinates may depend nonlinearly on both input coordinates.

The [proof](PROOF.md) gives full Gaussian majorisation at every variance
and threshold for arbitrary bounded laws, and both Kneser--Poulsen union
and intersection inequalities for arbitrary individual ball radii.
**Neither the law nor the selected centers need rotational symmetry.**
The theorem holds in every dimension n>=2, using a motion in R^(n+2).

The class includes latitude folds with arbitrary reversals and nonlinear
coupled maps on all of R3. A seven-label certificate has paired affine
rank six and defeats the direct scalar-defect test. The new input is a
uniform meridian lifting identity; the planar leapfrog and both transfers
are credited antecedents. Arbitrary changes of azimuth and the unrestricted
three-dimensional question remain open. No exclusion of all compositions
of known classes or historical-priority claim is made.

From this directory, standard-library Python 3.11 or later:

```sh
python3 -B verify.py
python3 -B -O verify.py
sha256sum -c SHA256SUMS
```

Both runs must print `MERIDIAN_CONTRACTION_CHECKS_PASS` and reproduce
[EXPECTED.json](EXPECTED.json). The checker audits exact polynomial
identities, finite geometry and rejected invalid controls. The continuum
proof and primary-source transfers remain written mathematics.
See [SOURCES.md](SOURCES.md) for attribution and scope boundaries.
