# Sources, mathematical dependencies, and priority boundary

Audit date: 27 September 2026. The sole problem source is the human-named
dimension-three Gaussian-majorisation question of Aishwarya--Li. This
packet contains a complete author proof, pending independent correctness
and historical-priority review.

## Primary literature

- Aishwarya--Li, [Gaussian Convolution, Internal Energies, and the
  Kneser--Poulsen Conjecture, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2),
  Theorem 1.4(i)(a), Theorem 1.5 and the following discussion. The sampled
  density comparison and the sufficiency of two auxiliary coordinates
  for full majorisation are prior inputs. The current version was checked
  through the [abstract record](https://arxiv.org/abs/2609.07041).
- Bezdek--Connelly, [Pushing disks apart, arXiv:math/0108098v1](https://arxiv.org/pdf/math/0108098v1),
  Section 3, Theorem 1 and Lemma 1. These supply the n+2-dimensional motion
  transfer for individual-radius unions and intersections and the classical
  leapfrog. Their piecewise-smooth definition permits finitely many
  exceptional times. Our first phase is analytic in the interior, with
  continuous endpoints; its intermediate configurations need not be in R3.
- Bezdek--Naszodi, [The Kneser--Poulsen conjecture for special contractions,
  arXiv:1701.05074v4](https://arxiv.org/pdf/1701.05074v4), Section 1.2 and
  Theorem 1.3. Coordinatewise strong contractions are an established
  sufficient class. The noncommuting derivative Gram matrices in our
  example exclude a single such representation even after independent
  fixed endpoint frame changes. This does not exclude compositions.
- Bezdek, [From the Kneser--Poulsen conjecture to ball-polyhedra,
  arXiv:0903.4846](https://arxiv.org/abs/0903.4846), is historical context
  for known contraction classes and lift-based consequences, not an
  additional premise of the proof.

The matrix Schur complement, the finite-dimensional Caratheodory ODE
existence theorem, and Cauchy--Schwarz are standard mathematical inputs.
The new candidate mechanism is the horizontal completion of an arbitrary
affine slice curve, followed by the uniform transverse-gain bound and an
explicit five-dimensional motion. No new general Gaussian-to-hinge or
motion-to-ball theorem is asserted.

Targeted searches combined Kneser--Poulsen, continuous contraction, affine,
parallel hyperplanes, slice, fiber, and prism. The inspected primary
sources did not state the entire class in this packet. This bounded search
does not establish first discovery. Constant affine maps and overlaps
with known strong or lower-dimensional classes are not novelty claims.
The candidate new Kneser--Poulsen consequence is the class-wide comparison
for arbitrary endpoint-contractive varying affine slices, including both
ball volumes and individual radii. Historical priority for that exact
class remains unresolved.

## Direct structural input and preserved classes

- R4's [cylindrical twist theorem](../gaussian_cylindrical_twist_contractions/PROOF.md),
  graph6492 `bafkreiatrj4tkhiaeagfankmtzhoxsxopelhmauelwipfc7qcf3z7mee5y`,
  source `d1398077ed58c27f8ec7446d6d3b0303ab6203fc`, is the direct
  constructive antecedent. It treats A(z)=a Q_(theta(z)), b=0, constant a,
  at its exact full-cylinder endpoint budget and allows arbitrary h.
  We use its unfolded axial speed sqrt(1-t+t h'^2), Cauchy pair estimate,
  and final one-dimensional fold. Our completion lemma replaces the
  constant conformal slice calculation by arbitrary matrices and
  translations on any convex cross-section. All its Gaussian and
  individual-radius ball conclusions are included, but its R4 lift is
  sharper than our R5 lift. We reprove the motion and do not use the
  unreviewed theorem's conclusion as an unexplained black box.
- The accepted [meridian theorem](../gaussian_meridian_contractions/PROOF.md),
  graph6468 `bafkreiabngjrclqthd36unxe7cjzyqw3uhmgbr5it62si6yjca6l6dnqf4`,
  and [twisted-meridian theorem](../gaussian_twisted_meridian_contractions/PROOF.md),
  graph6488 `bafkreigmm2o2uehdxbseg3q54qlxqytbrevh3qdbhdireoyv6c74ky47wq`,
  are complementary: their target axial coordinate can depend on radius,
  which is not allowed here. The twisted theorem's author source is
  `2de654f1c1f69a3ab543993d1a53553e91e2164b`. Its independent acceptances
  [6496](../gaussian_twisted_meridian_contractions_review2/REVIEW.md),
  `bafkreicwi3ehfaun5x5nqzh2jdgs2ab3xjhzolsd6sjr5enl3tvbawubvi`, and
  [6498](../gaussian_twisted_meridian_review/REVIEW.md),
  `bafkreibx65wrobievpiu3vai443qhbcxyq5x7wu46e6f6knxcbk35zllyq`,
  were read. They accept that prior theorem, not this extension. Their
  respective source commits are
  `fb98968d2af206773a57fd8e9b710d448bdf8a64` and
  `df4fc298eff95c41e7fb4deea34457127a84964f`.
- The reviewed [directional normal-bundle theorem](../gaussian_angular_ray_contractions/NORMAL_BUNDLES.md),
  graph6418 `bafkreidifxh4fbjb7cgjhs6p36ngsrlybpltu4axyiwdwkic7dsogtk574`,
  and [axial/matrix paths](../gaussian_axial_cone_rotations/MATRIX_PATHS.md),
  graph6118 `bafkreigbbgjyf5dy5wbhowdlqdrsc24ykargcfqfc6xzir4lvktnyxzmry`,
  remain unchanged. The auxiliary normal velocity in our proof is not an
  endpoint assumption of projection or normal-ray motion. We make no
  all-compositions classification or containment claim for those packages.
- R4's [two-body screw obstruction](../gaussian_two_body_screw_obstruction/PROOF.md),
  graph6472 `bafkreihbnqijjhqxiveavrjuvcudkzzr266lv57rty5b3n7uty4ctubvpu`,
  remains a boundary to universal R5 lifting. Arbitrary finite endpoint
  data, disconnected rigid groups, or rotational paraboloids do not
  supply a nonexpansive affine-slice extension on a whole prism. The present
  theorem does not contradict or independently re-review that obstruction.

R6's role here is the geometric completion and its internal-energy/Kneser--
Poulsen consequence. R4 retains extremal-map and deformation ownership;
R7 retains counterexample searches. No teammate or reviewer was assigned
work. The new construction is not a retuning of a phase clock or a
cosmetic normal-ray subclass.

## Current team frontier

The publication refresh read all seven other researchers' latest completed
reports and relevant source changes. R1's
[spherical comparison6494](../gaussian_spherical_sinc_comparison/PROOF.md)
now signs every bounded contraction's spherical gap, gives eventual
majorisation for every finite pair, and a uniform eventual bound for every
Lipschitz constant below one. Its
[independent acceptance](../gaussian_spherical_sinc_comparison_review2/REVIEW.md)
was also inspected. It does not give all variances or union/intersection
volume comparisons for arbitrary maps. R2's
[balanced finite certificate6504](../gaussian_balanced_loss_certificate/PROOF.md)
does give all variances under a positive scatter and balanced small-loss
guard; it uses a different straight-motion mechanism. Neither is a premise
here, and neither guard is required by (1).

R3's [measure-neighborhood transfer6500](../gaussian_robust_martingale_localization/README.md)
and R7's [diffuse signed-radial theorem6502](../gaussian_signed_radial_clouds/README.md)
have variance cutoffs. R8's
[small-target result6482](../gaussian_uniform_small_target/PROOF.md)
works at every specified variance with a variance-dependent target bound.
R5's accepted beta rows and retained-interaction result remain pressure
comparisons, not full all-variance majorisation. A final repository refresh
also found R5's new
[norm-preserving theorem](../gaussian_norm_preserving_majorisation/PROOF.md),
source `7ec05f2b89b4ab69de7a6696f236aa1f6ecc3ffc`: it claims all variances
and both ball-volume comparisons when all pointwise distances to an anchor
are preserved. Its imported spherical identity has independent acceptance;
these new consequences are still author-level. That exact anchor condition
is absent here, and the two full classes are not identified. These results
are complementary inputs to the shared problem and are not used in this
proof. The full three-dimensional all-variance question remains open.

## Exact evidence and limitations

The checker is self-contained, using Python Fraction and a small sparse
polynomial implementation patterned on the earlier meridian packets. It
checks the cleared-denominator matrix identity universally, rational
horizontal-completion jets, the singular-defect regularization algebra,
the entire-prism derivative bound, and a finite distance/clock example.
It rejects a missing inverse transpose, omitted translation completion,
the naive positive-square-root frame gauge, and raw linear axial
interpolation. It also checks the example's derivative Gram commutator.

These are author algebra controls, not an independent review or a
computer-assisted proof of the continuum theorem. The ODE existence,
integration and approximation arguments and the cited transfer theorems
remain written mathematics. No numerical integration, private data,
external solver, or omitted large certificate is used. Assertions are
required; the checker deliberately refuses Python's optimized mode.
