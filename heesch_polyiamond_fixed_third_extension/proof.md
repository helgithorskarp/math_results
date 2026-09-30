# Every integral fourth-and-fifth route over the fixed third prefix stops before six

Agent **six-heesch-2**, role **researcher**. Exact computational lemma with a
written geometric reduction. No independent review or formalization is claimed.

Let T be T214 from the
[local-deficit construction](../heesch_polyiamond_local_deficit/proof.md).
Axial coordinates use the basis(1,0),(1/2,sqrt(3)/2). Let C3 be the union of
the40 placements of levels0 through3 in the byte-pinned
[131-pose fixture](../heesch_polyiamond_hexapillar/coronas.json), applied to T.

**Lemma.** There do not exist finite packings C4=C3 union S4 and
C5=C4 union S5 satisfying all of the following:

1. Copies in S4 and S5 have integral axial translations and one of the twelve
   D12 orientations. Every new copy touches the preceding union; all whole
   tile interiors are disjoint.
2. C3 is contained in the interior of C4, and C4 in the interior of C5.
3. Some finite packing of congruent copies extending C5 contains C5 in its
   interior. These further copies may use arbitrary real translations,
   rotations and reflections.

The lemma allows holes and pinches in the later unions. It excludes integral
fourth-and-fifth routes to a sixth corona extending this specified third
prefix under either disc or final-hole conventions. It neither bounds all
configurations by five nor excludes real phases in the fourth/fifth layers.

## A new two-copy area obstruction

Place T at the identity and at matrix[0,-1,-1,0], translation(-3,-3).
Their whole footprints are disjoint. They bound the rhombus consisting of
up(-1,-3) and down(-1,-3), using the compact unit-cell notation of the source.
Both missing triangles are unoccupied, and each edge-neighbor outside this
two-triangle set is occupied by the two copies. Thus the open rhombus is a
bounded complementary component of area two unit triangles.

The interior of T is connected and has area214. If a nonoverlapping congruent
copy enters this complementary component, its entire connected interior
must lie there: an open connected tile interior cannot cross either existing
closed tile without positive-area overlap. Its area makes that impossible.
The two existing copies consequently cannot both be interior to a larger
finite packing. This argument permits all real motions for possible fillers.

The standalone certificate [hole.json](hole.json) is checked through the
earlier [definition-level pattern oracle](../heesch_polyiamond_fixed_fourth_extension/patterns.py):
it reconstructs both footprints, checks nonoverlap, missing triangles and
every edge-neighbor. No picture or floating-point test is a premise.
Common isometries transport this obstruction to every congruent instance.

## Complete fourth-layer reduction

C3 is a disc of8560 triangles with626 boundary vertices. Its full vertex halo
R contains1150 missing unit triangles. Every integral strict surround covers
R. Conversely full halo coverage supplies an open neighborhood of C3 in the
aligned unit mesh. Every nonoverlapping integral copy touching C3 contains
at least one halo triangle, so no admissible new copy is omitted.

For each D12 orientation and each required triangle, join it to every tile
triangle of the same facing. The resulting integral translation is unique.
Deduplicate poses and reject every whole-footprint overlap with C3. This
enumerates77044 distinct anchored trials and6208 candidates. A Boolean
variable selects each candidate. Positive clauses cover every required cell;
negative binaries prohibit all complete footprint overlaps, including those
outside R.

Under the hypothetical continuation, fixed and selected copies are interior.
The38 [published interior-pair exclusions](../heesch_polyiamond_local_deficit/expected.json)
therefore supply316 fixed-to-candidate exclusions and8333 candidate-pair
exclusions. The three
[earlier local patterns](../heesch_polyiamond_fixed_fourth_extension/patterns.json)
and the new rhombus pattern supply further necessary clauses by exact
congruence matching. The earlier small-gap provider arguments allow all
real motions; their sector alignment is not a global phase-collapse theorem.

## Four continuation exclusions and the final proof

The four selectors in [cases.json](cases.json) each choose39 fourth-layer
copies over C3. Independent of the search, the geometry phase reconstructs
their complete16906-triangle unions, verifies no overlaps, full coverage of
the C3 vertex stars, contacts with level3 copies, and a disc boundary.
Their four physical unions are distinct. Selection labels carry no marks
on the tile; they only index the regenerated candidate pool.

The original selector is exactly the79-pose fourth prefix of the
[committed predecessor lemma](../heesch_polyiamond_fixed_fourth_extension/proof.md).
That result excludes every integral fifth strict surround permitting an
all-motion further surround. It is an explicitly imported premise.

For each of the other three selectors A,B,C, rebuild the **complete** integral
fifth-layer inventory over its fixed79-copy union. The halo clauses, whole
footprint overlaps,38 interior-pair exclusions,three imported patterns and
new rhombus pattern are all necessary if a sixth surround exists. Each
formula is UNSAT, independently checked by DRAT-trim. Its positive small-gap
models or heuristic search history are not used as proof.

Each of these four strict-continuation exclusions gives a negative clause
on that selector's39 fourth variables. Such a clause remains sound for a
hypothetical selection containing the whole selector: its copies cover R,
so any additional integral copy touching C3 would overlap an occupied halo
triangle. The selection cannot be enlarged by another eligible fourth copy.

Add these four clauses to the complete C3 fourth-layer formula, including
all congruent rhombus instances. The final formula is independently
DRAT-verified UNSAT. Every hypothetical packing in the lemma would induce
a satisfying assignment respecting all its necessary clauses, a
contradiction. [expected.json](expected.json) pins counts and CNF/proof hashes.
The final refutation supplies completeness; an exploratory nine-model
census and its stopping conditions are not mathematical premises.

## Scope, literature and trust

The original lower construction has five complete disc coronas. The earlier
finite upper bound1316 was sharpened to385 by the
[first independent review](../heesch_polyiamond_deficit_review1/REVIEW.md),
then corroborated by the [native-certificate audit](../heesch_polyiamond_local_deficit_review2/REVIEW.md).
Thus5<=Hc(T214)<=Hh(T214)<=385 remains the global interval. Those reviews
assess the earlier deficit proof and do not cover this new prefix lemma.

[Mann2004](https://faculty.washington.edu/cemann/Heesch.pdf) contains the known
hexapillar-five family. The triangular interpretation is an attributed
qualification, not a new-five record or exhaustive priority finding.
[Kaplan2021/2022](https://arxiv.org/abs/2105.09438) and its
[dataset](https://cs.uwaterloo.ca/~csk/heesch/) concern bounded polyform sizes.
This lemma advances the remaining finite-six construction search to a
changed third prefix or genuinely different phases, within unmarked
connected/disc polyiamonds.

Trust boundaries include the written mesh/area/sector arguments, byte-pinned
exact Python geometry, candidate completeness, imported38 pair exclusions
and original fourth-prefix lemma, and Boolean encoding. Native negative
evidence is independently DRAT-checked; a solver guard, timeout, UNKNOWN or
incomplete inventory is never nonexistence. Native proofs and CNFs are
regenerated outside source. No solver resource setting is raised.
