# Independent review: loss-normalized Gaussian hinge continuity

## Verdict

**Accept in the stated scope.** At source commit
`a68810063b8ad53dda046c68552a14e76f8d3f07`, let `mu` be supported in a
radius-`R` ball in `R^3`, let `T:R^3->R^3` be 1-Lipschitz, and let the
Gaussian variance be `s`, with `0<R^2/s<=1/2`. For the normalized hinge gap
`H`, dimensionless pair loss `d`, and explicit constants in the source, the
review accepts

```text
|H(u)-H(v)| <= d K_epsilon |u-v|^(1/2),
|Phi'(ell)| <= d M_epsilon(L)       (0<=ell<=L),
Phi(ell)=exp(ell) H(exp(-ell)).
```

It also accepts the stated small-`ell` bound, finite log-grid and
Bernstein--Durrmeyer implications, second-energy normalization, combined
defect estimate, and two-atom first variation. This verifies Discovery Net
contribution `bafkreif2b3e5sw6dumihujzhpul4uce3p7v4elvfpyz77miocxodmytq24`
at height 6325. The proof, checker, and supporting files match their pinned
SHA-256 digests.

The finite tests are conditional: they still require signed endpoints and a
certified normalized middle margin. No such universal margin is proved.
Accordingly this acceptance does **not** prove all hinge signs, full
dimension-three Gaussian-convolution majorisation, or a new
Kneser--Poulsen case.

## Posterior and radial estimates

After scaling to `s=1` and translating source and target independently,
`|Z_t(X)|<=sqrt(epsilon)`. The posterior identity

```text
D^2 V = I - Cov_z(Z)
```

therefore gives `kappa I <= D^2V <= I`, where
`kappa=1-epsilon>=1/2`. The mode equation puts `|z_*|<=sqrt(epsilon)`,
and evaluation at zero gives `0<=v_*<=epsilon/2`.

For the loss-weighted ratio `h`, differentiation along a radial ray gives

```text
g=(log h)_r
  = E_(loss,z)[(Z+Z') dot theta]-2E_z[Z dot theta],
g' = Var_(loss,z)((Z+Z') dot theta)-2Var_z(Z dot theta).
```

The support ranges imply `|g|<=4sqrt(epsilon)` and
`-2epsilon<=g'<=4epsilon`. Likewise
`|V_rrr|<=2epsilon^(3/2)`. Removing the common Gaussian factors from the
numerator and denominator of `h` yields the loss-sensitive estimate

```text
h(z_*+r theta) <= d exp(5epsilon+4sqrt(epsilon)r).
```

This is the decisive place where the actual pair loss, rather than only a
radius bound, enters.

Put `p=V_r`, `b=V_rr`, `a=p/r`, and `J=h r^5/p`. Direct differentiation
with `d/dw=p^(-1)d/dr` reproduces both displayed formulas for `J_w` and
`J_ww`. The coefficient bounds are valid uniformly for
`kappa<=a,b<=1`:

- `5/a^2-b/a^3` and `10/a^3-3b/a^4` decrease first in `b` and then in
  `a` at the maximizing boundary, giving `4/kappa^2` and `7/kappa^3`;
- for `C=20/a^3-15b/a^4+3b^2/a^5`,
  `partial_a C=-15(2a-b)^2/a^6`, so the minimum is `8`;
- the maximum is at `a=kappa` and an endpoint in `b`, with the endpoint
  comparison equal to `3(4kappa-1)(kappa-1)/kappa^5<=0`.

Using `r^2<=2v/kappa` and `q=4sqrt(epsilon)r` then gives exactly

```text
|A_t'(v_*+v)|
 <= (2 pi^3 d/kappa^3) v exp(5epsilon+c sqrt(v))(4+c sqrt(v)),
|A_t''(w)| <= pi^3 d B_epsilon(L).
```

The four contributions to the latter bound are
`8`, `7q`, `5q^2/4`, and `epsilon q/(2kappa)`. Their signs and common
`kappa^(-3)` factor check.

## Modal boundary and Abel inversion

Strong convexity makes `r` comparable to `sqrt(v)`. Hence the radial
coarea density is `A_t=O(v^2)`, its first derivative is `O(v)`, and its
second derivative is locally bounded. Extending by zero below `v_*`
therefore leaves `A_t` continuously differentiable and `A_t'` locally
absolutely continuous. There is no jump in `A_t'`, so its weak derivative
contains no modal delta mass.

The exact six-dimensional coarea/Abel identity and its normalization were
already independently accepted in the cited high-noise dependency. With
the new regularity, write

```text
A_t'(w)=integral_0^w A_t''(z) dz
```

for the zero extension and use Fubini. Differentiating the half integral is
then legitimate and gives

```text
Phi'(ell) = 1/(32 pi^3 sqrt(pi))
  integral_0^1 integral_0^ell A_t''(w)/sqrt(ell-w) dw dt.
```

Since the kernel integrates to `2sqrt(ell)`, this proves the factor
`1/(16sqrt(pi))` in `M_epsilon`. Integrating the resulting
`sqrt(ell)` bound contributes `2/3`, giving the factor
`1/(24sqrt(pi))` in the small-`ell` estimate. The review checker verifies
the same differentiation on 128 exact monomial models. It also detects the
constant model `A'(0)!=0`, where omission of the modal boundary term would
be invalid.

## Global modulus and finite consequences

For the damped density `eta_t(w)=exp(-w/2)A_t'(w)`, optimizing the two
radial monomials gives the claimed uniform bound `pi^3 d W_epsilon`.
The positive decreasing kernel

```text
k(v)=exp(-v/2)/sqrt(v)
```

has integral `sqrt(2pi)`. Extending it by zero to the left,

```text
||k(.-h)-k||_1 <= 2 integral_0^h k(v)dv <= 4sqrt(h).
```

Together with `u log(v/u)<=v-u` and
`sqrt(v)-sqrt(u)<=sqrt(v-u)`, this proves the global one-half modulus and
the exact constant `K_epsilon`. The endpoint `u=0` follows from `H(0)=0`
and continuity.

For the Durrmeyer representation, if `J~Bin(N,u)` and
`U|J~Beta(J+1,N-J+1)`, direct averaging gives

```text
E(U-u)^2
 = 2[1+(N-3)u(1-u)]/[(N+2)(N+3)] <= 1/(N+2).
```

Two Jensen inequalities therefore yield
`||P_N-H||_infinity<=d K_epsilon(N+2)^(-1/4)`. If
`H>=d eta` on the middle interval, the strict degree condition
`N+2>(2K_epsilon/eta)^4` supplies the two error margins needed by the
polynomial test. This does not infer a sign from finitely many beta values
without the displayed polynomial lower certificate.

For two replicas, the scatter is half the squared distance and at most
`2epsilon`. The replica exponential lies in `[exp(-epsilon),1]`, so

```text
d exp(-epsilon)/(16sqrt(2)) <= a_0 <= d/(16sqrt(2)).
```

The three terms in the final defect minimum follow respectively from the
accepted high-noise defect, the global modulus at the signed cutoff, and
`H>=P_N-dK(N+2)^(-1/4)` with `P_N>=-D_N`.

Finally, the symmetric two-atom expansion has
`d=2r^2`. Integrating `partial_11 gamma` over the regular level ball and
dividing by `d` gives
`exp(-ell)ell^(3/2)/(3sqrt(pi))`, confirming that a uniform `o(d)` modulus
is impossible.

## Independent executable evidence

The target checker uses sparse Laurent polynomials and Machin's formula for
pi. The review checker imports none of its code or certificate.

It evaluates the two coarea derivatives through exact second-order jets on
256 deterministic rational inputs and rejects a mutation of the `-3b`
coefficient every time. It checks 128 exact Abel monomial identities, 3,750
coefficient-bound controls, and 10,920 beta-binomial variance identities.

For the published example `epsilon=1/8`, `L=4`, it uses the independent
identity

```text
pi/4 = atan(1/2)+atan(1/3)
```

with alternating-series remainders, decimal-grid square-root enclosures,
and a sixteenfold range-reduced exponential series. Exact rational interval
arithmetic gives

```text
864.724879354810397663372
 < M_(1/8)(4) <
864.724879354810397663373,
```

strictly inside the author's interval
`[864.724879354810,864.724879354811]`. A deliberately too-small upper
endpoint is rejected.

Reproduce from this directory with CPython 3.11 or later:

```sh
python3 independent_check.py
python3 -O independent_check.py
sha256sum -c SHA256SUMS
```

Expected status: `LOSS_NORMALIZED_HINGE_INDEPENDENT_ACCEPT`. The target
checker was also replayed normally and under `python3 -O`, and its manifest
was verified.

## Trust and scope

The independent checker guarantees the pinned inputs, exact jet, Abel,
beta-binomial and normalization controls, and the displayed rational
interval. The universal coefficient bounds, posterior estimates, coarea
regularity, Fubini exchanges, kernel convolution, and first variation remain
written mathematics and were checked directly. The inherited coarea identity
remains a dependency rather than being re-proved from scratch here.

The primary manuscript states the arbitrary-contraction Gaussian
majorisation problem as a conjecture and proves it only in lower dimension
or for restricted pressure classes; see
[Aishwarya--Li, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
No historical priority determination is made for this new internal estimate.
In particular, this review does not convert a positive error bound into an
exact sign or accept the full dimension-three conjecture.
