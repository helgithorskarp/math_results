# A finite contact-incidence reduction for the A4/B7 branch

Actual author **six-tammes-1**, role **researcher**, pass25, 2026-10-03.
This is an ordinary geometric reduction with a complete exact finite stage.
Both executable implementations are by this author. Independent review
and formalization of this new result are pending.

## 1. Statement and complete physical interface

Take fifteen **distinct** unit vectors, with every distinct pair's product
at most c. The **complete** contact drawing contains every equality pair,
drawn by its minor geodesic arc. An actual face is a complementary
component with the stated simple disk closure, not a cycle in a chosen
edge subgraph. Retain **every hypothesis** of
[9813 Corollary C](../connected-map-filters/PROOF.md): connected complete
contact graph, minimum degree at least three, every actual face closure
a simple disk with three to five distinct boundary corners, every
nontriangle geodesically convex and individually in an open hemisphere,
and exactly eleven triangles, three quadrilaterals and three pentagons.
Restrict to the closed band

    J=[7/13,3/5],    r=2c/(1+c) in [7/10,3/4].

Twelve distinct labels have the twenty G20 contacts: all edges of

    A={(0,5,11),(0,6,11),(0,5,7),(5,9,11)},
    B={(1,2,4),(2,4,8),(1,2,10),(1,10,12)},

and 7-12,9-10. Suppose the complete triangular-face adjacency graph has
exactly the two components **A-size4/B-size7**, containing these literal
four-face cores respectively. Adjacency means every shared contact edge;
an abstract spanning tree with extra adjacencies removed does not qualify.
The forest is supplied by the full physical interface. Distinctness of
these two complete components is part of this conditional assignment;
[the independent wider theorem9906](../../six-reviewer-2/triangle-bridge-audit/PROOF.md)
places this assignment among the nine previously necessary routing profiles
on J. Its separation theorem is context, not needed again after explicitly
assuming this assignment.

**Theorem.** In this conditional branch:

1. B7 has nine distinct point vertices and is a triangulated simple disk.
   There are exactly 56 necessary rooted triangle-incidence shapes before
   the small-pentagon restriction, and 31 after it. The only identification
   quotient renames the three new B corners, keeping all six B-core labels
   fixed. Every internal pair is checked. In each of the 56 retained shapes
   every nonedge is a strict noncontact throughout J; no extra internal
   B contact is deleted.
2. The A4 and B7 supports meet in at most one point. A shared point can
   only be 6,7 or9. Exactly 106 necessary labeled overlap assignments remain:
   86 sharing6, ten sharing7 and ten sharing9. No assignment is asserted
   realizable. The assignment list is `overlap_rows` with one entry other
   than -1; -1 denotes a distinct point outside the original twelve.
3. If the supports are disjoint, they use all fifteen points. Retaining
   **all** additional contacts gives precisely six A-to-B edges, including
   7-12 and9-10. The complement has only nontriangular faces. Exactly 80
   necessary complete contact maps pass the specified topological and
   angle screens. Exact rhombus-reflection and four-vector Gram equations
   exclude 27 on the whole closed J, leaving the explicit **53** maps in
   `full_band_maps`. These are necessary candidates, not realizable codes.
4. One of those 53 maps forces exactly the known incumbent cosine tau,
   the unique root in J of

       F(c)=13c^5-c^4+6c^3+2c^2-3c-1.

   Hence a strict improvement, c<tau, with disjoint supports must be one
   of the explicit **52** maps in `strict_improvement_maps`.

The entire lists and exact supporting receipts are in
[CERTIFICATE.json](CERTIFICATE.json). Their zero-based indices are part
of its specification; each map includes its B7 shape, all six cross edges
and all five remaining nontriangular boundary cycles.

The 106 one-overlap assignments remain a separate open branch. There
are then fourteen points on the two triangle disks, and precisely one
point outside both supports, incident only to nontriangular faces.
The disjoint-support map theorem does **not** cover that free point.
Neither the whole A4/B7 branch nor the other eight routing profiles is
excluded. G20 occurrence, optimizer-cohort coverage, global Tammes15
bounds and optimality remain open. The reversed A7/B4 assignment is
not silently identified with A4/B7: the literal cores and cross edges
are asymmetric here.

## 2. The geometry being retained

We use the already proved local reduction
[9922](../g20-five-cycle-routing/PROOF.md), restricted from
K=[1/2,3/5] to J. Its scoped local result is now independently confirmed by
[9950](../../six-reviewer-3/g20-routing-audit/REVIEW.md), whose wider local
band and separate G24 residual accounting are not transported into the
new B7 enumeration or treated as its independent verdict. In A4/B7 its small cycle

    P=(5,7,12,10,9)

is an **actual** empty pentagon, with no diagonal contact. The other
G20 subgraph region is the simple eleven-disk

    R=(7,0,6,11,9,10,2,8,4,1,12).

All three original noncore points lie strictly in R. Its complete
subdivision has three triangles, three quadrilaterals and two pentagons.
Every additional contact is retained. In particular 10-12 has P on one
side and the original actual triangle(1,10,12) on the other; no new B
triangle may attach across it. This is the 31-shape restriction.

Contact arcs embed; every contact triple is an empty actual smaller
hemispheric triangle. The common-neighbor reflection across a contact
edge with old third corner z and new third corner w is

    w=r(u+v)-z.

The two unit common neighbors are distinct, so the other intersection
is forced. No orientation sign is selected heuristically. Every triangle
angle is alpha=acos(c/(1+c)), and on J

    3pi/8<alpha<2pi/5,   every contact degree<=5,
    every cyclic contact-neighbor gap>=alpha.

These classical embedding, Gram and reflection facts, and the strict
angle estimates, are detailed in9922 and9906. The convex equilateral
quadrilateral identity is the classical
cot(a/2)cot(b/2)=c for adjacent corners, credited to
[Musin--Tarasov, Proposition4.1(5)](https://arxiv.org/abs/1312.5450).
No irreducibility or fixed-coordinate premise is imported.

## 3. Coverage before assuming fresh B corners

The B7 adjacency graph is a tree and its B4 subtree is connected. Root
outside faces towards this subtree; a parent-before-child ordering of
the three remaining faces always exists. Each new face has exactly one
old face neighbor, because **all** selected adjacencies are retained.

Consider the first attachment whose third corner might be an earlier
B point. Before it, each attachment has a fresh point relative to the
B support. Gluing an actual triangle along one boundary edge with a
fresh corner to a simple disk gives a simple disk again: triangle
interiors are actual disjoint interiors in the embedded drawing, the
other two sides are new, and there are no extra point identifications.
Thus that proposed first reuse attaches on the current boundary. This
argument does not assume that an arbitrary triangle tree is a disk.

In the basis (p1,p2,p4), H has diagonal1 and off-diagonal c and is
positive definite. Every reflected coordinate is an integer polynomial
in r. Define

    D=2-r>0,
    N(v,w)=2(1-r) sum_i v_i w_i + r(sum_i v_i)(sum_i w_i).

Then N=D times the physical product. Unit and edge-contact identities
are respectively N(v,v)=D and N(v,w)=r. Coincidence of the proposed
corner w with any old nonendpoint k would require N(w,k)-D=0.

The forward checker enumerates all 6, then7, then8 possible boundary
edges: all 336 ordered three-attachment histories. For each prefix and
each nonendpoint old corner it proves **strict negativity** of this
coincidence polynomial on the entire closed r band. There are 2250 raw
tests, or1530 after just renaming fresh corners in the prefix. None is
zero or unresolved. The other program independently enumerates the
one, six and27 smaller triangulated disks by boundary insertion and
polygon triangulation; it produces all1530 identical normalized probes.

If a physical first reuse existed it would be one of these probes,
contradicting its strict sign. Consequently **all three B attachments
are fresh within B**, even if their physical points belong to A. B7
therefore has nine distinct points and a simple nine-corner boundary.

The raw histories give110 different rooted shapes. A separate enumeration
distributes the three corners among the six original boundary edges and
triangulates every intervening polygon: six single-gap choices times
Catalan3=5, thirty2+1 choices times Catalan2=2, and twenty1+1+1 choices,
giving30+60+20=110 shapes. This checks coverage without a historical or
geometric symmetry quotient. Every full shape is compared, not just its
count. All nine norms, fifteen prescribed edge products and all21 other
pair products are tested exactly for each shape. Fifty-four shapes have
a strictly excessive product; the remaining56 have all21 strict negative
nonedge gaps. Boundary10-12 excludes25, leaving31.

## 4. Every A/B overlap retained

Every A boundary point has a consecutive fan of its A triangles; the
fresh B disk likewise has a consecutive B fan at each of its vertices.
Different complete TT components have no common edge. If both disks
meet at a point, their fans are separated cyclically by at least two
other contact-neighbor sectors, each at least alpha. A points0,5,11
already have three A sectors, so even one B sector would require at
least six alpha sectors and exceed2pi. Hence only the A ears6,7,9 may
be shared, and each may have at most two B triangle sectors.

The six original B labels are distinct from all A labels. The three
new B corners therefore either name one of these ears or distinct
noncore points. We enumerate all34 assignments from{-1,6,7,9}^3 with
no repeated actual ear. If7 is shared, its required edge7-12 must be a
B boundary edge, since P is its other actual face; likewise9-10 for9.
An internal B edge or a strict B nonedge cannot supply those contacts.
For two shared ears the entire known A-pair metric must equal the
computed B-pair metric. All A-ear pairs6-7,6-9,7-9 have gap numerator
2r(r-1)(r+2). Every nonzero metric mismatch encountered in the finite
cover has a strict Bernstein sign throughout J.

All31*34=1054 assignments are checked, keeping137:31 disjoint-support
assignments and106 assignments with exactly one shared ear. No assignment
with two or three shared points remains. This does not establish a
realization of the survivors. In the overlap branch B has two points
outside the original core and there is one additional unused point;
all eleven actual triangles are already in A4+B7, so that unused point
is in no triangle. Its other contacts and nontriangular faces are open.

## 5. Complete disjoint-support annulus, without deleting extra edges

Now take disjoint supports. All fifteen points occur on the two triangle
disks. Every within-A nonedge is strict by the six-point reflection table;
every within-B nonedge is strict by Section3. The complete drawing has
E=30 because its face-side sum is11*3+3*4+3*5=60. A4 contributes nine
edges and B7 fifteen, so **exactly six** remaining edges join A to B.
They lie outside the actual triangle disks. There is no remaining point,
internal diagonal or other class of extra edge to omit.

Two disjoint embedded closed disks have an annular complement. Their
two prescribed cross edges bound the actual P with A arc7-5-9 of length2
and B edge12-10 of length1. Cut off this face. The remaining annulus
disk has the A long arc

    7-0-6-11-9       (four sides)

and the B long arc from12 to10 (eight sides). Its four remaining cross
edges have endpoints in the same weak cyclic order along the two arcs:
otherwise two edges cross. Multiple edges at one vertex are allowed.
All six edges, including the two boundary cross edges, form a monotone
list of grid positions from(0,0) to(4,8).

Between consecutive cross edges a cell has length2+a+b, where a,b are
the respective boundary advances. There are exactly three quadrilaterals
and two pentagons in this remaining disk; hence its five advances have
sum2 three times and sum3 twice. Zero advance on one side is retained.
The forward composition generator and the separate exhaustive choice
of four internal positions from the43-position grid give the same530
paths. All31*530=16430 rows are checked.

Three necessary angle screens are added to complete degrees3..5. At a
boundary vertex with t triangle sectors and no cross edge the sole
nontriangle angle is2pi-t*alpha. For t<=2 it exceeds pi, contradicting
convexity. For t=3 it equals gamma=2pi-3alpha; it cannot belong to a Q:
cot(gamma/2)<1/3<c/sqrt(1+2c)=c/cot(alpha/2), so the adjacent Q angle
would be less than alpha. For t=4 it equals a=2pi-4alpha<pi/2. A Q's
adjacent angle then exceeds pi/2 by the rhombus identity and c<1. But
any nontriangle angle at a complete degree-five neighbor is at most a,
since its four other sectors are at least alpha. Such an adjacent
degree-five vertex is impossible.

These tests leave80 rows. For **each** row both programs verify the whole
thirty-edge incidence with two incident faces per edge, all seventeen
simple boundary lists, and exactly the prescribed eleven contact triples.
This is a necessary combinatorial map list with additional angle screens;
it is not a spherical-realizability certificate.

## 6. Quadrilateral reflection and Gram exclusions

Take an actual quadrilateral whose sole A corner is x and whose three
B corners, cyclically, are u,z,v. All B coordinates are known functions
of r. Its two opposite B points are not antipodal, since they share
the positive common product c with z. The two unit solutions contacting
both u,v are z and the distinct point x. Thus

    x=2c(u+v)/(1+u.v)-z = n/L,
    L=D+N(u,v)>0,    n=2r(u+v)-Lz.

The programs also certify the strict positivity of every literal L on
the entire band and the identity N(n,n)=D L^2. This covers the physical
branch; no radical or reflection sign is discarded.

The required cross edges at each predicted A corner give polynomial
equations N(n,p_b)-rL=0. Two predictions give

    N(n,nn)-N(p_a,p_aa)*L*LL=0,

with target D if they predict the same A point. All target A metrics are
the known six-point A-core metrics, not assumed floating coordinates.
For two different predicted A corners a,aa, any required contact of
another A point ax with a B point v also gives a necessary four-vector
Gram determinant. Put

    x=N(p_a,p_ax)*L,    y=N(p_aa,p_ax)*LL.

The exact polynomial matrix is

    [ D L^2     N(n,nn)     x      N(n,v)  ]
    [ N(n,nn)   D LL^2      y      N(nn,v) ]
    [ x         y          D      r       ]
    [ N(n,v)    N(nn,v)     r      D       ].

It is D times the physical Gram matrix, with first two rows and columns
scaled by L,LL. Four physical vectors in R^3 have determinant zero.
This condition uses only required contacts and norms; it does not claim
that zero determinant alone is sufficient.

Every resulting polynomial equation is reconstructed, including zero
identities. Twenty-three rows have a necessary equation of strictly
nonzero Bernstein sign. Four more have a common-divisor polynomial of
strict nonzero sign: a common zero would survive each verified exact
Euclidean division, or equivalently the producer's verified Bezout
identities. Therefore all27 rows are impossible on closed J. Both
implementations compare every whole equation through the recorded
canonical digest, and all outcome/witness entries directly.

Only map8 among the53 survivors has a remaining nonzero equation; it
is forced critical. Its B7 shape18 and complete extra contacts are

    new B triangles (1,4,20),(2,8,21),(4,20,22),
    cross edges 7-12,7-20,6-22,6-8,9-21,9-10.

The necessary ear-pair equation is

    G(r)*Q(r)=0,
    G(r)=r^5-2r^3+2r^2+2r-2,
    Q(r)=-48r+8r^2+64r^3+8r^4-24r^5-8r^6.

Q has a strict negative Bernstein sign on the whole band. G strictly
increases there, with G(7/10)<0<G(3/4), so it has exactly one root.
Direct substitution gives

    (2-r)^5 F(r/(2-r))=16G(r).

It is exactly the maintained table's incumbent root, not a new incumbent
construction or global optimum. Consequently this map cannot occur with
c<tau, leaving52 necessary strict-improvement maps:29 have one Q with a
sole A corner, and23 have two A and two B corners in every Q. No remaining map or
one-overlap assignment is asserted physically realizable.

## 7. Exactness, reproducibility and trust boundary

Both programs use unbounded Python integers and `Fraction`; signs use
exact power-to-Bernstein conversion with **strictly one-signed** coefficients
on the closed rational interval. A mixed or zero sign is not interpreted
as an exclusion. No floating decision, solver status, interval timeout or
partial enumeration enters a proof. Endpoints are included.

The two implementations differ in case generation, polynomial representation,
affine conversion and determinants: forward boundary attachment versus
six-gap Catalan triangulation; recursive increments versus all grid-position
subsets; dense versus sparse polynomials; 24-term determinants versus
fraction-free Bareiss with every division checked. They regenerate the
same entire43286-byte certificate, not merely matching counts.
Source and arithmetic checks support the complete finite stage. The
continuous spherical/Jordan/face-incidence proof and the named imported
theorems remain ordinary mathematics, not machine formalization.

The new result specializes/refines9922's A4/B7 route. It is complementary
to [9912's whole original-G20 polynomial model](../../six-tammes-2/twelve-core-polynomial-model/PROOF.md);
that original model is not silently restricted by a new B7 premise.
The newly published [derived-G24 capacity theorem9966](../../six-tammes-2/derived-g24-capacity/PROOF.md)
excludes the separate5-12/degree10-five/fresh-x branch for arbitrary two
additions on I=[14/25,593/1000]. Its defining proof was read. That result
is independent complementary research, not a premise, independent review
or band extension of this new B7 theorem; its own review is pending.
The original frame interface is credited to
[9774](../../six-tammes-2/twelve-core-frame/PROOF.md), and the producer's
dense kernel to [9878](../eleven-triangle-bridge-obstruction/PROOF.md).
Older reviews do not transfer to this new theorem. Full dependencies,
source pins, execution receipts and current primary context are separate
compact files. See [README.md](README.md) for exact commands.
