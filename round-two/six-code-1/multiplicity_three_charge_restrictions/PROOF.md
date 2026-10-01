# The multiplicity-three boundary in the 16/19 profile

Actual author: **six-code-1, researcher**, 2026-10-01.

Let F consist of71 five-subsets of18 points, with distinct words meeting
in at most two points. Assume its point-replication multiset is
`(16,19,20^16)`. Mark its replication16 and19 points u,v, and suppose
`lambda_uv=3`. Write `delta_xy=5-lambda_xy`, and let S be the sixteen
replication20 points. Deficits are nonnegative: the three-point tails
of words through a fixed pair are disjoint, proving `lambda_xy<=5`.

Partition S into A (deficient only to u), B (only to v), T (to both),
and Z (to neither). The three words through uv have disjoint tails;
let C be their nine-point union. Put

```
G = positive-deficit support on S,
X = sum_(unordered SS) max(delta_xy-1,0),
z = |Z|,   b = |T|,   c = |T intersect C|,
W = B union T,   p = |W|,   k = |W intersect C|.
```

Let mu be the number of uncovered pairs between replication-five
points in the shortened nineteen-word v-star. Equivalently these are
uncovered triples vxy with `lambda_vx=lambda_vy=5`.

**Necessary structural theorem, with the explicit computational inputs
below.** Under these hypotheses:

1. **X=0 and mu=0.** Every saturated internal deficit is zero or one.
2. **p=7.** Each point of W has `lambda_vx=4`; the other nine S points
   have `lambda_vx=5`. The v-star profile is `(3,4^7,5^9)`.
3. The necessary inventories `(k,c,z)` are exactly among

   ```
   (6,1,0), (6,1,1),
   (5,2,0), (5,2,1), (6,2,0), (6,2,1).
   ```

   This list asserts coverage, not realizability. In particular
   `1<=c<=2` and `z<=1`.
4. Let H_A count homogeneous saturated incidences at A centers in
   uncovered triples with exactly one hub. Then **H_A<=1-z**.
   If z=1, A is independent in G. If z=0, every internal A edge
   meets the same possible exceptional vertex; there is at most
   one such vertex and its G-degree is at most four.

This sharpens the preceding
[multiplicity-three alternative](../two_unsaturated_pair_at_least_three/MULTIPLICITY_THREE.md).
It does not exclude multiplicity three or any remaining size71 profile.
The campaign interval remains **69 <= A(18,6,5) <=71**. Independent
review of this transfer is pending; ordinary bridges are unformalized.

## Imported premises and exact coverage

The reviewed universal20 link theorem gives no uncovered pair between
replication-five points in **any** twenty-quadruple pair packing on17
points. Its ordinary degree consequence is that a saturated center
with h positive-deficit neighbors has exactly h-1 high-high leave
edges. Source: [review8323](../../../constant_weight_upper71_review1/REVIEW.md),
`bafkreibz6cr3e3mjpadu4jjr5n3kzwlji4ijgzbto7mw66xoqtyaa37ohe`.

The published
[two-unsaturated incidence lemma8497](../../../constant_weight_18_6_5_equality_structure/TWO_UNSATURATED_INCIDENCES.md),
`bafkreihndic4hlvy3isb4czkaiezhhrrxazlrwikjcstfhm77nwvpzuulm`, gives

```
Z subset C,      2X+z+c <=3,      b-z+4c+X <=13,                 (1)
R=3-z+c-2X.                                                  (2)
```

R is exactly twice the number of wholly saturated uncovered triangles
in G, plus the homogeneous saturated incidences in uncovered triples
containing exactly one hub. It is nonnegative, and each t in T intersect C
contributes at least two such one-hub incidences **at center t**.
That two-charge premise uses the independently checked marked-unit
classification8350/review8401. Incidences are counted by center even
when two centers belong to the same triple.

The same incidence lemma's good-vertex argument uses the three
published shared-isolated-hub obstructions: [unit/unit8397](../../../constant_weight_18_6_5_equality_structure/COMMON_UNIT.md),
[mixed/mixed8356](../../../constant_weight_18_6_5_equality_structure/COMMON_MIXED.md),
and [mixed/unit8438](../../../constant_weight_18_6_5_equality_structure/COMMON_MIXED_UNIT.md).
Their hypotheses concern two replication20 centers joined at pair
multiplicity four and sharing an isolated deficient hub; they impose
no replication condition at that hub. These premises are used again below.

Finally, six-code-3's complete
[nineteen-star classification8537](../../six-code-3/nineteen_star_classification/PROOF.md),
`bafkreigcg7dkxtl5ady54clyawxu2bpctj7qqyow5qx2fycla2qm4aiml4`,
classifies every nineteen-quadruple pair packing with mu>0. If a point
has replication three, its profile is `(3,4^7,5^9)`. The replication-three
point is unique, so every point isomorphism preserves its mark. The
complete relevant carrier consists of ten marked classes at mu=1
and three at mu=2. Marking an eligible low-low pair can duplicate an
unmarked class; retaining all thirteen preserves coverage.

The copied [NINETEEN_STARS.json](NINETEEN_STARS.json) is the unchanged
published manifest, SHA256
`83adc2817c988fa4450ede02c7da09b4da857e3f1850a0b0d0dee4cfd4a24bca`,
source commit `4c6b7abd85932d7c113c50843cbe11e49915e673`.
Its completeness is an imported theorem, not established by our readout.
Its original four entry points were completely replayed in the preceding
pass, recovering1374 packings,46 marked and44 unmarked classes.
There was no new relevant source change at this pass's refresh.

## The covered-low-point charge

In the v-link, C is exactly the covered neighborhood of u. Its replication
is three. Its other deficient points are W; its replication-five points
are A union Z. If an uncovered pair xy has x in `C intersect (A union Z)`
and y in W, the actual triple vxy is uncovered. At saturated center x,
v has link replication five. The universal20 theorem therefore forces
`delta_xy>0`; otherwise v,y would be a forbidden low-low leave pair.
At saturated center y both v and x are deficient, so vxy contributes
one homogeneous one-hub incidence to R. Different x give distinct
triples. Let q_y count those forced incidences at y.

For any proposed set `T_C=T intersect C`, the charge at W centers is
at least

```
Q(T_C) = sum_(y in W) max(q_y, 2*1_(y in T_C)).                (3)
```

Using a maximum accounts correctly for possible overlap between the
covered-low charge and the two-charge premise. We do not add overlapping
incidences as if they were distinct.

## Exclude every nineteen-star low-low leave

Assume mu>0. Apply classification8537 with the unique replication-three
point marked u. For every one of the thirteen representatives, the2mu
endpoints of its low-low matching belong to C. Direct block decoding gives:

| mu | k | Marked classes | sum q_y | Positive q_y values |
|---:|---:|---:|---:|---|
|1|1|2|6|`1,1,1,1,2` or `2,2,2`|
|1|2|2|5|`1,1,1,1,1`|
|1|3|6|4|`1,1,1,1`|
|2|2|3|3|`1,1,1`; all charged centers outside C|

The readout is invariant under actual point relabeling. The checker
rebuilds both anchor models and every candidate in two representations,
then compares the actual blocks, replications, uncovered pairs and each
q_y entry. It decodes all46 marked representatives, not just their counts.

From (1), X<=1. Also c<=2: c=3 would force X=z=0 and b>=3,
contradicting `b+12<=13`. For mu=1, the table and (3) give minimum Q
values4,5,6 for c=0,1,2, respectively. Each exceeds
`R<=3-z+c`. Thus mu=1 is impossible.

For mu=2 all three forced charged centers are outside C, so
`Q=3+2c`. If c>0, this exceeds R. If c=0, comparison with (2) forces
`X=z=0,R=3`. All three units of R occur at W centers. There is no
one-hub charge at an A center. Since z=0, both endpoints of each of the
two low-low leave pairs are in A. The universal20 theorem at either
endpoint forces their mutual S deficit to be positive. X=0 makes it one.

At any A center with no one-hub charge, u is isolated in the high leave.
If its G-degree is g and hub deficit is alpha, then `g=5-alpha` and
the high leave has g edges on the g saturated neighbors. Hence
`g<=choose(g,2)` and `g in {0,3,4}`. A degree3 center is a mixed2111
star with isolated deficit-two hub; degree4 is a unit star with isolated
unit hub. Adjacent nonzero-degree A centers contradict the applicable
shared-isolated-hub obstruction. The forced low-low leave edge is such
an adjacency. This excludes the three last carrier cases. Therefore

```
mu=0.                                                        (4)
```

## Exclude internal excess and restrict the cohort inventory

The v-S deficit weight is7, so p<=7. For an arbitrary nineteen-star
with marked replication-three u, its total positive deficit is9.
When mu=0, counting the leave inside W gives6+k edges. If b_j counts
blocks with j points of W, then

```
sum b_j=19,     sum j*b_j=5p-7,
sum choose(j,2)*b_j=choose(p,2)-6-k.
```

The nonnegative sum `b0+b3+3b4` consequently gives

```
6+k <=choose(p,2),      5p+k <=20+choose(p,2).                  (5)
```

For integers `0<=p<=7`, (5) gives k<=6. Each of the9-k covered
replication-five neighbors of u now has its unique leave neighbor in W,
so the covered-low-point argument gives at least9-k>=3 charges.
If X=1, (1) gives `z+c<=1` and thus `R=1-z+c<=2`, a contradiction.
Therefore **X=0**, `|E(G)|=27`, and `R=3-z+c`.

In this branch put

```
Q_W=max(9-k,2c),       h=R-Q_W >=0,
a=|A|=16-p-z,         D=sum_(x in A) deg_G(x).
```

All W-centered one-hub charges are distinct in center from those in A.
Thus H_A<=h. As in the preceding good-vertex argument, two A centers
with zero charge cannot be adjacent. Every internal A edge meets a
charged vertex. Such a vertex has degree at most four and costs at least
one unit of H_A. Hence

```
I_A=|E(G[A])| <=4H_A <=4h,
D <=27+I_A <=27+4h.                                          (6)
```

The u-S weight is19. Its weight on T, denoted w, is at least b>=c.
Its weight on A is19-w, giving

```
D=5a-19+w >=5a-19+c.                                        (7)
```

If h=0, every A center is good and A is independent. Its high-leave
edges supply D actual uncovered triples with one center in A and
two points in the other `p+z` saturated positions. No such triple has
two A points. A pair yz has at most `1+3delta_yz` uncovered completing
points, since its covered tails use3lambda_yz of the other16 points.
Independence leaves exactly27-D edges of G on those other positions.
Counting by the outside pair gives

```
D <= choose(p+z,2)+3*(27-D),
4D <= choose(p+z,2)+81.                                     (8)
```

The tiny integer inventory `0<=p<=7,0<=k<=p,0<=c<=k,0<=z<=3`
subject to (1) with b>=c, (5), `9-k<=R`, and (6)--(8) is exhaustively
checked using exact integers. The only surviving `(p,k,c,z)` are

```
(7,6,1,0), (7,6,1,1),
(7,5,2,0), (7,5,2,1), (7,6,2,0), (7,6,2,1).
```

Every excluded row and its specific degree or capacity contradiction
is listed in [expected.json](expected.json). This arithmetic enumeration
covers necessary parameters, not codes or nineteen-stars. As examples,
`(p,k,c,z)=(6,5,2,0)` has h=1, so (6) gives D<=31 but (7) gives
D>=33. The zero-overlap boundary `(7,6,0,0)` has h=0 and D>=26,
whereas (8) gives4D<=102, contradicting104<=4D.

The six survivors give p=7, forcing all seven v-S deficits to be one.
They also give h=1-z, proving the asserted H_A bound and exceptional-
vertex description. This completes the conditional structural theorem.

## Evidence and limits

The reproducible commands and exact inputs are in [README.md](README.md)
and [DEPENDENCIES.json](DEPENDENCIES.json). Normal and optimized Python
checkers must agree with every entry of expected.json. Their representative
decoders use different candidate generation and literal pair sets versus
pair-owner arrays. Sixteen malformed packing controls are rejected.
The Aw--Chee--Ling69 baseline is exactly rechecked; it supplies validation,
not novelty. Imported local classifications and the written saturation,
isolation, center-charge and capacity bridges remain proof premises.
Their agreement is not independent peer review or formal verification.

The maintained [primary table](https://aeb.win.tue.nl/codes/Andw.html),
refreshed live2026-10-01, still gives69--72. The historical lower bound
is [Aw--Chee--Ling2003, Theorem1 and AppendixA](https://ymchee66.github.io/home/PDF/6cwc.pdf).
The campaign's independently reviewed [upper71](../../../constant_weight_18_6_5_equality_structure/UPPER71.md)
is prior art, not a new outcome here. Historical priority of this
restricted transfer has not been assessed against the full literature.
Every checker operation is exact integer or set arithmetic; no solver,
timeout, UNKNOWN or incomplete enumeration supplies an exclusion.
