# All finite Gaussian contractions: a weight-uniform small-noise hinge band

[PROOF.md](PROOF.md) gives a complete author argument, pending independent
review. For a finite contraction x_i -> y_i in R3 with positive priors,
let d be the minimum **positive** distance occurring in either endpoint
cloud. Combine identical source sites first. Target coincidences are allowed.
With standard Gaussian variance s and normalized hinge threshold u,

    d^2/s>=131072  =>  H(u)>=0 for u>=exp[-d^2/(1024s)].

The result holds uniformly over all positive priors on the map, even
priors changing with s. There is no weight, cardinality, radius, loss or
degree parameter in the guard. Nonisometric maps have strict signs below
the target peak within the band; isometries have equality everywhere.

The new step is an exact split of the R6 lift into three-dimensional
conditional mixtures, using source coordinates in its first half and
grouped target coordinates in its second half. A level that is reached
supplies its own conditional amplitude floor. Quadratic coordinates and a
midpoint-uniform spherical comparison sign the complete fibre density.
Its square-root mode onsets are integrable, so local Abel inversion
applies. This is a threshold sign, not a moment-degree increment.

The unrestricted Gaussian conjecture remains open. No new Kneser--Poulsen
comparison, uniform conclusion for shrinking positive separations, or
sign below the displayed threshold is claimed. For the guarded
indecomposable frontier6602, collisions and vanishing auxiliary weights
are now permitted; arbitrarily fine mesh separations remain an obstacle.

## Reproduction

CPython 3.11 or later; standard library only. From this directory:

    python3 -B audit.py
    python3 -B -O audit.py

Both end with `ATOMIC_HINGE_WINDOW_AUDIT_PASS`. They check exact rational
constant budgets, closed boundaries, complete mergers, isometries,
normalization, and a credited seven-site collision control of paired rank
six with priors as small as 2^-2048. The code checks all 21 pairs and
conditional group weights; it rejects ten malformed inputs. The controls
do not prove the analytic theorem or independently review it. No Gaussian
quadrature, solver, random search or external certificate is used.

Optional input: `python3 -B audit.py input.json`. For example:

```json
{
  "source": [[0,0,0], [2,0,0]],
  "target": [[0,0,0], [0,0,0]],
  "weights": ["1/3", "2/3"],
  "variance": "1/32768",
  "log_threshold": 128
}
```

`log_threshold` is the exact number ell in u=exp(-ell), not a floating
evaluation of u. Coordinates, weights, variance and ell must be integers
or exact rational strings. Variance must be positive, ell nonnegative;
sources must be distinct. The output is NONNEGATIVE, EQUALITY, or
NOT_COVERED. The last means only that this sufficient guard does not apply.
Malformed input raises an error. For the example, the separation/variance
ratio is 131072, the maximum ell is 128, and the status is NONNEGATIVE.

## Provenance

- [Separated-component predecessor6598](../gaussian_separated_hinge_window/PROOF.md),
  source `3cdd8e3194d23dcb08b773e4962d51468765ecd1`. Its six-dimensional
  local charts and midpoint square completion are extended here; its
  stronger numerical cutoff for suitable distinct-target data remains valid.
- [Universal peak window6580](../gaussian_universal_peak_window/PROOF.md),
  source `9e18bbc050edb580004c4bef6d251e9238ad651f`, independently
  [accepted6592](../gaussian_universal_peak_window_review2/REVIEW.md),
  source `5947eff60b62832dcafdb61304cb4a60378466a5`.
- [R8 covariance-free small-loss6596](../gaussian_covariance_free_small_loss/PROOF.md),
  source `4feee1ee4c541c459c0c0440b44b25052b20201a`, independently
  [accepted6604](../gaussian_covariance_free_small_loss_review2/REVIEW.md),
  review source `b35df0d4b54aba954b2510dd947076c15e3fc994`: related work
  on normal fibres and absolute continuity, not a premise. Its bounded-radius,
  small-loss guard is different from the separation guard here.
- [Finite-degree collision exclusion6386](../gaussian_atomic_low_noise_exclusion/PROOF.md),
  source `02b579d7e9c77053d7399096fe9314b9fdfca6f1`, independently
  [accepted6392](../gaussian_atomic_low_noise_review_frontier/REVIEW.md),
  source `49a5aa6de6d9574c52ff4efab4e61e425f340874`. The coordinatewise
  absolute-value control is credited to this source, not a new map class.
- [Guarded indecomposable frontier6602](../gaussian_guarded_indecomposable_frontier/HANDOFF.md),
  source `4cbdf8e0475d69b40d8bbf8249c714ba5682f96d`: a potential consumer,
  not a theorem assumed in the sign proof.

The named question is [Aishwarya--Li, Conjecture 1.1](https://arxiv.org/html/2609.07041v2).
Historical priority is not claimed. This packet contains only compact
source and exact controls; the universal statement remains written analysis.
