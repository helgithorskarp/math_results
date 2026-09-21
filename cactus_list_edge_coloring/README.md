# Exact list chromatic index of cactus multigraphs

This note proves the List Edge-Coloring Conjecture for every finite loopless
cactus multigraph.  The proof is greedy and parameter-uniform; its structural
core is an exact formula for the degeneracy of the line graph.

## Conventions

A **cactus multigraph** is a finite loopless multigraph every block of which
is either a single edge or a cycle.  A cycle of length two consists of two
parallel edges.  Equivalently, distinct cycles are edge-disjoint and any two
cycles have at most one vertex in common.  The line graph `L(G)` is simple:
its vertices are the edges of `G`, and two are adjacent when they share at
least one endpoint.

Write `Delta=Delta(G)`.  The degeneracy `d(H)` of a finite graph `H` is the
maximum, over its nonempty induced subgraphs, of the minimum degree.

## Exact line-graph degeneracy

**Theorem 1.** Let `G` be a cactus multigraph with at least one edge.

1. If `Delta>=3`, then

   \[
   d(L(G))=\Delta-1.                                      \tag{1}
   \]

2. If `Delta=2`, then `d(L(G))=2` when `G` has a cycle component
   of length at least three, and `d(L(G))=1` otherwise.
3. If `Delta=1`, then `d(L(G))=0`.

### Proof for `Delta>=3`

The `Delta` edges incident with a maximum-degree vertex form a clique in
`L(G)`, so `d(L(G))>=Delta-1`.

For the reverse inequality, take any nonempty set `F` of edges and put
`H=(V(G),F)`, omitting isolated vertices.  The graph induced by `F` in
`L(G)` is exactly `L(H)`, and `H` is again a cactus multigraph.  We exhibit a
vertex of `L(H)` of degree at most `Delta-1`.

If `H` has a vertex `u` of degree one, its incident edge `uv` is adjacent in
`L(H)` to exactly `deg_H(v)-1<=Delta-1` other edges.

Suppose instead that every vertex of a chosen component of `H` has degree at
least two.  If that component is one cycle, an edge has line-graph degree
two when the cycle has length at least three, and degree one when it is a
2-cycle.  Both bounds are at most `Delta-1`.

Otherwise take a leaf block of its block-cut tree.  It cannot be a bridge,
because that would give a degree-one vertex, so it is a cycle with at most
one cut vertex.

- If its length is at least three, choose an edge whose two endpoints are
  not the cut vertex.  Both endpoints have degree two in `H`, so this edge
  has line-graph degree two.
- If it is a 2-cycle, let its non-cut vertex be `x`, its possible cut vertex
  be `w`, and choose either parallel edge.  The other parallel edge is
  counted at both endpoints but is only one neighbor in the simple line
  graph.  The chosen edge therefore has line-graph degree
  `deg_H(w)-1<=Delta-1`.

Thus every nonempty induced subgraph of `L(G)` has minimum degree at most
`Delta-1`, proving the upper bound in (1).

When `Delta<=2`, every nontrivial component of `G` is a path or a cycle
(with 2-cycles allowed), so the remaining assertions follow directly from
the line graphs of paths and cycles.

## List edge-colouring classification

**Theorem 2.** Every finite loopless cactus multigraph satisfies

\[
\boxed{\chi'_\ell(G)=\chi'(G).}                            \tag{2}
\]

More explicitly, for a nonempty `G`,

\[
\chi'_\ell(G)=\chi'(G)=
\begin{cases}
1,&\Delta=1,\\
3,&\Delta=2\text{ and an odd cycle is present},\\
2,&\Delta=2\text{ and no odd cycle is present},\\
\Delta,&\Delta\ge3.
\end{cases}                                                \tag{3}
\]

### Proof

A `d`-degenerate graph is `(d+1)`-choosable: recursively delete a vertex of
degree at most `d`, colour the remaining graph, and restore the deleted
vertex, when at most `d` colours are forbidden.  Edge lists on `G` are
vertex lists on `L(G)`.  Theorem 1 therefore gives
`chi'_ell(G)<=Delta` when `Delta>=3`, while the incident edges at a
maximum-degree vertex give `chi'(G)>=Delta`.  Equality follows.

For `Delta=1` the assertion is immediate.  For `Delta=2`, the components are
paths and cycles.  Paths are 2-edge-choosable.  An even cycle is also
2-edge-choosable: if all two-element lists agree, alternate their two
colours; otherwise start with a colour on one edge that is absent from a
neighboring edge's list and greedily colour around the cycle toward that
neighbor.  The final edge then automatically avoids the starting colour.
An odd cycle with identical two-element lists is not 2-edge-colourable, but
the degeneracy bound gives list chromatic index at most three.  This proves
(3), including disconnected graphs by colouring components separately.

The proof yields a list-independent elimination ordering and hence a direct
greedy colouring algorithm.  No enumeration, polynomial identity, or
solver result is used in the theorem.

## Reproduction

Run with CPython 3.11 or later and no third-party packages:

```sh
python3 verify.py
```

Compare the output with [`EXPECTED_OUTPUT.json`](EXPECTED_OUTPUT.json).
The checker:

- enumerates every labelled simple graph through six vertices;
- enumerates every loopless multigraph through five vertices in which each
  pair has multiplicity zero, one, or two;
- recognizes cactus multigraphs from their biconnected edge blocks;
- computes line-graph degeneracy directly by minimum-degree peeling and
  checks Theorem 1 on every recognized instance;
- exhausts every assignment of two-element subsets of a four-colour palette
  to cycles of lengths two, four, and six and checks the constructive cycle
  algorithm; and
- rejects both a triple-edge block and `K4` as non-cacti.

This finite audit checks definitions, parallel-edge conventions, and boundary
cases.  The universal result rests on the block-cut proof above.

## Literature and scope

The general List Edge-Coloring Conjecture remains open, even for complete
graphs of arbitrary even order.  Galvin's theorem covers bipartite
multigraphs, whereas the cactus class here includes arbitrary odd cycles and
trees of cyclic blocks.  A targeted search on 2026-09-21 did not locate this
exact cactus/line-degeneracy statement in the searched primary literature or
bibliographic indexes.  The argument is elementary, and no historical
priority claim is made.

This theorem does not address graphs whose blocks contain theta subgraphs or
other edges lying in multiple cycles.  Source details and the search boundary
are recorded in [`SOURCES.md`](SOURCES.md).
