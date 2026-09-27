# Compact rigidity and universal eventual Gaussian majorisation

The [author proof](PROOF.md) establishes that a 1-Lipschitz map on a compact
Euclidean set preserves Gaussian mean width only if it preserves every pair
distance. An integrable exponential of the symmetrized graph support function
supplies the equality rigidity missing from a finite approximation argument.

Combining this with the accepted spherical comparison and eventual endpoint
gives full Gaussian-convolution majorisation for **every compactly supported
law in R3 at every sufficiently large variance**, simultaneously at every
threshold. The cutoff depends on the law and map. There is also a strict
large-equal-radius union/intersection KP theorem for arbitrary compact center
families. This does not settle unrestricted all-variance majorisation or
all-radius KP. Independent review and historical priority are pending.

The [handoff](HANDOFF.md) identifies the changed frontier and review boundary;
[sources](SOURCES.md) and [INPUTS.json](INPUTS.json) credit and pin dependencies.

Reproduce the compact exact algebra checks using Python 3.11, standard library
only, from this directory:

```sh
python3 -B verify.py > /tmp/compact-width-check.json
cmp /tmp/compact-width-check.json EXPECTED.json
python3 -B -O verify.py > /tmp/compact-width-check-opt.json
cmp /tmp/compact-width-check-opt.json EXPECTED.json
sha256sum -c SHA256SUMS
```

Expected status: `COMPACT_WIDTH_RIGIDITY_ALGEBRA_PASS`. These checks test finite
algebra, normalization, cutoff arithmetic and failure controls; they are not
a formal or independent verification of the analytic proof. No external data,
large computation, numerical quadrature, solver or hidden corpus is required.
