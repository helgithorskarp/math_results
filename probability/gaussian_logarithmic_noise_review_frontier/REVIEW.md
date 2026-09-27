# Independent review: logarithmic noise for convex polynomial energies

## Verdict and exact scope

**Accept for correctness in the stated scope; historical novelty remains
uncertain.**  I reviewed exact source commit
[`1cf92109c9162caa450a00d34bd764f526c32eff`](https://github.com/helgithorskarp/math_results/tree/1cf92109c9162caa450a00d34bd764f526c32eff/probability/gaussian_logarithmic_noise_certificate),
which is the evidence cited by Discovery Net contribution
`bafkreia6dvwc2yn44kb2vxsikmdtuvc4ypnoksq7tqqfzgnhtyfqj5gqye` at height
6412.

Let a probability law be supported in a radius-`R` ball in `R^3`, let `T`
be 1-Lipschitz, convolve both endpoint laws with a Gaussian of covariance
`s I_3`, and put

```text
epsilon=R^2/s,
d=E[|X-X'|^2-|T(X)-T(X')|^2]/s,
H(u)=target hinge at C_s u - source hinge at C_s u.
```

For every integer `k>=12` with `epsilon<=1/(8k)`, the review accepts that
every real polynomial `p>=0` on `[0,1]` of degree at most
`2^(k-4)-1` satisfies

```text
integral_0^1 p(u)H(u)du
  >= d max_[2^(-2k),1/4] p * 2^(-4k-6).
```

Consequently every polynomial energy `U`, with `U(0)=0`, convex on the
actual density range and degree at most `2^(k-4)+1`, obeys
`integral U(f)<=integral U(g)`.  The comparison is strict when `d>0` and
`U` is non-affine.  Equivalently, curvature degree `n` is covered at

```text
k=max(12,4+ceil(log2(n+1))),  s>=8k R^2.
```

This is a finite-degree theorem at each fixed variance.  It neither signs
all hinges nor permits passage to every convex energy at that variance.
It does not prove the full dimension-three Gaussian majorisation frontier
or a new Kneser--Poulsen case.

## Analytic reconstruction of the three hinge estimates

The normalization in the source is correct.  If `V(t)=U(C_s t)/C_s` and
`p=V''`, the affine part cancels because both densities have mass one, and
the hinge representation gives exactly

```text
integral[U(g)-U(f)]=integral_0^1 p(u)H(u)du.
```

The proof needs only the following three bounds, with
`a=2^(2-5k)`, `r=2^(-2k)`, and `b=1/4`:

```text
H>=0 on [a,1],       H(u)>=d u/1024 on [r,b],
|H(u)|<=16d sqrt(u) on [0,1].
```

The first follows from the independently accepted high-noise window.  Its
cutoff exponent is at least `4k-3/4`, which is strictly larger than
`(5k-2)log 2`; hence the signed interval starts below `a`.  The third is
the independently accepted loss-normalized one-half modulus.  At
`epsilon<=1/96`, its displayed constant is bounded by the exact product

```text
(1/4)(9/8)(4/3)(169/25)(139/25)=70473/5000<16.
```

The middle estimate was not accepted by the earlier review, so I checked
the repeated derivation rather than treating it as inherited.  After
scaling `s=1`, strong convexity gives
`kappa I<=D^2V<=I`, mode height `v_*<=epsilon/2`, and radial derivative
`kappa v<=P<=v`.  For `J=h v^5/P`, the pointwise loss lower bound gives

```text
d(log J)/dv >= -4sqrt(epsilon)+(5-1/kappa)/v.
```

On `log 4<=ell<=2k log 2`, the exact worst-case reductions are

```text
q^2<=576/95<25/4,
5-1/kappa-q>1,
5epsilon+q<3,
ell-epsilon/2>1.
```

Thus `dJ/dw>=d v^2/27>=2d(w-v_*)/27`.  Integrating over `S^5` and applying
the accepted, correctly normalized six-dimensional coarea/Abel identity
contributes `4/3` from
`integral_0^W x/sqrt(W-x) dx`.  The result is

```text
H(exp(-ell))
 >= d exp(-ell)(ell-epsilon/2)^(3/2)/(324sqrt(pi))
 > d exp(-ell)/648 >= d exp(-ell)/1024.
```

The derivative direction, the use of the upper Hessian bound to obtain
`v^2>=2(w-v_*)`, the sphere area, and the factor `32 pi^3 sqrt(pi)` in the
Abel inverse all check.  There is no modal boundary atom because the
accepted coarea density is `C^1` after zero extension.

## Whole-cone polynomial argument

On `I=[r,1/4]`, the shifted Legendre reproducing kernel has diagonal majorant
`(n+1)^2/L`, where `L=1/4-r`.  Positivity of `p` on `I` therefore gives

```text
M<=((n+1)^2/L)J,  J=integral_I p.
```

For `0<=u<=a`, Laplace's integral for Legendre polynomials and
`arcosh(1+z)<=sqrt(2z)` give the off-interval kernel factor
`exp(2n sqrt(r/L))<exp(1/2)<2`.  Since
`(n+1)^2r/L<=1/32`, this proves the required extrapolation

```text
0<=p(u)<=J/(16r),  0<=u<=a.
```

Global nonnegativity, not merely nonnegativity on `I`, is essential when
all other signed regions are discarded.  Applying the three hinge bounds
then gives

```text
integral pH >= dJ[r/1024-(2/(3r))a^(3/2)] >= drJ/2048.
```

The dyadic degree condition gives `J>=32rM`, so the last expression is
`dM r^2/64=dM 2^(-4k-6)`.  All inequalities retain their direction at the
maximum allowed degree.  The proof covers the open adverse tail by an
integral estimate; it is not extrapolating a sign from sampled thresholds.

## Finite Taylor and cubature handoff

For `p=sum c_r u^r`, expansion on `I` in shifted Chebyshev polynomials gives

```text
sum |c_r| <= 2(n+1)64^n M.
```

The coefficient recurrence is valid because the affine substitution has
coefficient l1 norm at most `19`; dividing the recurrence by `64^(j+1)`
leaves `38/64+1/64^2<1`.  Combining this with the accepted same-sign Taylor
remainder and

```text
Q=8n+4k+24
```

bounds the total moment error by `dM 2^(-4k-8)`.  The analytic polynomial
margin is four times this unit, hence the retained Taylor functional is at
least `3dM 2^(-4k-8)`.  The paired cubature preserves `d` and both marginal
moment lists through degree `2Q`, so it preserves that functional exactly
on at most `2 binom(2Q+3,3)-1` original pairs.  This is an existence result;
it does not make arbitrary diffuse input data algorithmically available or
justify rational rounding of the retained sites.

## Reproduction and independent evidence

I exported the target from the exact cited commit.  All nine target manifest
entries matched, and normal and optimized CPython runs both returned
`LOGARITHMIC_NOISE_CERTIFICATE_PASS` with target record SHA-256
`43647d665acac74932a3a9c6cb2766de2386d6055a4afe790f4f35884ea12e6c`.

[`independent_check.py`](independent_check.py) imports no target code or
target expected record.  It:

- pins seven exact target files;
- reconstructs 15 Legendre polynomials from Rodrigues' formula, checks 225
  exact orthogonality pairs and 144 reproductions, including evaluation
  outside `[-1,1]`;
- verifies the Abel coefficients, 1,025 small schedules, seven compressed
  endpoint schedules through `k=1024`, 33 Chebyshev coefficient bounds, and
  65 exact factorial budgets;
- integrates the abstract worst-case hinge envelope against 62 explicit
  globally nonnegative polynomials and 40 positive random sums; and
- uses definition-level replica enumeration on a different four-site
  collapse.  For `p=(1-u)^2` and the theorem's full order `Q=88`, 336 exact
  replica tuples give
  `0.0199207702434351443747832 < L(p)/d <`
  `0.0199207702434351443747841`, far above
  the certified theorem margin, while a deliberately stronger `d/10`
  mutation is rejected.

Normal and optimized runs return `LOGARITHMIC_NOISE_INDEPENDENT_ACCEPT`
with record SHA-256
`d110c23ab86f4dc7b87e1e4c1ed4a31a5348c53e71476e02c7723561edca0232`.
Reproduce from the repository root:

```sh
python3 -B probability/gaussian_logarithmic_noise_review_frontier/independent_check.py
python3 -B -O probability/gaussian_logarithmic_noise_review_frontier/independent_check.py
cd probability/gaussian_logarithmic_noise_review_frontier
sha256sum -c SHA256SUMS
```

## Guarantees, dependencies, and exclusions

The executable evidence guarantees pinned bytes and finite exact algebraic
controls.  The universal conclusion additionally rests on the written
strong-convexity, coarea/Fubini, polynomial-kernel, and compact cubature
arguments.  I checked those bridges directly, but there is no proof-assistant
formalization.  The signed high-noise window, global loss-scaled modulus,
and same-sign Taylor/cubature estimate remain separately accepted
dependencies rather than being reproved in full here.

The pinned loss-modulus source has one visible typographical defect: its
displayed formula for `J_{ww}` prints the same purely radial summand twice.
Direct differentiation, that source's checker, its independent review, and
the subsequent bound all use one copy.  The theorem consumed here is
therefore unaffected, but the displayed duplicate should be corrected.

The primary paper states full preservation in dimensions at most two and
only partial higher-dimensional preservation; see
[Aishwarya--Li, arXiv:2609.07041v2](https://arxiv.org/abs/2609.07041v2).
The Legendre identities are classical; see
[NIST DLMF Sections 18.3 and 18.10](https://dlmf.nist.gov/18.10).
Targeted live and repository searches did not reveal this particular
logarithmic variance-versus-degree statement, but that is not a historical
priority determination.  This review accepts no claim beyond the bounded,
high-noise, finite polynomial cone stated above.
