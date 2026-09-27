# Attribution, provenance and the precise dependency boundary

The sole problem source is Gautam Aishwarya and Dongbin Li,
[*Gaussian Convolution, Internal Energies, and the Kneser--Poulsen
Conjecture*, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2),
refreshed on 27 September 2026. Their Conjecture 1.1 is the unrestricted
target. Their pressure hierarchy and Theorem 1.3 give the dimension-three
PC2 comparison. For curvature p=U'', the smooth PC2 condition becomes
(u^2 p(u))'>=0. We check that same cone for our abstract model; we do not
reprove or extend their Gaussian theorem.

The construction is self-contained once the scalar normalization is stated.
Laplace transforms, half integration, integration by parts, log-convexity,
Taylor bounds and beta concentration are standard tools. None of those
tools or the classical complete-moment criterion is claimed as new. The
claimed contribution is the simultaneous parametric countermodel to the
listed scalar constraints. Historical novelty has not been independently
established; the proof itself also awaits independent review.

The relevant durable sources are:

| Source | Role |
| --- | --- |
| [Global criterion6088](../gaussian_majorisation_global_criterion/PROOF.md), `bafkreihp3see622wt3h2fxowhnp6cj4jtz5t53dxp5bmerz7aj5tfo2eeq` | Fixes H, the normalized beta averages and their equivalence to the global coupling sign. We use the same definitions; no new coupling equivalence is claimed. |
| [Retained interaction6362](../gaussian_replica_interaction/PROOF.md), `bafkreicp5fr5uoquxbrunjvq7idskx5rg47hsxedl4qnastmppakpngaba` | Supplies the positive common lift and the all-m,all-ell inequalities being tested. They remain valid for actual replicas. |
| [Complete beta rows through12, original6476](../gaussian_complete_beta_row_eleven/MULTILEVEL.md), `bafkreicc53nkopfdrq5gi6ww4vnqlfagsgkskzbqlsavujucvi5f7x6hzy` | Uses nonnegative combinations of the retained inequalities through multilevel Young minorants. The new model obeys all those premises and preserves every q<=K at every index, for arbitrary finite K>=12. |
| [Independent acceptance6484](../gaussian_complete_beta_row_twelve_review2/REVIEW.md), `bafkreidahoadzotldu3qozitcptpruedrpz55awvddpqqanod45vb3hdta` | Independently accepts both the row theorem and full retained-interaction dependency. It is not a review of this new construction. |
| [Conditional-kernel obstruction6267](../gaussian_conditional_kernel_obstruction/PROOF.md), `bafkreicivyxiwogu64smlmuc3b2enfxmu7duowy7nr44yw5yzzeaeeutla` | Earlier failure of sufficient pointwise kernels at rank six. The present obstruction instead concerns one regular scalar profile satisfying infinitely many averaged constraints simultaneously. It does not infer a negative actual hinge from that earlier kernel failure. |
| [Averaged rank gap6436](../gaussian_averaged_replica_rank_gap/PROOF.md), `bafkreigqhx3wp5rxeobajbaohsyitdjtmmxstmfovnrh4iradqfwrlvdoi` | Its scalar consequence B2 B4>=(8/9)^3(1+eta)B3^2 is also satisfied here: strict log-convexity gives the stronger coefficient1, and its specified eta<=5/2808 makes the displayed coefficient less than1. No realization of its conditional diamond law or graph clock is asserted. |

The [input pins](INPUTS.json) give exact source commits and content hashes.
They are provenance, not external inputs needed by the new checker.
The [peak-pruning theorem](../gaussian_beta_peak_pruning/PROOF.md) already
signs a linear region whose aperture depends on a strict peak bound. We
do not rule out that statement, a data-dependent aperture, or a sublinear
region: the obstruction concerns a universal fixed c>0 without such data.

Publication refresh also inspected all seven other completed researcher
reports and the committed graph through6531. No matching scalar-family
construction was found in that bounded neighborhood. The latest sources
contain an author [compact mean-width rigidity theorem](../gaussian_compact_width_rigidity/PROOF.md)
giving eventual Gaussian majorisation for every bounded contraction, and an
author [fixed-variance neighborhood theorem](../gaussian_fixed_variance_neighborhoods/PROOF.md).
Those newly published extensions were not yet independently accepted at
this refresh. The norm-preserving all-variance result now has
[independent acceptance6522](../gaussian_norm_preserving_majorisation_review2/REVIEW.md),
and the support-cap result has
[independent acceptance6528](../gaussian_support_cap_localization_review2/REVIEW.md).
The geometric screw/meridian classifications and obstruction were also
inspected. None is a premise, consequence or counterexample of this scalar
construction. No variance-dependent Gaussian family is supplied here, so
there is no conflict with an eventual-variance theorem for actual inputs.

The remaining constructive obligation is precise: a uniform growing beta
wedge or the unrestricted coupling sign needs an averaged constraint or
Gaussian/replica realizability property that excludes this family. This
does not claim that the known premises cannot sign one further fixed
diagonal, and it is not a reason to infer failure of the headline conjecture.
No new Kneser--Poulsen consequence is asserted.
