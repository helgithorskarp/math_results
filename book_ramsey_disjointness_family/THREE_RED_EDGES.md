# The fixed Steiner core requires at least four internal red edges

Author: **six-books-2**, role **researcher**, 2026-09-30.

**Theorem.** Let F be exactly the labeled sixteen-vertex red graph in
[core16.edges](core16.edges), with every remaining core edge blue. Add six
vertices X and assign all 96 cross edges arbitrarily. If X has exactly
three red edges, the resulting graph has a red B4 or a blue B7. Together
with the [previous zero-, one- and two-edge exclusions](TWO_RED_EDGES.md),
any valid order-22 graph retaining F must have **at least four internal
red edges in X**.

Books are ordinary, noninduced subgraphs. The theorem assumes no symmetry,
degree range, edge count or regularity of the extension. Its coverage is
all 2^96 cross assignments for each of the 455 labeled three-edge placements.
It does not decide the unrestricted Ramsey problem.

## Core, complete row domain and a ten-row reduction

For completeness, construct F as follows. On points modulo 13, list the
26 triples x+{0,1,4} for x=0,...,12, followed by x+{0,2,7} in the same
order. Retain blocks with indices

    1,3,4,7,8,9,10,11,12,13,14,15,16,20,23,24.

Label them 0,...,15 in this order, and make disjoint triples red-adjacent.
This agrees exactly with the edge fixture. It is a six-regular red graph
with 48 edges. Its 120 core spines have residual page capacities
0:3, 1:45, 2:69, 3:3, counting both colors.

Write N_x for the red core neighbors of an outside vertex and
B_x=V(F)\N_x. All 65,536 subsets are checked for the exact one-vertex
conditions: core-spine capacity, at most three red pages at every red
cross spine, and at most six blue pages at every blue cross spine. There
are 3,138 valid rows, with size distribution

| Red row size | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---:|---:|---:|---:|---:|---:|
| Rows | 12 | 569 | 1,661 | 801 | 91 | 4 |

The four ten-row masks are 31861, 46954, 54748, 56199. Each induces a
cubic graph. A row of size ten cannot have two internal red neighbors:
every such neighbor must have its red row disjoint from the ten-row,
or a red cross spine already having three core pages gets a fourth.
If two such neighbors are blue-adjacent, they have all ten core vertices
as common blue pages. If they are red-adjacent, both red rows have size
at least five inside a six-set; their intersection has size at least four.
Either gives a forbidden book. Hence **every outside vertex with internal
red degree at least two has row size at most nine**. This uses no external
degree theorem.

All outside row masks are distinct. Equal rows on a red pair have at least
five common red core pages. On a blue pair, equal blue rows have at least
six core pages plus a common blue internal vertex. Every blue pair in the
five patterns below has at least one such vertex, as also checked from
their complete internal adjacency lists.

## All five patterns and normalization

Outside vertex 16+r has role r=0,...,5. Only the following pairs are red;
every other internal pair is blue.

| Pattern | Red pairs | Ordinary roles | Labeled placements |
|---|---|---|---:|
| Triangle plus three isolates | (3,4),(3,5),(4,5) | 0,1,2 | 20 |
| Star plus two isolates | (2,3),(2,4),(2,5) | 0,1 | 60 |
| Four-vertex path plus two isolates | (2,3),(3,4),(4,5) | 0,1 | 180 |
| Three-vertex path, a separate edge and an isolate | (1,2),(1,3),(4,5) | 0 | 180 |
| Three disjoint edges | (0,1),(2,3),(4,5) | none | 15 |

These exhaust all possibilities. A cycle with three edges is a triangle.
A forest of maximum degree at most three is either the three-edge star, a path
with two degree-two vertices, a path of two edges plus a separate edge,
or a matching. Their counts sum to binom(15,3)=455. The independent checker
also classifies all 455 edge subsets by these distinct degree multisets.
Normalization permutes only X, fixing every core label. It does not
assume that the graph respects an automorphism of F.

## Exact prefix coverage

All internal X edges are known at the start. An unassigned cross edge
belongs to neither known color. A book in known edges survives every
completion. The four exact prefix inequalities are those in
[TWO_RED_EDGES.md](TWO_RED_EDGES.md): core-spine residual capacity,
assigned internal-pair codegree including all internal pages, and the
red and blue cross-spine page budgets. Explicitly, for internal pattern J,
an assigned pair xz in color c has

    |C_x intersect C_z| + |J_c(x) intersect J_c(z)| <= q_c,

where C is N for red and B for blue, and q is 3 or 6. A red cross spine xy
has d_{F[N_x]}(y) plus assigned red internal neighbors containing y.
A blue cross spine has |B_x|-1-d_{F[B_x]}(y) plus assigned blue internal
neighbors containing y. These, together with core-spine capacities,
check every known spine. A pair with an unassigned endpoint has no known
common core pages; its internal page count is below the cap.

A domain is the **complete** set of one-vertex rows that can extend a valid
prefix without a known book. It is obtained by all four inequalities,
never by a score or heuristic. A previously computed domain can be used
as a base only when the new role has exactly the same constraints on
that earlier prefix. Later assignments can remove candidates but cannot
add them. Row sorting below uses only explicitly interchangeable roles.

**Triangle.** Sort the three ordinary rows. There are 58,836 valid ordinary
pairs and 3,294 valid ordinary triples. The complete single-endpoint
domains (size at most nine) have 123 total occurrences, maximum four.
They are the same for roles 3,4,5; the Python checker verifies the equality
directly. Only three ordinary contexts have at least three endpoint rows.
All twelve unordered endpoint triples have literal book certificates.
Their spines and pages are regenerated and independently verified.
Thus no triangle extension survives.

**Star.** Sort the ordinary pair. For every one of its 58,836 contexts,
compute the single-center domain (size at most nine) and the single-leaf
domain. Fewer than three distinct leaf rows rules out the three leaves
immediately. In the remaining contexts, all 127,614 ordinary-pair/center
prefixes are tested. Their complete single-leaf domains have sizes
0 in 127,560 cases, 1 in 45, and 2 in 9. None supplies three distinct
leaves, which share this domain before their own rows are assigned.

**Four-vertex path.** Sort the ordinary pair. Compute complete endpoint
and inner-vertex domains at every ordinary context; the inner vertices
have size at most nine. Every possible first endpoint is tried with
every compatible adjacent inner vertex. Exactly 63 such prefixes survive.
In each the complete domain of the next inner vertex is empty. This
excludes the path without needing to assign its last endpoint.

**Three-vertex path plus edge.** Try every one of the 3,138 ordinary rows.
For each, compute its leaf domain; there are 247,628 leaf occurrences.
Sort the two interchangeable leaves. Exactly 228,594 ordinary/two-leaf
prefixes are valid. In every one, the complete center domain, with row
size at most nine, is empty. No assignment of the separate edge is needed.

**Three disjoint edges.** Sort each edge's endpoint rows, and sort edges by
their smaller row. Enumerate all 57,601 possible first red pairs. For each,
try the smaller endpoint of the second edge, larger than the first edge's
smaller endpoint. Exactly 29,143 prefixes survive. In every one, the
complete domain of its red partner is empty. Sorting the partner above
the second endpoint loses no edge. No third edge is needed.

Every complete valid graph would follow one of these retained prefixes.
The stated zero domains or explicit books therefore exclude every cross
assignment in each pattern. Counts and hashes are reproducibility checks;
the complete generation and this prefix argument supply coverage.

## Reproduction and trust boundary

From the repository root, Python 3.11+ and a GCC/Clang-compatible C++17
compiler supporting unsigned 128-bit integers:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 book_ramsey_disjointness_family/check_three_edges.py --scratch scratch/books_three_edges
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 book_ramsey_disjointness_family/independent_three_edges.py scratch/books_three_edges
```

[search_three_edges.cpp](search_three_edges.cpp) scans masks and candidates,
packs core capacity use in 120 bits, and emits the complete decisive domain
records. [check_three_edges.py](check_three_edges.py) requires successful,
complete termination for all five patterns and compares the compact
[expected diagnostics](three_edges_expected.json). Any timeout or failed
process raises an error and establishes nothing.

[independent_three_edges.py](independent_three_edges.py) imports no generator
code. It reconstructs F from literal Steiner triples, traverses subsets
as combinations, and derives indexed sets of row IDs satisfying each
point, core-spine and pair inequality. Domain intersection replaces the
C++ candidate scan. It independently rebuilds every frontier and compares
all emitted domains entry by entry, including all 228,594 and 29,143
decisive empty domains in the last two patterns. It checks the twelve
triangle books with literal red and blue neighborhoods. Both programs
compute the full domains; no external catalogue or solver is trusted.

Traces and executable are regenerated in scratch and are not published.
The trust boundary is inspected exact C++/Python code, the labeled fixture
and Steiner construction, and the written, unformalized normalization
and completeness argument. These are author cross-checks, not independent
peer review or proof-assistant verification. No floating-point verdict,
incomplete enumeration or resource failure is used as nonexistence evidence.

## Prior work and scope

The primary [Lidicky--McKinley--Pfender--Van Overberghe paper, Table 1](https://arxiv.org/pdf/2407.07285)
and [Radziszowski DS1.18, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf)
were reopened on 2026-09-30. The located unrestricted interval remains
22--23. The known 21-vertex constructions were reproduced and attributed
in [README.md](README.md); reproduction is validation, not novelty. No
priority is asserted, and the global flag-algebra upper certificate has
not been independently replayed.

six-books-1's [capacity theorem](../book_ramsey_4_7_degree_reductions/capacity.md),
source commit `2e6f85b554f425b546c5f45af2d2d4228ea8b2c4`, gives universal
degree range 7--11 and edge range 97--121. Its
[degree-seven conditional theorem](../book_ramsey_4_7_degree_reductions/single_degree7.md),
source commit `d5b0389df7756c6c3b0629b08dcdcd0a8b5b94ac`, restricts a witness
having degree seven to 105--115 edges. On this three-edge frontier, 51 red
edges are fixed, so these would give row sum 46--70, or 54--64 when degree
seven occurs, and 7<=|N_x|+d_J(x)<=11. No such cuts are used in either final
enumeration. The new exactly-three-edge theorem is independent of those
peer theorems. The earlier zero/one/two exclusions are premises only of
the combined at-least-four statement. Patterns with four or more internal
red edges, and graphs not retaining F, remain unresolved here.
