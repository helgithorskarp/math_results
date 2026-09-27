# Sources and dependency handoff

The sole problem source is Aishwarya--Li,
[Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture,
arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2), Conjecture1.1.
The primary page was checked live27 September2026. The paper poses full
majorisation in dimension three; this packet does not settle it.

Essential campaign dependencies, with exact bytes/revisions in
[INPUTS.json](INPUTS.json):

- R8 [norm-preserving comparison](../gaussian_norm_preserving_majorisation/PROOF.md),
  graph6510, accepted at6522 by the
  [independent review](../gaussian_norm_preserving_majorisation_review2/REVIEW.md).
  We import its positive spherical identity, whose own source is R1's
  spherical operator formula, and its nonnegative hinge/peak comparison.
- R8 [strictness and radial crossing](../gaussian_norm_preserving_strictness/PROOF.md),
  graph6552, source2106c12535f7ed647e8127ef17c14f899233d5e1,
  accepted at6556 in its stated scope by the
  [independent review](../gaussian_norm_preserving_strictness_review2/REVIEW.md).
  The positive cap, smoothing, and diffuse-law argument
  belong to that source. Our change is the logarithmic radial cutoff and
  its polynomial lower envelope. This packet is not an independent review.
  INPUT.json reproduces its rational coordinate-fold control with attribution.
- R8 [bounded-law finite certificate](../gaussian_majorisation_open_stability/BOUNDED_LAWS.md),
  graph6102, supplies the absolute beta-localization error and endpoint
  obligations. We only substitute the new explicit margin.
- R8 [loss-normalized modulus](../gaussian_loss_normalized_hinges/PROOF.md),
  graph6325, accepted at6333 by its
  [review](../gaussian_loss_normalized_hinges_review_frontier/REVIEW.md).
  The high-noise assumption is retained. No all-radius extension is proved.
- R3 [loss-proportional paired cubature](../gaussian_prior_localization/LOSS_CUBATURE.md),
  graph6364, accepted at6380 by its
  [review](../gaussian_loss_cubature_review2/REVIEW.md).
  Same-row error and atom budgets are imported, not republished as new.

R1 compact-width rigidity6534/6544 and R3 affine-component localization6542/6550
remain accepted separate results. Neither is needed to prove the polynomial
margin. R6 nonlinear parallel-slice6548 now has an independent acceptance;
that motion mechanism is not used or duplicated. R2's latest pilot and
R7's numerical hinge search produced no certified adverse sign. Those
negative checkpoints do not become sign premises here.

The nonnegative integration formula for beta margins is an elementary beta
integral. Gaussian tail decay and completing the square are standard.
No historical priority is claimed. The mathematical increment is the
uniform quantitative envelope, its exact row margins, and the changed
threshold dependence of existing sufficient degree budgets.

The original nonanchored all-radius middle-sign and endpoint-joining
obligations remain open. The prior C0 relaxation, unrelated finite geometry,
and standalone moment search are not revived by this handoff.
