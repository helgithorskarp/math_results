# Sources, scope and trust

The sole problem source is
[Aishwarya--Li, Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture](https://arxiv.org/html/2609.07041v2).
The named question asks whether every bounded-law contraction in R3 has
favorable Gaussian majorisation at every variance. This work gives one
uniform eventual exclusion, not the full result.

The material team inputs are content-pinned in [INPUTS.json](INPUTS.json):

1. [Signed-radial exchange identity](../gaussian_signed_radial_tail_exclusion/PROOF.md),
   original6339, `bafkreiddqt4xvrsueribcytsogz5bncvo6kem6pu3mncsrv5mmcpjjgfui`.
   Source `b9a8693f0675712120e730c5bb6db0da37708359`. Separate iid exchanges,
   a four-point doubly stochastic comparison, and directional MGF products
   were already established there. We recall the identity and its direct
   cosh proof. No new general Rademacher contraction principle is claimed.
2. [Uniform eventual Gaussian endpoint](../gaussian_majorisation_eventual_endpoint/PROOF.md),
   original6032, `bafkreidhwtkvf5x7vwqont7sizng7wlezmowfgs6kvt4cdkee5yeelkqi4`.
   Source `48bcea2f85f958f7435aeeb94c2975c4b1e53fc6`. We use precisely its
   all-threshold theorem from a uniform spherical gap eta on
   lambda>=1/(2R), with variance cutoff R^2 max(8,44/eta).
3. [Independent endpoint acceptance](../gaussian_majorisation_eventual_endpoint_review2/README.md),
   review6048, source `c750676fd6e164db43c0891c0093ebed2a49c356`. Its full
   written review was read. It audits both the spherical-tail and high-noise
   dependencies and the threshold overlap. Those analytic results are
   imported; their numerical checkers were not needlessly rerun here.

The new step is a coefficient-space hexagon filled by conditional means of
radial clouds. It gives an exponential envelope with a finite mass penalty
and uniform tail growth. Together with the earlier positive exchange
identity, this supplies the gap that the accepted endpoint needs. The
qualitative origin-supported corollary allows arbitrary bounded radial
and angular laws under independence, including diffuse measures. The new
argument is written in full and uses only elementary convexity and
spherical second/absolute moments beyond the imported endpoint.

Relevant current boundaries, not additional analytic premises:

- [R2's uniform Lipschitz certificate](../gaussian_uniform_lipschitz_certificate/PROOF.md)
  signs all sufficiently large variances for every map with Lipschitz bound
  below1/sqrt(27), without a covariance floor. The present signed radial
  family permits Lipschitz constant one and preserved distances, but imposes
  independence and radial-cloud structure. Neither unrestricted scope is
  inferred from the other.
- R1's new [spherical sinc comparison](../gaussian_spherical_sinc_comparison/PROOF.md)
  appeared at publication refresh. Its complete author proof asserts the
  universal spherical sign, eventual comparison for every finite contraction,
  eventual comparison for every uniform Lipschitz bound c<1 on arbitrary
  bounded laws, and arbitrary-radius ball-hull mean-width monotonicity in R3.
  It remains pending review in the inspected context. It expressly leaves
  unrestricted diffuse laws at Lipschitz constant one open. Our added scope
  is the uniform diffuse radial-cloud theorem at that boundary; the finite
  fixture is only a control. The new sinc theorem is not a premise here.
- R3's new [measure-neighborhood transfer](../gaussian_robust_martingale_localization/PROOF.md)
  gives a distinct uniform eventual guard from a dilated-martingale reference
  and a strict perturbation budget. Its late handoff also explains the
  conditional use of R1's strictly contracting references. No such reference
  or perturbation budget is used in the present cloud-envelope proof.
- [R2's dilated-martingale theorem](../gaussian_dilated_martingale_certificate/PROOF.md),
  original6464 accepted6480, gives a different full-threshold eventual
  guard. Our exponential envelope has a mass penalty; no martingale
  coupling of endpoint laws is assumed or asserted, and no claim that every
  individual law here escapes that guard is made.
- [R8's uniform small-target theorem](../gaussian_uniform_small_target/PROOF.md)
  signs all thresholds at prescribed variance with much stronger damping
  and a source covariance floor. It retains those hypotheses.
- [R6's nonnegative normal-ray theorem](../gaussian_radial_contractions/README.md)
  and [meridian theorem](../gaussian_meridian_contractions/PROOF.md)
  supply all-variance and KP conclusions for their geometric classes.
  The present result permits negative radial output factors and proves
  only eventual Gaussian comparison. Their stronger conclusions are not
  imported for this class.

Primary literature and current public source were inspected on27 September
2026. A targeted literature search did not establish historical priority;
none is claimed. This is not an independent review of any cited theorem.

All new executable checks use standard-library integers and Fraction, with
no floating oracle, solver or omitted large certificate. They audit algebra,
finite barycentres, parameter arithmetic and one finite input. The continuum
Jensen argument, radial independence, integration over S2 and the accepted
Gaussian endpoint remain written analytic trust boundaries. Passing the
checker does not independently establish the theorem's universal quantifiers.
