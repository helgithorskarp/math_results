# Two productive TAIL parents for a literal minimum-eight prefix

Author: **six-covering-3, researcher**.

For P=(8:0,9:0,10:1,14:1,12:10), all 36 unused original divisors of 2520
at least 8 leave at least 2 holes outside each odd parent modulo 8, and at
least 40 outside each of parents 2 and 6. Together with published lemma 9709
for parent 4, the holes meet two parents. Any distinct cover by divisors of
10080 containing P therefore needs productive TAIL in two different parents.
Original 16/32 presence and other TAIL phases are not prescribed.

[proof.md](proof.md) states the exact scope, structural transport and
completion/marginal/lifting bridges. This is an author-checked computational
lemma; it neither excludes full P covers nor improves global L_min(8).
No external review, formalization or historical priority is claimed.

From this directory, reproduce all six new cases and controls:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -B reproduce.py --scratch /absolute/workspace/scratch/multi-parent-check
```

Python 3.11.2, standard library only. Every child has an unchanged 20s guard,
one CPU child runs at a time, and all numerical thread settings are 1. The
driver regenerates all 270 raw 15/18 phase pairs for each of six parents in
both normal and optimized modes. Independent literal AP checks compare every
one of the 1620 records field by field. It expects deficits 2,40,2,2,40,2 and
27 rejected damages per mode. `certificate.json` contains compact expected
cases; `verification.json` contains the measured author receipt. Raw streams
and generated receipts stay in workspace/scratch, outside this source.

The **parent 4 dependency is separate** and must be retained in the combined
theorem. From the repository root, its published source is reproduced by:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -B round-two/six-covering-3/parent4-base-obstruction/reproduce.py \
  --scratch /absolute/workspace/scratch/parent4-base-check
```

That command independently replays its 288-map affine normal form and all
four stages. Its published proof and validation are linked in
[dependencies.json](dependencies.json), with the exact committed reference
and verified source SHA. No numeric bounds from the other color or row
results are imported. Both contributions have unformalized elementary
bridges and different algorithms by the same author, without an external
independent review. Completion of a subset never establishes that every
original occurs in an irredundant covering.
