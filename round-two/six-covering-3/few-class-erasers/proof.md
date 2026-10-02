# Few-class erasure supports in two remaining prime layers

Actual author: **six-covering-3, researcher**, 2026-10-02. Complete written
derivation and independently coded same-author exact fixtures. No independent
review or formal proof is claimed.

## The resource model and cheap supports

Start with T nonempty first-layer target fibers V_i. A first-layer
resource is assigned to at most one of these labeled fibers and removes
one legal cofactor class from it. There are k1 original resources, labeled
by D1. Each surviving fiber then has p identical children, p>=2. The last
layer has k2 different original resources, labeled by D2, each assigned
to one child and removing one legal cofactor class. The cofactor class
family for a label agrees between depths when that label occurs in both
pools. A resource cannot be used at two prefixes within one layer.

The prime-tower interpretation, including exact residual states and the
basic horizon bound, is prior [contribution7102](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_prime_tower/proof.md).
The case of single-class erasers is [9160](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/eraser-matching/proof.md);
its unequal-pool refinement is [9172](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/prescribed-sixteen-allocation/proof.md)
by six-covering-2.
The argument below retains erasure supports involving several classes.

Fix an integer q>=2. For every original target V_i and every resource
subset S contained in D1 OR in D2 with 1<=|S|<q, put a hyperedge {i} unionS
when one legal class at each distinct label of S can together cover V_i.
S is a **cheap erasure support**; its phase choices need only exist.
The hypergraph uses target vertices and the cofactor labels D1 unionD2.
Shared cofactor labels do not identify the two original moduli.

Let(C,B) meet every hyperedge, with C a set of target vertices and B a set
of resource labels. Equivalently, every cheap support for any V_i outsideC
uses at least one label in B. Write c=|C| and bj=|B intersectDj|.

**Lemma.** Every completing two-layer assignment satisfies

    pq(q-1)c + p(q-1)^2 b1 + (q-1)b2
      >= pqT + pq(q-2)L - p(q-1)k1 - k2,              (1)

where

    L = max(0, T-floor(k2/p)).                         (2)

Any hypergraph cover gives a necessary cut. A failed cut excludes this
conditional state; passing all these cuts is not asserted sufficient.

## Proof

Let E first-layer targets be erased and h surviving targets be changed.
Every erased target requires at least one resource. If it receives fewer
than q, its resources constitute a cheap support. When its vertex is
outsideC, it must therefore receive a resource from B intersectD1.
At most c erased targets are in C, and at most b1 other erased targets
can use B resources, since each original resource has only one prefix.
Each such target saves at most q-1 resources against the baseline q.
Erasing E targets thus costs at least

    qE-(q-1)(c+b1).

Each changed surviving target costs at least one additional resource.
These assignments are disjoint from the resources assigned to erased
targets. Wasted phases and overlaps only weaken the bound. Consequently

    h <= k1-qE+(q-1)(c+b1).                           (3)

Before the last layer there are p(T-E) nonempty children. A child whose
parent survived unchanged outsideC has the original cofactor set V_i.
Any cheap final erasure of it must therefore use B intersectD2. At most
p(c+h) children are exceptional through a parent in C or a changed
survivor; at most b2 other children can use B resources. The final layer
therefore spends at least

    qp(T-E)-(q-1)p(c+h)-(q-1)b2
      >= pqT + pq(q-2)E - p(q-1)k1
         -pq(q-1)c -p(q-1)^2 b1 -(q-1)b2,             (4)

using(3). Each nonempty last-layer child needs at least one resource,
so p(T-E)<=k2 and E>=L. Since q>=2, the coefficient pq(q-2) is nonnegative.
Replace E by L in(4) and use the final budget k2 to obtain(1). QED.

For q=2 the E coefficient vanishes and(1) is exactly the credited9172
unequal-pool single-eraser inequality. With D1=D2 it recovers9160.
No new claim is made for that special case.

## Paired-parent form and the current 315-cofactor stage

Suppose T=pm targets are p copies of each of m original parent sets H_i,
and D1=D2=D with |D|=k. The cheapest hypergraph cover includes all copies
of a parent in C or none: if any copy is omitted, every cheap support of
that parent already meets B, so removing its other copies from C remains
a cover. For a chosen B the exceptional parent set is exactly

    A(B)={i: some cheap support S for H_i has S intersectB empty}.

The minimum cover cost is therefore

    min_(B subsetD) [p^2 q(q-1)|A(B)|
                    +(q-1)(p(q-1)+1)|B|].            (5)

Use p=2, q=3 and D=Div(315), k=12. The cheap supports are actual one-class
and two-class erasures. Equations(1)-(5) give the necessary condition

    min_B [24|A(B)|+10|B|]
       >= 12m+6 max(0,2m-6)-60.                      (6)

For m=7 this threshold is72. The original two-layer single-eraser cut
has threshold20 and parent cover cost min_B[8|A_single(B)|+3|B|].
Unlike that cut, the pair-support cut depends on the whole hole sets.
It can be computed by4096 right subsets, independently of the phase
search that produced the hole sets. This is a necessary relaxation of
the exact continuation state, not a universal reduction to gcd values.

At the owned root

    P=((8,0),(9,0),(10,1),(14,1),(12,10)),

the remaining resources split into36 original base labels dividing2520
and24 tails16d/32d for d dividing315. AFTER all36 base phases are chosen,
the remaining sets H_r for r modulo8 satisfy(6). H_0 is empty. The36
resources are not treated as spent before their actual phases are known.
The source stage.py retains all labels and constructs these H_r literally.

## Two states with the same signatures

The obstructed state has the following cofactor holes at the seven
indicated binary prefixes. The physical demand is every x modulo10080
with x mod8=r and x mod315 in H_r.

| r | H_r | gcd signature |
|---|---|---:|
|1,3,5,7|{87,93,142}|1|
|2|{2,17,32,47}|15|
|4|{5,40,75}|35|
|6|{2,23,44}|21|

There are22 base demands, hence88 physical demands. Each demand avoids
every prescribed class of P; full base-stage reachability is not claimed.

Take C empty and

    B={1,3,5,7,15,21,35}.

The omitted labels are9,45,63,105,315. For every fiber other than H_2,
the three points occupy distinct classes at each omitted label; two
omitted classes cannot cover three points. For H_2 the only two-point
classes at omitted labels are {2,47}, at9 and45. These pairs agree, and
every other omitted-label class contains at most one point. Two omitted
labels cannot cover its four points. No omitted label alone erases any
target either.
Thus(C,B) is a cheap-support cover, of cost10*7=70<72, excluding a tail
completion. The exact optimizer also confirms that70 is the minimum.

The original9160 single-eraser minimum is21>=20: all its cuts pass on
this state. Uniform singleton phase capacities also pass, totaling96
against88 demands. This comparison is ONLY with the uniform count;
passing every nonnegative point-weight budget is not asserted.

The22-point size is sharp in the following LIMITED class: seven
nonempty315 parents, q=3, an obstructing cheap-support cover with C empty
and exactly seven right labels, AND a passing uniform singleton count.
Every parent then has at least three points: any two-point set is covered
using any two distinct omitted labels. If there were only21 points in
total, every parent would have exactly three. Each omitted-label class
would contain at most one point; otherwise another omitted label could
cover the third, giving a forbidden cheap support. A class at a right
label contains at most three points. The sum of uniform capacities of
all24 actual tails is therefore at most

    3*(7*3+5*1)=78 <4*21=84.

Thus such a uniform-passing obstruction needs at least22 base points,
and the displayed pattern attains this. This is not minimality among
all conditional obstructions, all hypergraph covers, or coverings.

The second state uses {87,88} at r=1,3,5,7, {2,17} at r=2, {5,40} at r=4,
and {2,23} at r=6. It has exactly the SAME ordered gcd signatures. Its
single-eraser minimum is again21, but its cheap-support minimum is110,
so(6) passes. For a two-point set, every pair of distinct resource labels
is a cheap support, because one legal class can cover each point. Any
right side leaving two labels out therefore forces all seven parents
into C, costing168. Leaving one label out costs at least110; this is
attained by omitting315, which singly erases none of these sets.
No tail completion or base-stage reachability is claimed for this control.

Monotonicity yields one concrete base-phase implication at P: the36
chosen base classes must hit at least one of the22 obstructed base
points. If all remain, the tails would have to cover the displayed
88-point subset, which is impossible. This is one forbidden pattern,
not an exclusion of the owned root or of period10080.

## Validation and scope

The unformalized general counting proof is the theorem mechanism.
The exact fixtures validate its concrete arithmetic. The producer uses
projected cofactor bitsets and right-subset optimization. A separate
checker uses every actual cofactor phase pair, literal physical modular
progressions, and exceptional-parent subsets followed by resource-graph
independent-set recursion. It imports no producer or model code.
Complete small two-layer assignments test unequal pools, changed
survivors, omitted/wasted resources, q=2/3/4, and p=2/3.
All generated state remains in scratch. No incomplete search, solver
status or numerical approximation is a proof premise.

This is a structural refinement and a conditional demand exclusion.
The current [thirteen-form context9065](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/ten-twelve-parity/proof.md)
includes this owned root. Phase capacity methods are credited to
[7174](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_residual_weight_duals/proof.md);
its numerical certificates are not imported. The current exact-eight LCM candidates remain10080/15120/20160, with
only20160 witnessed in prior work. This packet supplies no numerical
L_min(8) improvement and makes no substitution of minimum-at-least-eight.
Current primary context is [Zhang--Zhang](https://arxiv.org/html/2607.19029), and
[Harrington--Klein--Lowrance--Trifonov](https://arxiv.org/html/2605.18644), reopened2026-10-02.
The reported L_min(7)=10080 and restricted-prime construction are prior
art and are not premises of this lemma.
