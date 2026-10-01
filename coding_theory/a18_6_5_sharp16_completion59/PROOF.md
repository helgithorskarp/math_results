# Sharp completion size 59 at a replication-sixteen marked hub

Author: **six-code-3, researcher**, 2026-10-01.

## Statements and coverage

Let `F` consist of distinct five-subsets of an eighteen-point set `V`,
with `|U intersect W|<=2` for distinct members. Write
`r_p=#{W in F:p in W}` and `lambda_pq=#{W in F:p,q in W}`.
The shortened star at `y` is `{W\{y}:y in W in F}`.

**Canonical lemma.** Set `V={0,...,17}`, `x=14`, `y=17`, and let `Q`
be the twenty literal quadruples in [input.json](input.json).
Assume the shortened `y` star is exactly `Q`. If `r_x=16` and a
distinct point `a` satisfies `r_a=20,lambda_xa=0`, then **`|F|<=59`**.
Equality is attained by [witness.json](witness.json).

**Generic consequence.** The same sharp bound holds when the shortened
`y` star is a twenty-block quadruple pair packing with profile
`(4^5,5^12)`, its leave on the five replication-four points has four
edges, and `x` is a marked isolated vertex of that induced leave.
The passage to `Q` imports [marked classification 8350](../a18_6_5_one_unsaturated_at_71/PROOF.md),
source **43dc0a95a2232b6b9ff1e85d18a1a34fe5705bbc**,
confirmed by [independent review8401](../../constant_weight_marked_star_review5/REVIEW.md),
source **b45ab435bac5ce32ee8ef711bdc879497f3044b6**.

**Additional exact classification.** Under either version's hypotheses,
the multiset of the seventeen `lambda_xp` is
`(0,3^k,4^(16-2k),5^k)` for some `k=0,1,2,3,4`.
All five patterns occur in admissible prefixes. The labeled normalized
prefix counts for these five patterns are `4,38,74,24,2`.
In particular every point other than `x,a` occurs with `x` at least
three times. Only four of142 prefixes have the regular pattern `k=0`;
regularity is not a hypothesis.

These are complete author computer-assisted local results. The producer
and different checker have the same author. This new stage awaits
independent peer review; the counting/normalization/completeness bridges
have not been formalized in a proof assistant. The canonical computation
is self-contained and uses no imported finite-output corpus or earlier
hub-replication exclusion. The generic interpretation uses 8350.

## Normalize the absent point and enumerate its full star

Directly in `Q`, the replication-four points are `{0,1,3,6,14}`; the
induced leave is a four-cycle plus isolated `x`. The uncovered neighbors
of `x` are `N={2,9,15,16}`. The four `x/y` words have three-point tails
`{0,4,12},{1,7,13},{3,8,11},{5,6,10}`. Thus `lambda_xy=4` and any
absent point must be in `N`.

The producer maps the high cycle and low-point leave cohorts, obtaining
3072 leave-preserving maps fixing `x`. Eight preserve the actual block
list. The checker instead enumerates bijections point by point,
preserving replication, pair and triple incidences before testing the
entire block list; all these tests are necessary for any true map.
It obtains the same eight maps in 121 states. Their images of2 are
exactly `N`. Relabeling the entire unknown family therefore lets us set
`a=2`, without assuming that family has any automorphisms.

The twenty shortened `a` blocks avoid `x`. They cover 120 distinct pairs
on sixteen points, exactly `binom(16,2)`. They consequently cover every
such pair once. Five fixed `y` words contain `a`; their three-point
tails partition `T=V\{a,x,y}`, of size fifteen. These five blocks cover
every pair with `y`, so the fifteen remaining `a` words avoid `y`.
Their shortened quadruples must cover the 90 pairs of `T` outside the
five tail triangles. The residual degree of every point is twelve.

Test every quadruple of `T`. Exactly405 avoid those fixed pairs, and 150
restore to `a` words compatible with every `y` word. The checker instead
tests all 8568 five-subsets of `V`, selecting those containing `a` but
avoiding `x,y`, and using literal intersections. The two complete
90-pair and 150-column arrays agree entry for entry.

The producer enumerates exact covers by choosing an uncovered pair
with fewest legal columns and branching over every containing column.
A completion has exactly one such column, so induction proves complete
coverage; all its six pairs are removed, and conflicting columns are
excluded. Too few available columns to cover the remaining pairs is a
necessary rejection. Deterministic pivots give one path per cover.

The checker uses whole-point stars with initial point demand four.
Choose a point with positive remaining demand and enumerate all choices
for its entire remaining star, in increasing column order, with disjoint
three-point tails. Subtract their incidences and recurse. Every possible
completion supplies one such remaining star at the chosen point.
Columns touching used pairs or a depleted point are impossible.
Insufficient columns, insufficient columns at a demanded point, or
fewer than three times its demand available tail points are necessary
rejections. At a zero-demand leaf check fifteen blocks and all 90 pairs
literally. Induction on demand proves coverage and uniqueness.

Both censuses give the same six actual fifteen-block cover keys:
109 pair-pivot states versus 451 whole-point states. Each cover supplies
a checked 35-word `a/y` union with `r_a=r_y=20,r_x=4,lambda_xa=0`.
Every word, intersection and the complete120-pair `a` star is checked.
No affine-plane classification is used.

## The complete142 three-star prefixes

Since `r_x=16`, exactly twelve further `x` words remain. They avoid
`a,y` and are `{x} union R`, where `R` is a quadruple of `T` compatible
with the35-word union. Two such words are compatible exactly when
their quadruples share no pair. The producer tests all quadruples of
`T`; the checker independently tests all eighteen-point five-subsets.
No point-replication quota is imposed on the twelve selected quadruples.

The producer uses exact integer-bitset clique enumeration, greedily
coloring the compatibility graph's available vertices. Each color is
an independent set and bounds any clique by one vertex per color.
Reverse-order branching includes a vertex, restricts to its neighbors,
then removes it before subsequent branches. A target clique has a
unique first branch; the color bound rejects only insufficient states.

The checker has a different binary recurrence on literal pair sets.
For a selected available quadruple `v`, every target packing either
includes `v` and excludes its conflicts, or excludes `v`. **Both
branches are completed**, including when the first has positive leaves.
A zero remaining target records the actual sorted key. Too few blocks
is a necessary rejection. Only completed negative states are memoized
by the exact remaining block set and target; positive states are never
cached as negatives or skipped when reached through another prefix.

For another safe rejection the checker partitions available blocks
into pairwise conflicting groups, intersecting actual conflict sets
as each group is built. A packing uses at most one block in each group.
A completed partition with fewer groups than the target is negative;
once the group count reaches the target it gives no rejection.
Induction on availability proves the two exhaustive branches complete,
and the necessary bounds and negative memoization preserve that result.
Every positive leaf and uniqueness of every path are checked literally.

|Absent-star cover index|Hub candidates|Producer states|Binary states|Twelve-block keys|
|---|---:|---:|---:|---:|
|0|129|33180|63557|20|
|1|127|35081|69251|19|
|2|129|29419|57161|20|
|3|128|29263|69805|32|
|4|128|39601|67181|32|
|5|127|36507|74483|19|

All cases finish under the unchanged 200000-state/ten-second guards.
The actual model arrays and all 142 keys agree entry for entry between
implementations. These are labeled normalized prefixes, not a count of
isomorphism classes. Each restores to47 distinct compatible words:
`20+20+16-5-4=47`. All three stars are closed. Direct pair counts give
the five claimed hub profiles; every listed pattern is attained.

## Direct residual certificates and sharpness

Every further word must avoid `a,x,y` and hence be a five-subset of `T`.
For each47-word prefix, the producer tests all `binom(15,5)=3003`
possibilities by exact bit intersections against every prefix word.
The checker uses a different literal characterization: the prefix has
nine two-center words and38 one-center words, covering respectively
nine and 152 distinct triples of `T`. No triple repeats, because prefix
words intersect in at most two points. Thus 161 triples are forbidden,
and 294 of `binom(15,3)=455` are eligible. A residual word is compatible
exactly when every one of its ten triples is eligible. The checker
tests all 8568 five-subsets of `V` by this rule, also excluding centers.
Both actual residual arrays agree for every prefix; each has6--19 words.

For each of these142 arrays, [certificate.json](certificate.json)
lists an actual partition of its indices into at most twelve groups.
The checker verifies exact coverage without duplicates, every index,
and **every pair of words within each group sharing at least three
points**. Such words cannot both belong to `F`; consequently at most
one residual word is chosen per group. The group-count distribution is

|Groups|5|6|7|8|9|10|11|12|
|---|---:|---:|---:|---:|---:|---:|---:|---:|
|Prefixes|10|20|23|34|32|9|10|4|

Therefore every admissible family has at most `47+12=59` words.
This upper bound uses literal conflict-partition certificates; no
floating-point bound or residual optimization verdict is trusted.
The full142-prefix census remains a reproduced exhaustive calculation,
whose written completeness argument is a separate trust boundary.

The certificate is 44354 bytes, SHA256
`dbbf91f55aa1b500665d5d81b048820a5de0b9b1422eb9a14a15e6145bda7e78`.
It contains actual template maps, all six absent-star cover keys,
all 142 twelve-block keys, exact carrier hashes, every residual partition,
and the positive witness's model key. Hashes are provenance checks;
the checker regenerates actual arrays before matching them.

The 59-word fixture restores one47-word prefix and twelve residual
words. Every word's weight, distinctness, all pairwise intersections,
the exact `y` star, `r_x=16,r_a=r_y=20` and `lambda_xa=0` are checked.
Its file SHA256 is
`72576f353a5cfc2eaa33778012f12aa0e6dba966b690226fe79c193495c86286`;
its canonical word-list SHA256 is
`b2eab0a2b3428f3725ab9d663a6e7e22563869f20185554b0b2247a25182653a`.
Canonical digests use sorted-key compact JSON with a final newline.
This proves sharpness of the conditional bound; it is not a new global
lower bound on `A(18,6,5)`.

## Consequences for larger families and71 words

The preceding [single-absence bound 8473](../a18_6_5_single_absent_sharp16/PROOF.md),
source **dff39045011d66f45ab84a3aaa5e5a254ef00141**,
proves `r_x<=16` under the same marked-star and saturated-absence
hypotheses, without requiring `r_x=16`. Combining that bound with the
new sharp completion lemma gives **`r_x<=15` whenever `|F|>=60`**.
The earlier 47-word fixture remains a valid sharpness example for8473;
the present result establishes the exact maximum completion size at 16.

At71 words, the classical point cap20 gives
`sum_p(20-r_p)=360-355=5`, so `r_x>=15`. Our consequence forces
`r_x=15` and all seventeen other replications20. This is the
one-unsaturated profile `(15,20^17)`. Six-code-1's separately published
[whole one-unsaturated exclusion](../../constant_weight_18_6_5_equality_structure/NO_SINGLE_UNSATURATED_71.md),
source **053622a2c8a24c2e83a6702e0d0648ede8031270**,
uses common-unit-star result 8397 and excludes that entire profile.
**If that complete author stage is adopted**, no 71-word family can
have our marked unit star and a saturated point absent from its mark.
That credited stage awaits independent review. Our new local result
does not depend on it; only this final71-word transfer does.

This excludes a specified local configuration, not all 71-word codes.
The global campaign interval remains **69--71**, with the upper end
from the separately credited [upper71 proof](../../constant_weight_18_6_5_equality_structure/UPPER71.md)
and its [independent audit](../../constant_weight_upper71_review1/REVIEW.md).
Code1's [unsaturated absent-pair exclusion 8442](../../constant_weight_18_6_5_equality_structure/ABSENT_PAIR_71.md)
concerns a complementary pair type. No72-word replication equalities
are transferred to71 here.

## Literature and validation boundaries

[Brouwer1975](https://ir.cwi.nl/pub/6883/6883D.pdf) proves `A(17,6,4)=20`,
the point cap used in the71-word transfer. The template `Q` is known
Case VII(f) of [Stanton--Street1987](https://combinatorialpress.com/jcmcc-articles/volume-001/some-achievable-defect-graphs-for-pair-packings-on-seventeen-points/),
JCMCC1,207--215. Their [1988 follow-up](https://combinatorialpress.com/ars/vol26a/)
has not been fully assessed; historical priority of this joint completion
claim is unassessed. The [primary maintained table](https://aeb.win.tue.nl/codes/Andw.html)
was checked live 2026-10-01 and still lists 69--72; campaign upper 71 has
its own source and independently checked dependencies.
[Aw--Chee--Ling2003](https://ymchee66.github.io/home/PDF/6cwc.pdf),
Theorem1 and AppendixA, supplies the known69-word lower bound.
The [published fixture](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69)
was re-fetched and exactly validated in this pass, unchanged SHA256
`cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d`.
That baseline reproduction is validation, not new research.

Both complete mathematical implementations are by six-code-3.
Thirty-five corruption/invalid-guard checks, including a partition
with correct coverage but a compatible pair in one conflict group,
are rejected under `-O`. Five actual zero-state/time jobs return
INCOMPLETE and give no exclusion. Complete tiny positive/negative
censuses and the 59-word fixture are accepted. [VALIDATION.json](VALIDATION.json)
records fresh normal and optimized runs. Controls may reuse the
already verified generated model cache solely to avoid redoing the
census; the mathematical verifier always regenerates all models.
Private full censuses and execution caches are omitted from publication.
No timeout, UNKNOWN, interruption or resource kill is a mathematical
nonexistence result. Resources and guards have not been escalated.
