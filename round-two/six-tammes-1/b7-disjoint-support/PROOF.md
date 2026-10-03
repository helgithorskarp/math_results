# A4 and B7 have disjoint supports on the closed physical band

Actual author **six-tammes-1**, role **researcher**, 2026-10-03.
This is an ordinary geometric proof with complete exact polynomial and
closed-interval checks. Both programs are by this author; independent
mathematical review and formalization of this new result are pending.

**Literal theorem.** None of the 106 distinct fourteen-point contact
masks defined below is realizable as a unit c-code in R^3 for any
**c in the closed interval J=[7/13,3/5]**. Extra contacts are allowed.
The individual mask exclusions require no face, cohort, degree,
hemisphere, closeness, optimizer, or fifteenth-point hypothesis.

**Physical corollary.** Retain every hypothesis of
[9972's complete A4/B7 incidence reduction](../b7-contact-incidence/PROOF.md),
including its entire 9813 physical interface. Then A4 and B7 have
**disjoint point supports**. Their six plus nine points consume all
fifteen points. Only the parent's explicit **53 necessary complete
contact maps on closed J** remain; for a strict improvement c<tau, only
its **52** listed maps remain. These counts and map lists are imported
from 9972, not newly enumerated here. No remaining map is asserted
realizable or excluded by this theorem.

For clarity, that complete physical interface means fifteen distinct
unit points with all distinct products at most c; every equality pair
is retained in the minor-arc contact drawing; the drawing is connected
with minimum degree at least three; every actual face has a simple disk
closure with three to five distinct corners; every nontriangle is
geodesically convex and individually lies in an open hemisphere; the
actual census is eleven triangles, three quadrilaterals and three
pentagons. The complete triangle-face adjacency has exactly the two
components A-size4 and B-size7 containing the literal cores below.
Every actual triangle adjacency is retained, rather than a chosen
spanning tree. These are conditional premises, not a theorem about all
global optimizers. The reversed A7/B4 assignment is a different case.

## 1. Exact specification and finite coverage

The original twelve labels are

    A labels: 0,5,6,7,9,11;    B labels: 1,2,4,8,10,12.
    A triangles: (0,5,11),(0,6,11),(0,5,7),(5,9,11).
    B-core triangles: (1,2,4),(2,4,8),(1,2,10),(1,10,12).
    Original cross contacts: 7-12 and 9-10.

All triangle sides have product c. [PARENT.json](PARENT.json) is the
entire immutable 43286-byte 9972 certificate, SHA256
`a623b07538a6f09b01496d6f411b4edc0ad24d2d758a1128c06a1d9be3ee5187`.
Take each of its `overlap_rows` having exactly one value different from
-1 after its shape index. There are 106 such rows: 86 sharing 6, ten
sharing 7, ten sharing 9. If the row is `(shape,a20,a21,a22)`, take all
seven triangles in `all_shapes[shape]`, on the six B-core labels and
fresh labels 20,21,22. Identify the unique non--1 entry's fresh label
with that A label. All other label classes are **distinct**, including
all twelve original labels. Add all A sides and both original cross
contacts. This specifies fourteen actual distinct unit points; every
distinct pair must have product at most c. It defines each literal mask
without asserting that its triangles are actual faces.

9972 proves that every physical one-overlap case in its conditional
cohort is in this list, and that two or more shared points are impossible.
We use that previous coverage only for the physical corollary. The
individual exclusions below apply directly to the explicit masks.
An arbitrary fifteenth point cannot rescue an impossible fourteen-point
subset, so no location or contact restriction on that point is needed.

There are 25 shared-ear coordinate groups: twenty sharing 6, three
sharing 7, two sharing 9. Equal coordinates permit reuse of an arithmetic
calculation; **they are not an equivalence of complete packing masks**.
Every original row and its entire nine-point B support are retained.
Indices of groups and rows are zero-based and fixed by the accompanying
programs and [CERTIFICATE.json](CERTIFICATE.json).

## 2. Complete contact normalization

Put

    r=2c/(1+c) in [7/10,3/4], D=2-r, c=r/D,
    Q=2r^3+2r^2-3r, q=Q/D,
    Hnum=2(1-r)Id+r11^T,
    N(v,w)=v^T Hnum w.

In the coefficient basis (p1,p2,p4), the physical product is N/D.
Hnum has positive eigenvalues 2(1-r),2(1-r),r+2 on the entire closed
band. A point is unit iff N(v,v)=D, and contact iff N(v,w)=r.

For distinct unit contact neighbors of a contact pair u,v, the two
solutions have midpoint c(u+v)/(1+c), with squared norm
2c^2/(1+c)<1. Thus, if one third point is w, the other is exactly

    flip(u,v,w)=r(u+v)-w.                         (1)

There are precisely two sphere/plane intersections; distinct prescribed
labels force the other one. Starting at p1=e1,p2=e2,p4=e3, (1) fixes the
entire original B4 and then every fresh corner of each parent B7 tree.
The producer and auditor reconstruct this independently and verify all
nine unit identities and all fifteen triangle-side contacts. No
orientation is chosen from floating coordinates or from an incumbent.

In the coefficient basis (p0,p5,p11), the A ears have rows

    p6=(r,-1,r), p7=(r,r,-1), p9=(-1,r,r).

Consequently every pair of distinct A ears has product q. Their leaf
matrix M has determinant

    det M=(2r-1)(r+1)^2>0.                       (2)

On the entire band, -1/2<q<0 and q+c>0. The identities

    q+1/2=(2r-1)^2(r+2)/(2D),
    q+c=2r(r^2+r-1)/D

make the first and third bounds explicit; q<0 follows from Q/r
=2r^2+2r-3, increasing with negative value at 3/4. In particular D+Q>0.
These formulas follow from the original A contacts and distinctness,
without a contact-face premise.

## 3. All 86 shared-6 cases

Let s=p6 be the known B coordinate at the shared corner, u=p7, v=p9,
b=p12, z=p10. Write K=N(s,b), L=N(s,z), X=N(v,b). Every realization
forces both four-vector Gram determinants to vanish:

    H1 = det [[D,Q,Q,K], [Q,D,Q,r],
              [Q,Q,D,X], [K,r,X,D]],
    H2 = det [[D,L,K,Q], [L,D,r,r],
              [K,r,D,X], [Q,r,X,D]].            (3)

These are quadratics in X, say aX^2+b1 X+c1 and dX^2+eX+f. The producer
collects their coefficients by exact interpolation at 0,1,-1 (the
determinants have degree at most two in X). The auditor expands a
bivariate determinant coefficient by coefficient, without interpolation.
Their common-root resultant is

    Res=(af-c1 d)^2-(ae-b1 d)(b1 f-c1 e).         (4)

The auditor obtains (4) independently as a 4-by-4 Sylvester determinant
using fraction-free Bareiss and checks every polynomial division.
A common X gives a nonzero kernel vector (X^3,X^2,X,1) of that matrix;
therefore Res=0 remains necessary even if a leading coefficient drops.
A zero or identically zero resultant is **not** a nonexistence proof.

Only positive rational content and powers of the strictly positive
factors r,D,1-r,1+r,2+r,2r-1,1+2r are removed. No exceptional zero factor
is discarded. Thirteen coordinate groups, covering 52 original rows,
have strictly nonzero reduced resultant on the entire closed band.

For each of the remaining seven groups, define

    ell=d b1-a e, num=a f-d c1,
    C=[Hnum s; Hnum z; Hnum b] (these are rows).

Eliminating the quadratic terms in (3) forces ell X=num. Both ell and
det C are strictly nonzero on the entire closed band, certified with
their signs. Solve

    C v=(Q,r,num/ell)^T                         (5)

by fraction-free Cramer data: RHS=(Q ell,r ell,num), numerators nv,
and denominator dv=ell det C. Every full row identity is checked.
Thus v=nv/dv in any actual code, without dividing by an uncertified
quantity. The remaining possibilities are:

| Group(s) | Original rows | Necessary outcome |
| --- | ---: | --- |
| 0,1,2,3,6,7,9,10,12,13,15,18,19 | 52 | Res is strictly nonzero on closed J |
| 4 | 1 | identically zero Res, but p9=p1 identically |
| 14 | 9 | identically zero Res, but p9=p2 identically |
| 5 | 14 | exceptional parameter only, then p9=p1 |
| 8 | 7 | exceptional parameter only, then p9=p2 |
| 11 | 1 | exceptional parameter only, then p7=p1 |
| 16 | 1 | remaining cell forces p7.p1>c |
| 17 | 1 | remaining cell forces p9.p12>c |

The two continuous aliases contradict distinct original labels.
For groups 5,8,11 the resultant is h times a strictly nonzero cofactor,
where

    h=r^2+2r-2,  D^2(3c^2-1)=2h.

Thus the only remaining parameter is c=1/sqrt(3) in closed J. All aliases
at that parameter are checked coefficientwise in Q[r]/(h). A nonzero
a+b r has inverse `(a-2b-b r)/(a^2-2ab-2b^2)`; the field norm and the
full inverse identity are checked. Groups 5 and 8 force their p9 aliases
using (5). Group 11 first recovers v and then uniquely solves
N(s,u)=Q, N(v,u)=Q, N(b,u)=r, with nonzero field determinant, obtaining
p7=p1. Equality at this parameter is retained and explicitly excluded
by distinctness, not rounded away.

For groups 16 and 17 the complete possible-root enclosures in r are

    group16,row128: [1891/2560,60513/81920],
    group17,row135: [30493/40960,60987/81920].

Complete closed nonzero covers of each resultant are checked to the
left and right of its displayed cell. All possible zeros are therefore
inside the cell; no existence or uniqueness of a root is needed. On
group16's whole cell, recover u by the independently nonsingular system
N(s,u)=Q,N(v,u)=Q,N(b,u)=r, clearing dv first. It forces p7.p1>c.
On group17's whole cell, (5) forces p9.p12>c.
For any forced point n/d and B point w, the safe cleared witness is

    W=(N(n,w)-r d)d,
    (n/d).w-c=W/(D d^2).                       (6)

The program certifies W>0 on the whole relevant closed cell, and d is
nonzero there. This argument does not presume a denominator sign or a
unit identity away from actual resultant roots. The forced coordinate
is used only as a necessary coordinate of an actual code.
The table covers 52+10+22+2=86 original shared-6 assignments.

## 4. All four orientations in the remaining twenty cases

For a shared 7, put s=p7 and z=p10; the first unknown is v=p9. For a
shared 9, put s=p9 and z=p12; the first unknown is v=p7. In either case
v is unit, s.v=q and z.v=c. The remaining A ear is u=p6.
Define the coefficient operator

    Jop(w)=(r+2)w-r(sum w)1,
    K=N(s,z), E=D^2-K^2,
    Delta=det [[D,Q,K],[Q,D,r],[K,r,D]],
    T=(r+2)Delta,
    Vden=(r+2)E,
    V0=(r+2)[(QD-Kr)s+(rD-KQ)z],
    V1=Jop(s cross z).

For each of the five coordinate groups the programs certify E>0 and
T>0 on the **entire closed band**. The affine two-plane intersection
has direction V1, perpendicular in the physical metric to s and z;
Hnum Jop=2(1-r)(r+2)Id. Its metric norm satisfies
N(V1,V1)=(r+2)E. The projected solution is V0/Vden, and its squared
remaining unit height is Delta/(D E). Hence the complete sphere fiber is

    v=(V0+eps sqrt(T)V1)/Vden, eps in {-1,+1}.   (7)

This is exactly the two-plane/unit-sphere solution set. All five actual
inputs are strictly transverse, so no singular or tangent endpoint is
silently omitted. A nonpositive or unresolved discriminant would fail
the proof rather than supply an exclusion.

Given s,v with product q, the remaining ear u has product q with both.
The midpoint is q(s+v)/(1+q); -1/2<q<0 gives two distinct solutions. The
identity

    sqrt(1+2q)/sqrt(D(r+2))=(2r-1)/D

turns their transverse multiplier into an exact rational function:

    u=[Q(s+v)+chi(2r-1)Jop(s cross v)]/(D+Q),
    chi in {-1,+1}.                             (8)

Both signs in (7) and both signs in (8) are retained. Invert the
nonsingular leaf matrix (2) to recover p0,p5,p11. Every A point now has
an expression `(n0+eps sqrt(T)n1)/den`, with a known strictly positive
polynomial denominator. For every chi and coordinate group, both
programs check all six A units, all nine A contacts, both prescribed
cross contacts, and all three ear-pair q identities coefficientwise
in the constant and sqrt(T) terms.

The auditor computes the transverse vectors differently, using

    cross(Hnum a,Hnum b)/(2(1-r))

with exact polynomial division instead of the producer's direct Jop
formula. It restores A roots by a separately expanded Cramer calculation.
These differences corroborate arithmetic; the geometric completeness
argument (7)-(8) is an ordinary proof, not formally verified software.

Each of the twenty original masks has four complete orientation cases,
giving **80** cases. For each retain its full nine-point B table.
For distinct A label i and B label j the cleared excess product is

    g0+eps sqrt(T)g1,
    g0=N(n0,pj)-r den, g1=N(n1,pj),
    pi.pj-c=(g0+eps sqrt(T)g1)/(D den).          (9)

The actual shared-ear/self-label pair is excluded from these comparisons:
it is a single physical point, so treating its product with itself as a
packing violation would be invalid. Every chosen witness compares two
distinct assigned physical points, explicitly checked by the auditor.

The certificate supplies **81 closed witness cells** covering all 80
cases. Seventy-nine cases have a whole-band witness. Only row117,
eps=+1,chi=+1 splits at r=29/40: pair6-8 covers [7/10,29/40] and pair6-21
covers [29/40,3/4]. Every cell proves (9) strictly positive by one of:

1. g0>0 and eps*g1>0 (or g1=0);
2. g0>0 and g0^2-T g1^2>0;
3. eps*g1>0 and T g1^2-g0^2>0.

Each condition implies strict positivity, retaining the sign guard
before squaring. The delivered witnesses use 22 cells of type1 and
59 of type3; type2 is supported and tested but unused here.
All 81 sign and coverage obligations pass exactly. A record merely
listing a favorable orientation, missing a half cell, or squaring
without the sign guard cannot establish the theorem.

Together Sections3 and4 exclude all106 literal masks. Parent9972's
physical overlap cover now forces disjoint supports, proving the
corollary with all of that parent's original scope intact.

## 5. Exact checking, coverage and trust boundary

[check.py](check.py) uses dense rational polynomial arithmetic, expanded
determinants, quadratic interpolation, the closed formula(4), direct
transverse vectors and strictly signed Bernstein coefficients.
[audit.py](audit.py) imports neither it nor its dense kernel. It uses
sparse rational arithmetic, independent face propagation, bivariate
Gram coefficients, Sylvester/Bareiss, dual transverse vectors, separately
expanded Cramer systems and rational Taylor enclosures.

For Bernstein checking, the exact coefficients on each rational closed
cell express p as a weighted average of its Bernstein coefficients;
all strictly positive coefficients prove p>0, including both endpoints.
For Taylor checking, write p(m+h t)=sum a_i t^i for |t|<=1, with exact
Fractions. The condition a0>sum_{i>0}|a_i| proves p>0 on the entire closed
cell. If needed, split into two closed halves and apply the same exact
bound; there is no floating precision or directed-rounding dependency.
Negative nonzero signs are checked by multiplying by -1.

Every delivered binary interval cover is prefix-free, contains no
duplicate leaf and has exact Kraft mass sum 2^(-depth)=1. Each rational
leaf endpoint is recomputed from its path, so the finite covers include
all endpoints and subdivision boundaries. Possible-root outer covers
have producer depth guard16; sphere packing covers have guard12; the
auditor allows maximum supplied depth18 and Taylor refinement depth18.
Any unfinished enclosure, timeout or failure is **unproved**, never an
exclusion. No process or memory setting was raised after a failed pilot.

The auditor reads the untrusted certificate before construction to
obtain witness choices. It freshly rebuilds all coordinate tables,
Gram coefficients, resultant identities, forced coordinates, radical
branches, complete row/orientation covers and every witness polynomial.
It then compares the entire canonical typed record. It does not claim
to have selected the witness pairs independently or to have opened
the certificate only after reconstruction. `--emit` emits its checked
reconstructed record for whole-byte comparison.

[controls.py](controls.py) runs both full baselines, checks determinant
rank/orientation, sparse zero coefficients/division, resultant leading
degree drops, exact quadratic-field inversion, closed-endpoint zeros,
both radical signs, invalid unsigned squaring, tangent zero and complete
closed cover boundaries. A damaged shared-self witness additionally
goes through the full sparse auditor and must reject. Other damaged
records are compared with the two once-freshly-verified complete
references; those are projection/integrity controls, not separate full
geometry reruns for every damage. Valid whitespace and key-order
representations pass. [VALIDATION.json](VALIDATION.json) and
[CONTROLS.json](CONTROLS.json) record actual runs and their limits.

The immutable parent list, ordinary reflection and complete sphere
fiber arguments, exact arithmetic implementation and closed coverage
are the trust boundary. The physical corollary additionally imports
9972's complete incidence/physical proof and necessary-map counts.
Neither same-author agreement nor publication is an independent review
or a formal proof-assistant verdict.

## 6. What remains

The earlier one-overlap branch's arbitrary fifteenth point is eliminated
because its fourteen-point contact prefix is impossible, without a
capacity or placement assumption on that point. The disjoint53 maps
remain necessary candidates; their52 strict-improvement maps split into
29 with a sole-A-corner quadrilateral and23 with all quadrilaterals
having two A and two B corners. Their complete realization/packing
obligations, the other triangle profiles, whole G20 occurrence and
global Tammes15 bounds remain open. The known incumbent tau is the
root of 13c^5-c^4+6c^3+2c^2-3c-1 in J; no new construction or global
optimality claim is made.

Fresh complementary [10012](../../six-tammes-2/g21-two-cap-capacity/PROOF.md)
excludes original G20 plus5-12 for fifteen points on its smaller closed
I=[14/25,593/1000], with every added point arbitrary. It is not a premise
of these full-J shared-ear exclusions. Independent
[9984](../../six-reviewer-3/derived-g24-audit/REVIEW.md) confirms the
earlier thirteen-label9966 only and proves its scoped sharpness; it does
not independently review either10012 or this theorem. Fresh
[10026](../../six-reviewer-3/g21-two-cap-audit/REVIEW.md) independently
confirms10012 on its original closedI and credits9984's inherited
sharpness; it does not review this shared-ear theorem or widen toJ. Likewise9950
confirms9922 and9906 supplies a separate wider triangle-core theorem,
with no verdict transported here. Exact dependencies and source credits
are recorded in [PINS.json](PINS.json), primary literature in
[LITERATURE.md](LITERATURE.md). Classical Gram, reflection, resultant
and sphere-intersection methods are credited without an exhaustive
historical-priority assertion.
