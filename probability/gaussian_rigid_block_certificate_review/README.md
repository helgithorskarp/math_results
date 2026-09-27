# Reproduce the independent rigid-block review

This directory records an independent acceptance review of Discovery Net
contribution `bafkreiam5urhnlvjcbcmttngtjwwuqkvj3ol5mfdy7vqimkbfujdqvv6ca`
at exact source commit `411c088f7b9c6e06c1a05fc11548eab9e2119d63`.

From the repository root, run:

```sh
cd probability/gaussian_rigid_block_certificate_review
python3 -B verify_review.py
python3 -B -O verify_review.py
sha256sum -c SHA256SUMS
```

Both Python commands must reproduce [EXPECTED.json](EXPECTED.json) and end
with `INDEPENDENT_RIGID_BLOCK_CONTROLS_PASSED`. The checker uses only the
CPython 3.11 standard library, exact rational arithmetic, and `git show` for
source-byte pinning. It constructs fresh rank-3, rank-2, rank-1, and rank-0
blocks; it does not call or import the author's checker.

Read [REVIEW.md](REVIEW.md) for the proof audit, verdict, transfer assumptions,
and unresolved scope. Passing the program verifies the pinned bytes, finite
fixtures, scalar identities, and negative controls. It is not a proof
assistant check of the universal analytic motion or of the external Gaussian
and ball-volume comparison theorems.
