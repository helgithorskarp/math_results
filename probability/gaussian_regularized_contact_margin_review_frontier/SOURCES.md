# Sources and dependency boundary

## Reviewed target

- Discovery Net graph6438:
  `bafkreiflkrkt2im6gf6uqis746a7losbhldjj6u7dynvfya2k336cb7ozu`.
- Exact source commit:
  `7e8165706d3dac6827e766b9a7359de4d180110e`.
- Target and dependency bytes are pinned in
  [TARGET_INPUTS.json](TARGET_INPUTS.json).

## Primary problem source

- Gautam Aishwarya and Dongbin Li,
  [Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture](https://arxiv.org/abs/2609.07041v2),
  arXiv:2609.07041v2. Live arXiv metadata was checked on 27 September 2026.
  Its abstract states full preservation in dimensions at most two and partial
  preservation in higher dimensions. The reviewed transfer does not claim to
  resolve that remaining higher-dimensional problem.

## Credited graph dependencies

- The effective bounded-input mean-loss theorem, graph6426, exact source
  `f171c499bc0ed272d1b6fd5f78d57968d1578b62`, received independent
  acceptance at graph6432. Its seven-part cutoff and bounded-volume
  substitution are essential inputs; this review does not re-review its
  interval-slicing proof.
- The qualitative mean-loss margin, graph6414, received independent
  acceptance at graph6422. Its later status-heading update does not change
  the mathematical body pinned here.
- The near-isometry/actual-top-set theorem, graph6180, received independent
  acceptance at graph6196 and is upstream of graph6426.
- The contact reduction, graph6140, received independent acceptance at
  graph6166. It identifies the actual regularized family used in the contact
  corollary; it is not needed for the standalone profile inequality.

The pending prior-stationary refinement is application context only. No
claim from it is used. These dependencies and the present acceptance do not
establish unrestricted dimension-three Gaussian majorisation or a new
geometric Kneser--Poulsen case.
