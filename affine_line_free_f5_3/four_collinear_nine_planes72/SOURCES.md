# Dependencies and provenance

* Elsholtz et al., *Maximal line-free sets in F_p^n*, Periodica
  Mathematica Hungarica 90 (2025), 7–21:
  [primary manuscript](https://arxiv.org/abs/2310.03382v2),
  [journal](https://doi.org/10.1007/s10998-024-00617-x).
  Source of the parameter, the prior published bounds and the known
  70-point construction. The public parent package improves the upper
  bound to 72; this contribution does not improve that numerical bound.
* [Global low-plane reduction](../low_planes72/README.md):
  complete 70 planar spectra and 61-equation, 463-column incidence
  system; exclusion of five collinear low-plane normals.
  Discovery Net bafkreifb7i4346rrz2c5ch5vhs4odx3n57xijazwl6jrgjhdmmijzthaqy.
* [Nine-plane frame](../nine_plane_frame72/THEOREM.md):
  exact inequality \(3a_8+a_9\ge11\).
  Discovery Net bafkreidz24r5ootmcelvbeuxsl3sp7ota4ycla343hkjgigmtl6bzl7nn4.
* [No eight-point plane](../no_eight_planes72/THEOREM.md), Team A
  researcher 2: exact exclusion of every eight-point plane, using the
  preceding two-eight-plane result and 1,252 mixed lifting proofs.
  The weighted bound and this exclusion together give \(a_9\ge11\).
  Discovery Net bafkreiauyfcdpuccibdqvyu6fmaabice6pjk5es4f3pnlwenisiaddyxuy.
  This new package excludes equality, proving \(a_9\ge12\).
* [Quadratic moment theorem](../quadratic_moments72/THEOREM.md), Team A
  researcher 3: the optional combined corollary uses its three moment
  types, the upper bound twelve in both higher ranks, and their normal
  configurations. The main certificate and affine two-case cover are
  independent of this additional premise.
  Discovery Net bafkreiamle5hqoxrssfa2xe4jatfux5g7u7sxdonwsf7iyus4vytsu7mqe.

The new material is the plane-pair consistency augmentation, the exact
certificate excluding eleven nine-planes, its projective consequence,
and the resulting global two-arrangement cover. The complete integral
pair-incidence control and two quotient controls state the precise
remaining obstruction. No absolute novelty or independent review claim
is intended.

SciPy 1.17.1 / HiGHS was used only to discover multipliers and controls.
The published replay uses exact integer arithmetic and does not import
SciPy. In particular, a solver's infeasibility status is not a proof
premise. The affine normalization has a six-map written proof and a
separate full finite group-action audit.

The 72-point equation system is not asserted for 71-point sets.
Existence at both 71 and 72 remains open in this package. Further
progress requires geometric lifting or stronger global compatibility.
