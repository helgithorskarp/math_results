# Review sources, attribution, and the independent control

This packet independently reviews R3's effective refinement of a shared
theorem. It makes no independent-discovery or historical-priority claim.
The supplementary projection argument is separately derived author
mathematics with a much coarser cutoff. It does not inherit independent
acceptance from the review of R3's different proof.

## Problem and primary literature

Gautam Aishwarya and Dongbin Li,
[Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture](https://arxiv.org/html/2609.07041v2),
arXiv:2609.07041v2, is the named problem source. Conjecture 1.1 asks for
all convex internal energies under arbitrary contractions; Theorems 1.2
and 1.3 give the established low-dimensional and partial pressure-class
results. The source was refreshed live on 27 September 2026. Gaussian
differentiation and classical polarization are credited prior methods.
No comprehensive historical priority assessment is made.

## Reviewed target

R3's [effective mean-loss proof](../gaussian_effective_mean_loss/PROOF.md),
source `f171c499bc0ed272d1b6fd5f78d57968d1578b62`, with its
[executable handoff](../gaussian_effective_mean_loss/HANDOFF.md), supplies
explicit all-radius constants and the sharper dyadic cutoff `2^-360` in
the small-radius normalization. Its interval-slice argument, source and
exact arithmetic were read and audited in full. Ten public source files
are pinned in TARGET_INPUTS.json. The primary publication from this lane
is a review of that result, not a separate claim of the same effective
frontier. PROJECTION_CONTROL.md supplies a different, coarser analytic
check of the rare-move mechanism; the projection proof was derived before
the source refresh disclosed the target.

The target's original graph contribution is6426,
`bafkreieyattiaogc4s7iosnunxfq3yi6sy2enhq23ftgtoua7fz22zb6ni`.
R8's concurrent [quantitative midpoint proof](../gaussian_mean_loss_margin/EFFECTIVE.md),
source `9117b9b64127df8ee18337d9205e4aa7a9b70960`, graph6428,
`bafkreicnf26bdsf25pg7bceowk7lep36lzqgz5d4bdlpyncaqd7pkh34ni`,
is acknowledged as a separate alternative for the same effective family.
It is not independently accepted in this review. That commit updates the
heading of R8's original PROOF.md, invalidating a dependency hash in the
target author checker on later main. REVIEW.md records the exact replay
version; the mathematical dependency body and reviewed theorem are unchanged.

## Analytic dependencies

1. R8's [uniform mean-loss margin](../gaussian_mean_loss_margin/PROOF.md),
   graph6414, artifact
   `bafkreie5iago7b2rtbm5oyabb3fshfabujmwms37a3vsojzo7efsgfybey`,
   source `888c64db59feccd280575061612804854b0f658c`, already proves
   the qualitative uniform full-rank small-mean-loss theorem. Both effective
   proofs use its bulk/rare decomposition, conditional alignment with an
   O(alpha^2) error, retained pair-loss bookkeeping and rare-fold
   calibration. Neither claims those as independent discoveries.
   Its [acceptance](../gaussian_mean_loss_margin_review2/REVIEW.md),
   source `0babf1cceeae17179cc6975dc1d588ebb86b7e95`, graph6422,
   `bafkreihagjha6hrnzivyd3iutnmtilrvx5dclurfrjcxf4q4ep5k56vpua`,
   was read in full. It accepts the qualitative result, not either
   effective refinement.
2. The accepted [near-isometry proof](../gaussian_contact_near_isometries/PROOF.md),
   graph6180, artifact
   `bafkreibqjjhajfhbi4fqjrdxpmlv4r4nhwjrnskomck26qycmerolzu3py`,
   source `3abc144c55648e210a7b91bfee213c192da7ab52`, supplies the
   Procrustes inequality, posterior-divergence identity, critical-level
   passage and Gaussian Hessian bound. Its
   [acceptance](../gaussian_contact_near_isometries_review2/REVIEW.md)
   is graph6196, artifact
   `bafkreibwzom3raijcz4yiet7oh3urnhmaxe3b27ms44xezwa3bjhjeblw4`,
   source `0610cbe2b1163ee2f825b977e9044d3284df279c`.

The interval proof makes the posterior mean along a move positive and
integrates the score between equal-density endpoints. The projection
proof instead repairs the background into the bisector halfspace and
quantitatively polarizes the actual source set. These are different
rare-point mechanisms sharing the credited rigidity and bulk estimates.
Neither assumes a compactness modulus, a unique mode, convex superlevels,
or a previously unknown contact sign.

## Relation to the shared finite frontier

The [quartic loss guard](../gaussian_loss_moment_middle/PROOF.md),
mathematical source `2207d8b5de0859222895ecb3e0524e64635446fe`,
graph6408, remains a complementary sufficient test. Its
[review](../gaussian_loss_moment_middle_review_frontier/REVIEW.md),
source `dc3c58a818f288df5cb024a1b0b8518073018f60`, graph6420,
accepts that original scope. Small mean loss does not force its Q/d guard;
the target's unbalanced rare-motion family proves this directly.

The accepted [paired cubature](../gaussian_prior_localization/CUBATURE_FRONTIER.md)
and [loss-preserving refinement](../gaussian_prior_localization/LOSS_CUBATURE.md)
are downstream interfaces. The latter is graph6364, accepted6380;
source `afacddeb257993b31ee118ff92e7360a7870cbc6`, corrected review
source `99d165ea308026e7c3241f90ac2fe984cc16fec9` at6382.
Only marginal moments through degree two are needed for the new guard,
so the existing 19-pair existence bound applies without extra mixed moments.

R8's [Jackson reconstruction](../gaussian_jackson_certification/PROOF.md),
graph6398, mathematical source
`052dc9a502f6e96f7899050d5a017c28f07ff4e2`, and R4's accepted
[coordinate/endpoint frontier](../gaussian_indecomposable_contractions/COORDINATE_HANDOFF.md),
graph6378, accepted6390, source
`2bd8d341950153a750c20f9ad4638991ce3cbdb2`, retain their own hypotheses.
A certified low-threshold overlap, control of covariance collapse, and
signs outside the small-loss neighborhood are still needed. The present
review does not certify a complete or practical global cover.

R6's [eight-site geometry](../gaussian_open_eight_site_obstruction/PROOF.md)
provides the target's exact positive-control configuration. We reconstruct
its distance table; its no-R5-motion obstruction is contextual and not
used to infer the Gaussian sign. R4's accepted
[parity alignment](../gaussian_parity_alignment/PROOF.md) already covers
balanced orbit weights at all variances. R2's
[polynomial comparison](../gaussian_logarithmic_noise_certificate/PROOF.md)
and R6's [normal-bundle theorem](../gaussian_angular_ray_contractions/NORMAL_BUNDLES.md)
are separate results, not dependencies of the reviewed analytic sign.
No cap, flap or symmetry variant is developed here.

## Evidence and trust

`independent_check.py` imports no target code. It pins ten target files,
independently reconstructs the seven exact budgets, checks27 interval
primitives and all28 template pairs, checks12 strongly unbalanced parameter
controls and three rare folds with unfavorable halfspace mass, and rejects
five adverse cases. The target author checker also passed normal and
optimized Python; this replay is not the independent part of the review.

`projection_controls.py` checks175 pair identities,51 projection controls,
204 reflection identities, eleven universal polynomial induction bounds,
and all exponent budgets, with seven adverse cases. Non-axial rational
normals exercise the geometry without assuming a coordinate reflection.
The rare-fold parameters are credited to R8. Both checkers produce exact
canonical records in normal and optimized Python.

The analytic continuum claims remain written mathematics, not a
proof-assistant certificate. No Gaussian quadrature, solver, large data or
heavy certificate replay is used. The supplementary cutoff is extremely
conservative; it is not a proposed practical alternative to R3's schedule.
Historical priority and unrestricted majorisation remain unestablished.
