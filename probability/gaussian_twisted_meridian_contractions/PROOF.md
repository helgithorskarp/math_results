# Twisted meridian contractions in three dimensions

Complete author proof, 27 September 2026. Independent correctness review and
historical priority are pending. The unrestricted Gaussian-majorisation
problem remains open.

## 1. A uniform class with changes of azimuth

Write points of R3 as (r exp(i theta),z). Let E be a nonempty Borel subset of
the meridian half-plane, and let

    S:E -> [0,infinity) x R,    S(r,z)=(rho(r,z),zeta(r,z)),
    |S(p)-S(q)| <= |p-q|,       0 <= rho(p) <= r.                 (1)

Let psi:E->R be Lipschitz. It is a real phase, not an angle defined only
modulo 2pi. Define the full rotational domain and map

    D={ (r exp(i theta),z): (r,z) in E, theta in R },
    T(r exp(i theta),z)=(rho(p) exp(i(theta+psi(p))),zeta(p)).    (2)

At r=0 the value is independent of theta. The law or chosen center list
need not have rotational symmetry.

**Uniform twisted-meridian theorem.** Suppose, in addition, that there are
R>0, 0<q<1, 0<=g<1, and L>=0 such that

    E subset [0,R] x R,     rho(p)<=q r,
    Lip(S)<=g,             Lip(psi)<=L,
    (RL)^2 <= 8(1-g^2)(1-sqrt(q))/(q(1+sqrt(q))).              (3)

Then (2) has one simultaneous contracting motion in R5 with analytic
trajectories and endpoints in R3 x {0,0}. In particular, T is 1-Lipschitz.
For every bounded Borel probability measure mu concentrated on D, every
variance s>0, and every h>=0,

    integral (mu*gamma_(3,s)-h)_+
      <= integral ((T#mu)*gamma_(3,s)-h)_+.                    (4)

Thus Gaussian majorisation and all defined convex internal-energy
comparisons hold. For every finite list x_i in D and arbitrary individual
ball radii b_i>=0,

    vol_3 union_i B(Tx_i,b_i) <= vol_3 union_i B(x_i,b_i),
    vol_3 intersection_i B(Tx_i,b_i)
      >= vol_3 intersection_i B(x_i,b_i).                     (5)

Neither an axial bound nor a bound on the total phase range is required.
The meridian outputs may mix r and z and may fold. The bound is on the
spatial variation of a chosen real phase. It is not claimed optimal.

Section 3 also gives an exact pairwise certificate for a simpler phase
schedule. It includes the entire untwisted meridian theorem when psi is
constant, without the strict constants or radius bound in (3).

## 2. The geometric identity and phase budget

For p=(r,z), p'=(r',z'), abbreviate

    a=r-rho(p),             a'=r'-rho(p'),
    A_t(p)=r-t a,           B_t(p)=(1-t)z+t zeta(p),
    M=|p-p'|^2-|S(p)-S(p')|^2 >=0,
    P_t=A_t(p) A_t(p'),     K_t=a A_t(p')+a' A_t(p) >=0,
    d=psi(p)-psi(p').

Let lambda be a real analytic function on a neighborhood of [0,1], with
lambda(0)=0 and lambda(1)=1. Consider

    F_t(r exp(i theta),z)=(
      A_t(p) exp(i(theta+lambda(t)psi(p))), B_t(p),
      sqrt(t(1-t))(r-rho(p)), sqrt(t(1-t))(z-zeta(p)) ).        (6)

This uses exactly two auxiliary coordinates. For
delta=theta-theta'+lambda(t)d, expansion of the coordinates gives

    |F_t(x)-F_t(x')|^2
      =(1-t)|p-p'|^2+t|S(p)-S(p')|^2+2P_t(1-cos delta).       (7)

The two auxiliary squares cancel both meridian interpolation defects.
Differentiating the squared distance gives

    -M-2K_t(1-cos delta)+2P_t lambda'(t)d sin delta.           (8)

The maximum of (8) over all azimuth differences is

    -M+2 sqrt(K_t^2+P_t^2 lambda'(t)^2 d^2)-2K_t.             (9)

Consequently the explicit motion (6) contracts all pairs if and only if

    M(M+4K_t) >= 4P_t^2 lambda'(t)^2 d^2                     (10)

for every meridian pair and every t. Here necessity concerns this motion
on the full rotational domain, not arbitrary possible lifts. Squaring
(9) is legitimate because M+2K_t>=0. When either source radius is zero,
P_t=K_t=0 and the requirement reduces to M>=0.

This is the new interaction with the meridian lift: some decrease of
meridian distance pays for changing azimuth. It is essential to control
every azimuth difference, rather than a sampled choice of center angles.

## 3. A certificate requiring only endpoint meridian data

For lambda(t)=t, put

    K_0=(r-rho(p))r'+(r'-rho(p'))r.

The motion contracts if and only if every meridian pair satisfies

    M(M+4K_0) >= 4r^2 r'^2 (psi(p)-psi(p'))^2.               (11)

Necessity follows at t=0. For sufficiency, when P_t>0 write

    H_t=K_t/P_t=a/A_t(p)+a'/A_t(p').

The quantity P_t decreases, H_t increases, and
sqrt(H^2+d^2)-H is nonnegative and nonincreasing in H>=0.
Thus 2P_t(sqrt(H_t^2+d^2)-H_t), the nonnegative term in (9),
is nonincreasing in t. Its value at zero is at most M by (11).
Zeros of P_t follow by continuity. This proves sufficiency, including
collisions, equal meridian points and vanishing target radii.

Constant psi recovers all of (1), up to a final rigid rotation. The
criterion allows general phase variation but can be substantially improved
by delaying rotation, as follows.

## 4. Delaying the phase proves the uniform theorem

Assume (3), and set

    c(t)=1-(1-q)t,
    lambda(t)=(c(t)^(-1/2)-1)/(q^(-1/2)-1).                  (12)

This is increasing and real analytic through both endpoints; q>0.
For positive source radii and t<1,

    P_t <= c(t)^2 r r',
    K_t/P_t >= 2(1-q)/c(t),
    P_t^2/K_t <= c(t)^3 r r'/(2(1-q)).                       (13)

Indeed, a/r>=1-q and a/A_t=(a/r)/(1-t a/r), an increasing
function of a/r. These estimates also allow unequal transverse factors
rho(p)/r; no scalar homothety of the meridian map is assumed.

Using sqrt(K^2+v^2)<=K+v^2/(2K), the positive term in (9) is
at most

    (P_t^2/K_t) lambda'(t)^2 d^2
      <= (RL)^2 (1-q)/(8(q^(-1/2)-1)^2) |p-p'|^2
      <= (1-g^2)|p-p'|^2 <= M.                              (14)

The middle constant follows from

    c(t)^3 lambda'(t)^2=(1-q)^2/(4(q^(-1/2)-1)^2).

The second inequality in (14) is precisely (3), since
(q^(-1/2)-1)^2/(1-q)=(1-sqrt(q))/(q(1+sqrt(q))).
This proves (10) and the uniform theorem's contracting motion. Cases with
zero radius or P_t=0 follow directly from (8) or by continuity. No positive
lower bound on rho is needed.

The mechanism is useful at small q: for fixed g<1 the permitted RL grows
like q^(-1/2). It permits much greater total twisting than the clock
lambda=t under the same uniform bounds. This is a proven sufficient
estimate, not an optimality assertion about phase schedules or maps.

## 5. Regularity, diffuse measures and arbitrary ball radii

Put t=sin(v)^2 for 0<=v<=pi/2. In (6), sqrt(t(1-t)) becomes
sin(v)cos(v); all labeled trajectories are analytic. The motion is jointly
continuous, including on the axis, since A_t<=r and S,psi are Lipschitz.
Positions and trajectory derivatives are bounded on every bounded part of
D. Distinct points do not collide before t=1: in (7), a nonzero meridian
difference contributes (1-t)|p-p'|^2; at the same meridian point the phase
difference d vanishes and A_t>=(1-t)r.

If a bounded law's support closure meets points outside the initially
chosen Borel domain, extend the Lipschitz maps S and psi continuously to
the meridian closure. All the stated inequalities pass to that closure,
as does (6). One may therefore work on the compact support closure.

Apply Aishwarya--Li, arXiv:2609.07041v2, Theorem 1.4(i)(a), in R5. At
the endpoints the densities are f(x)gamma_(2,s)(y) and g(x)gamma_(2,s)(y),
where f,g are the densities in (4). If X has density f and Z independently
has density gamma_(2,s), then gamma_(2,s)(Z)/(2pi s)^(-1) is uniform on
[0,1]. Hence

    Pr{f(X)gamma_(2,s)(Z)>h(2pi s)^(-1)}=integral(f-h)_+.

The sampled-density comparison yields (4). This two-coordinate transfer
is explicitly identified after Theorem 1.5 of that paper; it is a credited
input. No symmetry or finite-atomic approximation of mu is needed.

Reverse the analytic motion and apply Bezdek--Connelly, Theorem 1, to
obtain (5). Their transfer from an R^(n+2) motion to n-dimensional ball
volumes is another credited input.

For completeness, endpoint collisions can be removed within the new
construction. Given 0<epsilon<1, set h_0=1-epsilon,
S_epsilon=epsilon I+h_0 S, and use the phase lambda(h_0 t)psi in
place of lambda(t)psi. This phase ends at lambda(h_0)psi. For each pair,

    M_epsilon=h_0 M+epsilon h_0 |(p-p')-(S(p)-S(p'))|^2,
    P_epsilon,t=P_(h_0 t),   K_epsilon,t=h_0 K_(h_0 t).

The new phase derivative is h_0 lambda'(h_0 t)d, so (10) persists.
Moreover rho_epsilon>=epsilon r. For a finite list of distinct meridian
points, S_epsilon can identify a pair for at most one epsilon, since the
difference is affine and nonzero at epsilon=1. Avoid these finitely many
values. Distinct azimuths at the same meridian point remain distinct.
The regularized endpoints converge to T; continuity of finite ball volumes
then gives (5). Repeated source centers are merged using the largest
radius for unions and the smallest for intersections; zero radii follow
by continuity. The radii b_i are completely independent of the cylindrical
radii r_i of the centers.

## 6. A coupled, folding and winding example

On the entire cylinder 0<=r<=1, z in R, take

    rho=r/16,    zeta=r/2+|z|/4,    psi=7z.                   (15)

Away from z=0 the squared Frobenius norm of the meridian derivative is
1/256+1/4+1/16=81/256, so Lip(S)<=9/16, also across the fold by
integration on meridian segments. With q=1/16 and g=9/16, the right
side of (3) is 105/2, larger than L^2=49. Thus the entire cylinder
map

    T(x,y,z)=( (1/16) R_(7z)(x,y), sqrt(x^2+y^2)/2+|z|/4 )   (16)

has the full conclusions. Any Lipschitz phase with constant at most
sqrt(105/2) can replace 7z. There can be arbitrarily many turns as the
axial extent increases, and arbitrary nonsymmetric finite or diffuse laws
may be supported anywhere in a bounded portion. The example combines
loss of azimuthal radius, radial-to-axial motion and an axial fold; it is
not a rigid screw matching.

The following comparisons already hold on the bounded cylinder |z|<=1.
They demonstrate limitations of direct older certificates, not exclusion
from their finite compositions.

**No single all-frame scalar-defect certificate.** The earlier scalar
criterion would require fixed unit e,f with

    |x-x'|^2-|Tx-Tx'|^2 >= |e.(x-x')-f.(Tx-Tx')|^2.         (17)

At a differentiability point with Jacobian D, apply (17) to x'=x+h e and
let h tend to zero. Necessarily

    2 f.D e >= |D e|^2+(f.D e)^2.                            (18)

Take r=1/2, u in {(1,0),(0,1),(-1,0),(0,-1)}, and
z in {pi/7,2pi/7,-pi/7,-2pi/7}. All 16 points are interior. Let
sigma=cos(7z) in {-1,1} and eta=sign(z). Their rational Jacobians are

    D(u,sigma,eta)=
      [ sigma/16       0           -7 sigma u_2/32 ]
      [    0       sigma/16         7 sigma u_1/32 ]
      [   u_1/2       u_2/2               eta/4    ].         (19)

Their mean is zero and their mean D^T D is

    diag(33/256,33/256,113/1024),                             (20)

which is positive definite. Averaging (18) is impossible for unit e.
This covers arbitrary independent orthogonal endpoint frames; translations
cancel from pair differences. It is a continuum obstruction, not a claim
that these 16 center pairs alone fail (17).

**No single strong coordinate contraction in independent frames.** Such
frames would make every Jacobian have the form Q diag(d_1,d_2,d_3) P^T,
because an output coordinate cannot vary in the other two input directions.
All D^T D would therefore commute. The Gram matrices from (19) at
u=(1,0),(0,1), sigma=eta=1 have commutator entry (1,2) equal to
4145/262144, nonzero. This excludes one strong coordinate representation
of the full map.

The fixed set of (16) is {0}, and the map does not preserve rays from zero.
It is therefore not a direct convex-normal map fixing its core in the
displayed coordinates. No exclusion after all possible normal-map endpoint
frames, and no exclusion of finite compositions of older classes, is claimed.

## 7. Scope and proof status

The substantive class advance over graph6468 is nonconstant azimuth,
controlled by meridian distance loss and a delayed phase schedule. The
Gaussian and all-individual-radius Kneser--Poulsen consequences are class
theorems, not fixed-configuration asymptotics or finite numerical evidence.
Classical transfer theorems are not newly claimed.

These sufficient conditions do not cover every rotationally equivariant
contraction. In particular, R4's two-rigid-body screw obstruction rules
out a universal R5 lifting statement even on a rotational extension.
Its failure to lift is not a negative Gaussian or Kneser--Poulsen result.
R4's extremal-map/deformation and R7's adversarial ownership are unchanged.

The exact checker verifies (7)-(8) symbolically, rational phase-budget
controls including variable transverse factors and axes, the constants in
(3), and (19)-(20) and the noncommuting Gram matrices. It also rejects
wrong clocks, overlarge phase, and missing terms. The continuum inequalities,
the cited transfers and the hypotheses on maps are mathematical proof
obligations discharged above; finite controls are not their substitute.
Independent review, formalization, historical priority and unrestricted
dimension-three majorisation remain open.
