# Independent original-tail exclusion and weaker 16 hypothesis

Actual author **six-reviewer-2**, role **independent mathematical reviewer**,
2026-10-03. The shared signing identity does not establish authorship.
This is an ordinary unformalized proof with independent exact arithmetic.
The complete defining written LEMMA10022 was exposed; this is **not blind**.
The new target executable and expected record were unopened when this proof,
the two fresh arithmetic programs and their validation interface were sealed.

## Domain and dependencies

A finite covering of the integers has pairwise distinct ORIGINAL moduli
dividing 10080, minimum exactly 8, and placed classes

\[
8:0, 9:0, 10:1, 14:0, 12:10, 16:2, 28:4, 32:6.
\]

Here \(m:a\) denotes the class \(a\pmod m\). BASE comprises ALL selected
original divisors of 2520; its holes are residues modulo 2520. Other
original divisors are exactly \(16d,32d\), \(d\mid315\). A selected TAIL
is productive if it meets a physical 10080 lift of an actual BASE hole.
\(T\) counts productive ORIGINAL tails including the placed 16 and 32.
Actual LCM may be a proper divisor of 10080. All other phases and omissions
are free, including selected unproductive tails.

We prove the new implication **\(T=8\) is impossible** assuming an actual
BASE hole in parent 2 modulo 8 and essentiality of the placed 32 class.
Essentiality means deleting that particular congruence destroys coverage.
The placed 16 remains required, but need not be essential.

For \(T\ge8\), use the explicit earlier theorem 9978 in its essential
16/32 domain, and 10004's proved extension replacing essential 16 by a
nonempty actual parent 2. Thus \(T\ge9\) in the weaker domain as well.
This uses the earlier eight-tail theorem as a stated dependency; this
packet does not pretend to re-review all \(T\le7\) cases or rerun either
earlier source package. The BASE177 calculation credited to 9934 and the
odd-footprint method credited to 9920 are freshly recomputed here.
Different 14:1 numerical statements from 9859/9958 are unused.

In particular the entire essential 16/32 theorem 10022 follows. Presence
of the eight placed classes alone does not imply either remaining extra
hypothesis. There is no full-prefix exclusion, normalization of arbitrary
minimum-eight covers, covering witness, sharpness or global LCM bound.

## BASE demand, physical lifts, original labels

The six BASE prefix classes miss \(R\subset\mathbb Z/2520\), with
\(|R|=1396\) and parent populations \((0,224,150,224,200,224,150,224)\).
There are 35 unused original BASE labels, obtained by taking every divisor
of 2520 at least 8 and deleting the six spent labels. All phases of all
35 labels, including 21 and 2520, are retained.

For every raw phase pair \((a,b)\in[0,14]\times[0,17]\), put
\(F=R\cap((a\bmod15)\cup(b\bmod18))\). Any completed BASE covers at most

\[
K(a,b)=|F|+\sum_{m\ne15,18}\max_{0\le c<m}|(R\setminus F)\cap(c\bmod m)|.
\]

Both fresh implementations verify all 270 pairs and all 8910 marginals:
\(1051\le K\le1219\). Consequently every BASE leaves at least 177 holes.
Completing an omitted original by any phase can only reduce holes, so
this necessary lower bound covers partial inventories. It assumes no
tail selection, essentiality, or exact-LCM equality.

Every hole \(n\) has all four distinct lifts \(n+2520k\), \(0\le k<4\),
uncovered by BASE. An H original \(16d\) meets zero or two lifts, one
binary half; a Q original \(32d\) meets zero or one. CRT proves this
because \(d\mid315\), coprime to the binary part. Every tail belongs to
exactly one parent modulo 8. Unproductive selected tails repair no hole.

The nonempty parent 2 makes placed16 productive: its cofactor is one,
so it meets two lifts of every hole there. Essential32 supplies an
exclusive witness outside BASE, hence a hole in parent6 and productivity
of placed32. Parent2 needs at least two resources; parent6 at least
three, since a placed quarter and one half cover at most three lifts.
Any further hole parent needs at least two. Parent0 is filled by 8:0.
If all parent6 extras are H, their halves must cover all four lifts at
every hole without the placed quarter. BASE covers nonholes and that
quarter meets no other parent, making 32 globally redundant. Thus every
parent6 inventory has an extra Q. No extra tail is assumed essential.

All unused cofactors are
\(D=\{3,5,7,9,15,21,35,45,63,105,315\}\). H cofactors are globally
distinct across parents; Q cofactors likewise. Cross-type equality is
legal: \(16d\) and \(32d\) are different original labels.

## Exact footprint budgets

Parents2/6 share the odd shadow
\(U=\{y\bmod315:y\ne0\bmod9, y\ne1\bmod3, y\ne0\bmod7\}\),
of size 150. Actual additional BASE classes only shrink it.
The entire phase populations give, in the order \(1,D\),

\[
C(d)=(150,90,30,25,30,18,15,5,6,5,3,1).
\]

Compatible intersections have one phase at the cofactor LCM; incompatible
ones are empty. \(S_1,S_2,S_3,S_4=(90,120,150,175)\) are distinct-global-H
capacity sums. The complete Q rows give pair intersection 30, triple
intersection 18, three-Q sum of pair intersections 54, four-Q sum of
triple intersections 36 and five-Q sum of triple intersections 72.
All 55/165/330/462 cofactor groups are retained.

Three H in ONE parent have union at most 126. Every triple whose individual
sum exceeds 126 is checked at every raw phase; the others are bounded by
their individual sum. This assertion is not applied across parents.

For four Q in parent2, filling the missing half requires both missing
quarters. Assign the four labels to two nonempty arms A/B corresponding
to these quarters; irrelevant positions can be assigned to either arm,
enlarging the bound. Their common footprint is bounded by

\[
\min\{\sum_{a\in A}C(a), \sum_{b\in B}C(b), 
\sum_{a\in A,b\in B}C(\operatorname{lcm}(a,b))\}.
\]

Every quartet and all seven unordered nonempty partitions give 2310 rows,
with maximum 66. Fixing the first label in A counts each partition once.

For five H and one Q distributed across the mandatory parents, let P
be the nonempty parent2 H set and split the remaining H into nonempty
opposite-half O and same-half A relative to placed32. Any parent6 hole
must lie in \(\cup O\cap(\cup A\cup F_q)\). Its capacity is at most

\[
\min\{UB(O), \sum_{o\in O,a\in A}C(\operatorname{lcm}(o,a))+
\min(C(q),\sum_{o\in O}C(\operatorname{lcm}(o,q)))\}.
\]

Here UB is the exact one-parent maximum H union. Of all 462 five-H sets,
453 have individual sum at most176. The other nine have every P/O/A
assignment and every Q cofactor evaluated: 1620 assignments, maximum
175. Combining the low and high sets yields the conservative 176 bound.
The extra inner minimum respects one Q footprint even when counted in
several pair intersections. Cross-H/Q equality is retained.

Similarly, HQQ/HHQ has parent2 H capacity plus the Q-pair allowance30,
and the same O/A condition for its parent6 pair. All 1485 H assignments,
each with all eleven Q cofactors, give at most168. HHQ in parent6 alone
has at most90 holes: with one opposite H it is bounded by that H; with
two opposite H and no same-half H, the extra Q must be active.

The reviewer deliberately regenerates an enlarged required UB catalogue:
141 groups, 479477 COMPLETE raw phase entries, including all groups
needed by the triple, five-H, mixed and final inventory checks. This
differs from the author's 116-group subcalculation and is not its record.

## All three-parent and two-parent allocations at T=8

Four hole parents need at least \(2+3+2+2=9\) productive originals.
Three-parent counts are exactly \((2,4,2),(3,3,2),(2,3,3)\), with third
parent in \(\{1,3,4,5,7\}\). Two resources at the third parent must be
opposite H. Its pair footprint maximum is 28 in an odd parent,25 in4.
Globally coupling that pair \(g,h\) to three distinct further H labels
\(a,b,c\) gives

\[
M_r(\operatorname{lcm}(g,h))+C(a)+C(b)+C(c)\le166
\]

(165 in4). The full 4620 distinct-label rows are checked for both shadow
types, applying to all five physical parents. In counts2/4/2, parent2
extras are H and parent6 extras HHQ/HQQ/QQQ, giving166/148/136 in an odd
third parent. In counts3/3/2, parent6 extras are HQ and parent2 extras
HH/HQ/QQ, giving166/148/148. In2/3/3, mandatory parents have at most120
holes; the third HHH/HHQ/HQQ inventory has at most56/28/28 respectively;
QQQ cannot cover four lifts. Totals176/148/148 follow. Parent4 is smaller,
with maximum170. The complete 45 allocation rows and all1360 three-class
physical inactive/half/quarter states are retained. Hence three parents
cannot meet demand177.

Two-parent counts are exactly \((2,6),(3,5),(4,4),(5,3)\).
If h/q counts describe the extras, parent2 coverage implies an active H
or two active Q; parent6 implies an active H or three active Q. Thus
distinct global H sums plus the complete Q-intersection sums give all
generic bounds. The preceding triple-H, four-Q, five-H/Q, mixed and HHQ
lemmas close precisely the exceptional cases. The full 34 positive types
are regenerated; `type_rows` records the complete bounds/methods rather
than selecting only survivors. The raw10980 local states include all-H
redundancy and impossible inventories as well as positive types. A second
implementation realizes every state with actual original congruences at
four integer lifts. All types have upper bound below177 except

\[
\text{parent2 HHQQ / parent6 HQ at counts }(5,3),\quad\text{bound }180.
\]

No unallocated productive resource exists: productivity itself places
every counted resource in a hole parent. Relaxing Q collisions in generic
upper bounds preserves all actual inventories; the surviving inventory
then restores ALL global original-label restrictions.

## Unique surviving inventory, every original phase, BASE contradiction

Write a/b for parent2 H cofactors, f for parent6 H, g/h for parent2 Q and
q for parent6 Q. The H triple is distinct, the Q triple distinct,
and cross-type equality is legal. Necessary capacity is

\[
UB(a,b)+C(\operatorname{lcm}(g,h))+C(\operatorname{lcm}(f,q)).
\]

Every H triple other than3/5/9 has individual sum at most145, so adding
the parent2 Q-pair allowance30 gives at most175. For3/5/9 all1485
original inventory rows are checked. Only
\(f=q=5, \{a,b\}=\{g,h\}=\{3,9\}\) reaches177, with bound180.
The productive original labels are therefore

\[
\text{parent2: }16,48,144,96,288;
\qquad\text{parent6: }32,80,160.
\]

These can repair at most150/30 initial holes. Demand177 forces at least
147/27 repairable initial holes, respectively. We enumerate all46656
original48/144/96/288 phase tuples in parent2 and all200 original80/160
phase tuples in6. For EACH tuple allfour lifts of all150 initial holes
are evaluated. There are four qualifying parent2 tuples,

\[
(26,42,42,282), (26,42,90,138), (26,138,42,186), (26,138,90,42),
\]

each repairing all150 holes, and five qualifying parent6 tuples
\((14,54),(30,150),(46,86),(62,22),(78,118)\), each repairing30 holes
at one common mod5 phase. Thus all20 qualifying phase completions have
repairable set

\[
S_c=\{n\in R:n=2\bmod8\}\cup
\{n\in R:n=6\bmod8, n=c\bmod5\},\quad0\le c<5,
\]

with \(|S_c|=180\). This is necessary, not a realizable BASE inventory.
Actual holes are a subset of \(S_c\), so selected additional BASE classes
cover at most three of its points. Each individually intersects it in
at most three points. They must cover ALL \(|R\setminus S_c|=1216\)
outside points, since no productive tail can repair them and any
unproductive selected tail is, by definition, inactive on actual holes.

For each of the35 unused originals compute the maximum outside footprint
over every phase intersecting \(S_c\) at most three times. All46255
phase rows over the five shapes are checked. Each shape's full marginal
list sums to1156. At most one selected phase per original and arbitrary
omissions imply outside union at most1156, leaving at least60 necessary
points uncovered. The six fixed BASE classes meet no R point. This
contradicts covering, excludes \(T=8\), and completes the stated theorem
relative to the earlier eight-tail dependency.

## Trust and exact coverage

`literal.py` builds physical residues and compressed bitmaps; `direct.py`
uses set unions and direct modulo histograms for the earlier budgets and
an interleaved600-physical-incidence model for every final phase. It
derives its whole input/group/type catalogues independently and compares
EVERY mathematical field, complete finite rows and every raw phase stream.
No producer or prior researcher arithmetic module is imported. Whole
mode/cold results and all controls are recorded in RESULT/VALIDATION.
Generated ~1MB records stay in ignored caller scratch; compact source
and hashes regenerate them. Hash agreement is not the completeness proof:
the explicit Cartesian domains and ordinary reductions above supply it.

The remaining trust boundary is CPython exact integers/sets, the operating
system and these programs, together with ordinary covering-period/CRT,
essentiality/redundancy, omission/completion and case-coverage arguments.
The earlier at-least-eight theorem is an explicit mathematical dependency.
This is not proof-assistant formalization or an audit of worldwide priority.
