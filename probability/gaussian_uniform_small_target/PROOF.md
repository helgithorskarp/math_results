# A uniform all-threshold Gaussian comparison with a small target

27 September 2026. Complete author proof, pending independent review.
The unrestricted dimension-three contraction question remains open.

This supplies an actual lower-tail/upper-window join, uniformly over a
bounded full-covariance source class. It compares arbitrary endpoint laws;
no map between them is required. Its application to strongly damped
contractions permits every fixed positive Gaussian variance, at the cost
of a variance-dependent damping bound. It gives no new Kneser--Poulsen case.

The concurrent R2 [dilated-martingale theorem](../gaussian_dilated_martingale_certificate/PROOF.md)
already gives all thresholds for much larger targets at sufficiently large
variance. Use it where it is stronger. Our complementary parameter range
comes from a pointwise tail comparison and the classical homothety flow,
not from extending either R3 or R8 effective small-loss cutoff.

## 1. Statement

Work at variance one and write C=(2pi)^(-3/2). For a density rho set
H_rho(h)=integral(rho-h)_+. Let X,Y have arbitrary
bounded probability laws in R3, centered separately, with

```
|X|<=R,  Cov(X)>=kappa I,  kappa=2^-j,
R>=1 an integer, j>=0 an integer.
```

Only feasible hypotheses matter; necessarily 3kappa<=R^2. Define integers

```
Z=j+3+R^2,            zeta=2^-Z,
S=4R 2^j (5R^2+2j+4),
m=(S+R)^2,
B=m+j+5Z+R^2+14.                                      (1)
```

**Theorem 1.** If

```
|Y| <= b,    b=2^(-B-1),                               (2)
```

then f=law(X)*gamma and g=law(Y)*gamma satisfy

```
H(u)=integral(g-Cu)_+ - integral(f-Cu)_+ >=0
                                      for EVERY u>=0.  (3)
```

The inequality is strict for every 0<u<max(g)/C. On the whole possibly
adverse upper window it has the explicit margin

```
H(u)>=2^(-B-1),    2^-m<=u<=max(f)/C.                  (4)
```

There is no atom-count or minimum-mass assumption. Both laws may be
diffuse, and their weights or supports may vary throughout the stated
class. The target may have full covariance. There is no required pairing,
contraction, convex-order witness or spherical-gap certificate between
these endpoint laws.

**Corollary 2 (arbitrary sufficiently damped contractions).** For every
1-Lipschitz F on the source support and every

```
0<=c<=2^(-B-2)/R,                                     (5)
```

law(X)*gamma is majorised by law(c F(X))*gamma. Arbitrary target
translations do not matter. Indeed
|F(x)-E F(X)|<=E|x-X|<=2R, so its centered damped radius meets (2).
Here c<=1, so the prescribed map is also a contraction.

For variance s>0, apply the theorem to independently centered coordinates
divided by sqrt(s). Choose R>=max(1,source radius/sqrt(s)) and a dyadic
2^-j no greater than the normalized least covariance eigenvalue. The
target condition is radius/sqrt(s)<=2^(-B-1). The normalized hinge is
invariant under this spatial change. The permitted c depends on s; no
positive c working down to s=0 is asserted.

Example: R=1,j=2 gives S=208,m=43681,Z=6,B=43728. At unit variance,
every centered source in B1 with covariance at least I/4 has its Gaussian
convolution majorised by that of every centered target supported in
B_(2^-43729). These conservative constants are not optimized.

## 2. Covariance forces a uniform mass in every direction

For a unit theta put W=theta.X. Since E W=0 and |W|<=R,

```
E W_+ = E|W|/2 >= E W^2/(2R) >= kappa/(2R).
```

Set

```
a=kappa/(4R),   p=kappa/(4R^2).
```

The bound E W_+<=a+R P(W>=a) gives

```
P(theta.X>=a) >= p        for EVERY unit theta.         (6)
```

This is a uniform aggregate mass bound, not a lower bound on individual
atoms or arbitrarily fine support-net cells. It therefore remains valid
for diffuse laws and disappearing atom weights.

For r>=0, the source and target Gaussian formulas imply

```
f(r theta)/C >= p exp(-r^2/2+ar-R^2/2),
g(r theta)/C <=   exp(-r^2/2+br).                       (7)
```

If b<=a/2, these inequalities show f>=g for every |z|>=S whenever

```
S >= (R^2+2 log(1/p))/a.                               (8)
```

The integer S in (1) suffices: using log2<1 and log R<=R^2 gives

```
log(1/p)=j log2+log4+2log R <= j+2+2R^2,
aS=5R^2+2j+4=R^2+2(j+2+2R^2).                        (9)
```

The comparison is strict for |z|>S, because the exponent in (7) has
positive slope a-b>=a/2. No asymptotic remainder is used.

## 3. Sign every sufficiently small threshold

Inside B_S the elementary Gaussian lower bounds, and b<=R, give

```
f(z),g(z) >= C exp(-(S+R)^2/2).
```

Since log2>=1/2 and m=(S+R)^2, every 0<u<=2^-m is below this common
lower bound after normalization. Thus inside B_S both truncations
min(f,Cu),min(g,Cu) equal Cu. Outside B_S, (7)--(9) give
min(f,Cu)>=min(g,Cu) pointwise. Since both densities integrate to one,

```
H(u)=integral min(f,Cu)-integral min(g,Cu) >=0,
                                      0<u<=2^-m.       (10)
```

For any such u, sufficiently far outside the ball both densities are
below Cu, and f>g on a set of positive volume. Hence (10) is strict.
There is no exchange of a vanishing-loss or vanishing-mass limit with
a threshold limit. The same S works for the entire source/target class.

## 4. Uniform separation of the source peak from C

Independence of X,X' and the Gaussian product identity give, for every z,

```
(f(z)/C)^2
 = E exp(-|z-X|^2/2-|z-X'|^2/2)
 <= E exp(-|X-X'|^2/4)
 <= 1-E|X-X'|^2/[4(1+R^2)].                            (11)
```

For the second inequality, 1-e^-v>=v/(1+v) and
|X-X'|^2<=4R^2 suffice. Write V=E|X|^2>=3kappa, so
E|X-X'|^2=2V. Using sqrt(1-q)<=1-q/2 gives

```
max(f)/C <= 1-3kappa/[4(1+R^2)] <=1-3zeta.             (12)
```

The last inequality follows from
4(1+R^2)<=2^(3+R^2), valid for integer R>=1. This standard pair-overlap
peak bound is credited in SOURCES.md; it is recalled to fix constants.

## 5. A terminal homothety supplies the upper-window margin

Let f_t=law(tX)*gamma, 0<=t<=1, let N be an independent standard Gaussian,
and fix h>0. The classical homothety pressure identity is

```
-d/dt integral(f_t-h)_+
 = h t integral_{f_t>h} tr Cov(X | tX+N=z) dz,  t>0.    (13)
```

For completeness, the density evolves with velocity
v_t(z)=E[X | tX+N=z]. Gaussian posterior differentiation gives
Dv_t(z)=t Cov(X | z), while partial_t f_t+div(f_t v_t)=0.
For a smooth convex energy U, integration by parts gives
d/dt integral U(f_t)=-integral[f_t U'(f_t)-U(f_t)] div(v_t).
Approximate (r-h)_+ by smooth convex energies that vanish for r<h/2,
with uniformly bounded pressures converging to h 1_(r>h). Their spatial
integrands vanish unless f_t>=h/2. These superlevel sets stay in a common
bounded region for 0<=t<=1; the Gaussian mixtures are nonconstant real
analytic functions, so each positive level has measure zero. Dominated
convergence proves the integrated form of (13), including critical h.
At t=0, f_t converges in L1 to gamma. Thus (13) may be integrated down
to zero. It also proves the usual homothety monotonicity. The identity
and that monotonicity are prior tools, not new results here.

Put

```
r0=zeta/4,   t0=zeta/(4R).
```

For 0<=t<=t0 and |z|<=r0, one has |z-tX|<=zeta/2. Therefore

```
f_t(z)>=C exp(-zeta^2/8)>=C(1-zeta^2/8)>max(f).         (14)
```

Here zeta<=1 and (12) suffice. At such z the posterior density relative
to law(X) is gamma(z-tX)/f_t(z)>=exp(-zeta^2/8)>=1/2, since f_t<=C.
The pair-variance identity then gives

```
tr Cov(X | z) >= V/4 >=3kappa/4.                       (15)
```

For h=Cu with 0<u<=max(f)/C, retain only 0<t<t0 and B_r0 in (13).
Homothety monotonicity on the discarded part and (15) imply

```
H_gamma(h)-H_f(h)
 >= h V |B_r0| t0^2/8
 >= h kappa pi zeta^5/(2048 R^2).                     (16)
```

The coefficient is exact: |B_r0|=pi zeta^3/48 and
t0^2=zeta^2/(16R^2). Since C pi>1/8, R^2<=2^(R^2) and
u>=2^-m, (16) gives

```
H_gamma(Cu)-H_f(Cu) >=2^-B,
                        2^-m<=u<=max(f)/C.             (17)
```

This directly bounds the actual hinge. It does not consume the general
five-dimensional target-peak margin or a spherical martingale theorem.

## 6. Perturb the point-mass target and close the join

Gaussian translation and averaging give

```
||g-gamma||_1 <= E|Y| <= b,
|H_g(h)-H_gamma(h)| <= b.                              (18)
```

Indeed the L1 norm of a unit directional Gaussian derivative is
sqrt(2/pi)<1. Combining (2), (17) and (18) proves (4). For u>max(f)/C
the source hinge is zero, so H(u)>=0 directly; it is positive below
max(g)/C. The already proved strict low tail (10) supplies the remainder.
At u=0 the two hinges both equal one and their difference is zero.

The only remaining side condition is b<=a/2. Formula (1) gives
B+1>=j+3+R^2, and R<=2^(R^2), whence

```
b=2^(-B-1)<=2^(-j-3)/R=a/2<=R.                        (19)
```

This completes Theorem 1 and the corollary. The pointwise low tail and
the upper-window bound meet exactly at 2^-m for the same parameter class.

## 7. Certificate and scope

The exact schedule stores S,m,Z,B as integers and never constructs 2^B
to describe the cutoff. Integer sizes still depend on R and j. The finite
checker accepts two independent rational probability laws and verifies
source radius, all covariance principal minors, and target radius after
separate centering. Target coordinates may use an exact dyadic encoding.
No map, Gaussian quadrature or numerical eigenvalue is needed. Failure
of the sufficient guard is UNRESOLVED, not a counterexample.

This result is uniform in laws and covers the whole hinge curve at every
specified variance. It is a neighborhood of point-mass targets, with an
explicit size uniform over the source class, not a sign for the undamped
positive-loss interior or the near-isometry boundary. Its target radius
can be extremely small. In the contraction corollary the raw pair loss
is at least 6kappa-2b^2, since it equals twice the difference of marginal
trace covariances. This is separated from the near-isometry corner at
fixed kappa. R2's dilated-martingale bounds are far stronger
where their variance condition holds; the two results are complementary.

The accepted R3 cutoff is the shared small-loss consumer. R8's midpoint
formula is preserved as independent support by the
[consolidation notice](../gaussian_mean_loss_margin/CUTOFF_CONSOLIDATION.md).
Neither cutoff is extended here. Same-pair degree-two cubature retains
the radius and moment hypotheses when applied on original paired support;
it does not equate the original and cubature hinges. No common rule for
a parameter cell or ordinary rounding guarantee is supplied.

The proof is written analysis pending independent review. Exact code
controls check scalar budgets and finite hypotheses only. No universal
zero-defect theorem, fixed-map all-variance damping neighborhood, or new
Kneser--Poulsen consequence is asserted.
