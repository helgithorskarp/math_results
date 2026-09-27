# Independent review of the rigid-block certificate

This directory independently reviews Discovery Net artifact
`bafkreiam5urhnlvjcbcmttngtjwwuqkvj3ol5mfdy7vqimkbfujdqvv6ca` at exact
source commit `411c088f7b9c6e06c1a05fc11548eab9e2119d63`.

[`REVIEW.md`](REVIEW.md) contains the mathematical audit and scoped accepting
verdict.  [`independent_check.py`](independent_check.py) checks the rational
control family by an exact norm enclosure, rather than the target's Bernstein
implementation, and exercises a separate noncommuting Procrustes fixture.

Reproduce with CPython 3.11 and the standard library:

```sh
python3 -B independent_check.py > /tmp/rigid-block-review.json
cmp /tmp/rigid-block-review.json EXPECTED.json
python3 -B -O independent_check.py > /tmp/rigid-block-review-opt.json
cmp /tmp/rigid-block-review-opt.json EXPECTED.json
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_RIGID_BLOCK_REVIEW_PASS`.
