# Half separators for annuli with arbitrarily subdivided inner rims

This extends the all-mass annular gluing conclusion beyond the
[unsubdivided exchange theorem](../planar_two_geodesic_annular_exchange/README.md).
Every inner-rim edge may now be subdivided arbitrarily in the unit-edge
setting. Occupied attachment sectors need not have a two-vertex cover.
The proof combines a cyclic exchange with complete coverage of a heavy
rim patch. It does not resolve unrestricted
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).

The preceding unsubdivided result has been
[independently confirmed](../planar_two_geodesic_annular_exchange_review1/REVIEW.md).
The present subdivision extension awaits its own independent review.

## Graph and metric assumptions

Fix k>=5. The branch vertices of H are r, a_i, c_i, with indices modulo
k. Its edges r a_i, a_i a_(i+1), a_i c_i, a_i c_(i+1) have a common
length lambda>0. The remaining edges form internally disjoint paths
T_i from c_i to c_(i+1), each of total length at least lambda. Their
internal vertices have degree two in H. Assume additionally:

    if T_i has internal vertices, its total length is at least 2lambda.

Individual edges on T_i may have arbitrary positive lengths. Thus this
condition permits every unit-edge subdivision, with no bound on the
number of new vertices. An unsubdivided rim edge may have any length
at least lambda.

Let G be a finite connected simple planar graph obtained by attaching
graphs to H, with no additional edges between vertices of H. Require
H to be isometric in G. Every component K of G-V(H), including any
zero-mass component, has boundary contained in one of

    {r}, {r,a_i}, {r,a_i,a_(i+1)}.

In particular no outside edge meets an internal rim vertex. The new
edge lengths may be arbitrary positive numbers consistent with core
isometry. New lengths at least lambda/2 suffice: an excursion between
distinct boundary vertices cannot improve on their length-lambda
clique edge. Vertex masses are arbitrary nonnegative real numbers;
W denotes their total. All shortest paths below are shortest in G.

**Light-attachment theorem.** If each outside component has mass at
most W/2, G has a separator equal to the union of at most two ambient
geodesics, leaving every component with mass at most W/2.

**All-mass corollary.** If every local torso G[K union N(K)] has
treewidth at most three, the conclusion holds for every mass assignment.
This includes planar peripheral cones with universal r and arbitrary
order, glued along any pattern of the root edges or triangles.

A useful conditional strengthening keeps a prescribed spoke
P=(r,a_j,c_j) or (r,a_j,c_(j+1)). Define the local rim patch

    Gamma_i = interior(T_i) union {c_(i+1)} union interior(T_(i+1)).

If each outside component and every Gamma_i are light, every prescribed
spoke P can be completed by one ambient geodesic. When a patch is
heavy, the proof may replace both paths. We do not assert the stronger
prescribed-spoke conclusion without this extra condition.

## A path with three possible attachment vertices

The heavy-patch step uses the following elementary metric lemma. It
does not require planarity, unit lengths, or an isometric path.

**Path-cover lemma.** Let T be a simple path in a positive-length graph,
with distinct endpoints u,v and an internal vertex m. If every other
internal vertex of T has degree two in the ambient graph, all vertices
of T can be covered by two ambient geodesics.

Write T as ears u--m and v--m of lengths A,B. Put

    p=d(u,m), q=d(m,v), s=d(u,v),
    z=(2A-p+q-s)/4, t=(2B+p-q-s)/4.

The triangle inequalities, A>=p and B>=q imply 0<=z<=A and 0<=t<=B.
On the first ear, take the last vertex at coordinate x<=z from u and
the first vertex at coordinate x'>=z. On the second, take coordinates
y<=t and y'>=t from v. If a cut coincides with a vertex, use that vertex
for both choices. There are no uncovered vertices between a predecessor
and its successor.

Join the outer two vertices by their ear prefixes and an ambient
u-to-v geodesic. Join the inner two vertices along T through m. These
two walks cover all of T. To check they are geodesics, the distance
between opposite-ear vertices at coordinates x,y is

    min(x+s+y, x+p+B-y, A-x+q+y, A-x+B-y).

Indeed, a route can enter and leave the ears only through u,m,v. Each
displayed quantity is also the length of a corresponding walk; removing
loops never increases length. For the outer choice, the first quantity
is minimal because

    2x <= A+q-s, 2y <= B+p-s, 2(x+y) <= A+B-s.

For the inner choice, the fourth quantity is minimal because

    2x' >= A-p, 2y' >= B-q, 2(x'+y') >= A+B-s.

All six inequalities follow from the cut definitions and p+q>=s;
rounding to the indicated adjacent vertices only helps. Thus both
walks attain the ambient distance and are simple, since lengths are
positive. This also handles degenerate terminal triangles and cuts
at endpoints. QED.

Apply this to T_i followed by T_(i+1). Its only possible attachment
vertices are c_i,c_(i+1),c_(i+2). Therefore two ambient geodesics cover
all of Gamma_i, even when these long rim arcs are far from isometric.
If w(Gamma_i)>W/2, deleting those paths leaves less than W/2 total mass.
This proves the theorem whenever a heavy patch exists. It is safe to
restore the original spoke in this case because the replacement covers
the entire heavy patch. This is the same complete-coverage principle
used in the reviewed
[isometric-fragment guard](../planar_two_geodesic_isometric_fragment_guard_review1/REVIEW.md),
with a different metric cover lemma.

## Sweep when attachments and patches are light

Assume every outside component and every patch has mass <=h=W/2.
Rotate and reflect so the prescribed spoke is P=(r,a_0,c_0).

Let Y(K) be the active vertices a_i in K's boundary. Discard, only for
mass bookkeeping, all components with Y(K) empty or {a_0}; P already
detaches each of them. Let their total mass be D. Put

    alpha_i = w(a_i) + sum_{Y(K)={a_i}} w(K) for i!=0,
    gamma_i = w(c_i) for i!=0,       alpha_0=gamma_0=0,
    tau_i = w(interior(T_i)),
    kappa_i = sum_{Y(K)={a_i,a_(i+1)}} w(K),
    M = sum_i(alpha_i+gamma_i+tau_i+kappa_i) = W-w(P)-D.

A sector aggregate kappa_i may be heavy: its individual components
are what matter when both portals are deleted. For 0<=i<=k set

    L_i = sum_{j<i}(alpha_j+gamma_j+tau_j+kappa_j),
    R_i = M-L_i-alpha_i-gamma_i,

using alpha_k=gamma_k=0. After deleting P, the spokes
U_i=(r,a_i,c_i), V_i=(r,a_i,c_(i+1)) have respective core-side bounds

    U_i: (L_i,R_i),
    V_i: (L_i+gamma_i+tau_i, R_i-gamma_(i+1)-tau_i).

These inclusions follow from the cyclic order. Components disjoint
from the surviving core are individual outside components and are
light. A formal side may group several actual components at the seam;
this only overestimates mass.

If none of these spokes completes P, exactly one side at each step
exceeds h, since the side sum is at most M<=2h. In the sequence
U_0,V_0,U_1,...,V_(k-1),U_k, the endpoint bounds are (0,M) and (M,0).
There is consequently a right-heavy to left-heavy transition.

**Transition along a rim arc: U_i to V_i.** Extend U_i into T_i as far
as the last vertex at or before its metric midpoint from c_i. Extend
V_i into T_i from c_(i+1) to the first vertex at or after that midpoint.
Both extended paths are ambient geodesics: the two endpoints of T_i
are each at distance 2lambda from r, and its internal vertices have
no other entrances. The first extension retains the light left bound
L_i; the second retains the light right bound
R_i-gamma_(i+1)-tau_i. Their other side bounds have disjoint mass
support: every internal vertex of T_i is removed by at least one
extension. Those two supports are contained in the represented mass M.
They cannot both exceed h. One extension therefore completes P.

**Transition across a sector: V_i to U_(i+1).** Put

    L=L_i+gamma_i+tau_i, R=R_(i+1).

Both are at most h. If either T_i or T_(i+1) has an internal vertex,
their total lengths sum to at least 3lambda. The path

    Q=(c_i,a_i,a_(i+1),c_(i+2))

is an ambient geodesic of length 3lambda. To see this, suppress the
degree-two rim vertices only for a distance calculation. Every branch
edge then has length >=lambda. The only possible two-edge route from
c_i to c_(i+2) is through c_(i+1), and it has length >=3lambda.
All other routes use at least three branch edges; k>=5 excludes the
two-edge wraparound route. The displayed path attains the lower bound,
and core isometry preserves it.

After P and Q are deleted, sector i's individual attachments detach.
Every remaining core component is contained in one of the old sides
bounded by L,R, or in Gamma_i. All three are light. This includes both
seams and the case c_(i+1) was already removed by P.

If neither adjacent arc has an internal vertex, tau_i=tau_(i+1)=0.
The previous local exchange applies even if other rim arcs are long.
Write alpha=alpha_i, beta=alpha_(i+1), gamma=gamma_(i+1), kappa=kappa_i.
Then M=L+R+alpha+beta+gamma+kappa, and the failed spokes imply

    R+beta+kappa>h, L+alpha+kappa>h.

The two geodesics (a_i,a_(i+1),c_(i+2)) and
(a_(i+1),a_i,c_i) have remaining side bounds (L+gamma,R) and
(L,R+gamma). If both also failed, L+gamma>h and R+gamma>h.
Adding the four inequalities gives 2M-alpha-beta>4h, contradicting
M<=2h. Thus one local choice completes P. These two-edge paths are
geodesics since suppressing rim arcs cannot make their endpoint
distance less than 2lambda.

This proves the light-patch prescribed-spoke statement, and together
with heavy-patch coverage proves the light-attachment theorem.

## Heavy attachments and scope

For the all-mass corollary, an outside component K with w(K)>W/2 is
handled by the
[reviewed local centroid reduction](../planar_two_geodesic_prescribed_attachment_review1/REVIEW.md).
Attach a width-three decomposition of its torso to the outside bag
V(G)-K along its boundary clique of order <=3. Assign K's masses to
local bags and all outside masses to that outside leaf. A weighted
centroid cannot be the outside leaf, so a local bag of order <=4 is
a half separator in the full G. Two paired ambient geodesics cover
the bag; deleting more vertices preserves balance. If no attachment
is heavy, apply the light-attachment theorem. Zero total mass is trivial.

The result allows arbitrary unit subdivisions of every inner edge,
arbitrary mass on all new vertices, and arbitrary occupied sectors.
It includes unbounded graph order and distance from r. The earlier
[rerooting theorem](../planar_two_geodesic_rerooted_attachments/README.md)
required a two-vertex sector cover when handling subdivided rims.
The present result instead requires total length >=2lambda for an arc
with internal vertices; very short positive-metric subdivisions remain
outside its statement. The earlier unsubdivided theorem also retains
a stronger prescribed-spoke and sharper residual bound in its scope.
No unconditional prescribed-spoke extension, arbitrary cyclic-interface
theorem, arbitrary core-shortening metric claim, or historical priority
claim is made here.

For example, one unit fixture has k=6, one new vertex on every inner
edge, and three ten-vertex peripheral components in sectors 0,2,4.
It has 49 vertices. Its displayed core has positive-mass subdivisions
and occupied-sector cover number three, so neither of the preceding
annular statements applies to that displayed core under uniform mass.
This compares their stated hypotheses, not every possible alternative
representation of the same graph.

## Exact checks

Run from the repository root with Python 3.11 or later:

    PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_subdivided_annuli/verify.py --check

The [checker](verify.py) validates the metric path cover on general
three-terminal models, full-graph component inclusions, the midpoint
disjointness and four-term identity, selected paths against original
distances, spherical embeddings, core isometry, local decompositions,
and final half balance. Every proof branch is exercised, including
replacement of the original spoke by a pair covering a heavy patch.
It includes positive internal edge lengths below lambda while their
arc totals meet the condition, multiple attachments per sector,
treewidth-four attachments in the light theorem, and rejection of a
short subdivided arc. Rejection is a hypothesis check, not a negative
separator claim. Compact results are in [expected.json](expected.json).

These are exact regressions, not independent review, a formal proof,
or a census. The checker imports earlier construction and elementary
graph utilities. The universal real-mass assertions rest on the written
metric inequalities and component inclusions. No solver is a premise.
