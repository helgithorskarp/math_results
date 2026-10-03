# H7 phase weights 11 and 33 require adjacent minority positions

Actual author **six-vdw-2**, actual role **researcher**, 2026-10-03.
This is an author-checked computer-assisted lemma with ordinary, unformalized
proof bridges. Separate producer and literal auditors are by the same author;
mode agreement and shared signatures do not establish independent-person review.

Let H7 = <3^88> in the multiplicative group of F617. Let
c:F617*->{0,1} be H7-invariant and assume that every nonconstant seven-term
field arithmetic progression avoiding zero contains both colors. Put
y_i=c(3^i), indexed modulo88, and f_i=y_i XOR y_(i+44), indexed modulo44.
Write K=sum_i f_i. At K=11 call the eleven positions with f_i=1 selected;
at K=33 call the eleven positions with f_i=0 selected.

**Lemma.** If K is11 or33, two selected positions are adjacent on the44-cycle.
Equivalently, the minority phase value has a cyclic run of length at least two.
No assertion of attainability or impossibility of either whole phase weight
is made. The nonconstant phase band11..33, the complete H7 family, the
unrestricted3704 coloring target and the exact W(2,7) remain unresolved here.

## Lossless reduction to72 conditional cases

Suppose instead that all eleven selected positions are isolated. Their eleven
positive background gaps sum to33. The complete
[parent lemma9948](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-phase-eleven-isolated-gaps/PROOF.md),
artifact `bafkreibc4zo5kmjkv6thbo6nvv5geelgwiimyphv5eicpechqp6jyplzd4`,
source `efae21794efc3e7da5d0a0dadd8be7650e8a15aa`, gives minimum gap1 and
maximum gap4 in this conditional family. Before these new helpers were
imported, its entire21370-byte original body, all14 initial directed
relations,15 signatures and29677-byte canonical SDK/RPC transaction with
DeliverTx0 were freshly bound, together with145 whole recursive public
source files. This is an ordinary cover dependency, not an unconditional
local rule transferred to other phase families.

Choose **any** maximum gap and multiply field coordinates by the power of3
at its preceding selected position. Multiplication is a bijection of F617*
and transports every zero-avoiding arithmetic progression to another such
progression. It translates f on the44-cycle, without identifying lower
colors or exchanging phase values. Thus selected positions0 and5, and
background positions1,2,3,4,6,43, can be fixed. The last two background
positions follow from isolation. All tied longest gaps remain in the cover.

A minimum gap1 supplies selected positions j and j+2 modulo44. Neither
endpoint can be one of the six fixed background positions. Directly this
leaves exactly

    j in {5,7,8,...,40,42}.

For each of these36 possibilities, isolation also forces positions j-1,
j+1,j+3 to be background. Retain both backgrounds b=0 and b=1, with selected
phase1-b. There are72 cases. No first-pair ordering, reflection, inversion,
free rotation quotient, common lower orientation, or independent phase
exchange is imposed. Every tied shortest pair remains in the cover.
Global color complementation preserves f and all avoidance conditions and
permits the sole color gauge y_0=0.

## Exact physical models

Keep44 independent lower color variables. At a fixed phase position i,
the upper color is lower XOR f_i; elsewhere introduce one independent upper
color and one phase bit, with the four exact XOR clauses. The case head fixes
the phase positions just listed. Let N be the number of free phase positions
and q the number of free selected positions needed to reach exactly11.

| pair start j | N | fixed selections | q | counter levels | variables |
|---|---:|---:|---:|---:|---:|
|5,42|34|3|8|9|382|
|7,40|32|4|7|8|336|
|8..39|31|4|7|8|326|

For each prefix r of the free phase bits, T_(r,k) means that at least k
are selected. Use k=1,...,min(r,q+1), T_(r,0)=true and absent positive
thresholds=false. Four clauses encode exactly

    T_(r,k) = T_(r-1,k) OR (selected_r AND T_(r-1,k-1)).

The two final units T_(N,q) and NOT T_(N,q+1) enforce exactly q selections.
Induction over r proves the threshold meaning. There are
(q+1)N-q(q+1)/2 cells, and therefore44+(q+3)N-q(q+1)/2 variables.
The independent auditor verifies every local gate over its entire truth
table and checks every counter clause and both final units.

Every case retains all44 clauses forbidding two adjacent selected positions
and all44 length-five windows requiring a selection. These are **conditional**
isolation and maximum-gap constraints. The normalized head itself exhibits
a gap4. Numerical constraints are only all zero-avoiding field AP7s and
the previously universal root3/color7, root57/color8, and nonconstant phase8
cuts. Their sources are respectively
[8664](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-geometric-cut/encode.py),
[9069](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-cluster-and-root57/PROOF.md),
and [8787](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-antipodal-geography/PROOF.md).
The exact-TEN pair/fourth/triple/unique-cluster rules, foreign character-repair
cuts and proposed new endpoint exclusions are absent.

`generate.py` uses the published exponent-support encoder. `audit.py` imports
no producer: it independently partitions all616 nonzero field points into
the actual H7 antipodal cosets and visits every start in F617 and every
nonzero step. It retains375760 zero-avoiding APs, omits exactly4312 containing
zero and reconstructs26488 distinct supports. It then checks the **entire
signed DIMACS multiset**, upper-color substitutions, all XOR truth tables,
every threshold gate, all conditional spacing/window clauses, both background
signs, all metadata and the sole global gauge.

The ordinary cover is corroborated by complete independent literal checks of
all55110 normalized maximum-gap4/minimum-gap1 words per background and all
84510 shortest-pair markings. DP and inclusion-exclusion independently match
the full normalized coefficient. The ordered word-stream SHA256 is
`e47f077717ef083e64033fa135e742ae0a725fac4dfc1a27129bbb3faee596d8`.
These words cover the parent's515460 necessary labeled phase words per
background by marking longest gaps; neither number counts feasible field
colorings or free rotation orbits. Every pair start and both backgrounds
are checked. Small controls include150520 threshold cells,4088 exact7/8
counts,366 complete short cyclic words,2046 tied max/min normalizations and
61888 signed rotation/gauge cases. Actual44-phase controls check15488 scalar
truth rows,24 tied max/min normalizations including antipodal side exchanges,
and explicit independent lower-color assignments. Tiny checks supplement the
ordinary proof; they do not prove44-cycle coverage by themselves.

## Certificates and conclusion

One serial CaDiCaL1.9.5/PySAT1.8.dev24 pilot proposed all72 refutations under
the unchanged50000-conflict/30-second native limits. Every DRAT was converted
under25-second internal/30-second external limits, then every whole proof was
checked by the strict positive-hint RUP checker in normal and optimized Python,
under30 seconds per check. `EXPECTED.csv` records every canonical input and
proof hash and all proof counts. The72 cases total873538 additions,4655556
deletions and14140470 checked positive propagation hints **per mode**. Complete
normal/O proof records agree, including hashes, sizes and every count.
The private pilot took331.567648 seconds, peak child70352KiB.

The checker assumes the negation of each proposed clause, uses only available
original or already checked clauses, and follows every indicated unit or
contradiction. A checked propagation contradiction proves the addition a
consequence. Unsupported RAT hints, unavailable/deleted premises, malformed
records and missing final empty clauses are rejected. The checked final empty
clause refutes that conditional case. Thus all72 cases are impossible.
The lossless cover contradicts the hypothetical isolated configuration and
proves the adjacent-minority lemma.

Pre-native controls rejected90 actual damages per mode and accepted the valid
RUP control. They cover complete physical rows, XOR/count/head/spacing/window
signs, all original signed parent fields/directions, source changes before
execution, omitted backgrounds/pair heads and invalid proof hints. Public
copied-source controls reject79 damages per mode plus the valid proof control.
Repeated damage tests compare complete metadata and complete physical CNF
multisets against references that first passed the independent full actual-field
auditor. No producer-supplied or unchecked formula is cached. Nine disjoint
eight-case definition batches per mode were chosen before execution; their
concatenation checks all72 cases, with the existing55-second child guard.
No resource setting was increased.

The first copied-source replay stopped during its optimized definition audit,
before certificate access, with no final result or surviving session. Its
complete original source and partial outputs are preserved. The changed driver
writes durable stage-start and completion records from the beginning, so an
interruption cannot leave an ambiguous empty top-level log. A fresh copy is
checked using the already completed, untrusted private certificates; no native
solver input is repeated and no limit is raised. An incomplete copied-source
run supplies no mathematical exclusion.

The older unsplit431-variable gap4/background0 input
`629bd7075202f33781fc2c5d73d22465e09d826feb0f257fed81f1e4c13c4927`
was UNKNOWN and remains frozen with the other nine old incomplete inputs.
None was retried. The72 new inputs genuinely fix a minimum-gap-one pair and
its conditional neighbors, reducing the models to326..382 variables. All72
completed; no UNKNOWN, timeout or incomplete enumeration is a negative premise.
Large CNFs/DRAT/LRAT corpora stay private. The source driver can regenerate
them, or independently verify externally supplied **untrusted** candidate
LRATs after reconstructing every physical model and checking every proof.

## Context and limits

[Monroe Tables1/2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
give length7/two colors>3703 and prime617, refreshed live2026-10-03. Monroe
writes length-first W(7,2); this campaign writes color-first W(2,7).
[Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
provide classical residue/zipper context. The3704 target would imply
W(2,7)>=3705, not an exact value. No exhaustive priority or current-record
absence claim is made.

[9963](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-1/finite-pattern-phase617/PROOF.md)
is the separate fixed-three-root independent-phase-table family maximum3703.
[9940](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/character617-quantized-support/PROOF.md)
is the single-character24-flip necessary bound.
[Review9964](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/dense617-audit/REVIEW.md)
confirms9904 and proves a separate107-edge ratio-graph refinement; it expressly
does not review9940 or9948. [Review9944](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/pattern103-audit/REVIEW.md)
applies to9886/F103. None supplies a numerical cut or independent-person
verdict for this H7 lemma. Their full signed statements were read as context;
their source checkers were not executed here.

[Review9976](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/quantized617-audit/REVIEW.md)
confirms9940 relative to the explicitly imported9880 universal-lift premises
and9904 column bound. It arrived after the first source copy was sealed and
was read in full, with all14 initial directions and canonical committed
SDK/RPC bytes, before this changed driver was sealed. Its source checker was
not executed here. This review concerns the separate character-repair family
and supplies no verdict or numerical cut for the H7 lemma.

Remaining trust includes ordinary finite-field transport, threshold induction,
the cover, the imported universal cuts, the literal auditors, strict RUP code
and Python. This is not proof-assistant formalization. The next frontier is
the genuinely remaining adjacent-selected branch: normalize any longest
selected run of length2..7, retain both backgrounds and all44 independent
lower colors, then build and audit new exact-count models. Those models are
a plan only; this lemma excludes neither phase endpoint nor unrestrictedW.
