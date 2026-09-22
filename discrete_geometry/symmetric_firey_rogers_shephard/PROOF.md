# The symmetric Firey Rogers–Shephard inequality in every dimension

2026-09-22. Analytic proof; independent review and formalization pending.
Attribution and the scope of the literature search are in [SOURCES.md](SOURCES.md).

## 1. Statement

Let d >= 2, 1 < p < infinity, and q=p/(p-1). Let K be a compact convex
body with nonempty interior in R^d, containing the origin, and having a
center of symmetry. Firey addition uses

    h_(K+_p L)(n) = (h_K(n)^p+h_L(n)^p)^(1/p).

All volumes below are ordinary d-dimensional Lebesgue volumes. Define

    kappa_(d,p) = sum_(i=0)^d binom(d,i)/binom(d/q,i/q),       (1)
    binom(a,b) = Gamma(a+1)/(Gamma(b+1)Gamma(a-b+1)).

**Theorem.** One has the sharp inequality

    |K+_p(-K)| <= kappa_(d,p)|K|.                            (2)

Write K=C+x with C=-C and x in C. If S_C denotes ordinary surface area
measure and h=h_C, the following three conditions are equivalent:

1. Equality holds in (2).
2. |x.n|=h(n) for S_C-almost every n in S^(d-1).
3. x != 0 and, for the polar C^o, putting

       F = C^o intersect {u : x.u=1},

   one has

       C^o = conv(F union (-F)).                            (3)

Here F is necessarily a (d-1)-dimensional convex body in its affine
hyperplane. The equality class is independent of p in the stated range.
For a polytope C, condition 2 says that every facet contains x or -x.

For d=2 these conditions say exactly that K is a parallelogram with the
origin as a vertex. In higher dimensions there are many other equality
cases, including translated crosspolytopes and nonpolytopal double cones.

Inequality (2) is Conjecture 4 of Fradelizi–Manui–Meyer–Ndiaye,
arXiv:2607.03582v1. Its zonoid case and its sharp constant are prior work.
The planar equality theorem is also prior work in Discovery Net. The claim
here is the complete inequality and equality classification in all
dimensions. This is a proof claim, not an independently reviewed result.

The one-dimensional case is elementary: for K=[-a,b], a,b>=0 and a+b>0,
the ratio is 2(a^p+b^p)^(1/p)/(a+b)<=2, with equality exactly when a b=0.
Thus the substantive dimensional restriction in the proof is d>=2.

## 2. An exact translation-volume formula

For -1 <= t <= 1 put

    f(t) = ((1+t)^p+(1-t)^p)^(1/p),
    a(t) = f(t)-t f'(t),
    R(t) = integral_0^t f(s) a(s)^(d-2) f''(s) ds,
    Psi(t) = f(t)a(t)^(d-1)+(d-1)t R(t).                    (4)

The integrals at the endpoints are improper integrals. For |t|<1, direct
differentiation, with A=1+t and B=1-t, gives

    f' = (A^(p-1)-B^(p-1))/f^(p-1),
    a  = (A^(p-1)+B^(p-1))/f^(p-1) > 0,
    f'' = 4(p-1)(1-t^2)^(p-2) f^(1-2p) > 0.               (5)

Both f and a are positive and continuous on [-1,1]. Since p-2 > -1,
f'' is integrable at both endpoints, so R and Psi are continuous there.
Their parity is: f,a,Psi even and R odd. Their endpoint values include

    f(1)=2, f'(1)=1, a(1)=1.

**Volume formula.** For every C=-C with nonempty interior and every x in C,

    |(C+x)+_p(C-x)|
       = (1/d) integral_(S^(d-1)) h(n) Psi(x.n/h(n)) dS_C(n). (6)

We first prove (6) for smooth support h with positive curvature matrix

    Q = Hess_S h + h I.

For now assume x is in int C. Write l(n)=x.n, t=l/h, H=h f(t),
D=det Q and U=cof Q. The support of the Firey sum is exactly H.
All derivatives in the following calculation are spherical derivatives.
Because Hess_S l=-l I, differentiating l=ht gives

    h Hess_S t + grad h tensor grad t + grad t tensor grad h
       = -t Q.

The chain rule therefore yields the rank-one identity

    Q_H = a Q + h f'' grad t tensor grad t.                 (7)

In particular Q_H is positive definite. The rank-one determinant formula
in tangent dimension d-1 gives

    H det Q_H
       = h f a^(d-1) D
         + h^2 f a^(d-2) f'' <U grad t,grad t>.             (8)

The cofactor tensor U is divergence-free. This is the classical
Cheng–Yau identity: Hess_S h+hI is a Codazzi tensor on the unit sphere,
and the alternating determinant formula for its cofactor cancels each
covariant derivative. In particular, differentiation of

    h^2 grad t = h grad l-l grad h

and contraction with U show that

    div(h^2 U grad t)
       = <U, h Hess_S l-l Hess_S h>
       = -l <U,Q> = -(d-1)t h D.                           (9)

There is no derivative of U in (9), by the divergence-free identity.
Integrate div(R(t)h^2 U grad t) on the sphere. Its integral is zero, hence

    integral h^2 R'(t)<U grad t,grad t>
       = (d-1) integral t R(t)hD.                          (10)

Since R'=f a^(d-2)f'', substitute (10) into (8), and use the classical
support-volume identity |L|=(1/d)integral h_L det Q_L. The result is (6),
with dS_C=D dσ.

For arbitrary C and a fixed x in int C, approximate C in Hausdorff
distance by smooth symmetric bodies with positive curvature. This can be
done by smoothing the support function over rotations and adding a small
Euclidean ball. The supports converge uniformly and stay uniformly
positive. Eventually x is interior to each approximant and |x.n/h_j(n)|
stays below one by a uniform margin. Surface area measures converge weakly;
the integrands in (6) converge uniformly. Firey supports also converge
uniformly, and volume is Hausdorff-continuous. Thus (6) passes to arbitrary
C for interior x.

Finally replace a boundary point x by r x, 0 <= r < 1, and let r increase
to one. Continuity of Psi on its closed interval, h>0, and finiteness of
S_C justify the integral limit. The Firey supports converge uniformly.
This proves (6) for every x in C, including all nonsmooth equality cases.
In particular, no differentiability at t=1 is assumed when 1<p<2.

## 3. The scalar maximum and its exact value

Since a'=-t f'', the derivative terms in (4) cancel:

    Psi'  = f' a^(d-1)+(d-1)R,
    Psi'' = d f'' a^(d-1) > 0,        -1<t<1.               (11)

The even function Psi is therefore strictly increasing on [0,1]. Since
x is in C, |x.n| <= h(n), and (6) implies

    |(C+x)+_p(C-x)| <= Psi(1)|C|.                           (12)

To evaluate this endpoint, set s=f'/a. The function s increases from 0 to
1 as t increases from 0 to 1, because

    ds/dt = f f''/a^2.

The identities (5) imply

    (a+f')^q+(a-f')^q = 2^q,
    a = 2/((1+s)^q+(1-s)^q)^(1/q).

Consequently

    Psi(1) = 2+(d-1)R(1),
    R(1) = integral_0^1 [2/((1+s)^q+(1-s)^q)^(1/q)]^d ds.  (13)

All substitutions can first be made on compact subintervals and then
passed to the endpoints by positivity. With u=(1-s)/(1+s), (13) becomes

    R(1) = 2 integral_0^1 (1+u)^(d-2)/(1+u^q)^(d/q) du
         = integral_0^infinity (1+u)^(d-2)/(1+u^q)^(d/q) du. (14)

For the second equality substitute u=1/v in the tail integral: its
integrand times du is unchanged. Expansion of the numerator and the
Euler beta integral now give

    R(1) = (1/q) sum_(i=1)^(d-1)
                binom(d-2,i-1) B(i/q,(d-i)/q).             (15)

Every beta argument is positive. For 1<=i<=d-1 the gamma recurrence gives

    ((d-1)/q) binom(d-2,i-1) B(i/q,(d-i)/q)
       = binom(d,i)/binom(d/q,i/q).                         (16)

The i=0 and i=d terms in (1) are both one. Equations (13)--(16) identify
Psi(1) with kappa_(d,p), completing the proof of (2).

As normalization checks, kappa_(2,2)=2+pi/2,
kappa_(3,2)=6, and kappa_(4,2)=5+3pi/2. For fixed d the constant tends to
2^d as p decreases to one and to d+1 as p tends to infinity. These are
the classical symmetric Minkowski and convex-hull constants, respectively;
the endpoint equality theorems are not needed here.

## 4. Complete equality classification

Formula (6) gives the exact nonnegative deficit

    kappa_(d,p)|C|-|(C+x)+_p(C-x)|
       = (1/d) integral h(n)[Psi(1)-Psi(x.n/h(n))] dS_C(n). (17)

By strict increase, the bracket vanishes exactly when |x.n|=h(n).
This proves equivalence of conditions 1 and 2. In particular x=0 is never
an equality placement for finite p>1. It remains to prove that condition
2 is exactly the geometric class (3); merely approximating an arbitrary
body by equality polytopes would not prove this necessity.

We use the following standard surface-area support fact, with a proof to
make the passage to nonsmooth bodies explicit:

    conv{n/h(n) : n in supp S_C} = C^o.                     (18)

Indeed C is the intersection of the supporting halfspaces with normals
in supp S_C. To see this, suppose z is in that intersection but outside C,
and put D_0=conv(C union {z}). Then h_(D_0)=h_C on supp S_C. The mixed
volume formula and the classical first Minkowski inequality imply

    |C| = (1/d)integral h_(D_0) dS_C
         = V(C[d-1],D_0)
         >= |C|^((d-1)/d)|D_0|^(1/d).

But D_0 strictly contains the full-dimensional body C and has larger
volume, a contradiction. Polarity gives (18). Equivalently, if P is the
compact convex hull in (18), the just-proved assertion is P^o=C;
P has the origin in its interior, and the bipolar identity gives P=C^o.

Suppose condition 2 holds. Since |x.n|-h(n) is continuous, it vanishes
everywhere on supp S_C, not just almost everywhere. Thus the generating
set in (18) lies in the two exposed faces x.u=+/-1 of C^o. By symmetry
these faces are F and -F, and (18) proves (3). Full dimensionality forces
dim F=d-1: the linear span of F union (-F) has dimension at most
dim F+1 and must be all of R^d.

Conversely suppose (3). Approximate F in its hyperplane by
(d-1)-dimensional polytopes F_j contained in F, converging in Hausdorff
distance. Put

    P_j=conv(F_j union (-F_j)),    C_j=P_j^o.

For all sufficiently large j these are full-dimensional symmetric convex
bodies, P_j contains zero in its interior, and C_j converges to C.
Every vertex of P_j lies in one of the hyperplanes x.u=+/-1. Facets of
C_j correspond to these polar vertices, so every facet contains x or
-x. Surface area measure of a polytope is supported on its facet normals;
therefore C_j satisfies condition 2. The already proved volume formula
gives equality for C_j+x. Also x is in C_j since |x.u|<=1 on P_j.
Hausdorff continuity of volume and Firey addition passes equality to C+x.
This proves condition 3 implies condition 1 and completes the equivalence.

This converse does not assert that surface area measure is supported only
at extreme polar points for arbitrary bodies. It uses polytopal
approximation within the two fixed faces, where that statement is valid.

## 5. Examples and scope

* **Parallelotopes:** C=T[-1,1]^d, with T invertible and x any vertex.
  Every facet contains x or -x. This recovers the cube sharpness example.
* **Crosspolytopes:** C={y: sum_i |y_i|<=1}, x=e_1. Its polar is the cube,
  which is the convex hull of the opposite faces u_1=+/-1.
* **Double cones:** write R^d=R^(d-1) times R, let B=-B be any convex
  body with interior in R^(d-1), and put

      C={(y,z): ||y||_B+|z|<=1},    x=(0,1).

  Then C^o=B^o times [-1,1], so (3) holds. Choosing a Euclidean ball B
  gives nonpolytopal equality cases when d>=3.
* **Dimension two:** F in (3) is a nondegenerate segment. Its endpoints
  and their negatives form a centrally symmetric quadrilateral. Its polar
  C is a parallelogram, and the two constraints from the endpoints of F
  meet at the vertex x. Hence C+x has zero as a vertex, as claimed.

For positive-curvature smooth C and x in C the inequality is strict:
S_C has full spherical support, whereas |x.n|=h(n) cannot hold for all n
(choose n perpendicular to x). This is consistent with all equality
examples being nonsmooth; it is not a uniform quantitative stability bound.

No assertion here concerns general nonsymmetric bodies, the separate
asymmetric L_p-zonoid conjecture, p<=1, a quantitative distance-to-equality
estimate, or a proof-assistant formalization.

The proof uses classical support-volume and mixed-volume identities,
the divergence-free cofactor identity, smooth approximation, and weak
continuity of surface area measures. The finite exact checks in
[verify.py](verify.py) corroborate the algebra, constants, and selected
geometric examples. They do not replace these analytic arguments.
