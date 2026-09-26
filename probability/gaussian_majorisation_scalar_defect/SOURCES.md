# Sources and research scope

Primary papers were checked live on 26 September 2026.

1. Gautam Aishwarya and Dongbin Li,
   [Gaussian Convolution, Internal Energies, and the Kneser--Poulsen
   Conjecture, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
   The dimension-three majorisation question is the sole problem source.
   Theorem 1.4(i)(a) is the Gaussian premise used here.
2. Karoly Bezdek and Robert Connelly,
   [Pushing disks apart, arXiv:math/0108098](https://arxiv.org/pdf/math/0108098).
   Theorem 1 gives the arbitrary-radii volume consequence of the motion.
   Lemma 1 credits the square-root interpolation to Alexander. The present
   calculation shares one scalar coordinate instead of making two separate
   copies, and pays for the resulting quadratic defect. The basic
   interpolation method is prior work. Corollary 3 is the
   two-dimensional-displacement criterion distinguished in our example.
3. Karoly Bezdek and Marton Naszodi,
   [The Kneser--Poulsen conjecture for special contractions,
   arXiv:1701.05074](https://arxiv.org/pdf/1701.05074).
   Section 1.2 supplies the strong-contraction definition used in the
   scope comparison. No stronger novelty inference is made from it.

## Durable team inputs

- Researcher6's [paired-rank and cancellation proof](../gaussian_majorisation_rank_abel/PROOF.md)
  gives the exact Gaussian cancellation already used by the team.
  Its rank-five hypothesis is distinct from the scalar-defect criterion.
- Researcher6's [fixed-core result](../gaussian_majorisation_fixed_core/PROOF.md),
  source commit e78d73bcae9a21f1344e74166153abe308bf51e9, supplies
  coordinate-preserving maps and the class-building context. Our perturbation
  bound can be applied to such maps after scalar contraction, but does not
  keep a fixed core pointwise fixed. No such extra conclusion is asserted.
- Researcher7's [simplicial-cone result](../gaussian_simplicial_cone_reflections/PROOF.md),
  commit a792a1a8601d347e6e45a00bf9a3fc849d91f4b7, settles every simplicial
  flip and identifies the square-cone nine-point frontier. Our elementary
  exclusion of the scalar criterion is consistent with that work.
- Researcher8's [common-target theorem](../gaussian_majorisation_common_target/PROOF.md),
  commit 3ad6ed0be174d1292b250efcad734d03eed01af5, closes the uniform
  tetrahedral-background family at every variance and gives an injective
  finite limitation. It was read before this note; those routes are not
  reopened.
- Our [eventual endpoint](../gaussian_majorisation_eventual_endpoint/PROOF.md),
  commit 48bcea2f85f958f7435aeeb94c2975c4b1e53fc6, and its
  [independent acceptance](../gaussian_majorisation_eventual_endpoint_review2/README.md),
  commit c750676fd6e164db43c0891c0093ebed2a49c356, remain separate inputs.
  The review includes the spherical-tail and signed-window dependencies.
  The present proof does not use a noise restriction or an entropy-only
  inference.
- The late [asymmetric atomic obstruction](../gaussian_atomic_bridge_obstruction/PROOF.md),
  commit d05dd54b551a5a14329cfbe31f8b66c13cc0e217, excludes the martingale
  condition, including after common Gaussian smoothing, for an open
  square-cone weight family. It also gives a quantitative obstruction
  to approximate deterministic common outputs on the same supports.
  These restrictions are preserved in the next analytic obligation.
- Researcher6's late [axial-cone theorem](../gaussian_axial_cone_rotations/PROOF.md),
  commit 984e1edaaf7f02bf4572c80754edff1e296fdd19, proves a different
  full comparison class, including circular slopes with product at most
  $2/\pi$. Its four-dimensional motion and perimeter criterion are not
  duplicated. Spanning norm-preserving members fail our scalar condition.
- The [common-target independent review](../gaussian_majorisation_common_target_review2/README.md),
  commit 193f0e8fbf34bba8db0ef54d2aa87efa75de7034, accepts that theorem
  and checks its nine-point geometric dependency. It does not review
  the present criterion.

## What is new in this handoff

The useful addition is an explicit scalar-defect budget, its Lipschitz
perturbation corollary, and a rational example outside the paired-rank and
strong-coordinate tests. It gives both Gaussian and geometric endpoints
by established transfer theorems. This is a compact supporting theorem,
not the campaign's sought general solution, and no claim that its
geometric consequences were absent from every earlier sufficient class.

Targeted searches for scalar-coordinate defects, partial leapfrog
interpolation, and perturbations of continuous contractions did not locate
this exact condition in the inspected primary sources. This limited
search does not establish historical priority. The shared-coordinate
interpolation is close enough to the classical construction that the
scope and attribution above are essential.

No exploratory floating-point spherical search is evidence for this
theorem. A coarse apparent negative angular hinge disappeared on
refinement and was discarded; no counterexample is claimed.
