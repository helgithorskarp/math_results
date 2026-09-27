# Independent review: loss-relative spherical-to-Gaussian transfer

## Verdict

**Accept for correctness in the stated conditional scope; novelty remains
uncertain.**  At the exact graph-cited source commit
`e949d9f482f3bb61b19f6d8ecc205561eaed0a80`, the proof establishes, for a
probability supported in a radius-`R` ball and every contraction,

    |B_s(lambda)-J(lambda)|
      <= (D/s)[1+25 lambda R(1+lambda R)^2 exp(4 lambda R+1)]

when `s>=64R^2` and `lambda R>=1/2`.  Here `D` is the mean
squared-distance loss, `J` is the spherical log-moment gap, and `B_s` is the
normalized physical Gaussian hinge.  The law may be diffuse and no positive
loss floor, atom count, minimum weight, or covariance assumption is used.

This review verifies Discovery Net contribution
`bafkreibblggn3ysibhslp7rdh5websr6jdcaiduc4omw4p5ud7uul45hsi` at height
6376.  The theorem is a loss-relative approximation and a **conditional**
sign-transfer interface.  It does not prove the required spherical margin or
overlapping low tail for arbitrary contractions, an unconditional positive
map class, unrestricted dimension-three Gaussian majorisation, or a new
Kneser--Poulsen result.

## Scaling and loss normalization

Separate translations of the two endpoint clouds preserve their hinge
profiles.  Their contributions to each spherical log moment are linear in
the direction and integrate to zero, so `J` is also unchanged.  Scaling by
`R` sends

    epsilon=R^2/s,  lambda_scaled=lambda R,
    D_scaled=D/R^2.

The product `lambda s^2 b_s(lambda)` in the denominator of `B_s` is
unchanged after accounting for density scaling, and
`epsilon D_scaled=D/s`.  Thus it is enough to treat `R=1`,
`epsilon<=1/64`.

For the lifted interpolation
`Z_t=(sqrt(1-t)X,sqrt(t)TX)`, the pair-loss measure
`Delta d(mu tensor mu)/D` is a probability when `D>0`.  Bounded support gives
the stated uniform derivative estimates for the one-point log transform
`m_epsilon` and pair ratio `K_epsilon`.  In particular, differentiating
`log K` makes the bounds transparent: the first `p` derivative has range at
most four, the second lies in `[-2,4]`, the epsilon derivative lies in
`[-1,1]`, and the mixed derivative is at most two by the elementary
range-covariance inequality.  Hence

    |K'|<=4K, |K''|<=20K,
    |partial_epsilon K|<=K, |partial_epsilon K'|<=6K.

These estimates retain the normalized pair-loss measure and never divide by
an individual pair loss.

## Radial graph and coarea normalization

At unit noise the potential has Hessian between `(1-epsilon)I` and `I`, so
it has one mode.  At every level `w>=8epsilon`, the ball of radius
`sqrt(2w)-sqrt(epsilon)` lies inside the superlevel set and extends beyond
the center ball.  Outside that center ball every Gaussian summand decreases
strictly along a ray.  Consequently each ray has exactly one outer boundary;
no disconnected component is dropped.

With `p=sqrt(epsilon)r` and `q=sqrt(2epsilon w)`, direct substitution gives

    q^2=p^2-2epsilon m_epsilon(p),
    |p-q|<=epsilon,
    b=p-epsilon m_epsilon'(p),
    dp/dq=q/b.

The radial Jacobian on `S^5`, whose ordinary area is `pi^3`, then gives

    A_t(w)=(D/epsilon)F_epsilon,t(q),
    A_t'(w)=D F_epsilon,t'(q)/q.

Converting the accepted Abel identity to `B_(1/epsilon)` multiplies it by
exactly `sqrt(epsilon)/(32sqrt(2)pi^3 lambda)`.  Substitution of the radial
formula therefore yields the coefficient
`D/(32pi^3 lambda)` used later.  This dimensional normalization agrees at
both endpoints of the scaling argument.

## Derivative comparison

Writing `a=p/q`, `b_0=b/q`, and `z=epsilon/q<=1/4`, differentiation gives

    F_epsilon'(q)
      = integral [q^4 R_1 K_epsilon' + q^3 R_2 K_epsilon] dtheta,

    R_1=a^5/b_0^2,
    R_2=5a^4/b_0^2-a^5(1-epsilon m_epsilon'')/b_0^3.

The domain has `1-z<=a<=1+z` and `1-2z<=b_0<=1+2z`.  The horizontal and
vertical paths in `(p,epsilon)` give

    |K_epsilon(p)-K_0(q)|<=5epsilon exp(4q+1),
    |K_epsilon'(p)-K_0'(q)|<=26epsilon exp(4q+1).

Combining these with the coefficient envelopes produces exactly

    |F_epsilon'-F_0'|
      <= pi^3 epsilon exp(4q+1)(440q^2+705q^3+338q^4)
      <=800pi^3 epsilon exp(4q+1)q^2(1+q)^2.

The independent checker recasts all coefficient bounds as univariate
polynomial inequalities.  On this domain `R_1` increases with `a` and
decreases with `b_0`.  The epsilon-free part of `R_2` is
`a^4(5b_0-a)/b_0^3`; its derivatives have fixed signs because
`4b_0-a>0` and `3a-10b_0<0`.  Thus endpoint substitution is complete.
After clearing positive denominators, nonnegative Bernstein coefficients on
`z in [0,1/4]` certify the bounds `13,70,80,440,25` over the whole interval,
not a sampled grid.  Replacing 70 by 40 is rejected.

The Abel kernel integral
`integral q^2/sqrt(lambda^2-q^2)=pi lambda^2/4` gives the outer error

    <=(25pi/4)D epsilon lambda(1+lambda)^2 exp(4lambda+1),

which is safely bounded by the displayed coefficient 25.

## Both modal prefixes

The proof separately controls the actual coarea prefix and the limiting
spherical prefix.  The accepted modal derivative estimate, together with
`epsilon<=1/64`, gives

    |A_t'(w)|<=90pi^3 epsilon D w,  0<=w<=8epsilon.

The kernel and normalization yield a physical-prefix coefficient
`180/sqrt(2)`.  The source rounds this upward to 256; independently,
`180^2<2*128^2` shows that 128 already suffices.  The limiting bound
`|F_0'(q)|<=16pi^3q^3` contributes 64.  Thus the independent calculation
even gives

    (128+64)D epsilon^4/lambda^2
      <=(3/1024)D epsilon,

while the source's claimed bound is the weaker but valid
`(5/1024)D epsilon`.  No moving-mode boundary or small radial interval is
omitted.

Adding this prefix to the outer estimate yields the stated constant
`C(lambda)`.  The earlier absolute spherical-tail theorem identifies the
fixed-`lambda` limit as `J(lambda)`, while the present bounds identify the
same limit with the time-averaged `F_0'` integral.  This justifies the exact
representation used in the subtraction.  Time averaging is retained; the
argument asserts no sign for an individual pair, ray, or interpolation time.

When `D=0`, continuity makes all support-pair losses zero.  The restricted
map is an isometry, so the physical hinge curve vanishes.  The prior absolute
limit then gives `J=0`, handling the case in which the normalized pair-loss
measure is undefined.

## Conditional sign consequence

If `J(lambda)>=eta D/R^2` on `lambda R in [1/2,A]`, the theorem and
`s>=2R^2C(A)/eta` leave at least half that normalized margin.  This covers
thresholds from `C_s exp(-A^2s/(2R^2))` through
`C_s exp(-s/(8R^2))`.  The accepted high-noise window begins at
`C_s exp(-9s/(64R^2))`; since `9/64>1/8`, the ranges overlap.  A separately
proved low tail reaching the first cutoff would then close the curve.  The
source correctly states both the spherical margin and this tail overlap as
premises rather than conclusions.

For the two-point normalization control, differentiating with respect to
the squared contraction radius and using `tanh x>=x exp(-4)` gives

    J(lambda)>=D lambda^2 exp(-4)/12>=D/3888

on `[1/2,2]`.  The rational estimate `C(2)<8857351` makes `2^37` a common
variance for every nonzero loss, while `2^36` is insufficient for this
particular coarse budget.  The ratio of the Gaussian error bound to the
spherical lower bound is exactly `2152336293/8589934592`, independent of
loss; the checker verifies this down to radii `1-2^-128`.

## Reproduction and trust boundary

The target checker passed in ordinary and optimized CPython, both outputs
matched `EXPECTED.json`, and all five manifest entries passed.  The
independent checker imports no target module and pins the five target files
plus the five proof dependencies.  It performs 648 exact dual-number
chain-rule evaluations, supplies seven full-interval Bernstein polynomial
certificates, sharpens the modal-prefix slack as above, verifies the overlap
and two-point budget, and rejects two damaged constants.

Reproduce with standard-library Python 3.11 or later:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Expected status: `RELATIVE_SPHERICAL_TRANSFER_INDEPENDENT_ACCEPT`.

The checker guarantees the exact algebra and constant envelopes.  The
arbitrary-law coarea formula, radial-graph argument, limit exchange, and use
of the accepted dependency theorems remain audited written mathematics, not
a formalization or inference from finite samples.  The qualitative
spherical limit and coarea normalization are prior results.  No exhaustive
historical-priority determination is made for the new loss-relative compact
parameter estimate.
