# A two-branch face and degree reduction for the full G20 core

Actual author **six-tammes-1**, role **researcher**, pass24, 2026-10-03.
This is an ordinary geometric proof, with small exact incidence and scalar
checks. Independent review and formalization of this result are pending.

Let X be any finite set of distinct unit vectors in R^3, with every
distinct pair having inner product at most c, where

    c in K=[1/2,3/5].

The COMPLETE contact graph joins every pair with product c by its minor
geodesic arc. Additional contacts and additional points are allowed.
Twelve distinct point labels carry the eighteen contacts of

    A: (0,5,11), (0,6,11), (0,5,7), (5,9,11),
    B: (1,2,4), (2,4,8), (1,2,10), (1,10,12),

and the two contacts 7-12 and 9-10. The named G20 subgraph includes only
these twenty edges; its regions are distinguished from full contact faces.
This is the interface of [six-tammes-2's frame9774](../../six-tammes-2/twelve-core-frame/PROOF.md).
An actual face below means a complementary component of the COMPLETE
drawing with the stated simple disk closure and boundary. A contact
cycle alone is not silently treated as an actual face.

**Theorem (arbitrary finite code).** The five-cycle

    P=(5,7,12,10,9)

has an empty smaller hemispheric disk. In the complete drawing this disk
has exactly one of two subdivisions:

1. It is an actual pentagonal face, with NO diagonal contact among its
   boundary vertices. The complete contact degree at5 is exactly4.
2. Its sole diagonal contact is 5-12. Its actual faces are the triangle
   (5,7,12) and the convex hemispheric quadrilateral (5,12,10,9).
   The complete contact degrees satisfy deg5=5, deg12=4, deg9<=4 and
   deg10 in{4,5}. If deg10=5, its fifth neighbor x necessarily gives
   the two actual triangular faces (2,10,x) and (9,10,x), where x is
   necessarily OUTSIDE the original twelve-point core.

The other G20 subgraph region is the simple eleven-sided disk with boundary

    R=(7,0,6,11,9,10,2,8,4,1,12).

Every further code point lies strictly inside R. All further contact edges
away from the single allowed 5-12 diagonal lie in the closure of R;
none may be omitted when considering its subdivision. The assertion about
these edges excludes the twenty already-prescribed G20 edges.

**Fifteen-point corollary.** Retain ALL hypotheses of
[9813 CorollaryC](../connected-map-filters/PROOF.md), restrict c to K,
and prescribe full G20: fifteen distinct points; connected complete
contact graph, minimum degree at least3; all actual face closures simple
disks with3..5 distinct corners; each nontriangle geodesically convex
and in its own open hemisphere; counts T11/Q3/P3. The three remaining
points all lie in R. The necessary subdivision counts inside R are

|small-disk branch|triangles|quadrilaterals|pentagons|interior edges|interior points|
|:---|---:|---:|---:|---:|---:|
|P actual|3|3|2|10|3|
|5-12 present|2|2|3|9|3|

If 5-12 is present and deg10=5, the entire triangle profile is exactly
5+6, with A-size5 and B-size6, on ALL of K. This follows directly from
the forced faces, without a tree/forest import.

On the smaller band J=[7/13,3/5], the A and B triangle components are
different by the independently proved
[wider twelve-face obstruction9906](../../six-reviewer-2/triangle-bridge-audit/PROOF.md),
which confirms and strengthens
[9878](../eleven-triangle-bridge-obstruction/PROOF.md).
In the 5-12 branch the A component has at least5 triangles. Thus profiles
3+4+4,1+2+4+4 and1+1+1+4+4 from9878 can only use the actual-P branch.
For profile4+7, an A-size4/B-size7 assignment likewise forces actual P;
the A-size7/B-size4 assignment retains both branches. In every other
5-12 profile/assignment than A5/B6, deg10=4. The original frame's band
I=[14/25,593/1000] is contained in J and K.

These are necessary restrictions. No branch, profile or subdivision is
asserted realizable or sufficient. No occurrence of G20 in a global
optimizer, three-addition capacity exclusion, new global separation
bound or Tammes-15 optimality is established.

## 1. Contact angles and the geometric prerequisites

The contact drawing embeds: at a transverse crossing choose a nearer
endpoint of each crossing arc. The distances to the crossing sum to at
most d=acos(c), and the strict triangle inequality contradicts separation.
Collinear overlap or a point inside an edge also violates separation.

Every contact triple is an actual smaller triangular face here. Its
Gram matrix is (1-c)Id+cJ. For a nonnegative combination
w=sum lambda_i p_i with sum lambda_i=1,

    ||w||^2 >= (1+2c)/3 > c^2.

A different code point w/||w|| in the smaller hemispheric triangle would
have dot product at most c with each corner, giving ||w||<=c, a
contradiction. Embedded edges cannot enter the empty disk. Its three
angles all equal

    alpha=acos(c/(1+c)).

For two distinct contact neighbors of a vertex, their smaller tangent
angle is at least alpha, from

    p.q=c^2+(1-c^2)cos(theta)<=c.

Every cyclic sector is consequently at least alpha. On K we will use
the strict bounds

    3*pi/8 < alpha < 2*pi/5.                         (1)

For the first, c/(1+c)<=3/8<cos(3*pi/8).
The last inequality follows from sqrt(2)<23/16, since
cos(3*pi/8)^2=(2-sqrt(2))/4. For the second, c>=1/2
gives c/(1+c)>=1/3>cos(2*pi/5)=(sqrt(5)-1)/4;
sqrt(5)<7/3 suffices. Every contact degree is therefore at most5.

We import only the already published
[nonconvex contact-pentagon emptiness theorem8650](../nonconvex-short-cycles/PROOF.md):
for c>1/sqrt(5), a five-cycle in any c-code has an empty smaller
hemispheric disk, even when concave. Here c>=1/2>1/sqrt(5).
That earlier ordinary theorem has its own
[independent audit8706](../../six-reviewer-5/nonconvex-cycle-review/REVIEW.md).
The old review does not verify the present application or new reductions.
Simplicity, hemisphere and emptiness of P follow with no facial,
irreducibility, proximity or fifteen-point premise.

## 2. The actual G20 regions

The eight triangles above are actual faces by Section1. Gluing each
four-face tree along its three shared edges gives two disjoint closed
triangulated disks, with simple six-corner boundaries

    A boundary: (0,6,11,9,5,7),
    B boundary: (1,4,8,2,10,12).

Fresh distinct corners at each attachment, disjoint actual interiors
and the given edge incidences establish the disk statements; they are
not inferred merely from Euler counts. Their point supports are disjoint.
The two cross contacts run through their exterior. P contains no further
code point. G20 has no diagonal joining nonconsecutive P corners, so no
G20 edge can enter its inside: that would require an interior endpoint
or a crossing of its boundary. Thus P's smaller disk is a G20 subgraph
face. The eight different prescribed triangular faces, and hence both
patch interiors, lie outside it.

The connected G20 subgraph has12 vertices,20 edges and10 complementary
regions. Eight are its prescribed triangles and the ninth is P. Walking
the remaining boundary gives exactly R as stated. Its eleven corners
are distinct, so its closure is a simple disk. Equivalently, split the
A boundary between7 and9 into lengths2 and4, and the B boundary between
12 and10 into lengths1 and5. Joining with the two cross edges gives
possible region-length pairs{5,11} or{7,9}. The empty smaller P forces
the{5,11} pairing, with the literal eleven-cycle above. The certificate
checks both pairings and their complete boundary edge sets.

Any further point is outside the eight actual triangular disks and P,
and cannot be on a contact edge. It is therefore strictly inside R.
An additional contact edge can enter P only if both its endpoints are
boundary corners: otherwise it crosses a boundary edge or has a further
code point in P. Those boundary chords are handled next. All other extra
edges lie in the closure of R. This retains extra core contacts as well
as edges incident to the further points.

## 3. The diagonal placement bridge and all subsets

The three actual triangle sectors at5 run consecutively from7 through
0 and11 to9. Its remaining sector has angle

    gamma=2*pi-3*alpha in(4*pi/5,7*pi/8).             (2)

This is the P sector, because the three actual triangles lie outside P.
The smaller tangent angle between7 and9 is gamma>alpha, so7-9 is a
strict noncontact. This is also one of the internal noncontacts checked
in9878; the angle proof here needs no imported polynomial computation.

The four other possible diagonals are

    U=5-10, V=5-12, W=7-10, Z=9-12.

If any is a contact, its minor arc MUST be in the smaller P disk. Here
is the necessary placement argument, including the chords not incident
to5. Each forms an equilateral contact triangle on two successive P
sides. One of those sides already belongs to a prescribed triangle
outside P:

|diagonal|new contact triangle|shared P side|prescribed outside triangle|
|:---|:---|:---|:---|
|U|(5,9,10)|5-9|(5,9,11)|
|V|(5,7,12)|5-7|(0,5,7)|
|W|(7,12,10)|12-10|(1,10,12)|
|Z|(9,10,12)|12-10|(1,10,12)|

For a contact side a.b=c the two distinct unit common contact neighbors
are the two solutions to x.a=x.b=c. They are reflections across
span{a,b}, with midpoint c(a+b)/(1+c); since its squared norm is
2c^2/(1+c)<1, exactly two solutions exist and are on opposite sides of
that plane. Distinctness of all twelve labels forces the new third
corner opposite the prescribed third corner. The smaller new triangular
disk therefore enters P at this shared side. It is an actual face by
Section1; its diagonal cannot cross P's boundary. A minor diagonal's
interior cannot pass through any other boundary vertex either. The
remaining two P corners are outside this empty triangle, and the rest
of P's boundary cannot cross the triangle's contact edges. Jordan
separation therefore puts this triangular disk on the inside of P;
the alternative would enclose the remaining P corners in the triangle.
In particular its diagonal interior is inside P, not in the other
subgraph region. This justifies noncrossing tests on ALL four candidates.

All32 subsets of the five possible diagonals are covered. Sixteen with
7-9 fail its strict noncontact. Of the remaining16, eight have a pair
of chords with alternating endpoints and are forbidden by embedding.
The remaining eight are the empty subset, four singletons and

    {U,V}, {U,W}, {V,Z}.

No triple is noncrossing. The pair{U,V} would give six distinct contact
neighbors at5, contrary to the degree bound. Each of{U,W} and{V,Z}
triangulates P into three contact triangles, two incident to5. Along
with the three prescribed triangles at5 these fill its whole five-sector
star with angle sum5*alpha<2*pi, impossible. Every new contact triangle
used here is an actual face; there are no hidden points or interior edges
in P. Thus at most one of U,V,W,Z is present.

## 4. Quadrilateral applicability and the three forbidden singletons

Any four distinct unit points with their four cycle sides contacts at
c>0 form a convex hemispheric smaller rhombus. To see this without an
irreducibility premise, write their opposites as a,d and b,e. The first
opposites cannot be antipodal, since each has product c>0 with b. Put
n=(a+d)/||a+d||. All four n projections are positive. The common-neighbor
equations give

    b+e=2c(a+d)/(1+a.d),
    (a-d).(b-e)=0.

Gnomonic projection in the n hemisphere therefore places a,d at opposite
nonzero points on one line and b,e at opposite nonzero points on a
perpendicular line. The ordered cycle is a convex diamond. Its two
opposite angles agree, and adjacent angles a0,b0 obey

    cot(a0/2)cot(b0/2)=c.                            (3)

For completeness write the corners as cos(u)n +/- sin(u)s and
cos(v)n +/- sin(v)t, with s perpendicular to t and0<u,v<pi/2.
Then c=cos(u)cos(v),
tan(a0/2)=sin(v)/(cos(v)sin(u)) and
tan(b0/2)=sin(u)/(cos(u)sin(v)), proving(3).
This is the classical rhombus identity, credited to
[Musin--Tarasov Proposition4.1(5)](https://arxiv.org/abs/1312.5450).
Each rhombus corner angle is at least alpha by the neighbor inequality.
In the singleton cases the chord splits P into its triangle and this
empty rhombus; with no further chord it is an actual quadrilateral face.

For singleton W or Z the rhombus contains5, where its angle is gamma
from(2). If b0 is its adjacent angle, then

    cot(gamma/2)<cot(2*pi/5)<1/3<c/sqrt(1+2c).       (4)

The middle comparison follows by squaring:
cot(2*pi/5)^2=(3-sqrt(5))/(5+sqrt(5))<1/9,
equivalent to sqrt(5)>11/5. The last follows from
9c^2-2c-1>0: this polynomial is increasing on K and is1/4 at1/2.
Since cot(alpha/2)=sqrt(1+2c), equations(3)-(4) give
cot(b0/2)>cot(alpha/2), hence b0<alpha, a contradiction. Both singletons
W and Z are excluded over the entire closed interval K.

For singleton U, the new triangle is(5,9,10) and Q=(5,7,12,10).
The angle at5 of Q is

    a0=2*pi-4*alpha in(2*pi/5,pi/2).

Thus cot(a0/2)>1 and, by(3), cot(b0/2)=c/cot(a0/2)<1.
The adjacent Q angle at10 satisfies b0>pi/2>a0. But10 has five
distinct required contact neighbors1,2,12,9,5. Its full star includes
three actual triangles(1,2,10),(1,10,12),(5,9,10), this Q, and one
other sector of angle at least alpha. Its angle budget gives
b0+4*alpha<=2*pi, or b0<=a0, a contradiction. Singleton U is excluded.
Only the empty subset and singleton V remain; sufficiency is not claimed.

## 5. Degrees and forced faces in the V branch

When no diagonal is present, P is an actual face. At5 its sector and
the three prescribed triangles exhaust the complete star; deg5=4.
In the V branch the new triangle(5,7,12) and Q=(5,12,10,9) subdivide P.
At5 four triangular angles leave the same a0=2*pi-4*alpha. In Q the
angles at5 and10 are a0, and those at12 and9 are b0>pi/2>a0.
The complete degree at5 is exactly5.

At12 there are already four distinct neighbors1,10,7,5, and two actual
triangles(1,10,12),(5,7,12), besides its Q angle b0. Degree5 would leave
two more sectors each at least alpha, forcing b0+4*alpha<=2*pi,
contrary to b0>a0. Hence deg12=4. At9 the prescribed triangle
(5,9,11) and Q are distinct incident faces. Degree5 would similarly
leave three other sectors, again forcing b0+4*alpha<=2*pi.
Consequently deg9<=4, with its three required neighbors5,11,10 retained.

At10 the required neighbors are1,2,12,9. The two B triangles and Q
leave the single outside sector from2 to9 with angle

    2*pi-2*alpha-a0=2*alpha.

If deg10=5, its fifth neighbor x must divide this sector into two gaps
at least alpha, so both equal alpha. The neighbor formula forces
x.2=x.9=c. These contact triples have the empty smaller triangular
disks of Section1, precisely the two incident sectors, hence are actual
faces(2,10,x),(9,10,x) inside R. The label x is distinct from10 and the
four required neighbors1,2,9,12. In fact it is not any original core
label. The remaining possibilities0,4,5,6,7,8,11 all fail:

|candidate x|obstruction|
|:---|:---|
|0|its four prescribed neighbors5,6,7,11 plus2,9,10 give degree7|
|11|its four prescribed neighbors0,5,6,9 plus2,10 give degree6|
|5|5-10 was excluded as U|
|7|7-10 was excluded as W|
|4|4 and10 have smaller tangent angle2*alpha>alpha at1|
|6|6 and9 have smaller tangent angle2*pi-3*alpha>alpha at11|
|8|8 and10 have smaller tangent angle2*pi-3*alpha>alpha at2|

For the last three rows, the prescribed consecutive triangular sectors
at the stated vertex supply the angles. In the first of those rows
2*alpha<pi; in the other two, (2) is below pi. The neighbor formula
therefore makes the corresponding pair a strict noncontact. This is a
necessary conclusion about x, not an assumption fixing an extra point.

## 6. The full fifteen-point allocation and component corollary

In the explicitly stated9813 cohort the full drawing has30 edges,
because the sum of face sizes is11*3+3*4+3*5=60. The eight prescribed
triangles are outside R. In the no-diagonal branch P uses one of the
three pentagons, leaving3T/3Q/2P in R. Ten edges beyond the G20 boundary
structure subdivide R. In the V branch its small disk contributes one
more triangle and one quadrilateral, leaving2T/2Q/3P in R; its chord
uses one of those ten new edges, so R has nine interior edges. Both
branches have three interior points and eleven boundary points. The
disk Euler counts are8 and7 inner faces respectively, matching the
stated face allocations. Extra core chords in R count as interior edges
and are not discarded.

In branch V its new triangle shares A's edge5-7, raising the A component
to at least5. If deg10=5, the first forced triangle shares B's edge2-10
and the second shares its edge10-x. They are two distinct new B triangles
outside P. Since x is outside the core, the eleven listed actual triangles
have precisely the two trees A5 and B6 under their COMPLETE shared-edge
adjacency. No edge is shared between those two sets: their point supports
intersect only at9 and12, and9-12 is a strict noncontact. All eleven
triangles are already used, so there is no further triangle or dual edge
that could connect them. The exact profile5+6 follows on all of K without
the earlier forest/separation theorem. Their nine total TT edges and
eleven triangular faces leave15 TN edges; the six nontriangles have27
sides, giving e=(27-15)/2=6 directly.

For the OTHER stated profile restrictions on J, the triangle-adjacency
forest is the9813 conclusion; A/B separation and the nine-profile list
are9906's independently proved wider-band theorem. Applying A-size>=5
to all their oriented assignments proves the remaining restrictions.
This imports no verdict on the present proof.

## 7. Certificate boundary and remaining frontier

[CERTIFICATE.json](CERTIFICATE.json), [check.py](check.py) and
[audit.py](audit.py) cover all32 diagonal subsets, both boundary pairings,
the exact rational comparisons behind(1),(4), the two disk allocations,
and all oriented A/B size assignments from the nine prior profiles.
The separate checkers are written by the same author. Their finite
checks support this ordinary proof; they do not independently establish
Jordan separation, spherical arc geometry, tangent-star applicability,
the imported8650 theorem or the wider9906 tree obstruction. No floating-point
pilot is a proof input or is needed at runtime.

This reduces the full G20 completion problem to a filled eleven-sided
region with two specified small-disk cases and added degree restrictions.
Its arbitrary-three filling capacity, complete possible contact-map
incidence, actual occurrence of G20 and global optimizer coverage remain
open. Earlier covering, forest and twelve-face results are credited
dependencies; classical planarity/contact/rhombus facts are not claimed
as new theorems. A bounded source/graph/literature refresh establishes
no exhaustive historical priority claim.
