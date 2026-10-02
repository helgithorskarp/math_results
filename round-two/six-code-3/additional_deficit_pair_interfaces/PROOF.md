# An isolated deficient hub paired with a unit saturated star forces upper67

Actual author: **six-code-3, researcher**, 2026-10-02.
This is an exact computer-assisted local result, conditional on the
reviewed generic twenty-star classification8933 and universal8323.
The ordinary normalization and completeness arguments are unformalized.
Independent review of this new result and historical priority are pending.

Let F be distinct five-subsets of eighteen points, with distinct members
intersecting in at most two points. Write r_p for point replication and
lambda_pq for pair replication. A triple is covered if a member contains it.
The x-star leave has an edge pq exactly when xpq is uncovered.

**Combined theorem.** Let x,y,u,v be four distinct points. Assume
r_x=r_y=20, lambda_xy=4, lambda_xv=5, and xyv is uncovered.
Assume lambda_xu<5 and that u is isolated in the x-star leave induced
on H_x={p other than x:lambda_xp<5}. Finally assume every y-row pair
has multiplicity4 or5, with lambda_yu=lambda_yv=5. Then **|F|<=67**.
There is no other first-row multiplicity restriction, distinguished
extra point, covered-triangle condition, global degree profile or code
automorphism assumption. The old reviewed scopes retain their sharper
bounds; no sharpness is asserted for this combined theorem.

**New finite component.** Let x,y,u,v,w be five distinct points. Assume:

1. r_x=r_y=20, lambda_xy=4, lambda_xv=5, and xyv is uncovered.
2. lambda_xu=4, lambda_xw=3, and lambda_xp is4 or5 for every
   p outside {x,u,w}. The point u is isolated in the x-star leave
   induced on H_x={p other than x:lambda_xp<5}.
3. lambda_yu=lambda_yv=5, and lambda_yp is4 or5 for every p other
   than y. In particular, lambda_yw may be4 **or**5.

Then **|F|<=67**. No covered-triangle condition, other whole-code point
degree, hub multiplicity, global replication profile or automorphism
is assumed. Isolation permits leave neighbors outside H_x. No optimality
or sharpness is claimed. Consequently any packing of at least68 words
fails at least one of these hypotheses for every ordered choice of marks.

## Structural reduction to the two covered first-row domains

This is the ordinary combinatorial bridge for the combined theorem.
Shortening at x gives120 covered pairs amongC(17,2)=136 possible pairs,
so its leave has16 edges. Every replication-five link point has exactly
one leave neighbor, lying in H_x by universal8323. If h=|H_x|, the
17-h low points therefore account for exactly17-h leave edges; there
are **h-1 edges inside H_x**. The u and y marks are distinct deficient
points, so h>=2. Isolation of u bounds these internal edges by
C(h-1,2). The inequality h-1<=C(h-1,2), with h>=2, forces h>=4.
Positive integral deficits sum5; their only possible partitions are
**2111 or11111**. In particular lambda_xu must be3 or4, as a conclusion
of these hypotheses, rather than an extra selector requirement.

If all deficits are1, or if the unique deficit-two point is u, the
original hypotheses1--3 of9098 hold. The independently confirmed
[review9141](../../six-reviewer-5/unfiltered-two-star-audit/REVIEW.md)
gives bound66 in that domain. Otherwise u has deficit1 and a different
point w has deficit2. Since y has deficit1 and v has deficit0, w is
distinct from x,y,u,v. This is precisely the new finite component below,
with bound67. These cases exhaust the combined theorem.
Its contrapositive supplies a selector obstruction for every packing of
at least68 words, without requiring a named extra point or specified
first-row pattern. It still does not force the selector from a global
size71 profile.

## Why this is a different finite domain

The earlier [9098 local result](../good_cohort_z_residuals/PROOF.md),
source889e97cfb0062c4af143608b9922e4acbce28784, requires every first-row
pair other than its distinguished u pair to have multiplicity4 or5.
The new lambda_xw=3 therefore lies outside that theorem.
The tail-matching/point-assignment framework is adapted, with credit,
from [9045](../good_cohort_z_interfaces/PROOF.md),
sourcee2f9cc128036b909d4d45a88ba2c5b72f1db8e2d. Its old numerical
result is not a premise here. The color generator is adapted from9098;
all34 color arrays in this directory are newly generated.

The new [independent review9141](../../six-reviewer-5/unfiltered-two-star-audit/REVIEW.md),
sourcebde7ea936c220c567874957906688597da8387d7, confirms9098 and gives
sharp endpoints66,63 and58 for its original scopes. It closes the old
548-to34 transport gap. It explicitly does not cover this additional
lambda_xw=3 domain or prove a global three-hub selector. Its reviewed
old-domain bound66 is imported only in the combined ordinary theorem;
no completion maximum or color array is imported into the new34-root
finite computation. The cold replay here establishes that new component;
it does not repeat the reviewer's earlier-domain computation.

## Generic classification, marks and checked subgroups

Shortening either complete20-star gives twenty quadruples on seventeen
points with pairwise intersection at most one. A link point's replication
is the corresponding center-pair multiplicity, at most5 by disjoint
three-point tails. Its deficits d_p=5-lambda_xp sum85-80=5.
At x the positive deficit pattern is therefore2111: u has deficit1,
w has deficit2, and the other two positive deficits are1.
At y every positive deficit is1.

Generic23-fixture coverage is imported from
[review8933](../../six-reviewer-5/twenty-star-classification-audit/REVIEW.md),
source0509c3808f44b45fd3c333a10cf36bd329003450, conditional on the
reviewed [universal8323](../../../constant_weight_upper71_review1/REVIEW.md),
source02c1569568854e575f8b176ea07d552737a7da84.
The byte-identical literal [fixtures.json](fixtures.json) originates in
six-code-2's [8720](../../six-code-2/free_involution_upper68/PROOF.md),
source69f2312bb468eb59b8ab3d8978fe19b3d86cf58a, SHA256
c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7.
Only generic coverage and literal input data are imported; no symmetry
specific bound is used. We check every fixture's actual quadruples,
replications, covered pairs, leave neighbors and supplied maps.

At x, the replication-five v has a unique leave friend, which is y.
The u-v pair is covered because u differs from y. The u-y pair is
covered by u's isolation among deficient points. At y, both u and v
are replication-five link points, so their pair is covered by the
no-low-low-leave premise; u-x is covered by the same actual xyu word.
The second u's unique leave friend b is recorded with no constraint
on its image. The extra w is determined by the first row, and its
second-row multiplicity is allowed to be4 or5 throughout.

[domain.py](domain.py) derives the first ordered marks(u,v,y) from all23
literal fixtures. Only fixture8 is eligible, with u13,w14 and four marks:
(13,2,11),(13,5,12),(13,6,11),(13,7,12). Its supplied subgroup of order2
gives two actual mark orbits, represented by(13,2,11) and(13,5,12).
There are878 raw second marks(u,v,x,b), in eight unit-row fixtures,
with180 checked subgroup orbits. The domain therefore has3512 raw
products or360 normalized products.

Every supplied subgroup is checked to contain the identity, consist of
actual point bijections preserving every quadruple, and be closed.
Literal images partition each marking domain. No subgroup is assumed
maximal. First-star quotienting is an ambient point relabeling and
second-star quotienting is a reparametrization of its relative map.
They require no whole-code symmetry. The independent [verify.py](verify.py)
derives all marks and orbit covers from literal sets and replications,
without importing the producer or domain helper.

## Complete relative maps and compatible unions

Normalize x=17. The four xy words have disjoint three-point tails.
One tail contains u, whereas v lies outside all tails. A relative map
sends the second x,u,v to17 and the first u,v. Its u-tail has two
internal maps fixing u; the other three tails have3! matches and6^3
internal maps. This gives2592 distinct partial maps per product.
Fourteen source points are assigned; all six bijections of the three
remaining points are then accounted for. Thus each product represents
15552 complete relative maps. The normalized whole carrier has933120
partial maps representing5598720 full maps. The raw marking carrier
represents54618624 maps; no raw-positive count is inferred by division.

[produce.py](produce.py) matches complete block tails and rejects a
partial map only when an actual projected private second quadruple
already has three common points with a private first quadruple. Such a
collision persists in every extension. Intersections involving the four
common words are controlled by the common-tail matching and each
quadruple packing's pair uniqueness. Every remaining partial is expanded
through all six residual bijections and every positive union is checked
against all its actual word pairs.

The independent checker assigns source tail points individually, using
injectivity and source/target tail association; it does not permute
block tails. It reconstructs each whole2592-map universe, checks actual
private second words against **all20 first words**, expands every
unexcluded residual bijection, and checks all36-word unions directly.
Complete sorted partial universes and actual full positive arrays agree
with the producer in every product. The complete run expands11076 full
maps and visits4622688 DFS states, at most15454 in one product.
Every product accounts for all15552 extensions. Missing products,
timeouts, guards or incomplete processes prove no absence.

Exactly34 compatible maps remain in27 normalized products, with34
distinct labelled36-word unions, retained in [BRIDGE.json](BRIDGE.json).
These are marked normalized representatives, not full isomorphism
classes. No triangle filter is applied. The marking-domain SHA256 is
54bf1c6bbd498d87d424d06ae6c02bfaf82d0a6c4a4d3d73d7d257fb8bde3564;
the whole point-checker record hash is
aadc3b50d2884ccfd50074622ebfe9cc671f46f42e63257b3e350b023582b526.

## Actual residual domains and positive color certificates

Each union has20+20-4=36 words and already includes every word through
x or y. A further word must avoid both centers. For each representative
allC(16,5)=4368 five-subsets are tested against its actual36-word core.
The total residual population over34 roots is4179; the total number
of compatible candidate pairs is214165. An edge joins two candidates
precisely when their intersection has size at most2. Any completion
is a clique in this compatibility graph, and a proper k-coloring
therefore bounds its additional words by k.

[generate_colors.py](generate_colors.py) produces deterministic greedy
positive colorings, with at most64 fixed seeded priorities per root.
Failure to find a better coloring is never an exclusion or optimality
claim. [check_colors.py](check_colors.py) imports no producer, old census
or solver. It reconstructs all actual source/point-map images and all
local hypotheses from literal sets, builds every further-word domain
using owned triples, and checks every compatible pair's colors.
No cached graph or numerical search status is trusted.

The proper colors use25--31 classes. Full bound census:

| Certified upper bound | Marked representatives |
| --- | ---: |
| 61 | 1 |
| 62 | 5 |
| 63 | 7 |
| 64 | 11 |
| 65 | 3 |
| 66 | 2 |
| 67 | 5 |

Nineteen representatives have lambda_yw=4 and fifteen have lambda_yw=5;
both subscopes are fully retained, with respective maximum bound67.
The whole candidate-domain hash is
bc7c58f39b7f207b1a3646b18b41e86118e2c22ffb7bfc76114ed245820653fd;
all literal numerical records hash to
4a8108fdcf09c941c5d029123c24d71a0920cb4f48614f1274e4aac921d0c247.

## Validation, applicability and remaining trust boundary

[reproduce.py](reproduce.py) performs complete cold producer/point-DFS
replays against pre-existing frozen [expected.json](expected.json),
compares every actual positive array, regenerates every color byte,
and checks every literal mathematical record. Normal and optimized
Python replays agree. [controls.py](controls.py) rejects39 semantic
damages/population gaps; three actual relabelings transport69 literal
stars and102 whole marked interfaces, residual domains and color functions.
Commands, measured costs and executable hashes are in [README.md](README.md)
and [VALIDATION.json](VALIDATION.json). All computations are serial with
one thread, unchanged1CPU2GiB, and existing resource guards. Generated
corpora, complete intermediate records and logs remain private scratch.

The finite component's external premise is generic8933 conditional8323.
The combined theorem additionally imports the old-domain bound66 from9141.
CPython, same-author separate algorithms, and the ordinary shortening,
checked-subgroup quotient and finite coverage/color bridges remain
explicit trust boundaries. There is no formal proof-assistant theorem
or independent review verdict on this new result. The old review9141
is context, not a verdict on these new34 interfaces.

The current application candidate is the **P=6 branch** of the size71
profile(17,19,19,20^15), with w degree17 and u,v degree19 in either order,
P=lambda_uv+lambda_uw+lambda_vw. This profile and P value are **not**
premises of the local theorem. Proving that this branch forces a choice
of saturated x,y and those marked conditions remains separate global
selection/charging work. The private candidate P>=6 proof is not used.
The combined theorem permits a weaker proposed selector: first-row
lambda_xu<5 and isolation suffice, with no demand that its unique
deficit-two point be the globally degree17 hub, or that such a point
exist. The remaining common-pair/low-v and unit y-row conditions still
need an ambient forcing proof; no such existence is asserted here.
No entire three-hub profile or unrestricted size71 packing is excluded.
Campaign bounds69--71 remain unchanged.

The primary baseline remains classical:
[Brouwer1975](https://ir.cwi.nl/pub/6883/6883D.pdf),
[Aw--Chee--Ling2003, Theorem1/AppendixA](https://ymchee66.github.io/home/PDF/6cwc.pdf),
and the [maintained Brouwer table](https://aeb.win.tue.nl/codes/Andw.html).
The live table still records69--72. The known69-word certificate was
freshly reproduced against all690 triples and2346 pairs in this pass;
that is validation, not a new construction or a priority claim.
