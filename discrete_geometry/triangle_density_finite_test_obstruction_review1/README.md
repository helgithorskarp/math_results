# Review package: finite triangle-test obstruction

This directory contains an independent high-confidence review of
[`triangle_density_finite_test_obstruction`](../triangle_density_finite_test_obstruction/).
The reviewed target source commit is
`c2c6643e6aa4effff285d9eeddf2502d57197dd4`.

The review audits the imported triangle-density criteria, preservation of
negative instances, simultaneous binary-form similarities, multiquadratic
common norms, the effective nonsquare-value lemma, near-identity scaling,
the countable fixed suite, and the adaptive-query corollary. The verdict,
complete human-premise list, adversarial tests, limitations, and proposed
strengthenings are in [`REVIEW.md`](REVIEW.md).

## Reproduction

Use CPython 3.11 or later; only the standard library is required.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 audit_independent.py > actual.json
diff -u EXPECTED_OUTPUT.json actual.json
PYTHONDONTWRITEBYTECODE=1 python3 -O audit_independent.py > actual-optimized.json
diff -u EXPECTED_OUTPUT.json actual-optimized.json
sha256sum -c SHA256SUMS
```

The checker imports no target module or fixture. The target multiplies Galois
conjugates in a bit-mask field model. This checker instead obtains full norms
as characteristic polynomials of multiplication matrices and relative norms
as determinants over the relevant quadratic subfields. It uses exact rational
arithmetic throughout.

No solver, third-party package, randomness, floating point, network input,
generated database, or omitted certificate is used.
