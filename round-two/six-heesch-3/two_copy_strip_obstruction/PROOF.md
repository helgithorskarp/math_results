# A uniform two-copy obstruction to the next surround

Actual author **six-heesch-3**, role **researcher**. This is an
author-checked geometric lemma; independent review and formalization
remain pending. The written argument proves the unbounded parameter
range. The finite exact checks share previously published polygon
primitives and do not replace that argument. No historical priority or
shape-wide finite Heesch upper is asserted.

Define the closed polygon T_m as the union of the following convex atoms,
with m hexagons. For j=0,...,m-1 its atoms are the regular hexagon with
center (4+8j,0), the upper triangle ((8j+2,2),(8j+4,4),(8j+6,2)), and,
when j<m-1, the bridge triangle ((8j+6,2),(8j+8,0),(8j+10,2)). Add the
terminal half-triangle ((8m-2,2),(8m,0),(8m,2)). Coordinates mean physical
(x,sqrt(3)y)/4. Pose (a,f,x,y) reflects y if f=1, rotates by30a degrees,
then translates. Bašić2021, DOI10.1007/s00283-020-10034-w, is the primary
construction context; its record theorem is not claimed as new.

For integers **m>=2, 1<=r<=m-1**, fix copies

    A=(0,0,0,0), B=(0,0,8r+4,-4).

**No packing of congruent copies with disjoint interiors containing A,B
can cover open neighborhoods of both u=(8r,0) and v=(8r+6,-2).**
Consequently A,B cannot both be covered by a further complete corona.
Added copies may use arbitrary Euclidean motions and reflections. Holes
elsewhere are allowed. A common Euclidean isometry preserves the claim.
No grid, mate, plane-tiling or global Heesch upper theorem is a premise.

The prototype's lower boundary walk starts at(0,0), passes through
(8j+2,-2),(8j+6,-2),(8j+8,0) for j=0,...,m-1, then reaches(8m,2).
The upper walk, starting at (8m,2), visits
(8j+6,2),(8j+4,4),(8j+2,2) for j=m-1,...,0, then (0,0).
These lower and upper chains are the entire simple boundary of the
atom union; collinear entries are harmless. Apart from the upper tips,
the nonflat angles are90,120,150,240 or300 degrees.
Reading these segments therefore gives minimum angle60 and exactly the
m60-degree corners (4+8j,4). Each such corner occupies directions
240..300 degrees. At every internal lower tip(8r,0), A occupies300
degrees and leaves the gap240..300. B is away from u: its minimum x is
8r+4. At v, A's120-degree sector is60..180 and B's straight180-degree
sector is240..420, leaving the gap180..240.

These statements concern local boundary sectors, so the union of just
A,B need not be a disc. The pair itself is a packing for every stated
parameter. A has y>=-2; B's hexagons, bridges and half-triangle have
y<=-2. In the band -2<y<0, A's j-th hex occupies the x interval
(8j-y,8j+8+y). B's upper triangles occupy intervals(8n+y,8n-y), where
n=r+1,...,r+m. These lie in gaps between the A hexagons, or beyond A.
Thus their interiors do not overlap.

Any packing of this fixed positive-area bounded polygon is locally
finite: copies meeting a fixed ball contain mutually interior-disjoint
inscribed discs of one positive radius inside a larger bounded ball.
There can be only finitely many such discs by area. Shrink a neighborhood
of the chosen point to exclude those finitely many closed copies that
do not contain the point. Filling that neighborhood therefore requires
copies containing the point. A straight
edge or interior point contributes at least180 degrees, and a reflex
vertex contributes more. Exactly one60-degree corner must fill each
gap, since every positive prototype angle is at least60.

Matching that corner's rays fixes its rotation and reflection, and
matching the vertex fixes its translation. Thus the **complete
arbitrary-motion** suppliers at u are

    U_j=(0,0,8r-4-8j,-4),
    V_j=(6,1,8r+4+8j,-4), j=0,...,m-1;

and those at v are

    L_j=(10,0,8r-2-4j,-2+4j),
    R_j=(4,1,8r+2+4j,-6-4j), j=0,...,m-1.

Let H be the regular hexagon with center(8r,-4). All following
coincidences concern **whole hexagonal atoms**, with indices0,...,m-1:

| Suppliers | Supplier hexagon | Identical old hexagon or remaining common hexagon |
|---|---|---|
| U_j, 0<=j<=m-2 | j+1 | B,0, center(8r+8,-4) |
| V_j, 1<=j<=m-1 | j-1 | B,0, center(8r+8,-4) |
| L_j, 1<=j<=m-1 | j-1 | A,r-1, center(8r-4,0) |
| R_j, 0<=j<=m-2 | j+1 | A,r-1, center(8r-4,0) |
| U_(m-1) | m-1 | H |
| V_0 | 0 | H |
| L_0 | 0 | H |
| R_(m-1) | m-1 | H |

All indices are in range, including m=2. The coordinate identities hold
as affine identities in independent m,r,j. The linear parts are
symmetries of the regular hexagon. Every supplier except U_(m-1),V_0
at u and L_0,R_(m-1) at v overlaps an old copy. Every remaining choice
at each point contains H, so a supplier at u and a different supplier
at v overlap in their interiors.

The same copy cannot supply both points. Their squared physical
distance is3. Any two distinct60-degree vertices of T_m have squared
distance4(j-k)^2, never3. Isometries preserve this distance. The
necessary suppliers must consequently be distinct, giving the desired
contradiction.

The supplied checker verifies eleven affine identities coefficient by
coefficient in independent symbols m,r,j. It reconstructs the prototype
boundary, pinned suppliers and displayed whole-hexagon coincidences on
twelve nonvacuous controls, including m=2. The two complete positive
fixtures contain actual strict disc coronas: Bašić's T6 six-corona patch
and a T7 five-corona patch. Their covered inner prefixes contain no
forbidden pair; the T7 final layer contains the example pair and hence
has no sixth corona. Eight damaged inputs are rejected.

The theorem requires no computer enumeration. The finite controls do
not prove an infinite range, and the supplied polygon implementation is
shared author code, rather than an independent audit or formal proof.
Only an explicit occurrence can reject a packing that must have a later
surround. An occurrence involving an uncovered final layer is admissible.
Absence of this pair proves neither extendibility nor a global Heesch
bound. See [README.md](README.md) for provenance and reproduction.
