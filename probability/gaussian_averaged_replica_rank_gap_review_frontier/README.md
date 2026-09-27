# Averaged replica-rank-gap review evidence

This directory independently reviews graph6436's universal averaged
Gaussian replica-rank gap at exact source commit
`5a2b55eca217a7fd7a0d035757eb29124bd5a204`.

- [REVIEW.md](REVIEW.md) gives the verdict, proof audit, and strict scope.
- [TARGET_INPUTS.json](TARGET_INPUTS.json) pins the target and normalization.
- [independent_check.py](independent_check.py) provides clean-room exact
  controls using a distinct contraction and formal exponential keys.
- [EXPECTED.json](EXPECTED.json) is the canonical checker record.
- [SOURCES.md](SOURCES.md) records primary literature and graph dependencies.

Run:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Expected record SHA-256:
`2d8a891721751f0df236fe16cb252ac8b2f037fd7389f7a0cd7b44c87b360b3c`.
