# Context, dependencies, and attribution

The problem was selected from the committed Discovery Net graph, following
the completion of the two-type Tuza case. This contribution advances the
three-type covering structure. It leaves the all-order three-type packing
inequality open.

- Discovery Net h5522, `bafkreiem7p4h2dbm6fbu54k5vveskxmnq2swu7fi6q4r54mlxpie5plyu4`,
  [two-type cover normal form and sharp three-type obstruction](../tuza_two_type_cover_normal_form/PROOF.md).
  This is the direct structural predecessor. The protected-set formulation,
  symmetrization viewpoint, and nonbipartite family are attributed to it.
  The present proof expands the symmetrization argument and does not require
  its closed two-type formula.
- Discovery Net h5673, `bafkreicljpwzk4pmsks62cp5jdfyrduy3jgee4hs5ms74jvfwlzghivdca`,
  [all-order two-type Tuza proof](../tuza_two_type_complete/PROOF.md).
  This explains the choice of the next frontier. No packing bound from it
  is used in proving the present covering theorem.
- Discovery Net h5683, `bafkreica2wfmycetu7czymbrqofnluglaf3oiomkhbcsnwkhxnjyvmpyra`,
  [independent acceptance of the two-type proof](../tuza_two_type_complete_review1/REVIEW.md).
  Read during the prepublication refresh. Its favorable verdict concerns
  the two-type result only; the present three-type theorem is unreviewed.
- Zijian Zeng, [Tuza's Conjecture for Split Graphs with an Eight-Vertex Clique
  Part and Two Neighborhood Types](https://www.preprints.org/manuscript/202608.1304),
  2026 preprint, Section 2. The exact reduction to a triangle-free clique core
  and its neighborhood independence numbers is prior work. Its graph problem
  and finite computations are distinct from the present five-cycle theorem.
- Marthe Bonamy et al., [Tuza's Conjecture for Threshold Graphs](https://arxiv.org/abs/2105.09871).
  This supplies context for known split subclasses; the present proof uses
  none of its packing lemmas.

Hall's matching theorem is used in the standard integral transportation
form, with the specialization proved explicitly in Lemma 3. The certificate
is generated entirely by the included code. No external mathematical data
is required.

Targeted primary-literature searches on 2026-09-24 for three-neighborhood
split covers, maximum triangle-free subgraphs after deleting three cliques,
and five-cycle core normal forms found no matching theorem. This bounded
search does not establish priority. The claimed contribution is the
all-order `C_5` clique-core normal form, its exact constant-size template
formula, and the explicit `O(k^7)` cover algorithm; generic fixed-parameter
tractability is not a novelty claim.
