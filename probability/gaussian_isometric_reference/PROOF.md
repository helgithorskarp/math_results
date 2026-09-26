# Isometric reference sets and exact zero minimizers

Complete author proof, 26 September 2026; independent mathematical review
and formalization are pending. This is a signed boundary result for the
common-set formulation of Gaussian majorisation. It applies to every
contraction in every finite dimension, but only to the reference sets
specified below. The full dimension-three question remains open.

## 1. Statement

Let n>=1, let K be a nonempty compact subset of R^n, let T:K -> R^n be 1-Lipschitz,
and fix s>0. Write gamma_s for the Gaussian density with covariance s I_n.
For a probability law mu on K set

    f_mu = mu * gamma_s,       g_mu = (T#mu) * gamma_s,
    C_p(v) = sup_(|E|=v) integral_E p,           0<v<infinity.

Let sigma be a reference probability law on K, and suppose that an affine
Euclidean isometry S agrees with T on supp(sigma). Choose

    0<h<max f_sigma,     A={f_sigma>h},     v=|A|,     B=S A,
    Psi_A(x)=integral_A gamma_s(z-x) dz,
    q(x)=integral_B gamma_s(z-Tx) dz-Psi_A(x),
    J_A(mu)=C_(g_mu)(v)-integral_A f_mu.

All sets are Lebesgue measurable and equalities between sets are understood
up to null sets when optimizing their volume. No finiteness of the support
of either law, density for the laws, or extension of T outside K is assumed.

**Theorem.** The following conclusions hold.

1. For every x in K, q(x)>=0. Moreover,

       q(x)=0  iff  |Tx-Tc|=|x-c| for every c in supp(sigma).    (1)

2. For every probability law mu on K,

       J_A(mu) >= integral_K q dmu >= 0.                       (2)

   The minimum is zero, attained at mu=sigma. Its minimizers are exactly
   the laws mu for which both of the following conditions hold:

   (a) T agrees with one affine Euclidean isometry on
       supp(sigma) union supp(mu);
   (b) A is a maximizing set of volume v for f_mu.

   In particular, J_A(mu)>0 if T fails to preserve all pair distances on
   supp(mu), even when q vanishes on that entire support.

3. B is the unique common-set dual maximizer. More explicitly, with

       q_D(x)=integral_D gamma_s(z-Tx) dz-Psi_A(x),

   one has

       max_(|D|=v) min_(x in K) q_D(x)=0,                      (3)

   and equality in (3) is attained only by D=B up to a null set.

The same statements give tests at every prescribed finite positive volume:
the Gaussian level-volume function selects a unique h for each v. If the
allowed priors are further restricted but still include sigma, their
minimum in (2) remains zero and the minimizer classification is simply
intersected with those restrictions. This observation includes a prescribed
atom mass when the reference law has that mass; it does not change the law.

## 2. Basic properties and normalization

A compactly supported Gaussian mixture p is positive, real analytic,
nonconstant, and tends to zero at infinity. Its positive level sets are
null: p-h is a nonzero real analytic function. Its positive superlevel
sets are bounded. Consequently |{p>h}| is continuous and strictly decreasing
from infinity to zero as h goes from zero to max p. Strict decrease follows
because every intermediate density interval has a nonempty open inverse
image. These facts justify the assertion about v and h.

For |E|=|{p>h}|, subtract h times the two volumes to obtain

    integral_{p>h} p-integral_E p
      = integral (1_{p>h}-1_E)(p-h) >= 0.                      (4)

Equality forces E={p>h} up to the null level set. This proves existence
and uniqueness of each Gaussian maximizing set used below.

Pull the target coordinates back by S. Then T becomes S^(-1)T, fixes
supp(sigma) pointwise, and B becomes A. This changes neither the distances
in (1), the value of q, nor C_(g_mu). Subsequently translate source and
target by the same reference point c_0 in supp(sigma). We may thus suppose
throughout the proof that S=Id, c_0=0 and T fixes supp(sigma).

## 3. Affine-bisector polarization, including strictness

Fix x in K and put a=x, b=Tx. The assertion is immediate if a=b. Otherwise
let H be the open halfspace of points nearer b than a, and let R be the
affine reflection in its boundary. Thus R exchanges a and b. Contraction
and Tc=c imply

    |b-c|<=|a-c| for every c in supp(sigma),

so every reference center is in the closure of H. For z in H and each
such center, gamma_s(z-c)>=gamma_s(Rz-c). Integrating gives

    f_sigma(z)>=f_sigma(Rz),       1_A(z)>=1_A(Rz),  z in H.   (5)

Reflection pairing, whose Jacobian has absolute value one, now gives

    Psi_A(b)-Psi_A(a)
      = integral_H [1_A(z)-1_A(Rz)]
                    [gamma_s(z-b)-gamma_s(z-a)] dz >= 0.     (6)

This proves the transfer. It is the classical two-point polarization
argument, now with an affine bisector determined by the endpoint pair.

If all the center distances agree, supp(sigma) lies on the bisector, so
f_sigma and A are invariant under R and (6) is zero. Conversely, if a
reference center is strictly nearer b, the definition of support and
continuity give positive sigma mass in H. Every reference center remains
in its closure. Hence

    f_sigma(z)>f_sigma(Rz) for every z in H.                  (7)

Let e be the unit normal pointing into H. On its boundary, differentiation
of the Gaussian mixture shows that D_e f_sigma>0: in the integral the
normal displacement of every center is nonnegative and is positive on
a set of positive sigma mass. Every global maximizer of f_sigma therefore
lies in H. A point on the boundary can be improved in direction e, and a
point in the opposite halfspace can be improved by reflection.

Start at a global maximizer z_0 in H and follow z_0+t e, t>=0. The density
tends to zero, so for the given h it has a first crossing t_0>0. At the
crossing its value is h and the reflected value is strictly less than h
by (7). Just before the crossing, and on a nonempty open neighborhood,

    f_sigma(z)>h>f_sigma(Rz).

The first factor in (6) is one there and the second is strictly positive.
Thus q(x)>0. This proves both directions of (1) at every nontrivial level,
without a regular-value or smooth-boundary hypothesis.

Integrating (6) against mu and using the admissible competitor B proves
(2). For sigma, T is isometric and (4) gives J_A(sigma)=0.

## 4. A strictly positive transverse weight

Let U be the linear span of supp(sigma), and let V=U-perp, with m=dim V.
Suppose for now that m>=1. Write points as (u,w) in U plus V. The reference
density factors as

    f_sigma(u,w)=p_U(u) gamma_s^V(w),                         (8)

where p_U is the Gaussian mixture of sigma in U. Thus each nonempty section
A_u is an open ball in V centered at zero, of some finite radius R(u)>0.
The set of u with positive radius is nonempty and open in U. If U={0},
integration on U below means evaluation at its single point.

We claim that Psi_A has a continuous coefficient alpha(u,r)>0 such that

    grad_V Psi_A(u,w)=-alpha(u,|w|)w,       alpha<=2/s.        (9)

Here is an elementary proof, including the value at r=0. For R>0 let

    F_R(w)=integral_{|z|<R} gamma_s^V(z-w) dz.

This is radial. For a unit e in V, boundary integration and pairing z with
its reflection in e-perp give, for r>0,

    -d/dr F_R(r e)
      = integral_{|z|=R, z.e>0} (z.e)/R
          [gamma_s^V(z-r e)-gamma_s^V(z+r e)] dS(z) > 0.     (10)

Set a_R(r)=-(d/dr F_R(r e))/r. Its positive continuous extension at zero is

    a_R(0)=2/(Rs) integral_{|z|=R, z.e>0}
                        (z.e)^2 gamma_s^V(z) dS(z)>0.       (11)

The formulas hold also for m=1, with counting surface measure on the two
endpoints. Define F_0=a_0=0 for empty sections. Since F_R'(0)=0 and

    |F_R''(t)|<=||partial_ee gamma_s^V||_1<=2/s,

the mean value formula bounds 0<=a_R(r)<=2/s for all R,r, including zero.
Convolve these ball sections in the U coordinates to get

    alpha(u,r)=integral_U gamma_s^U(u'-u) a_{R(u')}(r) du'.   (12)

The bound just obtained justifies differentiation and dominated convergence,
including r=0. It proves continuity and the upper bound in (9).
Positive-radius sections and the positive Gaussian kernel prove strict
positivity everywhere. Rotational invariance of every section then proves
(9). No convexity or connectedness of A in the U coordinates is used.

## 5. Translation stationarity forces joint isometry

Suppose J_A(mu)=0. Equation (2), nonnegativity of q and its continuity imply
q=0 on supp(mu). Also A is a maximizing set of volume v for g_mu, since
both inequalities in (2) must be equalities.

By (1), for x in supp(mu) all its distances to the reference centers are
preserved. The reference includes zero, so |Tx|=|x|; subtracting squared
distances to c and to zero gives (Tx-x).c=0. Therefore

    x=(u,w),       Tx=(u,z),       |w|=|z|                    (13)

on supp(mu). If V={0}, this already says Tx=x there and the conclusion
follows. Otherwise use (9).

Translating an optimal volume-v set cannot increase its integral. Hence
the smooth function t -> integral_{A+t e} g_mu has derivative zero at
t=0 for every e in V. Differentiation under the integral is legitimate
because A and supp(mu) are bounded and Gaussian derivatives are continuous.
Fubini and (9) turn this stationarity into

    0=integral_A grad_V g_mu
     =-integral_K grad_V Psi_A(Tx) dmu(x)
     = integral_K alpha(u,|z|)z dmu(x).                      (14)

The same positive weight a(x)=alpha(u,|w|)=alpha(u,|z|) applies at both
endpoints of every label. Normalize a dmu to a probability law mu_hat.
This law has exactly the same support as mu, by continuity and positivity
of a. Equation (14) says E_(mu_hat) z=0.

For any two supported labels x=(u,w), x'=(u',w'), contraction and (13) give

    d(x,x')=|x-x'|^2-|Tx-Tx'|^2
           =2(z.z'-w.w') >= 0.                              (15)

Average independently with respect to mu_hat at the two labels. Then

    0<=E d=2(|E z|^2-|E w|^2)=-2|E w|^2<=0.                (16)

Thus d=0 almost everywhere for mu_hat times mu_hat. Its nonnegativity and
continuity imply d=0 on supp(mu) times supp(mu). All distances within the
actual support are preserved. All distances between that support and the
reference support were already preserved, and T fixes the reference.
T is therefore distance preserving on their union.

For completeness this partial isometry extends to an ambient orthogonal
map Q. The union contains zero, and its Gram products are recovered from
norms and pair distances. Sending a finite spanning set to its images
therefore defines a well-defined linear isometry of the two spans; every
other supported vector has the same image by its Gram products. Complete
orthonormal bases to extend it to R^n. Since Q fixes the reference support,
it fixes U pointwise and maps V orthogonally to itself. In particular it
preserves A, by (8). Since g_mu(z)=f_mu(Q^(-1)z), optimality of A for g_mu
is now equivalent to optimality of A for f_mu. This proves (a) and (b).

Conversely, suppose (a) and (b). In the normalized coordinates the common
isometry fixes every reference point and zero. Its orthogonal part fixes
U and preserves A. The change of variables just used shows J_A(mu)=0.
Undoing the normalization proves the exact stated equivalence.

## 6. The unique dual set

For any measurable D with |D|=v, averaging q_D against sigma gives

    min_K q_D <= integral_K q_D dsigma
               =integral_D g_sigma-integral_A f_sigma<=0.   (17)

The last inequality is (4) and the reference isometry. Our B attains zero
by (1)--(2). If another D attains zero, equality must hold in (17), so D
is a maximizing volume-v set for g_sigma. Its unique such set is S A,
again by (4). This proves (3) without invoking a minimax interchange.

## 7. Why pointwise equality is insufficient

An elementary control isolates the role of stationarity. Take

    K={0,e_1,-e_1},    T0=0,    Te_1=T(-e_1)=e_1,
    sigma=delta_0,     mu=(delta_(e_1)+delta_(-e_1))/2.

This is a contraction, and A is a centered ball of radius R>0. All reference
distances are preserved, so q=0 on every point of K. Nevertheless

    J_A(mu)=F_R(0)-F_R(e_1)>0

by (10). The reference ball is not optimal for the translated target
Gaussian. Pointwise reference slack alone cannot classify zero minimizers;
the translation condition (14) supplies the missing requirement.

## 8. Dependency boundary for the full question

The measure lane's common-set theorem identifies full majorisation with
m(A)>=0 for **every** finite-volume source set A, every compact K, every
contraction T and every s>0. This note evaluates m(A) and its entire
minimizer set for isometric-reference superlevel sets. In particular a
negative common-set witness cannot use such an A. No assertion that
arbitrary source sets have this form, or are positive combinations of
such tests, has been proved.

The construction extends the finite lane's dual-cone transfer without
enumerating its faces: contraction plus an isometric reference support
is the whole geometric hypothesis. Equations (14)--(16) further control
degenerate zero-slack supports. They do not give a uniform sign neighborhood,
a finite degree at equality, or atomic minimizers of a general common-set
problem. Applying them under an externally fixed atom mass requires the
reference law itself to obey that constraint.

There is a direct boundary condition for the map lane's new indecomposable
reduction, whose finite maps fix a nondegenerate tetrahedron. Choose sigma
with positive mass at each of its four fixed vertices. Then U=R^3, so (1)
and (13) give q(x)=0 exactly when Tx=x. The reference test is strictly
positive for every actual prior assigning positive mass to moved points.
This does not control that prior's own maximizing source set unless it
coincides with A. It therefore supplies a common-set control on the reduced
full-question class, without adding a geometric sign or factorization claim.

The weighted zero-distortion step is elementary Euclidean rigidity, also
used by the earlier entropy-rigidity work. No entropy deficit estimate is
used, and that work's unsigned implication is not promoted to a hinge
comparison. This test-dependent construction is not a prior-independent
Markov kernel. It leaves the heat-contact sign and the general endpoint
coupling problem open. No new Kneser--Poulsen class follows from this note.

The proof is analytic. No numerical integration, solver, generated instance,
or external computational certificate is a premise. The classical ingredients,
the previously known ball case, and the exact team sources are credited in
[SOURCES.md](SOURCES.md). Source hashes check integrity only.
