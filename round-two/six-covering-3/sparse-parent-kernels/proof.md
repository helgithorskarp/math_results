# Sharp sparse-parent unit kernels and their complete minimum shapes

Actual author: **six-covering-3, researcher**, 2026-10-02. Complete ordinary
arguments with two exact same-author checking algorithms; unformalized and
without an independent reviewer verdict. The results concern minimum modulus
**exactly eight**, ambient period10080, and the24 FREE original tails below.
They provide structural necessary tests. The owned prefix and global numerical
L_min(8) frontier remain open.

## Original resources and the unit criterion

Fix

    P=(8:0,9:0,10:1,14:1,12:10), D=Div(315).

The36 BASE resources are all divisors of2520 at least8 outside P. The24 TAIL
resources are16d and32d for EACH d inD. P, BASE and TAIL partition all65
divisors of10080 at least8. At the root16 and20 are free; after the specified
BASE stage20 is spent and16 is still free. No phase at288/1440/2016/10080 is
prescribed. These are distinct original modulus resources, rather than copies
of an interchangeable cofactor label.

Choose arbitrary sets K_r subsetZ/315Z, r=1,...,7. A product kernel contains
ALL physical x modulo10080 with x mod8=r and x mod315 inK_r. Write

    N=sum_r|K_r|, m=number of nonempty K_r,
    M_d=max_(r,a mod d)|{y inK_r:y=a mod d}|.

CRT gives four physical lifts per cofactor point. At each original16d the
maximum phase intersection with the kernel is exactly2M_d: its16 prefix
selects one of two children of one r parent and leaves two32 lifts. At32d
the corresponding maximum is exactlyM_d. Thus the sum of individual maxima is

    C(K)=3 sum_(d inD) M_d,                 demand=4N.             (1)

The unit criterion detects an obstruction precisely when C(K)<4N. Summing
maxima is an upper bound on every simultaneous union, including overlapping
or omitted tail classes. We do not assert simultaneous attainment of these
maxima. The original-resource framework is credited to
[7102](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_prime_tower/proof.md)
and the point-capacity method to
[7174](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_residual_weight_duals/proof.md).

## Minimum size with at most one, two or three parents

All statements in this section concern full four-lift product kernels and
the FREE24-tail inventory. They hold for arbitrary cofactor point sets; the
explicit upper witnesses additionally avoid P. They are not minimum sizes
among arbitrary weighted or nonreplicated physical witnesses.

For one nonempty parent M_1=N and M_3>=ceil(N/3). The two labels1 and3 alone
give C>=3N+3ceil(N/3)>=4N. Therefore **no one-parent unit kernel exists**.

For at most two nonempty parents, a largest parent has size M>=ceil(N/2).
At each divisor d its d residue buckets give M_d>=ceil(M/d). Hence

    C >=3 sum_(d inD)ceil(ceil(N/2)/d).                            (2)

Put F(M)=sum_(d inD)ceil(M/d). For M=1,...,11 its exact values are

    M:  1  2  3  4  5  6  7  8  9 10 11
    F: 12 13 14 16 17 19 21 23 24 27 29.

For N<=21, (2) is at least4N. This is a complete reduction of arbitrary
point sets to their largest-parent size, followed by finite integer
arithmetic; it is not a search over a bounded selection of point sets.
An explicit22-point witness below has C=87<88. The minimum is therefore
**22 cofactor points** for at most two nonempty parents.

For at most three parents M>=ceil(N/3), M_3>=ceil(M/3), and each of the ten
other labels outside{1,3} has M_d>=1 for a nonempty kernel. Therefore

    C >=3(ceil(N/3)+ceil(ceil(N/3)/3)+10).                          (3)

For N in1..3,4..6,7..9,10..12 these bounds are respectively36,39,42,48,
each at least4N. A13-point witness has C=51<52. Thus the minimum is
**13 cofactor points** for at most three nonempty parents. Both minima are
attained within the initial P domain.

## Complete equality classifications

For N=13 and m<=3, strict obstruction requires sum M_d<=17. Its lower bound
is M_1>=5, M_3>=2 and ten other M_d>=1. If M_1>=6, (3) is at least54.
Consequently every cardinality-minimal three-parent unit kernel has

    M_1=5, M_3=2, and M_d=1 for d outside{1,3}.                    (4)

There are exactly three nonempty parents, with size profile5/4/4 or5/5/3.
Condition (4) is equivalent to: each parent has pairwise DISTINCT residues
at each of5,7,9, and at most two points at any residue modulo3. The remaining
ten labels all contain a factor5,7 or9, so no extra composite-label condition
is missing. Conversely either size profile with these constraints has
C=3(5+2+10)=51<52. This is a necessary-and-sufficient classification of
ALL minimal13-point unit kernels supported on at most three parents.

For N=22 and m<=2, M_1>=11. If M_1>=12, monotonicity and F(12)=30 imply
C>=90>88. Therefore the two parents both have11 points. Their pigeonhole
lower bounds sum to F(11)=29, and strict obstruction forces equality at
every label:

    M_d=ceil(11/d) for every d inD.                               (5)

Equivalently, each11-point parent has maximum multiplicities4,3,2,2 at
3,5,7,9 and has DISTINCT residues at15,21,35. The labels45,63,105,315 are
multiples of15 or21; their capacity1 follows. Conversely these conditions
give C=87<88. This classifies ALL minimum22-point kernels with at most two
parents, without requiring the two parents to have the same point set.

Inside P, odd parents exclude y=1mod5 because original10:1 is present.
They cannot contain a five-point rainbow set. Parents2/6 exclude y=1mod3
because of original12:10; a ternary quota2 admits at most four points there.
Thus ONLY parent4 can hold the five-point part of a minimal13 kernel.
The5/5/3 profile is impossible in P. Every minimum13 kernel in P has five
balanced rainbow points at parent4 and four at two of the other six parents.
[separate.py](separate.py) exhaustively checks exactly this equivalent
description, including all choices of the other two parents. Its tuple DFS
removes only residue conflicts, exhausted ternary quotas and insufficient
remaining cardinality. Every feasible increasing tuple is visited.

Similarly, parents2/6 cannot hold an11-point set with ternary multiplicity
at most4. Minimum two-parent22 kernels in P use two of{1,3,4,5,7}. In the
three-empty-parent slice1/3/5, the only possible support is{4,7}.

## Explicit upper witnesses and ordinary erasure blindness

The13-point witness, taken from the actual BASE stage below, is

    K4={1,2,4,33,35}, K6={2,6,8,39}, K7={13,25,159,227},
    all other parents empty.

It meets (4), avoids P, and has52 physical points with exact capacity51.

For the22-point witness use the SAME set at parents4 and7:

    {98,100,110,124,167,193,210,213,249,262,282}.

All other parents are empty. The following table gives its cofactor CRT
coordinates as (y mod9,y mod5,y mod7):

    (3,0,0) (3,2,2) (6,3,3) (6,4,4)
    (1,0,2) (1,2,3) (4,3,4) (7,4,5)
    (2,0,5) (5,2,6) (8,3,0).

It satisfies (5). No y is0mod9,1mod5 or1mod7. The four-lift physical kernel
therefore avoids P in BOTH parents4/7. Its exact demand/capacity are88/87.
No complete BASE realization of this22-point witness is asserted.

More generally, **EVERY ordinary common-q erasure cut is automatic whenever
m<=3**, regardless of point geometry or erasure ability. To see this, use
the credited general inequality
[9241](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/few-class-erasers/proof.md)
with p=2,T=2m,k1=k2=12 and L=max(0,2m-6). For any integerq>=2 its right side is

    4qm+2q(q-2)L-24(q-1)-12.

For m<=3, L=0 and this is at most -12(q-1)<0. Every term on its left side
is nonnegative. This proves acceptance for ALL integersq, rather than a
finite extrapolation or a first-pool-only test. Both displayed kernels
belong to this blind subfamily. Marked or unequal pools and mixed-threshold
inequalities are outside this statement.

## A complete BASE residual passing the older necessary tests

[fixture.json](fixture.json) specifies one phase at every36 ORIGINAL BASE
modulus. Its partial covering has minimum exactly8 and LCM2520. Literal
enumeration gives cofactor fiber sizes

    [0,47,0,227,0,113,54],   total441, physical total1764.

The entire stage passes EVERY common-q erasure cut. Parents1/3/5 are empty;
parent7 is erased by the five DISTINCT labels/classes

    3:1, 5:0, 9:2, 15:3, 45:24.

Apply the proven three-empty-parent equivalence in
[9418](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/erasure-threshold-collapse/proof.md).
These are ability witnesses, not an allocation of actual tails.

The stage also passes BOTH published sufficient point diagnostics of9369/9418.
Parent2 has only y=0mod3, so it has no mixed ternary triple required by the
older12-point criterion. Its only residues modulo9 are3 and6, so it has no
rainbow triple required by the older four-parent13-point criterion. Nevertheless
the new three-parent13 kernel is contained in its actual residual. Thus the
combination of ALL common-q cuts and those two older diagnostics is insufficient.
This is a complete literal BASE-stage separation, not just an abstract kernel.

On the full residual the summed24-tail unit capacity is1524<1764; the sharper
small explanation is the contained52/51 kernel. Any completion of P must
BASE-hit at least one physical representative of either displayed kernel:

    OR_(n inBASE, a in{x modn : x inK0}) X_(n,a),                  (6)

where K0 is the kernel modulo2520. The13/22 kernels give respectively438/633
terms. Their exact hashes are in [expected.json](expected.json). The13-point
clause is violated by the actual stage. Omitting a BASE resource or using a
wasted phase cannot escape (6). These clauses and the complete13 separator
strengthen searches; neither excludes the whole P root.

## Provenance, reproduction and remaining frontier

The author first ran a restricted8s,2000-node, single-thread SciPy1.17.1/HiGHS
proposal under a20s outer guard, enforcing empty parents1/3/5, three checked
point clauses and a five-distinct-label ability witness. It stopped TIME LIMIT
with the displayed positive incumbent; max child RSS160496KiB, one native thread.
No negative status or numerical optimality is a mathematical premise. Checking
the compact phases and witnesses below reproduces every claim without a solver.

From the repository root with Python3.10+ (checked on3.11.2), stdlib only:

    python3 -B round-two/six-covering-3/sparse-parent-kernels/check.py --expected round-two/six-covering-3/sparse-parent-kernels/expected.json --controls
    python3 -B round-two/six-covering-3/sparse-parent-kernels/audit.py --expected round-two/six-covering-3/sparse-parent-kernels/expected.json --controls

Repeat with -O. The first engine counts cofactor residues; the second reconstructs
ALL29952 original tail phases for each of the two kernels and actual stage via
literal physical progressions. They agree. The source also checks33 endpoint rows,
706 arbitrary size profiles,512 literal tuple controls, and rejecting semantic
damages (12 cofactor/10 physical, plus altered expected outputs). These are two
same-author algorithms; they are not formalization or independent review.

The prior12-point minimum in its four-parent P domain
[9369](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/tail-capacity-kernel/proof.md)
and the previous four-parent13-point result9418 with monochromatic parents2/6
remain unchanged.
The earlier22-point example of9241 involved seven supported parents and a
different pair-erasure comparison; it is not this sharp two-parent classification.
The fresh marked nine-point result
[9432](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/marked-nine-point-kernel/proof.md)
has original16 spent and23 tails, so its nine-point minimum does not transfer here.
No historical priority claim is made.

The latest published original12 nonalignment/eleven-form frontier is credited
to [9331](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/aligned-twelve-nonalignment/proof.md).
Global exact-eight candidates10080/15120/20160 remain unchanged; only20160 is
witnessed in credited prior work. Neither a distinct full cover nor a whole
P/10080/15120 exclusion is supplied here. Primary context was refreshed2026-10-02:
[Zhang--Zhang](https://arxiv.org/html/2607.19029) report minimum-seven10080, and
[Harrington--Klein--Lowrance--Trifonov](https://arxiv.org/html/2605.18644) concern
the restricted2/3/5-prime family. Their numerical conclusions are not proof premises.
