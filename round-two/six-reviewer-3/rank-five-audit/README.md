# Independent uniform rank-five Hoffman audit

Actual author: **six-reviewer-3**, independent mathematical reviewer.

[REVIEW.md](REVIEW.md) confirms committed lemma 8583 for every uniform downset `D(n,5)`, integer `n>=7`, and all its finite products. It proves the larger closed sufficient repair interval `0<t<=2/((n-2)(n-3)(2*n-1))`, with the same maximal ranks and star equality. General H/I and an optimal interval remain open.

The independent [audit.py](audit.py) uses standard-library rational polynomial arithmetic, Newton traces and a ballot-product harmonic basis. It imports no author code. It reads the published `BOUNDARY_CERTIFICATES.json` and `POSITIVITY_CERTIFICATE.json` in `round-two/six-downset-2/uniform_rank_five`, requiring their exact pinned hashes and rechecking their identities. Keep those public source files at their repository paths.

From the repository root:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B round-two/six-reviewer-3/rank-five-audit/audit.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O round-two/six-reviewer-3/rank-five-audit/audit.py
```

Both must match [expected.json](expected.json). CPython 3.11.2 runs take about 2.3 seconds and below 25 MiB. [provenance.json](provenance.json) records the checked source and run receipts; [SHA256SUMS](SHA256SUMS) covers this packet. The review gives the ordinary all-order completeness, PSD endpoint and rank/equality bridges outside the exact checker.
