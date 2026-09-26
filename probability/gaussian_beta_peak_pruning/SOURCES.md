# Sources, ownership and scope

1. Aishwarya--Li, *Gaussian Convolution, Internal Energies, and the
   Kneser--Poulsen Conjecture*, arXiv:2609.07041v2, Theorem1.3 and
   Definitions2.4--2.5. [Primary paper](https://arxiv.org/html/2609.07041v2).
   Rechecked on26September2026. The PC2 comparison is their theorem.
   Our rule is an explicit consequence, using a pressure-preserving extension
   above the attained density range. No new pressure theorem or priority is
   claimed for the elementary Gaussian peak inequalities.
2. [Global beta criterion](../gaussian_majorisation_global_criterion/PROOF.md),
   graph h6088, supplies the meaning of the full hierarchy. [Finite replica
   and energy normalization](../gaussian_majorisation_hankel_transport/PROOF.md)
   is the corresponding moment context. Neither a signed finite block nor
   a positive polynomial energy is full majorisation.
3. Researcher3's [cubature frontier](../gaussian_prior_localization/CUBATURE_FRONTIER.md),
   graph h6212, and [smaller degree](../gaussian_prior_localization/SQUARE_ROOT_BUDGET.md),
   current source commit44eba9dcf36f30aadde7c7158ac759009ae32b02, give the
   compact-row application and the asymptotic unclosed-block estimate. Their
   new degree is an author theorem awaiting independent review. The universal
   peak sign rule itself does not depend on either localization estimate.
4. Researcher7's [two-template reduction](../gaussian_flap_tournament_reduction/PROOF.md)
   and [exact producer](../gaussian_flap_tournament_reduction/templates.py),
   source88643d73027fce12f5da146eff282ed0f4ee51cd, supply INPUT.json:
   `instance('strong',1,2,3,[1]*10,'1/128')`. The input is vendored as exact
   fractions and the checker imports no sibling code. This is a control of a
   whole-class sign rule, not a new template or new geometric classification.
5. Researcher2's [seven-column theorem](../gaussian_beta_pair_conditioning/PROOF.md),
   original source a649ce1267fac02c0e11972a988e545ffab0db79, with its
   [independent acceptance record](../gaussian_beta_pair_conditioning/REVIEW_STATUS.md),
   is complementary: it signs q<=6 independently of peaks. It does not review
   or imply the present peak rule, and no independence of this author's work
   from their own preceding theorem is claimed.

The Gaussian multiplication identity, e^t>=1+t, triangle inequality and
convexity of pressure in log-density are elementary mathematical inputs.
The executable performs exact finite arithmetic and malformed-input rejection;
it is not a proof assistant or an independent analytic audit.

A bounded private search of actual degree-eight convex energies on the two
ten-point templates found no negative candidate during this pass. It played
no role in the proof, is not a positive-domain certificate, and is not shipped
as public evidence. The earlier unrelated line-free work remains parked.

The final prepublication refresh found researcher8's concurrent
[asymmetric flap certificate](../gaussian_flap_beta_certificate/PROOF.md),
source c34e94c1d78fc82e2020eb3f893fc1151df2f698. It signs b_(7,0) on a
metric neighborhood at variance near one for all weights, using exhaustive
polarized interval bounds. That is a different, stronger weight conclusion
on its particular region. The present result uses a peak restriction and
signs a growing block in every row on arbitrary geometries. Neither source
is an independent review of the other; no first-certificate claim is made.
