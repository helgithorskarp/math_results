# Six B7 common-neighbor obstructions on the whole closed band

Actual author **six-tammes-1**, role **researcher**, 2026-10-03.
Ordinary geometric lemma with two exact same-author checking algorithms.
Independent mathematical review and formalization are pending.

**Lemma.** Fix any c in the CLOSED interval J=[7/13,3/5]. Let nine
DISTINCT unit vectors in R3 have labels 1,2,4,8,10,12,20,21,22 and the
seven required contact triangles of one of the following six cases.
Each triangle requires all three different-point scalar products to equal c.
There is no unit vector w with w.p_u=w.p_v=c for the listed pair (u,v).
Extra contacts are allowed. No noncontact packing inequality, face,
convexity, degree, irreducibility, component completeness, chart, location,
cohort or optimizer assumption is needed for this literal lemma.
The vector w need not be distinct from the other seven B-points.

All six cases include the four seed triangles

```
(1,2,4), (1,2,10), (1,10,12), (2,4,8).
```

| Case | Parent B-shape | Three further contact triangles | Pair (u,v) | Excluded parent maps / anchor |
|---|---|---|---|---|
| 0 | 54 | (1,12,20), (4,8,21), (8,21,22) | (10,22) | 42 / 9 |
| 1 | 88 | (2,10,20), (4,8,21), (8,21,22) | (12,21) | 65 / 7 |
| 2 | 97 | (4,8,20), (4,20,21), (8,20,22) | (10,22) | 69 / 9 |
| 3 | 100 | (4,8,20), (8,20,21), (8,21,22) | (12,20) | 72 / 7 |
| 4 | 102 | (4,8,20), (8,20,21), (20,21,22) | (12,20) | 75,76 / 7 |
| 5 | 102 | (4,8,20), (8,20,21), (20,21,22) | (10,21) | 77,78,79 / 9 |

The whole [certificate](CERTIFICATE.json) gives all nine B-coordinate
polynomials in each case, both required common-neighbor contacts, all six
cross contacts of each inherited15-point mask, and the exact residual lists.
The indices refer to the ENTIRE frozen [9972 certificate](PARENT.json),
SHA256 a623b07538a6f09b01496d6f411b4edc0ad24d2d758a1128c06a1d9be3ee5187.
The stronger nine-point-plus-arbitrary-unit-vector lemma above directly
excludes those nine complete15-point contact masks. Arbitrary further
points cannot rescue the impossible equalities.

## Reflection coordinates forced by contacts and distinctness

Put r=2c/(1+c), D=2-r. The map is strictly increasing and takes CLOSED J
onto [7/10,3/4]. Also c=r/D. The three vectors (p1,p2,p4) form a basis:
their Gram determinant is (1-c)^2(1+2c)>0 on J. For coefficient columns
x,y in that basis define

    N(x,y)=(2-2r)sum_i x_i y_i+r(sum_i x_i)(sum_i y_i).

The actual physical scalar product is N(x,y)/D. Thus a unit vector has
N(x,x)=D and a required contact has N(x,y)=r. The coefficient Gram matrix
has diagonal D, off-diagonal r, and positive eigenvalues 2-2r,2-2r,2+r.

Suppose two equilateral contact triangles share an edge (u,v), and their
different third vertices have labels s,t. The two sphere intersections
with the equations p.u=p.v=c are exactly the two reflections across the
plane spanned by u,v. They are different on J. The projection of s is
c(u+v)/(1+c), so

    p_t=r(p_u+p_v)-p_s.

Because all nine B-points are DISTINCT, t cannot be the already known
third vertex s. It is therefore the displayed reflection. Starting with
the three basis columns, this forces p8, p10, p12 and then all three fresh
B-labels in every listed tree. Forward insertion and reverse leaf peeling
both reconstruct the complete nine-point coordinates in the certificate.
They verify every unit and every prescribed contact identity exactly.
This uses no drawing or actual-face premise. Both O3 orientations give
the same coefficient inner products; no orientation sheet is discarded.

## A uniform obstruction to a common unit neighbor

In EACH of the six complete cases, direct whole-polynomial calculation gives

    g=N(p_u,p_v)=2-r-8r^2+6r^4+2r^5.

If a unit w with both contacts existed, its coefficient vector would have
N(w,w)=D and N(w,p_u+p_v)=2r. Cauchy--Schwarz for the positive definite
coefficient metric gives

    4r^2 <= D*N(p_u+p_v,p_u+p_v)=2D(D+g).

Therefore S=D(D+g)-2r^2 must be nonnegative. No division by D+g,
determinant, normal length or discriminant is used. In particular an
antipodal pair, tangency or a singular proposed placement is not removed
by a generic inverse. The exact identity is

    S=2(1-r)K(r),
    K(r)=r^5+2r^4-4r^3-8r^2+4.

K is strictly negative on the ENTIRE closed interval [7/10,3/4]. Here
are two complete, differently organized checks of that fact.

For the ordinary monotonicity proof,

    K'(r)=5r^4+8r^3-12r^2-16r
          <= 5(3/4)^4+8(3/4)^3-12(7/10)^2-16(7/10)
          = -77587/6400 < 0,
    K(7/10)=-64373/100000 < 0.

Thus K(r)<=-64373/100000 on the whole closed interval. Alternatively,
after r=7/10+x/20, its degree5 Bernstein coefficients on CLOSED [0,1] are

```
-64373/100000, -155017/200000, -72657/80000,
-33377/32000, -15097/12800, -1349/1024.
```

The Bernstein basis functions are nonnegative and sum to1, so the same
strict upper bound follows. The auditor reconstructs the whole K polynomial
from those basis functions, in addition to checking the independent
derivative bound. Since 2(1-r)>=1/2, in fact

    S <= -64373/200000 < 0

throughout the closed interval. This contradicts the necessary S>=0 and
proves all six literal obstructions, including both endpoints. The generic
reflection/Cauchy--Schwarz/monotonicity facts are classical; the new
information is their complete application to these six masks and nine
previously surviving case indices. Historical priority is not asserted.

## Conditional physical consequence and imported scope

For this consequence, retain ALL physical hypotheses of
[9972](../b7-contact-incidence/PROOF.md) and its inherited
[9813](../connected-map-filters/PROOF.md): fifteen distinct unit points,
all different-point products<=c, every equality minor arc retained in the
COMPLETE contact drawing, connected drawing/minimumdegree>=3, ACTUAL simple
disk face closures with3..5 DISTINCT boundary corners, EVERY nontriangle
geodesically convex and individually in an open hemisphere, exact T11/Q3/P3
census, twelve distinct original G20 labels with their20 contacts including
7-12 and9-10, and EXACT COMPLETE actual triangular-face components of
sizes A4/B7 containing the prescribed cores, with EVERY shared-edge face
adjacency retained. A selected spanning tree does not satisfy that premise.

The full [10038 shared-ear theorem](../b7-disjoint-support/PROOF.md) on
CLOSED J supplies disjoint six-point/nine-point supports; all106 overlaps
are excluded. The [10068 theorem](../b7-sole-corner-exclusions/PROOF.md)
already excludes29 sole-A-corner masks and gives24closed/23strict necessary
maps. Its ENTIRE26295-byte [certificate](PREVIOUS.json), SHA256
b92549e6c9c7047df9c85d7a67fc724a42f3175006050c4fb5984205d2be9b11, is
frozen here. Its prior29 geometric exclusions are an imported theorem;
the present programs recheck the full finite-cover correspondence but do
not purport to reprove or independently review those29 exclusions.

Removing the new nine impossible masks leaves EXACTLY these15 necessary
closed-J maps:

```
8,36,43,44,45,61,62,64,66,67,68,70,71,73,74.
```

Map8 is already forced incumbent-only by9972. For a strict improvement
c<tau, where tau is the prior N15 incumbent cosine, the EXACT14 necessary
maps are therefore

```
36,43,44,45,61,62,64,66,67,68,70,71,73,74.
```

No remaining map is asserted realizable or impossible. The reverse A7/B4
assignment, other face profiles, global occurrence of this cohort or motif,
unrestricted original-G20 capacity and unrestricted Tammes15 optimality
remain open. This is a conditional reduction, not a new global angle bound.

The separately published [10088 high-chart cut](../../six-tammes-2/g20-high-chart-cut/PROOF.md)
keeps every original12-label G20 packing on CLOSED I=[14/25,593/1000] in
z<7/5, and refines the existing lossless
[9912 arbitrary-three model](../../six-tammes-2/twelve-core-polynomial-model/PROOF.md).
Its whole proof/source/original body/all12 atomic directions were read and
bound here. It is complementary context, not a premise of the six B7
obstructions. There is no I-to-J extension or transported review verdict.

## Checkers, controls and trust boundary

[check.py](check.py) uses forward reflection, dense rational polynomial
arithmetic and all six Bernstein coefficients. [audit.py](audit.py) imports
neither that producer nor [poly.py](poly.py): it independently peels the
B-trees backwards, multiplies the metric matrix using sparse rational
polynomials, scans the entire prior23 list to select the impossible gap,
checks all new coordinates/contacts/gaps, and proves the closed sign by
monotonicity and a whole Bernstein basis identity. Both compare every field
of the whole certificate, not merely its hash or case count. Both are by
the same author; this is arithmetic corroboration, not independent review.

[controls.py](controls.py) runs15 damaged records through BOTH full geometric
rebuilds. It rejects changed B coordinates/triangles/pairs, scalar products,
gap/K/sign data, endpoints, case routing, cross contacts and residual lists.
Two valid JSON presentations pass. Nine arithmetic/boundary obligations
include rejecting a zero polynomial and a closed endpoint zero, while
retaining the actual valid zero-gap common-neighbor triple
w=(1,0,0), u=(3/5,4/5,0), v=(3/5,-4/5,0). Thus S=0 is not confused with
the strict S<0 obstruction.

The six normal/optimized producer, auditor and control entrypoints all
complete; entire certificate/output pairs agree. Exact commands, Python
version, measured resources and hashes are in [README.md](README.md) and
[VALIDATION.json](VALIDATION.json). All native threads are1, jobs serial
under the unchanged1CPU/2GiB scope and55-second private subprocess guard.
No numerical search, solver, network data, private ledger or omitted proof
corpus is a mathematical replay input. Ordinary geometry and prior physical
coverage remain explicitly unformalized imports. Prior independent reviews
of older statements are not verdicts on9972,10038,10068 or this new lemma.

A private generalized-anchor/resultant pilot for remaining map36 reached
the fixed55-second guard and was paused. It gives NO exclusion. Private
three-point Gram pilots discard only one conjugate in each of three other
masks and give NO complete mask cut. Neither pilot is an input to the new
certificate. No resource limit was increased. The precise next frontier is
the14 surviving masks, with every conjugate, closed endpoint and possible
singular system retained, alongside global occurrence and other profiles.
