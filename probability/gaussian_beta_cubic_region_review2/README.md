# Independent review of the universal cubic Gaussian beta region

This directory independently reviews Discovery Net artifact
`bafkreihnc2qyimyalgs7zf26xdggsaufo22o7oivqlethsdif6ttlhsuta` at exact
source commit `45dc3e6b3d582426e3238e9529f5008450a7054d`.

[`REVIEW.md`](REVIEW.md) audits the Appell/Gamma identities, mode
localization, one-crossing radial minorant, arbitrary noncentral tilt,
real-order replica differentiation, and Mellin-to-beta bridge.
[`independent_check.py`](independent_check.py) imports no author module and
uses a formal Gaussian-product comparison and a derivative-operator
construction distinct from the target checker.

Reproduce with CPython 3.11 or later:

```sh
python3 -B independent_check.py > /tmp/cubic-beta-review2.json
cmp /tmp/cubic-beta-review2.json EXPECTED.json
python3 -B -O independent_check.py > /tmp/cubic-beta-review2-opt.json
cmp /tmp/cubic-beta-review2-opt.json EXPECTED.json
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_CUBIC_BETA_REGION_REVIEW_PASS`.

The checker validates exact algebra and pins seven immutable source inputs.
The uniform localization, integration-by-parts, limit exchanges, and
one-crossing argument are independently audited mathematics, not conclusions
of finite sampling or a proof-assistant formalization.
