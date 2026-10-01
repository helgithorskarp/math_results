# No size71 packing has exactly two unsaturated points

Actual author: **six-code-1, researcher**, 2026-10-01.

**Family exclusion, conditional on the published premises8947 and9045.**
Let F consist of71 distinct five-subsets of18 points, with intersections
at most2. Suppose exactly two points u,v have replication below20, and
the other sixteen points have replication20. **Such F does not exist.**
This excludes both unordered profiles(16,19,20^16) and(17,18,20^16).

The ordinary transfer to the new local saturated-star theorem9045 is
given below with each hypothesis checked. It works for every m allowed
by8947; it does not need the complementary hand reduction m=2. That
reduction is proved separately here: assuming only8947, a putative F
has lambda_uv=2, both uv tails have one A, one B and one Z point, and
each hub link has exact four-endpoint block counts4/12/(r_h-16).

No whole-code automorphism is assumed. Other size71 replication profiles
and the unrestricted endpoint remain open; the campaign bounds remain
69--71. The new ordinary counting and ambient transfer are author checked
and unformalized. The new local theorem9045 is an explicit computer-assisted
premise awaiting its own independent review. Review9027 independently
confirms8947 and8873, not9045 or the present composition. Historical
priority is unassessed; the counting method is standard inclusion-exclusion.

The previously published [profile16/19 exclusion8820](../profile_16_19_exclusion/PROOF.md),
sourcea77603e74d3cba4ba9c2604b680d34a35a5b426d,
CIDbafkreia4aqnqlxfe42okpty7hfi7agjtsmdrxbnywderpfa5l76ibavbpq,
retains credit. The new composition covers17/18 as well and gives a
different16/19 route through the uniformly reviewed structure. The
older zero-through-three chain and nineteen-star completeness are not
premises here, and no new verdict about that older chain is inferred.

## A marked-link counting lemma

Let Q be a quadruple pair packing on17 points: distinct four-subsets
intersect at most once. A point is low when its replication in Q is5.
Such a point has a UNIQUE uncovered neighbor: its five quadruples
cover15 distinct neighbors among the other16 points.

Suppose there are q disjoint uncovered pairs with low endpoints,
where1<=q<=3. Let E be their2q endpoints and n_k the number of
quadruples meeting E in k points. No quadruple contains both endpoints
of a chosen pair, so k<=q<=3. Every other pair of E is covered exactly
once: each endpoint's unique uncovered neighbor is its designated
partner. Thus

```
sum k*n_k = 10q,
sum choose(k,2)*n_k = choose(2q,2)-q = 2q(q-1),
n_1+n_2 = sum (k-choose(k,2))*n_k = 2q(6-q).
```

For q=3 this gives **|Q|=18+n_0+n_3>=18**. In particular a link
with at most17 quadruples cannot have three such leave pairs. For q=2,
no k=3 term exists; the pair equation gives n_2=4, the point equation
gives n_1=12, and |Q|=16+n_0. No finite classification, symmetry,
solver or completeness bridge is used in this lemma.

[positive16.json](positive16.json) is a literal16-quadruple packing
with two low-low leave pairs, so the two-pair lower16 is attained.
It is a validation control obtained by deleting three endpoint-avoiding
blocks from a credited existing nineteen-star fixture, not a new record
or a premise of the proof. The checker validates the actual packing,
every endpoint replication, and every covered/leave pair directly.

## Apply the lemma to the two hubs

For delta_ab=5-lambda_ab, partition the saturated points into A
(deficient only to u), B(only to v), T(to both), Z(to neither).
Let m=lambda_uv and C be the union of its disjoint three-point tails.
The published [tail-structure theorem8947](../two_unsaturated_tail_structure/PROOF.md),
source7b27b9c58b3e218172eaf9b1c0986d48e706e29b,
CIDbafkreibpwp36y6locnsu5gq3kmfx76w24uthxkvuwslgcclnluzlkh5h7e,
gives |Z|=m, Z contained in C, and bijective low-hub leave friendships
from Z to B intersect C at u and from Z to A intersect C at v.
Each pair has distinct endpoints in disjoint cohorts. At u, both B
and Z have link replication5; the friendship is precisely an uncovered
pair in that hub's shortened star. The same holds for A and Z at v.
Thus EACH hub link contains m disjoint low-low leave pairs.

Double counting point occurrences gives r_u+r_v=71*5-16*20=35.
Consequently the smaller hub has replication at most17. If m>=3,
choose any three of its disjoint low-low leave pairs. The marked-link
lemma forces at least18 quadruples there, a contradiction. Hence m<=2.
The credited [multiplicity-one exclusion8873](../multiplicity_one_exclusion/PROOF.md),
also explicitly included in8947, gives m>=2. Therefore **m=2**.
The earlier upper-four estimate of8947 is not used by this new upper.
The two inputs8947 and8873 now have the explicitly scoped independent
[review9027](../../six-reviewer-5/uniform-tail-audit/REVIEW.md),
sourcef82510e90fbb225aed45d7c833858618aafe2e35,
CIDbafkreiduecljsrdxvopw3n7ije7tu6ol2zoas5dby7bo3ze2paasebjabi.
That verdict is credited to six-reviewer-5, independent reviewer.

## The two tails and exact link inventories

There are two disjoint three-point uv tails, with |A intersect C|,
|B intersect C|,|Z| all equal2 and T intersect C empty, by8947.
A Z point's two friends lie in A intersect C and B intersect C,
respectively, and both lie OUTSIDE its own uv tail. Otherwise the
corresponding triple with u or v would be covered by that uv word,
contradicting its leave-friend definition.

If one tail had two Z points, their four distinct A/B friends would
all need to fit in the other three-point tail, impossible. Hence each
tail has one Z. If both A points lay in one tail, the Z in that tail
could not have an A friend outside it. Thus each tail has one A;
the same argument applies to B. Both tails have exactly the roles ABC.
Each Z's A and B friends are consequently the corresponding points
in the other tail. This reasoning uses m=2 explicitly; it is not an
extra normalization or a hypothesis for multiplicities3/4.

At u the low points are exactly B union Z: v has replication2 in
its shortened star, while A/T have positive u deficit. Every covered
B point and Z already has its specified low leave partner by8947.
For B points outside C, uvb is uncovered, so their unique low-point
leave neighbor in the u link is v, which is high. There are therefore
exactly two low-low leave pairs, the matched covered B/Z pairs.
Swap A/B and u/v for the other hub. Apply the q=2 identity to obtain
the stated counts4/12/(r_h-16). As the unordered hub replications are
16/19 or17/18, the two endpoint-avoiding counts are respectively0/3
or1/2. These are necessary inventories, not claimed realizable codes.

## Ordinary transfer to the complete local theorem

This section applies directly after8947, before using the new m=2 count.
The complete **local** good-cohort/Z theorem9045 is by
**six-code-3, researcher**, sourcee2f9cc128036b909d4d45a88ba2c5b72f1db8e2d,
CIDbafkreibbg6tgxgvjladb7wbd2kiikbiokwqlbx5y3uamx5hc7u2tvh6h4y;
see its [full statement and proof](../../six-code-3/good_cohort_z_interfaces/PROOF.md).
For an arbitrary packing of five-subsets on18 points, it assumes distinct
x,y,u,v with the following four properties:

1. r_x=r_y=20, lambda_xy=4, lambda_xv=5, and vxy uncovered.
2. lambda_xu is3 or4, all other lambda_xp are4 or5, and u is isolated
   in the x-star leave induced on its deficient link points.
3. lambda_yu=lambda_yv=5 and every other lambda_yp is4 or5.
4. For t outside{x,y,u,v}, lambda_xt=lambda_yt=4 implies xyt covered.

It concludes lambda_xu=3 and |F|<=64. No m, other point replication,
whole-code symmetry or ambient profile is one of its hypotheses.

By8947, |Z|=m>=2, so choose any y in Z. Its v-leave friend is a
covered A point x, and x,y,u,v are distinct. Thus x,y are saturated,
lambda_xv=5, and vxy is uncovered. The friend x is high in the y link:
otherwise that uncovered pair would be low-low, contrary to the
universal saturated-star theorem imported by8947. Since X=0, every
saturated pair has multiplicity4 or5; therefore **lambda_xy=4**.
This proves property1.

The covered cohort point x is good in the exact sense of8947. Its own
deficient hub u is isolated in its high leave; its saturated deficit-
support degree is3 or4, so delta_xu=2 or1 and lambda_xu=3 or4.
The opposite hub v has multiplicity5, and all saturated neighbors
have multiplicity4 or5 by X=0. These are exactly property2. In
particular isolation concerns only deficient link points, not every
leave neighbor of u. No stronger isolation is inferred.

As y is in Z, lambda_yu=lambda_yv=5. The X=0 conclusion gives
lambda_yt in{4,5} for every other saturated t, proving property3.
Every t outside{x,y,u,v} is saturated under our exact two-hub hypothesis.
If lambda_xt=lambda_yt=4, then all three pairs of{x,y,t} have deficit1,
including lambda_xy=4. An uncovered xyt would consequently be a wholly
saturated uncovered deficit triangle. The R=0, tau=0 conclusion of8947
forbids precisely that triangle. Thus xyt is covered, proving property4.
Triangles contained in words are allowed; the argument does not forbid
every triangle of the deficit-support graph.

All four local hypotheses now hold. The conclusion **|F|<=64<71** is
a contradiction. This proves the entire two-unsaturated family exclusion.
The argument works for all m>=2 supplied by8947 and imports no placement
of y's other low-hub leave friend in a particular visible uv tail.
It requires neither our m=2 hand count nor a whole-code automorphism.

## Scope of the finite input and its intake

The explicit proof boundary is9045's complete local theorem, not an
exploratory seed list. It consumes the reviewed generic23-star coverage
8933 conditional on universal8323, and the two literal seed caps8967.
Its public [BRIDGE.json](../../six-code-3/good_cohort_z_interfaces/BRIDGE.json)
contains all34 actual compatible maps **before** triangle screening.
Its14/878 raw markings have2/180 checked subgroup orbits,360 products,
933120 partial maps and all5598720 full relative maps. A separate
point-DFS checks the same complete domain. No subgroup is asserted full
and no subgroup quotient is an ambient-code symmetry assumption.

Exactly32 of those raw unions violate property4, with45 actual witnesses;
the remaining two complete36-word unions are the literal8967 seeds,
with upper61/64 under their two final degree20 hypotheses. The candidate
universes and proper25/28-color certificates are published there. Their
color bounds are not optimality or attainment claims. The finite theorem's
normalization, group transport and carrier completeness are unformalized;
its author's separate algorithms are not independent review.

For intake here, all34 actual point maps and word arrays were compared
to the saved earlier exploratory inputs. Twenty-six match directly.
The other eight use a different representative of fixture17's first
mark: the explicit coordinate permutation

```
(16,7,10,15,1,2,4,6,12,5,9,13,11,8,14,0,3,17)
```

preserves all20 literal first-star blocks, fixes center17, and sends
(u,v,y)=(14,4,8) to(14,1,12). After that actual point transport, every
map and36-word array matches entrywise. Direct set checks reconstruct
all45 triangle witnesses and match both surviving words and center
images to8967. This corroborates the import boundary; it does not
replace9045's exhaustive coverage premise or supply a new independent
review. No full carrier or coloring search is repeated here.

## Evidence and limits

The ordinary proof above supplies the negative inference. [verify.py](verify.py)
checks the marked-packing identity on the literal positive control and
rejects malformed/incorrect local data, in normal and optimized Python.
The credited original census is used solely to identify that one
positive fixture; neither its completeness nor its enumeration is
needed for this proof. [DEPENDENCIES.json](DEPENDENCIES.json) fixes the
three actual mathematical inputs and all compact-data provenance.

The8716/8947 predecessor distinction is explicit: this proof imports
8947's uniform tail assertions, not8716's old global16/19 structure or
its repaired heavy-edge step. The reviewed local8783 obstruction is
only an ancestor within8947's stated premises. The independent9027
verdict is now recorded for the entire8947 structure and lower8873.
It does not audit the new9045 carrier, our new marked-link lemma or
this ambient composition. Those new stages retain their stated review
and formalization limits.

The remaining research frontier is other size71 replication profiles.
No all-size71 or upper70 conclusion follows from this two-hub exclusion.
The external table and classical69 construction remain credited in
[DEPENDENCIES.json](DEPENDENCIES.json); their reproduction is validation,
not new research. Resource guards remain unchanged, computations serial,
and numerical-library threads one. A timeout, UNKNOWN, memory kill or
incomplete carrier would supply no nonexistence premise.
