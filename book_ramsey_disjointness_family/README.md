# Construction-family obstructions for R(B4,B7)

Author: **six-books-2**, role **researcher**.

[PROOF.md](PROOF.md) gives two rigorous restrictions on natural constructive
routes toward the unresolved 22-versus-23 book Ramsey number.

* For every finite simple H, if its edge-disjointness graph avoids B4 and
  its line graph avoids B7, then H has at most 21 edges. At 21 the only
  nonisolated root graph is K7, yielding the known KG(7,2) construction.
  The proof actually permits maximum root degree up to 10.
* Deleting four vertices from any 26-vertex, 15-regular graph with edge
  codegree eight leaves at least 15 B7 spines. This covers the intersection
  graph of **every** Steiner triple system on 13 points.
* For the explicitly supplied cyclic Steiner(13) system, the exact minimum
  over all 14,950 four-block deletions is **39** B7 spines, attained 13 times.

Neither family can supply a 22-vertex witness through these operations.
The unrestricted Ramsey bounds remain 22 <= R(B4,B7) <= 23.

Run from the repository root, using Python 3.11+ and only its standard library:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 book_ramsey_disjointness_family/verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 book_ramsey_disjointness_family/independent_steiner_check.py
```

The first command independently checks the published irregular baseline,
the Kneser example, all 203 attachment partitions in the equality case,
malformed-input controls, and all 14,950 deletion sets. The second organizes
the deletion computation by each original blue spine instead of by each
deletion set, using the supplied blocks directly. Their ordered vectors
of offending-spine counts agree entry by entry, as recorded by the SHA256
in [expected.json](expected.json). The public evidence is compact; no
external input, solver, floating-point calculation, or large certificate
is needed. Tested with Python 3.11.2, one process and one thread.

The universal bounds are analytic proofs. Their finite checks are validation,
not exhaustive enumeration of arbitrary root graphs. The minimum 39 is an
exact finite computation specific to the supplied cyclic system; its trust
boundary is Python integer/set operations and the inspected enumeration.
The arguments are not formally verified or independently peer reviewed.

The known irregular witness fixture is the complement of the matrix at
https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt .
The retrieved source-file SHA256 was
`3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55`.
The fixture contains only its 93 edges, with vertex labels 0 through 20.
The original matrix's color orientation has codegrees 6/3; complementing
it gives the required 3/6 orientation.

The Kneser construction is known and explicitly attributed in PROOF.md.
Bounded primary-source and conceptual searches did not locate the present
family classification or cyclic deletion minimum. No priority is asserted.
