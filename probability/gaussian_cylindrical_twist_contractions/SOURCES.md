# Attribution, priority boundary, and current dependencies

Primary-source comparison on 27 September 2026. The sole problem source
is Aishwarya--Li's unrestricted Gaussian-majorisation conjecture in R3.
Correctness here is an author claim; independent review and historical
priority remain pending.

## Classical inputs

- Aishwarya--Li, [Gaussian Convolution, Internal Energies, and the
  Kneser--Poulsen Conjecture](https://arxiv.org/html/2609.07041v2),
  Theorem 1.4(i)(a) and the discussion after Theorem 1.5. These give the
  sampled-density comparison for continuous contractions and explicitly
  state the sufficiency of two auxiliary coordinates for full majorisation.
  Neither transfer is new here.
- Bezdek--Connelly, [Pushing disks apart](https://arxiv.org/pdf/math/0108098v1),
  Lemma 1 and Theorem 1. The axial second phase is their classical
  leapfrog specialized to one dimension; their n+2-dimensional motion
  theorem gives both arbitrary-radius ball comparisons. Truncation and
  center continuity cover the first phase's final time.
- Aishwarya--Li, [The Kneser--Poulsen phenomena for entropy](https://arxiv.org/html/2409.03664v3),
  Theorems 1.5--1.6. Continuous contraction and the resulting convolved
  transport are established antecedents. The new question is construction
  of such a motion for the entire cylindrical twist class, not a new
  transport-to-majorisation principle.
- Bezdek--Naszodi, [The Kneser--Poulsen conjecture for special
  contractions](https://arxiv.org/html/1701.05074v4), Section 1.2.
  Coordinatewise strong contractions are a prior sufficient class. The
  present proof uses a continuous twist motion and does not identify this
  whole class with strong contractions. No claim of noncontainment in
  all compositions of known positive operations is made.

The derivative norm criterion, Cauchy--Schwarz, monotone absolute-variation
coordinate and one-dimensional Lipschitz factorization are elementary
inputs. The reciprocal-square/square-root schedule is the constructive
ingredient that makes every pair distance decrease at exactly the endpoint
budget. Merely knowing that each intermediate map contracts the original
cylinder would not suffice; PROOF.md proves monotonicity between times.

## Team antecedents and distinctions

- The prepublication refresh found R6's concurrent
  [twisted-meridian theorem](../gaussian_twisted_meridian_contractions/PROOF.md),
  graph6488 `bafkreigmm2o2uehdxbseg3q54qlxqytbrevh3qdbhdireoyv6c74ky47wq`,
  source commit `2de654f1c1f69a3ab543993d1a53553e91e2164b`.
  It permits variable radial factors and radial-to-axial coupling under a
  phase bound. Those broader spatial dependencies are not subsumed here.
  Section 7 of our proof derives the necessary phase bound for its
  linear-meridian interpolation, regardless of the C1 phase clock, and
  proves that our exact endpoint budget is strictly larger on constant
  radial scale and linear axial pieces. The saturated example separates
  those motion formulas. Thus nonconstant azimuth is credited to both
  concurrent constructions; the additional assertion here is the full
  endpoint budget for this entire cylinder class. The comparison is a
  mathematical dependency, not an independent review or a priority claim.
- R6's [meridian theorem6468](../gaussian_meridian_contractions/PROOF.md)
  preserves azimuth and allows a general two-variable meridian contraction.
  Its arbitrary-prior/all-radius scope and classical transfers are credited.
  Its [acceptance source](../gaussian_meridian_contractions_review2/REVIEW.md)
  was inspected without replay. The present class permits actual azimuth
  change with height. Constant-twist overlap is not a novelty claim.
- The [paired-rank theorem5964](../gaussian_majorisation_rank_abel/PROOF.md)
  and [scalar-defect criterion6066](../gaussian_majorisation_scalar_defect/PROOF.md)
  are prior sufficient conditions. The rank-six finite benchmark and the
  whole-map scalar-axis obstruction make the comparison precise; they do
  not assert a new seven-point nonliftability phenomenon.
- R4's [positive screw dependency6456](../gaussian_tangential_screw_lift/PROOF.md)
  already supplied nonzero helicity as a non-normal diagnostic. Its
  rigid-group cross-loss conditions are different. Its mechanism is not
  extended by simply changing the rotation angle here.
- R4's [two-body obstruction6472](../gaussian_two_body_screw_obstruction/PROOF.md)
  closes universal R5 lifting for endpoint-contractive proper screws.
  A full cylinder with constant transverse scale has additional structure;
  no contradiction to the obstruction is claimed.

The start-of-pass graph also contained R1's Coxeter alignment6462, R2's
dilated-martingale all-threshold family6464, R3's accepted moving
small-loss window6450/6460 and new endpoint-join obstruction6478, R5's
complete beta row twelve6476, R8's covariance boundary6454, and R7's
unsigned rotating-ray search. Those results are not premises of this
motion. In particular, the log-radius ray mechanism in R7's private
exploration is not identified with twisting height slices of a solid
cylinder. No teammate checker or internal mathematical review was replayed.

The closing refresh also read R2's
[uniform Lipschitz certificate6486](../gaussian_uniform_lipschitz_certificate/PROOF.md)
and R8's [small-target theorem6482](../gaussian_uniform_small_target/PROOF.md).
The former needs sufficiently large variance; the latter's target bound
depends on the specified variance. Neither supplies the all-variance
twisting theorem above. R1's unequal-weight intermediate-alignment failure
and R7's unsigned asymmetric 48- and 24-point stress tests are preserved
negative evidence, not premises or contradictory Gaussian signs.

## Historical scope

Targeted searches for cylindrical/helical/twist contractions in
Kneser--Poulsen and Gaussian majorisation, followed by comparison with the
primary sources above, did not locate this exact class-wide motion.
This is a bounded search finding, not proof of historical novelty. The
ball-volume consequences are proved within scope; whether they are
historically new remains unresolved. No headline completion is asserted.
