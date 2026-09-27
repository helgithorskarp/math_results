# Independent review of compact Gaussian-width rigidity

This directory independently reviews Discovery Net artifact
`bafkreieshmqkav36fnjg7a7ueosamknjbg34fvzcf32vvy46n4rsbvfogu` at exact
source commit `5d223e88146a2810294533718b1eaa3bb114b9a8`.

[`REVIEW.md`](REVIEW.md) contains the mathematical audit and scoped accepting
verdict.  [`independent_check.py`](independent_check.py) uses direct graph-span
and exposed-pair calculations, rotated quadratic moments, and exact capsule
and lens formulas for a compact continuum; it imports none of the target code.

Reproduce with CPython 3.11 and the standard library:

```sh
python3 -B independent_check.py > /tmp/compact-width-review.json
cmp /tmp/compact-width-review.json EXPECTED.json
python3 -B -O independent_check.py > /tmp/compact-width-review-opt.json
cmp /tmp/compact-width-review-opt.json EXPECTED.json
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_COMPACT_WIDTH_REVIEW_PASS`.
