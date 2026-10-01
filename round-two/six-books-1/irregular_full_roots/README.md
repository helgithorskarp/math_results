# Full-degree roots on the irregular Book Ramsey boundary

Actual author **six-books-1**, role **researcher**, 2026-10-01.

A hypothetical ordinary (B4,B7)-avoiding22-point red graph with109 edges
has degree sequence10^21,8 or10^20,9^2. There are guaranteed degree-ten
roots whose ten red neighbors all have degree ten. At every such root,
the local graph is Petersen or Petersen with one edge deleted. Its miss
rows have sizes at most eight or seven, respectively. More generally,
any irregular valid graph with degrees8..10 admitting such a root has
107..109 edges; at107 edges all such neighborhoods are Petersen.

[PROOF.md](PROOF.md) gives the ordinary counting proof and credits the
earlier clique, packing, four-column and contraction mechanisms. No
regular-host finite neighborhood-floor or outside-star enumeration is
imported. The general degree bound is a credited premise of the109-edge
application. This is a structural reduction; the109-edge branch and
the22-versus23 Ramsey gap remain open.

From the repository root, run one command at a time with CPython3.11
and the standard library:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B round-two/six-books-1/irregular_full_roots/check.py
python3 -B -O round-two/six-books-1/irregular_full_roots/verify.py
```

The two programs import no code from each other. They check elementary
finite controls and signed identities, not all valid hosts. Independent
review and proof-assistant formalization are not claimed. Compact
expected data and exact resource measurements are recorded in
[expected.json](expected.json) and [provenance.json](provenance.json).

The21-point matrix is the off-diagonal red complement of the
[authors' known primary construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt).
Original raw SHA256:
`3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55`.
