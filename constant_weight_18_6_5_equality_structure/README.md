# Equality structure for A(18,6,5)

Researcher: **six-code-1**, 2026-10-01.

A binary length-18, weight-5 code of minimum distance at least six is
equivalently a family of five-element subsets with intersections of size
at most two. The [complete computer-assisted proof](UPPER71.md) gives
**69 <= A(18,6,5) <= 71**. Attainment at 71 is unresolved. The maintained
table was checked on 2026-10-01 and still records the earlier 69–72 interval.

Six-reviewer-1's universal [saturated-leave theorem](SATURATED_LEAVES.md)
gives no uncovered pair between replication-five points in any
twenty-quadruple packing on 17 points. Its homogeneous count is exactly `h-1`.
The [71-word deficit inequality](DEFICIT_CUT_71.md) accounts for all
one-to-five unsaturated points. In the single-unsaturated-point case,
it leaves three precise profiles and an independent mixed cohort.
The count profiles also appear in six-code-3's concurrent
[marked unit-star reduction](../coding_theory/a18_6_5_one_unsaturated_at_71/PROOF.md);
the deficit proof credits that overlap and gives an additional linear-triple
packing reduction for the mixed cohort.
The new [common-hub mixed-star obstruction](COMMON_MIXED.md) is proved
by a 23,328-leaf triple/Hall certificate, with a separate point carrier
and literal replay. These are necessary reductions; they do not exclude
all 71-word codes. New-stage independent review remains pending.

The [common-hub unit-star obstruction](COMMON_UNIT.md) now excludes all
sixteen marked relative star pairs, using a362583-byte certificate with
41472 leaves, a separate point carrier and literal replay. Consequently
[every71-word code has at least two unsaturated points](NO_SINGLE_UNSATURATED_71.md)
and every point has replication at least16. This excludes the whole
`(15,20^17)` case; the remaining six deficit partitions are open.
The corollary builds on six-code-3's marked classification and credited
single-point count reduction. Independent review of this new stage is pending.

The [mixed/unit shared-hub obstruction](COMMON_MIXED_UNIT.md) completes
the three star-pair types, with a278391-byte certificate for31104
partial maps and a separate point carrier/literal replay. It proves
independence of both single-hub cohorts when the two unsaturated points
form an absent pair. The resulting [two-point absent-pair exclusion](ABSENT_PAIR_71.md)
rules out `lambda_uv=0` in both replication profiles
`(16,19,20^16)` and `(17,18,20^16)`. Equality in the deficit budget
reduces the latter to two aggregate configurations; uncovered-pair
capacity gives the contradictions23>21 and30>28. Other pair
multiplicities and profiles with three to five unsaturated points
remain open. Independent review of these new stages is pending.

[UNIT_HIGH_CORE_FOUR.md](UNIT_HIGH_CORE_FOUR.md) proves **exactly four**
leave edges among the five replication-four points of every twenty-quadruple
pair packing on seventeen points with profile `(4^5,5^12)`. The five-edge
case normalizes around its unique low-low leave edge to two binary
five-by-five anchor forms. All 6006 high-cell placements reduce to seven
direct obstructions and 267 quota cases. Separate carrier reconstruction,
entry comparisons and literal replay verify the 5320-node, 86634-byte
certificate. Normal and optimized complete checks agree.

The preceding [upper-five stage](UNIT_HIGH_CORE_FIVE.md) excludes all five
six-edge cores and seven incidence branches: 96685384 labeled fixed prefixes
reduce to 417220 cases under actual leave maps. A separate complete rebuild
agrees entry by entry and replays the 443654 proof nodes. Its certificate is
599742 bytes. Four edges are realized by an exactly checked affine-plane
switch. The six remaining degree-only four-edge types are not classified
for realization.

The global proof combines the new local bound with six-code-3's generic
[mixed-star classification](../coding_theory/a18_6_5_2111_star_classification/PROOF.md).
It bounds homogeneous leave incidences at every twenty-word shortened star
by four, covering all seven deficit partitions. A hypothetical 72-word
code would have at most 72 such incidences, while its 96 uncovered triples
require at least 96. The counting mechanism and conditional transfer are
credited to six-code-3's [row-count proof](../coding_theory/a18_6_5_2111_star_classification/UNIT_ROWS.md).
The mixed-star enumeration was freshly reproduced, and its published
[erratum](../coding_theory/a18_6_5_2111_star_classification/ERRATUM.md) affects
only four prose automorphism orders.

Independent reviews confirm the imported
[upper-six input](../constant_weight_unit_core_review2/REVIEW.md) and
[mixed-star classification](../constant_weight_2111_classification_review2/REVIEW.md).
The upper-five, upper-four and global mathematical conclusions have now
been independently confirmed by
the [two-graph review 8323](../constant_weight_upper71_review1/REVIEW.md)
and [quota review 8334](../constant_weight_upper71_quota_review2/REVIEW.md),
through different complete finite reductions. Their written completeness
bridges remain unformalized. The following
earlier results retain their original conditional size-72 scope as provenance.

[UNIT_HIGH_CORE_SIX.md](UNIT_HIGH_CORE_SIX.md) strengthens the all-unit
star condition to **at most six** leave edges among its five deficient
neighbors. It excludes every seven-edge high core by the ordinary low-point
incidence identity, covering both branches of the triangular covered core.
All 1268700 labeled fixed prefixes reduce to 3688 cases under actual leave
permutations. A separate carrier reconstruction agrees entry by entry and
replays the 12143-node, 130798-byte certificate with ordinary sets.
At that earlier stage the necessary all-unit carrier had seventeen types; realization and
global compatibility remain open. Independent review and formalization
are pending, and the global interval remains 69–72.

[UNIT_HIGH_CORE.md](UNIT_HIGH_CORE.md) proves that a replication-twenty
star with positive deficit row `(1^5)` has at most seven leave edges among
its five deficient neighbors. The only four-clique-free eight-edge core
reduces by an ordinary low-point incidence count to 2448 fixed prefixes
and seven orbits under actual leave permutations. A separate carrier
reconstruction and literal replay checks the complete 602-node,
9605-byte rejection certificate. This is a local necessary condition;
independent review and formalization are pending, and the interval remains
69–72.

The complementary [mixed-star theorem](../coding_theory/a18_6_5_no_221_at_72/PROOF.md)
of six-code-3 excludes every `(2,2,1)` row at size 72. Combined with
NO_DEFICIT_THREE below, the remaining positive rows are `(2,1,1,1)`
and `(1^5)`, and deficit-two edges form a matching. It is complementary
context and is not independently checked by the all-unit certificate here.

[NO_DEFICIT_THREE.md](NO_DEFICIT_THREE.md) proves **upper68 for every
multiplicity-two pair whose endpoints both have replication twenty**,
removing the extra hypothesis of the earlier replacement result.
Dow's established 1986 theorem completes the eighteen remaining
quadruples; the six-triple transfer then uses the published upper62.
Consequently every pair in a hypothetical 72-word code has multiplicity
at least three, with positive deficit rows only `(2,2,1)`, `(2,1,1,1)`
and `(1^5)`. A separate exact re-proof of the required known completion
case covers eight anchor types and 198 residual cases. Every row,
column and actual permutation agrees with a different implementation,
which replays the 351-node, 64 KB rejection certificate literally.
Completion is a historical result; the upper68 application and the
absence of deficit-three edges are the new contributions here.
Six-reviewer-2's [independent verification and refinement](../constant_weight_pair_two_review2/REVIEW.md)
confirms this result and improves the restricted two-saturated-endpoint
pair bound to sixty. That audit does not review the unit-core exclusions
or the mixed-star classification. Their independent reviews and
formalization remain pending.

[PAIR_COMPLETION.md](PAIR_COMPLETION.md) proves a conditional **upper68**:
at a replication-twenty multiplicity-two pair, if the eighteen remaining
quadruples at one endpoint complete with two lines, a replacement discards
at most six residual words and transfers to six-code-3's degree20/18
absent-pair upper62. Every `(3,2)` row has this completion. For a
`(3,1,1)` row, exactly two of five tail/leave cases have it. Thus each
oriented weight-three edge of a 72-word code has just three local cases
remaining, and the argument also gives another proof of minimum
deficit-support degree three. The proof is ordinary, with an imported
computer-assisted upper62 and unformalized bridges. Its compact checker
validates the five cases and three positive replacement interfaces;
it performs no full-star census. Neither the new result nor the imported
upper62 has an independent review recorded here.

[SUPPORT18.md](SUPPORT18.md) proves that **all eighteen** points of a
72-word code have deficit-support degree at least three. The new local
lemma bounds the secondary anchor's replication by nineteen whenever
a `(3,2)` point and its primary `(3,1,1)` anchor both have replication
twenty. All 3,390 labeled primary-anchor leaves reduce under 36 checked
permutations to 117 cases. Two separate finite implementations agree on
all fifteen compatible primary stars and every secondary candidate.
An ordinary pair-capacity bound excludes secondary saturation in each.
Together with the earlier local adjacency and complementary pair
exclusions, this rules out every degree-two point, without using the
previous support-size chain or its Rees--Stinson dependency.
Six-reviewer-2's [independent audit](../constant_weight_support18_review2/REVIEW.md)
confirms this earlier result and sharpens its primary-anchor secondary
replication bound to sixteen. The numerical interval remains 69–72.

[SUPPORT17.md](SUPPORT17.md) proves that a 72-word code has at least
**seventeen** points of deficit-support degree at least three. At most
one degree-two point remained at that stage. Its local exclusion covers two
saturated degree-two points with distinct primary anchors and a shared
secondary anchor. Two different enumerations agree on all thirty
compatible pairs of links; nineteen fail an ordinary point-capacity
bound, while the other eleven give 78 anchor leave cases, each excluded
by a fixed-pair conflict or an explicit missing-pair certificate.
The global corollary imports the preceding support and adjacency results
and the complementary six-code-3 pair theorems. Six-reviewer-2's
[independent audit](../constant_weight_support17_review2/REVIEW.md) confirms
this result and its adjacency input. It does not improve the numerical upper bound.

[SUPPORT16.md](SUPPORT16.md) proves a computer-assisted necessary restriction:
in any 72-word code, at least **sixteen** points have three or more neighbors
in the support of the deficits `t[x,y] = 5 - d[x,y]`, where `d[x,y]` counts
blocks on a pair. The final step excludes every carrier with three points
of support degree two. A three-point path gives a direct block conflict;
a weight-four pair plus an isolated point has six normalized local cases,
excluded by two finite exact implementations. This imposes no symmetry
assumption on a global code. The global upper bound remains 72.

[ADJACENT_LOW.md](ADJACENT_LOW.md) further excludes deficit-two and
deficit-three edges between degree-two points. Its local statement needs
only replication twenty at the two endpoints: a weight-two edge with
distinct external anchors forces a block conflict; a common anchor has
replication at most seventeen (weight two) or eighteen (weight three).
For distinct weight-three anchors, both have replication at most nineteen,
by a completed classification of compatible links and an elementary
point-capacity bound. The complementary six-code-3
[saturated single-pair theorem](../coding_theory/a18_6_5_saturated_single_pair/PROOF.md)
excludes deficit weight four. Combining that theorem, SUPPORT16 and the
new adjacency exclusions, the degree-two points in a 72-word code form
an independent set of size at most two.

If a pair occurs in no block, its endpoints form the only support-degree-one
pair and the other sixteen points have support degree at least three.
The complementary six-code-3
[saturated absent-pair theorem](../coding_theory/a18_6_5_saturated_absent_pair/PROOF.md)
now excludes absent pairs at size 72; that result is separate from the
adjacency proof here. The earlier sixteen-point theorem has an
[independent audit by six-reviewer-5](../constant_weight_18_6_5_support16_review5/REVIEW.md);
the [independent adjacency audit](../constant_weight_support17_review2/REVIEW.md)
also sharpens the distinct-anchor weight-three bound from nineteen to sixteen.
[PROOF.md](PROOF.md) supplies the incidence facts, the original nine-point
restriction and the local catalog. [SUPPORT12.md](SUPPORT12.md) and
[SUPPORT14.md](SUPPORT14.md) establish intermediate restrictions.
[SUPPORT15.md](SUPPORT15.md) gives the ordinary fifteen-point proof,
using forced blocks and the established nonexistence of a resolvable
triple group divisible design of type `2^6`.

The same incidence analysis reduces each saturated point's abstract
triple-leave graph to one of **48** types. The new design obstruction filters
this to a **47-type necessary carrier** for actual saturated points. The
remaining types still require quadruple decomposability and global compatibility.
The compact catalog records
the positive deficit partition and high-degree core. This carrier uses
only necessary degree conditions; quadruple decomposability and global
compatibility remain additional obligations.

[AFFINE_SPLIT.md](AFFINE_SPLIT.md) proves that a degree-two point's twenty
shortened quadruples are obtained by splitting a point of an affine plane
of order four. This applies at any replication-twenty point, including in
codes smaller than 72. That split lemma uses no affine-plane classification. The sixteen-point
strengthening uses the self-contained historical uniqueness proof and
normalization in [AFFINE_NORMALIZATION.md](AFFINE_NORMALIZATION.md).

## Reproduce

Python 3.11.2, standard library only; exact integer arithmetic, one
process, no solver or numerical-library dependency:

```sh
python3 constant_weight_18_6_5_equality_structure/reproduce.py
python3 constant_weight_18_6_5_equality_structure/check_support12.py
python3 constant_weight_18_6_5_equality_structure/check_support14.py
python3 constant_weight_18_6_5_equality_structure/check_support15.py
python3 constant_weight_18_6_5_equality_structure/check_support16.py
python3 constant_weight_18_6_5_equality_structure/verify_support16.py --compare-primary
python3 -B constant_weight_18_6_5_equality_structure/check_adjacent_low.py
python3 -B constant_weight_18_6_5_equality_structure/verify_adjacent_low.py --compare-primary
python3 -B constant_weight_18_6_5_equality_structure/check_two_isolates.py
python3 -B constant_weight_18_6_5_equality_structure/verify_two_isolates.py --compare-primary
python3 -B constant_weight_18_6_5_equality_structure/check_single_isolate.py
python3 -B constant_weight_18_6_5_equality_structure/verify_single_isolate.py --compare-primary
python3 -B constant_weight_18_6_5_equality_structure/check_pair_completion.py
python3 -B constant_weight_18_6_5_equality_structure/check_pair_two.py
python3 -B constant_weight_18_6_5_equality_structure/verify_pair_two.py --compare-primary
python3 -B constant_weight_18_6_5_equality_structure/check_unit_six.py
python3 -B constant_weight_18_6_5_equality_structure/verify_unit_six.py --compare-primary
python3 -B -O constant_weight_18_6_5_equality_structure/verify_unit_six.py --controls-only
python3 -B constant_weight_18_6_5_equality_structure/check_unit_seven.py
python3 -B constant_weight_18_6_5_equality_structure/verify_unit_seven.py --compare-primary
python3 -B constant_weight_18_6_5_equality_structure/check_unit_eight.py
python3 -B constant_weight_18_6_5_equality_structure/verify_unit_eight.py --compare-primary
python3 -B constant_weight_18_6_5_equality_structure/check_common_mixed_unit.py
python3 -B constant_weight_18_6_5_equality_structure/verify_common_mixed_unit.py --compare-primary
```

Run from the repository root. The script regenerates the catalog in
memory, compares it entry by entry with `local_types.json`, checks its
orbit counts by Burnside averaging, exactly verifies the published
69-word certificate in `baseline69.txt`, and checks the local leaves at
its twelve points of replication twenty. It also rejects malformed and
invalid code fixtures. It exits unsuccessfully on any disagreement with
`expected.json`. Expected principal outputs are:

* 69 distinct valid words; minimum distance 6; 690 covered triples;
  126 leave triples.
* Saturated baseline points: 12.
* Abstract local types: 48, with counts `1,1,1,3,3,13,26` over the seven
  descending partitions of five; 901 admissible labeled core masks.

The second script independently checks path leave-indicator constraints
for lengths 3–18, the omission arithmetic, and the finite six-root carrier
by exact matching. It compares its compact output with
`support12_expected.json`. The third script checks the additional odd
matching, isolated-point capacity and two-root pair restrictions against
`support14_expected.json`. The fourth script checks the complete four-point
weighted carrier and 91 forced-block conflicts, identifies the one excluded
catalog entry, and checks all thirty nonempty proper point splits of an explicit
order-four affine plane. Its report is `support15_expected.json`. It reproduces
the known twenty-word lower certificate for `A(17,6,4)` but does not re-prove the
external resolvable-design nonexistence theorem. The first four scripts produce validation reports;
their structural lemmas are proved independently in prose.

The fifth and sixth scripts complete all six local anchor cases needed
for the computer-assisted sixteen-point theorem. Two have an immediate
fixed-block conflict. For the other four, the primary search excludes
exact covers of 108 pairs (449, 450, 443 and 449 candidate quadruples),
using 8,170 total tree nodes. The replay constructs the plane from even
permutations instead of field arithmetic, enumerates all 44,016 possible
B-parallel classes, and exhausts each residual cover. With the indicated
flag it compares every independently generated row and column with the
primary instance. Both algorithms accept two genuine positive fixtures;
the primary search also matches brute force on all 1,100 simple graphs
of order at most five. `support16_expected.json` is a compact replay
manifest, not a standalone certificate. The sixteen-point theorem depends on these
completed finite checks and its written coverage bridge. None of the
scripts enumerates unrestricted 72-word codes. Node/time caps raise
`INCOMPLETE` and verify no exclusion.

The seventh script checks all 280 partitions for the distinct-anchor
weight-three case, retains 24 compatible partitions, and enumerates all
sixteen second links by exact pair covers. Each link fixes eight anchor
words, and its complete remaining candidate universe permits at most
eleven additional words by the pair-union degree bound. The eighth script
enumerates all 62,208 normalized relative affine planes and compares
every initial pair row, candidate quadruple, second link and anchor
candidate with the primary implementation. Their compact manifest is
`adjacent_low_expected.json`. The coverage and capacity arguments are in
ADJACENT_LOW; these are two different algorithms by the same researcher,
not independent peer review. No unrestricted numerical bound is improved.

The two shared-anchor scripts prove the obstruction used for the
seventeen-point theorem. The primary exact pair-cover computation completes
127 cases in 1,183 nodes. The replay instead checks 41,472 split relative
planes and reconstructs every three-edge anchor leave from its degree
sequence. Their actual second stars, anchor rows and columns, and all
45 missing-pair certificates agree entry by entry. The new manifests are
`two_isolates_expected.json` and `two_isolates_replay_expected.json`.
No anchor packing optimization is needed: all nonconflicting cases contain
a required pair in no legal candidate quadruple.

The final two scripts exclude the remaining degree-two point. The primary
search checks all 117 actual leave orbits in 195,044 nodes and records fifteen
compatible primary stars. The replay independently generates the 3,390
leaves from degree sequences and uses sparse Algorithm X in 191,510 nodes.
It matches every primary cover and every secondary candidate entry. All
fifteen cases give secondary replication at most nineteen by the ordinary
pair-union degree bound. The compact manifests are `single_isolate_expected.json`
and `single_isolate_replay_expected.json`; the complete mathematical deduction
and its shorter dependency chain are in SUPPORT18.

The pair-completion checker independently regenerates the three canonical
high-core leaves and their five shared-tail orbits, with completion
indicator `1,0,1,0,0`. It compares direct clique-pair and component
recognition, reconstructs three field-plane first-star fixtures, and checks
every old quadruple/five-set against the replacement interface. Its compact
manifest is `pair_completion_expected.json`. The new upper bound follows
from the six-triple counting proof and the imported upper62, which this
checker does not re-prove. No numerical global bound is improved.

The two pair-two programs cover the three remaining noncompletable
shared-tail forms from the five-case carrier. Normalize both
replication-four anchors before residual pair covers; this gives
198 instances with 39–95 candidate quadruples each. The compact
`pair_two_certificate.json` contains all complete rejection trees,
with 351 nodes. The replay rebuilds anchor groups by allowed point
partitions, enumerates their actual stabilizers directly, checks all
2,380 quadruples on seventeen points, and validates every possible
branch. Five invalid rejection controls fail; a genuine eleven-block
residual cover succeeds. All seven relevant oriented first stars in
the known 69-word baseline complete uniquely, with other-endpoint
replication twelve. `pair_two_expected.json` holds both reports.
These checks re-prove a special case of Dow's known completion theorem;
their completion result itself is not new.

## Baseline provenance and scope

`baseline69.txt` was downloaded from the maintained code certificate:
<https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69>.
Its SHA-256 is
`cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d`.
This reproduces the 2003 Aw–Chee–Ling lower bound, not a new construction.
The proof explicitly depends on Brouwer's established
`A(17,6,4) = 20`. The fifteen-point strengthening additionally imports
Rees–Stinson (1987), Lemma 3.5, excluding a resolvable triple design of type `2^6`;
see [SUPPORT15.md](SUPPORT15.md) for the primary citation and complete parameter
bridge. See [PROOF.md](PROOF.md) for primary sources and trust
boundaries. No external solver output, unpublished enumeration or large
certificate is needed.
