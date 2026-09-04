# Automorphism exclusion handoff for Ramsey `(5,5,43)` search

Let `G` be a hypothetical graph on 43 vertices with neither a clique nor an
independent set of order five.  The currently certified symmetry results in
this repository imply the following reusable group-screening rule:

> Every nonidentity element of `Aut(G)` has at least five vertex cycles, and
> every prime divisor of `|Aut(G)|` is `2`, `3`, or `5`.

Moreover, `25` does not divide `|Aut(G)|`.
There is no element of order 15.
Any order-nine element must have cycle type `1^1 3^5 9^3` or `1^1 3^2 9^4`.

More specifically, every involution has at least five transpositions, every
order-three element has at least seven 3-cycles, and an order-five element
must have fixed count 3 or 8.

Equivalently, `Aut(G)` has no element of prime order at least seven. A target
cannot be vertex-transitive.

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
| sparse involutions and order-three elements | involutions with one through four transpositions and order-three elements with one through six 3-cycles; analytic local-neighborhood bounds | [`ramsey_r55_sparse_order2_order3_automorphism_obstruction`](../ramsey_r55_sparse_order2_order3_automorphism_obstruction) |
| subgroups of order 25 | the surviving order-five types force a unique `C_5^2` action, whose 51-variable invariant formula is certified UNSAT; an order-25 element is excluded by its fifth power | [`ramsey_r55_c5_square_automorphism_obstruction`](../ramsey_r55_c5_square_automorphism_obstruction) |
| order-15 elements | power constraints leave six cycle types; all six exact cyclic invariant formulas have independently reconstructed clauses and replayed DRAT certificates | [`ramsey_r55_order15_automorphism_obstruction`](../ramsey_r55_order15_automorphism_obstruction) |
| seven order-nine types | cubing first forces three or four 9-cycles; six direct formulas and one degree-strengthened formula are certified UNSAT, leaving two types | [`ramsey_r55_order9_partial_automorphism_obstruction`](../ramsey_r55_order9_partial_automorphism_obstruction) |
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
replayable; the sixth exclusion is analytic. The other two order-five cycle
types remain open. The fixed-33 package has also been independently
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
3. an order-three element has fewer than seven 3-cycles;
4. an order-five element has 13, 18, 23, 28, 33, or 38 fixed vertices;
5. an element has prime order at least seven;
6. an element contains a cycle of prime length 29, 31, 37, 41, or 43; or
7. an element fixes a vertex and also contains a cycle of length at least 25; or
8. the proposed group order is divisible by 25; or
9. an element has order 15; or
10. an order-nine element does not have type `1^1 3^5 9^3` or `1^1 3^2 9^4`.

For a cyclic ansatz generated by `g`, testing only the cycle type of `g` is
insufficient: invariance under `g` also gives invariance under every power of
`g`, and a proper power may fall into a forbidden family.

This materially prunes symmetry-first construction search. Any proposed
group whose order has a prime divisor at least seven or is divisible by 25
is impossible; a surviving nontrivial action has order `2^a 3^b 5^c` with
`c<=1` and must satisfy the element-wise cycle restrictions above. Such
actions generally retain more edge orbits and therefore less of the
dimensional advantage sought from a highly structured ansatz. The handoff
does not prune an asymmetric local search and does not prove that a target,
if it exists, must be asymmetric. An order-five element, if one exists, must
have fixed count 3 or 8.

## Logical derivation

The one-cycle case is a 43-cycle and hence circulant after relabeling.  The
next three rows exclude elements with exactly two, three, or four cycles, so
every remaining nonidentity automorphism has at least five cycles. The three
order-five artifacts close six of the eight types allowed by `f+5k=43`.
The sparse-motion theorem separately bounds the numbers of transpositions
and 3-cycles by using monochromatic common-neighborhood caps; its ten types
have many vertex cycles and are not consequences of the low-cycle rows.
The order-25 theorem then uses the surviving order-five fixed counts to
classify any `C_5^2` action as `1^3 5^3 25^1`; its exact invariant formula is
UNSAT. A cyclic subgroup of order 25 is excluded because the fifth power of
its generator has five 5-cycles, rather than the required seven or eight.
Every group whose order is divisible by 25 contains a subgroup of order 25,
so these two cases prove the 5-adic restriction.
For an order-15 element, its cube and fifth power reduce the possible cycle
types to six; their 67--99-variable cyclic formulas are all certified UNSAT.
For order nine, cubing and the sparse order-three theorem leave nine types.
Seven are certified UNSAT; thus either surviving type has exactly one fixed
point, and the two residual types remain explicitly open.
An order-seven permutation on 43 points has one of the six displayed
fixed-point/seven-cycle types, all covered by the order-seven artifact; the
analogous equation for order eleven gives three types, all covered by the
order-eleven artifact. The eight order-13, -17, -19, and -23 types are
covered by the medium-prime artifact. The prime-cycle restrictions are the
analytic long-cycle theorem plus the 43-cycle classification. These exhaust
the primes from 7 through 43. Finally, Cauchy's theorem converts absence of
an element of each listed prime order into the stated restriction on
`|Aut(G)|`.
