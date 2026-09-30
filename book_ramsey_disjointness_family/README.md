# Construction-family obstructions for R(B4,B7)

Author: **six-books-2**, role **researcher**.

[PROOF.md](PROOF.md) gives rigorous restrictions on natural constructive
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
* [CROSS_REPAIR.md](CROSS_REPAIR.md) rules out all **2^96** cross-edge
  assignments between an explicit sixteen-vertex Steiner core and six
  vertices forming a blue clique. Two complete 2^16 row checks and the
  analytic inequality 75>72 establish the exclusion.
* [ONE_RED_EDGE.md](ONE_RED_EDGE.md) also excludes the same fixed core
  when the six-vertex part has **exactly one red edge**. A complete
  endpoint reduction leaves 102 pairs, all closed by thirteen compact
  book certificates. Retaining the core therefore requires at least
  two internal red edges in the six-vertex part.
* [TWO_RED_EDGES.md](TWO_RED_EDGES.md) excludes both internal two-red-edge
  patterns, covering all 105 placements and arbitrary cross assignments.
  A C++ enumeration and separate Python indexed checker compare the complete
  domains entry by entry. Retaining this core requires **at least three**
  internal red edges.
* [THREE_RED_EDGES.md](THREE_RED_EDGES.md) excludes all five internal
  three-red-edge patterns, covering all 455 placements and arbitrary
  cross assignments. Separate exact implementations reconstruct every
  decisive domain and twelve explicit triangle books. Retaining this
  core therefore requires **at least four internal red edges**.

Neither family can supply a 22-vertex witness through these operations.
The unrestricted Ramsey bounds remain 22 <= R(B4,B7) <= 23.

Run from the repository root, using Python 3.11+ and its standard library.
The two- and three-edge commands also need a GCC/Clang-compatible C++17 compiler:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 book_ramsey_disjointness_family/verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 book_ramsey_disjointness_family/independent_steiner_check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 book_ramsey_disjointness_family/verify_cross_repair.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 book_ramsey_disjointness_family/check_one_red_edge.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 book_ramsey_disjointness_family/independent_one_red_edge.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 book_ramsey_disjointness_family/check_two_edges.py --scratch scratch/books_two_edges
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 book_ramsey_disjointness_family/independent_two_edges.py scratch/books_two_edges/two_edges.trace
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 book_ramsey_disjointness_family/check_three_edges.py --scratch scratch/books_three_edges
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 book_ramsey_disjointness_family/independent_three_edges.py scratch/books_three_edges
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

The third command reconstructs the new core from the triples, compares it
to the labeled edge fixture, and checks every row subset twice by different
representations and traversal orders. Its compact output is
[cross_expected.json](cross_expected.json). The 2^96 coverage follows from
the written counting proof; those cross assignments are not enumerated.

The fourth and fifth commands prove the single-red-edge extension exclusion.
Mask/fixture and combination/triple implementations compare all 1,786
retained endpoint rows and all 102 accepted endpoint pairs entry by entry.
They check one book certificate for the four-ten-row case and twelve
certificates on partial graphs for the remaining cases. Exact expected
output is [one_edge_expected.json](one_edge_expected.json).

The sixth and seventh commands prove the two-red-edge exclusion. The 2.46 MB trace
is regenerated in scratch and checked entry by entry; it is not published.
[TWO_RED_EDGES.md](TWO_RED_EDGES.md) gives coverage and trust boundaries.

The last two commands prove the three-red-edge exclusion. All traces are
regenerated in scratch and compared entry by entry. The five complete
prefix searches and their coverage are described in
[THREE_RED_EDGES.md](THREE_RED_EDGES.md). No teammate degree or edge bound
is used in either implementation.

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
The source construction is by Lidicky, McKinley, Pfender and Van Overberghe
and is adapted under its [CC BY 4.0 license](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/LICENSE.md).

The Kneser construction is known and explicitly attributed in PROOF.md.
Bounded primary-source and conceptual searches did not locate the present
family classification or cyclic deletion minimum. No priority is asserted.
