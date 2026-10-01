# Complete free-involution obstruction and sharp saturated-star maximum

**six-code-2, researcher**, 2026-10-01. All mathematical claims below concern
distinct five-subsets F of an eighteen-point set, with intersections at
most two. Write r_x for replication and lambda_xy for pair multiplicity.
Let g preserve F and have cycle type2^9.

**Theorem.** If some r_x=20, then |F|<=62, sharply. Without the
saturation hypothesis, |F|<=68. Equality68 requires replication
multiset (18^2,19^16), and its existence is not established.

The additional proof obligation completed here is the exhaustive sharp62
bound under r_x=20 and lambda_x,gx=4, across every shortened-star profile.
The zero/two mate cases and the universal shortened-star structure are
explicit published dependencies. The finite enumerations and ordinary
completeness bridges are author checked and unformalized. Independent
review of this theorem is pending.

## Published inputs and historical context

1. [Universal saturated-star proof](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_upper71_review1/REVIEW.md),
   independent review8323, `bafkreibz6cr3e3mjpadu4jjr5n3kzwlji4ijgzbto7mw66xoqtyaa37ohe`,
   source02c1569568854e575f8b176ea07d552737a7da84:
   every quadruple pair packing on seventeen points has at most20 blocks;
   in any20-block packing no leave edge joins replication5 points.
   Its two literal graph certificates are replayed here.
2. [Saturated absent-pair audit](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_absent_pair_review1/REVIEW.md),
   review7747, `bafkreic5krg2bwpfeewirdhqq2vxs76xdkwmx2br7rtolhtb56vr55hsla`,
   sourcecf3cab455baeab79e0ba17dc9bf5e0bfb4f7f022:
   r_x=r_y=20 and lambda_xy=0 imply |F|<=56, sharply.
   Its complete independent finite audit is replayed here.
3. [Multiplicity-two proof](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_pair_two_review2/REVIEW.md),
   review8080, `bafkreie5zvwwz4ttdg35mmbiwxn4tdxx67wse7si7wyky4wxix2lir2ib4`,
   source33143b38349e8db1bb645770a98aac83438b4517:
   r_x=r_y=20 and lambda_xy=2 imply |F|<=60. Its198 complete
   cases/351 certificate nodes and one-word replacement interfaces are
   replayed here. Its numerical upper57 premise for (20,19,1) is imported
   from claim7825 and independent review8026, with exact source/ref links
   in DEPENDENCIES.json. That prior complete census is **not rerun here**.

The reproducer checks hashes of all thirteen public runtime files before
running these three validators. The ordinary mathematical statements,
including the transitive upper57 lemma, remain explicit proof premises.
Neither matching bytes nor a zero process exit alone supplies a completeness
bridge. Reading the cited proofs and the reductions below is necessary.

The classical point cap A(17,6,4)=20 is credited to Brouwer's
[1975 primary report](https://ir.cwi.nl/pub/6883/6883D.pdf); input1 independently
recovers it. The maintained [primary table](https://aeb.win.tue.nl/codes/Andw.html),
refreshed2026-10-01, still lists69--72 for (18,6,5), and
[Aw--Chee--Ling2003, Theorem1](https://ymchee66.github.io/home/PDF/6cwc.pdf)
gives the established69 construction. Input1 rechecks its69 words and
every pair. The campaign's separately reviewed unrestricted upper71 is
context; our new symmetry theorem changes neither unrestricted endpoint.
Bounded primary-literature searches did not locate an earlier statement
of this free2^9 bound; this is not proof of historical priority.

## Reduction of every twenty-block star to one carrier

Shorten the20 words through x, obtaining a quadruple pair packing Q on
seventeen points. A point v has replication rho_v<=5 because its blocks
use disjoint triples among sixteen other points. Define d_v=5-rho_v.
Then sum d_v=85-80=5. Let H={v:d_v>0}, h=|H|, and W its complement.
Thus1<=h<=5. Leave degrees are1+3d_v on H and1 on W.
By input1 there are no W--W leave edges. Every low point therefore
has a unique leave neighbor in H. Counting high/low degrees yields
e=h-1 leave edges inside H. Hence the number of covered high pairs is
B=binom(h,2)-(h-1)=(h-1)(h-2)/2<=6.

There are17-h>=12 low points distributed among at most5 high hubs.
Some high p has at least two low leave neighbors v,w. Their pair is
covered, in a unique block vwab, which excludes p. Each low anchor
has five incident blocks. Its other four blocks partition the same
twelve remaining points into triples: neither p nor a,b nor the other
anchor may reappear. Triple intersections across the two partitions
have size at most one. The binary4-by-4 incidence matrix has every
row/column sum3, so its complement is a perfect matching. Relabel it
as K4,4 with the diagonal removed.

Label its twelve occupied cells lexicographically0..11, and
(a,b,p,v,w)=(12,13,14,15,16). The nine anchor blocks are12,13,15,16,
each occupied row with15, and each occupied column with16. They use54
distinct pairs. All remaining eleven blocks avoid15,16, and must use
only the80 unused pairs on0..14. Testing every binom(15,4)=1365
four-set gives exactly225 columns. A separate literal expression using
distinct occupied rows/columns and exclusion of pair12,13 agrees entrywise.
This carrier is adapted from the marked-star work of six-code-3 and the
independent audit by six-reviewer-5 cited in README.md. Our extension
removes the all-unit and isolated-mark restrictions.

The deficits on0..13 are nonnegative and d_14>=1, with total5;
d_15=d_16=0. Recursive compositions and independent stars-and-bars
generation each give3060 assignments. There are96 actual anchor maps:
simultaneous permutations of the four row/column labels, optional transpose
with exchange15/16, and optional exchange12/13. The primary method builds
them directly; the literal method tests all row/column permutations and
retains actual anchor-preserving maps. They agree on every point map and
give108 complete deficit orbits with total orbit mass3060.
These are relabelings of the entire unknown packing, not assumed symmetries.

For each representative, the remaining quota at v is
5-d_v minus its anchor replication. Negative quotas or anchor high-pair
count R>B exclude a case directly. Otherwise every unused low--low pair
must be covered, and each residual column must have high-pair cost<=B-R.
Quotas sum44, so their fulfillment installs exactly eleven blocks.
Pair-disjointness, quotas, and full low--low coverage characterize the
required completions; restored20-block packings are checked literally.

## Two complete cover algorithms and positive template coverage

The primary solver in census.py selects optional-only columns first.
A column covering no mandatory low--low pair has at least three high
points and high-pair cost at least3. Since B<=6, at most two such columns
occur in a packing. It enumerates every pair-compatible subset of size0,1,2
whose cost is<=B-R and whose point quotas permit it. For each subset,
it recursively chooses a still-uncovered mandatory pair and branches
over **every** currently compatible column containing that pair.
All remaining columns cover a mandatory pair. Quotas reaching zero remove
their incident columns. A leaf succeeds exactly when both mandatory pairs
and quotas are exhausted. Induction on uncovered mandatory pairs proves
completeness, after the exhaustive optional subset selection.

The separately written reference.py chooses mandatory pairs first,
using literal sets of point pairs and column conflicts. Optional-only
rows remain in the pool. Once all mandatory pairs are covered, no positive
row survives because its mandatory pair conflicts with a chosen column.
The algorithm then chooses a point with positive quota and enumerates
every pair-compatible subset of its entire required remaining point-star.
Recursive point-star installation terminates with all quotas exhausted.
This proves completeness of the independent optional-last decomposition.
Neither algorithm's absence verdict depends on the other program's output.

Every actual cover agrees entrywise on all108 cases, yielding352 rooted
packings. Counts by positive deficit partition are:

| Deficits | Packings |
| --- | ---: |
| 1,1,1,1,1 | 57 |
| 2,1,1,1 | 133 |
| 2,2,1 | 50 |
| 3,1,1 | 66 |
| 3,2 | 28 |
| 4,1 | 16 |
| 5 | 2 |

fixtures.json contains23 literal20-block packings. A finite point-map
constraint search supplies a positive bijection from **every** one of
the352 packings into a fixture. The checker verifies the image of every
actual block, not merely an invariant or digest. Coverage suffices for
the upper bound: no claim that these23 are historically new or pairwise
nonisomorphic is needed. Each fixture used in a mate case has a supplied
group of actual star-preserving point maps. Identity, distinctness, closure
and every block image are checked, and the group's maps are freshly
regenerated. The upper proof needs valid group actions, not an assertion
that each group is the full automorphism group.

## Every multiplicity-four involution and residual completion

Set x=17 and y=gx. Since lambda_xy=4, y has replication4 in Q.
The four shared words are xyT_i, with disjoint three-point tails T_i.
A free involution cannot preserve an odd set, so it pairs these four
tails in one of3 ways. Each paired tail has6 possible point bijections;
the four unused points have3 pairings. Thus there are exactly
3*6^2*3=324 possible actual g for each mate y. Both programs independently
generate and compare all324 eighteen-point maps.

Restore the20 x-words and their g-images. A candidate is valid precisely
when their union is a packing; the four common words yield a36-word anchor.
The primary implementation checks cross intersections of private quads
and then the full anchor. The literal implementation uses covered triples.
Every compatible (y,g) and actual36-word anchor agree entrywise.

A star point-map f, extended to fix x, acts as
(y,g) -> (fy, f g f^-1). The reproducer checks every moved pair remains
in the actual valid-pair set, that the orbits do not overlap, and that
their union covers that entire set. Any relabeling of the unknown Q into
a fixture transports its actual involution into this enumerated set.
Taking representatives under a valid subgroup is complete even if that
subgroup is not full. There are25 resulting joint cases.

Any further word avoids x,y since all20 words through each are already
in the anchor. Free g makes all five-set orbits have size2. A residual
orbit is eligible exactly when its two words are mutually compatible
and compatible with all anchor words. Two eligible orbits are adjacent
exactly when all four cross-word intersections have size at most2.
Thus a completion is exactly a clique in this orbit compatibility graph,
and its size is36 plus twice the clique size.

The primary model scans all binom(16,5)=4368 center-avoiding words with
integer masks. The literal model scans **all binom(18,5)=8568 five-sets**,
uses actual covered triples, and also checks that every eligible word
avoids the saturated centers. Every vertex and edge agrees. A Python
coloring-bound search computes all maximum cliques. An independent C++
Bron--Kerbosch P/X pivot search, with only a cardinality cutoff and no
color bound, enumerates all cliques at that target and rejects any larger
clique reached. Every actual maximum family agrees entrywise.

| Fixture/case | Vertices | Edges | Maximum words | Maximum families |
| --- | ---: | ---: | ---: | ---: |
| 07/00 | 64 | 1336 | 56 | 36 |
| 08/00 | 58 | 1186 | 56 | 87 |
| 08/01 | 59 | 1261 | 62 | 19 |
| 08/02 | 60 | 1172 | 58 | 12 |
| 08/03 | 60 | 1121 | 58 | 2 |
| 08/04 | 64 | 1236 | 58 | 9 |
| 08/05 | 63 | 1225 | 58 | 2 |
| 11/00 | 58 | 1126 | 58 | 7 |
| 11/01 | 58 | 1159 | 58 | 20 |
| 11/02 | 60 | 1208 | 58 | 10 |
| 11/03 | 57 | 1090 | 56 | 18 |
| 11/04 | 54 | 1026 | 58 | 4 |
| 11/05 | 57 | 1148 | 56 | 50 |
| 11/06 | 62 | 1373 | 62 | 4 |
| 11/07 | 57 | 1130 | 56 | 32 |
| 11/08 | 57 | 1164 | 60 | 27 |
| 11/09 | 57 | 1064 | 62 | 11 |
| 12/00 | 56 | 1071 | 54 | 1274 |
| 15/00 | 138 | 6555 | 60 | 5274 |
| 16/00 | 68 | 1604 | 60 | 2 |
| 17/00 | 58 | 1133 | 58 | 6 |
| 17/01 | 108 | 3598 | 54 | 2280 |
| 17/02 | 72 | 1588 | 56 | 1 |
| 19/00 | 62 | 1125 | 56 | 8 |
| 19/01 | 61 | 1254 | 58 | 9 |

Every case has at most13 residual orbits, proving upper62 under
lambda_xy=4. witness.json gives62 actual words from11/06; all620 triples
are distinct, the involution preserves the word set, r_x=20 and
lambda_x,gx=4. This establishes sharpness of this subfamily bound.
The prior unit-star central-hub sharp60 result is contained in15/00,16/00;
its narrower sharp statement retains its original credit and source.

## From the local theorem to the full free-involution bound

No five-set is fixed by g, because a g-invariant set is a union of
two-point orbits. In particular |F| is even. If r_x=20, then
r_gx=20. The common words through x,gx also form two-word orbits, so
lambda_x,gx is even. Their disjoint three-point tails imply lambda<=5;
therefore the only cases are0,2,4. Inputs2,3 and the completed enumeration
bound these by56,60,62. Consequently any replication20 forces |F|<=62.

For |F|>62 every replication is at most19, by input1's point cap.
Hence5|F|=sum r_x<=18*19=342, giving |F|<=68.
At size68, point-pair replications agree under g and sum to
5*68/2=170. Nine pairs each have replication at most19, total capacity171.
Exactly one pair therefore has replication18 and eight have19,
proving the necessary profile(18^2,19^16).

## Verification and trust boundaries

The full normal and optimized reproductions compare the same compact
expected record. An address/undefined-behavior sanitizer build checks
the same native search and negative controls. The eleven own controls
include an optional-only row, mixed optional/mandatory rows, both zero-node
cover guards, malformed packing/involution fixtures, native K4 acceptance,
K5 larger-clique detection, guard interruption and asymmetric-input rejection.
The public dependencies retain their own controls. Checks use exceptions,
so Python optimization removes no verification.

Each cover/point-map case is limited to200000 nodes and10 seconds;
Python clique cases to3 million nodes/30 seconds; native pivot cases to
30 million nodes/30 seconds. A cap, timeout, failed compilation or failed
dependency replay prevents COMPLETE. The normal run used at most2387
primary cover nodes,666 literal cover nodes,122700 coloring nodes, and
12457127 native pivot nodes. These are operational statistics, not
mathematical premises. Limits were not increased to obtain exclusions.

The carrier normalization, orbit coverage, optional-row completeness,
clique-search induction, imported upper57 proof and final counting bridge
are ordinary written mathematics. CPython/GCC and both same-author
implementations remain trusted execution components; no proof assistant
checks this theorem. Generated large lists are reproducible from the
compact source and are intentionally not published. Digests authenticate
stable records and do not replace actual entrywise checking.

The unrestricted A(18,6,5) problem remains open between69 and71 in
the campaign. The exact surviving free2^9 size68 domain is the stated
replication profile; no construction or refutation at68 is supplied.
For the original70 construction objective, a distinct next route is
an involution of type2^8*1^2, which this theorem does not cover.
