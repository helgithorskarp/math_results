# Sources, concurrent work and claim boundary

The human-named problem is full Gaussian majorisation in dimension three
from [Aishwarya--Li, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
The paper was checked live on 26 September 2026. Its Gaussian product
identity, pairwise-distortion differentiation and lifted configurations
are prior mechanisms. Theorem 1.3's PC2 sufficient class is not a proof
of all the curvature tests considered here: the example U''=(1-u)^6
fails that pressure condition on part of the attained range.
This is a bounded comparison with the cited source, not a priority claim.

Reader links below use main; the full commits record the inspected sources.

- [Relative moment gaps](../gaussian_contraction_moment_gaps/PROOF.md),
  commit `a0988e688107443394da70b00827d2a52a2179ad`, and the
  [Hankel/replica source](../gaussian_majorisation_hankel_transport/PROOF.md),
  commit `6f51c67737051a61290c070c9fb960e1da83b75b`, supply the normalized
  replica and distinguished-pair identities. We rederive the constants;
  those identities and the classical variance update are credited inputs.
- Researcher 8's [polarized weight-cell certificate](../gaussian_beta_weight_certificate/PROOF.md),
  commit `a006501b012a7084676d632df4d73af1fdd92a58`, supplies the
  homogeneous coefficient formula and full-paired-rank-five positive
  product. Its finite metric-cell bounds at N=5 are not independently
  replayed or superseded quantitatively here. The current proof signs
  that row globally and additionally signs seven diagonals at all degrees.
- Researcher 5's concurrent [centroid-projection theorem](../gaussian_beta_projection/PROOF.md),
  commit `8a1e00a5328e9e340b2e511b2adf6893231e5d03`, was found in the
  mandatory prepublication refresh. It already proves the qualitative
  signs and strictness for N-j<=5, including all polarized coefficients,
  by projecting the remaining vectors relative to the base centroid.
  The overlap is expressly credited. Our affine-span/Poisson-offset
  representation also covers N-j=6 and gives an explicit distance-loss
  lower bound, compressed compact-row certificates and an exact residual
  classification. The written proof here is self-contained and does not
  assume acceptance of that concurrent theorem.
- The [global criterion](../gaussian_majorisation_global_criterion/PROOF.md),
  commit `713e542a0bd389681a3fb4ee0c0b61a4f272f104`, identifies all beta
  signs with the full question. Signing a strip does not sign the rest,
  establish every Hankel matrix as positive semidefinite, or prove all
  convex polynomial comparisons.
- Researcher 3's [rational localization](../gaussian_prior_localization/RATIONAL_INTERFACE.md),
  commit `92c30828d980c4e556a25a49035ab0e39b6541ce`, and researcher 8's
  [uniform frontier](../gaussian_majorisation_open_stability/UNIFORM_FRONTIER.md),
  commit `88bc098a0f98080f8762ddae9b11cc4e63669e95`, are the operational
  consumers. Their original K_l has radius at most 2l and variance one;
  its moment diagonal is N_l=2^16 l^8-2. Our certificate applies to every
  configuration of that compact set, without using localization or
  moment-approximation error to infer a sign. All other columns remain.
- The [rank/Abel packet](../gaussian_majorisation_rank_abel/PROOF.md),
  commit `f7c122d6a5ade217930d63da27e67f9a9e55a539`, supplies the classical
  tetrahedral flap labeling and prior six-atom boundary. The checker
  reconstructs that rational fixture from its four vertices. The new
  seven-site determinant tests only the first unpruned conditional span;
  it is not a Gaussian counterexample and does not raise the minimum
  atom count for one.
- The separate [uniform defect bound](../gaussian_uniform_defect_bound/PROOF.md),
  commit `191c7aacaef3c087e5a75ef518d011393bf485bf`, proves D<=7/50.
  Its [second-reviewer acceptance](../gaussian_uniform_defect_bound_review2/REVIEW.md),
  commit `e01a03a4ea3084d9cec2bd746d4a09d9e446bc9e`, and
  [researcher 8 audit](../gaussian_uniform_defect_review_r8/REVIEW.md),
  commit `e6d8cdc4eb9ba4ddab0d02e3ea7926772984e05f`, are separate durable
  reviews of that earlier result, not of this packet. The present proof
  uses actual paired geometry rather than only the retained Gamma order.

The exact audit imports no sibling implementation or certificate. Its
finite controls are not a substitute for the all-parameter written proof.
The new result remains an author proof awaiting independent acceptance;
publication and successful author checks do not change that status.
