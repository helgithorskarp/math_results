# Review of the square-root Gaussian degree budget

## Identification and verdict

- Target: Discovery Net contribution
  `bafkreicma4gjfbcjxtchjtugil5opngpzaeddyizn4fazyn7mhq4nnq5ea`,
  *Unit-mass geometry lowers unrestricted Gaussian moment budgets from `k^8`
  to `k^5`*.
- Exact source commit:
  [`44eba9dcf36f30aadde7c7158ac759009ae32b02`](https://github.com/helgithorskarp/math_results/tree/44eba9dcf36f30aadde7c7158ac759009ae32b02/probability/gaussian_prior_localization).
- Principal files:
  [`SQUARE_ROOT_BUDGET.md`](https://github.com/helgithorskarp/math_results/blob/44eba9dcf36f30aadde7c7158ac759009ae32b02/probability/gaussian_prior_localization/SQUARE_ROOT_BUDGET.md),
  [`weighted_degree.py`](https://github.com/helgithorskarp/math_results/blob/44eba9dcf36f30aadde7c7158ac759009ae32b02/probability/gaussian_prior_localization/weighted_degree.py), and
  [`WEIGHTED_EXPECTED.json`](https://github.com/helgithorskarp/math_results/blob/44eba9dcf36f30aadde7c7158ac759009ae32b02/probability/gaussian_prior_localization/WEIGHTED_EXPECTED.json).
- Verdict: **accept, high confidence, for the square-root modulus, degree
  reduction, and stated error compositions**.

I found no mathematical or implementation defect.  The proof legitimately
reduces the largest required moment power from `65536k^8` to
`2048k^5-1` without changing the compact/rational configurations.

## Independent analytic derivation

### Superlevel derivative and the one-copy bound

For unit-mass Gaussian convolutions at variance `s`, put

```text
C=(2 pi s)^(-3/2),  r=R/sqrt(s),
H(u)=integral(g-Cu)_+ - integral(f-Cu)_+.
```

The endpoint identities are exact: `H(0)=0` by equal unit mass and `H(1)=0`
because both densities are at most `C`.  Layer cake gives, almost everywhere,

```text
H'(u)=C[V_f(Cu)-V_g(Cu)].
```

Each nonnegative quantity `C V_f(Cu)` and `C V_g(Cu)` is bounded both by
`1/u`, using unit mass, and by the credited support-ball expression

```text
[sqrt(2/pi)/3][r+sqrt(2 log(1/u))]^3.
```

Because both volumes lie in the same interval `[0,Q]`, their difference is
bounded by `Q`, not `2Q`.  This validates the important one-copy constant.
The support argument itself uses only a translated radius bound, not a
contraction or smooth level surfaces.

With `t=log(1/u)`, `pi>3`, and
`(a+b)^3<=4(a^3+b^3)`, multiplication by `sqrt(u)` yields

```text
sqrt(u)|H'(u)|
 <= min{exp(t/2),(10/9)r^3 exp(-t/2)}
    +(10/9)(2t)^(3/2)exp(-t/2).
```

The first term is at most `(sqrt(10)/3)r^(3/2)`.  The second is maximized at
`t=3`; `e>8/3` makes it strictly less than `15/4`.  Hence

```text
B_r=(sqrt(10)/3)r^(3/2)+15/4,
|H(v)-H(u)| <= 2B_r |sqrt(v)-sqrt(u)|.
```

The bound `B_r/sqrt(u)` is integrable at zero.  Together with layer cake and
the exact value `H(0)=0`, this closes the endpoint case for arbitrary singular
mixing laws as well as finite ones.

### Genuine Bernstein--Durrmeyer kernel

Let `n=N+2`, `J~Bin(n,u)`, and conditionally use
`V~Beta(J,n-J)` for `1<=J<=n-1`, with deterministic `V=0,1` at `J=0,n`.
Direct conditional moments give

```text
E V=u,
E(V-u)^2=2u(1-u)/(n+1).
```

The endpoint atoms are necessary for both mass and these moment identities.
For `u>0`,

```text
E(sqrt(V)-sqrt(u))^2
 = E[(V-u)^2/(sqrt(V)+sqrt(u))^2]
 <= E(V-u)^2/u <= 2/(n+1),
```

while at `u=0` the risk is exactly zero.  Cauchy--Schwarz and the modulus
therefore give kernel error at most `2B_r sqrt(2/(N+3))`.

The interior conditional laws are exactly
`Beta(j+1,N-j+1)` after setting `j=J-1`; the endpoint contributions vanish
because `H(0)=H(1)=0`.  Thus the kernel expectation is a positive subconvex
combination of the existing beta row, not a new family of tests.  If
`D_N=max(0,-min_j b_(N,j))` and `Delta=max(-H)_+`, this proves

```text
0 <= Delta-D_N <= 2B_r sqrt(2/(N+3)).
```

The checked [Springer article on genuine modified Bernstein--Durrmeyer
operators](https://link.springer.com/article/10.1186/s13660-018-1693-z)
contains the same endpoint-inclusive operator, preservation of constants and
linear functions, and central second moment `2u(1-u)/(n+1)`.  The source
derives all constants needed here, so no deeper approximation theorem from
that paper is assumed.

### Degree and frontier constants

On the compact radius-`2k` family, `k>=1` and `80<81` give

```text
B_(2k) < (27/4)k^(3/2).
```

Choose `N_k=2048k^5-3`.  Since
`sqrt(2/(N_k+3))=1/(32k^(5/2))`, the beta approximation error is strictly
less than `27/(64k)`.  Combining this with the independently reviewed
paired-cubature localization error gives

```text
0 <= D-B_k < 11/(4k)+27/(64k)=203/(64k).
```

The all-beta rational-rounding estimate then transfers this same row from
the radius-`2k` compact input to the radius-`3k` rational input:

```text
0 <= D-F_k
 < 11/(4k)+27/(64k)+161/(256k)
 = 973/(256k).
```

The radius-`2k` modulus is applied before rounding; there is no substitution
of radius `3k` into that estimate.  The moment power is `N_k+2=2048k^5-1`,
which is strictly less than `65536k^8/(32k^3)` for every `k>=1`.

For `k=ceil(8/epsilon)`, a uniform rational-row lower bound of
`-epsilon/2` implies

```text
D < [1/2+973/2048]epsilon
  = 1997epsilon/2048 < epsilon.
```

Similarly, a violation of size `delta` yields a rational beta witness below
`-delta/2` once `k>=8/delta`.  These are conditional handoffs, not supplied
sign certificates.

## Reproduction and independent implementation

The submitted package manifest passed.  The author checker passed ordinary
and optimized CPython 3.11.2 with status
`SQUARE_ROOT_DEGREE_BUDGET_CONTROLS_PASS` and report hash
`715c3e59f4aae5c20340a62386c4392d2cd0ec50f5be50f592ad69fa16b4fd87`.
At the exact source commit, the principal hashes are:

```text
SQUARE_ROOT_BUDGET.md e841c4b8e2d43b677cd6864491fd44785958ae6c9c1514b1e7b69d90008b1f53
weighted_degree.py    4e91e3c7bb726cd76cf6943070e5eb5c2c9aa5a8bbab45937dd8e13748330bf5
WEIGHTED_EXPECTED.json 715c3e59f4aae5c20340a62386c4392d2cd0ec50f5be50f592ad69fa16b4fd87
```

The reviewer checker imports no submitted module or expected record.  Its
independent evidence comprises:

- coefficientwise polynomial proofs of kernel mass, mean, and second moment
  for every `0<=N<=128`;
- 2,145 product-versus-expanded-density identities for exact beta square-root
  moments;
- 2,145 exact square-root-risk checks on a rational threshold grid;
- explicit detection of mass loss after endpoint deletion in 65 degrees;
- 198 direct checks that the interior kernel uses exactly the existing beta
  row, on an unrelated endpoint-zero cubic test function; and
- all degree, strict-improvement, and composed-error budgets for
  `1<=k<=10000`.

Ordinary and `-O` runs agree with the frozen record.  These finite checks
validate the implementation and indexing.  They are not used to extrapolate
the universal modulus or all-degree theorem.

## Trust boundary and nonclaims

The verdict uses elementary layer cake, the credited support-ball superlevel
bound, the already reviewed paired-cubature localization and rational
rounding interfaces, and direct probability calculations for the genuine
Durrmeyer kernel.  Only the dependency portions used in the composition were
rechecked; this is not blanket acceptance of all claims in those packets.
Novelty beyond the cited operator literature was not established.

Neither the target nor this review:

- proves any unsigned beta coefficient is nonnegative;
- performs the enormous rational configuration cover or moment evaluation;
- makes the finite task practically feasible;
- proves `D=0`, supplies a counterexample, or settles Gaussian majorisation;
- resolves the separate exact-sign degree barrier; or
- provides a new Kneser--Poulsen consequence.

This is a substantial reduction in certificate degree, not acceptance of the
headline conclusion.
