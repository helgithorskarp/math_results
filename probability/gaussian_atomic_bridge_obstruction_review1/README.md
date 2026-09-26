# Independent review: asymmetric atomic bridge obstruction

This directory independently reviews
[`gaussian_atomic_bridge_obstruction`](../gaussian_atomic_bridge_obstruction/)
at exact source commit `d05dd54b551a5a14329cfbe31f8b66c13cc0e217`.

**Verdict:** accept with high confidence the exact nine-atom obstruction to
both center-law martingale comparison and exact/nearby deterministic
common-output decompositions through five-dimensionally liftable contractions.
The open \(L^1\) weight neighborhood and all stated constants are valid.

This result is an obstruction to two sufficient proof mechanisms. It does
**not** disprove Gaussian density majorisation, decide the hinge inequalities
for the nine-atom pair, or prove a new Kneser--Poulsen inequality. The complete
scope and trust boundary are in [`REVIEW.md`](REVIEW.md).

## Independent method

[`independent_check.py`](independent_check.py) imports none of the reviewed
code and changes both principal finite methods:

1. It finds contracting bijections by incremental distance-compatible
   backtracking, rather than filtering all \(9!\) permutations.
2. It derives both covariance characteristic polynomials and uses exact Sturm
   sequences to count eigenvalues above \(16/25\) and \(13/20\), rather than
   checking the submitted LDL pivots.

It also reconstructs the square-symmetry classification, paired ranks,
eight projection constraints, moving circuit, Gram-rank obstruction, robust
covariance constants, exact mass-separation margin \(1/8464\), and approximate
output radius \(1/851\). A repeated-weight boundary case passes while an
origin-moving permutation is rejected.

## Reproduce

From the repository root with CPython 3.11 or later and no packages:

```sh
python3 probability/gaussian_atomic_bridge_obstruction_review1/independent_check.py \
  --out /tmp/atomic-bridge-review | \
  cmp - probability/gaussian_atomic_bridge_obstruction_review1/EXPECTED.json
python3 -O probability/gaussian_atomic_bridge_obstruction_review1/independent_check.py \
  --out /tmp/atomic-bridge-review-optimized | \
  cmp - probability/gaussian_atomic_bridge_obstruction_review1/EXPECTED.json
cd probability/gaussian_atomic_bridge_obstruction_review1
sha256sum -c SHA256SUMS
```

CPython 3.11.2 and 3.12.14 produced identical output. Runtime is below one
second and the checker writes only the compact `result.json` requested by
`--out`.
