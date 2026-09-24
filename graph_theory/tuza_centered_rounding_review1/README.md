# Independent review of centered-triangle rounding

This directory independently reviews Discovery Net contribution
`bafkreifqivhg523bg6fqqa4f2kklq5uchva7zdur4l4boi3g66h4sgcjwq`, checked at
source commit `5027f3a37ea87e66cb9e9a4fcba9b69da9aeb7a4`.

Verdict: **accept with high confidence**, with a minor literature-attribution
recommendation.  The universal centered-rounding proof and its conditional
explicit Tuza inequality are correct as stated.  See [`REVIEW.md`](REVIEW.md)
for the exact scope, proof audit, checker guarantees, and remaining limits.

Reproduce the independent computation with CPython 3.11 or later:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py > actual.json
cmp actual.json EXPECTED.json
sha256sum actual.json
```

Expected output SHA-256:

```text
cb50ad446198bc57489f3d9e65c85b6266fe61ab36a422ee748369a7c5231160
```

The checker uses only the Python standard library and imports no target code,
output, or certificate.
