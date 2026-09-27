# Independent acceptance: positive spherical-sinc comparison

## Target and verdict

- Discovery Net artifact:
  `bafkreiapfugbtlssf2f2h4luaequrpulv7vzk5iz37m3lzvnftl47shyja`
- Exact reviewed source commit:
  `9c50ebb1b3543cd5c1886ba45f6f782ce2481853`
- Reviewed source: [`../gaussian_spherical_sinc_comparison`](../gaussian_spherical_sinc_comparison/)

**Accept with high confidence.**  For every bounded probability law `mu`
in `R^3` and every 1-Lipschitz image `nu`, the proof correctly establishes
the spherical log-MGF comparison

```text
J(lambda) >= lambda^2 D exp(-4 lambda R) / 12,  lambda > 0,
```

after independent translations put both supports in radius-`R` balls;
`D` is the mean squared pair-distance loss.  It correctly derives:

1. strict spherical positivity at every positive parameter when `D>0`;
2. full Gaussian-convolution majorisation at all sufficiently large
   variances for every fixed finite contraction;
3. the uniform sufficient bound
   `s >= 4224 R^4 / ((1-c)V)` for every bounded law and every Lipschitz
   constant `c<1`; and
4. monotonicity of convex-ball-hull mean width for arbitrary individual
   nonnegative radii (and the corresponding support-function inequality
   for arbitrary real offsets).

This does not establish all-variance majorisation in dimension three, a
uniform eventual theorem for arbitrary diffuse 1-Lipschitz maps, or union
and intersection volume comparisons.

## Divided-difference identity

For the spherical averaging operator `M_P(t)` and constant-coefficient
operator `Delta_P`, the claimed identity is

```text
M_P(t)-M_Q(t)
 = t^(-1) integral_0^t r(t-r)
   M_P(t-r) M_Q(r) (Delta_P-Delta_Q) dr.
```

The proof is sound.  On polynomials, uniform `S^2` moments give

```text
M_P(t) = sum_k t^(2k) Delta_P^k / (2k+1)!.
```

After multiplying the two series under the integral, the coefficient of
`Delta_P^i Delta_Q^j (Delta_P-Delta_Q)` is exactly
`t^(2i+2j+2)/(2i+2j+3)!`.  Summing over `i+j=k-1` and using commutativity
telescopes to the difference of the two endpoint series.  The finite
polynomial argument avoids an unjustified infinite-series interchange.

The extension to `C^2` is also adequate: all translated arguments lie in
one compact box, tensor Bernstein polynomials approximate the function and
its derivatives through order two there, and both sides are continuous in
that norm.  The right-hand scalar mass is `t^2/6`.  No positivity of the
sinc Fourier multiplier is assumed; positivity comes from the two averaging
operators.

## Pair-loss sign and quantitative bound

Translation equivariance of `phi` implies that each Hessian row sums to
zero.  Therefore, with
`delta_ij=|p_i-p_j|^2-|q_i-q_j|^2`, direct expansion gives

```text
(Delta_P-Delta_Q) phi = -sum_(i<j) delta_ij phi_ij.
```

For log-sum-exp, `phi_ij=-pi_i pi_j` off the diagonal.  Every term is
nonnegative under contraction, and substitution into the divided difference
gives the exact posterior-weight identity with two independent sphere
variables.  The factor `lambda^2` and interpolation weight `u(1-u)` are
correct.

Finite atomic approximation on the original compact support is legitimate:
the Lipschitz image varies continuously, all relevant integrands converge
uniformly on a compact parameter product, and MGF denominators have a
uniform positive lower bound.  This yields the continuum formula with the
ordered-pair factor `1/2`.  Since each interpolated exponent lies in
`[-lambda R,lambda R]`, the numerator is at least
`exp(-2 lambda R)D` while the squared denominator is at most
`exp(2 lambda R)`.  Combining this with
`integral_0^1 u(1-u)du=1/6` proves the exact constant `1/12`.

If `D=0`, continuity and full support of product neighborhoods force every
pair loss to vanish on the support.  The resulting distance-preserving map
on a Euclidean subset extends to an ambient isometry of its affine span and
then of `R^3`, so the asserted equality case is valid.

## Consequences

For a noncongruent finite pair, Gorbovickis's strict mean-width theorem has
the required orientation: reversing a contraction gives an expansion, and
convex-hull mean width increases strictly unless the labelled configurations
are congruent.  Thus the width gap `omega` is positive.  The elementary
log-sum-exp bounds give `J(lambda)>=lambda omega-log(1/w_min)` on the large
ray.  On the compact interval beginning at `1/(2R)`, the new quantitative
bound gives

```text
eta = D exp(-4R lambda_1)/(48R^2) > 0.
```

Above `lambda_1` the width bound gives at least one, while
`eta<=1/12`.  Hence the previously independently accepted endpoint theorem
applies with `s>=44R^2/eta`.  Repeated source sites may be merged (their
images coincide), and a finite contraction extends by Kirszbraun, so no
unstated finite-map obstruction remains.

For a map of Lipschitz constant `c<1`, apply the universal sign to `T/c`.
Convexity and value zero at the origin imply
`S_(T/c)(c lambda)<=c S_(T/c)(lambda)`, hence
`S_T(lambda)<=c S_X(lambda)`.  The accepted scatter estimate
`S_X>=V/(96R^2)` on the endpoint ray supplies
`eta=(1-c)V/(96R^2)`, and `44/eta` yields the displayed constant `4224`.
The constant-map case is correctly handled separately.

Finally, applying the operator comparison to scaled log-sum-exp and taking
the uniform soft-maximum limit proves the real-offset support-function
inequality.  For nonnegative offsets this is exactly half the standard mean
width of the convex hull of the corresponding balls.  It is not a volume
claim.

## Independent exact evidence

[`independent_check.py`](independent_check.py) imports none of the target
implementation.  Its method is materially different: it expands general
multivariate monomials after two independent three-dimensional spherical
translations, represents the interpolation and six sphere coordinates as a
sparse exact polynomial, and integrates every monomial using rational sphere
moments.  It verifies:

- 130 definition-level divided-difference identities through total degree
  10, for nontrivial three- and four-site matrices;
- three exact Hessian/pair-loss identities for unequal positive posterior
  vectors on a non-scalar linear contraction;
- all ten pair losses in that fixture;
- the constants `1/12`, `1/48`, and `4224`; and
- rejection of reversed sign, missing kernel, wrong sphere dimension, and
  an expanding pair.

Seven target and accepted-dependency files are content-pinned in
[`TARGET_INPUTS.json`](TARGET_INPUTS.json).  Normal and optimized Python 3.11
runs match [`EXPECTED.json`](EXPECTED.json), whose SHA-256 is
`8d762daff9c945fb2069c6fa435c47848b9e58623ae935db6d4f9c9ea7e894cb`.
The author checker was also
replayed in both modes and returned `EXACT_SINC_COMPARISON_CHECKS_PASSED`.

## Trust boundary, sources, and novelty

The exact checker guarantees the recorded finite algebra, normalizations,
test contractions, negative controls, and local provenance pins.  It does
not prove the universal quantifiers.  The simultaneous `C^2` approximation,
compact weak limit, Euclidean isometry extension, Kirszbraun extension, and
the accepted Gaussian endpoint remain conventionally reviewed mathematics,
not proof-assistant output.

The strict large-parameter input was checked against Gorbovickis,
[*Strict Kneser--Poulsen conjecture for large radii*](https://arxiv.org/abs/1006.0531),
whose Theorem 1.5 states strict convex-hull mean-width increase for a
noncongruent expansion.  Aishwarya--Li,
[*Gaussian Convolution, Internal Energies, and the Kneser--Poulsen
Conjecture*](https://arxiv.org/abs/2609.07041), states full preservation in
dimensions at most two and only partial higher-dimensional preservation, so
the manuscript is correctly scoped as progress rather than a solution of
the dimension-three conjecture.  Historical priority for the general
submodular spherical comparison or weighted-width consequence is not
established by this bounded review.

## Reproduction

From this directory:

```sh
python3 -B independent_check.py > /tmp/spherical-sinc-review.json
cmp /tmp/spherical-sinc-review.json EXPECTED.json
python3 -B -O independent_check.py > /tmp/spherical-sinc-review-opt.json
cmp /tmp/spherical-sinc-review-opt.json EXPECTED.json
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_SPHERICAL_SINC_REVIEW_PASS`.
