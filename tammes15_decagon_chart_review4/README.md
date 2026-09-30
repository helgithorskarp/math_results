# Fourth-decagon independent audit

Actual reviewer: six-reviewer-4, independent mathematical reviewer.
See [REVIEW.md](REVIEW.md) for the confirming scope, complete mathematical
interpretation, and proved extra-pair cosine margin 1/1,000,000.

Run from the repository root using CPython 3.11.2 and SymPy 1.14.0:

```sh
python3 -m venv tammes15_decagon_chart_review4/.venv
tammes15_decagon_chart_review4/.venv/bin/pip install -r tammes15_decagon_chart_review4/requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 tammes15_decagon_chart_review4/.venv/bin/python -B tammes15_decagon_chart_review4/audit.py tammes15_decagon_chart_exclusion/certificate.json --check tammes15_decagon_chart_review4/expected.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 tammes15_decagon_chart_review4/.venv/bin/python -B -O tammes15_decagon_chart_review4/audit.py tammes15_decagon_chart_exclusion/certificate.json --check tammes15_decagon_chart_review4/expected.json --selftest
cd tammes15_decagon_chart_review4
sha256sum -c SHA256SUMS
```

Expected: 566 discarded-cell witnesses, 35,658 positive tensor coefficients,
compatibility graphs with 361/539 vertices and 28,811/65,666 edges,
both clique numbers 4, and the proved cosine excess `1/1000000`.
The optional selftest reports 33,792 definition-level graph checks and six
rejected frontiers on stderr. Any incomplete process establishes no verdict.

The original certificate is a compact public dependency pinned by hash;
the audit imports no original mathematical code. The exact original
source is identified in `provenance.json`. Large exploratory outputs,
environments, credentials and private graph data are excluded.
