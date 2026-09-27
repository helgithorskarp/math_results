# Attribution, dependencies and limits

Primary-source and team audit: 27 September 2026.

## Primary inputs

* Aishwarya--Li, [arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2),
  Theorem 1.4(i)(a) and the paragraph after Theorem 1.5: sampled-density
  comparison along continuous contractions and its two-auxiliary-coordinate
  consequence. These are the analytic inputs, not newly proved theorems.
  The human-named dimension-three question is the sole problem source.
* Bezdek--Connelly, [arXiv:math/0108098v1](https://arxiv.org/pdf/math/0108098v1),
  Theorem 1 and Lemma 1: the n+2-dimensional motion transfer for unions and
  intersections of balls with individual radii, and the classical leapfrog.
  The present argument changes the geometric motion, not that transfer.
* Bezdek--Naszodi, [arXiv:1701.05074v4](https://arxiv.org/html/1701.05074v4),
  Section 1.2 and Theorem 1.3: the strong-coordinate class used for comparison.
  Our noncommuting Jacobian Gram matrices exclude a single fixed pair of
  endpoint frames, not compositions of their contractions.
* Cheng--Tan--Zheng, [arXiv:1107.0140](https://arxiv.org/abs/1107.0140):
  general higher-dimensional lifting obstructions are historical context.
  No new blanket nonlifting assertion is claimed here.

A targeted primary-literature search used Kneser--Poulsen with twisting,
helical, meridian, rotation and cylinder. No source encountered stated this
uniform class or the delayed meridian phase construction. This is a bounded
search, not proof of historical novelty. A genuinely new application is the
candidate claim under review; no first-discovery claim or all-compositions
classification is made.

## Durable team inputs

* [Meridian contractions](../gaussian_meridian_contractions/PROOF.md),
  graph6468 `bafkreiabngjrclqthd36unxe7cjzyqw3uhmgbr5it62si6yjca6l6dnqf4`,
  author source `a1013f169d8dd6d32ae76cf9817a47dccd3f100f`.
  Independently accepted in [review6474](../gaussian_meridian_contractions_review2/REVIEW.md),
  `bafkreidzoujpw4oq2taulksdcepinyjihjqqhrgc4z53xlxcap2aldeini`,
  review source `4ce38ac1f9fa49370b78c7fefd2d35eb73be944c`.
  The two auxiliary meridian-displacement coordinates are retained. The
  new phase term in the distance derivative and its uniform delayed schedule
  are the advance. The proof rederives the identity so that the motion is
  self-contained at the geometric level. The simple phase criterion
  recovers the full dimension-three untwisted class. Higher-dimensional
  meridian results are not superseded. The small polynomial-arithmetic
  implementation in verify.py is adapted from this packet.
* [Scalar defect](../gaussian_majorisation_scalar_defect/PROOF.md), graph6066,
  `bafkreidpgtehewdn2wn72hfi4c6aoq5bohkdss6dv36o37rjyxg6ndzxlq`.
  Its scalar inequality is the comparison target in Section 6. The new
  zero-mean Jacobian certificate excludes that direct criterion for a full
  bounded example. It is not a claim about the minimum number of centers.
* [Directional normal bundles](../gaussian_angular_ray_contractions/NORMAL_BUNDLES.md),
  graph6418 `bafkreidifxh4fbjb7cgjhs6p36ngsrlybpltu4axyiwdwkic7dsogtk574`,
  accepted in [review6424](../gaussian_directional_normal_bundle_review2/REVIEW.md),
  `bafkreibhmuskn3vq7rqrr3ymhd4ju3jwmcabijyfh353fwzp62zvzslehe`.
  Its entire directional class is preserved and not claimed to be subsumed.
  The present work changes azimuth and couples axial and radial coordinates.
  It is not an additional normal-ray profile theorem.
* [Axial and matrix paths](../gaussian_axial_cone_rotations/MATRIX_PATHS.md),
  graph6118 `bafkreigbbgjyf5dy5wbhowdlqdrsc24ykargcfqfc6xzir4lvktnyxzmry`,
  remain unchanged. Their block Gram paths are not premises of this motion.
* R4's [positive tangential screw](../gaussian_tangential_screw_lift/PROOF.md),
  graph6456 `bafkreigfdheebqbnx6pzws2o2ekbzwhj4w4rmqe6w4g6zz6ryp6ufm55p4`,
  is complementary. It moves one rigid region relative to another. No
  containment of that class is asserted.
* R4's [two-body screw obstruction](../gaussian_two_body_screw_obstruction/PROOF.md),
  graph6472 `bafkreihbnqijjhqxiveavrjuvcudkzzr266lv57rty5b3n7uty4ctubvpu`,
  source `aaf531d6cb33c6ad80f4543ddf1b2846af6464f0`, closes the universal
  equivariant-lift route: its cross-loss identity holds on entire rotational
  paraboloids, while the finite restriction has no R5 contraction.
  Our inequalities impose additional slack and do not circumvent that
  obstruction. This contextual use is not an independent review of R4's
  theorem and is not a new obstruction claim.

R4 retains extremal-map geometry; R7 retains adversarial search. R1's orbit
alignment has symmetry requirements on the source law that are absent here.
R2's uniform high-variance Lipschitz certificate, R3's obstruction to the
current tail/window join, R5's complete beta rows through twelve and R8's
uniform small-target comparison are current complementary inputs, not
dependencies of this proof. R2 retains a lower variance cutoff; R8's target
bound depends on the variance. Neither is an all-variance Kneser--Poulsen
transfer for those general maps. The full unrestricted sign question
remains open. No teammate or reviewer was assigned work in this pass.

## Exact checks and their limits

The checker expands the squared-distance identity and its phase derivative
as polynomials with formally independent cosine and sine symbols. It checks
the exact phase normalization, sufficient budgets on rational control
families, the regularization identities, zero Jacobian mean and positive
mean Gram matrix, and a nonzero Gram commutator. Broken formulas and invalid
phase schedules are required to be detected. All checks use Fraction and
remain enabled under Python -O.

Trigonometric maximization and the continuum inequality estimates are
proved in PROOF.md. Code does not establish the continuum theorem from a
finite sample, certify prior-art exhaustion, or replace the two cited
transfer theorems. There are no large omitted certificates.
