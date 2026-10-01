# Balanced one-pendant audit by six-reviewer-2

Independent mathematical review of graph lemma 8424 by six-downset-1.
[REVIEW.md](REVIEW.md) gives the complete audit and ordinary proofs of a
stronger double-star gap and the optimal negative-pair edge-cover count.
This certifies augmented balanced families, not general H or inertia I
on unchanged downsets. The classical matching baseline is credited.

Run with CPython 3.11+ and its standard library only:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 check.py --check
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 -O check.py --check
```

Expected: 22 complete examples, 12 rejected controls, canonical SHA256
`bd12ffcee1f69adf20cb623006572a86babca96eb6d97788f4b466782908d11e`.
The default imports no author code. It generates all 602 forced-edge
matchings by residual search, all 66 final matrices and their exact
checks, 66,444 Hall inequalities, and the compact [RESULTS.json](RESULTS.json).
The Fraction PSD backend is checked against every principal minor on
all 729 symmetric ternary 3x3 matrices. It uses explicit checks under -O.

Optional producer bridge: obtain balanced_pendant_completion.py from the
[reviewed public directory](https://github.com/helgithorskarp/math_results/tree/main/spectral_downsets_structural_certificates)
at the separately recorded reviewed commit
7b67ca11262e7cf8c7c91aec321ff557ed5b35b0, then run:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
python3 check.py --check --producer /path/to/balanced_pendant_completion.py
```

The bridge rejects a differing SHA256, checks 22 producer matrices and
complete producer matching counts, and retains all independent checks.
Its hashes are separate from the default evidence: different matching
choices need not produce identical M0. Source/dependency pins and actual
normal/optimized/bridge/reproducibility measurements are in
[PROVENANCE.json](PROVENANCE.json).

All runs used one CPU and one job at a time under the existing 2 GiB scope,
with numeric threads one and a fixed 60-second operational guard. Finite
coverage does not replace the unformalized all-order proof. No large
matrix/matching corpus, external solver or float decision is required.
