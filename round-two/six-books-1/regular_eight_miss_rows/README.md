# Eight-point miss rows in R(B4,B7)

Actual author **six-books-1**, role **researcher**, 2026-10-01.

In a red ten-regular graph on 22 vertices avoiding ordinary red B4 and
blue B7, consider the ten-point red neighborhood A of any root. If an
outside blue neighbor misses eight A points, the induced graph on A
must be cubic and triangle-free. Its eleven outside miss rows have
sizes **8,5,5,4,4,4,4,4,4,4,4**. Each five-row meets the two points
omitted by the eight-row, and their intersections with the eight-row
overlap in at most two points.

Equivalently, a blue pair with exactly two common red neighbors forces
these restrictions at both endpoints. In the whole-graph capacity
defect, such pairs form a matching; each endpoint has nonzero defect
weights exactly **4,1,1**, all on blue pairs. This is a necessary
condition, with no host existence or endpoint assertion.

[PROOF.md](PROOF.md) gives an ordinary analytic proof. The new reductions
are the exclusion of `8+6+4^9` and the stated restrictions on `8+5+5+4^8`.
It also replaces the earlier finite local-fourteen eight-row exclusion
with an analytic contraction: adding the two low points' edge gives
the residual Gram `K(P+E)`, so a trace identity and repeated rows yield
a literal forbidden book. The latter exclusion was already known.

The explicit proof dependencies are the analytic portions of
[regular blue-codegree lemma8541](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/regular_blue_codegrees/PROOF.md)
and [low-neighbor packing lemma8559](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/local14-disjoint/PROOF.md).
No finite local catalogue, global minimum-degree result, solver, or
approximate arithmetic is a premise. The proof is unformalized and
conditional on ten-regularity. Independent review of this result is
pending; the two programs below share the stated author.

From the repository root, use **CPython 3.11.2**, standard library only,
one command at a time:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B round-two/six-books-1/regular_eight_miss_rows/check.py
python3 -B -O round-two/six-books-1/regular_eight_miss_rows/verify.py
```

Both fail on mismatched compact [expected.json](expected.json). They
import no code from one another. The generator uses direct column
margins for all 2,040 cubic bipartite five-by-five matrices; the separate
checker uses the complement's C10 or C4+C6 decomposition. Their complete
sorted matrix lists agree. Four independent triples on six points are
constructed by disjoint-intersection enumeration and independently by
assigning all six K4 edges to the outside labels; all 720 labeled
records agree. These enumerations validate elementary written steps;
they are not a census of valid 22-vertex hosts.

The checks also compare 204,000 pair-capacity entries, admissible word
records and 3,600 possible second-five-row records. Of the bipartite
six-row controls, 600 have negative capacity and the other 1,440 each
have eight admissible four-words, all meeting the distinguished side
in at most one point. All 15 marked complementary-matching controls
are checked, with 3 five-word lists and 12 fourteen-word lists. The
local-fourteen contraction is replayed on a literal ten-regular
22-point control with a nine-page blue book. This deliberately invalid
control checks the proof's final contradiction; it is not a witness.
Seven corrupted versions are rejected, even with Python assertions
disabled. Written completeness and spectral bridges remain analytic.

The [21-point fixture](baseline21.rows) is the off-diagonal complement
of the authors' [primary construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt),
whose raw SHA256 is
`3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55`.
A fresh download on 2026-10-01 matches it. Both programs reproduce
93 red edges, degree histogram 8:4,9:16,10:1, and page maxima 3/6.
This known construction is baseline validation, not a new result.

The unrestricted Ramsey gap remains **22..23**, as recorded in the
[primary Table1](https://arxiv.org/pdf/2407.07285) and
[Small Ramsey Numbers TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf).
The 23-vertex upper certificate was not independently replayed.
The constrained `8+5+5` branch and the rest of the regular and
unrestricted host problem remain open. Measured costs and provenance
are in [provenance.json](provenance.json).
