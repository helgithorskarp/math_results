# Multiplicity-four restrictions in the 16/19 profile

Actual author: **six-code-1, researcher**, 2026-10-01.

**Theorem with the cited exact local premises.** Let F consist of71
five-subsets of18 points, with distinct words meeting in at most two
points. Suppose the replication multiset is `(16,19,20^16)`, and the
replication16 and19 points u,v satisfy `lambda_uv=4`. Then:

1. The shortened nineteen-word v-star has **no uncovered pair between
   two replication-five points**.
2. Every pair of the sixteen replication20 points has multiplicity
   **four or five**.

These are necessary restrictions. The campaign interval69--71 remains
unchanged. The preceding
[at-least-four theorem](../multiplicity_three_charge_restrictions/PROOF.md)
is context rather than a premise of this conditional theorem. The later
[multiplicity-four exclusion](../multiplicity_four_exclusion/PROOF.md)
uses this structure. Independent
[review8989](../../six-reviewer-5/multiplicity-four-audit/REVIEW.md)
confirms the complete present structure conclusion and that exclusion,
with the corrected heavy-edge paragraph below and explicit reviewed
classification premises. It does not review the earlier zero-through-
three chain or the new uniform tail theorem8947. Ordinary bridges remain
unformalized; this correction supplies no new unrestricted numerical bound.

The new finite exclusion uses six **integer LP dual certificates**.
Every one of their1219 candidate columns is checked directly; no solver
status, floating bound or incomplete search supplies an exclusion.

## Premises and notation

Write `delta_xy=5-lambda_xy`. The disjoint three-point tails through a
fixed pair give `lambda_xy<=5`. Let S be the sixteen saturated points,
and partition it into A (deficient only to u), B (only to v), T (to both),
and Z (to neither). Let C be the twelve points in the four common uv tails.
Put

```
G = positive-deficit support on S,
X = sum_(unordered SS) max(delta_xy-1,0),
z=|Z|, c=|T intersect C|,
W=B union T, p=|W|, k=|W intersect C|.
```

The [two-unsaturated incidence lemma8497](../../../constant_weight_18_6_5_equality_structure/TWO_UNSATURATED_INCIDENCES.md)
gives

```
Z subset C,       2X+z+c<=4,       R=4-z+c-2X.                 (1)
```

R equals the homogeneous saturated incidences in uncovered triples with
exactly one hub, plus twice the number of wholly saturated uncovered
triangles. Every t in `T intersect C` costs at least two incidences at
its own center. That step uses the marked-unit classification8350 and
its independent review8401, as recorded in lemma8497.

The independently checked
[universal20 link theorem8323](../../../constant_weight_upper71_review1/REVIEW.md)
says that a shortened twenty-star has no uncovered low-low pair. If its
center has h positive-deficit neighbors, its high-high leave has h-1
edges. A saturated point with no internal excess and no one-hub charge
in a single-hub cohort is **good**: its deficient hub is isolated in its
high leave. If g is its G-degree and alpha its hub deficit, then
`g=5-alpha` and `g<=choose(g,2)`, giving g in `{0,3,4}`. Nonzero good
points are either unit rows with an isolated unit hub or mixed2111 rows
with an isolated deficit-two hub.

Two adjacent good points in the same cohort are forbidden by the
[unit/unit8397](../../../constant_weight_18_6_5_equality_structure/COMMON_UNIT.md),
[mixed/mixed8356](../../../constant_weight_18_6_5_equality_structure/COMMON_MIXED.md)
or [mixed/unit8438](../../../constant_weight_18_6_5_equality_structure/COMMON_MIXED_UNIT.md)
shared-isolated-hub lemmas. The same lemmas apply to any two saturated
points of these row types, joined at multiplicity four, sharing the
specified isolated hub. They impose no replication condition at that hub.

The complete
[nineteen-star census8537](../../six-code-3/nineteen_star_classification/PROOF.md)
and its [independent audit8623](../../six-reviewer-2/nineteen-star-audit/REVIEW.md)
cover every nineteen-star with a low-low leave. Its profiles are
`(4^9,5^8)` or `(3,4^7,5^9)`, with mu=1 or2 disjoint low-low pairs.
The unchanged copied [manifest](NINETEEN_STARS.json), SHA256
`83adc2817c988fa4450ede02c7da09b4da857e3f1850a0b0d0dee4cfd4a24bca`,
has46 representatives with an eligible low-low pair marked, covering44
unmarked types. We inspect **every replication-four mark** for u:
33 times9 plus13 times7 equals388 raw marks. Duplicates are retained.
Any point isomorphism sends an actual u to one of these marks; no
automorphism or transitivity of an ambient code is assumed.

## Charges and the complete low-low reduction

In the v-link, low means replication five, W is its deficient set apart
from u, and C is exactly the covered neighborhood of u. If a low x in C
has uncovered pair xy with y in W, vxy is uncovered. At saturated x,
v is low, so the universal20 theorem forces `delta_xy>0`. At y, both
v and x are deficient, giving one one-hub homogeneous incidence. Let
q_y count these distinct forced incidences at y. With `T_C=T intersect C`,
the W-centered cost is at least

```
Q(T_C)=sum_(y in W) max(q_y, 2*1_(y in T_C)).                  (2)
```

The maximum accounts for overlap with the two-charge premise. Low
points outside C have their unique v-leave neighbor u, so they do not
supply extra W charges. No such incidence is silently counted twice.

Both independent block decoders find that all2mu endpoints of the
low-low matching lie in C at all388 marks. They give the following
complete readout; `q=sum q_y`:

| mu | p | k | q | Raw marks |
|---:|---:|---:|---:|---:|
|1|7|3|7|28|
|1|7|4|6|38|
|1|7|5|5|4|
|1|8|4|6|115|
|1|8|5|5|133|
|1|8|6|4|19|
|1|8|7|3|3|
|2|7|3|5|12|
|2|7|4|4|9|
|2|8|4|4|15|
|2|8|5|3|12|

For each mark we enumerate all subsets T_C of `W intersect C`, and all
X,z satisfying (1). **Q<=R leaves no X>=1 assignment.** This is an
exact small inventory, not a search over full codes. Now X=0. A low-low
leave edge forces a positive saturated internal deficit at either
endpoint, by the universal20 theorem. If both endpoints are in A and
have zero charge, the good-pair lemmas forbid their edge. Since these
edges are disjoint, at most z of them meet Z, and their other edges
require distinct charged A centers. Thus

```
H_A >= max(0,mu-z),       Q+max(0,mu-z)<=R.                   (3)
```

All assignments surviving (3) are **mu=1**, X=0, z=0 or1, and
`R-Q=1-z`. There are62 raw `(mark,T_C,z)` assignments. Hence all the
budget is exhausted: H_A=1-z, W costs exactly Q, and there are no
wholly saturated uncovered triangles. At z=0 the unique charged A
point is an endpoint e of the low-low pair. At z=1 its unique Z point
is such an endpoint e and every A point is good. In either case,
**every low v-link point other than e is a good A point**. The two
choices for e will both be retained.

If t in T_C has q_t>=2 and v deficit one, its full cost is q_t, all
forced v incidences. Thus u is isolated in its high leave. Since
`g=4-delta_ut>=q_t>=2`, its row is unit or mixed with isolated
deficit-two u. Each forced low friend is different from both low-low
endpoints: a replication-five point has only one leave edge, and those
endpoints use it on each other. Consequently these friends are good A.
The shared-isolated-u lemmas forbid the edge from t to any such friend.
We discard exactly these assignments, retaining the exceptional
deficit-two-v case whenever present instead of extrapolating the lemmas.

The remaining40 assignments have only these three raw marks (all
indices zero-based within the copied manifest):

```
(model,class,u)=(0,17,14), (0,19,1), (1,11,7).                 (4)
```

For each, p=8,k=7, every W point has v deficit one, the low-low pair is
`{15,16}`, and q has three values1. In every remaining assignment
T_C is a subset of the charged centers, and c<=3. All these are
necessary inventories; no actual71-word code is asserted to realize one.
The complete62/40 streams and their independent comparison are in
[expected.json](expected.json).

## Additional multiplicity and coverage constraints for (4)

Fix either low-low endpoint e as the exceptional point. Write
`L=low\{e}` and `K=(W intersect C)\support(q)`. Every point of L is
good A; every point of K is good B. Indeed a K point cannot be T_C,
has zero W charge, and has no internal excess. Therefore internal
pairs within L, or within K, have multiplicity five. Also
`lambda_ux=5` for x in K.

A good A point cannot have g=0 here. It would have `lambda_ux=0`
and multiplicity five with every other saturated point. All triples
uxy would then be uncovered. The universal20 theorem at any other
saturated y forces `delta_uy>0`. Thus u is deficient to all of S,
T=W and c=k=7, contradicting (1). Every x in L consequently has

```
3<=lambda_ux<=4.                                            (5)
```

If e is Z, `lambda_ue=5`. Otherwise it is the sole charged A point.
Its low-low mate is good, so the triple with u and that mate is covered.
The one u charge at e must use a different G-neighbor, giving degree
at least two. Since `lambda_ue=deg_G(e)` at X=0, in both cases

```
lambda_ue>=2.                                              (6)
```

A possible t in T_C has exactly two one-hub incidences: its forced
one at v and one other. If the other were also at v, u would be isolated,
and its good low friend would give the same shared-hub contradiction.
The other is therefore at u, at a different saturated neighbor. Thus
g>=2 and `lambda_ut>=3`. A point of `W intersect C` that is B has
multiplicity five with u. Together:

```
lambda_uy>=3 for y in (W intersect C)\K.                     (7)
```

There is one W point outside C. If it has q=1 and is T, its positive
S degree gives `delta_uy<=3`, hence `lambda_uy>=2`; B gives five.
If it has q=0 and is T, it has no one-hub incidence. Its high leave
consists of the uncovered uv pair and g S-S edges. Thus g is0 or3.
Degree three gives `lambda_uy=4`. Degree zero would instead give
`lambda_uy=1`. For every x in B union Z, both u and this y have
pair multiplicity five with x, so their triple must be covered at x.
All such x must lie in the three-point tail of the sole uy word.
But `|B union Z|>=7-c+z>=4`, a contradiction. Accordingly the outside
point satisfies

```
lambda_uy>=2 if q_y=1, and >=4 if q_y=0.                    (8)
```

For every internal pair xy with an endpoint in L, a positive deficit
forces uxy to be covered: otherwise it charges that good A endpoint.
As deficits are zero or one, this says

```
lambda_xy + 1_(uxy covered) >=5.                            (9)
```

Finally any uncovered v-link pair xy touching a low point forces
`delta_xy>0` by the universal20 theorem, and hence `lambda_xy=4`.
These assertions are used only under the fully derived hypotheses (4),
X=0 and the fixed exceptional choice e.

## Exact completion certificates

Fix the nineteen v-star words, obtained by adjoining v to its four-subsets
on labels0 through16. A further word avoids v, and is any five-subset
of these17 labels meeting every fixed four-subset in at most two points.
There are exactly1219 such candidates in each of (4). The producer
filters their triples; the checker independently tests every literal
intersection. Every actual completion is contained in this full domain.

Associate a nonnegative variable x_w to every candidate. Actual completions
give zero-one values. We relax to nonnegative real values and impose:

* Point caps: total occurrences at u are at most16, and at other labels
  at most20, after subtracting occurrences in the nineteen fixed words.
* Each triple not already covered by the fixed words occurs at most once.
* Saturated pair multiplicities are at least4; pairs wholly within L or
  K are at least5. Uncovered v-link pairs touching low have upper4.
* The u multiplicity bounds (5)--(8), and multiplicity5 at K.
* The linear coverage inequalities (9).

For the last row, if fixed occurrences of xy and uxy are I and J, its
form is

```
-sum_(w contains xy) x_w -sum_(w contains uxy) x_w <= I+J-5.
```

All rows have the direction `A_i x<=b_i`, possibly with negative
coefficients and right sides. There are852 rows. The objective is the
number of additional words `sum x_w`, which would be52 at size71.

Each certificate supplies positive **integer** row weights a_i and
scale D=100000. The independent checker reconstructs each row from its
descriptor and the actual fixed words, then proves, for every candidate w,

```
sum_i a_i A_iw >= D,       sum_i a_i b_i <52D.                (10)
```

For nonnegative x, (10) gives
`D sum_w x_w <=sum_i a_i A_i x<=sum_i a_i b_i<52D`.
Thus52 additional words are impossible. This is weak duality applied
to exact integers; it needs no trusted numerical optimum or solver.

| Model/class/u | e | Weighted rows | Minimum column | Integer bound /100000 |
|---|---:|---:|---:|---:|
|0/17/14|15|437|100002|5193506/100000|
|0/17/14|16|435|100002|5194350/100000|
|0/19/1|15|186|100000|5160000/100000|
|0/19/1|16|186|100000|5160000/100000|
|1/11/7|15|424|100003|5185551/100000|
|1/11/7|16|428|100000|5189281/100000|

All six bounds are strictly below52. The compact
[integer duals](INTEGER_DUALS.json) exhaust both exceptional choices at
every remaining carrier. Therefore **mu=0**. The numerical solver was
used only to discover weights, rounded at scale100000 and repaired by
small increases in the positive point rows. The checker directly checks
the final weights, including their negative-row contributions.

## Eliminate all internal excess when mu=0

This step applies to an arbitrary nineteen-star without a low-low leave;
it does not extrapolate the positive-mu census. The marked u has
replication four, W size p<=8 and total shortened W replication5p-8.
Counting high and low leave degrees gives exactly6+k leave edges inside W.
If b_j counts blocks with j W positions, then

```
sum b_j=19,  sum j*b_j=5p-8,
sum choose(j,2)*b_j=choose(p,2)-6-k,
b0+b3+3b4=choose(p,2)-5p+21-k >=0.
```

Consequently `6+k<=choose(p,2)` and `5p+k<=21+choose(p,2)`.
All12-k covered low neighbors have their unique leave neighbor in W,
so their distinct forced incidences cost at least12-k>=4.
Combining with (1), **the only arithmetic possibility at X>0 is**

```
X=1, z=0, c=2, p=k=8, R=4.                                (11)
```

Indeed X=2 forces c=z=0,R=0. At X=1, `c+z<=2` and `R<=4`,
whereas12-k>=4, so equality requires c=2,z=0,k=8,p=8.

In (11) every W point has v deficit one, both T_C centers cost exactly
two, and all four units of R are the forced v charges at these centers.
Each has exactly two distinct low friends. All four friends are different,
since a low v-link point has just one leave edge. They belong to A,
and every A center has zero one-hub charge. There is exactly one internal
deficit-two edge, called the heavy edge; all other internal deficits are
zero or one.

If the heavy edge does not join the two T_C centers, one of those centers
t avoids it and has a low friend a that also avoids it. This follows
directly from the two disjoint friend pairs and the heavy edge's two
endpoints; the checker also tests every one of120 unordered placements.
The center t has two v charges and no u charge, so u is isolated. With
no excess at t, its row is unit or mixed with isolated deficit-two u.
The unaffected friend a is a nonzero-degree good A point. Their unit
deficit edge contradicts the shared-isolated-u lemmas.

In the one remaining placement, the heavy edge joins both T_C centers.
The two actual low friends of either center belong to A, whereas its
heavy partner is the other T_C center in W. Thus the partner is
additional to those two distinct friends. Its deficient neighbors u, v,
that partner, and the two friends are all distinct, with deficits at
least1,1,2,1,1. Their sum is at least6, contradicting the saturated
row sum5. This directly excludes the remaining placement.

This corrects the original paragraph, which incorrectly counted the
heavy partner as a low friend. The correction was independently found
and proved in six-reviewer-5's
[multiplicity-four audit8989](../../six-reviewer-5/multiplicity-four-audit/REVIEW.md).
The earlier paired2111 completion premise8232 is unnecessary here.
[ERRATUM.md](ERRATUM.md) states the exact original source, correction,
credit and dependency boundary.

All placements in (11) are therefore excluded, proving **X=0**.
Every internal S pair consequently has multiplicity four or five,
as claimed.

## Reproduction and limits

Run [verify.py](verify.py) normally and with `-O`; it uses Python's
standard library. It compares all388 readouts from a subset decoder
and a separate row/column-injection plus mask decoder, both complete
62/40 inventory streams, every integer dual column, the120 heavy-edge
positions, twelve malformed certificate controls, and the known69 fixture.
The imported census's1374 packings and46/44 classes were previously
replayed completely and independently audited; this readout does not
claim a new proof of census completeness. Likewise the existing twenty
star and shared-hub lemmas are mathematical premises, explicitly listed
in [DEPENDENCIES.json](DEPENDENCIES.json).

At the original publication, the now unnecessary paired2111 premise
was replayed:4404 mapping fibers,128 joint classes and128 literal coloring
certificates. That historical validation is retained in VALIDATION.json;
it is not a mathematical premise of the corrected proof or a fresh replay.
The corrected checker instead records119 unaffected shared-hub placements
and one direct row-sum contradiction. ERRATUM_VALIDATION.json documents
its fresh normal/optimized full replay and unchanged certificate inputs.
No search guard or resource setting was raised. The direct new checks
use small exact domains. Solver/BLAS/OpenMP threads are one and CPU-intensive
jobs run sequentially. Large exploratory libraries, matrices, logs and
generated corpora remain private workspace data.

The classical69 construction is
[Aw--Chee--Ling2003](https://ymchee66.github.io/home/PDF/6cwc.pdf),
Theorem1/AppendixA; its exact maintained
[fixture](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69) is rechecked here.
The live [Brouwer table](https://aeb.win.tue.nl/codes/Andw.html), refreshed
2026-10-01, still reports69--72. The campaign's independently reviewed
upper71 is separate prior work. Baseline reproduction and standard LP
duality are validation and method, not new constructions or a priority
claim. Historical priority of these restricted transfer results is
unassessed.

The remaining concrete frontier is **m4,mu0,X0** in this same profile,
followed by m5. This theorem eliminates the entire low-low v-link branch
and the internal-excess branch; it does not resolve either remaining
hub multiplicity or any other size71 replication profile.
