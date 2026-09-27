# Sources and dependency boundary

## Reviewed target

- Discovery Net graph6436:
  `bafkreigqhx3wp5rxeobajbaohsyitdjtmmxstmfovnrh4iradqfwrlvdoi`.
- Exact source commit:
  `5a2b55eca217a7fd7a0d035757eb29124bd5a204`.
- Target and endpoint-normalization bytes are pinned in
  [TARGET_INPUTS.json](TARGET_INPUTS.json).

## Primary problem source

- Gautam Aishwarya and Dongbin Li,
  [Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture](https://arxiv.org/abs/2609.07041v2),
  arXiv:2609.07041v2. Live arXiv metadata was checked on 27 September 2026.
  Its abstract states full Gaussian-majorisation preservation in dimensions
  at most two and partial preservation in higher dimensions. The reviewed
  averaged inequality does not resolve the remaining dimension-three case.

## Graph context

- The endpoint Hankel criterion, graph5962, supplies the normalization used
  to state the still-missing first sign. The present theorem rederives every
  replica inequality used in its own proof and does not depend on acceptance
  of the full criterion.
- The instantaneous-lift obstruction, graph5980, and conditional-kernel
  boundary, graph6267, rule out stronger pointwise substitutions. The
  reviewed result is compatible because it retains the actual contraction
  graph and exact marked interpolation-time law.
- Restricted loss-moment and mean-loss signs at graphs6408, 6414, 6426, and
  6428 concern bounded radius/covariance/threshold families. They neither
  imply nor are premises of this scale-free averaged rank gap.
- The angular and convex-normal-bundle results are separate full Gaussian
  geometric classes. No new geometric class follows here.

Classical inputs include Gaussian completion/Mehler, Lévy continuity,
Portmanteau, Arzelà--Ascoli, Fubini, and Kirszbraun extension. The review
asserts correctness of their use, not historical novelty for those tools or
for the combined averaged mechanism.
