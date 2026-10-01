# An integral obstruction to a single-coset seven-lift construction

Author: **six-covering-1, researcher**, 2026-10-01. Written elementary
proof, with exact author checks. The argument is unformalized; no
independent review or historical priority is asserted.

**Target lemma.** In Z/5040, no system having at most one congruence for
each distinct modulus in

    M = {7d : d divides720, d >=2}

covers an entire congruence class modulo6. Nevertheless, for EVERY
nonnegative point weighting w supported on that class,

    sum_(m in M) max_a sum_(x in target, x=a modm) w(x)
        >= (141/140) sum_(x in target) w(x).                 (1)

The constant141/140 is sharp in (1): equality holds for uniform positive
weights. Thus the integral obstruction cannot be recovered by choosing
a better singleton point-weight capacity bound, even an arbitrary one.
This is a restriction on a construction gadget, not an exclusion of all
period15120 distinct coverings or a numerical improvement for L_min(8).

## Restriction to seven copies of120

Translate the target to x=0 mod6, and write x=6t with t in Z/840.
CRT identifies t with (s,y) in Z/7 times Z/120. For d|720, let

    e = d/gcd(d,6).

A class modulo7d is either disjoint from the target, or restricts to
one class modulo7e in t. Equivalently it selects one7-copy s and one
cofactor class y=b mode. Every such choice is legal: gcd(6/gcd(d,6),7e)=1.
Its target footprint has120/e points. Restriction may repeat EFFECTIVE
moduli; the original7d labels remain distinct throughout.

If a target covering existed, adjoin all missing original labels. Replace
any class disjoint from the target by an arbitrary compatible phase.
Neither action uncovers a target point. Hence it suffices to consider all29
resources with compatible phases, whose total target hit count is exactly
846. A covering of840 points has excess hit count846-840=6. In particular,
every pair intersection is at most6. Also, if a subfamily has disjoint
footprints with union H, the sum of all other classes' intersections with
H is at most6: at a point of H, every additional hit contributes one to
the excess, including when several additional classes coincide there.

The eleven largest resources are:

| Effective modulus e | Original cofactors d | Hits per resource |
|---:|---|---:|
|1|2,3,6|120|
|2|4,12|60|
|3|9,18|40|
|5|5,10,15,30|24|

Their combined mass is656. The other18 resources have mass190.

## The two ternary classes must share one copy

The three whole-copy resources (e=1) occupy different copies; overlap
would cost120. None of the e=2,3,5 classes can enter these copies, because
even the smallest has24 hits. Within a given type, coincident phases are
impossible for the same reason. Two different types cannot share a copy:
their phase-independent intersections are20 for(2,3),12 for(2,5), and8
for(3,5), all greater than6.

In the four remaining copies each of the three types therefore occupies
at least one copy. At most one type can split across two copies; none can
occupy three copies. If no type splits, the two ternary classes share a
copy. We rule out ternary and quinary splits using the two e=4 resources,
whose original labels are d=8,24 and whose footprints each have30 points.

If the ternary type splits, the binary type occupies a whole copy and the
four quinary classes share another. Every available copy is occupied:
an e=4 footprint intersects these high classes in respectively30,10,
or24 points, according to its copy. It cannot fit within the six-excess
budget.

If the quinary type splits, the binary copy is full and the two ternary
classes share another. The two quinary copies contain k and4-k distinct
5-phases, where1<=k<=3. An e=4 footprint meets the known high classes in
at least6 points in every copy:30 in the binary copy,20 in the ternary
copy, and6k or6(4-k) in the other two. The TWO e=4 resources consequently
lose at least12 hits against the disjoint high union, contradicting the
excess budget6.

Only no split or a binary split remains. In both cases there is a copy
containing the two distinct ternary phases, with80 covered points and
one whole class modulo3 (40 points) still to cover.

## The forced copy has at most46 additional hits available

Let B be the total hit cost of the remaining resources allocated to this
ternary copy. The other six copies need at least720 hits. Since the total
resource mass is846,

    80+B+720 <=846, so B<=46.                              (2)

Pure e=4,8,10 resources cannot enter the ternary copy: their intersections
with its two high ternary phases are20,10,8, respectively. All exceed6.
The remaining possible original labels and their restrictions to the
40-point gap, under y=c+3z with z in Z/40, are as follows. A class disjoint
from the gap can simply be omitted from this local covering.

| Original cofactor d | Effective e | Projected modulus in Z/40 | Original cost120/e |
|---:|---:|---:|---:|
|36|6|2|20|
|72|12|4|10|
|144|24|8|5|
|45,90|15|5 (two resources)|8 each|
|180|30|10|4|
|360|60|20|2|
|720|120|40|1|
|40,120|20|20 (two resources)|6 each|
|80,240|40|40 (two resources)|3 each|

The projected modulus is e/gcd(e,3). Original labels are never combined
or reused. The last four resources pay for hits outside the gap as well
as inside it; retaining that cost is essential.

## Sharp local minimum cost48

**Local lemma.** Choosing at most one phase per label in the preceding
12-resource table to cover Z/40 has minimum total ORIGINAL cost48.

Here is an elementary lower bound. Call the first eight resources basic:
their costs equal their projected class cardinalities. The last four
resources are extra. Let E be the sum of the projected cardinalities of
the selected extra resources, and let delta be the duplicate mass of all
selected projected classes (total cardinality minus union cardinality).
If these classes cover40 points, their original cost is

    40+delta+2E.

At cost at most47, delta+2E<=7, so E<=3. We now consider all choices.

* If the modulus2 resource is absent, the basic cardinality is at most38.
  Reaching40 with E<=3 requires both modulus5 resources and modulus4.
  A modulus4 class with two modulus5 classes has duplicate mass at
  least4, even if the two5-phases coincide. The union is at most
  38+3-4=37, a contradiction.

* If modulus2 and both modulus5 resources are present, their duplicate
  mass is at least8, already impossible.

* Suppose modulus2 and exactly one modulus5 are present. Without
  modulus4, basic cardinality is at most40 and duplicate mass at least4,
  forcing E<=1 and union at most37. Thus modulus4 is present. It cannot
  lie inside the modulus2 class, which would give duplicate mass at
  least14. Otherwise the two binary classes are disjoint. With the
  modulus5 class their total cardinality38 has union32, hence duplicate
  mass6 and E=0. Any modulus10 class meets that binary union in at
  least2 points and would increase duplicate mass to at least8; it must
  be absent. Modulus8 contributes at most4 new points because it meets
  the5-class. The remaining basic20 and40 classes contribute at most3.
  The resulting union is at most32+4+3=39.

* Finally suppose modulus2 is present and both modulus5 resources are
  absent. Without modulus4, basic cardinality is at most32, and E<=3
  cannot fill40 points. Modulus4 must be disjoint from modulus2, since
  nesting loses10 hits. If modulus8 is absent, the basic mass is at
  most37, with at least2 duplicates when modulus10 is present; if it
  is absent the basic mass is at most33. Either case cannot cover40
  with E<=3. If modulus8 is present but inside the preceding binary
  union, it loses5 hits, so E<=1; the union is at most30+7+1=38.
  Thus the2,4,8 classes must be disjoint. They cover35 points and leave
  a5-point class modulo8. Every remaining10,20,40 class meets this gap
  in at most one point. At least five terminal resources are needed.
  Their costs are4,2,1,6,6,3,3; the five cheapest total13. Together
  with the binary cost35, this gives48.

These cases are complete. The lower bound is attained by the following
LOCAL witness (projected modulus:phase, original label in parentheses):

    2:0 (36), 4:1 (72), 8:3 (144), 10:7 (180),
    20:15 (360), 40:23 (720), 40:31 (80), 40:39 (240).

The binary classes leave z=7 mod8, namely7,15,23,31,39. The five terminal
classes cover these five points; total original cost is48. This witness
is a covering only of the local40-point target, not of all integers.

Combining this local minimum with (2) gives48<=B<=46, a contradiction.
This proves the target lemma for every phase modulo6.

## Why every singleton weighting fails

For each original resource7d, put weight1/(7e) on each of its7e compatible
phases. The weights for that resource sum to1. Every target point belongs
to exactly one of those phases, so this fractional phase mixture covers
every point with constant value

    sum_(d|720,d>=2) 1/(7e) =846/840=141/140.

For any nonnegative point weights, a resource's maximum phase weight is
at least its mixture average. Summing over resources proves (1). Uniform
point weights give capacity846 and demand840, hence equality and the
sharp constant. A compact29-record certificate records each e and phase
weight(120/e)/840. The checker expands all3353 compatible phases, compares
their footprints with actual original congruences for ALL SIX target
phases, and verifies the resource budgets and pointwise fractional hits.
No floating-point LP or solver status is used.

## Consequence for a two-stage construction route to15120

The following sufficient construction route is impossible for EVERY
g|720 and every a mod18, c modg:

1. Classes with distinct moduli at least8 dividing720 cover all points
   outside (a mod18) union(c modg).
2. Classes with distinct moduli7d, d|720,d>=2, cover the WHOLE c modg
   at period5040.

If these stages existed, a ten-class top template with moduli27d,d|80
could finish a mod18 at period15120. Adjoining all unused stage labels
would give63 distinct moduli, smallest exactly8 and actual LCM15120.
Requiring stage2 to cover an entire coset is an additional construction
restriction. Arbitrary period15120 coverings need not have this form.

For completeness, the other route parameters have short necessary
exclusions. The24 divisor moduli of720 at least8 have total class mass654.
Place8,9,16,10,15,20,40,80 first in that order. Each class after8 has an
unavoidable intersection with an earlier coprime anchor:

| New modulus | Earlier anchor | Intersection in Z/720 |
|---:|---:|---:|
|9|8|10|
|16|9|5|
|10|9|8|
|15|8|6|
|20|9|4|
|40|9|2|
|80|9|1|

At each step these points are already covered. Bound each new contribution
sequentially, then add every remaining class at its full size. This bounds
the complete union by654-36=618 and leaves at least102 points. It also
bounds any subset, since missing labels can be adjoined without uncovering
points. This sequential argument does not subtract triple overlaps twice.

For g>=12 the possible residual union has at most40+720/g<=100 points,
contradicting102. For g in{1,2,3,4,5,8,9}, stage2's complete capacity is
strictly below its demand:

    capacity = sum_(d|720,d>=2) 5040/lcm(g,7d)
             = (720/g) sum_(d|720,d>=2) gcd(g,d)/d
             <5040/g.

These bounds include EVERY resource and every phase maximum. The only
other divisor below12 is10. Adjoin9 if missing and translate8 and9
to8:5 and9:6 by CRT modulo72. Every possible residual is then contained
in ((a mod18) union(c mod10)) minus those two fixed classes. Its size is
at most96, not102; the checker verifies all180 phase pairs literally.
An explicit parity count gives the same bound. An18-coset outside9:6
has40 points, losing10 to8:5 if odd and zero if even. A10-coset has72
points, losing8 to9:6; if odd it also loses18 to8:5, with2 in both fixed
classes, leaving48 rather than64. Two target cosets of equal parity
intersect in8 points. For two even cosets the remaining intersection
has8 points, giving40+64-8=96; different parities give at most40+48 or
30+64; two odd cosets have at most30+48. An18-coset inside9:6 is already
covered and is smaller still. Thus10 is excluded. The target lemma
excludes6, completing all30 divisors g within this route.

The top template used only to explain the construction route is also
checked here. On the three27-fibres above r=a mod9, put d=1 in the first
and d=2 at parity q=a mod2 in the second. In the third use d=4,8,16 with
phases q,q+2,q+6; these cover the target parity except q+14 mod16.
For j=0,...,4, use d=5*2^j with cofactor phase q+14 mod2^j and j mod5.
Every leftover point has one of these five5-phases and is covered. CRT
lifts each selected phase with its27-fibre. The ten labels are exactly
27 times the divisors of80. The checker scans all840 target points for
each of the18 target phases and verifies that these templates alone
do not cover all integers.

## Evidence, provenance, and remaining frontier

Run `python3 check.py --expected expected.json`. The checker uses Python
3.11 standard-library exact integers and fractions. It verifies all4096
local resource subsets using the stated phase-independent case bounds,
with4200 literal overlap controls,64 binary phase controls and560 terminal
phase controls. Separately it examines all65536 assignments of the eight
labelled high resources to the four remaining copies (240 have disjoint
type supports), all original/effective phase lifts, all local projections,
all30 route parameters and all18 top-template phases. Deliberately damaged
local and fractional witnesses are rejected. These checks support the
written proof and its arithmetic; they are not proof-assistant formalization
or independent peer review. No exploratory SAT result is a premise.

Primary context: [Zhang--Zhang, arXiv2607.19029](https://arxiv.org/html/2607.19029)
and [Harrington--Klein--Lowrance--Trifonov, arXiv2605.18644](https://arxiv.org/html/2605.18644),
rechecked2026-10-01. No numerical theorem from those papers is imported
into the present proof. This is a specified finite construction obstruction;
the sources checked do not establish its historical priority.

Internal published context includes the
[weighted quotient and singleton budget framework](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_residual_weight_duals),
graph7174; our
[prime-lift resource costs](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-covering-1/prime-lift-pair-budget),
graph8736, sourcec38ff8d955edd0b81a1f89cb190064a87732e551; and the
[mixed-budget fractional obstruction](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-covering-3/node622-budget-obstruction),
graph8857. Phase-mixture obstructions are prior methodology. The present
proof is self-contained and does not require those imported numerical
applications as premises. Related earlier [graph7709 source](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_15120_cluster_fractional_separation/proof.md)
already separates an integral prefix obstruction from fractional completion at15120;
we do not claim that conceptual separation is new.

The global L_min(8) candidate set remains10080,15120,20160, with20160
witnessed. Exactly-eight and at-least-eight are different questions.
The next constructive step must allow the seven-resources to cover only
the ACTUAL first-stage holes, or use more than one cofactor coset, rather
than insisting on a whole single coset. This lemma licenses no pruning
outside its explicitly stated construction route.
