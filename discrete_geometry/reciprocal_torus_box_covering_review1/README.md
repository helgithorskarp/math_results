# Review evidence for reciprocal torus-box coverings

This directory contains an independent review of the theorem and source in
[`../reciprocal_torus_box_covering`](../reciprocal_torus_box_covering).

Verdict: **accept, with high confidence in the stated scope**.  See
[`REVIEW.md`](REVIEW.md) for the proof audit, explicit premises, adversarial
examples, source check, and caveats.

The clean-room checker uses a full Cartesian endpoint arrangement and direct
center membership tests.  It intentionally does not reuse the submission's
coverage-mask intersection reduction.

## Reproduce

Python 3.11+ and the standard library suffice.  From this directory run:

```sh
python3 verify.py --check
sha256sum -c SHA256SUMS
```

The first command must end with `"status": "PASS"`; the second must verify the
other three files.  Do not use Python's `-O` option because this audit program
uses assertions as executable proof obligations.

The exact continuum check covers 380,194 product strata over 14 constructions
under both the open reciprocal and strengthened half-open conventions.  The
finite computation corroborates, but does not replace, the universal human
proof reviewed in `REVIEW.md`.
