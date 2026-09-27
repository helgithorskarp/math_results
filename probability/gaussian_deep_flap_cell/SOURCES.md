# Sources, dependencies, and research boundary

Sources inspected 27 September 2026. The only problem source is the
human-named bounded-law dimension-three Gaussian majorisation problem.

## Primary literature

- G. Aishwarya and D. Li, *Gaussian Convolution, Internal Energies, and the
  Kneser--Poulsen Conjecture*, [arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
  Conjecture 1.1 is the target. Hinge inequalities express full majorisation.
  The published dimension-dependent pressure comparison is not used as a
  substitute for an unknown hinge sign.
- H. Cheng, S. P. Tan and Y. Zheng, *On continuous expansions of
  configurations of points in Euclidean space*,
  [arXiv:1107.0140](https://arxiv.org/pdf/1107.0140).
  The simplex-flap construction and its dimension obstruction are classical.
  We use it as a geometrically motivated finite input, not a new construction.
  No nonliftability claim is made for the damped or perturbed cell here.

Layer cake, radial integration, Gaussian translation bounds, angular charts,
interval arithmetic, and symmetry reduction are standard methods. We make
no priority claim for them. The reproducible mathematical evidence is the
complete signed cover for the explicit cell and the resulting operational
radial-volume method. It does not establish an all-variance family or classify
the remaining geometric cases.

## Computational and analytic premises

The exact file hashes in `radial.py` pin these R3 sources before import:

- [DIRECT_HINGE.md](../gaussian_prior_localization/DIRECT_HINGE.md) and
  [direct_hinge.py](../gaussian_prior_localization/direct_hinge.py), original
  source commit `2e0d74152db80935259c25142da0e42d37ff0399`, graph 6228.
  The nonsmooth absolute quadrature and tail bound have an
  [accepting independent review](../gaussian_direct_hinge_review_frontier/REVIEW.md),
  graph 6271, source `90f0acbbba998f8b46829656cce23fe40184d6f3`.
  The new radial-volume algorithm is not covered by that review.
- [CUBATURE_FRONTIER.md](../gaussian_prior_localization/CUBATURE_FRONTIER.md),
  graph 6212, defines the rational family R^c_k used for the membership check.
  Our normalization includes both zero anchors; no unanchored input is
  silently declared to belong to that family.

The all-knots slope sweep is reused from the
[earlier cell checker](../gaussian_frontier_middle_cell/verify.py), final
source `d849aef5f3e3c98c0d32d3dd992c7259f19f52cd`, original graph 6311.
Its [independent acceptance](../gaussian_frontier_middle_cell_review2/REVIEW.md)
is now graph 6321, source `db41b0d89d8248519d489d893c37f3e9aa55201b`.
That earlier cell used a pointwise clipped-density endpoint. The present
signed angular integration, scalar arithmetic, and complete radial cover
are new author obligations. Independent review is pending.

R8's [bounded-law functional bridge](../gaussian_majorisation_open_stability/BOUNDED_LAWS.md)
and [certificate interface](../gaussian_majorisation_open_stability/CERTIFICATE_INTERFACE.md)
provide the endpoint/middle research architecture. The proof here spells
out its actual endpoint bounds and perturbation cost. Qualitative stability
alone is not invoked to infer a numerical cell or a threshold sign.

## Concurrent advances consumed, with scope retained

- The [accepted depth-one selector theorem](../gaussian_flap_selector_motion/TEMPLATE_HANDOFF.md)
  gives all weights and variances for its orthocentric depth-one geometry.
  It does not state the depth-two finite certificate proved here. The
  [shallow-depth theorem](../gaussian_flap_depth_boundary/SUPPORT_SIGN.md)
  gives a geometry/weight/variance-dependent small-depth conclusion, not a
  numerical cutoff covering this input.
- The [rank-six conditional-kernel classification](../gaussian_conditional_kernel_obstruction/PROOF.md),
  original 6267 and accepted 6289/6293, remains a design constraint. No
  individual conditional kernel is assumed nonnegative.
- R5's [eighth-beta theorem](../gaussian_averaged_eighth_beta/PROOF.md),
  original 6315, now has [independent acceptance](../gaussian_averaged_eighth_beta_review_frontier/REVIEW.md)
  at 6327, source `6ba75f30ffd28c08181d193c183430b004ff1b9e`.
  The seven-factor obligation and row eight are closed. This certificate
  does not pursue adjacent beta entries or duplicate that analytic ownership.
- R8's [loss-normalized hinge continuity](../gaussian_loss_normalized_hinges/PROOF.md),
  original 6325, concerns a radius/noise regime absent here. Its new author
  bounds now have [independent acceptance](../gaussian_loss_normalized_hinges_review_frontier/REVIEW.md)
  at 6333. They are not a sign premise for this cell.
- R1's [prior-stationary contact reduction](../gaussian_prior_stationary_contacts/PROOF.md),
  original 6323, and R4's [linear mesh-height reduction](../gaussian_indecomposable_contractions/LINEAR_HEIGHT.md),
  original 6329, change the unrestricted witness landscape but do not
  supply the present hinge signs. Both retain their own review status.
- The [radial-contraction map theorem](../gaussian_radial_contractions/PROOF.md),
  original 6317, and its [convex-core extension](../gaussian_radial_contractions/CONVEX_CORES.md),
  original 6331, are different all-law, all-variance positive classes.
  The latter has [independent correctness acceptance](../gaussian_convex_core_review_frontier/REVIEW.md)
  at 6343, source `c38d271f4316ef4bcfd8115aeae7af561feb3148`;
  historical novelty remains uncertain. That review does not cover this cell.
  Radial *spatial integration* in this certificate is not an assumption that
  the finite contraction has a direction-preserving radial map form.
- The [source-cluster theorem](../gaussian_prior_localization/CLUSTER_DEFECT.md),
  original 6305, has two qualified reviews, 6313/6319. They accept its core
  bound and identify a factor-four exponent error in its optional separation
  schedule; R3 has now published the correction. Neither schedule is used
  here. The accepted unrestricted 7/50
  defect bound remains the broader context and is not optimized.
- R3's [full-prior and diffuse near-point cell](../gaussian_frontier_prior_cell/PROOF.md),
  original 6335, enlarges the earlier coordinate boxes through source-hinge
  convexity. It now has [independent acceptance](../gaussian_frontier_prior_cell_review2/REVIEW.md)
  at 6347, source `4f8c4b57008f7e99321bf7491c7880bca86aab46`.
  That review uses an independent asymmetric-orbit decomposition and accepts
  the stated all-threshold prior/measure cell at variance one. It does not
  review the radial roots, angular cover, or volume signs of this packet.
  This packet retains fixed masses and treats a different extended-target
  geometry; it does not duplicate that prior-simplex extension.
- R7's [signed radial product-law tail exclusion](../gaussian_signed_radial_tail_exclusion/PROOF.md)
  concerns a spherical log-MGF necessary condition. The present certificate
  directly signs actual superlevel volumes and Gaussian hinges; it does not
  assert an unrestricted implication from that necessary condition.
- R8's [uniform dominant-atom window](../gaussian_uniform_dominant_atom_window/PROOF.md),
  original 6349, source `a86e9ef2f7a4a3951e8d2214c2c4a52b9bf045d0`,
  is a separate author proof, awaiting independent review. It supplies an
  actual loss-normalized middle sign uniformly over bounded rare laws and
  contractions, with an explicit dominant-mass restriction. It leaves its
  lower thresholds unsigned. No overlap with a geometric tail cutoff is
  assumed, and it is not a premise of the complete cover in this packet.
- R4's [exposed-edge endpoint certificate](../gaussian_exposed_edge_tail/PROOF.md),
  original 6351, source `b731c0abe161351d37ca660635e4db2c87f4c9c1`,
  gives a quantitative mean-support margin for noncongruent finite
  contractions, including preserved distances. It is an author result
  awaiting independent review and signs endpoints, not the remaining
  middle. This packet instead supplies its own substantially larger
  geometry-specific tail interval and checks its overlap explicitly.

## Trust and reproducibility

The public packet includes every substantive input, generator, verifier,
and compact expected result. Python integers/Fraction and the written
mathematical reductions are the trust base. Floats are used only to propose
radial witnesses which are then checked by exact inequalities; changing
their implementation can affect runtime, failure, and diagnostic hashes,
but cannot turn a false sign into a successful certificate.

Normal/optimized author runs, scalar cross-checks, small unquotiented grids,
and damaged-root controls are validation, not independent mathematical
acceptance. No solver, imported dataset, private file, proof-assistant kernel,
or omitted large certificate is required. Exact source hashes detect changes
to the computational and quadrature premises. The universal theorem is not
inferred from tests alone.
