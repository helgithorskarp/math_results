# Exact H certificates for every maximally deleted triangle link

Actual author: **six-downset-3**, role **researcher**.

For every integer q>=4, retain the full two-skeleton on {a,b,c} union
W_q and exactly the triples abc, abx, acx. The ordinary proof and
22 exact unbounded polynomial sign certificates give capped H,
universally greatest lower rank N-1, a simple unit eigenvalue, and
upper gap at least 1/[8(N-s)]. The construction works for every real
0<t<=1/[12q(q+1)(q+2)] and is rational for rational t. All finite
products of these factors have the proved eligible-cylinder equality
classification. N=(q^2+11q+16)/2 and s=3q+4.

Read [PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/maximal-deletion/PROOF.md)
for the exact scope, complete harmonic reduction and trust boundary.
This is an author-checked unformalized theorem, with independent review
pending; general spectral Conjectures H/I remain open.

From this directory, with Python 3.11+ and its standard library:

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python -O verify.py
sha256sum -c SHA256SUMS
```

The source imports only two SHA-pinned small public helpers from
`../triangle-majority`, commit `99d63aa2f085127a670ae375b19a68b89e184074`.
The replay takes about 66 seconds and under 29 MiB in the author runs.
It checks 22 unbounded signs, nine normal minors, 88 original action
columns, ten secondary characteristic forms and 26 rejection controls.
The stored exact lists in SIGNS.json and case summaries in RESULTS.json
are rebuilt and compared; they do not replace the ordinary proof.

Expected final output includes `passed:true`, `unbounded_signs:22`,
`literal_action_columns:88`, `rejections:26`, and deterministic hashes

```
SIGNS_sha256   8f6f36d81d96acea38d4e940b741563fb6310f55f176081e42d2884064bb9c35
records_sha256 5717753ac1627fcf209646a135c8891cb11d17811eb78d63d2f55bba16278a77
```

Use `python verify.py --write` only to regenerate the compact evidence.
No solver, downloaded certificate, private data or large proof corpus is
required. No claim covers q<4 or every intermediate number of deletions.
