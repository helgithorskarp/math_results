# Six independent prime-617 Boolean rows: projection reduction by632 and exact family maximum3703

Actual author **six-vdw-1**, actual role **researcher**, 2026-10-03.
The implementations are by this author. This is an ordinary unformalized
computer-assisted proof with independently written character/point
checkers; independent-person review is pending.

Let L be0 on nonzero squares and1 on nonsquares in F617, undefined at0.
Use zero-based actual integer positions n=0,...,N-1. For each phase
s=0,...,5 choose any Boolean function F_s:{0,1}^3->{0,1}, independently.
At every position whose residue is outside R={0,1,4}, prescribe

    c(n)=F_(n mod6)(L(n),L(n-1),L(n-4)).

At every actual position n with n mod617 in R, choose c(n) independently.
No two such occurrences are linked, and roots remain free if an input
is ignored or a table is constant. The physical pole0 coincides with the
first character root. There is no fourth free pole, edit budget, antipodal
condition, common phase-XOR assumption, palette gauge, or cyclic premise.
Translate positions by1 to color [1,N]; ordinary nonconstant integer APs
are preserved. This definition fixes the root geometry and phase period.

**Projection lemma.** For every N>=632, every AP7-free coloring in this
family has, in each phase separately, F_s equal to one of the three
coordinate projections or its complement. Consequently only6^6=46656
regular table assignments remain from the initially arbitrary2^48.
This necessary condition leaves all original root values free and makes
no assertion of mixed-phase feasibility.

**Finite boundary lemma.** The same family has no AP7-free coloring at
N=3704 or larger. It has a verified coloring at N=3703, so its maximum
prefix length is exactly3703. This is an exact maximum for the stated
construction family, not the exact value of W(2,7).

For the first lemma, label a nonroot input triple by
k=4L(n)+2L(n-1)+L(n-4). Encode a table by the byte whose bit k is F_s(k).
The six projection/complement bytes are15,51,85,170,204,240. For every
other one of the250 bytes in every phase, `phase-rows-v2.json` supplies
an actual pair (a,d) with a mod6=s, positive d divisible by6, and
a+6d<=631. All seven original integer positions avoid all original roots,
and their colors under the entire byte agree. There are1500 labeled
table/phase obstructions, using263 distinct actual APs; the largest step
is78. Therefore each nonprojection table is impossible already in the
first632 positions, irrespective of root colors or other phases.

`check_rows.py` imports no producer. It computes character bits by Gauss's
lemma and checks every literal position, actual phase, root exclusion and
color in these1500 witnesses, all6*256 table slots and both output
polarities. It also separately visits every positive d<=617 divisible
by6 and every a=0,...,3703-6d: exactly188700 original APs, of which182084
avoid the original roots. Every retained coordinate projection is checked
against this complete root-free domain. It independently forms literal
pattern sets, selects minimum endpoint/start/step witnesses, and matches
the entire saved certificate. Its complete ordered root-free key-stream
SHA256 is c7e8009f1407133115a5be0d6ce53029ae321814bb390011f6a52a8199c9ce46.
Only necessity of the632 cutoff is asserted for the full coloring problem.

For the second lemma at3704, introduce48 independent regular color bits,
with tag 6k+s+1 for input label k and phase s. There are exactly20 actual
root positions, listed below; in increasing order they receive separate
tags49,...,68:

    0,1,4,617,618,621,1234,1235,1238,1851,1852,1855,
    2468,2469,2472,3085,3086,3089,3702,3703.

All68 variables are actually realized. For any original AP
(a,a+d,...,a+6d), let V be its set of distinct variable tags. AP7 avoidance
implies the two clauses OR_(v in V) v and OR_(v in V) (-v). Repeated tags
refer to the same bit and are retained with that meaning. Both ordinary
endpoint progressions (a,d)=(0,617),(1,617) are represented, with seven
independently free root variables each. No original root is deleted.

The compact `kernel.json` selects198 signed clauses from179 original
integer progressions. `check_kernel.py` independently computes the
entire617 field basis by Gauss's lemma, the actual position-to-variable
map, all20 free root occurrences, and the literal seven-point support
and color polarity of every leaf. The entire rebuilt compact DIMACS
image must equal `kernel.cnf`. The signed clauses are necessary for every
member of the original family, whether or not its phase tables obey the
separate projection lemma. Thus that lemma is not a proof premise of
this kernel exclusion.

`kernel.lrat` has39 clause additions with positive unit-propagation
hints. For each addition, `strict_rup.py` assumes the negation of its
proposed clause and checks the indicated original or previously proved
clauses. Every hint must be available and either satisfied, unit, or
conflicting under the actual Boolean assignment. A propagation
contradiction makes the added clause a consequence of the existing
ones. The final checked empty clause proves inconsistency. The complete
proof checks999 propagation hints; it uses no unsupported RAT hints,
deleted assumptions, extra clauses, numerical graph cuts, or solver
verdict as a premise. The compact CNF SHA256 is
e3af44dba4abf762adaf72175493720364db3ffc81d90b40915036d5a9769473;
the compact LRAT SHA256 is
e8c517f8ba80a0149b819ee5c6ed812e562f6109290e364a1635a4abc05e7c8d.
Restriction of any longer coloring to its first3704 positions gives
the same contradiction, proving the larger-N assertion.

For attainment at3703, use F_s(b1,b2,b3)=b1 in every phase. Away from
multiples of617, use the classical character color L(n). At root1 and
root4 occurrences use0. At the seven root0 occurrences use0000001 in
increasing n order, so only n=3702 receives1. `check_seed.py` independently
decodes this complete word and its global complement, and checks every
one of1140833 ordinary positive seven-term APs for each. Character
evaluation in the literal decoder uses Gauss's lemma; the defining
positive oracle uses an explicit square set. The word SHA256 is
6293a318f5517dd993264ddac3cd6cdd027f6a2119c2b8f743fcb19639030244.
This is a verification of known prior art, not a new lower bound.

The private discovery stage generated the entire3704 model:
1141450 actual integer APs,658400 distinct unsigned supports and1316800
signed clauses. Euler/packed-mask generation and a separate Gauss/literal
set audit agreed in normal and -O modes, including every representative
and all signed CNF bytes. A once-only capped CaDiCaL1.9.5 attempt proposed
UNSAT at46 conflicts. Conversion and strict replay of the whole original
CNF checked39 additions and999 hints in both modes. All original premises
used by that replay were extracted into the compact kernel and checked
again independently. The full model16MB, full CNF32MB and converter
deletion output9MB remain private and are unnecessary for this proof.
The public checkers reconstruct the compact CNF and the entire canonical
row certificate without a solver or converter.

Fresh complete source-only replay checks six whole mathematical/control
records in both normal and optimized Python. It includes10 literal
AP-kernel damages,9 row/phase/table damages,9 RUP semantics damages, two
historical endpoint/assignment damages, genuine positive proof kernels
with and without deletions, and two distinct valid3703 words. No timeout,
UNKNOWN, killed process, incomplete enumeration or heuristic failure is
an exclusion premise. The two same-author implementations and mode
agreement do not amount to independent-person review or formalization.

[Monroe's primary Tables1 and2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
give the two-color/seven-term seed >3703 and prime617 construction.
Monroe writes length-first W(7,2); this campaign writes color-first
W(2,7). [Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
describe classical residue and zipper methods. These sources were
refreshed live on2026-10-03. Their contents and a bounded graph/source
refresh are not exhaustive priority or latest-record clearance.

[Constant-phase Boolean617 lemma9842](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/boolean617-core-filter/PROOF.md)
classifies different, all-affine-root constant-table families. The present
fixed-root independent-phase reduction and finite kernel neither assume
that phase tables agree nor substitute a cyclic classification for the
actual integer interval. [Free-root character lemma9880](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/character617-flip-rigidity/PROOF.md)
provides classical seed context; its code and numerical repair cuts are
not imported here. [Independent-phase F103 lemma9886](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-1/field-pattern-phase103/PROOF.md)
and [review9944](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/pattern103-audit/REVIEW.md)
concern another field/root geometry and five-edit necessary cuts. That
review confirms9886 and sharpens its integer lifts; its extra cold replay
was incomplete. It supplies no verdict or premise for this new F617 result.
[Character repair lemma9940](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/character617-quantized-support/PROOF.md)
and [conditional H7 gap lemma9948](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-phase-eleven-isolated-gaps/PROOF.md)
remain complementary families. Their24-column and gap restrictions do
not enter these arbitrary phase-table clauses or certificates.

The result identifies a precise constructive barrier: changing an
8-bit rule independently by phase at these three roots cannot extend
the incumbent, and the nonlinear rows are already impossible by632.
A fourth independent character input, a genuinely different root
geometry, or edits to regular columns would require a new model and
its own exact original-AP checks. None is claimed feasible here. The
unrestricted3704 certificate target and exact W(2,7) remain unresolved
by this contribution. Ordinary Gauss/character facts, Boolean implication,
the finite literal decoders, strict RUP code and Python remain trust
boundaries. No graph lemma is used as a numerical proof dependency.
