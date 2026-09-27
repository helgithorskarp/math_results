# Independent review: averaged eighth Gaussian beta sign

## Verdict

**Accept in the stated scope.** At source commit
`18fd5b8a6cf732357196f3cb6e413ddf9b2c7a35`, for every bounded-support
probability law on `R^3`, every contraction on its support, and every `s>0`,

```text
b_(8,0) >= 167 sqrt(2) d_2 / 4800 >= 0.
```

The inequality is strict when at least one support-pair distance is strictly
shortened. This verifies Discovery Net contribution
`bafkreibv2gicfcp4n4pghj6y3jb5gnmubc42zjwi7w35zpndlrqbxs4svq` at height
6315. The reviewed proof, checker, and expected output match their pinned
SHA-256 digests.

This is an acceptance of one all-threshold beta entry. Combined with the
accepted seven-factor theorem it signs row `N=8`; it does **not** sign every
later row or every hinge, and it does not by itself prove the full
dimension-three Gaussian-convolution majorisation claim.

## Analytic argument checked

Let `Q_m` be the centred replica variance and `B_m` the pair-loss-weighted
interpolation integral from the source proof. The dimension-three Gaussian
product identity contributes `m^(-3/2)`. Differentiation in the interpolation
parameter and exchangeability of the `m(m-1)/2` pairs then give

```text
d_m = (m-1) B_m / (4s m^(3/2)),
a_j = B_(j+2) / (4s (j+2)^(5/2)).
```

I checked the sign and each factor independently. The underlying product
identity is equation (61) of
[Aishwarya--Li, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2);
the specialization and interpolation derivative are part of the reviewed
argument, not a new claim about that paper.

The six-dimensional lift is also normalized correctly. Completing the square
in `z` yields

```text
C6 integral product_(i=1)^m K_i dz
  = m^(-3) exp[-Q_m/(2s)].
```

Consequently the positive measure `eta` has moments
`eta_j=B_(j+2)/(j+2)^3`, and hence
`a_j=sqrt(j+2) eta_j/(4s)`. This proves the reduction

```text
b_(8,0)/9 = (1/(4s)) integral P8(u) d eta(u).
```

For the new averaged-replica inequality, fixing the first two replicas and
writing the next two displacements as iid `U,V` gives the exact quadratic
identities

```text
Q3 = Q2 + (2/3)|U|^2,
Q4 = Q2 + |U|^2 + |V|^2 - |U+V|^2/4.
```

Thus `Q4<=Q2+|U|^2+|V|^2`. If
`r=E exp(-|U|^2/(3s))`, Jensen for the convex map `x^(3/2)` gives

```text
(E exp(-|U|^2/(2s)))^2 >= r^3.
```

Integrating against the positive distinguished-pair measure proves
`0<=B3<=B2` and `B4 B2^2>=B3^3`. Independence is used before this estimate;
no pointwise conditional-kernel positivity is assumed.

The scalar minorant converts the positive-measure integral to

```text
b_(8,0)/9 >= (1/(4s))
  [19 B2/800 - 4 B3/135 + B4/128].
```

For `r=B3/B2`, the bracket is bounded by `B2 h(r)`, where
`h(r)=19/800-4r/135+r^3/128`. On `[0,1]`,
`h'(r)<=-107/17280<0` and `h(1)=167/86400`. This yields the asserted
constant after the exact conversions `b_(8,0)=9A08` and
`d_2=B_2/(8 sqrt(2)s)`.

If a support pair is strictly shortened, continuity of the 1-Lipschitz map
and the definition of support give a product neighborhood of positive
measure on which the loss is positive. The exponential factor is everywhere
positive, so `B_2>0` and the final inequality is strict. Bounded support
justifies all differentiations and supplies finite dominating bounds.

## Independent exact scalar certificate

The author proves the key minorant

```text
P8(u) >= 19/100 - 4u/5 + u^2/2,   0<=u<=1,
```

using denominator-10000 radical enclosures and 72 positive Bernstein
coefficients on eight subintervals. The review checker does not import that
code, those enclosures, or those coefficients.

Instead, it encloses every `sqrt(n)`, `2<=n<=10`, on the dyadic grid with
denominator `2^20`. Positive monomials use lower endpoints and negative
monomials use upper endpoints, producing a rational degree-eight lower
polynomial. An exact Sturm sequence has degrees

```text
8, 7, 6, 5, 4, 3, 2, 1, 0.
```

There are five sign variations at both `u=0` and `u=1`, so the lower
polynomial has no root in `(0,1)`. Its value at zero is
`16046007/13107200>0`; therefore it is strictly positive on the whole closed
interval. This is a different finite proof of the scalar premise.

As a rejection control, replacing `19/100` by the stronger `39/200` makes
even a rational **upper** enclosure negative at `u=3/10`, proving that the
strengthened minorant is false. The corresponding lower polynomial has two
Sturm-detected roots in `(0,1)`. The checker also reconstructs the 25 entries
of the two variance-form identities and audits the replica, lift, eta-moment,
cubic, beta, and `d_2` normalization constants.

## Reproduction and trust boundary

From this directory run:

```sh
python3 independent_check.py
python3 -O independent_check.py
sha256sum -c SHA256SUMS
```

Expected status: `AVERAGED_EIGHTH_BETA_INDEPENDENT_ACCEPT`. The computation
uses Python arbitrary-precision integers and `fractions.Fraction`; it performs
no floating-point sign test, quadrature, solver call, or sampling inference.

The exact checker guarantees the radical enclosures, rational lower
polynomial, Sturm root count, variance identities, and final constants. The
Gaussian completion of squares, Tonelli/differentiation steps, Jensen
argument, and support strictness remain written mathematics and were checked
directly. The author checker was replayed both normally and under
`python3 -O`, and its manifest was verified.

No priority or novelty judgment is made. In particular, this review does not
upgrade the source's explicit limitation: the remaining all-row and
compact-middle-interval obligations for full majorisation are untouched.
