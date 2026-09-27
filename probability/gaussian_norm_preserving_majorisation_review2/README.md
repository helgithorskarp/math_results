# Independent review of norm-preserving Gaussian majorisation

This packet independently reviews Discovery Net artifact
`bafkreiekpjods6d64zl5bjtziqfwgrxy5fhqvw237vqiepknp5g7yotwte` at exact
source commit `7ec05f2b89b4ab69de7a6696f236aa1f6ecc3ffc`.

The verdict and mathematical audit are in [REVIEW.md](REVIEW.md).
[`independent_check.py`](independent_check.py) imports no target code.  It
checks an end-to-end formal `S^2` moment expansion for power energies on two
fresh exact norm-preserving contractions, discrete Boolean mixed-difference
signs, the ball and cap encodings, negative controls, and seven provenance
pins.

Reproduce with CPython 3.11 or later, standard library only:

```sh
python3 -B independent_check.py > /tmp/norm-preserving-review.json
cmp /tmp/norm-preserving-review.json EXPECTED.json
python3 -B -O independent_check.py > /tmp/norm-preserving-review-opt.json
cmp /tmp/norm-preserving-review-opt.json EXPECTED.json
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_NORM_PRESERVING_REVIEW_PASS`.

