# An explicit mean-loss cutoff for Gaussian middle signs

27 September 2026. Complete author proof; independent review pending.
The full dimension-three majorisation question remains open.

R8's [mean-loss theorem](../gaussian_mean_loss_margin/PROOF.md) removes the
full-rank zero-loss boundary qualitatively. This paper makes that removal
effective at every fixed radius, positive covariance floor, and positive
lower threshold. The new ingredient is a quantitative comparison on each
interval component of a Gaussian source superlevel. It replaces both
compactness steps in the rare-displacement argument. Superlevels need not
be convex, have a unique mode, or have regular boundaries.

The accepted Procrustes and actual-top-set first-variation estimates are
credited to R1. The core/rare split and its conditional-alignment estimate
are credited to R8 and recalled below with constants. No new rigidity
lemma, full majorisation theorem, or Kneser--Poulsen consequence is claimed.

## 1. The effective statement

First let the Gaussian variance be one. Set

```
C=(2 pi)^(-3/2), gamma(z)=C exp(-|z|^2/2),
E X=E Y=0, |X|<=R, Cov(X)>=kappa I_3,
Y=an orthogonally aligned, centered 1-Lipschitz image of X,
Delta(x,x')=|x-x'|^2-|Y(x)-Y(x')|^2 >=0,
d=E Delta(X,X'), f=law(X)*gamma, g=law(Y)*gamma,
H(u)=integral(g-Cu)_+ - integral(f-Cu)_+.
```

The orthogonal alignment is Procrustes; the hinge is invariant under this
choice and under the separate centering. Assume R,kappa>0. Fix 0<t<=1,
choose B>=R+sqrt(2 log(1/t)), and any

```
0<w<=exp(-(B+R)^2/2).
```

Define the following explicit positive numbers:

```
K0=2 R^2/kappa,           L=96 R^3/kappa+6R,
K1=16 R/kappa,            K2=2R/t^2,
c0=w^2 min(t/4,1/16),     delta=c0/(4 K1),

d_* = min {
  kappa^2/(4 R^2 K0),
  delta^2/(2 K0),
  kappa delta^2/(8 R^2 K0),
  w^4 kappa^2 delta^2/(144 R^4 K0),
  2 kappa delta/R,
  c0 delta^4/(8 L^2 K0^2),
  c0^2 delta^4/(64 K2^2 K0^3)
}.                                                       (1)
```

**Theorem 1.** If 0<d<=d_*, then, for every u in [t,1] whose source
top set E={f>Cu} is nonempty,

```
integral_E(g-f) >= (C c0/2) |E| d,
H(u) >= (C c0/2) |E| d.                                (2)
```

An empty source top set gives H(u)>=0 directly. Therefore H>=0 on the
whole interval [t,1], and also above 1. If d=0, H is identically zero.
This holds for arbitrary bounded laws, including diffuse laws, and has no
minimum atom mass, atom-count bound, upper bound on Q/d where Q=E Delta^2,
or small maximum aligned displacement hypothesis. There is **no restriction
R<1**. The written constants are sufficient, not optimized.

At Gaussian variance s, use X/sqrt(s), Y/sqrt(s), d=E Delta_raw/s and
Cov(X)/s in (1). The volume in (2) is then |E|/s^(3/2). This is a test at
that variance, not an all-variance result for a fixed input.

**Dyadic corollary.** In the normalization of the previous
[quartic guard](../gaussian_loss_moment_middle/PROOF.md),

```
|X-E X|<=sqrt(s)/2, Cov(X)/s>=2^-15 I_3,
0<=d<=2^-360                                             (3)
```

imply

```
H(u)>=2^-40 d             for EVERY u in [1/64,1/2],
H(u)>=0                  for EVERY u>=1/64.              (4)
```

The 360-bit cutoff is deliberately conservative. It is an exact executable
removal of the zero-loss boundary, not a claim that a cover of the remaining
positive-loss region is cheap. In particular no threshold below 1/64 is
signed by this corollary.

## 2. A quantitative interval-component comparison

Let mu be centered, supported in B(0,R), f=mu*gamma, and E={f>a} be
nonempty, bounded by B(0,B), with a>0. For x,y with |x|<=R, set

```
l=|y-x|>0, e=(y-x)/l, m=(x+y)/2,
q=|x|^2-|y|^2, zeta(z)=(z-m).e,
m0=E_mu zeta=q/(2l), eta=E_mu (zeta)_-,
k_E(x)=integral_E gamma(z-x) dz.
```

Suppose m0>0 and eta<=w^2 m0/2, where
0<w<=exp(-(B+R)^2/2). Then

```
[k_E(y)-k_E(x)]/|E| >= C w^2 q/4.                      (5)
```

Here is a direct proof, including nonconvex E. At every z in B(0,B),
the posterior density r_z(b)=gamma(z-b)/f(z) relative to mu lies in
[w,1/w]. This uses Cw<=gamma(z-b)<=C and the same bounds on f(z).
Consequently

```
E_(posterior at z) zeta
 >= w m0-(1/w) eta >= w m0/2 =: c.                     (6)
```

Slice E by lines parallel to e. On each nonempty interval component use
the coordinate v=(z-m).e and write the endpoints A<D. The endpoint
densities both equal a. The score identity along the line is

```
d/dv log f = -v+E_(posterior) zeta.
```

Integrating between A,D, and using (6), proves

```
(A+D)/2 >= c.                                         (7)
```

Each slice is a finite union of intervals: its density is a nonconstant
real analytic function of v, tends to zero at both ends, and all positive
level roots in a compact interval are isolated. In particular, the
argument does not assume the whole slice is a single interval. Null or
empty slices cause no contribution.

For completeness, write the center and half-length of one component as
b=(A+D)/2 and r=(D-A)/2. The two kernels have equal perpendicular
coordinates, and their parallel centers are -l/2 and l/2. If
phi(v)=(2pi)^(-1/2)exp(-v^2/2) and
F_r(v)=integral_[-r,r] phi(z-v) dz, their interval-integral difference is

```
F_r(b-l/2)-F_r(b+l/2)
 = integral_[|b-l/2|,b+l/2] [phi(v-r)-phi(v+r)] dv.
```

For v>=0,

```
phi(v-r)-phi(v+r)
 = phi(v+r)(exp(2vr)-1) >= 2vr phi(v+r).
```

After multiplying by the common perpendicular Gaussian, the smallest
Gaussian in this lower bound is evaluated at the right endpoint of the
component minus x. That endpoint is in the closed ball of radius B;
thus this Gaussian is at least Cw. The difference is therefore at least

```
2r Cw integral_[|b-l/2|,b+l/2] v dv
 = (D-A) Cw b l >= (D-A) C w^2 q/4.                   (8)
```

Summing components and integrating the perpendicular variables proves
(5). The same computation with eta=0 improves its factor 1/4 to 1/2.
All integrals are over a bounded set, so ordinary Fubini applies to the
signed differences. No boundary differentiation or lower bound on a
level gradient occurs.

## 3. Contraction supplies an approximate half-space

Return to the coupled contraction in Section 1. Set h(x)=Y(x)-x,
M=E|h|^2. Centering and contraction give |Y(x)|<=2R for source labels.
For any label x, y=Y(x), and an independent source label z, contraction
implies

```
2 l zeta(z)=|x-z|^2-|y-z|^2 >= -6R |h(z)|.
```

Indeed expand |y-Y(z)|^2=|y-z-h(z)|^2 and use |y-z|<=3R.
Thus, when l>0,

```
eta<=3R sqrt(M)/l.                                    (9)
```

Let U=z.e. It has mean zero, variance at least kappa, and |U|<=R.
Since zeta=U+m0,

```
R m0-E U^2 = E[(U+m0)(R-U)] >= -2R eta,
m0 >= kappa/R-2 eta.                                 (10)
```

If l>delta and

```
sqrt(M)<=w^2 kappa delta/(12 R^2),                     (11)
```

then eta<=w^2 kappa/(4R), m0>=kappa/(2R)>0, and
eta<=w^2 m0/2. Equations (5) and (10) apply to every such rare label,
with

```
q>=kappa l/R > kappa delta/R.                         (12)
```

The exact mean pair loss of that label is

```
q_x=E_z Delta(x,z)=q+d/2.                             (13)
```

If also d<=2 kappa delta/R, then q>=q_x/2. Hence EVERY rare label
satisfies the quantitative tested-set inequality

```
[k_E(Y(x))-k_E(x)]/|E| >= (C w^2/8) q_x.              (14)
```

This is the effective replacement for the limiting fixed-background
argument in R8's theorem. Rare points need not approach their source
positions. The estimate of their unfavorable half-space mass is explicit
and needs only the whole-law mean square displacement.

## 4. The credited bulk estimate, with all required smallness tests

Procrustes makes A=E[XY^T] symmetric positive semidefinite. R1's accepted
estimate gives

```
M <= E Delta^2/(2 kappa) <= K0 d,   K0=2R^2/kappa,      (15)
```

because 0<=Delta<=4R^2. Let

```
G={|h|<=delta}, J=G^c, alpha=mu(J)<=K0 d/delta^2.
```

We reproduce R8's conditional-alignment bound to make its hypotheses
explicit. Require

```
R sqrt(M)<=kappa/2,
alpha<=min(1/2,kappa/(8R^2)).                         (16)
```

Then A>=kappa I/2 and Cov(X|G)>=kappa I/2. The former follows by
comparing A with Cov(X); the latter follows by removing mass alpha and
subtracting the conditional mean. Conditional source and target means
have norm at most 2 alpha R and 4 alpha R. If B_G is their conditional
centered cross-covariance, direct expansion gives

```
||B_G-A||_F <=12 alpha R^2.
```

If Q_G is an optimal orthogonal conditional alignment, its optimality
and the positivity of A give

```
(kappa/4)||I-Q_G||_F^2
 <=tr((I-Q_G)A)
 <=||I-Q_G||_F ||B_G-A||_F.
```

Thus ||I-Q_G||_F<=48 alpha R^2/kappa. The conditional translation has
norm at most 6 alpha R, so the optimally aligned conditional target
differs from Y by at most L alpha, L=96R^3/kappa+6R.

For two core labels, Delta<=8R delta. Applying (15)'s first inequality
to the conditional law, and returning to the original alignment, gives

```
M_G=integral_G |h|^2 dmu
 <=(32R/kappa) delta d+2 L^2 alpha^2.                  (17)
```

This is R8's bound, including its crucial alpha-squared error. To check
the factor: the conditional optimal square displacement is at most
(8R delta/kappa)d/(1-alpha)^2; multiply by 2(1-alpha) and use
1-alpha>=1/2. The translation/rotation error contributes at most
2L^2 alpha^2.

Let d_GG,d_GJ,d_JJ denote UNNORMALIZED pair losses. On the actual source
top set E={f>Cu}, the accepted posterior-divergence identity is

```
grad k_E(x)=-Cu integral_E integral (x-z)
                gamma(v-x) gamma(v-z)/f(v)^2 dmu(z) dv.
```

On G x G symmetrization, contraction, u>=t, and posterior weights at
least w give a contribution at least C t w^2 |E| d_GG/4. The absolute
G x J cross contribution is at most
2RC t^-2 |E| alpha sqrt(M). Here gamma/f<=1/t on E. Finally
||partial_ee gamma||_infinity<=C gives the integrated Taylor remainder
C |E| M_G/2. Combining these with (17),

```
integral_G [k_E(Y(x))-k_E(x)] dmu(x) / |E|
 >= C [ (t w^2/4)d_GG - K1 delta d
                         - L^2 alpha^2 - K2 alpha sqrt(M) ]. (18)
```

The posterior-divergence identity at critical levels is the regular-value
approximation in the accepted source: positive Gaussian-mixture level
sets are null and nearby top sets are in a common compact ball. The
slice argument of Section 2 itself needed no such approximation.

## 5. Assembly and exact cutoff

The first three entries in (1), together with (15), imply (16). The
fourth entry implies (11); the fifth permits (14). Integrating (14)
over J gives

```
integral_J [k_E(Y(x))-k_E(x)] dmu(x) / |E|
 >= (C w^2/8)(d_JG+d_JJ).                             (19)
```

Since d=d_GG+2d_GJ+d_JJ and d_GJ=d_JG, the favorable coefficients in
(18)--(19) are at least C c0 d for c0 in (1). No pair-loss term or
factor of two is dropped. Also K1 delta=c0/4. The last two entries of
(1) respectively ensure

```
L^2 alpha^2 <= c0 d/8,
K2 alpha sqrt(M) <= c0 d/8.
```

The resulting total is at least C c0 |E| d/2, proving (2).
Testing the target hinge on the same E gives the hinge inequality.
For d=0, (15) gives M=0. For u>1 both hinges vanish.

There are no limits of laws or of loss in this argument. The estimate
also holds uniformly as the nonempty top-set volume tends to zero,
because every estimate is proportional to that volume.

For direct comparison with R8's bounded-volume statement, let
r_V=(3V/(4pi))^(1/3), t=exp(-(r_V+R)^2/2), B=r_V+2R. The lower
Gaussian envelope and the upper tail envelope give a/C>=t and
E_f(v) subset B(0,B) for every 0<v<=V. The SAME proof and constants
therefore give its tested-set margin with an explicit d_*.

## 6. Dyadic constants and a family absent from the quartic guard

Take R=1/2, kappa=2^-15, t=1/64, B=7/2, w=2^-13. The bounds
log 2<3/4, e<3 and 3^8<2^13 establish both required exponential
inequalities. Formula (1) gives

```
K0=2^14, L=393219<2^19, K1=2^18, K2=2^12,
c0=2^-34, delta=2^-54.
```

Each of the seven entries of d_* is at least the dyadic number with
the following negative exponent, in order:

```
44, 123, 138, 208, 67, 319, 356.
```

In particular 2^-360<=d_*. For u<=1/2, the lower Gaussian envelope
puts B(0,1/2) inside E. Therefore |E|>1/2 and C>1/16, proving (4).
The exact checker verifies the seven inequalities and rejects weakened
cutoffs that fail this schedule.

Reuse the credited R6 eight-site geometry with
v_i=(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1):

```
a_i=v_i/80, b_i=-20v_i/80,
Ta_i=(1-tau)v_i/80, Tb_i=(1-tau)(58/3)v_i/80,
0<=tau<=2^-362, 0<=alpha<=2^-362,
p_i>=(1-alpha)/8, sum p_i=1-alpha,
r_i>=0, sum r_i=alpha.                              (20)
```

The two parameters tau and alpha are INDEPENDENT. All conditional
priors in the displayed simplexes are permitted, including zero outer
weights. The distance table in the prior quartic packet proves
contraction, centered radius<=11sqrt(3)/40<1/2, and covariance
>=I/25600>2^-15 I. For clarity, the radius uses alpha<=1/19 and
|E X|<=sqrt(3)/40. The covariance follows directly by retaining the
four core contributions of size at least (1-alpha)/8.

Core pair loss is at most tau/400. Loss on an outer-involving pair is
at most 1, and its total pair probability is at most 2alpha. Thus

```
d<=tau/400+2alpha <=(1/400+2)2^-362 <2^-360.            (21)
```

Equations (3)--(4) sign the whole parameter family. In particular, at
tau=0 and ANY alpha>0 the law still has nonzero loss. Every nonzero
pair loss is either 59/1200 (same-index outer/core) or 59/1800
(distinct outer sites). It follows that

```
Q/d >=59/1800 >2^-48.                                (22)
```

This entire rare-motion boundary fails the old quartic guard. With all
eight weights positive the same prescribed geometry retains R6's
no-R5-motion obstruction, but that obstruction is not a premise of our
Gaussian sign. Balanced within-orbit priors were already signed by R4's
stronger all-variance parity theorem. The present family permits
independent unbalanced priors; no exclusion of every other possible
positive proof or rematching is asserted.

## 7. Certification boundary

[HANDOFF.md](HANDOFF.md) specifies the exact guard and remaining positive-loss
domain. Degree-two paired cubature already preserves the new guard: no
mixed or quartic feature is needed. The new result does not give ordinary
rational rounding for all laws, sign H below the selected t, or sign the
complement d>d_*. A failed guard returns UNRESOLVED.

The accompanying standard-library checker tests exact schedules, the full
parameter inequalities and distance table, direct pair-versus-variance
loss formulas, approximate-half-space controls, and malformed inputs.
The analytic slicing, score identity, and Gaussian integration remain
written mathematics, not proof-assistant verification. The finite tests
are not independent acceptance. See [SOURCES.md](SOURCES.md) for dependency
status and source attribution.
