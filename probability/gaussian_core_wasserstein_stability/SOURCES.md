# Sources, dependence and current frontier

## Primary problem source

Aishwarya--Li, [arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2),
Conjecture 1.1 and the dimension-three Gaussian-majorisation problem.
The paper was checked in this pass. This source remains the sole problem
source; no claim is made to resolve its unrestricted conjecture.

## Analytic and computational dependencies

- R8, [mixed-chain strictness](../gaussian_motion_chain_strictness/PROOF.md),
  graph6572. Theorem B gives the whole middle margin with the total endpoint
  loss and uniformity in the number of links. Author proof, pending review.
- R3, [polynomial hinge margin](../gaussian_polynomial_hinge_margin/PROOF.md),
  graph6558. Essential through the N-step part of the mixed-chain theorem;
  author proof, pending review.
- R8, [strictness and peak bound](../gaussian_norm_preserving_strictness/PROOF.md),
  graph6552, independently accepted6556. The peak lemma applies to arbitrary
  short endpoints. See the [review](../gaussian_norm_preserving_strictness_review2/REVIEW.md)
  for its exact scope, including the used older openness bridge.
- R8, [norm-preserving comparison](../gaussian_norm_preserving_majorisation/PROOF.md),
  graph6510, accepted6522. Underlying positive kernel for N steps.
- R8, [signed cloud-tail argument](../gaussian_majorisation_open_stability/PROOF.md),
  graph6102. The radial root/cubic/layer-cake mechanism is reused. That
  lemma's two bounded-support assumptions do not imply the present
  unbounded-source statement; Section 4 supplies the required one-sided proof.
- R3, [support-cap localization](../gaussian_support_cap_localization/PROOF.md),
  graph6520, accepted6528. Antecedent for using source cap mass and target
  support asymmetrically. Its eventual high-variance result and width
  cubature are not recomputed here.
- R2, [single-anchor cloud join](../gaussian_effective_anchored_neighborhoods/PROOF.md),
  graph6564, and [mixed-chain cloud join](../gaussian_chain_stability_certificate/PROOF.md),
  graph6588. Author proofs pending review. The elementary rational cap,
  finite motion guards, and exponent join are reused with attribution.
  The fifteen-core fold input is reused from the latter; no new geometry
  or demonstration family catalogue is claimed.

[DEPENDENCIES.json](DEPENDENCIES.json) pins the exact local source bytes and
commits. These are imported written proofs, not calls to executable oracles.
Finite controls, even with different Gram/rank algorithms, do not amount to
independent mathematical acceptance of this result or its pending imports.

## Distinction from the refreshed unrestricted frontier

The bounded graph and report refresh reached6603 before final verification.
The [accepted all-radius localization](../gaussian_all_radius_loss_localization/PROOF.md)
6576/6578 supplies loss-relative error estimates, not a positive sign. The
accepted global adverse-defect bound remains 7/50. Nothing here improves it.

R8's new [covariance-free small-loss theorem](../gaussian_covariance_free_small_loss/PROOF.md)
6596 signs each bounded-radius positive-threshold slab near zero loss. It
remains an author result at this refresh and is not a premise here. Its
interior and low-threshold obligations are not covered by invoking a chain
without exhibiting one.

R4's [guarded indecomposable frontier](../gaussian_guarded_indecomposable_frontier/PROOF.md)
6602 preserves fixed tetrahedral roots of positive mass, compact radius and
covariance bounds while variance can approach zero. The roots are fixed, so
their core-pair losses are zero: they cannot supply this certificate's
positive loss floor. Its frontier is not signed by the present theorem.
The accepted [finite-symmetry reduction](../gaussian_finite_symmetry_reduction_review2/REVIEW.md)
6600 likewise supplies no chain, width reserve, or uniform positive-variance
floor. These are retained as the unrestricted context.

R1's upper-density sign is now accepted6592; its new separated-component
small-noise window6598 still has a different threshold and weight regime.
R5's binary common-kernel theorem6594 gives component-information order,
not the density concentration needed here. R3's spatial posterior-cover
result6590 is conditional on an adverse two-body contact, not a signed
input. Completed reports from all seven other lanes were read. No matching
Wasserstein/core-background all-threshold theorem or objection to6588 was
found in the bounded refresh. This is a scoped deduplication statement,
not a historical-priority claim.
