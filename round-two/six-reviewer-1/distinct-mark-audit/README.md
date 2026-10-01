# Reproduce the distinct-mark H audit

Reviewer six-reviewer-1 independently audits committed8863 and proves stronger
full-frame margins and a larger rational repair weight. See [REVIEW.md](REVIEW.md)
for quantified scope, proofs, credit and limitations.

CPython3.11+ standard library only; no author source is imported. From the
repository root, run sequentially:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-reviewer-1/distinct-mark-audit/check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B -O round-two/six-reviewer-1/distinct-mark-audit/check.py
```

Expected:25,111 checked requirements;15 canonical instances, one relabel,
58 sector fixtures, four old-core cases, two products, three exhaustive small
maximum-family cases, ten damage controls. Record SHA256:
`a0fddca912e81a4262d784d80e9bbb26f56a7c33d811f11bf7ae0953335957b6`.
No source or fixture is modified by a normal replay. Explicit regeneration:

```sh
python3 -B round-two/six-reviewer-1/distinct-mark-audit/check.py --emit-fixture /tmp/distinct-mark-audit.json
```

The optional `--fixture PATH` compares the entire freshly generated record.
Wrong and incomplete fixtures must be rejected even under `-O`. Mathematical
checks use explicit exceptions, not assertions. The bounded literal guard
n2..6 is an operational check limit; the written theorem has all-order scope.
In this directory, `sha256sum -c SHA256SUMS` checks the compact source manifest.
[provenance.json](provenance.json) records original source and exact run evidence;
no keys, private ledger, solver output or large generated dataset is published.
