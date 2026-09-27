# Sources, dependencies, and handoff

Primary literature checked on 27 September 2026:

- G. Aishwarya and D. Li, *Gaussian Convolution, Internal Energies, and the
  Kneser--Poulsen Conjecture*,
  [arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2), Conjecture 1.1.
  The full dimension-three question is the sole research target. This packet
  does not resolve it and does not assert a new Kneser--Poulsen class.
- Igors Gorbovickis, *Strict Kneser--Poulsen conjecture for large radii*,
  [arXiv:1006.0531v2](https://arxiv.org/html/1006.0531v2), Theorem 1.5 and
  Section 2. Strict mean-width decrease under every noncongruent finite
  contraction is already proved there. The paper uses higher-dimensional
  motions and rigidity; this packet supplies an explicit rational margin
  from a paired-hull edge. We claim neither qualitative strictness nor the
  large-radius ball inequalities as new. A bounded additional literature
  search did not determine priority for this exact quantitative formulation;
  no exhaustive novelty conclusion is asserted.

The Gaussian maximum interpolation identity, the tangent-cone edge
description, the vertex optimum of a compact polytope, and Cramer's rule
are standard facts. Their needed applications and constants are derived in
[PROOF.md](PROOF.md); no solver or software library certifies those general
steps. The exact checker supplies finite controls only.

The analytic dependency is Section 2 of the team's
[geometric low-threshold lemma](../gaussian_majorisation_open_stability/PROOF.md#2-low-thresholds-with-a-positive-geometric-margin),
graph `bafkreiaudc3oja6vhz7so5q5nc5ieqd7xcqvuxmnfa5jlu7dnnbpttgwhu`
at height 6094. Its current proof file was last touched by source commit
`52ef6716a271b31ac1046207764fc78d3db6165c`, with SHA-256
`ec382eca33145a0a7e487679d5205f31c42f94c290c2f98572c5e4a505b5e39b`.
Only its finite atomic, zero-cloud-radius case is used, and that argument
is recalled in full sufficient detail. We do not infer acceptance of its
entire original packet from later uses of this lemma.

The previous [strict-grid endpoint theorem](../gaussian_prior_localization/SIGNED_ENDPOINTS.md)
at graph 6287 (`bafkreidzywknhi3khr65enmniumcplrqltn7r6igpo3degnh6unhijkii4`)
uses a uniform positive loss on **every** pair to obtain a mean-support
margin. Source commit: `7bec0b3ac781fcc74a3d003a1e4d9fca2335c2b1`.
Its [accepting review](../gaussian_signed_endpoints_review_frontier/REVIEW.md)
is graph `bafkreictaxa627xhmay4rscjvdgjry56dmhe55qpojmj5qfk3tlb7ho5hy`
at 6297. The present bound is complementary: it permits arbitrarily many
tight pairs. We do not claim a better cutoff for the already strict grid.

The [local rigid-hull theorem](../gaussian_contact_rigid_hulls/PROOF.md), graph
`bafkreifcyaq2rjgyrec3w4mlsnlkolmavcbqf2hlpm4xj2umajfoomnljy` at 6222,
provides a local uniform linear mean-width gap near a full-rank isometry
under its general-position hypotheses. The present global bound uses a
different exposed-edge parameter and covers degenerate supports. Neither
statement alone supplies the middle sign for arbitrary contractions.

The intended consumer is the
[indecomposable test class](../gaussian_indecomposable_contractions/PROOF.md),
graph `bafkreihtkvrmyjs4cswetyjge4rpwvppjunbtmd4tnrw3o65cwvfa5wyey` at 6164,
source `4518e569424cbac04083e6cb9497cc97991cf301`. Its
[effective rational construction](../gaussian_indecomposable_contractions/EFFECTIVE_BOUND.md),
graph `bafkreib6l2ras4jqduttk2diybnooir2qrzg6jyin65ms44e45imfe7dkq` at 6260,
source `de9a0bb7af7179ea6e1b2c5b4013f84d6955f981`, leaves coordinate bit
length uncontrolled as a function of the input deficit. The present input
size bound applies once a rational map is given; it does not fill that gap.
The [linear chain-height improvement](../gaussian_indecomposable_contractions/LINEAR_HEIGHT.md),
graph `bafkreid7xm36tlhdk4jd6m3eebbbxerftmzyquwomgxwazfekxeif4hmm4` at 6329,
source `7b78d0a19464d4bcd847861438d5ae7001c344ba`, is a separate author proof
pending review. It preserves a larger hypothetical adverse hinge gap.

For that consumer the complete new interface is:

1. Verify rational coordinates, all contraction inequalities and one strict
   loss; remove zero-weight labels and choose a rational radius bound.
2. Either verify one supplied exposed-edge certificate and use Delta, or
   compute D,M and use the uniform Delta_0 from the input-size corollary.
3. Use the positive mass floor and variance to compute ell,B0,Q,E,b. Store
   the low cutoff as the exponent E. Both outer intervals have proved sign.
4. The remaining interval `[2^(-E),b]` still requires a signed argument.
   Endpoint control does not make an adverse-gap or beta-moment magnitude
   estimate into a sign proof.

The seven-site fixture is copied exactly from the already published
[positive three-cap control](../gaussian_disjoint_cap_reflections/PROOF.md),
graph `bafkreidc5kg5ekkk4drpdjpfgnr7frbhubsk77pncxp6vuizyvcedi6nay` at 6146,
source `bd57aa06efc46fd737b962bbd6d96384c4efdf2c`. We do not replay its
indecomposability classification or propose another cap/flap family. Its
known full positivity is used only to identify it as a positive control.

The accepted [straight-path pair obstruction](../gaussian_straight_path_pair_obstruction/PROOF.md),
graph `bafkreigr7q3hjdrmclmjdckwhfczkbkzfvebc7utennz5uaxvopx5fsotq` at 6295,
source `d940fbe38bc81839628861e87ffe95bdf4c1d59c`, remains valid. Positive
softmax pair terms for the Gaussian maximum in R6 do not imply positive
individual physical hinge-pair actions in R3.

The publication refresh also read the new
[convex-core theorem and accepting review](../gaussian_convex_core_review_frontier/REVIEW.md),
[full-prior cell review](../gaussian_frontier_prior_cell_review2/REVIEW.md),
[loss-normalized continuity review](../gaussian_loss_normalized_hinges_review_frontier/REVIEW.md),
[signed-radial spherical-tail exclusion](../gaussian_signed_radial_tail_exclusion/PROOF.md),
and [deep-flap cell](../gaussian_deep_flap_cell/README.md).
These remain distinct: the present theorem concerns effective endpoints for
all finite rational contraction maps, with no new all-threshold class.
No certificate replay or computation-intensive work was needed for this
source handoff. All finite calculations here use exact standard-library
Python arithmetic and complete in substantially less than one second.
