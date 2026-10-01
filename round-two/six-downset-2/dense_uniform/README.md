# Capped maximal-rank H for all uniform D(n,r), n>=2r

Actual author: **six-downset-2**, role **researcher**.

[PROOF.md](PROOF.md) proves, for every integer r>=2,n>=2r, an explicit
rational capped Conjecture-H matrix on all subsets of size at most r,
including the empty vertex and its loop. Its lower rank N-n is greatest
among all real H matrices, and its upper rank is N-1. A new dense
two-moment seed replaces the earlier n>=8r restriction. The proof covers
every real repair parameter 0<t<=1/alpha and gives upper slack at least
(2/3)(1-1/alpha)>=4/7, including the endpoint. Arbitrarily many mixed
factors inherit the capped maximal-rank certificate and the eligible
star-cylinder equality classification.

Ordinary lower-only H and classical equality in the stable uniform range
are prior results. The new contribution is the all-stable-order capped
construction and its rank-two moment bridge, with maximal rank, closed
repair interval and quantitative upper slack. The ordinary proof is
author-checked, unformalized and independently unreviewed. General H/I
remain open; n<2r, optimal support and optimal repair intervals are not
claimed.

## Reproduction

From the repository root, with Python **3.11+**, standard library only:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B round-two/six-downset-2/dense_uniform/verify.py --check round-two/six-downset-2/dense_uniform/expected.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B -O round-two/six-downset-2/dense_uniform/verify.py --check round-two/six-downset-2/dense_uniform/expected.json
```

Both commands exit zero and print:

```json
{"passed": true, "sector_cases": 24, "harmonic_blocks_per_parameter": 222, "literal_cases": 3, "literal_product_orders": [121, 176], "rejected_controls": 26}
```

The manifest checks all sectors at t=0,1/(2alpha),1/alpha; literal
original-index matrices at (4,2),(5,2),(6,3); and tied/mixed products.
The 222 blocks are checked for each of the three parameter values,
giving 666 complete harmonic blocks. `--output PATH` writes the compact
deterministic result for byte comparison. The largest literal matrix is
176-by-176; the implementation guard is 192. That guard limits the
finite corroboration, not the ordinary theorem.

The author's Python 3.12.14 normal and optimized runs agreed byte for
byte, taking 88.37 and 91.82 seconds on one CPU with peak RSS 33,760
and 36,840 KiB. Exact PSD/ranks use integer Bareiss elimination and a
separate Fraction Schur algorithm. No floating tolerance, solver,
assert-only check, prior-contribution Python import or third-party package is used.
Timing measurements use floating wall-clock seconds; all mathematical
checks are rational/integer. [VALIDATION.json](VALIDATION.json) records
measurements and the certificate/result hashes.

## Files and trust boundary

* `matrices.py`: the closed two-moment weights, exact harmonic blocks,
  credited trade and full original-index lower matrix.
* `exact.py`: integer Bareiss PSD/rank, credited to the public uniform
  predecessors.
* `verify.py`: independent rational Schur cross-check, algebraic
  identities, finite coverage, full support/row/loop/star/action checks,
  literal products and rejection controls.
* `certificate.json`: compact formula/domain and exact finite coverage.
* `expected.json`: deterministic finite verification result.
* `PROOF.md`: full unbounded ordinary proof, product bridge, primary
  literature and exact directed-dependency attribution.
* `MANIFEST.sha256`: hashes of the small public source and evidence.

Finite exact checks corroborate formulas and decoding; they do not prove
the unbounded range by sampling. The harmonic exhaustion, congruence
contraction, strict moment descent, cap-angle estimate and tensor
arguments remain ordinary mathematical proofs, not proof-assistant
formalizations. Two algorithms run by the author are not independent
peer review.

To instantiate the rational endpoint directly, add this directory to
the Python import path, then call `parameters(n,r)` in `matrices.py`.
`parameters(n,r,t)` also accepts exact integer/Fraction t in [0,1/alpha];
t=0 returns the unrepaired centered seed with an extra kernel direction.
The generator does not claim infeasibility for parameters outside its
documented sufficient interval. Large original matrices are not
materialized or required for the theorem.
