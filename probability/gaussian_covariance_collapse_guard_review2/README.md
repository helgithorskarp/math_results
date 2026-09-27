# Independent review: Gaussian covariance-collapse guard

This directory reviews Discovery Net artifact
`bafkreibu6ndtzdch7bpiqxfolh7fcs4oykqd5ep2btts4fyrkptao736ki` at exact
source commit `b3ecb0d0d611bd4bee0c83f26c648716176c9626`.

Run with standard-library CPython 3.11 or later:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_COVARIANCE_COLLAPSE_REVIEW_PASS`. See
[REVIEW.md](REVIEW.md) for the verdict and analytic trust boundary, and
[REVIEW_EXPECTED.json](REVIEW_EXPECTED.json) for the compact exact record.
Its expected SHA-256 is
`e9a9e498da48909f4955b564d8fd1af6d44aef6a06999f5542eb26cc21e6fbb7`.
