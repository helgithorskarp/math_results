# A binary-triple allocation obstruction for covering tails

Author: **six-covering-1, researcher**. Ordinary counting proof with a separate
literal arithmetic-progression audit. Unformalized and independently unreviewed.

## Model and statements

Put F={t modulo180: t is not3 modulo9}. There are five copies of F, numbered
0,...,4. Copy0 is marked and may receive one additional whole modulo9 row.
Every original label d dividing720, with d not in{1,2,4}, is a separate resource:
it may be omitted or assigned to one copy with one phase modulo
e=d/gcd(d,4). Inactive original phases have empty support. Equal projected
moduli do not merge original resources. For copy s let C_s be its union and
let K be the intersection of all five unions.

Assume an unmarked copy Q has **entire original inventory**
{d3,d9,24,720}, where d3 is3,6 or12 and d9 is9,18 or36.
The four other copies may receive any of the other original resources, with
arbitrary phases and omissions. The following bounds hold for a copy B other
than Q; additional originals on B are explicitly allowed.

1. If B contains {8,16,48,144}, then |K|<=110 when B is unmarked,
   and |K|<=107 when B is marked.
2. If B contains {8,16,48}, then |K|<=110 when B is unmarked,
   and |K|<=108 when B is marked.
3. Consequently, |K|>=111 requires selected classes from {8,16,48}
   productive on C_Q in **at least two** other copies. If every such productive
   class is in the marked copy, then |K|<=108.

There are nine original Q types and sixteen ordered Q/B placements.
No sharpness is asserted. These are conditional statements in the specified
five-copy relaxation, not a normalization or exclusion of arbitrary distinct
covering systems with minimum exactly8.

The physical interpretation is x=4t+3 modulo720, with native copy s represented
by x modulo7 equal to s+2. For an active original phase r, put

    b=(4r+3) mod d,
    A=b+d*((s+2-b)*inverse(d modulo7) mod7).

The corresponding original progression is A modulo7d. The marked row is an
effective resource supplied by the chosen TOP completion; it does not give a
second independently allocated original63 label. Original14:7 and28:15 account
for the other two modulo7 copies in that construction context. The complete
relaxation and an earlier99-point example are in the
[supplemental-tail source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-1/supplemental63-tail-support/proof.md).
Neither that positive example nor its numerical upper bound is used below.

## Large Q and the target capacities

Q has projected resources3,9,6,180. The colour sizes modulo3 in F are40,60,60;
each nonempty modulo9 row has20 points. The union of a colour, a row and a
colour-parity class has at most100 points, except for the following110-point
case:

    T0 = {t in F: t mod3=a or t mod9=u
                    or (t mod3=3-a and t mod2=p)},
    a in{1,2}, u in{0,6}, p in{0,1}.

Indeed, coincident colours give at most60+20. If one of two distinct colours
is0, they contribute at most80 or70 before adding the row. Two positive
colours contribute60+30; a row in one of them adds at most10, whereas a row
in colour0 adds20. The singleton contributes at most one point. Thus |Q|<=111,
and any Q footprint with at least108 points is contained in
T=T0 union{z}, z in F outside T0, |T|=111.
There are400 such targets:320 have z of parity different from p;80 have parity p.
If Q has110 points, a same-parity z may be chosen in the other colour0 row.

After removing Q and {8,16,48,144}, nineteen original resources remain.
Their phase capacities on T are the following, independently of the original
d3/d9 aliases. Multiplicities retain distinct original labels.

| Projected e | Multiplicity | z opposite parity | z same parity |
|---|---:|---:|---:|
| 3 | 2 | 60 | 60 |
| 5 | 3 | 23 | 23 |
| 9 | 2 | 20 | 20 |
| 10 | 1 | 14 | 15 |
| 15 | 3 | 12 | 12 |
| 18 | 1 | 10 | 10 |
| 20 | 1 | 7 | 8 |
| 30 | 1 | 6 | 6 |
| 45 | 3 | 4 | 4 |
| 60 | 1 | 3 | 3 |
| 90 | 1 | 2 | 2 |
| Sum | 19 | 319 | 321 |

Each modulo5 column contains22 points of T0, with one extra in the column of z.
Parity p has70 points of T0, fourteen per column and seven per matching
modulo20 phase. The opposite parity has40 points, eight per column and four
per matching modulo20 phase. Positive full colours give the e3/e15 capacities;
full rows and CRT counts give the remaining entries. The supplemental row has
capacity20. An original144 resource has e36 and capacity5; original72 has
e18 and capacity10.

Therefore, after removing only Q and {8,16,48}, the twenty-resource capacity
sum is324 or326. After removing Q and {8,16,48,72}, it is314 or316.
These counts bound arbitrary phases, inactive choices and omissions.

## A three-copy obstruction with no binary4 contribution

The nineteen-resource pool in the table, together with at most one supplemental
row, cannot cover T in three copies. Suppose otherwise. Credit every resource
with its displayed maximum, including resources omitted from these three
copies or spent somewhere else. The total credit W is339 or341, against333
required incidences. If D_i is its actual support in one of these three copies
(empty for a resource unavailable to them), define

    L = sum_i (w_i - |D_i|),
    R = sum_i |D_i| - sum_s |union of supports in copy s|.

Then L,R are nonnegative and L+R=W-333 is6 or8. Each pair intersection within
one copy is a lower bound for R; pair intersections are not assumed additive.

Both e3 originals must cover the full60-point colour a: any other colour has
at most31 target points. Their owners differ because overlap60 exceeds the
budget. Every e5 phase meets this colour in twelve points, so all three e5
originals belong to the third copy. Their columns differ, since equal columns
overlap in at least22 points. Their total support is at most23+22+22=67,
against credited69, so L>=2.

An e15 phase in colour a has twelve points. It cannot occupy a full-colour
copy, an e5-occupied column of the third copy, or a repeated finer column there.
Only two columns remain. Hence at least one of the three e15 originals is
outside colour a or omitted. Its loss is at least5 in the opposite-parity
case and at least6 in the same-parity case. Thus L>=7 or8.

The opposite-parity case contradicts its budget6. In the same-parity case,
L=8 and R=0 are forced. Every other original attains its maximum, including
the e10/e20 originals with15/8 points. These maxima require phases z modulo10
and z modulo20. Their supports meet the full colour a in six and three points,
so zero overlap places both in the third copy. Their mutual intersection has
eight points, contradicting R=0.

This obstruction does not use B's phases or its own coverage. Resources spent
as additional labels on B simply contribute empty D_i in the other three
copies. Thus it already permits those extra labels.

If B is unmarked and contains all four binary originals, |K|>=111 would give
K=Q=T, while the other three copies receive precisely a suballocation of this
nineteen-resource pool, with the marked row allowed. This is impossible.
If B is marked, |K|>=108 puts K inside such a T, while three unmarked copies
have total capacity at most321<3*108. This proves statement1.

We also need the alternate nineteen-resource pool that removes original72
instead of144. Its credit, including the marked row, is334 or336, leaving
budget1 or3. The two e3 originals again occupy different full-colour copies,
and the three e5 originals occupy distinct columns of the third copy, giving
L>=2. This already contradicts budget1. For budget3, the three e15 originals
again force another loss of at least6, contradicting it. Extra labels and
omissions are handled as empty supports exactly as before.

## The binary-triple obstruction

First let B be marked and contain {8,16,48}. If |K|>=109, the large-Q argument
places K inside a111-point T. The other three copies are unmarked and have at
most the twenty-resource pool of total capacity326<3*109. Therefore |K|<=108.

Now let B be unmarked, and suppose |K|>=111. Then K=Q=T. Let E be the additional
original labels on B, beyond {8,16,48}, and let S be the sum of their target
capacity credits. Covering T in the other three copies requires333 incidences.
Their total capacity is at most344-S or346-S, including the marked row.
Consequently S<=11 in the opposite-parity case, and S<=13 in the same-parity
case. In particular B's three binary phases must cover at least100 or98 points.

Write h for the e4 phase of original16. The e2 phase of original8 must be p:
if it has opposite parity, the three-phase union has at most
40+35+15+1=91 target points. Next h must have opposite parity to p, because an
e4 phase of parity p is contained in the e2 phase, leaving at most71+15=86.
The e12 phase of original48 must have residue h'=h+2 modulo4. Otherwise it is
contained in the e2 or e4 support, leaving at most91. Finally it must have
colour a. In another colour its support has at most6 points, so the union has
at most91+6=97. All these bounds are below98. Empty or omitted binary phases
can only reduce the union; one may also freely replace an empty phase by an
active one without losing any target point.

The forced phases leave uncovered the five-point row

    G = {t in F: t mod9=u and t mod4=h'}.

Its points form t0+36k for k=0,...,4 and have different residues modulo5.
Every additional original whose projected modulus is divisible by5 can cover
at most one of them.

The only additional originals with projected modulus not divisible by5 and
capacity no more than13 are72 and144. The other such labels are the two e3
originals (capacity60) and the two e9 originals (capacity20). If144 is on B,
statement1 already gives a contradiction. If72 is on B, the alternate
nineteen-resource obstruction above gives a contradiction, with all further
extras still permitted.

If neither72 nor144 is on B, every affordable extra original is divisible
by5 after projection. Repairing the five different points of G therefore
requires at least five extras. The five cheapest such distinct originals have
capacity credits2,3,4,4,4: canonical labels360,240,45,90,180. Their sum17 exceeds
both permitted budgets11 and13. Contradiction. This proves statement2.

For statement3, any selected core3 class not productive on C_Q may be moved
to B without removing a point of K from its former copy; an omitted class can
be added on B. If all productive core3 classes occur in at most one copy B,
these moves put all three labels on B while preserving K. Apply statement2.
If there are no productive core3 classes, choose B to be marked. If the
productive classes occur only in the marked copy, the marked108 bound applies.

## Exact audit and construction status

`audit_binary3.py` is a standalone standard-library checker for the counting
facts, using physical original progressions rather than a producer table.
It checks12,055 original-phase/owner maps,29,160 raw Q tuples, all400 targets,
193,200 remaining20 phase capacities, all38,400 binary3 phase triples, and
324,000 original-phase intersections with the forced five-point rows.
Only800 binary3 triples pass the forced-phase pattern; the other37,600 have
support at most96. The proof uses the weaker97 bound. The checker does not
enumerate all resource allocations, and such an enumeration is unnecessary
for the ordinary capacity/loss/overlap argument.

The new constraint is that productive core3 originals must split across at least
two non-Q copies in any111-point construction in this family. The global
L_min(8) problem and exactly-eight first-stage compatibility remain unresolved.
No stochastic search is a premise of this lemma. No sharpness is asserted.

Primary-literature context, checked2026-10-03: Shiliang Zhang and Jiheng Zhang,
[minimum7/LCM10080](https://arxiv.org/html/2607.19029), is prior art and is not a
new result here. The restricted-prime problem in
[arXiv2605.18644](https://arxiv.org/html/2605.18644) is distinct from this chosen
construction route. Neither paper supplies a numerical premise in the proof.
No exhaustive literature-absence or historical-priority assertion is made.
