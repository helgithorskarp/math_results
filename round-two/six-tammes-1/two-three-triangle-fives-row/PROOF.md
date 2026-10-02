# Excluding two three-triangle degree fives in the nine-Q class

Actual author **six-tammes-1**, role **researcher**, 2026-10-02.
Exact computer-assisted author proof; independent mathematical review and
proof-assistant formalization are pending.

## 1. Statement and scope

Let fifteen distinct unit points have all pair products at most c, with
**1/2<c<3/5**. Their **complete** contact graph joins exactly pairs with
product c. Assume its minor geodesic embedding is connected and cellular
on the sphere, with degrees 3,4,5 and simple strictly convex hemispherical
triangular and quadrilateral faces, exactly nine Q faces. The following
profile is impossible:

* Two degree threes U,V, each with no T corner.
* Two degree fives F,D, each with three T and two Q corners.
* Four one-T degree fours A,B,C,E and seven two-T degree fours.

There is no zero-T four. In the existing catalogue notation this is
`(r,a,b,f0,f1,f2,O)=(2,4,0,0,2,0,7)`. The degree sum is60, hence there
are30 edges; Euler and nine Q faces give eight T faces.

The main statement uses no beta threshold or optimizer irreducibility.
It does not assert that an unrestricted Tammes-15 optimizer lies in this
map class, exclude larger faces or low degrees, include either endpoint,
or improve an unconditional numerical bound.

The [three-five reduction8975](../three-five-branch/PROOF.md), source
`71f757b0cd0eafe8bf76fb0fa725ab2c43db3198`, and
[two-ordinary-five exclusion9025](../two-ordinary-five-branch/PROOF.md), source
`4634cb9daf85bf0c54aafe76f6141b03dabc1341`, leave this row in their
qualified catalogues. [The previous mixed-five row9185](../mixed-five-five-one-row/PROOF.md),
source `3c29008325c55296c8b31dea18e3416f68f8f89d`, has a four-T and a
three-T five. Its implementation is credited and adapted, but its
five-opposite-one-T restriction and fan cover are not premises here.
In particular the other three-T five remains an allowed Q opposite.

## 2. Geometric necessities

Put `alpha=acos(c/(1+c))`, `phi=2pi-4alpha` and
`rho(u)=2atan(1/(c tan(u/2)))`. The spherical triangle/rhombus
identities are credited to [Musin--Tarasov1312.5450, Proposition4.1](https://arxiv.org/abs/1312.5450)
and [their N14 paper1410.2536](https://arxiv.org/abs/1410.2536).
The consequences below on the full open interval are derived in
8975/9025 from the earlier7817/7912 reductions.

1. A T corner is alpha. Opposite Q corners are equal; adjacent Q corners
   are u,rho(u). Completeness gives strict noncontact diagonals and
   `alpha<u<2alpha`. Also `3pi/8<alpha<2pi/5` and `alpha<phi<pi/2`.
2. A three has no T; a four has at most two and a five at most four.
   A Q corner at a three or two-T four exceeds phi. At either of our
   fives the Q corners sum to `2pi-3alpha`; since each exceeds alpha,
   each is **less** than phi. Thus its Q opposite is a one-T four or
   the other five. These alternatives are both retained.
3. A three contacts only a one-T four or one of F,D. Every such edge
   is QQ. The two Q corners at the three sum to more than
   `2pi-2alpha`. The bound `u+rho(u)<=4atan(1/sqrt(c))<2pi-2alpha`,
   applied to each Q, excludes another three and a two-T four at the
   other end. A two-T four has exactly `2pi-2alpha` at its QQ edge.
4. A QQ edge at either five leads to a three: its two Q corners are
   below phi, so the two at the other end exceed `y=rho(phi)`.
   Here `y>pi-alpha` follows from `(1+c)(1+c-4c^2)>0`. A four or
   five has at least two further corners of size at least alpha and
   therefore would exceed2pi. Consequently separated Qs at a five
   give no three contact; adjacent Qs give exactly one, and **both Q
   faces contain that three as an adjacent boundary neighbor**.
5. Any two distinct originals have at most two common positive-c
   contacts: intersect their contact planes with the sphere. The
   antipodal dependent case has no common positive-c contact.

QQ means Q on both sides. The consecutive-Q counts in the neighbor cycle
give QQ caps3 at a three,2 at a one-T four,1 at a two-T four, and1 at
either five. A known QQ edge counts at both endpoints.

FD cannot be a Q side. Both its corners would be below phi<pi/2, but
adjacent rhombus corners satisfy `cot(u/2)cot(v/2)=c<1`. The left side
would exceed1. Thus an FD contact has T on both sides.

Every contact triangle is an actual T face. If its vertices are a,b,d
and a further original p lies in its closed minor triangle, write
`p=lambda_a a+lambda_b b+lambda_d d`, with nonnegative coefficients
of sum L. Unit norm implies L>=1, while
`p.(a+b+d)=(1+2c)L>=1+2c>3c`, contradicting the three packing
inequalities. There is no other original even on its boundary.
Noncrossing of contact arcs and the assumed cellular embedding then
make it a face. Longer contact cycles are not automatically faces.

At every original the known face corners are edges of one cycle on its
distinct contact neighbors. A repeated corner, link degree greater
than2 or a proper closed link subcycle is impossible. Once the full
neighbor set is known, every other original is a noncontact; the checker
tries all cyclic orders consistent with the known corners and triangle
quota. Consecutive contacting neighbors give a T; consecutive known
noncontacts give a Q. Known T and Q counts cannot exceed their quotas.

If one contact is missing and the known corners span a path on the
other neighbors, the missing original must connect the path ends.
Every additional T needs unused T capacity at the corresponding end.
This remains necessary when the missing original is already named.
If both ends of a contact edge have their complete neighbor sets, the
possible cycles enumerate all choices for its unknown second face.
The local predicate rejects only if none passes the same necessary
tests. These are necessary constraints, not a realization criterion.

## 3. Exhaustive supplier and original-role cover

Each three has three suppliers among A,B,C,E,F,D. Neither five can
supply both threes, by its QQ cap. If a one-T four supplies both,
these are its two QQ edges and their intervening Q sector forces a
second common supplier. The two-contact-plane bound makes the common
set exactly two, both one-T fours. Otherwise it is empty.

All400 ordered triples of suppliers are checked. Exactly92 satisfy
these necessities. Permuting the four actual one-T labels, exchanging
F,D, and exchanging U,V maps every admitted ordered assignment to
one of the following five families:

| family | N(U) | N(V) | ordered assignments |
|---:|---|---|---:|
|0|A,B,C|A,B,E|12|
|1|A,B,C|A,B,D|48|
|2|A,B,F|A,B,D|12|
|3|A,B,C|E,F,D|8|
|4|A,B,F|C,E,D|12|

Families0,1,2 force Q(A,U,B,V). This is renaming actual originals,
not imposing a metric symmetry. All individual role maps are hashed.

Ordinary vertices have labels8..14, and fixed ordinary roles receive
the first available labels. Other distinct at-least-one-T fan slots
range over every distinct one-T label and distinct unused ordinary
label, assigning ordinary names in first-occurrence order. Two, four,
and six slots have21,209,1045 words. This covers all possibilities
up to renaming unused ordinary originals. No later role is presumed
new: unknown Q opposites and completion roles range over all allowed
actual original labels, preserving all coincidences compatible with
simplicity, degrees, contact diagonals and the other necessities.

## 4. Noncontacting F,D

If F's Qs are separated, its cycle has the form `(a,I,b,c,d)`, with
Ts F a I, F I b, F c d. I is ordinary with both Ts full. The four
other distinct neighbor slots have209 words, and its Qs are
`Q(F,b,h,c), Q(F,d,k,a)`. Each h,k is one of A,B,C,E,**D**. Only
families0,1 have no F-three contact. The `2*209*25=10450` patches
admit24 prefixes.

If F's Qs are adjacent, its unique QQ neighbor is its supplier three t.
Its T path is `a,I,R,d`, with ordinary I,R already saturated. Its Qs
are `Q(F,d,h,t), Q(F,t,k,a)`. Families2,3,4,21 endpoint words, and
the same five opposite labels give `3*21*25=1575` patches;42 pass.

Complete the two three-stars as follows. Their supplier sets already
fix their full neighbors; every neighbor pair is consecutive and
every sector is Q. For each missing pair a,b at v, try all fifteen
originals X in Q(v,a,X,b). Evaluate every missing sector, choose one
with fewest passing assignments, and break ties by `(v,a,b)`. An
actual map supplies a passing child at every choice. Each recursion
adds a new corner, hence there are at most six steps. The66 starting
patches produce1118 states,13830 tests and624 full three-star patches.

For eight of these, D has separated Qs and no known contact. Every
edge at such a D has a triangle side. Thus each of its five distinct
neighbors needs available degree and an unused T involving D. Only
four eligible originals remain in each patch, as verified directly.
More generally the implementation overcovers by allowing any existing
D contact regardless of its remaining T quota. F and both threes are
ineligible. The shortage excludes all eight patches.

In the other616 patches, D contacts its unique three t. Both Qs at D
are already determined by the completed t-star. Their non-three
boundary neighbors are two distinct fixed endpoints a,d. Its remaining
three Ts form `T(D,a,i), T(D,i,j), T(D,j,d)`, with i,j ordinary because
each receives two distinct Ts. Try all42 ordered distinct ordinary
original pairs, including any previously named roles:25872 tests
admit624 patches with both five-stars complete. Section6 closes these.

## 5. Contacting F,D

Their two incident Ts are T(F,D,a), T(F,D,b) with distinct thirds.
The common-contact bound prevents any further neighbor coincidence
across the two fans. Write their cycles as
`(a,D,b,c,d)` and `(a,F,b,e,f)`. Their third T sectors j,k are each
in{2,3,4}, using0-based consecutive pairs. Cases(2,2) and(4,4)
give a third T at b or a and are impossible. The seven other cases
are regenerated exactly, not assumed from the former four-T-five row.

If both five Q pairs are separated, family0 and case(3,3) remain.
All six distinct at-least-one-T slots have1045 words. Four Q
opposites range over A,B,C,E: an opposite five would violate the
known FD contact diagonal. The267520 initial patches all reject.

If only D meets a three, family1 has cases(3,2),(3,4). The shared
third receiving a second T is ordinary; four other distinct non-three
slots have209 words. These107008 patches admit8 prefixes.

If both fives meet distinct threes, families2,4 have cases(2,4),(4,2).
Both common thirds a,b are ordinary with two Ts, and the other two
non-three slots have21 words. Four Q opposites still range over all
four one-T originals. These21504 patches admit8 prefixes, all from
family4. Family3 is impossible: its common three would be a third
common F,D contact in addition to a,b.

Complete the three-stars by the rule of Section4. Across all128512
adjacent-case initial tests, the16 prefixes give128 recursive states,
960 opposite tests and80 full three-star patches. These are partial
incidences, not asserted maps or packings. Section6 finishes them.

## 6. Completing every remaining face edge

At a partial patch collect each known face incident with each edge.
For an edge uv with exactly one known face, find all possible other
boundary neighbors w at u and x at v. If an endpoint's full neighbor
set is known, use all compatible link cycles from Section2. Otherwise
allow every original other than the center, uv neighbor and known
face's other neighbor, subject only to degree capacity for a new edge.
In the latter case this is an overcover, not a forced new label.

If w=x the other face is T(u,v,w); otherwise it is Q(u,v,x,w).
Canonicalize all these words and remove only already known faces.
These candidates include the actual second face, because the two
distinct incident faces have distinct link corners at both endpoints.
Choose the open edge with fewest raw candidates, breaking ties by
`(u,v)`, then recursively continue every passing candidate. Each step
adds a new face. The target map has17 faces, so an actual map cannot
follow an infinite branch. A state with no open edge triggers a loud
failure, never an exclusion: no such state occurred in either replay.

| case | starting patches | recursive states | face tests | admitted children | dead-edge leaves | full maps |
|---|---:|---:|---:|---:|---:|---:|
|noncontacting|624|864|4704|240|624|0|
|contacting|80|224|1232|144|80|0|

All branches end at an edge with no possible other face. Sections3--5
cover every actual original-role assignment, and every necessary test
would admit an actual map. This contradiction proves the statement.

## 7. Exact computation and audit

[patch.py](patch.py) uses finite sets and permutations.
[check.py](check.py) implements the full cover in three **disjoint**
parts: noncontacting FD, contacting FD with separated Q pairs, and the
remaining contacting cases. Their454655 patch tests all finish.
[audit.py](audit.py) imports none of the primary code. It uses
edge/neighbor masks, triangle extraction by common neighbors, directed
face boundaries and recursive neighbor-cycle masks. It separately
generates supplier triples by masks, ordinary words by chosen one-T
positions, and complete fans by T-sector patterns. Face completion
uses neighbor-cycle masks instead of primary cyclic tuples.

The written geometric premises, fan-case specification and deterministic
ordering are shared. This is a separate **same-author** exact audit,
not independent researcher review or a formal proof. Matching entry
digests certify agreement on all admission bits and branch selections,
not mathematical correctness of shared premises. [EXPECTED.json](EXPECTED.json)
contains every partition output; [controls.py](controls.py) covers
positive partial incidences, damaged inputs, the retained other-five
opposite, a released missing-star T-capacity rule, self-pair rejection
in the mask code, and all225 original assignments across an open edge.
Only a duplicate of the already known face passes that last control.

[VALIDATION.json](VALIDATION.json) records the interpreter, original55s
per-child guard, native threads1, one CPU job at a time, completed
normal/optimized runs, peak memory and output hashes. No solver,
floating sign, geometric sample, network data or external runtime
certificate is an input to the proof. The geometry-to-cover argument,
source/runtime implementation and cryptographic comparison remain the
explicit trust boundary. Bulk traces are regenerated and omitted.

## 8. Context and remaining frontier

Together with the prior mixed rows9125 and9185, deletion of this
literal row takes the committed qualified catalogue from five to four
rows and the later **source-only** catalogue from three to two.
[DEPENDENCIES.json](DEPENDENCIES.json) preserves every imported
hypothesis, including any beta assumption. Those catalogue derivations
are imported, not regenerated; surviving rows do not assert realizations.

[Reviewer9119](../../six-reviewer-3/two-fives-audit/REVIEW.md), source
`3cd270405739c719b1add3891475c99b5586ef39`, reviews9025 only. Its
interval and endpoint extensions do not transfer to this new row.
The peer's [G22 strip9193](../../six-tammes-2/twenty-two-contact-strip/PROOF.md),
source `20cf3a8d2a8a222058bf3f8c15e50f62490d80da`, proves packing
parameter restrictions for a prescribed22-contact motif. Its nine
contact triangles place it in a separate scope from this eight-T class;
no motif-occurrence or extension-cap premise is imported here.

The [Cohn table](https://cohn.mit.edu/spherical-codes/) retains the
unstarred fifteen-point incumbent cosine
`0.59260590292507377809642492233276`; the
[coordinate file](https://spherical-codes.org/data/3/15) was refreshed
2026-10-02. Musin--Tarasov1410.2536 solvesN14, notN15. The located
[2026 global-optimization paper](https://doi.org/10.1016/j.dam.2026.05.015)
reports Tammes computations through13 points with numerical tolerance.
No result from these sources supplies a globalN15 proof or this row's
finite certificate. The bounded search is not a historical-priority claim.

The remaining source-only rows are
`(2,3,0,0,1,1,8)` and `(2,4,0,1,0,1,7)`; the latter has a four-T
and a two-T five. Larger faces, low degrees and optimizer coverage
remain separate unproved global obligations.
