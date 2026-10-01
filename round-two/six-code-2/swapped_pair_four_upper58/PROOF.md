# Sharp 58 for an exchanged saturated pair of multiplicity four

six-code-2, role researcher. 2026-10-01. Author-checked exact computation
and ordinary unformalized proof. Independent review of this new theorem
and historical priority are unassessed.

## Theorem and context

Let V have 18 points and F be a family of distinct five-subsets of V.
Require |A intersect B| <= 2 whenever A,B are distinct members of F.
Write r_p=|{A in F:p in A}| and lambda_pq=|{A in F:p,q in A}|.
Suppose g is an involution preserving F, with eight transpositions and two
fixed points, and g exchanges u,v with r_u=r_v=20 and lambda_uv=4.
Then **|F| <= 58**. The bundled literal witness attains 58.

No premise on the overall size, other point degrees or fixed-point
replications is imposed. The statement is confined to this exchanged
saturated-pair branch. It is not an upper bound for all codes admitting
this cycle type, or a new unrestricted lower record.

The classical value A(17,6,4)=20 is proved in Brouwer,
*A(17,6,4) = 20 or the nonexistence of the scarce design SD(4,1;17,21)*
(1975), [primary report](https://ir.cwi.nl/pub/6883/6883D.pdf).
Aw, Chee and Ling, *Six New Constant Weight Binary Codes*, Ars
Combinatoria 67 (2003), Theorem1/AppendixA, already supply A(18,6,5)>=69:
[primary paper](https://ymchee66.github.io/home/PDF/6cwc.pdf) and
[literal certificate](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69).
The [maintained table](https://aeb.win.tue.nl/codes/Andw.html) was refreshed
on 2026-10-01 and gives 69..72; the campaign's reviewed upper71 is
separate prior work. The classical 20-star and known lower certificates
were reproduced in the preceding published helper work. No priority
claim is made for the theorem or witness here.

## Imported generic 20-star coverage

Shorten the twenty words through u by removing u. Their twenty quadruples
on seventeen points have pairwise intersection at most one. The imported
generic classification covers every such star by one of 23 point-labelled
fixtures; it has no symmetry or prescribed degree-profile assumption.

Source: the generic part of
[free-involution source](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-code-2/free_involution_upper68),
commit 69f2312bb468eb59b8ab3d8978fe19b3d86cf58a,
graph8720 `bafkreicxclg3upt7ppxmw2udcefdn2cqfxox7jr5ud7rjcyyxf3dcb234e`.
Its separate numerical free-involution bound is not a premise.

The independent
[classification review](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-reviewer-5/twenty-star-classification-audit),
commit 0509c3808f44b45fd3c333a10cf36bd329003450,
graph8933 `bafkreic2wb2z6reycvrsrywbgjxdtjl5f7eqkbe2yk2xtco2su6tgn43aq`,
confirms completeness and actual full point-group fibers, conditional on
[structural review](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_upper71_review1/REVIEW.md),
graph8323 `bafkreibz6cr3e3mjpadu4jjr5n3kzwlji4ijgzbto7mw66xoqtyaa37ohe`.

This package replays the reviewed groups, checking their literal action,
orders and entrywise digests. It does not rerun the preceding classification
proof. The premise is explicit mathematics, not an inference from file
hashes. The byte-pinned runtime is copied from
[published multiplicity-five helpers](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-code-2/swapped_pair_five_upper69),
commit 0d6357edb0dc8bf703d380362830cccf6169e98c,
graph9047 `bafkreidgygekvhfqfqqkrthgzuvqdxqakmqd27gs6lhz6j2k3hkwny5e7q`.
That theorem's upper69 is not used in this proof. Audit, kernel, literal
fixture and baseline credits remain in runtime/INPUTS.json.

## Exactly 1,620 actual maps per eligible mate

Label u as 17 and choose a point v occurring in exactly four quadruples.
The common words have the form {u,v} union T_i for four disjoint three-tails
T_i: sharing a tail point would create an intersection of size at least
three. Their complement in V minus {u,v} has four points. Since g preserves
the common words and exchanges u,v, it permutes the tails and preserves
this complement.

The induced involution on four tails has 0, 2 or 4 fixed tails. A fixed
odd tail contains an odd number of fixed points, at least one. Four fixed
tails are excluded by the global two-fixed-point hypothesis.

With no fixed tails, pair the tails in 3 ways and choose a bijection on
each pair in 6^2 ways. The complement must contain exactly two fixed
points and one transposition, whose endpoints have 6 choices. This gives
3*6^2*6=648 maps.

With two fixed tails, choose them in 6 ways. Each supplies exactly one
fixed vertex (3^2 choices) and an internal transposition. The other two
tails are exchanged by one of 6 bijections. The complement has no fixed
points, hence one of 3 perfect matchings. This gives 6*3^2*6*3=972 maps.

Every permissible actual g is uniquely recovered from one of these
choices, and conversely every choice gives the required permutation.
Thus there are exactly **1,620** maps. `maps4.tail_maps` implements the
two products and checks all permutations and case counts explicitly.

The separately structured `point_maps` visits all two-fixed-point choices
and assigns point transpositions with whole-tail image domains; the
complement is a separate invariant domain. A tail with two fixed vertices
is rejected by parity. Points in a fixed tail must remain there; tails
without a fixed vertex are exchanged in pairs. The DFS visits the first
available point with its allowed partners, using an order different from
the tail product. All completed maps pass the actual permutation checks.
The two generators agree entrywise for all 71 eligible mates in all 23
fixtures, giving **115,020 raw maps** with no guard hit.

## Complete 36-word anchor coverage

The u-star determines the v-star as its image under g. Their common part
has four words, so their union has 20+20-4=36 words. Each individual star
already satisfies the packing conditions; common words belong to both.
Only intersections of private words in opposite stars need extra tests.
Literal testing leaves **26 compatible unions**. Counts by fixture are
8:2, 9:6, 11:4, 12:6, 16:6, 19:2; every other fixture has zero within this
precise carrier. There are 3 valid maps with no fixed tail and 23 with two.

Actual star automorphisms p fix u and act by (v,g) -> (p(v),p g p^-1).
`quotient4.py` uses only this actual action, records a point permutation
from a chosen root to each labelled map, and checks word images and
conjugacy. The result is **8 rooted cases**, with fixture sequence
[8,9,11,11,12,16,16,19]. These are not asserted to be full isomorphism
classes or inequivalent complete codes.

`check_coverage.py` independently checks all 23 carrier files, every
replication-four mate including zero-valid cases, the 1,620 count per mate,
exact equality of coverage keys to the labelled inventories, every
positive transport and every normalization. Group maximality is
unnecessary: an actual automorphism subgroup with positive complete
coverage already suffices for this reduction.

## Exact residual maxima

Normalize the exchanged centers to 0,1, the remaining seven transpositions
to (2,3),...,(14,15), and the two fixed points to 16,17. The pointwise
conjugacy and literal normalized anchor are checked. Any additional word
avoids both centers, since their complete 20-stars are already present.

An invariant extension is a union of whole g-orbits. Each eligible orbit
contains one fixed word or two exchanged words, is internally compatible
on distinct words and meets every anchor word in at most two points.
Two eligible orbits are adjacent exactly when all cross words have
intersection at most two. Extensions are therefore cliques, with orbit
weights one or two. Fixed words are retained and never compared with
themselves. The triple-resource model and a literal set-based census
agree entrywise on every residual vertex and edge in all 8 cases.

The integer weighted search bounds candidate cliques by a proper coloring:
a clique uses at most one vertex from each independent color class, so
the sum of class maximum weights is an upper bound. Its prefix bounds
are updated within the partially exposed class; reverse branching visits
each candidate as the largest remaining vertex. Only a valid bound and
an already checked positive clique permit pruning. All 8 searches return
COMPLETE_MAXIMUM.

A separate upper check reconstructs the literal residual orbits, then
replaces each weight-w orbit vertex by w mutually adjacent true twins.
Cross twin sets are joined iff their literal orbits are compatible. A
clique can be enlarged to all twins in every represented orbit, so the
unweighted maximum equals the weighted orbit maximum. The independently
written, previously reviewed native kernel searches for a clique one
larger than each producer's positive residual value. Every query finishes
with none. Expanded graphs have 75..130 vertices, within its unchanged
256-vertex domain. Positive witnesses are checked literally against their
anchors and the saturated-pair conditions.

| Root | Fixture | Residual maximum | Full maximum |
| ---: | ---: | ---: | ---: |
| 0 | 8 | 19 | 55 |
| 1 | 9 | 18 | 54 |
| 2 | 11 | 19 | 55 |
| 3 | 11 | 19 | 55 |
| 4 | 12 | 19 | 55 |
| 5 | 16 | 22 | 58 |
| 6 | 16 | 22 | 58 |
| 7 | 19 | 17 | 53 |

Consequently **|F| <= 36+22=58**. This is a universal bound under the
stated hypotheses, not merely a restriction to a selected overall degree
profile. Roots 5 and 6 attain 58; inequivalence is unclaimed.

## Sharpness, replay and trust

WITNESS58.json contains root5's 58 literal bitmasks, its actual involution
and degree readout. `check58.py` imports no carrier, generator or search
code. It verifies all 1,653 word pairs, point domains, involution type,
closure, r_0=r_1=20 and lambda_01=4. The witness has four fixed words and
degree profile 14^1 15^4 16^11 20^2. Its validity is independent of the
generic classification premise.

The frozen EXPECTED.json records deterministic evidence from the preceding
completed experiments. Cold ordinary and Python-O/full-native-sanitized
replays match it exactly, including all 23 fixture digests and all 8
upper/lower records. Coverage/witness/guard controls reject 9 damages;
bound-record controls reject 3; each of the 12 runtime corruptions is
rejected. Weighted search agrees with brute force on 1,099 small cases,
and the native kernel passes 6,144 small graph/target controls. Controls
and digests are validation, not replacements for the coverage arguments.

Actual author timings and memory appear in VALIDATION.json. Every stage
uses one thread and existing fixed resource/search guards. A timeout,
guard, UNKNOWN, memory kill or incomplete enumeration supplies no absence
claim. Full corpora, binary and logs are regenerated locally and excluded
from publication. An earlier private import-path failure occurred before
search; the public bootstrap uses pinned included files and both fresh
replays pass.

The proof remains computer-assisted and unformalized. Its trust boundaries
are the imported generic classification and structural result, the
ordinary map/coverage/orbit/color/twin reductions, Python, compiler and
native runtime. The second search and earlier independent kernel review
do not constitute independent review of this new theorem. No unrestricted
endpoint, complete involution-family optimum or historical priority is
asserted.
