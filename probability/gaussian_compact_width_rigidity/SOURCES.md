# Sources, dependencies and scope

The sole campaign target is the full dimension-three majorisation question
from [Aishwarya--Li, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
The present conclusion is eventual in the variance for compactly supported
laws. It is not their unrestricted all-variance conjecture.

[Gorbovickis, Strict Kneser--Poulsen conjecture for large radii,
arXiv:1006.0531v2](https://arxiv.org/html/1006.0531v2), Theorems 1.5 and 1.3,
provides the prior finite-configuration strict mean-width and large-radius KP
results. Those conclusions are not new here. Sections 1--2 above provide a
self-contained compact equality argument instead of assuming finite
strictness survives a limit; Section 5 gives a uniform radial expansion for
arbitrary compact families. The Gaussian comparison interpolation itself is
classical, and no priority is claimed for it. A bounded literature search
did not establish historical priority for the compact extensions.

Exact source commits, graph references and SHA256 hashes of premises are
recorded in [INPUTS.json](INPUTS.json). The eventual conclusion uses:

- R3's support-cap theorem, graph6520:
  [proof](../gaussian_support_cap_localization/PROOF.md), accepted at6528:
  [review](../gaussian_support_cap_localization_review2/REVIEW.md).
  It already proves the cap-mass tail, the all-threshold eventual join
  conditional on positive support width, and finite rational certificate
  existence throughout that sector. We supply the compact equality theorem
  removing its remaining width hypothesis. The tail is restated with a
  cutoff to keep the present consequence checkable, not claimed as new.

- Universal spherical-sinc comparison, graph6494:
  [proof](../gaussian_spherical_sinc_comparison/PROOF.md), including its
  continuum quantitative estimate. The finite-support and uniformly strict
  Lipschitz eventual consequences were already proved there.
- Independent acceptance6506:
  [review](../gaussian_spherical_sinc_comparison_review2/REVIEW.md), and
  independent acceptance6508:
  [review](../gaussian_spherical_sinc_review/REVIEW.md).
- All-threshold eventual endpoint, graph6032, Theorem 1:
  [proof](../gaussian_majorisation_eventual_endpoint/PROOF.md), independently
  accepted at6048 in this [review](../gaussian_majorisation_eventual_endpoint_review2/README.md).
  Its analytic premises are the [spherical-tail estimate](../gaussian_majorisation_spherical_tail/PROOF.md)
  and [high-noise window](../gaussian_majorisation_high_noise_window/PROOF.md).

The current team reports and pertinent graph/source handoffs were read at
pass start and refreshed before publication. Relevant parallel developments
include R2's balanced-loss certificate6504, R3's robust localization6500,
R4's rigid-block certificate6516, R5's parked norm-preserving duplicate and
unequal-norm frontier, R6's affine-slice contractions6514, R7's signed radial
clouds6502, and R8's norm-preserving all-variance result6510. The refresh at
graph6529 also read R3's cap theorem6520 and review6528, R7's screw primitive
obstruction6524, R6's geometric class consolidation6526 and affine-slice
acceptance6518, and R8's norm-preserving acceptance6522. R2 explicitly parked
an overlapping cap consumer. None of those other class results is a
mathematical premise of compact rigidity. The new eventual theorem extends
qualitative scope but does not supersede their all-variance or uniform
quantitative information. No new independent acceptance is inferred from
acceptances of an earlier result.
