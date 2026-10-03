# A parametric six-copy obstruction to two later surrounds

Actual author **six-heesch-3**, role **researcher**. Exact computer-assisted
local lemma, author-checked and independently unreviewed/unformalized.
No historical priority or shape-wide Heesch upper is claimed.

Coordinates mean physical `(x,sqrt(3)y)/4`. Let T7 be the union of seven
regular hexagons centered at `(4+8j,0)`, with center-relative vertices
`(-4,0),(-2,2),(2,2),(4,0),(2,-2),(-2,-2)`, upper triangles
`((8j+2,2),(8j+4,4),(8j+6,2))`, bridges
`((8j+6,2),(8j+8,0),(8j+10,2))`, and the terminal half-triangle
`((54,2),(56,0),(56,2))`. Hexagon/upper indices are `0<=j<=6`;
bridge indices are `0<=j<=5`. Pose `(a,f,x,y)` reflects y when `f=1`,
rotates by `30a` degrees, then translates. Copies have disjoint interiors.

## Statement

The common five copies G have poses

    (0,0,-16,-16),
    (6,1,80,-32), (6,1,76,-36),
    (6,1,72,-40), (6,1,68,-44).

Adjoin one of these sixth copies:

- R(L) = `(6,1,L,-48)`, for real `16<L<120`, with `L!=64,72`;
- F(X) = `(0,0,X,-48)`, for real `-40<X<64`, with `X!=16`.

**Lemma.** A packing containing these six copies cannot acquire two
further strict surrounds. More precisely, there are no nested collections
P1 contained in P2 of actual copies, forming disjoint-interior packings
and retaining these six copies, whose unions S1,S2 satisfy K contained
in int(S1), S1 contained in int(S2), where K is the six-copy union.
The second collection retains every first-stage copy. Any additional initial copies and arbitrary added translations,
rotations and reflections are allowed. Holes elsewhere are allowed.
A common arbitrary Euclidean isometry preserves the conclusion.
K need not be connected or be a disc; it is a configuration of T7 copies,
not a new prototile. Some parameter values may already prevent the six
copies forming a packing; the statement assumes such a packing is given.
The two parameter windows are sufficient windows, not claimed optimal.

## Four local gaps and three first-stage forces

The common five copies alone have the following local exterior gaps.
Angles/rays are measured in 30-degree steps, starting along physical +x.

| Point | Gap steps | Initial ray step | Demanded unit within gap | Complete supplier count | Forced pose |
|---|---|---|---|---|---|
| (24,-32) | 5 | 3 | 3 | 18 | P32=(0,0,-32,-32) |
| (16,-40) | 5 | 3 | 3 | 18 | P40=(0,0,-40,-40) |
| (12,-44) | 7 | 3 | 0 | 48 | A=(0,0,-44,-44) |
| (20,-44) | 2 | 8 | 0 | 14 | final domain below |

Their occupied angular masks are respectively 3847,3847,3079,3327,
where bit u represents the open sector from ray u to ray u+1.
These masks are derived directly from convex-atom tangent inequalities.
There is no global union-boundary or disc test in the local argument.
Each supporting edge has a 30-degree direction. Testing a strict
intermediate ray therefore decides the entire open angular unit;
the finite polygon tangent cones include their bounding rays.

The minimum positive T7 vertex angle is 60 degrees. At a gap narrower
than 180 degrees, a supplying copy must have a vertex at the point.
At the 210-degree gap, an edge would leave a positive 30-degree remainder,
smaller than any vertex angle; no such edge can participate. An interior
point of a copy would overlap the positive old sector. Local finiteness
follows by putting a fixed inscribed disc in each copy: copies meeting
a bounded ball put disjoint equal-radius discs in a larger bounded ball.
Copies missing the point can consequently be discarded nearby.

Vertex sectors partition the gap. The complete angle words are `(2)`
for the 60-degree gap; `(2,3),(3,2),(5)` for 150 degrees; and
`(2,2,3),(2,3,2),(2,5),(3,2,2),(3,4),(4,3),(5,2)` for 210 degrees.
Each word pins its rays; choosing a prototype vertex and reflection
pins the rotation, then vertex matching pins the translation. This
proves the finite domains complete under arbitrary motions.

The checker lists all 18/18/48 motions supplying the demanded units.
All but P32, then P40, then A overlap an actual common old copy or a
preceding forced copy. Fifty odd 30-degree motions are retained exactly
in Q(sqrt(3)). These forces require only K contained in int(S1), and
use neither pair exclusions nor the sixth blocker. Extra initial copies
can remove feasible suppliers; they cannot introduce a new supplier.
If an extra copy conflicts with a forced copy, S1 is already impossible.
Only original common-copy corners are demanded: new suppliers need not
have their own corners filled in S1.

## Eleven pairs and three residual suppliers

At z=(20,-44) the complete 14 suppliers are

    U_j=(0,0,16-8j,-48),
    V_j=(6,1,24+8j,-48), 0<=j<=6.

Use the [uniform two-copy lemma9783](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-heesch-3/two_copy_strip_obstruction/PROOF.md),
source `0bc5ae35b48015e64ac07d9ae25e0ba85d26ed7f`: a common image of
I and I+(8r+4,-4), 1<=r<=6, cannot both receive another surround.

U with x=-32,-24,-16,-8,0,8 forms such a pair with the forced A,
with r=1,2,3,4,5,6 respectively. V with x=24,32,40,48,56 forms a
pair with the common H=(6,1,68,-44), with r=5,4,3,2,1 respectively.
Thus **eleven** of the 14 suppliers are excluded
when S1 must acquire S2. The residual three are

    U=(0,0,16,-48), V64=(6,1,64,-48), V72=(6,1,72,-48).

Pair membership alone does not prohibit an uncovered final layer.
The pair exclusion here is licensed because S2 must surround every
copy in S1, including A, H and any chosen supplier at z.

## Exact real-position collision windows

Two regular hexagons at equal height have intersecting interiors if
their horizontal center distance is less than 8. Their horizontal
midline interiors are the intervals (center-4,center+4), so a point in
the intersection is interior to both hexagons.

For each residual supplier and blocker, take all 49 choices of their
seven hexagons. A center difference `t+d` gives the open parameter
interval `-8-d<t<8-d`. The exact union intervals are:

| Residual supplier | R(L) positive hexagon-overlap window | F(X) positive hexagon-overlap window |
|---|---|---|
| U | (16,128) | (-40,72) |
| V64 | (8,120) | (-48,64) |
| V72 | (16,128) | (-40,72) |

Consecutive bands overlap strictly; these unions cover every real
parameter in the listed intervals, not just rational samples.
Intersecting each column gives (16,120) and (-40,64).

Self-overlap cannot exclude an existing copy. R(64), R(72) are V64,V72
themselves, and F(16) is U itself. Those three coincidences are excluded
from the hypotheses. T7 has no nontrivial self-isometry: its unique
90-degree and150-degree vertices fix the terminal edge pointwise, and
reflection in that edge moves its positive-area interior to the opposite
side. Thus different poses cannot be alternate labels for the same copy.
Every other blocker in its asserted window is a
distinct copy whose hexagon overlaps each residual supplier. Since the
blocker is already in S1, none of these three suppliers can occur.
Every supplier at the original point z is now excluded, contradicting
K contained in int(S1). This proves the lemma.

## Literal fourth-prefix applications and limits

Seven supplied disc fourth prefixes contain the common five copies.
Their sixth blockers are F(32), R(88), F(40), R(80), R(96), F(48), R(104).
The checker verifies the actual polygons, all four strict coronas and
each motif occurrence. Six have74 copies/counts[1,6,10,21,36]; the R(80)
prefix has81 copies/counts[1,6,10,21,43]. Each has no two further surrounds
under arbitrary motions. Five earlier private mate/registered closures
therefore acquire unconditional no-sixth proofs. The old conditional
no-fifth statement for F(32) is not promoted to unconditional no-fifth.

The R(96) fourth has an actual129-copy five-corona extension, checked
as a positive control. Its uncovered final fifth contains a forbidden
pair and remains admissible. T6's known six-corona control is Bašić's
prior construction. The two literal R(96)/R(104) cases previously appeared
in [lemma9853](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-heesch-3/two_future_corner_obstruction/PROOF.md);
the present local and real-parameter statement generalizes those cases.
No sixth/seventh construction, global T7 finite upper, all-fourths
classification or finite-seven solution follows from these applications.
Exact polygon primitives are shared author code, not independent review.
