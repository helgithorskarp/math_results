# Independent regular-six spectral downset review

Author: **six-reviewer-5**, independent mathematical reviewer.

Confirms all 34 regular six-point triple/full-two-skeleton capped Hoffman
certificates and their maximal ranks, star-only equality and all finite
mixed products. [REVIEW.md](REVIEW.md) gives the full verdict, prior-art
qualification and the two nine-point equality/rank boundary examples.
General H/I remain open in this work.

The checker uses independent 10+10 degree matching, the actual full lifted
matrices, exact fraction-free PSD elimination and exhaustive maximal-clique
enumeration. The compact orbit-value [fixture](certificates.json) is credited
to six-downset-3 and copied from verified source commit
`8edf860dda7f604eeb0e3267c761d5b5c78d63d5`; no source code is imported.

Python 3.11+, standard library only. From the repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B spectral_downset_regular_six_review5/audit.py --check spectral_downset_regular_six_review5/expected.json
```

Expected: 3,435 labeled families, 34 classes, 14 transitive classes,
all full ranks N-6 and N-1, exactly six maximum families per class, and
two explicit nine-point boundary families. All guard checks survive `-O`.
No external dataset, solver, floating arithmetic or large tensor is needed.

[SHA256SUMS](SHA256SUMS) authenticates the compact files. Generated output
and any private checkpoints should remain outside this directory.
