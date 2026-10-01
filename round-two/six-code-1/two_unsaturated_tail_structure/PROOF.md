# Tail structure when exactly two points are unsaturated at size71

Actual author: **six-code-1, researcher**, 2026-10-01.

**Theorem, with the explicit published local premises below.** Let F be
71 distinct five-subsets of an eighteen-point set, with any two members
meeting in at most two points. Suppose exactly two points u,v have
replication below20 and the other sixteen points S have replication20.
Write `m=lambda_uv` and let C be the union of the disjoint three-point
tails in the m words containing uv. For `delta_xy=5-lambda_xy`, partition
S into A (deficient only to u), B (only to v), T (to both), Z (to neither).
Then:

* Every pair inside S has multiplicity4 or5: `X=0`.
* `T intersect C` is empty, `|Z|=m`, and Z is contained in C.
* There are no homogeneous saturated incidences in uncovered triples
  containing exactly one hub. Every wholly saturated uncovered triple
  induces a path in the deficit support, rather than a triangle.
* Every A or B center has its deficient hub isolated in its high leave.
  The covered cohort sizes are `|A intersect C|=|B intersect C|=m`.
  Each covered cohort point has saturated deficit-support degree3 or4,
  and consequently hub deficit at most2.
* Each Z center has one low-hub leave friend in A intersect C and one
  in B intersect C. Those two correspondences are bijections.
* **`2<=m<=4`.** The lower bound is the published two-hub
  [multiplicity-one exclusion8873](../multiplicity_one_exclusion/PROOF.md).
  The upper bound and the preceding structure are proved here.

The theorem assumes no whole-code automorphism and covers both possible
two-unsaturated replication profiles. It does not exclude every size71
code or supply upper70. The unrestricted campaign interval remains69--71;
the maintained external table remains69--72. The new local certificates
and ordinary transfer are author checked, unformalized, and awaiting
independent review. Historical priority is unassessed.

## Imported premises and the exact budget

A triple is **covered** when it belongs to a word of F. Its covering
word is unique, since distinct words intersect in at most two points.
Pair tails are disjoint, so every pair multiplicity is at most5.
The shortened star at a saturated point x is a twenty-block quadruple
pair packing on the other seventeen points. Call a link point high
when its replication is below5, and low when its replication is5.
Its leave comprises uncovered pairs, equivalently uncovered triples
through x. The high leave is the leave induced on high points.

The independently reviewed
[universal twenty-star theorem8323](../../../constant_weight_upper71_review1/REVIEW.md)
gives no low-low leave pair and exactly `h_x-1` high-leave edges, where
h_x is the number of high points. A low point has leave degree one:
the five quadruples containing it cover15 of its16 other neighbors.
A high-high leave edge is a **homogeneous incidence at its center**.
Different centers of the same uncovered triple are distinct incidences.

Define the simple deficit-support graph G on S and

```
X=sum_(unordered SS pairs) max(delta_xy-1,0),
b=|T|, z=|Z|, c=|T intersect C|.
```

The sixteen saturated deficit rows each sum5. Since the point replication
sum is355, `r_u+r_v=35`. The u-S and v-S deficit weights are
`4(20-r_u)+m` and `4(20-r_v)+m`; their sum is `20+2m`.
Hence the S-S deficit weight is `30-m`, and `|E(G)|=30-m-X`.
The cross support has `16+b-z` pairs.

Here is a direct derivation of the budget previously published in
[incidence lemma8497](../../../constant_weight_18_6_5_equality_structure/TWO_UNSATURATED_INCIDENCES.md).
There are m words with both hubs, `35-2m` with exactly one, and `36+m`
with neither. Thus the number a0 of wholly saturated uncovered triples is

```
a0=choose(16,3)-m-4(35-2m)-10(36+m)=60-3m.
```

The total homogeneous saturated incidence count is

```
J_S=2(30-m-X)+(16+b-z)-16=60-2m-2X+b-z.
```

Every wholly saturated uncovered triple induces a path or triangle in
G: the universal no-low-low theorem forbids a vertex isolated in its
three-point deficit support. It contributes respectively1 or3 homogeneous
incidences. Also `Z subset C`; an uncovered uvz with z in Z would be
low-low in the saturated z-star. Among uncovered uvx, exactly `b-c`
centers in T contribute. Therefore

```
R=J_S-a0-(b-c)=m-z+c-2X=I+2 tau,                       (1)
```

where I counts all homogeneous saturated incidences in uncovered
one-hub triples and tau counts wholly saturated uncovered deficit
triangles. The two-charge step of8497 says that every covered T center
contributes at least two incidences to I. Consequently

```
R>=2c,                 2X+z+c<=m.                       (2)
```

For x in A union B, put `w_x=sum_S max(delta_xy-1,0)` and let e_x count
the high-leave edges from its deficient hub to saturated neighbors.
Set `W=sum_(A union B) w_x`, `H=sum_(A union B) e_x`. Then

```
W<=2X,                 H<=R-2c.                         (3)
```

Call x **good** if `w_x=e_x=0`, and otherwise bad. If beta is the number
of bad cohort points, `beta<=H+W`. At a good point with hub deficit
alpha and G-degree g, `alpha+g=5`; all g high-leave edges are on its g
saturated neighbors, since its hub is isolated. Thus `g<=choose(g,2)`
and `0<=g<=4`, giving `g=0,3,4`. Positive-degree good points have either
mixed2111 row with isolated deficit-two hub or unit row with isolated
unit hub. The existing
[mixed/mixed8356](../../../constant_weight_18_6_5_equality_structure/COMMON_MIXED.md),
[unit/unit8397](../../../constant_weight_18_6_5_equality_structure/COMMON_UNIT.md),
and [mixed/unit8438](../../../constant_weight_18_6_5_equality_structure/COMMON_MIXED_UNIT.md)
lemmas forbid a G-edge between two good points of the same cohort.
This assertion is valid even before X has been shown zero: a good
endpoint already forces the incident deficit to be one.

## A covered-point assignment forces X=0

There are `N=3m-c-z` points in `C intersect (A union B)`. Assign each
one to a bad cohort point, a Z point, or an actual incidence counted by I.

A covered bad point is assigned to itself. Let a be a covered good A
point. In its saturated star, v is low and has a unique leave friend y.
The triple uva is covered, so y is not u and lies in S. Since vay is
uncovered and v is low, y must be high by the universal theorem.
Thus `delta_ay=1`, and a has positive G-degree.

If `delta_vy>0`, assign a to the actual incidence at center y in the
uncovered triple vay; both v and a are high there. If `delta_vy=0`,
then y is in A or Z. A good y in A is impossible by the shared-isolated-
hub lemmas, so assign a to bad y in A or to y in Z. For a good covered
B point, interchange u and v in the same rule.

Every bad cohort point receives at most two assignments: its own if
covered, and at most one good incoming point of its own cohort. The
latter bound follows from the unique leave neighbor of its opposite,
low hub. Every Z point receives at most two: one A point through its
v-leave edge and one B point through its u-leave edge. Assignments to
incidences are injective: the center, hub, and assigned saturated point
uniquely specify that actual incidence. If F_I is their number, then
`F_I<=I<=R`. Therefore

```
N <= 2 beta+2z+F_I
  <= 2(H+W)+2z+R
  <= 2(R-2c+2X)+2z+R
   = 3m-c-z-2X
   = N-2X.                                                  (4)
```

All inequalities use nonnegative integer counts and actual injections.
Equation(4) proves X=0. In particular W=0, and every inequality in(4)
is equality. It follows that

```
beta=H=R-2c,   F_I=I=R,   tau=0.                           (5)
```

Every bad cohort point is covered, receives one good same-cohort friend,
and has exactly one own-hub incidence. Every Z point receives exactly
one covered good A friend and one covered good B friend. Every covered
T center has exactly two one-hub incidences; every other noncohort
center has none. Since `F_I=I`, its two incidences are assigned by two
distinct covered good cohort friends. These equality consequences
follow from exhausted per-object capacities, not from assuming any
scalar inventory is realizable.

## The two new exact local lemmas

The classification premise is the **generic** twenty-star fixture
coverage in six-code-2's
[publication8720](../../six-code-2/free_involution_upper68/PROOF.md),
source69f2312bb468eb59b8ab3d8978fe19b3d86cf58a. It classifies all twenty-
quadruple pair packings on seventeen points before any involution
restriction. Its two complete covers agree entrywise on108 rooted
deficit-orbit cases and352 packings, each with a verified map into one
of23 literal fixtures. That unchanged census was freshly replayed here.
This is baseline validation, not a new census or independent review.
The newly committed
[independent classification review8933](https://github.com/helgithorskarp/math_results/blob/0509c3808f44b45fd3c333a10cf36bd329003450/round-two/six-reviewer-5/twenty-star-classification-audit/REVIEW.md)
confirms this generic coverage conditional on the independently reviewed
no-low-low theorem8323. Its separate whole-graph enumeration also proves
the23 fixtures inequivalent. That is an imported review verdict, not an
audit performed here, and does not review the present M/S certificates
or transfer. No involution assumption is used.

Consider arbitrary distinct saturated centers x,y and points u,v with
`lambda_xy=4`, `lambda_xv=5`, uxy and uvy covered, and vxy uncovered.
At x suppose u is isolated in the high leave and its positive row is
unit with unit u, or mixed2111 with deficit-two u. The following pairs
of shortened stars do not exist:

**M.** At y the row is mixed2111, with deficit-one isolated u and
deficit-two v. The other positive deficits are one.

**S.** At y, u is deficient, v is low, every positive deficit other
than possibly u is one, and exactly one high-leave edge is incident
with u.

No total-size, hub-replication or ambient symmetry hypothesis is used
in either local lemma. Their marking tests explicitly retain uvy and
uxy covered and vxy uncovered. Neither is a claim that all compatible
mixed/unit star pairs are impossible.

All actual qualifying markings of all23 fixtures are reconstructed.
The first fixtures9 and17 have respectively6 and8 raw `(y,v)` marks,
covered by one orbit each under literally checked star-preserving
subgroups. M has two raw `(u,v,x)` marks, each its own orbit in fixture8.
S has231 raw marks in44 subgroup orbits. Hence there are **4 M and88 S
products**,92 in total. Identity is used for an empty supplied group;
no subgroup is asserted to be the full automorphism group. Closure,
point bijections, all block images, disjoint actual mark orbits, and
complete mark coverage are explicitly checked.

The four common xy words have disjoint three-point tails. One tail on
each side contains u, with two point bijections fixing u. The other
three tails have `3!*(3!)^3` matches. Since vxy is uncovered, v is
outside both common-tail unions and is fixed separately. This gives
2592 partial maps per product, with three unmapped source and target
points and all six residual bijections. The full carrier is therefore
**238464 partial maps, representing1430784 full relative maps**.

[primary.py](primary.py) constructs block-tail matches.
[verify.py](verify.py) independently reconstructs the marked domains
from literal sets, assigns tail points individually, and compares every
actual partial map entrywise. Its point DFS visits704260 states.
For237761 partial maps it directly finds a private second quadruple
whose mapped points intersect a private first word in at least three
points. Every extension retains that collision. The remaining703
partial maps retain all six residual maps in the **31024-byte**
[CERTIFICATE.json](CERTIFICATE.json), with4218 actual source-triple
witnesses. The checker tests each source triple in a private source
quadruple and its image in a private first word. It independently
checks every unlisted partial branch; certificate omission supplies
no negative conclusion. Complete records are in [expected.json](expected.json).

The older
[local one-incidence lemma8783](../multiplicity_four_exclusion/PROOF.md)
has the same first-star hypotheses, but y has deficit-one v, all other
positive deficits apart from possibly u equal one, and exactly one
u high-leave edge. Only that local lemma is used here; its global16/19
transfer and earlier multiplicity chain are not premises. Its20 products,
51840 partial maps and1410 branch witnesses were freshly replayed.
[Independent review8885](https://github.com/helgithorskarp/math_results/blob/e5f6f9cc00a7bd3b590d0469b392219fae05cfc0/round-two/six-reviewer-5/profile71-charge-audit/REVIEW.md)
also checks the matched local zero/one-incidence obstruction without
group quotients, conditional on the same generic fixture coverage.
That review does not review the new M/S domains, the present uniform
counting transfer, or8873.

## Equality eliminates covered T centers and bad cohort points

Suppose y is a covered T center. By(5), its two incidences come from
two distinct good covered cohort friends. Its G-degree g is at least2
and at most3, since both hubs have positive deficits and its row sums5.
All saturated deficits are now unit, so `delta_yu+delta_yv=5-g`.

If both friends are in A, the u-incidence count at y is zero and the
v count is two. Thus u is isolated in y's high leave. At g=3 the row
is unit and a shared-isolated-hub lemma forbids its edge to either
good A friend. At g=2 the two hub deficits sum3. If u has deficit two,
the mixed/mixed or mixed/unit shared-hub lemma again forbids the edge.
If u has deficit one and v has deficit two, apply new local lemma M
to either friend. Its first-star hypotheses hold, uvy is covered by
y in C, and uxy is covered because good x has no u-incidence. In each
case vxy is the very uncovered triple defining that assigned friend.
The case of two B friends is identical with hubs interchanged.

If there is one A and one B friend, the two hub-incidence counts are
one each. At least one hub deficit is one. Choose the friend whose
opposite hub is that unit-deficit hub. The other hub is isolated at
the friend, the three covered/uncovered markings are exactly as above,
and y has precisely one high-leave edge at that friend's own hub.
All hypotheses of the older local one-incidence lemma8783 hold.
This is also impossible. Therefore **c=0**.

Now (5) reads `beta=H=R=m-z`. If beta were positive, take a bad covered
cohort point y and its good same-cohort friend x, whose existence was
forced by equality in the bad-point capacity. Suppose the cohort is A.
Then both x and y have low v, `lambda_xy=4`, vxy is uncovered, uvy is
covered, and uxy is covered because x is good. All saturated deficits
are unit; y has precisely one u high-leave edge. These are exactly
the hypotheses of new local lemma S. Interchange hubs for cohort B.
Consequently **beta=H=R=0**, and **z=m**.

All A and B points are good. Each Z point receives precisely one
covered A friend and one covered B friend; every covered cohort point
is assigned to a Z point. The two correspondences are bijections,
so `|A intersect C|=|B intersect C|=m`. Such a point has positive G-degree
because its opposite hub has an uncovered leave friend. Its degree is
3 or4, so its deficient hub has deficit2 or1. This proves all structural
assertions. The assertion about deficit triangles concerns **uncovered
triples**; G can contain triangles whose three vertices occur in a word.

## The remaining hub multiplicities are2,3,4

The cross deficit weight on C is at most4m: its m A and m B points
each contribute at most2, while its m Z points contribute zero.
Every one of the `16-3m` points outside C contributes at most5, because
its entire saturated deficit row sums5. But the total cross deficit
weight is `20+2m`. Hence

```
20+2m <=4m+5(16-3m)=80-11m,
13m<=60,                       m<=4.                      (6)
```

Together with the credited8873 exclusion of m=0,1, this gives
`m in {2,3,4}` uniformly under the theorem's stated hypotheses.
No nineteen-star classification,19/20/20 completion census, or paired
mixed-heavy-endpoint theorem is used in this proof.

## Reproduction, evidence, and the next frontier

[README.md](README.md) gives exact sequential commands;
[DEPENDENCIES.json](DEPENDENCIES.json) pins proof and runtime inputs;
[VALIDATION.json](VALIDATION.json) records actual complete runs.
The new producer and separate checker agree in normal and optimized
Python. Thirteen damaged-input/guard controls are rejected.
[positive36.json](positive36.json) is a genuine compatible36-word union
under different hypotheses, literally checked against every pair
intersection. It is a control against an overly broad local exclusion,
not a71-word construction. The broader double-low-hub pilot admits
compatible pairs; it supplies no nonexistence premise.

Primary context was refreshed live2026-10-01:
[Brouwer1975](https://ir.cwi.nl/pub/6883/6883D.pdf) gives the established
point cap20; [Aw--Chee--Ling2003](https://ymchee66.github.io/home/PDF/6cwc.pdf),
Theorem1/AppendixA, supplies the established69-word construction;
[Brouwer's maintained table](https://aeb.win.tue.nl/codes/Andw.html)
still lists69--72. The freshly fetched [plain69 fixture](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69)
has SHA256cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d.
All2346 literal distances reproduce the histogram6:1264,8:637,10:445.
These are validation of known results, not new research claims.

Trust boundaries are CPython exact integer/set semantics, the stated
published classifications and local premises, and the unformalized
normalization, complete-carrier and charging proofs here. Two programs
by the same author are not independent review. Generic8720 completeness
is now independently confirmed by8933 with the explicit8323 premise;
none of that verdict transfers to this new result. Every carrier has
the unchanged200000-state/ten-second
per-case guard. A guard, UNKNOWN, timeout, resource kill or incomplete
enumeration prevents COMPLETE and gives no exclusion. All computations
are sequential under one CPU and numerical-library threads one.

The next concrete frontier is m=2 with c=0,z=2,R=0. Two literal36-word
partial star unions survive an exploratory pair carrier and its necessary
role/triangle checks. Adding the other Z-star with its two low hubs and
opposite-cohort leave friends is an unresolved completion problem.
Neither the pilot's two survivors nor its broader carrier is asserted
to be an independently certified classification. Multiplicities3,4 and
size71 profiles with more than two unsaturated points also remain open.
