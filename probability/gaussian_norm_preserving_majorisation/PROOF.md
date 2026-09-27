# All-variance Gaussian majorisation for norm-preserving contractions

Complete author argument, 27 September 2026. Independent review of these
consequences is pending. The imported R1 spherical-mean identity has
independent campaign acceptance at graph6506. The unrestricted
bounded-law dimension-three problem remains open. Historical priority of
the consequences below is not asserted.

The new functional step is to apply R1's positive operator difference to
**supermodular functions without affine equivariance**. Equal distances to
an anchor remove the diagonal Hessian terms. This signs every Gaussian
hinge at each spatial radius, at every variance, and has direct union and
intersection Kneser--Poulsen consequences. It does not pass through an
entropy bound, a large-variance limit, or a contracting-motion hypothesis.

## 1. Statements

Let S be a bounded subset of R3 and let T:S -> R3 satisfy

    |T(x)-T(x')| <= |x-x'|                       (x,x' in S).

Assume there are anchors a,b in R3 such that

    |T(x)-b| = |x-a|                            (x in S).       (1)

The anchors need not be means or points of S. A map given only on S is
sufficient. When needed, it extends to the closure by continuity. Translate
by a and b independently, and write p=x-a, q=T(x)-b. Thus |p|=|q|.

**Theorem A (radial conditional convex order).** Let mu be any probability
measure supported on S, nu=T#mu, s>0, and

    gamma_s(z)=(2 pi s)^(-3/2) exp(-|z|^2/(2s)),
    f=mu*gamma_s,              g=nu*gamma_s.

For every rho>=0, if theta is uniform on S2, then

    E U(f(a+rho theta)) <= E U(g(b+rho theta))                 (2)

for every continuous convex U on [0,(2 pi s)^(-3/2)]. Their angular means
are equal. In particular the assertion includes all hinge functions.

**Theorem B (full Gaussian majorisation in this class).** Under the same
hypotheses, simultaneously for every s>0 and every h>=0,

    integral_R3 (f(z)-h)_+ dz <= integral_R3 (g(z)-h)_+ dz.     (3)

Both densities have integral one, so this is precisely f majorised by g.
There is no support-cardinality, weight, covariance, loss-size, or variance
restriction in (3). The exact anchor condition (1) is material.

**Theorem C (arbitrary-radius Euclidean ball volumes).** Let p_i,q_i in R3,
1<=i<=N, satisfy |p_i|=|q_i| and |q_i-q_j|<=|p_i-p_j|. For every list
r_i>=0,

    Vol union_i B(p_i,r_i) >= Vol union_i B(q_i,r_i),
    Vol intersection_i B(p_i,r_i) <= Vol intersection_i B(q_i,r_i). (4)

The same conclusion permits independent translations of the two lists.

**Theorem D (arbitrary spherical caps in S2).** Let u_i,v_i be unit vectors
in R3 and suppose their geodesic distances on S2 satisfy
d(v_i,v_j)<=d(u_i,u_j). For any radii alpha_i in [0,pi], the areas of the
closed spherical caps C(u_i,alpha_i) obey

    Area union_i C(u_i,alpha_i) >= Area union_i C(v_i,alpha_i),
    Area intersection_i C(u_i,alpha_i)
                         <= Area intersection_i C(v_i,alpha_i). (5)

There is no connectivity or hemisphere restriction in (5). This is a
substantial claimed consequence requiring independent scrutiny: the
primary sources discussed in SOURCES.md prove restricted spherical cases.
The proof of (5) is given directly below; it is not inferred from a
Euclidean volume comparison or from Gaussian majorisation.

## 2. Imported positive spherical-mean difference

Write sigma for probability area on S2. For N-by-3 matrices P,Q with rows
p_i,q_i and phi in C2(R^N), set

    M_P(t) phi(c) = integral_S2 phi(c+t P theta) d sigma(theta),
    Delta_P = sum_(a=1)^3 (sum_i p_ia partial_i)^2.

R1, graph6494, [Lemma 1](../gaussian_spherical_sinc_comparison/PROOF.md),
proves the exact identity

    M_P(t)phi(c)-M_Q(t)phi(c)
      = (1/t) integral_0^t r(t-r)
          M_P(t-r) M_Q(r) (Delta_P-Delta_Q)phi(c) dr,   t>0.  (6)

The spheres in the two averaging operators are independent. Both operators
preserve pointwise nonnegativity; the weight r(t-r)/t is nonnegative. No
intermediate Gram matrix is required to have rank at most three.

For clarity, the algebra behind the imported result is

    M_P(t)=sum_k t^(2k) Delta_P^k/(2k+1)!

on polynomials. Substitution into (6) gives the coefficient
t^(2i+2j+2)/(2i+2j+3)! for Delta_P^i Delta_Q^j(Delta_P-Delta_Q).
Commutation and (A-B) sum_(i+j=k-1) A^i B^j=A^k-B^k telescope it.
This is a finite calculation on each polynomial. Approximation of phi and
its derivatives through order two on the compact set of arguments extends
the equality to C2. This recollection credits R1's proof, not a separate
new evolution argument or independent acceptance of that contribution.

## 3. Removing the diagonal terms

Put

    K_ij=p_i.p_j-q_i.q_j,
    delta_ij=|p_i-p_j|^2-|q_i-q_j|^2 >= 0.

Equal norms give K_ii=0, and polarization gives K_ij=-delta_ij/2. Therefore

    (Delta_P-Delta_Q)phi
       = sum_(i,j) K_ij phi_ij
       = -sum_(i<j) delta_ij phi_ij.                        (7)

A C2 function with phi_ij>=0 for every i!=j is called supermodular here.
Equations (6)--(7) imply, for every c and t>=0,

    M_P(t)phi(c) <= M_Q(t)phi(c)       if phi_ij>=0 (i!=j),  (8)

with the reverse inequality if all these mixed derivatives are <=0.
There is no condition on the diagonal derivatives or on the sign of the
first derivatives. No affine-equivariance condition is imposed.

This differs from R1's use of log-sum-exp: there, zero Hessian row sums
remove diagonal Gram losses for arbitrary contractions. Here, equal norms
remove those losses for arbitrary supermodular test functions. In
particular, convex functions of sums of exponentials become admissible.

## 4. Gaussian hinges at each radius

First take mu=sum_i w_i delta_(a+p_i), with w_i>0 and sum_i w_i=1. Fix
s>0 and rho>=0 and define

    A=(2 pi s)^(-3/2) exp(-rho^2/(2s)),
    c_i=log(w_i)-|p_i|^2/(2s),          t=rho/s,
    F(z)=A sum_i exp(z_i),             phi(z)=U(F(z)).       (9)

The same offsets c_i work at the target because |p_i|=|q_i|. Thus

    f(a+rho theta)=F(c+t P theta),
    g(b+rho theta)=F(c+t Q theta).

If U is C2 and convex on the relevant positive range, then for i!=j,

    phi_ij(z)=U''(F(z)) A^2 exp(z_i+z_j) >= 0.             (10)

Extend U convexly and smoothly if necessary beyond that compact range.
Apply (8) to obtain (2). At rho=0 the two values are identical directly.
For any continuous convex U on the density range, first approximate it
uniformly by convex piecewise-linear interpolants. Extend each interpolant
affinely at both ends and mollify on the real line. This gives uniform
convex smooth approximation on the density interval even when U has an
infinite one-sided derivative at an endpoint. No derivative convergence is
required: pass to the limit in the angular expectations. This also covers
hinges U(v)=(v-h)_+.

More explicitly, for a smooth convex U and rho>0, the exact nonnegative
difference is

    E U(g(b+rho theta))-E U(f(a+rho theta))
      = t^2 integral_0^1 u(1-u) E_(theta,eta)
           sum_(i<j) delta_ij U''(F(z)) v_i(z) v_j(z) du,   (11)
    z_i=c_i+t[(1-u) theta.p_i+u eta.q_i],
    v_i(z)=A exp(z_i).

Every factor in each summand has the displayed sign. Unlike a moment or
entropy comparison, (11) permits every smooth approximation of a hinge.
Pass to the hinge limit at fixed rho before integrating in rho; this
avoids integrating a smoothing error over infinite Euclidean volume.

The angular means are equal because theta.p_i and theta.q_i have the same
one-dimensional distribution for each i. Alternatively apply (8) to both
U(v)=v and U(v)=-v; their off-diagonal derivatives in (10) are zero.

For a general bounded law, choose finite approximations supported on its
original support, with atoms mapped by the original T. Both the short-map
and norm equalities hold exactly on every approximation. Partition the
compact support into sets of diameter tending to zero and choose one
representative of each positive-mass set. The resulting densities converge
uniformly, since gamma_s is globally Lipschitz and T is 1-Lipschitz.
The finite angular comparisons therefore pass to (2) at every fixed rho.
This construction imposes neither a weight floor nor a finite atom budget.

Finally take U(v)=(v-h)_+ in (2). Multiply by 4 pi rho^2 and integrate from
zero to infinity. Polar coordinates and Tonelli give (3). Each integral is
at most one. At h=0 both equal one; above the common Gaussian peak both are
zero. This proves Theorems A and B.

## 5. Spherical caps and Euclidean balls

Let chi_epsilon:R->[0,1] be a smooth nondecreasing function equal to zero
on (-infinity,-epsilon] and to one on [epsilon,infinity). Define

    I_epsilon(z)=product_i chi_epsilon(z_i),
    O_epsilon(z)=1-product_i (1-chi_epsilon(z_i)).

For i!=j their mixed derivatives are

    (I_epsilon)_ij = chi'_epsilon(z_i) chi'_epsilon(z_j)
                       product_(k!=i,j) chi_epsilon(z_k) >= 0,
    (O_epsilon)_ij = -chi'_epsilon(z_i) chi'_epsilon(z_j)
                       product_(k!=i,j) (1-chi_epsilon(z_k)) <= 0. (12)

Empty products are one; the one-ball case is immediate.

For Theorem D, geodesic contraction on unit S2 is equivalent to
u_i.u_j<=v_i.v_j, hence to Euclidean chord contraction. Use (8) with P=(u_i),
Q=(v_i), t=1, and c_i=-cos(alpha_i). The tests above converge almost
everywhere on S2 to the indicators of intersection and union of the caps,
respectively. Each individual boundary {theta:theta.u_i=cos(alpha_i)}
has area zero, including the degenerate radii zero and pi. Bounded
convergence proves (5).

For Theorem C, fix rho>0 and use

    c_i=r_i^2-|p_i|^2-rho^2,          t=2 rho.              (13)

Again the offsets agree at both endpoints. Now

    c_i+t theta.p_i = r_i^2-|rho theta-p_i|^2,

so (8) and (12) compare the smoothed intersection and union indicators on
each sphere of radius rho. Integrate with 4 pi rho^2. For 0<epsilon<=1,
all these indicators vanish outside a fixed ball containing every
B(p_i,sqrt(r_i^2+1)) and B(q_i,sqrt(r_i^2+1)). They are bounded by one.
Euclidean ball boundaries have volume zero, including radius zero.
Dominated convergence proves (4). This proof needs no generic-position,
nondegeneracy, boundary-transversality, or contracting-motion assumption.

## 6. Scope, certificate interface, and the remaining target

For rational finite data and supplied rational anchors, (1), all pairwise
contractions, and the probability-vector conditions are exact rational
checks. The optional input mode of verify.py implements precisely this
sufficient guard. It can hand R2 a whole all-variance certificate, including
configurations with paired affine rank six and zero-loss pairs. A failure
of the guard is not a negative hinge and does not decide any other class.

The anchor condition is invariant under independent endpoint isometries.
It must be tested **before any unrelated mean centering**: independently
centering at the two probability means generally destroys (1). If both
anchors actually are the two means, norm preservation forces equal scatter,
and a contraction is an isometry on the support; that special situation is
not the general class proved here.

This is an all-threshold sign for an entire geometric class, at arbitrary
fixed variance. It does not assert that every short map has suitable
anchors, that a finite cubature preserves (1), or that arbitrary endpoint
errors can be absorbed uniformly at zero loss. R3's earlier effective
cutoff and R8's midpoint support remain consolidated and unchanged.
R2's balanced-loss straight-motion guard is complementary: it assumes a
positive minimum pair loss when its Gram defect is nonzero, whereas this
guard allows many zero-loss pairs. No noninclusion from every historical
motion class is claimed for any calibration example.

R1's source is an essential analytic dependency; its independent review6506
accepts (6). The present consequences have not yet been independently
accepted. The exact checker only
verifies rational hypotheses, ranks, and finite mixed-derivative algebra;
it does not formalize the spherical operator identity, smooth approximation,
measure limits, or polar integration. The general non-norm-preserving,
all-variance bounded-law R3 Gaussian-majorisation question remains open.
