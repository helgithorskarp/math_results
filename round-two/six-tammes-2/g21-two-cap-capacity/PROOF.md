# Original G20 plus5-12 has capacity at most fourteen on the full cosine band

Actual author **six-tammes-2**, role **researcher**, 2026-10-03.
This is an ordinary exhaustive normalization and convexity proof with a
complete exact sign/coverage certificate. Independent mathematical review
and formalization of this new result are pending.

**Theorem.** Let I=[14/25,593/1000]. Let X be any finite set of distinct
unit vectors in R^3 with every distinct-point product at most t, for some
t in I. Suppose twelve distinct labels in X have the original G20 contacts

```
0-5 0-6 0-7 0-11 1-2 1-4 1-10 1-12 2-4 2-8 2-10
4-8 5-7 5-9 5-11 6-11 7-12 9-10 9-11 10-12,
```

and **5-12** is also a contact. Then **|X|<=14**. All points outside these
TWELVE labels are arbitrary. Every extra core and added-point contact is
allowed. No actual thirteenth point, contact degree, face/cohort, support,
location, proximity or optimizer premise is imposed for this capacity
proof. Every endpoint and the entire critical strip of I are retained.

This removes the fresh-x premise of
[the earlier derived-G24 exclusion9966](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/derived-g24-capacity/PROOF.md).
That earlier result required5-12 and a thirteenth point contacting2,9,10.
Here the entire5-12 branch is excluded for fifteen points, including
complete degree10four. The new proof supplies its own exhaustive
normalization and regenerates the entire two-cap certificate. It does
not import the earlier actual-x capacity theorem as a premise.

**Routing corollary.** By
[9922's finite-code two-branch theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/g20-five-cycle-routing/PROOF.md),
any fifteen-point t-code on I carrying original G20 must have the
undivided actual pentagon P=(5,7,12,10,9); its three additional points
lie strictly in the complementary eleven-disk. Only this corollary
imports9922. No9813 physical-cohort, triangle-tree, face census or A4/B7
assignment is needed. The actual-P arbitrary-three branch, whole original
G20 capacity and global occurrence/optimality remain unresolved. An
entire triangle-size profile such as A5/B6 is not excluded in other
branches. No new unconditional Tammes15 separation bound is claimed.

## 1. Exhaustive two-candidate normalization

Write a=1+t, b=1-t, c=1+2t and r=2t/a. Normalize the coefficient basis
as(p1,p2,p4). Its Gram matrix is H_t=(1-t)Id+t11^T, where1 is the all-ones
column. Eigenvalues1-t,1-t,1+2t are strictly positive on I. Put

    <u,v>_t=(1-t)sum_j u_j v_j+t(sum_j u_j)(sum_j v_j).

For a contact side u.v=t, two distinct unit common contact neighbors are
reflections across span{u,v}: if one is z, the other is r(u+v)-z. The
common-neighbor midpoint has squared norm2t^2/(1+t)<1 for0<t<1, so these
are exactly the two solutions. Distinct prescribed labels select the
other solution. This introduces no orientation quotient or discarded
reflection branch. The three B reflections determine p8,p10,p12.

The additional5-12 contact makes(p5,p7,p12) equilateral. The original
A triangles give consecutively

    p0=r(p5+p7)-p12,
    p11=r(p0+p5)-p7,
    p9=r(p5+p11)-p0.

Substitution yields

    p9=r^2(r+1)p5+r(r^2-2)p7+(1-r^2)p12.          (1)

Thus its product with p12 is intrinsic, independent of the placement of
that A patch:

    d=p9.p12=2Q4/a^3-1,
    Q4=(1-t^2)(1+3t)+8t^4>0.                     (2)

Now p10 and p12 are known distinct unit vectors with product t. The
unknown p9 is unit and has products t with p10, and d with p12. Its
Gram determinant is

    1-2t^2-d^2+2t^2d
      =16t^2 b^2 c L^2/a^6>0,
    L=1+2t-t^2=1+t(2-t)>0.                      (3)

The two independent affine plane equations therefore intersect the unit
sphere in exactly two distinct points. A rational solution is

    V/a^3,
    V=(2t(5t^2-1),(3t+1)(5t^2-1),-2ta(3t+1)).

Its unit and both plane identities are checked exactly. The other solution
is its orthogonal reflection in span{p10,p12}, explicitly

    p9'=2[A p10+B p12]-V/a^3,
    A=t(1-d)/(1-t^2), B=(d-t^2)/(1-t^2).

Every denominator is strictly positive on I. Direct multiplication gives

    p9'.p2-t
      =b(5t^2-1)(1+7t+7t^2b)/a^5>0,             (4)

since t>=14/25>1/sqrt5 and0<t<1. This contradicts the packing comparison
between the distinct labels2 and9. Thus exactly the first rational p9
can occur in a code. Equation(4) is a whole-interval factorization,
including endpoints, not a sampled or numerical branch selection.

Both p5 and p10 have product t with p9 and p12. They are distinct unit
common neighbors. Since1+d=2Q4/a^3>0 and |d|<1 by(3), their general
reflection formula forces

    p5=2t(p9+p12)/(1+d)-p10.

Equation(1) then determines p7 uniquely: r(r^2-2)<0 throughout I. Finally
p0,p11 and p6=r(p0+p11)-p5 are determined. This proves that EVERY physical
realization of the literal21 contacts has the rational coordinates below,
up to an orthogonal isometry. No moving chart, radical or free angle
remains. Contacts alone do not force the incumbent cosine tau.

## 2. Positive integral coordinates and exact prefix feasibility

For the six B labels define numerators with denominator a^2:

```
B1=(a^2,0,0), B2=(0,a^2,0), B4=(0,0,a^2),
B8=(-a^2,2ta,2ta), B10=(2ta,2ta,-a^2),
B12=(2t(1+3t),3t^2-2t-1,-2ta).
```

With V,Q4,L as above, define vector polynomials

```
Five=t a^2(V+a B12)-Q4 B10,
W0=1+6t+5t^2-28t^3-29t^4+94t^5+103t^6-56t^7,
W1=-2t^2(1-t)(3t+1)(3+13t+11t^2-7t^3),
W2=2ta(3t+1)(1+3t-3t^2-9t^3+4t^4),
Zero=2t(L Five+a W)-a Q4 L B12,
Eleven=2t(Zero+a L Five)-a^3 W,
Six=2t(a Zero+Eleven)-a^3 L Five,
Omega=a^5 Q4 L>0.
```

The TWELVE points p_i=Y_i/Omega are

```
Y_i=a^3 Q4 L B_i                  i=1,2,4,8,10,12,
Y9=a^2 Q4 L V, Y5=a^3 L Five, Y7=a^4 W,
Y0=a^2 Zero, Y11=a Eleven, Y6=Six.
```

[model.py](model.py) implements these ring formulas. The coordinate
formulas are credited to9966, now with their weaker literal-mask
interpretation proved exhaustively above. No actual extra point from
that source is assumed. [geometry.py](geometry.py) checks all73 generic
integer identities: twelve units,21 literal contacts, all scalar
reflections and A-chain identities, intrinsic d, both p9 candidates,
strict discriminant/pruning factorizations, both cap norms and the sole
weak prefix packing factorization. There is no quotient-field inverse,
float or specialized parameter in these checks.

There are45 noncontact core pairs. All44 except6-8 have strictly positive
cleared packing gaps throughout closed I, verified by both exact sign
replays. For6-8, removal of only strictly positive factors and positive
integer content leaves exactly

    (3t^2-1)(23t^3+17t^2+t-1).

The cubic is positive for t>1/2; its value is at least53/8 there. Therefore
the normalized twelve-point family is itself a code precisely when
**3t^2-1>=0** on I. Equality is retained:6-8 becomes an additional contact.
All other noncontacts remain strict. This useful prefix classification
is not an extra hypothesis of the capacity certificate, which covers
all of I, even where the prefix fails packing.
The sole-gap factor agrees with the independently published
[9984 refinement of the earlier thirteen-label motif](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/derived-g24-audit/PROOF.md).
That prior result additionally supplies uniform fourteen-point attainment
for its stronger mask. Those classification/sharpness facts are credited
and are not asserted newly discovered here. Its capacity theorem is not
an input to this weaker-mask two-cap proof.

## 3. Two fixed caps and the bounded cut avoidance polytope

In the coefficient basis set

    n1=(-5,-14,20), cut1=15,
    n2=(-8,12,-5),  cut2=9.

Their physical squared norms are exactly

    ||n1||_t^2=621-620t in[12667/50,1369/5],
    ||n2||_t^2=233-232t in[11928/125,2577/25].

Both cuts are positive and strictly below the respective normal norm.
Let

    K_t={y:<p_i,y>_t<=t for all twelve labels},
    C_t=K_t intersect{<n1,y>_t<=15,<n2,y>_t<=9}.

The origin is strictly feasible. A complete positive-dependence
certificate, using only core normals, proves that p0,p4,p9 span R^3 and

    lambda0 p0+lambda4 p4+lambda9 p9+p11=0,
    lambda0,lambda4,lambda9>0.

Its four strict Cramer signs hold throughout CLOSED I. If h is a
recession vector of K_t, the four projections are all nonpositive.
Strict positive dependence forces them all to vanish; spanning gives
h=0. Hence K_t and C_t are bounded full-dimensional polytopes, without
any contact-face or hemisphere-placement assumption.

We prove

    every y in C_t has ||y||_t^2<49/50.            (5)

Every vertex of C_t has three independent active normals among its
fourteen planes: twelve core planes and the two cap cuts, labeled98/99.
ALL C(14,3)=364 triples appear in
[CERTIFICATE.json](CERTIFICATE.json). Four are identically singular;
360 have complete closed parameter covers with367 leaves:31 short and
336 opposite-residual infeasibility leaves, maximum depth4.

For a nonsingular triple, exact Cramer data(D,W) give y=W/D. The cleared
identity M W=rhs D is checked, including every positive-factor cancellation.
At isolated zeros of D this triple cannot define a vertex and no point
is inferred from division. Each CLOSED dyadic cell certifies either

    49D^2-50<W,W>_t>0,                             (N)

or two inactive residuals with opposite strict signs

    H_j=row_j.W-rhs_jD>0, H_k<0.                  (I2)

For(N), any defined intersection has squared norm<49/50. For(I2), if D>0
it violates plane j, and if D<0 it violates plane k. Thus no determinant
branch or possible feasible intersection is silently deleted.

The complete prefix-free binary covers include both endpoints and every
subdivision boundary. There are703 cap sign obligations plus four for
boundedness, and the44 strict prefix packing gaps, **751 strict sign
obligations in total**. Each polynomial is divided only by positive integer
content and powers of the known strictly positive factors

    t,1+t,1-t,1+2t,3t-1,3t+1,Q4,L.

Every clearing identity is checked. In particular3t^2-1, which can vanish
inside I, is NEVER a canceled positive factor. Integer Bernstein
coefficients generate the certificate; a separate rational Horner/affine
Bernstein implementation replays every sign; a centered exact rational
Taylor implementation supplies a different complete enclosure route.
They share coordinate/Cramer reduction and the integer polynomial kernel,
and are same-author arithmetic corroboration, not independent peer review.

All feasible vertices satisfy(5). Every point of the bounded polytope
is a convex combination of its vertices and squared H_t norm is convex.
Thus(5) holds for all of C_t. Arbitrary added points are never presumed
to be vertices, to have active contacts or to lie near a fixed configuration.

## 4. At most two arbitrary additions

A unit vector avoiding all twelve core points cannot belong to C_t by(5).
Consequently it belongs to at least one of the two OPEN caps

    <n1,y>_t>15,        <n2,y>_t>9.

For a positive cut b below the norm of n, any two unit vectors in the
open cap<n,y>_t>b have product strictly greater than
2b^2/||n||_t^2-1, by the tangent-component Cauchy--Schwarz inequality or
by adding their angles about the cap axis. For the first cap this lower
bound is at least881/1369>593/1000, so it contains at most one code point.

For the second cap use the **pointwise** inequality in t, rather than
comparing its worst lower bound with the largest parameter:

    2*9^2-(1+t)||n2||_t^2=232t^2-t-71
      >=747/625>0 on I.

Its derivative464t-1 is positive throughout I, and the displayed lower
value is attained at14/25. Therefore2*9^2/||n2||_t^2-1>t for every t in I.
The second cap also contains at most one code point. An overlapping pair
of caps still has at most two code points in its union. Every arbitrary
addition is in that union, so |X|<=12+2=14. This proves the theorem and,
using9922, the routing corollary.

## 5. Reproduction, control and remaining scope

At t=29/50 the exact control verifies all twelve units/all66 core packing
pairs. The rational unit vector

    x=(3t^2-2t-1,2t(1+3t),-2ta)/a^2

passes all twelve additional packing comparisons. A rational vertex
supported by(0,4,6) passes all thirteen avoidance comparisons against
that prefix and x, and has squared norm>1. Radially scaling it to norm1
preserves all inequalities with positive right side. Thus TWO actual
additional unit points are possible at this parameter, yielding a
fourteen-point control. The capacity bound is nonvacuous and attained
somewhere in I. This is no new packing record or fifteen-point construction.
The optional x appears only in this control, never as a theorem hypothesis,
a cap plane or an actual point assumed in the exhaustive normalization.

[README.md](README.md) gives serial standard-library commands.
[SYSTEM.json](SYSTEM.json) fixes the literal mask and arbitrary-point
quantifier. Runtime pins, complete normal/optimized results and scope,
coverage, arithmetic orientation and endpoint controls are recorded in
[VALIDATION.json](VALIDATION.json), [EXPECTED.json](EXPECTED.json),
[AUDIT_EXPECTED.json](AUDIT_EXPECTED.json) and [CONTROLS.json](CONTROLS.json).
A timeout, UNKNOWN, incomplete cover or partial enumeration is failure
and supplies no exclusion. Floating discovery streams are not proof inputs.

The main trust boundary is ordinary common-neighbor reflection,
exhaustive two-plane sphere intersection, strictly positive packing
branch pruning, bounded-polytope vertex representation, convex norm and
the elementary cap inequality, plus the complete exact source/certificate.
The corollary additionally imports9922's stated local two-branch routing.
Its independent9950 review confirms that parent, not this new capacity
result. Neither its wider bands nor its9813 physical residual interface
are transported here. The newer9972 A4/B7 incidence theorem remains
complementary scoped research, including its106 shared-ear cases and
52 strict-improvement disjoint maps. It is not a capacity premise.
Fresh independent REVIEW9984 confirms9966 on its original thirteen-label
mask and band; its full review and proof were read and bound to the signed
body. That verdict also does not assess the present weaker-mask result.

The new result removes the entire5-12 branch from fifteen-point original
G20 codes on I. The actual-P three-arbitrary-point problem, other physical
profile completions, original-G20/global occurrence and an unconditional
Tammes15 bound remain open. Classical reflection, convexity and cap/sign
methods and the credited kernels are not asserted new; no exhaustive
historical-priority claim is made.
