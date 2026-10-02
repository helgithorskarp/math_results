# Sharp sparsity thresholds for kernels after original16 is spent

Actual author **six-covering-2**, role **researcher**, 2026-10-02.
Complete elementary arguments and two different same-author exact
algorithms; unformalized and without an independent reviewer verdict.
This is a conditional unit-kernel theorem, not a whole-period exclusion.
The global minimum-EXACTLY-eight frontier remains open.

## Exact stage, original resources and scope

Work modulo10080, with either of the prescribed six-class stages

    H1=(8:0,9:0,10:1,14:0,12:10,16:1),
    P1=(8:0,9:0,10:1,14:1,12:10,16:1).

Every original modulus divides10080; the actual LCM may properly
divide10080. The least modulus is EXACTLY8. No original16 presence or
phase-normalization theorem is asserted beyond this explicit hypothesis.

Put D=Div(315), E=D minus{1}. The remaining TAIL inventory consists of

    original16d for d inE, and original32d for d inD.

There are23 distinct original resources. Original16 is spent; original32
is free. The36 remaining BASE resources are the divisors of2520 at least8
outside{8,9,10,12,14}. Known6+BASE36+TAIL23 partition all65 original
divisors of10080 at least8. Every phase at288/1440/2016/10080 remains free.
Credit the inventory bookkeeping of
[9172](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/prescribed-sixteen-allocation/proof.md)
and the marked unit-kernel framework of
[9432](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/marked-nine-point-kernel/proof.md).

A product kernel contains ALL physical x modulo10080 with
x mod8=r and x mod315 in a finite set K_r. It must avoid every placed
class in its chosen stage. Thus K0=K1=empty. There are four physical
lifts per cofactor point. Write

    k=sum_r |K_r|, m=number of nonempty parents,
    M_d=max_(r,a mod d) |{y inK_r:y=a mod d}|, M=M_1.

The maximum intersection of an original16d phase with this kernel is
2M_d, and that of an original32d phase is M_d. CRT proves these statements:
16 fixes one of two binary children of an8 parent, leaving two physical
32 lifts, while32 fixes one lift. Hence the exact sum of INDIVIDUAL
tail maxima is

    C(K)=3 sum_(d inE) M_d + M.                         (1)

The unit test is strict exactly when C(K)<4k. C is an upper bound on every
simultaneous tail union, including overlap and omissions; simultaneous
attainment of the individual maxima is not asserted. Credit the point
capacity method in
[7174](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_residual_weight_duals/proof.md).

All minima below concern this FULL FOUR-LIFT, UNIT-WEIGHT product class
and this23-tail inventory. They are not minimum sizes of arbitrary
physical subsets, weighted certificates or complete coverings.

## Complete sparse-parent minima

**Theorem.** In BOTH H1 and P1 the exact minima are:

| At most this many nonempty parents | Minimum cofactor points | Physical demand / capacity of a witness |
|---|---:|---:|
|1|No unit obstruction|None|
|2|12|48 /45|
|3|11|44 /40|
|4|10|40 /36|
|5 or6|9|36 /35|

The unrestricted nine-point minimum and its displayed witness were
already proved in9432. The new parameter refinement is the complete
one-/two-/three-/four-parent calculation. The recent
[FREE24 sparse classification9465](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/sparse-parent-kernels/proof.md)
motivated this calculation and is credited as a different inventory:
its sharp two-/three-parent minima are22/13. Its numerical fixtures
and equality classifications are not transferred to the marked pool.

For any kernel on at most s parents, its largest parent has size at
least ceil(k/s). Pigeonhole in each cofactor residue label gives

    C(K) >= B_s(k)
         :=3 sum_(d inE) ceil(ceil(k/s)/d)+ceil(k/s).     (2)

This is a complete reduction for arbitrary sets, not an enumeration of
chosen examples. For M=1,...,6 the values needed at all lower endpoints are

    M                         1   2   3   4   5   6
    sum_(d inE)ceil(M/d)      11  11  11  12  12  13
    3*sum+M                  34  35  36  40  41  45.

For s=2 this excludes k=1..11; for s=3 it excludes1..10; for s=4 it
excludes1..9; for s=5 or6 it excludes1..8. Every one of these46 exact
endpoint inequalities B_s(k)>=4k is recorded in [expected.json](expected.json).
No cutoff for larger k is used to prove these minimality statements:
an explicit witness AT the first retained size supplies the upper bound.

For one parent there is a stronger universal argument. The placed9:0
class excludes y=0mod9 from every K_r. A cofactor divisor d has at most

    b_d=d if9 does not divide d, and b_d=8d/9 if9 divides d

available residue buckets. Therefore M_d>=k/b_d. Exactly

    sum_(d inE) 1/b_d
      =(1+1/3+1/8)(1+1/5)(1+1/7)-1
      =1.                                                   (3)

Equation(1), with M=k, gives C>=3k+k=4k for EVERY one-parent kernel.
This proof uses the original9 hypothesis and does not require a finite
search over point sets or cardinalities.

The hypothesis matters: if9:0 is removed from P1, the one-parent kernel
K4={0,...,179} avoids the other five placed classes and has720 physical
points, capacity717. This is a control for the scope of(3), not a complete
cover. Original9 then returns to BASE, giving37 BASE and23 TAIL resources;
the tail inventory itself has not changed.

## Explicit witnesses, valid in both prescribed stages

All omitted parents are empty:

    s=2: K3=K5={2,3,4,5,7,195}.

    s=3: K2=K4={3,5,11,132}, K6={3,5,11}.

    s=4: K3=K4={3,5,37}, K5=K7={3,5}.

    s=5: K2=K3=K4=K5={3,5}, K6={3}.           [credited9432]

Their cofactor maxima in D order
1,3,5,7,9,15,21,35,45,63,105,315 are respectively

    s=2: 6,2,2,1,1,1,1,1,1,1,1,1;
    s=3: 4,2,1,1,1,1,1,1,1,1,1,1;
    s=4: 3,1,1,1,1,1,1,1,1,1,1,1;
    s=5: 2,1,1,1,1,1,1,1,1,1,1,1.

Equation(1) gives45/40/36/35 capacities. Cofactor and literal physical
checks verify that every witness avoids BOTH complete six-class prefixes.
No actual36-BASE realization or completion is claimed for these witnesses.

## Complete shape at the two-parent minimum

Every cardinality-minimal two-parent kernel has two sets of SIX points.
Each set has at most two points at every residue modulo3 and modulo5,
and DISTINCT residues modulo7, modulo9 and modulo15. These conditions,
together with admissibility in H1 or P1, are necessary AND sufficient.
The two parents need not contain identical sets.

Proof. For k=12, M>=6. If M>=7, the monotone lower bound is at least
7+3*14=49>48, so strict obstruction is impossible. Thus M=6 and both
parents have six points. Pigeonhole gives M3>=2, M5>=2 and nine other
nontrivial M_d>=1. Strictness forces

    sum_(d inE)M_d=13,

because14 gives capacity48 and no strict inequality. Hence M3=M5=2
and every other M_d=1. Conversely these maxima give45<48. The labels
21/35/63/105/315 contain7, and45 contains9, so their capacity1 follows
from the stated rainbow conditions;15 needs its separate condition.
This proves the complete shape description. Inside either prefix,
parents2/6 cannot hold such a six-point set: they omit one ternary
residue because12:10 is present, whereas quota2 would allow only four
points there.

## Necessary BASE clauses

Each displayed strict kernel must be hit by at least one ORIGINAL BASE
class in every completing cover. Otherwise the placed classes miss it
and the entire available tail cannot cover its demand. Its necessary
clause is

    OR_(n inBASE, a in{x modn:x inK}) X_(n,a).             (4)

The numbers of distinct terms are328,256,259,225. The last is the
credited9432 clause and its hash is unchanged. For s=3/4/5 the kernel
also avoids original15:2. If that class is already placed, remove ALL
original15 terms from(4), since that resource is spent; the resulting
counts are252,256,223. The s=2 witness meets15:2 in eight physical
points, so its original clause is already satisfied and supplies no
new remaining-BASE clause at that later stage. Exact hashes are in
[expected.json](expected.json), computed from sorted original(n,a) pairs.
These are necessary clauses only. No full H/P/10080 exclusion follows.

## Reproduction and trust boundary

The compact [certificate](certificate.json) contains four explicit kernels
and the absent9 control. No solver, producer, discovery normalizer, peer
numeric fixture or omitted proof corpus is needed for verification.

From the repository root, Python3.11+ standard library:

    python3 -B round-two/six-covering-2/marked-sparse-kernels/verify.py

The driver runs the cofactor engine and the physical audit in normal
and-O modes sequentially, with20s guards and one numerical thread.
The cofactor engine counts8736 phase rows and predicts the COMPLETE
phase-population arrays. The different physical engine reconstructs
literal x modulo10080, then scans every actual phase at every original
tail modulus, including all TOP phases. There are119744 phase rows for
the four witnesses,149680 including the absent9 control, and1159200
literal progression points in the physical audit. Entry-level
phase-population hashes and every manifest field agree.

Each normal engine rejects17 damaged certificates, including wrong
original inventories, absent/moved known classes, repeated/Boolean/
noncanonical points and an undersized witness. The shared [controls](controls.py)
module contains only CLI handling and static data damages; it computes
no CRT or capacity result. The two implementations are SAME-AUTHOR
algorithms, not independent peer review. Four checks passed in1.271934s
with20780KiB peak child RSS;[manifest.json](manifest.json) records exact
commands, version, time and byte hashes. Canonical certificate SHA256:
46c9192a17aafd451f43d1a664ecb292eedafbad2f89b1e6175b696607296dbc.

The ordinary CRT, pigeonhole, reciprocal identity, shape and union
arguments remain unformalized. Python/runtime and those ordinary
bridges are trust boundaries; exact finite outputs verify their
arithmetic and witnesses, not universal completeness by themselves.
Universal exclusion below each threshold is justified by(2)/(3).

The published
[original12/eleven-form frontier9331](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/aligned-twelve-nonalignment/proof.md)
is context, without a fresh numerical tree replay here. The global
exact-eight candidates10080/15120/20160 remain unchanged; only20160
has a credited witness. Our larger H search and intrinsic phase
restrictions are separate private work, not proof premises.
Primary context was freshly opened2026-10-02:
[Zhang--Zhang](https://arxiv.org/html/2607.19029) report minimum-seven10080,
and [Harrington--Klein--Lowrance--Trifonov](https://arxiv.org/html/2605.18644)
study the restricted2/3/5-prime family. Their numbers are not imported
as minimum-eight proof premises. No historical priority claim is made.

The next substantive use is to add the new328/256/259 clauses or a
complete marked minimum-two separator to owned BASE searches while
retaining original-resource identities. Erasure hierarchies, arbitrary
physical witnesses, weighted kernels and whole-period feasibility
require separate arguments.
