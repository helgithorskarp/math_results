# Sources, dependencies, and scope

The sole motivating problem is the dimension-three Gaussian-convolution
majorisation question in Aishwarya--Li. Other literature below supplies
established lifting tools or checks the scope of the resulting class.

## Primary papers

1. Gautam Aishwarya and Dongbin Li, *Gaussian Convolution, Internal Energies,
   and the Kneser--Poulsen Conjecture*,
   [arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
   Conjecture 1.1 is the target. Theorem 1.4(i)(a) supplies the
   density-value stochastic order for a continuous contraction; two
   auxiliary Gaussian coordinates then give the hinge identity in our
   equation (12). These results are dependencies, not contributions here.
2. Karoly Bezdek and Robert Connelly, *Pushing disks apart—the
   Kneser--Poulsen conjecture in the plane*,
   [arXiv:math/0108098](https://arxiv.org/pdf/math/0108098).
   Theorem 1 transfers a piecewise-smooth expansion in `R^(n+2)` to
   union and intersection volume inequalities in `R^n`, with arbitrary
   radii. Corollaries 3--5 record displacement-dimension, small-cardinality,
   and partial positive-dilation classes. Theorem 1 is the exact external
   premise of our ball-volume consequence.
3. Karoly Bezdek and Marton Naszodi, *The Kneser--Poulsen conjecture for
   special contractions*,
   [arXiv:1701.05074](https://arxiv.org/abs/1701.05074).
   Section 1.2 defines strong contraction by coordinatewise pair-distance
   decrease and treats one-sided coordinate reflections. Our nonorthogonal
   dual-basis example is not strong in any common orthonormal coordinates.
   This distinction does not exclude all possible compositions of known
   constructions.
4. Holun Cheng, Ser Peow Tan, and Yidan Zheng, *On continuous expansions
   of configurations of points in Euclidean space*,
   [arXiv:1107.0140](https://arxiv.org/abs/1107.0140).
   Their Theorem 1.4 gives the classical `(d+1)^2`-point simplex-flap
   obstruction to motion in dimension below `2d`, also credited there to
   independent work of Belk and Connelly. Their concluding remarks ask
   for the smallest cardinality. Our nine-point square-cone proof is
   self-contained; it does not assume that the 2011 cardinality question
   remains unanswered or claim a smallest possible obstruction.

## Team results inspected

- [Paired rank and Gaussian cancellation](../gaussian_majorisation_rank_abel/PROOF.md),
  researcher 6: the rank-five sufficient condition, its two-coordinate
  cancellation proof, and the classical simplex-flap fixture. The
  cancellation proof is reused and written out. Our explicit motion is
  an additional input beyond its rank hypothesis.
- [Spherical tail and arbitrary-offset ball hulls](../gaussian_majorisation_spherical_tail/PROOF.md),
  researcher 5: this reduction motivated unequal-offset stress tests.
  No spherical asymptotic estimate is used in the cone theorem.
- [Nested-hull small-mass comparison](../gaussian_majorisation_nested_hulls/PROOF.md),
  researcher 6: this covers a different regime, with small mass at fixed
  variance. It does not enter our proof.
- [Balanced twelve-ray relabelling](../gaussian_ray_relabelling/PROOF.md),
  this lane: the earlier theorem changes the deterministic label map while
  preserving the output law. Here the given map itself has a five-dimensional
  motion, with no weight-balance condition. Neither statement subsumes the
  other as formulated.
- [High-noise hinge window](../gaussian_majorisation_high_noise_window/PROOF.md)
  and [sparse Hankel hierarchy](../gaussian_sparse_hankel_hierarchy/PROOF.md),
  researcher 8: refreshed before publication, at repository commits
  `42fef5f` and `c8df516`. They give a threshold window, a spherical range
  `lambda R<=1`, and finite-size Hankel bounds. Our class theorem treats
  every threshold and variance, but only for the specified geometry.
- [Fixed tetrahedral core and balanced rays](../gaussian_majorisation_fixed_core/PROOF.md),
  researcher 6, commit `e78d73b`: the latest all-variance and unequal-ball
  class extends output-law and target-union relabelling to a fixed core.
  Our cone motion follows the original labels and uses no balancing
  identities; the constructions are complementary.
- [Eventual full majorisation from spherical gaps](../gaussian_majorisation_eventual_endpoint/PROOF.md),
  researcher 5, commit `48bcea2`: a uniform positive spherical gap now
  completes every hinge threshold at sufficiently large variance, with
  an explicit tetrahedral-core class. This sharpens the purpose of the
  remaining spherical stress tests and does not enter our motion proof.

The nine-point binary-weight matching observation explicitly reuses the
binary-expansion argument in the nested-hull source. It is not presented
as a new combinatorial device.

## What is asserted as progress

The explicit five-dimensional motion for arbitrary simplicial positive-
dual separation is the geometric ingredient. Its established Gaussian
and Kneser--Poulsen consequences exclude every dual-basis flip, including
arbitrary weights and points in the interiors of the two cones. The
nine-point obstruction identifies an exact nonsimplicial boundary target
for continued asymmetric counterexample exploration.

Primary-source checks and targeted searches on 26 September 2026 for
simplicial or polar cones, two rigid clusters, central reflection,
low-dimensional continuous contractions, and nine-point obstructions did
not locate these exact formulas or statements. This is a record of the
search, not a proof of historical priority. The five-dimensional lifting
criterion itself is explicitly prior. The full dimension-three majorisation
and Kneser--Poulsen problems are not claimed solved.
