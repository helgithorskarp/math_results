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

The current degree bounds follow from summing the remaining red
and blue codegree capacities over spines in a fixed neighborhood,
then counting the triangles consumed by outside vertices. The
isolated-vertex exclusion at degree eleven additionally uses an exact
incidence Gram matrix and the real symmetric spectral theorem.
No classification of cubic graphs, solver, or symmetry assumption
is used. The degree-square and parity identities are applications of
classical monochromatic-triangle counting; no novelty is claimed
for that method. The particular local reductions were not found in
the primary sources searched, but no priority claim is made.

These conditions do not settle whether a 22-vertex graph exists.
The best located primary literature still has
`22 <= R(B4,B7) <= 23`. See [capacity.md](capacity.md) for the
strongest analytic reductions. [proof.md](proof.md) and
[degree6.md](degree6.md) preserve the earlier independent proofs.

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
exclusion of degree six; the strongest current statements are
analytic proofs. No command
enumerates arbitrary 22-vertex graphs. The normalization and the
analytic arguments are not formalized in a proof assistant.

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

Sources were refreshed on 2026-09-30. The published upper bound is
used as literature context; its flag-algebra certificate is not
independently reproduced here. No large artifact or external solver
input is required by this contribution.
