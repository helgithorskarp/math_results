# Complete independent first-slack audit

Reviewer: **six-reviewer-4**, independent mathematical reviewer.

[REVIEW.md](REVIEW.md) confirms all53 defect forms for degree histograms
(6,14,2), (8,8,6), (10,2,10), at97/98/99 red edges in ordinary
red-B4/blue-B7-free graphs on22 vertices. The conditional surplus-four
exclusion and, with credited degree/saturation premises, universal
3n8+n9<=31 budget are verified. The Ramsey endpoint remains unresolved.

Run from repository root, Python3.11+ standard library, one process:

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -B book_ramsey_first_slack_review4/audit.py \
  --check book_ramsey_first_slack_review4/expected.json
~~~

Add Python -O for the optimized check. Runtime is about half a second.
Optional passive comparison, separately from the expected check:

~~~sh
python3 -B book_ramsey_first_slack_review4/audit.py \
  --compare-author book_ramsey_4_7_degree_reductions/first_slack_expected.json
~~~

No author input selects the domain. The exact checker uses ordered surplus
compositions, all degree assignments, then center permutations; finite-field
elimination with CRT/Hadamard uniqueness reconstructs integer determinants.
All53 direct prime nonresidue certificates (primes<=37) are in expected.json.
No solver, external catalogue, large certificate or numerical tolerance.

PROVENANCE.json names source snapshots and inherited trust boundaries;
VALIDATION.json records successful final runs and two original replays;
SHA256SUMS covers the compact published files.
