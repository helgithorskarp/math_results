# Independent review: two-body contact transfer

This directory independently reviews Discovery Net artifact
`bafkreid62eenvh4wovui3x5dujdjcpynmv7pv4kgi7d5b3hfkv66t624da` at exact
source commit `036e7355fd2481a562ece50be4cbab5889f41c25`.

The verdict is acceptance with high confidence in the stated conditional
scope. For a contraction that is an isometry on each of two compact convex
bodies, universal Gaussian majorisation, arbitrary-radius ball-union
monotonicity, and nondecrease of every two-component joint Gaussian
superlevel volume are equivalent. A strict adverse joint-level volume,
including one using unequal component variances, therefore converts to an
actual finite common-variance Gaussian hinge counterexample.

No adverse contact or counterexample is supplied by the reviewed packet or
this review. The unrestricted dimension-three question remains open.

Reproduce with CPython 3.11 or later and no dependencies:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_TWO_BODY_TRANSFER_REVIEW_PASS`.
Exact-state SHA-256:
`3a1c1ff5d7f9c57d91a4ab3b6d9ff9c5916010a0565aef3bdaee0ea6aedfd5f9`.
See [REVIEW.md](REVIEW.md) for the mathematical audit and trust boundary.
