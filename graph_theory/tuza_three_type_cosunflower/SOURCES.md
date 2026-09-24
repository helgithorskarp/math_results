# Sources and scope of the advance

The target came from the committed Tuza / few-neighborhood split-graph
frontier in Discovery Net, not from a fresh literature-first problem
selection. A bounded primary-literature search on 2026-09-24 found no
matching theorem for the three-type co-sunflower condition. This does not
establish historical priority. No result for arbitrary three-type split
graphs is asserted.

- Bonamy, Bozyk, Grzesik, Hatzel, Masarik, Novotna, and Okrasa,
  *Tuza's Conjecture for Threshold Graphs*, DMTCS 24:1 (2022), article 24.
  [Primary paper](https://dmtcs.episciences.org/9916/pdf).
  Lemma 3 gives the matching factorizations and Lemma 6 gives the exact
  clique packing number used in the finite proof. Their threshold-graph
  theorem covers nested neighborhoods. Our three neighborhoods may cross.

- Zijian Zeng, *Tuza's Conjecture for Split Graphs with an Eight-Vertex
  Clique Part and Two Neighborhood Types*, preprint version 1 (2026).
  [Primary preprint](https://www.preprints.org/manuscript/202608.1304).
  The general split cover/packing perspective and the two-type order-eight
  result are prior context. Its finite catalogue is not used here.

- Chahua and Gutierrez, *On Tuza's conjecture in dense graphs*, Discrete
  Applied Mathematics 377 (2025), 225--233.
  [Primary manuscript](https://arxiv.org/abs/2405.11409).
  Their split-graph result assumes a minimum-degree condition; our arbitrary
  multiplicities need not satisfy it. Random relabeling of a clique packing
  is a prior averaging ingredient, not claimed as a new principle.

## Durable graph work

The following public source directories are in this repository.

1. **Logical dependency for at most two active types:**
   [all-order two-type theorem](../tuza_two_type_complete/README.md),
   graph h5673 `bafkreicljpwzk4pmsks62cp5jdfyrduy3jgee4hs5ms74jvfwlzghivdca`,
   source commit `26d8a45ee5932b544cb8d16e64d156bdc8cf7459`.
   [Independent review](../tuza_two_type_complete_review1/README.md),
   h5683 `bafkreica2wfmycetu7czymbrqofnluglaf3oiomkhbcsnwkhxnjyvmpyra`,
   accepts that theorem with high confidence. The present theorem has not
   received such a review. The finite bound, cap, rectangle argument, and
   some audit helpers are adapted from this prior work.

2. **Methodological predecessor:**
   [two-type uniform gap](../tuza_two_type_uniform_gap/PROOF.md),
   h5548 `bafkreihudoilzxemequeeqi5k3bcgefhszofzmew24ddiu6pus62q74zgq`.
   The new proof extends its independent-palette, residual-clique, and
   uniform-union-cut argument to three types under the co-sunflower
   condition. The pairwise-union estimate, exact quartic gap, and finite
   three-type closure are the proposed new steps. The old stronger
   quantitative constant for two types is not superseded.

3. **Frontier context, not a proof dependency:**
   [three-type C5 cover normal form](../tuza_three_type_c5_core/README.md),
   h5685 `bafkreibn2ff62v4czjnzqlt3huaauspidswmtarid6up6m74rvy4npiium`.
   It covers unrestricted three-type neighborhoods but only the cover side.
   The current proof uses inexpensive bipartite covers instead of this
   exact cover oracle. Arbitrary three-type Tuza remains a packing problem.

4. **Complementary result:**
   [support-union theorem](../tuza_split_support_union/README.md),
   h5578 `bafkreib2rmuyiy7kf3bpefr2ajow4hwrpyzlhuowggduahdivmxfmb2lz4`.
   It allows arbitrarily many neighborhood types with a bounded support
   union. It is neither used nor subsumed here.

The overarching graph problem is
`bafkreidlaiqmklxw4swbqbmre6xqxf66u57ttopv4xo7q4guwe43i6rcei`.
