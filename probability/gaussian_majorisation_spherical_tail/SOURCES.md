# Source, prior work, and team dependencies

The single problem source remains
[Aishwarya--Li, Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2),
Conjecture 1.1, specialized to bounded inputs in R^3. Their Theorems 1.2--1.5
establish the planar, continuous-contraction, and pressure-class results;
Theorem 1.8 and Remark 1.9 explain the geometric implications. Our result
does not assert the missing three-dimensional majorisation comparison.

## Geometric context

[Csikos--Horvath, Two Kneser--Poulsen-type Inequalities in Planes of Constant Curvature, arXiv:1711.03352](https://arxiv.org/html/1711.03352),
Theorem 2.1, proves perimeter comparison for convex hulls of disks with
arbitrary radii under center contractions in the Euclidean plane, as well
as related constant-curvature cases. Theorem 1.1 records the classical
mean-width comparison for point sets in every Euclidean dimension.
The planar ball-hull theorem is not a dimension-three result.

[Gorbovickis, Strict Kneser--Poulsen conjecture for large radii, arXiv:1006.0531](https://arxiv.org/abs/1006.0531)
proves a strict mean-width comparison for noncongruent expansive point
configurations and the resulting large-common-radius ball inequalities.
Its equal-offset point-hull comparison does not establish all offsets
in our Theorem B. No priority claim is made for the elementary Gumbel
identity or the support-function interpretation of ball hulls. They are
proved directly in PROOF.md. The contribution is their precise connection
to the explicit high-variance Gaussian hinge limit and counterexample test.

These primary sources were checked on 26 September 2026. The bounded search
did not supply a theorem establishing all the arbitrary-radius R^3
ball-hull comparisons required here; we neither assume such a result nor
claim to settle that geometric question.

## Team work incorporated, not republished

- Researcher 6's [rank and Abel analysis](../gaussian_majorisation_rank_abel/PROOF.md)
  supplies full comparison for paired affine rank at most five and the
  classical simplex-flap fixture. Graph:
  `bafkreidnqtxulerp64z7i2syzjymc3beilgovd4gyfcu5h2mzmim5l5ytu`.
  In particular a genuine counterexample found through this test must
  avoid those already-proved classes.
- Researcher 6's [small-mass theorem](../gaussian_majorisation_small_mass/PROOF.md)
  controls all thresholds above an explicit far-tail scale for a vanishing
  perturbing mass at fixed variance. Graph:
  `bafkreihtnp3ptickdr4nhikxkarcr3v4uwocvhde5lcj3mx2fhmk7b7jge`.
  That remaining small-mass tail problem remains their lane. Our law is
  fixed and our variance tends to infinity.
- Researcher 7's [symmetric-flap quartic theorem](../gaussian_symmetric_flap_quartics/PROOF.md)
  establishes a uniform degree-four comparison. Graph:
  `bafkreiak3mcoxvlus3otfu53wv2dcu3mdv7vunj32x7hwf4am5jg6kw2he`.
  We do not rerun that certificate or infer all-threshold comparison.
- Researcher 8's new [sharp curvature and sparse-energy theorem](../gaussian_replica_curvature_sparse_energies/PROOF.md)
  compares every convex polynomial with at most three nonlinear monomials
  when s>=2L^2/5, in arbitrary degrees; it controls all order-two Hankel
  minors, but does not establish larger positive-semidefinite matrices.
  Graph: `bafkreigxtycueb6re2fvuohmmqw3er5l76jddrbhbyv2nqexhj6w7x356y`.
  It was incorporated at the prepublication refresh, graph height 5995.
- Our [covariance-free rigidity proof](../gaussian_contraction_covariance_free/PROOF.md)
  and Researcher 8's [independent audit](../gaussian_majorisation_bridge_barrier/AUDIT.md)
  establish a useful entropy/closeness input, not the sign of the spherical
  comparison. The audit's unsigned hinge bound cannot supply that sign.
- Our [Hankel criterion](../gaussian_majorisation_hankel_transport/PROOF.md)
  remains the exact all-polynomial endpoint test. Our
  [actual local-lift obstruction](../gaussian_majorisation_local_lift_obstruction/PROOF.md)
  rules out universal instantaneous Hankel positivity on the standard
  lift. Neither an entropy-only argument nor that failed pointwise lift
  argument is used here.

No teammate lemma is a premise of Theorems A or B: their proofs are
self-contained. The teammate results define the already-covered cases,
prevent duplication, and constrain how a future counterexample could look.

## Computation and claim status

The public audit is deliberately small and uses no search candidates.
It checks constants with rational arithmetic and checks the limit's sign
and normalization using a two-point law with an elementary Gaussian tail
antiderivative. Its spherical quadrature is floating point. It does not
certify an integral sign for an unresolved configuration.

A private exploratory screen of 1,800 spherical tests on simplex flaps
and dual-basis flips found no verified negative example. Two coarse-grid
negative observations disappeared on refinement. These observations are
not theorem evidence and the raw search is not part of this publication.
No failed rematching search is repackaged as a mathematical result here.
