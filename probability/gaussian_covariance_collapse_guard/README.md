# Exact Gaussian sign guard near marginal covariance collapse

**Author proof; independent acceptance pending.** This gives a uniform
middle-threshold sign for every bounded probability law whose source or
target is sufficiently close to a plane in mean square.

Normalize covariance by the Gaussian variance s, and let d be the mean
squared-distance loss divided by s. If the centered source radius is at
most `sqrt(s)/2`, d>0, and either marginal has a unit direction with

```
directional variance / s <= 2^-86 d^2,
```

then the favorable hinge gap satisfies `H(u)>=2^-42 d` for **every**
`u in [1/64,1/2]`, and `H(u)>=0` for all `u>=1/64`. The proof covers
diffuse laws, arbitrary priors and rare outliers. There is no covariance
floor or small-loss assumption. Zero loss gives equality.

The [proof](PROOF.md) transfers a quantitative rank-five margin through
an actual contraction of a projected source or target. The source case
uses `T(PX)`, not the potentially expanding matching `PX -> T(X)`.
No low-dimensional motion for the original rank-six data is asserted.

Consequently, an adverse middle hinge at positive loss requires **both**
normalized covariance matrices to be strictly above `2^-86 d^2 I`.
This removes covariance collapse from any compact region with a fixed
positive loss floor. It does not settle the joint zero-loss boundary,
low thresholds or the full dimension-three conjecture.

## Reproduce

Standard-library CPython 3.11 or later, from the repository root:

```sh
python3 -B probability/gaussian_covariance_collapse_guard/verify.py
python3 -B -O probability/gaussian_covariance_collapse_guard/verify.py
python3 -B probability/gaussian_covariance_collapse_guard/guard.py probability/gaussian_covariance_collapse_guard/TARGET_THIN.json
```

The first two reproduce [EXPECTED.json](EXPECTED.json), print
`COVARIANCE_COLLAPSE_GUARD_PASS` and a canonical record hash. The last
returns an exact direction and margin certificate for the compact
[target-thin control](TARGET_THIN.json). From this directory,
`sha256sum -c SHA256SUMS` checks all packet bytes.

Input fields are `sources`, `targets`, `weights`, and optional positive
`variance` (default 1). Coordinates and weights must be integer or rational
strings. The guard checks all positive-mass pairs and the centered source
radius. Exact completion of squares finds a rational direction whenever
either covariance matrix fails the strict lower bound. It uses no
floating-point eigenvalues or Gaussian quadrature.

Outputs are `SIGNED_MIDDLE`, `ISOMETRIC_ZERO`, or `UNRESOLVED`.
Malformed data or an expanding pair are rejected. A failed guard is not
a counterexample. The verifier checks witnesses by direct ordered-pair
formulas, independently of the producer's centered-moment calculation.

Finite controls cover 1,728 exact symmetric matrices, singular equality,
source and target projection branches, a rare outlier, scaling, translation,
zero masses, and corrupted data. The three signed controls have paired
rank six and exceed the worked small-loss and Q/d cutoffs. They are
calibrations, not newly discovered map classes. The universal analytic
reduction remains written mathematics, not formalized or independently
accepted. See [HANDOFF.md](HANDOFF.md), [SOURCES.md](SOURCES.md) and
[INPUTS.json](INPUTS.json).

A saved guard record can also be checked separately with
`python3 -B verify.py --input TARGET_THIN.json --certificate record.json`
from this directory. This validates signed witnesses by ordered-pair sums;
an `UNRESOLVED` record asserts no sign and is not an exclusion certificate.
