# Dependencies and scope

The named target is Aishwarya--Li,
[Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture](https://arxiv.org/html/2609.07041v2),
arXiv:2609.07041v2, Conjecture 1.1 in dimension three. The primary source was
refreshed live on 27 September 2026. This packet signs a specified measure
cell at variance one and does not settle the conjecture.

R2's [coordinate-cell proof](../gaussian_frontier_middle_cell/PROOF.md),
source `daa4dc44a121df7fd8ed8e34d4769a799018a94d` with anchoring clarification
`d849aef5f3e3c98c0d32d3dd992c7259f19f52cd`, already closes all thresholds for
the prior `(24,22,22,22,22,22,22)/156`. Its public proof was read before
selecting this extension. The coordinate boxes, practical low endpoint,
centered target Taylor estimate, reference lattice, knot-sweep strategy and
rank-six control are inherited or adapted from that result. It now has
[independent acceptance](../gaussian_frontier_middle_cell_review2/REVIEW.md),
source `db41b0d89d8248519d489d893c37f3e9aa55201b`, graph6321. That review
accepts the fixed-prior cell, not this new prior/measure extension. We do
not present this work as an independent review of it.

The new measure-side step is the prior simplex with six lower mass floors,
the source-hinge convexity reduction to its seven vertices, the two vertex
types and their actual finite middle bounds. The target reference is weight
independent. The proof explicitly avoids assuming convexity of a difference
of two weight-dependent hinges. The common low tail is rebuilt from the
mass floors using a concave radial lower envelope, without a fixed prior's
mean bound. Arbitrary diffuse source components and target laws are handled
by uniform Gaussian total-variation estimates.

The absolute [hinge oracle](../gaussian_prior_localization/DIRECT_HINGE.md)
and [scalar code](../gaussian_prior_localization/direct_hinge.py), original
graph6228, have [independent acceptance](../gaussian_direct_hinge_review_frontier/REVIEW.md)
at graph6271, source `90f0acbbba998f8b46829656cce23fe40184d6f3`.
Their nonsmooth quadrature and Gaussian-tail estimates are analytic premises.
This packet pins those exact files and uses their enclosures; it does not
duplicate the review. Both new vertex histograms are compared entrywise to
the unquotiented routine on small grids before the production run.

The [paired-cubature frontier](../gaussian_prior_localization/CUBATURE_FRONTIER.md),
original6212 and independent review6218, supplies the unchanged family
`R^c_1`: `A_1=39,L_1=256,W_1=156`, radius three, matched zero anchor and
squared pair-loss floor `1/256`. We retain all these requirements.
The accepted [general signed endpoints](../gaussian_prior_localization/SIGNED_ENDPOINTS.md)
are preserved. Their very small worst-case cutoff is unnecessary for this
particular cell; no improved general cutoff is claimed.

The [source-cluster defect bound](../gaussian_prior_localization/CLUSTER_DEFECT.md),
source `e8f0528f71f366a945090afa8a1ebb5b160e4825`, graph6305, remains a separate
positive-error certificate, not a premise here. The present result supplies
actual signs with substantial overlap of the Gaussian components. The relative-window
oracle's pending review is also not a premise of this calculation.
The cluster result's tolerance schedule was corrected in
`915d7fe2bf98be309848c472fd4d417ad6206ed4` after two qualified reviews;
the core bound and seven-ball certificate were accepted by both reviewers.

Classical Gaussian translation/Taylor estimates, scalar hinge convexity,
finite-simplex extremality, signed-permutation counts and piecewise-linear
maximization are not claimed as new methods. Qualitative positive
neighborhoods were already available through the team's stability work.
The scoped contribution is a larger explicit parameter region with a
gap-free, checkable sign certificate. No historical-priority, all-variance,
new Kneser--Poulsen, or unrestricted-majorisation claim is made.
