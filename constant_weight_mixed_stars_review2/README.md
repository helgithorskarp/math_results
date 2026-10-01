# Independent double and mixed saturated-star review

**six-reviewer-2, independent mathematical reviewer**, 2026-10-01.

This package confirms that no72-word A(18,6,5) packing has a positive
deficit row(2,2,1). It independently closes the needed first-star classification,
sharp double-row maximum58 and the two specified sharp mixed maxima58/57.
[REVIEW.md](REVIEW.md) gives the complete scope, proof and trust boundaries.
The third mixed marking is outside the census. The global gap remains69--72.

CPython3.11, g++12.2, standard libraries only. From the repository root,
execute these **sequentially**:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B constant_weight_mixed_stars_review2/reproduce.py --work /tmp/mixed-review-normal
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B -O constant_weight_mixed_stars_review2/reproduce.py --work /tmp/mixed-review-normal
```

With a new work directory, the first command recomputes all629 first-star
cases,884029 mixed fibers,85995 double-row fibers,66 common residual ceilings,
all literal attaining fixtures and controls. The second command reruns the
first/double/residual checks and uses the source-bound completed mixed results.
For a fully cold optimized mixed census choose a different fresh work directory.
Every run compares the complete stable mathematical record with
[expected.json](expected.json); timing/RSS are recorded separately.

Default inputs are sibling repository directories
`coding_theory/a18_6_5_double_221_pair` and
`coding_theory/a18_6_5_no_221_at_72`. Only their expected JSON files and the
double-row58/known69 fixtures are consumed; target-author executable code is
never imported or run. [INPUT.json](INPUT.json) gives exact historical pins,
hashes and reviewer source reuse. If those files later change, point
`--classification PATH` and `--target PATH` to the pinned copies.

The mixed generator checkpoints at complete C-model boundaries. Resume requires
unchanged mathematical input fingerprints and hashes of its Python proof
modules and native source. Generated outputs remain under the work directory.
Interrupted models are incomplete and contribute no exclusion. `--record`
explicitly replaces the expected baseline; it is not an expected-result check.
The optional `census.py --reference PATH` compares all inputs/outputs against
an authenticated source-author model summary if separately regenerated; it is
not required for public reproduction or a proof premise.

Normal cold mixed work measured82.26+110.13 seconds and below57MiB peak
Python RSS in this campaign; the other complete components take tens of
seconds. Timings vary by host. All local200000-state/ten-second guards and
the1CPU/2GiB scope remain unchanged; a guard failure raises INCOMPLETE.
See [VALIDATION.md](VALIDATION.md) for evidence and limitations.
