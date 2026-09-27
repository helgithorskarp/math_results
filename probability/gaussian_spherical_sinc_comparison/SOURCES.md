# Sources, dependencies, and scope of novelty

Primary problem source:
[Aishwarya--Li, Gaussian Convolution, Internal Energies, and the
Kneser--Poulsen Conjecture, arXiv:2609.07041v2](https://arxiv.org/abs/2609.07041v2).
The campaign target is its unrestricted dimension-three full-majorisation
question. This contribution does not claim to resolve that question.

The original identity for the three-dimensional spherical mean as the
wave-equation sine propagator is classical Kirchhoff/Duhamel theory.
Section 2 gives a self-contained finite-polynomial proof using the uniform
coordinate distribution on S2 and an elementary beta integral. Historical
priority is not claimed for the divided-difference identity itself.

For the strict finite large-parameter tail we use
[Gorbovickis, Strict Kneser--Poulsen conjecture for large radii,
Theorem 1.5](https://arxiv.org/html/1006.0531v2).
It gives strict convex-point-hull mean-width decrease under a noncongruent
contraction in every dimension at least two. This geometric fact is cited,
not proved or claimed as new here.

For comparison with the arbitrary-radius geometric conclusion, we inspected
[Csikos--Horvath, Two Kneser--Poulsen-type inequalities in planes of constant
curvature, arXiv:1711.03352](https://arxiv.org/abs/1711.03352).
Its Theorem 2.1 concerns convex-hull perimeter for disks of arbitrary radii
in two-dimensional constant-curvature geometries; its introduction also
credits the classical unweighted point-hull mean-width theorem.
Theorem C here concerns mean width of arbitrary-radius ball hulls in R3.
No union-volume or intersection-volume conclusion is asserted.

A bounded search also found Gordon's Gaussian-process comparison papers,
listed on [the author's publication page](https://gordon.net.technion.ac.il/publications/),
including the 1987 elliptically contoured and 1992 Gaussian-majorization
papers. Full texts of those two papers were not obtained in this pass.
Thus this source audit does **not** establish historical priority of
the general submodular spherical comparison or its weighted-width consequence.
The new-to-campaign content is the universal spherical sign and the resulting
unconditional finite eventual endpoint.

## Durable team inputs

Exact source commits and file hashes are in [INPUTS.json](INPUTS.json).

- Spherical-tail reduction, graph 6002:
  [proof](../gaussian_majorisation_spherical_tail/PROOF.md).
  It defines the spherical obstruction and its relation to weighted
  ball-hull comparisons. That reduction is prior work.
- Eventual endpoint, graph 6032:
  [proof](../gaussian_majorisation_eventual_endpoint/PROOF.md).
  We use its Theorem 1 and finite coercive-tail argument.
- Independent endpoint acceptance, graph 6048:
  [review](../gaussian_majorisation_eventual_endpoint_review2/README.md).
  The review also audits the spherical-tail and
  [high-noise-window](../gaussian_majorisation_high_noise_window/PROOF.md)
  analytic dependencies. It does not review our new spherical-sign proof.
- Two-body screw configuration, graph 6472:
  [source](../gaussian_two_body_screw_obstruction/PROOF.md).
  We use only the explicit fixture, whose contraction and paired affine
  rank are independently reconstructed by our exact checker. Its separate
  dimensional-motion obstruction is not a dependency.
- R2 uniform Lipschitz theorem, graph 6486:
  [proof](../gaussian_uniform_lipschitz_certificate/PROOF.md) and
  [independent acceptance](../gaussian_uniform_lipschitz_review/REVIEW.md).
  We reuse and credit its elementary scatter lower bound and endpoint
  constant 4224. The new spherical comparison removes its factor sqrt(27)
  and extends its eventual theorem to every Lipschitz constant below one.

The latest completed R2--R8 reports, their pertinent committed source, and
the target's bounded graph neighborhood were inspected at pass start and
refreshed before publication. Relevant new accepted context includes the
dilated-martingale family (6464/6480) and the meridian class (6468/6474).
The refresh additionally inspected the cylindrical-twist and twisted-meridian
source, the small-target theorem (6482), and the uniform-Lipschitz theorem
and review (6486). These results remain separately useful; their older
steps are credited wherever used here.
