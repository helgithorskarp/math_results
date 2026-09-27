# Attribution and scope

Primary sources inspected live on 27 September 2026:

- Gautam Aishwarya and Dongbin Li, [Gaussian Convolution, Internal Energies,
  and the Kneser--Poulsen Conjecture, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
  Theorem 1.4 transfers a continuous contraction to Gaussian internal-energy
  comparisons. The unrestricted dimension-three question is the campaign
  target; that theorem does not by itself construct the motion used here.
- K. Bezdek and R. Connelly, [Pushing disks apart — The Kneser--Poulsen
  conjecture in the plane, arXiv:math/0108098](https://arxiv.org/abs/math/0108098).
  Its continuous-motion/lifting framework supplies the classical
  arbitrary-radius ball comparisons. Our analytic R3 motion is within
  that framework. Those comparison theorems are not new claims here.

The following team dependencies and comparisons were inspected as source.
[`INPUTS.json`](INPUTS.json) pins the seven proof/review files used by the
finite audit. GitHub links below use the main-branch paths; exact source
commits are recorded separately.

- Accepted R1 [weighted Gram alignment](../gaussian_contraction_rigidity/PROOF.md),
  with [independent acceptance](../gaussian_contraction_rigidity_review1/REVIEW.md).
  Original graph `bafkreiheirbfdiqq4igulat36rylgtda5zd2jc2ksdrif3qildy7ulnvy4`;
  accepting review5633 `bafkreibmhq6cg4rwvr2g5dbegsx47pglj4njuv6gjv3rp6tekly2lxe6ru`.
  Repository file commit `33bb5788b6ecf84a706fbd3eea99cf336f23e25b`.
  Its Hilbert-space identity provides `E<=2F/k`. It already applies to
  general probability laws; no novelty is claimed for this extension.
- R4 [rigid-block certificate](../gaussian_rigid_block_certificate/PROOF.md),
  graph6516 `bafkreiam5urhnlvjcbcmttngtjwwuqkvj3ol5mfdy7vqimkbfujdqvv6ca`,
  source `411c088f7b9c6e06c1a05fc11548eab9e2119d63`.
  [First](../gaussian_rigid_block_certificate_review/REVIEW.md) and
  [second](../gaussian_rigid_block_certificate_review2/REVIEW.md) accepting
  reviews were read before publication. Their source commits are
  `589366adace0fc9b1f97c8667bc618c7369cd6ec` and
  `0d57bcadb6a91fc25760a898817f44b5f23828b3`, respectively.
  The rotation-logarithm, acceleration and Green-kernel mechanism is credited
  here. The new ingredient is support-wide affine control from conditional
  covariance, followed by a polar path with compression. Our full-rank
  theorem does not subsume the lower-dimensional rigid-block cases.
- R2 [balanced finite loss](../gaussian_balanced_loss_certificate/PROOF.md),
  source `91c63ff5a464f725ea6bee38290e56df594f1c60`, graph6504
  `bafkreihaxhapv7kvng2yatxu2unok44m3v3vxwvp47mdgxkfvuqlxvzmgy`.
  This is prior all-variance small-loss control for the finite frontier.
- R8 [norm-preserving comparison](../gaussian_norm_preserving_majorisation/PROOF.md),
  source `7ec05f2b89b4ab69de7a6696f236aa1f6ecc3ffc`, graph6510
  `bafkreiekpjods6d64zl5bjtziqfwgrxy5fhqvw237vqiepknp5g7yotwte`,
  and R6 [affine-slice contractions](../gaussian_affine_slice_contractions/PROOF.md),
  source `9c1feb8cf43d8726c7fddc540dd6a8b143749f47`, graph6514
  `bafkreia4ivwxrdzlhqa6ywpddshfzqk5p6s2n7fzz67tqedsnnfk7uq6xa`.
  These are complementary full-domain hypotheses, not inferred from matching
  finitely many Gaussian moments or a sampled cloud.
- R3 [support-cap localization](../gaussian_support_cap_localization/PROOF.md),
  source `6eeb8a1d66bbbae6a998f814ba646bea9d2039d7`, graph6520
  `bafkreiaw7nlu2jooneqkbw4pbujsxgzrosyjclqjfkbfk2acv3vbm3tn3i`,
  with [accepting review](../gaussian_support_cap_localization_review2/REVIEW.md),
  review source `71e6e17b987f6159d6d947aa1cd1edba5030fba1`.
  Its eventual all-threshold conclusion is distinct from the present
  all-variance support certificate.

Recent context, not premises: R1's
[compact-width rigidity](../gaussian_compact_width_rigidity/HANDOFF.md),
source `5d223e88146a2810294533718b1eaa3bb114b9a8`, claims a universal eventual
comparison; R8's [fixed-variance neighborhoods](../gaussian_fixed_variance_neighborhoods/README.md),
source `d244f4dce12434d9bde1dc8558a5a4608c7dd1f3`, allows spatial and prior
perturbations at a chosen scale. Neither is used in this proof. Their
acceptance status must be tracked separately from this author claim.

No historical-priority theorem is asserted. The new quantitative guard and
its full-domain consumer are the proposed contribution. Conventional real
analysis and the cited motion transfers remain outside the exact checker;
the checker is not independent peer acceptance or a proof-assistant theorem.
