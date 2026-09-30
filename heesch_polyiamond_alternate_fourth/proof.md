# A fixed alternative fourth prefix has no two further real surrounds

**six-heesch-2, researcher; 2026-09-30.**

## Statement and geometry

T is the same unmarked 214-iamond defined by the side-sign table in the
byte-pinned [reviewer input](../heesch_polyiamond_deficit_review1/input.json)
and constructed in [the original source](../heesch_polyiamond_local_deficit/proof.md).
Axial coordinates (x,y) denote the Euclidean point
(x+y/2,sqrt(3)y/2). Integral linear isometries are the twelve maps preserving
this Gram form. Tile boundaries have angles in multiples of 60 degrees and
minimum positive angle 60 degrees. Reflections are admissible.

[witness.json](witness.json) specifies 89 copies with levels 0 through 4.
Let A_i be the cumulative closed union through level i, and let A=A_4.
Every A_i is a topological disc, every new copy contacts the preceding
layer, and A_i is contained in int(A_(i+1)) for i<4. Their exact counts are:

| level | copies in layer | cumulative copies | unit faces | boundary vertices |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 214 | 72 |
| 1 | 5 | 6 | 1284 | 192 |
| 2 | 12 | 18 | 3852 | 412 |
| 3 | 30 | 48 | 10272 | 592 |
| 4 | 41 | 89 | 19046 | 786 |

**Theorem.** No finite packing B containing these specified copies admits a
further finite packing D containing the B copies with
`A subset int(B)` and `B subset int(D)`.
All interiors are disjoint and all motions are real congruences. Neither
contact of added copies nor a topological condition on B,D is assumed.

The statement does not decide existence of one further surround of A.
It does not exclude six coronas based on another fourth prefix. In
particular the previously proved global lower five persists.

## Positive certificate

The checker reconstructs all whole footprints, verifying 214 faces per
copy and disjoint interiors. At every prefix it checks edge connectivity,
manifold vertex links, a single boundary cycle and Euler characteristic
one. It checks contact against the immediately preceding layer. Every
vertex of A_i has all six incident unit faces present in A_(i+1).
In this finite cell setting that implies strict inclusion of the entire
closed prefix: full stars give open neighborhoods at vertices, and the
adjacent faces give neighborhoods along edges and interiors. Hence these
are four complete admissible disc coronas, not merely corner coverings.

## An all-real necessary placement pool

Assume B,D as in the theorem. At any reentrant vertex of A the remaining
angular gap is 60 or 120 degrees. A copy covering that neighborhood must
have a convex vertex there: interior points and straight or concave
boundary points have angles too large. Finite strict coverage partitions
the gap into tile angles, each at least 60 degrees. A 60-degree gap has one
aligned acute provider; a 120-degree gap has one aligned 120-degree
provider or two aligned acute providers. No positive angular slack can
remain. Thus all these providers have integral D12 poses, even though
unrelated copies of B,D can have arbitrary real poses.

The 329 reentrant vertices of A require 441 missing incident unit faces.
For each such face, match every tile face with all twelve integral linear
isometries. Equality of centroid coordinates determines an integral
translation when their two differences are divisible by three. Removing
whole-copy overlaps with A gives exactly 2213 distinct poses. This method
regenerates the vertex-anchor discovery inventory with pool digest
`4db8aff16e062984055c58d8b4efca03b441f1112d1e6e09ce887d53babd2c68`.
It enumerates every integral pose covering any required face and therefore
every locked provider actually occurring in B. Other real B copies are
omitted, which weakens the necessary constraints.

Number poses lexicographically by their six integer matrix/translation
entries. X_j means the j-th pose occurs in B. A complete face-owner clause
is necessary for every required face. Every selected provider is interior
in D because B is strictly inside D. All fixed A copies are interior too.
Consequently the old 38 forbidden interior-pair lemmas apply to both fixed
and selected copies. These are imported mathematical conclusions of the
original local-deficit proof, with independent earlier audits; they are
not inferred from mere relative-pose enumeration in this checker.

## Two new local gap patterns

[patterns.json](patterns.json) contains two normalized triples of copies.
In each triple an unoccupied unit sector has angle 60 degrees at a vertex
with five occupied sectors. If all three copies are interior in a further
packing, that vertex must be filled by an aligned acute copy. All 22
possible acute providers are enumerated and each overlaps a whole fixed
copy in the triple. Thus neither triple can consist of interior copies in
any finite packing, allowing arbitrary real motions and topology.

Discovery anchored convex vertices; its separate affine-triangle oracle
checked each pattern. The public centroid checker regenerates all 22
acute providers and rechecks whole-copy overlap. Each pattern gives a
negative clause whenever its three poses occur among fixed A copies and
candidate B providers. No marked-edge assumption is used.

## The 19-clause contradiction

The public certificate retains five complete face-owner clauses, four
imported pair units, eight imported pair binary clauses, and two new local
pattern clauses. Its exact forward unit replay has 18 assignments.

Four singleton cover clauses force
`X_1268, X_1279, X_1285, X_1291`.
The remaining complete cover requires one of

```
368 370 524 525 530 535 540 1457 1458 1463 1468 1473 2207 2210
```

The pair units forbid `368,524,1457,2207`. The pair binary clauses with
the four forced providers forbid `525,530,535,540,1458,1463,1468,1473`.
The new triple patterns forbid `370` and `2210` because `1291` is forced.
Every literal of the complete cover is false, a contradiction.

The reader establishes each retained cover is the **entire** owner list
from the complete pose pool; each imported exclusion is checked against
its exact old relative-pair catalogue; and each new pattern clause is
matched against exact whole placements. The compact certificate neither
assumes native SAT output nor consumes the dense discovery formula.
This proves the theorem for all real motions under its two strict-surround
hypotheses. Contact and final-hole conventions do not enter the negative
argument. The four positive coronas satisfy the stronger disc convention.

## Reproducibility and limits

Run [check.py](check.py) as documented in [README.md](README.md). The pinned
helpers use exact integers and explicit exceptions; the malformed unit
controls must reject with assertions both enabled and disabled. The
checker reuses prior reviewer centroid geometry and author-authored sparse
helpers. This is a different implementation from discovery, within the
same researcher's work. No new independent review or formalization is
claimed. The written sector argument and the old pair lemmas are explicit
trust boundaries.

A larger complete fifth-grid formula build exceeded the unchanged
55-second process guard before solver invocation. That event gave no
nonexistence conclusion. The new theorem uses an independently regenerated
small-gap pool, local geometric checks, and the sparse contradiction above.
Other corona prefixes, global exact Heesch values and a finite-six
construction remain unresolved.
