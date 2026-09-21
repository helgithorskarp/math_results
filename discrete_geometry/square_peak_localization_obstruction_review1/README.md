# Review package: square peak-localization obstruction

This directory contains an independent high-confidence review of
[`square_peak_localization_obstruction`](../square_peak_localization_obstruction/).
The reviewed source is commit
`0304625ef7389aea66942690ed14d7befdf6b22b`.

The review checks the geometric reduction, exact finite classification,
singular-case completeness, protected-band stability argument, and Bernstein
polynomial consequence. The verdict, every human proof premise, adversarial
tests, limitations, and improvement opportunities are in
[`REVIEW.md`](REVIEW.md).

## Reproduction

Use CPython 3.11 or later; only the standard library is required.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 audit_independent.py > actual.json
diff -u EXPECTED_OUTPUT.json actual.json
PYTHONDONTWRITEBYTECODE=1 python3 -O audit_independent.py > actual-optimized.json
diff -u EXPECTED_OUTPUT.json actual-optimized.json
sha256sum -c SHA256SUMS
```

The checker imports no target module or fixture. It assigns four cyclically
ordered vertices independently to all `8^4=4096` edge tuples, parametrizes
each edge by a coordinate in `[0,1]`, solves the four square equations, and
enumerates vertices of the resulting affine section of the four-cube. This is
different from the target's center/radius active-set implementation.

A rectangle positive control forces nondegenerate one-dimensional solution
families. All calculations are exact rational arithmetic. No solver,
third-party package, randomness, floating point, network input, generated
database, or omitted certificate is used.
