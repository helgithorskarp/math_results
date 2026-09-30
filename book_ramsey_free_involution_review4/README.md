# Independent free-involution Book Ramsey review

Author: **six-reviewer-4**, independent mathematical reviewer.

The [review](REVIEW.md) confirms h7914 under its exact hypotheses.
The [proof](PROOF.md) forbids three five-orbit cores with arbitrary
complement colors and proves that exactly seven uniform blocks require
at least three red ones. The unrestricted Ramsey interval remains 22–23.

Use Python 3.11+ standard library and g++ 12.2.0/C++17 (tested versions).
From the repository root, run sequentially with one CPU and native thread:

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -B book_ramsey_free_involution_review4/audit.py \
  --scratch /tmp/book-involution-review4-normal

OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -B -O book_ramsey_free_involution_review4/audit.py \
  --scratch /tmp/book-involution-review4-optimized
~~~

Scratch must be outside this contribution directory. The script builds
one warning-free C++ binary, completes its quotient census, then completes
a separately written Python census. Every surviving pattern and inside
flag is compared with both censuses and all explicit template images.

Expected complete evidence: 5,739,370 blue choices, 868 surviving patterns,
42,112 inside assignments, three classes, 6,144 literal page/degree/difference
checks, 720 A row tuples, 90 B row pairs and four rejected corruption controls.
EXPECTED.json pins exact evidence. An initial normal run took 8.38 s,
peak child RSS 91,348 KiB and Python RSS 25,588 KiB; finalized normal/optimized
measurements are in validation.json.

No third-party package, solver, author executable or external data corpus
is needed. Generated census records, binaries and timing logs remain in
scratch; only compact reproducible source and evidence are published.
The analytic local-core theorem is ordinary unformalized mathematics.
The seven-pair consequence additionally trusts complete C++/CPython
enumeration and the independently confirmed at-least-two-red predecessor.

[provenance.json](provenance.json) pins all nine target files.
[SHA256SUMS](SHA256SUMS) checks the owned source. Neither finite
quotient data nor the expected fixture proves an unrestricted Ramsey bound.
