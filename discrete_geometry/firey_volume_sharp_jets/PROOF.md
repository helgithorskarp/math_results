# Firey translation volumes and the sharp facet-dependent jet order

2026-09-22. An analytic proof with exact finite corroboration; unformalized.
See [SOURCES.md](SOURCES.md) for attribution and the limits of the literature
search. The planar result is prior work. The result below extends the volume
transform and inverse theorem to every dimension and gives the optimal
dimension-dependent jet order.

## Statement and conventions

Let d >= 2 and let C = -C be a compact convex body with nonempty interior in
R^d. Its center is the designated origin. Write h_C for its support function,
S_C for its ordinary surface area measure, and |C| for d-dimensional volume.
Firey addition at exponent two means h_(K+_2 L)^2 = h_K^2 + h_L^2, for
bodies containing zero. For x in int C put

    F_C(x) = |(C+x) +_2 (C-x)|,
    G_C(x) = 2^(-d/2) F_C(x) = |C +_2 [-x,x]|.                 (1)

The last expression extends G_C to all real x. Indeed the support functions
in (1) are related by a factor sqrt(2). Taylor terms below are homogeneous
polynomials, with factorials already divided out, in fixed coordinates.

**Theorem.**

1. Define the even analytic kernel

       Phi_d(t) = (1+t^2)^((2-d)/2)
                  + (d-1)t integral_0^t (1+s^2)^(-d/2) ds.    (2)

   For every real x and every such C, including nonsmooth bodies,

       G_C(x) = (1/d) integral h_C(n) Phi_d(x.n/h_C(n)) dS_C(n). (3)

2. Push the positive measure h_C dS_C forward by n -> n/h_C(n), obtaining
   an even measure nu_C on the polar boundary. Put

       M_(2m)(x) = integral (x.u)^(2m) dnu_C(u),
       b_(d,m) = (-1)^(m-1) (d/2+1)_(m-1)
                 / ((m-1)! (2m)(2m-1)), m >= 1.              (4)

   Here (a)_j is the rising factorial. Near zero,

       G_C(x) = |C| + sum_(m>=1) b_(d,m) M_(2m)(x).           (5)

   For every v != 0,

       ||v||_C = lim_(m->infty)
           (|[t^(2m)]G_C(tv)| / |b_(d,m)|)^(1/(2m)).         (6)

   The radius of the one-variable Taylor series is exactly 1/||v||_C.
   Consequently the local germ determines C among all bodies in the stated
   class. This assertion is noiseless and is not a stability estimate.

3. Suppose C has exactly 2r facets, with r >= d, and set

       k = r-d+2.                                           (7)

   The two homogeneous terms T_(2k)G_C and T_(2k-2)G_C determine C among
   **all** full-dimensional origin-symmetric convex bodies, without a
   polytope assumption on a competitor. Hence its jet through degree 2k
   determines C. An explicit algebraic reconstruction is given below.

4. For every d >= 2 and r >= d there are two distinct origin-symmetric
   polytopes, each with exactly 2r facets, whose jets agree through degree
   2k-1. Thus 2(r-d+2) is the sharp uniform jet order for this class.

5. As a corollary using classical L_p Minkowski uniqueness, the term
   T_(2k)G_C alone determines C if 2k != d. If 2k = d, it determines C
   exactly up to positive dilation. A constant term or T_(2k-2) then
   recovers the scale. The exceptional case really occurs, starting with
   parallelotopes in dimension four.

The normalized volume G avoids factors 2^(d/2); all conclusions transfer
unchanged to F. For invertible linear T,

    G_(TC)(Tx) = |det T| G_C(x).                             (8)

The bound is uniform in facet positions, so general position is not assumed.
It is not an assertion that every individual polytope needs that many terms.

## 1. Rank-one curvature calculation

First assume h = h_C is smooth and its spherical curvature matrix

    Q = nabla_S^2 h + h I

is positive definite on the tangent bundle of S^(d-1). Write A = cof Q,
l(n) = x.n, t = l/h, f(t) = sqrt(1+t^2), and H = h f(t). All derivatives
in this section are covariant derivatives on the sphere.

Since nabla^2 l + l I = 0, differentiating l = ht yields

    h nabla^2 t + nabla h tensor nabla t
      + nabla t tensor nabla h + t Q = 0.                   (9)

Differentiating H and using (9) gives

    Q_H = (f-t f') Q + h f'' nabla t tensor nabla t
        = f^(-1) Q + h f^(-3) nabla t tensor nabla t.        (10)

The determinant lemma, with tangent dimension d-1, therefore gives

    H det Q_H = h f^(2-d) det Q
               + h^2 f^(-d) <A nabla t, nabla t>.           (11)

The spherical tensor Q is Codazzi, so div A = 0. This is the classical
Cheng-Yau cofactor identity (see [SOURCES.md](SOURCES.md), item 3). One way
to check it directly is to write the cofactor with the alternating
Kronecker symbol. In each differentiated product, the Codazzi identity
nabla_i Q_ab = nabla_a Q_ib allows interchange of the derivative index and
one alternating index, making the contraction zero. Codazzi for Q follows
by commuting third derivatives of h on the unit sphere; the curvature terms
cancel the derivatives of h I. This also covers d=2, when A is the scalar 1.
No flat-coordinate Hessian is being substituted for the spherical Q.

Contract (9) with A and use tr(AQ) = (d-1)det Q. The product rule gives

    div(h^2 A nabla t) = -(d-1) h t det Q.                  (12)

Set J_d(t) = integral_0^t (1+s^2)^(-d/2) ds. Integrating the divergence
of J_d(t) h^2 A nabla t on the closed sphere proves

    integral h^2 f^(-d) <A nabla t,nabla t>
      = (d-1) integral h t J_d(t) det Q.                    (13)

Finally |C+_2[-x,x]| = (1/d) integral H det Q_H. Substitution of
(11) and (13) proves (3) for smooth C. This argument uses no smallness of x.

## 2. Extension to arbitrary bodies and coefficient extraction

Approximate h uniformly by positive averages of rotated support functions,
using smooth approximate identities on the rotation group, and then add
epsilon_j |.| with epsilon_j > 0 tending to zero. The resulting even support
functions h_j are smooth with positive Q_j and converge uniformly to h.
They can be chosen to correspond to bodies containing C, although this is
unnecessary for the all-real-x definition of G.

The standard continuity of surface area measures under Hausdorff convergence
gives S_(C_j) -> S_C weakly. Their total masses are bounded. Because h is
bounded away from zero, the continuous integrands
h_j(n) Phi_d(x.n/h_j(n)) converge uniformly on the sphere. The right side of
(3) therefore converges. The support functions
sqrt(h_j^2+(x.n)^2) converge uniformly too; continuity of volume gives
convergence of the left side. This proves (3) for every C in the theorem.
These standard continuity facts are named analytic inputs, not numerical
assumptions.

Differentiation of (2) gives the useful normalization

    Phi_d(0)=1, Phi_d'(0)=0,
    Phi_d''(t)=d(1+t^2)^(-(d+2)/2).                         (14)

The binomial series integrated twice gives exactly
Phi_d(t)=1+d sum_(m>=1)b_(d,m)t^(2m), with b as in (4).
Every b_(d,m) is nonzero. If ||x||_C<1, then
|x.n/h(n)| <= ||x||_C<1, so uniform absolute convergence permits
integration term by term. The same argument in a small complex polydisc
establishes an analytic germ, rather than only formal derivatives. Minkowski's
integral formula integral h dS_C=d|C| establishes the constant in (5).

## 3. Supported polar hull and exact Taylor radius

For any full-dimensional origin-symmetric body,

    conv(supp nu_C) = C polar.                              (15)

Here is a dimension-independent justification that does not assume that
S_C has full support. Its support Z spans R^d: otherwise the surface area
measure would be concentrated on a great subsphere, impossible for a body
with interior (equivalently, use the positive volumes of its projections).
The symmetric intersection

    D = intersection_(n in Z) {y : |y.n| <= h_C(n)}

is bounded, contains C, and has interior. For n in Z, containment and its
defining inequality give h_D(n)=h_C(n). Thus
V_1(C,D)=(1/d) integral h_D dS_C=|C|. The classical Minkowski inequality
V_1(C,D)^d >= |C|^(d-1)|D| gives |D|<=|C|. Since C is contained in D,
equal volume of these convex bodies implies D=C. Polarity proves (15).
The map n -> n/h_C(n) is a homeomorphism from the sphere onto the polar
boundary and the weighting h_C is strictly positive, so its image of Z
is precisely supp nu_C.

For v != 0 put a = max_(u in supp nu_C)|v.u|. By (15) and symmetry,
a = ||v||_C > 0. For every epsilon in (0,a), positive mass lies in
{|v.u|>a-epsilon}. Therefore

    (a-epsilon)^(2m) nu_C{|v.u|>a-epsilon}
      <= M_(2m)(v) <= a^(2m) d|C|.                         (16)

Taking roots proves (6). Moreover

    |b_(d,m+1)/b_(d,m)|
       = ((d/2+m)/m) ((2m)(2m-1)/((2m+2)(2m+1))) -> 1.

Hence |b_(d,m)|^(1/(2m)) -> 1. Cauchy-Hadamard applied to (5) proves
the claimed radius. All even directional moments are strictly positive;
there is no coefficient cancellation. Odd coefficients vanish. For v=0,
the restriction is constant and its radius is infinite. The radius refers
to the complex Taylor series, not to an obstruction to continuation along
the real axis.

## 4. A projective separation lemma with the necessary dimension saving

Let L_1,...,L_r be distinct one-dimensional subspaces spanning R^d, r>=d,
and set k=r-d+2. Let I_k be the space of homogeneous degree-k polynomials
vanishing on their union.

**Separation lemma.** The common real projective zero set of I_k is exactly
{L_1,...,L_r}. Also, for each j there is a homogeneous polynomial Q_j of
degree k-1 which vanishes on all other lines and is nonzero on L_j.

Proof of the first assertion: select representatives of d of the lines
forming a basis. For a nonzero z on none of the r lines, choose a nonzero
coordinate of z in this basis. The span of the other d-1 basis vectors is
a hyperplane avoiding z. For each of the remaining r-d+1 lines, choose
a hyperplane containing it and avoiding z; this is possible because z is
not on that line. The product of the k defining linear forms belongs to
I_k and is nonzero at z. The reverse inclusion is immediate.

For the second assertion, the representatives on the r-1 other lines have
rank at least d-1. If their rank is d-1, their span avoids L_j because all
r lines span R^d. If their rank is d, choose a basis among them and delete
a basis vector at a nonzero coordinate of a representative of L_j. In
either case, d-1 other lines lie in a hyperplane avoiding L_j. Cover the
remaining r-d other lines individually by hyperplanes avoiding L_j.
The product of these 1+(r-d)=k-1 linear forms is Q_j. This proves the lemma.

This is a projective homogeneous version of the classical positive-polynomial
finite-moment mechanism. Its role here is to improve the naive order 2r to
2(r-d+2), and to handle arbitrary facet configurations without a genericity
hypothesis. The proof is included so no external regularity bound for ideals
of points is needed.

## 5. Reconstruction from two terms, against arbitrary competitors

For even e let L_e(P)=integral P(u)dnu_C(u) on homogeneous polynomials
of degree e. The coefficients of T_eG_C give L_e: if |alpha|=e, then

    L_e(u^alpha) = [x^alpha]T_eG_C
                  / (b_(d,e/2) multinomial(e;alpha)).       (17)

Form the positive semidefinite Gram form on homogeneous degree-k polynomials

    B_k(P,Q)=L_(2k)(PQ).                                    (18)

For a 2r-facet polytope, nu_C has positive masses on r antipodal pairs
{+-u_j}. Its normal lines L_j span R^d. Positivity implies

    ker B_k = I_k.                                         (19)

The separation lemma therefore recovers the r lines as the common real
projective zeros of a basis of the kernel. It is a finite algebraic
reconstruction, even when the coordinates are irrational. It is not a
claim that factoring a single binary polynomial suffices in dimension >2.

Choose a nonzero representative v_j of each recovered line and write
u_j=alpha_j v_j up to sign, with alpha_j>0. Choose Q_j from the lemma
and a linear form A_j with A_j(v_j)=1. Then

    alpha_j^2 = L_(2k)(A_j^2 Q_j^2) / L_(2k-2)(Q_j^2).     (20)

Both integrals have only the j-th antipodal pair contributing. Its positive
mass, the factor alpha_j^(2k-2), and Q_j(v_j)^2 cancel. The denominator is
strictly positive. The recovered body is

    C = {x : |x.(alpha_j v_j)| <= 1 for j=1,...,r}.         (21)

Now let D be an arbitrary body in the theorem with the same two terms.
It has the same Gram kernel. For a basis P_1,...,P_N of I_k,
integral sum P_i^2 dnu_D=0, so positivity and continuity force supp nu_D
onto the same r lines. Each line meets the polar boundary of D in just
two antipodal radial endpoints. The nonzero integrals
L_(2k-2)(Q_j^2) force every line to occur. Formula (20) fixes every
endpoint, and (15) gives D=C. This is why finite computation among
polytopes is not being used to infer uniqueness against smooth competitors.

For completeness, B_(k-1) and B_k have rank r. The isolating polynomials
make evaluation in degree k-1 surjective. Multiplication by a linear form
nonzero on every line gives surjectivity in degree k. These are useful
validation checks, but rank r by itself is not used as a substitute for the
common-zero-set argument.

Unlike in the plane, singularity of B_k alone does not characterize
polytopes. For the circular cylinder C=B_2^2 x [-1,1] in R^3, the polar
measure is supported on a circle in the xy-plane and the two z-axis
endpoints. The nonzero quadratics xz and yz vanish on that support, so
B_2 is singular although C is not a polytope. Its ranks at degrees two
and three are four and five. The theorem uses the finite projective common
zero set from the separation lemma, not a transplanted planar rank criterion.

## 6. Sharpness in every dimension and for every facet count

Set k=r-d+2>=2. In R^2 let P be a regular 2k-gon centered at zero, and in
R^d let

    C = P x [-1,1]^(d-2).

For d=2 the second factor is omitted. This product has 2k+2(d-2)=2r
facets. Its polar measure is supported on the k normal lines of P in
the first coordinate plane and on the d-2 remaining coordinate axes.
The first 2k atoms have equal weights and radii; the axis atoms depend
only on the area of P and are unaffected by rotations within that plane.

For a homogeneous polynomial of degree e<2k, its restriction to the
circle in that plane has Fourier frequencies between -e and e. Summing
over 2k equally spaced atoms kills every nonzero frequency. Its integral
is consequently independent of the rotation angle. The axis atoms do
not change, and a monomial using both a planar and a nonplanar coordinate
vanishes at every atom. Hence all moments of degrees below 2k, as well
as volume, are unchanged under planar rotation.

Choose a rotation angle outside (pi/k)Z. It gives a different polytope
with the same Taylor jet through degree 2k-1, proving the sharp lower
bound for every (d,r). These are exactly realizable convex bodies, not
abstract positive measures asserted without a realization argument.

## 7. Highest term and its scale-critical exception

Put p=2k. Formula (17) also identifies T_pG_C with degree-p moments of
the classical L_p surface area measure

    dS_p(C,n)=h_C(n)^(1-p)dS_C(n)

on the unit sphere. If D has the same term, the same homogeneous kernel
argument forces S_p(D) onto C's r pairs of unit normal directions.
For each pair choose Q_j as above and a linear A_j taking value 1 at
its chosen unit representative. The nonnegative degree-p polynomial
A_j^2 Q_j^2 isolates that pair. Its integral recovers the pair's total
mass. Evenness then gives S_p(C)=S_p(D).

The remaining step is classical L_p Minkowski uniqueness, not a new general
injectivity statement for even-p projection bodies. To spell out the
dimension exception, equality of S_p gives

    V_p(C,D)=|D|,  V_p(D,C)=|C|.

The L_p Minkowski inequality for p>1 reads

    V_p(C,D)^d >= |C|^(d-p)|D|^p,

with equality exactly for positive dilates. If p!=d, the two inequalities
force |C|=|D|, then equality forces C=D. If p=d, each inequality is already
an equality, so D is a positive dilate of C. Conversely S_d and T_dG are
unchanged by dilation, since

    T_pG_(aC) = a^(d-p) T_pG_C.

This proves exactly the stated ambiguity. The constant term scales by a^d
and T_(d-2) by a^2, so either removes it. The latter term is nonzero.

## Checks, scope, and what is not established

The all-dimensional transform, positivity, common-zero-set argument, and
sharpness family are proved above. The compact exact checker tests distinct
normalizations and realizable examples; it is not the universal proof.
Classical support-function calculus, surface-measure continuity, Minkowski's
inequality, and (only in Section 7) its L_p version are the mathematical
inputs. Kernel checking in a proof assistant and independent review remain
outstanding at publication.

No numerical conditioning, stability under noise, minimal sampled-direction
count, finite-jet characterization of every nonpolytope, or extension to
nonsymmetric bodies is claimed. No assertion is made for Firey exponent
other than two. The result is a complete answer to the selected
all-dimensional germ and sharp polytope-jet problem, not to a general
Rogers-Shephard inequality. Historical priority is not established.
