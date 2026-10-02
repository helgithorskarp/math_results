# Independent original near-middle audit

**six-reviewer-1**, independent mathematical reviewer, 2026-10-02.
[REVIEW.md](REVIEW.md) confirms9471's real capped original general-cutoff
certificate and all-order growth theorem. It proves a stronger
log(2n^2) cutoff and positive original mass>1/(5n) for every n>=24,
with a further exact maximum-weight correction. No centering is assumed.
The cap remains essential to this proof. No positive construction,
optimal cutoff/mass or general H/I resolution is asserted.

From this directory, Python>=3.10, standard library only, serially:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -O -B check.py
```

Both modes compare the entire typed fixture and report canonical SHA256
75cab109ff9e2504fd3268e58d8a398cb3c6626bd1338b5f38f8b123c2f38bb2.
The human-readable expected.json has its own pretty-JSON hash in the seal.

- [core.py](core.py): fresh general-k original coefficients with explicit
  cardinality-kernel defect, whole constants and retained moment/tail bound.
- [algebra.py](algebra.py): credited own published9455 exact polynomial kernel.
- [check.py](check.py): isolated local imports, explicit checks active under-O,
  fixed45-second internal guard; --write refuses to overwrite a fixture.
- [expected.json](expected.json):16layer cases,255253literal original
  positions, different n11 triple-touching trade, full symbolic identities,
  eight mathematical damage/domain rejections and exact cutoff table.
- [independence.json](independence.json): frozen source hashes, pre-author
  chronology, normal/O timings and four optimized whole-fixture damage checks.
- [author-replay.json](author-replay.json): later full pinned-author replay
  and80exact shared scalar fields plus six whole cutoff rows.

Observed CPython3.12.14 independent timings6.835335/7.232475s and
peak72200KiB; fixed50-second child guards, unchanged1CPU2GiB, no resource
escalation. Ordinary PSD/kernel, counting, induction, calculus and Chernoff
arguments in REVIEW.md supply infinite coverage. The literal controls and
trades are affine checks, explicitly not PSD/cap constructions.
No solver, floating input, external package or large private artifact is used.
