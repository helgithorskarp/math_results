# Sources, interfaces and validation boundary

The named target is Conjecture 1.1 of Gautam Aishwarya and Dongbin Li,
[*Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture*](https://arxiv.org/html/2609.07041v2),
arXiv:2609.07041v2. The primary source was refreshed live on 26 September
2026. Neither that paper's pressure-class comparisons nor its contracting
motion theorem is used to assign a new Gaussian sign here.

Kirszbraun's classical theorem extends a Euclidean 1-Lipschitz map from
a subset to the full space without increasing its Lipschitz constant:
M. Kirszbraun, *Über die zusammenziehende und Lipschitzsche Transformationen*,
Fundamenta Mathematicae 22 (1934), 77--108,
[publisher page](https://impan.pl/en/publishing-house/journals-and-series/fundamenta-mathematicae/all/22/0/93089/uber-die-zusammenziehende-und-lipschitzsche-transformationen).
Here it is needed only to identify the support-map formulation with the
full-space formulation. The extension is not claimed to preserve volume
outside the prescribed cube union.

The measure approximation, rational perturbation and equal-weight splitting
are elementary. The Gaussian translation bound is proved in the text and
is also used in the prior team sources. Minimizing an affine function over
a cube proves the exact whole-component criterion. No priority is claimed
for these tools. Focused searches for Gaussian majorisation of uniform sets,
volume-preserving contractions and piecewise translations did not supply
this particular integer-cube reduction. That is not an exhaustive novelty
assessment. The contribution is the combined failure-preserving reduction
with its explicit metric condition and quantifier boundary.

## Durable team dependencies

- The [strict finite rational-witness reduction](../gaussian_majorisation_rank_abel/PROOF.md),
  graph h5964, is the earlier qualitative finite frontier. The current proof
  spells out the uniform-weight splitting and whole-component thickening
  instead of silently treating repeated source labels as distinct images.
- The [common-set minimax proof](../gaussian_prior_localization/PROOF.md),
  graph h6122, has a unique diffuse optimizer in a fixed-map problem.
  It is compatible with this result because our transformation changes the
  map, support, noise scale and law, and retains a strict gap or supremum.
- The [uniform compact localization](../gaussian_prior_localization/DEFECT_LOCALIZATION.md),
  source `4ed178725774e2fd3bb486f952825f58e52766cc`, graph h6134,
  gives a defect-dependent atom/radius bound. That bound does not count
  the repeated labels or bound the integer dilation used here.
- The [shift-averaging obstruction](../gaussian_prior_localization/SHIFT_AVERAGING_BOUNDARY.md),
  source `5239ba267b375e14159f1540db8d6569c1223dd9`, graph h6148,
  rules out discarding a signed interaction after averaging grid shifts.
  No such partition cancellation occurs here. Its t=1/4 rational geometry,
  rescaled by 256, supplies the eight-cube audit control; no Gaussian sign
  at that specific parameter was asserted there or is asserted here.
- The [fixed-atom reduction](../gaussian_majorisation_global_criterion/ANCHOR_REDUCTION.md),
  h6112, fixes a dominant atom in a different equivalent class. Our uniform
  set law has no atoms and is not asserted to preserve that prescribed
  mass. The two reductions can test the full question separately.

The latest seven other researchers' completed reports and relevant sources
were inspected. In particular the
[compact-moment/anchor handoff](../gaussian_majorisation_global_criterion/INTERFACES.md),
h6144, and [support-uniform moment budget](../gaussian_majorisation_open_stability/UNIFORM_FRONTIER.md),
source `88bc098a0f98080f8762ddae9b11cc4e63669e95`, h6150,
retain absolute approximation errors and their unresolved signs. Their
degree bounds are not finite cutoffs for our unbounded lattice class.
The [contact-flux reduction](../gaussian_majorisation_heat_profiles/CONTACT_REDUCTION.md),
h6140, has its separate conditional sign obligation. The
[common-set equality faces](../gaussian_majorisation_minimax_faces/PROOF.md),
h6142, cover special test sets. No sign from either is inferred here.

The [rigid-mesh reduction](../gaussian_majorisation_extremal_maps/PROOF.md),
h6132, acts on the map side by enlarging its finite domain. Our map is
locally a translation on the law support, but the full-space extension
need not be a translation, smooth, volume preserving, or supported on a
mesh of bounded complexity. The
[three-cap class](../gaussian_disjoint_cap_reflections/PROOF.md), h6146,
the [axial benchmark](../gaussian_axial_cone_rotations/LANE_HANDOFF.md), h6138,
and the ordered-weight class retain their own positive hypotheses. They
are not premises of the present reduction. Researcher 7's latest completed
search report supplied no certified negative integrated witness.

The final source refresh also inspected the
[indecomposable-contraction reduction](../gaussian_indecomposable_contractions/PROOF.md),
source `4518e569424cbac04083e6cb9497cc97991cf301`, and the
[universal Markov-transfer obstruction](../gaussian_markov_intertwining/PROOF.md),
source `b001598e004ba85c0934a5070f031d56c550a717`. The indecomposable reduction preserves a failing sign
through a covering step but need not retain a uniform fraction of its gap;
the present approximation retains arbitrarily much of a gap by changing
the geometry. Their normal forms are not asserted simultaneously. In
particular our strict center configurations are not indecomposable tight
meshes. Nothing here constructs a prior-independent Gaussian channel for
a fixed nonlinear map. The
[matrix-path regularity supplement](../gaussian_axial_cone_rotations/REGULARITY.md),
h6158, removes a qualification in an existing geometric class and is not
a premise of the uniform-set reduction.

Researcher 5's concurrently published
[isometric-reference theorem](../gaussian_isometric_reference/PROOF.md),
source `3a70618cd4611e258dcd275bdf45a139fd44e459`, gives the additional single-component common-set boundary
at the end of PROOF.md. Its author proof was read before incorporating
that corollary. A uniform cube reference has a full-dimensional support
on which T is one translation. The strict whole-cube inequalities therefore
give positive reference slack at every point of every other component.
The core uniform-set reduction and exact interaction identity do not use
this theorem, whose independent review remains pending. It does not imply
that the actual mixed law's maximizing source set is such a reference test.

**Attribution correction, 26 September 2026:** the initial version of
this paragraph and the accompanying graph broadcast mistakenly named
researcher 2. The general isometric-reference theorem is researcher 5's
work. Researcher 2 owns the distinct finite dual-cone/equality-face result
cited above. The linked source, mathematical premise, and optional
corollary are unchanged. The core uniform-set reduction is independent
of both results.

The [reference-test boundary](REFERENCE_MIXTURE_BOUNDARY.md) now checks
one possible extension of researcher 5's theorem. All isometric reference
laws for its explicit two-cube map are confined to one cube, so their
unit-variance Gaussian superlevel sets are convex by the posterior
covariance identity. An elementary midpoint and inclusion-exclusion
argument separates their same-volume convex averages from an actual
mixed-law superlevel set, uniformly even after L1 closure. This is a
boundary of that proposed coverage step, not a correction to the
reference theorem or a counterexample to majorisation. Its positive
control uses Aishwarya--Li Theorem 1.4 through the displayed continuous
contraction; no new Kneser--Poulsen class is inferred.

Before publishing this supplement the latest source for the team's
hemispherical/four-cap theorem, the matrix-lift regularity boundary, and
the failed posterior contact comparison were inspected. They do not
supply the missing mixed-test comparison. No existing geometric class,
certificate search, or contact-flux calculation is repeated here.

Researcher 5 concurrently published a
[separate analytic review](../gaussian_uniform_set_review/REVIEW.md),
source `e7980f4640026600f5a13bf7b184c08e8a5c210e`, accepting Theorem 1
and the exact interaction identity without mathematical correction. The
review pins the unchanged PROOF.md, whose initial status label predates
the review. It excludes independent acceptance of the optional application
of the reviewer's own reference theorem. It does not review this new
reference-test boundary. The review also independently identified and
corrected the attribution error above. This is an internal separate-lane
review, not external peer review or formalization.

## Exact audit and trust boundary

The compact standard-library program [verify.py](verify.py) uses integers
and exact fractions. It verifies every pair of cube corners, compares
their minimum squared-distance loss to the closed formula, checks lattice
separation, and computes the paired affine rank of the eight-cube control.
Its second positive fixture realizes the multiplicities 1 and 2 with
distinct equal-weight labels and a strict within-cluster contraction.
Three dilation controls distinguish expansion, a nonstrict boundary,
and strict whole-cube contraction. The universal sufficiency of corners
comes from the affine identity proved in PROOF.md, not sampling.

Neither the finite controls nor their expected output establishes a
Gaussian hinge sign. The analytic approximation, Gaussian scaling, error
bound, and supremum argument are unformalized written proofs. No solver,
quadrature, external data, large output, or omitted certificate is needed.
Author checks are not independent mathematical acceptance. The full
conjecture and the all-configuration inequality in Theorem 1 remain open.

CPython 3.11.2, normal and optimized runs, produced report SHA256
`907f37209d898b20da67da990538db628c44e7e5066a0832ea760055e35ce2ee`.
The positive controls cover 31 component pairs, each tested at all 64
corner pairs, in addition to the three dilation cases and the nonstrict
boundary replay. A damaged expected report is rejected under optimized
Python. No prior result's source or checker was edited by this contribution.
