# Regularized-contact margin review evidence

This directory independently reviews the effective Gaussian-regularized
contact margin at graph6438 and source commit
`7e8165706d3dac6827e766b9a7359de4d180110e`.

- [REVIEW.md](REVIEW.md) gives the verdict, proof audit, and limitations.
- [TARGET_INPUTS.json](TARGET_INPUTS.json) pins the target and dependencies.
- [independent_check.py](independent_check.py) provides clean-room exact
  controls.
- [EXPECTED.json](EXPECTED.json) is the canonical checker record.
- [SOURCES.md](SOURCES.md) records the primary literature and graph boundary.

Run:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Expected record SHA-256:
`357c63dabd905187aaaac74102c117a770b8ec1ad3851c2993faf60c711b276b`.
