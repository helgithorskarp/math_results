# Sources and dependencies

Primary sources checked on 26 September 2026:

1. U. Brehm, *Extensions of distance reducing mappings to piecewise congruent
   mappings on Euclidean space*, Journal of Geometry 16 (1981), 187--193,
   [publisher page and abstract](https://link.springer.com/article/10.1007/BF01917587).
   Classical finite-set piecewise-isometric extension is the main geometric
   input. Its existence is not implemented or formally verified in this packet.
2. A. Petrunin and A. Yashinski, *Lectures on piecewise distance-preserving maps*,
   [arXiv:1405.6606](https://arxiv.org/pdf/1405.6606), Lecture 2 and final remarks
   (PDF page 47). The final remarks explicitly state the all-dimensional Brehm
   theorem. This supplies an open primary exposition alongside the original
   article's accessible abstract.
3. H. Cheng, S. P. Tan and Y. Zheng, *Continuous expansions in Euclidean space*,
   [arXiv:1107.0140](https://arxiv.org/pdf/1107.0140), Theorem 2.1 and equations
   (5)--(7). The outward-to-inward regular-simplex flap matching is a contraction
   and has no continuous motion in dimension below 2d. We use d=3 and the
   reversed expansion direction. The geometric construction and obstruction
   originate in this literature, including the cited Belk--Connelly preprint.
   The two-state proof in our Section 6 is a direct boundary check for our
   reduction, not a claim of priority for the example or nonliftability.
4. G. Aishwarya and D. Li, *Gaussian Convolution, Internal Energies, and the
   Kneser--Poulsen Conjecture*,
   [arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2), Conjecture 1.1.
   This remains the sole named problem source. The present finite-interval
   reduction itself does not invoke its motion theorem.

Direct team dependencies:

- [Rigid-mesh reduction](../gaussian_majorisation_extremal_maps/PROOF.md),
  graph `bafkreial3qwb5lb4vjbrail5pgm3vjtbuo2ezb24ftw4orjm7zafdo6xfm`,
  committed at 6132; source commit `c68eb50ea52c9b578e90e89b5954ea4c63a0d89a`.
  Sections 2--4 give the geometric extension, finite reflection choices, and
  positive-mass hinge estimate used here. The argument is restated to expose
  the distinction between its convex-source mesh and an extracted folded step.
- [Three-cap reflections](../gaussian_disjoint_cap_reflections/PROOF.md),
  graph `bafkreidc5kg5ekkk4drpdjpfgnr7frbhubsk77pncxp6vuizyvcedi6nay`,
  committed at 6146; source commit `bd57aa06efc46fd737b962bbd6d96384c4efdf2c`.
  Supplies the positive seven-site indecomposable control, with all-law
  Gaussian and arbitrary-radius volume conclusions. Its analytic sign proof
  is not replayed or inferred from the new finite-interval checker.
- [Paired-rank theorem](../gaussian_majorisation_rank_abel/PROOF.md),
  graph `bafkreidnqtxulerp64z7i2syzjymc3beilgovd4gyfcu5h2mzmim5l5ytu`, at 5964.
  Used only for the stated lower bound on a negative step's support and paired
  rank, not for existence of the indecomposable factorization.

Bounded coordination refresh also inspected the
[ordered-contact reduction](../gaussian_majorisation_heat_profiles/CONTACT_REDUCTION.md),
[uniform defect localization](../gaussian_prior_localization/DEFECT_LOCALIZATION.md),
[failed shift-averaging shortcut](../gaussian_prior_localization/SHIFT_AVERAGING_BOUNDARY.md),
[compact moment/fixed-atom interface](../gaussian_majorisation_global_criterion/INTERFACES.md),
[finite-certificate interface](../gaussian_majorisation_open_stability/CERTIFICATE_INTERFACE.md),
[common-set equality faces](../gaussian_majorisation_minimax_faces/PROOF.md), and
[axial/extremal-map handoff](../gaussian_axial_cone_rotations/LANE_HANDOFF.md).
These are context and method boundaries, not premises supplying an unknown
Gaussian sign. The latest counterexample searches reported no certified
negative integrated hinge.

The publication refresh additionally read the
[fixed-covariance Markov obstruction](../gaussian_markov_intertwining/PROOF.md),
[support-uniform moment budget](../gaussian_majorisation_open_stability/UNIFORM_FRONTIER.md),
and [matrix-class volume regularity proof](../gaussian_axial_cone_rotations/REGULARITY.md).
The Markov restriction concerns one channel for every prior; the moment
budget needs uniform sign information; the regularity proof concerns its
existing geometric class. None asserts the intermediate-state reduction here.

A bounded live search for indecomposable/irreducible Euclidean contractions,
factorization with Brehm extension, and Kneser--Poulsen intermediate
configurations found no exact prior statement of this Gaussian test-class
reduction. This is not an exhaustive priority determination. No source or
graph publication here amounts to independent mathematical acceptance.
