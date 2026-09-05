# Automorphism exclusion handoff for Ramsey `(5,5,43)` search

Let `G` be a hypothetical graph on 43 vertices with neither a clique nor an
independent set of order five.  The currently certified symmetry results in
this repository imply the following reusable group-screening rule:

> Every nonidentity element of `Aut(G)` has at least five vertex cycles, and
> every prime divisor of `|Aut(G)|` is `2` or `3`.

In particular, `|Aut(G)|=2^a 3^b`. There is no element of order five;
the earlier order-25 and order-15 restrictions are now subsumed by this.
There is no element of order nine. Every nontrivial 3-subgroup has exponent
three; this does not bound its order by three or imply it is abelian.

More specifically, every involution has at least five transpositions, every
order-three element has at least ten 3-cycles (and at most 13 fixed
vertices). If it has exactly ten, the moving triangles have internal
colors split four versus six; all five other counts up to complementation
are excluded. In the remaining four-versus-six case, the four minority
triangles are paired by cross blocks of own-color weight one; their other
mutual blocks have weight two. Every minority triangle has mixed weights
one or two, with one through four weights equal to one. The four anchor
profiles remain open; 94 of the former 98 have checked exclusions in
[`ramsey_r55_order3_ten_cycle_anchor_sweep`](../ramsey_r55_order3_ten_cycle_anchor_sweep).
Their phases are now forced as well: the twelve minority vertices induce
the single explicit core in
[`ramsey_r55_order3_ten_cycle_phase_sweep`](../ramsey_r55_order3_ten_cycle_phase_sweep).
It is 7-regular in their internal color and triangle-free in the other.
Each fixed vertex is adjacent in the minority color to at most two whole
minority triangles. Twenty compact certificates exclude the other five
phase classes; the four anchor extensions of the remaining core stay open.
At least three of the thirteen fixed vertices are adjacent to none of the
minority core in that color. If exactly three are, the four singleton and
six pair signatures each occur once. The hand proof and sharp local
25-vertex fixture are in
[`ramsey_r55_order3_fixed_signature_bound`](../ramsey_r55_order3_fixed_signature_bound).
The whole ten-cycle type remains open. The last order-five type
`1^3 5^8` is excluded by the two certified full-extension formulas in
[`ramsey_r55_no_order5_automorphism`](../ramsey_r55_no_order5_automorphism),
using the analytic two-pattern incidence reduction.

Equivalently, `Aut(G)` has no element of prime order at least five. A target
cannot be vertex-transitive.

For the **M=214 hard branch only**, the degree sequence `20^13 21^30`
and its two-unit exceptional-incidence budget additionally force an
order-three element to have at most twelve moving 3-cycles. Together
with the global minimum, only ten, eleven, or twelve remain in this
branch. The solver-free lemma and sharp degree/incidence fixture are in
[`ramsey_r55_m214_symmetry_audit`](../ramsey_r55_m214_symmetry_audit).
The fixture contains an independent five-set. The upper bound is
conditional on the branch; thirteen and fourteen moving cycles remain
open for the full Ramsey problem.
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
| subgroups of order 25 | the surviving order-five types force a unique `C_5^2` action, whose 51-variable invariant formula is certified UNSAT; an order-25 element is excluded by its fifth power | [`ramsey_r55_c5_square_automorphism_obstruction`](../ramsey_r55_c5_square_automorphism_obstruction) |
| order-15 elements | power constraints leave six cycle types; all six exact cyclic invariant formulas have independently reconstructed clauses and replayed DRAT certificates | [`ramsey_r55_order15_automorphism_obstruction`](../ramsey_r55_order15_automorphism_obstruction) |
| order-nine elements | nine types surviving the earlier cubing bounds; seven earlier certificates and two centralizer-normalized certified formulas exclude all nine | [`ramsey_r55_order9_automorphism_obstruction`](../ramsey_r55_order9_automorphism_obstruction) |
| order-seven elements | all six types `1^f 7^k`, where `f+7k=43`; exact formula checks and replayed certificates | [`ramsey_r55_no_order7_automorphism`](../ramsey_r55_no_order7_automorphism) |
| order-eleven elements | all three types `1^f 11^k`, where `f+11k=43`; exact formula checks and independently replayed RUP certificates | [`ramsey_r55_order11_automorphism_search`](../ramsey_r55_order11_automorphism_search) |
| orders 13, 17, 19, and 23 | all eight types `1^f p^k`, where `f+pk=43`; exact formula checks and independently replayed RUP/DRAT certificates | [`ramsey_r55_medium_prime_automorphism_search`](../ramsey_r55_medium_prime_automorphism_search) |
| long cycles | a fixed point cannot coexist with a cycle of length at least 25; prime cycles of lengths 29, 31, 37, and 41 are excluded analytically | [`ramsey_r55_automorphism_long_cycle_obstruction`](../ramsey_r55_automorphism_long_cycle_obstruction) |

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
proof replay excludes five cases and explicitly leaves the four-versus-six
case unresolved. Internal checking is not new independent peer review.
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
3. an order-three element has fewer than ten 3-cycles;
4. an element has order divisible by five, or a vertex cycle of length
   divisible by five;
5. an element has prime order at least seven;
6. an element contains a cycle of prime length 29, 31, 37, 41, or 43; or
7. an element fixes a vertex and also contains a cycle of length at least 25; or
8. the proposed group order is divisible by five; or
9. an element has order divisible by nine, or a vertex cycle with length
    divisible by nine.

For a cyclic ansatz generated by `g`, testing only the cycle type of `g` is
insufficient: invariance under `g` also gives invariance under every power of
`g`, and a proper power may fall into a forbidden family.

When candidate edges are assigned to an action with exactly ten moving
3-cycles, additionally require four monochromatic moving triangles of one
color and six of the other. The remaining case has a further valid anchor
normalization with 98 cross-weight profiles, explicitly listed in the
ten-cycle package. The new anchor sweep certifies 94 exclusions and leaves
only indices 64,65,67,69. At every minority triangle, the same-color weights
are 1,2,2 and the opposite-color weights have p ones and 6-p twos for
1<=p<=4. Thus the minority weight-one blocks form a perfect matching;
their twelve vertices induce a 7-regular graph in that color and have
full-graph degree at most 22 in it. These four remaining profiles are not
graph realizations or excluded cubes. The new result's large original and
extracted DRAT traces are regenerated outside Git from source and compact
manifests, with full clause checks and replay. It has no independent peer
review of the older internal-color dependency yet. The 94-anchor
refinement itself now has an accepted
[independent review](../ramsey_r55_order3_ten_cycle_anchor_sweep_review1),
explicitly conditional on that preceding internal-color split.

The subsequent phase sweep uses the matching simultaneously at all four
minority triangles. After normalization, its only remaining core has words
01=23=100 and 02=03=12=13=110. Each word gives the three red bits from
coordinate zero of the lower-indexed triangle to the other. The core is
provided as a literal 42-edge list on twelve vertices. Its complement has
no triangle, and a fixed vertex has a minority-incidence signature of
weight at most two. All twenty new exclusion certificates are published
in full, totaling 310,309 bytes; replay requires a DRAT checker and fresh
parent reconstruction, but no SAT solver. The complete ten-cycle type
remains open. The phase refinement now has an
[accepted independent review](../ramsey_r55_order3_ten_cycle_phase_sweep_review1),
explicitly conditional on the older internal-color split.

Writing X for the number of singleton fixed signatures and Y for pair
signatures gives X+2Y<=16 and 3X+2Y<=24. Hence at most ten fixed vertices
have nonempty signatures, and at least three are opposite-color complete
to the whole minority core. Equality forces every singleton and pair
signature once. The new hand proof does not require a solver; its complete
forced-blue count-vector census leaves 1,868 necessary vectors, not graph
realizations. A literal 25-vertex core-plus-fixed graph attains equality.
No six-majority-triangle extension is supplied by that fixture, and the
signature refinement has no independent peer review yet.

This materially prunes symmetry-first construction search. Any proposed
group whose order has a prime divisor at least five is impossible; a
surviving nontrivial action has order `2^a 3^b` and must satisfy the
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
only four triangles of one color and six of the other. This does not raise
the minimum to eleven or exclude the remaining ten-cycle case.
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
An order-seven permutation on 43 points has one of the six displayed
fixed-point/seven-cycle types, all covered by the order-seven artifact; the
analogous equation for order eleven gives three types, all covered by the
order-eleven artifact. The eight order-13, -17, -19, and -23 types are
covered by the medium-prime artifact. The prime-cycle restrictions are the
analytic long-cycle theorem plus the 43-cycle classification. These exhaust
the primes from 7 through 43. Finally, Cauchy's theorem converts absence of
an element of each listed prime order into the stated restriction on
`|Aut(G)|`.
