# Independent review: uniform Lipschitz Gaussian endpoint

## Verdict

**Accept in the stated high-variance, strong-contraction scope.** At source
commit `ba0c239ecafa9d02a611dde4960ca3682e9adc17`, let `X` be any bounded
probability law on `R^3` with

```text
|X-E X| <= R,                 V=E|X-E X|^2>0,
27|T(x)-T(x')|^2 <= q^2|x-x'|^2,     0<q<1.
```

Then every Gaussian-convolution hinge comparison has the favorable sign,
simultaneously for every density threshold, whenever

```text
s >= 4224 R^4/((1-q)V).
```

In particular, every map of Lipschitz constant at most `1/6` is covered for
`s>=33792R^4/V`, by taking `q=7/8`. This verifies Discovery Net artifact
`bafkreicig6auyae5d2ofi6rkpoqdkoij34sb6pra2ytn7xbqfyrsnsa7cq`.

This does **not** prove the unrestricted dimension-three conjecture, weak
contractions, the same family at all variances, or a new Kneser--Poulsen
consequence. The constants are sufficient and are not claimed sharp.

## Universal spherical comparison

For a bounded law `Z` in `R^d`, write

```text
S_Z(lambda)=integral_S log E exp(lambda theta.Z) d sigma(theta),
A_Z(v)=E cosh(v.(Z-Z')).
```

I checked the independent-copy symmetrization carefully. Independence gives
`A_Z(v)=M_Z(v)M_Z(-v)`, and changing `theta` to `-theta` in the spherical
average yields the exact identity

```text
2S_Z(lambda)=integral_S log A_Z(lambda theta) d sigma(theta).
```

For an orthonormal frame `e_1,...,e_d`, convexity of
`u -> cosh(sqrt(u))` gives

```text
F_X(lambda):=E cosh(lambda|X-X'|/sqrt(d))
 <= (1/d) sum_j A_X(lambda e_j).
```

Every `A_j>=1`, so its arithmetic mean is at most `product_j A_j`.
Taking logarithms and averaging frames, whose individual vectors all have
the normalized spherical marginal, proves

```text
log F_X(lambda) <= 2d S_X(lambda).
```

If `|Y-Y'|<=L|X-X'|`, Jensen for `log`, radial domination, convexity of
`log cosh` at zero, and concavity of `z^alpha` with
`alpha=L sqrt(d)<=1` give

```text
S_Y(lambda)
 <= (1/2) log E cosh(lambda L|X-X'|)
 <= (alpha/2) log F_X(lambda)
 <= d^(3/2)L S_X(lambda).
```

All inequality directions and dimension factors are correct. In dimension
three the pair hypothesis gives `L<=q/sqrt(27)`, hence

```text
J(lambda):=S_X(lambda)-S_Y(lambda) >= (1-q)S_X(lambda).
```

This is an averaged analytic statement. It does not assert pointwise
positivity of a conditional replica kernel or replace the sphere by a finite
mesh.

## Scatter gap and endpoint transfer

Center `X`. For `Z=theta.X`, the MGF is nondecreasing on nonnegative
parameters because

```text
d/dlambda E exp(lambda Z)=E[Z(exp(lambda Z)-1)]>=0.
```

At `lambda_0=1/(2R)`, `|lambda_0 Z|<=1/2`. The elementary bounds

```text
exp(z)>=1+z+z^2/4,
log(1+u)>=u/2                 (0<=u<=1/16)
```

therefore imply

```text
log E exp(lambda Z) >= E Z^2/(32R^2),
S_X(lambda) >= V/(96R^2)     (lambda>=1/(2R)).
```

The spherical covariance factor is exactly `1/3`. Consequently

```text
J(lambda) >= eta=(1-q)V/(96R^2).
```

The already independently accepted spherical-gap endpoint applies to this
uniform ray and signs all thresholds once

```text
s >= R^2 max(8,44/eta).
```

Since `V<=R^2` and `q>0`, the second term dominates and reduces exactly to
the claimed `4224R^4/((1-q)V)`. The endpoint's tail and high-noise ranges
overlap by `9/64-1/8=1/64`; threshold zero is equality. I inspected the
exact pinned endpoint source and its independent review rather than treating
the target checker as proof of this transfer.

The original map need only be given on the source support. Kirszbraun extends
it with the same constant, and its value at `E X` anchors the target inside a
radius-`LR` ball, hence inside the radius-`R` ball required by the endpoint.
Independent translations do not change spherical averages or Gaussian
hinges. Thus no unjustified target-centering assumption is present.

The claimed auxiliary bounds also follow:

```text
D=E(|X-X'|^2-|Y-Y'|^2) >= 2(1-q^2/27)V,
J(lambda)/D >= (1-q)/(192R^2).
```

The second uses `D<=2V`, not an unproved covariance lower bound.

## Finite certificate and separation family

For rational finite inputs, the producer's reduction is sound. It computes
the exact squared Lipschitz ratio `beta`, centered squared radius `B`, and
scatter `V`. If `beta<1/27`, the automatic choice
`q=(1+27 beta)/2` satisfies `q^2>=27 beta` because

```text
q^2-27 beta=(1-27 beta)^2/4.
```

The separate checker reconstructs `B` and `V` from ordered-pair identities,
checks every pair, and distinguishes a certified future variance interval
from the requested variance. Its unresolved branches make no sign claim.
The isometric and point-target branches use valid elementary facts: distance
rigidity gives equality in the first, while hinge convexity makes a Gaussian
translate majorise any mixture of its translates in the second.

I independently reconstructed the 18-site family

```text
X=(u,v,z),  u,v in {-1,0,1}, z in {-epsilon,epsilon},
Y=(|u|,|v|,|u+v|)/12.
```

The Lipschitz estimate is structural:

```text
144|Delta Y|^2
 <= a^2+b^2+(a+b)^2
 <= 3(a^2+b^2),
```

where the remainder in the last inequality is `(a-b)^2`. Hence the squared
ratio is at most `1/48`, with equality attained. For every
`0<epsilon<=1/100`,

```text
B=2+epsilon^2,        V=4/3+epsilon^2,
Cov(X)=diag(2/3,2/3,epsilon^2).
```

Direct exact reconstruction gives the target covariance displayed in the
source. After subtracting `I/972` and scaling by `5832`, its three leading
principal minors are `3,9,90`, so the claimed positive covariance floor is
valid. Since `epsilon^2<1/972`, conditional Jensen rules out every proposed
martingale relation `E[U|W]=aW`, `a>=1`, even after independent endpoint
isometries. The selected paired-affine determinant is exactly
`-epsilon/54`, and

```text
16896(2+1/10000)^2/(4/3) < 51000,
```

so one variance covers the entire stated interval. This is a separation of
sufficient certificate classes, not a new geometric-class theorem.

## Independent computation and trust boundary

`independent_check.py` imports no author module or certificate. With Python
integers and `Fraction`, it verifies 13 pinned inputs, the frame-product
polynomial in dimensions two through eight, 32 exact positive coefficients
of the radial-cosh second derivative, 72 endpoint schedules, four automatic
factor controls, and every theorem constant. It reconstructs 459 unordered
pair inequalities at three exact values of `epsilon`, both covariance
matrices, the covariance-floor minors, the paired-affine determinant, and
the uniform variance budget. Four damaged schedules are rejected.

The author checker was also replayed normally and under Python optimization;
both modes reproduced 60 parameter schedules, all ten status controls, 14
damaged-input rejections, and record hash
`ea0eb47c088ac4e723f89111269b1e23dc405da1f9f80bf257d94e8a79eb4740`.
The supplied family record and every source hash passed separately.

The executable evidence checks finite algebra, provenance, and constants.
The symmetrization, frame averaging, Jensen steps, MGF monotonicity,
Kirszbraun extension, and imported endpoint remain conventional written
mathematics, not proof-assistant output. I checked those steps directly.
There is no numerical sphere integration, floating-point sign, solver, or
omitted large certificate.

The live arXiv record for Aishwarya--Li states full preservation in dimensions
at most two and partial higher-dimensional results. That supports the scope
distinction but is not an exhaustive historical-priority search. No novelty
or priority verdict beyond the inspected paper and committed graph is made.

## Reproduction

From this directory run:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_UNIFORM_LIPSCHITZ_ACCEPT`.
