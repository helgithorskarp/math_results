# Independent acceptance: uniform dilated-martingale certificates

## Verdict

**Accept in the stated scope.** At source commit
`63f42fa6f5173c69391c08b40af53a470663221a`, Discovery Net artifact
`bafkreigsw5tg5pvscer2mm55fmd57ackiiwh55a24qu7wnbzjjmy7uguba` correctly
proves the following dimension-three theorem.

Let `X` have centered support radius at most `R`, scatter
`V=E|X-EX|^2>0`, and let `Y=T(X)` for a contraction. If a coupling of the
centered laws satisfies `E[U|W]=aW` for some `a>1`, then every Gaussian
hinge has the favorable sign for every

```text
s >= 4224 a R^4 / ((a-1)V).
```

The covariance family is also accepted: if `Cov(X)>=kappa I_3`, then for
every 1-Lipschitz `F`, every `0<=c<=kappa/(4R^2)`, and every

```text
s >= 2816 R^4/kappa,
```

`law(X)*gamma_s` is majorised by `law(cF(X))*gamma_s` at all thresholds.
The statements include arbitrary bounded diffuse laws and atomic laws with
arbitrary weights. The coupling is an auxiliary endpoint-law coupling; the
dilated deterministic map need not be contractive.

This is an explicit high-variance family. It does not prove the conclusion
at all positive variances, infer the coupling hypothesis from contraction,
settle unrestricted dimension-three majorisation, or yield a new
small-variance Kneser--Poulsen theorem. Historical priority beyond the
cited primary paper and inspected graph remains uncertain.

## Analytic audit

For a sphere direction and centered moment-generating functions, conditional
Jensen and the `L^a` norm inequality give

```text
M_Y(lambda) <= M_Y(a lambda)^(1/a) <= M_X(lambda)^(1/a).
```

Thus the spherical log-MGF gap is bounded below by
`(1-1/a) integral log M_X`. For centered `Z=theta.X`,
`M_X'(lambda)=E[Z(exp(lambda Z)-1)]>=0` when `lambda>=0`. At
`lambda_0=1/(2R)`, the elementary bound

```text
exp(z) >= 1+z+z^2/4,  |z|<=1/2,
```

gives `M_X(lambda_0)>=1+E Z^2/(16R^2)`. The negative half of this scalar
bound follows by differentiating
`exp(-u)-1+u-u^2/4` and using `exp(-1/2)>1/2`; the positive half is weaker
than the ordinary Taylor bound. Since `log(1+q)>=q/2` for `0<=q<=1/16`,
spherical averaging with `integral theta theta^T=I_3/3` yields exactly

```text
J(lambda) >= eta=(a-1)V/(96aR^2),  lambda>=1/(2R).
```

The imported endpoint at graph height 6032 is independently accepted at
height 6048. That review directly checks its uniform tail error
`44R^2/s`, the high-noise window, and the overlap
`9/64-1/8=1/64`. Substitution gives
`R^2(44/eta)=4224aR^4/((a-1)V)`; because `eta<1/96`, this dominates the
endpoint requirement `8R^2`. Independent translations cause no gap:
spherical averaging kills the added linear MGF terms, while Kirszbraun lets
the target be anchored at the image of the source-ball center, giving it
the same radius `R`.

Conditional squared-norm Jensen gives
`a^2 E|W|^2<=V`, hence the claimed pair-loss floor
`D>=2(1-a^-2)V`. No instantaneous Gaussian conditional-kernel positivity is
used.

## Product coupling and covariance family

With centered endpoint laws and `Sigma=Cov(X)>0`, the density

```text
K(x,y)=1+a x^T Sigma^(-1)y
```

has both prescribed marginals because both means vanish. Its conditional
first moment is

```text
integral x K(x,y)dmu(x)=a Sigma Sigma^(-1)y=ay.
```

Consequently nonnegativity of `K` constructs the required coupling for
diffuse as well as finite laws. If `Sigma>=kappa I`, source radius is `R`,
and centered target radius is `r`, then `K>=0` whenever `aRr<=kappa`.
For a 1-Lipschitz `F`, the centered image radius is at most `2R`; choosing
`a=2` and `c<=kappa/(4R^2)` gives the kernel condition. Finally
`V=tr Sigma>=3kappa` converts the general cutoff to
`2816R^4/kappa`. Also `V<=R^2`, so `c<=1/12` and `cF` remains a contraction.
All boundary equalities are harmless.

## Independent exact evidence

The author packet was replayed at its exact source bytes. Its hashes pass;
normal and optimized CPython 3.11.2 runs both reproduce
`DILATED_MARTINGALE_UNIFORM_FAMILY_PASS` and canonical record SHA-256
`eaf39f616b0688a7e1ef9b66fb0a06e23dc8d8667131d2e16d716f25cb1e2d46`.
The standalone supplied certificate also passes.

`independent_check.py` imports no target module or certificate. It constructs
a new eight-site law from the symmetric pairs

```text
plus-or-minus (1,0,0), plus-or-minus (0,2,0),
plus-or-minus (0,0,3), plus-or-minus (1,1,1),
```

and applies `F(x)=(|x_1|,|x_2|,|x_3|)` with damping `c=1/144`. This is a
global Euclidean contraction and the resulting matched configuration has
paired affine rank six. The source has `R^2=9`, `V=17/4`, and

```text
Cov(X) = [[1/2,1/4,1/4],
          [1/4,5/4,1/4],
          [1/4,1/4,5/2]] >= (1/4)I.
```

All seven principal minors of the shifted covariance are positive. A
Cramer-adjugate inverse, rather than either target implementation, produces
the affine coupling. The checker evaluates all 64 masses, both marginals,
every conditional coordinate, all matched contraction inequalities, and
the pair-loss floor. Its minimum kernel is `1957/2040`; its exact general
cutoff is `2737152/17`, below the corollary cutoff `912384`. A separately
translated and threefold-scaled reconstruction verifies translation
invariance, scale-invariance of the gap and kernel, and quadratic scaling of
loss and variance. Three damaged controls are rejected.

Reproduce from this directory with:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Both Python modes must report `INDEPENDENT_DILATED_MARTINGALE_ACCEPT`.
Thirteen material target and endpoint files are content-pinned in
`TARGET_INPUTS.json`.

The code guarantees the finite rational coupling, covariance bounds,
constant substitutions, scale/translation controls, and input provenance.
Conditional Jensen, the scalar exponential/logarithm inequalities,
spherical averaging, Kirszbraun, and the separately reviewed endpoint are
reviewed written mathematics rather than proof-assistant output. Python
arbitrary-precision integer and `Fraction` arithmetic remain a computational
trust boundary.

The primary Aishwarya--Li manuscript, arXiv:2609.07041v2, states full
preservation in dimensions at most two and only partial preservation in
higher dimensions. This review accepts the present effective damped,
high-variance subclass, not the open full dimension-three conclusion.
