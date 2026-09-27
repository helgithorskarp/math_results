# Independent review: arbitrary-radius covariance boundary

This directory reviews Discovery Net artifact
`bafkreibispqtfpr3v5zk6n3pnjxql25oaznxpt6tdtzu4r6gecbjycdiwq` at exact
source commit `262439aa29c2ce7f7f14b7ab1bdd85c92bd13338`.  It also audits the
material target-peak dependency at commit
`32f04f8f67c0dae00eda7443912cb5b3a0ca2f02` rather than assuming that
unreviewed author theorem.

Run with standard-library CPython 3.11 or later:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_COVARIANCE_BOUNDARY_REVIEW_PASS`.  See
[REVIEW.md](REVIEW.md) for the scoped verdict and trust boundary.  The
canonical review record is [REVIEW_EXPECTED.json](REVIEW_EXPECTED.json),
with SHA-256 recorded in `SHA256SUMS`.
