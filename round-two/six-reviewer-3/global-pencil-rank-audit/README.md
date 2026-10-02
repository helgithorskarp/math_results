# Global stationary-pencil rank audit

Actual **six-reviewer-3**, **independent mathematical reviewer**.
[REVIEW.md](REVIEW.md) confirms9649, proves generic complex rank exclusion
outside four exact s values, and improves the real pointwise derivative bound.
The feasible rank-two locus and first-power endpoint remain open.

Python3.12 standard library only. From the repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 -B round-two/six-reviewer-3/global-pencil-rank-audit/verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 -B -O round-two/six-reviewer-3/global-pencil-rank-audit/verify.py
python3 -B round-two/six-reviewer-3/global-pencil-rank-audit/validate.py
```

Every subprocess is serial with fixed45s guard; all six native thread
variables are set to1. No package installation, CAS, solver or network is needed.
Expected PASS SHA256:
`1aa6ffcf98ffe7601829041269cd858aa5e097fd919b5847c8d821153fa8d5b7`.
Full85 rational Gaussian fixed determinants, full141/155 modular cardinal
interpolations, four full univariate units, all polynomial coefficients and
18 bridge controls are regenerated. All six changed-fixture cases reject in
normal/O. Exact arithmetic establishes identities; the ordinary proof supplies
the quantified reduction and real/complex/feasible trust boundaries.

`pencil.py` is unchanged earlier owned9598 `build.py`; `algebra.py`,
`certificates.py`, `polys.py` are unchanged owned9598 kernels. The entire
owned9550 audit is regenerated against its canonical pin. The independently
derived full fixture is [EXPECTED.json](EXPECTED.json); it is not a producer
input. `audit.py`, `controls.py`, `verify.py` and the pre-native proof notes were
sealed before accessing target code/fixture. [INDEPENDENCE.json](INDEPENDENCE.json)
and [PROVENANCE.json](PROVENANCE.json) record sources and the boundary.

Optional late producer comparison, from an ordinary complete repository tree:

```sh
python3 -B round-two/six-sendov-2/global-rank-two/verify.py --export /tmp/rank-two-export.json
python3 -B round-two/six-reviewer-3/global-pencil-rank-audit/compare_author.py \
  round-two/six-sendov-2/global-rank-two/expected.json /tmp/rank-two-export.json
```

The producer needs its pinned9602/9550 siblings. The optional adapter imports
no producer code; it compares complete exported coefficients and recorded
units. [COMPARISON.json](COMPARISON.json), [NATIVE.json](NATIVE.json) and
[VALIDATION.json](VALIDATION.json) are compact corroboration. Producer replay
is not the independent proof. Generated caches, exports and temporary damages
remain private or ignored. [SEALED-NOTES.md](SEALED-NOTES.md) preserves the
pre-native generic-complex and projection arguments.
