# A separated-component spectral window for actual Gaussian hinges

27 September 2026. Complete analytic author argument. Independent review
and formalization are pending. The unrestricted dimension-three question
remains open.

## 1. The theorem and its precise increment

Let x_i -> y_i, 1<=i<=N, N>=2, be a contraction of distinct finite sites
in R3, with **distinct target sites**. Let w_i>0 sum to one. Define

    d=min_(i<j)|y_i-y_j|>0, p=min_i w_i,
    f=sum_i w_i gamma_s(.-x_i), g=sum_i w_i gamma_s(.-y_i),
    C_s=(2 pi s)^(-3/2),
    H(u)=integral(g-C_s u)_+ - integral(f-C_s u)_+,
    D=sum_(i,j) w_i w_j (|x_i-x_j|^2-|y_i-y_j|^2).

**Theorem.** If

    d^2/s >= 65536+8 log(1/p),                             (1)

then

    H(u)>=0 for every u>=exp[-d^2/(512s)].                 (2)

If D>0, (2) is strict at every threshold below max(g)/C_s.
If D=0, all hinges agree. In the sufficient rational version of (1),
replace log(1/p) by any integer b with p>=2^(-b).

The hypotheses allow arbitrary finite cardinality, arbitrarily large source
radius, tight nearest pairs, and vanishingly small positive loss. There is
no degree bound: (2) is a simultaneous sign for actual hinges throughout
the stated interval. The constants are deliberately loose.

Consequently any adverse hinge in the certified regime satisfies

    -s log u > d^2/512.                                   (3)

For fixed finite input, every positive normalized threshold band is signed
at all sufficiently small variances. The result says nothing about target
collisions or thresholds below (2). In particular it does not prove full
majorisation or a new Kneser--Poulsen inequality.

The sole problem is [Aishwarya--Li, Conjecture 1.1](https://arxiv.org/html/2609.07041v2).
The structural predecessor is the
[universal peak window6580](../gaussian_universal_peak_window/PROOF.md),
source 9e18bbc050edb580004c4bef6d251e9238ad651f, independently accepted at
graph6592 in [this review](../gaussian_universal_peak_window_review2/REVIEW.md),
source 5947eff60b62832dcafdb61304cb4a60378466a5. We extend its quadratic
normal form, midpoint square completion, and spherical comparison from
one nearly unit mode to all separated mixture components. Its local
measure/Abel inversion is included below, with the same normalization.

The accepted [finite-degree small-noise exclusion6386](../gaussian_atomic_low_noise_exclusion/PROOF.md),
source 02b579d7e9c77053d7399096fe9314b9fdfca6f1, signs each fixed Hankel
matrix at sufficiently small noise. Its
[review6392](../gaussian_atomic_low_noise_review_frontier/REVIEW.md)
is at source 49a5aa6de6d9574c52ff4efab4e61e425f340874.
That result handles collisions and is not superseded here. It is context,
not a premise: the present proof uses no replica-exponent optimization,
Hankel-degree extension, or counterexample search.

## 2. Every high level lies in a separated component

Normalize the variance to one. Consider an arbitrary finite mixture in R6

    Q(z)=sum_i w_i exp(-|z-c_i|^2/2),  V=-log Q,

with pairwise center distances at least a and weights at least p. Assume

    a^2>=65536+8 log(1/p), and put L=a^2/512.               (4)

In particular a>=256. Around a center c_i, write

    Q(z)=w_i exp(-|z-c_i|^2/2)(1+theta_i(z)),
    theta_i(z)=sum_(j!=i)(w_j/w_i)
      exp[-|c_j-c_i|^2/2+(z-c_i).(c_j-c_i)].

On the ball B(c_i,a/4), the exponent in each summand is at most
-|c_j-c_i|^2/4. For 0<=k<=5, the function r^k exp(-r^2/4) is decreasing
on r>=a. Euclidean multilinear derivative norms therefore obey

    ||D^k theta_i|| <= p^(-1) a^5 exp(-a^2/4)=:tau.        (5)

The weights are summed before using 1/w_i<=1/p; there is no additional
cardinality or source-diameter factor. Let

    phi_i=log(1+theta_i),
    eta=256 tau, epsilon=2a eta.

The parameter guard implies

    epsilon=512 p^(-1) a^6 exp(-a^2/4)<=a^(-3).            (6)

Here is an elementary bound sufficient for (6). For a>=256,
log a<=a/8: the difference a/8-log a is positive at 256, using e>2,
and has positive derivative there and thereafter. Also
9+9a/8<=a^2/8. Hence

    log(512a^9)<9+9a/8<=a^2/8,
    log(1/p)<=a^2/8,
    512p^(-1)a^9 exp(-a^2/4)<=1.

It follows in particular that tau<=1 and eta<=1/4. The partition formula
for derivatives of log(1+theta_i), with denominator at least one, gives

    ||D^k phi_i||<=eta,                       0<=k<=5.    (7)

For orders one through five the absolute partition coefficient sums are
1,2,6,26,150, all below 256; products of derivatives in (5) are bounded
by tau because tau<=1. Order zero uses log(1+theta_i)<=theta_i.
These are multilinear operator-norm bounds, not entrywise estimates.

On B(c_i,a/4) we have

    V(z)=-log w_i+|z-c_i|^2/2-phi_i(z),
    Hess V >= (1-eta) I.                                 (8)

The map z -> c_i+grad phi_i(z) is a contraction of the ball B(c_i,2eta)
into itself. It has a unique fixed point z_i with |z_i-c_i|<=eta.
This is the unique mode in B(c_i,a/4). Write sigma_i=V(z_i)>=0.

Finally Q(z)<=max_i exp(-|z-c_i|^2/2), so

    {V<=L} is contained in the union of B(c_i,a/16).       (9)

These balls are disjoint. Thus every high superlevel component is in a
region where (7)--(8) hold. No component near a saddle or outside these
balls can be omitted from the ensuing calculation.

## 3. Uniform quadratic coordinates on each component

Fix i and center coordinates at z_i. On |x|<=R=a/8, the entire segment
z_i+t x remains in B(c_i,a/4). Set

    B(x)=2 integral_0^1 (1-t) Hess V(z_i+t x) dt,
    F(x)=B(x)^(1/2)x.

Then

    V(z_i+x)-sigma_i=|F(x)|^2/2,
    ||D^j(B-I)||<=eta,                         0<=j<=3.

The matrix square-root series gives

    ||D^j(B^(1/2)-I)||<=8eta,                  0<=j<=3.

Indeed each coefficient has absolute value at most one, derivatives of a
product of n factors contribute at most n^3 eta^n, and

    sum_(n>=1)n^3 eta^n
      =eta(1+4eta+eta^2)/(1-eta)^4<=8eta    for eta<=1/4.

Consequently, on the radius-R ball,

    |F(x)-x|<=epsilon/2,
    ||DF-I||, ||D^2F||, ||D^3F|| <=epsilon.                (10)

For the derivative estimates, respectively bound 8eta(R+1), 8eta(R+2),
and 8eta(R+3) by 2a eta, using a>=256. The displacement bound is
8eta R=a eta.

By (6), epsilon<=1/64. The map F is injective on the radius-R ball.
For |y|<a/12, the map x -> y-(F(x)-x) contracts the closed radius-R ball
into itself because a/12+epsilon/2<a/8. Denote its inverse by Psi.
It has values in that ball and satisfies

    V(z_i+Psi(y))=sigma_i+|y|^2/2,
    |Psi-y|<=epsilon/2, ||D Psi-I||<=2epsilon,
    ||D^2 Psi||<=8epsilon, ||D^3 Psi||<=18epsilon.          (11)

The inverse derivative formulas give the last two bounds as
2*epsilon*2^2 and 16epsilon+96epsilon^2, respectively. The Jacobian
J=det D Psi is positive.

For sigma_i<=w<=L, (9) and |z_i-c_i|<=eta put every point of the ith
sublevel component inside the chart. Conversely every y with
|y|<=sqrt(2(w-sigma_i)) has |y|<=a/16<a/12 and an inverse in the chart.
Equation (11) puts that inverse in {V<=w}; (9) then assigns it to the
same center ball. Thus this entire component is exactly the image of the
round ball of radius sqrt(2(w-sigma_i)). If sigma_i>L it contributes
nothing. The component boundaries and the coordinates have both been
accounted for.

## 4. A midpoint-uniform spectral bound on the larger charts

Write P=D Psi and

    A0(y)=|y|^2-|Psi(y)|^2+log J(y).

The log-determinant derivative formulas, including the factor six in a
trace bound, give

    |grad log J|<=96epsilon,
    ||Hess log J||<=216epsilon+1536epsilon^2<=256epsilon.

Using |Psi|<=a/8 and (11) yields, on |y|<a/12,

    |grad A0|<=(97+a/2)epsilon<=a epsilon,
    ||Hess A0||<=(266+2a)epsilon<=4a epsilon,
    |Delta Psi|<=48epsilon.                              (12)

For the second estimate use ||P^T P-I||<=5epsilon and
||D^2 Psi||<=8epsilon. All displayed simplifications hold for a>=256.

For any midpoint m in R6, with no restriction on its distance from this
component, define

    W_m(y)=exp(|y|^2-|Psi(y)-m|^2)J(y)
          =exp(2m.Psi(y)+A0(y)-|m|^2).

Differentiation gives

    Delta W_m/W_m
     =4|P^T m|^2+2m.(Delta Psi+2P grad A0)
                          +|grad A0|^2+Delta A0.         (13)

The least singular value of P is at least 1/2. From (12),

    |Delta Psi+2P grad A0|<=5a epsilon,
    Delta A0>=-24a epsilon.

Completing the square in m in (13), then using (6), proves

    Delta W_m/W_m >=-25a^2 epsilon^2-24a epsilon
                   >=-49/a^2.                           (14)

The positive quadratic term is essential: marked centers may be arbitrarily
far from the local mode. No global source-radius bound can be inserted here.

Let S_m(r) be the unnormalized spherical mean of W_m on S5. It satisfies

    S_m''+5S_m'/r+(49/a^2)S_m>=0.

The regular solution of the corresponding equality is

    B0(r)=b(7r/a),
    b(x)=sum_(k>=0)(-1)^k x^(2k)/(4^k k! (3)_k).

For 0<=x<=1 its alternating series gives b(x)>=11/12 and
0<=-x b'(x)<=1/6. The Wronskian
r^5(S_m'B0-S_m B0') has nonnegative derivative and vanishes at zero.
Since r<=a/16 implies 7r/a<=7/16<1, it follows that

    4S_m(r)+rS_m'(r)>=(42/11)S_m(r)>0.                   (15)

This is the same scalar spherical comparison as in the peak-window
proof, with its spectral parameter scaled to the separation length.

## 5. Every marked-pair coarea density is increasing on [0,L]

Fix any marked centers U,V0 in R6 and let K_U(z)=exp(-|z-U|^2/2).
The measure K_U K_V0 Q^(-2) dz, pushed forward by z -> V(z), has on the
ith component the density

    A_i(w)=exp(2sigma_i-|U-V0|^2/4) r^4 S_(m_i)(r),
    m_i=(U+V0)/2-z_i, r=sqrt(2(w-sigma_i)),               (16)

for w>sigma_i, and zero below sigma_i. This follows from (11) and

    K_U(z)K_V0(z)=exp(-|U-V0|^2/4)
                     exp(-|z-(U+V0)/2|^2).

The exponent four in (16) is r^5 dr divided by dw=r dr.
By (15),

    A_i'(w)>=(42/11)exp(2sigma_i-|U-V0|^2/4)
                         r^2 S_(m_i)(r)>0.               (17)

Its zero extension is C1 at sigma_i: A_i=O((w-sigma_i)^2) and
A_i'=O(w-sigma_i). Sum (16) over all centers. Equation (9) ensures that
this is the **complete** marked-pair level density on [0,L]. It is C1,
zero at zero, and nondecreasing, with positive derivative whenever w
exceeds at least one component's minimum.

This local result signs a complete level interval even though other,
possibly critical, levels of the same mixture may lie above L.

## 6. Transfer to the actual endpoint hinge

Use the orthogonal lift

    Z_t(i)=(sqrt(1-t)x_i,sqrt(t)y_i)/sqrt(s),  0<=t<=1,
    delta_ij=(|x_i-x_j|^2-|y_i-y_j|^2)/s>=0.

Every pair of its centers has distance at least a=d/sqrt(s), at every t.
The mixture weights are unchanged, so Sections 2--5 apply uniformly.
Let Q_t,V_t be their unit-variance mixture and potential, and put

    M_t(z)=sum_(i,j)w_i w_j delta_ij K_(Z_t(i))(z)K_(Z_t(j))(z),
    h_t=M_t/Q_t^2, C6=(2pi)^(-3).

Define a positive measure rho on the potential levels by pushing h_t dz
forward under V_t and then averaging over 0<=t<=1. Its Laplace transform
is finite at every positive argument. The exact lifted moment identity is

    integral_0^1 u^j H(u)du
     =(C6/4)sqrt(j+2) integral exp(-(j+2)w) d rho(w).      (18)

The normalization can be checked without any real-order differentiation.
For k=j+2 replicas, let q_k(t) be their centered squared scatter in R6.
Gaussian integration gives

    C6 integral Q_t^(k-2) M_t
      =k^(-3) E[delta_(I1,I2)exp(-q_k(t)/2)].

Differentiate the dimension-three endpoint replica energy
k^(-3/2) E exp(-q_k(t)/2), using
q_k'=-sum_(r<v)delta_(Ir,Iv)/k. Exchangeability gives the factor
(k-1)k^(-3/2)/4. Divide by k(k-1), as in the hinge-moment identity,
to obtain (18). The scatter is affine in t, so endpoint square-root
derivatives are not taken.

On [0,L], Sections 2--5 give rho a C1 density A with

    A(0)=0, A'(w)>=0.                                    (19)

Indeed it is a finite sum of the component densities (16), weighted by
w_i w_j delta_ij, and integrated over t. For this fixed input the centers
and marked midpoints stay bounded in t. The uniform chart estimates and
the O((w-sigma_i)_+^2), O((w-sigma_i)_+) bounds justify differentiation
under the time integral, including the entering component minima.
The modes depend continuously on t by their unique contraction equations.

For clarity, the inversion needs no assertion about global regular levels.
Set G(l)=exp(l)H(exp(-l)) and

    (I v)(l)=(1/sqrt(pi)) integral_0^l v(w)/sqrt(l-w) dw.

Equation (18) implies that (I G)(l)dl and (C6/4)d rho(l) have equal
Laplace transforms at every integer k>=2. Multiplying both by exp(-2l)
and pushing forward under u=exp(-l) gives finite signed measures on [0,1]
with equal polynomial moments. Polynomial density identifies them.
On [0,L] their continuous densities therefore satisfy I G=(C6/4)A.

The beta integral gives I(I G)(l)=integral_0^l G. Apply I again and
differentiate locally, using A(0)=0. The exact result is

    H(exp(-l))=(C6 exp(-l)/(4 sqrt(pi)))
                integral_0^l A'(w)/sqrt(l-w) dw,
                         0<=l<=L.                        (20)

The zero density at each mode removes its boundary term. Levels above L
do not enter (20). Equations (19)--(20) prove (2).

If D>0 and u<max(g)/C_s, a positive time interval near t=1 has a
component minimum below -log u. On those times at least one pair deficit
is positive, and (17) is positive for that pair on a nonempty level
interval. Tonelli in (20) proves the strict assertion. If D=0, all pair
distances agree and (18), or an isometric alignment, gives equality at
every threshold. Values u>=1 give zero for both hinges.

## 7. Scope and reproduction

At fixed finite geometry and positive weights, the right side of (2)
tends to zero exponentially as s decreases. Unlike a finite-degree
criterion, the theorem leaves no adverse hinge in the certified normalized
threshold band, even if the threshold and any witnessing polynomial
depend on s. The degree theorem6386/6392 still covers collisions and has
its own loss-dependent quantitative content; it is not replaced wholesale.

The distinct-target and positive-weight hypotheses are material. No
uniform conclusion through a shrinking target separation or changing
weights is claimed unless the displayed guard holds. Ball-volume limits
probe exponentially small thresholds too, so (3) is not an unrestricted
Kneser--Poulsen proof.

The proof is analytic and unformalized. The exact audit checks its rational
constant bounds and the executable geometric hypotheses, including boundary
and rejected inputs. It does not establish the theorem by sampling Gaussian
integrals. All source, data and checks are compact and self-contained; there
is no external certificate corpus, numerical solver, or hidden computation.
The reader can inspect the earlier peak-window proof for the same local
inversion, but that inversion is fully supplied here as well.
