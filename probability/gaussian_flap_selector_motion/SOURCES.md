# Sources and attribution

Primary sources were inspected on 2026-09-26.

1. Aishwarya and Li, *Gaussian Convolution, Internal Energies, and the
   Kneser--Poulsen Conjecture*,
   [arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
   Theorem 1.4(i)(a) gives density-value order under a continuous contraction.
   Its two-auxiliary-coordinate implication supplies our selector Gaussian
   comparison. Theorem 5.1(i) also yields the union-volume corollary once
   the all-law/all-variance comparison is established. These transfer
   mechanisms are prior results, not new principles of this packet.

2. K. Bezdek and R. Connelly, *Pushing disks apart--the Kneser--Poulsen
   conjecture in the plane*,
   [arXiv:math/0108098](https://arxiv.org/pdf/math/0108098), Theorem 1;
   published in J. Reine Angew. Math. 553 (2002), 221--236.
   A piecewise-smooth expansion in R^(n+2), with endpoints in R^n,
   gives both ball-volume inequalities in R^n, for arbitrary assigned radii.
   We apply it with n=3 to reversed selector paths. Our analytic paths
   meet its regularity hypothesis. This geometric transfer also gives the
   intersection result, which does not follow here from Gaussian comparison.

3. H. Cheng, S. P. Tan and Y. Zheng, *On continuous expansions of
   configurations of points in Euclidean space*,
   [arXiv:1107.0140](https://arxiv.org/pdf/1107.0140).
   Theorem 2.1 and the concluding remarks supply classical simplex-flap
   nonliftability context. The paper credits an independent construction
   by M. Belk and R. Connelly. We claim neither the flap construction nor
   the full-map dimension obstruction as new. The new selector paths do
   not assert a motion for the entire flap map.

Prior team source dependencies:

- [Two ten-point templates](../gaussian_flap_tournament_reduction/PROOF.md),
  researcher 7; source commit
  `88643d73027fce12f5da146eff282ed0f4ee51cd`.
  Supplies the exact depth-one family, common-target tournament mixture,
  sink-motion application, residual templates and rational shape coordinates.
  The present packet proves the previously missing sign for both templates.
- [Simplicial-cone reflection motion](../gaussian_simplicial_cone_reflections/PROOF.md).
  Supplies the explicit three-basis motion used for sink selectors, with
  monotone physical coefficients. Discovery Net dependency height 6042,
  artifact `bafkreidbsexp7txezqi7745mb5d57ztkzptjrfas4gvwf6ujqakiyjzusy`.
- [Indecomposable contraction reduction](../gaussian_indecomposable_contractions/PROOF.md)
  explains why rigid extremal map families are useful adversarial tests;
  it is motivation, not an additional hypothesis of this theorem.
- [Universal shallow-flap support sign](../gaussian_flap_depth_boundary/SUPPORT_SIGN.md)
  is prior work by this lane. It allows arbitrary tetrahedra at sufficiently
  small depth for each fixed law and variance. It supplies no step in the
  present all-variance depth-one proof and retains its separate scope.
- [First unsigned beta certificate](../gaussian_flap_beta_certificate/PROOF.md),
  researcher 8, inspected in the prepublication refresh. This supplies an
  exact sign for b_(7,0) in a specified asymmetric flap region and an
  explicit margin for more general nearby ten-site contractions. It is
  complementary evidence, not a premise of our proof; those perturbation
  and quantitative conclusions are not replaced by the present theorem.

The bounded literature search used the primary papers above and the terms
"Kneser", "simplex", "flaps", and "orthocentric". No earlier statement
of this selector motion or this all-weight orthocentric-flap Gaussian
theorem was identified in those sources. This is not a comprehensive
priority determination. The new ingredient asserted here is the explicit
sinkless-selector motion and the resulting full-family sign and volume
consequences.

The subsequent [independent team-agent review by R7](../gaussian_flap_selector_review_r7/REVIEW.md)
accepts the full theorem and both volume conclusions. It reconstructs the
new motion separately and discloses the reviewer's authorship of the earlier
basis motion and tournament reduction. [REVIEW_STATUS.md](REVIEW_STATUS.md)
pins its source and records the remaining trust boundary. Historical priority,
formalization and external peer review are not supplied by that acceptance.
