# No integral fifth layer over the fixed fourth prefix can continue to six

Agent **six-heesch-2**, role **researcher**. Exact computer-assisted lemma with
a written motion reduction; not formalized or independently peer reviewed.

Let T be the unmarked214-iamond from the
[local-deficit construction](../heesch_polyiamond_local_deficit/proof.md).
Coordinates use the axial basis (1,0),(1/2,sqrt(3)/2). Let C4 be the union of
the79 placements of levels0 through4 in the pinned
[fixture](../heesch_polyiamond_hexapillar/coronas.json), applied to T.
The reader can reconstruct these inputs from `common.py`, which pins the
prior constructor and exclusion manifest; that constructor also pins the
earlier geometry and fixture bytes.

**Lemma.** There is no finite packing C5=C4 union S in which:

1. Every copy in S has a triangular-grid orientation (one of the twelve D12
   matrices) and an integral axial translation, avoids C4 and all other copies,
   and touches C4.
2. C4 is contained in the interior of C5.
3. A finite packing extending C5 by congruent copies of T contains C5 in its
   interior. These further copies may use all real Euclidean motions.

The lemma permits holes and pinches in C5 and its extension. In particular
it excludes every integral fifth corona continuing this specified fourth
prefix to a sixth corona under either Hc or Hh. The earlier four prefixes are
fixed. It does not exclude a real-phase fifth layer, a different fourth
prefix, or all six-corona configurations of T. It gives no exact Heesch
number or new record.

## Three local obstructions under all real motions

Every listed pattern consists of two, three or four nonoverlapping congruent
copies of T. A pattern is forbidden whenever all its copies are interior to
a finite larger packing. Applying a common Euclidean isometry preserves
each obstruction.

**Two-copy enclosed triangle.** Copies at the identity pose and its translate
(-12,-12) enclose the downward unit triangle (1,-1,-3) in compact notation.
Its three neighboring triangles are occupied by these copies. Thus its open
interior is a bounded component of their complement, of area at most one
unit triangle. Any further tile whose interior enters that component must
have its entire connected interior inside it: it cannot cross the closed
existing copies without positive-area overlap. Its area is214 unit triangles,
so none can enter. A boundary point of this enclosed region cannot become
interior to a larger packing, contradicting the asserted strict surround.

The same argument works for any enclosed complementary component with area
strictly smaller than an interior-connected tile. No lattice assumption on
the potential filling tile is needed for this area obstruction.

**Three-copy unfillable small gap.** The second pattern in `patterns.json`
leaves one60-degree sector at (-21,9). Its missing triangle is
up(-21,9). A strict surround must fill that sector with a60-degree tile
vertex. Its rays align with the gap, forcing a D12 orientation; vertex
coincidence forces an integral translation. The independent triangle oracle
finds22 sector-compatible poses. Every whole footprint overlaps one of
the three pattern copies. Hence no strict surround exists.

**Four-copy clash of forced providers.** The third pattern has the two
specified targets (0,-7) and (0,-3). Their missing triangles are respectively
down(-1,-7) and up(-1,-3). The occupied star at each target is contiguous and
has angle240 or300, leaving a120- or60-degree gap. A120-degree gap is filled
by a120-degree vertex or two60-degree vertices; a60-degree gap is filled by
one60-degree vertex. In every case incident filling vertices are at the
target and their rays align with triangular-grid directions. Again the
relevant providers are integral D12 copies even when all real motions are
initially permitted.

The triangle oracle enumerates22 and72 sector-compatible poses at these
targets. Removing complete footprint overlaps with the four fixed copies
leaves one pose at each: matrices[-1,-1,0,1] and[-1,-1,1,0], both translated
by(-3,-3). Their footprints are distinct and overlap in positive-area unit
triangles. One tile therefore cannot serve as both providers, and selecting
both is impossible. This excludes the pattern.

The oracle constructs providers by mapping every tile triangle bijectively
onto the required triangle through all six vertex permutations. It derives
each affine isometry from those images, checks the axial metric, then checks
the star sector and the complete footprint. This differs from the
convex-vertex/matrix enumeration used to discover the patterns. The preceding
sector argument shows that every admissible provider is included. Copies
not incident at a target have positive clearance in a finite patch and cannot
replace its required local filling.

## Complete fifth-layer formula

C4 is a disc with16906 triangles and812 boundary vertices. Let R be the union
of the six-triangle stars at those vertices, minus C4. It has1468 triangles.
Every integral strict surround covers R. Conversely covering R supplies an
open neighborhood of C4 in this aligned unit mesh. Any nonoverlapping integral
copy touching C4 contains some cell of R, so no eligible copy is omitted.

For each of twelve orientations, join each required cell to every same-facing
cell of the oriented tile. The resulting integral translation is unique.
Deduplicate poses and reject any whole-footprint overlap with C4. There are
99511 distinct anchored trials and7693 remaining candidates. One Boolean
variable denotes selection of each candidate. Every required triangle has a
positive covering clause. Every pair with a whole-footprint overlap has a
negative binary clause, including overlaps outside R.

If C5 can be strictly surrounded, all its copies are interior. The38
[previously proved two-copy exclusions](../heesch_polyiamond_local_deficit/expected.json)
are therefore necessary between fixed and candidate copies and between
selected candidate copies. They yield417 unit exclusions and10139 candidate
pair exclusions before geometric overlap clauses are combined. The fixed
79-copy prefix itself contains none of these forbidden pairs. This base
formula has7693 variables and1769563 clauses.

Finally transport each of the three new patterns by every possible fixed or
candidate anchor pose. If every transformed pattern pose belongs to C4 or the
candidate inventory, prohibit selection of all its nonfixed members. Fixed
copies are already present. The three patterns have1049,25,17 congruent
instances, giving1091 distinct additional clauses. This is a necessary
condition for any strict surround of C5, regardless of its new copies' real
translation phases. No untested model or heuristic completion is excluded.

The resulting formula has1770654 clauses and is UNSAT under an independently
checked DRAT certificate. Every hypothetical packing satisfying the lemma's
three conditions would induce a satisfying candidate assignment, a
contradiction. See `expected.json` for exact hashes and counts. The large CNF
and trace are regenerated in scratch, not published as opaque inputs.

## Context and trust boundary

The upstream construction has five complete disc coronas. Its original
all-motion finite bound was1316. Independently selected
[reviewer1](../heesch_polyiamond_deficit_review1/REVIEW.md) refined the bound to385;
[reviewer2](../heesch_polyiamond_local_deficit_review2/REVIEW.md) authenticated
the original native certificates and corroborated that refinement. Neither
review assesses this new fixed-fourth-prefix lemma.

[Mann2004](https://faculty.washington.edu/cemann/Heesch.pdf) contains the known
hexapillar-five family; our triangular realization remains an attributed
qualification, not a new-five or exhaustive-priority claim.
[Kaplan's census](https://arxiv.org/abs/2105.09438) and
[author dataset](https://cs.uwaterloo.ca/~csk/heesch/) concern bounded sizes.
This certificate closes a specified construction branch and does not replace
the unresolved finite-six/seven campaign target.

The38 old pair exclusions are mathematical prerequisites, imported from the
byte-pinned published proof, not claimed re-established by this replay.
All three new patterns are checked by the exact triangle oracle. The written
sector and area arguments, input reconstruction, candidate completeness,
Python implementation, PySAT and DRAT-trim remain explicit trust boundaries.
Assertions require an unoptimized interpreter. Solver UNKNOWN, a guard,
timeout, missing input or failed trace is never a mathematical exclusion.
