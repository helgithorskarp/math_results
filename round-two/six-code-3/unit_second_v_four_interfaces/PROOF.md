# Local upper67 without a second-row v multiplicity premise

Actual author: **six-code-3, researcher**, 2026-10-02.
This is an author-checked exact computer-assisted local result, conditional
on generic twenty-star classification8933 and universal8323. The combined
theorem additionally imports the earlier local lemma9176. Ordinary
normalization, completeness and coloring arguments are unformalized.
Independent review of the new result and historical priority are pending.

Let F be distinct five-subsets of eighteen points, with distinct members
intersecting in at most two points. Write r_p for point replication and
lambda_pq for pair replication. A triple is covered if a word contains it.
The x-star leave has an edge pq exactly when xpq is uncovered.

**Combined theorem.** Let x,y,u,v be four distinct points. Assume:

1. r_x=r_y=20, lambda_xy=4, lambda_xv=5, and xyv is uncovered.
2. lambda_xu<5, and u is isolated in the x-star leave induced on
   H_x={p other than x:lambda_xp<5}.
3. lambda_yu=5, and lambda_yp is4 or5 for every p other than y.

Then **|F|<=67**. The second-row v multiplicity is unrestricted within
the stated unit row. There is no other first-row multiplicity restriction,
specified extra point, covered-triangle condition, global replication
profile or whole-code automorphism assumption. Isolation concerns the
induced leave on H_x; leave neighbors outside H_x are permitted.

**New finite theorem.** Under the same hypotheses, with the additional
condition **lambda_yv=4**, one has **|F|<=67**. If **yuv is covered**, the
new finite theorem strengthens to **|F|<=65**. Both assertions are proper
coloring bounds, with no optimality or sharpness claim.

The combined theorem follows by its two exhaustive y-row possibilities.
If lambda_yv=5, apply the earlier
[lemma9176](../additional_deficit_pair_interfaces/PROOF.md), verified
source9ece64b2e910e80df829be899217e2a43bda0b5c. If lambda_yv=4, apply
the new finite theorem proved below. Thus9176 retains credit for the
earlier domain; its numerical computation is not repeated by this runner.
The combined theorem gives a selector obstruction for every packing of
at least68 words. It does not force the selector from any global profile.

## Generic input and the marking domain

Shortening either complete20-star gives twenty quadruples on seventeen
points, with pairwise intersection at most one. A link replication is
the corresponding center-pair multiplicity. It is at most5 because its
incident quadruples have disjoint three-point tails. Deficits sum
17*5-20*4=5.

The imported generic23-class coverage is the explicitly conditional
[independent review8933](../../six-reviewer-5/twenty-star-classification-audit/REVIEW.md),
source0509c3808f44b45fd3c333a10cf36bd329003450. Its no-low-low-leave
premise is the reviewed
[universal8323](../../../constant_weight_upper71_review1/REVIEW.md),
source02c1569568854e575f8b176ea07d552737a7da84. The literal
[fixtures.json](fixtures.json) is byte-identical credited input from
six-code-2's [8720](../../six-code-2/free_involution_upper68/PROOF.md),
source69f2312bb468eb59b8ab3d8978fe19b3d86cf58a, SHA256
c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7.
No symmetry-specific numerical bound is imported from8720.

For a shortened star call replication-five link points low, and positive
deficit points high. These names describe link replication, not whole-code
degree. Every low point has one leave neighbor, which is high by8323.
The star has16 leave edges; if h is its number of high points, precisely
h-1 leave edges join high points. At the first star u and y are distinct
high points. Isolation of u gives h-1<=C(h-1,2), and h>=2 implies h>=4.
The positive deficits sum5, so the only first-row partitions here are
2111 and11111; lambda_xu is consequently3 or4. This is a conclusion of
the hypotheses, not an extra restriction imposed by the computation.

At the first star v is low and its unique leave friend is y. The u-v
pair is covered since u differs from y. The u-y pair is covered because
u is isolated among the high points. At the second star all high
points have deficit1, u is low, and **v and x are high and joined by a
leave edge**. The second u-x pair is covered by the actual xyu word.
Write b for the second u's unique leave friend. Crucially, **b may equal
v**: the second u-v pair may be uncovered.

[domain.py](domain.py) derives all first marks(u,v,y) and all second
marks(u,v,x,b) from the23 literal fixtures. First marks require only the
stated isolated deficient u, low v with friend y, and replication-four
y. Second marks enumerate **every actual high-high x-v leave edge**,
with low u and covered u-x. No u-v coverage restriction is added.

There are18 raw first marks, in four checked subgroup orbits:

| First fixture | Representative(u,v,y) | Raw marks in fixture |
| --- | --- | ---: |
| 8 | (13,2,11) | 4 |
| 8 | (13,5,12) | included above |
| 9 | (13,2,11) | 6 |
| 17 | (14,1,12) | 8 |

There are658 raw second marks, in144 checked subgroup orbits.
**110 raw second marks have b=v**, with32 representative orbits of
this kind. The full product domain has11844 raw products or576
normalized products. Raw marks with uncovered u-v are retained throughout.

Every supplied subgroup is checked for actual point bijections preserving
the quadruples, identity, closure and literal orbit coverage. No group
maximality is assumed. Quotienting first marks is an ambient relabeling;
quotienting second marks reparametrizes the relative point map. Neither
step requires whole-code symmetry. The separate [verify.py](verify.py)
independently derives marks and orbit partitions from actual sets and
replications; it imports neither the producer nor the domain helper.

## Complete relative maps and compatible unions

Normalize x=17. The four xy words have disjoint three-point tails.
The covered xyu triple places u in one tail; xyv being uncovered places
v outside all four. This holds in both source and target stars.
A relative map sends the second x,u,v to17 and the first u,v. There
are two internal maps of the u-tail,3! matches of the other tails,
and6^3 internal maps. This gives2592 distinct partial point maps.
Fourteen source points are assigned. All six bijections of the remaining
three points are accounted for, giving15552 full maps per product.
The whole normalized carrier has1492992 partial maps representing
**8957952 full maps**. No raw-positive count is inferred from subgroup
sizes or division of representative counts.

[produce.py](produce.py) matches block tails. It discards a partial map
only when a projected private second quadruple already meets a private
first quadruple in three points; extension cannot undo that collision.
Common-tail matching and pair uniqueness control common words. Every
unexcluded partial is expanded through all six residual bijections, and
each positive union is checked against every actual pair of words.

The independent checker assigns tail points individually through a DFS
with injectivity and tail-association constraints. It reconstructs the
whole2592-map universe, checks private second words against **all20
first words**, and checks complete36-word unions literally. Sorted
partial universes and every actual positive point map/word array agree
with the producer in every product. It tests22356 full maps explicitly
and visits6687660 DFS states, at most15454 in one product. Every product
accounts for all15552 extensions. All576 products occur exactly once;
missing products, resource guards and incomplete processes prove no absence.

Exactly **50 positive maps** remain in39 products, with50 distinct
labelled36-word unions, stored in [BRIDGE.json](BRIDGE.json). These
are normalized marked representatives, not full isomorphism classes.
There is no triangle filter. Eighteen unions have one observed u-v word,
and32 have two. The first star always supplies one. The second supplies
one exactly when its u-v pair is covered; the literal core check requires
this actual count, rather than assuming it is always two.

The complete marking-domain SHA256 is
e6e22a572f29b5615a3752bfe0c2ad4b051bbca4a0a0044d250aa33608831ea9;
the whole independent point-checker record SHA256 is
47c12510b02b5e03d3b911d11988a979a5691e63cd9e775b2af6971af4728a2f.

## Residual domains and positive certificates

Each union already contains every word through x or y and has
20+20-4=36 words. Every further word avoids both centers. We examine
allC(16,5)=4368 possible further words at every representative. The
total surviving candidate population is5986. Compatibility means
intersection at most two; the total number of compatible pairs is300375.
Any completion is a clique in this graph. A proper k-coloring permits
at most k additional words, and hence bounds |F| by36+k.

[generate_colors.py](generate_colors.py) constructs proper positive
colorings by deterministic greedy DSATUR, with at most64 fixed seeded
priority orders per root. Failure to improve a coloring proves nothing
about optimality or nonexistence. The literal [check_colors.py](check_colors.py)
imports no producer, domain helper, previous census or solver. It
rebuilds actual star images and every stated local hypothesis, derives
each residual universe from the360 owned triples, and checks every
compatible pair for distinct colors. The50 color functions are new.

The proper colorings use26--31 colors and give these bounds:

| Certified upper bound | Marked unions |
| --- | ---: |
| 62 | 7 |
| 63 | 19 |
| 64 | 17 |
| 65 | 6 |
| 67 | 1 |

Thus every completion has at most67 words. The source u-v leave cases
cannot be dropped: the unique largest bound67 is in the one-observed-u-v
branch. All32 unions with two observed u-v words have bound at most65.
If yuv is covered, the complete y-star must supply that word, so the
core has two observed u-v words and this sharper bound applies.
The6 unions with first deficit pattern11111 have bound at most64;
the14 with lambda_xu=3 have bound at most65. These are conditional
certificate bounds, not exact completion maxima. A final whole-code
lambda_uv can exceed the observed core count, so the observed-count
readout is not silently treated as a whole-code pair-multiplicity premise.

The whole literal residual-universe SHA256 is
d8fde1e724ee3f99d81f4360045c02f3661625e13a602a6a90680fc762f73666.
The certificate SHA256 is
444dc6a9771c04a98a7c3c244d5670052c33566d8613f3d380591e6781d8af38.

## Verification, trust and prior work

[reproduce.py](reproduce.py) requires the pre-existing frozen
[expected.json](expected.json), bridge and certificates. It runs every
producer and independent checker product in sequential30-product chunks,
checks the exact whole-file inventory and concatenated independent record
coverage, compares all actual positive arrays, regenerates the complete
certificate bytes, and checks every literal color record.
Normal and optimized Python modes run from separate empty directories.
The whole mathematical RESULT must be byte-identical; time/interpreter
metadata is kept separately. Exact measured receipts are in
[VALIDATION.json](VALIDATION.json); commands are in [README.md](README.md).

[controls.py](controls.py) rejects41 semantic damages or population gaps:
10 fixture/group damages,8 bridge damages,13 certificate damages,
7 primary record damages, the whole product population gap, an
account-consistent but false u-v pruning rule, and deletion of an
uncovered-u-v marked orbit. It accepts the actual one-u-v-word control.
Three actual point bijections transport all23 fixtures, all marks,
all50 cores, every residual candidate and every color function:150
transported interfaces. Transport checks mathematical objects, not only
counts. These checks expose implementation errors; completeness still
rests on the explicit marking, common-tail and extension arguments.

One serial CPU-intensive job and all numerical threads1 are used under
the unchanged1CPU2GiB process scope. Guards remain10 seconds/product,
200000 point-DFS states/product,5 seconds/color product,64 priorities,
and60 seconds/subprocess. No timeout, UNKNOWN, missing record or memory
kill is mathematical nonexistence. No guard is raised to complete a claim.

The producer/point-checker and color framework is adapted from9176 and
the earlier [9045](../good_cohort_z_interfaces/PROOF.md) and
[9098](../good_cohort_z_residuals/PROOF.md), with their exact source credit
in [DEPENDENCIES.json](DEPENDENCIES.json). This computation has its own
changed mark predicates,576 products,50 new core arrays and50 new colors.
It imports no old numerical completion arrays. The combined theorem
uses9176 solely for its stated lambda_yv=5 bound67; that dependency is
author-checked and independently unreviewed at preparation. Reviews8933
and8323 concern their explicitly imported generic inputs, and confer
no verdict on the new theorem.

Current primary literature is
[Brouwer's live table](https://aeb.win.tue.nl/codes/Andw.html) and
[Aw--Chee--Ling, Theorem1/AppendixA](https://ymchee66.github.io/home/PDF/6cwc.pdf),
which supplies the known69 construction. The live
[literal69 code](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69)
was freshly checked:69 distinct weight-five words,2346 word pairs,
690 unique owned triples; distance counts6:1264,8:637,10:445.
Its source SHA256 is
cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d.
That reproduction is baseline validation, not new research. The reviewed
campaign interval69--71 is unchanged. No ambient selector, whole
replication-profile exclusion, unrestricted upper70, whole-code symmetry,
exact clique maximum or historical-priority claim is made here.
