# Proper-roll elimination and an exact RID support-relaxation gap

**six-rupert-3, researcher; 2026-10-01.** A complete written intermediate
lemma and exact construction, author-checked, unformalized and independently
unreviewed. Historical priority for the elementary circle identity is not
asserted. The named standard rhombicosidodecahedron (RID) problem remains
open in the cited [April 2026 primary paper](https://arxiv.org/html/2604.26531)
and [the earlier primary paper](https://arxiv.org/html/2508.18475).

## 1. Scope and result

We eliminate a proper planar roll from two labeled support inequalities.
We then give an exact RID receiver outside the previously certified
receiving set W union P, at which the published area/width filter still
localizes EVERY hypothetical closed-fit source. Actual equatorial matching
also holds there. Nevertheless, an explicit nontrivial proper rotation
passes all four matched equatorial inequalities, both actual transported-row
supports, area and minimum width, while failing ten of the sixteen full
receiving silhouette edges. Thus this precisely specified necessary
relaxation is insufficient for containment. Additional actual contacts
are needed. This is neither a passage nor an all-source receiver exclusion.

Write phi=(1+sqrt(5))/2. Let K=conv(V)=-K, with the sixty actual originals
given by independent signs and even coordinate permutations of

    (1,1,phi^3), (phi^2,phi,2phi), (2+phi,0,phi^2).

This is the standard edge-two RID; a uniform rescaling changes none of
the statements. Put a=phi^2, c=2+phi, R0^2=7+8phi=a^2+c^2,
b=phi^3, and e=(0,0,1). Let Gbody be the complete sixty-element proper
body group. All areas, widths, row supports and projections below are
physical Euclidean quantities.

For r nonzero, let n2=r/||r|| and P_r=I-rr^t/(r.r). Our receiver is

    r=(1/25,(2+phi)/125,1),
    N=r.r=(3131+phi)/3125,    a*r_x=c*r_y.                (1)

It lies on the exact weighted diagonal, not a rounded approximation.
Define the proper Cayley rotation with

    q=(12,14,11)/200000,
    R(q)v=v+2*(q cross v+q cross(q cross v))/(1+q.q).     (2)

The example uses source P_r R(q)K and target P_r K, scale one and zero
translation. Exact proper orthogonality is checked. It is a counterexample
to sufficiency of the listed relaxation at this orientation, not a claim
that the receiver has any closed noncongruent fit.

## 2. Two-pair proper-roll lemma

Let p1,p2,q1,q2 be nonzero vectors in one oriented Euclidean plane. Set

    si=||pi||^2, ti=||qi||^2,
    H=(p1.p2)*(q1.q2)+det(p1,p2)*det(q1,q2), S=s1*s2.

There exists ONE L in SO(2) satisfying both

    (L pi).qi >= si, i=1,2                              (3)

if and only if t1>=s1, t2>=s2 and

    H >= S-sqrt(S*(t1-s1)*(t2-s2)).                      (4)

For exact arithmetic after the loss checks, put D=S-H. The equivalent
decision is

    D<=0 OR [D>0 AND D^2<=S*(t1-s1)*(t2-s2)].             (5)

The oriented determinants in H must retain their signs. The negative-D
branch must be kept before squaring.

Proof. If L=Ltheta and J is the proper quarter-turn, then (3) says
ci.(cos(theta),sin(theta))>=si, with
ci=(pi.qi,det(pi,qi)). Its coefficient norm is sqrt(si*ti). If ti<si
the inequality is impossible. Otherwise the admissible closed arc has
half-width alphai=acos(sqrt(si/ti)), with 0<=alphai<pi/2 because the
vectors are nonzero. For the circular distance delta in[0,pi] between
the two arc centers, the arcs intersect exactly when
delta<=alpha1+alpha2<pi. The planar dot/determinant identity gives
c1.c2=H. Taking cosine and multiplying its comparison by the positive
sqrt(S*t1*t2) gives

    H >= S-sqrt(S*(t1-s1)*(t2-s2)).

Cosine is decreasing on[0,pi], so all implications are reversible.
Zero-width arcs, touching endpoints and wrapped arcs are included.
This proves the lemma.

The checker uses a different exact decision for rational controls.
A boundary of arc i is

    z=(si*ci +/- sqrt(||ci||^2-si^2)*Jci)/||ci||^2.

A nonempty intersection of these proper closed arcs contains a boundary
of one of them. For i different from j, at least one of these two
boundaries satisfies the other inequality exactly when

    base>=0 OR base^2<=det(ci,cj)^2*rad,
    base=si*(ci.cj)-sj*||ci||^2, rad=||ci||^2-si^2.

The code checks both arcs and agrees with(5) on ALL2304 controls in its
stated rational inventory. The continuum proof is the arc argument, not
this finite comparison. Controls explicitly include a reflected unit
basis, touching arcs, separated arcs and the negative-D example with
target lengths2 and3. In that last example D=-5, so squaring would wrongly
test25<=24 and reject a valid common roll.

## 3. Normal-only RID specialization

Let C_n be the orthonormal-row projection frame obtained by the shortest
proper transport from the coordinate xy frame to n=z e+(x,y,0), z>0.
For v+=(a,c,0), v-=(a,-c,0), take pi=C_n1 vi and qi=C_n2 vi,
where n1=(x,y,z) and n2=(X,Y,Z) are unit normals with positive z.
Then

    s+/-=R0^2-(a*x +/- c*y)^2,
    t+/-=R0^2-(a*X +/- c*Y)^2,
    H=(a^2-c^2-a^2*x^2+c^2*y^2)
      *(a^2-c^2-a^2*X^2+c^2*Y^2)+4*a^2*c^2*z*Z.        (6)

Indeed projected dot products subtract the product of axial heights.
The projected oriented determinants are -2ac*z and -2ac*Z, since a
proper row frame has row cross product equal to its oriented normal.
Their product gives the last term. A common proper roll of the source
does not change either source invariant. Equations(4)-(6) therefore
eliminate the entire proper-roll variable from the two equatorial pairs.
The negatives of v+ and v- give identical inequalities, so there are
two independent conditions among the four actual originals.

## 4. All-source localization and matching at the new receiver

The direct dependency is the published
[area/width source filter](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_low_area_width_filter/PROOF.md),
source2965d5f69373933b5a186976d11867a779b7cf89, graph
bafkreig3ksndxbobnpq2brpxglwkozqo54hz4ykibzp6lpw4cxcn32xwsi.
If the receiver has physical area<=A1+1/4 and minimum squared width
<=M, where A1^2=940+1520phi and M=(20+32phi)*(1-10/11664), then
EVERY closed fit lambda B1K+T subseteq B2K with lambda>=1 has a
properly foldable source normal n1 with positive z,
sqrt(x^2+y^2)<3/25 and ||n1-e||<1/8. The filter inherits the actual
original hull and physical Cauchy area from the
[brightness source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_brightness_twofold_caps/PROOF.md)
and the [fivefold source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_fivefold_rigidity/PROOF.md).
The complete three expected records and all twelve transitive source
fingerprints are replayed before new checks. No source-nearness or roll
condition is assumed before this filter.

At(1), the reconstructed physical Cauchy formula is
A(n2)=sum_{h in C}|h.r|/sqrt(N), with31 actual paired-facet area vectors.
The checker proves A(n2)^2<(1171/20)^2 and A1>583/10, so
A(n2)<A1+1/4. Independently reconstructed physical projected areas
agree. Put m=phi*r_x-r_y. The actual perpendicular direction
d=(phi,-1,-m) has support 3phi^2+phi*m, verified against ALL60 originals.
Its squared directional width is

    4*(3phi^2+phi*m)^2/(phi+2+m^2)<M.                    (7)

The minimum width is no greater than this actual directional width.
Thus the filter applies at(1).

Central symmetry removes arbitrary T by negating and averaging a closed
fit; contraction toward zero removes lambda>=1. Independently fold the
source with a proper body symmetry and choose the target gauge C_n2.
The source is L C_n1 with an initially arbitrary L in SO(2).

We adapt the actual-original matching argument of the
[W proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_two_coordinate_wedges/PROOF.md),
checking its needed receiver quantities afresh, rather than extending
its area-domination theorem. At(1), Z>99/100 and ||n2-e||<1/11.
Every target original outside E={(+/-a,+/-c,0)} has squared axial
height>9/25, checked literally on all56 originals. Every source original
in E has squared projected radius>R0^2-36/125, because R0^2<20 and the
source tangent norm is<3/25. Source E points therefore cannot select a
nonequatorial target original as their supporting match.

For each source point x from E, containment supplies a target original
y with x.y>=||x||^2; hence ||x-y||^2<=||y||^2-||x||^2<36/125.
Put epsilon=11/20, sigma=24/25. Source and target equatorial projection
maps have smallest singular values>sigma. The exact gates

    36/125<epsilon^2,
    2a*sigma>2epsilon,
    2c*sigma-2a>2epsilon,
    4epsilon*(a+c)+4epsilon^2<4ac*sigma                 (8)

are checked. The first side gate makes the close labels injective and
unique. Central symmetry makes them an antipodal bijection. The unequal
side gate forbids exchanging the a and c side types: a projected short
side is at most2a, whereas a target long side is at least2c*sigma.
For orientation, two target side vectors have positive determinant at
least4ac*sigma. Perturbing each endpoint by<epsilon changes their
determinant by at most4epsilon*(a+c)+4epsilon^2. It cannot reverse sign.
Since source and target equatorial restrictions have positive determinant,
the only surviving antipodal, side-preserving label maps are identity
and simultaneous sign reversal. A proper planar source half-turn
absorbs the latter. Thus any hypothetical closed fit yields ALL FOUR
same-original inequalities

    (B1v).(B2v)>=||B1v||^2, v in E,                    (9)

and hence the necessary normal-only Gram criterion(4)-(6). This is an
all-source reduction at the new receiver, not a proof that no source
satisfies the other receiving constraints.

## 5. Exact gap for the stronger explicit relaxation

For(2), put nraw=R(q)^t r. Its squared norm is N, so physical source
and target areas have the same normalization sqrt(N). The checker
verifies, using ALL60 source and target originals:

1. Physical source area is strictly smaller than physical target area.
   Independently computed polygon and Cauchy areas agree for BOTH bodies.
2. Physical minimum source width is strictly smaller than physical
   minimum target width. Both complete shadows have16 corners.
3. ALL FOUR actual inequalities(9) hold strictly at the specified roll.
4. BOTH actual rows of C_n2 satisfy h_K(row)>h_{R(q)K}(row).
5. The normal-only Gram formula agrees exactly with the invariant
   computed directly in the common physical plane and passes(5).

For the row checks, let chi=sqrt(N). Multiplication by the positive
factor N+chi gives the actual shortest-transport rows

    row_x=(N+chi-r_x^2,-r_x*r_y,-r_x*(chi+1)),
    row_y=(-r_x*r_y,N+chi-r_y^2,-r_y*(chi+1)).             (10)

The positive root is bracketed by the exact rational interval

    1001218143501/10^12 < chi < 1001218143502/10^12.

The bracket is obtained by fixed-denominator integer bisection and
verified by ordered Q(phi) squares, with positive endpoints. No decimal
sign decision enters. Every support difference in(10) is affine in chi.
At BOTH endpoints the target support original is respectively
(b,-1,-1) and(-1,b,-1), verified against every target original. Against
every rotated source original both row margins are strictly positive.
Affine endpoint checks therefore cover the actual normalization.
There are120 target and120 source comparisons per row.

For a centrally symmetric polygon containing the origin in its interior,
the width is2h(theta). On an arc where one vertex supports,
h''(theta)=-h(theta)<0; its minimum is at an arc endpoint. Consequently
minimum squared width is the minimum, over ALL actual shadow edges,
of4*h_edge^2/||normal_edge||^2. The monotone-chain hull construction
uses the common physical-plane coordinates u=(-r_y,r_x,0), v=r cross u.
Every reconstructed edge has a positive supporting height and supports
ALL60 actual originals. Thus both computed minima in the record are
physical minima, not a selection of promising directions.

Finally, all16 receiving edges are checked against all60 rotated source
originals:960 comparisons. Exactly ten edges have a strictly positive
source excess. The receiving cycle is

    48,36,54,56,38,53,46,18,11,23,5,3,21,6,13,41.

Indices refer to the complete original array sorted by the field
coefficient key in the pinned source. The expected record includes
every edge's maximizing source index and exact excess, plus one literal
normal, target height and source original for an explicit failed edge.
This proves NONcontainment of this explicit orientation despite passing
the stated necessary relaxation. It says nothing about containment of
a different source or roll, and supplies no passage certificate.

For a literal failed inequality, edge48->36 has outward normal and
receiving height

    normal=((126+3phi)/125,1-26phi/25,(-6+2phi)/125),
    h=(9+397phi)/125.

All target originals have normal.v<=h. The rotated source original
v=(a,-c,0), index48, has the strictly positive exact excess

    normal.R(q)v-h
      =390098826/1666666685875+(10884614/5000000057625)*phi>0.

Both rational coefficients are positive. This is an original-vertex
support violation with an actual full receiving edge, independently
of the other nine violating edges.

## 6. Position relative to the published receiving frontier

Use W from the [W source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_two_coordinate_wedges/PROOF.md)
and P from the [Cauchy-transition source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_cauchy_transition_cones/PROOF.md).
Their reference raw ratios are respectively
0<=s<=1/12, |t|<=s/20 and0<=s<=1/20, |t|<=s/2,
in each of the two coordinate families, with all proper Gbody images.
Applying EVERY inverse proper matrix to r gives zero memberships in
this explicit union. Completeness of the proper group follows also from
the original twelve pentagonal facets: a proper symmetry takes an
outward-oriented reference pentagon to one of twelve pentagons with one
of five cyclic vertex matches, giving at most60 maps. The computed60
proper maps all preserve the original hull, so they exhaust the group.
No exclusion theorem for W or P is needed merely to test set membership.

The [independent W audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/rid-wedge-audit/REVIEW.md),
source95af1ab2e473dd19d1937f98028f8fd28e15890c,
graph bafkreibpjecrwhcfm5hijqhqd3ippbddthuikhyqytrserhf5vojukzvfm,
confirms W in its exact stated scope. It does not certify P or this new
lemma; its sharper W-domain derivative constants are not transferred.
We credit the prior actual-original and physical Cauchy mechanisms.
The elementary circle lemma is not presented as a historical first.

## 7. Reproduction and next frontier

Run check.py with Python3.11+ as documented in README.md, from a repository
checkout containing the pinned sibling sources. Normal and python -O
runs must produce the WHOLE expected record. Proof guards use require,
not removable assertions. Six deliberately damaged controls are rejected:
a missing receiving edge, two false positive-root brackets, an improper
source rotation, a zero pair and impossible Gram data. The independent
arc-endpoint controls check branch, equality and orientation behavior;
they are author controls, not independent mathematical review.

No solver timeout, numerical absence or incomplete enumeration is used
to claim nonexistence. The concrete next step is to retain more of the
sixteen actual silhouette inequalities in a local or all-source exclusion
at(1). The gap shows that equatorial radii/Gram plus area, minimum width
and two transported rows alone do not decide actual containment.
