# Attribution, dependencies and novelty boundary

The following primary and shared sources were read. This packet claims an
exact counterexample reduction for (1)-(2) in PROOF.md, not invention of
simplex flaps, tournament classification, convexity, or the basis motion.
Independent historical-priority and mathematical reviews remain pending.

1. Gautam Aishwarya and Dongbin Li, *Gaussian Convolution, Internal
   Energies, and the Kneser--Poulsen Conjecture*,
   [arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2), revised
   13 September 2026, refreshed live on 26 September. Conjecture 1.1 is
   the sole human-named target. Theorem 1.4(i)(a), with two independent
   auxiliary Gaussian coordinates, is the analytic premise for pruning
   selectors that have an R5 motion. We use its density-value coupling
   and do not need the stronger smooth transport clause (i)(b).

2. Holun Cheng, Ser Peow Tan and Yidan Zheng, *On continuous expansions
   of configurations of points in Euclidean space*,
   [arXiv:1107.0140](https://arxiv.org/pdf/1107.0140), especially
   equations (5)-(7) and Theorem 2.1. The regular depth-one flaps are their
   classical construction, reversed to be contracting. The paper credits
   the independently constructed Belk--Connelly example. The present note
   does not transfer the full labelled configuration's motion obstruction
   to its ten-point selectors.

3. Shared *Simplicial-cone reflections and a nine-point obstruction*,
   [PROOF.md](../gaussian_simplicial_cone_reflections/PROOF.md), source
   `a792a1a8601d347e6e45a00bf9a3fc849d91f4b7`, graph 6042:
   `bafkreidbsexp7txezqi7745mb5d57ztkzptjrfas4gvwf6ujqakiyjzusy`.
   Its Sections 2-3 supply the explicit F_t and monotone basis coefficients.
   Our new application permits different origins for the moving flaps;
   the sign follows from the exact derivative identity (13). Its Section 4
   already credits the two-coordinate Gaussian cancellation. This earlier
   author proof is a dependency, not an independent review of this packet.

4. Shared *Full Gaussian majorisation by a common-target convex
   decomposition*, [PROOF.md](../gaussian_majorisation_common_target/PROOF.md),
   source `3ad6ed0be174d1292b250efcad734d03eed01af5`, graph 6052:
   `bafkreiefowbrpgnu2cjyyuyig4y2gzk5zdchubp3xqpcgu2rzzpy5fe25m`.
   Its elementary common-target lemma is restated and credited. Its
   balanced regular-flap comparison already covers arbitrary tetrahedral
   core mass and a specified open weight neighborhood. Neither that case
   nor a new neighborhood is claimed here. The target coincidences in (2)
   instead give an exact reduction for all weights and asymmetric shapes.
   The injective-target theorem in its Section 6 explains why further
   deterministic common-target decomposition on a selected ten-point
   source need not offer any reduction.

5. Shared *Full shallow-flap comparison at each fixed Gaussian variance*,
   [RELATIVE_TAIL.md](../gaussian_flap_depth_boundary/RELATIVE_TAIL.md), source
   `9061c33648c8a9f297181e2964220d839b7a7a2d`, builds on the
   [earlier tail proof](../gaussian_flap_depth_boundary/TAIL_BLOWUP.md), source
   `37e553af78b3b0f868fdb741c5f2ac22a6548e9f`. The latest result, inspected
   during the final refresh, signs all thresholds in an open asymmetric
   geometric class at sufficiently small depth for each fixed variance
   and positive weights. Its parameter-dependent cutoff does not settle
   depth one at arbitrary weights and variances. This is context for the
   geometric lane, not a premise of the tournament reduction.

6. Shared *Six universal beta columns from Gaussian projection*,
   [PROOF.md](../gaussian_beta_projection/PROOF.md), source
   `8a1e00a5328e9e340b2e511b2adf6893231e5d03`, and the newer
   [seven-column affine-conditioning proof](../gaussian_beta_pair_conditioning/PROOF.md),
   source `a649ce1267fac02c0e11972a988e545ffab0db79`, are used only to prune
   already positive tests in HANDOFF.md. They are not needed to prove the
   tournament reduction. The first unsigned beta test is now b_(7,0),
   not b_(6,0). They extend the earlier
   [polarized weight-cell argument](../gaussian_beta_weight_certificate/PROOF.md).

7. Shared [rational compact interface](../gaussian_prior_localization/RATIONAL_INTERFACE.md)
   at source `92c30828d980c4e556a25a49035ab0e39b6541ce`
   is context for the distinction between dense rational inputs in a
   specific family and an effective global finite-atomic reduction. We do
   not duplicate its producer or the finite-certificate lane's integration
   machinery. The [paired-rank theorem](../gaussian_majorisation_rank_abel/PROOF.md)
   supplies the earlier sufficient rank-five class; full-support selectors
   here have rank six, and the sink cases need the different explicit motion.

Bounded concept searches of primary literature and all current repository
mathematical notes found no existing tournament-selector reduction of this
flap family. That is a searched-source novelty check, not a priority claim.
The two four-vertex tournament types and their counts are elementary and
are proved afresh solely to make the search reduction exhaustive.

The committed graph was refreshed at height 6207 before publication, after
earlier ledger-read failures. Bounded teammate reports and new repository
commits were also checked. Source publication alone asserts no graph
commitment; the graph handoff retains every known relation.
