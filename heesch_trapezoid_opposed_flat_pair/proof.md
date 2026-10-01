# An opposed-flat pair has no strict surround

Actual author **six-heesch-3**, role **researcher**, 2026-10-01.
Written all-real author proof with exact affine checks. Unformalized and
independently unreviewed. This is a local obstruction; the connected
Euclidean finite-Heesch-at-least-seven target remains unresolved.

## Physical tile and statement

Axial coordinates (q,r) mean (q+r/2,sqrt(3)r/2) in the Euclidean plane.
For an integer n>=8 the skeleton is the counterclockwise quadrilateral

    (0,-1), (n,-1), (n-1,1), (0,1).

Its bottom is subdivided into n unit chords, top into n-1 and left into
two. The remaining side is a straight segment of length sqrt(3). On a
counterclockwise unit chord v to v+e use the physical quartic

    v+u*e+(s/100)*u^2*(1-u)^2*(e_y,-e_x),  0<=u<=1,

where the vectors and perpendicular are Cartesian. The intrinsic state s
is -1 on the bottom and +1 on the top and left; the flat is unchanged.
The resulting unmarked connected Jordan disc is T_n. These states and
labels describe geometry and impose no external matching rules.
The maximum displacement is delta=1/1600. Scaling the amplitude from
zero preserves the simple prototype, as proved in the credited
[uniform-strip proof](../heesch_trapezoid_uniform_strip_obstruction/proof.md).

Write R(q,r)=(-r,q+r), J(q,r)=(q+r,-r). Pose(h,k,a,b) means R^k J^h
followed by translation(a,b). Fix an integer 1<=l<=n-2 and put

    O=(0,0,0,0),  B_l=(1,3,n+l,-2).

**Claim.** No finite packing containing O and B_l can make both entire
closed copies strictly interior to its union. Added copies may use
arbitrary real rotations, reflections and translations. No disc,
connectedness, hole or added-copy-contact requirement is imposed.
A common Euclidean isometry transports the statement.

Both O and B_l require interiority. The argument neither proves
surroundability at l=0 or l=n-1 nor asserts those endpoint cases impossible.

## Completeness of the two forced flat mates

The [whole-old-flat sublemma](../heesch_trapezoid_protected_contact_reduction/proof.md)
applies to B_l alone being strictly interior. Its all-offset exclusion of
split flat contacts uses the uniform O,U,L obstruction. It requires no
later surround of the newly supplied mate. Thus a whole opposite flat
mate must occur.

B_l's counterclockwise flat runs from (l,-1) to (l+1,-3). A full endpoint
match determines a Euclidean rotation or reflection and translation;
the prototype has exactly one flat. The complete twelve-orientation
endpoint census, with coordinates affine in n,l, gives exactly

    P_l=(0,0,l-n+1,-2),  F_l=(1,0,l-n+1,-2).

These are all possible full mates for arbitrary real motions, because a
segment and its reversed endpoint pair fix the isometry up to its two
hands. The finite census verifies that geometric determination rather
than replacing a continuous-phase proof by sampled placements.

## The proper mate creates an impossible 120-degree gap

At z=(0,-1), O has its 60-degree corner: in twelve counterclockwise
30-degree slots it occupies 0,1. P_l's positive top runs along r=-1 from
q=l-n+1 to q=l. The strict inequalities

    l-n+1<=-1,  l>=1

make z a regular labelled junction on that top. P_l occupies slots
6,...,11. Their missing sector is the contiguous 120-degree gap 2,...,5,
bounded by O's positive unit from (0,0) to z and P_l's positive unit
from z to (-1,-1).

Since O is strictly interior, a small ball about z must be covered.
In a finite packing, copies not containing z have positive distance
from it; they cannot fill the missing sector sufficiently near z.
Incident copies have positive tangent angles 60,90,120 or180 degrees.
The [finite analytic-star argument](../heesch_trapezoid_protected_contact_reduction/proof.md)
forces adjacent physical germs to coincide: distinct analytic branches
would leave a zero-angle gap or overlap which no positive-angle copy
can fill. The [atomic-unit lemma](../heesch_weighted_matching_obstruction/quartic_realization.md)
then requires opposite intrinsic states, also for reflected copies.

The complete necessary angle/state words in the
[single-surround proof](../heesch_trapezoid_single_surround_alignment/proof.md)
give no completion of this gap. One 120-degree corner has states(+,+),
where both required exterior states would be negative. Two 60-degree
corners, each with one positive and one negative side, would have their
negative sides on the two exterior positive germs and leave an internal
positive/positive seam. A 90-degree corner leaves 30 degrees, smaller
than any available angle. A smooth 180-degree point cannot fit.
Therefore P_l cannot occur in this strictly surrounding packing.
P_l itself needs no interiority.

## The reflected mate overlaps a required mate of O

F_l's negative bottom runs along r=-1, counterclockwise from q=l to
q=l-n. It includes the whole unit from (1,-1) to (0,-1), since
l>=1 and n-l>=2. O has the same intrinsic negative state on the
reverse unit (0,-1) to (1,-1). These two inward profiles alone leave a
thin gap. Their rejection here uses O's interiority explicitly.

Every open charged arc of strictly interior O has a whole opposite
unit mate Q. This follows from the atomic-unit lemma and finite algebraic
boundary cover: finitely many noncoincident arcs have only finitely many
intersections and cannot cover that open arc. Q's coincident unit has
positive state, the same endpoints and skeleton interior below r=-1.
F_l's skeleton is on that same side. Q's further interiority is not assumed.

Here is a uniform quantitative physical-overlap proof, independent of
which positive unit of Q supplied the match. The midpoint of any charged
prototype unit lies at Euclidean distance at least sqrt(3)/4 from every
other skeleton side carrier. For a bottom unit with midpoint(k+1/2,-1),
0<=k<=n-1, the distances to the left, top and flat carriers are at least
sqrt(3)/4, sqrt(3) and1/2. For a top unit with midpoint(k+1/2,1),
0<=k<=n-2, its distances to the left, bottom and flat carriers have those
same three respective lower bounds. For either left unit with
midpoint(0,+/-1/2), the bottom and top distances are at least sqrt(3)/4,
and the flat distance is at least n-3/4. These bounds hold throughout
the indicated whole integer domains; the exact reader derives their
primitive determinant inequalities symbolically.

Let m=(1/2,-1) be the common unit midpoint. Move vertically downward
by h=sqrt(3)/32, giving the exact axial point

    x=(17/32,-17/16).

In both F_l and Q, x is strictly inside the skeleton. Its distance from
the common unit carrier is h, and its distance from every other carrier
is at least sqrt(3)/4-h=7sqrt(3)/32. Hence its distance from the entire
skeleton boundary is at least h>delta. Every physical boundary stays
within delta of its own skeleton boundary during amplitude scaling.
No boundary crosses x, so winding number one is preserved and x belongs
to both physical interiors. This contradicts packing disjointness.
The squared displacement h^2=3/1024 exceeds delta^2 exactly.

This proves F_l impossible without treating two unprotected inward
chords as an artificial matching conflict. O's required opposite unit
mate, and the displayed common interior point, are essential.

Both complete whole-flat options are now excluded, proving the claim.

## Exact evidence, nonvacuity and corona use

[check.py](check.py) uses Python3.11+ standard library and rational affine
coefficients. It checks the complete flat endpoint census, tangent slots,
empty state words, reflected whole unit and all midpoint carrier bounds
on their unbounded parameter domains. [certificate.json](certificate.json)
specifies the semantic claim, [expected.json](expected.json) its output;
eight malformed controls must fail. Python -O is explicitly rejected.
No previous executable, constructor, solver, inventory, native trace or
private full corona witness is imported. Generic affine/state/network
primitives are adapted with attribution from the
[preceding tip-propagation reader](../heesch_trapezoid_tip_propagation/check.py).
The all-real finite-cover, star, whole-flat and winding arguments remain
written trust boundaries, rather than formalized theorems.

The n=12,l=5 fixture consists of O and(1,3,17,-2). It is checked directly
as one physical disc subpacking, with seven whole complementary contacts,
38 exposed ports, nonincident distance squared3/4 and incident ray
separation30 degrees. The credited
[physical network deformation](../heesch_trapezoid_four_coronas/proof.md)
preserves this embedded skeleton network. Under frame(0,1,-1,-22), the
literal pair is(0,1,-1,-22),(1,4,1,-7). This is a nonvacuous local
packing, not a corona existence certificate.

Under strict prefix conventions, any corona prefix containing a displayed
pair cannot have one further strict surround. A pair involving proposed
new copies is therefore a sound necessary exclusion when that proposed
prefix needs a later corona. Occurrences in a finite candidate pool do
not prove its completeness, justify unrelated native clauses or classify
all first coronas. The theorem supplies no new corona lower count,
global Heesch upper bound, exact height or finite-seven construction.

The literature context retains [Kaplan2021/2022](https://arxiv.org/abs/2105.09438),
the [primary Hc/Hh data and conventions](https://cs.uwaterloo.ca/~csk/heesch/),
and the [2025 connected finite-six discussion](https://arxiv.org/html/2509.12216v1).
This bounded context check is not an exhaustive historical-priority claim.
