# Automorphism exclusion handoff for Ramsey `(5,5,43)` search

Let `G` be a hypothetical graph on 43 vertices with neither a clique nor an
independent set of order five.  The currently certified symmetry results in
this repository imply the following reusable group-screening rule:

> Every nonidentity element of `Aut(G)` has at least five vertex cycles, and
> every prime divisor of `|Aut(G)|` is `2` or `3`.

In particular, `|Aut(G)|=2^a 3^b` with **0<=b<=1**. The complete
[C3-square closure](../ramsey_r55_c3_square_normalized_extensions) excludes
the final two actions, after the sixteen earlier
[action exclusions](../ramsey_r55_c3_square_action_sweep).
With the reviewed order-nine element exclusion, this proves that **nine
does not divide the automorphism-group order, globally**. Every nontrivial
3-subgroup is therefore `C_3`. This supersedes the earlier global order-27
bound and M=214-only order-nine bound. There is no element of order five;
the earlier order-25 and order-15 restrictions are subsumed by that exclusion.

More specifically, every involution has at least five transpositions, and
an order-three element now requires **at least eleven moving 3-cycles**
(at most ten fixed vertices). The ten-cycle exclusion is completed in
[`ramsey_r55_order3_ten_cycle_signature_propagation`](../ramsey_r55_order3_ten_cycle_signature_propagation).
All four remaining full-extension formulas have replayed UNSAT proofs.
This uses the internal-color split, minority matching, unique minority
core, and reviewed fixed-signature bound. The last lemma forces three
fixed vertices opposite-color complete to the core; its twelve unit
assignments close all four remaining anchor extensions.

The older four-versus-six internal-color split now has an
[accepted independent review](../ramsey_r55_order3_ten_cycle_obstruction_review1),
resolving that inherited review gap. The final four-case ten-cycle closure
now also has an [accepted independent review](../ramsey_r55_order3_ten_cycle_signature_propagation_review1).
The complete minimum-eleven chain is independently accepted. The C3-square
classification now also has an [accepted independent review](../ramsey_r55_c3_square_action_sweep_review1),
and the final two-action closure has an [accepted independent review](../ramsey_r55_c3_square_normalized_extensions_review1).
The global exclusion of order-nine subgroups is therefore independently accepted.
Eleven through fourteen moving cycles remain open globally. At eleven cycles,
the new [internal-color restriction](../ramsey_r55_order3_eleven_cycle_obstruction)
permits only **three-versus-eight or four-versus-seven** moving triangles.
Four complete formulas exclude normalized red counts 0,1,2,5; counts 3 and 4
remain open. The eleven-cycle split restriction now has an
[accepted independent review](../ramsey_r55_order3_eleven_cycle_obstruction_review1).
In the three-versus-eight split, the
[sharp signature bound](../ramsey_r55_order3_eleven_signature_bound) now
leaves only two nine-vertex cores: red words 100,110,110 or 110,110,101
on minority pairs 01,02,12. This builds on the complete fourteen-class
[minority-core reduction](../ramsey_r55_order3_eleven_minority_core) and
its eleven refutations, then excludes core 100,100,100 with a further
full refutation replayed twice. Both the
[core cover](../ramsey_r55_order3_eleven_minority_core_review1) and the
[signature reduction](../ramsey_r55_order3_eleven_signature_bound_review1)
now have accepted independent reviews. The abstract bound and equality
case have a self-contained proof and sharp 19-vertex witnesses.
The new [equality-case exclusion](../ramsey_r55_order3_eleven_empty_split)
strengthens the full three-versus-eight branch: **at least two fixed
vertices are blue to all nine minority vertices**. Each of the two cores
is split into exactly one versus at least two empty signatures. Both
exactly-one cases have full refutations replayed twice; both other cases
return UNKNOWN. This strengthening now has an
[accepted independent review](../ramsey_r55_order3_eleven_empty_split_review1),
keeps both cores open, and leaves the minimum moving count at eleven.
The subsequent [empty-pair lemma](../ramsey_r55_order3_eleven_empty_pair)
says that a blue edge between two empty-signature fixed vertices has at
most two common blue fixed neighbors. Each is red to at least two
minority triangles, and two cannot omit the same triangle. The bound has
sharp 13-vertex witnesses; a 14-vertex red-pair example shows the color
hypothesis is necessary. All four full pair-color extensions remain
UNKNOWN. The new lemma and clause bridge await independent review.
In the four-versus-seven branch, the new
[four-triangle core classification](../ramsey_r55_order3_eleven_four_core)
gives a complete cover by **197 action classes**, containing all 115543
locally valid labeled cores. Each representative fits the existing
full-graph normalization and has eighteen checked primary units.
This complete cover and its full-parent normalization now have an
[accepted independent review](../ramsey_r55_order3_eleven_blue_k4_exclusion_review1).
The later results below prune its full extensions; the branch remains open.
The subsequent [fixed-vertex theorem](../ramsey_r55_order3_eleven_four_fixed)
constructs four valid 22-vertex extensions for every core, so the core
plus ten uniform fixed vertices cannot eliminate any of these cases.
For the 118 cores containing a blue K4, ten is the sharp maximum:
the signatures are exactly the four singletons and six pairs, each
once. All fixed edges are forced except the three complementary-pair
edges, of which at most one may be blue. These four choices are all
valid. The other 79 cores have the same constructions but their other
fixed extensions are not classified. This new local theorem awaits
independent review; it supplies no full-formula or full-extension verdict.
The subsequent [full-extension incidence obstruction](../ramsey_r55_order3_eleven_blue_k4_exclusion)
now excludes **all 118 cores containing a blue K4**, leaving **79**
four-versus-seven classes. Each blue moving triangle can be blue to
at most one pair-signature fixed vertex, so seven triangles supply
at most seven incidences. The six pair vertices each need at least
two such incidences to keep their red degrees at most 24, requiring
at least twelve. This hand proof uses the full moving remainder and
R(4,5)=25; its exact thirteen-row certificate sums to `0 >= 5`.
This exclusion now has the same accepted independent review, including
the complete core cover and its full-parent normalization.
The subsequent [bounded full-extension sweep](../ramsey_r55_order3_eleven_residual_sweep)
tests all 79 remaining classes with the entire 43-vertex parent and exactly
eighteen core units. It refutes **34 additional classes**, leaving **45**
open four-versus-seven classes. All 34 full DRAT proofs pass replay and
are replayed again after fresh reconstruction of all 79 complete formulas.
Thus 152 of the original 197 classes are excluded; 85,789 of the original
115,543 locally valid labeled cores are covered. The new refutations await
independent review. Every remaining case returned UNKNOWN at the fixed
ten-second solver limit, and both three-versus-eight cores remain open.
The global minimum moving count stays eleven.
The subsequent [empty-signature theorem](../ramsey_r55_order3_eleven_empty_signature)
uses a weaker hypothesis than a core blue K4: if every complementary
three-triangle core has a blue triangle, a full extension must have a
fixed vertex blue to all four red triangles. Eleven of the 45 open cores
satisfy this hypothesis. Four necessary first-row units strengthen their
complete formulas, giving **seven further refutations** and leaving
**38 four-versus-seven classes** open. The four tested survivors
131,139,162,173 inherit the empty-signature requirement; the other 34
classes were not retested. The new hand theorem, unit bridge and
computational exclusions await independent review. The three-versus-eight
branch and minimum moving count eleven are unchanged.
The subsequent [complete empty-multiplicity split](../ramsey_r55_order3_eleven_four_empty_split)
refutes both exactly-one and at-least-two-empty branches of cores
131,139,162,173. All eight full formulas have proofs replayed twice after
fresh complete reconstruction. Thus **34 four-versus-seven classes**
remain open; 163 of the original 197 classes are excluded. Every remaining
core has a complementary three-triangle subcore with no blue triangle.
The new split and computational closure await independent review, as does
the inherited empty-signature theorem. No full eleven-cycle exclusion or
new Ramsey lower bound follows.
The last order-five type
`1^3 5^8` is excluded by the two certified full-extension formulas in
[`ramsey_r55_no_order5_automorphism`](../ramsey_r55_no_order5_automorphism),
using the analytic two-pattern incidence reduction.

Equivalently, `Aut(G)` has no element of prime order at least five. A target
cannot be vertex-transitive.

For the **M=214 hard branch only**, the degree sequence `20^13 21^30`
and its two-unit exceptional-incidence budget additionally force an
order-three element to have at most twelve moving 3-cycles. Together
with the global minimum, only eleven or twelve remain in this
branch. The solver-free lemma and sharp degree/incidence fixture are in
[`ramsey_r55_m214_symmetry_audit`](../ramsey_r55_m214_symmetry_audit).
The fixture contains an independent five-set. The upper bound is
conditional on the branch; thirteen and fourteen moving cycles remain
open for the full Ramsey problem.
The earlier C3-square classification already excluded order-nine subgroups
in this branch: both then-open global types have an element with fourteen
moving 3-cycles. The final two-action closure now gives **b<=1 globally**.
Neither the branch corollary nor its global strengthening changes the
hard-branch profile count.
The standalone M=214 degree/incidence lemma and its explicitly conditional
Ramsey corollary now have an accepted
[independent review](../ramsey_r55_m214_symmetry_review1).

These are necessary conditions, not a construction and not an improvement
to the known lower bound for `R(5,5)`.

## Durable inputs

| exclusion | coverage and evidence | artifact |
|---|---|---|
| one vertex cycle | exhaustive classification of all `2^21` circulant colorings; every one has a monochromatic `K_5` | [`ramsey_r55_circulant43_classification`](../ramsey_r55_circulant43_classification) |
| exactly two vertex cycles | degree reduction to `19+24`, `20+23`, and `21+22`, followed by exact objective classifications | [`ramsey_r55_two_cycle_automorphism_obstruction`](../ramsey_r55_two_cycle_automorphism_obstruction) |
| exactly three vertex cycles | all 154 types: 79 exact degree obstructions and 75 independently replayed UNSAT certificates | [`ramsey_r55_three_cycle_low_orbit_obstruction`](../ramsey_r55_three_cycle_low_orbit_obstruction) |
| exactly four vertex cycles | all 588 types: 185 exact degree obstructions and 403 independently replayed UNSAT certificates | [`ramsey_r55_four_cycle_minimal_orbit_obstruction`](../ramsey_r55_four_cycle_minimal_orbit_obstruction) |
| four middle order-five types | `1^13 5^6`, `1^18 5^5`, `1^23 5^4`, and `1^28 5^3`; exact formula checks and replayed DRAT certificates | [`ramsey_r55_order5_middle_obstruction`](../ramsey_r55_order5_middle_obstruction) |
| degree-strengthened order-five type | `1^33 5^2`; exact multiplicity-expanded degree networks, independent formula reconstruction, and a replayed DRAT certificate | [`ramsey_r55_order5_f33_degree_obstruction`](../ramsey_r55_order5_f33_degree_obstruction) |
| analytic order-five type | `1^38 5`; the moving orbit is a two-colored `C_5`, and `R(4,5)=25` plus `R(3,5)=14` gives the contradiction `16 <= |Y| <= 13` | [`ramsey_r55_order5_f38_analytic_obstruction`](../ramsey_r55_order5_f38_analytic_obstruction) |
| external fixed-eight order-five exclusion | `1^8 5^7`; the wustep/maths q4 certificate is independently reconstructed from all five-sets and truth-table gate clauses, then replayed | [`ramsey_r55_order5_f8_external_reproduction`](../ramsey_r55_order5_f8_external_reproduction) |
| final order-five type | `1^3 5^8`; both analytic incidence patterns have 148-variable full Ramsey formulas, independent orbit/clause reconstruction, and replayed DRAT proofs | [`ramsey_r55_no_order5_automorphism`](../ramsey_r55_no_order5_automorphism) |
| sparse involutions and order-three elements | involutions with one through four transpositions and order-three elements with one through six 3-cycles; analytic local-neighborhood bounds | [`ramsey_r55_sparse_order2_order3_automorphism_obstruction`](../ramsey_r55_sparse_order2_order3_automorphism_obstruction) |
| seven moving 3-cycles | `1^22 3^7`; degree equality reduces the moving graph to a cyclic matching cover of `K_7`, excluded by complete enumeration and a compact 191-addition RUP certificate | [`ramsey_r55_order3_seven_cycle_obstruction`](../ramsey_r55_order3_seven_cycle_obstruction) |
| eight moving 3-cycles | `1^19 3^8`; a local deficit budget and five complete normalized formulas, with full orbit/clause reconstruction and 4,088 committed RUP additions | [`ramsey_r55_order3_eight_cycle_obstruction`](../ramsey_r55_order3_eight_cycle_obstruction) |
| nine moving 3-cycles | `1^16 3^9`; deficit budget four with the retained complete-block cap, five fully reconstructed formulas, and regenerated/replayed DRAT certificates | [`ramsey_r55_order3_nine_cycle_obstruction`](../ramsey_r55_order3_nine_cycle_obstruction) |
| ten moving 3-cycles, partial | `1^13 3^10`; explicit fixed-vertex degree bounds and five checked DRAT proofs exclude internal red counts 0,1,2,3,5; only the four-versus-six split remains open | [`ramsey_r55_order3_ten_cycle_obstruction`](../ramsey_r55_order3_ten_cycle_obstruction) |
| minority matching at ten cycles | 94 checked anchor-profile exclusions leave four rows; the four minority triangles have weight-one blocks forming a perfect matching and induce a 7-regular graph in their internal color | [`ramsey_r55_order3_ten_cycle_anchor_sweep`](../ramsey_r55_order3_ten_cycle_anchor_sweep) |
| unique minority core at ten cycles | 27 normalized phase triples form six classes; twenty published small DRAT certificates exclude five classes, forcing one 12-vertex core with triangle-free complement; four extensions stay open | [`ramsey_r55_order3_ten_cycle_phase_sweep`](../ramsey_r55_order3_ten_cycle_phase_sweep) |
| fixed signatures at ten cycles | at most ten fixed vertices have nonempty minority-color signatures, so at least three are empty; equality has all ten nonempty signatures once; a 25-vertex fixture is locally sharp and 1,868 vectors meet the forced-blue clique constraints | [`ramsey_r55_order3_fixed_signature_bound`](../ramsey_r55_order3_fixed_signature_bound) |
| final ten-cycle extensions | twelve reviewed signature-consequence units in each of the four remaining full formulas; four UNSAT proofs replayed, closing the type under the inherited reductions; large proof traces regenerated outside Git | [`ramsey_r55_order3_ten_cycle_signature_propagation`](../ramsey_r55_order3_ten_cycle_signature_propagation) |
| eleven moving 3-cycles, partial | complete formulas and checked DRAT proofs exclude normalized internal red counts 0,1,2,5; only three-versus-eight and four-versus-seven remain open, with the minimum moving count unchanged | [`ramsey_r55_order3_eleven_cycle_obstruction`](../ramsey_r55_order3_eleven_cycle_obstruction) |
| three minority triangles at eleven cycles | fourteen normalizer classes cover all 343 labeled cores; eleven full-extension refutations leave three explicit nine-vertex cores, containing 54 labeled forms; all three extensions remain open | [`ramsey_r55_order3_eleven_minority_core`](../ramsey_r55_order3_eleven_minority_core) |
| signatures at eleven cycles | at most nine uniform vertices have nonempty red signatures to three red triangles; sharp equality fixes multiplicities; 1623 primary consequences exclude core 8 and leave cores 11,13 open | [`ramsey_r55_order3_eleven_signature_bound`](../ramsey_r55_order3_eleven_signature_bound) |
| equality excluded at eleven cycles | full extensions of both residual three-versus-eight cores with exactly one empty fixed signature are refuted; at least two fixed signatures must be empty; both residual cores remain open | [`ramsey_r55_order3_eleven_empty_split`](../ramsey_r55_order3_eleven_empty_split) |
| empty blue pair at eleven cycles | at most two common blue fixed neighbors, each red to at least two minority triangles; sharp local witnesses and exact primary consequences; all four core/pair-color extension cases remain UNKNOWN | [`ramsey_r55_order3_eleven_empty_pair`](../ramsey_r55_order3_eleven_empty_pair) |
| four minority triangles at eleven cycles | 108 local red-K5 obstructions leave 115543 labeled cores, partitioned into 197 normalizer classes with compatible full-graph representatives and eighteen checked primary units; no extension verdict | [`ramsey_r55_order3_eleven_four_core`](../ramsey_r55_order3_eleven_four_core) |
| ten uniform fixed vertices on four minority triangles | all 197 cores have four explicit valid 22-vertex extensions; for 118 blue-K4 cores, ten is maximum and all equality extensions have singleton/pair signatures and exactly those four edge patterns; no full 43-vertex verdict | [`ramsey_r55_order3_eleven_four_fixed`](../ramsey_r55_order3_eleven_four_fixed) |
| full seven-blue-triangle incidence obstruction | blue-K4 minority cores require at least 12 fixed-pair/blue-triangle incidences but permit at most 7; excludes 118 of 197 full core classes, leaving 79, by a hand proof and exact row-sum certificate | [`ramsey_r55_order3_eleven_blue_k4_exclusion`](../ramsey_r55_order3_eleven_blue_k4_exclusion) |
| residual four-versus-seven full-extension sweep | all 79 complete 43-vertex formulas audited; 34 new refutations replayed twice, leaving 45 explicit UNKNOWN cases; 152 of 197 total core classes excluded | [`ramsey_r55_order3_eleven_residual_sweep`](../ramsey_r55_order3_eleven_residual_sweep) |
| four-triangle empty-signature propagation | blue triangles in all four complementary triples force an empty fixed signature; eleven selected complete formulas yield seven further replayed refutations, leaving 38 total core classes open | [`ramsey_r55_order3_eleven_empty_signature`](../ramsey_r55_order3_eleven_empty_signature) |
| complete four-core empty-multiplicity split | exactly one versus at least two empty signatures; eight complete refutations close cores 131,139,162,173, leaving 34 core classes; every survivor has a blue-triangle-free complementary triple | [`ramsey_r55_order3_eleven_four_empty_split`](../ramsey_r55_order3_eleven_four_empty_split) |
| C3-square actions and order 27 | sixteen of eighteen actions excluded; the two open types have one fixed point, two three-orbits and four regular nine-orbits; an index-three stabilizer argument excludes order-27 subgroups globally and order-nine subgroups in M=214 | [`ramsey_r55_c3_square_action_sweep`](../ramsey_r55_c3_square_action_sweep) |
| complete C3-square closure | both remaining actions excluded after proven centralizer normalization, with fresh full formula reconstruction and DRAT replay; nine does not divide the automorphism-group order globally | [`ramsey_r55_c3_square_normalized_extensions`](../ramsey_r55_c3_square_normalized_extensions) |
| subgroups of order 25 | the surviving order-five types force a unique `C_5^2` action, whose 51-variable invariant formula is certified UNSAT; an order-25 element is excluded by its fifth power | [`ramsey_r55_c5_square_automorphism_obstruction`](../ramsey_r55_c5_square_automorphism_obstruction) |
| order-15 elements | power constraints leave six cycle types; all six exact cyclic invariant formulas have independently reconstructed clauses and replayed DRAT certificates | [`ramsey_r55_order15_automorphism_obstruction`](../ramsey_r55_order15_automorphism_obstruction) |
| order-nine elements | nine types surviving the earlier cubing bounds; seven earlier certificates and two centralizer-normalized certified formulas exclude all nine | [`ramsey_r55_order9_automorphism_obstruction`](../ramsey_r55_order9_automorphism_obstruction) |
| order-seven elements | all six types `1^f 7^k`, where `f+7k=43`; exact formula checks and replayed certificates | [`ramsey_r55_no_order7_automorphism`](../ramsey_r55_no_order7_automorphism) |
| order-eleven elements | all three types `1^f 11^k`, where `f+11k=43`; exact formula checks and independently replayed RUP certificates | [`ramsey_r55_order11_automorphism_search`](../ramsey_r55_order11_automorphism_search) |
| orders 13, 17, 19, and 23 | all eight types `1^f p^k`, where `f+pk=43`; exact formula checks and independently replayed RUP/DRAT certificates | [`ramsey_r55_medium_prime_automorphism_search`](../ramsey_r55_medium_prime_automorphism_search) |
| long cycles | a fixed point cannot coexist with a cycle of length at least 25; prime cycles of lengths 29, 31, 37, and 41 are excluded analytically | [`ramsey_r55_automorphism_long_cycle_obstruction`](../ramsey_r55_automorphism_long_cycle_obstruction) |

The ten-cycle rows record the stages of the proof. Their intermediate open
cases are superseded by the final signature-propagation row. The intermediate
C3-square open types are superseded by the complete C3-square closure row.

The prime-order theorems are disjoint from the two-, three-, and four-cycle
theorems: every type newly used in the prime-divisor conclusion has at least
five vertex cycles. The older `1+21+21` obstruction is now subsumed by the
complete three-cycle theorem and is not counted as an additional exclusion.

Certificate compactness differs across inputs.  The two-, three-, and
four-cycle artifacts and the order-eleven artifact retain independently
checkable enumeration or RUP evidence.  The complete order-seven theorem
combines four compact standalone
DRAT proofs with sibling results for one and eight fixed points.  Its
one-fixed-point artifact omits a 1.304 GB proof tree under the repository's
compact-artifact policy, but retains all leaf assignments and hashes and
records that every leaf was replayed on the research host.  Users requiring
a wholly compact standalone trust boundary should preserve that caveat.
The five computational order-five certificates are compact and independently
replayable; the sixth exclusion is analytic. The external fixed-eight
certificate is independently reconstructed and replayed by a package that
downloads pinned source and proof bytes. The analytic incidence reduction
for the last type `1^3 5^8` leaves the column
multisets `0,1,2,3,5,5,6,6` and `0,1,2,3,4,5,6,7`, with red fixed-neighbor
bit weights `x=1,y=2,z=4`, with `xy` red and `xz,yz` blue.
Both pass every local test using the fixed vertices and two moving cycles;
their full extensions are now both certified UNSAT. The final package
regenerates the two formulas and traces outside Git, independently
reconstructs every clause, and replays the proofs. Its reference traces
are 257,320 and 4,415,625 bytes; only source and compact evidence are committed.
The complete order-five theorem, including all eight cycle types, now has
an independently reconstructed and replayed review in
[`ramsey_r55_no_order5_automorphism_review3`](../ramsey_r55_no_order5_automorphism_review3).
The seven-3-cycle exclusion has no omitted certificate: its 3,125-byte RUP
trace is committed, and its separate direct enumeration covers all
`3^15` normalized matching assignments. Verification requires no solver.
The eight-3-cycle package also needs no solver: five committed clause
subsets and their addition-only RUP traces total 269,427 bytes. Each core
clause is checked against a completely reconstructed 43-vertex formula.
Its complete minimum-nine dependency chain has now been independently
accepted in
[`ramsey_r55_order3_eight_cycle_review1`](../ramsey_r55_order3_eight_cycle_review1).
The nine-3-cycle package regenerates five general DRAT traces totaling
81,986,115 bytes outside Git. All five fresh traces match the reference
hashes and pass independent replay; the large formulas and proofs are not
committed. Solver and checker sources, generators and exact commands are pinned.
The nine-cycle theorem and its dependency chain now have an accepted
independent review in
[`ramsey_r55_order3_nine_cycle_review1`](../ramsey_r55_order3_nine_cycle_review1).
The ten-cycle package also regenerates large general DRAT traces outside
Git. Its independent complete-clause reconstruction covers all six formulas;
proof replay excluded five cases and initially left the four-versus-six
case unresolved. The subsequent signature-propagation artifact closes that
case. The older five-case split now has an accepted independent review;
the final four-case closure has also been independently accepted in
[`ramsey_r55_order3_ten_cycle_signature_propagation_review1`](../ramsey_r55_order3_ten_cycle_signature_propagation_review1).
The fixed-33 package has also been independently
regenerated, reconstructed, and replayed in
[`ramsey_r55_order5_f33_degree_obstruction_review1`](../ramsey_r55_order5_f33_degree_obstruction_review1).
The order-25 finite obstruction has a separate clean-room action, formula,
and RUP replay in
[`ramsey_r55_c5_square_automorphism_review1`](../ramsey_r55_c5_square_automorphism_review1).

## How to use the handoff

For a proposed symmetry group `H <= S_43`, compute the vertex-cycle
partition of every nonidentity element (or enough powers and conjugacy-class
representatives to cover the group).  Reject the construction family if:

1. an element has at most four vertex cycles;
2. an involution has fewer than five transpositions;
3. an order-three element has fewer than eleven 3-cycles;
4. an element has order divisible by five, or a vertex cycle of length
   divisible by five;
5. an element has prime order at least seven;
6. an element contains a cycle of prime length 29, 31, 37, 41, or 43; or
7. an element fixes a vertex and also contains a cycle of length at least 25; or
8. the proposed group order is divisible by five; or
9. an element has order divisible by nine, or a vertex cycle with length
    divisible by nine; or
10. the proposed group order is divisible by nine.

For a cyclic ansatz generated by `g`, testing only the cycle type of `g` is
insufficient: invariance under `g` also gives invariance under every power of
`g`, and a proper power may fall into a forbidden family.

For an invariant candidate coloring with an order-three automorphism having
exactly eleven moving triangles, additionally reject internal assignments
whose minority count is 0,1,2 or 5. Only counts 3 and 4 survive the complete
six-count sweep. This prunes internal color assignments, rather than the
whole eleven-cycle permutation type.
For minority count three, the core may now be screened by the complete
normalizer invariant. Its sorted red cross weights and distinguished-phase
sum must be (1,2,2) with zero sum or (2,2,2) with nonzero sum.
The three-core artifact defines the phase convention and compatible
full-graph relabelings; signature propagation supplies the additional
exclusion of (1,1,1) with zero sum. Both refinements now have accepted
independent reviews.
For each, at least two fixed vertices must be blue to all three minority
triangles. The exactly-one case would have two copies of each singleton
and one of each pair; both full equality extensions are newly refuted.
This last strengthening now has an accepted independent review. The full
extensions with at least two empty signatures are still unresolved.
If two empty-signature fixed vertices have a blue edge, at most two other
fixed vertices can be blue to both; each common blue neighbor has at
least two red minority incidences. No two common blue neighbors can
both be blue to the same minority triangle. This new conditional screen
has a hand proof and sharp local examples; the full pair-color sweep
excluded no additional case.
For minority count four, the complete 197-class catalog supplies the
corresponding normalizer cover. A core must avoid every complete block
and each of the 108 listed occupancy obstructions; its compatible
representative then determines eighteen primary bits. No full extension
is excluded solely by membership in this catalog.
For each of the 118 cores having a blue K4, a full candidate's ten
fixed vertices must realize every singleton and pair signature exactly
once. Intersecting signatures have blue edges; disjoint signatures
have red edges except at most one complementary-pair edge. All four
patterns really extend the local core. Fixture labels must be reconciled
with the parent's full eleven-bit fixed-row ordering before imposing
units. The remaining 79 cores also admit these local constructions.
Further pruning therefore needs the other moving triangles or other
full-graph information; no core is excluded by the fixed-only relaxation.
Using all seven blue moving triangles now excludes the 118 blue-K4
cores by the twelve-versus-seven incidence contradiction. A remaining
four-versus-seven core must therefore be one of the 79 catalog entries
with no blue K4. The hand exclusion and complete marked-action cover are
now independently accepted. The subsequent full-parent sweep excludes 34
of those 79 entries, so the compatible core must lie in the **45 open
indices** listed in
[the result manifest](../ramsey_r55_order3_eleven_residual_sweep/result.json).
These new computational exclusions have full replay and fresh formula
reconstruction but await independent review. Four-versus-seven indices
11 and 13 excluded there are unrelated to the two open three-versus-eight
cores with the same numeric indices in a different catalog.
The subsequent empty-signature theorem supplies four necessary first-row
units for the eleven cores whose every complementary triple has a blue
triangle. The new full tests refute 87,101,110,112,120,121,147. The four
tested survivors 131,139,162,173 must have an empty signature, and the
other 34 previously open classes are unchanged. The current exact list
of **38** open classes is in
[the new boundary manifest](../ramsey_r55_order3_eleven_empty_signature/boundary.json).
The new theorem and computational exclusions await independent review.
The complete one-empty/multiple-empty split then refutes both branches of
all four tested survivors. The current exact list is now **34** classes,
listed in [the latest boundary manifest](../ramsey_r55_order3_eleven_four_empty_split/boundary.json).
In each, at least one complementary three-triangle subcore has no blue
triangle. This new full-core closure and its inherited empty-signature
premise await independent review. Do not replace the fourth red triangle
by a blue triangle when using the nine-vertex subcore as an anchor.

The finished ten-cycle chain proceeded through the four-versus-six
internal-color split, 94 of 98 anchor exclusions, and twenty further
phase exclusions. The remaining minority core has words 01=23=100 and
02=03=12=13=110, with coordinate differences interpreted as in the
literal core artifact. The matching and phase refinements have accepted
independent reviews; their formerly unreviewed internal-color antecedent
has now been independently accepted as well.

Writing X for singleton fixed-signature multiplicities and Y for pair
multiplicities gives X+2Y<=16 and 3X+2Y<=24. Thus at least three fixed
vertices are opposite-color complete to the core. Equality forces every
singleton and pair signature once. This lemma, its 1,868 necessary
count vectors, and its locally sharp 25-vertex fixture now have an
[accepted independent review](../ramsey_r55_order3_fixed_signature_bound_review1).
The fixture itself supplies no extension by six majority triangles.

In the inherited fixed-row lexicographic normalization, the first three
fixed vertices therefore have empty minority signatures. Twelve necessary
primary unit clauses enforce this. The four full formulas retain every
parent degree counter and all five-set constraints. All four returned
UNSAT within 120 seconds per solve and passed DRAT replay, so the
formerly open ten-cycle type is closed under the inherited reductions.
The new formula generators, layer checker, certificate extraction and
support checker, hashes and reports are public; large generated proof
traces remain outside Git and must be regenerated for independent replay.
This is a completed symmetry restriction, not a target coloring.

This materially prunes symmetry-first construction search. Any proposed
group whose order has a prime divisor at least five is impossible; a
surviving nontrivial action has order `2^a 3^b`, with b<=1 globally,
and must satisfy the
element-wise cycle restrictions above. Such
actions generally retain more edge orbits and therefore less of the
dimensional advantage sought from a highly structured ansatz. The handoff
does not prune an asymmetric local search and does not prove that a target,
if it exists, must be asymmetric.

## Logical derivation

The one-cycle case is a 43-cycle and hence circulant after relabeling.  The
next three rows exclude elements with exactly two, three, or four cycles, so
every remaining nonidentity automorphism has at least five cycles. The three
order-five artifacts close six of the eight types allowed by `f+5k=43`.
The external q4 certificate closes a seventh, `1^8 5^7`: the fixed-vertex
degree equation leaves neighbor-cycle counts three and four, complementation
reduces to three, and its anchored invariant CNF is independently
reconstructed and its DRAT proof replayed. For the final type `1^3 5^8`,
the mixed common-neighborhood cap and row sums leave two incidence
patterns. Their 148-variable full Ramsey formulas are independently
reconstructed and refuted by replayed DRAT proofs. The first needs no
further normalization; the second uses a global coordinate multiplier
and independent rotations to minimize seven anchor words. All eight
order-five types are therefore excluded, so Cauchy's theorem gives
`5` not dividing the automorphism-group order.
The sparse-motion theorem separately bounds the numbers of transpositions
and 3-cycles by using monochromatic common-neighborhood caps; its ten types
have many vertex cycles and are not consequences of the low-cycle rows.
The additional type `1^22 3^7` attains equality in the sparse color-degree
bound. Every moving triangle then has degree 18 in its own color, and two
neighbors in each other moving cycle in that color. Opposite-colored
triangles are incompatible. All moving triangles therefore share a color,
and every opposite-color cross block is a perfect matching. Independent
phase changes leave a cyclic threefold matching cover of `K_7` with 15
free ternary shifts. Complete prefix enumeration covers all 14,348,907
assignments without a survivor, and a separately reconstructed 45-variable
formula has a 191-addition RUP refutation. This gives a minimum of eight
moving cycles. The next type `1^19 3^8` has a local deficit budget of two:
each cross block with own-color weight `w` costs `2-w+3*[w=3]`. A separate
24-vertex fixture shows that the moving-vertex condition alone is insufficient.
The full 43-vertex formulas cover all five internal-color counts up to
complementation. Verified small clause subsets have 4,088 RUP additions
through the empty clause. This raises the current minimum to **nine**
moving 3-cycles. At the next type `1^16 3^9`, the deficit budget is four,
but at most one complete own-color block is still allowed. Retaining the
common-neighborhood cap gives 987 local arithmetic profiles; the budget
alone admits 28 impossible profiles with two complete blocks. The five
full internal-color cases have audited DRAT refutations. This raises the
current minimum to **ten** moving 3-cycles, leaving ten through fourteen
as possible moving counts. At `1^13 3^10`, the analogous deficit bound is
six, with the complete-block cap still necessary. There are 10,679 local
arithmetic profiles; the deficit budget alone admits 1,380 impossible
weight vectors. Explicit degree counters at all thirteen fixed vertices
strengthen the full formulas. Five verified internal-color cases leave
only four triangles of one color and six of the other. The later matching
and phase reductions leave four full extensions of one minority core. The
reviewed fixed-signature bound then forces twelve primary units in the
fixed-row normalization. Their four reconstructed formulas all have
replayed DRAT refutations. Combining this final step with the inherited
chain excludes the entire ten-cycle type and raises the minimum to eleven.
At eleven cycles, the local deficit budget is eight, but the full degree
upper bound becomes active: max(0,D-4-3m)<=a<=min(10,4-3m,D+2-3m).
The complete six-count formulas enforce both moving degree bounds, all
fixed degrees, the common-neighbor cap, and justified centralizer ordering.
Independent full-clause reconstruction and replayed DRAT proofs exclude
r=0,1,2,5. The remaining r=3,4 cases reached their 180-second limits, so
three-versus-eight and four-versus-seven stay open. The minimum stays eleven.
The exact local census has 80,726 arithmetic profiles; without the upper
degree constraint twelve additional profiles would be incorrectly admitted.
The parent eleven-cycle split reduction now has an accepted independent
review. Within its three-versus-eight split, three noncomplete minority
cross words give 343 labeled nine-vertex cores. Their unordered weights
and zero/nonzero distinguished-phase sum classify fourteen normalizer
orbits. Eleven full-extension refutations leave only words 100,100,100;
100,110,110; or 110,110,101, on pairs 01,02,12. The three cubes returned
UNKNOWN at 60 seconds. This core restriction now has an accepted
independent review; the minimum moving count remains eleven.
The later three-triangle uniform-signature lemma gives I<=12 and X<=6,
where I counts fixed red incidences and X singleton signatures. With Z
triple signatures, twice the nonempty count is I+X-Z<=18. Thus at most
nine fixed vertices have nonempty signatures, forcing at least one empty
among ten. Equality uniquely fixes all nonempty multiplicities. The three
forced first-row bits and 1620 proved signature cuts give a full replayed
refutation of core8. Cores11 and13 remain UNKNOWN, and the four-versus-seven
split is unchanged. The bound is locally sharp on 19-vertex witnesses;
the lemma and full-extension exclusion now have an accepted independent
review. The subsequent complete four-case split into exactly one versus
at least two empty signatures refutes both equality branches. Each uses
27 further incidence units and a full proof replayed twice. Thus at least
two fixed vertices are blue to the minority core; both remaining cores
with that restriction return UNKNOWN. This strengthening now has an
accepted independent review. The next bounded pair-color sweep adds the
sharp common-blue-neighbor lemma in the blue branches and splits each
core by the first empty pair's edge. All four final cases are UNKNOWN;
the new hand lemma and its clause bridge await independent review.
The earlier order-25 theorem uses the then-surviving fixed counts three and eight to
classify any `C_5^2` action as `1^3 5^3 25^1`; its exact invariant formula is
UNSAT. A cyclic subgroup of order 25 is excluded because the fifth power of
its generator has five 5-cycles, rather than the required seven or eight.
Every group whose order is divisible by 25 contains a subgroup of order 25,
so these two cases gave the earlier 5-adic restriction, now subsumed by
the complete order-five theorem.
For an order-15 element, its cube and fifth power reduce the possible cycle
types to six; their 67--99-variable cyclic formulas are all certified UNSAT.
This separate historical exclusion is likewise subsumed by absence of
order-five elements.
For the earlier order-nine proof, cubing and the then-known sparse
order-three bound left nine types.
Seven earlier certificates exclude seven of them. Sorting internal cycle
profiles and independently minimizing the cross words to one anchor cycle
gives valid centralizer normalizations for the last two. Their exact formulas
are independently reconstructed and their DRAT proofs replayed. All nine
types are therefore excluded. Every element of order divisible by nine has
a power of order nine, so every nontrivial 3-subgroup has exponent three.
The two new generated traces are omitted from Git; the artifact regenerates
and independently replays both, with reference hashes and pinned tools.
The C3-square classification uses the minimum-eleven motion bound to
limit each nonidentity element to at most ten fixed vertices. Write a for
global fixed points, b_L for three-orbits stabilized by each of four lines,
and c for regular nine-orbits. The equations a+3sum(b_L)+9c=43 and
a+3b_L<=10 leave eighteen actions up to GL(2,3), whose projective action is
S4. Full invariant Ramsey formulas and replayed proofs exclude sixteen.
The two remaining actions both have exactly one global fixed point.
If a subgroup P of order27 existed, its index-three subgroups would all
be C3-square and normal. The unique fixed point of one is fixed by P,
and an orbit of size3 would give its stabilizer at least three fixed
points. Thus P has one fixed point and all remaining orbits divisible
by9, contradicting 43-1=42. This proves the new global restriction
27 not dividing the group order. Each residual C3-square action contains
an element with fourteen moving triangles, contradicting the M=214-specific
upper bound. That branch consequently excludes order-nine subgroups.
The subsequent [centralizer-normalized closure](../ramsey_r55_c3_square_normalized_extensions)
excludes both final actions. Sort the four regular copies by their five-bit
fixed-edge/internal-direction profiles, then independently minimize the
three regular and two quotient anchor words under translations. These
centralizer relabelings preserve the parent complement unit. Each complete
formula adds 2,840 primary normalization clauses; both have reconstructed
bases and tails and replayed DRAT refutations. This excludes C3-square
subgroups globally. A group of order nine is cyclic or C3-square, so the
reviewed cyclic exclusion now gives nine not dividing the automorphism-group
order globally. Both the parent action classification/sixteen exclusions and
the final two-case closure now have accepted independent reviews.
An order-seven permutation on 43 points has one of the six displayed
fixed-point/seven-cycle types, all covered by the order-seven artifact; the
analogous equation for order eleven gives three types, all covered by the
order-eleven artifact. The eight order-13, -17, -19, and -23 types are
covered by the medium-prime artifact. The prime-cycle restrictions are the
analytic long-cycle theorem plus the 43-cycle classification. These exhaust
the primes from 7 through 43. Finally, Cauchy's theorem converts absence of
an element of each listed prime order into the stated restriction on
`|Aut(G)|`.
