# Sources, dependencies and scope

The single problem source is Aishwarya--Li,
[Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture,
arXiv2609.07041v2](https://arxiv.org/html/2609.07041v2), checked live on
27 September 2026. The unrestricted bounded-law R3 majorisation question
is not resolved by this packet. Its continuous-contraction result and
replica identities are prior work.

## Analytic dependencies and existing obstructions

- [Retained replica interaction](../gaussian_replica_interaction/PROOF.md),
  original6362 `bafkreicp5fr5uoquxbrunjvq7idskx5rg47hsxedl4qnastmppakpngaba`,
  source `49a7d4c0828418b342e209b91c8753173a51ed3b`, fixes the marked
  B_m normalization and the elementary iid-replica expansion. Its author
  proof of the power hierarchy and two beta signs remains separately
  review-pending. Those sign certificates are not premises here.
- [Hankel criterion](../gaussian_majorisation_hankel_transport/PROOF.md),
  original5962 `bafkreids462diitdof5ijilzcq2xqwftk2bzjr5t2gihnxk327uezbndbm`,
  gives the full endpoint hierarchy. Its first block identifies the
  still-missing constant (8/9)^(5/2). The current argument rederives every
  B_m inequality it uses; it does not re-prove or claim that full criterion.
- [Averaged replica curvature](../gaussian_replica_curvature_sparse_energies/PROOF.md)
  already used the exact two-added-replica quadratic identity and a
  radius-dependent loss. Here the improvement is universal in the radius
  and all other input scales, but its non-effective constant is weaker than
  the full-sign threshold. No favorable parameter range is newly advertised.
- [Instantaneous lift obstruction](../gaussian_majorisation_local_lift_obstruction/PROOF.md),
  original5980 `bafkreifseyjs3jimzu7yvo3lpfd3555dmnf5q6hraqdonaldti3nqjgxqy`,
  and [conditional kernel boundary](../gaussian_conditional_kernel_obstruction/PROOF.md),
  original6267 `bafkreicivyxiwogu64smlmuc3b2enfxmu7duowy7nr44yw5yzzeaeeutla`,
  prohibit the indicated pointwise substitutions. The present theorem
  is compatible with both: it uses the actual time law and does not
  posit a positive rank-five kernel at each time or tuple.

Gaussian completion gives the classical Mehler identity explicitly in the
proof; it is not claimed as new. Levy's continuity theorem, Portmanteau,
Arzela--Ascoli, Fubini, and Kirszbraun extension are the standard mathematical
tools in the written compactness argument. No numerical value of its
separation constant is assumed, computed or independently certified.

## Current team results and ownership

These are context rather than premises of the universal averaged gap.
Their restrictions are not silently inserted or removed:

- [R3 loss-moment guard](../gaussian_loss_moment_middle/PROOF.md),6408,
  `bafkreig4z2sgxtkwwalum5gjmqxrga4lmvqlbok767ejxj2ler6tzvdqwi`, is
  independently accepted6420. It gives a uniform middle sign under radius,
  covariance and second-to-first loss-moment conditions. The clock law in
  this packet alone supplies none of those complete conditions.
- [R8 mean-loss margin](../gaussian_mean_loss_margin/PROOF.md),6414,
  `bafkreie5iago7b2rtbm5oyabb3fshfabujmwms37a3vsojzo7efsgfybey`, is
  independently accepted6422. Its cutoff is uniform over fixed radius,
  covariance-floor and bounded-volume families, but non-effective. We do
  not duplicate or invoke its functional zero-loss argument.
- The publication refresh also read R3's
  [effective mean-loss theorem](../gaussian_effective_mean_loss/PROOF.md),6426,
  `bafkreieyattiaogc4s7iosnunxfq3yi6sy2enhq23ftgtoua7fz22zb6ni`, and R8's
  [alternative quantitative polarization](../gaussian_mean_loss_margin/EFFECTIVE.md),6428.
  They now supply explicit cutoffs for that same restricted family; R3's
  source has independent correctness acceptance. Radius, positive covariance
  and threshold/volume bounds remain. Their effective cutoffs neither compute
  e_graph here nor prove the unrestricted replica sign. They are credited
  as advances of the certification lane, not premises of this proof.
- [R2 logarithmic-noise theorem](../gaussian_logarithmic_noise_certificate/PROOF.md),6412,
  `bafkreia6dvwc2yn44kb2vxsikmdtuvc4ypnoksq7tqqfzgnhtyfqj5gqye`, signs
  finite-degree polynomial cones at sufficient variance. It does not turn
  the present non-effective gain into an all-degree or first-Hankel sign.
- [R6 angular-ray theorem](../gaussian_angular_ray_contractions/PROOF.md),6402,
  `bafkreidy6wjmsnzoenmqqwo4kos36fwuvpj65gq5iioqownidek64axyaa`, is
  accepted6410/6416. The separate
  [convex normal-bundle extension](../gaussian_angular_ray_contractions/NORMAL_BUNDLES.md)
  is separately accepted6424, with its own whole-normal-ray hypotheses.
  Those full Gaussian/KP
  geometric classes are preserved; they are not consequences of this packet.

R1's actual-contact frontier, R4's deformation/averaging route and R7's
asymmetric search were inspected through their latest completed reports.
No contact sign, adversarial witness or new map class is asserted here.
This is the analytic lane's averaged mechanism, not an internal review or
a synthesis contribution. Targeted primary-literature searches did not
provide the claimed averaged gap as an imported result; historical priority
remains unassessed rather than guaranteed.

The graph contribution accompanying this packet records the verified source
commit separately and points to these reader-facing main-branch files.
