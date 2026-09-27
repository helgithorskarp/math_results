# Dependencies, attribution and scope

The sole named target is Aishwarya--Li,
[Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture,
arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2). Its full arbitrary
contraction conjecture in R3 is still open. The primary text was refreshed
live on 27 September 2026.

The Gaussian posterior-divergence method is credited prior work; see also
Aishwarya--Li, [The Kneser--Poulsen phenomena for entropy,
arXiv:2409.03664v3](https://arxiv.org/html/2409.03664v3), Section 3.
Procrustes alignment, double centering, finite interpolation, Gaussian
derivative moments and Remez/sublevel methods are classical. Our strip
estimate is proved directly and does not import an analytic Remez theorem.
No historical priority claim is made for these ingredients.

The following accepted team results are consumed:

1. [R1 first variation and Gram rigidity](../gaussian_contact_near_isometries/PROOF.md),
   source `3abc144c55648e210a7b91bfee213c192da7ab52`, graph6180
   `bafkreibqjjhajfhbi4fqjrdxpmlv4r4nhwjrnskomck26qycmerolzu3py`;
   [independent acceptance6196](../gaussian_contact_near_isometries_review2/REVIEW.md),
   `bafkreibwzom3raijcz4yiet7oh3urnhmaxe3b27ms44xezwa3bjhjeblw4`.
   We use its covariance-controlled Procrustes estimate and posterior
   identity. We do not claim a new first-variation method or assume the
   whole straight interpolation is contracting.

2. [Same-pair loss-proportional cubature](../gaussian_prior_localization/LOSS_CUBATURE.md),
   source `afacddeb257993b31ee118ff92e7360a7870cbc6`, graph6364
   `bafkreicuyedmct5zhkt5cxba2nkvgel3tkursxckgxcryd45ed53khps5e`;
   [independent acceptance6380](../gaussian_loss_cubature_review2/REVIEW.md),
   `bafkreia62tjvdimerupjq35kmi27cdxsknhqy4sg6bzhoiuatovvrwdluu`.
   The atom count, exact loss preservation, beta-row error and sufficient
   q schedule belong to that result. The added theorem makes its
   whole-curve transfer valid at arbitrary bounded radius with actual
   source covariance bounded below. No cubature feature is added.

3. [R8 loss-normalized hinge modulus](../gaussian_loss_normalized_hinges/PROOF.md),
   source `a68810063b8ad53dda046c68552a14e76f8d3f07`, graph6325
   `bafkreif2b3e5sw6dumihujzhpul4uce3p7v4elvfpyz77miocxodmytq24`;
   [independent acceptance6333](../gaussian_loss_normalized_hinges_review_frontier/REVIEW.md),
   `bafkreieyqbx7j34qcop5tdz46qgtub5jcvo3rz3cxzdc6d4uspcshm6uo4`.
   This supplies the earlier loss-relative certification framework.
   Its proof is not needed for the new modulus: that proof uses a convex
   six-dimensional potential at small radius, while ours controls the
   actual three-dimensional straight-path level strips using covariance.
   Its stronger exponent and absence of covariance assumptions remain
   preferable in its original domain. Neither statement subsumes the
   other uniformly through covariance collapse.

4. [Complete beta criterion and positive reconstruction](../gaussian_majorisation_global_criterion/PROOF.md),
   graph6088 `bafkreihp3see622wt3h2fxowhnp6cj4jtz5t53dxp5bmerz7aj5tfo2eeq`.
   We use the already established beta normalization and
   Bernstein--Durrmeyer expectation identity. The program independently
   checks its elementary second-moment calculation. Faster reconstruction
   schedules can replace it; none is claimed optimal here.

[INPUTS.json](INPUTS.json) pins exact source-file hashes and revisions.
These are provenance guards; the checker imports no teammate Python module.
This packet is an author proof, not an independent review of its ancestors.

## Refreshed adjacent frontiers

- The [strict screw](../gaussian_strict_screw_motion_barrier/WITNESS.json)
  is independently accepted at graph6560,
  `bafkreif4um4b6l6464cpdv6y4tprlmdyrkdd6viwlmfzrgcvk2fwkjio6i`,
  [review](../gaussian_strict_screw_motion_barrier_review2/REVIEW.md),
  source `1946f0fbe6928d99b8716ea1a009e2de77be25c7`. Its uniform 24-point
  law satisfies our guards with R=8,kappa=1/1000 at variance one. This
  demonstrates applicability to an unresolved configuration, not its sign.
- R2's [effective anchored cloud families](../gaussian_effective_anchored_neighborhoods/PROOF.md),
  graph6564 `bafkreihiczghyg3ug22qv3a7xm37arsugcuknetyojdnlprnsuxlls6tky`,
  now consume our previous polynomial margin. That is a separate
  all-threshold positive family with reference loss/mass/support reserves;
  this packet does not repeat its joining schedule.
- R8's [strict motion/chain margins](../gaussian_motion_chain_strictness/PROOF.md)
  similarly use the previous polynomial margin and provide signed
  families when a geometric chain is supplied. The present error bound
  requires no motion certificate and manufactures no such sign.
- R5's [universal cubic beta region](../gaussian_beta_cubic_region/PROOF.md),
  graph6562 `bafkreihnc2qyimyalgs7zf26xdggsaufo22o7oivqlethsdif6ttlhsuta`,
  has an [independent acceptance](../gaussian_beta_cubic_region_review2/REVIEW.md).
  It signs an unbounded region approaching the upper threshold; it does
  not supply all beta rows required by the reconstruction used here.
- R6's [parallel affine-fiber theorem](../gaussian_affine_fiber_contractions/PROOF.md)
  is a new author positive class, not a premise of our modulus. R7's
  [two-rigid-body contact transfer](../gaussian_two_body_contact_transfer/HANDOFF.md),
  graph6570 `bafkreid62eenvh4wovui3x5dujdjcpynmv7pv4kgi7d5b3hfkv66t624da`,
  needs an actual adverse joint-level volume. No such datum is inferred
  from our unsigned error estimate. R1 and R4's latest negative method
  checkpoints supply no negative Gaussian hinge.

The remaining common obligation is an actual parameter-uniform middle
margin outside the currently signed geometry, or a certified adverse sign.
All-radius relative approximation at fixed covariance is a localization
dependency toward that obligation. It is not another positive neighborhood,
an unrestricted theorem, or a new Kneser--Poulsen consequence.
