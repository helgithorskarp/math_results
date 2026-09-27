# Quantitative polarization and Gaussian mean-loss margins

The [constructive proof](EFFECTIVE.md) makes the constants in the
[original compactness theorem](PROOF.md) explicit through a quantitative
midpoint reflection inequality and robustness to a small exceptional mass.
R3's concurrent [effective theorem](../gaussian_effective_mean_loss/PROOF.md)
already signs the same full parameter family by a different argument, with
better constants in its worked example. This packet supplies an alternative
proof and compressed certificate; it claims no further signed class.

At unit Gaussian
variance, every centered bounded law with radius at most 1 and source
covariance at least `I/32`, and every contraction of mean pair loss
`D<=2^-567`, satisfy

```
L_target(v) - L_source(v) >= 2^-69 v D,    0 < v <= 4 pi/3.
```

The same bound holds on the actual aligned source top set. The general
rational schedule works for every positive radius, covariance floor and
finite volume bound. It includes diffuse laws and rare points moving a
fixed distance; no minimum atom mass or second-loss-moment guard is used.
The cutoff is conservative, and full dimension-three majorisation remains
open. Independent mathematical review of this constructive continuation
is pending. The original qualitative theorem has been independently
[accepted](../gaussian_mean_loss_margin_review2/REVIEW.md).

[effective.py](effective.py) computes the cutoff as a compressed exponent
and optionally checks finite rational source/target data. A failed guard
returns `UNRESOLVED`. Passing signs the specified volume range and, when
requested, every hinge above the specified positive threshold. It does
not sign the remaining low-threshold tail.

From the repository root, with standard-library Python 3.11:

```sh
python3 probability/gaussian_mean_loss_margin/effective.py --radius 1 --covariance 1/32 --volume-radius 1
python3 probability/gaussian_mean_loss_margin/effective.py --radius 1/2 --covariance 1/384 --threshold-bits 6
python3 probability/gaussian_mean_loss_margin/effective_check.py
python3 -O probability/gaussian_mean_loss_margin/effective_check.py
```

The first schedule returns cutoff exponent 567 and margin exponent 69.
The second returns cutoff exponent 967, and signs `H(u)>=0` for `u>=1/64`.
Its uniform middle margin is `H(u)>=2^-124 D` on `[1/64,1/2]`.
Neither example is an optimized cutoff or a numerically sampled sign.

To check finite data, append `--input file.json`. Its fields are `sources`,
`targets`, `weights`, and optional positive `variance` (default 1).
Coordinates and weights must be exact strings or integers. Radius,
covariance and volume parameters are in Gaussian-normalized coordinates.
The checker validates every active pair contraction and the source
radius/covariance before testing the loss. Zero-weight labels are omitted.
It centers the source itself; no supplied alignment is trusted.

[effective_check.py](effective_check.py) checks expanded rational budgets
against the compressed schedule, finite-input branches, the exact repair,
reflection algebra and rejection controls. Both normal and optimized runs
must print `EFFECTIVE_MEAN_LOSS_CHECKS_PASS` with the same record hash.
[EFFECTIVE_EXPECTED.json](EFFECTIVE_EXPECTED.json) is the compact output.
These checks are author validation, not an independent proof of the
universal analytic theorem.

The prior exact controls remain available:

```sh
python3 probability/gaussian_mean_loss_margin/verify.py
python3 -O probability/gaussian_mean_loss_margin/verify.py
```

They must print `MEAN_LOSS_MARGIN_CONTROLS_PASS` and match
[EXPECTED.json](EXPECTED.json). [SOURCES.md](SOURCES.md) records attribution,
the credited first variation and the R2/R3/R8 interface. [SHA256SUMS](SHA256SUMS)
lists the compact source hashes. No external dataset, Gaussian quadrature,
solver, proof-assistant formalization or credentials are required.
