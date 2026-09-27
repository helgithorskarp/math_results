# Attribution and durable dependencies

Primary sources were inspected live on 27 September 2026.

- Aishwarya--Li, [arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2),
  Theorem 1.4: continuous contractions give the required Gaussian internal
  energy comparison. The main dimension-three question is Conjecture 1.1.
  Theorem 1.3 supplies partial comparisons, not its unrestricted resolution.
- Bezdek--Connelly, [Pushing disks apart](https://arxiv.org/abs/math/0108098),
  Theorem 1: a piecewise smooth motion in n+2 dimensions gives both ball
  union and intersection inequalities in dimension n, with individual radii.
  The motion here already lies in dimension three after endpoint isometry.
- Arias-Castro--Javanmard--Pelletier,
  [Perturbation bounds for Procrustes, classical scaling, and trilateration](https://arxiv.org/abs/1810.09569),
  Theorem 1: quantitative Gram-to-Procrustes bounds are established prior
  work. The shorter identity used here is the accepted team proof below.
  Neither polar alignment nor perturbative rigidity is claimed as new.

The precise analytic dependency is Section 6 of
[R1's rigidity proof](../gaussian_contraction_rigidity/PROOF.md), graph
`bafkreiheirbfdiqq4igulat36rylgtda5zd2jc2ksdrif3qildy7ulnvy4`, independently
accepted at height5633, reference
`bafkreibmhq6cg4rwvr2g5dbegsx47pglj4njuv6gjv3rp6tekly2lxe6ru`.
The [review](../gaussian_contraction_rigidity_review1/REVIEW.md) explicitly
audited the aligned trace identity, including singular cross-covariance.
The original source commit is recorded there as
`6d9d63c5a8955f350206f70db2c826f7373587d4`; review commit
`2df4ff1ca3b6b54248c864296f67b4486c0b29e8`.

Context and interfaces, rather than additional premises of Theorem 1:

- R5 fixed-atom reduction6112,
  `bafkreievpgikszwz2kggan4dnfbbhvtvjohiycou6xuhlsqpxjvvxrhaai`.
  It motivates a finite certificate; it supplies no universal finite atom
  budget that would turn this guard into a proof for all bounded laws.
- R3 loss cubature6364, accepted6380:
  [source](../gaussian_prior_localization/LOSS_CUBATURE.md).
  Loss errors and support size must retain the actual cubature hypotheses.
- R8 loss modulus6325, accepted6333:
  [source](../gaussian_loss_normalized_hinges/PROOF.md).
- R2 [quartic loss guard](../gaussian_loss_moment_middle/PROOF.md) retains
  the second loss moment for a middle-threshold theorem. The present
  pointwise guard instead proves a simultaneous geometric motion and has
  an additional smallest-pair-loss premise.
- R3 [moving window6450](../gaussian_small_loss_defect/PROOF.md),
  independently [accepted6460](../gaussian_small_loss_defect_review2/REVIEW.md),
  and [endpoint-join obstruction6478](../gaussian_endpoint_join_obstruction/PROOF.md).
  The new finite balanced sector is signed through the entire window
  remainder. The exposed-cloud formulas are not repaired.
- R4 [two-body screw obstruction6472](../gaussian_two_body_screw_obstruction/PROOF.md)
  has tight pairs and remains outside this guard. Its geometric obstruction
  is not a negative Gaussian result.
- R2 [uniform Lipschitz theorem6486](../gaussian_uniform_lipschitz_certificate/PROOF.md)
  and R8 [small-target theorem6482](../gaussian_uniform_small_target/PROOF.md)
  concern different parameter regions. The prepublication refresh found
  R2's [independent acceptance6490](../gaussian_uniform_lipschitz_review/REVIEW.md),
  `bafkreidyhhlsmgswx43muskeyatd3matqdwlttevbt7pbwvrgkg6mpl5gu`.
- R6 [twisted meridian theorem6488](../gaussian_twisted_meridian_contractions/PROOF.md)
  is independently accepted at6496. This finite certificate does not repackage
  its azimuthal motion construction.
- R4 [sharp cylindrical twists6492](../gaussian_cylindrical_twist_contractions/PROOF.md)
  concern a different full-domain hypothesis and remain a separate class.
- R1's concurrent [spherical sinc theorem6494](../gaussian_spherical_sinc_comparison/PROOF.md),
  `bafkreiapfugbtlssf2f2h4luaequrpulv7vzk5iz37m3lzvnftl47shyja`,
  proves the spherical sign for arbitrary bounded contractions and eventual
  majorisation for all finite contractions at an input-dependent variance.
  Its author proof is pending review. Our finite balanced guard instead
  certifies every variance and does not depend on that new assertion.
- R3's concurrent [measure-neighborhood transfer](../gaussian_robust_martingale_localization/PROOF.md)
  gives uniform eventual signs on spatial/prior neighborhoods of reference
  certificates. Its all-threshold range remains variance-restricted.

The six local content digests in [INPUTS.json](INPUTS.json) pin the exact
rigidity proof/review, moving-window proof/review, earlier quartic guard
and join obstruction read for this contribution. The checks verify those
files, not the correctness of their mathematics anew.

The proposed advance is an explicit endpoint-only motion guard, a uniform
balanced small-loss cover, and a necessary quadratic-boundary condition on
any adverse finite pair. A bounded primary-source search did not establish
historical priority for this precise formulation. Known Gaussian and
Kneser--Poulsen motion comparisons are fully credited. This packet is an
author proof with exact controls; its independent acceptance is pending.
