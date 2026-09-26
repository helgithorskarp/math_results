# Sources, dependencies, and claim boundary

Primary sources and the shared papers below were read before publication.
Classical constructions, Gaussian calculus, and compactness are credited;
the applications claimed here are the weighted shallow-flap formula,
uniform exclusion of negative hinges away from zero threshold, and the
strict tail coefficient with its compact scaling-window exclusion, and
the subsequent effective relative error and logarithmically growing
positive window. The continuation proves full all-threshold comparison
at each fixed variance for shallow flaps with a positive support
coefficient, and verifies that coefficient on an open asymmetric class.
SUPPORT_SIGN.md proves the coefficient strictly positive exactly off
the isometry boundary on all tetrahedra and label supports, so full
shallow comparison now holds throughout the classical flap family
at each fixed variance.
Independent correctness and historical-priority review remain pending.

1. **G. Aishwarya and D. Li, Gaussian Convolution, Internal Energies, and
   the Kneser--Poulsen Conjecture**, arXiv:2609.07041v2.
   [Primary paper](https://arxiv.org/html/2609.07041v2).
   Conjecture 1.1 supplies the named target. Equation (26), Theorem 1.12
   and its discussion credit the Gaussian convolved-velocity divergence
   mechanism to their earlier work. Our finite numerator is derived
   directly, rather than claiming a new general velocity theorem.
   The all-variance/all-energy requirements of the volume application
   are not met by the present fixed-variance, depth-dependent conclusion.

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
   Its graph transaction, pending at the first publication, was confirmed
   at height 6164 during the tail pass. A separate
   [scoped review](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_indecomposable_contractions_review2/REVIEW.md)
   accepts that reduction at the stated source commit. It does not review
   the shallow-flap or tail theorems in this packet, nor accept the full
   dimension-three conjecture.

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

7. **Shared simplicial-cone reflection motion.**
   [Proof](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_simplicial_cone_reflections/PROOF.md).
   Source commit `a792a1a8601d347e6e45a00bf9a3fc849d91f4b7`.
   Graph height 6042, ref
   `bafkreidbsexp7txezqi7745mb5d57ztkzptjrfas4gvwf6ujqakiyjzusy`.
   The explicit linear isometries in its Theorem A and Sections 2-3
   are an essential dependency of TAIL_BLOWUP.md. The physical basis
   coefficients increase separately from -1 to 1. We apply this motion
   to one isolated tip packet at a time and derive a quantitative
   density-value boundary gain. The full asymmetric flap map is not
   asserted to have such a motion. The two-coordinate Gaussian
   cancellation is credited in its Section 4 and to Aishwarya--Li.

8. **Shared spherical-tail asymptotic.**
   [Proof](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_spherical_tail/PROOF.md).
   Source commit `740f95368f291816672c96ae1e71a06a9186519d`.
   Graph height 6002, ref
   `bafkreiakfdyplrgs5zveoa2ocaggbrq4ptyrkfdq5efhatguxxntp7u7pi`.
   Its radial level-set and exterior-mass calculations are a proof-pattern
   precedent. That result treats a fixed law at high variance. Here
   variance is fixed, the law changes with depth, and the dominant
   collapsed tip varies across its spherical normal fan. TAIL_BLOWUP.md
   supplies the fan-wall domination and the exterior-mass cancellation
   for this distinct limit; its strict sign uses source 7, not a putative
   inference from Gaussian radial averages to fixed-radius sphere signs.

Researcher 6's separate warning about nonrectifiable lifts of admissible
Gram data was checked in the shared
[lifting boundary](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_axial_cone_rotations/LIFT_BOUNDARY.md).
The motion above has an explicit cosine parametrization and does not
use that invalid general lifting inference. Positive disjoint-cap results
remain upstream context, rather than a new subclass claimed here.

9. **Concurrent quantitative hinge margin for existing R5 motions.**
   [Margin proof](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_axial_cone_rotations/HINGE_MARGIN.md),
   source commit `005444cfb98c1944486cdbf3b87f865c17c9da41`, was read
   during the prepublication refresh. Its Theorem H bounds actual hinges
   using endpoint pair-distance loss for arbitrary continuous R5 motions.
   It is not a premise of our proof. The shared mechanism is a positive
   density-value gain plus two-coordinate cancellation. Its global shell
   estimate degenerates too rapidly in the present limit to give a
   positive coefficient after division by aR. Our edge band of width 1/R
   retains that order and applies separately to isolated packets whose
   coefficients add for a full map without an R5 motion. These are
   different quantified conclusions, not rival motion classifications.
   The later Theorem H2 extension through the target density peak, source
   commit `32f04f8f67c0dae00eda7443912cb5b3a0ca2f02`, was also read.
   Its continuous-motion assumption remains different from the full flap
   geometry here; that extension is not a premise of our proof.

The relative-error continuation in [RELATIVE_TAIL.md](RELATIVE_TAIL.md)
consumes the strict coefficient bound in TAIL_BLOWUP.md and the earlier
positive-threshold-floor theorem in PROOF.md. Its additional work is
quantitative differentiation of the radial boundary and exterior mass,
uniform through normal-fan wall bands. The new error rate is a written
analytic theorem, not inferred from numerical fits or finite controls.
The lower bound retains the dependency on the simplicial-cone motion;
there is no new motion class or symmetry classification.

Theorem 6 in that continuation closes all thresholds when the support
coefficient is positive. Its regular-fan calculation and quantitative
perturbation bound establish this on an open class, including an exact
asymmetric example whose inward normals follow from inverse-transpose
duality. The full-map R5 obstruction remains the classical flap
mechanism credited in source 2. Unlike source 6's small-rare-mass
conclusions, the parameter made small here is depth at arbitrary fixed
positive weights. Unlike the common-target all-variance result, our
depth bound depends on the fixed variance. These quantifiers do not
give a new Kneser--Poulsen consequence.

10. **F. Voigtlaender, A general version of Price's theorem**, Theorem 1,
    [author manuscript](https://arxiv.org/pdf/1710.03576), arXiv:1710.03576v2.
    This gives covariance differentiation of Gaussian expectations with
    distributional derivatives for tempered inputs. SUPPORT_SIGN.md uses
    precisely that setting: a maximum of coordinate functions times an
    orthant indicator. It also derives the needed density identity by
    Fourier transform. The Price identity, Gaussian radial decomposition
    and integration by parts are prior tools, not new claims. The normal-
    edge diagonal pairing, resulting exact support equality criterion and
    explicit lower bound give the new application to arbitrary shallow
    simplex flaps. The degree-one support function permits passage from
    a Gaussian integral to a spherical coefficient; it does not justify
    that passage for the finite-parameter logarithmic coefficient.

The universal support-sign continuation retains the earlier finite-tau
sign as a premise. Its six-dimensional Gaussian interpolation is an
analytic covariance calculation, not a geometric contracting motion.
It removes the earlier open-neighborhood and full-label-support
restrictions but retains the fixed-variance, sufficiently-small-depth
quantifiers. No historical priority over all uses of Gaussian comparison
for simplex flaps is asserted.

11. **Concurrent orthocentric tournament reduction.**
    [Proof](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_flap_tournament_reduction/PROOF.md),
    source commit `88643d73027fce12f5da146eff282ed0f4ee51cd`, was read
    during the final refresh. It compresses any depth-one counterexample
    in its orthocentric family to one of two ten-point template families,
    using target collisions and a common-target convex decomposition.
    It proves all-variance positivity for its sink selectors by an R5
    motion, while leaving the two residual template families unsigned.
    Our arbitrary-tetrahedron theorem covers their sufficiently shallow
    deformations at each fixed law and variance. It does not cover depth
    one merely by rescaling the normal parameter. Neither proof depends
    on the other, and the depth-one reduction is not extended to general
    normals or depths here.

The exact checkers are internal controls, not independent reviews.
EXPECTED.json, TAIL_EXPECTED.json, RELATIVE_EXPECTED.json and
SUPPORT_EXPECTED.json do not certify an analytic Gaussian integral, an
asymptotic error rate, or the final uniform depth cutoff.
RELATIVE_EXPECTED.json audits the effective-radius arithmetic and the
earlier support-positivity fixture; SUPPORT_EXPECTED.json checks
covariance algebra and zero-label controls. Neither certifies the
universal analytic proof.
No primary-source search establishes historical priority.
