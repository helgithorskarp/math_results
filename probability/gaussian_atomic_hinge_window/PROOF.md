# A weight-uniform small-noise hinge window for every finite contraction

27 September 2026. Complete analytic author argument; independent review
and formalization pending. The unrestricted dimension-three Gaussian
majorisation question remains open.

## 1. The statement

Let x_i -> y_i, 1<=i<=N, be a contraction in R3. Combine repeated source
sites first, and give the resulting distinct source sites positive weights
w_i summing to one. Target sites may coincide in any pattern. For N>=2 let

    d^2=min { |x_i-x_j|^2, |y_i-y_j|^2 : i<j,
                                      the displayed distance is positive }.

Thus d>0 even if all target sites coincide. At variance s>0 set

    C_s=(2 pi s)^(-3/2),
    f=sum_i w_i gamma_s(.-x_i), g=sum_i w_i gamma_s(.-y_i),
    H(u)=integral(g-C_s u)_+ - integral(f-C_s u)_+,
    D=sum_(i,j) w_i w_j (|x_i-x_j|^2-|y_i-y_j|^2).

**Theorem.** If

    d^2/s >= 131072,                                      (1)

then

    H(u)>=0 for every u>=exp[-d^2/(1024s)].                 (2)

If D>0, the inequality is strict whenever u<max(g)/C_s in this range.
If D=0, all hinges agree, without a noise restriction. For a single
source site they also agree.

The constants are sufficient, not optimized. Neither (1) nor (2) contains
a minimum weight, cardinality, source-radius, loss-floor or polynomial-degree
parameter. They apply simultaneously to all positive priors on the fixed
finite map, including priors that depend on s and tend to zero. There is
no requirement that a nearest pair shorten. Exact target collisions are
included; a *positive* endpoint separation shrinking to zero remains a
material boundary.

In particular, an adverse hinge in the regime (1) must satisfy

    -s log u > d^2/1024.                                  (3)

Every fixed positive normalized threshold band is eventually signed for
every fixed finite contraction, uniformly over its priors. This is an
actual hinge sign, not a finite-degree moment assertion. It does not sign
the remaining exponentially low thresholds or give a new Kneser--Poulsen
inequality.

## 2. The structural change and credited inputs

The previous [separated-component theorem6598](../gaussian_separated_hinge_window/PROOF.md)
treated all six coordinates together. It required distinct targets and
a weight floor. The [peak-window theorem6580](../gaussian_universal_peak_window/PROOF.md),
independently [accepted6592](../gaussian_universal_peak_window_review2/REVIEW.md),
supplied its quadratic normal form, midpoint-uniform square completion,
spherical comparison and local Abel inversion.

Here we disintegrate into **three-dimensional normal fibres**. During the
first half of the orthogonal lift, the source coordinates give separated
normal centers. During the second half, group coincident targets and use
the target coordinates instead. The normal amplitudes depend on the other
three coordinates, but sum to at most one. An active high level supplies
its own amplitude floor. The spherical density is now r*S(r), whose
derivative remains positive by the same midpoint-uniform spectral idea.
Its square-root mode onsets require an absolute-continuity argument.

R8's [covariance-free small-loss proof6596](../gaussian_covariance_free_small_loss/PROOF.md)
also uses three normal directions and locally absolutely continuous coarea
densities. That result, now [accepted6604](../gaussian_covariance_free_small_loss_review2/REVIEW.md),
concerns a different small-loss boundary;
no conclusion from it is assumed here. The estimates, fibre decomposition
and inversion needed below are supplied explicitly. R7's accepted
[finite-degree small-noise theorem6386](../gaussian_atomic_low_noise_exclusion/PROOF.md)
already includes collisions and tight nearest pairs. The present theorem
signs a whole threshold band without a degree or mass floor; it does not
replace the quantitative degree statements of that source.

The sole problem is [Aishwarya--Li, Conjecture 1.1](https://arxiv.org/html/2609.07041v2).
Source provenance and consumer boundaries are in [README.md](README.md).

## 3. A conditional mixture needs no prescribed amplitude floor

Consider a three-dimensional mixture, not necessarily of total mass one,

    q(z)=sum_j b_j exp(-|z-c_j|^2/2), V(z)=-log q(z),
    b_j>0, sum_j b_j<=1, |c_j-c_k|>=a for j!=k,
    a>=256, L=a^2/512.                                   (4)

A mixture with one center is permitted; its separation condition is
vacuous. Since q<=max_j exp(-|z-c_j|^2/2),

    {V<=L} is contained in the disjoint balls B(c_j,a/16). (5)

If the jth ball meets {V<=L}, take z in that intersection. The other
centers are at distance at least 15a/16 from z. Therefore

    e^(-L)<=q(z)<=b_j+exp(-225L),
    b_j >= e^(-L)-e^(-225L) >= (1/2)e^(-L).               (6)

The last inequality follows from L>=128 and e>2. Call a center eligible
if b_j>=(1/2)e^(-L). Every component at the levels being studied is
eligible, even though many of the original amplitudes may be arbitrarily
small. We never delete their contributions to q.

For an eligible center, on B(c_j,a/4), write

    q(z)=b_j exp(-|z-c_j|^2/2)(1+theta_j(z)),
    theta_j(z)=sum_(k!=j)(b_k/b_j)
      exp[-|c_k-c_j|^2/2+(z-c_j).(c_k-c_j)].

For 0<=k<=5, r^k exp(-r^2/4) decreases on r>=a. Summing the amplitudes
before estimating gives the Euclidean multilinear derivative bounds

    ||D^k theta_j||<=b_j^(-1)a^5 exp(-a^2/4)=:tau_j.

Put eta_j=256tau_j and epsilon_j=2a eta_j. Uniformly over eligible centers,

    epsilon_j=512b_j^(-1)a^6 exp(-a^2/4)<=a^(-3).          (7)

Here is an elementary check. For a>=256,

    log a<=a/8,
    log(512a^9)<9+9a/8<=a^2/8,
    log(1/b_j)<=L+log 2<=a^2/8.

For the middle estimate the relevant polynomial is a^2-9a-72>0 and
increasing; for the last, 1+a^2/512<=a^2/8. These imply (7).
In particular eta_j<=1/4 and epsilon_j<=1/64. The partition formula for
derivatives of phi_j=log(1+theta_j) gives

    ||D^k phi_j||<=eta_j, 0<=k<=5.                        (8)

The absolute partition coefficient sums at orders 1,...,5 are
1,2,6,26,150, all below 256; products of the derivative bounds are at
most tau_j because tau_j<=1. The zeroth bound uses log(1+theta)<=theta.
There is no site-count or upper-separation factor in these estimates.

## 4. Normal form and the midpoint-uniform spectral estimate

Fix an eligible center and suppress its subscript. On B(c,a/4),

    V=-log b+|z-c|^2/2-phi(z), Hess V>=(1-eta)I.

The contraction z -> c+grad phi(z) has a unique fixed point z_* in
B(c,2eta), with |z_*-c|<=eta. It is the unique mode in B(c,a/4).
Let sigma=V(z_*)>=0. On |x|<=a/8 define

    B(x)=2 integral_0^1 (1-t) Hess V(z_*+tx)dt,
    F(x)=B(x)^(1/2)x.

Then V(z_*+x)=sigma+|F(x)|^2/2 and
||D^j(B-I)||<=eta for j=0,...,3. The matrix square-root power series
gives ||D^j(B^(1/2)-I)||<=8eta: coefficients have absolute value at most
one, the product derivative count is bounded by n^3, and

    sum_(n>=1)n^3 eta^n=eta(1+4eta+eta^2)/(1-eta)^4<=8eta.

Consequently

    |F-x|<=epsilon/2,
    ||DF-I||, ||D^2F||, ||D^3F||<=epsilon.

For |y|<a/12 the map x -> y-(F(x)-x) contracts the closed radius-a/8
ball into itself. Its inverse Psi satisfies

    V(z_*+Psi(y))=sigma+|y|^2/2,
    |Psi-y|<=epsilon/2, ||D Psi-I||<=2epsilon,
    ||D^2 Psi||<=8epsilon, ||D^3 Psi||<=18epsilon.          (9)

The inverse derivative bounds follow by differentiating F(Psi)=y;
the last uses 16epsilon+96epsilon^2<=18epsilon. The Jacobian
J=det D Psi is positive. By (5) and (9), the entire jth sublevel component
at sigma<=w<=L is the Psi-image of the round ball

    |y|<=sqrt(2(w-sigma))<=a/16.                         (10)

Indeed all points of the original component lie inside the chart, and
every point of this round ball has an inverse whose potential is at most
w. Equation (5) assigns that inverse to the same center ball. No boundary
piece or additional component is omitted. If sigma>L there is no such
component.

Set P=D Psi, A0=|y|^2-|Psi(y)|^2+log J. The following loose bounds,
valid already with dimension-six trace constants, also hold here:

    |grad log J|<=96epsilon,
    ||Hess log J||<=216epsilon+1536epsilon^2<=256epsilon,
    |grad A0|<=a epsilon, ||Hess A0||<=4a epsilon,
    |Delta Psi|<=48epsilon.                              (11)

For the last two derivative estimates one can use |Psi|<=a/8,
||P^TP-I||<=5epsilon, 97+a/2<=a and 266+2a<=4a.
All Laplacians in this section have three coordinates. Using the larger
trace bound six only weakens the estimates.

For **any** m in R3 define

    W_m(y)=exp(|y|^2-|Psi(y)-m|^2)J(y).

Its exact Laplacian ratio is

    Delta W_m/W_m
      =4|P^T m|^2+2m.(Delta Psi+2P grad A0)
                              +|grad A0|^2+Delta A0.

The least singular value of P is at least 1/2, the vector in the linear
term has norm at most 5a epsilon, and Delta A0>=-24a epsilon. Completing
the square in m, then using (7), yields

    Delta W_m/W_m >=-25a^2 epsilon^2-24a epsilon>=-49/a^2. (12)

This is uniform in the marked midpoint, whose distance from the local
mode can be arbitrarily large. Bounding its linear term alone would not
suffice.

Let S_m(r)=integral_(S2) W_m(r theta)dtheta. Spherical integration of
(12) gives

    S_m''+2S_m'/r+(49/a^2)S_m>=0.

The regular comparison solution is B0(r)=b(7r/a), where

    b(x)=sin(x)/x=sum_(k>=0)(-1)^k x^(2k)/(2k+1)!.

For 0<=x<=1, its alternating series and that of its derivative give

    b(x)>=5/6, 0<=-x b'(x)<=1/3.

The derivative of r^2(S_m'B0-S_m B0') is nonnegative and this Wronskian
vanishes at zero. Since r<=a/16 implies 7r/a<1,

    S_m(r)+rS_m'(r) >= (3/5)S_m(r)>0.                   (13)

Thus the lower radial power in dimension three still leaves a positive
margin. A six-dimensional r^4 density has not been substituted for this
three-dimensional r density.

## 5. Complete fibre densities and their mode onsets

Fix any marked centers U,V0 in R3. Let K_U(z)=exp(-|z-U|^2/2).
Push K_U K_V0 q^(-2) dz forward under V=-log q. On the jth component its
density for sigma_j<w<=L is

    A_j(w)=exp(2sigma_j-|U-V0|^2/4) r S_(m_j)(r),
    r=sqrt(2(w-sigma_j)), m_j=(U+V0)/2-z_j.              (14)

It is zero below sigma_j. This follows by polar integration in (9):
the radial volume factor r^2 dr becomes r dw. Equations (13)--(14) give

    A_j'(w)>= (3/5) exp(2sigma_j-|U-V0|^2/4)
                                      S_(m_j)(r)/r>0.   (15)

At its mode A_j=O(sqrt(w-sigma_j)) and
A_j'=O((w-sigma_j)^(-1/2)). Its zero extension is continuous and absolutely
continuous, although generally not C1. The singularity is integrable.
Sum (14) over eligible centers. By (5)--(6) this accounts for the entire
pushforward measure on [0,L], not just a subset of components. Its density
is absolutely continuous, vanishes at zero and is nondecreasing.

This argument also proves the lemma for a single center, where theta=0
and Psi is the identity. Centers or amplitudes may vary with an external
parameter. For subsequent integration the following uniform bound is
useful. At an active level sigma_j<=w<=L, (9) gives J<=8, while

    W_m(y)<=8 exp(|y|^2)<=8exp(2L).

Hence the expression in (14) is at most

    32pi sqrt(2L) exp(4L).                               (16)

The bound does not depend on m or the amplitude floor. Any additional
positive prefactor at most one preserves it.

## 6. Switching the normal coordinates handles all target collisions

Use the normalized orthogonal lift in R3 x R3,

    Z_t(i)=(sqrt(1-t)x_i,sqrt(t)y_i)/sqrt(s),
    q_t(z)=sum_i w_i exp(-|z-Z_t(i)|^2/2), V_t=-log q_t,
    delta_ij=(|x_i-x_j|^2-|y_i-y_j|^2)/s>=0.

Under (1) put a=d/sqrt(2s)>=256 and L=a^2/512=d^2/(1024s).

For 0<=t<=1/2, fix the second coordinate block v and integrate normally
in the first block z. The conditional mixture is exactly (4), with

    c_i=sqrt(1-t)x_i/sqrt(s),
    b_i(v)=w_i exp(-|v-sqrt(t)y_i/sqrt(s)|^2/2).

Its normal centers are pairwise separated by at least a and sum_i b_i<=1.
No lower bound on b_i is assumed.

For 1/2<t<=1, fix the first block v and integrate normally in the second
block z. Partition the labels into exact target coincidence groups J,
write their distinct targets as y_J, and use

    c_J=sqrt(t)y_J/sqrt(s),
    b_J(v)=sum_(i in J) w_i
                   exp(-|v-sqrt(1-t)x_i/sqrt(s)|^2/2).

Distinct normal centers are again separated by at least a; one center
is allowed. The total amplitude is at most one. Internal source geometry
within a collapsed group remains in b_J(v); it is not replaced by a
single source point. These are exact factorizations of the full mixture.

For any marked pair of lifted labels U,V0, the product of their kernels
in either splitting has the form

    c(v) exp(-|z-U_normal|^2/2) exp(-|z-V0_normal|^2/2),
    0<c(v)<=1.

Sections 3--5 therefore apply to its complete normal-fibre pushforward.
The group representation is used only for the denominator; marked pairs
retain their original labels and nonnegative deficits.

Let nu_t be the pushforward under V_t of

    h_t(z) dz,
    h_t(z)=sum_(i,j) w_i w_j delta_ij
                 K_(Z_t(i))(z)K_(Z_t(j))(z)/q_t(z)^2.

It is a positive locally finite measure with finite Laplace transform at
every positive parameter. On [0,L], Fubini and the fibre lemma give it
an absolutely continuous density A_t(w). More explicitly, sum the
densities (14), multiply by c(v)w_iw_jdelta_ij and integrate over v.
Every fibre density has a nonnegative integrable derivative.

Here are the domination details, including varying modes and eligibility.
For this fixed finite input all lifted centers lie in a ball B(0,R0).
If a fibre reaches V_t<=L, its fixed coordinate v lies in
B(0,R0+sqrt(2L)), by the full Gaussian envelope. Formula (16), at most N
components, and sum_(i,j)w_iw_jdelta_ij=D/s bound A_t(L) uniformly in t.
All relevant functions are measurable; an eligible mode is the limit of
its unique contraction iteration. Ineligible centers have no component
on [0,L]. Each component's zero extension satisfies
A_j(w)=integral_0^w A_j'(v)dv. Tonelli, using the nonnegative derivatives
and the bound at L, now proves that

    A(w)=integral_0^1 A_t(w)dt

is absolutely continuous on [0,L], A(0)=0 and A'(w)>=0 almost everywhere.
This does not require bounded mode derivatives, a globally regular level,
or a fixed number of active components. Switching coordinate blocks at
t=1/2 changes no measure identity.

## 7. Local Abel inversion signs the actual hinge

Write rho=integral_0^1 nu_t dt and C6=(2pi)^(-3). For every integer k>=2,
the exact replica identity is

    integral_0^1 u^(k-2)H(u)du
       =(C6/4)sqrt(k) integral exp(-kw)d rho(w).          (17)

For completeness, if q_k(t) is the centered squared scatter of k iid
lifted labels, Gaussian integration in R6 gives

    C6 integral q_t^(k-2) (q_t^2 h_t)
       =k^(-3) E[delta_(I1,I2)exp(-q_k(t)/2)].

The dimension-three endpoint power energy is
k^(-3/2) E exp(-q_k(t)/2). Since
q_k'=-sum_(r<v)delta_(Ir,Iv)/k, differentiation gives the coefficient
(k-1)k^(-3/2)/4 in front of this same pair expectation. Divide by
k(k-1) to obtain the hinge moment. This gives precisely (17); squared
scatter is affine in t, so no singular square-root path derivative is used.

Set G(ell)=exp(ell)H(exp(-ell)) and

    (I F)(ell)=(1/sqrt(pi)) integral_0^ell F(w)/sqrt(ell-w) dw.

Equation (17) identifies the measures (I G)(w)dw and (C6/4)d rho(w).
Indeed their Laplace transforms agree at every integer k>=2; multiply
by exp(-2w) and push forward under u=exp(-w). These are finite signed
measures on [0,1] with equal polynomial moments, so they agree.
Finiteness follows also directly from |H|<=1 and the Gaussian product
formula. This argument makes no global coarea-regularity assertion.

On [0,L] it follows that I G=(C6/4)A. The beta integral gives I^2=I_1.
Apply I again and differentiate in distributions. Absolute continuity
of A and A(0)=0, proved above despite the square-root mode onsets, give

    H(exp(-ell))=(C6 exp(-ell)/(4sqrt(pi)))
                 integral_0^ell A'(w)/sqrt(ell-w) dw     (18)

for almost every 0<ell<L. The right side is nonnegative. H is continuous,
so it is nonnegative throughout the closed interval, including both
ends. For u>=1 both hinges are zero. This proves (2).

If D>0 and u<max(g)/C_s, some point of the terminal lifted mixture has
q_1>u. Continuity gives an open set of times near 1 and fixed-coordinate
fibres whose modal level is strictly below ell=-log u. A marked pair
with delta_ij>0 has positive coefficient on those fibres, and (15) is
strict above that mode. Restrict to a smaller compact set of times,
fibres and a positive-width level interval strictly below ell. Its
positive contribution to (18) is bounded below uniformly for ell' near
ell. The almost-everywhere identity and continuity of H give H(u)>0,
also at ell=L. If D=0, every pair distance agrees, so centered Gram
matrices give an isometry of the finite clouds and equality of all hinges.

## 8. What this closes and what it leaves open

This removes two escape conditions from the earlier actual-hinge window:
arbitrarily small priors and exact target collisions. Both are allowed
uniformly here. The spectral argument is conditional and uses three
normal directions; it does not assert that the entire six-dimensional
mixture remains separated or globally convex.

An adverse finite input must fail (1) or satisfy (3). In particular, if
all positive endpoint separations are at least d0>0 and u>=u0>0, no choice
of atom count or positive weights can preserve adversity as s tends to
zero. If u0=exp(-ell0), the sufficient bound is

    s<=d0^2 / max(131072,1024ell0).

R4's [guarded indecomposable frontier6602](../gaussian_guarded_indecomposable_frontier/HANDOFF.md)
can consume this without a lower weight bound or injective targets. Its
mesh can still introduce arbitrarily small *positive* separations; no
uniform sign of that full frontier is inferred. R7's finite symmetry
reduction and R3/R8 compact controls likewise retain their open interior.

The low thresholds excluded from (2) include the scales relevant to
general ball-union limits. There is no unrestricted Gaussian or
Kneser--Poulsen conclusion. This is a written analytic proof. The exact
audit checks constants and finite premise controls; it does not evaluate
Gaussian hinges, supply an independent review, or formalize the argument.
