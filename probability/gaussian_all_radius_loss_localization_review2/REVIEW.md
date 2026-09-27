# Independent acceptance: all-radius loss-relative Gaussian localization

## Target and verdict

- Discovery Net artifact:
  `bafkreibivrqpvaay3jjrqcg3ezx4u64efeszvrtcyr6k5jtlh4lexfghqm`
- Exact reviewed source commit:
  `1104fcce0bfcf2d9cb16f70daa45c361f54c977c`
- Reviewed source:
  [`../gaussian_all_radius_loss_localization`](../gaussian_all_radius_loss_localization/)

**Accept with high confidence in the stated scope.** Let `X` be a bounded
law in `R3`, let `T` contract its support, and convolve both endpoint laws
with a Gaussian of variance `s`. Suppose

```text
|X-E X| <= R sqrt(s),      Cov(X)/s >= kappa I_3,
```

where `R>=1` is an integer and `kappa>0`. For the normalized favorable hinge
gap `H` and ordered squared-distance loss `d`, the proof establishes an
explicit modulus

```text
|H(u)-H(v)|
 <= d[2T0 2^(-L/2)+K_L |u-v|^(1/r)]
```

for every `L>=0` and `u,v` in `[0,1]`, with the constants stated in the
source. The infimum over `L` tends to zero with `|u-v|`. This holds at every
bounded radius; the actual covariance floor is the material replacement for
the earlier small-radius hypothesis.

Together with the independently accepted same-pair cubature, the proof also
gives

```text
||H_mu-H_nu||_infinity
 <= d[2E_(N,L)+B_(N,q)(R^2)],
```

where `nu` uses at most `2 binom(2q+3,3)-1` original pairs. For fixed
`R,kappa` and relative tolerance, the degree and atom budget are independent
of how small `d` is.

This is an unsigned approximation theorem. It proves no new Gaussian hinge
sign, does not evaluate the strict screw, does not remove the covariance
floor, and gives no new Kneser--Poulsen case. Historical priority for the
particular loss-relative strip argument is uncertain.

## Procrustes loss scaling

Scale to `s=1`, center the endpoint laws separately, and choose the
orthogonal Procrustes alignment so that `A*B` is symmetric positive
semidefinite. Put `h=Y-X`, `M=E|h|^2`, and

```text
Delta=|X-X'|^2-|Y-Y'|^2,   D=E Delta.
```

Double centering `Delta` gives `-2(X.X'-Y.Y')`. Hence, with
`F=||AA*-BB*||_HS^2`, orthogonal projection in `L2(mu x mu)` gives

```text
F <= E Delta^2/4.
```

Writing `U=A+B` and `V=A-B`, the Procrustes symmetry gives the exact identity

```text
F=(1/2)tr(U*U V*V)+(1/2)tr((U*V)^2).
```

Here `U*U>=A*A>=kappa I`, while the second trace is nonnegative. Thus
`F>=kappa M/2`. Since `0<=Delta<=4R^2`,

```text
M <= E Delta^2/(2kappa) <= 2R^2 D/kappa.
```

This also closes the zero-loss case: `D=0` forces `M=0` after alignment, so
the endpoint laws are isometric and `H=0`. No division by loss is needed.

## Straight-path posterior identity

The aligned straight interpolation `Z_t=X+t(Y-X)` remains in `B(0,2R)`;
it is not asserted to be a contracting motion. If

```text
q_t(z)=E exp(-|z-Z_t|^2/2),
v_t(z)=E_posterior h,
```

then differentiation of the posterior gives

```text
div v_t=(1/2)E_(pi,pi)(Z_t-Z'_t).(h-h').
```

The pair identity

```text
-2(Z_t-Z'_t).(h-h')
 = Delta+(1-2t)|h-h'|^2
```

therefore converts differentiation of the hinge into

```text
H(u)=(C u/4) integral_0^1 integral_(q_t>u) G_t(z) dz dt.
```

The sign-changing coefficient `1-2t` is retained; the proof uses this
formula only for absolute estimates and never treats the straight path as
monotone. Positive levels of a bounded Gaussian mixture are null because
the density is nonconstant real analytic and decays at infinity. Regular
level approximation, common Gaussian envelopes, and dominated convergence
justify critical levels and integration in `t`.

On `q_t>=a`, division by the squared posterior normalizer gives

```text
|G_t| <= (D+2M)/a^2 <= Lambda D/a^2.
```

The alternative global posterior bound

```text
|G_t(z)| <= Lambda D exp(4S|z|+S^2),  S=2R,
```

also has the correct exponent: each denominator is bounded below by
`exp(-S|z|-S^2/2)` and the pair numerator is bounded above after removing
the common Gaussian factor.

## Level-strip interpolation

For `q(z)=E exp(-|z-Z|^2/2)` with `|Z|<=2R`, the decisive new estimate is

```text
|{u<=q<=v}| <= 48 B^3 (4(v-u)/a)^(1/r),
a=2^-L, B=2R+ceil(sqrt(2(L+1))), r=32B^2-1.
```

The strip lies in `[-B,B]^3`. On each coordinate slice, let `E` have length
`b`, and choose `r+1` points by equal restricted-Lebesgue quantiles. Because
the restricted measure is dominated by ordinary length,

```text
|x_i-x_j| >= |i-j|b/r.
```

Lagrange interpolation of `Q-u` at those points gives

```text
|P(B)| <= (v-u)(12B/b)^r.
```

The coefficient calculation is exact: the reciprocal factorial sum is
`2^r/r!`, and `r!>=(r/e)^r` with `e<3` supplies the constant 12.

The slice is a subprobability mixture of translated one-dimensional
unnormalized Gaussians. Fourier inversion gives

```text
sup_x |Q^(2m)(x)| <= E G^(2m)=(2m)!/(2^m m!),
m=16B^2, 2m=r+1.
```

Consequently the order-`2m` remainder at the common anchor is at most

```text
(2B^2)^m/m! <= (3/8)^m <= 2^-m <= a/4.
```

Meanwhile every slice satisfies `Q(B)<=a/2`, whereas `u>=a`, so
`|Q(B)-u|>=a/2` and therefore `|P(B)|>=a/4`. Rearranging gives the slice
length bound, and integration over the remaining square contributes
`4B^2`. This argument remains valid at critical levels; it uses measure
quantiles rather than a gradient lower bound.

The independent checker verifies 391 exact quantile-separation, Lagrange,
and monomial-reproduction controls, together with 64 Gaussian moment and
factorial-remainder checks. The universal Fourier and measure arguments are
human-audited, not inferred from these finite cases.

## Middle and low-threshold joins

Subtracting the posterior formulas at `a<=u<v<=1` splits the change into a
common superlevel term and the thin strip. The common-domain volume is at
most `8B^3`; the strip estimate above and the posterior bound give

```text
|H(u)-H(v)|
 <= 14 Lambda D B^3 a^-2 (4(v-u)/a)^(1/r)
 <= 56 Lambda D B^3 a^-3 |u-v|^(1/r).
```

For the low-threshold end, `{q_t>u}` lies in a ball of radius
`S+sqrt(2 log(1/u))`. Integrating the global posterior envelope and using

```text
4S sqrt(2 ell) <= ell/4+32S^2
```

leaves a factor `sqrt(u)`. The polynomial radial factor is bounded by
`4(S+3)^3`, and `e<4` yields the stated conservative `2^(296R^2)` constant.
Inserting the level `a` joins low and middle regimes. The resulting tail
term is an absolute error, not a signed endpoint theorem.

## Reconstruction, cubature, and schedules

The Bernstein--Durrmeyer reconstruction has the exact representation
`P_N(u)=E H(U)`, with `J~Bin(N,u)` and
`U|J~Beta(J+1,N-J+1)`. Direct polynomial evaluation gives

```text
E(U-u)^2
 =2[1+(N-3)u(1-u)]/[(N+2)(N+3)] <=1/(N+2).
```

Jensen applied to the Holder term proves the reconstruction estimate. The
checker independently reconstructs this as a polynomial identity for every
`0<=N<=48`, rather than sampling values of `u`.

The accepted same-pair cubature preserves the source mean, covariance,
centered support radius, and `D`, and retains a contraction on the selected
original pairs. Thus both the original and sparse laws satisfy the same
localization hypotheses. The nonnegative Bernstein basis transfers the
accepted beta-row error, and two reconstruction errors give the factor
`2E_(N,L)`.

The explicit order of choices—first `L`, then `N`, then `q`—is correct. The
displayed symbolic schedule makes each reconstruction term at most
`zeta/8` and the cubature term at most `zeta/2`. Its sufficient degree
guards hold without materializing the enormous integers. The checker audits
180 exact schedules over multiple radii, covariance floors, and tolerances.
The resulting `2^(O(A^2))` statement is an existence bound, not a practical
enumeration algorithm.

## Computation and trust boundary

The author checker passes normally, under optimized Python, and against its
complete SHA-256 manifest. Its finite scope is accurately stated.

The new [`independent_check.py`](independent_check.py) imports no author
module and pins all nine files at the exact reviewed commit. It records:

- 196 exact beta-variance polynomial controls;
- 391 quantile/Lagrange controls;
- 64 Gaussian derivative and remainder controls;
- 192 localization-constant checks;
- 1,280 straight-path pair identities;
- four independent rational Procrustes/loss cases; and
- 180 symbolic whole-curve budget checks.

Its status is `INDEPENDENT_ALL_RADIUS_LOCALIZATION_REVIEW_PASS`, with
exact-state SHA-256
`f3fbfd9d7f9a304587daea11392fa3fdec9e29777c38933b340f81f42fd500a1`.

These computations guarantee exact source identity and finite algebra. They
do not formalize Procrustes operator inequalities, Fourier inversion,
analytic level-set nullity, regular-value limits, or the universal cubature
theorem; those are independently audited written mathematics. No Gaussian
quadrature or hinge sign is computed. Consumers must retain the actual
covariance floor and separately prove any required low, middle, and high
sign margins. The unrestricted `R3` frontier remains open.
