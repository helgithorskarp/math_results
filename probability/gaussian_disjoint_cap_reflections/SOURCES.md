# Sources and dependency boundary

Primary sources checked on 26 September 2026:

1. Gautam Aishwarya and Dongbin Li, *Gaussian Convolution, Internal Energies,
   and the Kneser--Poulsen Conjecture*,
   [arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
   Conjecture 1.1 is the shared target. Theorem 1.4(i)(a) is the density-value
   stochastic comparison used in Section 5. The paragraph following Theorem
   1.5 already notes that two auxiliary dimensions suffice for full
   majorisation. The transfer itself is not new here.
2. K. Bezdek and R. Connelly, *Pushing disks apart---the Kneser--Poulsen
   conjecture in the plane*, [arXiv:math/0108098](https://arxiv.org/pdf/math/0108098).
   Theorem 1 applies to endpoints in dimension $n$ with a piecewise smooth
   motion in $n+2$ dimensions and proves both union and intersection
   inequalities for individual radii. Its displacement-span-at-most-two and
   at-most-$n+3$-points corollaries are useful prior boundaries.
3. K. Bezdek and M. Naszodi, *The Kneser--Poulsen conjecture for special
   contractions*, [arXiv:1701.05074](https://arxiv.org/pdf/1701.05074).
   Section 1.2 defines coordinatewise strong contractions and discusses
   one-sided folds. The core/face argument and complete eight-state check in
   our Section 6 rule out every finite strong-contraction chain in dimension
   three for our finite example, including changing orthonormal frames.

Useful durable team context:

- [Paired affine rank and Gamma transfer](../gaussian_majorisation_rank_abel/PROOF.md),
  graph contribution `bafkreidnqtxulerp64z7i2syzjymc3beilgovd4gyfcu5h2mzmim5l5ytu`,
  committed height 5964; source commit
  `f7c122d6a5ade217930d63da27e67f9a9e55a539`.
  Sections 2--3 expose the dimension-five transfer, reproduced here to make
  the application self-contained. Our seven-site fixture has paired rank six.
- [Extremal-map and rigid-mesh reduction](../gaussian_majorisation_extremal_maps/PROOF.md),
  source commit `c68eb50ea52c9b578e90e89b5954ea4c63a0d89a`.
  This motivated studying interacting reflection cells. The present theorem
  does not depend on that reduction. Its existing broadcast was confirmed
  during the publication refresh at height 6132, with exact body and all
  four relations checked; it was not resubmitted.
- [Global interfaces](../gaussian_majorisation_global_criterion/INTERFACES.md)
  and [fixed-atom reduction](../gaussian_majorisation_global_criterion/ANCHOR_REDUCTION.md),
  [prior localization](../gaussian_prior_localization/PROOF.md),
  [axial rotation review guide](../gaussian_axial_cone_rotations/REVIEW_GUIDE.md),
  [ordered weights](../gaussian_majorisation_square_cone_orbits/ORDERED_WEIGHTS.md), and
  [finite-orbit obstruction](../gaussian_majorisation_finite_orbit_obstruction/PROOF.md)
  were inspected as shared scope and overlap context. None is used as a
  premise of the three-cap motion proof. The publication refresh also checked
  [uniform defect localization](../gaussian_prior_localization/DEFECT_LOCALIZATION.md),
  [the finite-certificate interface](../gaussian_majorisation_open_stability/CERTIFICATE_INTERFACE.md),
  and [the axial/extremal-map interface](../gaussian_axial_cone_rotations/LANE_HANDOFF.md).
  These clarify distinct ownership and trust boundaries; they do not supply
  the sign or the motion established here.

The final graph refresh reached height 6141. In particular it inspected the
new first-contact reduction at height 6140,
`bafkreibrti7gur7ddhxqck2kq7lco2x6lmosmorbytzjfzb26qufiasy3m`, which leaves an
ordered-contact flux inequality unresolved. That global reduction does not
turn the present cap class into a proof for unrestricted maps. There were no
review/objection relations on the cited paired-rank or rigid-mesh nodes at
that refresh. The earlier axial portfolio retains its independent review
and priority obligations.

No independent verification or priority finding is asserted by citing these
sources. Publication and the finite exact controls are not substitutes for
review of the analytic proof.
