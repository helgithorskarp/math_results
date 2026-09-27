# Strict Gaussian comparison through contracting motions and mixed chains

Author proof, 27 September 2026; independent review is pending. The
unrestricted R3 problem remains open. Non-strict comparison under an R5
contracting motion and under finite composition is already known. The
increment is a loss-linear hinge margin uniform over the motion and the
number of steps, with strictness retained under bounded-radius limits.

## 1. Statements and precise motion hypothesis

Write gamma_s^(n) for the centered Gaussian density of covariance s I_n,
C_s=(2 pi s)^(-3/2), and H_f(h)=integral_R3(f-h)_+. For a bounded source
law mu and a short map T on its support put f=mu*gamma_s,
g=(T#mu)*gamma_s, M_g=max g and

    D=E[|X-X'|^2-|TX-TX'|^2].                              (1)

The independent copies in (1) make D an ordered mean loss.

An admissible R5 motion consists of trajectories Z_t(x), 0<=t<=1, whose
endpoints are isometric embeddings of x and Tx into R5. Every pair distance
is nonincreasing. Trajectories are absolutely continuous, with jointly
measurable velocities satisfying

    integral_0^1 ess sup_(x under mu) |dot Z_t(x)| dt < infinity. (2)

The same assertion may hold on finitely many joined time intervals.
Maps on the support are taken continuous in x. The usual piecewise smooth
bounded-support certificates, including trigonometric parametrizations of
orthogonal lifts, meet these hypotheses. We do not infer (2) for an arbitrary
continuous motion without an approximation argument.

For an integer R>=1 and integers j,k>=0 define

    B_N(R)=40R^2+9R+38,     B_M(R)=66R^2+2R+18,
    n_N(R,j,k)=B_N(R)+3j+8k,
    n_M(R,j,k)=B_M(R)+4j+5k,
    n_C(R,j,k)=max(n_N(R,j,k+1),n_M(R,j,k+1))
                                  +k+2R^2+2R+1.            (3)

**Theorem A (any supplied admissible R5 motion).** Suppose the source fits
a ball of radius R sqrt(s) and T has such a motion. Then

    H_g(h)-H_f(h) >= (D/s) 2^(-n_M(R,j,k))                  (4)

throughout C_s 2^-j<=h<=M_g-C_s 2^-k. There is no atom-count, atom-mass,
covariance, positive-loss-floor, speed or path-length constant in (4).
Condition (2) is a regularity premise, not a numerical budget in the bound.

**Theorem B (arbitrarily many mixed steps).** Start with a law fitting a
ball of radius R sqrt(s). Apply any finite sequence of short maps on the
successive supports. Each step must be either:

* M: supplied with an admissible R5 motion; or
* N: supplied with anchors a,b satisfying |x-a|=|Tx-b|<=R sqrt(s).

Let D be the total endpoint loss (1). At the same thresholds,

    H_g(h)-H_f(h) >= (D/s) 2^(-n_C(R,j,k)).                 (5)

The bound is independent of the number of steps and of the distribution of
their losses. The anchor-radius restriction on N steps is material. The
non-strict composition implication is an antecedent, not a new theorem here.
There is also one whole-curve lower envelope. Set m=M_g/C_s and

    B_C(R)=max(B_N(R)+8,B_M(R)+5)+2R^2+2R+1.

For every 0<=u<=1, the same chain satisfies

    H_g(C_s u)-H_f(C_s u) >= (D/s)2^-B_C u^4(m-u)_+^9.    (5a)

For a single M step the corresponding lower envelope is
(D/s)2^-B_M u^4(m-u)_+^5. No positive threshold cutoff is part of either
whole-curve statement. A separately certified lower bound p<=m may replace m.

**Theorem C (limits and ambient stability).** The same real-parameter bounds
proved below, and hence (5), pass to weak limits of paired endpoint laws in
a fixed compact set, for chains with a common R. Their lengths may diverge.
Every nonisometric limiting short map has H_g(h)>H_f(h) for every 0<h<M_g
and has M_g>M_f. Equality at one nontrivial hinge forces support isometry.

By the accepted compact-width theorem and the earlier bounded-law openness
criterion, every such nonisometric pair is an ambient product-W_infinity
interior point at fixed variance. Independent small perturbations of both
laws may leave all these geometric classes. A common neighborhood exists
on any specified compact interval of positive variances. No common positive
radius as D or s tends to zero is asserted.

This is a stability theorem for supplied certificates and their controlled
limits. It is not a construction of an R5 motion for an arbitrary short map,
nor a sign for the proper screw excluded by the existing mixed-chain result.

## 2. A two-sided peak budget for every bounded contraction

Normalize s=1. This lemma holds in any ambient dimension n. Suppose the
source and target laws fit independently centered radius-R balls. With
C_n=(2 pi)^(-n/2) and M_f,M_g their Gaussian peaks,

    (D/4)exp(-4R^2) <= log(M_g/M_f) <= (D/4)exp(R^2),
    0<=M_g-M_f<=C_n exp(R^2)D/4.                           (6)

Here and below Var_pi(X)=E_pi|X-E_pi X|^2 is scalar trace variance.
The Gibbs variational formula, with the spatial maximum taken too, gives

    log(M_f/C_n)=sup_pi [-Var_pi(X)/2-KL(pi||mu)],           (7)

where pi ranges over probability laws on source labels absolutely continuous
with respect to mu. Indeed at a fixed z the variational expression is
E_pi[-|z-X|^2/2]-KL; optimizing z gives z=E_pi X. A maximizing z exists
because the convolution vanishes at infinity. Its Gaussian posterior pi
attains (7). The same label-space formula holds with TX for the target,
even if distinct labels have the same image.

For a law in B(0,R), a mode is a posterior mean and lies in B(0,R).
Its posterior likelihood ratio obeys

    exp(-2R^2) <= d pi/d mu <= exp(R^2/2).                  (8)

The lower bound uses |z-X|<=2R and M_f<=C_n. The upper bound uses
M_f>=f(0)>=C_n exp(-R^2/2). All relative entropies of these posteriors
are finite. Evaluate the source optimizer in the target version of (7):

    log(M_g/M_f)>=D_(pi_source)/4>=exp(-4R^2)D/4.

Evaluate the target optimizer in the source problem for the upper bound,
using D_(pi_target)<=exp(R^2)D. Finally 1-exp(-v)<=v and M_g<=C_n give
the second line of (6). The lower estimate was already proved in
[strict norm-preserving hinges, Section 2](../gaussian_norm_preserving_strictness/PROOF.md).
The reverse-posterior upper estimate is what controls a suffix of losses.
No entropy-order-to-majorisation implication is assumed.

We also use a classical consequence of Kirszbraun's extension theorem:
a short image of a set in a radius-R ball of a Euclidean space fits some
radius-R ball in the target Euclidean space. Extend the map to the source
ball center. Thus every intermediate configuration of a contracting motion,
and every law in a short-map chain, has circumradius at most R. This works
even when the intermediate ambient space is R5. These centers are used
pointwise in estimates; they are never differentiated in time.
For completeness, it also follows directly from the smallest enclosing
ball of a compact image: its center is a convex combination of boundary
points y_i, with weights a_i. Its squared radius is Var_a(Y), at most
Var_a(X) by the pair-distance formula, and hence at most
sum_i a_i|x_i-c_source|^2<=R^2. This uses only the elementary optimality
condition for the smallest enclosing ball, including lower-dimensional
images.

## 3. The credited pressure identity in five dimensions

Still take s=1. Put c=(2 pi)^(-1), C=(2 pi)^(-3/2), so C_5=cC.
Let Q_t=law(Z_t(X))*gamma_1^(5). For a smooth convex U with U(0)=0 and
0<=U'<=1, vanishing on a neighborhood of zero, define

    V(r)=r U'(r/c),              P_V(r)=r V'(r)-V(r)
                                             =r^2 U''(r/c)/c. (9)

Two-dimensional Gaussian integration in polar coordinates gives exactly

    integral_R2 V(f(x)gamma_1^(2)(y))dy=U(f(x)).             (10)

Indeed the left side is integral_0^1 f(x) U'(f(x)v)dv. Thus the endpoint
V energies of Q_t are precisely the desired three-dimensional U energies.
This inverse two-Gaussian-coordinate transform and the continuous-contraction
pressure mechanism are from [Aishwarya--Li, Theorems 1.4/1.5 and Sections 3/4](https://arxiv.org/html/2609.07041v2).
We retain their positive integrand to obtain a strict bound, rather than
claiming a new transfer theorem or evolution construction.

For almost every time let

    ell_t(x,x')=-d/dt |Z_t(x)-Z_t(x')|^2>=0,
    L_t=E ell_t(X,X'),             D=integral_0^1 L_t dt.    (11)

The canonical posterior velocity v_t(z)=E[dot Z_t(X)|Z_t(X)+G=z]
satisfies the continuity equation and

    div v_t(z)=tr Cov_(pi_t,z)(dot Z_t,Z_t)
                              =-E_(pi_t,z x pi_t,z)ell_t/4.

The factor 1/4 follows by symmetrizing the covariance and differentiating
the squared pair distance. Differentiating the V energy, integrating by
parts and using (9) therefore gives

    integral U(g)-integral U(f)
      =1/(4c) integral_0^1 integral_R5 U''(Q_t(z)/c)
        E[ell_t(X,X') gamma_5(z-Z_t(X))
                            gamma_5(z-Z_t(X'))] dz dt.     (12)

Assumption (2) justifies the continuity equation, time differentiation in
L1 and Fubini. For each smooth U used below, its derivatives vanish below a
positive density threshold, confining the pressure to a common bounded set.
This justifies spatial integration by parts without an unproved boundary
term. All terms on the right of (12) are nonnegative; Tonelli applies.
In particular (12) recovers the already known non-strict sign.

## 4. Extracting loss where the level is crossed

Let 0<tau,epsilon<=1 and suppose C tau<=h<=M_g-C epsilon. Define

    lambda(t)=integral_t^1 L_r dr,
    lambda_0=2epsilon exp(-R^2),
    ell=log(2/tau),  L=2R+sqrt(2ell),  A=L+2R.             (13)

The logarithmic radial cutoff is the useful refinement from R3's
[polynomial norm-preserving margin, Sections 2--3](../gaussian_polynomial_hinge_margin/PROOF.md).
We use it here for the different five-dimensional motion kernel.

The current-to-final matching is a contraction in R5. By (6), whenever
lambda(t)<=lambda_0,

    max(Q_t/c)>=M_g-C exp(R^2)lambda(t)/4
                                      >=h+C epsilon/2.   (14)

Fix such a time and any mode z_* of Q_t. Relative to any enclosing ball
center c_t it satisfies |z_*-c_t|<=R. The global bound
||grad(Q_t/c)||_infinity<=C follows directly from the Gaussian derivative.
On every ray z_*+r theta, theta in S4, at r_0=epsilon/4 one has

    Q_t(z_*+r_0 theta)/c>=h+C epsilon/4.

At r=L, the distance to every center is at least sqrt(2ell), and hence

    Q_t(z_*+L theta)/c<=C exp(-ell)=C tau/2.

Here L>r_0 because R>=1. Let U be a smooth hinge with U'' a probability
density supported within distance min(C epsilon/8,C tau/4) of h.
Along each ray its first derivative changes from one to zero. The
fundamental theorem of calculus and the global gradient bound yield

    integral_(r_0)^L U''(Q_t(z_*+r theta)/c)dr>=1/C.         (15)

No regular level, unique mode, or monotonicity along a ray is required.
On the annulus, every center is at distance at most A from the point of
integration. Thus each product of Gaussian kernels is at least
C_5^2 exp(-A^2). Use r^4>=epsilon^4/256, the surface area |S4|=8 pi^2/3,
and (15) in (12). At this time the lower bound per unit dt is

    [pi C epsilon^4 exp(-A^2)/(3*2^8)] L_t.                (16)

The absolutely continuous nonincreasing lambda goes from D to zero, so
the integral of L_t over {lambda(t)<=lambda_0} is min(D,lambda_0).
Because D<=4R^2, R>=1 and lambda_0<=2,

    min(D,lambda_0)>=epsilon exp(-R^2)D/(2R^2).

Consequently the real-parameter motion bound is

    H_g(h)-H_f(h)>=c_M(R,tau,epsilon)D,
    c_M=pi C epsilon^5 exp[-A^2-R^2]/(3*2^9 R^2).          (17)

Pass from smooth hinges to the actual hinge by dominated convergence at
the two endpoints, using 0<=U(v)<=v and U(0)=0. The lower bound is uniform
in the smoothing width. The elementary square inequality gives

    A^2=(4R+sqrt(2ell))^2<=32R^2+4ell.

It follows that c_M>=pi C exp(-33R^2)tau^4 epsilon^5/(3*2^13 R^2).
Now pi C>1/8, 3<4, e<4 and R^2<=2^(2R) imply

    c_M>=2^-B_M tau^4 epsilon^5.                          (17a)

This gives n_M in (3), proving (4) at s=1, including critical thresholds
and diffuse laws. Set tau=u, epsilon=M_g/C-u for 0<u<M_g/C to obtain
the single-motion whole-curve statement. At zero the two hinges equal one;
at and above M_g both are zero by (6).

## 5. A budget independent of the number of steps

R3's [polynomial refinement](../gaussian_polynomial_hinge_margin/PROOF.md)
of the previous [norm-preserving strictness theorem](../gaussian_norm_preserving_strictness/PROOF.md)
gives, at C tau<=h<=M_target-C epsilon, the usable real coefficient

    c_N(R,tau,epsilon)=2^-B_N tau^3 epsilon^8.             (18)

It gives the dyadic exponent n_N in (3). The kernel and original strictness
have independent acceptance; the polynomial refinement is an author-proof
dependency pending independent review. The review of the original
strictness also audited the exact portion of the openness theorem used below.

Let D_i>=0 be the ordered loss of step i, 1<=i<=m. The pair-distance
differences telescope, so sum_i D_i=D. Let M_i be the Gaussian peak after
step i. With h<=M_m-C epsilon, call an index eligible if

    sum_(r>i) D_r <= 2epsilon exp(-R^2)=lambda_0.

Applying (6) to its entire remaining composite gives M_i>=h+C epsilon/2.
Thus each eligible step, of either type, contributes at least

    c_0 D_i,       c_0=min(c_N(R,tau,epsilon/2),
                          2^-B_M tau^4(epsilon/2)^5).

The eligible indices form a suffix. Their total loss is at least
min(D,lambda_0): if it is not the entire chain, the first eligible step
crosses that loss budget. This remains true for zero-loss steps and for
one step larger than the budget. Every discarded step has nonnegative
hinge difference. Summing therefore proves

    H_g(h)-H_f(h)>=c_C(R,tau,epsilon)D,
    c_C=min(c_N(R,tau,epsilon/2),2^-B_M tau^4(epsilon/2)^5)
                                     *epsilon exp(-R^2)/(2R^2). (19)

For epsilon=2^-k the final factor is at least
2^(-k-2R^2-2R-1). Equations (17)--(18) give n_C in (3), proving (5).
There is no accumulation of approximation errors, and no lower bound on
an individual D_i has been inserted.

For the whole-curve form use 0<tau,epsilon<=1. The minimum in (19) is at
least 2^-max(B_N+8,B_M+5) tau^4 epsilon^8. The remaining factor is at least
epsilon 2^(-2R^2-2R-1). Taking tau=u, epsilon=M_g/C-u proves (5a) in the
interior. Continuity and (6) give its endpoint and exterior cases.

For general s, divide all coordinates by sqrt(s). Density thresholds are
multiplied by s^(3/2), ordered losses become D/s, and hinge values are
unchanged. This gives all the displayed variance-s statements.

## 6. Limits, equality, and the scope of the join

Consider paired endpoint laws pi_n supported in a fixed compact subset of
R3 x R3 and converging weakly to pi. Each support satisfies
|y-y'|<=|x-x'|. This closed condition passes to pi x pi and hence to every
pair of its support points. Two points with the same x must have the same
y. Compactness of the projection then identifies the limiting support
as the graph of a 1-Lipschitz T on the limiting source support.

The endpoint Gaussian densities converge uniformly and in L1; the former
follows from compactness, the common Gaussian modulus, and uniform tails,
and the latter also follows from pointwise convergence and unit integrals.
Their peaks converge. The ordered losses converge by bounded continuity
on the compact product. For a threshold on a closed upper band edge, use
epsilon_n=min(epsilon,(M_(g_n)-h)/C)>0 for large n. It tends to epsilon.
The real coefficients (17)--(19) are continuous in epsilon, so their bounds
pass with the same constants. A common R is necessary for this conclusion.

For every 0<h<M_g some positive tau,epsilon put h in the band. If D>0,
the gap is strict. If D=0, continuity and nonnegativity of the pair loss
make all distances on the support equal; the map extends to a rigid
isometry of its affine span and then R3. Every hinge is then equal.
The lower half of (6) gives the strict peak when D>0.

The independently accepted [compact width rigidity](../gaussian_compact_width_rigidity/PROOF.md)
gives a strict support mean-width gap for every such nonisometric limit.
With peak and hinge strictness, the [older bounded-law openness theorem](../gaussian_majorisation_open_stability/BOUNDED_LAWS.md)
applies directly. This proves the ambient-interior assertion and its compact
positive variance-band version. To see the latter explicitly, a common
physical radius bound becomes a common integer R after division by the
square root of the smallest variance in the interval. The same certificates
work at every variance there. Thus the fixed endpoint pair satisfies all
three strict conditions throughout the interval, and the compact-family
clause of the older openness theorem supplies one neighborhood. General
openness is not reproved here.

The finite composition sign was already recorded in the team's
[geometric portfolio](../gaussian_geometric_portfolio/CLASSIFICATION.md).
This proof adds a uniform strict margin that survives increasing chain
length and the specified limits. It does not remove an anchor-radius
condition by taking its bound to infinity. Existing R2 balanced, R3 affine-
component and R6 nonlinear-slice motion certificates can use Theorem A with
their hypotheses unchanged. No new motion is supplied for an unsigned pair.

For the R2/R3 finite-certificate mechanism, once separately signed low and
peak endpoints give a middle band as above, (4) or (5) gives an explicit
minimum. The old finite beta criterion succeeds when its error E_n obeys
2E_n<(D/s)2^(-n_M) or 2E_n<(D/s)2^(-n_C), respectively. This statement
does not make R2's proper-screw pilot a member of either input class, and
does not make its absolute quadrature error proportional to loss.

Neither a practical unrestricted cover nor a new Kneser--Poulsen consequence
is asserted. The meaningful new control is uniformity through small loss,
long certified chains, and bounded-radius limits at fixed variance.
