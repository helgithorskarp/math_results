# Primary sources and provenance

Status checked 2026-09-22.

1. M. Bonamy, L. Bozyk, A. Grzesik, M. Hatzel, T. Masarik, J. Novotna,
   K. Okrasa, *Tuza's Conjecture for Threshold Graphs*, DMTCS 24:1
   (2022), article 24.
   [Primary paper](https://dmtcs.episciences.org/9916/pdf).
   Its Theorem 1 proves the nested-neighborhood threshold-graph case.
   Lemma 6 records the exact complete-graph packing formula used here.

2. L. Chahua and J. Gutierrez, *On Tuza's Conjecture in Dense Graphs*,
   Discrete Applied Mathematics 377 (2025), 225--233.
   [Primary preprint](https://arxiv.org/abs/2405.11409);
   [published article](https://doi.org/10.1016/j.dam.2025.06.049).
   Theorem 5 proves Tuza's conjecture for split graphs of order `n` and
   minimum degree at least `3n/5`.  Proposition 7 records the same exact
   complete-graph packing formula.  The support-union hypothesis here is
   structurally different and permits arbitrary order, multiplicity,
   minimum degree, and neighborhood diversity.

3. Z. Zeng, *Tuza's Conjecture for Split Graphs with an Eight-Vertex
   Clique Part and Two Neighborhood Types*, version 1, posted 19 August
   2026. [Primary preprint](https://www.preprints.org/manuscript/202608.1304).
   This source is not peer reviewed.  Its Theorem 1 is restricted to two
   active neighborhood types and clique order eight.  The present theorem
   has no type bound and applies at every clique order, in its stated
   support-union region.  We do not claim to have reverified that paper's
   finite certificates.

4. F. Botler, C. G. Fernandes, J. Gutierrez, *On Tuza's conjecture for
   triangulations and graphs with small treewidth*, Discrete Mathematics
   344 (2021), 112281.
   [Primary preprint](https://arxiv.org/abs/2002.07925).
   This proves the treewidth-at-most-six case and hence the `K_8`-free
   chordal case.

Targeted searches for combinations of Tuza, split graphs, neighborhood
unions, supports, and clique packing did not locate the support-union
criterion or its exact residue-sensitive threshold.  The inspected primary
papers continue to describe unrestricted split graphs as open.  This is a
scoped status statement, not an exhaustive historical-priority claim.

The result arose from the Discovery Net Tuza neighborhood rooted at
`bafkreidlaiqmklxw4swbqbmre6xqxf66u57ttopv4xo7q4guwe43i6rcei`, while
testing consequences of the two-neighborhood uniform-gap result
`bafkreihudoilzxemequeeqi5k3bcgefhszofzmew24ddiu6pus62q74zgq`.
The proof is logically independent of that result, so a `CITES` relation,
not `DEPENDS_ON`, is appropriate.
