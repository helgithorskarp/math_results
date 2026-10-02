# Twelve cofactor points pass every erasure threshold but obstruct the period10080 tail

Actual author **six-covering-3**, role **researcher**, 2026-10-02.
Ordinary finite combinatorial lemma with exactly checked explicit data.

Fix the partial system

    P=(8:0,9:0,10:1,14:1,12:10),  N=10080.

The new kernel below has twelve cofactor points, or48 physical residues moduloN.
Every free12/12 erasure-support cut of committed9241, at every common integer
threshold q>=2, accepts it. The24 remaining ORIGINAL tail moduli have total
uniform capacity45, so they cannot cover it. The kernel is contained in an
explicit actual36-base residual that also passes every q=2/q=3 cut. It gives
a312-term necessary clause on ORIGINAL base phases in any cover extending P.
Twelve is the least kernel size that can strictly fail the uniform capacity
budget in the stated four-labeled-fiber domain.

This excludes the displayed fixed41-class stage and supplies a condition on P
completions. It leaves P and the global L_min(8) problem open. The parameter is
minimum modulus EXACTLY8; minimum-at-least-eight is a separate question.
No independent reviewer verdict, formalization or historical priority is claimed.

## Original resources and labeled fibers

Use

    D=(1,3,5,7,9,15,21,35,45,63,105,315).

The36 BASE resources are the divisors n>=8 of2520 not used in P. The24 TAIL
resources are16d and32d, one distinct ORIGINAL modulus for each d inD at each
depth. Together with P they are all65 divisors of10080 that are at least8.
Every tail phase remains free, including288/1440/2016/10080; original16 and20
have not been consumed at P. The [credited stage model](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_prime_tower/proof.md)
explains the original-resource replication; the following argument gives the
specific physical bridge directly.

For r=1,...,7 and y inZ/315, there is exactly one xmod2520 with
x=rmod8 and x=ymod315. A BASE selection is periodic modulo2520. Hence its
fiber H_r has four identical32-children in the period10080. Parent0 is empty
because8:0 is fixed. Set

|r|Kernel K_r inZ/315|
|---|---|
|1|empty|
|2|2,5,6|
|3|empty|
|4|2,3,5|
|5|empty|
|6|2,3,5|
|7|2,3,5|

Let W be all xmod10080 with xmod8=r and xmod315 inK_r. Then |W|=48.
The literal checker verifies W avoids P and lies in the actual base residual
specified below. The same cofactor value at different r denotes distinct
physical points; no parent or original resource is identified across fibers.

## Every threshold in the credited erasure hierarchy accepts K

For B subsetD, let Q_{q-1}(B) count labeled fibers that are empty or contained
in at most q-1 cofactor classes at DISTINCT labels inD minusB. This is a local
ability test. Its witnesses at separate parents do not assert simultaneous
tail allocation. There are four nonempty parents, giving eight first-layer
targets. With p=2 and k1=k2=12, the credited [9241 theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/few-class-erasers/proof.md)
has L=8-floor(12/2)=2. Its reduced cover inequality is

    4q(q-1) A_(q-1)(B) +(q-1)(2q-1)|B| >=4(q-1)(q-3).

Here A counts nonempty qualifying parents. Divide by q-1 and add the three
empty parents, so Q=A+3. The entire family is exactly

    4q Q_(q-1)(B) +(2q-1)|B| >=16q-12.                 (1)

For q=2 this is8Q1+3|B|>=20, the credited [9160 single-eraser specialization](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/eraser-matching/proof.md).
For q=3, multiply(1) by2 to obtain24Q2+10|B|>=72, whose [9309 finite reduction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/cardinality-cores/proof.md)
is credited. These inequalities are prior results, not new claims here.

If1 is not inB, its class covers every fiber and Q=7. If1 is inB, Q>=3 and
|B|>=1, giving27>=20 at q=2 and41>=36 at q=3. Thus both families accept any
configuration with these three empty parents, regardless of its other shapes.
The literal full-subset minima for K are27 and92 in the q2 and doubled q3
normalizations, respectively; all4096 subsets are checked for each.

For EVERY q>=4, split by the number of legal labels. If at least three remain,
each K_r has at most three points, which can be assigned one class each at
three distinct legal labels. Thus Q=7, and the difference in(1) is

    (12+2|B|)q +12-|B| >0.

If fewer than three remain, |B|>=10 and Q>=3. The difference is at least

    (2|B|-4)q +12-|B| >0.

Both expressions have nonnegative slope and are positive at q=4. This proves
the infinite threshold statement without extrapolating a finite q scan. The
source checks16068 explicit distinct-label three-class containments over4017
large-pool subsets, and the79 small-pool affine bounds. The assertion concerns
the common-q free12/12 hierarchy of9241, not an unspecified stronger mixed cut.

## Uniform ORIGINAL tail capacity strictly rejects K

For a cofactor configuration H define

    M_d=max_(r,a) |{y inH_r:y=a mod d}|.

CRT gives every cofactor phase at each binary child. One ORIGINAL16d class
occupies two of the four32-children of one parent, while one ORIGINAL32d class
occupies one. Its maximum count on the lifted H is therefore2M_d or M_d,
respectively. Consequently any tail completion must satisfy

    4 sum_r |H_r| <=3 sum_(d inD) M_d.                 (2)

Equivalently, this is the [credited original-resource capacity method](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_residual_weight_duals/proof.md)
at unit weight: each distinct modulus supplies at most its largest phase gain.
Omitted tail resources reduce this bound. Overlaps only reduce actual covered
union size, so their sum is a valid upper bound.

For K, M1=3, M3=2 and M_d=1 at every other d inD. Thus the right side of(2) is
3*(3+2+10)=45, whereas the left side is48. The independent physical audit
enumerates every ORIGINAL phase and confirms all24 maxima in [expected.json](expected.json).
The value45 is a sum of individual maxima, with no claim that a45-point union
is attainable. No solver result is a nonexistence premise.

## Sharp twelve-point minimum in the stated four-fiber domain

Consider arbitrary sets H_r contained in the initial P holes, supported only
on r in{2,4,6,7}, with all four physical copies. At r=2 or6, original12:10
removes exactly the cofactor residue1mod3, so these two fibers use only two
ternary residues. Let t=sum_r|H_r| and h=max_r|H_r|. If t>0, every M_d>=1,
and M1=h>=ceil(t/4). For1<=t<=10,

    3 sum_d M_d >=3*(ceil(t/4)+11) >=4t.

At t=11, if h>=4 the lower bound is at least45>=44. Otherwise the sizes are
3,3,3,2. At least one of r=2,6 has size3, forcing M3>=2 by pigeonhole. Hence
the budget is again at least3*(3+2+10)=45>=44. Empty configurations obey(2).
This proves that at most eleven points cannot strictly reverse the unit budget
in this domain. K has twelve and does. Both checkers verify the corresponding
1365 labeled cardinality vectors. This is a minimum for these four fibers
under unit weights; it asserts no minimum for arbitrary fibers or other weights.

## Actual shared-base realization and a necessary base clause

[fixture.json](fixture.json) gives one legal phase at EVERY one of the36
BASE resources. After P and those classes, the seven actual fiber sizes are

    [0,84,0,117,0,111,68],

so there are380 base points and1520 physical holes. Its full24-resource uniform
capacity is966. The entire actual residual passes all4096 q2 cuts and all4096
q3 cuts, with minima27 and92. It contains K. The infinite-q assertion above
is made for the twelve-point K, with no higher-q claim for this larger residual.
The stage is a partial distinct system with minimum exactly8 and LCM2520;
it is nonextendible using the remaining24 ORIGINAL10080-divisor resources.

This full shared-base control resolves the joint q2/q3-core feasibility question
positively. The previous9309 control satisfied only B={1,3}, not the whole q3
family; its abstract q2 nonreplacement control had no asserted base realization.
Here every phase is shared across all labeled fibers. The construction was
proposed by two bounded8s single-thread HiGHS runs, both TIME LIMIT with an
incumbent. Literal checks prove the stated positive properties; solver optimality,
discovery reproduction and numerical negative status are unused.

Let K0=W mod2520, with twelve distinct physical residues, and define

    A_n={x mod n:x inK0},  n inBASE.

Every cover extending P with ORIGINAL moduli dividing10080 must satisfy

    OR_(n inBASE,a inA_n) X_(n,a),                      (3)

where X selects that original congruence class. If every term were false, all
of W would remain for the tail, contradicting45<48. This argument also allows
omitted BASE resources. There are312 distinct terms; the displayed full stage
violates(3). [emit_cut.py](emit_cut.py) emits the compact class list; its canonical
JSON SHA256 is d5c52a1c1ca6b4017e7c42939164cdcd66208387f9c3335bef92c27b6cac8e8f.
This clause can augment the previous shared-base encoding while preserving
every original phase. It is a necessary restriction, not a root exclusion.

The same argument gives a reusable condition, beyond this one kernel. Call a
triple admissible if its points have pairwise different residues modulo5,7,9,
and are not all equal modulo3. If the actual residuals at EACH of r=2,4,6,7
contain an admissible triple, take those twelve points and leave the other
kernel fibers empty. Their M1=3 and M3<=2; the original12 restriction forces
M3=2 at r=2 or6. Every other label inD is divisible by5,7 or9, giving M_d=1.
Thus the same45<48 obstruction applies regardless of additional holes at ANY
parent. Every P completion must leave at least one of these four labeled
fibers without an admissible triple after its BASE stage.

[separate.py](separate.py) implements this necessary test and emits a violated
OR clause whenever it finds four triples. It scans all ordered pairs x<y;
literal residue masks retain exactly z>y that complete an admissible triple.
Hence failure to find a triple at a parent is a complete local diagnostic,
with no tail-feasibility conclusion. It reconstructs the frozen kernel and
agrees with direct triple enumeration on all256 subsets of a small control set.

## Reproduction and context

The self-contained standard-library [checker](check.py) uses lower-period fibers,
difference gcds, remainder classifiers and the CRT capacity formula. The separate
[audit](audit.py) imports none of those routines: it enumerates all10080 physical
points and ORIGINAL phase maxima, and literal315 phase unions. They agree on every
reported value. [verify.py](verify.py) runs six serial20s-guarded children in normal
and optimized modes, with source-integrity checks and twelve semantic certificate
damages rejected by each engine in both modes. These are different same-author
algorithms, not an independent review or a formal proof-assistant check.

The current [9331 frontier](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/aligned-twelve-nonalignment/proof.md)
has eleven unexcluded period10080 forms, including this P. Its original12
nonalignment is compatible with12:10 and8:0. The separate [9329 period720 bound](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-1/stage720-four-hole-bound/proof.md)
narrows a15120 route to99..110. Those numerical trees/tables are context, not
premises or fresh replays here. Global candidates10080/15120/20160 stay unchanged,
with only20160 witnessed in credited campaign work. [dependencies.json](dependencies.json)
records exact source commits, graph references and imported scopes.

Primary context reopened2026-10-02: [Zhang--Zhang](https://arxiv.org/html/2607.19029)
reports L_min(7)=10080 through filtering and final solver exclusions; [HKLT](https://arxiv.org/html/2605.18644)
studies the restricted2/3/5-prime minimum-modulus problem. Neither paper is a
numerical proof premise here. No literature-absence or historical-priority claim
is made. The new information is the infinite-hierarchy/capacity separation,
its sharp four-fiber kernel and its actual shared-base realization/necessary cut.
