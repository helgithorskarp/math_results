# Independent near-cube Hoffman review

Actual agent **six-reviewer-1**, role **independent mathematical reviewer**.
[REVIEW.md](REVIEW.md) confirms the all-order near-cube affine H theorem,
then proves its full spectrum, sharp optimal cap excess, and exact
affine inertia-tightness/simultaneous-cap intervals. The assertions about
caps concern this architecture. General H/I remain open.

CPython3.11+ standard library, from repository root, sequentially:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -B spectral_downset_near_cube_review1/audit.py \
 --check spectral_downset_near_cube_review1/expected.json
python3 -B spectral_downset_near_cube_review1/inertia.py \
 --check spectral_downset_near_cube_review1/inertia_expected.json
```

Repeat with `python3 -B -O` to check explicit optimized-mode failures.
[audit.py](audit.py) derives universal characteristic polynomials and
constructs full matrices from literal partitions. It checks complete
structured eigenspaces, quotient lifts, full determinants and backend
controls. [inertia.py](inertia.py) independently counts signed full-matrix
inertia by exact congruence. Complete compact outputs are
[expected.json](expected.json) and [inertia_expected.json](inertia_expected.json).
The all-order conclusions require the written proof, not extrapolation.
Neither independent checker imports author code or a fixture.

Optional supplemental entry comparison:

```sh
python3 -B spectral_downset_near_cube_review1/compare_entries.py
```

This explicitly imports the original author constructor at the exact hash
in [provenance.json](provenance.json). It checks633494 literal entries in22
cases; [entry_comparison.json](entry_comparison.json) records the result.
That import is not an input to the independent proof or two main checkers.
[SHA256SUMS](SHA256SUMS) covers compact source. No external package, solver,
floating-point decision, large corpus or private operational input is needed.
