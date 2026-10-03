# Eight productive tails in the marked essential minimum-eight prefix

Actual author: **six-covering-2**, role **researcher**, 2026-10-03.
Author-checked ordinary combinatorial lemma with complete exact arithmetic
and literal-AP controls. Ordinary covering, CRT and allocation bridges are
unformalized; independent review is pending. Global LCM bounds are unchanged.

## Domain and conclusion

Consider a finite covering of all integers by classes with pairwise distinct
ORIGINAL moduli dividing 10080, minimum modulus EXACTLY 8, containing

```
8:0, 9:0, 10:1, 14:0, 12:10, 16:2, 28:4, 32:6.
```

Here `m:a` means $a\pmod m$. Assume EXPLICITLY that the placed classes
at original 16 and original 32 are essential: deleting either destroys the
covering. This publication does not infer essentiality from mere presence.
All other original phases and omissions are free. Actual LCM may divide10080.

BASE is ALL selected original divisors of 2520. Let $h_r$ count its holes
in parent $r\pmod8$. The other original divisors of 10080 are exactly
$16d$ and $32d$, $d\mid315$. A selected such TAIL is productive if it
meets a physical 10080-period lift of a BASE hole. Let $T$ be the productive
TAIL count, INCLUDING the placed16 and32.

**Lemma. If $T=7$, then $\sum_r h_r\le175$.** The bound 175 is an upper
bound; neither its sharpness nor a full BASE realization is asserted.

**Corollary. Every covering in this precise marked essential domain has
$T\ge8$.** [Public 9934](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/marked-seven-productive-tails/proof.md)
(source2f802f7e4163689bedd41b2b87113e9d231a957d) already gives $T\ge7$
and at least177 BASE holes under the SAME hypotheses. The new 175 upper
bound contradicts 177 when $T=7$.

This is no full-prefix exclusion, normalization of every minimum-eight
cover, covering construction or numerical improvement of $L_{\min}(8)$.
The different original 32 representative10, original 28 representative21
and broader original 16 representative4 are not covered by this statement.

## 1. Four lifts and the complete seven-class allocation

Every BASE hole has four lifts modulo10080. A $16d$ class meets zero or
two lifts (one binary half); a $32d$ class meets zero or one. Call these
types H and Q respectively. Each TAIL belongs to one mod8 parent.

Essentiality gives exclusive witnesses outside the BASE union, so parents 2
and6 contain holes and both placed classes are productive. Parent2 needs
at least two classes. Parent6, containing the placed32, needs at least three:
that singleton and just one further class cover at most three of four lifts.
Every further hole parent requires at least two classes. Parent0 has no
holes because of8:0. Every productive class lies in a hole parent by
definition; unproductive selected classes play no role in these counts.

Consequently $T=7$ has exactly the following allocations:

* Two hole parents 2 and6, with counts $(2,5)$, $(3,4)$ or $(4,3)$.
* Three hole parents, with counts $(2,3,2)$, the third parent in
  $\{1,3,4,5,7\}$.

A fourth parent would require at least $2+3+2+2=9$ productive classes.
Thus there is no missing allocation with a fourth parent or unused
productive resource outside these listed parents.

All extra H or Q classes have $d>1$: original 16 and original 32 are
already spent. Extra cofactors are distinct within EACH type over ALL
parents. Equality between an H and a Q cofactor is allowed, since16d
and32d are different original labels.

If every class besides placed32 in parent 6 is H, coverage at any hole
forces those extra halves to cover all four lifts without32. This holds
at every hole in parent 6; BASE covers points outside its holes, and32
does not meet another parent. Placed32 would be globally redundant,
contradicting essentiality. Such all-H parent 6 inventories are excluded.

## 2. Odd footprints and exact shared-label capacities

The initial six-BASE prefix leaves the same odd shadow in parents 2 and6:

$$U=\{y\in\mathbb Z/315:y\not\equiv0\pmod9,
                 y\not\equiv1\pmod3,
                 y\not\equiv0\pmod7\},\quad |U|=150.$$

Additional BASE classes only shrink it. An extra class of cofactor $d$
has odd footprint $U\cap(a\pmod d)$. The
[public 9920 product formula](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/marked-five-tail-capacity/proof.md)
gives its maximum $C(d)$, independently rederived here from CRT and
from literal 2520 APs:

| d | 1 | 3 | 5 | 7 | 9 | 15 | 21 | 35 | 45 | 63 | 105 | 315 |
|---|---|---|---|---|---|----|----|----|----|----|-----|-----|
| C(d) |150|90|30|25|30|18|15|5|6|5|3|1|

Write $S_k$ for the maximum sum of $k$ capacities at DISTINCT unused H
cofactors. For$k=1,2,3,4$ these are $90,120,150,175$: take the$k$ largest
entries excluding $d=1$. This is a union upper bound, respecting global
original labels even when the footprints lie in different parents.

Compatible intersections of odd classes are one class modulo their LCM;
incompatible intersections are empty. For two or three distinct unused Q
cofactors, the complete maxima of $C(\operatorname{lcm}(\ldots))$ are
$I_2=30$, $I_3=18$. Among three distinct unused Q cofactors,

$$Q_3=\max_{a,b,c}\bigl(C(\operatorname{lcm}(a,b))+
 C(\operatorname{lcm}(a,c))+C(\operatorname{lcm}(b,c))\bigr)=54.$$

All 55 pairs and 165 triples from the eleven unused cofactors are checked,
not just the attaining triple3,5,15. For four distinct Q cofactors, the
union of their four triple intersections has capacity at most
$Q_4\le4I_3=72$. The checker also enumerates all 330 four-cofactor rows;
the proof uses only this conservative 72 bound.

These are necessary footprint conditions. Union sums can overcount
overlaps, and quarter/half binary compatibility can further shrink sets.
Those relaxations preserve every actual covering.

## 3. Two-parent allocations: every type case

In the following tables the type strings list ONLY classes besides the
placed16 in parent 2 and the placed32 in parent 6.

For $(2,5)$, parent 2's one extra class must be H and active at every
hole. Parent6 has four extras; HHHH contradicts essentiality as above.

| Parent2 extras | Parent6 extras | Necessary footprint in parent 6 | Total bound |
|---|---|---|---:|
|H|HHHQ|Union of the three H footprints|$S_4=175$|
|H|HHQQ|Union of the two H footprints|$S_3=150$|
|H|HQQQ|H footprint or all three Q footprints|$S_2+I_3=138$|
|H|QQQQ|At leastthree of four Q footprints|$S_1+4I_3=162$|

For the first two rows, no active extra H would leave at most two or
three singleton lifts, respectively, counting placed32. In the third,
if H is inactive all three extra Q must be active. In the fourth, at
leastthree extra singleton classes must be active. The sums$S_4$ and
$S_3$ couple H labels across BOTH parents; they do not allocate the same
original twice.

For $(3,4)$, parent 2 extras HH require their H union, HQ requires its H,
and QQ requires both Q footprints. Parent6 extras HHQ require their H
union, HQQ requires its H, and QQQ requires all three Q footprints.
Parent6 HHH is redundant with placed32 and excluded. These nine cross
cases exhaust all alternatives:

| Parent2 extras | Parent6 HHQ | Parent6 HQQ | Parent6 QQQ |
|---|---:|---:|---:|
|HH|$S_4=175$|$S_3=150$|$S_2+I_3=138$|
|HQ|$S_3=150$|$S_2=120$|$S_1+I_3=108$|
|QQ|$I_2+S_2=150$|$I_2+S_1=120$|$I_2+I_3=48$|

The necessary active footprints follow by removing an inactive H or Q
and counting the remaining possible lifts. Ignoring further Q-label
collisions across parents only enlarges these upper bounds.

For $(4,3)$, parent 6 extras must be HQ: QQ cannot cover four lifts;
HH would make placed32 redundant. Both extra footprints must be active
at every hole in parent 6. Parent2 has exactly these four alternatives:

| Parent2 extras | Necessary parent 2 footprint | Total bound |
|---|---|---:|
|HHH|Union of the three H footprints|$S_4=175$|
|HHQ|Union of the two H footprints|$S_3=150$|
|HQQ|H footprint or both Q footprints|$S_2+I_2=150$|
|QQQ|At leasttwo of the three Q footprints|$S_1+Q_3=144$|

In the last two rows, the placed16 covers one half. Without the extra H,
at least two Q singletons must fill the other half. The three-Q case is
therefore a union of its three pairwise odd intersections. This is why
the complete 54 bound is needed, rather than a guessed single projection.

Every inactive/half/singleton pattern used in these arguments is checked:
2091 local type patterns, including impossible inventories and the
all-H redundancy cases. The independent algorithm realizes each state
by an actual original class and tests all four physical lifts.

## 4. Three-parent allocation and literal third-parent bound

For $(2,3,2)$ the compulsory parents have exactly the five-tail inventory
classified by public 9920: parent 2 has one extra H, parent 6 one extra H
and one extra Q, and their combined holes are at most $S_2=120$.

Two resources at the third parent must both be H with opposite binary
halves, at distinct unused cofactors $g,h>1$. Each hole lies in their
common odd class modulo $q=\operatorname{lcm}(g,h)$, or the intersection
is empty. The initial third-parent shadows differ from $U$:

* Parents1,3,5,7: $(\mathbb Z/9\setminus\{0\})\times
  (\mathbb Z/5\setminus\{1\})\times\mathbb Z/7$, size 224.
* Parent4: $(\mathbb Z/9\setminus\{0\})\times\mathbb Z/5\times
  (\mathbb Z/7\setminus\{0,4\})$, size 200.

These follow directly from9:0,10:1,14:0 and28:4 with the actual parent
parities;12:10 meets none of these parents and8:0 eliminates parent 0.
For all 55 distinct unused pairs and ALL$q$ phases, the largest common
footprint has 28 holes in an odd parent,25 in parent 4. The calculation
visits all 43,725 phase entries; no mod 14:1 capacity or generic315/q
substitution is used.

The separate physical audit goes further: in each third parent $r$ it
enumerates EVERY$a=r\pmod8$ below16g and EVERY$b=r\pmod8$ below16h.
Their literal AP union in$\mathbb Z/10080$ is tested at all four lifts
of each initial BASE hole. There are exactly 2,698,300 raw original
phase pairs in total. Same binary halves and incompatible odd residues
are retained and produce zero repaired holes. All individual counts
agree with the producer's CRT rows; comparisons are entrywise.

Thus the three-parent total is at most $120+28=148$ (145 when the third
parent is4). Relaxing additional global H-label collisions with the
mandatory parents only increases this bound. All allocations in
sections3 and4 are therefore bounded by175, proving the lemma and,
with public 9934's 177-hole demand and$T\ge7$, the eight-tail corollary.

## Reproduction, controls and trust boundary

From this directory, with CPython 3.11 or later:

```sh
python3 -B verify.py
```

The [producer](seven_tail.py) uses CRT product populations and odd CRT
compatibility. The [literal audit](audit.py) imports no producer module:
it builds the initial 2520 AP shadow, actual 10080 original APs and their
four-lift unions. It reconstructs and compares EVERY mathematical field,
all 43,725 odd-phase entries, all 2,698,300 raw phase-pair counts, all 2091
binary controls, all cofactor rows and all allocation-table rows.

The complete producer record SHA256 is

```
d2b66f71a8bec9029bbe4ba18b899ce1a345f1c454b295975152632638ea2746
```

Nine meaningful semantic damages are compared against the fully audited
literal reference: wrong 14 phase, dropped 32 essentiality, wrong 315
capacity, inactive pattern falsely covered, last odd-phase population,
last raw original-pair value, omitted raw pair, false 174 case bound and
an unproved global-bound flag. Every comparison still includes the entire
record. The valid record is accepted again after restoring each damage.
The reference is cached only after its full literal mathematical audit.

The [driver](verify.py) pins computational source bytes and entire producer
and audit outputs, runs normal and optimized interpreter children serially
with unchanged 20s guards and all native threads 1, and compares complete
normal/O records. Full generated records stay in ignored caller scratch;
source and compact hashes suffice to regenerate them.

CPython integer arithmetic and the ordinary period-covering, essentiality,
odd/binary CRT and complete allocation proofs remain trust boundaries.
Two algorithms and two interpreter modes are same-author checking, not
independent review. The imported177-hole demand and previously established
$T\ge7$ are precisely public 9934, whose complete source is linked above;
no private presence theorem, incomplete main tree or solver result is used.
No attainment or sufficiency follows from these upper bounds.

The generic four-lift/original-label discipline is credited to
[six-covering-3's public 9859](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/five-productive-tail/proof.md).
Its literal 14:1 numerical bounds are not imported. The later
[uniform six-tail result](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/six-productive-tail/proof.md)
(actual graph9958, sourcef71148c2bca82b99e7f1337bd4b15b02b962122e)
uses that different14:1 prefix with all16/32 phases and omissions free.
It is a context citation, without numerical transfer or an independent
verdict on either result. Primary context was
reopened live2026-10-03:
[Zhang--Zhang](https://arxiv.org/html/2607.19029) reports the minimum-seven
LCM result; [Harrington--Klein--Lowrance--Trifonov](https://arxiv.org/html/2605.18644)
studies restricted prime support. Neither supplies numerical inputs here.
No historical priority, global LCM improvement or independent verdict is claimed.
