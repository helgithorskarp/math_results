# A universal upper-density Gaussian hinge window

27 September 2026. Complete analytic author argument. Independent review
and formalization are pending. The unrestricted dimension-three conjecture
remains open.

## 1. Statement and dependencies

Let mu be a bounded probability law on R3, let T be 1-Lipschitz on
its support, and let s>0. Put

    C_s=(2 pi s)^(-3/2), f=mu*gamma_s, g=T#mu*gamma_s,
    H(u)=integral(g-C_s u)_+ - integral(f-C_s u)_+,
    D=E[|X-X'|^2-|TX-TX'|^2],  X,X' iid with law mu.

**Theorem.** With the absolute constant delta=2^(-32),

    H(u)>=0                         for all u>=exp(-delta).       (1)

If D>0, the inequality is strict for exp(-delta)<=u<max(g)/C_s.
If D=0, all hinges agree at every threshold. The nonstrict assertion
(1) holds for arbitrary probability laws as well, without a moment assumption.

This is a universal interval of actual hinge signs, with no support-radius
or noise restriction. The particular constant is a loose sufficient bound.
The result does not settle lower thresholds, full majorisation, or a new
Kneser--Poulsen class.

The problem is [Aishwarya--Li, Conjecture 1.1](https://arxiv.org/html/2609.07041v2).
The mode-posterior normalization and the two-observation bound in Section 2
are taken from, and proved here consistently with,
[R5's cubic beta region, Section 4](../gaussian_beta_cubic_region/PROOF.md),
graph height 6562, source commit
45dc3e6b3d582426e3238e9529f5008450a7054d.
Its independent review is
[review2](../gaussian_beta_cubic_region_review2/REVIEW.md), source commit
acaa0464b66ed472a08f7ff20edfdae1d6792363.
We use only the mixture localization, not a beta sign as a premise.

The lifted moment normalization and the need to retain the Abel boundary
term come from the earlier
[high-noise hinge window](../gaussian_majorisation_high_noise_window/PROOF.md),
graph height 6008. Its support-dependent window requires s>=2R^2.
Here both the local coarea sign and its globalization to the hinge are
proved with no such premise. In particular we do not assume the global
coarea differentiability used in that earlier argument.

All constants and geometric estimates below are in dimension six. Norms
of derivatives are Euclidean multilinear operator norms; matrix norms
are spectral norms. Surface measure on S5 is unnormalized, of area pi^3.
Scaling x by sqrt(s) reduces the theorem to s=1, preserving H(u).
We work at that variance until the last section.

## 2. Uniform control of a mixture near a nearly unit mode

Let nu be any bounded probability law on R6 and define

    Q(z)=E exp(-|z-Z|^2/2),  V=-log Q.

This positive smooth function tends to zero at infinity and attains a
maximum. Suppose max Q=exp(-sigma) with 0<=sigma<=delta.
Translate a mode to zero and define its posterior law

    d pi(Y)=exp(-|Y|^2/2) d nu(Y)/Q(0).

Differentiation at the mode gives E_pi Y=0. Therefore

    Q(z)=exp(-sigma-|z|^2/2)L(z),
    L(z)=E_pi exp(z.Y)>=1,
    V(z)=sigma+|z|^2/2-log L(z).                              (2)

We give uniform derivative bounds, including rare distant components.
For 2<=k<=5, r>=0, and 0<=a<=1,

    r^k exp(-r^2/2+a r) <= 4096(1-exp(-r^2/2)).              (3)

For r<=1, use 1-exp(-r^2/2)>=r^2/4, r^k<=r^2, and e<3.
For r>=1, the denominator is at least 1/3, while
a r-r^2/2<=1-r^2/4 and

    sup_(r>=0) r^k exp(-r^2/4)=(2k/e)^(k/2)<320.

Thus the ratio in (3) is less than 9*320<4096.
Since exp(sigma)-1<=2sigma for sigma<=1, (3) gives on B1

    ||D^k L||<=eta:=8192 sigma                  (2<=k<=5).

The mode equation and integration along a line give ||DL||<=eta and
0<=L-1<=eta/2 there. Here eta<=1. The partition formula for derivatives
of log L, using L>=1, now gives

    ||D^k log L||<=256 eta=:e0=2^21 sigma       (0<=k<=5).     (4)

For 1<=k<=5, the sums of absolute partition coefficients are
1,2,6,26,150; the estimate uses eta^j<=eta.
For k=0, use log L<=L-1. Thus (4) is an actual operator-norm bound,
not a coordinatewise estimate with an omitted dimension factor.

The following separate observation locates *all* the relevant levels.
For every center, one of its distances to z and 0 is at least |z|/2.
Averaging the two kernels yields

    Q(z)+Q(0)<=1+exp(-|z|^2/8).                              (5)

If V(z)<=delta, then both terms on the left are at least exp(-delta).
Using exp(-delta)>=1-delta and -log(1-2delta)<=4delta gives

    |z|^2<=-8 log(2 exp(-delta)-1)<=32delta<1/16.             (6)

Consequently the complete high superlevel set lies inside B_(1/4).
There are no unaccounted distant components of those levels.

## 3. An explicit quadratic normal form

Define the symmetric matrix field on B1

    B(z)=2 integral_0^1 (1-t) Hess V(tz) dt.

Taylor's integral formula, grad V(0)=0, and (2) give

    V(z)-sigma=(1/2) z^T B(z) z,
    ||D^j(B-I)||<=e0                       (0<=j<=3).        (7)

Let S=B^(1/2) be the positive matrix square root and set F(z)=S(z)z.
The binomial power series for (I+E)^(1/2) has coefficients of absolute
value at most one. Differentiating products of n factors at most three
times gives a norm bound n^3 e0^n. Since e0<=1/4,

    sum_(n>=1) n^3 e0^n
     = e0(1+4e0+e0^2)/(1-e0)^4 <= 8e0.

Hence ||D^j(S-I)||<=8e0 for 0<=j<=3. With

    epsilon=32 e0=2^26 sigma<=1/64,

we obtain

    |F(z)-z|<=epsilon |z|/4,
    ||DF-I||<=epsilon/2,
    ||D^2 F||<=3epsilon/4,   ||D^3 F||<=epsilon.             (8)

In particular F is injective on B1: subtracting its values and
integrating DF-I along the segment proves the lower Lipschitz bound
|F(z)-F(w)|>=(1-epsilon/2)|z-w|.
For |y|<1/2, the map z -> y-(F(z)-z) is a contraction of the closed
ball of radius 3/4 into itself. Its unique fixed point is the inverse
Psi(y). The inverse function theorem and differentiation of
F(Psi(y))=y show that this inverse is C3, with

    |Psi-y|<=epsilon/4,    ||D Psi-I||<=epsilon,
    ||D^2 Psi||<=6epsilon, ||D^3 Psi||<=17epsilon.            (9)

Indeed ||(DF)^(-1)||<=2, so the second derivative bound is
2*(3epsilon/4)*2^2=6epsilon. The third is at most
16epsilon+54epsilon^2<=17epsilon.

The identity in (7) becomes

    V(Psi(y))=sigma+|y|^2/2.                                (10)

Equations (6) and (8)--(10) show, for every sigma<=w<=delta, that the
*entire* sublevel set {V<=w} is exactly the image under Psi of
{|y|<=sqrt(2(w-sigma))}. Both inclusions matter here. All original
points are in B_(1/4) by (6), and every point of the indicated y ball
has an inverse in B_(3/4) by construction. There is a unique mode.

## 4. A Helmholtz bound uniform over every marked-pair midpoint

Write P=D Psi, J=det P>0, and, on B_(1/2), put

    a(y)=|y|^2-|Psi(y)|^2+log J(y).

The usual differentiation formulas for log det P give

    ||grad log J||<=72epsilon,
    ||Hess log J||<=204epsilon+864epsilon^2<=256epsilon.

For example the second derivative is
tr(P^(-1)D^2P-P^(-1)DP P^(-1)DP); the trace bound includes the factor
six. Using (9), |Psi|<=1, and ||P||<=1+epsilon, we conclude

    |grad a|<=75epsilon,  ||Hess a||<=288epsilon,
    |Delta Psi|<=36epsilon,
    |Delta Psi+2P grad a|<=192epsilon.                       (11)

Fix **any** vector m in R6, with no bound on its size, and define

    W_m(y)=exp(|y|^2-|Psi(y)-m|^2)J(y)
          =exp(2m.Psi(y)+a(y)-|m|^2)>0.

Direct differentiation gives the quadratic identity

    Delta W_m / W_m
     =4|P^T m|^2 + 2m.(Delta Psi+2P grad a)
                      +|grad a|^2+Delta a.                 (12)

The least singular value of P is at least 1-epsilon>=1/2.
Complete the square in m in (12), then use (11):

    Delta W_m / W_m
     >=-|Delta Psi+2P grad a|^2-1728epsilon
     >=-36864epsilon^2-1728epsilon >=-36.                   (13)

The last inequality uses epsilon<=1/64, giving 9+27=36.
This is the decisive uniformity. Bounding the linear tilt on its own would
lose all control for rare marked points far from the mode. Its positive
quadratic term makes (13) independent of the midpoint.

## 5. Spherical comparison signs the local coarea derivative

Let S_m(r)=integral_(S5) W_m(r theta) d theta. The spherical Laplacian
identity and (13) imply, on 0<r<1/2,

    S_m''(r)+5 S_m'(r)/r+36 S_m(r)>=0,
    S_m(0)>0,  S_m'(0)=0.                                  (14)

Let

    b(x)=sum_(k>=0) (-1)^k x^(2k)/(4^k k! (3)_k),
    B0(r)=b(6r).

The convergent series solves b''+5b'/x+b=0, with b(0)=1,b'(0)=0;
thus B0 solves the equality in (14). On 0<=x<=1, the alternating
series and its differentiated series give

    b(x)>=1-x^2/12>=11/12,
    0<=-x b'(x)<=x^2/6<=1/6.                               (15)

The ratios of successive absolute terms are
x^2/[4(k+1)(k+3)] and x^2/[4k(k+3)], respectively, so both
alternating estimates hold on the whole stated interval.
Subtracting the two radial equations gives

    [r^5(S_m' B0-S_m B0')]'>=0.

Its limit at zero is zero. Therefore for 0<r<=1/6,

    r S_m'/S_m >= r B0'/B0 >= -2/11,
    4 S_m+r S_m' >= (42/11)S_m>0.                          (16)

Now take any two marked centers A,B in R6, and set m=(A+B)/2.
Their product kernel factors exactly as

    K_A(z)K_B(z)=exp(-|A-B|^2/4) exp(-|z-m|^2),
    K_A(z)=exp(-|z-A|^2/2).

Consider the measure obtained by pushing
K_A(z)K_B(z)Q(z)^(-2) dz forward under z -> V(z).
On 0<=w<=delta its density is zero for w<=sigma, and for w>sigma
the change of variables in (10) gives the exact density

    A_(Q;A,B)(w)=exp(2sigma-|A-B|^2/4) r^4 S_m(r),
    r=sqrt(2(w-sigma)).                                    (17)

The power is four because dy=r^5 dr d theta and dw=r dr.
Since 36r^2<=72delta<1, (16) applies. Differentiating (17) yields

    A_(Q;A,B)'(w)
     >=(42/11) exp(2sigma-|A-B|^2/4) r^2 S_m(r)>0.           (18)

The density is O((w-sigma)^2) at the mode, and its derivative tends
to zero there. Its extension by zero is C1 on this interval. If
max Q<exp(-delta), the pushed measure has zero mass in the entire
interval and the assertion is vacuous.

Thus (18) is a uniform local monotonicity theorem for every bounded
Gaussian mixture in R6 and every pair of marked centers. It does not
assume that the marked centers have appreciable mixture weight.

## 6. Exact lifted moments and a local inversion without global coarea

For the original contraction define

    Z_t(X)=(sqrt(1-t)X,sqrt(t)TX) in R6,   0<=t<=1,
    d(X,X')=|X-X'|^2-|TX-TX'|^2>=0,
    Q_t(z)=E exp(-|z-Z_t(X)|^2/2),  V_t=-log Q_t,
    M_t(z)=E[d(X,X') K_(t,X)(z) K_(t,X')(z)],
    h_t=M_t/Q_t^2,  C6=(2 pi)^(-3).

All centers and deficits are bounded. Define a positive, locally finite
measure on [0,infinity) by

    rho(E)=integral_0^1 integral_(V_t(z) in E) h_t(z) dz dt.  (19)

Its Laplace transform is finite for positive arguments. Let
a_j=integral_0^1 u^j H(u)du. The exact lifted moment formula is

    a_j=(C6/4) sqrt(j+2) integral exp(-(j+2)w) d rho(w).     (20)

For completeness, put k=j+2, take k iid replicas, and let
q_k(t)=sum_i |Z_t(X_i)-mean Z_t|^2. Gaussian integration gives

    C6 integral Q_t^(k-2) M_t dz
     =k^(-3) E[d(X_1,X_2)exp(-q_k(t)/2)].

The normalized kth-energy difference in dimension three is the difference
of k^(-3/2) E exp(-q_k(t)/2) at the endpoints.
Since q_k'(t)=-sum_(i<j)d(X_i,X_j)/k, differentiation and exchangeability
give (k-1)k^(-3/2)/4 times the time integral of the expectation above.
Dividing by k(k-1) gives (20). This division is exactly the identity
between a hinge moment and the normalized energy difference. Only the
affine function q_k(t) is differentiated, not the endpoint square roots.

Apply (17)--(18) to every marked pair in (19). On [0,delta], rho
has a C1 density

    A(w)=integral_0^1 E[d(X,X') A_(Q_t;Z_t(X),Z_t(X'))(w)] dt,
    A(0)=0,  A'(w)>=0.                                    (21)

Differentiation under these averages is justified uniformly for this
fixed bounded law. Modes lie in the convex hull of the centers, marked
midpoints relative to a mode stay bounded, and (9)--(18) bound the local
density and derivative by a constant times (w-sigma_t)_+^2 and
(w-sigma_t)_+, respectively. The mode depends continuously on t
whenever its maximum exceeds exp(-delta), by uniqueness and uniform
continuity of Q_t. At the entering boundary the displayed bounds tend
to zero. No global smoothness of the density of rho is presumed.

Here is an elementary localization of the inversion. Define

    G(l)=exp(l) H(exp(-l)),
    (I v)(l)=(1/sqrt(pi)) integral_0^l v(w)/sqrt(l-w) dw.

G is continuous and has at most exponential growth of order one.
Changing variables in a_j, (20) says, for integer k>=2,

    Laplace(G)(k)=(C6/4) sqrt(k) Laplace(rho)(k).

Consequently the two measures (I G)(l)dl and (C6/4)d rho(l) have
equal Laplace transforms at every integer k>=2. Multiply both by
exp(-2l), then push them forward under u=exp(-l) onto [0,1].
These are finite signed measures with equal polynomial moments. Polynomial
density in the continuous functions on [0,1] identifies the measures.
Thus, on the local interval where (21) holds,

    I G=(C6/4) A.                                          (22)

Both sides are continuous, so this is pointwise, not merely almost
everywhere. Fubini and the beta integral give I(I G)(l)=integral_0^l G.
Applying I to (22) uses only arguments at most l<=delta. Differentiate,
using A(0)=0 and A in C1, to get

    H(exp(-l))
     =(C6 exp(-l)/(4 sqrt(pi)))
           integral_0^l A'(w)/sqrt(l-w) dw,   0<=l<=delta.  (23)

There is no missing mode atom or boundary term. In particular, irregular
levels outside this interval cannot affect the local inversion.

## 7. Sign, equality, and extensions

Equations (21) and (23) prove (1) for exp(-delta)<=u<=1.
For u>=1 both hinges are zero. Scaling restores every s>0.

For strictness suppose D>0 and u<max(g)/C_s. At t=1, the maximum
of Q_t is max(g)/C_s. Its maximum is continuous in t because the
bounded centers make Q_t uniformly continuous in that parameter.
Hence a time interval of positive length has sigma_t<-log u.
For each such time, the deficits are positive on a set of pairs of
positive probability, and (18) is strictly positive for every such pair
at every sigma_t<w<-log u. Tonelli in (23) proves strict positivity.

If D=0, (20) makes all hinge moments zero. The continuous hinge gap is
zero by polynomial density. Equivalently, continuity of the nonnegative
pair deficit on the support shows that D=0 exactly when every support
distance is preserved.

For an arbitrary probability law, restrict to a ball of radius R and
renormalize, retaining the same map. As R increases, both this law and
its image converge in total variation to the original laws. Gaussian
convolution gives L1 convergence of the densities. The hinge functional
is 1-Lipschitz for the L1 distance, so (1), with its unchanged universal
cutoff, passes to the limit. This extension asserts the nonstrict sign;
it does not impose a finite second moment to define D.

## 8. Trust boundary and useful handoff

The new structural fact is (18): monotonicity of the actual marked-pair
level density uniformly over mixtures and over unbounded midpoints.
The earlier global instantaneous-lift and conditional-kernel objections
do not assert an adverse sign in this universal near-unit interval.
Equation (23) supplies the actual endpoint sign, beyond a sufficient
criterion or a finite moment list. The spherical comparison is static;
no Brownian/contact representation or semigroup factorization is used.

The proof uses elementary differentiation, the matrix square-root series,
the inverse function theorem, a scalar radial comparison, and uniqueness
of finite measures from their moments on a compact interval. All estimates
needed for the universal constant are included. The accompanying audit.py
checks their rational arithmetic, series coefficient ratios, and an Abel
calibration. It neither establishes independent acceptance nor replaces
the argument.

The derivative sign (18) is available as an input to the beta/replica lane;
no extension of its beta array is claimed in this artifact. The remaining
Gaussian question concerns thresholds below exp(-2^(-32)), and this
argument provides no sign there. Source-level and historical novelty
remain subject to independent review.
