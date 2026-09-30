# The original second-prefix branch has five coronas and no sixth

**Agent six-heesch-2, role researcher.** This exact computer-assisted result
concerns the connected unmarked214-iamond T214 in the byte-pinned
[prototype input](../heesch_polyiamond_deficit_review1/input.json).
Axial coordinates(x,y) mean(x+y/2,sqrt(3)y/2). Reflections are allowed.
The shape belongs to the attributed hexapillar-five family; its positive
five-corona construction is inherited rather than a new record.

## Precise statements and conventions

Let A2 be exactly the17 copies at levels0 through2 in that input, with level
counts1,5,11. Let A3 be exactly its40 copies at levels0 through3, with counts
1,5,11,23. These are fixed named families, not arbitrary second/third prefixes.
For a finite copy family X write U(X) for its closed union. Every packing has
disjoint whole-copy interiors. Families in a strict-surround chain are nested,
and each old union lies in the interior of the next union.

**Theorem.** A3 has no three successive strict surrounds. There are no finite
whole-copy packing families B,D,E, containing A3 and then one another, with

    U(A3) contained in int(U(B)),
    U(B) contained in int(U(D)),
    U(D) contained in int(U(E)).

All translations, rotations and reflections may be arbitrary real Euclidean
motions. No contact, disc, connectedness or final-hole condition is imposed
on B,D,E. The theorem transports under a common congruence.

**Corollary.** A2 has no four successive strict surrounds. In particular no
six-corona chain can start with this original second prefix, for any third,
fourth or fifth choices. This uses the explicit earlier
[second-prefix rigidity theorem](../heesch_polyiamond_second_prefix_rigidity/proof.md):
two successive surrounds of A2 force all23 original third copies in the
first extension, even without a contact condition. A hypothetical
A2,B3,D4,E5,F6 chain therefore has A3 as a subfamily of B3. D4,E5,F6 would
give the three forbidden surrounds of A3. No equality B3=A3 is needed.

The131-copy positive fixture is fully rechecked: its level sizes are
1,5,11,23,39,52, and it has five complete disc coronas. Thus the maximum
corona depth continuing this **specified** second-prefix branch is five.
For A3 the maximum number of further strict surrounds is two. Neither
statement classifies unrelated first/second prefixes or gives H(T214)=5.
The global interval remains `5 <= Hc(T214) <= Hh(T214) <= 385`, with upper385
credited to [review1](../heesch_polyiamond_deficit_review1/REVIEW.md) and
[corroboration](../heesch_polyiamond_local_deficit_review2/REVIEW.md).
Those audits concern the earlier upper-bound proof, not this new result.

Hc requires disc prefixes; Hh allows holes in the final prefix, following
[Kaplan's conventions](https://cs.uwaterloo.ca/~csk/heesch/). The negative
above applies to a broader arbitrary-topology class. No finite-six
construction, new tile, height record, size optimum, peer review or
formalization of this new contribution is asserted.

## Complete local covers with unrestricted real motions

T214 has minimum positive vertex angle60 degrees. At a lattice vertex of a
known union with a contiguous missing60- or120-degree sector, strict
neighborhood coverage forces genuine tile corners at the vertex. A tile
edge-interior point would occupy180 degrees and a tile-interior point360;
both would overlap the known occupied sectors. Tiles not containing the
vertex have positive distance from it, since the packing is finite.

The missing sector is covered by one60-degree corner, one120-degree corner
or two60-degree corners. Its boundary rays force the incident corner rays
to the triangular-lattice directions. Hence the relevant providers have one
of the twelve lattice linear isometries. Their incident source vertices
force integral translations. This locks only these providers; unlisted
copies remain free to use arbitrary real motions. The mechanism is credited
to the [earlier local proofs](../heesch_polyiamond_third_prefix_closure/proof.md).

For a required incident unit triangle, join its centroid to every prototype
triangle under every linear isometry. Reject wrong incident sectors and
every whole-footprint intersection with the known union. These exact face
joins regenerate the **complete** allowed list, separately from discovery's
convex-vertex anchors. Centroid pairs in the certificates are three times
the physical axial centroids. An allowed incident tile owns the entire
required unit triangle. Every cover clause therefore contains an owner
present in any hypothetical strict surround.

Aligned integral copies have positive-area overlap exactly when their
unit-face sets intersect. The reader also checks that T214 has only the
identity automorphism: every real automorphism maps the polygon's edge
directions and a lattice vertex to themselves as lattice data, so a complete
one-face join census suffices. Thus the pose codes used here name distinct
physical copies.

The38 excluded interior attachments from the
[original deficit proof](../heesch_polyiamond_local_deficit/proof.md), with
the separate review above, remain mathematical premises. Regenerating its
59-pose narrow-pocket catalogue and21 retained indices does not itself
prove those38 exclusions. Each used pair is checked in both relative
directions. Such a pair cannot lie in the interior of a larger packing.
Its use on newly selected B copies therefore needs U(B) inside int(U(D)).

Single-surround patterns are rechecked by complete empty-corner lists,
incompatible pairs of complete forced-provider lists, or enclosure of a
one/two-face hole. Connected tile interiors of area214 cannot enter a small
enclosed hole without crossing a fixed tile interior. Strict interiority
of its boundary would require filling that hole. Final holes being allowed
does not avoid this obstruction. The preceding
[fourth](../heesch_polyiamond_fixed_fourth_extension/proof.md),
[third](../heesch_polyiamond_fixed_third_extension/proof.md),
[alternate](../heesch_polyiamond_alternate_fourth/proof.md),
[single-gap](../heesch_polyiamond_six_copy_obstruction/proof.md) and
[corner](../heesch_polyiamond_third_prefix_closure/corner-pattern.json)
sources are credited.

Two additional pairs in [single-patterns.json](single-patterns.json) leave
acute unfillable gaps. One is the identity copy and pose
matrix(0,1,1,0), translation(-12,-12), at vertex(0,-2). The other is identity
and matrix(-1,0,0,-1), translation(-3,-3), at vertex(-3,-1).
Each complete census has1284 centroid joins and22 incident trials; every
trial overlaps a whole fixed copy. They forbid making the corresponding
target interior under arbitrary real motions. Their common-congruence
instances supply sound single-surround negative clauses.

## Thirty-seven common fourth copies under two future surrounds

Assume only that A3 has two successive strict surrounds B,D. The Boolean
variables in [common.json](common.json) name379 relevant B-copy poses.
Every listed copy is whole-disjoint from OLD A3. Unlisted real copies are
unrestricted. The sparse necessary clauses are:

| Clause reason | Count |
| --- | ---: |
|Complete old-point60/120-degree cover|32|
|Whole-copy overlap binary|266|
|Old interior-pair unit against A3|62|
|Old interior-pair binary|14|
|Single-surround pattern|5|

The379 forward unit steps force32 copies and exclude347 other providers.
There is no two-surround-pattern premise in this forcing proof, so two
future surrounds of A3 suffice. A separate bit-mask checker validates each
unit reason; the discovery propagation trace is not an input.

At five vertices of OLD A3, the resulting partial B packing has a single
60-degree gap. The reader checks these points belong to OLD A3, not merely
to selected B copies. Sequential complete whole-disjoint censuses force:

| Old vertex | Required centroid times3 | Unique provider(matrix; translation) |
| --- | --- | --- |
|(-27,15)|(-80,46)|(1,0,-1,-1);(-36,36)|
|(-6,42)|(-16,125)|(0,-1,-1,0);(6,51)|
|(0,-39)|(-2,-116)|(0,1,1,0);(-12,-48)|
|(24,-45)|(71,-136)|(-1,0,1,1);(33,-66)|
|(45,-21)|(136,-65)|(-1,-1,0,1);(66,-33)|

Each list again has1284 joins and22 trials, with just one whole-disjoint
provider. No pair exclusion is needed for these terminal implications.
Previous forced copies act as blockers, but are never assumed interior
in B. The OLD-point condition is essential: coverage is required in B
only for points of A3. Let L be these five copies and the32 unit-forced
copies. All37 members of L are now proved to occur in B.

## Four complete fourth subsets

Remove the four marked selector clauses from [closure.json](closure.json).
The remaining330 clauses are necessary already under A3 inside B inside D:
nine complete covers at OLD A3 points,282 whole-overlap binaries,11 old-pair
units,25 single-surround clauses and three overlap units against the five
derived terminal copies. Every positive cover is regenerated against only
OLD A3. The derived constants can block whole copies without licensing
new protected points on their own boundaries.

Temporarily assert that none of the following four tail pairs is present in
B. These are exactly the four marked negative selector clauses:

| Name | First pose(matrix; translation) | Second pose(matrix; translation) |
| --- | --- | --- |
|A|(-1,0,1,1);(78,-12)|(0,1,-1,-1);(57,30)|
|original|(-1,0,1,1);(81,-18)|(0,1,-1,-1);(60,24)|
|B|(-1,0,1,1);(84,-24)|(0,1,-1,-1);(63,18)|
|C|(-1,0,1,1);(87,-30)|(0,1,-1,-1);(66,12)|

Thirteen elementary RUP additions ending in the empty clause refute all334
clauses. For each addition, negating its literals and running unit
propagation against the previous clauses gives a contradiction. Therefore
the330 necessary clauses imply that at least one complete tail pair occurs.
This proof does not rely on the completeness of a saved native model census.

For each tail pair the family A3 union L union tail has79 copies and16906
faces. Exact mesh checks give a disc. Every vertex star of A3 is filled, so
A3 lies strictly inside this family. This identifies four complete fourth
subsets under **two** future surrounds, with arbitrary-motion extra copies
still permitted. It removes the fourth-layer grid restriction of the
[old four-case reduction](../heesch_polyiamond_fixed_third_extension/proof.md).

If every new B copy touches A3, B is exactly one of these four families.
Indeed the selected79-copy union is a subpacking and contains an open
neighborhood of A3. Any further tile touching A3 would meet the interior
of that subpacking. A small open set in the prospective Jordan tile cannot
be covered solely by finitely many tile boundaries, which have empty
interior. It would overlap an existing whole tile's interior and must be
that same tile. This contact-interiority argument is also credited to
[P17](../heesch_polyomino_four_corona_frontier/proof.md).
Equality is optional; subset containment is enough for the exclusion below.

## Four small obstructions exclude two more surrounds

The normalized patterns in [two-patterns.json](two-patterns.json) are
subfamilies of the corresponding fourth subsets. Every complete local
cover is regenerated against only its own fixed pattern; no global79-copy
premise or discovery pool is loaded. The geometric negatives use only
overlaps, old interior pairs and rechecked single-surround patterns.
Forward bit-mask proofs establish that each pattern has no two successive
strict surrounds, with arbitrary real motions and topology:

| Fourth case | Fixed copies | Relevant providers | Covers | Clauses | Unit steps |
| --- | ---: | ---: | ---: | ---: | ---: |
|A|3|7|2|8|7|
|original|9|41|6|42|41|
|B|7|62|7|63|62|
|C|7|12|4|13|12|

For example the A pattern has identity, matrix(0,-1,1,1) at(-6,3), and
matrix(0,-1,-1,0) at(24,15). Its two complete allowed lists have three and
four providers. One old-pair unit and five single-surround clauses force
a conflict. The other exact patterns and reason lists are supplied in full.
They transport under a common congruence. The fixed supports were found
by96 seeded deletion orders; no minimum-support claim is made.

Now assume three future surrounds B,D,E of A3. The two-surround reduction
places one of the four fourth subsets in B. Each contains its corresponding
proved local pattern. U(B) inside int(U(D)) and U(D) inside int(U(E)) would
give that pattern its two forbidden surrounds. The four selector negatives
are thus genuine geometric consequences under this additional stage,
rather than temporary assumptions. The same13 RUP additions give the
direct three-surround contradiction.

The stage count cannot be shortened. Two-surround patterns made of B
copies require BOTH D and E. They cannot be applied when only B and D are
assumed. The original five-corona fixture provides two actual further
surrounds of A3 and verifies this boundary of the result. Along with the
imported A2 rigidity this proves the stated five-but-no-six branch result.

## Source, validation, literature and remaining frontier

The [reader](check.py) uses exact standard-library Python and byte-pinned
older centroid/pattern routines. It reconstructs all complete lists,
whole-copy tests, terminal implications, transported patterns, forward and
RUP proofs, prototype automorphisms and the positive five-corona fixture.
It does not trust a dense formula, native SAT verdict, DRAT, extractor,
constructor inventory, model count or supplied discovery trace.
[expected.json](expected.json) records every census and reason count.
The documented normal and optimized commands must agree exactly and reject
all ten malformed controls. The earlier A2 rigidity has a separate documented
replay command and remains an explicit imported theorem.

Trust boundaries include the written small-sector locking, enclosure,
halo and Jordan contact arguments, the old38 interior-pair lemmas and
ordinary exact Python execution. No independent peer verdict or formal
proof of this new result is claimed. Source certificates are compact;
private generated formulas, native traces and adaptive histories are omitted.
No timeout, UNKNOWN, killed process or incomplete enumeration supplies a
mathematical negative. The paused dense7657-pose route is not reused.

[Kaplan2021/2022](https://arxiv.org/abs/2105.09438) and its author data give
bounded polyform censuses and corona conventions;
[Mann2004](https://faculty.washington.edu/cemann/Heesch.pdf) supplies the known
finite-five family. [Kaplan2025](https://arxiv.org/html/2509.12216v1) gives
connected-disc record context through six. Bounded enumerations are not
global maxima. The standing disconnected arbitrary-height qualification
does not settle the assigned connected-disc frontier. No exhaustive2026
priority finding is asserted.

This closes the different original second-prefix branch after the
[alternative18-copy closure](../heesch_polyiamond_second_prefix_closure/proof.md).
The new [P17 three-first reduction](../heesch_polyomino_three_first_corona_frontier/proof.md)
and [curved-trapezoid upper-six theorem](../heesch_trapezoid_six_upper_bound/proof.md)
are complementary different-tile work. Their full proofs and committed
bodies were read; their geometry is not a T214 premise and their readers
were not replayed. No reviewer was directed. Their contact and complete
neighborhood mechanisms support the next broader classification step.
Remaining T214 first/second prefixes, or a changed connected unmarked
polyiamond with actual finite-six coronas, remain the substantive frontier.
