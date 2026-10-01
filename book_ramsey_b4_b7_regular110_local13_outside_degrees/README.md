# R(B4,B7): outside degrees at a thirteen-edge regular root

Actual author **six-books-3**, role **researcher**, 2026-10-01.

In every valid ten-regular red graph on 22 vertices, if the ten red
neighbors of a vertex span thirteen edges, its eleven blue neighbors
induce a red graph of degree sequence **5,5,4^9**. Here valid means red
edge codegrees at most three and blue edge codegrees at most six.

The finite computation assumes the explicit local degree sequence
2^4,3^6. Its complete exclusion of a six-point miss row is proved in
[PROOF.md](PROOF.md); the thirteen-edge corollary uses the credited
[positive-codegree result](../book_ramsey_b4_b7_regular110_positive_codegrees/PROOF.md).
The computation leaves two five-point miss rows, with nine four-point
rows. It does not exclude that remaining case or resolve R(B4,B7).

Use CPython 3.11 or later; all code uses only the standard library:

```bash
cd book_ramsey_b4_b7_regular110_local13_outside_degrees
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 generate.py
python3 -O check.py
python3 check.py --compare-generator
python3 -O controls.py
```

Run these sequentially. Generation compares fresh compact certificate
bytes against the published files. `--write-certificates` explicitly
regenerates those files. The default checker imports no generator and
checks all integer negative forms after its own finite census. The
comparison mode additionally requires equality of the complete state
sets and every residual matrix entry.

Expected: **2607** labeled F graphs, **11** F orbits, **56** normalized
profiles, **256500** labeled local cores, **43** admissible six-point rows,
**42** covering configurations and **40191** excluded matrices. There
are **208** primitive integer witnesses, maximum absolute entry **863**.
Detailed hashes, control counts and measured limits are in
[RESULTS.md](RESULTS.md) and [MANIFEST.json](MANIFEST.json).

The two implementations are by the same researcher. This is separately
implemented exact verification with written completeness bridges, not
an independent review or a proof-assistant formalization. The fixture
[baseline21.rows](baseline21.rows) verifies an existing primary
21-vertex construction; it is not new research. Raw local-core and
matrix corpora are reconstructed in memory and are not distributed.
