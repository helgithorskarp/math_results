# Attribution, dependencies and scope

Primary literature was checked live on27 September 2026.

1. Gautam Aishwarya and Dongbin Li,
   [Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture](https://arxiv.org/html/2609.07041v2),
   arXiv2609.07041v2. Conjecture 1.1 is the sole problem source. Theorem 1.3
   gives the pressure-class comparison, and the full convex-energy
   comparison is known in dimensions at most two. We study the bounded-law
   dimension-three question. No all-variance sign is inferred from a
   fixed-variance approximation.
2. Feilong Cao and Xiaofei Guo,
   [Approximation by Jackson-type operator on the sphere](https://hrcak.srce.hr/en/61810),
   Mathematical Communications15(2),331--346(2010),
   [publisher PDF](https://hrcak.srce.hr/en/file/92590), Section 2.
   The positive sine-power Jackson kernel, zonal spherical operators and
   Legendre multipliers are classical. Our proof rederives the particular
   first-moment constant6/p and rational normalization needed here. We do
   not claim a new Jackson approximation theorem. Legendre orthogonality,
   its addition formula, and the standard bound |P_j(t)|<=1 on[-1,1]
   are also classical. The rational bound pi<22/7 is used only for the
   optional improved kernel cost.

Analytic dependencies:

- [Loss-dependent hinge modulus](../gaussian_loss_normalized_hinges/PROOF.md),
  original 6325 `bafkreif2b3e5sw6dumihujzhpul4uce3p7v4elvfpyz77miocxodmytq24`,
  source `a68810063b8ad53dda046c68552a14e76f8d3f07`;
  [accepting review](../gaussian_loss_normalized_hinges_review_frontier/REVIEW.md),
  original 6333 `bafkreieyqbx7j34qcop5tdz46qgtub5jcvo3rz3cxzdc6d4uspcshm6uo4`.
  Its Theorem 2 and equation7 supply the relative angular derivative bound.
  Its epsilon<=1/2 restriction is retained. The all-radius absolute
  angular estimate in the present proof does not use this dependency.
- [R3 paired loss-proportional cubature](../gaussian_prior_localization/LOSS_CUBATURE.md),
  original 6364 `bafkreicuyedmct5zhkt5cxba2nkvgel3tkursxckgxcryd45ed53khps5e`,
  source `afacddeb257993b31ee118ff92e7360a7870cbc6`;
  [independent acceptance](../gaussian_loss_cubature_review2/REVIEW.md),
  original 6380 `bafkreia62tjvdimerupjq35kmi27cdxsknhqy4sg6bzhoiuatovvrwdluu`,
  review source `99d165ea308026e7c3241f90ac2fe984cc16fec9`.
  Common cubature, exact loss preservation and
  the signed moment remainder are premises, not new claims here.
  Provenance detail: graph6380 prints a different full review-source SHA;
  the SHA above is copied from fresh repository resolution and identifies
  the linked review actually inspected. This is not a mathematical objection.
- [The global hinge criterion](../gaussian_majorisation_global_criterion/PROOF.md)
  and [exact Hankel/replica identities](../gaussian_majorisation_hankel_transport/PROOF.md).
  Global criterion 6088 is `bafkreihp3see622wt3h2fxowhnp6cj4jtz5t53dxp5bmerz7aj5tfo2eeq`;
  the cited proof file is preserved at source
  `713e542a0bd389681a3fb4ee0c0b61a4f272f104`.
  These define the ordinary moments and the preceding Bernstein--Durrmeyer
  rate. We replace the reconstruction operator, preserving those moments.

Context, not proof premises:

- R2's [extended-target prior certificate](../gaussian_extended_target_prior_cell/PROOF.md),
  source `4e006ae51713af09a45229d9df59341a6f4fd03c`, is a new actually signed fixed-variance prior simplex,
  pending independent review. Its extended target and signed endpoints
  are not replaced or assumed by our moment formulas.
- The [loss-relative spherical transfer](../gaussian_relative_spherical_transfer/PROOF.md),
  original 6376 `bafkreibblggn3ysibhslp7rdh5websr6jdcaiduc4omw4p5ud7uul45hsi`,
  now has [independent acceptance](../gaussian_relative_spherical_transfer_review_frontier/REVIEW.md),
  original 6384 `bafkreihrc6hyp2ot7hc2hlzl65awvvlgngxflhpukbwdjewzmbbya7ejde`.
  It still requires an actual spherical margin and overlapping signed tail.
  It is preserved, but the new proof does not rely on it.
- R7's [all-finite low-noise degree exclusion](../gaussian_atomic_low_noise_exclusion/PROOF.md),
  original 6386, is a search restriction, now
  [independently accepted](../gaussian_atomic_low_noise_review_frontier/REVIEW.md).
  No fixed finite
  polynomial degree is asserted sufficient for all small variances here.

All universal reasoning remains written mathematics. Exact finite controls
are corroboration and reusable code, not independent peer review or a
proof-assistant formalization. There is no unknown solver result, large
certificate, private data dependency or external numerical library.
