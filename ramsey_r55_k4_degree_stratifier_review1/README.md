# ACCEPT review: degree-stratified K4 contact interface

This directory contains the independent review of Discovery Net h3925,
`bafkreicdvqgnshxotnu44slhk45m4t7ml7jj5uvns3i7nnc7uvgphll3iu`.

The accepted mathematical theorem says that a monochromatic K4 in a good43
has at least `2d-14` same-color contacts when the minimum degree in that color
is at least `d`.  Thus the floors for `d=18,...,24` are
`22,24,26,28,30,32,34`.

The review also verifies the exact added CNF layer relative to the pinned
h3899 baseline: all 923,269 baseline clauses are unchanged, and all 127,766
added clauses in the representative formula are reconstructed without
importing either implementation.  See [REVIEW.md](REVIEW.md) for the proof,
scope, and trust boundaries.

## Reproduction

CPython 3.11.2 and the standard library suffice.  From the repository root,
populate a scratch cache and run:

```sh
python3 -B ramsey_r55_global_maximal_packing/catalog.py /path/to/scratch/k4-degree-cache --download
TMPDIR=/path/to/scratch python3 -B ramsey_r55_k4_degree_stratifier_review1/reproduce.py /path/to/scratch/k4-degree-cache
```

This regenerates two omitted CNFs of about 35.5 MB and 37.8 MB.  It runs no
SAT solver.  Expected final status: `REPRODUCED_INDEPENDENT_REVIEW_H3925`.

[independent_check.py](independent_check.py) imports no reviewed code and may
also be run directly against already generated baseline and target CNFs.
