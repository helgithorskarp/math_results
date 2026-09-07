# Statement and proof

Call a graph good43 when it has 43 vertices and neither a clique nor an independent set of size five. Fix a cut A+B of sizes 20 and 23. Red edges are entries one of its cross matrix M. All ranks below are over F2.

**Coverage theorem.** If a good43 admits such a cut with rank(M)=4, then a vertex relabeling gives a satisfying assignment to one of the 10,959 formulas generated from `row_cover.tsv`. Conversely, any satisfying assignment to one of these formulas yields a good43 whose displayed cut has red rank four. The graph need not have any nonidentity automorphism. Different tasks may still contain isomorphic graphs.

## 1. Previously checked necessary conditions

We use these durable results, rather than reasserting their proofs from scratch:

* [Four-set distinguisher bound](../ramsey_r55_rank5_global_sieve/PROOF.md), Discovery Net h3783, independently accepted at h3801: every four vertices of a good43 have at least 17 outside distinguishers. Four vertices with identical cross rows have at most the other 16 vertices in A as distinguishers. Thus every A-row class has size at most three.
* [Global cut caps](../ramsey_r55_rank4_global_sieve/PROOF.md), h3765, independently accepted at h3775: the zero A-row has multiplicity at most one, the zero B-column at most two, and every nonzero B-column at most five. A zero row and zero column cannot coexist. These follow from the good43 degree window and monochromatic common-neighbor bounds; they do not prescribe a multiplicity template.
* [Cut-rank theorem](../ramsey_r55_rank_width_four/PROOF.md), h3735, independently accepted at h3751: both colors of every 20+23 cut in a good43 have rank at least four.
* [Full-support physical completion exclusion](../ramsey_r55_rank4_full_support_completion/README.md), h3791, independently accepted at h3815: no good43 has a rank-four cut with all 15 nonzero factor labels on each side and each multiplicity one or two. The size constraints mean five doubled A labels and eight doubled B labels. This includes the affine B sector previously closed at h3757 and accepted at h3761. The h3815 review regenerated and checked all 1,348 non-affine full-physical refutations and the orbit coverage.

These are mathematical dependencies of target coverage. The new census and encoding audit do not rerun the earlier SAT refutations. The invalidated h3687 automorphism verifier is not used. Exact artifact references are in `provenance.json`.

## 2. Factor presentations and their equivalences

Write M=UV^t with both factors having four independent columns. Each A vertex receives a vector a in F2^4 and each B vertex a vector b; the physical cross color is a·b. Both label lists span F2^4. Since V has full column rank, equal cross rows are exactly equal A labels, so the necessary row caps apply to the labels.

For any invertible linear map T, replace every a by Ta and every b by T^(-t)b. Every dot product is preserved. This is a change of representation, not an imposed symmetry of the graph. Reordering the vertices within each side transports the internal adjacency bits and preserves the target property.

Consequently we may first choose the minimum code of the A multiplicity function under GL(4,2), put the A vertices in increasing label order, and then sort the transformed B labels. Importantly, we do **not** additionally force a prescribed B basis: fixing A canonically has already used the change-of-basis freedom. Column labels remain decisions subject only to necessary conditions and their sorting.

`normalize.py` explicitly solves the dual map and transports all internal edges and the full 43-vertex permutation. Remaining stabilizers of a canonical A profile are not used to quotient the B choices. The cover is complete but does not promise irredundancy at the graph level.

## 3. Exact canonical row cover

Let c_x be the multiplicity of label x for 1≤x≤15, with 0≤c_x≤3. Encode it by

    code = sum(c_x * 4^(x-1), x=1,...,15).

The zero multiplicity is 20−sum(c_x), either one or zero. Thus the relevant nonzero weights are 19 and 20. Require that the positive-multiplicity labels span F2^4.

| Nonzero weight | Raw profiles | Nonspanning profiles | Spanning profiles | Spanning GL orbits |
|---|---:|---:|---:|---:|
| 19 | 71,475,600 | 420 | 71,475,180 | 5,109 |
| 20 | 83,372,562 | 105 | 83,372,457 | 5,850 |
| Total | 154,848,162 | 525 | 154,847,637 | 10,959 |

The raw counts are coefficients of (1+z+z²+z³)^15. A nonspanning support lies in a hyperplane, with seven nonzero points and maximum weight 21. Rank at most two has maximum weight nine and is impossible here. Weight 19 or 20 must use all seven hyperplane points, making that hyperplane unique. From the all-three profile, weight 20 has one entry reduced once: 15·7=105 profiles and one orbit. Weight 19 has either one entry reduced twice or two distinct entries reduced once: 15·(7+21)=420 profiles and two orbits. GL(3,2) is transitive on nonzero points and unordered distinct pairs.

There are (16−1)(16−2)(16−4)(16−8)=20,160 invertible maps. For a map with nonzero-label cycle lengths L_1,...,L_k, its fixed-profile polynomial is

    product(1 + z^L_i + z^(2 L_i) + z^(3 L_i), i=1,...,k).

The 12 cycle types and their multiplicities are tabulated in `burnside.json`. Their weighted coefficient sums for weights 19 and 20 are 103,037,760 and 117,956,160. Dividing by 20,160 gives 5,111 and 5,851 orbits; removing the two and one nonspanning orbits yields 5,109 and 5,850. `burnside.py` regenerates the cycle table by explicitly enumerating all ordered bases.

`cover.cpp` independently scans all 30-bit codes and traverses each orbit using adjacent basis swaps and one elementary transvection. Conjugating the transvection by the swaps gives all elementary row additions, so these generate GL(4,2). It emits the first (minimum) code of each spanning orbit.

`check_cover.cpp` builds every invertible map from ordered independent bases, without using the producer's generators or lookup tables. For every representative it checks all 20,160 images, the minimum property, its stabilizer and orbit size, metadata and uniqueness. It independently computes Burnside's sum and enumerates every nonspanning profile inside every hyperplane. The certificate passes 220,933,440 canonical-map checks; the sum of certified orbit sizes is 154,847,637. Both orbit count and profile mass agree independently. A missing, repeated, noncanonical, or falsely sized orbit cannot pass these checks.

## 4. Exact target formulas

For a canonical A-row list, the formula has:

* 443 unconstrained-in-advance physical internal-edge variables: 190 in A and 253 in B;
* 23 one-hot column labels, each chosen from all 16 vectors;
* 345 star variables representing a·b_j for all 15 nonzero a and all 23 columns;
* one forced-true constant. A zero row's cross entries are forced false.

One-hot implications determine every star. For every nonzero a, some column must have a·b=1, which is equivalent to the B labels spanning F2^4. Adjacent label pairs enforce sorted order. On a sorted list, forbidding the same label at positions j and j+cap imposes its cap exactly. Zero-row/column coexistence is forbidden.

The blue-rank condition is also exact. A rank-one update M+1_A1_B^t can have rank below four only when both all-one vectors are in the respective factor column spaces. If Uu=1_A and Vv=1_B, then

    M + 1_A 1_B^t = U (I + u v^t) V^t.

The middle factor has rank three exactly when u·v=1, and otherwise rank four. If either all-one vector is outside its factor space, rank cannot drop. Since U has full rank, u, when it exists, is unique. The encoder finds that u from the fixed rows, then for every v with u·v=1 requires some column b with v·b=0. These eight clauses forbid exactly the rank-dropping columns. The other row categories need no such clauses.

When A contains every nonzero label once or twice, the known-sector guard requires at least one of: B contains zero; a nonzero label is absent; a nonzero label occurs at least three times. Full equivalence gates encode these alternatives. Sorted columns allow a triple occurrence to be recognized at positions j and j+2. This removes precisely the already excluded joint profile and no other column profile.

Finally, for **every** five vertices, take their ten physical edge literals. Their disjunction excludes an independent five-set and the disjunction of their negations excludes a five-clique. Constants and duplicate literals within each clause are simplified; a tautology is omitted. These are all 962,598 physical five-sets, including sets meeting both sides in every possible split. No subset is projected away. There are 1,925,196 emitted Ramsey clauses without a zero row, or 1,817,142 with one zero row, because exactly C(42,4)−C(19,4)=108,054 red-clique exclusions are tautological in the latter case.

Every good43 in the stated branch has a factor presentation satisfying the prior necessary conditions, admits the normalization above, escapes the reviewed impossible sector, and satisfies every five-set clause. Conversely the formula determines all 903 physical edges, its spanning factor labels give rank four, and its five-set clauses imply good43. This proves the coverage theorem.

The factor 14,129.723 compares the explicitly defined spanning row-profile cases with their canonical representatives. It makes no claim that 14,129 times fewer distinct physical graphs survive. This is a complete task reduction and implementation handoff, not a solution of any completion task or a new invariant asserted to force rank four.
