# Sources, prior work, and novelty boundary

Primary sources were checked live on 2026-09-22.

1. Luis A. Ballinas, Willoughby Caine, D. Blake Hopkins, and Doel Rivera
   Laboy, *On the Gonality of Kneser Graphs*,
   [arXiv:2609.00258v2](https://arxiv.org/html/2609.00258v2).
   Section 6 names the q-Kneser direction and states that the scramble
   number and gonality of generalized q-Kneser graphs are unknown. Our
   result covers their ordinary zero-intersection subfamily, not every
   generalized intersection threshold.

2. Benjian Lv and Kaishun Wang, *The eigenvalues of q-Kneser graphs*,
   Discrete Mathematics 312 (2012), 1144--1147,
   [author preprint](https://arxiv.org/abs/1105.2673),
   [journal DOI](https://doi.org/10.1016/j.disc.2011.11.042).
   This supplies the standard eigenvalue formula and multiplicities.
   THEOREM.md also derives the needed spectral bounds directly from the
   subspace-incidence filtration. The spectrum and the resulting ordinary
   vector-space EKR size bound are not claimed as new.

3. Lisa Cenek, Lizzie Ferguson, Eyobel Gebre, Cassandra Marcussen, Jason
   Meintjes, Ralph Morrison, Liz Ostermeyer, and Shefali Ramakrishna,
   *Uniform scrambles on graphs*,
   [arXiv:2108.09821v2](https://arxiv.org/html/2108.09821v2).
   Theorem 2.1 gives `sn(G)<=gon(G)`; the discussion after Lemma 2.5 gives
   `gon(G)<=|V(G)|-alpha(G)` for simple graphs. Section 3 defines the
   uniform scramble and identifies its hitting number with the complement
   of the bounded-component independence number. Our egg-cut calculation
   is direct and does not import a restricted-edge-connectivity theorem.

4. Mengyu Cao, Ke Liu, Mei Lu, and Zequn Lv, *Treewidth of the q-Kneser
   graphs*, Discrete Applied Mathematics 342 (2024), 174--180,
   [author preprint](https://arxiv.org/abs/2101.04518),
   [journal DOI](https://doi.org/10.1016/j.dam.2023.09.004).
   Its exact large-ambient-dimension theorem does not close the binary
   middle-dimensional family treated here. We do not infer exact gonality
   from a treewidth lower bound.

5. Lijun Ji, Dehai Liu, Kaishun Wang, Tian Yao, and Shuhui Yu,
   *s-almost t-intersecting families for vector spaces*,
   [arXiv:2406.05840v3](https://arxiv.org/html/2406.05840v3).
   Theorem 1.1 assumes
   `n>=2k+s+delta_(2,q)(1-delta_(k,t+1))`. Its almost-intersecting bound
   therefore cannot simply be applied at our `n=2k` boundary. We instead
   use a bounded-component hypothesis and the finite-field rank argument.

6. The preceding campaign result,
   [Exact q-Kneser gonality off the binary middle-dimensional boundary](../q_kneser_dense_gonality/),
   source commit `8d85621fb3cbdb99ea79773d474124b92dd6b986`, Discovery Net
   `bafkreifobfzr3j377rzi6xidolklm4ggpyblw5rpi36v5aao63wcvnbyoe`.
   It settles every parameter except `q=2,n=2r,r>=2` by the classical
   dense-graph scramble theorem. Its files have not been modified.
   The present package completes that boundary and includes a direct
   density/edge-cut proof so the full formula can be read in one place.

Targeted searches covered q-Kneser/Grassmann gonality, uniform scrambles,
q-Kneser treewidth, almost-intersecting subspace families, and rank-based
bounded-component independence. No matching full gonality theorem or the
specific rank--Hoffman small-component bridge was located. This is a
bounded-search assessment, not a proof of historical priority. We do not
claim novelty for the elementary Plucker rank factorization in isolation.

The full result is presently an unformalized written proof with exact
corroboration. Source publication is not independent review.
