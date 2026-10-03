# Capacity at most fourteen for the derived thirteen-label G24 branch

Actual author **six-tammes-2**, role **researcher**, 2026-10-03.
Ordinary algebra and convexity proof with a complete exact computational
certificate. Independent mathematical review and formalization of this
new result are pending.

**Theorem.** Let I=[14/25,593/1000]. Let X be any finite set of distinct
unit vectors in R^3, with p.q<=t for every different pair and some t in I.
Suppose thirteen distinct labels in X have the twenty original G20
contacts

```
0-5 0-6 0-7 0-11 1-2 1-4 1-10 1-12 2-4 2-8 2-10
4-8 5-7 5-9 5-11 6-11 7-12 9-10 9-11 10-12
```

and the four further contacts

```
5-12, 2-x, 9-x, 10-x,
```

where x is outside the original twelve labels. Then **|X|<=14**. Every
point outside this thirteen-point motif is arbitrary. No contacts,
degrees, locations, proximity, faces or contact-map cohort are prescribed
for those points. All additional core and added-point contacts are allowed.

This is the G24 **derived** by
[the five-cycle/degree reduction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/g20-five-cycle-routing/PROOF.md),
LEMMA9922. Here the source label13 denotes its fresh x. This literal mask
differs from the older fixed-incumbent G24: that mask adds
6-8,2-13,8-13,9-13 to G20. An edge count or the name G24 does not transfer
that older theorem to the present motif.

**Degree corollary.** In a fifteen-point t-code on I carrying original
G20, if5-12 is present, the complete contact degree at10 is exactly4.
Indeed9922 proves deg10 in{4,5} and derives the present fresh x if deg10=5,
for arbitrary finite codes. The theorem excludes that branch. No9813
physical-cohort, tree/forest or profile premise is needed for this corollary.
Its logical external dependency is precisely this part of9922.

[Independent review9950](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/g20-routing-audit/REVIEW.md)
confirms that parent implication and supplies a wider local geometry band.
Its full defining review and proof were read and bound to the original
signed body. The capacity theorem here retains its own entire closed I;
9950 is context, not a verdict on this new proof. Its separate physical
eleven-disk interface retains all9813 hypotheses and is not imported:
the two further points here remain arbitrary unit code points.

The actual-P branch and the5-12/deg10=4 branch remain. A triangle profile
such as A5/B6 is not ruled out in other branches. Whole-G20 arbitrary-three
capacity, occurrence of G20 in a relevant optimizer, and a new unconditional
global Tammes bound remain open. I is retained in full, including its
endpoints and the entire critical strip below the incumbent cosine.

## 1. Normalization by reflection, with no missing branch

Set a=1+t and r=2t/a. Normalize the coefficient basis as(p1,p2,p4), whose
Gram matrix is H_t=(1-t)Id+t11^T. Its eigenvalues1-t,1-t,1+2t are strictly
positive on I. Write

    <u,v>_t=(1-t)sum_j u_j v_j+t(sum_j u_j)(sum_j v_j).

For a contact side u.v=t, the two distinct unit common contact neighbors
are reflections across span{u,v}: if one is q, the other is
r(u+v)-q. The squared norm of their midpoint is2t^2/(1+t)<1 for0<t<1.
Thus this formula exhausts both possibilities, with the already specified
different label selecting the other one. It introduces no orientation
assumption. The original contact triangles first determine p8,p10,p12
by reflection from(p1,p2,p4).

The new contacts then determine

    x=r(p2+p10)-p1,
    p9=r(p10+x)-p2.

Next p5 and p10 are the two distinct common neighbors with product t
against p9 and p12. Put d=p9.p12. These two vectors are distinct and
cannot be antipodal, since they have positive product t with p10.
The general common-neighbor reflection gives

    p5=2t(p9+p12)/(1+d)-p10.

Direct calculation below gives1+d=2Q4/a^3>0. Finally, reflect consecutively
in the three original A triangles to obtain

    p0=r(p5+p7)-p12,
    p11=r(p0+p5)-p7,
    p9=r(p5+p11)-p0.

The last equation, after the first two substitutions, is

    p9=r^2(r+1)p5+r(r^2-2)p7+(1-r^2)p12.

Because0<r<1 on I, r(r^2-2) is strictly negative, so this equation
determines p7 uniquely. Then p0,p11 and p6=r(p0+p11)-p5 are determined.
This proves that EVERY realization of the prescribed thirteen labels,
up to an orthogonal isometry, has the following rational coordinates.
There is no surviving core-circle or radical parameter. These contacts
alone do not force the incumbent cosine: the family varies with t.
The final reflection-chain formula was also suggested by six-tammes-1
in campaign discussion; its scalar identities are checked here.

## 2. Positive integral coordinates

Let

    Q4=(1-t^2)(1+3t)+8t^4,     L=1+2t-t^2,
    Omega=a^5 Q4 L.

All these clearing factors are positive for0<t<1. The six B numerators
(denominator a^2) are

```
B1=(a^2,0,0), B2=(0,a^2,0), B4=(0,0,a^2),
B8=(-a^2,2ta,2ta), B10=(2ta,2ta,-a^2),
B12=(2t(1+3t),3t^2-2t-1,-2ta).
```

The new x and p9 have numerators

```
Xn=(3t^2-2t-1,2t(1+3t),-2ta),      x=Xn/a^2,
V=(2t(5t^2-1),(3t+1)(5t^2-1),-2ta(3t+1)),  p9=V/a^3.
```

Then d=2Q4/a^3-1. Define vector polynomials

```
Five=t a^2(V+a B12)-Q4 B10,
W0=1+6t+5t^2-28t^3-29t^4+94t^5+103t^6-56t^7,
W1=-2t^2(1-t)(3t+1)(3+13t+11t^2-7t^3),
W2=2ta(3t+1)(1+3t-3t^2-9t^3+4t^4),
Zero=2t(L Five+a W)-a Q4 L B12,
Eleven=2t(Zero+a L Five)-a^3 W,
Six=2t(a Zero+Eleven)-a^3 L Five.
```

The thirteen points p_i=Y_i/Omega are specified completely by

```
Y_i=a^3 Q4 L B_i                   i=1,2,4,8,10,12,
Y_x=a^3 Q4 L Xn, Y9=a^2 Q4 L V,
Y5=a^3 L Five, Y7=a^4 W,
Y0=a^2 Zero, Y11=a Eleven, Y6=Six.
```

[model.py](model.py) uses these ring operations only. The13 unit identities,
24 literal contacts,30 reflection scalar identities and the d/normal
formulas are all zero integer polynomials under [check.py](check.py).
There is no specialization, floating decision or unproved field inversion
in these69 generic checks. The preceding ordinary argument proves their
exhaustive interpretation. Core packing on the entire interval is not
assumed merely from these equalities; if an actual code exists its full
packing inequalities apply. The avoidance certificate below even holds
at parameters where this prefix itself fails packing.

## 3. A fixed cap and a bounded cut polytope

In the normalized coefficient basis put n=(-5,-14,20). Its physical
vector has

    ||n||_t^2=621-620t in[12667/50,1369/5].

The bound15 lies strictly between0 and||n|| throughout I. Consider

    K_t={y:<y,p_i>_t<=t for all13 labels},
    C_t={y in K_t:<y,n>_t<=15}.

The origin is strictly feasible. For each t in I, the positive-dependence
certificate proves that p0,p4,p9 are linearly independent and

    lambda0 p0+lambda4 p4+lambda9 p9+p11=0,
    lambda0,lambda4,lambda9>0.

The four exact Cramer sign obligations, with determinant orientation-1,
are checked throughout the CLOSED interval. For a recession vector h
of K_t all four indicated projections are nonpositive. Their strictly
positive dependence forces all four to vanish; spanning then gives h=0.
Therefore K_t and C_t are bounded full-dimensional polytopes. This step
does not assume contact-map geometry or hemisphere placement.

We prove the uniform cut bound

    every y in C_t satisfies ||y||_t^2<49/50.        (1)

Each vertex of C_t has three independent active normals selected from
the13 core planes and the cut plane, labeled99. All C(14,3)=364 triples
are covered by [CERTIFICATE.json](CERTIFICATE.json). Four determinants
vanish identically. For a nonsingular triple, let its exact Cramer data
be(D,W); its intersection is y=W/D. Positive factor cancellation and
the identity M W=rhs D are checked algebraically. At isolated zeros of
D the triple cannot define a vertex and is not interpreted as one.

Each leaf covers a CLOSED dyadic parameter cell. It certifies either

    49D^2-50<W,W>_t>0,                             (N)

or two inactive residuals

    H_j=row_j.W-rhs_j D>0,
    H_k=row_k.W-rhs_k D<0.                         (I2)

In(N), any intersection with D!=0 has squared norm<49/50. In(I2), if
D>0 it violates plane j; if D<0 it violates plane k. Hence it is
infeasible regardless of the determinant sign. No division by a
zero-containing interval or discarded determinant branch occurs.

The certificate has360 complete triple covers and4 identically singular
records, with367 leaves:32(N) and335(I2). Only three triple covers require
subdivision; maximum depth is4. Prefix-free complete binary trees prove
coverage of all t in I, including endpoints and all subdivision boundaries.
There are702 strict cap sign obligations plus4 boundedness signs.

Each sign polynomial is divided only by positive integer content and
powers of the eight known positive factors

    t,1+t,1-t,1+2t,3t-1,3t+1,Q4,L.

The exact clearing identity is checked. The remaining degree is at most17.
Positive Bernstein coefficients on the cell prove strict positivity on
its whole closed interval. [generate.py](generate.py) computes them with
integer affine substitution/factorial scaling; [check.py](check.py) uses
an independently implemented rational Horner affine substitution and
Bernstein conversion. [audit.py](audit.py) instead encloses every sign
polynomial by centered exact rational Taylor bounds, subdividing with a
complete closed binary cover when needed. Its sign method does not use
Bernstein coefficients. It shares the coordinate/Cramer reduction and
polynomial kernel, and is same-author arithmetic corroboration.

Thus EVERY feasible vertex has the bound in(1). Every point of the bounded
polytope is a convex combination of its vertices, and squared H_t norm
is convex. This proves(1) for the entire polytope. Arbitrary added points
are never assumed to be vertices or to have three active contacts.

## 4. At most one arbitrary addition

A unit vector avoiding all thirteen points cannot belong to C_t by(1).
Therefore it lies in the OPEN spherical cap<n,y>_t>15. For two unit
vectors in that cap, Cauchy--Schwarz in the tangent components, or the
angle sum bound about the cap axis, gives

    <y,z>_t>2*15^2/||n||_t^2-1
             >=450/(1369/5)-1=881/1369>593/1000.

Consequently two such points cannot belong to a t-code anywhere in I.
There is at most one additional point. This proves |X|<=14 and, using
the specified geometric implication of9922, the degree corollary.

## 5. Controls and trust boundary

At t=29/50 the checker verifies all13 rational unit points and all78
prefix packing pairs. The rational vertex for active planes(0,4,6)
satisfies all13 avoidance tests and has squared norm>1. Scaling that
vertex by the inverse square root of its norm gives one actual unit
addition: scaling toward the origin preserves every inequality with
positive right side. This control shows that one addition is possible
and that the capacity theorem is not a vacuous assertion about an
infeasible prefix. It is not a new packing record or fifteen-point code.

The complete normal/optimized generator and both exact replay methods,
plus scope, coverage, orientation and boundary controls, are recorded
in [VALIDATION.json](VALIDATION.json) and their compact expected outputs.
Runtime source is pinned. A timeout, UNKNOWN, incomplete sign cover or
incomplete triple list causes failure and is never interpreted as
nonexistence. No package, external runtime dataset or large proof corpus
is needed. These checks are by one author; independent review remains
pending and no earlier review verdict is transferred.

The ordinary trust boundary comprises common-neighbor reflection,
normalization, bounded-polytope vertex representation, convex squared
norm and the elementary cap inequality, together with the exact source
and complete sign/coverage certificate. The degree corollary additionally
imports9922's stated motif derivation. The graph/frame theorem9774 and
the moving-frame stopping gate are not logical premises of the main
capacity theorem. The classical cap/vertex method and earlier
[different thirteen-core completion work](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/thirteen-core-completion/PROOF.md)
are credited; the integer polynomial kernel is copied unchanged from
[the unrestricted polynomial model](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/twelve-core-polynomial-model/polynomials.py).
The new result is the complete conditional exclusion for this distinct
derived mask on I. No exhaustive historical-priority claim is made.
