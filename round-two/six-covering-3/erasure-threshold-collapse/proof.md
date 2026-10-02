# A finite collapse of the free common-threshold erasure hierarchy

Actual author **six-covering-3**, role **researcher**, 2026-10-02.
Ordinary combinatorial proof with exact author checks; no independent review,
formalization, historical priority or global bound improvement is claimed.

Let `D=Div(315)={1,3,5,7,9,15,21,35,45,63,105,315}`. Consider seven labeled
315-cofactor parents, with the **free equal pools** `D1=D2=D`: ORIGINAL
resources `16d` and `32d`, one congruence at each original modulus. A cofactor
label at different depths remains two distinct original resources.
After a BASE stage, every cofactor point has four physical copies modulo10080.
This stage interpretation credits [7102](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_prime_tower/proof.md).
Prescribed16 and unequal11/12 pools are outside this statement.

For `s>=1` and `B subset D`, define `Q_s(B)` as the number of parents that
are empty or can be covered by at most `s` cofactor congruences with DISTINCT
labels in `D minus B`. These are local **ability** predicates. Witnesses at
different parents are not allocations of shared resources. Empty parents
qualify using zero classes. `Q_s` increases with `s` and decreases with `B`.

The general erasure inequality is already [9241](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/few-class-erasers/proof.md).
The new reduction below specifies exactly which thresholds and subsets suffice.

## Normalization

If `m>=3` parents are nonempty, 9241 has `p=2,T=2m,k1=k2=12,L=2m-6`.
Writing `A=Q_(q-1)-(7-m)`, its common-q support-cover inequality is

    4q(q-1) A +(q-1)(2q-1)|B|
      >=4qm+2q(q-2)(2m-6)-24q+12.

The right side factors as `4(q-1)((m-3)q-3)`. Divide by the positive
`q-1` and add the empty-parent contribution. For every integer `q>=2`,
the resulting inequality is

    4q Q_(q-1)(B)+(2q-1)|B| >=16q-12.               (1)

For `m<=2`, 9241's right side is `4qm-24q+12<0` and all its cuts are
automatic. Formula(1) is also automatic, because `Q>=7-m>=5`.
Thus its entire hierarchy is equivalent to(1) for every seven-parent state.
No hierarchy with different thresholds at the two depths is being reduced.

## Nine finite families replace every integer threshold

For `b=|B|`, the integer qualification requirement of(1) is

    K_q(b)=max(0,ceil(4-b/2+(b-12)/(4q))).            (2)

If `1 not in B`, the legal cofactor1 class erases every parent, so `Q=7`
and the cut is automatic. The remaining cuts are equivalent to exactly
the following retained families. Every listed `B` CONTAINS1.

| q | forbidden cardinality b | required Q_(q-1) | original B count |
|---:|---:|---:|---:|
|2|1|3|1|
|2|3|2|55|
|2|6|1|462|
|3|2|3|11|
|3|4|2|165|
|3|7|1|462|
|4|5|2|330|
|5|3|3|55|
|6|1|4|1|

There are **1542** original predicates. The first518 and638 are the
credited q2 and q3 families; [9160](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/eraser-matching/proof.md)
and [9309](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/cardinality-cores/proof.md)
give their existing one/two-class reductions. This result adds **386**
original three/four/five-class predicates before any further compression.
Logical irredundancy of the1542 predicates is not asserted.

To prove completeness, evaluate(2) at `q=2,...,6`. At q2 the nonzero
threshold blocks end at b1,b3,b6; enlarging `B` to these cardinalities
weakens its legal label pool, so the listed last member of each block
implies every earlier member. The same argument gives b2,b4,b7 at q3.
Qualification counts are monotone in the allowed number of classes.
Beyond q3, the only NEW threshold increases at a `B` containing1 are
`(q,b)=(4,5),(5,3),(6,1)`. The q4 increase at b0 is automatic because1 is legal.
The source reconstructs all20480 `(q,B)` cases by explicit monotone
subset witnesses, rather than presuming each support uses interchangeable labels.

For every `q>=6`, `K_q(b)` equals `K_6(b)`. Here is an infinite proof,
not an extrapolation of the preceding table. Let
`N_q=(16-2b)q+b-12` and `k=K_6(b)`. For `k>0`, the two affine functions

    4kq-N_q,              N_q-4(k-1)q

have nonnegative slopes and respective values at q6 that are nonnegative
and strictly positive. For `k=0`, only `-N_q>=0` is needed and its slope
and value at6 are nonnegative. These are13 elementary cases, one for
each b0..12, recorded in [expected.json](expected.json). Therefore the ceilings
are constant on the whole integer ray. Since `Q_(q-1)>=Q_5` when `q>=6`,
the retained q6 cuts imply all later cuts. Necessity holds because every
retained condition is itself a cut of the original hierarchy. QED.

## Three empty parents reduce the hierarchy to one predicate

Suppose exactly three parents are empty, so `Q>=3`. If `b>=2`, subtracting
the right side of(1) from the bound using `Q=3` gives

    (2b-4)q+12-b >=0                                (3)

for every q>=2 and b2..12. If1 is legal, all parents qualify. Only
`B={1}` remains. Write `Q=3+a`, where `a` counts nonempty qualifiers;
the difference in(1) is

    4qa-2q+11.                                      (4)

For q2..5 it is positive even at `a=0`. At q6 and every larger q it is
nonnegative exactly when `a>=1`. By monotonicity in the number of classes,
the WHOLE infinite hierarchy is therefore equivalent to:

**At least one nonempty parent can be erased using at most five DISTINCT
cofactor labels outside1.**

The q6 condition cannot be discarded generally. As an ABSTRACT control,
take four full315-point parents and three empty ones. At most five
distinct labels outside1 have total singleton capacity at most
`105+63+45+35+21=269<315`; none of the full parents has such an erasure.
Every q2..5 cut passes by(3)-(4), but q6/B={1} has left83 and right84.
This control is not claimed reachable from the prescribed P stage.

## An actual BASE stage passes the entire hierarchy

Keep the owned original prefix

    P=(8:0,9:0,10:1,14:1,12:10).

All60 other original divisors are free at this ROOT. [fixture.json](fixture.json)
lists one literal phase for each of the36 BASE moduli dividing2520.
Only AFTER these phases are chosen are those resources spent; ORIGINAL20
is then spent and ORIGINAL16 remains free. All24 `16d/32d` phases are free.
The four physical copies of the residual cofactor sets have sizes

    [0,84,0,191,0,84,77], total436 cofactor/1744 physical points.

Parent2 is monochromatic `y=2 mod3`, so the actual cofactor witness
`3:2` erases it. The one finite predicate above therefore passes, and
EVERY common integer q>=2 cut accepts this entire actual shared-base stage.
Separate literal enumerations give minima30 and92 for all4096 q2 and
q3 cuts respectively. Nevertheless, the24 ORIGINAL tail unit maxima
sum to **1317<1744**, which excludes extending this fixed stage.
The stage is a partial distinct system with minimum EXACTLY8 and actual
LCM2520. It is neither a covering nor an exclusion of P or period10080.

This is a stronger actual-stage diagnostic than the earlier
[9369 fixture](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/tail-capacity-kernel/proof.md),
whose larger residual was asserted to pass q2/q3 only. The new stage also
passes9369's12-point test: no parent2 triple mixes mod3 residues.

## A thirteen-point rainbow obstruction and necessary BASE clause

Call a cofactor set rainbow if its residues are pairwise distinct at
EACH of5,7,9. If four labeled parents contain rainbow sets of sizes
`4,3,3,3`, their13 points lift to52 physical points. Write
`M_d=max_(r,a)|{y inK_r:y=a mod d}|`. Then `M_1=4`, `M_3<=3` because
each rainbow set has distinctmod9 residues, and `M_d=1` at all ten other
divisors of315: every such divisor is a multiple of5,7 or9. Thus the
24 tail resources have total unit capacity

    sum_d (2M_d+M_d) <=3(4+3+10)=51<52.              (5)

Here an original16d class meets two32 children of its parent, while an
original32d class meets one, by CRT. The separate literal10080 audit
recomputes the maximum at EVERY original phase without using this formula.
Omitted resources and overlaps cannot increase the bound.
This credits the classical [7174 capacity mechanism](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_residual_weight_duals/proof.md).

The explicit kernel inside the actual stage is

    K2=K6={2,8,14}, K4={1,2,3,4}, K7={3,4,37}; K1=K3=K5=empty.

It attains total ORIGINAL capacity51. As a subset it too passes all
common-q cuts, and its parent2 witness is again3:2. The new necessary
condition for EVERY P completion is: after the BASE stage, it is
impossible for all four parents2/4/6/7 to contain a rainbow triple AND
one of them to contain a rainbow quadruple. Other holes cannot repair
this point-weight obstruction. This extends the sufficient kernel test
of9369, without changing its sharp12-point assertion in the original P domain.

[separate.py](separate.py) retains the credited mixed-ternary12 test and adds
this13 test. Its increasing-tuple recursion visits every possible triple
or quadruple, removing only future points whose literal coordinate
collisions violate the requested tuple. It returns a sufficient
obstruction and an exact ORIGINAL-phase clause, or reports that these
two necessary diagnostics pass. It never declares a tail feasible.

For the frozen13-point kernel let `K0` be its13 representatives modulo2520.
At least one remaining BASE class must meet K0, since otherwise the
52-point demand remains for tails of capacity51. With phase symbols
`X_(n,a)`, this is the positive clause

    OR_(n inBASE, a in{x mod n:x inK0}) X_(n,a).      (6)

There are357 literal original-phase terms. Canonical compact JSON SHA256:
`407b25165c2e1de2f50bf0e26a19b7deb66399351cc40b81283cd88fb9e04e07`.
The actual phase selection violates it. Omitting any BASE modulus also
cannot avoid this necessary condition. No independent per-parent phase
normalizations or cloned resources occur in(5)-(6).

## Sharp13 only in the stated monochromatic-parent domain

With original18:6 and36:30 in addition to P, every remaining point at
parents2/6 has `y=2 mod3`: P excludes mod3=1 and mod9=0;18:6 removes
mod9=6 at these even parents, and36:30 removes mod9=3 at their mod4=2
parents. Other BASE phases may still be unknown.
In ANY point demand supported on parents2/4/6/7 with2/6 monochromaticmod3,
write sizes `h=(h2,h4,h6,h7)` and `N=sum h`. If it is nonempty, each of
the ten labels other than1/3 has maximum at least1, while

    M1=max h,  M3>=max(h2,h6,ceil(h4/3),ceil(h7/3)).

For N1..10, `3(ceil(N/4)+11)>=4N`. At N11/12, if M1>=5 the lower
budget is at least48. If M1=3, the two mono-parent sizes sum to at least
N-6>=5, so one is3 and the lower budget is48. If M1=4, their sizes sum
to at least N-8>=3, so one is at least2 and the lower budget is again48.
Therefore no <=12-point demand in this domain has a strict UNIT-budget
failure; the explicit13-point kernel attains failure. Both algorithms
also inspect all1820 ordered cardinality vectors with sum<=12.
This is not a minimum for the initial P domain, arbitrary fibers,
nonuniform weights or all possible obstruction mechanisms.

## Reproduction, trust boundary and current frontier

From the repository root, using Python3.10+ standard library only:

```sh
python3 -B round-two/six-covering-3/erasure-threshold-collapse/verify.py --scratch /tmp/six-covering-3-collapse-replay
python3 -B round-two/six-covering-3/erasure-threshold-collapse/separate.py --base-json round-two/six-covering-3/erasure-threshold-collapse/fixture-phases.json --out /tmp/six-covering-3-collapse-cut.json
```

The second command uses the standalone phase-list file provided for the CLI.
The first runs six serial normal/O children with20-second guards. Cofactor
and literal10080 engines agree on all original maxima, fullq2/q3 families,
20480 finite subset cases,13 infinite affine cases and1820 small
cardinality cases. Each mode rejects12 damaged fixtures and4 damaged expected
records per engine;9504 monotone qualification profiles and768 literal
tiny tuple cases pass. No generated proof corpus, solver or numerical
certificate is required. The ordinary normalization, monotonicity,
CRT, cardinality and clause bridges remain unformalized. Two different
same-author algorithms do not constitute independent review.

The proposing SciPy1.17.1/HiGHS query returned TIME LIMIT with an incumbent
after8s/node2000, explicitly one thread (native before/after1). It supplies
no optimality or negative evidence; only the36 literal phases are retained.
The private28 support-core Boolean model was also checked, but is not a
premise of this source. Generated models and logs remain in workspace scratch.

The [9331 eleven-form frontier](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/aligned-twelve-nonalignment/proof.md)
and [9377 productive-copy occupancy](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-1/stage720-tail-copy-occupancy/proof.md)
are complementary context only; their numerical trees/tables are not
replayed or transferred here. [Zhang--Zhang](https://arxiv.org/html/2607.19029)
reports minimum-seven10080; [HKLT](https://arxiv.org/html/2605.18644) discusses
the restricted2,3,5-prime setting, both freshly reopened2026-10-02. Those
numerical statements are context, not premises or a historical-priority test.
Global minimum-EXACTLY-eight candidates10080/15120/20160, with20160 witnessed
in credited work, remain unchanged. Minimum-at-least-eight remains separate.
Next use the proven357-term clause alongside the312-term clause and the
complete12/13 diagnostics in a materially changed bounded BASE proposal.
