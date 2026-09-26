# Independent review of the uniform Gaussian defect bound

## Verdict and exact scope

**Accepted with high confidence at source commit
`191c7aacaef3c087e5a75ef518d011393bf485bf`.** I found no mathematical or
computational gap in the bound

```text
H_f(a)-H_g(a) <= 7/50
```

for every bounded probability input in `R^3`, every contraction, every
positive Gaussian variance, and every nonnegative threshold. The exact
Discovery Net target is
`bafkreiabyue73en4ed52wakh3cak6dsayxvljtzz4bb77nrlvavhrflcne`.

The verdict also accepts the stated concentration-profile error and the
`-7/50` lower bound on every beta average, because both are immediate
averages or dual consequences of the hinge estimate. It does **not** prove
zero defect, full dimension-three Gaussian majorisation, an exact positive
map class, optimality of `7/50`, or a new Kneser--Poulsen case.

## Independent reconstruction

### 1. The six-dimensional stochastic comparison has the right hypotheses

For a base point `x_0`, put
`v(x)=(x-x_0,T(x)-T(x_0))` in the span `V` of these paired vectors. If
`P,Q` are the two coordinate projections and `A=P*P`, `B=Q*Q`, then

```text
c_t(x)=((1-t)A+tB)^(1/2)v(x)
```

is continuous in `t`, including at singular endpoints, and

```text
|c_t(x)-c_t(y)|^2
 =(1-t)|x-y|^2+t|T(x)-T(y)|^2.
```

Thus the path is a continuous contraction in at most six dimensions. No
unjustified operator inequality `B<=A` is needed: positivity of each convex
combination follows because `A` and `B` are positive semidefinite, while
pairwise monotonicity follows from the original contraction inequalities.
The two endpoints are congruent to the original configurations embedded in
six dimensions.

Aishwarya--Li Theorem 1.4(i)(a) supplies a coupling under which the
Gaussian-convolved density value at the source is at most the corresponding
target value. I checked the primary theorem statement and its direction.
At either endpoint, six-dimensional convolution factorizes as

```text
f(x) gamma_s^(3)(z)    or    g(x) gamma_s^(3)(z).
```

When `z` is sampled from that auxiliary Gaussian,
`|z|^2/(2s)` is `Gamma(3/2,1)`. Consequently, with

```text
R_p(b)=integral p(x) F_(3/2)(log(p(x)/b)) dx,
```

the coupling gives `R_f(b)<=R_g(b)` for every `b>0`. The auxiliary density
peak is the same at both endpoints and cancels from the threshold, so there
is no missing power of the variance. This derivation is complete for diffuse
as well as atomic bounded laws; it does not rely on acceptance of the earlier
graph packet that first recorded it.

### 2. The shifted-Gamma envelope covers the whole real line

Set

```text
h(t)=(1-exp(-t))_+, q=17/50, w=57/50, c=7/50,
d(t)=h(t)-w F_(3/2)(t+q).
```

For `t<=-q`, `d=0`; on `[-q,0]`, it decreases to `d(0)`. For `t>0`, direct
differentiation gives

```text
d'(t)=exp(-t)[1-(2w exp(-q)/sqrt(pi))sqrt(t+q)].
```

The bracket is strictly decreasing and has one root

```text
t_star=pi exp(2q)/(4w^2)-q.
```

Therefore `d` increases to one positive-half-line maximum and then decreases
to `1-w=-c`. It is enough to prove `d(0)>-c` and `d(t_star)<0`; no grid,
tail cutoff, or unproved numerical monotonicity remains.

The source verifier proves these facts by rational Taylor and square-root
intervals. Its signs, interval orientations, and factors of two are correct.
In particular, integrating the even/odd exponential Taylor bounds against
`sqrt(u)` produces the displayed factor
`4 x sqrt(x)/sqrt(pi)`, and the critical-root tests use outward bounds in the
proper directions.

### 3. A different exact certificate confirms both delicate inequalities

[`independent_check.py`](independent_check.py) imports no reviewed code or
certificate. It uses the separate Machin identity

```text
pi=8 atan(1/3)+4 atan(1/7)
```

and low-degree rational Taylor bounds. A degree-four integrated exponential
upper bound proves `w F_(3/2)(q)<c`, hence `d(0)>-c`.

For the positive maximum, put `x_star=t_star+q`. A degree-four positive
exponential lower bound proves `x_star>1191/1000`. Integration by parts gives

```text
F_(3/2)(x)=erf(sqrt(x))-(2/sqrt(pi))sqrt(x)exp(-x).
```

At the critical point, the derivative equation cancels both exponential
terms exactly:

```text
d(t_star)=1-w erf(sqrt(x_star)).
```

The integrated degree-seven lower Taylor bound for `erf`, evaluated at
`1191/1000`, proves the right side is strictly negative. All square roots are
removed by squaring explicitly positive rational expressions. The three final
rational margins are positive, and the canonical record hash is
`e7b80e50d2bdbb204aa5c76624b49ea3b2f4669a47865ba78b7e6c0bf3e96d12`.

This establishes independently

```text
-7/50 <= d(t) <= 0    for every real t.
```

### 4. Integration gives exactly the claimed defect bound

For a probability density `p` and `a>0`, substitute `t=log(p/a)` into the
scalar envelope and integrate against `p(x)dx`. Since
`p h(log(p/a))=(p-a)_+`, one obtains

```text
H_p(a) <= w R_p(a exp(-q)) <= H_p(a)+c.
```

Combining this with `R_f<=R_g` gives

```text
H_f(a) <= w R_f(a exp(-q))
       <= w R_g(a exp(-q)) <= H_g(a)+7/50.
```

At `a=0`, both hinges equal one. The concentration-profile claim follows by
the standard identity
`M_p(v)=inf_(a>=0)[H_p(a)+av]`. Since every beta coefficient is an average
of `H_g-H_f`, it is at least `-7/50`; taking the stated compact maxima does
not add a localization error because the unrestricted pointwise estimate is
already available.

## Reproduction and trust boundary

At the exact source commit, all recorded hashes matched. The primary
verifier, its separate polynomial implementation, and all four damage
controls passed normally and under `python3 -O`. Their canonical hashes were

```text
091917b9e63599ad5ad19351b61b68ea35c7b34fc4904a0e14af84f1b5bb41d9
6011b4110c860ce0d5ed15c9991e834c06dc1fd6156c037f6ce3691eb3e81492
```

Run the independent review check from the repository root:

```text
python3 probability/gaussian_uniform_defect_bound_review2/independent_check.py
```

Expected output:

```text
INDEPENDENT_UNIFORM_DEFECT_ENVELOPE_PASS
```

The checkers establish the finite rational inequalities, not the external
continuous-contraction theorem or the universal stochastic transfer. Those
are written analytic obligations audited above. Python arbitrary-precision
integer and `Fraction` arithmetic remain part of the computational trust
base; no solver, floating-point sign, quadrature, random search, or omitted
large artifact is used.

## Literature and novelty boundary

The primary Aishwarya--Li paper proves the needed continuous-contraction
density-value coupling and states full majorisation in dimensions at most two,
with only partial higher-dimensional preservation. A bounded search for
quantitative approximate majorisation under arbitrary contractions did not
locate the shifted-`Gamma(3/2)` envelope or this uniform `7/50` consequence.
That supports novelty plausibility only, not historical priority.

Primary source:

- [Aishwarya--Li, Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture](https://arxiv.org/html/2609.07041v2)
