# Leaf-neighbor reduction for Book Ramsey candidates

Actual author six-books-1, role researcher. See [PROOF.md](PROOF.md)
for the exact22-vertex/108-edge/maximum-degree-ten hypotheses, ordinary
proof, inherited classification and unresolved completion scope.

Python3.11.2 and its standard library suffice. From this directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 verify.py --self-test
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O verify.py --self-test
```

Both full records must equal [expected.json](expected.json), including
all twelve labeled patterns and literal spine contradictions. The
summary is12 patterns,144 pairs,48 red four-page/96 blue seven-page
violations,9216 single cross-edge controls,144 all-red cross-block
controls, and the seven-page injection obstruction. The self-test
rejects eight damaged records through the actual expected-record check.

The producer exhausts6561 column assignments; the independent checker
uses4900 ordered row pairs and literal Boolean-matrix pages. The complete
interface-list SHA256 is
`9b50aaadcd0357d0757e6d9cf6d00959842a51373c9f3d5abf0fe115a5e5e2d3`.
These are small necessary-interface controls, not complete host enumeration
or peer review. The written proof handles every cross-block completion.

[primary21.blue](primary21.blue) is the freshly verified prior21-point
matrix, one means blue off diagonal and zero means red off diagonal.
Both programs reproduce93 red edges and page maxima3/6. Source provenance
is in [provenance.json](provenance.json); hashes in [MANIFEST.json](MANIFEST.json).
No cache, generated corpus or solver dependency is required. Every run
was measured serially with one numerical thread and a fixed90-second
guard; compact timing evidence is recorded in provenance. No guard was
reached or resource limit raised.
