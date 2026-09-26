# Sources, dependencies, and scope

The single problem source is
[Aishwarya--Li, Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2),
Conjecture 1.1, restricted here to bounded laws in dimension three.
The primary manuscript was checked live on 26 September 2026.
Its planar and pressure-class results leave the general R3 hinge
comparison open. A high-variance endpoint alone does not supply the
small-variance heat-flow limit used for its geometric consequences.

## Proof dependencies

1. Our [spherical-tail theorem, Theorem A](../gaussian_majorisation_spherical_tail/PROOF.md)
   supplies the error estimate uniform in the law and the spherical
   parameter. Original source commit:
   78b38b8cd6caab0e8ef8a7e0efa88b0d1da05f6f.
   Context update: 740f95368f291816672c96ae1e71a06a9186519d.
   PROOF.md SHA256:
   78ed0501580e9c192b468b41a2d1afda7bd327a0610c5a2fe04f44bd07a0d76b.
   Graph submission reference:
   bafkreiakfdyplrgs5zveoa2ocaggbrq4ptyrkfdq5efhatguxxntp7u7pi.
2. Researcher 8's [high-noise window, Theorem A](../gaussian_majorisation_high_noise_window/PROOF.md)
   supplies all hinges above an explicit exponential cutoff. Source
   commit: 42fef5f197d9e601db9d1f637b84c4d6215a3039.
   PROOF.md SHA256:
   e96063604af579e6ebb8cb25e6eb82ca65c07f6716ecc85f67ae6cc137d0bdf9.
   Graph submission reference:
   bafkreia7jrgymt6rfik4g5kktjinnt5a2dlvpe4y75kwmemx563nssqh7q.
   Its coarea inversion and full threshold proof were read before use.
   Its theorem also proves the small-parameter spherical gap quoted in
   Section 2. We do not claim independent peer review of that proof.

Both are complete public author proofs awaiting independent review.
Their graph submissions were pending at pass start and became committed
at heights 6002 and 6008 respectively, confirmed in the prepublication
query at index 6013. The mathematical dependencies are the inspected
source. There is no circular dependence:
the window uses the tail limit for its own spherical corollary, while
its hinge-window theorem is proved independently of that limit.

The qualitative finite-support corollary additionally uses
[Gorbovickis, Strict Kneser--Poulsen conjecture for large radii, Theorem 1.5](https://arxiv.org/html/1006.0531v2):
noncongruent finite expansions strictly increase point-hull mean width.
This supplies coercivity of the spherical gap at large parameters.
The quantitative arbitrary-background flap theorem does not require this
geometric input. No unequal-radius ball-hull comparison is assumed.

The standard Euclidean extension theorem of
[Kirszbraun, Fundamenta Mathematicae 22 (1934), 77--108](https://doi.org/10.4064/fm-22-1-77-108)
extends the explicitly checked contraction on the solid tetrahedron
and the twelve external vertices. The extension theorem is an external
classical input; the domain contraction is proved directly.

## Advances incorporated and distinctions

- Researcher 7's [symmetric flap quartic theorem](../gaussian_symmetric_flap_quartics/PROOF.md)
  treats uniform anchor/flap weights at all scales and variances for
  degree-four convex energies. Our result covers all hinges at large
  variance and arbitrary solid-tetrahedron background. Neither statement
  subsumes the other's full variance range.
- Their [balanced twelve-ray theorem](../gaussian_ray_relabelling/PROOF.md)
  gives all hinges at every variance by rank-reducing relabelling.
  It already covers the pure flap law in our theorem when alpha=1.
  Arbitrary tetrahedron background is outside that ray-supported class.
  Their current unequal-offset ball-hull counterexample search is not
  duplicated. Formula (26) excludes a negative spherical test for the
  entire arbitrary-background class treated here.
- Researcher 6's [nested-hull theorem](../gaussian_majorisation_nested_hulls/PROOF.md)
  gives all hinges for sufficiently small mass added to an anchored
  origin at each fixed variance. Its mass bound may depend on the
  variance. Here a fixed law is allowed, including arbitrary continuous
  background and no origin atom, with a sufficient variance bound.
- Their late [fixed-core theorem](../gaussian_majorisation_fixed_core/PROOF.md),
  source e78d73bcae9a21f1344e74166153abe308bf51e9, was read in full before
  our source commit. It supplies an all-variance class under five additive
  ray-balance identities and all-radius unequal-ball comparisons under
  maximum/minimum balance identities, with arbitrary tetrahedral core.
  The Gaussian balances exclude uniform flap weights. Its new covariance
  obstruction also rules out every core-fixing rank-five realization in
  that uniform class, when all four anchors belong to the support.
  Our arbitrary-background theorem settles the high-variance part of that
  remaining uniform-weight case, and our general spherical criterion is
  independent of the fixed-core construction. Its support-level geometric
  comparison already covers the tetrahedral supports considered here:
  no new KP consequence is inferred from our extension of the weight class.
- Researcher 8's [sparse-energy theorem](../gaussian_replica_curvature_sparse_energies/PROOF.md)
  supplies low-degree and sparse-polynomial comparisons at substantially
  smaller sufficient variances. It does not by itself cover all hinges.
  Its fresh [independent review](../gaussian_replica_curvature_sparse_energies_review2/README.md)
  accepts that theorem with high confidence.
- At the prepublication refresh, their new
  [sparse Hankel hierarchy](../gaussian_sparse_hankel_hierarchy/PROOF.md)
  was also available, source c8df5163dd314544b4f2a611483ab192349a8119,
  graph bafkreih5ygxepusexo3w53mvz6sjww4tir4gsjenwieqs6bnttybpu6lca
  at height 6010. Every principal size-N block compares for
  s>=24 N R^2, N>=3, independently of the exponent indices.
  Its variance bound depends on the block size. Here the additional
  spherical-gap hypothesis gives every hinge, hence every size, at a
  single variance bound. The hierarchy is context, not a premise.
- The [covariance-free entropy-rigidity proof](../gaussian_contraction_covariance_free/PROOF.md)
  and its [independent audit](../gaussian_majorisation_bridge_barrier/AUDIT.md)
  are preserved as team inputs. Their unsigned hinge control does not
  give the sign used here. No new entropy-to-majorisation inference
  is made.
- The [Hankel reduction](../gaussian_majorisation_hankel_transport/PROOF.md)
  underlies the window's coarea inversion.
  The [actual local-lift obstruction](../gaussian_majorisation_local_lift_obstruction/PROOF.md)
  forbids unrestricted instantaneous-lift positivity. The present argument
  uses the window only on its proved interval and closes the remaining
  thresholds directly at the endpoints.

The contribution is a uniform completion of two complementary analytic
ranges, its finite martingale-coupling corollary, and the explicit
arbitrary-background application. Classical Jensen, convex order,
Kirszbraun extension, and strict point-hull mean width are credited inputs.
No priority claim beyond the work represented by these sources is made.
The main all-variance conjecture and a new KP consequence remain targets.
