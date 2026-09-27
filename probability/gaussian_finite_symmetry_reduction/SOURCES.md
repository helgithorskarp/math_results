# Sources, attribution and dependency boundaries

The sole headline source is Aishwarya--Li,
[Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
Its Conjecture 1.1 and discussion of convex energies specify the full
majorisation question. The present reduction does not prove that
conjecture or claim a new Kneser--Poulsen consequence.

The ingredients of the proof are elementary group averaging, the usual
Kirszbraun extension theorem, Gaussian Chernoff bounds and L1 continuity
of Gaussian translations. They are not claimed as new. The primary text
was consulted live at pass entry. Bounded literature searches did not
locate this precise finite-symmetry defect equality; this is not a
historical-priority certificate.

Relevant earlier team source:

1. [Fixed-atom reduction](../gaussian_majorisation_global_criterion/ANCHOR_REDUCTION.md),
   source `138993ba3ec2efde720c789a2a3d887c9c417c69`.
   It already proves a separated-mixture transfer uniform in threshold,
   with a fixed rare mass multiplying the defect. The present proof
   credits and reuses that elementary mechanism. All copies here carry
   the same endpoint comparison, so their defects sum without a rare-mass
   factor; equivariance and strict cross-block contractivity are new
   obligations. No new Gaussian proximity or entropy claim is made.
2. [Reflection-group alignment](../gaussian_coxeter_alignment/PROOF.md),
   source `dd18e51215c5ef5b5450ef457c750574c1fe6456`.
   It signs alignment of the two oriented halves, including arbitrary
   orbit masses and representatives. Its Section 5 explicitly leaves
   arbitrary contractions of invariant laws unresolved. We do not extend
   its positive kernel, rerun its checker or claim arbitrary orbit
   contraction from its alignment premise.
3. [Two-body contact transfer](../gaussian_two_body_contact_transfer/PROOF.md),
   source `036e7355fd2481a562ece50be4cbab5889f41c25`.
   Its asymmetric eight-site fixture is reused solely for exact geometry
   controls. No adverse datum was supplied there or here. The two-body
   equivalence is not an analytic premise of this proof.
4. [All-radius loss localization](../gaussian_all_radius_loss_localization/README.md),
   source `1104fcce0bfcf2d9cb16f70daa45c361f54c977c`, author-pending6576.
   Its actual covariance guard motivates stating (7a) explicitly. It is
   not a premise of the symmetry reduction, and no competing cubature
   is built. The new compact Cov=I, radius-2 normalization gives no
   lower variance bound or unknown Gaussian sign.

These source files are pinned in INPUT.json. The analytic proof here is
self-contained except for the classical global extension theorem. The
finite/rational approximation argument is supplied directly; effective
localization budgets from the measure-side lane are not silently imported.

At entry through graph 6573, the prior two-body transfer6570 had no incoming
feedback. The new motion-chain strict-margin6572 is author-pending and
retains its supplied-motion/common-radius premises; it does not sign an
arbitrary representative block. Accepted compact-width, cubic-beta and
strict-screw results retain their scopes. No teammate implementation,
unpublished numerical search or reviewer verdict is an assumption.

Before publication the two-body transfer received independent acceptance
at6574, [review](../gaussian_two_body_contact_transfer_review2/REVIEW.md),
source `cdfe4d311485012c5d3cc9f3d2fb0a50005a6caf`. Its conditional scope
and absence of an adverse datum were retained. No previous packet was
modified. The all-radius localization6576 and new completed R3/R5/R6
reports were also read; none contained this finite-symmetry reduction.

Claim status: complete author proof pending independent review, with
finite exact consistency controls. The checker is not a formalization
and is not evidence that a Gaussian counterexample exists. Full R3
majorisation and the sign on the reduced class remain open.
