# A covariance-free small-loss sign at arbitrary Gaussian radius

Complete author argument, 27 September 2026; independent review pending.
The unrestricted dimension-three conjecture remains open. This theorem
removes the covariance premise from a uniform small-mean-loss sign on
each fixed positive-threshold range. With the existing covariance-boundary
theorem it excludes the simultaneous zero-loss, zero-covariance corner
of that compact frontier. It supplies neither the remaining interior sign
nor a uniform conclusion down to threshold zero.

## 1. Statement and exact schedules

Let X be any bounded probability law in R3 and Y=T(X), with T short on
the source support. At variance s>0 put

    C_s=(2 pi s)^(-3/2), f=law(X)*gamma_s, g=law(Y)*gamma_s,
    H(u)=integral(g-C_s u)_+ - integral(f-C_s u)_+,
    d=E[|X-X'|^2-|Y-Y'|^2]/s,       m=max(g)/C_s.

Primes denote independent copies: d is the ORDERED normalized loss.
Assume |X-E X|<=R sqrt(s), with integer R>=1. For integer j>=1 set

    c=ceil sqrt(2(j+1)),       B=3R+c,          S=6R,
    E=BS+2B^2,                F=BS+4B^2+2,
    K=3(E+6)(1+BS)+12F,
    b=ceil log2(3RK),         N=2(j+6RB+b).                 (1)

**Theorem A (uniform small-loss sign without a covariance floor).** If

    d<=2^-N,

then H(u)>=0 for every u>=2^-j. This holds for arbitrary atom weights,
atom counts, diffuse laws and singular or degenerating covariance. If d=0,
H is identically zero by support isometry.

**Theorem B (loss-linear middle margin).** Under the same hypotheses, for
each integer k>=0 put

    P=2[(6R+1)^2+R^2]+2R+2j+5k+19.                        (2)

On the possibly empty closed band 2^-j<=u<=m-2^-k,

    H(u)>=d 2^-P.                                         (3)

The coefficient has no positive loss or covariance floor. In particular,
when d>0 all hinges in [2^-j,m) are strictly favorable.

**Corollary C (the joint boundary of a compact slab is excluded).** Fix
R,j. Any adverse hinge with |X-E X|<=R sqrt(s) and u>=2^-j must have
d>2^-N. Let

    Z=31+47R^2+2(2R+c)^2+5N,      L_cov=2Z+4.             (4)

By the previously accepted covariance-boundary theorem, that same adverse
input must also have

    Cov(X)/s > 2^-L_cov I,    Cov(Y)/s > 2^-L_cov I.        (5)

Thus both loss and marginal covariances are bounded away from zero by
known constants on every fixed bounded-radius, positive-threshold adverse
frontier. No sign on its remaining interior is inferred. The original
law's low-threshold endpoint remains an independent obligation.

The new argument is transverse spherical cancellation in the standard R6
lift, followed by a local Abel inversion. It constructs no R5 motion and
does not infer hinge signs from entropy order or positivity of an Abel
transform alone. The old covariance-dependent small-loss arguments and the
new all-radius localization theorem retain their separate hypotheses.

## 2. The credited singular-safe alignment, with its proof recalled

Scale to s=1 and center the endpoints independently. Rotate Y by optimal
orthogonal Procrustes alignment. Put h=Y-X, M=E|h|^2, and

    Delta=|X-X'|^2-|Y-Y'|^2>=0,       D=E Delta=d.

The covariance-free rigidity source supplies the estimate

    M<=sqrt(6) R sqrt(D).                                  (6)

Only its matrix-geometric part is used, not its entropy theorem. Here is
a self-contained justification. Regard centered coordinate functions as
rank-at-most-three operators A,B:R3->L2(mu), and put Q=AA*, S=BB*.
The Procrustes identity and the classical square-root trace inequality give

    M<=||sqrt(Q)-sqrt(S)||_HS^2<=||Q-S||_1
       <=sqrt(6)||Q-S||_HS.                                (7)

For clarity, the first inequality follows from
M=tr Q+tr S-2||A*B||_1 and
||A*B||_1=||sqrt(Q)sqrt(S)||_1>=tr(sqrt(Q)sqrt(S)).
To prove the second, write U=sqrt(Q)+sqrt(S), V=sqrt(Q)-sqrt(S), so
Q-S=(UV+VU)/2. Testing its trace norm against sign(V) gives
||Q-S||_1>=tr(|V|U)>=tr V^2: in a V-eigenbasis, U+V and U-V are
positive semidefinite, hence U_ii>=|V_ii|. Work in the finite-dimensional
range of A and B, so this argument is valid at every rank.

Double centering of squared distances gives
Q-S=-(1/2)J Delta J, with J projecting off constants in L2(mu). Therefore

    ||Q-S||_HS^2<=E Delta^2/4<=R^2 D,

because 0<=Delta<=4R^2. This proves (6). Centering and shortness also give

    |Y|<=E|X-X'|<=2R,       |h|<=3R.                       (8)

These are bounds for the actual law. No auxiliary full-rank probability,
small essential displacement, or unproved linear estimate M=O(D) is used.
The rare-fold example in the earlier rigidity source already shows why a
universal linear estimate M=O(D) would be false.

## 3. Three almost Gaussian directions in the known six-dimensional lift

The standard lift (sqrt(1-t)X,sqrt(t)Y), 0<=t<=1, has pair distances
squared equal to (1-t)|X-X'|^2+t|Y-Y'|^2. At each time apply the block
orthogonal rotation which expresses it instead as

    Z_t=(P_t,W_t)=(X+t h, sqrt(t(1-t))h) in R3 x R3.        (9)

This rotation changes neither a Gaussian integral nor a coarea profile.
It is used pointwise in t, not differentiated. In these coordinates,

    |Z_t|<=2R, |W_t|<=3R/2, E|W_t|^2<=M/4.               (10)

Let q_t(z)=E exp(-|z-Z_t|^2/2), V_t=-log q_t, and

    h_t(z)=E[Delta K_X(z)K_X'(z)]/q_t(z)^2,
    K_X(z)=exp(-|z-Z_t(X)|^2/2).                           (11)

This h_t is a nonnegative loss-weighted posterior expectation; it is not
the label displacement h. Its numerator is linear in the nonnegative
pair-loss measure. We keep that positivity throughout the proof.

Put a=2^-j and ell_max=log(1/a)=j log 2. Fix t and a physical coordinate
x in the first R3 for which the normal fibre q_t(x,.) has maximum at
least a. Take any normal mode w_*. It is a normal posterior mean, so
|w_*|<=3R/2. Its posterior pi_* on source labels satisfies

    E_(pi_*)|W_t-w_*|^2
      <=E_(pi_*)|W_t|^2<=M/(4a).                          (12)

The last inequality uses K_X<=1 and q_t(x,w_*)>=a. Center its normal
labels U=W_t-w_* and set F_x(z)=E_(pi_*) exp(z.U). Then

    E_(pi_*) U=0, |U|<=3R, F_x(z)>=1,
    q_t(x,w_*+z)=q_t(x,w_*) exp(-|z|^2/2)F_x(z).           (13)

For |z|<=B, its tilted covariance is at most

    eta I,    eta=(M/(4a))exp(3RB),                        (14)

since the second moment numerator is at most exp(3RB)E|U|^2 and
the denominator F_x is at least one. Hence the normal potential has
Hessian between (1-eta)I and I in this ball.

Every point of this fibre with q_t>=a lies in that ball about w_*:
the Gaussian envelope gives |w|<=3R/2+sqrt(2ell_max), whereas
|w_*|<=3R/2 and B>=3R+sqrt(2ell_max). In particular, if eta<1,
there is a unique relevant mode and every level below ell_max is a
strictly convex normal sublevel set. Each ray from w_* crosses its
boundary once. This uses normal convexity only, not convexity of the
full six-dimensional potential.

Equations (1),(6) and e<4, sqrt(6)<3 imply

    eta <= (3R/4)2^(j+6RB)sqrt(D) <= 1/(4K).              (15)

In particular eta<1/2. This is the sole small-loss guard. It is uniform
over x,t and contains no covariance inverse.

## 4. Spherical cancellation of the potentially negative radial term

Fix such a fibre. Write v_*= -log q_t(x,w_*). For 0<v<=ell_max-v_*,
let r=r(v,theta) solve

    V_t(x,w_*+r theta)=v_*+v,       theta in S2,
    r0=sqrt(2v), p=V_r=r alpha, beta=V_rr.

Along each ray put l=(log F_x)_r. From (13)--(15),

    0<=l<=eta r, 1-eta<=alpha,beta<=1,
    r0<=r<=r0/sqrt(1-eta)<=(1+eta)r0,       r<=B.           (16)

The last elementary inequality holds for 0<=eta<=1/2. Decomposing (11)
using the fixed posterior pi_* shows that h_t on the fibre is the positive
pair integral of functions

    h_pair(z)=c_pair exp(z.S_pair)/F_x(z)^2,
    c_pair>=0, |S_pair|<=6R=S.                            (17)

Here c_pair includes Delta and the two posterior weights; in the diffuse
case it denotes a positive measure density. No cancellation between
different loss pairs will be needed.

For one term, the normal coarea integrand is J=h_pair r^2/p. If
c_theta=theta.S_pair, direct differentiation gives

    J_v = h_pair [r c_theta-2r l+2-beta/alpha]
                                      /(r alpha^2).       (18)

The term r c_theta need not be pointwise positive. Compare (18) with its
spherical reference

    J0_v=c_pair exp(r0 c_theta)(1+r0 c_theta)/r0.          (19)

At the level surface, 2log F_x=r^2-r0^2. Consequently the exponential
ratio of h_pair to c_pair exp(r0 c_theta) has logarithm e_0 satisfying

    |e_0|<=eta(BS+2B^2)=eta E.                            (20)

The remaining prefactor p_0=r0/(r alpha^2) obeys

    |p_0-1|<=6eta,       0<p_0<=4.                       (21)

Finally the numerator in (18) differs from 1+r0 c_theta by at most

    eta(BS+4B^2+2)=eta F.                                (22)

For (20) use |r-r0|<=eta r0 and
0<=log F_x=(r^2-r0^2)/2<=eta r0^2. For (21) use
sqrt(1-eta)<=p_0<=(1-eta)^-2 and (1-eta)^-2-1<=6eta.
For (22) use 2r l<=2eta r^2<=4eta r0^2 and
|1-beta/alpha|<=2eta. These bounds remain valid as v decreases to zero.

Since eta E<=1, |exp(e_0)-1|<=3eta E and exp(e_0)<=3. Combining
(20)--(22) proves the exact error bound

    |J_v-J0_v|<=c_pair exp(r0 c_theta) eta K/r0.           (23)

Indeed |exp(e_0)p_0-1|<=3eta(E+6), and
|exp(e_0)p_0|<=12, which give precisely K in (1).

The reference derivative has a favorable spherical average:

    integral_S2 exp(r0 c_theta) r0 c_theta dtheta >=0.     (24)

Pair theta with -theta; its summand is proportional to z sinh z>=0.
Equations (19),(23),(24), eta K<=1/4 and Jensen on the sphere therefore give

    integral_S2 J_v dtheta
       >=(1-eta K)c_pair/r0 integral_S2 exp(r0 c_theta)
       >=2pi c_pair/r0.                                 (25)

The weakened last constant uses |S2|=4pi. This is the new functional
step: the possibly negative linear term is integrated on a sphere before
the perturbation error is estimated. Bounding that term pointwise would
lose the sign when a rare loss pair is far from the normal posterior mean.

## 5. The local Abel inversion, including critical levels

Let nu_t be the pushforward of h_t(z)dz by V_t(z). This positive measure
is locally finite, and integral exp(-2w)dnu_t(w)<infinity. Define its
normal-fibre coarea density on 0<=w<=ell_max by

    A_(t,x)(w)=integral_S2 h_t(x,w_*+r theta)r^2/V_r dtheta

when w>v_*(x), and zero otherwise. Fibres whose maximum is below a
contribute zero on this interval. Normal radial integration and Fubini
show that A_t(w)=integral_R3 A_(t,x)(w)dx is a density of nu_t there.

By (25), each fibre density is nondecreasing. It is zero continuously
at its modal level: its size is O(sqrt(w-v_*)), and its derivative is
O((w-v_*)^-1/2). These follow from (16)--(18); constants are uniform here.
For explicit domination, sum c_pair<=D/a^2, r<=B, F_x>=1 and |S_pair|<=S
give A_(t,x)<=8pi B(D/a^2)exp(BS). Relevant x lie in
B(0,2R+sqrt(2ell_max)). Thus these bounds are integrable uniformly in t.
Each fibre is absolutely continuous. Tonelli applied to its nonnegative
derivative shows that

    A(w)=integral_0^1 A_t(w)dt

is absolutely continuous and nondecreasing on [0,ell_max], with A(0)=0.
There is no unproved full-dimensional regular-value assumption here.

We recall the exact replica/Abel normalization, then explain why a local
coarea assertion suffices. Gaussian product integration, differentiated
only through the affine squared pair distances, gives for each integer k>=2

    integral_0^1 u^(k-2)H(u)du
       =sqrt(k)/(32pi^3) integral_0^1 integral exp(-kw)dnu_t(w)dt.
                                                               (26)

For an explicit constant check, let S_k(t) be the sum of the squared
distances of all unordered pairs of k independent lifted labels. Gaussian
product integration in n dimensions is

    integral q_t(z)^k dz=(2pi)^(n/2) k^(-n/2)
                                      E exp[-S_k(t)/(2k)].

The elementary hinge integral divides a k-th power difference by
k(k-1)C_s^(k-1). Differentiating S_k(t), then using exchangeability,
therefore gives the left side of (26) as
(1/(4k^(5/2))) integral_0^1 E[Delta_12 exp(-S_k(t)/(2k))]dt.
The weighted six-dimensional integral on its right, before its prefactor,
is (2pi)^3 k^-3 times that same expectation. This proves the constant
sqrt(k)/(32pi^3). Bounded pair losses and Gaussian domination justify
each operation for bounded diffuse laws. This is the earlier R6 moment
identity, not a new replica inequality.
Put Phi(ell)=exp(ell)H(exp(-ell)), and let

    (I_(1/2)F)(ell)=1/sqrt(pi) integral_0^ell F(w)/sqrt(ell-w)dw.

The Laplace transform of I_(1/2) at k is multiplication by k^-1/2.
Thus (26) says that the measure 32pi^3 I_(1/2)Phi(w)dw has the same
Laplace transforms at every integer k>=2 as the average of nu_t.
Both have finite total variation after multiplication by exp(-2w).
Substituting z=exp(-w), uniqueness of moments of finite measures on [0,1]
proves equality. In particular, locally,

    I_(1/2)Phi=A/(32pi^3).                                (27)

Apply I_(1/2) once more and differentiate in distributions. The semigroup
identity I_(1/2)I_(1/2)=I_1, A(0)=0, and local absolute continuity yield

    Phi(ell)=1/(32pi^3 sqrt(pi))
        integral_0^ell A'(w)/sqrt(ell-w)dw                (28)

for almost every 0<ell<ell_max. Its right side is nonnegative. Since H
is continuous, H>=0 throughout [a,1]. Above one both hinges vanish.
This proves Theorem A, including all critical levels and diffuse laws.
Neither positivity of nu_t alone nor the old half-order comparison would
justify this inversion sign; (25) is indispensable.

## 6. A strict loss-linear margin below the target peak

Assume a<=u<=m-epsilon, with 0<epsilon<=1, and put ell=-log u.
The two-sided peak estimate of the preceding motion-chain proof, valid
for every bounded contraction, gives

    m-max(q_t)<=exp(R^2)(1-t)D/4.                         (29)

Indeed every intermediate lift has circumradius at most R, because it is
a short image of the initial support; extend to its enclosing-ball center,
or use the smallest-ball variance proof in that source. Its remaining
loss is (1-t)D. The endpoint normalized six-dimensional peak is m.

On times with (1-t)D<=2epsilon exp(-R^2), the peak of q_t is at least
u+epsilon/2. Choose a global mode (x_*,w_*). Its norm is at most 2R.
For |x-x_*|<=epsilon/8, the global Gaussian gradient bound |grad q_t|<=1
shows that the normal-fibre peak is at least u+3epsilon/8. Hence

    ell-v_*(x)=log(q_*(x)/u)>=3epsilon/8,

using q_*(x)<=1. For all w in [ell-epsilon/16,ell], the excess fibre
level is positive and its r0 is at most sqrt(2j). The interval is positive
because ell>=epsilon, which follows from u<=1-epsilon.

The normal mode in each such fibre has norm at most 3R/2. Since
|x|<=2R+1 and |Z_t|<=2R, all its distances to lifted centers are at most
6R+1. Therefore the pair coefficients at that fibre mode sum to at least

    D exp[-(6R+1)^2].                                    (30)

The posterior denominator is at most one, so it can only improve this
lower bound. Integrate (25) on the physical ball of radius epsilon/8:

    A_t'(w)>=pi^2 epsilon^3 D exp[-(6R+1)^2]/(192 sqrt(2j)). (31)

All other fibre contributions are nonnegative. The eligible times have
total loss min(D,2epsilon exp(-R^2)), at least
epsilon exp(-R^2)D/(2R^2), since D<=4R^2. In (28), the integral over
[ell-epsilon/16,ell] of (ell-w)^-1/2 equals sqrt(epsilon)/2. Combining
these constants gives

    H(u)>= u epsilon^(9/2) D exp[-(6R+1)^2-R^2]
               /[3*2^13 R^2 pi sqrt(2pi j)].             (32)

The argument first gives this at almost every threshold; continuity of
H supplies every threshold and the closed band edges. With epsilon=2^-k,
use epsilon^(9/2)>=epsilon^5, e<4, pi<4, sqrt(2pi)<4,
sqrt(j)<=2^j and R^2<=2^(2R). This proves (2)--(3).

Theorem A can be proved without (29); the strict margin imports that
previous upper peak budget, whose short posterior proof is recorded in
the pinned source. No source covariance hypothesis is reintroduced.

## 7. The compact frontier consequence and its exact limits

The contrapositive of Theorem A gives d>2^-N for every adverse hinge in
the stated slab. Apply the independently accepted arbitrary-radius
covariance-boundary theorem at its threshold index m=j and loss-floor
index k=N. Its formulas are exactly (4)--(5). This proves Corollary C.

The preceding small-loss sign and covariance-boundary sign each left the
simultaneous zero-loss, zero-covariance corner open. Theorem A closes that
corner for a fixed radius and positive threshold cutoff. R3's independently
accepted all-radius loss-relative localization can be used on the remaining
adverse frontier with the explicit actual covariance floor (5). This does
not declare any uncomputed finite sign positive, or replace an endpoint
sign by an absolute approximation error.

As j increases the permitted loss decreases. A given nonisometric input
is not therefore signed at every positive threshold by this theorem.
No unrestricted zero-defect theorem, negative hinge, new R5 motion or
Kneser--Poulsen consequence is claimed. R2's anchored perturbation producer
and R3's localization are not duplicated; this supplies the missing
uniform small-loss boundary input while preserving their trust boundaries.

## 8. Exact finite controls

The accompanying rational consumer checks the actual centered source
radius, all active pair contractions, the ordered loss, and (1). It gives
UNRESOLVED outside the sufficient guard, never a negative hinge. The
integer schedule is independent of covariance and atom-mass floors.

The familiar 16-label simplex-flap control, scaled by one half, uses one
anchor of mass 1-epsilon and equal remaining masses epsilon/15. It has
paired affine rank six and exactly d=(8/5)epsilon at variance one. The
source and target covariance eigenvalues tend to zero with epsilon.
The whole family 0<epsilon<=2^-487 satisfies R=3,j=3,N=482. It receives
the margin d 2^-781 at every 1/8<=u<=m-1/4. This old geometric example
is a boundary control, not a new positive class or a new motion exclusion.

The finite checks audit the radial derivative algebra, perturbation budgets,
replica normalization, the degenerating family and malformed inputs. They
do not replace the spherical cancellation, measure identities, or Abel
inversion by samples. All universal claims above remain written analysis.
See SOURCES.md for exact attribution and review status.
