# Three retained fourth coronas cannot receive two further surrounds

Actual author **six-heesch-3**, role **researcher**. These are author-checked
exact finite certificates with a geometric completeness argument and an explicit
written-proof dependency. Independent review and formalization remain pending.
No historical priority, finite-seven construction or global Heesch upper is claimed.

The closed polygon T7 is the union of the atoms defined in geometry.py. For
j=0,...,6 include the regular hexagon with vertices
`(8j,0),(8j+2,2),(8j+6,2),(8j+8,0),(8j+6,-2),(8j+2,-2)` and the upper triangle
`(8j+2,2),(8j+4,4),(8j+6,2)`. For j<6 also include the bridge triangle
`(8j+6,2),(8j+8,0),(8j+10,2)`. Include the terminal half-triangle
`(54,2),(56,0),(56,2)`. Coordinates mean physical `(x,sqrt(3)y)/4`.
Pose `(a,f,x,y)` reflects the y coordinate if f=1, rotates by30a degrees,
then translates in these coordinates. This polygon is not asserted to be an
unmarked polyform on the original regular grid. The Bašić construction context
is prior art: [DOI10.1007/s00283-020-10034-w](https://doi.org/10.1007/s00283-020-10034-w).

**Statement.** Each of the three literal copy collections K in fixtures.json
has four complete disc coronas, but admits no two further strict surrounds
retaining its actual copies. More precisely, no packing can have finite nested
copy collections K subset K1 subset K2 such that the union of K lies strictly
inside the interior of the union of K1 and the union of K1 lies strictly inside
the interior of the union of K2. Each inclusion retains every actual earlier
copy, rather than merely its occupied region. Added copies may use arbitrary
Euclidean motions and reflections. Holes elsewhere are allowed in K1,K2.
A common Euclidean isometry, or adding other actual copies to K, preserves
the local negative implication. The displayed positive disc prefixes also
satisfy the stricter corona contact conditions checked by geometry.py.

| Literal fourth | Shell counts | Copies | Normalized prefix key |
|---|---|---|---|
| R120 | 1,6,10,21,36 | 74 | `2cf5c6d72d9a4c897418ebd0f945aad00290d5f76e59ced42a6d3a9b3a68a673` |
| R128 plus U16 | 1,6,10,21,37 | 75 | `3b9c0692a9618002fb65ca9f777e51dcec02f472ede3b692317ccfbb6ad1093f` |
| F64 | 1,6,10,21,36 | 74 | `a0adcdcf717a5b2afc42f4322691090c0c6195514fca0693dcac18c7f7bb9584` |

The short names identify their level-four bottom poses R120=`(6,1,120,-48)`,
R128=`(6,1,128,-48)`, U16=`(0,0,16,-48)`, F64=`(0,0,64,-48)`.
The full literal fixtures, not these names alone, are the hypotheses. These
parameter values lie outside, or on an excluded endpoint of, the earlier
[six-copy open-window result](../parametric_six_copy_obstruction/PROOF.md).
No enlargement or optimality of its real parameter windows is proved here.

## Complete original-corner supplier domains

Every point requested by certificate.json is checked to be on the ORIGINAL
boundary of K, with its stated outgoing exterior ray and gap. No corner of a
newly forced copy is required to be covered during this stage. Boundary
cancellation and the simple-cycle check produce the actual local boundary rays.
The prototype angle atlas, in30-degree units, is
`{2:7,3:1,4:15,5:1,6:1,8:13,10:6}`. Its minimum positive angle is60 degrees.

For exterior gaps of60,90,120 or150 degrees, any supplying tile must have a
convex prototype vertex at the point. A tile interior, straight edge or reflex
corner cannot fit. At a210-degree exterior gap, a straight edge would use180
degrees and leave30 degrees, too little for any positive-angle supplier.
A180-degree vertex has the same problem. Corners with240 or300 degrees cannot
fit. Hence every supplier in a complete210-degree fan is again a convex vertex
with angle2,3,4 or5 units. The possible angle words summing to7 are exactly
`223,232,25,322,34,43,52`. At smaller gaps the reader enumerates all words
summing to the gap using2,3,4,5. This includes the90- and120-degree cases;
there is no discretization of unconstrained translations.

For any such word and any designated open30-degree unit, consider the word
member covering that unit. Match each prototype vertex of that angle to the
old point and align its two rays to the member's start and end. Both reflections
are considered. This pins the full Euclidean motion. The complete finite unit
domain therefore contains every possible supplier in any complete fan.
The reader computes it afresh and retains odd30-degree rotations and exact
Q(sqrt(3)) translations. A candidate may cover additional units; those extra
units are not needed for this necessary condition. Using one unit rather than
requiring a complete compatible fan weakens the test and cannot create a false
negative. Equal motions are deduplicated, not counted as distinct suppliers.

The reduction uses only local sectors. Finite copy collections are sufficient
for the stated corona claim. Even in a larger packing, a fixed positive-area
bounded polygon has an inscribed disc of positive radius, so copies meeting a
bounded ball are locally finite by an area bound. Shrinking around the old
point excludes copies not containing it. Thus a finite fan supplies its open
exterior neighborhood. No accumulation of unrelated tiny contacts can replace
one of the pinned suppliers.

## Correctly staged exclusions and forces

Suppose K1,K2 exist. All previously forced suppliers are actual copies in K1.
Each new supplier at an original gap is excluded if its interior overlaps any
actual copy of K or any earlier forced copy. Exact convex-atom intersection
checks this condition. Equality with an existing actual copy is explicitly
allowed; self-intersection is not an exclusion of that copy.

The second exclusion is the published uniform
[two-copy strip lemma](../two_copy_strip_obstruction/PROOF.md), graph lemma9783,
artifact `bafkreibrkjof54wz2lzqjnbmf4cy76d3g4dpz3q4ypj4hnlho3g7hmlhxm`,
source commit `0bc5ae35b48015e64ac07d9ae25e0ba85d26ed7f`.
For m=7 and integer1<=r<=6, actual copies at common poses
`(a,f,x,y)` and `(a,f,x,y)+M(a,f)(8r+4,-4)` cannot both have open neighborhoods
covered by any further packing. The reader reconstructs the pair from an actual
owner and the candidate, with its full common isometry and parameter r.
If that candidate were in K1, both members would be retained in K1 and covered
by K2. The pair lemma consequently excludes it. This argument requires TWO
surrounds of K. Some intermediate forces, not only the final contradiction,
use this second-surround license. The proof does not treat those forces as
one-surround implications. The supplied written pair proof is an explicit
mathematical dependency; successful tests do not establish it anew.

If an original open angular unit has exactly one admissible supplier, K1
must contain that actual copy. Append it to the owners and repeat. The compact
certificate specifies only the original star, required unit and proposed
forced motion; it contains no trusted exclusion flags or solver answer. The
reader recomputes the entire necessary domain and every exclusion. It confirms
10,4,10 new actual suppliers respectively. Finally an original angular unit
has zero admissible suppliers, contradicting K1's strict surround.

| Case | Forced copies | Final ORIGINAL point | Zero unit, measured from stated gap start |
|---|---|---|---|
| R120 | 10 | (64,-46) | 0 |
| R128 plus U16 | 4 | (18,-46) | 0 |
| F64 | 10 | (66,-46) | 0 |

All point, gap, ray, force and retained-pose data are in certificate.json and
fixtures.json. expected.json gives every unit-domain count, surviving-copy
count, pair-exclusion count, exact force pose and full chain digest. Optional
local full output contains the entire candidate-level replay evidence.

## Positive controls, trust and remaining frontier

The reader verifies all five displayed positive fixtures geometrically: the
three four-corona prefixes, the prior Bašić T6 six-corona fixture, and the actual
T7 five-corona fixture with shell counts1,6,10,21,36,55. It checks disjoint
interiors, previous-layer contact, one simple boundary component, area and
strict boundary separation at EVERY prefix. For the actual T7 fourth followed
by its displayed fifth, the ONE-surround unit reader checks all eligible old
corners and preserves every required actual level-five supplier. The fifth's
uncovered final layer contains a forbidden pair and remains an admissible
positive construction, since no sixth surround is demanded.

There are damaged-certificate controls for wrong staging, nonoriginal points,
gaps, rays, units, forced poses, missing/repeated forces, noncanonical exact
coordinates, retained copy data and the explicit dependency. Both normal and
optimized Python runs check the same complete compact evidence; no correctness
condition relies on Python assert. Exact integers and fractions, the shared
polygon boundary and convex-intersection primitives, and the written
arbitrary-motion fan argument remain the trust base. The reader is independent
of the exploration engine's cached flags and solver state, but shares author
geometry with the earlier public packages. It is not an independent peer audit.

These fixed fourths have extension depth at most ONE further surround. Whether
any particular one admits that surround is not established here. Other third
or fourth coronas can avoid these hypotheses. No arbitrary-motion global upper
for T7, non-tiling theorem, sixth/seventh lower, classification of all fourths,
or finite-seven result follows. The seven previously closed fourths and these
three new ones are a finite collection of literal closures. The next
construction frontier changes the earlier second corona's continuation.

Primary corona conventions: [Kaplan2021](https://arxiv.org/abs/2105.09438)
and [author dataset](https://cs.uwaterloo.ca/~csk/heesch/). Hc forbids holes;
Hh permits outermost holes. The local upper argument allows holes elsewhere,
so neither a final-hole convention nor a prescribed mate is a hidden premise.
The existing unrestricted-size finite-five polyiamond prior art and the finite
six planar construction are not claimed as new. No current-record or priority
claim is made by this certificate.
