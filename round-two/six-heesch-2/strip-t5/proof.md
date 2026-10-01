# Exact Hc=2 and Hh=3 for a 23-cell unmarked polyhex

Actual author **six-heesch-2**, role **researcher**, 2026-10-01.
This is an author-checked computer-assisted proof with explicit, unformalized
geometric and software trust boundaries. No independent T5 review, Heesch
record, historical-priority claim, or theorem about all strip lengths is asserted.

For k>=1, in axial hexagon-center coordinates, put

```
T_k = {(0,0),(-2k,k-1),(-2k-1,k)}
      union {(x,y): 0<=r<k,
                     x in {-2r-1,-2r-2}, y in {r+1,r+2}}.
```

Use unit-side regular hexagons with center basis
`(sqrt(3),0),(sqrt(3)/2,3/2)` and neighbor differences
`(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)`.
T5 has 23 cells and is a connected topological disc. All Euclidean rigid
motions and reflections are permitted. Hc requires each corona prefix to
be a disc. Hh permits holes only in the final corona, following
[Kaplan's conventions](https://arxiv.org/abs/2105.09438).

**Theorem.** Hc(T5)=2 and Hh(T5)=3. T5 does not tile the plane.

## Checked lower constructions

`lower-Hc2.json` gives 28 whole copies in layers 1,8,19. The cumulative
cell counts are 23,207,644 and every prefix is a disc. Thus Hc>=2.
`lower-Hh3.json` gives 48 copies in layers 1,5,14,28 and cumulative cell
counts 23,138,460,1104. The first three prefixes have no holes; the final
prefix has 27 empty hole cells. Thus Hh>=3. The reader checks congruence,
global disjointness, complete halo inclusion, each new copy's attachment
to the preceding layer, connectivity and every required hole condition.

## All-motion and finite-depth reduction

We use the [published polyhex locking and pair-depth argument](../proof.md).
Only its general reduction transfers; every numerical T5 exclusion is new.
Here is the geometric bridge. A polyhex boundary corner has angle 120 or
240 degrees. A corner at a smooth point of another boundary edge either
overlaps or leaves a 60-degree sector, too small to fill with a polyhex
corner. Around a completely covered old boundary, unit-edge endpoints
therefore align. Filled vertices have complementary 120/240 sectors or
three 120-degree sectors. The incident unit edges fix the common honeycomb
grid, including vertex contacts. Induction through complete corona prefixes
locks all copies to the root grid. The same local argument locks an actual
plane tiling; it needs no assumption that tiling-distance prefixes are discs.
The [independent T4 audit](../../six-reviewer-3/strip-t4-audit/REVIEW.md)
also checked this general bridge. Its verdict concerns T4, not this result.

Let E0 be all disjoint grid copies contacting the root by a unit edge.
It is finite: an orientation and a pair of opposing boundary edges fix a
translation. The reader enumerates exactly 664 footprints by that method.
There is no nonidentity prototype stabilizer, so transport through the
unique D6 isometry is unambiguous. In this honeycomb grid a shared vertex
also forces a shared unit edge between incident cells; halo contacts include
all point contacts of disjoint grid polyhexes.

Define E_(r+1) to contain those B in E_r whose fixed union T5,B has a
disjoint whole-copy halo cover with all contacts in E_r. Holes are allowed.
For any reciprocal domain D, the complete finite candidate pool is the
union of its transports at the fixed copies, excluding overlap and
forbidding any contact with a fixed copy outside D. Mutual candidate
contacts must also be in D. Copies meeting no required halo cell can be
omitted. The exact-cover rejection reader implements precisely this problem.

If a contacting pair has both levels <=H-r in an H-corona patch, it belongs
to E_r. For the inductive step, its actual halo neighbors have levels at
most one greater; at the preceding depth, all their contacts are allowed.
The actual neighbors therefore supply the required pair-halo cover.
The same induction works in a plane tiling, using its finite neighborhoods.

For a domain D let F(D) be the one-sided support of root-halo covers whose
root contacts and mutual neighbor contacts are in D. For E0, mutual
compatibility is just packing. The certificate rejects 317 forced root
contacts, leaving a 347-contact set U0 containing F(E0). It rejects 110
forced contacts in D1, leaving a 56-contact set U1 containing F(D1).
These are necessary support sets; the proof does not need positive
certificates establishing exact equality with F(D).

**Directed support pruning.** If a finite packing completely covers the
halo of each fixed center, every added copy touching that center occurs in
one of its own complete root surrounds. Its relative contact therefore
lies in that center's transported F(D), provided all contacts in that local
surround are in D. It is safe to restrict candidate contacts with fixed
centers accordingly. This does not impose F(D) from an uncovered added
copy's viewpoint, or between two uncovered added copies.

Applying that observation with D=E0 gives a complete pair-halo universe
using outgoing U0 at both fixed centers and packing only among the added
copies. It reduces the 64 early negative certificates from 40,544 states
and 9.55 MB to 98 states and 30.8 KB. No restriction to the reciprocal
230-contact set, or global U0 compatibility, is used on added neighbors.

## Necessary domains and the upper bound three

A contact in E1 needs a root surround at both ends. Removing the 317
unsupported contacts and their reciprocals leaves 230 candidate pairs.
The 64 directed-support pair-halo rejections leave D1 of size 166.
The certificate then rejects 127 pair-halo covers in D1, leaving D2 of
size 39, and 17 covers in D2, leaving D3 of size 22. All domains are
reciprocal. Inductively E_r is contained in D_r. Positive tests and
equalities E_r=D_r are unnecessary.

The complete D3-compatible root-surround inventory has three stars,
with 6,6,5 neighbors. The independent inventory recursion chooses the first
uncovered cell, unlike the producer's MRV order. Every root-contacting copy
contains a root halo cell, which disjointness prevents any other copy from
covering. Thus an admissible root surround cannot have omitted redundant
neighbors. This enumeration includes every first corona.

Fix each such root and star. A next-halo cover compatible with D2 is
impossible, with rejection DAGs of 7,10,5 states. In a hypothetical fourth
corona, all contacts through level one are in E3 subset D3, so its first
corona is one of these stars. All contacts through level two are in
E2 subset D2, so its second corona supplies the impossible halo cover.
Therefore Hh<=3 and Hc<=3. An actual plane tiling supplies those same
finite neighborhoods, so this contradiction also proves non-tiling.

## Excluding the third disc corona

For three coronas, the first surround is D2-compatible. Its complete
inventory has eight stars, all disc first prefixes. Five next-halo
rejections in D1 have 31,9,9,9,7 states. The remaining cases are 4,5,6,
with 6,6,5 first copies. The following joint encodings cover every possible
second and third corona from those first prefixes, rather than selected
second-corona witnesses.

In a three-corona patch, every root/first center is completely covered
through level two. All contacts among its neighbors are in E1 subset D1.
Directed support pruning restricts each incident second copy to U1 at
that fixed center. Selected second copies must satisfy D1 compatibility
with one another. There are respectively 95,91,82 second candidates.
Every selected second center is completely covered through level three,
so its incident third copies belong to outgoing U0. Third copies are
disjoint from the fixed prefix and its halo, because the second corona
already covers that halo. Enumerating all permitted second parents gives
9008,8769,7983 third candidates. No U0 compatibility is imposed between
third copies, and no reciprocal support condition is imposed on them.

Each footprint has one selection variable. The CNF imposes global packing
by at-most-one selection at every cell, coverage of the fixed prefix halo
by second copies, coverage of each selected second copy's halo by the fixed
prefix or selected second/third copies, and a selected second parent for
every selected third copy. It also imposes D1 incompatibilities between
second copies. These are necessary conditions for every actual three-corona
patch, even though they relax attachment and most topology conditions.

Small at-most-one rows use a sequential chain. Large rows assign distinct
(row,column) tags to each candidate, imply both tags when it is selected,
and allow at most one row tag and one column tag. Two distinct selections
therefore conflict in at least one tag. Conversely, any at-most-one
selection extends to the tags and sequential auxiliaries, so no genuine
packing is lost by the encoding.

Cases 4 and 5 are contradictory without topological cuts. Case 6 uses two
necessary final-hole cuts. Each records a finite connected cell set C,
a point q in C, and selected wall footprints. The independent reader
checks that C is disjoint from the fixed prefix and wall, and that its
entire halo lies in their union. Retaining that wall confines C inside
a bounded complementary component. A final disc union retaining it must
cover q. The cut is exactly the disjunction of negated wall variables and
every permitted footprint covering q. Hence every three-disc patch
satisfies each cut. This necessity is established geometrically, separately
from the SAT contradiction. The encoding allows other holes freely.

The independently reconstructed CNFs have the following frozen dimensions
and hashes; none of the original CNFs is a reader input.

| case | variables | clauses | SHA256 | RUP additions |
|---|---:|---:|---|---:|
| 4 | 92099 | 536757 | b2b3117085ba5ad1b35a470ea00a61382da951d668d481ad270ec4cfca264e5c | 7 |
| 5 | 90198 | 523222 | 8f15a2281928dc674118176f2553df06ead675246b776d837f9efa5e08a1ed3f | 14 |
| 6 | 83458 | 477620 | e92168bac6251a541cbb4de0299582e77773204c4008534b73ae5a44bc931ad3 | 57 |

The [published solver-free RUP reader](../shifted-inner/rup_audit.cpp)
checks each addition by unit propagation under its negation and reaches
the empty clause. The three cores total 3,843 bytes. That reader runs
2,304 exhaustive two-variable controls and four false/malformed controls.
Deleting no proof clauses is sound under the stronger retained formula.
All necessary topology cuts are present in the final checked formula.

Thus all possible first coronas fail to extend to three disc coronas.
Hc<=2. Combining the two lower witnesses and the upper bounds proves the
theorem.

## Scope, verification and prior art

The portable reader checks 1,504 rejection states and independent first
inventories of 55+99 recursion nodes. It shares neither producer bitset
conflict matrices nor solver output as trusted verdicts. Its D6 matrices
are reconstructed by choosing successive/preceding unit-edge directions.
Coverage, conflict and topology checks use exact integers and sets;
all rejection checks remain active under Python -O. Normal/-O runs agree
on all deterministic evidence. Seven geometry/certificate controls and
three topology-cut controls reject. The RUP program is a reused generic
dependency, whose earlier shape-specific claims are not transferred.
This is same-author algorithm independence, not peer review or formalization.

The primary [Kaplan census](https://cs.uwaterloo.ca/~csk/heesch/) currently
enumerates polyhexes through 17 cells. T3 is its known 15-cell four-corona
control; [T4](../strip-t4/proof.md) has exact Hc=Hh=3, as independently
reviewed. Those results do not establish T5's domain exclusions or lower
witnesses. The [later Kaplan survey](https://arxiv.org/abs/2509.12216)
supplies current context for the wider Heesch problem. These sources were
refreshed on 2026-10-01. Being outside the census is not evidence of
historical novelty. The assigned finite-five polyhex frontier remains open here.
Lengthening this strip to k=5 does not reach it; no conclusion for k>=6
or a different endpoint pattern follows.
