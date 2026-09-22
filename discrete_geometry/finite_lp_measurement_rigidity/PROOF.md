# Finite Lp measurements and volume: an exact uniqueness criterion

2026-09-22. Analytic theorems, with exact finite corroboration. These proofs
are not formalized and have not yet received independent review.
Classical ingredients and the scope of the literature search are recorded
in [SOURCES.md](SOURCES.md).

## 1. The classification

Fix a dimension d >= 2, a real p > 1, and 0 < alpha < 1. All bodies below
are full-dimensional compact convex bodies in R^d, symmetric about the
designated origin. Competitors need not be smooth. Coordinates are fixed;
uniqueness means equality, not congruence.

Write h_K for the support function on the unit sphere, S_K for ordinary
surface area measure, V(K) for volume, and

    dS_p(K,n) = h_K(n)^(1-p) dS_K(n).

Let W be any finite-dimensional real subspace of the even functions in
C^alpha(S^(d-1)). The measurements are

    D_W(K) = ( V(K), { integral phi dS_p(K) : phi in W } ).       (1)

A basis of W suffices, so (1) consists of finitely many real numbers.
Let H_alpha be the open set of even h in C^(2,alpha) with

    h > 0,       Q_h = Hess_S h + h I > 0.                       (2)

These are precisely the support functions in the smooth positive-curvature
class used here. The corresponding boundary has positive Gauss curvature.

**Theorem 1 (finite-measurement classification).** For K with h_K in
H_alpha, the following statements are equivalent:

1. D_W determines K among all origin-symmetric convex bodies.
2. D_W determines K in some C^(2,alpha) neighborhood in H_alpha.
3. h_K^p belongs to W as a function on the sphere.

If condition 3 fails, the equal-data bodies near K form an
infinite-dimensional C^1 submanifold of H_alpha, of codimension
dim(W)+1. In particular, there are distinct equal-data bodies arbitrarily
close to K. For every positive integer N, an injective C^1 family with N
parameters passes through K and has exactly the same measurements and
volume.

The implication 3 -> 1 holds without the smoothness assumption on K.
The converse in the general finite-measurement theorem is asserted only
under (2). No conclusion for p <= 1 is asserted.

## 2. Global sufficiency

The classical Lp mixed volume and Minkowski inequality, for p > 1, are

    V_p(L,K) = (1/d) integral h_K^p dS_p(L),
    V_p(L,K) >= V(L)^((d-p)/d) V(K)^(p/d),                      (3)

with equality if and only if K and L are positive dilates. This result
applies to arbitrary convex bodies containing the origin in their
interiors; see Lutwak--Yang--Zhang, formula (1.5), in the sources.

Suppose h_K^p is in W and D_W(L)=D_W(K). Then

    V_p(L,K) = (1/d) integral h_K^p dS_p(K) = V(K).

Because V(L)=V(K), equality holds in (3). Thus L is a positive dilate of K,
and equality of volume makes that dilation one. This proves 3 -> 1.
The implication 1 -> 2 is immediate.

This short sufficiency argument is an application of the classical
inequality, not a new mixed-volume inequality. The substantive converse
will keep both the measured moments and volume exactly fixed.

## 3. A normalized local coordinate system

Throughout this section, integrals without a specified measure use the
ordinary spherical area element d sigma. For h in H_alpha set

    D = det Q_h,       C = cof Q_h,
    V = (1/d) integral h D,
    f = F_p(h) = h^(1-p) D / V.                                (4)

Thus f is the density of S_p(K)/V(K). In particular,

    integral h^p f = d.                                        (5)

**Lemma 2.** For every real p > 1, F_p is a C^1 local diffeomorphism
from H_alpha to the positive even functions in C^alpha. This includes
p=d.

We give the analytic argument to make the precise regularity, normalization
and spectral estimate explicit. The ingredients are classical support
calculus, the Hilbert--Brunn--Minkowski spectral gap, elliptic Fredholm and
Schauder theory on the sphere, and the Banach inverse function theorem.

Put d mu = h D d sigma and let E denote mean with respect to mu, so that
mu(S^(d-1))=dV. Write a variation as u=h g. Mixed-volume differentiation
and the self-adjoint Cheng--Yau identity give

    DV(h)[u] = integral u D = dV E g.                           (6)

The Cheng--Yau identity says div C=0; equivalently, the operator
u -> C:(Hess_S u+uI) is self-adjoint under spherical integration. It holds
first for smooth h and extends here by smooth approximation in C^2.

Define the second-order operator

    A_h g = (1/(hD)) div( h^2 C grad_S g )
          = h tr(Q_h^(-1) Hess_S g)
            + 2 <Q_h^(-1) grad_S h, grad_S g>.                 (7)

For C^(2,alpha) h the second expression is the classical C^alpha
expression; the first is its weak divergence form. Smooth approximation
justifies the integration identities below at this regularity. Directly,

    Q_(h g) = g Q_h + h Hess_S g
              + grad_S h tensor grad_S g
              + grad_S g tensor grad_S h.

Differentiating (4) consequently yields

    DF_p(h)[h g] / f
        = T_(h,p) g
        = A_h g + (d-p)g - d E g.                              (8)

There is no division by d-p in this formula.

For real g, integration by parts gives

    integral A_h g d mu = 0,
    -integral g A_h g d mu
        = integral h^2 <C grad_S g, grad_S g> d sigma
        =: E_h(g).                                            (9)

We need only the classical spectral gap

    E_h(g) >= (d-1) integral (g-Eg)^2 d mu.                    (10)

Here is a derivation, to avoid assuming a stronger local Lp or logarithmic
Brunn--Minkowski conjecture. The path h+t h g remains a support function
for small positive and negative t. The first and second variations are

    V' = integral g d mu,
    V'' = (d-1) integral g^2 d mu - E_h(g).                    (11)

For the second identity, differentiate D in (6), substitute the formula
for Q_(h g), and use (9). Concavity of V^(1/d) along this Minkowski path
is the classical Brunn--Minkowski inequality. It gives

    V'' <= ((d-1)/d) (V')^2/V
         = (d-1) dV (Eg)^2,

which is exactly (10).

The decomposition into constants and mu-mean-zero functions is preserved
by T_(h,p). On constants it acts by -p. On a mean-zero function it is
A_h+(d-p), and (9)--(10) give

    -integral g T_(h,p)g d mu
       >= (p-1) integral g^2 d mu,        Eg=0.                (12)

In particular the kernel is zero: averaging Tg=0 first yields Eg=0,
and then (12) yields g=0.

For completeness, surjectivity here is an elliptic fact, not an inference
from injectivity alone. A_h-I is an isomorphism C^(2,alpha) -> C^alpha
on the closed sphere by the maximum principle and Schauder solvability.
The difference T_(h,p)-(A_h-I) is a zeroth-order multiplication and a
rank-one mean term. As an operator C^(2,alpha) -> C^alpha it is compact
(the Holder embedding loses two derivatives). Thus T_(h,p) is Fredholm
of index zero. Its zero kernel makes it an isomorphism with bounded
inverse. Equivalently one may use its self-adjoint elliptic realization
and (12). Antipodal symmetry of the coefficients ensures that the unique
solution for an even right-hand side is even, so the same conclusion
holds on the even subspaces.

Multiplication by h and f are bounded invertible maps on the respective
Holder spaces. Therefore (8) makes DF_p(h) an isomorphism. The map (4)
is C^1: determinant, positive real powers and volume are C^1 in these
spaces. The Banach inverse function theorem proves Lemma 2.

The unnormalized density has a scale degeneracy at p=d. In contrast,
F_p(c h)=c^(-p)F_p(h); its constant logarithmic mode in (8) is -p.
This is why the same proof covers the critical exponent.

## 4. Volume in density coordinates and the converse

In a neighborhood supplied by Lemma 2, view V as a C^1 function of f.
If eta=DF_p(h)[h g], multiply (8) by h^p f=hD/V and integrate. Equations
(6) and (9) give

    integral h^p eta
      = (1/V)[(d-p) integral g d mu - d(Eg) integral d mu]
      = -(p/V) integral g d mu
      = -p D log V(h)[h g].                                   (13)

Consequently, in density coordinates,

    D log V(f)[eta] = -(1/p) integral h^p eta d sigma.          (14)

Notice both the minus sign and the absence of an extra volume factor.
As a check, scaling f to (1+t)f scales h by (1+t)^(-1/p), and (5)
makes (14) equal -d/p, as required.

Let

    E_W = { eta in C^alpha_even : integral phi eta=0
                                  for every phi in W }.

The moment functionals have rank dim(W): their Gram matrix on any basis
of W is positive definite under d sigma. Hence E_W is a closed
infinite-dimensional subspace of codimension dim(W).

Suppose h^p is not in W. Let Pi_W be the L^2(d sigma) projection onto W
and choose

    eta_0 = h^p - Pi_W(h^p).

This function is in E_W and C^alpha_even, and

    integral h^p eta_0 = integral eta_0^2 > 0.                 (15)

Thus log V restricted to the affine space f+E_W has nonzero derivative
at f. The implicit function theorem on this Banach space makes

    { f' near f : f'-f in E_W, V(F_p^(-1)(f'))=V(K) }          (16)

an infinite-dimensional C^1 submanifold, of codimension one within
f+E_W. Positivity is an open condition, so every sufficiently nearby f'
in (16) remains positive and corresponds to a body satisfying (2).

For these bodies the normalized W-moments agree; equality of V in (16)
then gives equality of the *unnormalized* measurements in (1). Conversely,
equal data in (1) gives precisely the two conditions in (16).
Pulling back by the local diffeomorphism proves the stated codimension
dim(W)+1 in H_alpha.

For an explicit finite-parameter interpretation, choose any N functions
zeta_1,...,zeta_N in E_W independent modulo the line spanned by eta_0.
Use f'=f+s eta_0+sum t_i zeta_i. Equation (14)--(15) solves the volume
constraint for s=s(t_1,...,t_N), with s(0)=0. Linear independence and
the local inverse show that distinct t give distinct bodies. Such choices
exist for every N because E_W is infinite-dimensional.

This proves failure of statement 2 whenever statement 3 fails and
completes Theorem 1. The construction is exact; an infinitesimal kernel
alone would not have sufficed.

## 5. One Firey Taylor term and volume

For any origin-symmetric body K define, near x=0,

    G_K(x) = 2^(-d/2) V((K+x)+_2(K-x))
           = V(K+_2[-x,x]).                                   (17)

Here h_(A+_2 B)^2=h_A^2+h_B^2. T_q G denotes the homogeneous degree-q
Taylor polynomial, with the factorial already included. The earlier
[all-dimensional Firey transform](../firey_volume_sharp_jets/PROOF.md)
proves analyticity near zero and

    T_(2m)G_K(x) = b_(d,m) integral (x.n)^(2m) dS_(2m)(K,n),
    b_(d,m) = (-1)^(m-1) (d/2+1)_(m-1)
                / ((m-1)! (2m)(2m-1)),                        (18)

for m>=1. Every b_(d,m) is nonzero; (a)_j is the rising factorial.
Odd terms vanish and G_K(0)=V(K). Equation (18) is the only imported
Firey-transform result in this application; Theorem 1 does not depend
on it. Its source includes the proof for nonsmooth competitors.

Fix an even p>=2. Expanding (x.n)^p shows that T_p gives exactly the
integrals of all degree-p homogeneous monomials in n. Thus its probe
space is

    W_p = { P restricted to S^(d-1) : P homogeneous of degree p }.

Lower even spherical polynomial degrees are included via multiplication
by powers of sum n_i^2; no lower *Lp indices* are inferred from this fact.

**Corollary 3.** If h_K satisfies (2), the pair (V(K),T_pG_K) determines
K among all origin-symmetric convex bodies if and only if the homogeneous
function h_K(x)^p is a polynomial of degree p on R^d. If it is not,
arbitrarily close distinct C^(2,alpha) bodies have the same pair, with
the local fiber described by Theorem 1.

Indeed sphere membership h_K^p in W_p is equivalent to the homogeneous
polynomial identity by homogeneity. This classifies a *single term plus
volume*. It does not classify an arbitrary smooth body's entire jet
through degree p, whose different terms involve different measures S_q.

At p=d, if h_K^p is polynomial, T_p alone already determines K up to
dilation: equality of that term gives V_p(L,K)=V(K), and the right side
of (3) is V(K) regardless of V(L). Equality in (3) implies dilates.
All those dilates do have the same T_d, since S_d is scale invariant.

## 6. Complete quadratic classification, including nonsmooth bodies

For p=2 define the positive definite matrix

    M(K) = integral (n n^t)/h_K(n) dS_K(n).

The support of S_K is not in a great subsphere for a full-dimensional
body, which proves positive definiteness. Equation (18) reads
T_2G_K(x)=(1/2)x^t M(K)x.

**Corollary 4.** Among *all* origin-symmetric full-dimensional convex
bodies, exactly the ellipsoids are uniquely determined by their full
quadratic Firey jet (V,T_2). Every nonellipsoid has arbitrarily
Hausdorff-close distinct equal-jet bodies.

Sufficiency follows from Section 2 because an origin-centered ellipsoid
has quadratic h^2. For necessity, the affine transformation law is

    M(AK)=|det A| A^(-t) M(K) A^(-1),       A invertible.       (19)

For a smooth body it follows by mapping the unit normal n to
A^(-t)n/|A^(-t)n|, transforming the surface element by
|det A| |A^(-t)n|, and transforming support values by the reciprocal
factor |A^(-t)n|. The same law for every convex body follows by smooth
Hausdorff approximation and weak continuity of surface area measures;
h stays bounded away from zero.

Take A=M(K)^(1/2), the positive square root. Then M(AK) is a positive
scalar multiple of the identity. Every rotation R of AK has exactly
the same matrix and volume. If AK were fixed by every rotation, its
support function would be constant and it would be a Euclidean ball.
For a nonellipsoid K, AK is not a ball, so some rotations change it.
There are such rotations arbitrarily near the identity: otherwise the
stabilizer would contain a neighborhood of the identity and hence all
of the connected group SO(d). Transforming these rotated bodies back
by A^(-1) proves the assertion, including Hausdorff closeness.

This separate elementary argument removes the regularity restriction
only for p=2; it does not remove it in Theorem 1 for general W.

## 7. Every even minimum jet order occurs for smooth bodies

**Theorem 5.** For every d>=2 and every even integer p>=2, there is an
origin-symmetric C^infinity body of positive curvature whose minimum
full Firey jet order for uniqueness among all symmetric convex bodies
is exactly p. One explicit family has homogeneous support function

    h_e(x) = [ |x|^p + e Re(x_1+i x_2)^p ]^(1/p),
    0 < |e| <= 1/(4p).                                        (20)

The result is uniform in d and p; the constant is sufficient, not claimed
optimal.

First verify that (20) is a support function with the stated curvature.
On the unit sphere let Y(n)=Re(n_1+i n_2)^p and a=|e|. Euclidean
derivatives of this homogeneous polynomial give

    |Y|<=1,       |grad_S Y|<=p,
    ||Hess_S Y||<=p(p-1)+p=p^2.

For the last estimate use Hess_S Y=Hess_E Y restricted to tangents
-pY I. With h=(1+eY)^(1/p), the chain rule therefore yields

    Q_h >= [ (1-a)^(1/p)
              - p a(1-a)^(1/p-1)
              - (p-1)a^2(1-a)^(1/p-2) ] I
        = (1-a)^(1/p-2)[1-(p+2)a+2a^2] I
        >= (1/2) I.                                         (21)

Indeed a<=1/(4p) and p>=2 imply (p+2)a<=1/2, while the prefactor is
at least one. Thus h>0 and Q_h>0. The positive homogeneous extension
is convex because its tangential Hessian is Q_h/|x| and its radial
direction is null; equivalently, criterion (2) gives its convex body.
It is even and C^infinity away from zero. The associated boundary is
C^infinity and has positive curvature.

The pth power in (20) is a homogeneous polynomial because p is even.
Corollary 3 proves uniqueness from V and T_p, hence from the full p-jet.

For sharpness rotate only the (x_1,x_2)-plane. The body is invariant
under angle 2pi/p but not under all angles. Every homogeneous Taylor
term T_q of G_K inherits that cyclic symmetry. In complex coordinates
z=x_1+i x_2, zbar=x_1-i x_2, a monomial

    z^a zbar^b x_3^c3 ... x_d^cd

of total degree q has planar rotation weight a-b with |a-b|<=q.
Invariance under angle 2pi/p permits only weights divisible by p.
If q<p the only permitted weight is zero. Thus every T_q with q<p
is invariant under *every* planar rotation. The constant term, volume,
is rotation invariant too.

For a rotation R in this plane, equivariance of (17) gives
G_(RK)(x)=G_K(R^(-1)x). Consequently K and RK have identical full jets
through degree p-1. They are distinct whenever the rotation changes
Re(z^p) in (20); for example angle pi/(2p) does. Such rotations can
also be chosen arbitrarily close to zero. This proves the exact
minimum p. It is an assertion about individual smooth bodies, not only
the worst case over a parameter family.

## 8. Verification and limits

The universal conclusions follow from the analytic proof. The companion
standard-library [verifier](verify.py) checks exact zonal support-function
variations and spherical integrals, the normalization and signs in
(8)--(14), critical scaling, the algebra in (21), and the frequency
obstruction used for sharpness. It includes deliberately wrong formulas
that must be rejected. It does not certify general elliptic regularity,
the Banach inverse function theorem, or classical Minkowski equality.

All new classification claims are restricted as stated. The general
nonsmooth finite-probe converse, a classification from a collection of
different Taylor degrees, stability with noisy measurements, and p<=1
are not resolved here. No claim of absolute historical priority is made.
