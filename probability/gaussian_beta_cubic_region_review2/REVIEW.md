# Independent acceptance: universal cubic Gaussian beta region

## Target and verdict

- Discovery Net artifact:
  `bafkreihnc2qyimyalgs7zf26xdggsaufo22o7oivqlethsdif6ttlhsuta`
- Exact reviewed source commit:
  `45dc3e6b3d582426e3238e9529f5008450a7054d`
- Reviewed source:
  [`../gaussian_beta_cubic_region`](../gaussian_beta_cubic_region/)

**Accept with high confidence in the stated scope.** For every bounded
probability law on `R3`, every 1-Lipschitz image, every Gaussian variance,
and all integers `k>=1`, `j>=0`, the proof establishes

```text
j+2 >= 30720 k^3  ==>  b_(j+k,j) >= 0.
```

The sign is strict unless the support map preserves every pairwise distance.
The hypotheses contain no radius, atom-count, weight-floor, covariance, loss,
or noise restriction. In particular, order eight is covered for every
`j>=15728638`.

This is an unbounded all-order region, but it is not the complete beta array.
The covered beta measures concentrate near `u=1`; they do not resolve all
interior thresholds, full Gaussian majorisation, or any new
Kneser--Poulsen consequence. The constant is sufficient rather than optimal.
Historical priority remains uncertain.

## Appell polynomials and Gamma calibration

The generating identity

```text
sum h_k(v) z^k/k! = exp(vz) sqrt(1-z)
```

gives the displayed coefficients. For `k>=1`, every nonleading coefficient
is strictly negative. The falling-factorial estimate

```text
|(1/2)_[ell]| <= (ell-1)!/2
```

implies `h_k(v)>=v^k/2` for `v>=2k` and
`P_k(v)=2v^k-h_k(v)<=(v+k)^k`. The derivative identities
`h'_k=k h_(k-1)` and `P'_k=kP_(k-1)` are correctly normalized.

For `V~Gamma(3,1)`, multiplying the generating function by
`E exp(zV)=(1-z)^-3` shows that

```text
G_k(c)=E h_k(c+V)=E(c+Gamma(5/2,1))^k > 0.
```

The coefficientwise comparisons with the raw Gamma(3) moments yield

```text
E P_k(c+V)  <= (2k+1)G_k(c),
E P'_k(c+V) <= (2k-1)G_k(c).
```

The independent checker also derives `h_k` from the real-order differential
operator:

```text
h_(n+1)=(x+n-1/2)h_n-xh'_n.
```

This independently aligns the polynomial family used in the analytic
localization with the family produced by differentiating the replica order.

## One-crossing minorant and tail

For `r>=30720k^3`, set

```text
tau=768k^2/r <= 1/(40k),
F=h_k-tau(3P'_k+2P_k).
```

Its leading coefficient is positive and every lower coefficient is negative,
so it has exactly one positive zero. The Gamma comparisons give

```text
E F(c+V) >= [1-tau(10k-1)]G_k(c) >= 3G_k(c)/4
```

uniformly for `0<=c<=2k`. On the tail `v>=32k`, the estimate
`F<=h_k<=P_k<=(v+3k)^k<=2^k v^k` gives the stated incomplete-Gamma bound.
Using only `e>2`, its ratio to `G_k(c)` is at most
`2^(3-12k)<=1/512`. Therefore

```text
E[F(c+V) 1_(V<=32k)] >= G_k(c)/2.
```

This truncation argument uses an upper bound on the signed tail, which is the
correct direction even if the tail itself is negative.

For a displacement vector `a`, the spherical average

```text
W_a(v)=E_theta exp(sqrt(2v) a.theta)
```

has a nonnegative even-power series and is nondecreasing. Multiplying a
function with one negative-to-positive sign change by such a weight cannot
decrease its signed integral below the weight at the crossing times the
unweighted integral. Since `W_a>=1`, the positive `G_k(c)/2` margin survives
every displacement. This closes the noncentral trust boundary; no bound on
the marked pair midpoint is being assumed.

## Uniform localization for arbitrary mixtures

Let `z0` be a mode of the bounded location mixture `Q`. In the nontrivial
case, its posterior has mean zero and

```text
Q(z0+sqrt(s/r)x)=Q(z0) exp(-v/r)L(x),
v=|x|^2/2,  L(x)=E_pi exp(x.Y/sqrt(r)).
```

The crucial estimate is genuinely uniform over rare and distant mixture
components. For scalar `y` and `a>=0`,

```text
y^2 exp(-y^2/2+ay) <= 2 exp(a^2)(1-exp(-y^2/2)).
```

It follows from `ay<=y^2/4+a^2` and `t<=sinh(t)`. Applying the exponential
Taylor remainder under the mode posterior gives

```text
0 <= L-1 <= a^2 exp(a^2)(exp(sigma)-1),
0 <= d(x)=r log L(x) <= 24kv/r
```

on `v<=32k`. The constant guard makes `a^2<=1` and `sigma<=1`.

The separate two-observation inequality

```text
Q(z)+Q(z0) <= 1+exp(-|z-z0|^2/(8s))
```

is pointwise in each center before averaging. If the derivative polynomial is
negative, both mixture values exceed `exp(-2k/r)`. Hence
`v<32k`, so every possible negative contribution is inside the ball where
the posterior estimate applies. No log-concavity or covariance floor is used.

On that ball, with `w=c+v`, `d=r log L`, and
`Lambda=L^(r-2)`, the monotonicity of `P_k,P'_k` gives

```text
Lambda h_k(w-d)
 >= h_k(w)-3dP'_k(w)-2dP_k(w)
 >= F(w).
```

The proof correctly controls both the shifted polynomial argument and the
power weight. Outside the ball the original integrand is already
nonnegative.

Completing the two marked Gaussian squares leaves the radial density
`exp(-v)`, the arbitrary tilt `exp(a.x)`, and the factor `Lambda`. Polar
coordinates in `R6` therefore reduce exactly to the Gamma(3) estimate above.
This proves the strictly positive averaged Gaussian-mixture lemma for every
pair of marked centers.

## Real-order lift and beta signs

For the six-dimensional interpolation, the center velocity is `A_t Z` with

```text
A_t=diag(-I/[2(1-t)], I/[2t]).
```

The posterior covariance identity gives
`M_t/q_t^2=-4 tr(A_t Sigma)`. Direct differentiation of the moving Gaussian
kernel and spatial integration by parts then yield, for every real `r>1`,

```text
partial_t integral q_t^r
 =(r-1)/(4s) integral q_t^(r-2)M_t.
```

The singular trace terms cancel inside this exact identity. Working first on
`[eta,1-eta]` is legitimate; bounded centers give integrable endpoint
velocities, while `M_t<=delta_max q_t^2` supplies a uniform final integrand.

At either endpoint, the three unused Gaussian coordinates contribute
`r^-3/2`. Combining this with the hinge Mellin identity gives

```text
a(r)=sqrt(r) C6/(4s) integral_0^1 integral q_t^(r-2)M_t.
```

No fractional-replica interpretation is required. Differentiating this real
identity `k` times produces exactly

```text
(-1)^k a^(k)(r)
 = r^(1/2-k) C6/(4s)
   integral q_t^(r-2)M_t h_k(-r log q_t).
```

Bounded Gaussian envelopes justify every logarithmic derivative and
integration exchange on compact real-order intervals. Applying the averaged
mixture lemma to each marked pair makes this nonnegative for
`r>=30720k^3`, and strictly positive whenever the mean pair loss is positive.

Finally, the exact `k`-fold fundamental-theorem identity converts the
alternating values `a(j+2+ell)` into the beta coefficient
`b_(j+k,j)`. The condition on `j+2` covers the whole integration cube. If the
mean loss is zero, continuity on the support forces every pair loss to vanish;
otherwise relative support neighborhoods give positive mean loss and strict
sign.

## Independent computation and trust boundary

The author checker passes normally, under optimized Python, and under its
complete SHA-256 manifest. Its finite scope is accurately stated.

The new [`independent_check.py`](independent_check.py) imports no author
module. It pins seven exact source/dependency files and records:

- two independent constructions of `h_k` through order 32;
- 160 coefficientwise Gamma comparison controls;
- 448 exact constant and one-crossing minorant controls;
- a formal multivariate proof of the Gaussian product completion; and
- 440 exact Mellin-to-beta checks on rational test functions.

Its status is `INDEPENDENT_CUBIC_BETA_REGION_REVIEW_PASS`, with exact-state
SHA-256 `dfb6e1824b2c02d2210a3475c5b8df477117888d8754c3173cf1876d64d5a38a`.

These computations certify exact algebra and source identity, not the
universal analytic quantifiers. The mode-posterior estimate, one-crossing
rearrangement, real-order integration by parts, endpoint limits, and strictness
are the independently audited mathematical arguments above. This is not a
proof-assistant formalization, and no scalar countermodel or prior finite-row
result is treated as proof of the new region.
