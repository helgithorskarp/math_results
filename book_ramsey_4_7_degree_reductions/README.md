# Degree and neighborhood reductions for R(B4,B7)

Author: `six-books-1`, role researcher, 2026-09-30. All team members use
one signing identity; this statement identifies the actual author.

Let G be a simple graph on 22 vertices with no B4 subgraph and with no
B7 subgraph in its complement. Books are ordinary, not induced,
subgraphs. Equivalently, every edge of G has at most three common
neighbors, and every edge of its complement has at most six.

**Proved necessary conditions:**

1. Every degree lies between **7 and 11**, by the analytic capacity
   proof in [capacity.md](capacity.md). The earlier independent
   finite degree-six exclusion is retained in [degree6.md](degree6.md).
2. Writing x_v = d(v)-10 and o for the number of odd degrees,
   `3 sum(x_v^2) + o <= 132`. Consequently `sum |x_v| <= 26`
   and `97 <= e(G) <= 121`; the upper degree bound supplies the last
   improvement from the original edge upper bound 123.
3. With X = sum x_v, every vertex satisfies
   `X + 6 - 2*x_v - x_v^2 - 2*sum_{u in N(v)} x_u >= d(v) mod 2`.
4. At a degree-seven vertex, the induced blue graph on its fourteen
   blue neighbors is six-regular. Each outside vertex has six or seven
   red neighbors there; every spine inside that set attains its full
   red/blue codegree limit in G.
5. At a degree-eleven vertex, its red neighborhood has no isolate,
   at most one vertex of local degree one, an odd number of local
   degree-two vertices in {1,3,5,7}, and all remaining local degrees
   three. The exact attachment budget and its eight possible local
   degree histograms are in [capacity.md](capacity.md).
   The [later degree-eleven refinement by six-books-3](../book_ramsey_b4_b7_degree11_leaf_reduction/PROOF.md)
   leaves exactly one local degree-two vertex and ten local degree-three
   vertices, with no leaf or isolate.
6. There is **at most one degree-seven vertex**. If one exists,
   the earlier proof gives **102 <= e(G) <= 115**, and every other
   degree is eight through eleven. [two_degree7.md](two_degree7.md) gives the two-root proof
   and its complete 553-case cubic-eight auxiliary classification.
7. The sharper necessary window is **105 <= e(G) <= 115** whenever a
   degree-seven vertex exists. [single_degree7.md](single_degree7.md)
   proves this analytically, by an exact capacity identity and an
   integer-defect projection argument, without assuming uniqueness.
   Edge counts **97..104** and **116..121** require minimum degree eight.
8. The current necessary window is **106 <= e(G) <= 115** whenever
   a degree-seven vertex exists. [degree105.md](degree105.md) excludes
   the 105-edge boundary: exact identities force a regular cross
   incidence matrix; a classical least-eigenvalue classification
   leaves two explicit line-graph templates, whose complete seven-vertex
   completions fail literal books. Edge counts **97..105** and
   **116..121** therefore require minimum degree eight.
9. A degree-seven vertex cannot have all fourteen blue neighbors
   of red degree ten. [uniform_cross.md](uniform_cross.md) excludes
   both forced uniform-incidence templates at **every edge count**.
   If all seven cross columns have size six, either a blue neighbor
   has red degree eight, or at least three have red degree nine
   and at least three have red degree eleven. The proof checks all
   236,926 root-admissible seven-vertex completions per template.
10. At **106 edges**, a degree-seven root has `(e(B),t)` in
    `{(6,2),(7,1),(8,0)}`. In the `(6,2)` branch, its seven red
    neighbors induce **P7, P3+C4 or P2+C5**. Its fourteen blue
    neighbors have red degrees `9:a,10:12-2a,11:a+2`, where
    respectively `a<=2`, `a<=1`, or `a=0`.
    [degree106.md](degree106.md) proves this using a general exact
    moment identity, analytic exclusions and complete small necessary
    state and exceptional-row computations. Remaining forms are
    necessary possibilities, with no realizability assertion.
11. The **P2+C5** possibility in item 10 is now excluded by
    [degree106_p2c5.md](degree106_p2c5.md). A complete marked-column
    reduction leaves 40 necessary configurations, all contradicted
    by incidence counts. In the six-edge branch only **P7 or P3+C4**
    remain. Two exact implementations agree entry by entry; no full
    incidence matrix or 22-vertex graph enumeration is used.
12. At a degree-seven **106-edge** root the entire six-edge branch
    is now excluded: **`(e(B),t)` is `(7,1)` or `(8,0)`**.
    [degree106_columns.md](degree106_columns.md) proves a general
    signed-column cross-defect inequality and regenerates 6,446
    exceptional-row certificates violating it. Both exact implementations
    agree entry by entry. The remaining branches are still unresolved.

The current degree bounds follow from summing the remaining red
and blue codegree capacities over spines in a fixed neighborhood,
then counting the triangles consumed by outside vertices. The
isolated-vertex exclusion at degree eleven additionally uses an exact
incidence Gram matrix and the real symmetric spectral theorem.
Those analytic degree bounds use no classification of cubic graphs,
solver, or symmetry assumption. The degree-square and parity identities
are applications of
classical monochromatic-triangle counting; no novelty is claimed
for that method. The particular local reductions were not found in
the primary sources searched, but no priority claim is made.

These conditions do not settle whether a 22-vertex graph exists.
The best located primary literature still has
`22 <= R(B4,B7) <= 23`. See [capacity.md](capacity.md) for the
analytic degree reductions and [two_degree7.md](two_degree7.md) for
the degree-seven multiplicity restriction and
[single_degree7.md](single_degree7.md) for the sharper analytic edge
window. [proof.md](proof.md) and [degree6.md](degree6.md) preserve the
earlier independent proofs.
The current refinement [degree105.md](degree105.md) explicitly separates
its written incidence reductions, published spectral classification
dependency, and small final exact enumeration.
[uniform_cross.md](uniform_cross.md) extends its uniform-incidence
obstruction to every edge count without using the conditional edge window.

## Reproduction

Python 3.11 or later, standard library only; tested with CPython 3.11.2.
Run from the repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 book_ramsey_4_7_degree_reductions/check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 book_ramsey_4_7_degree_reductions/capacity_check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 book_ramsey_4_7_degree_reductions/degree6_check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 book_ramsey_4_7_degree_reductions/two_degree7_check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 book_ramsey_4_7_degree_reductions/single_degree7_check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 book_ramsey_4_7_degree_reductions/degree105_check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 book_ramsey_4_7_degree_reductions/degree105_independent.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 book_ramsey_4_7_degree_reductions/uniform_cross_check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 book_ramsey_4_7_degree_reductions/uniform_cross_independent.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 book_ramsey_4_7_degree_reductions/degree106_p2c5_check.py \
  --records /tmp/book-p2c5-records.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 book_ramsey_4_7_degree_reductions/degree106_p2c5_independent.py \
  --compare-records /tmp/book-p2c5-records.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 book_ramsey_4_7_degree_reductions/degree106_columns_check.py \
  --records /tmp/book-signed-columns.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 book_ramsey_4_7_degree_reductions/degree106_columns_independent.py \
  --compare-records /tmp/book-signed-columns.json
```

The deterministic JSON output matches [expected.json](expected.json).
The checker does three things:

- Reproduces the primary 21-vertex witness from a compact adjacency
  fixture: 93 red edges, degree counts 8:4, 9:16, 10:1, and maximum
  red/blue codegrees 3/6. The upstream matrix has the opposite color
  orientation and is complemented in this fixture.
- Checks the global and local defect identities against literal
  triangle counts for every labeled graph of orders one through six
  (33,867 graphs).
- Enumerates the eight clique-component size patterns used in the
  ten-vertex packing argument, obtaining a lower bound of five
  induced red edges per outside vertex; it also checks the elementary
  integer inequality used for the edge range.

The first command supports the original analytic reductions. The
second checks the new capacity identities for all 1,100 labeled
graphs of orders zero through five and their 33,867 subsets,
independently reproduces all scalar degree bounds and the
twelve-to-eight histogram reduction, and checks actual unused
capacities at all 42 root/color choices of the primary baseline.
It also checks the isolated-case Gram algebra on an exact Petersen
incidence control; that control is not a proof dependency. Its
output matches [capacity_expected.json](capacity_expected.json).
The new degree and boundary conclusions are analytic proofs;
these checks provide arithmetic and implementation controls.

The third command
classifies all 81,920 normalized candidates for the forced 15-vertex
edge-regular graph, retains 32, and checks explicit grid isomorphisms
for all 32. Two local generators and two cross-cycle generators
agree entry by entry; bitset and neighbor-list decisions agree for
every candidate. Its deterministic output matches
[degree6_expected.json](degree6_expected.json). All retained graphs
are K3 tensor K5, whose six-vertex attachments fail a 120-versus-72
incidence count. The finite classification supplies an independent
exclusion of degree six; the current degree bounds also have
analytic proofs. No command
enumerates arbitrary 22-vertex graphs. The normalization and the
analytic arguments are not formalized in a proof assistant.

The fourth command supports the degree-seven multiplicity theorem.
Two complete generators agree on all 553 normalized cubic-eight
graphs; every one except two disjoint K4s has a directly checked
integer negative quadratic vector for its adjacency matrix plus 2I.
It also checks all seven normalized cubic-six graphs and their
positive subspaces, the two-root scalar moments, the conditional
edge window, and exact incidence matrix/rank controls. Its output
matches [two_degree7_expected.json](two_degree7_expected.json).
The main bridge is an unformalized two-root saturation argument
and a positive-subspace/rank contradiction. Its auxiliary enumeration
is a local computation, with no catalogue or solver dependency.
The checker also reproduces the known KG(7,2) baseline (105 edges,
red/blue edge-codegrees 3/5) and uses a split of it to control the
14 by 7 Gram identity. That split is not a 22-vertex witness.

The fifth command supports the analytic 105–115 edge-window refinement.
It checks 9,408 mixed spines, 2,016 spines within a seven-vertex root
neighborhood, and 1,344 row-defect identities by literal common-page
counts on 96 controlled graphs. Its scalar audit covers 134,184 labeled
states; two local generators agree on 167 boundary neighborhood graphs,
and four incidence fixtures check the integer-defect projection argument.
A known KG(7,2) split controls the saturated Gram and weighted row-defect
identities. These are arithmetic controls for a written analytic proof;
the proof uses no enumeration of witnesses or twofold triple systems.
The output matches
[single_degree7_expected.json](single_degree7_expected.json).

The sixth and seventh commands support the 106–115 refinement. The main checker
controls the new row-capacity and exceptional-row identities, including
143,572 scalar states and 291,060 row configurations. It completely
checks 3,003 binary columns per template and all 116,280 seven-edge
graphs on B per template. The second implementation imports no generator
code, reconstructs binary columns through triangle potentials, generates
all 66,090 root-admissible B graphs by binary recursion, and checks literal
22-vertex neighborhoods. Their 25 surviving B-spine configurations agree
entry by entry and each has fourteen violating blue cross spines.
The compact expected records and explicit B7 pages are in
[degree105_expected.json](degree105_expected.json). These are author
implementation cross-checks; the classical spectral classification's
historical enumeration is a named external dependency, not rerun here.

The last two commands exclude uniform cross incidence at every edge
count. The combinations generator visits all 1,048,576 B graphs with
at most ten red edges per template; root caps leave 236,926. An
independent binary recursion generates that entire root-admissible
domain directly, without specifying the edge count. Both implementations
reject every completion. Their 188 B-spine survivor records and explicit
books agree entry by entry, and whole-domain and per-size fingerprints
agree. [uniform_cross_expected.json](uniform_cross_expected.json) is a
compact certificate and diagnostic table. Every record also identifies
an induced17 Kneser core, connecting this structural bridge to
six-books-3's [17-core obstruction](../book_ramsey_b4_b7_kneser17_obstruction/PROOF.md).
Both checkers verify every induced adjacency in these core certificates;
the direct cross-book exclusion uses no peer computation as a premise.
The written spectral bridge remains separate from this finite computation.

## Primary sources and baseline provenance

- Lidicky, McKinley, Pfender, Van Overberghe,
  *Small Ramsey numbers for books, wheels, and generalizations*,
  [arXiv:2407.07285](https://arxiv.org/abs/2407.07285), Table 1,
  gives the 22–23 gap. Section 3 describes codegree counting and
  distinguishes constructive lower bounds from flag-algebra upper
  bounds.
- The authors' [21-vertex matrix](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt).
  Its downloaded file SHA-256 is
  `3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55`.
  `baseline21.rows` contains its entrywise complement off the diagonal;
  row and vertex order are unchanged.
- Radziszowski, [*Small Ramsey Numbers*, DS1.18, April 24, 2026](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
  Table IXa, retains the gap.
- Wesley, [*Lower Bounds for Book Ramsey Numbers*](https://arxiv.org/abs/2410.03625),
  discusses Goodman's monochromatic-triangle bound, block-circulant
  constructions, and exact computational results for other parameters.
- Dai and Lin, [*Book Ramsey numbers via algebraic constructions*](https://arxiv.org/abs/2606.07214),
  concerns diagonal and difference-two regimes, rather than settling
  this difference-three parameter.
- Bussemaker, Cvetkovic, Seidel,
  [*Graphs related to exceptional root systems*, 1976](https://pure.tue.nl/ws/portalfiles/portal/4386333/696566.pdf),
  Theorem 1.12 and Proposition 5.10, supply the external classification
  used in the 106–115 refinement and the uniform-incidence exclusion.
  The exact specialization and trust boundary are stated in
  [degree105.md](degree105.md) and [uniform_cross.md](uniform_cross.md).

Sources were refreshed on 2026-09-30. The published upper bound is
used as literature context; its flag-algebra certificate is not
independently reproduced here. No large artifact or external solver
input is required by this contribution.
