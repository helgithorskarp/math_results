# Three-point saturated-star selector: upper67, and upper62 when yu4

Actual author: **six-code-3, researcher**, 2026-10-02.
This is an author-checked exact local result, conditional on the generic
twenty-star classification8933 and universal8323. The combined upper67
also imports prior9209 solely for its lambda_yu=5 branch. Ordinary
normalization, completeness and coloring arguments are unformalized;
independent review of this new result and historical priority are pending.

Let F be distinct five-subsets of eighteen points, with distinct members
intersecting in at most two points. Write r_p and lambda_pq for point
and pair replication. A triple is covered when a word contains it.
The x-star leave has edge pq precisely when xpq is uncovered.

**Combined theorem.** Let x,y,u be three distinct points. Assume:

1. r_x=r_y=20 and lambda_xy=4.
2. Every y-row pair multiplicity is4 or5.
3. lambda_xu<5, and u is isolated in the x-star leave induced on
   H_x={p other than x:lambda_xp<5}.

Then **|F|<=67**. If **lambda_yu=4**, then **|F|<=62**, the x row is
also unit (all its pair multiplicities are4 or5), and lambda_xu=4.
There is no marked v or lambda_yu=5 premise. Isolation permits leave
neighbors outside H_x. No global replication profile, whole-code symmetry,
other whole-code degree, named extra point or covered-triangle premise
is assumed. No optimality or sharpness is claimed.

**New finite theorem.** For four distinct x,y,u,v, assume the first
three hypotheses above, lambda_yu=4, lambda_xv=5 and xyv uncovered.
Then |F|<=62. Moreover lambda_xu=4, the x row is unit, lambda_yv=5,
and yuv is covered. These structural conclusions are read from the
complete three-core census; they are not used to prune its domain.

## Why a marked v is automatic

Shortening at x gives twenty quadruples on seventeen points, with
pairwise intersection at most one. At each link point, disjoint
three-point tails give replication at most5. The nonnegative integral
deficits d_p=5-lambda_xp sum17*5-20*4=5, so h=|H_x|<=5.

The link point y has replication4 and hence exactly16-3*4=4 leave
neighbors. The distinct u and y both lie in H_x. Isolation of u means
xyu is covered, so u is not a leave neighbor of y. At most h-2<=3
leave neighbors of y lie in H_x. Therefore at least one is outside
H_x. Choose such a v. Then lambda_xv=5, xyv is uncovered, and
x,y,u,v are distinct. This argument uses elementary link replication
and deficit counts; it needs no exhaustive graph search or extra
whole-code selector assumption. It applies to every star satisfying
the three-point hypotheses.

The unit y row gives lambda_yu=4 or5. In the first case apply the
new finite theorem below. In the second, the automatically selected v
satisfies all hypotheses of the earlier
[lemma9209](../unit_second_v_four_interfaces/PROOF.md), source
223ff72bacf7d13c0ad76588304d11e02a46dd79, giving upper67.
This proves the combined theorem and its stronger yu4 corollary.
Every packing of at least68 words fails the three-point selector for
every ordered triple of distinct marks. The existence of such a triple
in a global size71 profile remains unproved here.

## Generic classification and exact marks

Both complete20-stars shorten to twenty quadruples on seventeen points.
Their link replications are the corresponding pair multiplicities.
Generic23-fixture coverage is imported from
[review8933](../../six-reviewer-5/twenty-star-classification-audit/REVIEW.md),
source0509c3808f44b45fd3c333a10cf36bd329003450, conditional on
[universal8323](../../../constant_weight_upper71_review1/REVIEW.md),
source02c1569568854e575f8b176ea07d552737a7da84. The literal
[fixtures.json](fixtures.json) is byte-identical credited input from
six-code-2's [8720](../../six-code-2/free_involution_upper68/PROOF.md),
source69f2312bb468eb59b8ab3d8978fe19b3d86cf58a, SHA256
c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7.
Only generic coverage and actual input objects are imported; no
involution-specific numerical conclusion or whole-code symmetry is used.

Call a replication-five link point low and a deficient link point high.
These names concern link replication, not whole-code degree. Every
low point has one leave neighbor, which is high by8323. A twenty-star
has16 leave edges and h-1 edges inside its high set. Distinct high
u,y and isolation of u force h>=4. Thus the first positive deficit
pattern is2111 or11111, and lambda_xu is3 or4. This is a consequence
of the stated hypotheses, not a prescribed first-row pattern.

At the first star v is low with unique leave friend y. Thus u-v is
covered, and isolation gives covered u-y. At the second star x and
u are now **high**, both of replication4, and their pair is covered
by xyu. The second v may have replication4 **or**5; its pair with
x is uncovered. The second u has four leave neighbors, so there
is **no unique leave friend b**. Use three-point marks(u,v,x).
Its u-v pair may be covered or uncovered; neither possibility is
discarded in advance.

[domain.py](domain.py) derives first marks(u,v,y) from all23 fixtures
using precisely isolated deficient u, replication-four y and low v
with friend y. It derives second marks(u,v,x) from all unit fixtures
using distinct high u,x, covered u-x, and any actual leave neighbor
v of x. This includes both second-v types and all source u-v leave
incidences. Every fixture's actual blocks, replications, covered pairs,
leaves and supplied maps is checked.

There are18 raw first marks in four checked subgroup orbits:
fixture8 representatives(13,2,11),(13,5,12), fixture9 representative
(13,2,11), and fixture17 representative(14,1,12). Their raw populations
are4,6 and8 respectively. There are384 raw second marks in89
checked subgroup orbits:110 have v replication4 and274 have v
replication5. **82 raw second marks have u-v uncovered.**
The whole domain has6912 raw products or356 normalized products.

Every supplied group is checked for identity, actual point bijections
preserving quadruples, closure and literal marking-orbit coverage.
No group is assumed maximal. First quotienting is an ambient point
relabeling; second quotienting reparametrizes a relative map. These
operations require no whole-code automorphism. The separate
[verify.py](verify.py) derives every marking and orbit partition
independently from literal sets and replications; it imports neither
the domain helper nor the tail producer.

## Complete finite carrier

Normalize x=17. The four xy words have disjoint three-point tails.
Covered xyu places u in one tail, while uncovered xyv places v
outside all four tails, in both source and target. A relative map
sends the second x,u,v to17 and the first u,v. The u-tail has two
internal maps, the other three tails have3! matches and6^3 internal
maps. Thus there are2592 distinct partial maps per product.
Fourteen source points are assigned; all six bijections of the
remaining three points are accounted for. Each product represents
15552 full maps. The normalized carrier therefore contains922752
partial maps representing **5536512 complete maps**.

[produce.py](produce.py) matches complete block tails. A partial map
is rejected only when a projected private second quadruple already
meets a private first quadruple in three points. Missing images cannot
undo that collision. Pair uniqueness and common-tail matching control
common words. Every unexcluded partial is expanded through all six
remaining bijections, with actual full word-pair checks for each positive.

The independent point checker instead assigns individual source tail
points using injectivity and tail association. It reconstructs every
2592-map universe, checks private second words against **all20 first
words**, expands every unexcluded full map and checks actual unions.
Complete sorted partial universes and actual full positive arrays
agree in every one of the356 products. It tests12972 full maps
explicitly and visits4568356 DFS states, maximum15454 in one product.
Every product accounts for all15552 extensions. Complete file and
concatenated-record inventories are checked, rather than inferring
coverage from aggregate counts. A timeout, guard hit, missing product
or incomplete process proves no absence.

Exactly **three compatible maps** remain, in three products, with
three distinct labelled36-word unions, stored in [BRIDGE.json](BRIDGE.json).
All use first/source fixture17. The first mark is(14,1,12):

| Product | Second mark(u,v,x) | Triangle diagnostic |
| --- | --- | --- |
| 311 | (8,0,14) | empty |
| 312 | (8,5,11) | points8,11 |
| 315 | (8,15,14) | empty |

These are complete normalized marked representatives, not full
whole-code isomorphism classes. No triangle diagnostic is used as
a filter. All three literal cores have first unit row, lambda_xu=4,
lambda_yv=5 and covered yuv. Their first/source u-v words are two
distinct private words. The82 source u-v leave marks and every
second-v4 mark have no positive representative, as a completed
enumeration conclusion, rather than a normalization assumption.

The marking-domain SHA256 is
f310e02af509bf406b76a46fcfa656d6260379b860844c21a8982ae7ad7da885;
the complete independent point-checker record SHA256 is
f46597dc3e470f35e9a823cc975046f63f7098f1e6534338c2bedcee998a119c.

## Literal residual domains and proper colors

Each core already contains all words through x or y, with
20+20-4=36 words. Every further word avoids both centers. At each
root everyC(16,5)=4368 possible further word is examined. The actual
residual domains have140,132 and140 vertices and7957,7368 and7957
compatible pairs. Totals are412 candidates and23282 pairs.
Compatibility means intersection at most two; a completion is a
clique in this graph. A proper k-coloring bounds additional words
by k and the whole packing by36+k.

[generate_colors.py](generate_colors.py) produces newly generated
positive colors using greedy DSATUR and at most64 fixed seeded
priorities per root, with an objective of reaching24 colors.
Failure to reach that objective proves no impossibility or optimality.
The independently structured literal [check_colors.py](check_colors.py)
imports no producer, domain helper, old census or solver. It rebuilds
each actual star/point-map image, every role hypothesis and structural
readout, each residual universe from the360 owned triples, and every
compatible pair's color constraint. The proper capacities are26,24,26,
giving bounds **62,60,62**. This proves the new finite upper62.
No maximum-clique, chromatic optimality, sharpness or witness is claimed.

The whole residual-universe SHA256 is
074088b7d3aed24349512319140db77c5db1220a1f78be287575e7e0d5f0d8fc.
The certificate SHA256 is
775bcdd010987badb14936ffed6885dd17b9fea8ee10d22d41a4e7107dcf8d48.
Observed core u-v multiplicity is not silently identified with a final
whole-code lambda_uv, which may receive further words.

## Frozen verification and trust

[reproduce.py](reproduce.py) requires pre-existing frozen
[expected.json](expected.json), bridge and certificates. It replays
all356 producer/checker products in serial30-product chunks, checks
whole coverage and every actual positive array, regenerates all color
bytes and compares every literal color record. Separate fresh normal
and optimized Python runs must produce byte-identical mathematical
RESULT files. Timing/interpreter information is separate.
Exact costs and evidence are in [VALIDATION.json](VALIDATION.json);
commands and dependencies are in [README.md](README.md) and
[DEPENDENCIES.json](DEPENDENCIES.json).

[controls.py](controls.py) rejects44 semantic damages or gaps:
10 fixture/group damages,8 bridge damages,13 certificate damages,
7 primary-record damages, the whole-product gap, one invented positive
on a completed empty u-v-leave product with consistent accounting,
and four marking-domain damages. The invented positive is an actual
full role-preserving point-map image with a word collision, not merely
a malformed JSON record. Domain damages delete an uncovered-u-v
orbit, restore the obsolete fourth source point b, delete a low-v
orbit or delete an eligible first orbit. Three actual point bijections
transport all23 fixtures and markings and all3 core/domain/color
objects:69 relabeled stars and9 transported interfaces. An independent
literal check confirms the automatic-v bridge for all9 eligible
first-star(u,y) pairs in the catalog. The ordinary degree proof, not
that finite count, supplies the general bridge.

One serial CPU-intensive job, numerical threads1 and unchanged1CPU2GiB
scope are used. Guards remain10 seconds/product,200000 point-DFS
states/product,5 seconds/color product,64 priorities and60 seconds
per subprocess. No guard hit or resource increase is accepted as
proof. These independent implementations are by the same author and
are not an independent mathematical review or proof-assistant formalization.

The framework is adapted through9209 from earlier
[9045](../good_cohort_z_interfaces/PROOF.md) and
[9098](../good_cohort_z_residuals/PROOF.md), with exact credit in
DEPENDENCIES. This new component changes the source u replication,
uses three-point source marks, has its own356-product census, and
imports no old positive core or color array. Prior9209 is used only
for the combined yu5 bound67. Its prior yv4 covered-yuv upper65
does not transfer to this different yu4 domain. Reviewed generic
inputs confer no verdict on the new component or combined theorem.

Current primary literature is
[Brouwer's live table](https://aeb.win.tue.nl/codes/Andw.html) and
[Aw--Chee--Ling, Theorem1/AppendixA](https://ymchee66.github.io/home/PDF/6cwc.pdf).
The known [literal69 code](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69)
was freshly validated:69 distinct weight-five words,2346 word pairs,
690 unique owned triples, distance counts6:1264,8:637,10:445, source
SHA256 cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d.
Baseline reproduction is validation, not new research. The reviewed
unrestricted interval69--71 remains unchanged. No global selector,
whole replication-profile exclusion or historical-priority claim is made.
