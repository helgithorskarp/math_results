# Excluding all 29 sole-A-corner A4/B7 contact masks

Actual author: **six-tammes-1**, role **researcher**, round two, pass27.
This is an author-written ordinary geometric reduction with exact finite
polynomial certificates. Two different same-author programs check it.
Independent mathematical review and formalization are pending.

## 1. Literal theorem and physical corollary

Put J=[7/13,3/5]. For each row of [CERTIFICATE.json](CERTIFICATE.json),
there do not exist **fifteen distinct unit vectors in R^3**, labeled

    {0,5,6,7,9,11} union {1,2,4,8,10,12,20,21,22},

and any c in **closed J** such that every side of

    A=((0,5,11),(0,6,11),(0,5,7),(5,9,11)),

of that row's seven `B_triangles`, and of its six `cross` edges has
inner product c. All29 rows, with their complete B triangles and cross
edges, are explicit in the certificate. Their indices in the immutable
9972 `geometric_maps` list are

    2,4,5,10,12,13,15,18,19,24,26,30,34,35,37,
    38,39,40,46,47,48,49,51,52,54,55,57,60,63.

This is an exclusion of the literal **required contacts**. Additional
contacts are allowed. No noncontact packing inequality, face, degree,
connectedness, convexity, cohort, irreducibility, optimizer, or selected
coordinate location is needed for this individual theorem. The `quad`
field names a four-contact cycle; it need not be an actual face.
In particular, the theorem excludes unit c-codes with these masks.

For the **physical corollary**, import **ALL** hypotheses of
[9972](../b7-contact-incidence/PROOF.md), including its complete A4/B7
actual triangle-component assignment and the full inherited
[9813](../connected-map-filters/PROOF.md) cohort. Use
[10038](../b7-disjoint-support/PROOF.md) to exclude the106 shared-ear
prefixes on the same closed J, hence to make the A and B supports
physically disjoint. The complete map must then be one of the parent53
closed-band maps. The theorem above removes29 of them, leaving exactly
these **24 necessary maps**:

    8,36,42,43,44,45,61,62,64,65,66,67,
    68,69,70,71,72,73,74,75,76,77,78,79.

Parent9972 already proves that map8 forces c=tau, the maintained
incumbent cosine. Therefore a strict improvement c<tau leaves the
**23** maps in that list other than8. Every quadrilateral in each of
those23 has **two A and two B corners**. Map8 remains only a necessary
critical candidate, with its three sole-A-corner quadrilaterals.
None of these surviving maps is asserted realizable. This neither
improves an unconditional Tammes15 upper bound nor proves that an
optimizer enters this cohort or the A4/B7 assignment. Reversed
assignments, other triangle profiles, and the global problem remain open.

## 2. Forced reflection coordinates, retaining both spatial orientations

Set

    r=2c/(1+c), D=2-r, Q=2r^3+2r^2-3r.

Closed J maps exactly to [7/10,3/4]. The independent B root vectors
p1,p2,p4 form a basis: their physical Gram matrix has diagonal1 and
off-diagonal c. In coefficient coordinates put

    N(v,w)=2(1-r) sum_i(v_i w_i)+r(sum_i v_i)(sum_j w_j).

Then v.w=N(v,w)/D. The numerator metric has diagonal D and
off-diagonal r; its eigenvalues are2-2r (twice) and2+r, all strictly
positive on the closed band. Thus this is a genuine real basis, not a
chosen numeric configuration. Changing its orientation covers all of O(3).

For two distinct equilateral triangles on the same edge u,v, their
opposite unit vertices z,x are the two solutions of the two independent
linear contact equations and the unit equation. Since u.v=c, their sum
is 2c(u+v)/(1+c), so

    x=r(u+v)-z.

Global distinctness prohibits choosing z again. Every original A ear and
every fresh B triangle is therefore forced by this formula. The two
programs reconstruct all nine B coordinates and verify every whole norm
and required B contact polynomial. Their forward and reverse attachment
orders differ, and no floating coordinates enter either computation.

For the A roots (p0,p5,p11) and leaves (p6,p7,p9), the same formula gives

    [ p6 ]   [ r -1  r ] [ p0  ]
    [ p7 ] = [ r  r -1 ] [ p5  ].
    [ p9 ]   [-1  r  r ] [ p11 ]

Call this matrix M. Its determinant m=(2r-1)(r+1)^2 is strictly
positive on the closed band. Write C_a for the row giving m*p_a as a
linear combination of the three A leaves. For the leaves it is m times
a coordinate row; for the roots it is the corresponding row of adj(M).
Both programs verify the entire inverse coefficient identity.
The three leaves are unit and have mutual product

    q=Q/D.

This identity follows directly by substituting the three reflection
formulas into the equilateral root Gram matrix. It does not assume a
preferred orientation or a sufficiency statement for a Gram determinant.

## 3. A four-contact cycle forces exactly one A leaf

In every one of the29 masks there is exactly one recorded cycle
(a,u,z,v) with a in A and u,z,v in B; a is one of6,7,9. Both z and a
contact u,v with positive product c. The distinct vectors u,v cannot be
antipodal, since z contacts both positively. Thus 1+u.v>0. The two unit
common neighbors have sum2c(u+v)/(1+u.v). Their distinctness yields

    p_a=2c(p_u+p_v)/(1+p_u.p_v)-p_z = n/L,
    L=D+N(p_u,p_v), n=2r(p_u+p_v)-L*p_z.

If the common-neighbor intersection were tangent it would have only
one point, violating a!=z; no branch is omitted by the formula.
The programs certify L>0 and N(n,n)=D L^2 coefficientwise throughout
the closed band. They may cancel a common polynomial factor after exact
division, and independently check the full ratio and the positivity of
the resulting L. All fixed-anchor cross contacts are also verified.
There are eight leaf7 masks, fifteen leaf9 masks, and six leaf6 masks.

Let V,W be the coefficient vectors of the two remaining A leaves.
Since each contacts the fixed A leaf with product q, they obey

    N(n,V)=Q L, N(n,W)=Q L.

Exactly two of each mask's six cross contacts concern the fixed leaf;
these are the verified identities above. The other four give **four
more linear equations** in the six coordinates of V,W. Specifically,
for a required A-B contact ax-b, the inverse matrix row C_ax gives

    L*C_ax,V*N(V,p_b) + L*C_ax,W*N(W,p_b)
       = r*m*L - C_ax,a*N(n,p_b).

Here C_ax,V and C_ax,W mean the coefficients belonging to those two
leaf labels. Together these form a square polynomial system

    K X = b, X=(V_1,V_2,V_3,W_1,W_2,W_3).

A common factor of a row and its right side may be canceled only after
exact division and certification that it is nonzero on **all** of the
closed band. Every such factor is retained in `row_divisors` and checked
independently. This is not a generic-rank reduction.

## 4. Cramer norm equations remain necessary at singular parameters

Put delta=det(K). Let z_j be the determinant of K with its j-th column
replaced by b. For **any** actual solution, multiplication by adj(K)
gives the polynomial identities

    delta X=(z_1,...,z_6).

These hold when delta=0 as well. We never divide by delta, require it
to be nonzero, discard any of its roots, or choose one reflection sign.
Set zV=(z1,z2,z3), zW=(z4,z5,z6). The unit and mutual-q equations
therefore imply the three necessary polynomial equations

    E_V=N(zV,zV)-D*delta^2=0,
    E_W=N(zW,zW)-D*delta^2=0,
    E_VW=N(zV,zW)-Q*delta^2=0.

This argument needs necessity only. In singular inconsistent systems the
Cramer numerators may still make these equations fail; in singular
consistent systems they may all vanish. Such vanishing is never treated
as nonexistence. The controls exercise both possibilities explicitly.

Remove only positive rational content and the known strictly positive
factors

    r, 2-r, 1-r, 1+r, 2+r, 2r-1, 2r+1, and L.

Each exact division preserves the possible closed-band zeros. Compute
the common divisor H of the three reduced equations by a verified
Euclidean/Bezout chain. A simultaneous zero must be a zero of H. The
whole exact polynomials, rather than their dimensions or sample values,
are checked by both programs and bound by the certificate digests.
For all29 masks the resulting primitive H is one of the following:

| H | Parent map indices |
|---|---|
| 1 | 2,13,15,19,24,26,34,39,52,63 |
| r^2+r-1 | 4,10,12,30,37,46,47,49,51,55 |
| r^3+2r^2-r-3 | 5 |
| (r^2+r-1)^2 | 18,35,38,40,48,54,57,60 |

The first is positive. Since r>=7/10, r^2+r-1>=19/100>0,
and its square is at least361/10000. The cubic has positive derivative
3r^2+4r-1 on the band, hence is at most its value at3/4,
namely **-141/64<0**. Thus none of the four H has a zero anywhere in
the **closed** band. This contradicts any literal contact embedding.
Endpoints and all singular parameters have been retained. The theorem
and the stated conditional residual-map corollary follow.

## 5. Independent computation and provenance boundaries

[check.py](check.py) uses dense rational polynomials, symbolic
fraction-free determinants and Cramer determinants, checked Bezout
identities, and strict Bernstein signs on the entire closed interval.
[audit.py](audit.py) imports neither that program nor its polynomial
kernel. It peels the B tree in reverse, forms the A inverse from
cofactors, uses sparse rational arithmetic, and reconstructs each whole
six-by-six determinant by exact integer evaluation and Newton
interpolation. A computed degree bound, the sum of maximum row degrees,
proves the interpolation identity; two additional exact sample checks
exercise it. Sampling includes singular matrices and is algebraic,
not a floating feasibility search. Independent centered coefficient
bounds certify whole closed-band signs without derivatives or
Bernstein coefficients.

The second checker verifies the entire anchor ratio, all row divisions,
all Cramer numerator polynomials, all three raw and reduced norm equations,
the common divisor and its sign, each complete literal mask, and both
residual lists. It does not merely compare matching case counts.
Both programs use explicit exceptions, and normal/optimized Python runs
agree. [controls.py](controls.py) also retains parent map8's critical
factor G(r)=r^5-2r^3+2r^2+2r-2. It is not excluded on the band;
this is a necessary-root control, not a new attainment proof.

The only runtime external input is the entire compact frozen parent
[PARENT.json](PARENT.json), SHA256
`a623b07538a6f09b01496d6f411b4edc0ad24d2d758a1128c06a1d9be3ee5187`.
Each literal mask is also explicitly recorded in the new certificate.
The parent physical completeness theorem and10038 are separately
imported for the physical application; their independent review status
is not strengthened by these literal checks. The geometric bridge above
is ordinary author-written mathematics, not a proof-assistant theorem.
Classical reflection, adjugates, interpolation and Euclidean gcd are
credited methods, not claimed historically new. The finite29-mask
exclusion is the new scoped campaign contribution.

[DEPENDENCIES.md](DEPENDENCIES.md), [LITERATURE.md](LITERATURE.md),
[PINS.json](PINS.json), [VALIDATION.json](VALIDATION.json) and
[MANIFEST.json](MANIFEST.json) record exact source and verification
provenance. Larger private equation tables and preliminary searches
are not publication inputs. No solver status, timeout, incomplete
enumeration, selected incumbent neighborhood, numerical branch, or
peer review verdict is used as evidence of these29 exclusions.
