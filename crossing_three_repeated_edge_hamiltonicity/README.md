# Repeated crossed edges at crossing number three

This directory records a proof-level reduction for the open Hamiltonicity
frontier at crossing number three.

## Main result

Let `H` be a finite simple projective-planar graph and let `x,y` be distinct
nonadjacent vertices.  If

```text
G = H + xy
```

is 4-connected, then `H` has a Hamiltonian path from `x` to `y`.
Consequently, the added edge `xy` lies on a Hamiltonian cycle of `G`.

The crossing-number consequence is immediate.  If a 4-connected graph has a
plane drawing with at most three crossings and one edge occurs in at least two
of the crossing pairs, then the graph is Hamiltonian.  Indeed, deleting that
edge leaves a drawing with at most one crossing, hence a projective-planar
graph, and the theorem applies.  Thus every hypothetical non-Hamiltonian
4-connected graph of crossing number three must have six distinct crossed
edges in every optimal three-crossing drawing.

The proof is in [PROOF.md](PROOF.md).  It is a structural deduction from the
projective-plane Tutte-path theorem of Kawarabayashi and Ozeki, with a planar
Tutte path used to absorb the exceptional three-attachment flap.  There is no
enumeration or solver trust boundary.

## Status and scope

Ozeki and Zamfirescu proved Hamiltonicity through crossing number two and
listed crossing number three as open.  A current-status search performed on
2026-09-21 found no later primary source settling that question or stating the
relative edge-addition theorem above.  This is a search-relative status
statement, not a claim of priority.

The result does **not** settle the full crossing-number-three problem.  It
removes exactly the crossing patterns in which a crossed edge is repeated.
The residual case has three pairwise edge-disjoint crossing pairs.

## Primary sources

1. K. Kawarabayashi and K. Ozeki, *4-connected projective-planar graphs are
   Hamiltonian-connected*, Proc. SODA 2013, 378--395,
   [DOI 10.1137/1.9781611973105.28](https://doi.org/10.1137/1.9781611973105.28).
   The freely available manuscript contains the technical projective-plane
   Tutte-path theorem (Theorem 2), its exceptional-flap definition, and the
   planar flap-filling theorem (Theorem 5):
   <https://tgt.ynu.ac.jp/ozeki/2012KO.pdf>.
2. K. Ozeki and C. T. Zamfirescu, *Every 4-connected graph with crossing
   number 2 is Hamiltonian*, SIAM J. Discrete Math. 32 (2018), 2783--2794,
   [DOI 10.1137/17M1138443](https://doi.org/10.1137/17M1138443).  Theorem 1
   proves the crossing-number-two case; Table 1 records the crossing-number-
   three case as open.  Manuscript: <https://tgt.ynu.ac.jp/ozeki/2017OZ.pdf>.
3. D. P. Sanders, *On paths in planar graphs*, J. Graph Theory 24 (1997),
   341--345,
   [DOI 10.1002/(SICI)1097-0118(199704)24:4<341::AID-JGT6>3.0.CO;2-O](https://doi.org/10.1002/(SICI)1097-0118(199704)24:4%3C341::AID-JGT6%3E3.0.CO;2-O).

## Reproduction

No software is required.  The independently checkable object is the written
proof and its explicit case audit:

```bash
sha256sum PROOF.md
```

The expected digest is recorded in `SHA256SUMS`.
