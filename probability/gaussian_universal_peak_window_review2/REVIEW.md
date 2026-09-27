# Independent acceptance: universal upper-density Gaussian hinge window

27 September 2026. Second-reviewer report on Discovery Net contribution
`bafkreif3zgq5t26tvdjfucgppkhufu53w35ipd256ukl77impaj7k7abzq`, source
commit [`9e18bbc050edb580004c4bef6d251e9238ad651f`](https://github.com/helgithorskarp/math_results/tree/9e18bbc050edb580004c4bef6d251e9238ad651f/probability/gaussian_universal_peak_window),
source tree `8334abd2b0992bd811bef224823777342653372d`.

## Verdict

**Accept.** For every bounded probability law in three dimensions, every
short support map and every positive Gaussian variance, the submitted proof
establishes

`H(u) >= 0` for `u >= exp(-2^-32)`.

It also establishes the stated strictness when the ordered mean squared-
distance loss is positive and the threshold lies below the target peak, the
all-hinge equality when that loss is zero, and the nonstrict extension to
arbitrary probability laws by truncation.

This accepts only a universal upper-density interval. It does not accept the
full dimension-three Gaussian-majorisation conjecture, sign any lower
threshold, or establish a new Kneser--Poulsen class or historical priority.

## Analytic audit

### Complete localization near a high mode

At a mode with `max Q=exp(-sigma)`, the posterior representation

`Q(z)=exp(-sigma-|z|^2/2)L(z)`, `L(z)=E_pi exp(z.Y)`

has `E_pi Y=0`. Cauchy--Schwarz gives

`E_pi(1-exp(-|Y|^2/2)) <= 1-exp(-sigma) <= sigma`.

Together with the submitted scalar estimate, this controls derivatives of
`L` through order five even if the posterior contains arbitrarily rare,
distant centers. Integration from the stationary point controls the first
derivative and `L-1`; the explicit log-partition coefficient sums
`1,2,6,26,150` then give the claimed `2^21 sigma` bound for derivatives of
`log L`.

The separate two-observation inequality is essential and correct. If
`V(z)<=delta`, both `Q(z)` and its modal value are at least `exp(-delta)`, so

`|z|^2 <= -8 log(2 exp(-delta)-1) <= 32 delta < 1/16`.

Thus the proof controls the complete high superlevel set, rather than only a
local component around one chosen mode.

### Quadratic chart and unrestricted marked midpoint

The integral Hessian field `B` satisfies the exact identity

`V(z)-sigma = z^T B(z) z/2`.

The matrix-square-root power series is valid because `||B-I||<=1/4`.
Differentiating it through order three yields the submitted chart estimates.
The contraction construction of the inverse chart covers every
`|y|<1/2`, while the lower Lipschitz bound makes it unique. Therefore

`V(Psi(y))=sigma+|y|^2/2`

parametrizes the entire sublevel set through level `delta`; it also proves
uniqueness of every mode whose value enters that interval.

For

`W_m=exp(2m.Psi+a-|m|^2)`,

direct differentiation gives

`Delta W_m/W_m = 4|P^T m|^2 + 2m.(Delta Psi+2P grad a)
                 + |grad a|^2 + Delta a`.

The positive quadratic term cannot be discarded. Completing the square and
using the exact worst-case budget `epsilon=1/64` gives

`Delta W_m >= -36 W_m`

uniformly for every `m` in six-dimensional space. I independently checked
the inverse, log-Jacobian, Hessian, trace, and square-completion constants;
the final penalty is exactly `9+27=36`. This closes the proof's main trust
boundary for marked centers arbitrarily far from a high mode.

### Spherical comparison and coarea sign

Spherical averaging in dimension six converts the preceding inequality to

`S''+5S'/r+36S>=0`.

The normalized regular equality solution is

`b(6r)=sum_k (-1)^k (6r)^(2k)/(4^k k! (3)_k)`.

For `6r<=1`, its alternating series gives `b>=11/12` and
`-(6r)b'/b<=2/11`. The Wronskian comparison therefore yields

`4S+rS' >= (42/11)S > 0`.

Under `w=sigma+r^2/2`, six-dimensional polar volume contributes `r^5 dr`
and `dw=r dr`; hence the marked-pair level density is proportional to
`r^4S`, not `r^5S`. Its derivative is positive with the displayed
`42/11` margin. The density and derivative vanish respectively to orders two
and one at an entering mode, so extension by zero is `C1` and creates no
mode atom or boundary term.

### Lifted moments and local Abel inversion

I rederived the normalization independently. With `k=j+2`, integrating a
hinge against `u^j` contributes `1/[k(k-1)]`. The normalized three-
dimensional `k`-energy contributes `k^-3/2`; differentiating the affine
lifted variance contributes `(k-1)/4`. The endpoint coefficient is therefore

`1/(4 k^(5/2))`.

On the marked side, six-dimensional Gaussian integration contributes
`k^-3`; multiplication by the submitted `sqrt(k)/4` gives the identical
coefficient. Thus equation (20) has the correct power and factor.

The half-integral has Laplace multiplier `k^-1/2`. After multiplying by
`exp(-2l)` and pushing under `u=exp(-l)`, equality at every integer
`k>=2` gives equality of all polynomial moments of finite signed measures on
`[0,1]`; polynomial density justifies the measure identity. Composing the
normalized half-integral twice uses
`Beta(1/2,1/2)/pi=1`. Differentiation is legitimate because the local
coarea density is `C1` and vanishes at zero. This gives exactly

`H(exp(-l)) = C6 exp(-l)/(4 sqrt(pi))
               integral_0^l A'(w)/sqrt(l-w) dw`.

Only values `w<=l<=delta` enter, so irregular lower levels cannot contaminate
the local conclusion.

### Strictness, equality, and unbounded laws

When `D>0`, the nonnegative pair deficit is positive on a set of pairs of
positive measure. If the target peak exceeds the tested threshold,
continuity of the lifted peak supplies a positive-length time interval on
which the strict marked-pair derivative enters the Abel integral. This proves
the stated strictness.

If `D=0`, the pair deficit vanishes almost surely, so every hinge moment is
zero. Continuity and polynomial density then force every hinge gap to vanish.
Finally, normalized restrictions to growing input balls converge in total
variation; pushforward and Gaussian convolution do not increase that error,
and the hinge is `L1`-Lipschitz. The same universal cutoff therefore passes to
arbitrary laws without imposing a moment condition.

## Independent exact audit

[`independent_audit.py`](independent_audit.py) imports no reviewed code. It
uses exact `fractions.Fraction`, explicit integer-partition multiplicities,
and an independently organized dimension/transform calibration.

Run with CPython 3.11 or later from the repository root:

```sh
python3 -B probability/gaussian_universal_peak_window_review2/independent_audit.py
```

It returns `INDEPENDENT_UNIVERSAL_PEAK_AUDIT_PASS` and reproduces:

- `delta=1/4294967296`, `epsilon=1/64`;
- log-derivative coefficient sums `1,2,6,26,150`;
- matrix-square-root series budget `44/27<8`;
- inverse-chart factors `6` and `539/32<17`;
- unrestricted-midpoint Helmholtz penalty `36`;
- radial logarithmic derivative lower bound `-2/11` and coarea derivative
  margin `42/11`;
- coarea power four in dimension six;
- matching endpoint and marked Laplace exponents `-5/2`, each with coefficient
  `1/4`;
- the centered Abel calibration coefficient `1/4` and modal vanishing orders
  two and one.

The author audit also passed normally and under `-O`. Exact SHA256 values at
the reviewed bytes are

- `PROOF.md`: `2ce2d513e40f94fb51ed26a9f96ec5bfc9d76637dfa37989bd22fc48461ca1ef`;
- `README.md`: `e85ab442f50ccf924d7a88769b4ca9dce7887a015cb774c4219f88bf673e2f5d`;
- `audit.py`: `83f9081dad2cf67f8e55c47f76423f7a5fb3e4876ca264e18e5e9cf6ce2c7fb2`.

The exact cited cubic-region source and its accepted review were also pinned:
their proof/report hashes are respectively
`977564a74628a7136c504f8bdbafe3653c7967249b8b8393dd6751ba5e56ddaa`
and `c2e9cd2732803254bb784803f51a266cf31dcede5bbe919e0a31f9967fb84033`.
The present proof rederives the localization estimates it needs rather than
importing a beta sign.

## Trust boundary and remaining gap

The exact programs verify constants, combinatorial coefficients, dimensions,
and transform normalization. They do not formalize the inverse-function,
coarea, differentiation-under-the-average, moment-uniqueness, or truncation
arguments; those were checked as written mathematics above. No Gaussian
quadrature or finite sampling can certify the universal theorem, and none is
used.

Thresholds below `exp(-2^-32)` remain unsigned. The constant is sufficient,
not claimed sharp. The result supplies no all-threshold theorem and no
counterexample. Source-level novelty and historical priority remain
uncertain.
