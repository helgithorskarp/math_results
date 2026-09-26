# Sources, dependencies, and claim boundary

Primary sources and the shared papers below were read before publication.
Classical constructions, Gaussian calculus, and compactness are credited;
the application claimed here is the weighted shallow-flap formula and the
uniform exclusion of negative hinges away from zero threshold.
Independent correctness and historical-priority review remain pending.

1. **G. Aishwarya and D. Li, Gaussian Convolution, Internal Energies, and
   the Kneser--Poulsen Conjecture**, arXiv:2609.07041v2.
   [Primary paper](https://arxiv.org/html/2609.07041v2).
   Conjecture 1.1 supplies the named target. Equation (26), Theorem 1.12
   and its discussion credit the Gaussian convolved-velocity divergence
   mechanism to their earlier work. Our finite numerator is derived
   directly, rather than claiming a new general velocity theorem.
   The all-variance/all-energy requirements of the volume application
   are not met by the present threshold-truncated conclusion.

2. **H. Cheng, S. C. Tan and Y. Zheng, Continuous expansions in Euclidean
   space**, arXiv:1107.0140.
   [Primary paper](https://arxiv.org/pdf/1107.0140).
   Equations (5)--(7) give the regular-simplex flaps, with the expansion
   reversed here. Theorem 2.1 supplies the classical R5 motion obstruction.
   The remark after the contraction calculation treats general simplices;
   the concluding remarks discuss extensions of the obstruction. We give
   a self-contained tight-Gram argument for the precise arbitrary-normal
   family used here, without claiming priority for this geometric fact.

3. **Shared indecomposable-contraction reduction.**
   [Proof](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_indecomposable_contractions/PROOF.md).
   Source commit `4518e569424cbac04083e6cb9497cc97991cf301`.
   This motivates testing rigid maps with only two intermediate distance
   states. The present analytic proof does not require its Brehm reduction.
   Its graph transaction was still pending at the initial refresh; a
   source publication is not independent mathematical acceptance.

4. **Shared first-contact reduction.**
   [Proof](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_heat_profiles/CONTACT_REDUCTION.md).
   Graph height 6140, ref
   `bafkreibrti7gur7ddhxqck2kq7lco2x6lmosmorbytzjfzb26qufiasy3m`.
   Its treatment of null positive levels and hinge differentiation through
   critical levels was checked. Depth is the parameter here, not heat time;
   no sign of the outstanding contact covariance inequality is inferred.

5. **Shared isometric-reference theorem.**
   [Proof](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_isometric_reference/PROOF.md).
   Source commit `3a70618cd4611e258dcd275bdf45a139fd44e459`.
   Positivity on superlevel sets of a fixed reference law does not make
   those sets optimal for a perturbed source. This distinguishes its
   common-set conclusion from the actual perturbed hinges treated here.

6. **Earlier flap and common-target results.**
   [Common-target proof](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_common_target/PROOF.md),
   graph 6052, proves full comparison for a specified neighborhood of
   balanced ray weights with arbitrary tetrahedral background. The present
   family varies all face-normal depths near zero on arbitrary tetrahedra.
   [Small-mass boundary](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_small_mass/PROOF.md),
   graph 5984, is a precedent for treating the density maximum separately
   before making a uniform conclusion above a positive threshold floor.
   Its parameter is the mass moved from one fixed Gaussian, whereas here
   the map deforms at arbitrary weights and the limiting law can have four
   atoms and critical levels.
   [Nested-hull proof](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_nested_hulls/PROOF.md),
   graph 6000, closes its small-mass tail under additional geometric
   conditions. Neither conclusion closes the small-depth tail in this
   paper, and neither earlier result is superseded.

The exact checker is an internal control, not an independent review.
No bound in EXPECTED.json claims to integrate a Gaussian hinge or estimate
the uniform depth t_*. No primary-source search establishes priority.
