# Sources, ownership, and scope

The sole problem source is Gautam Aishwarya and Dongbin Li,
[Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture](https://arxiv.org/html/2609.07041v2),
arXiv:2609.07041v2. The dimension-three question, Gaussian product identity
and PC2 comparison context were refreshed against the primary text during
this pass. We make no historical priority claim for the general use of
Gram matrices, Gaussian coefficient extraction or positive polynomial tests.

The mathematical dependency is R2's
[pair-conditioned beta identity](../gaussian_beta_pair_conditioning/PROOF.md),
source a649ce1267fac02c0e11972a988e545ffab0db79. Its formula(6) reduces the
actual bounded-law beta gap to nonnegative pair loss times a conditional
kernel; its formula(14) supplies the polarized collection. Its q<=6 proof
was independently accepted in
[R8's earlier review](../gaussian_beta_conditioning_review_r8/REVIEW.md).
R5's earlier [centroid-projection proof](../gaussian_beta_projection/PROOF.md)
is also credited; it signs q<=5. The present packet does not repeat either
conditioning or Poisson-offset theorem as its new contribution.

R2's unpublished campaign note `gaussian_pass07/RESEARCH_NOTES.md`, dated
26 September2026, already derived the matching formula L_q and the positive
regular-six-simplex specialization as a large-base asymptotic. Its content
hash is recorded in INPUTS.json for attribution. R6 and R5 also tested the
unsigned kernel without a rigorous negative. The new mathematical steps
here are the exact finite-base recentering/cube-integral bridge and the
two PSD trace certificates proving L_7>=(5/2)_7 for **all** PSD7x7 Grams.
The matching formula and every premise needed to check it are rederived
in this packet; no private note or unpublished numerical search must be
trusted or retrieved to reproduce the proof.

The following durable results locate the theorem. They are context unless
expressly used above; none supplies the missing sign in our proof.

| Source | Relationship and remaining boundary |
| --- | --- |
| R3 [square-root degree budget](../gaussian_prior_localization/SQUARE_ROOT_BUDGET.md) and [direct hinge enclosure](../gaussian_prior_localization/DIRECT_HINGE.md) | Reduce/evaluate the unrestricted compact frontier. Our exact margin signs its q=7 entries, without quadrature or a moment cancellation. Other required entries remain. |
| R2 [peak pruning](../gaussian_beta_peak_pruning/PROOF.md) | A separate growing block at certified density peaks; no peak restriction is needed here. |
| R8 [accepted global-defect review](../gaussian_uniform_defect_review_r8/REVIEW.md) | The universal bound7/50 remains separate; it is not reduced to zero by a finite beta diagonal. |
| R2 [endpoint-scatter obstruction](../gaussian_beta_endpoint_scatter_obstruction/PROOF.md) | Closes a stronger inverse-variance positive-measure representation. Our finite-kernel/Gram proof does not assume that representation. |
| R4 [full orthocentric-flap theorem](../gaussian_flap_selector_motion/PROOF.md), [accepted by R7](../gaussian_flap_selector_review_r7/REVIEW.md) | Every threshold and variance, plus both KP inequalities, on that geometric family. Our theorem is a finite-energy comparison on unrestricted bounded laws. |
| R1 [rigid-hull local theorem](../gaussian_contact_rigid_hulls/PROOF.md) | Full thresholds in a data-dependent neighborhood at fixed weights and variance. No such neighborhood restriction appears here. |
| R8 [previous flap beta certificate](../gaussian_flap_beta_certificate/PROOF.md) | Its sign is covered globally now; its explicit larger pattern margins remain a separate certificate. The old source is preserved. |

The source hashes in INPUTS.json pin the inputs read for this scope audit.
They are not substituted for theorem verification or independent peer review.
The external web search found no source used to import the new Gram
positivity claim. Its finite matrix identities are checked directly here.
