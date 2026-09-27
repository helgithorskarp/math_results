# Dependencies, credit, and evidence

The target is Aishwarya--Li's unrestricted Gaussian-convolution
majorisation conjecture in dimension three:
https://arxiv.org/html/2609.07041v2 . The primary statement was refreshed
on 27 September 2026. A targeted literature search did not establish any
priority claim for this corollary; no historical novelty claim is made.

The new step here is a quantitative Gaussian-increment truncation that
preserves covariance and a definite fraction of the original pair loss,
while its profile error retains the volume factor. This permits an
explicit application of the following bounded theorem to the actual
unbounded regularized contact inputs.

1. R3, effective bounded-input mean-loss margin, source
   `f171c499bc0ed272d1b6fd5f78d57968d1578b62`, graph6426,
   `bafkreieyattiaogc4s7iosnunxfq3yi6sy2enhq23ftgtoua7fz22zb6ni`.
   [Proof](../gaussian_effective_mean_loss/PROOF.md).
   Its seven-part cutoff and bounded-volume substitution are essential
   mathematical inputs. It received independent acceptance at graph6432
   during the prepublication refresh, review source
   `6ebac9c96dcf201db531c08abe180644958191b9`, artifact
   `bafkreififbypnz6a7duxi3g75relsg4g2oexl22hbgeh4xk6wkebaxqxvq`.
   [Review](../gaussian_effective_mean_loss_review_r4/REVIEW.md).
   Its full proof and review were read; the review does not cover our transfer.
2. R8, mean-loss margin, source
   `888c64db59feccd280575061612804854b0f658c`, graph6414, accepted6422.
   [Proof](../gaussian_mean_loss_margin/PROOF.md).
   R3 explicitly credits its core/rare and conditional-alignment method.
   Its qualitative compactness theorem alone would not supply the
   growing-radius cutoff needed here; this packet does not reprove it.
3. R1, accepted near-isometry/contact theorem, graph6180/accept6196.
   [Proof](../gaussian_contact_near_isometries/PROOF.md).
   Its actual-top-set first variation and Procrustes estimates are upstream
   inputs to R3/R8. Section 6 expressly left a tail budget to be checked
   for the unbounded auxiliary law. The current transfer discharges that
   budget in its stated regime using mean loss, without a displacement
   condition. It does not supersede the other parts of that theorem.
4. R1, accepted contact reduction, source
   `1d1f1c6e58ceb3010e05dcbe5fc477f4c7edde6f`, graph6140/accept6166.
   [Source](../gaussian_majorisation_heat_profiles/CONTACT_REDUCTION.md).
   This identifies the actual family to which the conclusion is applied;
   the profile comparison itself does not assume the existence of a contact.
5. R1, prior-stationary/Brownian refinement, source
   `4e1899ea00cd49e86c365604e2b4cbbe2016fbfb`, graph6323, pending review.
   [Source](../gaussian_prior_stationary_contacts/PROOF.md).
   This is application context only. Neither its additional stationarity
   nor its event bounds is needed to prove the present inequality.

`INPUTS.json` pins the actual written inputs used. R8 added a heading/status
notice to its accepted PROOF.md in
`9117b9b64127df8ee18337d9205e4aa7a9b70960`; its mathematical body is unchanged.
We inspected that diff and pin the new notice-bearing version for this replay.
R3's own original checker requires the older dependency bytes from its exact
reviewed commit; this source-version issue does not change its theorem.
The R1 accepted and pending packets are unchanged. The R2 certification work, R4 parity class, R5
interpolation coupling, R6 normal-bundle class and R7 counterexample searches
retain separate ownership; no computation from those lanes is duplicated.

`verify.py` uses standard-library CPython integers and Fractions. It checks:
the two chi-square numerical bounds; universal affine exponent certificates
on q>=8; the initial schedule and dyadic induction base; finite probability
identities for latent-noise conditioning and retained pair loss; scaling;
and rejection of damaged exponent budgets and missing loss retention.
The finite probability controls are not Gaussian quadrature. The Gaussian
moment-generating function, probability inequalities, profile comparison,
and the upstream bounded theorem remain written mathematical inputs.
No sampled signs, floating-point thresholds, external solver, proof
assistant, hidden large certificate, or independent reviewer is claimed.
