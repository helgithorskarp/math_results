# A fixed Steiner core requires at least three internal red edges

Author: **six-books-2**, role **researcher**, 2026-09-30.

**Theorem.** Keep the labeled sixteen-vertex red graph F in
[core16.edges](core16.edges). Add six vertices X and assign all 96 cross
edges arbitrarily. If X spans exactly two red edges, the resulting graph
contains a red B4 or a blue B7. Together with [CROSS_REPAIR.md](CROSS_REPAIR.md)
and [ONE_RED_EDGE.md](ONE_RED_EDGE.md), every hypothetical valid 22-vertex
graph retaining F therefore has **at least three red edges inside X**.
Books are ordinary, noninduced subgraphs; page-to-page edges are unrestricted.
This family theorem does not decide the global Ramsey problem.

There is **no degree, edge-count, regularity or automorphism assumption on
the extension**. The coverage is all 2^96 cross assignments for each of the
105 internal two-edge placements, by the prefix argument below.

## Complete row domain

Core labels are 0,...,15 and outside vertex 16+r has role r=0,...,5.
Write N_x for its red core neighbors and B_x=V(F)\N_x. A red cross spine
xy requires d_{F[N_x]}(y)<=3. Because F is six-regular, the cut of N_x has
at least 3|N_x| and at most 6(16-|N_x|) edges, so |N_x|<=10.

At blue cross spine xy, y in B_x, its core blue page count is

    beta_x(y)=|B_x|-1-d_{F[B_x]}(y).

The allowance for outside pages is 6-beta_x(y). Each old core spine ij
has residual capacity 3-c_R(i,j) if red and 6-c_B(i,j) if blue. A row
consumes one unit when both endpoints are in its corresponding color set.
These old-spine and new-cross-spine conditions are necessary and sufficient
for adding one vertex to F. Both implementations check all 65,536 subsets
and obtain exactly **3,138** rows:

| Red row size | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---:|---:|---:|---:|---:|---:|
| Number | 12 | 569 | 1661 | 801 | 91 | 4 |

The four size-ten masks are 31861, 46954, 54748, 56199; each induces a
cubic subgraph. Bit y represents core vertex y. These are finite facts
about this exact F, not facts from a graph catalogue.

## Internal patterns and ten-row reductions

Up to permuting X while fixing **every** core label, exactly two red edges
have two types:

* Matching M: pairs (2,3),(4,5), ordinary roles 0,1. Its 45 placements
  are binom(6,4)*3.
* Path P: pairs (3,4),(3,5), ordinary roles 0,1,2, center 3, leaves 4,5.
  Its 60 placements are binom(6,3)*3.

All other internal edges are blue. Their 45+60 count is binom(15,2), so
the normalization loses no placement and uses no symmetry of F.

If N_x has size ten, its local degrees are three. Every internal red
neighbor z must have N_z disjoint from N_x: a vertex y in the intersection
would make red spine xy have its three core pages plus z.

In the matching, suppose role 2 has a ten-row. Its partner N_3 is a subset
of its complementary six-set, and B_2 union B_3=V(F). Each ordinary vertex
o has blue overlaps at most three with both paired endpoints, whose
internal blue spines already have three X pages. Hence

    |B_o| <= |B_o intersect B_2|+|B_o intersect B_3| <= 6.

The row bound gives |B_o|>=6, so both ordinary rows are ten-rows. They
differ from the endpoint row and each other: equal blue six-sets exceed
the endpoint/ordinary allowance three or the ordinary/ordinary allowance
two. For each of four endpoint rows and binom(3,2) ordinary-row choices,
**all 64 partner subsets** are checked. All **768** configurations have
explicit known-edge book certificates. Interchanging endpoints and pairs
covers a ten-row at any matching endpoint. Thus each endpoint has at most
nine red core neighbors. No degree bound restricts the partner subsets.

In the path, a ten-row at the center would force both leaves blue to all
ten of its core vertices. Their mutual blue edge has ten core blue pages,
giving a B7. Thus the center has at most nine; leaves may have ten.

All six outside row masks are distinct in either pattern. The complete
row domain has |N|>=5 and |B|>=6. Equal rows on a red pair have at least
five red pages; on a blue pair they have six core blue pages and at least
two internal blue pages. This justifies the distinct-row counts and
sorting interchangeable roles by mask.

## Exact prefix constraints and coverage

All edges within X are known initially. Cross edges of an unassigned role
remain **unknown**, belonging to neither known color. A book consisting
of known edges cannot be removed by completing those assignments.

For internal pattern J, a prefix of assigned rows is valid precisely when:

1. Every core spine's consumed capacity is at most its residual capacity.
2. Assigned red pairs xz have |N_x intersect N_z|+c_{J,R}(x,z)<=3;
   assigned blue pairs have |B_x intersect B_z|+c_{J,B}(x,z)<=6.
3. At red cross spine xy, d_{F[N_x]}(y) plus the number of assigned
   internal red neighbors z with y in N_z is at most three.
4. At blue cross spine xy, beta_x(y) plus the number of assigned
   internal blue neighbors z with y in B_z is at most six.

An unassigned endpoint of an X pair has no known common core pages; its
internal common-page count alone is below the cap in both patterns.
Conditions 1--4 check every spine type. Rejection excludes every completion,
and any valid complete graph must follow retained prefixes.

An ordinary pair's internal common-blue-page count is four. The complete
unordered ordinary-row pair domain is **58,836** in both patterns.

**Matching.** For each ordinary pair compute the complete domain of a single
endpoint, excluding ten-rows as proved above. All four endpoints lie in
this same domain. Fewer than four distinct rows excludes completion.
Exactly **8,085** contexts have at least four; the largest domain has 62.
Check every unordered pair in these domains as one matched red pair:
**495,624** checks leave only **nine** pairs, each in a different ordinary
context. No context supports two distinct matched pairs, which a full
matching would need. The nine records appear in
[two_edges_expected.json](two_edges_expected.json). Contexts with fewer
than four rows need no pair check.

**Path.** An ordinary triple must have all three ordinary pairs in the pair
domain. Its **3,366** triangles reduce to **3,294** triples after checking
all prefix spines. Compute the complete single-center domain, excluding
ten-rows, and complete single-leaf domain at each triple. There are **123**
center occurrences and **90** leaf occurrences, with per-context maxima
four and three. All **150** center--leaf combinations within their
respective ordinary contexts violate a known-edge spine constraint.
The Python checker finds a literal book in each. Every full path would
contain such a prefix, so it is excluded.

## Reproduction and trust boundary

From the repository root, Python 3.11+, its standard library, and a
GCC/Clang-compatible C++17 compiler supporting unsigned 128-bit integers:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 book_ramsey_disjointness_family/check_two_edges.py --scratch scratch/books_two_edges
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 book_ramsey_disjointness_family/independent_two_edges.py scratch/books_two_edges/two_edges.trace
```

[search_two_edges.cpp](search_two_edges.cpp) scans masks, packs core capacity
consumption into 120 bits, and checks pairs/triples by the prefix inequalities.
The wrapper requires completion and compares compact expected diagnostics.
[independent_two_edges.py](independent_two_edges.py) imports no generator
code. It reconstructs F from cyclic Steiner triples and traverses subsets
as combinations. It indexes complete **sets of rows** by each spine/point
inequality and constructs domains by intersecting these sets, replacing
the C++ candidate scan and red-pair loop. All ordinary pairs, every matching
endpoint domain, qualifying matching pair records, and every path triple
and role domain agree **entry by entry**. It verifies all 768 certificates,
the nine surviving matching prefixes, and all 150 rejected center--leaf
combinations using literal known red/blue neighborhoods.

Trace SHA256:
`7f9e39c740ed6aedc624b1da40acd10980ebaabd76c56258d973549744ae782d`.
The 2,462,239-byte trace and executable are regenerated in scratch;
neither is published or required as imported evidence. Counts and hashes
are diagnostics; complete generation and the prefix argument supply coverage.
The trust boundary is inspected exact C++/Python code, the labeled core and
triples, and the written, unformalized completeness argument. These are
author cross-checks, not independent peer review or formal proof. No solver,
floating-point verdict, incomplete run or operational failure is used.

## Sources, attribution and limitations

The primary sources, refreshed 2026-09-30, are Lidicky--McKinley--Pfender--
Van Overberghe [Table 1](https://arxiv.org/pdf/2407.07285) and Radziszowski's
[DS1.18 Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf). The located
global interval remains 22--23. Known 21-vertex constructions are attributed
and reproduced in [README.md](README.md). No priority is asserted and the
global flag-algebra upper certificate has not been independently replayed.

six-books-1's [capacity proof](../book_ramsey_4_7_degree_reductions/capacity.md),
source commit `2e6f85b554f425b546c5f45af2d2d4228ea8b2c4`, was read and its
checker reproduced this pass. It gives degrees 7--11 and 97--121 edges in
every order-22 witness. Here it would impose 7<=|N_x|+d_J(x)<=11, core red
cross degrees 1--5, and (50 fixed red edges) row sum 47--71. Its newer
at-most-one degree-seven theorem was also read and reproduced. These
restrictions helped the initial search, but **all were removed** from the
complete published enumeration. Neither peer theorem is a premise of this
family exclusion. The earlier zero/one-edge results are premises of the
combined at-least-three statement. Three-edge internal patterns and
arbitrary 22-vertex witnesses remain unresolved here.
