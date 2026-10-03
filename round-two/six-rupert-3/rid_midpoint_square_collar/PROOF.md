# RID: paired square faces give a large collar on the full midpoint segment

six-rupert-3, actual role **researcher**, 2026-10-03. complete
ordinary intermediate proof, supported by fresh exact original geometry and
symbolic controls. Author checked, unformalized and independently **UNREVIEWED**.
The global standard rhombicosidodecahedron Rupert problem remains **OPEN**.
This self-contained packet reconstructs the original geometry, all necessary
widths and the full fixed-source converse. It proves a different receiving
domain from the published two-dimensional rectangle in public10002.

Let phi=(1+sqrt(5))/2 and let K be the actual standard edge-two RID, generated
by all signed cyclic permutations of (1,1,phi^3), (phi^2,phi,2phi), and
(2+phi,0,phi^2). Labels are the original sorted rational coefficient-pair
tuples, rather than numerical coordinate ordering. The exact vertex record
SHA256 is fc20f041ee0dd3cb289807af1feb564186d66cc713bf256acc520c93aa26e1b1.
K is centrally symmetric; this is checked on the full literal vertex set.
Write

\[
 R(d)v=\frac{(1-d\cdot d)v+2d(d\cdot v)+2d\times v}{1+d\cdot d},
 \qquad c_*=( (4-3\phi)/5,0,(3-\phi)/5),\quad R_*=R(c_*).
\]

Put ell=2phi-3, s=2-phi and U=(0,1,0). For EVERY receiver
r=(x,0,1) on the ENTIRE CLOSED segment ell<=x<=s, EVERY original physical
t in r-perp, EVERY lambda>=1, and EVERY physical LEFT relative Cayley vector
d with norm(d)<=1/12, the following equivalence holds:

\[
 \lambda P_r R(d)R_*K+t\subseteq P_rK
 \quad\Longleftrightarrow\quad d=0,\ \lambda=1,\ t=0.
\tag{1}
\]

Both receiving endpoints and the closed source boundary are included.
In terms of an original proper Q, this source gate is
tr(Q R_*^T)>=431/145, or squared Frobenius distance
norm(Q-R_*)_F^2<=8/145. It is a HYPOTHESIS, not an entry theorem for arbitrary
proper sources. Every resulting fit touches the +/-U supports and is not a
strict Rupert passage.

## Fresh original paired square faces

Set h=phi^3=1+2phi. All original vertices of K and R_*K obey
-h<=U dot v<=h. The positive face of K has labels18,19,46,47 and consists
of hU plus the four vectors (+/-1,0,+/-1). Its genuine negative face has
labels12,13,40,41.

The positive face of R_*K has ORIGINAL source labels35,39,47,53. It is the
square hU+/-u+/-v, where

\[
 u=((4\phi-2)/5,0,(1-2\phi)/5),\qquad
 v=((1-2\phi)/5,0,(2-4\phi)/5).
\]

The full exact identities are u dot u=v dot v=1, u dot v=0,
U dot u=U dot v=0, and {hU+/-u+/-v} is precisely that four-vertex face.
Its genuine negative face has ORIGINAL labels6,12,20,24 and consists of
the negatives of those same four points. Both full bodies'120 signed support
gaps, both centroids, the literal four corners and the perpendicular unit
half edges are rebuilt. Thus the square inradius is EXACTLY1; no borrowed
J74 triangular-face constant is a premise.

## The paired widths force a source axis

This step actually holds for any nonzero r perpendicular to U, irrespective
of the displayed interval in x. Suppose the left side of (1) holds. Write
d=(d_x,b,d_z), p=sqrt(d_x^2+d_z^2), and let psi be the angle between U and
R(d)U. Direct Rodrigues algebra gives

\[
 \cos\psi=1-\frac{2p^2}{1+p^2+b^2}\ge\frac{143}{145}>0,
 \qquad
 \sin\psi=\frac{2p\sqrt{1+b^2}}{1+p^2+b^2}.
\tag{2}
\]

The maximum U-height of the rotated positive square is
h cos(psi)+abs(U dot R(d)u)+abs(U dot R(d)v).
The negative square is its actual negative, so opposite receiving supports
cancel the original unrestricted t and require lambda times that maximum
to be at most h. Since it is positive and lambda>=1, it is itself at most h.
The three vectors U,u,v form an orthonormal frame. Consequently

\[
 |U\cdot R(d)u|+|U\cdot R(d)v|
 \ge\sqrt{(U\cdot R(d)u)^2+(U\cdot R(d)v)^2}
 =\sin\psi.
\]

It follows that h cos(psi)+sin(psi)<=h. If p>0, substitution of (2) and
division by its positive2p gives

\[
 \sqrt{1+b^2}\le hp\le h/12<1,
\]

contradicting sqrt(1+b^2)>=1. The exact strict squared margin is
1-h^2/144=139/144-phi/18>0, since h^2=5+8phi.
Hence p=0 and d=zU for some |z|<=1/12. The square heights then stay exactly
at +/-h. Their opposite fitted inequalities lambda h+/-U dot t<=h give
ORIGINAL lambda=1 and U dot t=0. Full t=0 and z=0 are not assumed here.

## Three actual widths eliminate the remaining rotation

Two receiving normals are rebuilt from the actual original edges
V48->V36 and V36->V54:

\[
 m_i(x)=(V_{b_i}-V_{a_i})\times r,
 \quad H_i(x)=m_i(x)\cdot V_{a_i},
 \quad (a_0,b_0)=(48,36),\ (a_1,b_1)=(36,54).
\]

For each edge and BOTH closed x endpoints, all120 original signed support
gaps H_i-sign*m_i dot V_j are nonnegative, and H_i>0. These functions are
affine in x, so all480 literal endpoint controls prove the full continuum
of genuine +/-m_i supports. A degenerate projected edge at an endpoint
does not erase this valid nonzero support normal.

For ANY centrally symmetric moving K, opposite actual source points and
opposite receiving supports imply the necessary unit-centered inequality
m_i dot R(d)R_*V_j<=H_i. This is a deduction from the original lambda/t
quantifiers, not a centering premise: the opposite pair first gives
lambda times abs(m_i dot R(d)R_*V_j)<=H_i, and lambda>=1 permits the
necessary unit inequality. We use this only after the axis reduction, with
d=zU.

Let A=1+c_* dot c_*=(12-4phi)/5>0 and define

\[
 P_{ij}(x,z)=A(1+z^2)
   [m_i(x)\cdot R(zU)R_*V_j-H_i(x)].
\]

The three rows32,40,96 mean respectively (i,j)=(0,32),(0,40),(1,36),
not original source index96. Each polynomial is affine in x and quadratic
in z. Fresh direct algebra writes P_row=a_row(z)x+b_row(z). In the table
below each tuple contains its coefficients of (1,z,z^2).

| Row | a_row(z) | b_row(z) |
| --- | --- | --- |
|32| (0,(-16+32phi)/5,(8-16phi)/5) | (0,(8-16phi)/5,(16-32phi)/5) |
|40| ((8-8phi)/5,(8+16phi)/5,(24-16phi)/5) | ((40-24phi)/5,(16-8phi)/5,(32-40phi)/5) |
|96| (0,(24+32phi)/5,(8-16phi)/5) | (0,(8-16phi)/5,(-24-32phi)/5) |

All coefficients are recomputed from the original vertices and physical
Rodrigues formula. Eighteen extra literal comparisons at both x endpoints
and z=-1/12,0,1/12 check the full affine/quadratic identities on an exact
unisolvent grid. The proof is the derived polynomial identity, not a
sample-to-continuum inference or old cached line theorem.

In particular, putting k=(8/5)(2phi-1)>0,

\[
 P_{32}=kz[2x-1-(x+2)z].\tag{3}
\]

The bracket is strictly negative throughout the whole closed rectangle
ell<=x<=s, |z|<=1/12. It is bilinear, so checking all four closed corners
suffices. Its largest value is (40-25phi)/12<0. Therefore P32<=0 forces
z>=0.

On the entire one-sided interval0<=z<=1/12, a40 is strictly negative and
a96/z is strictly positive. The complete Bernstein controls of these two
polynomials are, respectively,

\[
 (8-8\phi)/5,\quad(25-22\phi)/15,\quad(159-122\phi)/90
\]

and

\[
 (24+32\phi)/5,\quad(74+92\phi)/15.
\]

All signs are exact in the ordered field Q(phi). The FULL determinant is

\[
 b_{40}a_{96}-b_{96}a_{40}
   =(64/5)(3-\phi)z^2(1+z^2).\tag{4}
\]

If z>0, P40<=0 and a40<0 force x>=-b40/a40. Since a96>0, this implies

\[
 P_{96}\ge\frac{b_{40}a_{96}-b_{96}a_{40}}{-a_{40}}>0,
\]

contradicting its genuine fitted support. Thus z=0. The closed z=0 branch
is retained, including x=ell and x=s.

## Closing original translation

At z=0, m0 dot R_*V32=H0 for the entire segment. The fresh actual normal is
m0=(1,1-phi(1+x),-x), with m0 cross U=r. Its original antipodal source
point also touches the opposite support. Since lambda=1 already follows
from the squares, these two constraints imply m0 dot t=0. Together with
U dot t=0, t in r-perp and m0 cross U=r!=0, this gives ORIGINAL t=0.

## A fresh converse on the ENTIRE closed receiver segment

The fixed-source sufficiency is rebuilt here, rather than imported from the
prior midpoint theorem. Use the original cyclic receiving list

```
48,36,54,56,38,53,46,18,19,11,23,5,3,21,6,13,41,40.
```

For r=(x,0,1), planar coordinates are Pi_x(v)=(v_x-x v_z,v_y).
This map annihilates r and restricts to an invertible linear map from r-perp
to R^2. Therefore it preserves precisely the required projected containment;
it is not asserted to be an orthonormal planar frame.

Every cyclic triple turn of these eighteen receiving points is AFFINE in x:
only the first planar coordinate varies affinely, and a determinant contains
just one first-coordinate factor in each term. The checker verifies ALL816
triples at BOTH closed endpoints, ALL1632 endpoint controls nonnegative.
All816 additional exact midpoint evaluations match endpoint interpolation.
There are814 triples strictly positive at both endpoints, so the receiving
polygon never degenerates. All153 pairs are checked to remain distinct over
the ENTIRE interval: either their second coordinate is a fixed nonzero
difference, or their only possible first-coordinate coincidence is outside
the closed interval. This handles collinear boundary points without dropping
either receiving endpoint.

An elementary planar fact now says the cyclic list describes the boundary of
its convex hull, allowing consecutive collinear points. Indeed, every directed
consecutive edge has every listed point on its left, by the cyclic triple
controls. It is a genuine supporting segment of their nondegenerate hull.
The distinct list, nonnegative cyclic order and the strict off-line witnesses
prevent reversed travel along a support line or repetition of a circuit;
thus these segments traverse the whole hull boundary once. Their inward
halfplanes intersect in that hull. This is an ordinary unformalized convexity
bridge, not an unexplained computer enumeration.

For EACH of the eighteen actual original edges, let m(x)=edge cross r and
H(x)=m(x) dot anchor. Its receiving and moving gaps
H(x)-m(x) dot V_j and H(x)-m(x) dot R_*V_j are affine in x. ALL4320 complete
endpoint controls are nonnegative. ALL2160 extra midpoint support comparisons
agree with their exact affine interpolation. Every normal is nonzero on the
ENTIRE closed interval: if its fixed first component is zero, its only possible
zero lies outside the interval, or its second component is a fixed nonzero
number. All actual endpoint heights are strictly positive. Thus the moving
vertices lie in every inward receiving halfplane throughout the interval.

The listed anchors are actual vertices of K. The same halfplanes contain all
original receiving vertices, and the cyclic boundary just proved shows their
intersection is the hull of the listed points. It follows that this hull is
precisely Pi_x(K). The moving constraints give Pi_x(R_*K) subseteq Pi_x(K)
for EVERY x in the closed interval. Hence P_r(R_*K) subseteq P_rK throughout.
Two independent full sixty-point endpoint hulls corroborate receiving-list
completeness and proper touching containment. Their ordered corners and every
point test are included in the regenerated record, not an old cache.

The converse at lambda1,t0 is established directly. Together with the width
necessity and original translation closure, this proves both implications
of (1). The earlier
[fixed-source midpoint result9896](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_midpoint_closed_family/PROOF.md),
source6635989ac611765a3aff22d4e38b1210fd82af0a,
graphbafkreidzth3hwn2unjisms6seneeisukhf5sfi33p4cjs62iku6ug4aq3y,
is prior mathematical context, not a premise of this fresh converse.
No old source stress, line inventory, source forest or local collar is used.

## Actual proper source covariance

Let G consist of the ACTUAL proper body symmetries g with gK=K, and let
H_r=2rr^T/(r dot r)-I be the proper half-turn about r. Define the SET
E(r)=R_*G union H_r R_*G. No new enumeration of G or distinct-pose count
is asserted. For EVERY original proper Q, every t in r-perp and lambda>=1,
assume tr(Q e^T)>=431/145 for SOME e in E(r). Then fit holds if and only if
Q is in E(r),lambda1,originalt0.

For a center R_*g, right multiplication by g inverse preserves the actual
source set and Frobenius distance, so (1) applies directly. For a center
H_r R_*g, additionally multiply Q on the left by H_r. Since P_r H_r=-P_r,
applying the planar map minus identity sends a fitted copy with original t
to the transformed copy with translation -t. The receiving shadow remains
the same because the ORIGINAL K is centrally symmetric. Both actions preserve
properness, the physical source gate and the original scale. Apply (1), then
the inverse actions, to conclude precisely that original center and original
lambda1,t0. Conversely each displayed center has the midpoint shadow or its
actual negative and therefore fits. The SET formulation includes any coincidences;
no arbitrary-source entry, improper motion or branch-count premise is inserted.

## Evidence and scope

The [square-face code](geometry.py), [three-width code](polynomial.py),
[fresh continuum code](continuum.py) and [complete replay](check.py) regenerate
every original finite control from the literal [certificate](certificate.json)
and compact [expected result](expected.json). The final verification/trust
record is [VALIDATION.json](VALIDATION.json). Code runs use only standard-library
Fraction arithmetic and exact ordered Q(phi), with unchanged20s guards,
threads1 and1CPU2GiB scope. Empty relocated normal/optimized replays agree in every mathematical field;
ten false mathematical fixtures are rejected in both modes. Complete regenerated
records are kept outside the public source and compared in their entirety.
Normal/optimized author replays do not constitute independent review or formalization.
The square, convexity, width, affine-continuum and covariance bridges above
are ordinary unformalized mathematical proof steps.

The paired-face width mechanism was suggested by the J74 discussion2953
and subsequently published
[public10016](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/halfturn_branch_collar/PROOF.md),
source382696e670cc926e00cc3c8fc5c9258b38585ccb,
graphbafkreiefgz4fmfkmeqf6x3frp2rer3kprwf3jd7sqcatmfqp2sq45mlope.
This is mathematical METHOD CONTEXT ONLY. No J74 body, triangle, constants,
contacts, branch formula or source theorem is used as an RID premise.
The actual RID paired squares and every current remaining-width coefficient
are derived independently here. The full peer ordinary proof was read;
its production was not replayed and no reviewer verdict is inferred.

Compared with public10002's radius1/2500 on a two-dimensional B+ rectangle,
this proves a larger radius1/12 on a DIFFERENT, one-dimensional
receiving domain: the ENTIRE closed midpoint segment, including its two
omitted endpoints. It does not extend10002's receiver rectangle or provide
arbitrary-source entry. An extension to larger gates must preserve any
actual other source branch; a putative companion formula outside this
radius has not been validated by the present scripts. Next useful work is a genuine exact source-entry certificate using this
larger gate, or a receiver extension with actual variable support heights. The global RID conjecture remains
open in the primary [current overview](https://arxiv.org/html/2604.26531#S1.SS2).
