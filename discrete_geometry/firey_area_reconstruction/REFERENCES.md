# Sources and attribution

Primary-source audit: 2026-09-21. These are selected relevant sources, not an
exhaustive bibliographic search. The proposed Firey-germ and sharp finite-jet
statements are new to these searched sources; historical priority is unestablished.

1. [Reviewed planar Firey area transform](https://github.com/helgithorskarp/math_results/blob/main/discrete_geometry/firey_planar_sharp_stability/PROOF.md),
   Section 2, equation (6), and its p=2 specialization at the end of Section 6.
   Source commit 32ba5b7f9a8a2d1273767ae958afd49549d67ba4.
   [Independent review packet](https://github.com/helgithorskarp/math_results/tree/main/discrete_geometry/firey_planar_sharp_stability_review1),
   source commit 9e0113dde56637773ba882c4e8548b0b89ce15e8.
   This is the actual external mathematical dependency. The sharp stability
   inequality and equality classification are prior graph results, not new here.
2. Fradelizi, Manui, Meyer and Ndiaye,
   [L_p-Rogers–Shephard type inequalities for L_p-zonoids and symmetric bodies](https://arxiv.org/html/2607.03582v1).
   Corollary 29 and Conjecture 5 supply the original planar symmetric Firey
   context. The graph subsequently settled that equality problem. This paper
   is not cited as posing the inverse problem studied here.
3. Lutwak, Yang and Zhang,
   [L_p affine isoperimetric inequalities](https://math.nyu.edu/~yangd/papers/jdg00.pdf),
   Journal of Differential Geometry 56 (2000), 111–132. The L_p surface area
   measure and L_p projection-body definitions identify the coefficient
   integrals with established geometric data. The L_p mixed-volume inequality
   and equality condition are classical inputs to the one-term corollary.
4. Ryabogin and Zvavitch,
   [The Fourier transform and Firey projections of convex bodies](https://www.math.kent.edu/~zvavitch/Fourier-Firey.pdf).
   Equation (4), Section 2, Theorem 3 and its following remark distinguish
   uniqueness at non-even p from failures for general bodies at even p.
   The remark cites Lutwak's L_p surface-area uniqueness theorem. Our
   finite-facet support argument avoids the even-p cosine-transform kernel
   for the specific polygon input; it does not assert general even-p injectivity.
5. Kousholt,
   [Reconstruction of n-dimensional convex bodies from surface tensors](https://arxiv.org/pdf/1606.08240),
   especially Lemma 3.1 and Theorem 3.2. This gives established finite-moment
   determination for polytopes, by nonnegative polynomials, and sharpness
   examples using regular polygons. Our data are moments of a measure on the
   polar boundary, not her ordinary surface-area measure on the unit sphere.
   We credit the positive-polynomial and rotational-cancellation mechanisms.
6. Gravin, Lasserre, Pasechnik and Robins,
   [The inverse moment problem for convex polytopes](https://arxiv.org/abs/1106.5723),
   Discrete & Computational Geometry 48 (2012), 596–621.
   The article reconstructs polytopes from axial volume moments using
   Prony/Vandermonde methods. Finite moment inversion and annihilating
   polynomials are established methods, not inventions of this packet.

Search scope included Firey sums of translates, translation area and volume
determination, Firey reconstruction, L_p covariograms, even-p projection
uniqueness, surface-tensor reconstruction, and polytope moment inversion.
The claimed contribution is the exact inverse interpretation of one local
scalar area function, its gauge/radius formula, and sharp finite-jet
reconstruction and facet detection. It is not a claim that all geometric
moment reconstruction is new, nor that these inverse questions were named
open problems in the cited papers.

## Discovery Net provenance

- Original planar Firey problem:
  `bafkreicafoo54mtx6wfmjncrewegqdpo33tub57irza46bsq2cfpvfvbgy`.
- Transform and sharp stability:
  `bafkreibhh7hqrbwd3iqzmhvlhu45v7j356h5ac775ayjj7mw2hpcpu7raa`.
- Independent transform/stability review:
  `bafkreihaw7w4fp2o2vsibazqdhhrkniugtbn5clz3dleigv3tndybyv2h4`.

The current contribution is a named structural inverse-geometric consequence
of that reviewed transform. No old source or graph result is resubmitted.
