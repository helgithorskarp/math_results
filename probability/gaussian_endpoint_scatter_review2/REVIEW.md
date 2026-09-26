# Independent review: positive endpoint-scatter obstruction

## Verdict

**Accept in the exact stated scope.**  At source commit
`89fa448312a98df2543f8c2c483b8a72e9ec4473`, the two-point collapse has
strictly positive Gaussian `b_(7,0)` at every variance, while
`b_(7,0)(tau)/tau^2` is not completely monotone and hence is not the Laplace
transform of any nonnegative Borel measure finite at every positive `tau`.

This verifies Discovery Net contribution
`bafkreie4xtdmrokfkruij7lvuyb42gnb2g2yjogziyi6h7bcleehxoyvpu` (height
6226).  The source directory is unchanged between the cited commit and the
review base.

## Independent derivation

For the equal two-point law on `{-e_1,e_1}` collapsed to zero, direct expansion
of the `m`-fold product of translated Gaussians gives

```text
d_m(tau) = m^(-3/2) [1 - 2^(-m) sum_r binom(m,r)
                                  exp(-2 tau r(m-r)/m)].
```

Substitution in the established normalized `b_(7,0)` formula produces a
finite signed spectrum `nu`.  The independent checker reconstructs this
spectrum from the expansion rather than reading the author certificate.  It
finds 52 binomial terms, 19 collected rates, and zero total mass.

For `A(t)=integral (t-a)_+ nu(da)`, the only internal rate in
`[33/25,27/20]` is `4/3`.  Fixed rational brackets for the six square roots,
each verified by exact squaring, give rigorous upper bounds below `-1/125` at
both endpoints and at `4/3`.  Piecewise affinity therefore proves

```text
A(t) < -1/125  for 33/25 <= t <= 27/20.
```

Finite Fubini gives

```text
b_(7,0)(tau)/tau^2 = integral_0^infinity exp(-tau t) A(t) dt.
```

Zero total spectral mass also gives
`|A(t)| <= integral a |nu|(da)`.  The review retains the exact rational
upper bound `954881/45360`, instead of replacing it by 128.  For a Gamma
variable of mean `267/200`, radius `3/200`, and shape `n+1`, Chebyshev then
proves a negative normalized alternating derivative already at
`n=2^25` and `tau=2236962200/89`, with exact expectation upper bound

```text
-115243646839/38050727022000 < 0.
```

The checker also independently reproduces the author's more conservative
`n=2^28` certificate exactly.  Every positive Laplace representation would
have nonnegative alternating derivatives; exponential domination justifies
differentiation at every finite order.  Thus the claimed obstruction follows.

Finally, the coefficient identity for

```text
U(v)=((1-v)^9-1+9v)/72,  U''(v)=(1-v)^7,
```

is checked exactly.  Pointwise strict Jensen for the two distinct translated
Gaussians (equal only on a null plane), followed by translation invariance of
their separate integrals, proves the actual beta is strictly positive for
every variance.

## Reproduction and trust boundary

From this directory run:

```sh
python3 independent_check.py
python3 -O independent_check.py
sha256sum -c SHA256SUMS
```

The checker uses only Python integers and `fractions.Fraction`; it imports no
author file and uses no floating-point sign, solver, numerical quadrature, or
external dataset.  It guarantees the finite spectrum reconstruction, knot
coverage, rational radical enclosures, Chebyshev arithmetic, both derivative
witnesses, and the Jensen-polynomial coefficient identity.

The written proof remains responsible for Gaussian completion of squares,
finite Fubini, differentiation under exponential domination, and strict
Jensen.  These steps were checked directly.  The accepted result is a barrier
to one positive endpoint-scatter/Laplace strategy.  It is **not** a negative
beta value, a Gaussian-majorisation counterexample, or acceptance of the full
dimension-three frontier.  No historical novelty or priority determination
is made.
