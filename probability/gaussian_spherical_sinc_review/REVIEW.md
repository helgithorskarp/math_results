# Independent review: spherical sinc comparison

## Verdict

**Accept for correctness in the stated scope.** At source commit
`9c50ebb1b3543cd5c1886ba45f6f782ce2481853`, the proof establishes the
following four conclusions for dimension three.

1. If `mu` is bounded, `T` is 1-Lipschitz, `nu=T#mu`, and the separately
   translated source and target supports lie in radius-`R` balls, then

   ```text
   J(lambda)=average_theta[log M_mu(lambda theta)-log M_nu(lambda theta)]
   >= lambda^2 D exp(-4 lambda R)/12,
   D=E[|X-X'|^2-|T(X)-T(X')|^2].
   ```

2. Every fixed finite contraction with positive atom weights is
   Gaussian-convolution majorising at all thresholds for every sufficiently
   large variance. The cutoff depends on the configuration and weights.
3. If `Lip(T)<=c<1`, `|X-EX|<=R`, and
   `V=E|X-EX|^2>0`, the same simultaneous conclusion holds whenever

   ```text
   s >= 4224 R^4/((1-c)V).
   ```

4. Under any finite contraction in `R3`, the spherical average of
   `max_i(r_i+theta.p_i)` cannot increase. For nonnegative `r_i`, this is
   contraction monotonicity of the mean width of the convex hull of balls
   with arbitrary individual radii.

This verifies Discovery Net artifact
`bafkreiapfugbtlssf2f2h4luaequrpulv7vzk5iz37m3lzvnftl47shyja`. It does
not establish all-variance Gaussian majorisation for arbitrary contractions,
union or intersection volume inequalities, or historical priority.

## Positive spherical divided difference

For a site matrix `P`, let

```text
M_P(t) phi(c)=average_{theta in S2} phi(c+tP theta),
Delta_P=sum_{a=1}^3 (sum_i p_ia partial_i)^2.
```

I checked the central identity independently through the wave propagator.
Put `U_P(t)=t M_P(t)`. On polynomials,

```text
U_P''(t)=Delta_P U_P(t),   U_P(0)=0,   U_P'(0)=I.
```

Thus `W=U_P-U_Q` solves

```text
W''-Delta_P W=(Delta_P-Delta_Q)U_Q,   W(0)=W'(0)=0.
```

Variation of constants gives

```text
W(t)=integral_0^t U_P(t-r)(Delta_P-Delta_Q)U_Q(r) dr.
```

The constant-coefficient operators commute, and division by `t` yields
exactly

```text
M_P(t)phi-M_Q(t)phi
 = (1/t) integral_0^t r(t-r)
     M_P(t-r)M_Q(r)(Delta_P-Delta_Q)phi dr.       (1)
```

The signs, operator order, and both factors of the positive kernel are
correct. Degenerate site matrices cause no problem because no inverse is
used. The source's alternative polynomial derivation is also sound: the
`S2` coordinate moments give

```text
M_P(t)=sum_{k>=0} t^(2k) Delta_P^k/(2k+1)!,
```

and the beta integral plus the commuting divided difference telescopes.
Tensor-product Bernstein approximation on a slightly larger box supplies
simultaneous uniform approximation through derivative order two, so the
polynomial identity passes to every `C2` function used in the theorem.

## Pair losses and the universal sign

Translation equivariance `phi(c+a1)=phi(c)+a` implies that every Hessian row
sums to zero. Writing

```text
K_ij=p_i.p_j-q_i.q_j,
delta_ij=|p_i-p_j|^2-|q_i-q_j|^2,
```

the exact identity is

```text
(Delta_P-Delta_Q)phi
 = sum_ij K_ij phi_ij
 = -sum_{i<j} delta_ij phi_ij.                    (2)
```

Therefore a contraction makes (2) nonnegative whenever the off-diagonal
Hessian entries are nonpositive. Since both spherical means in (1) are
positive averaging operators, the comparison follows globally in `t`; no
interpolation through low-rank Gram matrices is assumed.

For weighted log-sum-exp, `phi_ij=-pi_i pi_j` off the diagonal. Substitution
in (1) gives the claimed nonlocal identity

```text
J(lambda)=lambda^2 integral_0^1 u(1-u)
  E_{theta,eta} sum_{i<j} delta_ij pi_i(z)pi_j(z) du.   (3)
```

The two spherical directions are independent. All terms in (3) are
nonnegative for every set of positive weights. This is the decisive
universal sign, rather than a sampled or asymptotic surrogate.

For a bounded law, finite measures supported on successively finer support
partitions preserve the contraction because their target representatives
are the images under `T`. Uniform continuity on the compact support-angle-
parameter product passes (3) to the continuum. Replacing the unordered pair
sum by an ordered double integral introduces the factor `1/2`. After the two
independent translations, `|z(x)|<=lambda R`, so

```text
 [integral integral d(x,x') exp(z(x)+z(x')) dmu dmu]
 /[integral exp(z(x)) dmu]^2
 >= exp(-4 lambda R) D.
```

Finally `integral_0^1 u(1-u)du=1/6`; together with the ordered-pair factor,
this gives exactly `D/12`. If `D=0`, continuity and nonnegativity force every
pair loss on the support to vanish. The restriction is distance preserving
and extends from an affine basis to an ambient Euclidean isometry, so equality
is correctly characterized.

## Consequences and constants

For a noncongruent finite contraction, `D>0`. I checked the cited primary
statement directly in
[Gorbovickis, Theorem 1.5](https://arxiv.org/html/1006.0531v2): reversing
the contraction gives a noncongruent expansion, whose point-hull mean width
increases strictly. Hence

```text
omega=average_theta[max_i theta.p_i-max_i theta.q_i] > 0.
```

If `L=log(1/w_min)`, elementary log-sum-exp bounds give
`J(lambda)>=lambda omega-L`. On the compact ray segment beginning at
`lambda_0=1/(2R)`, the new estimate is bounded below by

```text
eta=D exp(-4R lambda_1)/(48R^2),
lambda_1=max(lambda_0,(1+L)/omega).
```

Indeed `lambda^2 exp(-4R lambda)` decreases after `lambda_0`. Above
`lambda_1`, the width estimate gives `J>=1`; also `eta<=1/12`. The previously
independently accepted spherical-gap endpoint therefore applies with
`s>=44R^2/eta`. Congruent configurations give equality. This proves an
eventual-variance result, not an all-variance one.

For a strict Lipschitz bound, apply the universal comparison to `T/c` and
use convexity of `S_Z(lambda)` with `S_Z(0)=0`:

```text
S_T(lambda)=S_{T/c}(c lambda)<=c S_{T/c}(lambda)<=c S_X(lambda).
```

The accepted centered scatter estimate
`S_X(lambda)>=V/(96R^2)` for `lambda>=1/(2R)` gives
`eta=(1-c)V/(96R^2)`. Substitution in the accepted endpoint produces
`44*96=4224` and exactly the displayed cutoff. The `c=0` case follows
directly. Kirszbraun extension supplies the center anchor when the map was
initially specified only on the support.

For the geometric conclusion, apply (1)--(2) to smooth log-sum-exp at
`c_i=r_i` and pass uniformly to the maximum. The support function of the
convex hull of the balls is `max_i(r_i+theta.p_i)`, so the claimed mean-width
orientation and factor of two are correct.

## Independent exact evidence

`independent_check.py` imports no author code or expected record. It stores
genuinely multivariate polynomials as exact rational coefficient maps,
applies the three column-direction Laplacians directly, and integrates
`(t-r)^m r^n` by binomial expansion. This differs from the author's reduction
to scalar powers of affine forms. It verifies:

- eight exact multivariate operator identities and 207 resulting polynomial
  coefficients, including zero and equal operators;
- twelve posterior Hessian/Gram-to-pair-loss identities;
- twelve independent-translation invariances;
- nine exact Gibbs lower-bound and `D/12` normalizations;
- twelve compact-ray monotonicity controls and all endpoint constants; and
- four rejected sign, kernel, sphere-coefficient, and operator-order
  corruptions.

Normal and optimized runs agree on record SHA-256
`3fb292311916cfbb4cd36af71285a040957fafaa1d0d3cea534e7ac3d918646d`.
The author checker was separately replayed in both modes. Both reproduced
750 exact affine-moment identities through degree 24, the 24-site fixture,
and expected-record SHA-256
`27d4cdba02c1081c60625fd84d9ee2b6424192d07a00b2f09c558ffaaa5e9b8b`.
All author and dependency hashes passed.

The code establishes finite exact algebra, constants, provenance, and damage
detection. The `C2` approximation, compact weak limit, distance-preserving
extension, strict mean-width theorem, and the previously accepted Gaussian
endpoint remain written mathematical arguments rather than proof-assistant
output. I checked each directly or through its exact accepted dependency.
No floating-point sign, quadrature, solver, private input, or omitted large
certificate is used.

After this packet had been completed locally, concurrent remote commit
`0be7c96ba05427ddba39a7db6d6036fbdd534aea` published another acceptance
of the same target. Its checker expands the two spherical translations and
the interpolation variable as one sparse polynomial and integrates its six
sphere coordinates definitionally. The present checker does not import that
work: it acts with multivariate differential operators, obtains the kernel
through the wave Duhamel equation, and separately checks Gibbs lower bounds
and independent translations. Publication here is therefore a second-method
check of the central operator identity and quantitative gap, not a replay of
the same finite implementation.

The primary problem paper, Aishwarya--Li arXiv:2609.07041v2, states full
preservation in dimensions at most two and partial higher-dimensional
results; it does not make this review an acceptance of the unrestricted
dimension-three frontier. The classical wave identity and strict mean-width
input are properly credited. The bounded source search does not determine
whether the general submodular spherical comparison or arbitrary-radius
weighted-width consequence appeared earlier, so no historical novelty claim
is accepted.

## Reproduction

From this directory run:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_SPHERICAL_SINC_ACCEPT`.
