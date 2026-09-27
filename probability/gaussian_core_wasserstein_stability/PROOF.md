# All-threshold stability from a protected source core in Wasserstein distance

Complete author argument, 27 September 2026. Independent review is pending.
The unrestricted dimension-three Gaussian-majorisation question remains open.

The increment over the [mixed-chain cloud certificate](../gaussian_chain_stability_certificate/PROOF.md)
is a uniform family with an arbitrary background measure, a mass floor on
only a fixed source core, and a Wasserstein-1 perturbation budget. The actual
source need not have bounded support. An explicit target support envelope
remains essential. The proof consumes R8's [mixed-chain margin](../gaussian_motion_chain_strictness/PROOF.md),
which incorporates R3's [polynomial margin](../gaussian_polynomial_hinge_margin/PROOF.md),
and the reviewed [peak lemma](../gaussian_norm_preserving_strictness/PROOF.md).

We do not claim new reference-map geometry, a new width certificate, or the
qualitative chain sign. The one-sided use of source cap mass and target
support is already present in R3's [support-cap localization](../gaussian_support_cap_localization/PROOF.md).
Here it gives a fixed/compact-variance all-threshold Wasserstein theorem
through an explicit source-core retention estimate and signed low-tail join.

## 1. Uniform theorem

Write gamma_s for the R3 Gaussian of covariance s I, C_s=(2 pi s)^(-3/2),
and H_f(h)=integral (f-h)_+. Normalize the variance interval to [1,S], S>=1.
Other intervals [s0,s1] follow by dividing coordinates and W1 distances by
sqrt(s0), and setting S=s1/s0.

Let mu be a compactly supported reference probability law, and let nu be
its image under a finite chain of short support maps. The initial source
fits a radius-R ball, R>=1 integer. Every step has a supplied certificate
of one of the two types of R8's Theorem B:

* N: anchors a,b with |x-a|=|Tx-b|<=R on the entire step support;
* M: an admissible contracting R5 motion, with continuous support maps,
  absolutely continuous trajectories, measurable velocities and finite
  integral of maximal speed, as defined in that source.

The same label law is used throughout. Select finitely many source labels
with points p_i and weights v_i>=m=2^-ell, ell>=0 integer. Their final images
are q_i. Repeated locations can be merged, or treated as labelled masses.
The remaining reference measure is unrestricted subject to this chain and
the radius premise. Put P_c={p_i}. Let K be a compact convex set containing
supp(nu). After independent source and target translations, P_c and K fit
radius-Re balls, Re>=1 integer. Only the reference source, not the actual
source below, must satisfy the radius-R premise.

For probability area measure sigma on S2 set W(A)=integral h_A(theta) d sigma,
where h_A(theta)=sup_(x in A) theta.x. This is translation invariant and
half the usual mean width. Suppose 0<w<=2Re and

    W(P_c)-W(K)>=w.                                         (1)

Let D=E[|X-X'|^2-|TX-TX'|^2] be the ordered endpoint loss. Assume an integer
a>=0 satisfies D/S>=2^-a uniformly over the reference family. Section 5
certifies this using only core pairs, without assigning mass to a background
vertex or imposing any bound on the number of background atoms.

Choose an integer b_rho>=0 and set rho=2^-b_rho so that

    rho <= min(1/2,w/4).                                    (2)

Use the following schedule:

    A=6(Re+1)^2+2S(ell+1),       Q0=8A/w,
    j=ceil(Q0^2),               k=a+9R^2+4,
    B_N=40R^2+9R+38,            B_M=66R^2+2R+18,
    N=max(B_N+3j+8(k+1), B_M+4j+5(k+1))+k+2R^2+2R+1,
    M=a+N,                     B=max(M+1,k,ell+b_rho+1).    (3)

**Theorem.** Let mu',nu' be arbitrary probability laws of finite first
moment, satisfying

    eta=W1(mu,mu')+W1(nu,nu') <= 2^-B,
    supp(nu') subset K+B(0,rho).                             (4)

Then simultaneously for all s in [1,S] and h>=0,

    H_(nu'*gamma_s)(h) >= H_(mu'*gamma_s)(h).                 (5)

On the entire band C_s 2^-j <= h <= ||mu'*gamma_s||_infinity the gap is at
least 2^-(M+1). The band may be empty. The actual pair need not be a
contraction, preserve the reference chain, or have a common prior.
In particular (5) covers every genuine contraction pair meeting (4).

There is no support bound on mu', no positive mass requirement on individual
background components, and no atom-count restriction on the background.
The same budget works for every reference chain, prior and background law
with these guards; it is independent of the number and smallest loss of the
links. The target-envelope hypothesis in (4) is not replaced by W1 closeness.
This is not a whole unrestricted W1 neighborhood of both endpoint laws.

## 2. Retained core mass and Gaussian transport errors

For each core point p_i, an optimal W1 coupling (or couplings approaching
the infimum) can move at most W1(mu,mu')/rho mass from p_i outside the closed
ball B(p_i,rho). The first marginal mass at p_i is at least v_i. Therefore

    mu'(B(p_i,rho)) >= m-eta/rho >= m/2=2^-(ell+1).          (6)

No disjointness of the balls is needed. One ball attaining the directional
core support will be used at a time. If several labelled masses share a
point, the same bound still holds.

A Gaussian translation by vector z changes its L1 norm by at most
sqrt(2/pi)|z|/sqrt(s) <= |z|/sqrt(s), using the integral of a directional
Gaussian derivative. Its L-infinity change is at most
C_s |z|/sqrt(s), since sup |grad gamma_s|=C_s exp(-1/2)/sqrt(s).
Integrating along a transport coupling gives, for f=mu*gamma_s,
g=nu*gamma_s and f'=mu'*gamma_s, g'=nu'*gamma_s,

    ||f'-f||_1+||g'-g||_1 <= eta/sqrt(s) <= eta,
    ||f'-f||_infinity <= C_s eta/sqrt(s) <= C_s eta.         (7)

These estimates need finite transport cost, not bounded actual support.
Hinges are 1-Lipschitz in density L1.

## 3. The middle band and upper thresholds

R8's Theorem B gives, with d=D/s>=2^-a and the exponent N in (3),

    H_g(h)-H_f(h) >= d 2^-N >= 2^-M                       (8)

throughout C_s 2^-j <= h <= M_g-C_s 2^-k, M_g=||g||_infinity.
All normalized radii for s>=1 are bounded by the supplied R. This entire
chain margin is an analytic import, not an output of integer verification.

The reviewed peak lemma applies to the composite short endpoint map and the
reference source radius R. Since e<4,

    M_g-M_f >= (C_s/4)(D/s) exp(-9R^2/2)
             >= 4 C_s 2^-k.                               (9)

By (7), ||f'||_infinity<=M_g-3 C_s 2^-k. Thus the full asserted middle band
lies inside (8). Its actual hinge gap is at least
2^-M-eta>=2^-(M+1). Above the actual source peak its hinge vanishes, so the
required sign is automatic. No peak search or threshold sampling is used.

## 4. Signed low thresholds with an unbounded actual source

The old [cloud-tail proof](../gaussian_majorisation_open_stability/PROOF.md)
uses bounded supports on both sides. We give the needed asymmetric argument
explicitly. Put R0=Re+1, m'=2^-(ell+1), delta=w/2, and

    K0=R0^2+2S log(1/m'),       A0=K0+5R0^2 <= A.

For theta in S2 write alpha=h_(P_c)(theta)-rho and beta=h_K(theta)+rho;
both lie in [-R0,R0]. The entire maximizing source-core ball lies in
B(0,R0) and has mass at least m' by (6), whether or not the rest of mu'
is bounded. For r>=0 this gives

    f'(r theta)/C_s >= exp((-r^2+2r alpha-K0)/(2s)).         (10)

The target support condition and its total mass one give

    g'(r theta)/C_s <= exp((-r^2+2r beta)/(2s)).             (11)

No lower bound on target atom masses, or upper bound on the source remainder,
is used here. Translations are chosen independently for the two inequalities;
superlevel volumes and hinges are translation invariant.

Let h=C_s exp(-q^2/(2s)) and suppose q>=Q0=4A/delta. Since delta<=2R0,
K0>=R0^2, and A>=K0+5R0^2, these inequalities imply q>=4R0,
q>=K0/R0 and q^2>2K0. The superlevel {f'>h} contains the star body of
radial function

    r_-(theta)=q+alpha-K0/q > 0.

Indeed the quadratic exponent in (10) exceeds the threshold on the whole
interval from zero up to alpha+sqrt(q^2+alpha^2-K0), and that root is at
least r_-. We do not assert that the actual source superlevel is star-shaped.
The target superlevel is contained in the star body of radial function

    r_+(theta)=q+beta+K0/q,

because the positive root in (11) is beta+sqrt(q^2+beta^2)<=r_+.

For |u|<=R0 and e=+/-K0/q, we have |e|<=R0 and, using q>=4R0,

    |(q+u+e)^3-q^3-3q^2 u|
      <=3K0 q+12R0^2 q+8R0^3 <=3A0 q.                    (12)

Integrating the two radial cubes with ordinary sphere area measure and
dividing by three now proves

    |{f'>h}|-|{g'>h}|
      >=4pi q^2[W(P_c)-W(K)-2rho]-8pi A0 q
      >=2pi delta q^2.                                    (13)

All these volumes are finite, at most 1/h. For probability densities,
H_(g')(h)-H_(f')(h)=integral_0^h (|{f'>t}|-|{g'>t}|) dt;
this is the layer-cake identity applied separately to min(f',h) and min(g',h).
Equation (13), valid at every smaller positive threshold too, gives

    H_(g')(h)-H_(f')(h)
      >=4pi delta s h [log(C_s/h)+1] > 0                  (14)

for 0<h<=C_s exp(-Q0^2/(2s)). Since j>=Q0^2, log 2>=1/2 and s>=1,
this includes every 0<h/C_s<=2^-j. Combine (14) with Section 3.
At h=0 both hinges equal one. Both joins include their endpoints.
This proves the theorem, including for unbounded mu' of finite first moment.

## 5. A finite certificate for a continuum of background laws

The executable takes k>=2 rational core sites at each stage, a nonempty
rational vertex list V for a background polytope B0=conv(V), and one supplied
N, straight-M or orthogonal-lift-M guard for each link. Every point of B0
is fixed at every reference stage. The reference laws range over

    mu=sum_i v_i delta_(p_i) + lambda,
    nu=sum_i v_i delta_(q_i) + lambda,
    v_i>=2^-ell, sum_i v_i<=1,
    lambda any nonnegative Borel measure on B0 of mass 1-sum_i v_i. (15)

The vertices are geometric witnesses, not labels required to carry mass.
Repeated vertices and redundant interior points may be added without
restricting (15). We now justify why the finite checks certify all of (15).

For each link the checker appends V to the core lists and checks all pairs.
For a core pair it verifies the exact squared-distance loss is nonnegative.
For a core point p->q and x in B0 the loss

    |p-x|^2-|q-x|^2=|p|^2-|q|^2-2(p-q).x                  (16)

is affine in x. Its nonnegativity on V proves it throughout B0. All
background-background distances are fixed. Thus every stage map on the
whole core union B0 is short; any collision has a consistent image.
Such a map is continuous, so R8's support-map hypotheses hold.

For an N guard, verify the norm equality and radius at every appended
vertex and core site. The equality |x-a|^2-|x-b|^2=0 is affine on B0,
and the squared radius is convex, so both extend from V to B0.
For a straight-M guard, for every appended pair check

    (q_i-q_j).[(q_i-q_j)-(p_i-p_j)] <= 0.                  (17)

Half the squared-distance derivative along straight interpolation is
increasing in time, and (17) is its terminal value. For a core-background
pair (17) is (q-x).(q-p)<=0, affine in x. Background pairs have derivative
zero. Hence the entire continuum moves contractively in R3, admissibly in R5.
For orthogonal-lift-M require shortness and

    affdim(core_source union V)+affdim(core_target union V)<=5. (18)

Their convex hulls have those same affine spans. Independent translations
and isometric coordinates let the whole compact support use
(cos(pi t/2) P, sin(pi t/2) Q) in the orthogonal sum. Squared pair distances
are the decreasing convex interpolation of the endpoint squared distances.
The trajectories are smooth with bounded speed on the compact label set.
These two M guards are reused from R8 and the previous consumer.

The initial radius check uses all initial core points and V; convexity
extends it to B0. The endpoint-radius and width checks use the source core
alone on the source side, and

    K=conv({q_i} union V)

on the target side. Barycentric containment places K in conv(P_c). The old
single rational cap guard supplies a lower support gap gamma on a cap of
probability (1-c)/2, giving w=(1-c)gamma/2. Transverse norms are rounded
upward by an exact integer square root, then checked by squaring. No cap
enumeration or new cap inequality is part of this contribution.

All cross and background losses are nonnegative. Thus, uniformly for every
law (15),

    D >= d0=2(2^-ell)^2 sum_t sum_(i<j, core) Delta_ij^t
           =2(2^-ell)^2 sum_(i<j, core)(|p_i-p_j|^2-|q_i-q_j|^2). (19)

The ordered factor two is essential. The producer selects a with 2^-a<=d0/S,
and the explicit schedule (2)--(3). Only k*2^-ell<=1 is required for a
nonempty prior domain. The number of background vertices or atoms does not
enter this feasibility condition or d0.

## 6. Calibration, scope and checking boundary

The [input](INPUT.json) reuses the previous fifteen-point core and six folds:
0, +/-e_i, +/-2e_i, and +/-(3/2,3/2,3/2), folding outside +/-3/2 in each
coordinate. It adds the *entire cube* B0=[-1/3,1/3]^3 as a fixed arbitrary
background. This cube lies in conv({+/-e_i}); the geometry is not new.
With R=4, Re=3, S=4 and ell=5, every core weight is at least 1/32 and up
to 17/32 of the mass can be any measure on the cube. The exact record gives

    sum_core unordered loss =270,       d0=135/256,
    a=3,       w=13/20000,              rho=2^-13,
    B=12564298226894.

These constants certify *every* reference prior and background in (15),
and every pair of actual laws satisfying (4), at *every* threshold and
every variance in [1,4]. Arbitrary background atom counts, vanishing
background masses and diffuse measures are included by the proof, not
inferred from finite samples. Even starting from a finite reference law,
(4) permits tiny source components arbitrarily far away, or an unbounded
finite-first-moment source tail. Such perturbations are not in the previous
fixed-radius cloud family. The target remains confined to its envelope.

An exact dual supported on the core has coefficients -1,-1,+1,+1 on
+e_1,-e_1,+2e_1,-2e_1. Its total mass and source/target vector moments
vanish, while its squared-norm-loss sum is 6. Therefore these endpoint
configurations admit no independent norm-preserving anchors. Adding the
background cannot remove this obstruction. Both endpoint core diameters
squared are 27; no same-reference strict homothety buffer is inserted.

The producer uses pair differences and row reduction. The separately written
record checker imports neither it nor its helpers: it uses Gram losses,
a core trace-variance telescope, scatter-matrix principal minors for rank,
and rational inequalities for the cap and schedule. The default suite calls
the producer only for reproducibility controls; supplied-record mode never
does. All checks use Python arbitrary-precision integers and Fraction.

The code certifies the rational hypotheses and exponent schedule. Equations
(6)--(19), the extension from vertices to the continuum, Gaussian transport
estimates, and the imported analytic results remain written mathematical
proofs, not proof-assistant theorems. Dependency statuses and hashes are in
[DEPENDENCIES.json](DEPENDENCIES.json) and [SOURCES.md](SOURCES.md). The large
dyadic denominator is never constructed. No effective practical unrestricted
cover, unsigned middle-frontier sign, or new Kneser--Poulsen consequence is
claimed. Author-side checks are not independent acceptance.
