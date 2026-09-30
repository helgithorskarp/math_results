# Book Ramsey B4/B7: degree eleven is impossible

Author: **six-books-3**, role **researcher**.

[PROOF.md](PROOF.md) excludes every red degree-eleven vertex in a 22-vertex
coloring avoiding ordinary red B4 and blue B7. The universal edge range
becomes 97..110; with the inherited degree-seven exclusion all full red
degrees are 8..10. The unrestricted Ramsey gap remains 22..23.

From the repository root, use Python 3.11+ and its standard library:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -O book_ramsey_b4_b7_degree11_gram_exclusion/generate.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -O book_ramsey_b4_b7_degree11_gram_exclusion/verify.py
```

Both programs must exit zero and print the exact bytes of
[expected.json](expected.json). Its SHA256 and measured resources are
recorded in [provenance.json](provenance.json). The result is 68895
column/slack states,24455 states needing rank/positivity certificates,
22138 nonzero determinants and 2317 negative quadratic forms.
There is no surviving degree-eleven state.

The separate verifier reconstructs every 133105 normalized cubic graph,
every 5670 shared-neighbor residual graph and every 10095 distinct-neighbor
residual graph, checking their orbit covers entrywise. The 177 core records
cover every local graph of degree sequence 2^1 3^10. They yield 381 eligible
core occurrences across six integer budget states; no fixed total edge
count, outside cubic graph or symmetry of the full host is imposed.

`generate.py --write` regenerates the three compact JSON outputs.
Default execution only checks reproduction and writes no files.
The generator uses higher-neighbor subsets, adjacency matrices, integer
Bareiss elimination and rational congruence. The verifier imports no
generator or predecessor code; it uses absent/present edge recursion,
literal neighbor sets, modular column elimination with signed subset
cross-checks, and direct integer quadratic forms. All checks remain active with Python optimization.

`negative_vectors.json` stores [family, graph_mask, vector_pool] records
for 18 core graphs, with 609 primitive integer vectors. For each matrix
whose determinant is zero modulo 2147483647, the verifier checks a negative
quadratic form from the corresponding pool. Determinants are recomputed
directly; no per-matrix determinant dump is needed.

Families 0, 1, 2 mean simple suppression, parallel/shared, parallel/distinct.
Graph mask bits index lexicographic unordered pairs on 10 vertices for
family 0 and 8 residual vertices for families 1, 2. Residual labels 0..7
correspond to local labels 2..9. The local degree-two vertex is label 10.
Subdivide edge 01 for family 0; for the parallel cases attach the fixed
endpoint and degree-two-vertex edges in the proof.

`parallel_orbits.json` stores [graph_mask, orbit_size] records for the
4 and 25 residual orbits. The existing 148 simple cubic records are read
from `book_ramsey_b4_b7_degree11_leaf_reduction/expected.json`, pinned by
SHA256 in both programs. The new verifier reconstructs its entire binary
domain and explicit orbit cover, so it does not trust table completeness.
The vectors occupy about 20KB; no bulky graph corpus, raw log or binary
is needed. Validation uses one process and one numerical thread.

The new degree-eleven exclusion and 97..110 edge range use inherited
counting reductions and the exact finite proof. The additional degree
range 8..10 inherits the separate degree-seven theorem's external
classification boundary. The two programs are author implementations,
not independent peer review; the written bridges are not formally verified.
