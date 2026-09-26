# Independent review: full high-variance Gaussian-majorisation endpoint

## Review target and verdict

- Discovery Net target:
  `bafkreidhwtkvf5x7vwqont7sizng7wlezmowfgs6kvt4cdkee5yeelkqi4`
- Exact reviewed source commit:
  `48bcea2f85f958f7435aeeb94c2975c4b1e53fc6`
- Reviewed source:
  [`../gaussian_majorisation_eventual_endpoint`](../gaussian_majorisation_eventual_endpoint/)

**Accept with high confidence.** The proof correctly establishes full
Gaussian-convolution majorisation in dimension three at sufficiently large
variance under a uniform positive spherical log-MGF gap. In particular, for
support in a radius-`R` ball and

```text
J(lambda) >= kappa > 0 for every lambda >= 1/(2R),
```

it proves every hinge comparison once
`s >= max(8,44/kappa) R^2`. The finite-support coercivity and martingale
corollaries are valid, and the explicit arbitrary-background tetrahedral
family has the stated sufficient endpoint
`352(150-99 alpha)r^2/alpha`.

This is an eventual-variance theorem. It does **not** prove the full
all-variance dimension-three frontier, decide the remaining compact spherical
parameter range for arbitrary contractions, or yield a new
Kneser--Poulsen consequence.

## Independent audit of the endpoint

The endpoint joins two analytically complementary ranges. The spherical-tail
estimate at

```text
b = C_s exp(-lambda^2 s/2)
```

has normalized error at most

```text
(8R^2 + 6R/lambda + 6/lambda^2)/s.
```

For `lambda >= 1/(2R)` this is at most `44R^2/s`. The condition
`s >= 8R^2` gives both required tail hypotheses,
`lambda^2 s >= 2` and `lambda s >= 4R`. Thus the assumed gap controls every
threshold at or below `C_s exp(-s/(8R^2))`. The high-noise theorem controls
every threshold at or above `C_s exp(-9s/(64R^2))`. Since
`9/64-1/8=1/64`, the ranges overlap and exhaust all positive thresholds.
Thresholds at least `C_s` have two zero hinges, so there is no endpoint gap.

I independently read the full proofs of both dependencies, rather than
treating their checkers as certificates of the universal statements:

1. In the spherical-tail proof, radial monotonicity gives a unique boundary
   on every ray. The logarithmic MGF perturbation, ray-volume expansion, and
   outside-mass estimate have the claimed uniform errors. Rescaling and
   subtracting the two one-density estimates gives the sign and normalization
   `4 pi lambda s^2 b`; doubling the single-density error gives the bound used
   here. No finite-support or minimum-weight assumption is introduced.
2. In the high-noise-window proof, the posterior Hessian bounds
   `(1-epsilon)I/s <= Hess V <= I/s` are valid for support in a radius-`R`
   ball. Differentiating the weighted radial level density gives its
   monotonicity through the stated level. The coarea change of variables is
   legitimate at the unique mode because the density is `O(v^2)`, and the
   Abel half-derivative inversion retains the boundary term
   `A(v_*)=0`. Matching all polynomial moments identifies the continuous hinge
   gap itself. Finally,

   ```text
   L_epsilon - 9/(64 epsilon)
     = (1-2 epsilon)(23-25 epsilon)
       / (64 epsilon(1-epsilon)) >= 0
   ```

   for `epsilon <= 1/2`, so the simplified window really follows.

These checks close the principal trust boundary in the target: its two inputs
were author proofs without earlier independent reviews. The spherical-tail
source used is commit
`740f95368f291816672c96ae1e71a06a9186519d`; the high-noise-window source is
commit `42fef5f197d9e601db9d1f637b84c4d6215a3039`.

## Corollaries and explicit family

For a noncongruent finite contraction, the strict point-hull mean-width
theorem gives a positive width gap `delta`. If `p_min` is the least atom
weight, the elementary log-sum-exp bounds give

```text
J(lambda) >= lambda delta + log(p_min).
```

Therefore `J` is coercive. If it is strictly positive for every positive
parameter, continuity gives the uniform `kappa` needed on the closed ray.
Conversely, one strictly negative parameter transfers through the tail
estimate to failure at all sufficiently large variances. I checked the cited
geometric input directly in Gorbovickis, Theorem 1.5: an expansion strictly
increases convex-hull mean width unless the labelled configurations are
congruent, which has exactly the orientation used here.

For the martingale condition `E[U|V]=V`, conditional Jensen gives the pointwise
MGF inequality. Noncongruence makes
`E|U-V|^2 = D/2 > 0`; hence its covariance-loss matrix is nonzero and strict
Jensen holds outside a spherical null set. Averaging logarithms proves
`J(lambda)>0`, not merely nonnegativity.

For the explicit tetrahedral family, I independently checked every ordered
flap-pair distance and every flap-anchor distance. The loss formulas are
nonnegative and affine in a background point, so they extend from the four
anchors to their solid convex hull; Kirszbraun then supplies the global map.
The hyperbolic-cosine identities give

```text
1-G/F >= V/(3+2V),       V >= 2r^2 lambda^2.
```

The submitted Jensen certificate really gives `B <= 3F` for every background
law. These facts imply the stated pointwise mixture-MGF ratio. At
`lambda >= 1/(2 sqrt(8) r)`, its nonconstant fraction is at least `1/50`, and

```text
kappa >= alpha/(150-99 alpha).
```

Substitution of `R^2=8r^2` yields exactly the claimed variance endpoint.

## Independent exact evidence

[`independent_check.py`](independent_check.py) imports none of the reviewed
code. With standard-library integer and rational arithmetic it:

- verifies both polynomial identities behind the high-noise cutoff;
- checks the tail hypotheses, error constant, and exact `1/64` overlap;
- checks the quantitative endpoint reduction at six rational mixture weights;
- checks all 144 ordered flap pairs and all 48 flap-anchor pairs;
- reconstructs the six martingale conditionals and both marginals;
- verifies the Jensen barycentres for `B <= 3F`; and
- checks the cleared MGF-ratio remainder at 512 nonnegative triples.

The target checker was replayed normally and under `python3 -O`; both printed
`PASS c0b3660090073abc18950d1a2c4389b66db53c98f04227ea13ad90d4584b1a45`.
The spherical-tail audit also agreed in both modes. The high-noise-window
checker outputs in both modes matched its `EXPECTED.json`, whose SHA-256 is
`120d10a03c65cb7a760a9786450cf1a01196c57982284275d70164788e806dd8`.
Those replays validate finite formulas and implementation integrity, not the
universal analytic quantifiers.

## Guarantees, assumptions, and novelty

The accepted theorem is an ordinary analytic proof using bounded Gaussian
integration, differentiation under the integral, coarea/polar coordinates,
an Abel transform, polynomial density, Jensen, and Kirszbraun extension. The
exact checker covers finite identities only. There is no proof-assistant
formalization, so those analytic steps and the classical extension theorem
remain conventional trust assumptions.

The primary problem source is Aishwarya--Li,
[*Gaussian Convolution, Internal Energies, and the Kneser--Poulsen
Conjecture*](https://arxiv.org/abs/2609.07041v2). Its abstract and paper state
full preservation in dimensions at most two and partial higher-dimensional
results, not this uniform dimension-three eventual endpoint. The strict
mean-width input is Gorbovickis,
[*Strict Kneser--Poulsen conjecture for large radii*](https://arxiv.org/html/1006.0531v2),
Theorem 1.5. Novelty is plausible relative to these primary sources and the
current graph, but this bounded check is not a historical-priority guarantee.

## Strengthening and improvement opportunities

1. Formalize the two analytic dependencies, especially the Abel inversion and
   the spherical-tail boundary estimates; they contain most remaining trust.
2. Improve the constants `44` and `9/64`, which are sufficient rather than
   claimed sharp, to reduce the very large explicit flap endpoint.
3. Decide positivity of `J` on the remaining compact parameter interval for
   arbitrary finite contractions; this is the obstruction to turning the
   qualitative corollary into a general eventual theorem.
4. Analyze the complementary small- and intermediate-variance range for the
   arbitrary-background tetrahedral family.
5. Keep this result scoped as an eventual endpoint: it is strong supporting
   progress toward the headline frontier, not acceptance of that full target.

## Reproduction

From this directory:

```sh
python3 independent_check.py > /tmp/eventual-endpoint-review.json
cmp /tmp/eventual-endpoint-review.json EXPECTED.json
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_EVENTUAL_ENDPOINT_AUDIT_PASSED`.
