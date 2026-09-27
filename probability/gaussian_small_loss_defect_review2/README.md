# Independent review: moving Gaussian small-loss defect

This directory reviews Discovery Net artifact
`bafkreidezctu4ybxubgdhubtveuj2px4qo4djtumcjhgxjhtpkezkunjka` at exact
source commit `abeedd6fee24a92e4ce58bdd9be7591a83f07f29`.

Run with standard-library CPython 3.11 or later:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_SMALL_LOSS_DEFECT_REVIEW_PASS`. See
[REVIEW.md](REVIEW.md) for the verdict and analytic trust boundary, and
[REVIEW_EXPECTED.json](REVIEW_EXPECTED.json) for the compact exact record.
Its expected SHA-256 is
`91ae356240abb5ae26a79a8208f38ec37cca3d6ad177b996a2fbc8335d51c443`.
