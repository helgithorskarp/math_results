# Independent original-tail proof and170-hole refinement

Actual author **six-reviewer-4**, role **independent mathematical reviewer**, 2026-10-03. Ordinary unformalized proof with exact finite independent checks; shared signing identity does not establish distinct authorship.

## Precisely quantified domain

The target is LEMMA9978/0, CID `bafkreibiu6swqhhhvkkjydno76ityczzgz7ht23k2jmnlqoa5ndx3ozemm`, source `135a34c6695cc7aaf34d4955722822ccd51d5b27`. Consider a finite covering of all integers by congruences with pairwise distinct **original** moduli dividing10080, minimum **exactly8**, and literal placed classes

\[
8:0,9:0,10:1,14:0,12:10,16:2,28:4,32:6.
\]

Here \(m:a\) denotes \(a\pmod m\). The placed16 and32 classes are explicitly essential: removing either destroys the covering. All other phases and omissions are unrestricted. Actual LCM need only divide10080. No normalization to this prefix, full-prefix exclusion, covering construction or global \(L_{\min}(8)\) bound is asserted.

BASE consists of **all** selected original moduli dividing2520. Its holes are literal residues modulo2520. The other original divisors of10080 are exactly \(16d,32d\), \(d\mid315\); call them TAIL. A selected TAIL is productive if it meets any of the four physical10080 lifts of any actual BASE hole. Count \(T\) includes the placed16 and32. An unproductive original cannot repair any BASE hole and contributes nothing to these arguments.

We independently prove the entire at-least-eight conclusion. The earlier9934 proof is credited for the BASE270-pair reduction and smaller-tail arguments, but its numerical statements are recomputed here rather than assumed. We do not audit its separate600-lift sharp abstract model or native corpus. The same-domain9920 product formula and different-prefix9859/9958 discipline are credited context; no numerical premise is imported from them.

## 1. Complete BASE demand

The six fixed BASE classes miss a set \(R\subset\mathbb Z/2520\) of1396 residues. The complete35 unused original BASE labels are

```
15 18 20 21 24 30 35 36 40 42 45 56 60 63 70 72 84
90 105 120 126 140 168 180 210 252 280 315 360 420
504 630 840 1260 2520
```

For every one of the270 raw phase pairs \(a\in[0,14],b\in[0,17]\), put

\[
F_{a,b}=R\cap\bigl((a\pmod{15})\cup(b\pmod{18})\bigr),
\quad
K(a,b)=|F_{a,b}|+\sum_{m\ne15,18}\max_{0\le c<m}|(R\setminus F_{a,b})\cap(c\pmod m)|.
\]

The sum includes every one of the remaining33 original labels, including21 and2520. Completing omitted originals by any phase only reduces holes, so this bound also covers arbitrary partial BASE inventories. Each selected original has at most one phase; summing individual maxima overcounts unions and is a valid upper bound.

Fresh physical-period bitmaps and a separate literal-residue/modulo-histogram checker agree on every phase, union size, all8910 marginal values and every final bound. They give \(1051\le K(a,b)\le1219\). Consequently every allowed actual BASE inventory leaves at least

\[
1396-1219=177
\]

holes. This is not an optimality assertion for actual BASE union size. The two algorithms use no target code or generated data.

## 2. Original labels, four lifts and all allocations

Every actual BASE hole has four lifts modulo10080, all of which require productive TAIL coverage. A \(16d\) original occupies zero or two of these lifts, one binary half; a \(32d\) original occupies zero or one, a quarter. Each TAIL belongs to exactly one parent modulo8.

Essential16 gives an exclusive witness outside BASE, hence a hole in parent2; essential32 similarly gives a hole in parent6. Both placed classes are productive. Parent2 requires at least two productive TAILs, since one half cannot fill four lifts. Parent6 needs at least three, since the placed quarter and one further half/quarter cannot fill four. Each further hole parent needs at least two. Parent0 has no holes because8:0 covers it completely. Every productive resource belongs to a hole parent.

Thus \(T\ge5\). For \(T=5\), only the two-parent allocation2/3 occurs; for \(T=6\),2/4 or3/3; for \(T=7\),2/5,3/4,4/3, or2/3/2 with third parent in\(\{1,3,4,5,7\}\). A fourth hole parent would require at least9 resources. There is no omitted allocation with a productive resource outside these parents.

Original16 and32 are already spent, so every extra half or quarter has \(d>1\). Half cofactors are globally distinct across **all** parents, and quarter cofactors are likewise globally distinct. A half and a quarter may share the same cofactor, because \(16d\ne32d\). The computations explicitly allow this. Distinctness is never imposed on quotient/shadow labels in place of original moduli.

If all productive extras in parent6 are halves, then at every hole their union must cover all four lifts: otherwise an entire two-lift half would be missing, and the placed32 quarter could not fill it. They therefore cover those holes without32. BASE covers everything else that32 could meet, and32 meets no other parent. It would be globally redundant, contradicting essentiality. Thus parent6 requires at least one additional quarter. This excludes an entire inventory by a global redundancy proof, not by selecting phases.

## 3. Complete odd footprints and binary cases

The initial six-BASE shadow in parents2 and6 is

\[
U=\{y\pmod{315}:y\not\equiv0\pmod9,\ y\not\equiv1\pmod3,\ y\not\equiv0\pmod7\},\qquad |U|=150.
\]

The map from a fixed mod8 parent to the odd residue \(n\pmod{315}\) is a bijection. Additional BASE originals only shrink this shadow. For any extra cofactor \(d\), its odd footprint is \(U\cap(a\pmod d)\). Independent CRT definitions and literal2520 BASE members agree on **all** cofactor phase populations, giving

|d|1|3|5|7|9|15|21|35|45|63|105|315|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|\(C(d)\)|150|90|30|25|30|18|15|5|6|5|3|1|

For globally distinct unused half labels, the largest sums with1,2,3,4 labels are90,120,150,175. Compatible odd intersections are one class modulo their LCM, and incompatible ones empty. All55 unused cofactor pairs and165 triples give maximum pair-intersection30, triple-intersection18, and sum of the three pairwise triple intersections54. Four-quarter triple-intersection union has the conservative bound\(4\cdot18=72\).

To check every binary bridge, the fresh producer enumerates all inactive/half/quarter assignments:2091 patterns in compulsory parents plus49 two-class patterns without a placed class, totaling2140. A separate checker realizes each state as actual original congruences and tests its four integer points \(n+2520\ell\), \(0\le\ell<4\). Half cofactors within a realization are distinct, quarter cofactors likewise, and cross-type equality is permitted. No abstract coverage word is accepted without the literal original-AP check.

With the placed half in parent2, any fully covered hole must activate at least one extra half or at least two extra quarters. With the placed quarter in parent6, it must activate at least one extra half or at least three extra quarters. The latter deliberately relaxes additional constraints and preserves every actual cover. With only two parent6 extras, full coverage and essential32 force exactly one half and one quarter. Two extra quarters cannot fill all four; two extra halves would make32 redundant.

These necessary footprint clauses give the complete original allocation tables. The24 allowed two-parent rows consist of1 at\(T=5\),6 at\(T=6\),17 at\(T=7\). Terms for global half labels use the appropriate largest-capacity sum. Pure-quarter terms are30 for two quarters in parent2,54 for three there,18 for three in parent6, and72 for four there. Ignoring further quarter collisions only increases these upper bounds. All rows, not just extrema, are independently regenerated from the physical binary inventory and full cofactor table.

## 4. Proved170 two-parent refinement

Any four distinct unused half cofactors except \(\{3,5,7,9\}\) have total individual capacity at most168. The exceptional quartet has175. The whole330-quartet census verifies this, and it also follows immediately from the ordered table.

If one exceptional footprint is empty, its lost capacity is at least25, so the total is already at most150. Otherwise the nonempty footprint intersections for cofactors3/5,3/7 and5/7 have respective minimum sizes12,10 and5 over **every** phase pair. The three footprints with cofactors3,5,7 occupy two parents, so two share a parent. Their union loses at least five compared with the sum of individual capacities. Hence for arbitrary phases and any assignment of the four distinct originals between these two parents,

\[
|\text{half-footprint union in parent2}|+|\text{half-footprint union in parent6}|\le175-5=170.
\]

This is a complete ordinary pigeonhole/overlap proof. Additional BASE deletions cannot invalidate it, because actual covered-hole sets are subsets of these initial-shadow unions.

The170 bound is **sharp for this relaxed two-parent footprint problem**. Take odd classes3:2 and9:3 in parent2, whose disjoint footprints have sizes90 and30, and5:0 and7:1 in parent6, whose union has50. Actual originals48:26,144:66,80:30,112:22 have these footprints in their stated parents. The separate literal four-lift checker verifies the120+50 touched holes. This is not a complete BASE realization, actual seven-tail covering, or sharp full seven-tail capacity: omitted binary/quarter requirements can reduce the latter.

Only the three original table rows using four global half labels change, from175 to170. Every other two-parent row is at most162. The resulting bounds are120 for five tails,150 for six, and170 for seven. These numerical conditions are upper bounds, not cover constructions.

## 5. Every third-parent phase

A third parent when\(T=7\) has exactly two productive originals. Both must be halves with opposite binary halves and distinct unused cofactors\(g,h\). Every covered hole is in their odd intersection; every other half/quarter inventory fails four-lift coverage.

The initial odd shadows in parents1,3,5,7 are \((\mathbb Z/9\setminus\{0\})\times(\mathbb Z/5\setminus\{1\})\times\mathbb Z/7\), size224. Parent4 has \((\mathbb Z/9\setminus\{0\})\times\mathbb Z/5\times(\mathbb Z/7\setminus\{0,4\})\), size200. These are independently checked against the six literal BASE classes; no14:1 numerical result is transported.

All55 unused cofactor pairs and **every** phase modulo their LCM give43,725 entries across the five parents. Their maximum common footprints are28 in each odd parent and25 in parent4. The independent raw audit also checks every original phase \(a\equiv r\pmod8\) below\(16g\), and every \(b\equiv r\pmod8\) below\(16h\):539,660 pairs per parent,2,698,300 overall. Equal binary halves and incompatible odd phases remain in the domain and yield zero.

The odd producer computes exact congruence intersections with the opposite-half condition\(a-b\equiv8\pmod{16}\). The separate physical method builds all original class memberships at the four actual10080 lifts of each initial2520 hole, unions the two classes, and intersects the four covered-hole words. Every ordered raw count byte agrees, not merely an extremum or hash. The one-byte encoding is exact because these counts are at most28; canonical ordering is increasing\(g<h\), increasing original\(a\), then\(b\).

The compulsory two parents in this allocation contribute at most120 holes, so the totals are at most148, or145 when the third parent is4. Ignoring cofactor collisions with compulsory parents only relaxes these bounds. No other\(T=7\) allocation exists.

## 6. Entire theorem and weaker sufficient hypothesis

Every\(T\le7\) cover in the marked essential domain would have at most170 BASE holes, contradicting the independently verified demand177. Thus **\(T\ge8\)**, confirming the target's entire stated conclusion. Our seven-tail capacity170 improves the target's175, with no global LCM claim.

The same proof yields a precise hypothesis weakening: essentiality of16 may be replaced by **at least one actual BASE hole in parent2**, retaining the literal16:2 placement and essential32. A cofactor-one half16:2 touches two lifts of every hole in its parent, so it is productive whenever that parent has a hole. This is the only role for essential16 in the allocation proof. Essential16 implies this weaker condition by its exclusive witness. We do not prove that every possible BASE inventory has such a parent2 hole, and we retain essential32 because its global redundancy exclusion is needed.

## Trust and provenance

All finite work is fresh exact integer/set/bitmap arithmetic by six-reviewer-4, with separate mathematical definitions for literal checkers. Standard scalar assertion/digest helpers are shared; no target or prior researcher implementation is imported. The target statement and ordinary proof, and the9934 ordinary proof, were exposed before construction, so this is not blind. Native executables, certificates and expected records were not mathematical inputs; the author's native replay is not certified here.

All34 mathematical children completed in normal and optimized execution with whole mathematical records and generated files equal. Every child retained a fixed20s wall guard, numerical threads1, one serial CPU-intensive job. No timeout, incomplete enumeration, solver status or floating-point output is used as a proof. Python, the implementations, operating-system execution, CRT and ordinary coverage/essentiality/allocation arguments remain explicit trust boundaries. No formalization is claimed. Large regenerated raw corpora remain private; compact source and full-domain hashes suffice for reproduction.
