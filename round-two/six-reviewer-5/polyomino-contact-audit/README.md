# Independent real-phase polyomino contact audit

**six-reviewer-5, independent mathematical reviewer.** See the complete
[review and proved smaller anchored mesh](REVIEW.md). The target is committed
lemma8694 by six-heesch-1, source4f67530506370b6a36dc916b0c117df990aeb816.
No target code is imported; no solver is required.

From the repository root, using standard-library CPython3.11:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B round-two/six-reviewer-5/polyomino-contact-audit/independent_check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -O -B round-two/six-reviewer-5/polyomino-contact-audit/independent_check.py
```

Each output must match [expected.json](expected.json). Exact input hashes and
immutable original URLs are in [inputs.json](inputs.json). Coordinates,
positive witnesses and eight short RUP traces are copied credited public
evidence. Six independent type inventories, twenty exact input formulas,
461 RUP additions, anchored phase controls, disc hypotheses and negative
controls are checked. The initial slow implementation timed out without a
verdict; final executions complete under the unchanged180-second guard.
Only compact source/evidence is included, with no generated formula corpus.

The known seven-cell all-motion calibration is confirmed at Hh=1. The new
mesh refinement halves at least one axis denominator and both for integral
pairs. It supplies no new Heesch record or five-corona construction.
