# Sources, dependency status and scope

Primary problem: Aishwarya--Li,
[arXiv:2609.07041v2](https://arxiv.org/abs/2609.07041v2).
The target remains full Gaussian-convolution majorisation under a
1-Lipschitz map for bounded measures in dimension three. The paper's
full comparison is established through dimension two; its higher
dimensional results do not settle this target.

The present contribution is an author proof, not independently accepted
or formalized. It makes no historical priority claim. The elementary
Gaussian tail calculations are written out rather than attributed as
new identities.

## Mathematical dependencies

- R3's [effective mean-loss theorem](../gaussian_effective_mean_loss/PROOF.md),
  graph6426, bafkreieyattiaogc4s7iosnunxfq3yi6sy2enhq23ftgtoua7fz22zb6ni,
  source f171c499bc0ed272d1b6fd5f78d57968d1578b62.
  The interval-component comparison, rare-label loss retention, seven-budget
  assembly and fixed upper-window cutoff are used here.
  [Independent acceptance](../gaussian_effective_mean_loss_review_r4/REVIEW.md)
  at graph6432, bafkreififbypnz6a7duxi3g75relsg4g2oexl22hbgeh4xk6wkebaxqxvq,
  review source 6ebac9c96dcf201db531c08abe180644958191b9.
  The new threshold-dependent replacements in this packet are not covered
  by that acceptance.
- R1's [near-isometry proof](../gaussian_contact_near_isometries/PROOF.md),
  graph6180, supplies Procrustes rigidity and the actual-top-set derivative
  with regular-value approximation.
  [Accepted review](../gaussian_contact_near_isometries_review2/REVIEW.md)
  at graph6196. The present proof does not rebrand this rigidity as new.
- R8's [mean-loss margin](../gaussian_mean_loss_margin/PROOF.md),
  graph6414, accepted at graph6422 by
  [this review](../gaussian_mean_loss_margin_review2/REVIEW.md).
  The core/rare conditional alignment and its alpha-squared error are
  credited dependencies, already inherited by the effective theorem.
- R8's [loss modulus](../gaussian_loss_normalized_hinges/PROOF.md),
  graph6325, bafkreif2b3e5sw6dumihujzhpul4uce3p7v4elvfpyz77miocxodmytq24,
  source a68810063b8ad53dda046c68552a14e76f8d3f07.
  Its whole-curve loss factor and square-root threshold modulus are used
  to obtain the explicit relative defect estimate.
  [Accepted review](../gaussian_loss_normalized_hinges_review_frontier/REVIEW.md)
  at graph6333, bafkreieyqbx7j34qcop5tdz46qgtub5jcvo3rz3cxzdc6d4uspcshm6uo4,
  review source 7ff2bc792281a317829319b8cf25e5af42e31154.
- The [paired cubature frontier](../gaussian_prior_localization/CUBATURE_FRONTIER.md),
  graph6212, accepted at6218, supplies the 19-pair degree-two preservation
  interface. No new cubature theorem, rationality guarantee or uniform
  parameter rule is claimed.

Versioned byte pins in INPUTS.json identify the exact written inputs.
The independent-acceptance file is pinned at its publication commit; the
other inputs are pinned at the effective theorem's source commit.
This avoids mistaking a later header edit for a mathematical revision.

## Concurrent work and nondependencies

R8's [midpoint-polarization continuation](../gaussian_mean_loss_margin/EFFECTIVE.md)
at graph6428 was independently accepted at6434. It proves the same
fixed-window family by another argument; it is credited context, not
a premise of the new tail estimate. R2 independently derived and parked
an overlapping fixed-window proof.

R1's [regularized-contact margin](../gaussian_regularized_contact_margin/PROOF.md)
at graph6438 transfers the accepted bounded theorem to an actual unbounded
Gaussian-regularized contact regime. It is a different transfer with an
explicit smoothing restriction, not a premise or a duplicate of the
present bounded-law moving threshold theorem.

R8's [covariance-collapse guard](../gaussian_covariance_collapse_guard/PROOF.md)
is author work at source b3ecb0d0d611bd4bee0c83f26c648716176c9626, available during the final refresh.
It signs a fixed middle window near either marginal's rank-two boundary.
It is complementary and does not establish the missing joint limit
needed to remove our positive covariance floor.

R2's logarithmic degree/noise polynomial theorem is now independently
accepted in its finite-degree scope. R5's averaged replica rank-gap
improvement remains short of its first Hankel target. R6's normal-bundle
class has independent acceptance. None provides the missing unrestricted
sign used implicitly here; none is a premise of our theorem.

The finite template in HANDOFF.md is the earlier R6
[eight-site geometry](../gaussian_open_eight_site_obstruction/PROOF.md);
its prior-uniform radius, covariance and mean-loss estimates are in the
accepted effective theorem. Balanced within-orbit priors already have
R4's stronger all-variance parity theorem. These examples calibrate the
consumer and do not establish a new positive geometric class.

## Trust boundary

Gaussian score integration, analytic slicing, kernel differentiation,
Fubini and regular-value approximation are written mathematics. The new
checker controls exact constants and algebra without importing a prior
checker. It does not supply an independent review or a proof-assistant
kernel. No floating-point signs, hidden corpus, large computation,
or solver result enters the proof.

The full conjecture and the accepted global defect cap7/50 are unchanged.
The new estimates depend on radius and a positive covariance floor.
A flat upper bound as d tends to zero is not a zero-defect theorem at a
fixed positive d.
