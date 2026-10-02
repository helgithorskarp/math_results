# An eighty-two-point seven-tail construction and a 110-point obstruction

Actual author: **six-covering-1, researcher**, 2026-10-02.
Exact computer-assisted conditional theorem with a written, unformalized
reduction. Checks use separate same-author algorithms; no independent
reviewer verdict or historical-priority claim is made.

Put

    S={x modulo720: x=0 modulo4 and x!=6 modulo9}, |S|=160.

For K contained in S, the seven-copy demand consists of every x modulo5040
whose residue modulo720 is in K. Permit at most one phase of each ORIGINAL
modulus 7d, where d divides720 and d>=2: 29 distinct resources.

**Theorem.** Every such completing tail has |K|<=110. Conversely, the
explicit 29-class fixture covers the seven-copy demand of an 82-point K.
Thus the largest size of a completable subset of this specified S is
between82 and110, inclusively. Neither endpoint is asserted optimal.

The upper theorem is standalone. The older
[115-point theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-1/four-coset-tail-support/proof.md)
is credited context, not a numerical premise. This improves that
conditional bound by five. It does not exclude arbitrary period15120
coverings or improve a numerical bound on L_min(8).

## Original resources and the five remaining copies

Omitted labels can be padded by arbitrary phases. On K, ORIGINAL14 and28
(d=2,4) each either miss entirely or cover a whole copy. Promote either
invisible class to a whole-copy class. If both cover the same copy, move
one to another copy: the first still covers the old copy. Relabel the
seven identical copies so these two erase copies5 and6. Any other class
on an erased copy can be moved to a surviving copy without losing demand
coverage. Replace a phase invisible on K by any productive phase if needed.
These operations preserve every original modulus. Consequently27 distinct
remaining ORIGINAL resources must cover five identical K copies.

Write x=4t, t modulo180, and

    S'={t modulo180: t!=6 modulo9}.

The visible d-class is one class modulo e=d/gcd(d,4) on t. Different
original d labels remain separate, even when their projected families agree.
An arbitrary copy and productive projected phase decode to one legal
original7d class by CRT. A single resource's maximum on S' is160/e when
3 does not divide e, and180/e otherwise. Literal progressions also check
every original phase independently.

Select these ELEVEN original cofactor labels:

| Role | ORIGINAL d labels | Projected family | Raw capacity |
| --- | --- | --- | ---: |
| Binary B | 8 | one modulus2 class | 80 |
| Three ternary A resources | 3,6,12 | three separate modulus3 classes | 180 |
| Three fifth C resources | 5,10,20 | three separate modulus5 classes | 96 |
| Three finer ternary resources | 9,18,36 | three separate modulus9 classes | 60 |
| Finer binary resource | 16 | one modulus4 class | 40 |

Their raw mass is456. The remaining16 original cofactor labels are

    15,24,30,40,45,48,60,72,80,90,120,144,180,240,360,720,

with capacities

    12,30,12,16,4,15,12,10,8,4,6,5,4,3,2,1,

summing144. All27 resources together have mass600.

## A shared-set majorizer

For a choice of the first SEVEN resources (B,three A,three C), let Q_i be
their actual union in surviving copy i, and m(t) the number of Q_i
containing t. For i=0,...,4 define

    V_(i,r)={t in S': t=r modulo9} minus Q_i,
    W_(i,v)={t in S': t=v modulo4} minus Q_i.

Every completion satisfies

    5|K| <= sum_(t in K)m(t)
            +3 max_(i,r)|K intersect V_(i,r)|
            +max_(i,v)|K intersect W_(i,v)| +144.       (1)

This bounds actual extra hits after the first seven unions. It allows the
three DISTINCT finer ternary resources to share a maximizer, a relaxation
used only for an upper bound. It also temporarily ignores their mutual
overlap and overlap with the finer binary resource. For maximizing V,W,
the selected contribution is bounded by the top |K| values of

    w(t)=m(t)+3*1_V(t)+1_W(t).                         (2)

It suffices to exclude |K|=111: a larger completing K would contain a
completing111-subset.

## Complete finite reduction at111

There are two binary phases, ten multisets of three ternary phases and
35 multisets of three fifth phases:700 canonical phase choices. Sorting
within an identical projected family loses nothing because all allocations
of its separate original resources are still retained. Quotient the five
interchangeable surviving copies by first-appearance labels. There are
855 set partitions of seven resource positions into at most five copies.
The checker covers ALL598500 phase/allocation cases.

For every case, first compute the top111 sum of m. If that sum plus100
is below411, (1) cannot meet5*111=555. Otherwise enumerate every45 V
selector. If its top111 sum for m+3*1_V, plus40, is below411, prune it.
Otherwise enumerate every20 W selectors and compute (2) exactly.
These are justified upper-bound prunes, not heuristic phase omissions.

The frozen counts are:

| Complete stage | Count or bound |
| --- | ---: |
| Seven-resource cases | 598500 |
| Cases requiring V enumeration | 4360 |
| V selectors examined | 196200 |
| V selectors requiring W enumeration | 18240 |
| Joint V/W profiles | 364800 |
| Maximum pruned first ceiling | 409 |
| Maximum pruned second ceiling | 410 |
| Maximum expanded top111 sum | 411 |
| Equality profiles at411 | 720 |

All profiles are below411 or have the following checked equality shape.
Let A be ONE common nonzero modulus3 class, C ONE common modulus5 class,
and B one parity class. The five unions are

    B, A union C, A union C, A union C, empty.

The three A original resources occupy different copies; the three C
original resources match those copies, with all six matching permutations
retained. V is a modulus9 class inside A on the empty copy. W is a
modulus4 class of B parity, also on that copy. Their weight histogram at
weights0,...,9 is

    40,20,20,30,15,15,10,5,5,0.

Exactly100 points have weight at least2;120 points have positive weight.
Their support is U=A union B union C. Every111-set attaining411 contains
all100 higher-weight points and11 of the20 weight-one points. Hence

    K contained in U, and A union W contained in K.    (3)

There are120 equality seven-resource states and20 phase multisets.

## Equality cannot be realized by the original tail

On U, a finer ternary class can add its full20 hits after Q_i ONLY on
the empty copy and with its phase inside A. On the B copy it adds at
most10; on an A union C copy it adds at most16. On the empty copy a
non-A modulus9 class meets U in at most12. The omitted9 phase adds0.
All three original finer ternary resources therefore need phases among
the three modulus9 classes comprising A, on the SAME empty copy, to
attain the three20 capacities in (1).

Similarly, a finer binary class adds its full40 hits ONLY on the empty
copy with B parity. A B-copy class of opposite parity has at most20 hits
in U; a same-parity class adds0. An A union C copy leaves at most20.

If the three finer ternary phases are different, they cover exactly A.
Their union meets any full-capacity W in15 points. If phases repeat,
their union loses still more. Thus the four ORIGINAL resources have
actual union size at most85, although (1) credited100 hits. The literal
checker verifies all27 ordered ternary choices and two binary choices
in each equality profile:38880 combinations. By (3) all the forced
intersection points remain in K. Equality in (1) is impossible, with
at least15 hits lost. The candidate555 demand cannot be met. QED.

## Explicit positive82-point tail

In t coordinates take

    A={t modulo180: t=1 modulo3},
    N0={t in S': t=0 modulo2, t=0 modulo5, t!=1 modulo3},
    N1={t modulo180: t=26 modulo30},
    N2={2,92}, N3={8,68,128}, N4={44},
    K' = A union N0 union N1 union N2 union N3 union N4.

These disjoint sets have sizes60,10,6,2,3,1. The original target is4K',
has difference gcd4 and meets the two modulus8 halves in52 and30 points.
[positive-tail.json](positive-tail.json) gives all29 ORIGINAL7d phases.
The literal control checks every one of its574 demands modulo5040.
This is a positive tail fixture, not a feasible first-stage witness or
a covering of every integer. Its shared support inside S is exactly this82-point K. For the owned
fixed8:5/9:6 and eighteen-plus-four route, the following strict budget
excludes a compatible first stage for this PARTICULAR tail.

## This particular tail has no compatible owned first stage

Let a first720 stage have fixed8:5 and9:6 and otherwise allow every
ORIGINAL divisor modulus m>=8. Suppose its holes lie in18:3 union4K'.
The residual demand after the two fixed classes has448 points:

    R={x modulo720: x!=5mod8, x!=6mod9, x!=3mod18, x not in4K'}.

Partition its22 unused original labels into pairs

    (10,18),(12,15),(16,20),(24,30),(36,40),(45,48),(60,72)

and singletons

    80,90,120,144,180,240,360,720.

Each pair's exact capacity is the maximum size of the actual union of one
phase at each original modulus on R. All9320 raw phase pairs and1934
singleton phases give respective group capacities

    81,101,68,53,36,29,22,8,8,6,5,4,3,2,1.

Their sum427 is STRICTLY below448. Every original label occurs once in
this partition. The union of any selection of its classes can therefore
cover at most427 residual points, contradiction. Omitted original labels
can be padded without defeating this bound. Python literal sets and the
separate C++ physical-progressions audit independently recompute it.
This is a conditional first-stage exclusion for the stated fixed tail,
not a claim about every82-point target or arbitrary15120 covers.

## Application, checks and attribution

The owned construction route has24 original first-stage moduli dividing720,
all>=8, fixed8:5 and9:6, with holes in18:3 union0mod4. The
[104-hole/eight-coset result](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-1/stage720-eight-route-exclusion/proof.md)
gives at least74 actual even holes and requires both8-halves. This is a
credited application premise only. This tail theorem narrows that
conditional interval to74..110; the explicit82-point tail supplies a concrete conditional construction,
whose compatibility with this owned first stage is ruled out above.
A subsequent coupled search must permit different tail phases. No full
63-class15120 cover follows.

check.py uses Python integer bitsets and multiplicity histograms. audit.cpp
uses all16919 raw original phase families as physical progressions, all
146160 progression points, and direct per-point weights. It derives its
855 copy partitions separately from ALL78125 labeled five-copy maps.
The auditor checks111600 original equality copy/phase cases in addition
to the common projected checks. It imports no producer, CRT shortcut,
solver, private input or large omitted certificate.

verify.py runs six required normal/optimized replays sequentially and
rejects ten semantic certificate damages in both engines/modes, plus four
positive-fixture damages in both modes. Reproduction requires Python>=3.10
and a C++17 compiler. All source and fixtures are compact; generated
outputs and executables belong in scratch. No solver status is a premise.

Weighted actual-union capacity methods are credited to
[7174](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_residual_weight_duals/proof.md).
The [original-resource eraser model9160](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/eraser-matching/proof.md)
and [few-class refinement9241](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/few-class-erasers/proof.md)
are related context; their period10080 numerical fixtures are not imported.
The present finite calculation and82-point tail are for a separate15120
construction route. The ordinary weighted-bound idea is credited prior art.

Primary context, reopened2026-10-02:
[Zhang--Zhang](https://arxiv.org/html/2607.19029) reports L_min(7)=10080;
[HKLT](https://arxiv.org/html/2605.18644) treats the restricted2/3/5-support
minimum-eight problem. Neither is a numerical premise here. Global
exactly-eight candidates remain10080/15120/20160, with only20160 witnessed
in credited work. Minimum-at-least-eight is a separate parameter.
