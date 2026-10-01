# Sources, dependencies and claim boundaries

Actual author **six-tammes-1**, role **researcher**, 2026-10-01.
Assigned family: Tammes problem for fifteen points on the unit sphere.

## Primary literature and current table

[Musin--Tarasov, Enumeration of irreducible contact graphs](https://arxiv.org/abs/1312.5450),
Proposition4.1, is credited for the classical convex spherical T/Q corner
relations. Their [N14 paper](https://arxiv.org/abs/1410.2536) proves a
separate cardinality, not N15. The local relations used here are rederived
in PROOF.md, under its explicit embedding and completeness hypotheses.

The live [Cohn table](https://cohn.mit.edu/spherical-codes/) and
[spherical-code table](https://www.spherical-codes.org/) were refreshed
2026-10-01. The dimension3,size15 row is unstarred and retains cosine
0.59260590292507377809642492233276 and quintic
`13c^5-c^4+6c^3+2c^2-3c-1`. The current
[fifteen-point coordinate file](https://spherical-codes.org/data/3/15)
has890bytes,15lines,SHA256
`1b77ee43d73613885d3fdcfb03dc8fad2e40302ff9c9ff639559cc9b326fb805`.
The refreshed Cohn page SHA256 is
`829afd7ef3789ad9dacd90d935f96754525a94f23c3f40403a4648a30bff563d`.
Coordinates are contextual prior art and are not proof inputs.

The current [Musin distance-distribution preprint](https://arxiv.org/abs/2309.13854v3),
revised2026-09-27, studies three/four-point SDP distance restrictions;
its stated main example is the dimension-four24-cell. The current
[Kuznetsov--Sahinidis global-optimization article](https://www.sciencedirect.com/science/article/pii/S0166218X26002982)
states recovery of established Tammes cases up to13points in its abstract.
Neither source supplies a global N15 solution. These are bounded primary
checks, not a guarantee about unlocated literature or historical priority.
The known incumbent and classical formulas are not new results here.

## Exact campaign dependencies

- [Odd-degree restriction7817](https://github.com/helgithorskarp/math_results/blob/main/tammes15_nine_quad_odd_degree_reduction/PROOF.md),
  source `d6547391ae745a70087f067568047c8dbba0e099`, artifact
  `bafkreic6shrttfdlf7vbae5wye7eytruyxeeb7j6422ubytjcwlaadlkfa`.
  Its `n3=n5<=3` supplies the at-most-two corollary. Its local corner,
  deficit and three-contact facts are credited and rederived here.
- [Local QQ facts7912](https://github.com/helgithorskarp/math_results/blob/main/tammes15_nine_quad_single_three_fan_reduction/PROOF.md),
  artifact `bafkreicjxhbyqcxdeplfvby6k2bysmhhk7fbksapoenneqsigtfos2dulu`.
  Its deficient-five QQ-to-three fact is prior mathematics. The unique-
  three lemma and parameter collar in its later sections are not imported.
- [All-three-ordinary case8881](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/three-ordinary-fives/PROOF.md),
  source `be03a995eeb5775792de6f9ecabdf050c6339ed5`, artifact
  `bafkreih62rkoiqikzku3z5spgdrjs5gd24po4x2bluefyh7umzcbhlzaii`.
  This exact full-interval statement supplies the sole missing k=3 case.
  The new zero/one/two-ordinary arguments do not import its fan theorem.
  The newly published [independent incidence audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/incidence-audit/REVIEW.md),
  actual author six-reviewer-3, graph8953
  `bafkreid4wwif27qam7uovxjgwklyqe7guki55nwjs5uzpy7ppqvw476sfm`, source
  `ac895797cfcd1c04ba37d727c0bb9fe664160387`, verifies8881 within its
  explicit contact-map hypotheses and proves a wider cosine interval.
  Its verdict is specific to8881 and is not transferred to this proof.
- [Committed beta catalogue8360](https://github.com/helgithorskarp/math_results/blob/main/tammes15_one_triangle_four_exclusion/PROOF.md),
  source `8e69194e595ae7411d3624537473870f67ff79c8`, artifact
  `bafkreicjsndjhrckpkt2flkpfa7pawhzyb6k4k6xpecudodmdmfvqb2aue`.
  Only the10-profile corollary imports this21-row list, retaining **all
  its hypotheses and dependencies**. Its original list derivation is not
  newly verified by deleting rows. Its beta is the root in(119/200,3/5)
  of `1+4c+2c^2-4c^3-11c^4-24c^5`. That beta is not a premise of the
  new full-interval exclusion.

The fixture freezes8360's [21 rows](https://github.com/helgithorskarp/math_results/blob/main/tammes15_one_triangle_four_exclusion/EXPECTED.json),
SHA256 `f5b06870bae78981393afeb38600a3fd9742b376d7a5cb7b26eed3ad49e45cf2`.
They are split0/10/11 for r=1/2/3. Excluding r3 removes11 and leaves10
r2 rows. The later [18-row public source](https://github.com/helgithorskarp/math_results/blob/main/tammes15_two_ordinary_fives_exclusion/EXPECTED.json),
source `6dffbb940c10f415b71e275a45010a7141d1ee4e`, SHA256
`f376a4cdebfad5e8d0e3eef5e52e7755ee0a151c25148e3695b639d9b425944a`,
has0/7/11 rows. Under its additional source hypotheses it leaves7 r2
rows. Its intervening source-only/rejected registrations are not made
committed by this citation. Pinned original bytes were compared with
current published bytes before publication. Neither list is a census of
all embedded maps or all spherical codes. The new r3 theorem uses neither.

## Complementary current work and unresolved coverage

[six-tammes-2's negative-cross-edge reduction8929](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/negative-cross-reduction/PROOF.md),
source `a0707173b61f1e6071ebd737560db38ce9352555`, artifact
`bafkreidzzrxf4edknxz5eufgjactm7im7xsflongddahytmrrkk2ntueii`, leaves
one quartic equal-contact candidate curve for the specified23-edge core.
Two-point extensions and global motif occurrence remain unresolved there.
Its proof and current report were read; it is context, not a premise here.
No review of a different core is transferred to it or to this proof.

The new mathematics is the complete zero/one/two-ordinary incidence
reduction and its two actual-link terminal contradictions. The r3 branch
is thereby empty once8881 is imported. Author checks are ordinary written
proof plus complementary same-author exact programs, not proof-assistant
certification or an independent verdict on the new branches.

Next: the remaining r2 T/Q rows, actual larger faces, isolated/lower-degree
vertices and a justified unrestricted optimizer domain. An exact contact
profile is useful pruning, not global Tammes-15 optimality. No numerical
packing record or historical priority is claimed here.
