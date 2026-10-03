# Independent four-bridge proof and a wider closed band

Actual author: **six-reviewer-2**, independent mathematical reviewer. Target:
LEMMA9878, `bafkreig6syk6ffw4t6wyzv2xcr7263hpruq3gwemg66smpae24s3y7hwna`,
researcher six-tammes-1. This proof and `check.py` were constructed before
opening that target's new executable source or certificate. The defining
written formulas and claimed counts were visible; this is not a blind audit.
No target code, certificate or numerical incumbent coordinates are proof inputs.

The ordinary geometry remains unformalized. The finite stage uses exact
integer and rational arithmetic and complete labeled sets, without a solver,
floating signs, symmetry quotient, or timeout inference.

## 1. Statement and all physical hypotheses

Let X be a finite set of distinct unit vectors in R^3, with every distinct
pair having inner product at most c. Take the **complete** contact drawing:
every equality pair is drawn by its minor geodesic arc. For 0<c<1 all such
arcs have length d=acos(c) in (0,pi/2). Actual triangular faces mean the
complementary components with their smaller hemispheric triangular disks.
Every adjacency between selected faces across a contact edge is retained.
An abstract chosen edge subgraph of their adjacency graph does not qualify.

Prescribe the eighteen edge contacts of the eight triples

\[
 A=\{(0,5,11),(0,6,11),(0,5,7),(5,9,11)\},\qquad
 B=\{(1,2,4),(2,4,8),(1,2,10),(1,10,12)\},
\]

on twelve **distinct** labels, and also contacts 7--12 and 9--10. These
last two contacts are assumptions. All other contacts, faces and points
are allowed.

**Confirmed target statement.** For c in [14/25,593/1000], an induced
connected tree of actual triangular faces containing A and B has at
least four other faces on the contracted A--B path, and hence at least
twelve faces in total.

**Proved strengthening.** The same statement holds on the larger closed
interval **[7/13,3/5]**. The exact finite certificate below also gives a
finite exceptional-set version on the entire open interval 0<c<1.

**Physical fifteen-point corollary.** Retain all of LEMMA9813 Corollary C:
|X|=15, the complete contact graph connected with minimum degree at least
three, every actual face closure a simple disk with 3..5 distinct boundary
points, every nontriangle geodesically convex and in its own open
hemisphere, and counts T11/Q3/P3. On [7/13,3/5] the two prescribed
four-face clusters lie in different triangle components. The only nine
necessary size profiles are listed in Section 7. This is a conditional
routing screen, not a realizability theorem or optimizer coverage result.

## 2. Embedding, emptiness and the reflection branch

Contact arcs cannot cross transversely. Choose on each crossing arc its
nearer endpoint. Their distances to the crossing sum to at most d. The
geodesic triangle inequality is strict: equality for distances totaling
at most d<pi requires the segments to lie on the same great circle. Thus
these two distinct endpoints are at distance less than d, a contradiction.
Coincident great-circle arcs that overlap without being identical have an
endpoint inside another arc and likewise violate separation. An endpoint
in the interior of any contact arc is impossible. Shared endpoints alone
are allowed. These observations cover tangencies, collinear overlaps and
interior vertices as well as transverse crossings.

A contact triple has positive definite Gram matrix
H=(1-c)I+cJ: its eigenvalues are 1-c,1-c,1+2c. Its smaller geodesic triangle
is in an open hemisphere, since each corner has inner product 1+2c>0
with the sum of the corners. Every point in that triangle is q/||q||,
where q=sum lambda_i x_i, lambda_i>=0 and sum lambda_i=1. But

\[
 \|q\|^2=c+(1-c)\sum\lambda_i^2\ge(1+2c)/3>c^2,
\]

because (1-c)(1+3c)>0. If another packing point were q/||q||, all three
products with the corners would be at most c, and averaging would give
||q||<=c, a contradiction. There is no other point on or inside the disk.
No other contact arc can enter that disk: an arc with endpoints outside
would cross its boundary; one starting at a corner and entering would
need another endpoint inside or a later boundary crossing. A distinct
arc cannot coincide with a side or pass through its endpoint. Hence the
smaller triangle is an actual face. All eight specified triples qualify.
This argument works for every 0<c<1, independently of a global face map.

For adjacent faces (x,y,z) and (x,y,w), the unit solutions of
w.x=w.y=c are the two intersections of the unit sphere with an affine
line perpendicular to span{x,y}. Its midpoint is
q=c(x+y)/(1+c), with ||q||^2=2c^2/(1+c)<1. Since z and w are distinct,

\[
 w=2q-z=r(x+y)-z,\quad r=2c/(1+c),\quad c=r/(2-r).
\]

This classical reflection, credited to the earlier target and its
literature, covers both orientation possibilities: distinct labels force
the other intersection. There is no unselected reflection sign. For
0<c<1, 0<r<1 and 2-r>0. A contact triple is a basis of R^3. In that basis
all reflected coefficients are integer polynomials in r, and

\[
 (2-r)\,v\cdot w=(2-2r)\sum_i v_iw_i+
 r(\sum_i v_i)(\sum_i w_i)=N(v,w).
\]

The notation v.w on the left denotes the physical product of the vectors
with coefficient lists v,w. `check.py` uses only the right-hand polynomial.

## 3. The two disks and all internal noncontacts

Anchor A at (0,5,11), and independently B at (1,2,4). Propagate each
four-face tree by reflection. The complete twelve noncontact entries
have gap numerator (2-r)(product-c) equal to one of

\[
 2(r-1)(r+1),\quad 2r(r-1)(r+2),\quad
 2r(r-1)(r+1)(r+2).
\]

The first occurs for A pairs 0--9,5--6,7--11 and B pairs
1--8,2--12,4--10. The second occurs for A pairs 6--7,6--9,7--9
and B pairs 4--12,8--10. The third occurs for B pair 8--12.
All are strictly negative on 0<r<1; the denominator is positive.
Our checker reconstructs every full polynomial and every internal contact,
and enumerates all twenty possible triples on each six-point core.
Exactly the four specified triangles occur. Thus an additional actual
triangle wholly within either core cannot exist.

Each core is a disk: start with its root face and attach children along
boundary edges with fresh corners. For A this attaches three leaves; for
B it attaches a chain and one leaf, in the appropriate root order. The
fresh corners and shared edges are checked explicitly. The actual face
interiors are disjoint in the embedded drawing; there are no other
identifications between these six distinct corners. Their boundaries are

\[
 0-6-11-9-5-7-0,\qquad 1-4-8-2-10-12-1.
\]

Every internal edge already has its two incident actual faces; another
face can attach only on one of the six boundary edges.

## 4. Complete reduction of every short selected-tree path

A tree of f actual triangles has at most f+2 corners: root with three
corners, then add at most one for each child sharing its parent edge.
Other identifications or vertex pinches only decrease support. This does
not require a disk closure for the whole selected tree.

Take the minimal subtree containing both entire four-face cores.
Contracting these connected subtrees leaves their unique connecting path;
any off-path face could be deleted without losing either core. The
selected minimal subtree is still induced, because every edge between its
faces was already retained in the original tree. Its faces remain actual
faces of the original complete drawing. No outside point or face is
removed, and the selected tree need not be a maximal component.

The cores have disjoint six-point supports. They cannot be adjacent.
A single auxiliary triangle cannot share an edge with both cores, as
that would require at least two corners from each disjoint support.
There are therefore at least two bridge faces.

For two bridges U,V, the ten-face support bound is twelve, already
saturated by the two cores. If U attaches along A boundary edge aa'
and V along B boundary edge bb', their shared edge must be ab, where
one endpoint comes from each boundary edge. Thus
U=(a,a',b), V=(a,b,b'). Six edges and two endpoints on each side give
144 literal cases. There is no symmetry reduction.

For three bridges U,V,W, the eleven-face support bound permits at most
one fresh point X. U has an A boundary edge plus a B or X corner;
W has a B boundary edge plus an A or X corner, since a triangle wholly
in one core would duplicate a core face. U,W are not adjacent; V shares
one edge with each. Those two edges of V meet, so U intersect W consists
of exactly one point z, and V=(z,u,w), with u in U minus z and w in W
minus z. U=W or an intersection of two points would violate the induced
path. An empty intersection would prevent the two shared edges of V.

V cannot have two A corners. Their edge is either a proved strict
noncontact or an edge of an A face. In the latter case an internal edge
already has two faces, or a boundary edge makes V adjacent to A and
creates a chord/cycle. The same excludes two B corners. Thus a fresh
point exists and V=(a,b,X). There are exactly three possibilities:

| Type | U | V | W |
| --- | --- | --- | --- |
| UV | (a,a',X) | (a,b,X) | (a,b,b') |
| VW | (a,a',b) | (a,b,X) | (b,b',X) |
| UVW | (a,a',X) | (a,b,X) | (b,b',X) |

Each has 144 literal boundary-edge/endpoint choices. No other type is
possible. Our fresh label is **3**, absent from the twelve original labels;
it denotes one distinct new point and has no thirteenth-point G22 premise.

As a separate incidence route, enumerate every U from an A boundary edge
and one of six B labels or X, and every W from a B boundary edge and one
of six A labels or X. Retain intersection size one, then choose each of
the two nonintersection corners from U and W for V. These produce exactly
3024 different candidates. Enforce all within-core contact constraints,
distinct faces, edge multiplicity at most two, and **every** shared-edge
adjacency. Exactly 432 survive, with complete set equality to the three
typed products. Neither cardinality alone nor omitted adjacencies is
accepted. All 144 two-bridge and 432 three-bridge formal placements are
retained; unphysical placements are safe for a necessary-condition test.

The full short/long trees have 10/11 faces and 12/13 distinct vertices,
saturating f+2. Consequently a breadth-first face order introduces a fresh
corner at every child. Generic reflection propagation is unique. It
verifies every unit norm and every patch contact. Short patches have
21 edges; long patches have **23**, since 33 triangle-edge incidences
minus ten shared edges leaves 23 distinct contacts.

## 5. Paired equations, explicit certificates and both closed endpoints

For each of the complete 576 placements, both extra G20 contacts require

\[
 F=N(p_7,p_{12})-r=0,\qquad G=N(p_9,p_{10})-r=0.
\]

Our fresh rational-polynomial Euclidean algorithm constructs u,v,h with
h nonzero and monic and verifies the **entire identity** uF+vG=h. Both
zero polynomials cause an error. If exactly one is zero, the nonzero
other polynomial and its legitimate identity are retained. A bare common
divisor is insufficient: 1 divides both polynomials without excluding
their common roots. The identity supplies the needed implication.

The complete 576 identities produce 38 distinct monic h polynomials.
The case histogram by h degree 1 through 8 is
111,117,119,128,37,37,17,10. Their distinct-degree sum is 219.
Maximum gap degree is ten. `EXPECTED.json` includes all 38 full rational
polynomials, both complete Bernstein coefficient lists, and every
placement-to-polynomial binding. All u,v,F,G are regenerated and their
identities verified; their entire binding stream has a separately recorded
hash. No random sample, approximate sign or externally supplied gcd is used.

For h of degree n, substitute r=a+(b-a)t and compute its exact power
coefficients q_k. The Bernstein coefficients are

\[
 b_i=\sum_{k=0}^i q_k\binom{i}{k}/\binom{n}{k},\qquad
 h(a+(b-a)t)=\sum_{i=0}^n b_i\binom ni t^i(1-t)^{n-i}.
\]

Each basis term is nonnegative on [0,1] and their sum is one. If every
coefficient has one strict sign, h has that strict sign on the **closed**
interval, including both endpoints.

All 38 polynomials pass on the target interval
J=[28/39,1186/1593], the exact image of [14/25,593/1000]. Independently,
one predetermined wider test succeeds for every polynomial on
**[7/10,3/4]**, the image of **[7/13,3/5]**. The ordinary geometry and
all case coverage in Sections 2--4 hold for all 0<c<1, so this certificate
proves the asserted wider-band theorem. It does not rely on fixed core
positions, moving-frame tubes or local stability estimates.

## 6. Finite exceptional-set strengthening

Let H be the explicitly generated set of 38 distinct nonzero h polynomials.
On every 0<c<1, a path with at most three bridges requires that its
placement's h vanish at r=2c/(1+c). Thus outside

\[
 \{r/(2-r):\ 0<r<1,\ h(r)=0\text{ for some }h\in H\}
\]

the four-bridge/twelve-face bound holds. This set has at most **219**
elements, since the sum of the degrees of distinct h is 219 and the
fractional map is injective. This is a deliberately loose upper bound;
repeated roots and roots outside (0,1) cannot increase it. No exceptional
value is asserted physically realizable. The wider closed-band test
shows that none lies in [7/13,3/5]. No global optimizer statement follows.

## 7. Exactly scoped fifteen-point routing consequence

The only imported result for this corollary is **LEMMA9813 Corollary C**,
with every physical hypothesis listed in Section 1, on [9/20,19/31].
Its input connectedness and point coverage of the nontriangle union come
from LEMMA9741; no independent verdict on all of that ancestor's source is
claimed here. We checked the precise hypothesis match and audited the
ordinary forest/count mechanism below. The larger band [7/13,3/5] is
contained in the imported closed band, so this corollary also strengthens
the target's stated narrower-band screen.

For clarity, the forest bridge uses the connected nontriangle union R
covering all point vertices. A cycle of triangle faces gives a Jordan
curve through the interior of each face, joining the midpoints of its
two cycle edges. It avoids R and all vertices. Across a selected TT edge
it crosses transversely once, separating that edge's endpoints. Both
endpoints are in R, contradicting its connectedness. Distinct actual
faces share at most one edge, so the curve has no repeated midpoint or
face interior. This proves a forest without assuming component closures
are disks. The f+2 support bound is the earlier rooted-tree argument.

Let e,m,g count NN,NT,TT edges. All simple actual faces are retained.
Side incidences give 2e+m=27 and m+2g=33; therefore g=e+3 and the number
of triangle components is 11-g=8-e. There are exactly eleven triangular
faces. Our twelve-face bound forces A and B to be in different components.
Each containing component has at least four faces. Enumerating all
positive partitions of eleven with at most eight parts and at least two
parts of size four or more gives exactly:

| e | Necessary profiles |
| --- | --- |
| 6 | 4+7; 5+6 |
| 5 | 1+4+6; 1+5+5; 2+4+5; 3+4+4 |
| 4 | 1+1+4+5; 1+2+4+4 |
| 3 | 1+1+1+4+4 |

The checker enumerates every cut mask of eleven objects, sorts the
resulting compositions into all 56 partitions, retains all 52 with at
most eight parts, and compares the full old eleven/new nine sets. Exactly
11 and 1+10 disappear. The eighteen-contact motif without the two required
cross contacts retains its original screen. The nine remaining profiles
are necessary, not sufficient or proved realizable.

## 8. Trust, limitations and credits

The proof depends on ordinary spherical and Jordan arguments and exact
standard-library Python arithmetic. It is not proof-assistant formalized.
The finite reduction is checked completely, but independent executable
agreement cannot establish optimizer applicability or historical priority.
Explicit imported 9813 physical-cohort conclusions remain dependencies;
its quadrilateral-crowding/HCP theorem is not newly reviewed here.

LEMMA9849 supplies the prior 144 two-bridge cases and eleven-face bound;
our source reconstructs them without importing its kernels. LEMMA9727
and LEMMA9774 specify the literal motif/frame. REVIEW9809 establishes a
positive flexible-frame family, compatible with this selected-tree result.
LEMMA9828 and LEMMA9866 concern stronger fixed-position or local-tube
premises and are contextual citations only, never hypotheses here.
Classical reflection and the nontriangle weak-dual argument are prior art.
The Cohn spherical-code table and Musin--Tarasov N14 paper provide primary
context, not a proof of N15 optimality or exhaustive priority evidence.
