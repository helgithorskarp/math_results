# Joint contacts remove 85.309% of the current complete R(5,5) carrier

This is an exact computer-assisted reduction of a **globally covering carrier of labelled 43-vertex colorings**. No good43 graph, new task exclusion, or improvement of the Ramsey bound is claimed. The finite tables are established by two different exhaustive decompositions. Historical priority is not claimed.

## Complete family and declared gate

Use the ordered maximal-packing carrier of h3887, with the representative restriction of h4035 and its physical destination bridge h4045. Its 18 classes have q=7,8,9,10 monochromatic four-clique blocks, r red blocks (5<=r<=q), and an R(4,4) core of order n=43-4q. The root is red. The registry has 2,189,178 task IDs. Keep q7, q8 and q10 unchanged. In every q9 task, require the induced graph on each one of its nine blocks and its entire seven-vertex core to be R(5,5). Keep the **same two selected core edges and same augmentation rule** on red blocks as h4035.

The gate, recorded in `GATE.json` before computation, requires at least a factor-two reduction of the complete h4035 bare carrier, complete independent counts for all 362 seven-vertex cores, and physical rank/unrank. The result meets all three requirements. It is not a restriction to one labelled core or one input graph.

A *bare carrier* here imposes the fixed monochromatic blocks and core, the old two-block Ramsey domains, proper single-column stars, root column order, root block order, and the h4035 augmentation restriction. It does **not** yet impose every global five-set or maximality clause. Each remaining assignment is a complete physical coloring, often with a monochromatic five-set involving several blocks. Counting the carrier is not counting good graphs, distinct isomorphism classes, or SAT solutions.

Every good43 has an h4035 representative, physically supplied by h4045. That representative automatically obeys the added block/core conditions. Thus the new whole carrier remains globally covering. The added conditions are literal Ramsey consequences within each task; the augmentation restriction has the earlier global representative meaning. It must not be asserted as a Ramsey implicate of an arbitrary old task.

## Exact contact characterization

Let C be an R(4,4) graph on seven labelled vertices and B a red K4 with labelled vertices 0,1,2,3. Write the four red-contact rows as subsets A_0,...,A_3 of V(C). The induced graph on B union C contains no monochromatic K5 if and only if:

1. The intersection of all four rows is empty.
2. The intersection of any three rows is independent in C.
3. The intersection of any two rows contains no red triangle of C.

Indeed a red K5 using 4, 3, or 2 vertices of B gives exactly these three obstructions. A red K5 using at most one vertex of B would contain a red K4 in C. A blue K5 uses at most one vertex of B and would contain a blue K4 in C. Both are impossible. This proves necessity and sufficiency, not merely a relaxation. Complementing all colors gives the blue-block case.

There are 15^7=170,859,375 old red contact assignments: every core column is a proper subset of B. Let A(C) count those passing all three tests. For a blue block the count is A(complement C). `COUNTS.tsv` includes an explicit catalogue destination and a seven-vertex permutation for each complement. All 7,602 edge identities are checked; this is an isomorphism certificate, not an assumption of graph symmetry.

Let e,f be the first two edges of the lexicographically greedy red matching of C. Let z_e and z_f be the sets of block rows adjacent to both ends of e and f. In a locally valid contact, their sizes are at most two, by condition 2. The unchanged h4035 augmentation occurs precisely when z_e and z_f are complementary two-subsets of B: replace B by z_e union e and z_f union f. Define J(C) as the count of locally valid contacts without this augmentation.

The ordinary h4035 one-red-block count was 50,151*15^3=169,259,625. Here J(C) is counted **jointly** with all local Ramsey restrictions; no dependent probabilities are multiplied.

## Two complete finite counts

`row_count.cpp` enumerates a<=b<=c for the first three sorted row masks. For a subset s of C, precompute the sets of possible fourth rows d satisfying triangle-freeness of s intersect d, independence of s intersect d, or emptiness of s intersect d. Intersect these bitsets for the six pairs, four triples, and the fourfold intersection. Restrict d>=c. This enumerates every unordered multiset of four row masks exactly once.

Restore the labelled row assignments with 4!/product(multiplicity factorial). When d>c the weights for a=b=c, a=b<c, a<b=c, or a<b<c are respectively 4,12,12,24. When d=c they are 1,6,4,12. No quotient by block-row symmetry is taken. In particular all contact row labels remain available independently of the already ordered root/block matrix coordinates.

For J(C), classify each row by whether it contains e, f, both, or neither. The augmentation condition says exactly two rows have the e-only type and two have the f-only type. Remove exactly these choices. The program also writes cumulative labelled weights for each (a,b) bucket, giving the contact codec's exact rank partition.

`column_check.cpp` uses a different exhaustive decomposition. It assigns seven labelled core columns, each from the 15 proper subsets of B. A previously assigned core edge forbids any three block rows adjacent to both ends; a previously assigned core triangle forbids any two block rows adjacent to all three ends. The allowed last-column bitmask is summed exactly. A separately constructed table checks all six literal two-subsets of B for augmentation. The core-vertex assignment order is a deterministic degree order, with every column choice retained; there is no orbit pruning. It visits 3,602,604,842 partial assignments across all 362 cores. This checker never imports the row counter or its tables.

All 724 plain/joint counts agree entrywise. A(C) ranges from 108,386,957 to 154,083,631; J(C) from 107,922,365 to 153,193,945. Fourteen small complete cross-edge cubes, including a red-core triangle and a two-edge augmentation, are also compared against a definition-level enumeration of all monochromatic five-sets (164,369 assignments total).

## Exact complete-carrier effect

For a q9 task with r red blocks and core C put a=r-1, b=9-r, and

    M_r = binom(1998+a-1,a) binom(1931+b-1,b)
          * 37823^(binom(a,2)+binom(b,2)) * 35714^(a*b).

This is the unchanged h3887 matrix-coordinate count. The root coordinates are multisets with ties, not independent uniform root matrices. The contact coordinates remain independent of these matrix coordinates. Consequently the new per-task count is exactly

    M_r * J(C)^r * A(complement C)^(9-r).

The prior h4035 count for that task was

    M_r * 169259625^r * 170859375^(9-r).

Sum the new expression over all 362 cores and all r=5,...,9, leaving the other thirteen classes exactly unchanged. `check_counts.py` performs all arithmetic as integers and rational fractions, validates the pinned parent cardinalities, and checks the declared gate. `EXPECTED.json` records the complete exact totals and fractions.

| Measured set | Fraction removed |
| --- | ---: |
| Entire current h4035 bare carrier | 0.8530904627855127172519224538339276509304... |
| Its q9 portion | 0.8835995846143423732672877113380359211868... |
| Every one of the 1,810 q9 task carriers | Greater than 0.5924 |

The largest individual task retained fraction is 0.4075623258287522837026339074008940490524... . All 1,810 reductions are strict, and every new per-task count is positive. Thus **zero task verdicts** change.

An optional accounting consequence uses the existing h4001 exclusions and h4029/h4035 composite upper envelope. Its q9 term is the old exact q9 bare count; replacing only that term decreases this upper envelope by 0.8572715183985757721269295669095898481021... . This does not multiply dependent q8 restrictions or assert that the envelope is an attained count. The main theorem uses the exact complete bare carrier, without this optional envelope.

## Physical interface and validation

`contact_codec.py` ranks and unranks all **ordered labelled** contact rows by their sorted multiset and their lexicographic distinct permutation. The cumulative bucket boundaries and the explicit fourth-row bitset partition prove a bijection. The blue-block codec transports through the checked complement permutation and complements all contact colors.

For a full q9 graph, retain the original two multiset root coordinates and all ordinary block-pair coordinates. Replace its 63 separate star digits by nine contact digits with the exact sizes above. `PhysicalCarrier` converts these digits back to the original physical 903-edge representation using h3887. Its task parameter remains the original `bo1-q9-rR-cCCCCCC` identifier; **its integer code is a new contact-carrier index and is not an old bo1 code**.

Across all 1,810 tasks, first/middle/last indices give 5,430 physical round trips. The standalone checker imports no producer or parent code: it checks every fixed core/block edge, both root-order conventions, all two-block five-sets, all block/core five-sets, and the unchanged red augmentation condition. This includes 33,524,820 literal local five-sets. Another 10,860 contact round trips exercise bucket boundaries, repeated rows, and extreme indices. Out-of-range indices, malformed contact rows, changed census entries, false complement maps, altered prefix bytes, and changed fixed physical edges are rejected.

`classify.py` accepts a complete original q9 carrier graph and returns one of three honest outcomes. A local Ramsey violation carries a literal physical monochromatic five-set. A locally valid augmentation carries two disjoint red K4s and requests the existing h4045 redirect, subject to that bridge's original source checks, including red maximality. This local witness does not establish those additional source conditions. An admitted contact-carrier graph gets a new integer code. Admission is not a target verdict. Tests cover 724 monochromatic rejections and 362 augmentation redirects, one of each applicable type for every core.

Every positive physical test fixture has an independently checked global monochromatic five-set and is explicitly not a target. If the complete standalone clique finder unexpectedly finds none, the control stops with a request to preserve and invoke the target verifier; it cannot silently label such a graph as an ordinary failed fixture.

## Trust and limits

Dependencies are the h3887 global cover and matrix domains, the h4035 normal representative theorem, the h4045 physical bridge, and the pinned 362-record R(4,4;7) catalogue. h4045 independently checked catalogue coverage on all 2^21 labelled seven-vertex graphs; this pass does not recompute that parked result. As emphasized by the independent h4053 acceptance of h4045, completeness of the large order-11/order-15 catalogues and the original global cover remain inherited assumptions. The present finite computation assumes integer/bit semantics, SHA256 identity checks, and correct compiler/interpreter execution. It uses no floating-point inference, SAT answer, DRAT proof, or heuristic sample for its exact counts.

The full native census is checked in release and address/undefined-sanitized builds. Python checks run normally and with assertions disabled. The mathematical reduction is not formally verified. No claim of solver speedup, candidate success, new q10 closure, or historical novelty is made. h3987's 99 certified closures and 161 unknown children remain team-r55-1's unchanged ledger; h4001 separately remains 518 q7-r5 exclusions and 122 unknown tail cases.
