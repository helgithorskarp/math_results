# Independent triangle-majority audit

six-reviewer-3, independent mathematical reviewer, 2026-10-01.
The [review](REVIEW.md) confirms scoped lemma8757 and proves the exact
upper spectral gap for its fixed rational matrices at every integer q>=4:
`min(N-2s, N-(1+alpha)/2)/(N-s)`, where
`alpha=q(q+1)/2+3(q+1)/(3q+5)`. Its sharp uniform value is5/13.
It also gives the exact core-cap minimum and exact product upper gaps.
Separate q2/3 boundary tables are audited for the original theorem;
the new generic gap statements exclude them. General H and I remain open.

Requires Python3.10+ standard library (tested3.11.2), no solver/CAS.
From this directory, obtain the three pinned public author inputs:

```bash
mkdir -p /tmp/triangle-majority-review-inputs
curl --fail --location https://raw.githubusercontent.com/helgithorskarp/math_results/99d63aa2f085127a670ae375b19a68b89e184074/round-two/six-downset-3/triangle-majority/BOUNDARIES.json -o /tmp/triangle-majority-review-inputs/BOUNDARIES.json
curl --fail --location https://raw.githubusercontent.com/helgithorskarp/math_results/99d63aa2f085127a670ae375b19a68b89e184074/round-two/six-downset-3/triangle-majority/SIGNS.json -o /tmp/triangle-majority-review-inputs/SIGNS.json
curl --fail --location https://raw.githubusercontent.com/helgithorskarp/math_results/99d63aa2f085127a670ae375b19a68b89e184074/round-two/six-downset-3/triangle-majority/RESULTS.json -o /tmp/triangle-majority-review-inputs/RESULTS.json
curl --fail --location https://raw.githubusercontent.com/helgithorskarp/math_results/d2ff55ed49209535344ec32da2fba28fefd066b2/round-two/six-reviewer-3/three-petal-audit/audit.py -o /tmp/triangle-majority-review-inputs/independent8682.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B audit.py --prior-audit /tmp/triangle-majority-review-inputs/independent8682.py --boundaries /tmp/triangle-majority-review-inputs/BOUNDARIES.json --signs /tmp/triangle-majority-review-inputs/SIGNS.json --author-results /tmp/triangle-majority-review-inputs/RESULTS.json --check expected.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B -O audit.py --prior-audit /tmp/triangle-majority-review-inputs/independent8682.py --boundaries /tmp/triangle-majority-review-inputs/BOUNDARIES.json --signs /tmp/triangle-majority-review-inputs/SIGNS.json --author-results /tmp/triangle-majority-review-inputs/RESULTS.json --check expected.json
sha256sum -c SHA256SUMS
```

The code verifies all four external file hashes before importing/decoding.
In a repository checkout, the default toolkit path is the sibling
`three-petal-audit/audit.py`, so `--prior-audit` can be omitted if that
hash-pinned file is present. No author Python is imported. The expected
output has `ok:true`,33 sign records, three original matrix comparisons,
six literal parameters,238 projector columns,12 rejected controls, and
receipt SHA256 `7fb10b7945f9884e789540285c48eaa55bff9b3672516386b251087764a7fb02`.

[VALIDATION.md](VALIDATION.md) states actual coverage and timing.
The [compact receipt](expected.json) contains complete reconstructed
certificate polynomials, matrix hashes, census summaries, spectral records
and forced product Grams. Neither a large enumeration corpus nor a full
product matrix is required. The unbounded conclusion also requires the
written degree, action-completeness and spectral arguments in the review.
