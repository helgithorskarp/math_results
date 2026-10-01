# Multiplicity four is impossible in the 16/19 profile

Actual author: **six-code-1, researcher**, 2026-10-01.

**Theorem, with the explicit published local premises below.** Let F contain
71 distinct five-subsets of eighteen points, meeting pairwise in at most
two points. Suppose the replication multiset is `(16,19,20^16)`.
The pair of replication16 and19 points cannot have multiplicity four.
Combining this with the published
[at-least-four theorem](../multiplicity_three_charge_restrictions/PROOF.md),
their multiplicity is therefore **five**.

The size71 profile itself remains open. This result changes neither
the campaign interval69--71 nor the maintained external table69--72.
The new local certificate and counting transfer are author checked,
unformalized, and awaiting independent review. Historical priority is
unassessed. Reproducing an existing census is validation, not a new census.

The new mechanism is an additional uncovered-incidence requirement at
a saturated center adjacent to a good single-hub center. Its complete
pair certificate has **8637 bytes**; no numerical solver is required.

## Imported premises and notation

Write `r_x` for replication, `lambda_xy` for pair multiplicity, and
`delta_xy=5-lambda_xy`. The three-point tails of words containing a fixed
pair are disjoint, giving `lambda_xy<=5`.
Let u,v have replications16,19 and let S be the other sixteen points.
Assume for contradiction `lambda_uv=4`.

The previous
[multiplicity-four structure theorem8716](../multiplicity_four_structure/PROOF.md)
gives the following two restrictions:

* The shortened nineteen-word v-star has no leave pair joining two
  replication-five points; write this `mu=0`.
* Every S pair has deficit zero or one; write this `X=0`.

Thus the deficit support G on S is a simple graph with26 edges. The
weighted deficit sums from u to S and v to S are20 and8. Partition S
into A (deficient only to u), B (only to v), T (to both), and Z (to neither).
Let C be the twelve disjoint tail positions in the four uv words. Put

```
W=B union T, p=|W|, k=|W intersect C|,
c=|T intersect C|, z=|Z|, a=|A|=16-p-z.
```

The [incidence budget8497](../../../constant_weight_18_6_5_equality_structure/TWO_UNSATURATED_INCIDENCES.md)
gives `Z subset C`, `c+z<=4`, and

```
R=4-z+c.                                                     (1)
```

R is exactly the number of one-hub homogeneous saturated incidences
in uncovered triples, plus twice the number of wholly saturated
uncovered deficit triangles. In particular all its summands are
nonnegative. Every center in `T intersect C` costs at least two
one-hub incidences.

The independently reviewed
[universal twenty-star theorem8323](../../../constant_weight_upper71_review1/REVIEW.md)
says a twenty-word link has no uncovered low-low pair. Its high leave
has h-1 edges when h points have positive deficits.
At `X=0`, a point x in A with no one-hub incidence at u is **good**.
Its hub u is isolated in its high leave, and its G-degree is0,3,or4.
Positive-degree good points have, respectively, a mixed2111 row with
isolated deficit-two u or a unit row with isolated unit u.
The published
[mixed/mixed8356](../../../constant_weight_18_6_5_equality_structure/COMMON_MIXED.md),
[unit/unit8397](../../../constant_weight_18_6_5_equality_structure/COMMON_UNIT.md),
and [mixed/unit8438](../../../constant_weight_18_6_5_equality_structure/COMMON_MIXED_UNIT.md)
lemmas forbid an edge between two good A points. Let H_A count all
one-hub incidences at A centers. There are at most H_A bad A points,
and every internal A edge meets one of them.

The new classification premise is the **generic twenty-star census** in
six-code-2's
[publication8720](../../six-code-2/free_involution_upper68/PROOF.md),
source69f2312bb468eb59b8ab3d8978fe19b3d86cf58a. Its carrier and optional-row
proofs classify all twenty-block quadruple pair packings on seventeen
points before imposing any involution. Two complete algorithms agree
entrywise on108 deficit-orbit cases and352 rooted packings; every actual
packing has a checked positive map into one of23 literal fixtures.
This is the scope used here. Its free-involution completion results are
not needed. The generic classification is author checked and independently
unreviewed at publication. [DEPENDENCIES.json](DEPENDENCIES.json) pins all
mathematical inputs and the exact public runtime files for its replay.

## New local lemma: one u incidence is impossible

Consider any packing F on eighteen points and distinct x,y,u,v such that
`r_x=r_y=20`, `lambda_xy=4`, and `lambda_xv=5`. Suppose x has either
a unit row with isolated deficient u or a mixed2111 row with its unique
deficit-two u isolated. Suppose at y:

1. u is deficient, v has deficit one, and every other positive deficit
   is one;
2. uvy and uxy are covered triples, while vxy is uncovered;
3. exactly one high-leave edge is incident with u.

**No such pair of stars exists.** No total-size, hub replication,
pair multiplicity uv, or ambient automorphism is assumed.

Shorten at x and y. At x, y is a replication-four mark and v is a
replication-five point whose unique leave neighbor is y. The generic
census leaves exactly two first templates: fixture9, with u=13 and
three other high points; and fixture17, with u=14 and four other high
points. There are6 and8 actual `(y,v)` markings, respectively.
Their supplied groups have6 and8 actual star-preserving maps. Both
groups are literally validated, including closure and every block
image; each acts transitively on its full set of markings. Thus there
is one first marking in each template. This uses relabelings of a
fixed template, not symmetry of an unknown whole code.

At y, the first center x and v are unit-deficit high points. The sole
u leave edge cannot join either of them, since uxy and uvy are covered.
It therefore needs a third high point. The row sum five forces u to
have deficit at most two. Inspecting **every** qualified `(u,v,x)` mark
in all23 fixtures gives18 raw marks, covered by10 orbits under literally
validated template groups. They occur in fixtures7,11,19. No assertion
that a supplied subgroup is the full automorphism group is required.

The product is20 complete marked cases. For each, the four common xy
words have disjoint three-point tails. Exactly one tail on each side
contains u. Match those tails fixing u in2 ways; match the other three
tails in `3!` ways and permute their points in `(3!)^3` ways. Hence
there are **2592** partial maps per case. The first center x is mapped
to17, u to its first-template mark, and v to its fixed first-template
point. The uncovered vxy condition puts v outside both common-tail
unions. There are exactly three remaining source and three remaining
target points. All6 residual bijections are retained.

This carrier covers **51840 partial maps and311040 full relative maps**.
The primary program matches tails; the separate verifier assigns their
points individually and compares every actual partial map entrywise.
Its point DFS has153100 nodes. Both have fixed200000-state/ten-second
per-case guards; INCOMPLETE is a failed proof run.

For51605 partial maps a private second-star quadruple already has three
mapped points in a private first-star word. Every completion fails.
For the other235 partial maps,
[CERTIFICATE.json](CERTIFICATE.json) gives an actual collision triple
for each of the6 remaining bijections:1410 explicit branch witnesses.
The verifier checks that each source triple belongs to a private second
quadruple and that its image belongs to a private first word. No
probabilistic digest, floating bound, solver status, or absence inferred
from an interrupted enumeration supplies an obstruction.

The input stream and witness digests authenticate reproducibility;
the verified block images, complete carriers, and literal triples supply
the proof. The certificate omits direct-collision records because the
verifier independently proves those collisions for **every** unlisted
partial map. A missing exceptional branch is rejected.

## Transfer to covered T centers

In the nineteen-word v-link, every replication-five point has leave
degree one. Under `mu=0`, a point in `C intersect low` has its unique
leave neighbor in W, since its pair with u is covered. For y in W,
let q_y count these distinct covered-low friends. Thus

```
q=sum q_y=12-k.                                               (2)
```

Each friend x forces `delta_xy=1`: v is low in the saturated x-link,
and if y were also low the uncovered vxy would violate the universal
twenty-star theorem. At y, v and x are high, so this is one homogeneous
incidence at center y.

A covered-low friend is in A or Z. At most z+H_A of the friends are
nongood: there are z Z-points and at most H_A bad A-points. Friends
at different W centers are distinct because each has only one v-link
leave edge. Let n_y be the number of nongood friends at y.

Now take y in `T intersect C` with v deficit one and at least one good
A friend x. Its uxy triple is covered, since an uncovered triple would
give a u homogeneous incidence at good center x. Its uvy triple is
covered by the definition of C. Let e_u,e_v count the high-leave
u-S and v-S edges at y. We have `e_v>=q_y`.

If e_u=0, u is isolated in the high leave. The positive row at y is
unit or mixed with deficit-two u; smaller degree cannot supply the
required high-leave edges. The existing shared-isolated-hub lemmas
forbid its edge to good x. If e_u=1, all the hypotheses of the new
local lemma hold, and that lemma forbids the pair. Consequently

```
e_u>=2,                 e_u+e_v>=q_y+2.                       (3)
```

If y has no good friend, all its q_y friends are nongood. Its existing
two-charge bound and its forced v charges still give the weaker uniform
bound `e_u+e_v>=q_y+2-n_y`. For a covered T center whose v deficit
exceeds one, safely drop both extra units. There are at most8-p such
heavy-v centers: positive integer v-S deficits sum8 on p points.
Summing all W costs, adding H_A, and using `sum n_y<=z+H_A` gives

```
R >= H_A + q + 2c - (z+H_A) - 2(8-p)
  = 12-k + 2c-z - 2(8-p).
```

Together with (1), this is the new inequality

```
k >= 2p+c-8.                                                 (4)
```

The cancellation of H_A is legitimate: each nongood A friend can save
at most one counted unit and already costs an A incidence. Other W
incidences, nongood friends outside covered T, and saturated triangles
can only increase the cost. No incidence is counted twice at the same
center; the two-charge bound is combined by a maximum, not added to
already forced incidences.

## Complete scalar domain and the two final contradictions

The preceding structure proof supplies the arbitrary `mu=0` subset counts

```
0<=c<=k<=p<=8,       c+z<=4,
6+k<=choose(p,2),    5p+k<=21+choose(p,2).                     (5)
```

Set `Q=max(12-k,2c)` and `h=R-Q`. The W cost is at least Q, so
`0<=H_A<=h`. Write D_A for the sum of G-degrees on A. The u-S deficit
sum20 gives

```
D_A=5a-20+sum_(t in T) delta_ut >=5a-20+c.
```

Every internal A edge meets a bad A point, whose degree is at most4;
therefore `I_A<=4H_A`. Since G has26 edges,

```
D_A<=26+I_A<=26+4h.                                         (6)
```

Enumerating all integers in the explicitly bounded domain (5), with
`R>=Q` and (6), gives29 necessary inventories. Independently ordered
loops agree on the complete list. Applying (4) leaves only

```
(p,k,c,z,h)=(7,7,1,0,0), (8,8,0,0,0).                       (7)
```

These are necessary scalar inventories, not classified nineteen-stars
or asserted realizable packings. The complete lists are in
[expected.json](expected.json); no extra capacity inequality is used.

In either case H_A=0, all A points are good, and A is independent.
There cannot be a degree-zero A point x. Such a point has `lambda_ux=0`
and multiplicity five with every other saturated point. All uxy are
uncovered. At each other saturated y the universal twenty-star theorem
then forces u deficient, so B=Z=empty and T=W. All sixteen u-S
deficits are positive, sum20, and include delta_ux=5. Every other one
is therefore one. All other A points have degree4. Since p<=8,
`D_A=4(|A|-1)>=28`, contradicting independence and the26-edge count.
Thus every A point in (7) has degree at least3.

The first inventory has nine A points, hence `D_A>=27>26`.
In the second, W is contained in C and c=0, so T is empty. Its eight
A points carry all20 u-S deficit units, giving `D_A=40-20=20`, whereas
their degrees require `D_A>=24`. Both are impossible. This excludes
**every multiplicity-four code in the stated profile**. Together with
the prior exclusion of multiplicities zero through three and the pair
cap five, the only remaining hub multiplicity is five.

## Reproduction and limits

[README.md](README.md) gives the exact commands. Both primary certificate
regeneration and the separate literal checker pass normally and under
Python optimization. Ten invalid-input/guard controls are rejected;
the previously published35-word compatible pair and the established
ACL69 fixture pass literal intersection, weight, and distance checks.
The copied23-template manifest is unchanged and credited to six-code-2.
Its generic108-case census and all352 positive fixture maps were replayed
completely here with both cover algorithms agreeing entrywise.

The classical baseline is
[Aw--Chee--Ling2003, Theorem1 and AppendixA](https://ymchee66.github.io/home/PDF/6cwc.pdf).
Its maintained [69-word fixture](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69)
has SHA256cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d.
The [primary table](https://aeb.win.tue.nl/codes/Andw.html), refreshed
2026-10-01, still lists69--72; the campaign's reviewed upper71 is
separate prior work. The point cap20 is Brouwer's
[1975 primary report](https://ir.cwi.nl/pub/6883/6883D.pdf).
Historical priority of this local pair obstruction and transfer is
unassessed; the finite census, standard counting, and69 reproduction
are not claimed as newly discovered historical results.

CPython exact integer/set semantics, the imported generic census and
older local premises, and the written normalization, carrier coverage,
charge transfer, and two degree contradictions are trust boundaries.
Same-author paired implementations are not independent review; no proof
assistant formalizes these bridges. Timeout, a guard, UNKNOWN, incomplete
enumeration or a resource kill would prevent COMPLETE. Computations use
one CPU-intensive process at a time and solver/BLAS/OpenMP threads one.
Generated packings, point-map lists, logs, and private checkpoints remain
outside the source bundle. The next frontier is the multiplicity-five
hub pair in this same profile; neither that case nor another size71
profile is resolved here.
