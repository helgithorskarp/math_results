# Review of the paired-cubature Gaussian frontier

## Identification and verdict

- Target: Discovery Net contribution
  `bafkreia425hkp6pibvmb4dqein5ybdlxy4kkeywfmuqd3gd6mkptjll4rq`,
  *Near-cubic atom budgets for contraction-preserving Gaussian localization*.
- Exact source commit:
  [`cc561805eaf1e28f7138b5f71c8b37dbc9ce2a1a`](https://github.com/helgithorskarp/math_results/tree/cc561805eaf1e28f7138b5f71c8b37dbc9ce2a1a/probability/gaussian_prior_localization).
- Principal files:
  [`CUBATURE_FRONTIER.md`](https://github.com/helgithorskarp/math_results/blob/cc561805eaf1e28f7138b5f71c8b37dbc9ce2a1a/probability/gaussian_prior_localization/CUBATURE_FRONTIER.md),
  [`paired_cubature.py`](https://github.com/helgithorskarp/math_results/blob/cc561805eaf1e28f7138b5f71c8b37dbc9ce2a1a/probability/gaussian_prior_localization/paired_cubature.py), and
  [`CUBATURE_EXPECTED.json`](https://github.com/helgithorskarp/math_results/blob/cc561805eaf1e28f7138b5f71c8b37dbc9ce2a1a/probability/gaussian_prior_localization/CUBATURE_EXPECTED.json).
- Verdict: **accept, high confidence, for the stated atom reduction and its
  error/rational-interface consequences**.

The proof correctly replaces the old `k^6` compact atom budget by

```text
A_k = min{k^3 M(2 ell+3), ceil(k/h)^3 M(4 ell+8)},
ell = ceil(log2 k),  h=floor(sqrt(ell+1)),
M(p)=2 binom(p+3,3)-1,
```

and proves `A_k=O(k^3(1+log k)^(3/2))`.  I found no mathematical or
implementation defect.  Later repository refinements not present in the
cited commit are outside this review.

## Independent analytic derivation

### Shared-site cubature

For a source law and its contracted image, use the feature vector consisting
of the constant plus every nonconstant source and target monomial through
degree `p`.  It has exactly

```text
1 + 2[binom(p+3,3)-1] = M(p)
```

coordinates and lies in the affine hyperplane whose constant coordinate is
one.  Caratheodory therefore represents its expectation using at most
`M(p)` actual source/image pairs with common positive weights.  Equivalently,
the finite-function form of Tchakaloff cubature applies.  Because the chosen
pairs remain `(x,T(x))`, every contraction inequality survives exactly;
there is no polynomial-map assumption and no need for joint six-dimensional
moments.

The cited [Bayer--Teichmann theorem](https://arxiv.org/abs/math/0502473v2)
does give a finite positive formula on points of the concentration set for a
finite measurable feature map.  The compact-support/continuous-map case used
here is therefore safely within its hypotheses.  The
[Ma--Wu--Yang paper](https://arxiv.org/abs/2404.08913v2) supports the local
moment-matching context but is not needed as a premise for the proof below.

Matching degrees one and two separately in the two marginals preserves their
means and covariance traces.  Hence it preserves exactly

```text
E[|X-X'|^2-|TX-TX'|^2]
  = 2 tr(Cov(X)-Cov(TX)).
```

This statement applies to the law entering the cubature step; it does not say
that the earlier localization or later rational rounding preserves the same
quantity.

### Gaussian identity and TV transfer

Let `sigma=mu-nu`, where both laws lie in `B(c,r)` and have equal moments
through degree `p`.  Expanding translated Gaussian densities gives the exact
identity

```text
integral ((mu*gamma_1)-(nu*gamma_1))^2/gamma_1(.-c)
 = double_integral exp((x-c).(x'-c)) d sigma(x)d sigma(x').
```

Uniform absolute convergence is immediate from bounded support.  For every
`j<=p`, the coefficient vanishes because

```text
double_integral (u.v)^j d sigma(u)d sigma(v)
 = sum_{|alpha|=j} [j!/alpha!]
     (integral u^alpha d sigma(u))^2 = 0.
```

The total-variation norm of `sigma` is at most two, so the remaining absolute
sum is at most `4 tau_p(r^2)`.  Cauchy--Schwarz, including the factor one-half
in probability total variation, yields

```text
TV(mu*gamma_1,nu*gamma_1) <= sqrt(tau_p(r^2)).
```

An equal-mass hinge is 1-Lipschitz in this TV distance.  Applying the estimate
to both marginals therefore costs `2 sqrt(tau_p(3b^2/4))` on a cube of side
`b`.  The same uniform bound transfers directly to beta averages and is not
amplified by alternating moment coefficients.

### Tail schedules and atom exponent

For `0<=a<p+2`, comparison with a geometric series gives

```text
tau_p(a) <= U_p(a)
 = a^(p+1)/[(p+1)!(1-a/(p+2))].
```

For unit cubes, `U_3(3/4)=135/8704<1/64`; raising the degree by two multiplies
the bound by less than `1/4`.  Thus `p=2 ell+3` gives a tail below
`1/(64k^2)`.

For the wider schedule, `b=k/ceil(k/h)<=h`, so
`a<=3h^2/4<=3(ell+1)/4`.  With `q=4ell+9`, the elementary estimates
`q!>(q/e)^q`, `e<3`, and `a/(p+2)<3/16` give

```text
U_(4ell+8)(a)
 < (16/13)(9/16)^(4ell+9)
 < 1/(64*4^ell) <= 1/(64k^2).
```

Both endpoint TVs therefore sum to less than `1/(4k)`.  The asymptotic count
also checks: `h>=sqrt(ell+1)/2`, `ceil(k/h)<=4k/sqrt(ell+1)`, and

```text
M(4ell+8) < (4ell+11)^3/3
           <= 1331(ell+1)^3/3,
```

so `A_k <= (85184/3)k^3(ell+1)^(3/2)`.

### Localization and compact maximum

The focused part of the credited shifted-grid localization supplies one
source cube of side `k` with loss at most `3 sqrt(2/pi)/k`.  Subdividing it
and applying paired cubature in each occupied cell retains the cell masses.
Convexity of TV makes the error a mass-weighted average, with no factor for
the number of cells.  Choosing one retained pair as anchor and translating
the two endpoint clouds separately gives both radii at most
`sqrt(3)k<2k`; contractivity is unchanged.  Consequently

```text
0 <= D-E_k
 < [3 sqrt(2/pi)+1/4]/k
 < 11/(4k).
```

Padding with zero weights places all configurations in one finite-dimensional
compact set.  The same Gaussian envelope used in the credited localization
proof gives continuity through collisions and zero weights, so the maximum
`E_k` is attained.  This review rechecks only the dependency portions used
here, not every claim in their packets.

### Rational handoff

The previously reviewed merge-expand-round argument remains valid with
`m<=A_k`, coordinate denominator `L=256k^3`, and the new weight denominator
`W=4kA_k`.  Largest-remainder rounding has
`L1` error at most `A_k/W=1/(4k)`, so its all-hinge error remains below
`161/(256k)`.  Combining the compact bound, the focused radius-only beta
approximation `2/(3k)`, and rational rounding gives

```text
0 <= D-G_k
 < 11/(4k)+2/(3k)+161/(256k)
 = 3107/(768k).
```

Thus `k=ceil(9/epsilon)` plus a uniform finite beta bound of
`-epsilon/2` implies
`D<6563 epsilon/6912<epsilon`.  A non-point rational law has the ordered
pair-loss floor

```text
2/(256k^4 W^2) = 1/(2048k^6 A_k^2).
```

The enumeration count
`A_k[(1536k^4+1)^6(4kA_k+1)]^(A_k)` follows by direct overcounting; the beta
index multiplier is below `2^16 k^8` at the reviewed degree.

## Reproduction and independent implementation

The submitted package hash manifest passed.  Its producer passed ordinary
and optimized CPython 3.11.2 with status
`PAIRED_CUBATURE_FRONTIER_CONTROLS_PASS` and report hash
`dc78b5dac03926e56f027a33e43de894c9efe986c039f0a503f38562f29105ab`.
At the exact source commit, the principal file hashes are:

```text
CUBATURE_FRONTIER.md  0dbcaf36263ee8ce2976d75d1073db4f878db908fd5c53161e55485c5da53632
paired_cubature.py    e533824e8e7260147a27ebe75607e7f4360aded6b23cb6d58080e7632bbe2b00
CUBATURE_EXPECTED.json dc78b5dac03926e56f027a33e43de894c9efe986c039f0a503f38562f29105ab
```

The independent checker in this directory uses a different pivot order,
support-elimination order, nonlinear contraction, coordinates, and weights.
It imports no submitted module or expected output.  Exact normal and `-O`
runs both produce:

- support sizes `7,19,39` at degrees `1,2,3`;
- 68 raw and 68 independently translated marginal-moment equalities;
- 18 Gaussian-kernel coefficient cancellations;
- exact pair-loss preservation at degrees two and three;
- three successful updated rational-rounding controls, with minimum integer
  pair margin at least 5,968; and
- exact schedule, transition, composition, pair-floor, and near-cubic bounds
  for every `1<=k<=8192`.

The finite run checks implementations and edge transitions.  The universal
result is accepted from the derivation above.

## Trust boundary and nonclaims

The accepted theorem uses classical finite-function cubature, Kirszbraun
extension, elementary Gaussian integration, exact tail estimates, and the
focused localization and radius-only beta bounds described above.  The
credited beta row remains an unformalized dependency beyond the portion
rechecked here.  Novelty beyond the explicitly cited literature was not
established.

Neither the target nor this review:

- determines any previously unknown beta sign;
- enumerates or certifies every rational configuration;
- makes the huge finite task computationally feasible;
- upgrades the degree-five cell consumer to the reviewed high-degree row;
- proves `D=0`, supplies a counterexample, or settles the full
  dimension-three frontier; or
- yields a new Kneser--Poulsen theorem.

This is a correct and useful reduction of the headline problem, not its final
solution.
