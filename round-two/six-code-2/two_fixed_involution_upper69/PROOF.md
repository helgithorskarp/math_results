# Sharp 69 for packings admitting a two-fixed-point involution

six-code-2, researcher. 2026-10-01. Author-complete computer-assisted
proof, with ordinary unformalized bridges and explicit mathematical
imports. Independent review of this joint result and historical priority
are unassessed.

Let F be distinct five-subsets of an 18-point set, with |A intersection B|
at most two for distinct A,B. Let g preserve F and have cycle type 2^8 1^2.
Write r_p for the number of words through p and lambda_pq for the number
through both p,q. **Then |F|<=69, sharply.** No overall degree profile,
saturation or pair-multiplicity premise is added to this statement.

## Ordinary reduction covering every such packing

The classical A(17,6,4)=20 implies r_p<=20 by shortening through p.
If all 16 moved points had degree at most19, then
5|F|=sum r_p<=16*19+2*20=344, so |F|<=68.
Thus |F|>=69 forces a moved point u with r_u=20; invariance gives
v=g(u) distinct from u and r_v=20. Common words through u,v have disjoint
three-element tails on the other16 points, hence lambda_uv<=5.

All possible multiplicities have the following sufficient upper bounds:

| lambda_uv | Bound | Exact imported or new scope |
| ---: | ---: | --- |
| 0 | 56 | arbitrary saturated absent pair; review7747 |
| 1 | 58 | deletion and arbitrary (20,19,1) upper57; 7825/review8026 |
| 2 | 60 | arbitrary saturated multiplicity-two pair; review8080 |
| 3 | 56 | new exchanged-pair lemma below |
| 4 | 58 | published exchanged-pair lemma9089 |
| 5 | 69 | published exchanged-pair lemma9047 |

For lambda1 there are19 words containing v but not u. Delete any one:
the resulting packing has r_u=20,r_v=19,lambda_uv=1 and at most57 words,
so |F|<=58. The imported57 applies to arbitrary packings; the deletion
need not preserve g. Sharpness of this convenient58 bound is unclaimed.

For |F|>=70, the capacity argument supplies an exchanged saturated pair
and every table row contradicts the size. Therefore |F|<=69. At equality,
**every moved degree20 point has multiplicity5 with its mate**. This is
an equality condition, not a classification of all attaining codes.
No two-fixed-saturated obstruction or prescribed replication profile is
needed for this argument.

The already published one-cap Steiner69 construction is preserved by
g=(0,1)(2,3)...(14,15), fixing16/17. Its included unchanged literal
certificate and standalone checker establish sharpness. The checker
tests all2,346 distinct word pairs, actual involution type and closure.
The construction, C4 symmetry and lower69 are credited to9047 below;
they are not new unrestricted lower records here.

## New sharp56 lemma for multiplicity three

Assume additionally g exchanges u,v with r_u=r_v=20,lambda_uv=3.
**Then |F|<=56, sharply**, with no other degree or size premise.
Shortening the u-star gives twenty quadruples on17 points with pairwise
intersection at most one. The imported complete generic classification
places every such star in one of23 fixtures. No symmetry of that single
star, nor any special point-degree profile, is assumed.

The three common words are {u,v} joined to three disjoint three-tails;
their complement has seven points. The involution on the three tails has
one or three fixed tails. Each fixed odd tail contains a fixed vertex,
so three fixed tails are impossible with only two global fixed points.
The single fixed tail contains one fixed vertex and an internal pair.
The other two tails are exchanged by a bijection. The odd complement
has exactly one fixed vertex, with the remaining six points paired.
Consequently each mate has exactly
3*3*6*7*15=**5,670 actual maps**, each uniquely recovered from these
choices and each giving the stated involution. `maps3.tail_maps` checks
these choices. A separately ordered point/domain DFS visits all choices
of the two fixed vertices and all allowed transpositions; whole-tail
image constraints and complement invariance are enforced. Its maps agree
entrywise with the product generator for every eligible mate.

All23 fixtures have13 eligible multiplicity-three mates, yielding73,710
maps. The v-star is the image of the u-star; their union has20+20-3=37
words. Literal private-star cross checks leave44 compatible unions:
fixture6:24,7:4,8:4,10:12, zero in every other fixture in this carrier.

Actual point automorphisms p of the u-star act by
(v,g) -> (p(v),p g p^-1). The positively checked transports cover the44
labelled unions by nine roots, with fixture sequence
[6,6,6,7,7,8,8,10,10]. The independent coverage checker verifies exact
coverage-key equality, every mate including zero-valid cases, literal
word images, conjugacy and normalized anchors. Group maximality is not
needed: actual subgroup transports with complete positive coverage suffice.
The nine roots are not asserted full-code isomorphism classes.

Normalize u,v to0/1, the remaining pairs to(2,3),...,(14,15), and fixed
points to16/17. Every further word avoids the saturated centers. An
invariant extension is a union of whole g-orbits, each of weight1 or2.
Eligible orbits are internally compatible and compatible with all anchor
words; fixed words are retained. Two vertices are adjacent exactly when
all their cross words meet in at most two points. Thus extensions are
weighted cliques. The triple-resource census and separate literal
set-based orbit/edge checks agree entrywise at every root.

Weighted search uses proper-color upper bounds: a clique uses at most
one vertex per independent color class, hence the sum of maximum class
weights bounds its weight. Reverse branching, prefix class bounds and
positive witnesses yield COMPLETE_MAXIMUM for every root.

A separate upper search reconstructs literal orbits and replaces an
orbit of weight w by w mutually adjacent true twins, joining cross twin
sets precisely on literal compatibility. A clique can be enlarged to
all twins of each represented orbit, so the unweighted maximum equals
the weighted one. The previously independently reviewed native kernel
finds no clique one larger than each positive residual maximum. All nine
queries complete, including all cases under ASAN/UBSAN; expanded graphs
have51..84 vertices, within the unchanged256-vertex cap.

| Root | Fixture | Residual maximum | Full maximum |
| ---: | ---: | ---: | ---: |
| 0 | 6 | 19 | 56 |
| 1 | 6 | 19 | 56 |
| 2 | 6 | 19 | 56 |
| 3 | 7 | 18 | 55 |
| 4 | 7 | 17 | 54 |
| 5 | 8 | 18 | 55 |
| 6 | 8 | 19 | 56 |
| 7 | 10 | 18 | 55 |
| 8 | 10 | 15 | 52 |

Thus |F|<=37+19=56. Root0 attains it. WITNESS56.json has56 literal
bitmasks, its involution and degrees; `check56.py` imports no carrier,
generator or search code and checks all1,540 word pairs plus the exact
scoped hypotheses. Its profile is14^4 15^8 16^4 20^2 with two fixed words.
Witness validity does not depend on the classification premise.

## Exact mathematical dependencies and attribution

Classical point-cap20: Brouwer (1975),
*A(17,6,4)=20 or the nonexistence of the scarce design SD(4,1;17,21)*,
[primary report](https://ir.cwi.nl/pub/6883/6883D.pdf).
Aw, Chee and Ling, *Six New Constant Weight Binary Codes*, Ars
Combinatoria67 (2003),313–318, Theorem1/AppendixA supplies lower69:
[primary paper](https://ymchee66.github.io/home/PDF/6cwc.pdf).
The [maintained table](https://aeb.win.tue.nl/codes/Andw.html), refreshed
2026-10-01, retains69..72; the reviewed campaign upper71 is separate prior
work. The classical baseline and known literal69 certificate were
independently reproduced earlier and the included validators rerun here.
Bounded prior searches establish no historical priority for this joint
result or witness.

Generic23-star classification:
[source8720](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-code-2/free_involution_upper68),
commit69f2312bb468eb59b8ab3d8978fe19b3d86cf58a,
ref `bafkreicxclg3upt7ppxmw2udcefdn2cqfxox7jr5ud7rjcyyxf3dcb234e`.
Its separate free-involution bound is not a premise here.
[Independent classification audit8933](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-reviewer-5/twenty-star-classification-audit),
commit0509c3808f44b45fd3c333a10cf36bd329003450,
ref `bafkreic2wb2z6reycvrsrywbgjxdtjl5f7eqkbe2yk2xtco2su6tgn43aq`,
confirms generic coverage conditional on the reviewed no-low-low-leave
structural theorem8323:
[review](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_upper71_review1/REVIEW.md),
commit02c1569568854e575f8b176ea07d552737a7da84,
ref `bafkreibz6cr3e3mjpadu4jjr5n3kzwlji4ijgzbto7mw66xoqtyaa37ohe`.
Audit and native kernel credits are preserved in runtime/INPUTS.json.

Low-multiplicity premises, with their full arbitrary-packing scopes:

* [Absent-pair review7747](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_absent_pair_review1/REVIEW.md),
  commitcf3cab455baeab79e0ba17dc9bf5e0bfb4f7f022,
  ref `bafkreic5krg2bwpfeewirdhqq2vxs76xdkwmx2br7rtolhtb56vr55hsla`:
  r_u=r_v20,lambda_uv0 gives upper56.
* [Pair-two review8080](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_pair_two_review2/REVIEW.md),
  commit33143b38349e8db1bb645770a98aac83438b4517,
  ref `bafkreie5zvwwz4ttdg35mmbiwxn4tdxx67wse7si7wyky4wxix2lir2ib4`:
  r_u=r_v20,lambda_uv2 gives upper60, importing upper57 explicitly.
* [20/19 single-pair lemma7825](https://github.com/helgithorskarp/math_results/blob/main/coding_theory/a18_6_5_twenty_nineteen_single_pair/PROOF.md),
  commitd1ec84bc52bbe7fc05e1806a2122674d612b456c,
  ref `bafkreidblmx7qa77knvtwvulu76avze5ruh454nkwf6fslzcoo42ox5jjm`:
  r_u20,r_v19,lambda_uv1 gives upper57.
  [Independent confirmation8026](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_twenty_eighteen_review2/REVIEW.md),
  commit45d1c6acf5a7acd86fa4eba942d5376d6753ee91,
  ref `bafkreignqprv3lftlnz3ysxjbfspqeokqnngldny2vaqvz67tfr2ivvfia`.

Published exchanged-pair premises under this actual involution:

* [Multiplicity-four sharp58/9089](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-2/swapped_pair_four_upper58/PROOF.md),
  commita70013740de126fe482870dcc6c162a292b042e9,
  ref `bafkreiattty3vpep7okylf5ljycwo6xazk37kipsqpgvxymnligtmhnd5m`.
* [Multiplicity-five sharp69/9047](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-2/swapped_pair_five_upper69/PROOF.md),
  commit0d6357edb0dc8bf703d380362830cccf6169e98c,
  ref `bafkreidgygekvhfqfqqkrthgzuvqdxqakmqd27gs6lhz6j2k3hkwny5e7q`.
  The broadened numerical upper69 generalizes that upper-bound component;
  the earlier construction and C4 family are credited without generalizing
  their separate construction statement.

The fresh prepublication refresh found
[independent review9115](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/swapped-five-audit/REVIEW.md),
commitb701fed831d85c668c7c0d92281ff3e8db052216,
ref `bafkreiemrxuubxmom7bjx5zasuiardzgz2ezt4qwudwez4ysjf2b2quw2q`.
Its independently generated complete map cover, literal completion graphs
and Python maximum searches confirm9047 at the same generic8933/8323
premises. It also confirms the standalone construction and gives a broader
ordinary one-cap omission census. That review does not review9089, the
new multiplicity-three lemma, or this whole-family reduction. Its review
status is not transferred to this new joint result.

The joint result depends on all these bounds; its new multiplicity-three
lemma requires only the generic classification/structure, not earlier
numerical sharp58 or sharp69. Included copied runtime code is credited
separately from mathematical dependencies.

## Replay and proof boundary

EXPECTED.json was frozen from preceding sealed experiments, then matched
by cold ordinary and Python-O/all-native-sanitized replays. These compare
all23 raw fixture bytes and all nine coverage/upper/lower records. The
three byte-pinned prerequisite validators are freshly completed in both
modes. The full upper57 census and earlier multiplicity-four/five and
generic classification censuses remain imported, not rerun by this bundle.

Actual commands, timings, memory and controls are in README.md and
VALIDATION.json. Every exception guard remains active under Python-O.
No timeout, incomplete enumeration, resource kill or failed process is
used as absence evidence. No resource/search guard was raised. Full
corpora and build products are generated locally and excluded from source.

The proof is unformalized and trusts the explicit imported mathematics,
ordinary map/coverage/orbit/color/twin/deletion/capacity reductions,
Python, compiler and native runtime. A second algorithm and earlier
independent kernel review do not independently review this new theorem.
This closes the stated involution family; other automorphism types and
codes without such an involution remain outside it.
