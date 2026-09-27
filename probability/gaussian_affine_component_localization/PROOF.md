# Uniform all-variance comparison for affine components

27 September 2026. Author proof, independent acceptance pending. The
unrestricted dimension-three Gaussian-majorisation problem remains open.
This constructs one support-level contracting motion; there is no
variance/threshold cutoff or atom-count parameter.

The mechanism builds on R4's rigid-block motion and the accepted weighted
Procrustes identity. Component covariances convert auxiliary mean error
to control of every support point. Polar deformation then permits genuine
affine compression inside each component. Gaussian and ball-volume
comparisons from a contracting motion are credited prior theorems.

## 1. Statement

Let bounded K be a finite union of compact sets K_j in R3. Assume T is a
contraction on K, with the affine formula

    T(x)=b_j+A_j(x-c_j) on K_j,        ||A_j||op<=1.             (1)

Choose an AUXILIARY probability lambda=sum_j p_j lambda_j, with lambda_j
supported on K_j and

    p_j>=m>0, E_(lambda_j)X=c_j, Cov_(lambda_j)X>=kappa I3,
    Cov_lambda X>=k I3,       kappa,k>0,       diameter(K)<=d.  (2)

The auxiliary law need not be the law whose Gaussian comparison is
requested. Since c_j belongs to conv K_j, every x in K_j satisfies
|x-c_j|<=d. The conditional covariance floor is full rank; this theorem
does not include lower-dimensional components.

For independent X,X' from lambda set

    Delta(x,x')=|x-x'|^2-|T(x)-T(x')|^2,
    D=E Delta(X,X'),      epsilon=sup_(K x K) Delta.

Let delta_cross lower-bound every loss between different components.
Write X0=X-EX, Y0=T(X)-ET(X), and use independent primed copies in

    F=E[(X0.X0'-Y0.Y0')^2],
    e=2F/(km),              C=4+78d^2/kappa.                  (3)

**Theorem 1.** If

    e<=kappa/4,              delta_cross>=Ce,                 (4)

then after one target isometry, T has a simultaneous real-analytic
contracting motion in R3 on ALL of K. Thus for EVERY probability mu
supported on K, EVERY s>0 and h>=0,

    integral (mu*gamma_s-h)_+ <= integral ((T#mu)*gamma_s-h)_+.(5)

Every finite choice of centers in K also satisfies both Kneser--Poulsen
volume inequalities with arbitrary individual nonnegative radii: union
volume decreases and intersection volume increases. Separate endpoint
isometries leave these conclusions invariant. If F=0, T is an ambient
isometry on K and equality holds.

No atom weight, covariance, or component mass floor is imposed on the
requested mu. Those floors belong only to the auxiliary certificate (2).
The finite component count is at most1/m; the number of support points or
atoms in each component is unrestricted.

**Corollary 2 (a whole mean-loss sector).** If cross losses are at least
rho epsilon, with 0<rho<=1, then

    D <= 2rho k m/(4+78d^2/kappa)                             (6)

suffices for (5) and both ball-volume signs. The bound is uniform as D
tends to zero. It applies to an entire parameter region at all variances,
not a chosen input neighborhood or a new eventual joining schedule.

## 2. Weighted Procrustes and affine control

View the centered source/target coordinates as operators P,Q:R3->L2(lambda).
The accepted R1 trace identity gives an orthogonal target alignment with

    E=E_lambda|T(X)-X|^2 <= 2F/k.                            (7)

For completeness, polar alignment makes P*Q symmetric positive
semidefinite. With U=P+Q,V=P-Q, direct expansion yields

    F=||PP*-QQ*||HS^2
     =(1/2)tr(U*U V*V)+(1/2)tr((U*V)^2).

Here U*V=P*P-Q*Q is symmetric and U*U>=P*P>=kI. The second trace is
nonnegative, giving F>=k||P-Q||HS^2/2. Restoring means proves (7).
This is the existing Hilbert-space argument, with no finite-atom premise.

Apply that global target isometry and retain the symbols A_j,b_j. Put

    u_j=b_j-c_j,
    E_j=E_(lambda_j)|T(X)-X|^2
       =|u_j|^2+tr((A_j-I)Cov_(lambda_j)X(A_j-I)^T).           (8)

Consequently |u_j|^2<=E_j and ||A_j-I||F^2<=E_j/kappa. For different
i,j, the useful estimate is

    E_i+E_j <= (p_i E_i+p_j E_j)/m <= E/m <= e.               (9)

Each E_j<=e as well. This converts a weighted mean bound to uniform
control on the whole affine component. Arbitrary support clouds do not
have this implication. If F=0, (8) forces all aligned A_j=I and u_j=0,
so every point of K is fixed. Otherwise (4) forces positive cross losses
and hence disjoint components, avoiding any ambiguity in the paths below.

## 3. Polar paths and cross-distance control

By (4), ||A_j-I||op<=1/2. Its segment from I is invertible, so det A_j>0.
Polar decomposition A_j=Q_j S_j gives Q_j in SO3 and 0<S_j<=I. The polar
factor minimizes Frobenius distance to orthogonal matrices (by SVD), so

    ||S_j-I||F<=||A_j-I||F,  ||Q_j-I||F<=2||A_j-I||F.         (10)

Let Omega_j be the shortest skew rotation logarithm of Q_j. For rotation
angle theta in[0,pi], ||Q_j-I||F^2=8sin^2(theta/2). Using
theta/(2sin(theta/2))<=pi/2 and pi^2<10 gives

    ||Omega_j||op^2<=(5/4)||Q_j-I||F^2<=5E_j/kappa.           (11)

Use the same clock for every component:

    S_j(t)=I+t(S_j-I),
    z_j(t,x)=c_j+t u_j+exp(t Omega_j)S_j(t)(x-c_j).            (12)

Within a component, rotation preserves norms and the positive eigenvalues
of S_j(t) decrease. Therefore all within-component distances decrease,
including equality directions. For r=x-c_j, differentiation gives

    z_j'=u_j+exp(t Omega_j)[Omega_j S_j(t)+(S_j-I)]r,
    z_j''=exp(t Omega_j)[Omega_j^2 S_j(t)+2Omega_j(S_j-I)]r.

No commutation between Omega_j and S_j is assumed. Since ||S_j(t)||<=1,
|r|<=d, sqrt5+1<4 and 5+2sqrt5<10, (8)--(11) imply

    |z_j'|^2<=E_j(2+32d^2/kappa),
    |z_j''|<=10d E_j/kappa.                                 (13)

The second term in the acceleration is essential for affine compression;
one cannot reuse the rigid-block constant after omitting it. For the
difference Z of points in two distinct components, (9) now gives

    |Z'|^2<=e(4+64d^2/kappa),   |Z''|<=M=10de/kappa.          (14)

The Dirichlet Green kernel bounds deviation from the endpoint chord by
M t(1-t)/2<=M/8. Endpoint contraction bounds both endpoint norms by d,
so |Z(t)|<=d+M/8. With f=|Z|^2, let

    L=2[e(4+64d^2/kappa)+(d+M/8)M] >= sup|f''|.

Because integral_0^1 f'=-Delta, integration of the derivative bound yields

    f'(t)<=-Delta+L integral_0^1|t-v|dv<=-Delta+L/2.

For e<=kappa/4,

    L/2<=e[4+(74+25/8)d^2/kappa]<=e[4+78d^2/kappa]=Ce.        (15)

The remaining coefficient margin is7/8. Guard (4) therefore makes every
cross distance nonincreasing. This proves the simultaneous analytic motion.

Aishwarya--Li2609.07041v2 Theorem1.4 gives (5). Classical moving-center
comparison, or Bezdek--Connelly's theorem after embedding R3 in R5,
gives the arbitrary-radius ball conclusions. Distinct source centers
cannot collide before the last time: nonincrease would force their analytic
squared distance to vanish on an interval. Endpoint limits cover coincident
targets and zero radii. These transfer theorems are prior results.

Weighted double centering of the squared-distance kernel gives

    F<=(1/4)E Delta^2<=epsilon D/4.                          (16)

For Corollary2 use e0=epsilon D/(2km). Condition (6) gives
Ce0<=rho epsilon<=delta_cross. Also epsilon<=d^2 and
e0<=rho d^2/C<kappa/78<kappa/4. Thus (4) holds. The zero-loss case is
the isometry case. D here is the loss of the auxiliary law, not a claimed
loss bound for every requested mu.

## 4. Exact certificates for whole solid boxes

The executable treats K_j=c_j+product_l[-h_jl,h_jl], with positive
rational halfwidths and rational matrices/centers. The auxiliary lambda_j
is uniform volume, with covariance diag(h_jl^2/3). For global source,
target and cross covariances V_X,V_Y,C_XY, elementary identities give

    F=tr(V_X^2)+tr(V_Y^2)-2||C_XY||F^2,
    D=2tr(V_X-V_Y).                                        (17)

The covariance floors and I-A_j^T A_j>=0 are exact rational PSD checks.
Source diameter squared is
max_(i,j)sum_l(|c_il-c_jl|+h_il+h_jl)^2, including i=j.

To check cross contraction on WHOLE boxes, write a=c_i-c_j, b=b_i-b_j,
x=c_i+u, x'=c_j+v and M=I-A_i^T A_j. Direct expansion gives

    Delta=|a|^2-|b|^2+2(a-A_i^T b).u-2(a-A_j^T b).v
          -2u^T Mv
          +u^T(I-A_i^T A_i)u+v^T(I-A_j^T A_j)v.              (18)

The last two quadratics are nonnegative. Bound the other variable terms
below by their coordinate absolute-value bounds. The producer's resulting
minimum is a uniform lower bound, not a sampled vertex claim. The separate
checker evaluates the remaining MULTIAFFINE polynomial at all64 corners;
its exact minimum also bounds (18) below. Testing only full quadratic
values at vertices would be unsound because an interior minimum is possible.

A successful record thus verifies the global contraction itself; there
is no separate unverified actual-map premise. The actual probability law
can be any law on the box union. Production uses O(B^2) fixed-size rational
matrix operations and O(B) storage for B components, plus input-dependent
bit cost. No Gaussian quadrature or variance grid is used.

The separate checker reconstructs F directly as a weighted centered Gram
sum. It uses27 rational points per box: in each coordinate the nodes
-h,0,h have weights1/6,2/3,1/6. This preserves all degree-two moments.
It is legitimate for the QUADRATIC alignment calculation, not a statement
that Gaussian hinges are determined by finitely many moments.

## 5. An exact nontrivial parameter interval

Use three source solid cubes of halfwidth1, centered at
c_1=(-16,0,0), c_2=(16,0,0), c_3=(0,16,0). Their uniform volume laws
have auxiliary weights1/3. Set b_j=(1-t)c_j and A_j=Q_j S_j, where

    Q_1=I, Q_2=R_z(theta), Q_3=R_x(theta),
    cos(theta)=(1-t^2)/(1+t^2), sin(theta)=2t/(1+t^2),
    S_1=diag(1-t,1,1), S_2=diag(1,1-t,1), S_3=diag(1,1,1-t). (19)

**Corollary3.** Every 0<=t<=2^-36 satisfies (5) for every law on the
three solid cubes, at all variances, and both ball-volume inequalities.
This is a rigorous interval, not finite sampling or a historical novelty
claim for the example. The main result is the arbitrary-component guard.

Here m=k=kappa=1/3, d^2=1164<35^2 and C=272380. Also
||A_j-I||op<=3t, so any source point moves at most22t. Every pair loss
is therefore at most3080t once contraction is established. Direct traces
give D=(4102/9)(2t-t^2)<=912t.

For a cross pair write the source difference as a+w, with
sqrt512<=|a|<=32, |w|<=4. The target difference is (1-t)a+w+v,
where |v|<=12t. Expansion yields

    Delta>=t[(2-t)|a|^2-32|a|-96-144t]>=128t  (t<=1/16).     (20)

The bracket increases for |a|>=22. At22 and t=1/16 it is515/4>128.
Within each cube the matrix contracts, so (20) verifies global contraction.
Equation (16) now gives e<=12640320t^2. The exact integer inequalities

    12*12640320 <= 2^72,
    272380*12640320 <= 128*2^36                               (21)

prove both guards on the entire interval. The published finite fixture
uses t=2^-36 and the sharper exact F rather than this coarse upper bound.

For t>0 the solid-domain map cannot be covered by finitely many rigid
pieces. Within component1 an isometric restriction must have all its
differences perpendicular to the compressed axis, hence lie in one affine
plane. Finitely many such planes cannot cover the cube interior. The same
argument applies to the other components. Exact anchored norm preservation
is also impossible on an open component: its quadratic coefficient would
force A_j^T A_j=I, which fails regardless of anchors or endpoint isometries.

No global orthogonal target alignment makes straight interpolation
contract either. Preserved directions e_2,e_3 in component1 force the
alignment O to fix them, so O=diag(+/-1,1,1). Preserved e_1,e_3 in
component2 would additionally require O Q_2 e_1=e_1, impossible since
sin(theta)>0. The necessity comes from the quadratic squared-distance
function of a straight motion for a pair whose endpoint distance is equal.

These statements distinguish actual hypotheses: finite rigid pieces,
exact anchor norms, and a globally aligned straight clock. They do not
exclude every known motion class or every possible composition.

## 6. Scope and trust

The certificate lifts mean-error alignment to arbitrary diffuse component
laws without an atom-count factor and allows non-isometric affine pieces.
It signs a whole small-loss sector at all thresholds and variances.
General nonlinear components, covariance collapse, uncontrolled auxiliary
component masses, and too-small cross losses remain outside it. In
particular adjacent arbitrary affine cells and the cross-tight screw
obstruction are not automatically covered. Failed guards are unresolved,
not negative Gaussian hinges.

The near-cubic cubature, accepted middle theorem, and support-cap6520 keep
their hypotheses; none is used to bypass the affine or cross-domain
conditions. R4's lower-dimensional rigid blocks remain a complementary
case rather than being silently included in this full-rank statement.

The Hilbert-space identity, polar decomposition, rotation logarithms,
Green-kernel estimate and classical motion transfers are conventional
mathematics. Exact checks certify finite rational inputs, identities and
controls; they do not formalize the proof or independently accept it.
Historical priority for this quantitative criterion is not established.
