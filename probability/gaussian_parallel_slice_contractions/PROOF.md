# Arbitrary nonlinear maps between parallel slices

Complete author proof, 27 September 2026. Independent correctness review and
historical priority are pending. The unrestricted R3 Gaussian-majorisation
question remains open.

## 1. The full class

Let K be a nonempty closed convex subset of R2 and I a nondegenerate interval
of R. Suppose

    T:K x I -> R2 x R,       T(u,z)=(f(u,z),h(z))             (1)

is 1-Lipschitz for the Euclidean metric. There is no affinity assumption on
f, no differentiability assumption, and no additional contraction margin.
The last output coordinate is required to depend only on the last input
coordinate. Nonexpansiveness implies that h is 1-Lipschitz and that f is
jointly 1-Lipschitz. K need not have interior or be bounded; h may fold,
have flat intervals, or have derivative of magnitude one.

**Theorem.** Every map (1) has one simultaneous continuous contracting motion
in R5, with both endpoints in the original R3. The motion can be given C1
trajectories with uniformly bounded speeds on bounded source sets.

For every bounded Borel probability law mu on K x I, every Gaussian variance
s>0 and every threshold a>=0, it follows that

    integral_R3 (mu*gamma_s-a)_+
        <= integral_R3 ((T#mu)*gamma_s-a)_+,                  (2)

where gamma_s is the centered Gaussian density of covariance s I3. Thus
all defined convex internal energies with U(0)=0 compare in the majorisation
direction. For every finite labeled selection x_i in K x I and arbitrary
individual radii r_i>=0,

    volume union_i B(Tx_i,r_i) <= volume union_i B(x_i,r_i),
    volume intersection_i B(Tx_i,r_i)
        >= volume intersection_i B(x_i,r_i).                 (3)

The law, its weights, and its support require no symmetry. The hypotheses
are on a whole prism extension, not only on selected finite endpoint pairs.
Independent Euclidean endpoint frames are allowed by invariance of (2)-(3).
The coordinate-free premise is that one fixed target linear coordinate is
a function of one fixed source linear coordinate, with a convex product
domain perpendicular to that source direction.

This removes the transverse affinity requirement from accepted
[affine-slice6514](../gaussian_affine_slice_contractions/PROOF.md), whose
[independent acceptance6518](../gaussian_affine_slice_contractions_review/REVIEW.md)
is preserved. Section 2 replaces its affine-isometry completion with an
elementary partition argument. Section 4 then uses its existing motion,
which in turn uses R4's unfolded-height construction. The classical Gaussian
and ball transfers are unchanged.

## 2. A geometric estimate that does not differentiate f

Since h is 1-Lipschitz, it is absolutely continuous on compact subintervals
and |h'|<=1 almost everywhere. Fix z0 in I and define

    omega(z)=sqrt(1-h'(z)^2),
    A(z)=integral_(z0)^z omega(q) dq.                        (4)

These integrals are signed below z0; choices on the null set where h' is
undefined have no effect. The function A is continuous, nondecreasing,
and 1-Lipschitz. We prove the universal pair estimate

    |f(u,z)-f(v,w)|^2
        <= |u-v|^2+|A(z)-A(w)|^2.                            (5)

Assume w<z. Choose any finite partition
w=z_0<z_1<...<z_N=z of this interval, using the local indices only in this
paragraph, and put

    ell_i=sqrt((z_i-z_(i-1))^2-(h(z_i)-h(z_(i-1)))^2),
    L=sum_i ell_i.                                          (6)

Every radicand is nonnegative. If L>0, allocate the horizontal displacement
along the segment in K by

    u_i=v+(ell_1+...+ell_i)(u-v)/L,       u_0=v.              (7)

The whole-prism hypothesis permits applying the endpoint contraction (1)
to each pair (u_(i-1),z_(i-1)),(u_i,z_i). Subtract the squared height change:

    |f(u_i,z_i)-f(u_(i-1),z_(i-1))|^2
        <= |u_i-u_(i-1)|^2+ell_i^2
        = (ell_i/L)^2 (|u-v|^2+L^2).                        (8)

The triangle inequality and sum_i ell_i/L=1 imply

    |f(u,z)-f(v,w)| <= sqrt(|u-v|^2+L^2).                   (9)

This also handles zero individual ell_i without division by them. If L=0,
every vertical pair (u,z_(i-1)),(u,z_i) has identical f values, by the same
contraction inequality. First move horizontally from (v,w) to (u,w), at
cost at most |u-v|, and then vertically at zero f cost. This proves (9)
also when the total length vanishes.

Now take dyadic equal-length partitions of [w,z]. The piecewise constant
averages b_N of h' on their cells converge to h' almost everywhere by
Lebesgue differentiation. Since h is absolutely continuous, (6) becomes

    L_N=integral_w^z sqrt(1-b_N(q)^2) dq.

The integrands lie in [0,1]; dominated convergence gives

    L_N -> integral_w^z sqrt(1-h'(q)^2)dq=A(z)-A(w).          (10)

Indeed these lengths are nonincreasing under dyadic refinement by concavity
of t->sqrt(1-t^2). Passing to the limit in (9) proves (5). Equal heights
follow directly from (1), and reversed heights follow by symmetry.

Only the scalar function h was differentiated. No Jacobian, transverse
regularity, matrix inverse, isometric embedding, or exceptional-line
argument for f is needed. The same estimate holds with arbitrary Euclidean
dimensions for u and f; the dimension-three restriction enters the R5
application below.

## 3. Exact factorization through the unused axial length

The estimate has a useful converse. For a fixed 1-Lipschitz h and A given
by (4), maps (1) are nonexpansive exactly when there is a 1-Lipschitz map

    G:K x A(I) -> R2,       f(u,z)=G(u,A(z)).                (11)

**Necessity.** If A(z)=A(w), (5) with u=v makes f(u,z)=f(u,w). Hence G
is well defined even on flat intervals of A. For any two representatives,
(5) gives precisely its Euclidean 1-Lipschitz bound on K x A(I).

**Sufficiency.** The curve z->(A(z),h(z)) is absolutely continuous and has
speed sqrt(omega^2+h'^2)=1 almost everywhere. Thus for w<z,

    |A(z)-A(w)|^2+|h(z)-h(w)|^2 <= (z-w)^2.                (12)

Combine (12) with the assumed bound for G to obtain the contraction
inequality for T. This proves both directions, including the case where
A is constant. In that case f is independent of z. This factorization
characterizes the entire stated class; it is not a claim that an arbitrary
R3 contraction has a scalar output of the form h(z).

In particular, the hypotheses can be supplied constructively by choosing
any 1-Lipschitz h and any 1-Lipschitz planar-valued G on K x A(I). G may
depend nonlinearly on all three arguments. The Gaussian result below is
uniform over this whole family, including all folds and equality cases.

### 3.1. An exact finite-data application in prescribed frames

Suppose finitely many labeled endpoints are written in fixed source and
target frames as x_i=(u_i,z_i), y_i=(v_i,t_i), with u_i,v_i in R2.
There exists a global map of the form (1), with K=R2 and I=R, extending
all these assignments if and only if the following conditions hold.

1. Equal source heights have equal target heights. Write the distinct source
   levels as z_1<...<z_m and their prescribed target heights as t_1,...,t_m;
   let k(i) be the level of label i.
2. For every adjacent pair, |t_(k+1)-t_k|<=z_(k+1)-z_k. Set

       a_1=0,
       a_(k+1)-a_k=sqrt((z_(k+1)-z_k)^2-(t_(k+1)-t_k)^2).

3. For every pair of labels,

       |v_i-v_j|^2 <= |u_i-u_j|^2+(a_(k(i))-a_(k(j)))^2.   (F)

**Necessity.** The first two requirements follow from the scalar form and
shortness of h. For any extending h, concavity of sqrt(1-b^2) and Jensen's
inequality give, on each adjacent source-level interval,

    integral_(z_k)^(z_(k+1)) sqrt(1-h'^2)
        <= sqrt((z_(k+1)-z_k)^2-(t_(k+1)-t_k)^2).

Summing these nonnegative bounds and using (5) gives (F). This argument
also proves necessity for an extension on any whole convex prism containing
the prescribed sites and all their height levels.

**Sufficiency.** Let h be piecewise linear through (z_k,t_k) and constant
outside the extreme levels. It is 1-Lipschitz. With the primitive A anchored
at z_1, its values at the levels are exactly a_k. Condition (F) makes the
finite map (u_i,a_(k(i))) -> v_i 1-Lipschitz, including well-definedness when
two transformed sites coincide. By the classical Kirszbraun--Valentine
extension theorem it has a 1-Lipschitz extension G:R3->R2. One may apply
[Cavagnari--Savare--Sodini, Theorem 2.13, with the trivial group](https://arxiv.org/html/2305.04678v2)
in R3 after appending a zero output coordinate, then project back to R2.
Section 3 gives the required global T(u,z)=(G(u,A(z)),h(z)). If there is
only one source level, use constant h and a_1=0; the same proof applies.

Thus every finite configuration satisfying this criterion inherits all
weights, variances, thresholds, and individual-radius conclusions. The
criterion characterizes extension in the supplied frames, not existence of
an arbitrary R5 motion and not a search over possible frames. General real
inputs involve square roots; the accompanying rational checker verifies
certificates with supplied rational a_k, and makes no claim to implement a
decision procedure for arbitrary sums of algebraic radicals.

## 4. The inherited R5 motion

Work in coordinates (x,H,y) in R2 x R x R2. For 0<=t<=1 put

    q_t(z)=sqrt(1-t+t h'(z)^2),
    H_t(z)=(1-t)z0+t h(z0)+integral_(z0)^z q_t(s)ds,
    Phi_t(u,z)=(sqrt(1-t)u,H_t(z),sqrt(t)f(u,z)).            (13)

This is the first phase of the affine-slice motion, now justified for
arbitrary f by (5). Its unfolded height credits
[R4 cylindrical6492](../gaussian_cylindrical_twist_contractions/PROOF.md).

Fix z>w. For t<1 write

    L_t=integral_w^z q_t,
    C_t=integral_w^z omega^2/q_t,
    Q=|f(u,z)-f(v,w)|^2-|u-v|^2.

The squared pair distance in (13) is

    (1-t)|u-v|^2+t|f(u,z)-f(v,w)|^2+L_t^2.

On compact subintervals of t<1 the denominator q_t is bounded away from
zero, so differentiation under the integral gives L_t'=-C_t/2. By (5)
and Cauchy--Schwarz applied to sqrt(q_t) and omega/sqrt(q_t),

    derivative(pair square)=Q-L_t C_t
        <= (integral_w^z omega)^2-L_t C_t <= 0.             (14)

At equal heights, the transverse endpoint map is 1-Lipschitz and the same
conclusion is immediate. Continuity handles t=1, including sets where h'=0.
This is a simultaneous contraction of the whole prism, with endpoints

    Phi_0(u,z)=(u,z,0),
    Phi_1(u,z)=(0,H_1(z),f(u,z)),
    H_1(z)=h(z0)+integral_(z0)^z |h'(s)|ds.                 (15)

Rotate the two transverse R2 planes by a common quarter turn. This is an
ambient isometry and ends at (f(u,z),H_1(z),0). Since

    |h(z)-h(w)| <= |H_1(z)-H_1(w)|,

there is a well-defined 1-Lipschitz g on H_1(I) with g(H_1(z))=h(z).
A flat interval of H_1 forces h to be constant there. With the transverse
coordinate v fixed, use the classical one-dimensional leapfrog

    (v,x,0,0) ->
    (v,(1-s)x+s g(x),sqrt(s(1-s))(x-g(x)),0).                (16)

Its squared axial-plus-auxiliary pair distance equals
(1-s)(x-y)^2+s(g(x)-g(y))^2, and hence decreases. The endpoint is
(f(u,z),h(z),0,0). Concatenate these three phases in the same R5.

For clarity, all three phases are jointly continuous in time and labels.
They are uniformly bounded on bounded source sets. The zero sets of omega
and h' cause no inverse-function or choice-of-representative problem.

The time regularity can be made C1, even though f and h need not be smooth.
In (13) use t=sin(theta)^2, 0<=theta<=pi/2. Then

    q(theta,z)=sqrt(cos(theta)^2+sin(theta)^2 h'(z)^2),
    partial_theta q
      =-sin(theta)cos(theta)(1-h'^2)/q,
    |partial_theta q|<=1                                  (17)

in the interior. At theta=0 this derivative tends to zero; as theta tends
to pi/2 it tends to -1 where h'=0 and to zero elsewhere. Dominated
convergence therefore gives continuous one-sided derivatives for H and
for every labeled trajectory through the phase endpoints. Their speeds
are uniformly bounded on bounded source sets. The other phases have
bounded one-sided derivatives after the analogous sine-square clock for
(16). Apply a smooth increasing clock with derivative zero at both ends
of each phase, for example 3r^2-2r^3 after normalizing its parameter. The
concatenated motion then has C1 trajectories. Each phase is also C-infinity
on its open time interval: for the first phase, every parameter derivative
of q is bounded on compact interior time intervals because q is bounded
away from zero, permitting repeated differentiation under the integral.
The other phases are elementary smooth expressions in time. Thus the
motion meets the piecewise-smooth definition in Bezdek--Connelly as well
as the continuous-motion hypothesis in Aishwarya--Li. No truncation at
lifted endpoints outside R3 is required.

## 5. Gaussian and ball-volume consequences

[Aishwarya--Li, 2609.07041v2,Theorem 1.4(i)(a)](https://arxiv.org/html/2609.07041v2)
applies to this continuous R5 contraction. The two endpoint densities are
f0(x)gamma_(2,s)(y) and f1(x)gamma_(2,s)(y). If Y has density gamma_(2,s),
then gamma_(2,s)(Y)/c is uniform on [0,1], with c=(2pi s)^(-1). Therefore,
for X of density f_j independent of Y,

    Pr{f_j(X)gamma_(2,s)(Y)>ca}=integral(f_j-a)_+.

The cited increasing coupling of sampled density values proves (2). This
two-Gaussian-coordinate cancellation and the sufficiency of two auxiliary
dimensions are established inputs, explicitly discussed after Theorem 1.5
of that paper. The usual hinge representation gives the convex energies.
If a bounded support meets a finite excluded endpoint of I, the 1-Lipschitz
map extends continuously to the closure of the prism and preserves the
form (1); apply the same argument there.

Reverse the finite piecewise-smooth motion and apply
[Bezdek--Connelly, math/0108098v1,Theorem 1](https://arxiv.org/pdf/math/0108098v1)
to obtain both inequalities in (3). For coincident targets, use
T_epsilon=(1-epsilon)T+epsilon Id. It is 1-Lipschitz and retains(1), with
f_epsilon=(1-epsilon)f+epsilon u and h_epsilon=(1-epsilon)h+epsilon z.
For finitely many distinct source labels, each target pair coincides for
at most one epsilon, so a sequence decreasing to zero avoids all collisions.
Nonincreasing pair distances and distinct final centers give distinct
intermediate centers. Apply the theorem and then pass to the limit by
continuity of finite ball volumes in their centers. Repeated source
centers may be merged, retaining the largest radius for unions and the
smallest for intersections. Zero radii follow by a radius limit.

## 6. A nonlinear full-prism control and the extent of the enlargement

On K=[-1,1]^2,I=[-1,1] take

    h(z)=-3z/5 for z<=0,       h(z)=5z/13 for z>=0;
    A(z)=4z/5 for z<=0,        A(z)=12z/13 for z>=0.

For v=(v1,v2,v3) in [-1,1]^3 define

    G(v)=((v1^2+v2^2+v3^2)/8,
          (v1v2+v1v3+v2v3)/8),
    f(u,z)=G(u1,u2,A(z)).                                  (18)

The squared Jacobian Frobenius norm of G is at most 3/8: the first row has
three entries of magnitude at most 1/4, and so does the second. Thus G
is 1-Lipschitz on the entire cube. Since A(I) lies in [-1,1], Section 3 proves
that T=(f,h) is 1-Lipschitz on the whole input cube. Alternatively its
piecewise Jacobian Frobenius square is at most 3/8+9/25=147/200<1.

This map is not affine on parallel source planes in any independent fixed
endpoint frames. On each open height half, its first scalar component has
positive-definite Hessian diag(1/4,1/4,c^2/4), with c=4/5 or 12/13. It is
therefore strictly convex along every nonconstant local line. A vector map
affine on a two-dimensional plane would make every scalar component affine
on each line in that plane, a contradiction. Endpoint isometries do not
alter this implication. Thus the new theorem genuinely removes the former
affinity premise, even after reframing. This control is illustrative; the
whole nonlinear function class, not a particular polynomial or coefficient,
is the result. No exclusion of all compositions or all other positive
mechanisms is claimed for this example.

The full-map example is also outside coordinatewise strong contraction in
any fixed endpoint frames. The notion and its existing ball-volume theorem
are from [Bezdek--Naszodi, Theorem 1.3](https://real.mtak.hu/100302/7/1701.05074.pdf).
On an open three-dimensional domain, a strong contraction makes each output
coordinate depend only on the corresponding input coordinate; a smooth
scalar component therefore has Hessian rank at most one. On either open
height half in (18), write D=diag(1,1,c). The Hessian of a scalar combination
alpha f_1+beta f_2+delta h is

    D [((2alpha-beta)/8) I + (beta/8) J] D,

where J is the all-ones matrix. The middle matrix has eigenvalues
(2alpha-beta)/8 twice and (alpha+beta)/4 once. Its rank is at most one
exactly when beta=2alpha. Three independent output coordinate functionals
cannot all lie in that two-dimensional coefficient plane. Input isometries
preserve Hessian rank, proving the assertion even with independent endpoint
frames. This separates the stated function classes; it does not establish
historical priority or exclude compositions of old positive mechanisms.

The prism condition remains material. On two source sites (0,-1),(0,1),
the assignments f(0,-1)=(-1,0), f(0,1)=(1,0), and both target heights 1
are a contraction. They cannot extend to (1) with h(z)=|z| on [-1,1]: then
omega=0 almost everywhere and (5) forces f(0,z) to be constant. This simple
control explains which premise a finite-only test omits; it is not a new
obstruction to general contracting motions.

The [meridian and normal portfolio](../gaussian_geometric_portfolio/CLASSIFICATION.md)
remains complementary: general meridian maps may make target height depend
on transverse radius. R4's [sharp screw/meridian boundary6530](../gaussian_screw_meridian_boundary/PROOF.md)
concerns full rotational extensions of rigid finite groups, a different
premise. R7's [composition obstruction6524](../gaussian_screw_primitive_obstruction/PROOF.md)
still prevents all known R5-motion and anchored-norm steps from generating
every finite contraction. The present theorem supplies a broader positive
R5 class; it makes no unrestricted factorization or adversarial-sign claim.

## 7. Evidence and priority boundary

[verify.py](verify.py) uses only exact rational arithmetic and exact signs of
quadratic surds. It checks the partition allocation on nonlinear data, the
transverse estimate, the first-phase derivative and axial fold, flat-height
and unit-slope profiles, and deliberately invalid shortcuts. The fixture's
global derivative bound and the universal partition argument are
written mathematics, not conclusions from a sampled grid. No numerical
quadrature, nonlinear solver, ODE integration, external dataset, or omitted
large certificate is used.

[SOURCES.md](SOURCES.md) and [INPUTS.json](INPUTS.json) give dependencies and
source pins. The new input is (5), its exact factorization, and the consequent
removal of transverse affinity. The leapfrog framework, unfolded height,
R5 interpolation, Gaussian cancellation, and ball transfer are credited
antecedents. Historical priority for this full nonlinear class has not been
established by the bounded primary-source comparison. The theorem is an
author proof pending independent review, not a solution of the full problem.
