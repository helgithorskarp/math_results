# Review package: local Firey-area reconstruction

This directory contains an independent high-confidence review of
[`firey_area_reconstruction`](../firey_area_reconstruction/).

The review audits the nonsmooth supported-polar-hull lemma, directional
coefficient growth, finite-rank moment criterion, explicit radius recovery,
sharp jet order, affine covariance, and the `L_p` surface-area uniqueness
corollary. The verdict, complete human-premise list, limitations, and proposed
strengthenings are in [`REVIEW.md`](REVIEW.md).

## Reproduction

Use CPython 3.11.2 or later; only the standard library is required.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 audit_independent.py > actual.json
diff -u EXPECTED_OUTPUT.json actual.json
PYTHONDONTWRITEBYTECODE=1 python3 -O audit_independent.py > actual-optimized.json
diff -u EXPECTED_OUTPUT.json actual-optimized.json
sha256sum -c SHA256SUMS
```

The checker imports no target module and implements no decoder. It completely
enumerates a declared bounded lattice-polygon catalogue, derives polar moment
data from oriented edges, performs exact collision tests for full jets and
highest terms, verifies Gram ranks and radius ratios, and includes smooth-disk
and regular-polygon adversaries.

No solver, third-party package, randomness, floating point, external input,
generated database, or omitted certificate is used.
