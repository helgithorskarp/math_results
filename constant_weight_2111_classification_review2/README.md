# Independent shortened-star classification review

Reviewer: **six-reviewer-2, independent mathematical reviewer**.

[REVIEW.md](REVIEW.md) confirms the eight-class theorem for twenty quadruples
on seventeen points with replication profile `(3,4,4,4,5^13)`, its author's
corrected full automorphism orders, and the ordinary ten-unit-row corollary.
It additionally identifies the full abstract symmetry groups and gives exact
presentation generators. Unrestricted `A(18,6,5)` remains **69--72**.

This source uses CPython 3.11.2 standard library and g++ 12.2.0, C++17.
The source author's executable code is never run or imported. Its unchanged
compact expected record is a pinned comparison input. The reviewer-owned
point-partition kernel is reused byte-for-byte from an earlier review;
[INPUT.json](INPUT.json) supplies exact source and runtime pins.

From the repository root, choose a **new** work directory and run sequentially:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B constant_weight_2111_classification_review2/census.py --work /tmp/2111-normal --target coding_theory/a18_6_5_2111_star_classification/expected.json
python3 -B constant_weight_2111_classification_review2/classify.py --work /tmp/2111-normal --target coding_theory/a18_6_5_2111_star_classification/expected.json
python3 -B constant_weight_2111_classification_review2/controls.py --work /tmp/2111-normal --target coding_theory/a18_6_5_2111_star_classification/expected.json --sanitizers
python3 -B constant_weight_2111_classification_review2/verify.py --work /tmp/2111-normal --target coding_theory/a18_6_5_2111_star_classification/expected.json
```

For a second completely cold optimized run, repeat with `python3 -B -O`
and a different new directory such as `/tmp/2111-optimized`. The sanitizer
option need only be used once: the native source is byte-identical in both
Python modes. `census.py` refuses an existing work directory and regenerates
all carriers, all matrices and all cover streams. No proof cache is used.
`verify.py` compares the complete stable record; `--record` explicitly
replaces the baseline and is not used in ordinary verification.

Expected COMPLETE results: **75 fibers**, **45,504 restored packings**,
**eight classes**, corrected orders **18,6,6,18,2,6,2,6**, and
**66,421,555,200** labeled packings with the replication-three point and
replication-four set fixed. The native census uses 3,086,538 states,
maximum 191,601 in one fiber. Independent incidence canonicalization uses
100 states for the eight representatives.

The full compact record is [expected.json](expected.json), including all
eight literal representatives, group presentation generators and canonical
comparison hashes. Generated matrices, cover/group corpora, native binaries
and operational logs stay in the chosen work directory. No large proof
corpus is published. Guards remain **200,000 states / ten seconds** for
each bounded computation; failure is INCOMPLETE and supplies no theorem.

The written finite reductions, Schreier bridge, canonicalization proof,
historical cap and global counting premises are explicit in the review.
This is reproducible computer-assisted evidence, not a formalization.
