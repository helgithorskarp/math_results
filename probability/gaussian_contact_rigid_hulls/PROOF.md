# All-threshold Gaussian comparison near a rigid convex configuration

26 September 2026. Complete author proof; independent mathematical review
is pending. The result removes the volume cutoff from the accepted local
contact theorem for fixed finite source configurations with an
infinitesimally rigid hull and no nonvertex sites on its boundary. In
particular it applies to every finite source in general position. It has
no atom-count cap. The neighborhood depends on the source, its positive
weights and the
Gaussian variance. The unrestricted dimension-three question remains open.

The main analytic input is a deformation-relative tail estimate, proved
below for arbitrary separated finite configurations. Unlike an absolute
tail asymptotic, its error vanishes with the displacement. A quantitative
mean-width margin then gives an actual sign at every small threshold.
The method of differentiating the radial boundary and the exterior mass
is credited to R4's [relative-tail proof](../gaussian_flap_depth_boundary/RELATIVE_TAIL.md).
We prove the estimate needed here directly, without assuming R4's flap
theorems. Other dependencies and scope are in [SOURCES.md](SOURCES.md).

## 1. Statement and explicit neighborhood

Let x_1,...,x_N be distinct sites spanning R3, let P be their convex hull,
and let p_i>0 with sum p_i=1. Each source site is assumed to be either a
vertex of P or strictly inside P; there are no other boundary sites.
Center the source so sum p_i x_i=0. Let I be the set of m hull vertices
and E the set of actual hull edges. Assume the hull rigidity matrix

    (h_i)_(i in I) -> ((x_i-x_j).(h_i-h_j))_(ij in E)          (1)

has rank 3m-6. This is a finite linear-algebra condition. In particular it
holds for every convex three-dimensional polytope with triangular faces,
by the classical infinitesimal rigidity theorem. The seven-point example
in Section 7 is checked directly, without that theorem.

**General-position corollary.** The hypotheses hold for every finite source
with N>=4 and no four coplanar sites: its hull has triangular faces, and
every remaining site is strictly inside it. Hence the theorem below covers
all such sources, for arbitrary positive weights and any fixed variance.
This is an open geometric class for every finite N, not a list of small
configurations.

Let y_i be any contracted image: |y_i-y_j|<=|x_i-x_j| for every pair.
Center and orthogonally Procrustes-align y to x with the SAME weights, so

    sum p_i y_i=0,     sum p_i x_i y_i^T is symmetric PSD.
    h_i=y_i-x_i,       delta=max_i |h_i|.                     (2)

At variance t>0 write

    f_t(z)=sum p_i gamma_t(z-x_i),
    g_t(z)=sum p_i gamma_t(z-y_i),
    gamma_t(z)=(2 pi t)^(-3/2) exp(-|z|^2/(2t)),
    H_u(a)=integral (u-a)_+,   L_u(v)=sup_(|A|=v) integral_A u.

**Theorem.** For each such fixed source, weights and t>0 there is an
explicit delta_*>0 such that every contracted image satisfying
delta<=delta_* obeys

    H_g_t(a)>=H_f_t(a) for every a>0,
    L_g_t(v)>=L_f_t(v) for every 0<v<infinity.                (3)

If the map is not an isometry on these labels, the hinge inequality is
strict for 0<a<max g_t, and the profile inequality is strict at every
finite positive volume. Isometries give equality. Thus every profile
contact in this neighborhood is isometric, and its two bulk heat fluxes
are equal. There is no regular-level assumption.

Here are constants at t=1. Choose

    R_x>=max_i |x_i|>0,   0<nu_0<=min_(i<j)|x_i-x_j|,
    Cov_p(x)>=kappa I_3, kappa>0,   p_*=min_i p_i.

For each hull edge e=ij let l_e=|x_i-x_j| and let alpha_e>0 be the
length of its normal-fan arc on S2 (the exterior dihedral angle). Choose

    0<beta<=min_e alpha_e/(2l_e).                            (4)

Let C_E be any finite constant such that

    max_i |h_i| <= C_E sum_(ij in E) |(x_i-x_j).(h_i-h_j)|    (5)

whenever sum p_i h_i=0, sum p_i x_i cross h_i=0, and
(x_i-x_j).(h_i-h_j)<=0 for ALL pairs. Section 2 supplies C_E explicitly
from the hull matrix, the depths of the interior sites, and kappa.
No optimization over actual Gaussian mixtures is needed. Define

    c=beta/(2 C_E),   M=R_x+1,   nu=nu_0/2,
    B=20 N(N-1)/nu,
    A=280M+248+B(log(1/p_*)+M^2),
    R_0=max{2,4M,4 pi A/c,(4 pi B/c)^2},
    q_0=exp(-[(R_0+2R_x)^2/2+(R_0+4R_x)^2]),

    delta_* = min{1, nu_0/4,
                  beta nu_0/(8 pi C_E N(N-1)),
                  kappa q_0/(16R_x)}.                       (6)

Larger R_0 and smaller delta_* are allowed. The constants are deliberately
conservative. For general fixed t apply (4)-(6) to x_i/sqrt(t) and
y_i/sqrt(t), and multiply the resulting displacement bound by sqrt(t).
No positive common neighborhood for all variances is asserted.

## 2. Rigidity gives a linear mean-width margin

Use the unnormalized support integral

    W(X)=integral_(S2) max_i theta.x_i d sigma(theta),
    sigma(S2)=4 pi.                                         (7)

It is invariant under translation and rotation. A maximizing label is
unique outside a finite union of great circles. Dominated differentiation
therefore gives

    DW_X[h]=sum_i h_i . integral_(C_i) theta d sigma,          (8)

where C_i is the spherical normal cell of vertex i; strictly interior
sites have no maximizing directions. The spherical identity
Delta_(S2) theta=-2 theta and the divergence theorem give

    integral_(C_i) theta d sigma
        =-(1/2) integral_(boundary C_i) n_out ds.

On the arc shared with C_j, n_out=(x_j-x_i)/l_ij. Summing the two
contributions on each arc proves the first-variation formula

    DW_X[h]=(1/2) sum_(ij in E)
                   (alpha_ij/l_ij) (x_i-x_j).(h_i-h_j).       (9)

Cell corners have zero boundary length. Nonadjacent cells have no shared
arc. Thus this calculation uses exactly the actual hull edges.

First suppose every site is a hull vertex. The rank assumption says that
the kernel of (1) consists precisely of rigid velocities h_i=a+b cross x_i.
The six gauge conditions eliminate that kernel. Indeed the mean condition
gives a=0, and the torque condition gives

    (tr(Cov_p(x)) I-Cov_p(x)) b=0.

The matrix is positive definite because the source spans R3. Hence b=0.
The linear map (1) is injective on that gauge subspace. Finite-dimensional
norm comparison proves (5), even without the pair-strain inequalities in
this vertex-only case. More constructively, append the six gauge
rows to the edge matrix, select any full-column-rank square row subsystem,
and take a left inverse with zero coefficients on unused rows. Its norm
on the edge columns supplies C_E. All this is rational linear algebra
when the coordinates and weights are rational.

Write s_ij=(x_i-x_j).(h_i-h_j). Here is the promised explicit extension
to interior sites. Let C_H be a
constant obtained by that hull-only matrix calculation, using uniform hull
weights and centering the hull at its own centroid. It bounds the maximum
residual velocity on I by the sum of absolute edge strains whenever that
residual has zero hull mean and torque. For each interior source site choose
rho_i>0 such that B(x_i,rho_i) is contained in P. Set

    K=max({1} union {2R_x/rho_i : i not in I}),
    C_E=(2+R_x^2/(2kappa)) K C_H.                            (5a)

This is a valid choice in (5). To prove it, fit a rigid velocity
a+b cross x_i to the h_i on the hull by least squares, and write
r_i=h_i-a-b cross x_i for every label. The hull residual has zero mean
and torque by the normal equations; its zero mean makes the torque
condition invariant under recentering the hull. Subtracting a rigid
velocity leaves all pair strains unchanged. Hence

    max_(i in I)|r_i| <= C_H sum_(ij in E)|s_ij| =: H.

For any interior i and any hull vertex j, the pair-strain condition gives

    (x_i-x_j).r_i <= (x_i-x_j).r_j <= 2R_x H.

If r_i!=0, the contained ball supplies a hull vertex j with
(x_i-x_j).r_i >= rho_i |r_i|: minimize the linear functional in the
direction r_i over P. Thus |r_i|<=2R_x H/rho_i. Altogether
max_i|r_i|<=K H=:L.

Return to the gauge for ALL sites with the actual p_i. It gives
a=-sum p_i r_i and

    (tr(Cov_p(x)) I-Cov_p(x)) b=-sum p_i x_i cross r_i.

The left-hand matrix is at least 2kappa I. Therefore
|a|<=L and |b|<=R_x L/(2kappa), whence
max_i|h_i|<=(2+R_x^2/(2kappa))L. This proves (5a).
Distances from interior sites to the finitely many hull facets give
explicit positive rho_i; rational lower bounds suffice for rational data.
Thus (5a), not an unquantified rigidity claim for interior points, is the
constant used in the general theorem.

The aligned h in (2) obeys both gauge conditions exactly. Endpoint
contraction gives

    s_ij <= -|h_i-h_j|^2/2 <=0.                             (10)

Consequently (4), (5) and (9) imply

    -DW_X[h]>=beta sum_(ij in E)(-s_ij)>=beta delta/C_E.       (11)

We also need a finite remainder. If the maximizing label in direction
theta changes between X and X+s h, then for some pair i,j

    |theta.(x_i-x_j)|<=2s delta.

A spherical slab |theta.d|<=b has area 4 pi min(1,b/|d|).
The union of these slabs over all unordered pairs has area at most
4 pi N(N-1)s delta/nu_0. On it the change of directional velocity has
absolute value at most 2delta; off it the velocity is unchanged.
Integrating the derivative difference in s from zero to one yields

    |W(Y)-W(X)-DW_X[h]| <= 4 pi N(N-1) delta^2/nu_0.         (12)

This argument does not assume that the normal fan stays combinatorially
fixed. Equations (6), (11) and (12) show

    W(X)-W(Y)>=c delta.                                     (13)

The hull rigidity and interior-depth hypotheses give this LINEAR margin.
Mere strict decrease of mean width for each nonisometric contraction would
not imply (13), uniformly as the contraction tends to an isometry.

## 3. A relative tail lemma for arbitrary separated finite paths

Here no contraction, convex position, rigidity, centering or gauge is
assumed. Let z_i(s)=z_i(0)+s h_i, 0<=s<=1, with fixed p_i>0, and suppose

    |z_i(s)|<=M,   |z_i(s)-z_j(s)|>=nu>0,
    delta=max_i |h_i|,  p_*=min_i p_i.

Let u_s=sum p_i gamma_1(.-z_i(s)). For R>=max(2,4M), put

    a_R=(2 pi)^(-3/2) exp(-R^2/2),
    E(R)= (pi/R) [280M+248
            +(20N(N-1)/nu)(log(1/p_*)+M^2+log R)].           (14)

**Relative tail lemma.** Uniformly along the path,

    | -partial_s H_u_s(a_R)/(a_R R^2) - partial_s W(z(s)) |
          <= delta E(R).                                   (15)

In particular the endpoints satisfy

    | [H_u_1(a_R)-H_u_0(a_R)]/(a_R R^2)
                   -[W(z(0))-W(z(1))] | <= delta E(R).      (16)

The R-dependent error is O(log R/R), with its constants displayed.
Its factor delta is essential: it permits a sign comparison with (13).
The lemma treats distinct fixed labels, including sites that are not
hull vertices. It does not give a uniform estimate as sites collide or
positive weights tend to zero.

### Radial boundary and volume derivative

The a_R-superlevel set is star shaped about zero, with unique boundary
r=r(theta,s) in [R-M,R+M]. To check the inner and outer bounds, all kernels
are at least a_R on |z|<=R-M and at most a_R on |z|>=R+M. Between these
radii the radial logarithmic derivative is -r+m, where m is the posterior
mean of theta.z_i and |m|<=M. Since R-M>M, this derivative is strictly
negative. This also proves uniqueness and a smooth radial boundary.

At that boundary define

    pi_i=p_i gamma_1(r theta-z_i)/a_R,
    m=sum pi_i theta.z_i,  A_1=sum pi_i theta.h_i,
    B_1=sum pi_i z_i.h_i.

Primes in this section denote s derivatives at fixed theta,R,a_R.
Implicit differentiation of the boundary level gives

    r'=(r A_1-B_1)/(r-m),
    |r'-A_1|<=4M delta/R,   |r'|<=2delta.                    (17)

Discard the union of spherical slabs

    |theta.(z_i-z_j)|<=eta,
    eta=[log(1/p_*)+M^2+log R]/(R-M).                        (18)

Its area is at most 2 pi N(N-1)eta/nu. Off these slabs a unique
dominant label i has projection advantage at least eta over every other
label. The ratio of their total kernel contributions to its contribution
is at most

    p_*^(-1) exp(-(R-M)eta+M^2/2) <=1/R.

Thus |A_1-theta.h_i|<=2delta/R, and
|r'-theta.h_i|<=(4M+2)delta/R off the slabs. Also
|(r/R)^2-1|<=(9/4)M/R. The volume V_s of the superlevel set satisfies

    V_s'/R^2 = integral_(S2) (r/R)^2 r' d sigma.

Off the slabs this integrand differs from theta.h_i by at most
(10M+2)delta/R. On the slabs use the coarse bound
|(r/R)^2 r'|+|theta.h_i|<=(25/8+1)delta<=5delta.
The ideal integral is exactly partial_s W(z(s)). Since
1/(R-M)<=2/R, we obtain

    |V_s'/R^2-partial_s W(z(s))|
      <= (pi delta/R) [40M+8
           +(20N(N-1)/nu)(log(1/p_*)+M^2+log R)].             (19)

### Exterior mass derivative and its cancellation

Let Q_s=integral_(outside the superlevel set) u_s. At fixed theta, write
Q_theta=integral_r^infinity u_s(ell theta) ell^2 d ell. Make the exact
substitution

    ell=sqrt(r^2+2u),    d=ell-r,
    J(u)=sum_i pi_i exp(d theta.z_i).

The boundary equality u_s(r theta)=a_R gives

    Q_theta/a_R=integral_0^infinity e^(-u) ell J(u) du.       (20)

Here r>=3R/4>=1, M/r<=1/3, d<=u/r, and

    |ell'|<=2delta,  |d'|<=2delta u/r^2,  |z_i'|<=delta.

At the moving boundary,

    pi_i'=pi_i (r theta-z_i).(h_i-r' theta),
    sum pi_i'=0,    sum |pi_i'|<=3(r+M)delta<=5R delta.

The ZERO SUM permits subtracting 1 from the exponential in the posterior
derivative term. It yields the extra factor u/r which is lost if exterior
masses are bounded separately:

    |J'(u)|<=exp(Mu/r) [5R delta M u/r
                         +2delta M u/r^2+delta u/r].        (21)

Use J<=exp(Mu/r), ell/r<=1+u, and

    integral_0^infinity e^(-2u/3) du=3/2,
    integral_0^infinity e^(-2u/3)(u+u^2) du=9.

These give an integrable derivative majorant and hence justify
differentiating (20). Explicitly,

    |Q_theta'/a_R|<=delta(45RM+18M+12)
                     <=60R delta(M+1).

After spherical integration,

    |Q_s'|/(a_R R^2)<=240 pi delta(M+1)/R.                   (22)

Finally, total mass is one, so H_u_s(a_R)=1-Q_s-a_R V_s.
Adding (19) and (22) proves (15), including the constants
40M+8+240(M+1)=280M+248. Integration in s proves (16).
All differentiations above are at a strictly regular radial boundary;
no assertion about a critical interior threshold was needed.

## 4. The tail has a uniform positive sign

Return to the contracted pair in Sections 1-2 and use its straight path.
The restrictions delta<=1 and delta<=nu_0/4 ensure |z_i(s)|<=M and
pair separation at least nu=nu_0/2. This path need not itself be a
continuous contraction: only the endpoint contraction (10) was used.

With A,B as in (6), E(R)=pi(A+B log R)/R. For R>=R_0, the elementary
bound log R<=sqrt(R) gives

    E(R)<=pi A/R+pi B/sqrt(R)<=c/2.

Equations (13) and (16) therefore give the actual endpoint estimate

    H_g_1(a_R)-H_f_1(a_R) >= (c/2) a_R R^2 delta,  R>=R_0.   (23)

For a nonisometric contracted pair delta>0, so this proves strict sign at
EVERY 0<a<=a_0, where a_0=(2 pi)^(-3/2) exp(-R_0^2/2).
No limit is exchanged with delta, and the cutoff R_0 does not depend on
the chosen contraction inside the neighborhood.

## 5. Close the remaining thresholds with the accepted local theorem

We use Theorem 1 of [Gaussian contacts near isometries](../gaussian_contact_near_isometries/PROOF.md),
whose [independent review](../gaussian_contact_near_isometries_review2/REVIEW.md)
accepts its finite-displacement and critical-level estimates. At variance
one that theorem gives, if delta<=kappa q(R_x,1,v)/(16R_x),

    L_g_1(v)-L_f_1(v) >= [v (2 pi)^(-3/2) q(R_x,1,v)/8] D,
    D=sum_(i,j) p_i p_j (|x_i-x_j|^2-|y_i-y_j|^2),
    q(R_x,1,v)=exp(-[(r_v+R_x)^2/2+(r_v+3R_x)^2]),
    r_v=(v/(4 pi/3))^(1/3).                                (24)

It is valid for all finite positive v, including critical density levels,
whenever the displayed proximity condition is satisfied. It also proves
D>0 for every nonisometric contracted pair under the alignment (2).

Take any a>=a_0 with a<max f_1. Its actual source top set
F_a={z:f_1(z)>a} has a finite positive volume v. The Gaussian support
envelope puts F_a inside the ball of radius R_0+R_x, so

    v <= (4 pi/3)(R_0+R_x)^3,
    q(R_x,1,v)>=q_0.

The last restriction in (6) makes (24) simultaneous on this entire volume
range. Testing the target hinge at its optimal set of volume v gives

    H_g_1(a) >= L_g_1(v)-av
              > L_f_1(v)-av = H_f_1(a)                      (25)

for a nonisometric pair. If a>=max f_1, the desired weak inequality is
automatic since H_f_1(a)=0. Together with (23) this proves all hinges.
It also forces max g_1>=max f_1. Thus strictness holds for every
0<a<max g_1: below max f_1 it was proved, and above it H_g_1(a)>0=H_f_1(a).

For completeness, the standard duality identities are

    H_u(a)=sup_(v>=0)(L_u(v)-av),
    L_u(v)=inf_(a>=0)(H_u(a)+av).

For a Gaussian mixture and 0<v<infinity, the latter minimum is attained
at a unique positive level a_g(v)<max g_1. Gaussian mixtures have null
positive level sets. Evaluating both dual expressions at this target
level and using strict hinge comparison proves

    L_g_1(v)=H_g_1(a_g(v))+a_g(v)v
              > H_f_1(a_g(v))+a_g(v)v >= L_f_1(v).

If delta=0 the aligned mixtures agree; undoing the alignment is a rigid
motion and preserves every hinge and profile. Scaling proves general t.
This completes the theorem.

## 6. Contact-sign consequence and remaining boundary

The [accepted contact reduction](../gaussian_majorisation_heat_profiles/CONTACT_REDUCTION.md)
requires J_f(v)>=J_g(v) at an ordered equality, where the bulk flux is

    J_u(v)=-integral_(u>a_u(v)) Laplacian u.

In the neighborhood (6), equality at even one finite positive volume
forces an isometry. The fluxes are then equal by invariance under rigid
motions. The improvement over the earlier local theorem is that there
is now NO volume ceiling and no escaping sequence of nontrivial contacts
at thresholds tending to zero, for this fixed finite rigid source.

This does not prove the general ordered-contact sign. The reduction's
auxiliary input is Gaussian-regularized and unbounded, and is not a fixed
finite rigid configuration. Neither the tail lemma nor (13) supplies the
uniformity needed to approximate that class. The constants also deteriorate
under site collision, vanishing weights, failure of hull-edge rigidity,
covariance collapse and variance degeneration. These restrictions cannot
be removed by pointwise strict mean-width monotonicity.

No continuous contracting path has been constructed or assumed. Conversely
we do not claim that this class has been separated from every known
continuous-motion class. The result is a quantitative all-threshold local
theorem and a reusable relative tail estimate. It proves neither the full
dimension-three conjecture nor a new Kneser--Poulsen volume consequence.

## 7. Exact finite controls and trust boundary

The source x_i=(i,i^2-4,i^3), i=-3,...,3, with weights 1/7 is centered.
All seven sites are vertices: the linear functional (2i,-1,0) is uniquely
maximized at label i, since 2ij-j^2= i^2-(j-i)^2. Every four distinct
unshifted moment-curve points have nonzero Vandermonde determinant, so
all hull faces are triangular. The audit independently enumerates the
supporting faces, obtains 10 facets and 15 edges, and verifies rigidity
rank 15 and augmented gauge rank 21 by rational elimination.

Its covariance is

    [[4,0,28],[0,12,0],[28,0,1588/7]],

which is positive definite. The audit constructs rational lower bounds
for kappa,beta,nu_0 and an upper bound for C_E, then an integer R_0
satisfying (6), using pi<4 and log 7<7. It also adds an eighth atom at the
centroid, verifies a positive interior ball radius against every hull facet,
and computes the rational C_E in (5a) for the resulting uniform law.
No fantastically small Gaussian
threshold or numerical gap is evaluated. A deleted-edge control and the
cube edge framework fail the rigidity test, as expected; this is not a
negative Gaussian-majorisation claim for either configuration.

[audit.py](audit.py) also checks the exact coefficient collections and
elementary integrals used in the relative tail bound. Its output is
[EXPECTED.json](EXPECTED.json). It uses only the Python standard library
and imports no teammate code or data. These finite checks do not certify
the universal analytic estimates, classical rigidity theorem, or full
Gaussian majorisation. The written proof requires independent review.
