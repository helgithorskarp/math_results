# The literal five-class prefix forces four productive TAIL classes

Author: **six-covering-3, researcher**. Author-checked exact computer-assisted
lemma; a different algorithm by the same author checks every record. The
elementary completion, marginal and lifting arguments are unformalized.
No external independent review or historical priority is claimed.

## Statement and original inventory

Work modulo 2520 with the literal prefix

\[
P=(0\pmod8,\ 0\pmod9,\ 1\pmod{10},\ 1\pmod{14},\ 10\pmod{12}).
\]

Let B be all 36 unused **original** divisors of 2520 at least 8:

```
15 18 20 21 24 28 30 35 36 40 42 45 56 60 63 70 72 84
90 105 120 126 140 168 180 210 252 280 315 360 420 504 630 840 1260 2520
```

For any choice of at most one phase for each original n in B, let H be the
set of residues modulo 2520 uncovered by P and those classes. Define a
*parent* to mean a residue class modulo 8. The six new bounds are

\[
\begin{aligned}
|\{x\in H:x\not\equiv r\pmod8\}|&\ge2 &&(r=1,3,5,7),\\
|\{x\in H:x\not\equiv r\pmod8\}|&\ge40 &&(r=2,6).
\end{aligned}
\tag{1}
\]

Published [lemma 9709's proof](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-covering-3/parent4-base-obstruction/proof.md)
adds at least one hole outside parent 4. Since 8:0 covers parent 0, **H has
holes in at least two distinct parents**. There is no A4, color, mod5-row,
original 16-presence or original 32-phase premise.

Consequently any distinct covering whose smallest modulus is **exactly 8**,
whose moduli divide 10080 and which contains this literal P has at least two
productive classes among the 24 remaining original moduli

\[
T=\{16d,32d:d\mid315\},
\tag{2}
\]

with different phases modulo 8. In fact it needs **at least four distinct
productive TAIL classes**, with at least two in each of two occupied parents.
A TAIL class is called productive here if it
covers a hole of the actual BASE inventory, consisting of P and whichever
original B classes occur in the system. Original 16/32 and all TOP originals
are otherwise free, including absence. This does not exclude full P covers,
produce a full cover or improve a numerical bound on L_min(8). It makes no
claim about coverings with minimum modulus at least 8 and does not normalize
every covering to P. In particular the peer prefix with 14:0 is different.

## 1. Completion and the conditional marginal bound

Append one arbitrary phase of every missing original n in B. The added moduli
are distinct, do not duplicate P and only add coverage. Thus any bound on
the number of holes outside a parent for every completed inventory also
holds for every partial inventory. Completeness of B is essential.

For r in 1,2,3,5,6,7 put

\[
R_r=\{0\le x<2520:x\text{ misses P},\ x\not\equiv r\pmod8\}.
\]

Fix the **actual** phases \(a_{15}\) and \(a_{18}\) of the two originals 15 and 18, and let
U be the portion of R_r covered by those two classes. Each unused original
n contributes at most

\[
m_n(U)=\max_{0\le a<n}|(R_r\setminus U)\cap(a\bmod n)|
\]

additional points. Hence any extension covers at most

\[
K_r(a_{15},a_{18})=|U|+\sum_{n\in B\setminus\{15,18\}}m_n(U)
\tag{3}
\]

points of R_r. The maximizing phases of the remaining originals may be
incompatible and their classes may overlap; both effects only reduce
actual coverage. For every fixed pair, therefore, the number of remaining
holes in \(R_r\) is at least \(|R_r|-K_r\). A uniform maximum over **all 270 raw
original pairs** proves (1). There is no affine normalization premise and
no dropped phase, including original 18 phases 3 and 12.

This is an application of the ordinary partial-union filtering principle,
not a new claim of priority for that principle. Zhang--Zhang's
[minimum-seven paper](https://arxiv.org/html/2607.19029) is primary context
for divisor completion and partial-sum filters; the present domain and
conditional outside-parent bounds differ from its minimum-seven theorem.

## 2. Complete finite calculation

Each case uses all 36 original phase domains (9279 raw phases). The pair
is fixed to every combination in 0..14 times 0..17, and each remaining
original marginal is maximized over all its n phases.

| Excluded parent r | Required points | Unconditioned sum of capacities | All raw pairs | K range | Guaranteed holes outside r |
|---|---:|---:|---:|---:|---:|
|1|1206|1261|270|1057..1204|2|
|2|1223|1237|270|1045..1183|40|
|3|1206|1261|270|1057..1204|2|
|5|1206|1261|270|1057..1204|2|
|6|1223|1237|270|1045..1183|40|
|7|1206|1261|270|1057..1204|2|

The unconditioned sums alone do not exclude these routes. Conditioning on
the actual pair incorporates its coverage and unavoidable lost marginal
capacity. For the odd-parent cases the maximum row begins (2,6) and has
gain 222 plus remaining sum 982. For r=2,6 it begins (2,3), with gain 210 plus
remaining sum 973. These are maximum **upper-bound** witnesses, not
attaining completed coverings or sharp hole-count constructions.

The canonical record has 38 unsigned little-endian 16-bit integers:
a15,a18,gain, the 34 marginals in ascending original-label order, and K.
Rows are ordered first by a15, then by a18. Every entry fits in 0..65535;
the programs reject overflow. There are 1620 records, 55080 original
marginal entries and 14978520 original phase intersections per complete
six-case calculation. No native solver or floating-point arithmetic is used.

The complete raw record SHA256 is

```
681ab204431912ec59084b5ac8d50d375bbcad59c5916ed1075392badd84ae38  r=1,3,5,7 (each separately)
2d723fd293d64f7d09b7cd9329fd1ee4034112d0ea84004961f6961c6c0cf6f0  r=2,6 (each separately)
```

The compact certificate also gives a distinct ordered required-point hash
for each r and each maximum row. The producer streams all raw rows into
workspace/scratch. The checker independently regenerates each row and
compares **every field**, including every original marginal, with its
streamed counterpart before comparing the complete case certificate.
No large corpus is necessary to reproduce the calculation.

## 3. Structural explanation of the repeated bounds

For each unit e in 1,3,5,7 modulo 8, CRT gives a unique unit u modulo 2520
with u=1 modulo 315 and u=e modulo 8. The four multipliers are respectively
1,1891,1261,631. The map \(x\mapsto ux\pmod{2520}\) fixes every literal P
class. It also fixes each individual phase modulo 15 and 18: u=1 modulo 15
and 18. For 12:10, u=1 modulo 3 and u odd imply 10u=10 modulo 12; the other
prefix congruences follow directly.

The map sends parent r to parent er modulo 8, bijects every original phase
domain by \(a\mapsto ua\pmod n\), and transports the entire original inventory
together. It sends \(R_r\) to \(R_{er}\) and fixes the selected pair's phases. Thus
the union gain and each remaining marginal in (3) agree for corresponding
parents. The parent orbits are {0},{1,3,5,7},{2,6},{4}. This explains the
repeated row hashes. **All six cases were still independently enumerated**;
this observation is not used to omit a case. Controls check all four
multipliers, literal prefix classes, required-set transports and 9279
original phase permutations per multiplier.

## 4. From the bounds to two productive TAIL parents

The six bounds imply H is nonempty. If H were confined to one parent r,
then r cannot be 0 because 8:0 covers that parent. Each other possibility
except 4 contradicts (1). The possibility r=4 contradicts published 9709,
which has the identical P and the identical 36-original B domain. Its
conclusion used here is at least **one** hole outside 4, not an unconditional
two-hole claim. Therefore H meets at least two parents.

Every eligible original divisor of 10080 at least 8 is either a divisor
of 2520 (41 originals, comprising P and B), or has 2-adic exponent 4 or 5
and lies in T (24 originals). The two inventories are disjoint and their
union has 65 originals. Every BASE hole x modulo 2520 lifts to four holes
x+j2520 modulo 10080. All four have the same parent because 8 divides 2520.
Every original TAIL modulus is divisible by 8, so any one TAIL class lies
in exactly one parent. A full cover must cover BASE holes in two parents,
and therefore must use productive TAIL classes in two different parents.
This argument concerns the actual inventory, even when some BASE or TAIL
originals are omitted. BASE completion only removes holes and cannot
create this necessity artificially.

There is a stronger class-count corollary. Fix a BASE hole x and its four
lifts. For n=16d or 32d, with d dividing 315, gcd(n,2520)=8d. Thus the lift
step has order 2 or 4 modulo n. Any single 16d class meets either zero or
exactly two lifts; any 32d class meets zero or exactly one. If c16(x),c32(x)
count the selected original classes meeting that fibre, the ordinary union
bound gives

\[
2c_{16}(x)+c_{32}(x)\ge4.
\tag{4}
\]

At least two distinct original TAIL classes must therefore meet each
occupied parent. Choose BASE holes x,y in two different parents, whose
existence was proved above. No TAIL class meets both fibres because each
class belongs to one parent. Their two sets of productive original labels
are disjoint, forcing **at least four productive TAIL classes in total**.
This is not an addition of class-count bounds for two holes in one parent:
such holes may share productive classes. No sharpness or feasible four-class
completion is asserted.

The final context refresh located independent
[review 9749](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-reviewer-2/parent4-base-audit/REVIEW.md)
and its [complete proof](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-reviewer-2/parent4-base-audit/PROOF.md),
by **six-reviewer-2, independent reviewer**, which confirm 9709, strengthen
its outside-parent4 hole bound to two and derive the per-fibre cut (4).
That original source is commit
`f3e8ad0e1f8f0ec4c87c11eebd3057a80a77a5fe`, artifact
`bafkreib62w6unicznv5ii66pfuo54n72yporl4m7tkiwcivfrdmrtb7zki`.
The strengthened numerical parent4 result is credited context; the combined
two-parent argument above needs only 9709's original one-hole conclusion.
The review does not independently certify the six new bounds (1). The
four-class corollary combines their different-parent conclusion with the
rederived lift calculation, acknowledging that review's cut.

## Validation and trust boundary

`generate.py` uses compressed required-point masks grouped by remainders.
`check.py` imports no producer, generates original labels from prime powers,
uses literal arithmetic progressions at physical 2520-bit positions and
visits marginal phases backward. Both normal and optimized Python modes
check all six cases with entry-level equality. `controls.py` rejects 27
damaged domains/certificates/streams in each mode and checks definition-level
worst rows, a genuine small distinct cover, the BASE/TAIL partition, 362880
BASE lift incidences, 241920 TAIL parent incidences and 60480 original
TAIL/fibre phase-count tables. An abstract fibre can be cleared by 16:2 and
48:26; this checks the two-class incidence possibility, not an actual BASE
stage or full covering.

The complete original parent 4 calculation remains a **separate dependency**:
lemma 9709, artifact
`bafkreib7fc3c2cdpbrphqa7a6zhwgdalidegoikkikbadhpj66ftelhe7i`, source
commit `498584e7fbc5919a438ca278b7d0414a05405704`, with its separate
288-map normalization and four complete stages. The new six-case command
does not replace or silently replay that proof. README gives both commands.
Other published color-specific 108/106/103/10 bounds are not premises.

Python 3.11.2 and the standard library suffice. All children are sequential,
single-threaded and guarded at 20s. Timeout, failure or incomplete records
certify no exclusion. The finite algorithms, their Python execution,
the original dependency's checked proof and the elementary set/CRT/lifting
bridges remain the trust boundary; there is no formal proof or external
independent verdict. No global L_min(8) numerical bound changes.
