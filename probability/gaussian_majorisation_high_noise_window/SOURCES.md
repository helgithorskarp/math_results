# Source and dependency record

The single problem source is
[Aishwarya--Li, Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2),
Conjecture 1.1, restricted here to bounded inputs in dimension three.
The source's Gaussian replica formula and continuous-lifting framework
are prior work. The named paper was rechecked live on 26 September 2026;
the latest version was v2, dated 13 September 2026. The full conjecture
and its all-variance geometric implication are not proved in this package.

## Mathematical dependencies

- [The team's exact Hankel/lift reduction](../gaussian_majorisation_hankel_transport/PROOF.md)
  supplies the identity `a_j=sqrt(j+2) integral u^j d eta/(4s)` and the
  hinge-moment uniqueness argument. Graph:
  `bafkreids462diitdof5ijilzcq2xqwftk2bzjr5t2gihnxk327uezbndbm`.
  Source commit `6f51c67737051a61290c070c9fb960e1da83b75b`.
  Section 2 of our proof rederives its normalization; we do not claim that
  exact representation as new. The new step is its signed inversion
  using weighted coarea monotonicity on a quantitative level interval.
- [The team's spherical-tail transfer theorem](../gaussian_majorisation_spherical_tail/PROOF.md),
  Theorem A, is a premise of Theorem C here. It identifies the scaled
  high-variance hinge limit with the spherical log moment-generating
  difference, with a uniform error. Original source commit
  `78b38b8cd6caab0e8ef8a7e0efa88b0d1da05f6f`; refreshed context at
  `740f95368f291816672c96ae1e71a06a9186519d`.
  Its sign and scaling were inspected before applying it. We neither
  repackage that limit as new nor assume its unresolved sign at every
  parameter. Theorem C proves a quantitative sign when `lambda R<=1`.

The Laplace transform of the half derivative, Gaussian posterior Hessian
formula, and radial changes of variable are proved directly in PROOF.md.
No unquoted fractional-calculus theorem is needed for the inversion.
The continuity, growth, and zero boundary value at each moving mode are
included explicitly. Literature searches for contraction majorisation
at high noise and spherical log moment-generating comparisons did not
identify the stated quantified window. This is not a historical priority
claim.

## Closed routes and complementary team results

- The [covariance-free rigidity proof](../gaussian_contraction_covariance_free/PROOF.md)
  was independently audited in our
  [bridge-barrier package](../gaussian_majorisation_bridge_barrier/AUDIT.md),
  graph `bafkreibohj2zayll2fnt5zmiug23fkkai6oy4mv3mhinmh5etuxvgzofxq`.
  Neither rigidity nor entropy alone provides the signed hinge inequality.
  The new proof retains the deficit-weighted Gaussian geometry throughout.
- The [actual instantaneous-lift obstruction](../gaussian_majorisation_local_lift_obstruction/PROOF.md),
  graph `bafkreifseyjs3jimzu7yvo3lpfd3555dmnf5q6hraqdonaldti3nqjgxqy`,
  rules out unrestricted pointwise positivity. We use explicit radius,
  variance, and level restrictions, not that disproved hypothesis.
- Our [sharp replica/sparse-energy theorem](../gaussian_replica_curvature_sparse_energies/PROOF.md),
  graph `bafkreigxtycueb6re2fvuohmmqw3er5l76jddrbhbyv2nqexhj6w7x356y`,
  source `5586f0d772d6b7861bd73207901e183690f4d22b`, proves all
  order-two Hankel minors at `s>=2R^2/5`. It does not prove all hinges.
  Conversely the present threshold window leaves an uncontrolled tail
  and does not by itself prove every higher Hankel matrix positive.
- The [small-mass theorem](../gaussian_majorisation_small_mass/PROOF.md),
  graph `bafkreihtnp3ptickdr4nhikxkarcr3v4uwocvhde5lcj3mx2fhmk7b7jge`,
  and its new [nested-hull extension](../gaussian_majorisation_nested_hulls/PROOF.md)
  concern a varying law near a dominant atom at fixed variance. The latter
  closes every threshold for sufficiently small mass if the support
  hulls are nested and the maximum radius strictly decreases. Original
  extension commit `260e84d6a1a8f58b5964eac77cd52fdcff5df491`.
  Those are distinct assumptions and limits from this uniform result
  for arbitrary fixed bounded laws at sufficiently large variance.
- The [balanced twelve-ray theorem](../gaussian_ray_relabelling/PROOF.md),
  source `4ae1468058b90d7d8c9040153dc68853cc39cba1`, establishes full
  majorisation for its specified balanced radial laws via rank-reducing
  relabelling. The [unique-mass relabelling obstruction](../gaussian_majorisation_nested_hulls/PROOF.md)
  excludes a proposed deterministic extension to uniquely labelled flap
  masses. No adversarial search in the settled ray class is pursued here.

The pass began at source `5586f0d772d6b7861bd73207901e183690f4d22b` and
graph height 5995, then incorporated the spherical-tail source and, before
publication, the newer nested-hull and balanced-ray artifacts. The graph
remained at height 5995 on that refresh, while the repository had advanced
to `b09e0372b9c9e6e8b416543ff9b6c469e7f07b79`. Repository sources are
durable citations even where the team's graph submissions await commitment.

## Arithmetic dependency and trust boundary

`verify.py` imports only the standard library and the adjacent
`gaussian_majorisation_hankel_transport/bounds.py`, pinned to SHA256
`60ff5166c623797055f37442d5532b1a29c06275b8871fa4fdf34dcd12f54fc7`.
The interval/exponential primitive is reused, not claimed independently
implemented. New logarithm and pi series include explicit remainder
bounds; integer square roots and rational outward rounding give the
remaining enclosures. The independent integral formula and midpoint
error bound are stated in the checker. No arbitrary-precision floating
point or unvalidated quadrature is used in its certificates.

The universal theorem remains an analytic author proof awaiting external
review. Publishing source or passing finitely many controls does not
resolve that trust boundary.

## Small-radius all-order error consequence

[SMALL_RADIUS_DEFECT.md](SMALL_RADIUS_DEFECT.md) is a later quantitative
consequence of Theorem A in the unchanged original PROOF.md. Its only additional
analytic estimate is the explicitly integrated inner/outer Gaussian shell
bound. This converts the signed threshold window into an exponentially small
possible adverse defect. It does not independently audit the coarea theorem.

The fallback7/50 comes from the reviewed
[uniform-defect theorem](../gaussian_uniform_defect_bound/PROOF.md), graph6186
`bafkreiabyue73en4ed52wakh3cak6dsayxvljtzz4bb77nrlvavhrflcne`.
The [independent scalar acceptance](../gaussian_uniform_defect_bound_review2/REVIEW.md)
and [functional-lane acceptance](../gaussian_uniform_defect_review_r8/REVIEW.md)
retain their scopes. No claim to the constant's authorship is made.

The consumer uses the existing finite schema of the
[paired-cubature frontier](../gaussian_prior_localization/CUBATURE_FRONTIER.md).
It gives a radius-based upper defect certificate on actual cells in that family,
without changing the localization, atom counts, or rational rounding. R3's
[threshold-relative quadrature](../gaussian_prior_localization/RELATIVE_HINGE.md),
graph6258 `bafkreigrupfl3ygeobrisweseaoxdunqlnlxyph7gzlmfxkiqob3k6m65q`,
is a complementary producer when a spatial grid is needed. The radius certificate
does not numerically integrate those cells or claim that it covers the full family.

The [seven-factor sign](../gaussian_seven_factor_kernel/PROOF.md) now has
[R5 acceptance](../gaussian_seven_factor_review_r5/REVIEW.md) and a
[second independent acceptance](../gaussian_seven_factor_review2/REVIEW.md),
graph6262 `bafkreifkp2tre6g3zuwlrg2okhhbgt5z47do6hrurjkpgd6vzmsad5yvou`.
Those exact signs remain separate from the all-order error estimate.
R2's [conditional-kernel rank classification](../gaussian_conditional_kernel_obstruction/PROOF.md)
closes a pointwise all-order iteration of the Gram-kernel route. Its seven-site
absolute-value fold is reused only as a scaled exact geometry control; all of its
actual hinges are already known positive. The new bound does not claim to repair
negative individual kernels or to settle b_(8,0).

The pinned paths, source revisions and SHA256 hashes for this addition are in
[RADIUS_INPUTS.json](RADIUS_INPUTS.json). The new code imports no teammate code,
solver, interval library or unvalidated numerical output. Its finite controls
are author checks of the certificate arithmetic, not another independent review.
