# Sources, attribution and scope

Checked on 26 September 2026. The primary target is the human-named full
dimension-three question, not a graph-selected replacement problem.
All new results in this package are author proofs pending independent review.

## Primary literature

1. Gautam Aishwarya and Dongbin Li, *Gaussian Convolution, Internal Energies,
   and the Kneser--Poulsen Conjecture*,
   [arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
   Theorem 1.4(i)(a) is the density-value stochastic comparison used after
   the R5 motion. The two-coordinate transfer from that conclusion to all
   R3 Gaussian hinges is already known; it is not a new cancellation theorem.
2. K. Bezdek and R. Connelly, *Pushing disks apart---the Kneser--Poulsen
   conjecture in the plane*, [arXiv:math/0108098](https://arxiv.org/pdf/math/0108098).
   Theorem 1 gives both individual-radius ball-volume comparisons from a
   piecewise smooth motion in two auxiliary dimensions. Its hypotheses were
   checked directly. Its displacement-span-at-most-two consequence does not
   cover a generic map in the present class, whose normals can span R3.
3. K. Bezdek and M. Naszodi, *The Kneser--Poulsen conjecture for special
   contractions*, [arXiv:1701.05074](https://arxiv.org/abs/1701.05074).
   Strong coordinatewise contractions and one-sided folds are relevant
   prior positive classes. The no-finite-chain obstruction used here comes
   from the team's complete seven-site argument, not this paper.

Projection, the spherical triangle inequality, nonnegative affine duals,
and finite winding are classical ingredients. In particular, the obstruction
has the elementary Borsuk--Ulam mechanism of antipodal odd winding versus
triangle cancellation. Its entire finite argument is included; no unstated
topological result or computational topology package is a premise.

## Essential campaign input

The [three-cap proof](../gaussian_disjoint_cap_reflections/PROOF.md), graph
height **6146**, artifact
`bafkreidc5kg5ekkk4drpdjpfgnr7frbhubsk77pncxp6vuizyvcedi6nay`, verified source
commit `bd57aa06efc46fd737b962bbd6d96384c4efdf2c`, supplies:

- the conditional all-cap-count motion from U_ij<=1+2N_ij;
- the all-domain distance margin from disjointness and convexity;
- the seven-site obstruction to every finite strong-contraction chain,
  allowing changing orthonormal frames.

We repeat the short motion calculation to make the new certificate's
interpretation auditable. The prior automatic three-normal construction
used the stronger U_ij<=N_ij. We supply a different hemispherical projection
criterion for arbitrary cap count, the weaker four-normal construction,
and the exact limit to universal normal-only feasibility. The previous
source's proof and files are preserved. The four-cap control restricts to
its seven-site map, so the stated chain obstruction retains that explicit
author-proof dependency and review boundary.

## Other team interfaces consumed

The [finite positive-certificate interface](../gaussian_majorisation_open_stability/CERTIFICATE_INTERFACE.md),
h6136, commit `9a1047c925763125c72fa862e9200c40717b9c25`, was the planned
entry point of this pass. Its normalized moments, signed low endpoint,
source peak and all selected beta margins remain exact producer obligations.
The new cap result made a complete geometric finite dependency immediately
available; no routine moment producer or catalogue of positive samples was
published instead. This proof does not supply those inputs for arbitrary
unresolved configurations.

The [uniform defect localization](../gaussian_prior_localization/DEFECT_LOCALIZATION.md)
at h6134 and the [global/anchor interface](../gaussian_majorisation_global_criterion/INTERFACES.md)
at h6144 retain their all-configuration maxima and defect-dependent bounds.
The [ordered-contact reduction](../gaussian_majorisation_heat_profiles/CONTACT_REDUCTION.md),
h6140, retains its missing contact-flux sign. None is needed for the cap
motion, and none turns the two positive classes into the unrestricted theorem.

The [axial review portfolio](../gaussian_axial_cone_rotations/REVIEW_GUIDE.md)
and [geometric handoff](../gaussian_axial_cone_rotations/LANE_HANDOFF.md)
were inspected as benchmarks. The cap construction is a separate piecewise
affine map class, not a repackaging of an axial parameter bound. No universal
inclusion comparison with all earlier geometric classes is claimed.

The earlier [finite-orbit obstruction](../gaussian_majorisation_finite_orbit_obstruction/PROOF.md)
and [exact equality-face work](../gaussian_majorisation_minimax_faces/PROOF.md)
remain unchanged. A failed auxiliary motion certificate, like a failed
finite orbit rule, is not a negative integrated Gaussian hinge. The explicit
positive shallow-cap control demonstrates this distinction here.

The pre-publication refresh also consumed the [uniform moment-budget
improvement](../gaussian_majorisation_open_stability/UNIFORM_FRONTIER.md)
at h6150, the [grid-interaction obstruction](../gaussian_prior_localization/SHIFT_AVERAGING_BOUNDARY.md)
at h6148, the [Markov-kernel rigidity argument](../gaussian_markov_intertwining/PROOF.md),
and the [matrix-path regularity completion](../gaussian_axial_cone_rotations/REGULARITY.md)
at h6158. The cap proof uses none of these as a premise. In particular it
does not assert a prior-independent Gaussian Markov intertwiner; its motion
has analytic trajectories already, so it needs no regularization of a
general absolutely continuous matrix path. The updated moment budget remains
an approximation guarantee, not the missing all-configuration sign.

A final source refresh found the [indecomposable-contraction reduction](../gaussian_indecomposable_contractions/PROOF.md),
the [general isometric-reference equality classification](../gaussian_isometric_reference/PROOF.md),
and the [contact-equivalence audit](../gaussian_majorisation_contact_audit/REVIEW.md).
Their statements retain, respectively, an unresolved Gaussian sign on the
reduced class, arbitrary source sets outside the isometric-reference tests,
and the missing contact-flux sign. None is a premise of the cap proof or an
independent review of it.

Bounded primary-source searches for disjoint reflected caps, hemispherical
normals, and auxiliary-circle contraction did not identify this exact
automatic class statement. This is not an exhaustive priority determination.
The claim of extension is precise relative to the cited team three-cap
source; historical novelty and mathematical correctness both remain subject
to independent review.
