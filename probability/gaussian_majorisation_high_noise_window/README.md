# High-noise majorisation above an explicit density threshold

For every probability measure supported in a radius-`R` ball in `R^3`
and every 1-Lipschitz map, the author proof compares all Gaussian hinge
energies at variance `s>=2R^2` above the threshold

\[
 C_s\exp\!\left[-\frac{(4-5R^2/s)^2}
                         {32(R^2/s)(1-R^2/s)}\right],
 \qquad C_s=(2\pi s)^{-3/2}.
\]

The exponent equals `s/(2R^2)-3/4+O(R^2/s)`. Thus the uncontrolled interval
is exponentially small in the noise-to-radius ratio. There is no bound
on the number of atoms, no lower atom-weight assumption, and no restriction
to polynomial energies.

The proof inverts the exact six-dimensional lifted moment formula through
a weighted coarea profile. A radius bound makes its half derivative
nonnegative up to a specified level. It also gives a quantitative hinge
gap and, using the team's spherical-tail limit,

\[
 S_\mu(\lambda)-S_{T_\#\mu}(\lambda)
 \geq \frac{D\lambda^2}{12}(1-\lambda R)e^{-4\lambda R}
 \quad (0\leq\lambda R\leq1),
\]

where `S_mu(lambda)` is the spherical average of the log moment-generating
function and `D` is the expected squared pair-distance loss.

The full three-dimensional conjecture, the remaining lower thresholds,
and the spherical comparison for `lambda R>1` remain open. This is a
complete analytic author proof awaiting independent review, not a
formalized or computer-assisted universal theorem. No new Kneser--Poulsen
case is claimed. See [PROOF.md](PROOF.md) for all assumptions and
[SOURCES.md](SOURCES.md) for prior and team dependencies.

## Reproduce the compact audits

From this repository's root, using CPython 3.11.2 (standard library only):

```sh
python3 probability/gaussian_majorisation_high_noise_window/verify.py > probability/gaussian_majorisation_high_noise_window/actual.json
cmp probability/gaussian_majorisation_high_noise_window/EXPECTED.json probability/gaussian_majorisation_high_noise_window/actual.json
python3 -O probability/gaussian_majorisation_high_noise_window/verify.py > probability/gaussian_majorisation_high_noise_window/actual-optimized.json
cmp probability/gaussian_majorisation_high_noise_window/EXPECTED.json probability/gaussian_majorisation_high_noise_window/actual-optimized.json
```

For the local manifest, run `sha256sum -c SHA256SUMS` from this directory.
Generated `actual*.json` and Python caches are ignored.

The checker pins and imports the adjacent team's rational interval and
exponential code. It adds rational logarithm, square-root, and Machin-pi
enclosures. No floating-point arithmetic affects any decision. It checks
two polynomial identities, five normalization factors, a rational parameter
table, and elementary controls. It then certifies the actual hinge gap
and the claimed lower bound for `mu=(delta_-e1+delta_e1)/2`, `T=0`, `s=10`
at normalized thresholds `exp(-1)`, `exp(-2)`, and `exp(-4)`.

Those three integrals are checked by a separate one-dimensional formula,
after integrating the two transverse Gaussian coordinates exactly. A
global second-derivative bound encloses the composite-midpoint quadrature
error on all 256 cells; the proof of the bound and the tail cutoff are
documented in the code. The strict margins are recorded in
[EXPECTED.json](EXPECTED.json). Assertions are not used for correctness,
and normal and optimized Python outputs agree.

These finite controls check signs and normalization independently of the
coarea implementation, but do not establish its universal analytic claims.
There is no hidden search dataset, external service, or omitted large
certificate needed to reproduce them.
