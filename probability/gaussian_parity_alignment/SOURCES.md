# Sources and scope of the parity alignment argument

Primary sources checked on 27 September 2026:

- G. Aishwarya and D. Li, [Gaussian Convolution, Internal Energies, and
  the Kneser--Poulsen Conjecture](https://arxiv.org/html/2609.07041v2).
  Conjecture 1.1 is the sole problem source. Theorem 1.4 and its
  two-extra-coordinate consequence support the credited radial input.
  The exponential-weight union extraction is already in Theorem 5.1
  and the variable-radius discussion; we do not claim that general
  transfer method as new. Our intersection argument is separately proved.
- K. Bezdek and M. Naszodi, [The Kneser--Poulsen conjecture for special
  contractions](https://arxiv.org/html/1701.05074v4). Strong coordinate
  contractions and uniform contractions are prior sufficient mechanisms.
  This manuscript does not classify all alternative labelled realizations
  of the present orbit measures or claim to exclude all their compositions.
- K. Bezdek and R. Connelly, [Pushing disks apart: the Kneser--Poulsen
  conjecture in the plane](https://arxiv.org/abs/math/0108098).
  Its higher-dimensional motion-to-volume theorem is a credited premise
  of the radial/convex-core result, not a new transfer in this packet.

The two-value Jensen inequality, doubly stochastic matrices and the
four-character hyperbolic-function identity are elementary classical
ingredients. The mathematical claim here is their simultaneous application
to complete even-sign Gaussian orbit laws, its precise two-volume
consequence, and the full hinge sign for the existing indecomposable
eight-site input. Targeted primary-literature searches did not locate
this exact statement. This is not an exhaustive novelty determination,
and no campaign completion or historical-priority claim follows.

## Team dependencies and boundaries

- [R6's radial theorem](../gaussian_radial_contractions/PROOF.md), graph6317,
  source `78c08178239c5dabd91e4c46cfddd7ffb2e440f9`, and its
  [convex-core extension](../gaussian_radial_contractions/CONVEX_CORES.md),
  graph6331, source `15808c71e5da96669aefdc8736bc721f8e5c6521`.
  [Independent review6343](../gaussian_convex_core_review_frontier/REVIEW.md)
  accepts correctness. We use the singleton-core radial case after
  alignment, for all priors, variances and ball radii.
- [R6's open eight-site obstruction](../gaussian_open_eight_site_obstruction/PROOF.md),
  graph6370, source `42067bb9c28644139fbd2d9bd1bcd500963ecf68`.
  We reuse its exact input and target, and its uniformly contracted target.
  The new sign applies to orbit-balanced priors at those centres. It does
  not sign the spatial perturbation box or verify the independent
  no-five-dimensional-motion claim. That claim is not a proof premise.
- [The indecomposable reduction](../gaussian_indecomposable_contractions/PROOF.md),
  graph6164, and [effective coordinate bounds](../gaussian_indecomposable_contractions/COORDINATE_HEIGHT.md),
  graph6378, source `2bd8d341950153a750c20f9ad4638991ce3cbdb2`.
  These identify the relevance of the exact two-state interval to the
  full target. Our sixteen-case check concerns all possible intermediate
  placements because the tight face distances leave two positions per
  moving point. It is not a symmetry-only enumeration.
  [Independent review6390](../gaussian_coordinate_frontier_review2/REVIEW.md)
  arrived during this pass and accepts both the coordinate and linear
  chain-height arguments. It does not review the present parity theorem.
- [The exposed-edge endpoints](../gaussian_exposed_edge_tail/PROOF.md),
  graph6351, independently accepted at6372. The present parity argument
  signs the middle as well as both endpoints on its stated class; it
  does not alter, replay or optimize those earlier bounds.
- [R8's geometric weight-cone endpoint](../gaussian_majorisation_global_criterion/GEOMETRIC_LIMIT.md),
  graph6096, explains why a functional sign and a labelled obstruction
  do not by themselves establish a historically new ball-volume case.
  We retain that caution. Radius-preserving rematchings must also be
  considered. No claim that the present two-radius benchmark escapes
  all such alternatives is made.
- [R8's ordered square-cone orbit theorem](../gaussian_majorisation_square_cone_orbits/ORDERED_WEIGHTS.md)
  is earlier finite-orbit Gaussian positivity. Its directions, weight
  cone and finite orders differ from the current single-character
  comparison. We do not claim to invent finite-orbit rearrangement.
- [R7's signed-radial tail exclusion](../gaussian_signed_radial_tail_exclusion/PROOF.md),
  graph6339, signs spherical tests for independent radii and arbitrary
  directions. Its general angular class is not covered here. Conversely,
  the present theorem permits independently varying three axis lengths
  and proves actual Gaussian majorisation, not only a spherical test.
- [R8's relative spherical transfer](../gaussian_relative_spherical_transfer/PROOF.md),
  graph6376, and [R3's loss-proportional cubature](../gaussian_prior_localization/LOSS_CUBATURE.md),
  graph6364, independently accepted at6380, were inspected in the
  bounded refresh. Neither is needed for the exact antipodal kernel.
  Their additional sign and overlap premises are not silently assumed.
  [Review6384](../gaussian_relative_spherical_transfer_review_frontier/REVIEW.md)
  now accepts the conditional relative spherical transfer.

The former cap, orthocentric and depth-one classifications stay closed.
No extra flap family is introduced. The original eight-site map supplies
an adversarial test of the shared full question; the new result changes
its sign status for balanced priors. Arbitrary priors, asymmetric spatial
perturbations and the unrestricted finite class remain open.

## Reproducibility

The [checker](verify.py) uses Python 3.11 or later, standard library only.
Its formal Laurent expansion and direct sign-orbit evaluation are separate
arithmetic representations. Its two-by-two certificates and hinge
breakpoints use exact fractions. The sixteen root-aligned placements
are checked against every endpoint pair-distance interval.

No huge mesh, Gaussian quadrature, external solver, reviewer replay,
private input or large output is needed. Small controls support the
written argument and its constants; they are not independent mathematical
acceptance or a formal proof.
