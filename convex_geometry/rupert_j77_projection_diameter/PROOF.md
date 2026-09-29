# Exact minimum projection diameter of J77

Author: six-rupert-2, researcher. Prepared 2026-09-29.

This is a computer-assisted optimisation theorem and an analytic obstruction
for a restricted receiver view. It does not decide whether J77 is Rupert.
All finite checks use exact arithmetic in the ordered field
\(\mathbb Q(\sqrt5)\). The continuous-to-finite reduction is proved below.

## 1. Statements

Let \(P\) be the unit-edge paragyrate diminished rhombicosidodecahedron
(Johnson solid J77). Write \(\pi_d\) for orthogonal projection onto the plane
perpendicular to the unit vector \(d\). Then

\[
\boxed{\min_{\|d\|=1}\operatorname{diam}(\pi_dP)
       =2\sqrt{\frac{787+293\sqrt5}{298}}.}
\tag{1}
\]

One direction attaining this minimum is parallel to

\[
D=\left(0,-1,\frac{7+\sqrt5}{2}\right).
\tag{2}
\]

Every strict projected passage of a copy scaled by \(\lambda\), allowing all
orientations, in-plane rotations and translations, satisfies

\[
\boxed{\lambda<\sqrt{\frac{2797-75\sqrt5}{2552}}.}
\tag{3}
\]

Consequently the Nieuwland number, defined as the supremum of such scales,
is at most the radical in (3). The checker proves that this radical lies
strictly between 1.015031019664 and 1.015031019665 by squaring rational
endpoints and comparing in \(\mathbb Q(\sqrt5)\).

There is also the restricted exclusion in Section 6. Neither (1) nor (3)
excludes unit-scale passages with general receiver directions.

## 2. Exact model and centrally symmetric core

Put \(s=\sqrt5\), \(\varphi=(1+s)/2\), and

\[
C_1=\frac{1+s}{4},\quad C_3=\frac{3+s}{4},\quad
C_5=\varphi,\quad C_7=\frac{5+s}{4},\quad C_9=\frac{2+s}{2}.
\]

The usual unit-edge rhombicosidodecahedron has vertex set \(O\) given by
all independent changes of signs and cyclic permutations of

\[
(1/2,1/2,C_9),\qquad(0,C_3,C_7),\qquad(C_3,C_1,C_5).
\]

There are 60 distinct vertices. Set

\[
A=(0,\varphi,1),\quad H=\frac{5+3s}{4},\quad T=\frac{9+3s}{4},
\]

and let

\[
K=\{p\in O: |A\cdot p|\le H\},\qquad
C=\{p\in O: A\cdot p=-T\}.
\]

Deleting the two opposite pentagonal cupolas gives the 50-vertex
parabidiminished rhombicosidodecahedron \(\operatorname{conv}K\), J80.
Restore the negative cupola after gyrating it through \(\pi/5\) around
the axis \(A\). Thus J77 has vertex set \(V=K\cup\rho(C)\), where

\[
\rho(p)=C_1p+(1-C_1)\frac{A\cdot p}{A\cdot A}A
             +\frac{s-1}{4}(A\times p).
\tag{4}
\]

This is Rodrigues' rotation formula because
\(C_1=\cos(\pi/5)\) and
\((s-1)/4=\sin(\pi/5)/\|A\|\). In particular,
\(C_1^2+((s-1)/4)^2(A\cdot A)=1\).

`model.py` independently generates this construction and contains the
standard McCooey coordinate fixture. The checker proves that the two
55-vertex sets coincide. It also verifies the fixture's supporting regular
faces and incidence counts: 55 vertices, 105 edges, and 52 faces comprising
15 triangles, 25 squares, 11 pentagons and one decagon.

Every \(p\in V\) satisfies

\[
\|p\|^2=R^2=\frac{11+4s}{4}.
\tag{5}
\]

The set \(K\) is centrally symmetric. Choose one representative \(a_i\)
from each of its 25 antipodal pairs, in the fixture order used by the checker.

## 3. Finite direction reduction

**Lemma.** Suppose \(a_1,\ldots,a_m\) are nonzero vectors in
\(\mathbb R^3\) with the same norm \(R\). The maximum on the unit sphere of

\[
f(d)=\min_i|a_i\cdot d|
\]

is attained at a direction parallel to one of

\[
a_i,\qquad a_i+\epsilon a_j,\qquad
(a_i-\epsilon a_j)\times(a_i-\eta a_k),
\tag{6}
\]

where \(i<j<k\), \(\epsilon,\eta\in\{-1,1\}\), and zero vectors are omitted.

**Proof.** The continuous function \(f\) attains a maximum on the compact
sphere. That maximum is positive: a finite union of great circles cannot
cover the sphere. Let \(d\) be a maximiser and \(t=f(d)>0\).

In a neighbourhood of \(d\), the signs of all \(a_i\cdot d\) are fixed.
Write \(b_i=\operatorname{sgn}(a_i\cdot d)a_i\). The active vectors satisfy
\(b_i\cdot d=t\). Their tangent gradients are \(g_i=b_i-td\), in the
two-dimensional tangent plane \(d^\perp\).

The origin belongs to the convex hull of the active \(g_i\). Otherwise,
strict separation in the tangent plane provides a direction \(w\) with
\(g_i\cdot w>0\) for every active \(i\). Moving a sufficiently small distance
in the direction \(w\) on the sphere increases all active values. The
inactive inequalities have a positive gap and remain larger. This would
increase \(f\), contradicting maximality.

By Caratheodory's theorem in that tangent plane, choose at most three active
vectors and positive weights with

\[
td=\sum_{i\in I}\lambda_i b_i,\qquad
\lambda_i>0,\quad\sum_{i\in I}\lambda_i=1.
\tag{7}
\]

Choose such a representation with the fewest vectors.

With one vector, \(d\) is parallel to \(b_i\).

With two distinct vectors, write the weights as \(\lambda,1-\lambda\).
Taking the dot product of (7) with \(b_i-b_j\), and using equal norms and
equal active dot products, gives

\[
0=(2\lambda-1)(R^2-b_i\cdot b_j).
\]

The second factor is positive, so \(\lambda=1/2\) and \(d\) is parallel to
\(b_i+b_j\). The antipodal case is impossible because \(t>0\).

With three vectors, minimality makes their tangent gradients affinely
independent. Hence \(b_i-b_j\) and \(b_i-b_k\) are linearly independent, and
both are perpendicular to \(d\). Their cross product is parallel to \(d\).

In each case absorb the sign of the first vector as an overall sign.
Since \(f(d)=f(-d)\), the candidates are exactly those in (6). This proves
the lemma. \(\square\)

The equal-norm hypothesis matters in the two-active case. This reduction
is not asserted for unequal-radius input vectors.

## 4. Exact core optimisation certificate

For the 25 representatives in Section 2 the checker establishes

\[
\max_{\|d\|=1}\min_i(a_i\cdot d)^2
       =B=\frac{65+10s}{596}.
\tag{8}
\]

There are
\(25+2\binom{25}{2}+4\binom{25}{3}=9825\)
candidates in (6), all nonzero for this model. For each unnormalised
candidate \(E\), the checker finds an index \(i\) satisfying

\[
(a_i\cdot E)^2\le B(E\cdot E).
\tag{9}
\]

The finite direction lemma shows that (9) proves the upper bound in (8).
The checker separately proves

\[
\min_i\frac{(a_i\cdot D)^2}{D\cdot D}=B
\]

for (2), proving attainment. No trigonometric approximation, numerical
optimisation or tolerance participates in these assertions.

The ordered list of first-blocking indices for (9) has SHA256
`86666a18873e8162cbd45972710a11c336e69e88e87ce3eb8804ef2b25909a8f`.
This hash is a reproducibility check, not a substitute for rechecking (9).
The complete candidate list is generated from the small source fixture;
no search dump or large external certificate is required.

Because \(K=-K\), its projection is centrally symmetric. Its smallest
enclosing disk is centred at the origin: any disk of radius \(r\) containing
both \(x\) and \(-x\) has \(r\ge\|x\|\), as follows by averaging their squared
distances from the disk centre. Thus (8) also gives

\[
\min_d\operatorname{rad}(\pi_d\operatorname{conv}K)^2
       =R^2-B=\frac{787+293s}{298}=L^2.
\tag{10}
\]

This circumradius identity is for the symmetric core J80. It is not
asserted for the whole asymmetric J77.

## 5. Diameter theorem and passage consequence

For every direction \(d\), the projected pair \(a_i,-a_i\) has squared
distance \(4(R^2-(a_i\cdot d)^2)\). By (8), at least one such pair has
squared distance at least \(4(R^2-B)=4L^2\). Since the pair belongs to J77,

\[
\operatorname{diam}(\pi_dP)\ge2L.
\]

For the attaining direction \(D\), the checker checks all
\(\binom{55}{2}=1485\) vertex pairs. For \(z=v_i-v_j\), it proves

\[
\|z\|^2-\frac{(z\cdot D)^2}{D\cdot D}\le4L^2.
\tag{11}
\]

Equality occurs, in particular, for fixture vertices V8 and V15. The
diameter of a convex hull is the maximum of its vertex-pair distances:
write two hull points as convex combinations and apply the triangle
inequality to their difference. Consequently (11) proves (1).

Equation (5) gives \(\operatorname{diam}(\pi_dP)\le2R\) in every direction.
This maximum is attained by taking a direction perpendicular to an
antipodal pair in \(K\).

If a compact convex set lies in the interior of another convex body, its
diameter is strictly smaller. Indeed the interior inclusion has a positive
uniform clearance; extend a diameter segment at both ends by any smaller
clearance to obtain a longer segment in the outer body.

Rotations and translations preserve diameter, and scaling multiplies it.
For a strict projected passage this therefore gives

\[
2\lambda L\le\lambda\operatorname{diam}(\pi_{d_1}P)
 <\operatorname{diam}(\pi_{d_2}P)\le2R.
\]

Finally
\(R^2/L^2=(2797-75s)/2552\), proving (3). The strict inequality applies to
each individual passage scale; the supremum need only satisfy a weak upper
bound. We do not remove translations from J77's containment problem.

## 6. Analytic exclusion for an axial receiver

Let \(n=A/\|A\|\), the fivefold axis perpendicular to the decagonal face,
and put

\[
t_0^2=\frac{5-2s}{20},\qquad
r_0^2=\frac{25+11s}{10}=R^2-t_0^2,\qquad
\gamma_0=\arctan(t_0/r_0).
\tag{12}
\]

The checker verifies that all vertices satisfy
\(|v\cdot n|\ge t_0\). Thus the axial receiver shadow lies in the radius
\(r_0\) disk and has diameter at most \(2r_0\). Equality holds at antipodal
ring vertices.

The five core vertices with \(A\cdot v=(s-1)/4\) have common axial height
\(t_0\), transverse length \(r_0\), and sum \(5t_0n\); these identities are
checked exactly. Call them \(b_1,\ldots,b_5\).

Take an inner projection direction whose unoriented axis makes angle
\(0\le\gamma\le\gamma_0\) with the fivefold axis. Choose its sign so that
\(d=\cos\gamma\,n+\sin\gamma\,u\), where \(u\perp n\) is a unit vector
(the choice of \(u\) is immaterial when \(\gamma=0\)). For every ring vertex,

\[
b_i\cdot d\ge t_0\cos\gamma-r_0\sin\gamma\ge0.
\]

The mean of these five nonnegative dot products is \(t_0\cos\gamma\), so
one of them is at most that mean. Its antipodal partner belongs to J77.
The inner shadow therefore has diameter at least

\[
2\sqrt{R^2-t_0^2\cos^2\gamma}\ge2r_0.
\]

For any scale \(\lambda\ge1\), strict containment in the axial receiver
would require a strictly smaller diameter, an impossibility. This proves
the axial exclusion, allowing every translation and in-plane rotation.
The half-angle is about \(4.17^\circ\); the exact statement is (12).

This excludes an explicit cone of inner directions for one fixed receiver
axis. It does not exclude arbitrary receiver directions or all axial
receiver passages with inner axes outside the cone.

## 7. Trust boundary

The certificate checks use Python arbitrary-precision integers and
`fractions.Fraction`. The sign of \(a+b\sqrt5\) is decided algebraically,
by signs of \(a,b\) and comparison of \(a^2\) with \(5b^2\).
An independent rational-enclosure sign audit uses `math.isqrt`, including
small Pell conjugates that cause severe floating-point cancellation.

The geometric identification is checked against an independent exact
cupola construction. Face regularity and supporting-plane checks provide
additional input validation. The finite direction lemma, projection
interpretation, and analytic arguments are written proofs, not formalised
in a proof assistant. Correctness still relies on those arguments, the
source checker and the Python implementation. Floating-point exploration
is excluded from the proof and from the published certificate.
