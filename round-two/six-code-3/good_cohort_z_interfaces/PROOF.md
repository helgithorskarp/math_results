# Two local saturated-star interfaces under the uncovered-triangle condition

Actual author: **six-code-3, researcher**, 2026-10-01. The exploratory
two-seed inputs and broader carrier observation are credited to
**six-code-1, researcher**, messages930/1050/1075. The complete enumeration
and separate point checker in this directory are by six-code-3.

**Local theorem.** Let F consist of five-subsets of eighteen points, with
distinct members intersecting in at most two points. Let r_p count words
through p, lambda_pq count words through p,q, and let x,y,u,v be distinct.
Assume:

1. r_x=r_y=20, lambda_xy=4, lambda_xv=5, and vxy is uncovered.
2. lambda_xu is3 or4; lambda_xp is4 or5 for every p other than x,u.
   In the x-star leave, u is isolated among the points p with lambda_xp<5.
3. lambda_yu=lambda_yv=5, and lambda_yp is4 or5 for every p other than y.
4. For every t outside {x,y,u,v}, if lambda_xt=lambda_yt=4,
   then xyt is covered.

Then **lambda_xu=3 and |F|<=64**. More precisely, after point relabeling
the complete union of the x- and y-stars is one of the two literal
36-word seeds17/18 in [seed_certificates.json](seed_certificates.json),
and their respective total bounds are61/64. No bound is asserted sharp.
No hub multiplicity, other point replication, whole-code symmetry, or
global replication profile is assumed.

The x-star leave has edge pq exactly when xpq is uncovered. Isolation
in assumption2 concerns the leave induced on deficient link points;
it does not forbid low leave neighbors of u. Assumption4 concerns only
triples with both specified centers. It does not forbid every triangle
in a global deficit-support graph.

This is an author-checked exact computer-assisted local result,
conditional on the credited reviewed generic twenty-star classification.
The ordinary normalization, subgroup transport and enumeration-completeness
arguments are unformalized. Independent review of this new result and
historical priority remain pending. Unrestricted campaign bounds69--71
are unchanged.

## Imported classification and complete marking domain

Shortening at x or y gives twenty quadruples on seventeen points with
pairwise intersection at most one. Each link replication is at most5
because its five triples must be disjoint. The positive deficits
d_p=5-lambda_xp sum85-80=5, and likewise at y.

The generic23-fixture coverage from
[six-code-2 lemma8720](../../six-code-2/free_involution_upper68/PROOF.md),
source69f2312bb468eb59b8ab3d8978fe19b3d86cf58a, is independently confirmed
and strengthened by
[review8933](../../six-reviewer-5/twenty-star-classification-audit/REVIEW.md),
source0509c3808f44b45fd3c333a10cf36bd329003450. That review is conditional
on the reviewed universal no-low-low-leave theorem8323. Only generic
fixture coverage is imported, not any involution conclusion. We do not
repeat that earlier whole classification. Every credited literal fixture,
replication, covered pair and supplied subgroup is checked here.

At x, u has deficit1 or2 and all other positive deficits are1. Its high
leave is isolated at u. Since v is low, it has exactly one leave neighbor,
which is y by assumption1. Thus u,v and u,y are covered link pairs:
the former because u differs from the unique leave friend y, and the
latter by the high-leave isolation. At y, both u,v are low and its row
is unit. The pair u,v is covered by the universal no-low-low theorem;
the pair u,x is covered by the x-star isolation. The unique u-leave
friend b is recorded as a marking, with **no condition on its image**.

[domain.py](domain.py) derives all markings from all23 actual fixtures.
The first-star ordered marks (u,v,y) number14, in fixtures9/17 with
6/8 marks. The second-star ordered marks (u,v,x,b) number878, in eight
unit-row fixtures. Every supplied map is checked as a point bijection,
an actual star automorphism, and a member of an identity-containing
closed subgroup. An empty supplied group means identity only.
No supplied subgroup is asserted to be full.

Actual mark orbits are disjoint and exhaust the raw domains:2 first
orbits and180 second orbits, hence360 products. Quotienting the first
star is an ambient point relabeling fixing its center; quotienting the
second is a reparametrization of its relative map. Neither operation
assumes a symmetry of F. The separate [verify.py](verify.py) reconstructs
these raw domains and orbit covers directly from literal block sets.

## Exhaustive relative maps and compatible unions

Normalize x=17. The four common xy words have disjoint three-point tails.
One tail contains u; v is outside their union because vxy is uncovered.
A relative map sends the second-star x marking to17, its u,v to the
first u,v, and its four tails bijectively to the first four tails.
The u-tail has two point maps fixing u. The other three tails have
3! tail matches and (3!)^3 point maps. There are therefore2592 partial
maps per product. Fourteen source points are mapped; the remaining
three have all six bijections. The complete normalized carrier is
933,120 partial maps representing5,598,720 full relative maps.

[produce.py](produce.py) constructs block-tail matches. For each partial
map it tests projected private second quadruples against every private
first quadruple; three common mapped points certify a collision in every
extension. The source-private words exclude x and the first-private words
exclude y. Common-tail matching and the pair-packing property already
control intersections with common words. Every noncolliding partial is
expanded through all six remaining bijections. Every positive union is
also checked against all actual word pairs.

The separate checker assigns each source tail point individually, using
only injectivity and the requirement that points of the same source tail
belong to one target tail and different tails to different target tails.
This DFS enumerates every2592-map partial universe without permutations
of block tails. It checks literal intersections with **all20 first words**,
including the actual second center, and expands every unexcluded residual
bijection. Each sorted partial-map universe and each full positive-record
list agrees entrywise, through canonical hashes and actual positive arrays,
with the producer. The DFS visits4,622,688 states, at most15,454 per product.
Its fixed guard is200,000 states and10 seconds per product. An incomplete
process, guard or missing product establishes no absence.

Exactly34 compatible full maps remain, giving34 distinct labelled
36-word unions in28 products:26 with first fixture9,8 with first fixture17.
These are normalized marked interfaces, not asserted to be34 full
isomorphism classes. The raw positives are retained in
[BRIDGE.json](BRIDGE.json); no triangle or multiplicity-two restriction
is used to obtain that complete raw population.

## Literal triangle screening and the two certificates

All members through x or y are in each36-word union. Consequently every
lambda involving either center and every covered/uncovered xyt triple
are already final in any extension retaining their degrees20.

For32 of the34 maps, a t outside {x,y,u,v} has all three pair counts
lambda_xy=lambda_xt=lambda_yt=4 while xyt is uncovered. These violate
assumption4. There are45 such actual triangle witnesses in total.
[check_bridge.py](check_bridge.py) reconstructs all actual block images,
all36-word packings and every triangle witness without importing a
producer, census helper or graph module. The witness readout SHA256 is
1ada3a40200d101cf4c58ea7ccf981ee2f274e151615ed30be939562dfcbda7a.
The compact bridge alone verifies these literals; its population
completeness additionally requires the full carrier replay above.

The survivors are products42/49, both first fixture9 with
(u,v,y)=(13,2,11); second fixture11 with marks(6,0,13,11) and
(6,9,13,11). Their actual mapped words equal the two published seeds
of [lemma8967](../two_saturated_seed_interfaces/README.md), source
e26ac0cd59844e9aee9eb8f48e513ffd20910925. In particular lambda_xu=3.
The input seed certificate is copied byte-for-byte and credited.
The bridge checker reconstructs allC(16,5)=4368 possible further words
avoiding the two complete centers. The118/121 candidates have5803/6087
compatible pairs; the supplied proper25/28-colorings give61/64 totals.
No new coloring search, optimality assertion or solver exclusion is used.

The mathematical carrier record SHA256 is
858f4fd6a754da4f3f183500762b924cadc06a8ee1a85a6f9c6ce55fe0476ea0;
the marking-domain SHA256 is
bc13d5616c7d8c4b4714fb8d1775a27c0bf6189dcbea456dea20418600fe66d1.
[expected.json](expected.json) is a frozen comparison record, not an
absence certificate or replacement for the completeness arguments.

The motivating [two-unsaturated structure8947](../../six-code-1/two_unsaturated_tail_structure/PROOF.md)
is separately credited author-checked work. It is not a premise of this
local theorem. Its charging argument now has the separate
[independent review9027](../../six-reviewer-5/uniform-tail-audit/REVIEW.md),
sourcef82510e90fbb225aed45d7c833858618aafe2e35, with explicit reviewed
local premises. That review does not audit this new34-map carrier or
local theorem. Any uniform size71/profile application keeps its distinct
transfer and dependencies.

## Validation and trust boundary

[reproduce.py](reproduce.py) performs a cold serial producer/point-DFS
replay against pre-existing expected/bridge files, literal witness/seed
checks, and semantic controls. Run normally and under Python-O as in
[README.md](README.md). Thirty damaged inputs/records are rejected;
three point relabelings of all23 stars preserve all marking populations.
Full map arrays, logs and generated census files stay in workspace scratch.
Only compact reproducible source,34 positives and credited input fixtures
are published. CPython, the imported classification, and the ordinary
finite reductions are explicit trust boundaries. Separate algorithms run
by this author are not a new independent reviewer verdict.

The established point cap and code baseline are classical:
[Brouwer1975](https://ir.cwi.nl/pub/6883/6883D.pdf),
[Aw-Chee-Ling2003](https://ymchee66.github.io/home/PDF/6cwc.pdf),
and the [maintained table](https://aeb.win.tue.nl/codes/Andw.html).
The69-word public baseline was freshly checked against all690 triples
and2346 pairs. That reproduction is validation, not a new construction.
