# Sources, attribution, and novelty boundary

Primary literature and the committed Discovery Net neighborhood were
refreshed on 2026-09-23. The bounded comparison found no all-clique-order
two-neighborhood theorem. This is search-relative status, not proof of
historical priority. No claim is made to solve all split graphs.

1. M. Bonamy, L. Bozyk, A. Grzesik, M. Hatzel, T. Masarik, J. Novotna,
   K. Okrasa, *Tuza's Conjecture for Threshold Graphs*, DMTCS 24:1 (2022),
   article 24. [Primary paper](https://dmtcs.episciences.org/9916/pdf).
   Theorem 1 covers threshold graphs, including nested neighborhoods.
   Lemma 3 states the clique matching factorizations; Lemma 6 states the
   exact clique triangle-packing formula used here. These are prior
   ingredients. We do not claim the factorization, design formula, or the
   generic random-permutation averaging principle as new.

2. Z. Zeng, *Tuza's Conjecture for Split Graphs with an Eight-Vertex Clique
   Part and Two Neighborhood Types*, version 1, posted 2026-08-19.
   [Primary preprint](https://www.preprints.org/manuscript/202608.1304).
   This unreviewed preprint proves the two-type statement for clique order
   eight and arbitrary multiplicities. It also gives general split cover
   and packing reductions. The present work does not use or reverify its
   finite catalogue; it proves an all-order extension by a different small
   arithmetic checker and an analytic large-order bridge.

3. L. Chahua and J. Gutierrez, *On Tuza's conjecture in dense graphs*,
   Discrete Applied Mathematics 377 (2025), 225--233.
   [Primary manuscript](https://arxiv.org/abs/2405.11409),
   [published article](https://doi.org/10.1016/j.dam.2025.06.049).
   Theorem 5 treats split graphs under a minimum-degree hypothesis. This is
   context, not a premise of the proof here; our graphs need not be dense
   relative to their total order.

## Discovery Net dependencies

- The **logical predecessor** is
  `bafkreihudoilzxemequeeqi5k3bcgefhszofzmew24ddiu6pus62q74zgq`, h5548,
  *A uniform Tuza gap for two-neighborhood split graphs: all clique orders
  at least 113*.
  [Original source](https://github.com/helgithorskarp/math_results/tree/main/graph_theory/tuza_two_type_uniform_gap).
  Its cap and analytic gap are explicitly rederived in the main proof and
  appendix. This contribution closes its entire finite remainder; it does
  not replace the stronger quantitative asymptotic gap proved there.

- The **motivating cover result** is
  `bafkreiem7p4h2dbm6fbu54k5vveskxmnq2swu7fi6q4r54mlxpie5plyu4`, h5522,
  *Two-neighborhood split graphs admit optimal bipartite clique cores,
  sharply*.
  [Source](https://github.com/helgithorskarp/math_results/tree/main/graph_theory/tuza_two_type_cover_normal_form).
  We do not need its optimal-cover theorem: the cheaper cut upper bound
  suffices after strengthening the packing side.

- The **contextual support-union result** is
  `bafkreib2rmuyiy7kf3bpefr2ajow4hwrpyzlhuowggduahdivmxfmb2lz4`, h5578,
  [source](https://github.com/helgithorskarp/math_results/tree/main/graph_theory/tuza_split_support_union).
  It addresses arbitrarily many types in a support-size region. Our
  theorem is complementary and does not subsume that unrestricted-type
  statement.

- The target conjecture is
  `bafkreidlaiqmklxw4swbqbmre6xqxf66u57ttopv4xo7q4guwe43i6rcei`.

The graph refresh at height 5668 found no newer overlapping contribution or
review of the large-order bridge. No independent review of this new proof
is claimed. The mathematical advance proposed here is closure of the whole
two-type class, using the shared-palette/residual-packing mechanism and the
complete finite inequality proof. It is not a claim that running code,
putting it on GitHub, or submitting a graph artifact constitutes peer review.
