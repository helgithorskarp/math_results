# Independent Sendov boundary audit

Actual author: **six-reviewer-3**, independent mathematical reviewer.

[REVIEW.md](REVIEW.md) confirms the sharp degree-nine first-power boundary coefficient and complete leading-profile classification in committed lemma 8530. It also proves that every balanced profile is uniformly realized by the same construction with common cubic correction `3/40` instead of `1`, and determines the sharp infimum of that correction within this ansatz. The threshold endpoint and global first-power conjecture are not settled.

The [independent exact checker](audit.py) uses Python 3.11 standard library only. From the repository root:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B round-two/six-reviewer-3/sendov-boundary-audit/audit.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O round-two/six-reviewer-3/sendov-boundary-audit/audit.py
```

Both executions match [expected.json](expected.json). [provenance.json](provenance.json) contains compact run receipts and hashes of the audited original source. [SHA256SUMS](SHA256SUMS) covers the source packet. The review states the inherited analytic premises and the ordinary proof bridges outside the exact finite checker. No solver or external proof data is required.
