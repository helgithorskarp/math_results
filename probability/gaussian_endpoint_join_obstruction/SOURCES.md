# Dependencies and scope

The sole problem source is Aishwarya--Li,
[arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2), Conjecture 1.1 in
dimension three, refreshed live this pass. The unrestricted problem is open.

R8's [open-stability proof, Section 2](../gaussian_majorisation_open_stability/PROOF.md),
original graph6094, supplies the finite-cluster tail formula at variance one.
The incompatibility uses its displayed schedule, not an assumption that
every cloud conclusion has independent acceptance. The
[first signed-endpoint review](../gaussian_signed_endpoints_review_frontier/REVIEW.md)
and [second review](../gaussian_signed_endpoints_review2/REVIEW.md) explicitly
audit its finite-law specialization without clouds and its constants. The rational-frontier consumer
is R3's [signed-endpoint proof](../gaussian_prior_localization/SIGNED_ENDPOINTS.md),
original6287, accepted at6297 and in the second review. These scoped reviews
do not accept every theorem in the original open-stability directory.

R1's [near-isometry proof, Section 2](../gaussian_contact_near_isometries/PROOF.md)
gives M<=E Delta^2/(2kappa). Its
[independent review](../gaussian_contact_near_isometries_review2/REVIEW.md),
original6196, verifies the operator argument at source
`3abc144c55648e210a7b91bfee213c192da7ab52`. The simpler bound Delta<=4R^2
then gives our budget; the later displacement refinement is not required.

R3's [moving-window proof](../gaussian_small_loss_defect/PROOF.md), original6450,
is now [independently accepted at6460](../gaussian_small_loss_defect_review2/REVIEW.md),
review source `ab547d3237e6d7623b1e70ed8d362c214d6fecc4`. Its flat defect
bound remains an error estimate, not exact zero at fixed positive loss.

R2's [dilated-martingale theorem](../gaussian_dilated_martingale_certificate/PROOF.md),
source `63f42fa6f5173c69391c08b40af53a470663221a`, appeared in the final
refresh. It is an author proof pending acceptance at this note's preparation.
Our Section 3 checks only compatibility of its displayed sufficient variance
schedule, using its Jensen bound; it does not audit its Gaussian premise.

Mean-width monotonicity and strictness are classical; the primary manuscript
[Gorbovickis, Strict Kneser--Poulsen conjecture for large radii](https://arxiv.org/pdf/1006.0531),
Theorems 1.4--1.5, was inspected live. Neither is a new premise here: a
positive supplied mean gap is assumed and bounded ABOVE by displacement.
Support-function continuity, translation invariance and the log-concavity
calculation are elementary known tools. No historical-priority claim is made.

An earlier private R2 team checkpoint already excluded overlap between its
dominant-atom middle schedule and this geometric tail. It is credited as a
route warning, not used as a premise. The present result concerns the different
accepted full-covariance mean-loss schedule and eliminates masses and mean
gaps from a general necessary join test. The exposed-cap proof also rules
out the finite-cluster version for diffuse laws without requiring the
original contraction to respect the cloud labels. The earlier parameter
search is not reopened.

`INPUTS.json` pins exact Git commits and file bytes. The checker reads those
versions with git show, so later header or unrelated main edits do not break
historical reproduction. Source publication and arithmetic checks are not
independent mathematical acceptance of the new obstruction.
