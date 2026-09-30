# Independent Tammes-15 eight-Q audit

Reviewer **six-reviewer-4**, independent mathematical reviewer, 2026-09-30.

[REVIEW.md](REVIEW.md) confirms the local degree-pattern exclusion of graph
7729, audits its original-fan prerequisites, and proves a uniform cosine
violation greater than 1/1000 in each terminal metric branch. The eight-Q
beta specialization retains the published degree-pattern theorem as an
explicit dependency. No global bound improvement or optimizer coverage is claimed.

CPython 3.11.2, SymPy 1.14.0, mpmath 1.3.0; exact rational arithmetic only:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 .venv/bin/python audit.py --check
```

The checker regenerates [expected.json](expected.json) from definitions.
It imports no researcher code or external certificate. The free-face-first
incidence enumeration covers 5875 necessary cases and 24 actual-label
transports. A separate Q(c)/Sturm implementation checks 466 identities,
327 coordinate denominators, 202 prerequisite pairs and both metric seeds
at every branch. No floating-point computation is a mathematical premise.

[provenance.json](provenance.json) records pinned target and prerequisite
proof hashes; [SHA256SUMS](SHA256SUMS) covers this compact package.
The infinite-interval geometry remains an ordinary written proof, not a
formalization or a historical-priority claim.
