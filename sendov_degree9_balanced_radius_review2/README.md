# Independent near-balanced reciprocal-radius review

**six-reviewer-2**, independent mathematical reviewer, 2026-09-30.

This independently confirms six-sendov-1's degree-nine four-plus-four
two-channel origin gap and exact radial-monotonicity obstruction. A new
phase-aware normalized transport proof widens the allowed radius difference
from `(1-a)/1000000` to `(1-a)/20000`, preserving the strict origin gap
`(1-a)/8`. The unrestricted first-power Tang–Zhang endpoint remains open here.

[REVIEW.md](REVIEW.md) gives all hypotheses, the proof, literature boundary,
independent methodology and trust limits. [INPUT.json](INPUT.json) pins the
original seven files at commit `b3c2e98504f243383d4cf6e25287e0cfdaf4dfbc`.
The independent checker imports no author module. Its real/imaginary binomial
norm and reversed delta-domain certificate differ from the native routes.

From repository root, with Python3.11.2 or later and the standard library:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -I -B sendov_degree9_balanced_radius_review2/reproduce.py
python3 -I -B -O sendov_degree9_balanced_radius_review2/reproduce.py
```

The original directory `sendov_degree9_balanced_radius_origin_gap` must match
the pinned hashes. To use a separate copy of the original seven files, pass
`--input-dir /path/to/original`. Input drift is rejected. Independent arithmetic
can also be run alone with `python3 -I -B sendov_degree9_balanced_radius_review2/audit.py`.

Expected: all6487 individual rational coefficients, full norm and delta
quotient,60 exact definition checks,5 malformed controls, exact radial
counterexample values and the fiftyfold imbalance improvement. The
[compact manifest](expected.json) records exact minima, zero locations,
coefficient hashes and constants. Full coefficient lists are reconstructed
temporarily and are not published. All native comparisons run in separate
subprocesses after the independent calculation. No numerical library, solver,
large input corpus or proof assistant is needed.
