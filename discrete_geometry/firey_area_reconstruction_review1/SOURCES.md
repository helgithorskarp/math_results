# Primary sources and dependency audit

Audit date: 2026-09-21 UTC.

## Direct mathematical dependency

- The target uses the `p=2` specialization of the planar support-area
  transform proved in the previously accepted
  [`firey_planar_sharp_stability`](../firey_planar_sharp_stability/PROOF.md)
  package, source commit
  `32ba5b7f9a8a2d1273767ae958afd49549d67ba4`.
- Its independent accepted review is
  [`firey_planar_sharp_stability_review1`](../firey_planar_sharp_stability_review1/README.md),
  source commit `9e0113dde56637773ba882c4e8548b0b89ce15e8`.
- Discovery Net dependency:
  `bafkreibhh7hqrbwd3iqzmhvlhu45v7j356h5ac775ayjj7mw2hpcpu7raa`.
  Accepted review:
  `bafkreihaw7w4fp2o2vsibazqdhhrkniugtbn5clz3dleigv3tndybyv2h4`.

## Primary literature checked

1. Lutwak, Yang, and Zhang,
   [*L_p affine isoperimetric inequalities*](https://math.nyu.edu/~yangd/papers/jdg00.pdf),
   Journal of Differential Geometry 56 (2000), 111--132. Equation (9)
   states the `L_p` mixed-volume inequality with equality exactly for dilates.
   This is the classical uniqueness input used only after equality of the full
   `L_p` surface-area measures has been established.
2. Ryabogin and Zvavitch,
   [*The Fourier transform and Firey projections of convex bodies*](https://www.math.kent.edu/~zvavitch/Fourier-Firey.pdf).
   Theorem 3 and its following remark separate uniqueness of `S_p` for
   `p != n` from noninjectivity of the even-degree cosine transform. This is
   exactly the distinction respected by the target's finite-support argument.
3. Kousholt,
   [*Reconstruction of n-dimensional convex bodies from surface tensors*](https://arxiv.org/abs/1606.08240),
   especially the finite-moment polytope determination and sharpness results
   in Section 3. These establish nearby moment-reconstruction mechanisms as
   prior art; the target uses a different degree-dependent polar measure.
4. Gravin, Lasserre, Pasechnik, and Robins,
   [*The inverse moment problem for convex polytopes*](https://arxiv.org/abs/1106.5723),
   Discrete & Computational Geometry 48 (2012), 596--621. This documents
   Prony/Vandermonde and annihilating-polynomial reconstruction as established
   methods.
5. Fradelizi, Manui, Meyer, and Ndiaye,
   [*L_p-Rogers--Shephard type inequalities for L_p-zonoids and symmetric bodies*](https://arxiv.org/abs/2607.03582),
   provides the current Firey-sum context. It does not state the inverse germ
   theorem reviewed here.

## Search and priority boundary

Targeted searches covered Firey sums of opposite translates, translation
area/volume determination, local Firey germs and Taylor jets, even-degree
projection uniqueness, surface-tensor reconstruction, and polytope inverse
moments. No matching theorem for this scalar local area germ was found.
This is bounded search-relative evidence, not a historical-priority claim.
