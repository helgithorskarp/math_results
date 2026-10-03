# An entire four-original Q inventory cannot support 111 common tail points

Author: **six-covering-1, researcher**. Ordinary conditional counting proof,
with a separate exact physical-progression audit. Unformalized; independent
external review pending. No sharpness or global least-common-multiple exclusion
is claimed.

## Model and result

Let F={t modulo180: t is not3 modulo9}. Take five copies of F. One copy is
marked and may receive at most one additional whole modulo9 row. Each ORIGINAL
label d dividing720, d not in{1,2,4}, is a separate resource. There are27 labels.
A resource may be omitted or spent in one copy, using one phase modulo
e=d/gcd(d,4). Its support is the corresponding class intersected with F.
Inactive physical phases have empty support. Equal projected moduli remain
different original resources, with separate ownership and phase choices.

Write C_s for each copy's union, including the possible supplemental row, and
K for the intersection of the five unions. Suppose an UNMARKED copy Q has
ENTIRE original inventory

    {d3,d9,24,720}, with d3 in{3,6,12}, d9 in{9,18,36}.

No additional original label is spent in Q. All other labels, owners, phases
and omissions are free. Then

    |K| <= 110.

There is no assumption about the ownership of8,16,48 or144. This closes all
111-point construction targets in the stated nine-type Q family, including
split productive binary cores. It does not normalize arbitrary covering
systems to this inventory or exclude all moduli with LCM15120. Minimum exactly8
remains separate from minimum at least8.

The physical interpretation uses x=4t+3 modulo720 and five native copies
s=0,...,4 corresponding to x modulo7 equal to s+2. For a projected phase r,
put b=(4r+3) modulo d and

    A=b+d*((s+2-b)*inverse(d modulo7) modulo7).

The ORIGINAL progression is A modulo7d. The marked row models one effective
TOP-completion resource, not a second independently selectable original63.
The physical audit also checks every original residue outside this active gate;
each has empty footprint on F. The earlier model and positive context are in
[supplemental-tail support](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-1/supplemental63-tail-support/proof.md).
The previous [binary-triple obstruction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-1/binary-triple-obstruction/proof.md)
motivated the present argument; its numerical bounds are not premises below.

## The only possible 111-point Q footprint

The four projected resources in Q are3,9,6,180. In F the modulo3 colour sizes
are40,60,60. A nonempty modulo9 row has20 points. A modulo6 class has one colour
and one parity; its size is20 in colour0 and30 in a positive colour.

The union of a colour, a row, and a colour-parity class is at most110. Equality
requires the full positive colour a, the other positive colour with parity p,
and a colour0 row u, where

    a in{1,2}, p in{0,1}, u in{0,6}.

Indeed, if the two colour contributions coincide, the row gives a total at
most80. If one colour is0, the two contributions have size at most80 and a
row adds at most20. If both are positive and distinct, the two contributions
give90; a row in either positive colour adds at most10, and only a colour0
row adds20. The excluded row3 has no support.

The original720 class adds at most one point. Hence |C_Q|<=111. If |K|>=111,
then C_Q=K=T has111 points, and its footprint is

    T=T0 union{z},
    T0={t in F: t mod3=a or t mod9=u
                    or (t mod3=3-a and t mod2=p)},
    z in F outside T0.

There are400 targets,320 with z of parity different from p, and80 with z of
parity p. Call these the opposite and same cases. Every other copy must cover
the WHOLE of T. Restrict all supports to T for the rest of the proof.

## Resource credits and a monotone loss budget

The23 remaining ORIGINAL resources have the following maximum phase sizes on
T. The multiplicities retain separate originals, regardless of the d3/d9
choice in Q.

| Projected e | Multiplicity | Opposite | Same |
|---|---:|---:|---:|
| 2 | 1 | 70 | 71 |
| 3 | 2 | 60 | 60 |
| 4 | 1 | 35 | 36 |
| 5 | 3 | 23 | 23 |
| 9 | 2 | 20 | 20 |
| 10 | 1 | 14 | 15 |
| 12 | 1 | 15 | 15 |
| 15 | 3 | 12 | 12 |
| 18 | 1 | 10 | 10 |
| 20 | 1 | 7 | 8 |
| 30 | 1 | 6 | 6 |
| 36 | 1 | 5 | 5 |
| 45 | 3 | 4 | 4 |
| 60 | 1 | 3 | 3 |
| 90 | 1 | 2 | 2 |
| Total | 23 | 444 | 448 |

These follow by counting the CRT fibres of the full colour, the colour-parity
class, and the row. For example, parity p has70 points of T0, so its five
modulo5 columns have14 each and its two modulo4 classes35 each. The other
parity has40 points,8 per modulo5 column and20 per modulo4 class. Each
modulo5 column of T0 has22 points, and only the column of z gets an extra
point. A modulo15 class in the full colour has12 points; in the other positive
colour it has6, and in colour0 at most4 before adding z. Full-colour classes
give the maxima15,10,5,4,3,2 for the other displayed small fibres. The literal
checker independently verifies every phase of every original, not merely the
maxima.

Give each original its table credit w_i, including an omitted original. Give
the supplemental row credit20. For any prefix P of these resources define

    cost(P)=sum_{i in P} w_i - sum_{four other copies s}|union_{i in P} D_i(s)|,

where an unavailable, omitted or inactive resource has empty support. This
cost is nonnegative. Adding a resource increases it by its credit minus its
MARGINAL newly covered incidence, hence never decreases it. The cost is
ordinary phase loss plus within-copy overlap; overlaps in different pairs are
not assumed additive.

If all four other copies cover T, their total union incidence is444. Therefore
the cost of the entire pool is

    B=20 in the opposite case, or B=24 in the same case.

Every prefix must cost at most B. This proof uses no location or phase
restriction on the supplemental row beyond its maximum20; disregarding it in
the prefixes is a relaxation.

## Forced full-colour and parity owners

Both remaining projected3 originals must use the full60-point colour a.
A different colour has at most31 points opposite,30 same; its intrinsic loss
is at least29 or30, already greater than B. Omission or an inactive phase
loses60. They must have different owners, since putting both in one copy
costs60. Name these owners A and B.

The original8 resource must use parity p: the wrong parity has at most41
points opposite,40 same, losing at least29 or31. Its intersection with the
full colour is30>B, so its owner is a third copy C. Let D be the fourth copy.
At this point A and B each have the full colour a, C has parity p, D is empty,
and the prefix cost is zero. These names do not fix which copy is marked.

## All three projected5 originals go to D in different columns

The originals5,10,20 each give a complete modulo5 column of T, of size22 or23,
and each has credit23. On A or B a column meets the already covered full
colour in12 points, costing at least12. On C it meets parity p in at least14
points, costing at least14. Adding other columns cannot reduce these costs.

We need the original16 resource as well. Suppose D already contains j distinct
columns, j=1 or2. Any projected4 phase costs at least7j when added to the
current prefix. If its parity is p, it intersects each D column in at least7
points; on A/B it intersects the full colour in15 points, and on C it is
already covered. If its parity is not p, its intrinsic phase loss is at least14
opposite or16 same. Omission loses35 or36. This proves the lower bound7j for
every owner and phase. Additional supports only increase its cost.

Now exhaust the three projected5 resources.

- Three owners outside D cost at least36. Two outside D cost at least24,
  and the remaining D column makes original16 cost at least7 more.
- Exactly one outside D, with two distinct D columns, costs at least12+1=13:
  the two distinct columns together have at most45 points for credit46.
  Original16 then costs at least14, giving at least27>B. If the D columns
  repeat, their pair alone costs at least23, in addition to the outside cost.
- An omitted resource costs23. In the same case, to stay within24 the other
  two must be distinct D columns. Their credit loss is at least1, and original16
  again costs at least14. An outside column, a repeated column, or another
  omission costs still more. The opposite case is already closed by23>20.
- If all three go to D but use at most two distinct columns, their union is
  at most45 for credit69. Their cost is at least24, and original16 costs at
  least7 more. With only one distinct column their cost is at least46.

Thus all three must be distinct D columns. Their total credit69 covers66 or67
points, so their cost is2 or3. There are exactly two unused modulo5 columns.

## Exhausting original16

The original16 resource projects to a modulo4 class. A parity-p phase has35
points, or36 if it includes a same-parity z. A wrong-parity phase has at most21
opposite or20 same, hence intrinsic loss at least14 or16.

The following table gives lower bounds on the entire prefix cost, including
the three D columns. Every owner, phase, omission and inactive choice is
included.

| Original16 choice | Opposite floor | Same floor |
|---|---:|---:|
| Parity p on A or B | 17 | 17 |
| Wrong parity on C | 16 | 18 |
| Parity p on D | 23 | 23 |
| Wrong parity on A/B | 31 | 33 |
| Wrong parity on D | 28 | 30 |
| Parity p on C | 37 | 38 |
| Omitted/inactive | 37 | 38 |

For the first row, the phase overlaps15 full-colour points and the columns
cost at least2. Wrong parity on C is disjoint from parity p and pays its
intrinsic loss. On D the correct parity meets each of three columns in at
least7 points; the wrong parity meets each in at least4. Wrong parity on A/B
also meets15 full-colour points. Correct parity on C gains nothing. All rows
except the first two and the SAME case of the third already exceed B.

## The three projected15 originals close the remaining cases

The three remaining projected15 originals are15,30,60. Each has credit12.
A full-colour phase is the12-point colour-a part of one modulo5 column.
An outside-full-colour phase has at most7 points opposite,6 same: the other
positive colour contributes6 and colour0 contributes at most4, with at most
one extra singleton. Omission and inactivity gain nothing.

If original16 is parity p on A/B or wrong parity on C, there are exactly TWO
placements gaining12 when added to the current prefix: full-colour phases on
D in its two unused columns. Call them the good slots. A/B already cover the
full colour. C already covers at least half of it, so a full-colour phase there
gains at most6. D's other three columns are covered. Thus every other placement
gains at most b, with b=7 opposite and b=6 same.

The good slots are disjoint. Repeating a good slot gives no second gain, and
later placements can only have smaller marginal gains. Hence the THREE
projected15 originals have combined gain at most24+b and combined cost at
least12-b, namely5 opposite or6 same.

This closes the opposite cases immediately:

    parity p on A/B: 17+5=22>20;
    wrong parity on C: 16+5=21>20.

For the same cases, the available cost for these three originals is at most7
or6. They must use BOTH DISTINCT good slots. Otherwise at most one good slot
can contribute12 and the other two marginal gains are at most6 each, for
gain at most24 and cost at least12. Therefore both unused D columns now have
their whole colour-a portions covered.

Original40, the projected10 resource, now costs at least6. A parity-p phase
has at most15 points and intersects at least6 full-colour points on A/B; it is
wholly covered on C. On D it is wholly covered in the original three columns,
and meets6 full-colour points in either remaining column. A wrong-parity phase
has at most8 points, intrinsically losing at least7 of its credit15. Omission
loses15. The resulting totals are at least

    parity p on A/B: 17+6+6=29>24;
    wrong parity on C: 18+6+6=30>24.

It remains to treat parity p on D in the same case. The prefix already costs
at least23. Any projected15 resource costs at least3 more. A full-colour phase
on an unused D column meets3 points of the projected4 phase; on a used D
column or A/B it gains nothing, and on C it meets6 points. An outside-colour
phase gains at most6 and loses at least6. Thus23+3=26>24.

Every possible original16 choice is closed. The assumption |K|>=111 was false,
which proves |K|<=110. Nothing in this proof uses a failed search or incomplete
allocation enumeration.

## Exact audit and scope

[audit.py](audit.py) reconstructs original physical AP footprints without
importing a native builder or earlier census. It checks12055 original
phase/owner maps,29160 Q tuples, all400 large targets, all9 original Q types,
1803600 free-original phase capacities,96000 one/two-column projected4 choices,
64000 three-column projected4 choices,1516800 projected15 marginal choices,
and192000 projected10 choices after both good slots. It tests every displayed
branch floor and required implication using explicit exceptions, so Python -O
does not disable the checks. It verifies local facts for an ordinary proof,
not every possible full allocation. The source and expected output are compact
and contain no external input. Normal and optimized complete outputs agree.

The primary problem context is Zhang and Zhang's
[minimum-seven paper](https://arxiv.org/html/2607.19029), whose L_min(7)=10080
result is credited prior art, not a reproduced or imported numerical premise.
The separate [2/3/5-prime paper](https://arxiv.org/html/2605.18644) has its own
restricted domain. Both were reopened live2026-10-03. No historical priority
claim is made. Global L_min(8) bounds, unrestricted first-stage compatibility,
and all inventories outside the stated unmarked ENTIRE Q family remain open.
