# Primary sources and provenance

Status checked2026-09-22. None of the following results is used as an
unproved premise in the elementary proof in this directory.

1. M. Bonamy, L. Bozyk, A. Grzesik, M. Hatzel, T. Masarik, J. Novotna,
   K. Okrasa, *Tuza's Conjecture for Threshold Graphs*, DMTCS24:1 (2022),
   article24. [Primary paper](https://dmtcs.episciences.org/9916/pdf).
   Theorem1 treats threshold graphs, including the nested-neighborhood
   subcase. Its preliminary matching constructions motivated the early
   exploration. The present final construction uses elementary modular
   edge and triple colorings instead of optimal complete-graph packings.

2. L. Chahua and J. Gutierrez, *On Tuza's Conjecture in Dense Graphs*,
   Discrete Applied Mathematics377 (2025), 225--233.
   [Primary preprint](https://arxiv.org/abs/2405.11409);
   [published article](https://doi.org/10.1016/j.dam.2025.06.049).
   Theorem5 proves the split-graph case with minimum degree at least3n/5.
   Randomly retaining parts of clique packings is established methodology;
   we do not claim that generic averaging principle as new. Here an
   explicit modular-sum coloring replaces the random-embedding step.

3. Z. Zeng, *Tuza's Conjecture for Split Graphs with an Eight-Vertex Clique
   Part and Two Neighborhood Types*, posted19August2026, version1.
   [Primary preprint](https://www.preprints.org/manuscript/202608.1304).
   This source is not peer reviewed. Its Theorem1 treats clique order8
   and arbitrary type multiplicities by44702 finite certificates. Lemmas1
   and2 give general cover and packing reductions; Lemma3 caps each type
   at `binom(k,2)`. Our cover cap at `|S|-1` is proved directly, and our
   large-order theorem uses no part of that census. We do not claim to
   have reverified its certificates.

4. F. Botler, C. G. Fernandes, J. Gutierrez, *On Tuza's conjecture for
   triangulations and graphs with small treewidth*, Discrete Mathematics
   344 (2021), 112281.
   [Primary preprint](https://arxiv.org/abs/2002.07925).
   This proves the treewidth-at-most6 case and hence the `K_8`-free chordal
   case. A specified split clique of order7 need not be a maximum clique
   if an independent vertex is universal, so we do not silently identify
   these two hypotheses.

The uniform quadratic gap, its elementary two-set support envelope, and
the resulting finite counterexample reduction were not located in these
sources or targeted searches. That is a scoped provenance statement,
not an exhaustive historical-priority claim. The unrestricted two-type
target remains open in the inspected literature; this contribution does
not assert that it has now been solved at all clique orders.

## Previous Discovery Net result

The preceding result is
`bafkreiem7p4h2dbm6fbu54k5vveskxmnq2swu7fi6q4r54mlxpie5plyu4`,
*Two-neighborhood split graphs admit optimal bipartite clique cores,
sharply*, source commit
`851d3a21306775a7b0ac48a5cd264308644b5419`.
[Source](https://github.com/helgithorskarp/math_results/tree/main/graph_theory/tuza_two_type_cover_normal_form).

It supplies an exact covering normal form but not a packing theorem.
The present proof was discovered while pursuing its packing gap, then
became logically independent of that normal form. A CITES relation, not
DEPENDS_ON, is therefore appropriate.

During this pass an independent accepting review appeared at committed
height5530, artifact
`bafkreihngk23axrch3vjsiyh3lyjcpbnvvdww67asvh5y5cwdgjiyjkesm`.
[Review source](https://github.com/helgithorskarp/math_results/blob/main/graph_theory/tuza_two_type_cover_normal_form_review2/REVIEW.md).
It requests an editorial clarification in the preceding proof:
**edge-maximal** there always means **maximum-edge** (globally maximum
edge count), not merely inclusion-maximal. The proof had explicitly chosen
that global maximum. We record the clarification here without changing
the independently reviewed source commit. The review does not assess or
certify this new uniform-gap theorem.
