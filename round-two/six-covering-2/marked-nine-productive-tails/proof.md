# Nine productive tails by original-inventory and BASE gluing

Actual author **six-covering-2**, role **researcher**, 2026-10-03.
Ordinary combinatorial proof with complete exact same-author checks.
The ordinary covering, CRT, essentiality and allocation bridges are
unformalized. Independent review of this new nine-tail result is pending.

## Precisely quantified domain

Let a finite covering of all integers have pairwise distinct ORIGINAL
moduli dividing10080, minimum modulus EXACTLY8, and the literal classes

```
8:0, 9:0, 10:1, 14:0, 12:10, 16:2, 28:4, 32:6.
```

Here `m:a` means the congruence class `a mod m`. Assume EXPLICITLY that
the placed16 and32 classes are essential: deleting either destroys the
covering. All other original phases and omissions are unrestricted.
The actual LCM may be a proper divisor of10080. Presence alone is not
essentiality; no presence theorem is a premise of this publication.

BASE consists of **all** selected original divisors of2520. Every other
original divisor of10080 is16d or32d, where d divides315; these are TAILs.
A selected TAIL is productive when it meets any physical10080 lift of
an actual BASE hole. Count T includes the productive placed16 and32.

**Theorem. Every covering in this precise domain has T at least9.**

Two ordinary public dependencies have exactly these hypotheses:
[9934](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/marked-seven-productive-tails/proof.md),
source2f802f7e4163689bedd41b2b87113e9d231a957d, gives at least177 BASE
holes; [9978](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/marked-eight-productive-tails/proof.md),
source135a34c6695cc7aaf34d4955722822ccd51d5b27, gives T at least8.
We exclude T=8. This driver's new computations do not claim to rerun
those separate public packages. Their exact proof sources are linked.

This is a conditional tail-resource result. It excludes neither the
whole displayed prefix nor all10080 minimum-eight covers, and improves
no global L_min(8) bound. The32:10,28:21,16:4 and14:1 domains remain
separate. No covering, feasibility, optimality or sharp capacity is claimed.

## 1. Period, essentiality and original-label accounting

The six placed BASE classes leave R of size1396 modulo2520. Its hole
counts in parents0 through7 modulo8 are

```
0, 224, 150, 224, 200, 224, 150, 224.
```

Every actual BASE hole has four physical lifts n+2520k, k=0,1,2,3.
An H class16d covers zero or two lifts, one binary half. A Q class32d
covers zero or one. Each TAIL belongs to one mod8 parent. Unproductive
selected TAILs touch no BASE hole and cannot repair one.

Essentiality supplies exclusive witnesses outside BASE, hence nonempty
hole parents2 and6 and productivity of placed16/32. Parent2 needs at
leasttwo TAILs; parent6 needs at leastthree because placed32 is one
quarter. Any further hole parent needs at leasttwo. Parent0 has no holes.
Four hole parents thus need at least2+3+2+2=9 resources.

All extra cofactors exceed1 because original16 and32 are already spent.
H cofactors are globally distinct across ALL parents; Q cofactors are
likewise globally distinct. Equality of an H and Q cofactor is allowed:
16d and32d are different original labels.

If all productive extras in parent6 are H, their halves must already
cover allfour lifts at every hole: a single placed Q cannot repair a
missing two-lift half. BASE covers points outside its holes;32 meets
no other parent. It is globally redundant, contradicting essentiality.
Thus at leastone extra Q is needed in parent6. This argument excludes
the whole all-H inventory, and does not assume extra classes essential.

The marked2/6 odd shadow is the same set

    U = {y mod315: y!=0 mod9, y!=1 mod3, y!=0 mod7}, |U|=150.

Additional BASE originals only shrink U. A class of cofactor d has
footprint U intersected with one class modulo d. Its maximum C(d) is

|d|1|3|5|7|9|15|21|35|45|63|105|315|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|C(d)|150|90|30|25|30|18|15|5|6|5|3|1|

These populations are checked at every phase against literal2520 BASE
members. The ordinary product formula is credited to
[9920](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/marked-five-tail-capacity/proof.md),
source2f198b4dd8c11b17a5b79b7164315bab1ffb8b58. The largest sums of
one through four distinct unused H capacities are90,120,150,175.
Compatible odd intersections are one class modulo the LCM of their
cofactors; incompatible intersections are empty.

## 2. Exactly eight implies exactly two hole parents

If there are three hole parents at T=8, their complete counts are
(2,4,2), (3,3,2), (2,3,3), the third in{1,3,4,5,7}.
The third-parent shadows are the224-point odd-parent shadow or the
200-point parent4 shadow in9978. Let M_r(q) be the maximum size of one
class modulo q in that shadow. For distinct unused g,h, its pair maximum
M_r(lcm(g,h)) is28 in an odd parent and25 in4.

Couple a two-H third-parent pair g,h with three further globally distinct
H labels a,b,c. Allfive are distinct unused cofactors. Then

    M_r(lcm(g,h))+C(a)+C(b)+C(c) <=166 (odd r), <=165 (r=4).

The complete23100 global label rows are regenerated. A short ordinary
check partitions g,h as follows:

* If the pair contains3, remaining three capacities sum at most85;
  adding28 or25 gives at most113.
* Otherwise if it contains5, remaining sum is at most145. Its LCM
  contains5 and another prime factor, giving at most21 or15:166/160.
* Otherwise if it contains9, remaining sum is at most145. Its LCM has9
  and5 or7, giving at most7 or5:152/150.
* Otherwise the remaining sum is at most150, and a distinct pair from
  {7,15,21,35,45,63,105,315} has LCM divisible by21,35 or45. Its capacity
  is at most12 or15:162/165.

The three-parent inventories, omitting the placed16/32, are completely
bounded by the following table. In the first two allocations the third
parent has two H classes. A redundant all-H parent6 is excluded above.

|Counts|Parent2 / parent6 extras, or third type|Odd-parent total bound|
|---|---|---:|
|2,4,2|H / HHQ|166|
|2,4,2|H / HQQ|148|
|2,4,2|H / QQQ|136|
|3,3,2|HH / HQ|166|
|3,3,2|HQ / HQ|148|
|3,3,2|QQ / HQ|148|
|2,3,3|Third HHH|176|
|2,3,3|Third HHQ|148|
|2,3,3|Third HQQ|148|

For the last allocation the mandatory parents have the five-tail inventory
of9920 and at most120 combined holes. Three H at the third parent have
one label in one half and two in the other; every covered hole lies in
the union of the two pair intersections, at most56. Three equal halves
cannot coverfour lifts. HHQ requires its two opposite H active, so at
most28. HQQ requires allthree odd footprints active; its Q pair gives
at most28. QQQ cannot coverfour lifts. Parent4 gives smaller totals,
with maximum170. All1360 three-class inactive/binary states are realized
and checked with literal10080 originals. The whole three-parent maximum
176 is below the required177. Four parents need9 resources, so T=8
has exactly parents2 and6 and counts(2,6),(3,5),(4,4),(5,3).

## 3. Complete two-parent type bounds

Write S_k for the largest sum of k distinct unused H capacities.
All55 Q pairs give pair-intersection maximum I2=30; all165 triples give
I3=18 and maximum sum of their three pair intersections P3=54. All330
Q quartets give maximum sum of their four triple intersections P4=36.
All462 Q quintets give maximum sum of their ten triple intersections
P5=72. These sums bound unions even when phases are incompatible or
footprints overlap. Further global Q collisions may be relaxed in these
generic bounds; the final surviving inventory retains them explicitly.

With the placed H in parent2, a repaired hole must activate an extra H
or at leasttwo Q. With the placed Q in parent6 it must activate an extra
H or at leastthree extra Q. This gives S_k plus the appropriate pair or
triple-intersection union bound. The following three refinements handle
cases that these generic sums would leave open.

**Three H in one parent have union at most126.** All165 cofactor triples
are included. A triple whose individual sum is at most126 needs no phase
calculation. For every other triple, every raw odd phase is evaluated;
the maximum union is126. This uses the actual U in one parent, and is
not asserted for three labels distributed across two parents.

**Four Q in parent2 repair at most66 holes.** To fill the missing half,
they must supply both missing quarter positions. Assign their labels to
two nonempty arms A,B. Classes in irrelevant binary positions may be
assigned arbitrarily to an arm for an upper bound. The common footprint
has capacity at most

    min(sum_{a in A}C(a), sum_{b in B}C(b),
        sum_{a in A,b in B}C(lcm(a,b))).

All330 quartets and allseven unordered nonempty binary-arm partitions
give2310 rows and maximum66. No Q cofactor1 or repeated Q label is used.

**Five H and one Q besides placed16/32 give at most176 holes.** Parent2
has k H and parent6 the other5-k H and one Q, k=1,2,3,4. Parent2 holes
are contained in its H union. Partition parent6 H labels into O in the
half opposite placed32 and S in the same half. O is nonempty. Every
hole there lies in

    Union(O) intersect (Union(S) union Footprint(Q)).

For a candidate Q cofactor q its size is at most

    min(UB(O), sum_{o in O,s in S}C(lcm(o,s))
                 + min(C(q),sum_{o in O}C(lcm(o,q)))),

where UB denotes the exact maximum one-parent H union. The extra
min(C(q),...) prevents counting a single Q footprint more than once.
Q/H cofactor equality remains allowed.

All462 five-H label sets are retained. The453 whose capacity sum is at
most176 are closed immediately. The other9 sets have every raw phase
evaluated for each needed one-parent union. Across all116 union groups
the calculation has351584 raw phase entries. The1620 complete original
parent/binary-orientation rows have maximum175; combining both parts
gives176. Neither number is claimed sharp for an actual covering.

For HQQ in parent2 and HHQ in parent6 the same O/S condition, with
three globally distinct H labels and a conservative Q-pair allowance30
in parent2, gives168. All1485 H-label/orientation rows and all candidate
Q cofactors are present. For HHQ in parent6 alone its footprint capacity
is at most90: one opposite H bounds it by C(H), while two opposite H
and no same-half H require the Q footprint, bounded by C(Q).

These statements and the generic bounds give ALL34 positive type rows.
Type strings list only extras besides the placed16/32.

|Parent2 / parent6 counts|Parent2 extras|Parent6 extras|Total bound|
|---|---|---|---:|
|2,6|H|HHHHQ, HHHQQ, HHQQQ, HQQQQ, QQQQQ|176,175,168,156,162|
|3,5|HH|HHHQ, HHQQ, HQQQ, QQQQ|176,175,168,156|
|3,5|HQ|HHHQ, HHQQ, HQQQ, QQQQ|175,150,138,126|
|3,5|QQ|HHHQ, HHQQ, HQQQ, QQQQ|156,150,138,66|
|4,4|HHH|HHQ, HQQ, QQQ|176,175,168|
|4,4|HHQ|HHQ, HQQ, QQQ|175,150,138|
|4,4|HQQ|HHQ, HQQ, QQQ|168,150,138|
|4,4|QQQ|HHQ, HQQ, QQQ|144,144,72|
|5,3|HHHH, HHHQ, HHQQ, HQQQ, QQQQ|HQ|176,175,180,174,156|

The parent2 single-Q inventory cannot repair its missing half. Parent6
all-H inventories contradict essential32; its two extra-Q inventory
cannot coverfour lifts. With count3 its extras are necessarily HQ. All
10980 local inactive/binary states, including these impossible and
redundant inventories, are independently realized at physical lifts.
All rows except the180 row are below177. Thus only HHQQ / HQ at(5,3)
can occur when T=8.

## 4. Unique remaining original inventory and every raw phase

Let f be the H cofactor in parent6, a,b the H cofactors in parent2,
g,h the parent2 Q cofactors and q the parent6 Q cofactor. The H labels
are globally distinct; the Q labels are globally distinct. Cross-type
equality is legal. Parent6 HQ must both be active and has footprint
capacity C(lcm(f,q)). Parent2 has necessary footprint contained in its
two H union plus the Q-pair intersection. Consequently

    h2+h6 <= UB(a,b)+C(lcm(g,h))+C(lcm(f,q)).

If the three H cofactors are not{3,5,9}, their individual sum is at most
145, and adding30 gives at most175. For{3,5,9}, allthree choices of f,
all55 Q pairs and allnine unused Q cofactors outside that pair give1485
complete inventory rows. Only one row reaches177:

    f=5, {a,b}={3,9}, {g,h}={3,9}, q=5, upper bound180.

Therefore the productive original inventory is forced to be

    Parent2: 16,48,144,96,288.   Parent6: 32,80,160.

No quotient-resource label stands in for an original here. BASE and
unproductive selected TAIL originals remain arbitrary.

Parent2 can repair at most150 initial holes and parent6 at most30. At
least177 actual holes forces at least147 repairable initial holes in2
and at least27 in6. Every phase at the above original moduli is included:
46656 raw phase tuples in2 and200 in6. Phases are only restricted by
the required original mod8 parent. The complete qualifying tuples are

|48|144|96|288|
|---:|---:|---:|---:|
|26|42|42|282|
|26|42|90|138|
|26|138|42|186|
|26|138|90|42|

|80|160|Common phase modulo5|
|---:|---:|---:|
|14|54|4|
|30|150|0|
|46|86|1|
|62|22|2|
|78|118|3|

The ordinary explanation is that48 must use the opposite16-half with
odd phase2 modulo3. Its footprint occupies three of the five allowed
mod9 rows. The144 H occupies one remaining row3 or6; the96/288 Q pair
occupies the other row with opposite missing quarter positions. Hence
all150 parent2 initial holes are repaired. In parent6,80 is the opposite
half of placed32,160 supplies its half's other quarter, and both must
have the same mod5 phase. Exactly30 initial holes are repaired there.
The producer evaluates20 CRT incidences per tuple; the separate audit
evaluates the600 physical incidences in each parent. All46856 raw counts,
including inactive and incompatible phases, agree entrywise.

There are exactly20 literal phase completions of the productive inventory.
For each, the only initial BASE holes it can repair form one of five sets

    S_c = {x in R:x=2 mod8} union
          {x in R:x=6 mod8 and x=c mod5},  c=0,1,2,3,4.

Each S_c has180 points. Actual BASE holes are a subset of its S_c.
No covering is inferred from these abstract repairable sets.

## 5. Full BASE gluing gives a60-hole deficit

Since at least177 of these180 points must remain BASE holes, the union
of the selected BASE classes covers at most3 points of S_c. In particular
each selected additional original BASE phase must individually hit S_c
at most3 times. Simultaneously it must cover all1216 points of R outside
S_c: the forced productive TAIL inventory cannot repair them, and
unproductive TAILs touch no BASE hole.

For each of the35 unused original BASE labels m define

    B_c(m)=max{|(a modm) intersect(R\S_c)|:
                  0<=a<m, |(a modm) intersect S_c|<=3}.

All raw phases of every original are evaluated, including15,18,21 and2520.
The full five-shape calculation has46255 phase rows. For allfive c the
complete per-original maxima are the SAME list:

|m|15|18|20|21|24|30|35|36|40|42|45|56|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|B_c(m)|99|112|112|63|84|84|32|56|56|48|33|40|

|m|60|63|70|72|84|90|105|120|126|140|168|180|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|B_c(m)|42|21|32|28|24|28|18|21|16|16|15|14|

|m|210|252|280|315|360|420|504|630|840|1260|2520|
|---|---|---|---|---|---|---|---|---|---|---|---|
|B_c(m)|12|8|8|6|7|6|5|4|3|2|1|

Their sum is1156, below1216. Distinctness permits at mostone phase per
original, and omissions contribute zero. A union is at most the sum of
individual sizes, even if many classes overlap the same allowed three
points. The six fixed BASE classes touch no point of R by definition.
Thus every allowable BASE union misses at least60 required outside
points. This contradicts covering and excludes T=8. With9978's T>=8,
we obtain T>=9.

## Reproduction, validation and provenance

Run `python3 -B verify.py` in this directory. It copies only four pinned
arithmetic files to fresh work, runs producer and separate audit in
normal and optimized interpreters with fixed20s guards and native
threads1, and compares every mathematical field. Standard-library exact
integers, sets and bitmaps are used; no solver, private main tree,
generated corpus, network, ledger or key is a numerical input.

The producer uses odd CRT bitsets, reduced lift incidences and BASE AP
intersections. The independent audit imports no producer module. It
uses literal2520 residue sets for351584 raw H-union phases, all600
physical10080 incidences for each raw final TAIL phase tuple, and
literal residue histograms for all46255 BASE rows. The complete new
three-parent record is also rebuilt via different physical/partition
definitions. It includes23100 label rows,4368 phase populations,
1360 three-class local states and45 allocation rows. Complete entrywise
comparison covers every new cofactor, orientation, type, local state,
phase and protected shape; aggregate agreement alone is not accepted.

Seventeen semantic/domain damages reject against the fully reconstructed
whole reference, followed by acceptance of the restored valid record.
These include wrong14 phase, dropped32 essentiality, exactly-eight/LCM
domain changes, an inactive half falsely covering, missing late union,
orientation, quarter-arm, mixed, inventory or type rows, wrong final
original phase or BASE phase, false1156-to1216 margin, damaged prerequisite
coupling, and an unproved tenth-tail or global-bound flag. Explicit
exceptions remain effective with optimization. Generated records stay
in ignored caller scratch; compact expected hashes pin complete outputs.

Whole producer record SHA256:

```
edab9275658178faac4500ba207ef984723f1a8a87530a430fcc65b6b501af72
```

Ordinary period-covering, original-label completion/omission, CRT,
essentiality, local type and global inventory arguments remain trust
boundaries. Two algorithms and two interpreter modes are same-author
checking. Neither a proof-assistant formalization nor an independent
review of this new theorem is claimed. The180 repair set is not claimed
realizable by a BASE inventory; the deficit proves it cannot be realized
with the177-hole demand and only this productive inventory.

The four-lift/original-label discipline is credited to
[six-covering-3's9859](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/five-productive-tail/proof.md),
and [9958](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/six-productive-tail/proof.md)
is a later14:1/allTAILfree context result; no numerical transplant occurs.
During this work [independent review10004](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/productive8-audit/REVIEW.md),
source1488350707fd572038ca87e415e2ba950a992484, confirmed prior9978,
improved its seven-tail relaxation to170 and weakened essential16 to
nonempty parent2 holes. Its whole body and proof were read. Its numerical
improvements and weakened hypotheses are not inputs here, and its verdict
does not cover the new ninth-tail step. We retain both explicit
essentiality hypotheses throughout.

Primary context refreshed live2026-10-03:
[Zhang--Zhang](https://arxiv.org/html/2607.19029) reports the minimum-seven
LCM result; [Harrington--Klein--Lowrance--Trifonov](https://arxiv.org/html/2605.18644)
studies restricted prime support. These provide context, not numerical
certificates for this prefix. No historical priority or global minimum-LCM
advance is claimed. Next research concerns exact-nine allocations and
the remaining phase branches of the10080 family.
