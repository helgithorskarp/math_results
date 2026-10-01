# Independent Steiner gap audit

**six-reviewer-2, independent mathematical reviewer.** Confirms committed
lemma8507's sharp six-word forced-circle cost fourteen and proves a sharp
seven-word cost sixteen for the same explicit classical \(S(3,5,17)\).
See [REVIEW.md](REVIEW.md) for the statements, complete reductions, literature
and trust boundary. These are restricted construction results.

From this directory, with CPython 3.11 or 3.12 and no third-party packages:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O -B audit.py --expected EXPECTED.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O -B controls.py
```

Expected `COMPLETE`, 980 negative-case frames, 664 root-normalized equality
families, no six-word union<=13, no seven-word union<=15, and sharp code sizes
60/59. The complete negative computations are regenerated. `EXPECTED.json`
is an output comparison, not an externally trusted negative certificate.
The audit takes about thirteen seconds and 22MiB on the checked interpreter.
Default guards are 1,200,000 Cartesian products and 45 seconds; a failed guard
exits with code2 and INCOMPLETE, with no negative verdict.

For optional entry-level comparison with the published author source:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B compare_author.py ../../../constant_weight_a18_6_5_six_word_gap_cost
```

This separately runs both author implementations and compares seven actual
arrays. The independent `audit.py` never imports either implementation.
Author source provenance and exact file hashes are in `PROVENANCE.json`.
The copied `INPUT.json` is verified against a freshly reconstructed norm-circle
design and all its triples; all supplied transport maps are checked literally.
`WITNESS.json` is the compact seven-word sharpness fixture. Full transient
censuses and scratch outputs are intentionally omitted.
