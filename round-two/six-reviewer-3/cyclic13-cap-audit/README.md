# Independent cyclic13 cap audit

Reviewer: **six-reviewer-3**, independent mathematical reviewer, 2026-10-01.

[REVIEW.md](REVIEW.md) confirms the finite point-budget theorem and the
whole-operator upper-bound argument of committed claim8446. It also proves
rational intervals for the least common real point budgets and smaller
centered caps for the same Pasch closures. Lower ranks, sparse repair and
tensor consequences retain the dependencies specified in the review.

The independent implementation uses unpruned reflected-Gray enumeration of
all4,194,304 subsets of22 tuple-defined translation orbits. It imports no
researcher module and uses integer or rational arithmetic for every proof
check. The compact [expected.json](expected.json) records counts, exact
negative witnesses, joint matrices, margins and transcript hashes.

Run from this directory with Python3.11 or newer, standard library only:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B audit.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B -O audit.py
sha256sum -c SHA256SUMS
```

Both executions use explicit exceptions; optimized Python retains every
check. `--author-expected PATH` additionally compares the independently
derived counts and all12 original comparison records with the author's
compact expected file. It supplies no mathematical input to the computation.
`--propose` is separately marked floating-point exploration and never
establishes a certificate. The default exact audit does not call it.

Only compact source and evidence are published. The complete census and
minor transcripts are regenerated in memory and summarized by hashes.
