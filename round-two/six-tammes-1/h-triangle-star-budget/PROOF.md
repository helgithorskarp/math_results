# Small-diagonal triangles have a three-contact center and a sharp point budget

Actual author **six-tammes-1**, role **researcher**, 2026-10-02.
Status: complete ordinary author proof with two separate exact auxiliary
checks. Independent mathematical review and formalization are pending.

## 1. Local model and precise statements

Let X be a finite set of distinct unit points with every different-point
inner product at most c, where **1/2<=c<=3/5**. The complete contact
graph joins exactly the pairs of inner product c by minor geodesic arcs.
Choose a family of its **actual simple strictly convex hemispherical
quadrilateral faces**. No conditions on the other faces, no global
degree lower bound, no N=15 or total face count are imposed here.
A bare four-contact cycle cannot replace an actual face.

Set

```text
alpha=acos(c/(1+c)), phi=2*pi-4*alpha,
rho(u)=2*atan(1/(c*tan(u/2))), y=rho(phi).
```

For each chosen Q whose equal opposite corners have angle u<phi, join
that opposite pair by its internal minor diagonal. These edges form H.
The comparison is **strict**. The definition and the ordinary Q identities
are credited prior work.

**Triangle-star lemma.** Every triangle of H, with vertices F0,F1,F2,
has a unique original point U of contact degree three. Its three neighbors
are exactly F0,F1,F2; its three incident faces are the Qs supplying the
triangle's edges, and each corner at U is strictly greater than y.
Conversely, a degree-three point whose three incident Qs belong to the
chosen family and all have corners greater than y gives such a triangle.
Each triangle vertex has contact degree three or four.

**Sharp point budget.** If k of the three triangle vertices have degree
four, then X has at least **7+k distinct original points**. For every
beta<c<=3/5 and every k=0,1,2,3, explicit unit packings with exactly 7+k
points attain the budget and have the required actual Q faces. Here beta
is the previously known root of

```text
P(c)=1+4*c+2*c^2-4*c^3-11*c^4-24*c^5
```

in (119/200,3/5). In particular H is triangle-free throughout
**1/2<=c<=beta**, including beta, and this threshold is sharp in the
stated local model.

**Convex-cell corollary.** If every remaining incident face at each
triangle vertex is also a simple strictly convex cell, all three vertices
have degree four. The patch then requires at least ten originals. Larger
convex faces are allowed in this corollary; they need not be T or Q.

The sharpness examples have degrees one or two elsewhere and an
unrestricted outer face. They do not provide a fifteen-point, nine-Q,
globally convex T/Q contact map, a Tammes-15 optimal configuration or an
optimizer-occurrence theorem. No endpoint transfer of the prior global
profile catalogues is claimed.

## 2. Credited facts and the closed endpoint calculation

Opposite Q corners agree, adjacent corners are u,rho(u), and each
diagonal bisects its endpoint corners. Completeness and the actual face
interpretation make both diagonals strictly longer than the contact
length: a shorter diagonal violates packing, and an equal diagonal
would be a contact edge inside the face. Consequently

```text
alpha<u<2*alpha, rho(alpha)=2*alpha.
```

These are classical equilateral spherical Q identities, credited to
[Musin--Tarasov, Proposition 3.2](https://arxiv.org/abs/1410.2536) and
the [geometric audit7182](https://github.com/helgithorskarp/math_results/blob/main/tammes_15_triangle_quad_exclusion_review1/README.md),
source f026ccec6854eb913e5c156f4ff0cf08ed5cb4a9. That review applies to
its earlier target and is not a verdict on this lemma.

On the **closed** current interval we still have

```text
3*pi/8 < alpha < 2*pi/5, alpha<phi<pi/2.
```

Indeed c/(1+c)<=3/8<cos(3*pi/8) and
c/(1+c)>=1/3>cos(2*pi/5). The strict last comparisons reduce respectively
to512<529 and45<49. This explicitly checks the endpoints rather than
inferring endpoint geometry from the closed polynomial certificates.

Every cyclic gap between contact tangent rays is at least alpha. If
a gap g<=pi, the cosine law for its two contact neighbors gives
c^2+(1-c^2)cos(g)<=c, hence cos(g)<=c/(1+c). If g>pi the bound is
automatic. Distinct original contacts have distinct tangent rays.
Since alpha>pi/3 and all gaps sum to2*pi, no point has six or more
contacts. This assertion is independent of face type and convexity
away from the chosen Qs.

The minor contact arcs form an embedding. An edge cannot contain another
original in its interior, since that original would be closer than the
contact length to an endpoint. If two different edges crossed
transversely, choose an endpoint of each within half the contact length
of the crossing. Their distance is strictly less than the sum of those
two subarc lengths, hence strictly less than the contact length. This
violates packing. Overlapping collinear edges would likewise contain an
original in an edge interior. Thus actual faces and cyclic contact links
have their usual embedded meaning.

Two distinct unit points have at most two common positive-c contacts.
Their two affine contact planes meet in a line with at most two sphere
intersections. The only dependent case is antipodality, which admits
no common positive-c contact. In particular a Q opposite pair fixes
its two other corners. Its convex hemispherical interior is unique,
so H has no repeated edge. A Q has at most one selected opposite pair:
u<phi<pi/2 implies rho(u)>2atan(1/c)>pi/2>phi. The selected diagonals
lie inside different actual cells.

The [full-interval five obstruction9410](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/full-interval-five-diagonal-triangles/PROOF.md),
source bb2ba13cb84f908ed428e28e55db4b2c04af27ed, proves the following
angle estimates on the open interval. Here the strict estimates are
recalled with the endpoints checked explicitly. If v=rho(u) is adjacent
to a selected corner, the diagonal product s satisfies

```text
s=c^2+(1-c^2)*cos(v),
s>4*c^2/(1+c)-1 >= -1/3,
s<(3*c^2-1)/(1+c^2) <= 1/17 < 1/16.
```

The first strict inequality uses v<2alpha. The second uses u<pi/2,
so tan(v/2)>1/c. The lower rational expression increases with derivative
4c(2+c)/(1+c)^2 and equals-1/3 at1/2; the upper expression increases
with derivative8c/(1+c^2)^2 and equals1/17 at3/5. Thus the side window
(-1/3,1/16) stays strict at both endpoints.

For three side products r,s,t in this window, their products lie in
(-1/48,1/9) and K=sqrt((1-s^2)(1-t^2))>8/9. The spherical cosine law
for each smaller angle theta gives

```text
cos(theta)=(r-s*t)/K,  -1/2<cos(theta)<3/32,
7*pi/16<theta<2*pi/3.                              (1)
```

For the cosine bounds, the numerator lies in(-4/9,1/12), with the
division split according to its sign. For the lower angle comparison,
cos(7*pi/16)=sin(pi/16)>1/8>3/32 by strict sine concavity. These bounds
also exclude a degenerate triangle. The coarse product window was
already used in the [odd-degree proof7817](https://github.com/helgithorskarp/math_results/blob/main/tammes15_nine_quad_odd_degree_reduction/PROOF.md),
source d6547391ae745a70087f067568047c8dbba0e099; it is credited, not a
new inequality here.

No H triangle contains a five-contact point, now also at the endpoints.
At such a corner the two incident Qs cannot be separated: both bisector
sectors would exceed (u+v)/2+alpha>2alpha>3*pi/4, contradicting(1).
If consecutive, the smaller sector is (u+v)/2<phi<pi/2. The other three
contact gaps sum to at least3alpha, giving
theta<=pi-3alpha/2<7pi/16, again contradicting(1). This is9410's ordinary
mechanism with the closed parameter calculations supplied above.

## 3. Original center identification and its full contact link

Consider an H triangle F0,F1,F2. A triangle corner cannot have degree
zero or one because a Q supplies two distinct contacts. If a corner
had degree two, its two different incident Qs would use the same two
contacts A,B. Then A and B would have all three Fi as common contacts,
contradicting the positive-c plane bound. Degrees above five were ruled
out by the gap budget, and degree five by Section2. Thus each corner
has degree three or four.

The two incident Qs at a corner must be consecutive. Otherwise both
bisector sectors contain another complete contact gap and exceed
2alpha>3*pi/4, inconsistent with(1). Let Ui be the actual shared contact
on their common boundary edge at Fi. Because the two Qs have opposite
corners Fi,Fj and Fi,Fk, Ui contacts **all three** F0,F1,F2. If Ui and
Uj were different originals they would have three common contacts,
again impossible. Hence Ui=U for all i.

This shared-neighbor observation is the consecutive-corner ingredient
already used below beta in7817 Section5. The full-interval correspondence,
sealed center, original-point budget and sharp examples are the additions
developed here.

Write the three actual faces, with original labels, as

```text
Q01=(U,F0,W01,F1), Q12=(U,F1,W12,F2), Q20=(U,F2,W20,F0).
```

At U these actual corners force the three neighbor-link edges
F0-F1,F1-F2,F2-F0. In a cyclic contact link a complete three-cycle cannot
be a proper subgraph of a longer cycle. Thus U has exactly the three
contacts Fi and these three Q sectors, with no additional contact ray.
This reasoning needs the actual face interpretation: a proposed four-edge
cycle could otherwise conceal an additional edge in a corner.

The angle at U in Qij is rho(uij)>rho(phi)=y, where uij<phi is the
selected equal angle at Fi,Fj. Conversely a degree-three point with
three chosen Q sectors all greater than y has opposite endpoint angles
rho(v)<phi; each neighbor pair is therefore an H edge. Distinctness is
provided by the original contact star and simple Qs. The positive-c
common-contact bound makes the center unique in both directions.

No convex H-triangle-face assumption, hidden halfplane correspondence,
fresh-original naming convention or total-face count is used to identify
the center.

## 4. The 7+k point budget and the convex-cell corollary

The three Ws lie outside {U,F0,F1,F2}. Simple faces exclude U and the
two adjacent Fi; equality with the third Fi would make an H diagonal
a contact. If two Ws agreed, that point and U would share all three Fi
as contacts. Thus U, the three Fs and the three Ws are seven distinct
original points.

If Fi has degree four, let Ji be its fourth contact besides U and its
two adjacent Ws. Ji is different from those three and from Fi. It
cannot be another F, since the F pairs are noncontact Q diagonals. The
only other core candidate is the nonadjacent Wjk. That point and U
already have Fj,Fk as common contacts, so a new Fi contact would be a
third. Consequently Ji lies outside the seven-point core.

Two different Ji,Jj cannot agree. Fi,Fj already have U and Wij as two
distinct common contacts; their common fourth contact would be a third.
Therefore k four-contact triangle corners require k distinct additional
originals, establishing |X|>=7+k.

At a degree-three triangle corner, the two consecutive selected Q angles
u,v satisfy u+v<2phi<pi. The remaining face sector has angle
2pi-u-v>pi. If that incident face is a simple strictly convex cell this
is impossible. Thus in the convex-cell corollary every triangle corner
has degree four and the original point budget is ten. Larger convex
cells are permitted; only the strict local corner bound is used.

## 5. The exact threshold, including beta

The three angles at U exceed y and sum to2*pi, so an H triangle requires
y<2pi/3. Put D1=1+2c-c^2, which is positive on the closed interval.
The half-angle identities give

```text
tan(phi/2)=2c*sqrt(1+2c)/D1,
tan(y/2)=D1/(2c^2*sqrt(1+2c)),
D1^2-12c^4*(1+2c)=P(c).
```

All quantities being compared are positive and y/2 is in(0,pi/2).
Thus y>=2pi/3 is equivalent to P(c)>=0. These polynomial and threshold
identities are prior work in7817/7182. Uniqueness of the root can also
be checked directly on[1/2,3/5]:

```text
P'(c)=4+4c-12c^2-44c^3-120c^4
     <=32/5-3-11/2-15/2=-48/5<0,
P(1/2)=25/16>0, P(3/5)=-112/3125<0.
```

The bracket(119/200,3/5) is confirmed exactly in the source. Consequently
an H triangle is impossible for1/2<=c<=beta. At c=beta the angles at
U are still **strictly greater** than y=2pi/3 because H selects u<phi;
their sum cannot be2pi. This endpoint result concerns this H graph,
not other marked-angle capacity statements or global catalogues.

## 6. Exact packings attaining every budget above beta

For any **beta<c<=3/5**, set a=sqrt(1-c^2), D0=1+3c^2 and h=4c/D0.
With i=0,1,2 define

```text
U=(0,0,1),
Fi=(a*cos(2pi*i/3),a*sin(2pi*i/3),c),
Wij=h*(Fi+Fj)-U    for ij=01,12,20,
Ji=(2c*Fi_x,2c*Fi_y,2c^2-1).
```

Use U, the three Fs, the three Ws and any chosen subset of the three Js.
The Fs and Js are unit by direct calculation. For a W,
Fi dot Fj=(3c^2-1)/2 and its definition gives unit norm and contacts
Fi dot Wij=Fj dot Wij=c. This is the elementary two-contact reflection
construction; that mechanism and the symmetric three-ray fan are credited
classical ingredients.

Let q=(5c^2-1)/D0. All remaining pair products are:

| pair | product |
|---|---|
| U,Fi or Fi,Wij (incident) or Fi,Ji | c |
| distinct Fi,Fj | (3c^2-1)/2 |
| U,Wij | q |
| Fi, nonadjacent Wjk | c*(9c^2-5)/D0 |
| distinct Ws | (3q^2-1)/2 |
| U,Ji | 2c^2-1 |
| Fi,Jj, i!=j | c*(3c^2-2) |
| Wij,Ji or Wij,Jj | (6c^4-3c^2+1)/D0 |
| Wij,Jk, k outside ij | (18c^4-15c^2+1)/D0 |
| distinct Ji,Jj | 6c^4-6c^2+1 |

Every noncontact product is strictly below c, even on the entire closed
[1/2,3/5] interval. The programs give exact positive Bernstein coefficients
of all nine noncontact gap numerators after multiplication by D0^2>0.
All45 different-point pairs of the largest ten-point construction and
all ten unit norms are checked as polynomial identities. A smaller
chosen-J subset inherits these bounds. Thus these are exact finite
packings and their **complete** contact graphs have exactly nine plus k
edges: UFi, the six incident Fi-Wij edges, and the chosen Fi-Ji edges.
There are 7+k distinct points; all three Fi have degree3 or4 as prescribed.

The three proposed Qs are actual simple strictly convex hemispherical
faces, as follows. Their vertices all have positive z:
U_z=1, Fi_z=c>0, Wij_z=q>=1/7>0. Apply gnomonic projection (x/z,y/z)
to this hemisphere. If B=sqrt(3)*(1-c^2)/2>0, the four successive
homogeneous corner determinants of Qij=(U,Fi,Wij,Fj), starting at U,
are

```text
B, h*B, B, h*B.
```

They are positive. More explicitly, after scaling the projected Fs to
unit planar radius, the polygon is(0,p,lambda*(p+r),r), where p,r are
120 degrees apart and lambda=4c^2/(5c^2-1)>1/2. Its four turns are
positive, so it is a simple strictly convex quadrilateral. These are the
three disjoint120-degree azimuth wedges between successive Fi rays;
the Q interiors are disjoint and contain no other construction point
or contact arc. Therefore they are actual faces of the complete graph.

Adding any Ji preserves those faces. Ji has negative z=2c^2-1 and lies
on the outward meridian through Fi, at colatitude2d if Fi has colatitude
d=acos(c). The minor Fi-Ji arc runs outward from d to2d on the boundary
azimuth of its two Q wedges, beyond Fi. It does not enter a Q interior.
The three different meridians do not intersect on these arc segments.
The noncontact gap certificates exclude every other potential edge.

The Q angle at U is exactly2pi/3, and the equal angle at Wij is the
same. Each Fi Q angle is rho(2pi/3). Since c>beta, P(c)<0 gives
y<2pi/3, equivalently rho(2pi/3)<phi. Thus each Fi-Fj diagonal is
selected; the large U/W pair is not selected. H has exactly the triangle
F0,F1,F2. Any subset of k Js supplies the required k four-contact corners,
attaining every 7+k budget. The rational c=599/1000 is an explicit
exact instance in the upper strip; no floating-point coordinate input
or approximate inequality is used.

For k=0 the outer boundary has six edges and the outer face has corners
greater than pi at the Fs. For k>0 the outward pendant contact edges
give repeated outer boundary vertices. The Ws have degree two, and the
Js degree one. These features specify exactly which global convex-cell
and fifteen-point hypotheses the sharpness family does not satisfy.

## 7. Exact checks and reproducibility boundary

Use CPython>=3.11, standard library only. From this directory:

```sh
python3 -B check.py > replay.json
cmp replay.json EXPECTED.json
python3 -B -O check.py > replay-optimized.json
cmp replay-optimized.json EXPECTED.json
python3 -B audit.py > audit-replay.json
cmp audit-replay.json EXPECTED.json
python3 -B -O audit.py > audit-optimized.json
cmp audit-optimized.json EXPECTED.json
```

Both programs generate the entire compact certificate without external
runtime inputs. check.py constructs Cartesian polynomial coordinates in
the radical quotient a^2=1-c^2,b^2=3, all with denominator D0. It computes
all ten norms,45 products and12 homogeneous turns directly. audit.py
imports no primary code: it uses latitude/phase Gram data with six rational
phase cosines and the factored gnomonic turns. Primary Bernstein coefficients
use affine substitution followed by the power-to-Bernstein map; the audit
uses direct polarized coefficients. All entries agree, not only totals.

The original-alias budget is checked by a primary recursive neighbor-set
cover and an audit of all raw labeled assignments using bit incidences.
There are1,8,81,1000 candidate maps for k=0,1,2,3, with1,1,2,6 retained
fully distinct fresh-label assignments. The accepted entries explicitly
have7+k points. Removing the common-contact cap admits seven-point
abstract assignments; these are relaxed incidence controls, not unit
packings. The center-link audit compares actual cyclic permutations with
raw Hamiltonian edge subsets. It retains only the two orientations of
the degree-three link. All19 pairs of Q positions at degrees3/4/5 are
retained with their separate consecutive/separated classifications.

Controls also reject a changed reflection norm, a repeated fourth-contact
alias and a contact diagonal. The repeated alias is the fixture for both
the duplicate-center and shared-fourth-contact plane obstructions; these
are not advertised as independent fixtures. Exact P-sign controls include
599/1000 above beta and119/200 below beta. Requirements use explicit
exceptions and remain active under Python-O. [VALIDATION.json](VALIDATION.json)
records actual sequential runs and [MANIFEST.json](MANIFEST.json) the compact
source bytes.

The actual face/corner interpretation, plane/sphere bound, strict angle
budgets, geometric correspondence, gnomonic convexity and actual faceness
are ordinary written proofs. The code verifies their algebra and finite
encodings, not those bridges by itself. Closed polynomial certificates
do not substitute for the explicit endpoint argument in Section2.
Separate algorithms by the same author do not establish independent
researcher review. No solver, large proof corpus, private ledger, peer
certificate or floating-point input is required.

## 8. Use in the Tammes-15 structural frontier

The local classification supplies an original degree-three center and
a ten-original budget whenever a remaining H triangle has convex incident
cells. It identifies the precise exceptional structure that a global
proof must handle in the upper strip. Actual H can have a four-contact
triangle in the local model above beta; the graph H* obtained by deleting
four-four edges is not interchangeable with it in original face arguments.
The previously published32-profile H* reduction keeps its own open
interval and global nine-Q premises.

The [Cohn table](https://cohn.mit.edu/spherical-codes/) and
[N15 coordinate table](https://spherical-codes.org/data/3/15) remain primary
status sources; the incumbent cosine is0.59260590292507377809642492233276,
unstarred at the current refresh. The [N14 theorem](https://arxiv.org/abs/1410.2536)
is context, not an N15 solution. The symmetric local fan, Q identities,
contact-plane reflection and below-beta shared-neighbor observation are
credited prior ingredients. Bounded primary and repository searches did
not locate this exact closed triangle-star/budget/sharpness statement;
no exhaustive historical-priority claim is made. Global numerical bounds,
the original fifteen-point face/degree classification and optimizer
occurrence remain open.

The tabulated incumbent cosine is below119/200<beta. Thus the sharp local
examples above beta are outside the parameter range of a strictly better
packing. Their role is to certify the auxiliary graph's exact local scope
and distinguish literal H from H*, rather than narrow the present global
optimum gap. A global occurrence/domain bridge to a relevant excluded core
remains a separate substantive frontier.
