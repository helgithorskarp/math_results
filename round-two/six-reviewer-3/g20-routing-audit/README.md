# G20 contact pentagon independent audit

Actual author **six-reviewer-3**, independent mathematical reviewer.
The complete ordinary proof is in [PROOF.md](PROOF.md); scope and verdict
are in [REVIEW.md](REVIEW.md). No geometric realization or Tammes15
optimality is claimed.

Using CPython 3.12.14 (standard library only), run from this directory:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B audit.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -O -B audit.py
python3 -B validate.py
```

Expected complete summary is [SUMMARY.json](SUMMARY.json). The whole
27,672-byte independent [EXPECTED.json](EXPECTED.json) record has SHA256
**03f284b66c79cc5b5f150cf5112cb6b7b252a16cfe9c1c9026c99b290f6bb5cc**.
The audit regenerates every field; no supplied expected data enters its
proof computation. `validate.py` checks normal/optimized agreement,
ten mathematical source damages in both modes, six complete-record
damages and three valid representation controls. Its serial children
have a fixed 45-second guard and all six native thread variables equal
one. [VALIDATION.json](VALIDATION.json) records actual measurements.

The finite evidence comprises all three full oriented sphere maps, every
vertex link and facial dart, all 32 diagonal subsets, all 56/52 partitions
and fourteen oriented profile assignments, all twelve fresh-corner core
candidates, all forced triangle adjacencies, three complete residual-disk
budgets and eleven strict rational parameter margins. The ordinary
embedded disk, reflection, face-identification, angle and Jordan bridges
in the proof remain essential. This is not a proof-assistant theorem.

[SEAL.json](SEAL.json) fixes the fresh primary work before native access.
Later native replay and comparison receipts, when present, are explicitly
secondary evidence. Written target mathematics and dependency results were
visible; the review is independent through its derivation and method,
not through a blind claim or a distinct signing key.

No numerical incumbent coordinate, solver, third-party package, private
ledger or large proof artifact is needed to reproduce the independent work.
