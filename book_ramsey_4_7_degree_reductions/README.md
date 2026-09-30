# Degree and neighborhood reductions for R(B4,B7)

Author: `six-books-1`, role researcher, 2026-09-30. All team members use
one signing identity; this statement identifies the actual author.

Let G be a simple graph on 22 vertices with no B4 subgraph and with no
B7 subgraph in its complement. Books are ordinary, not induced,
subgraphs. Equivalently, every edge of G has at most three common
neighbors, and every edge of its complement has at most six.

**Proved necessary conditions:**

1. Every degree lies between 7 and 12. The analytic proof gives 6..12;
   an exact finite classification plus an analytic attachment count
   excludes degree six, as described in [degree6.md](degree6.md).
2. Writing x_v = d(v)-10 and o for the number of odd degrees,
   `3 sum(x_v^2) + o <= 132`. Consequently `sum |x_v| <= 26`
   and `97 <= e(G) <= 123`.
3. With X = sum x_v, every vertex satisfies
   `X + 6 - 2*x_v - x_v^2 - 2*sum_{u in N(v)} x_u >= d(v) mod 2`.
4. If d(v)=12, its induced red neighborhood has minimum degree at
   least two and maximum degree at most three.
5. If d(v)=6, its induced blue neighborhood, viewed in G, is an
   eight-regular graph on fifteen vertices with exactly three common
   neighbors at every red edge. It has no K4. For each red neighbor
   a of v, the neighbors of a in this fifteen-vertex graph form an
   independent set.

The exclusion of degree 13 uses a forced K3 component and a cubic
ten-vertex component, then compares two counts of edges induced in
the latter by outside neighborhoods. No classification of cubic
graphs, exhaustive graph search, solver, or symmetry assumption is
used. The degree-square and parity identities are applications of
classical monochromatic-triangle counting; no novelty is claimed
for that method. The particular local reductions were not found in
the primary sources searched, but no priority claim is made.

These conditions do not settle whether a 22-vertex graph exists.
The best located primary literature still has
`22 <= R(B4,B7) <= 23`. See [proof.md](proof.md) for the analytic
reductions and [degree6.md](degree6.md) for the finite strengthening.

## Reproduction

Python 3.11 or later, standard library only; tested with CPython 3.11.2.
Run from the repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 book_ramsey_4_7_degree_reductions/check.py
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

The first command supports the analytic reductions. The second
classifies all 81,920 normalized candidates for the forced 15-vertex
edge-regular graph, retains 32, and checks explicit grid isomorphisms
for all 32. Two local generators and two cross-cycle generators
agree entry by entry; bitset and neighbor-list decisions agree for
every candidate. Its deterministic output matches
[degree6_expected.json](degree6_expected.json). All retained graphs
are K3 tensor K5, whose six-vertex attachments fail a 120-versus-72
incidence count. The finite classification supplies the exclusion of
degree six; the other statements are analytic proofs. No command
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
