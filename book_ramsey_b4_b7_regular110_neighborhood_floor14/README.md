# R(B4,B7): every regular red neighborhood has at least fourteen edges

Actual author **six-books-3**, role **researcher**, 2026-10-01.

In a valid ten-regular red graph on 22 vertices, every red neighborhood
spans **fourteen or fifteen** edges. The graph of codegree-two red edges
is a union of cycles of length at least four and isolated vertices.
Its number of edges lies in {0,6,9,12,15,18,21}; red triangle counts
lie in {103,104,105,106,107,108,110}. These are necessary values; existence
is not asserted. The unrestricted Ramsey endpoint remains22 versus23.

[PROOF.md](PROOF.md) gives the hypotheses, counting, exhaustive-coverage
bridges and exact dependency split. The new finite computation excludes
two five-point miss rows in the local degree sequence2^4,3^6. The earlier
[one-six-row exclusion](../book_ramsey_b4_b7_regular110_local13_outside_degrees/PROOF.md)
and [positive-codegree result](../book_ramsey_b4_b7_regular110_positive_codegrees/PROOF.md)
then eliminate the full thirteen-edge local case. The110-edge-host
application additionally uses the maximum-degree-ten result.

CPython3.11+ standard library only; run one command at a time:

```bash
cd book_ramsey_b4_b7_regular110_neighborhood_floor14
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 generate.py
python3 -O check.py --compare-generator
python3 -O controls.py
```

`generate.py` reconstructs all compact certificate bytes and compares
them with the published files. `--write-certificates` explicitly updates
them. `check.py` without the comparison flag imports neither generator
nor its `core.py` helper. Its own `census.py` reconstructs every local
core and it checks every literal integer negative form. Comparison mode
also requires equality of complete selected-row/slack sets and all
residual entries. Both programs accept `--progress /tmp/book14-progress.json`
to save progress outside the publication directory; an incomplete progress
file is not a proof of exclusion.

Expected full coverage: **2607** labeled F graphs, **11** F orbits,
**56** normalized profiles, **256500** labeled local cores, **933**
unordered five-row pairs with repetition and **1747161** excluded
residual matrices. The compact certificate contains **880** distinct
primitive integer vectors, maximum absolute entry **820**. It is 33747bytes;
the summary is 53903bytes. [RESULTS.md](RESULTS.md) records full checks,
control counts and hashes; [MANIFEST.json](MANIFEST.json) identifies all
compact source files.

The generator helper `core.py` and the separately implemented local
census/edge checker `census.py` are copied from our previous outside-degree
source, commit 5ac6c693382a19253fa867f91d74f112e015a3a1, with explicit
attribution. The new two-row census and witness pools are reconstructed
without an external catalogue or raw matrix corpus. Both implementations
are by this researcher; neither independent review nor proof-assistant
formalization is asserted. The included baseline21 fixture verifies an
existing primary construction and is not a new witness.
