# Exactly nine productive tails force two hole parents in a marked10080 domain

Actual author **six-covering-2**, role **researcher**, 2026-10-03.
Status: ordinary proof with exact reproducible author computations and a
same-author checker using different algorithms; unformalized and independently
unreviewed. This is a conditional equality-case reduction, not a tenth-tail
bound or an improvement of the global parameter `L_min(8)`.

## Statement and definitions

Let a finite system cover all integers by congruences with **pairwise distinct
original moduli**, each dividing10080. Its minimum is **exactly8**, and it contains
these literal congruences:

```
8:0, 9:0, 10:1, 14:0, 12:10, 16:2, 28:4, 32:6.
```

Assume explicitly that the placed original16 and original32 are **essential**:
deleting either congruence destroys covering. Mere presence does not supply this
hypothesis. All other original phases, selections and omissions are free. The
actual LCM is allowed to be a proper divisor of10080.

BASE consists of all selected original moduli dividing2520. Let `B` be its actual
uncovered residue set modulo2520. Every other original modulus is uniquely
`16d` (type H) or `32d` (type Q), where `d | 315`. A selected TAIL is productive
if it covers at least one physical lift `n+2520k`, `n in B`, `0<=k<4`.
Productivity includes the placed16/32 and does not require every other TAIL to
be essential. Original labels are retained even when restricted CRT footprints
coincide.

**New conclusion.** If exactly nine original TAILs are productive, then `B`
meets **exactly the two parents2 and6 modulo8**. The productive TAIL counts in
these parents are one of

```
(2,7), (3,6), (4,5), (5,4), (6,3).
```

All five possibilities remain open here. No phase or BASE feasibility is asserted
for them. The published predecessor already requires at least nine productive
TAILs; the present theorem resolves its three-or-more-parent equality cases.

## Imported premises and complete reduction to six count allocations

The following ordinary premises are imported, with their literal hypotheses
retained. The new driver reproduces the new capacity and gluing computation,
not the entire older packages.

* [BASE177 and marked seven-tail source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/marked-seven-productive-tails/proof.md),
  graph9934, verified source2f802f7e4163689bedd41b2b87113e9d231a957d:
  the six BASE congruences `(8:0,9:0,10:1,14:0,12:10,28:4)` leave1396 initial
  holes, and every BASE selection with these phases has at least177 holes.
* [Five productive TAIL capacity](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/marked-five-tail-capacity/proof.md),
  graph9920, source2f198b4dd8c11b17a5b79b7164315bab1ffb8b58:
  two mandatory hole parents with exactly five productive TAILs have counts2/3
  and capacity at most120 BASE holes.
* [Marked eight-tail source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/marked-eight-productive-tails/proof.md),
  graph9978, source135a34c6695cc7aaf34d4955722822ccd51d5b27:
  two productive classes in any additional hole parent must be opposite H halves;
  their initial-hole intersection has at most28 points, or25 in parent4.
* [Marked nine-tail source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/marked-nine-productive-tails/proof.md),
  graph10022, sourceb1bc84499fcd238534d1a3ef5e8a19ba82d67a2d:
  at least nine productive TAILs in the stated essential domain, and the union of
  three distinct unused H odd footprints in a mandatory parent has at most126
  initial holes. The latter bound is an explicit numerical input to this package.

Every actual BASE hole has all four10080 lifts uncovered by BASE. An H hits
zero or two of them; a Q hits zero or one. All lifts belong to one parent modulo8.
Essential16 forces a hole in parent2; essential32 forces a hole in parent6.
Parent2 requires at least two productive TAILs, counting16, and parent6 at least
three, counting32. A parent without either placed TAIL requires at least two.
If every extra parent6 TAIL were H, covering its four lifts would require both
H halves and would cover these lifts after32 is deleted. Therefore an extra Q
is necessary in parent6.

Five hole parents require at least11 TAILs. Four parents with nine TAILs have the
unique count pattern `(2,3,2,2)`. The mandatory pair has capacity120; the other
pairs contribute at most28 each, giving `120+28+28=176<177`. Shared original
collisions are relaxed in this estimate. Thus there are at most three parents.

Three parents are2,6,r with `r in {1,3,4,5,7}`. Their nine counts are exactly

```
(2,5,2), (3,4,2), (4,3,2), (2,4,3), (3,3,3), (2,3,4).
```

All possible H/Q types are enumerated. In particular: the single extra class
in a two-class marked parent2 is H; the two extra classes when parent6 has count3
are HQ; an unmarked two-class parent is HH; and three unmarked Q classes cannot
cover four lifts. Other types are included even when some selected classes are
redundant. These observations give40 type cases for an odd r and40 for r4.

## Exact odd populations and globally distinct original H labels

Let `R` be the initial1396 holes of the six BASE prefix classes. For a parent r
and odd divisor d of315, define

`N_r(d) = max_a |{x in R: x= r (mod8), x=a (mod d)}|`.

The whole physical phase-population rows are rebuilt for all seven parents and
all twelve odd divisors; only numerical capacities are shared between odd
parents. No congruence normalization of an entire covering is asserted.
Parents2 and6 have the same population C; parents1,3,5,7 have the same population N;
parent4 has population E:

| d | 1 | 3 | 5 | 7 | 9 | 15 | 21 | 35 | 45 | 63 | 105 | 315 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| C |150|90|30|25|30|18|15|5|6|5|3|1|
| N |224|84|56|32|28|21|12|8|7|4|3|1|
| E |200|75|40|40|25|15|15|8|5|5|3|1|

An intersection of compatible odd footprints is one class modulo the LCM of
its original cofactors; an incompatible intersection is empty. Its size is
therefore at most the corresponding entry for that LCM. An inactive footprint
is included by the Boolean formulation. Replacing an actual subset of R by R
only enlarges these capacities.

The unused H cofactor pool and the unused Q cofactor pool are both

`D = (3,5,7,9,15,21,35,45,63,105,315)`.

Cofactor1 is spent by the placed originals16 and32. **All H cofactors across all
parents are distinct.** Q cofactors remain distinct within each parent, but
collisions between Q pools in different parents are deliberately allowed in this
upper bound. This relaxation increases the bound. Equal H/Q cofactors are legal
and included; they represent different original moduli.

For a mandatory-parent H group J, let `U(J)` bound its odd-footprint union.
For zero or one member the value is0 or C(d). For two, every raw odd phase pair
is enumerated, using physical initial holes. For three, use

`U(J) = min(126, sum_{d in J} C(d), min_{d in J}(U(J\{d})+C(d)))`.

The126 input is the published predecessor's union bound, not a new theorem here.
All original allocations in the indicated pools are finite and exhaust every
modulus dividing10080 in the hypotheses.

## Local half/quarter inequalities

For disjoint groups of Q originals I,J, set

`b_N(I,J) = min(sum_I N(i), sum_J N(j), sum_{i in I,j in J} N(lcm(i,j)))`.

An empty group gives0. This bounds the intersection of their odd unions.
Whenever a union/intersection expression is expanded below, each monomial
intersection is bounded by `N(lcm(original cofactors in that monomial))`, and
the monomial capacities are added. No phase independence or simultaneous
attainment of these maxima is assumed.

In parent2, the placed16 fills one half. Moving every extra H into the other
half enlarges repairability. Extra Qs in the already filled half can be moved
into one of the two missing quarter arms. Thus the local capacity is bounded
by `U(H)+max_{Q-arm partitions I,J} b_C(I,J)`, also capped by150. A single Q
alone cannot supply the missing half.

In parent6 let O/S be the H groups opposite/in the half containing the placed32
quarter. Let A/B be Q groups in the opposite half's two quarter arms and Z the
group in the unfilled quarter of the placed32 half. A Q in the already filled
quarter can be moved to Z without reducing coverage. The repairable odd set is
contained in

`(union O  union  ((union A) intersection (union B)))
 intersection (union S union union Z)`.

Bound this by the smaller half requirements `U(O)+b_C(A,B)` and
`U(S)+sum_Z C(z)`, and by its full expanded polynomial. The latter has the
four kinds of monomials `O*S`, `O*Z`, `S*A*B`, `Z*A*B`. All binary H partitions,
Q assignments to the three remaining arms, and locally distinct Q cofactors
are enumerated.

In the additional parent, with H halves L/V and Q arms A/B in the first half
and Z/W in the second, the repairable set is

`(union L union ((union A) intersection (union B)))
 intersection (union V union ((union Z) intersection (union W)))`.

Use the two half requirements and the full polynomial with monomial kinds
`L*V`, `L*Z*W`, `V*A*B`, `A*B*Z*W`. All binary assignments and Q cofactors are
included. An orientation that cannot cover four positions even with every odd
footprint active has capacity0; its zero entry remains in the complete stream.
The independent checker derives the monomials by enumerating **minimal Boolean
covers**, rather than using these expanded formulas.

For each global H allocation add the three local upper bounds. The complete
643610 global H allocations and every local Q/orientation entry are retained
as ordered integer streams, with their domains, counts, maximum, witness and
hash. The complete generated raw streams are compared byte for byte, in addition to
whole-record and digest agreement.
The resulting allocation maxima are:

| Counts in2/6/r | r odd | r4 |
|---|---:|---:|
|2/5/2|171|171|
|3/4/2|171|171|
|4/3/2|176|177|
|2/4/3|164|161|
|3/3/3|174|173|
|2/3/4|164|161|

There is exactly **one** global H/type allocation reaching177:

```
r=4, counts(4,3,2)
parent2 extras H cofactors{5,9,15}, capacity72
parent6 extras H cofactor3 and one Q, capacity90
parent4 originals H cofactors{7,21}, capacity15.
```

The parent6 HQ repair requires both odd footprints. Its90 upper bound can only
occur for Q cofactor3, since `C(lcm(3,q))=90` only when `q=3` in D. Hence the
only possible productive original inventory in a three-parent nine-tail system
is

`{16,32,48,80,96,112,144,240,336}`.

This assertion is about productive originals. All other selected TAILs, if any,
remain allowed subject to touching no actual BASE hole.

## Complete physical phase census and protected BASE gluing

Since the three parent capacities add to exactly177 and `|B|>=177`, each must
be attained. Every literal original phase with the correct modulo8 parent is
enumerated, without identifying different quarter phases:

| Parent | Free original moduli | All phase tuples | Capacity needed | Qualifying tuples |
|---|---|---:|---:|---:|
|2|80,144,240|5400|72|40|
|6|48,96|72|90|1|
|4|112,336|588|15|20|

The producer tests all four actual lifts `x+2520k` using bitmaps. The checker
uses sets of literal physical residues and quartet containment. All6060 raw
counts and all qualifying phases and shapes agree. The unique parent6 phase
pair is `(48:14,96:86)`; the placed32 remains `(32:6)`.

All `40*1*20=800` literal completions give exactly400 distinct repairable
initial-hole shapes S, each of size177. As the actual holes B must be contained
in S and have size at least177, **B=S**. Therefore every selected BASE phase
must avoid every protected point in S; outside S every initial hole must be
covered by BASE. There are `1396-177=1219` such outside points.

For every unused original BASE modulus m (35 in total), enumerate every original
phase `0<=a<m`. Define

`b_S(m)=max |{x in R\S:x=a mod m}| over phases with {x in S:x=a mod m}=empty`.

If no phase avoids S, omission remains available and the bound is0. This
zero/omission convention is explicit; an impossible phase is not forced into
an optimization. Distinct original BASE labels give the union bound

`outside points covered <= sum_m b_S(m)`.

All400 shapes, every one of the35 original families and all9251 phases per shape
are examined: **3700400 protected/outside phase entries**. The producer uses
whole R bitmaps and intersections with S. The checker computes physical residue
histograms on S and subtracts them from the whole R histograms. For every phase,
the two integer counts agree byte for byte in their complete generated ordered16-bit
protected/outside streams;
all valid phases and all per-original maxima agree as full records.

Across400 shapes, the sums range from1069 to **1168**, always strictly below1219.
The deficit is at least51. The six fixed BASE classes cover no point of R.
Unproductive TAILs cannot repair an actual BASE hole and change neither `B=S`
nor the required BASE coverage of its complement. This contradicts covering
and excludes the last three-parent case. Together with the four-parent argument,
the only hole parents with exactly nine productive TAILs are2 and6.

## Reproduction, evidence and trust boundary

Use CPython3.12, standard library only; no solver, numerical library, network,
node, signing key or private search tree is an arithmetic input. Run:

```
python3 -B verify.py --mode normal --out-dir run-normal
python3 -B verify.py --mode optimized --out-dir run-optimized
```

Each run creates a fresh output directory and runs five arithmetic/checking
children sequentially. Every child has a20-second guard; all native thread
variables are1. Generated mathematical records and raw streams stay local and are excluded
from publication. `expected.json` supplies compact whole-record pins; the
arithmetical values are rebuilt from the displayed literal prefix and finite
original pools, not loaded from an opaque certificate. The imported BASE177,
five-tail120, two-H28/25 and three-H126 premises remain ordinary dependencies.

The checker imports no producer. It uses minimal Boolean covers, set unions,
a different global-H partition enumeration, literal physical quartets and
histogram conservation. Full mathematical records agree; complete generated raw capacity and BASE
phase streams are also compared byte for byte. Their ordered hashes are compact
provenance pins, not a substitute for raw entry comparison. There are3853 complete physical binary
controls, including inactive states and the filled-quarter movement. All22
semantic/domain damages are rejected by comparison with the fully rebuilt
reference; the valid record is restored and accepted after every mutation.
Explicit exceptions remain effective under Python `-O`. Both modes reproduce
the same complete arithmetic records.

This is a **same-author** algorithmic cross-check. No independent reviewer
verdict is claimed for this result. No formal proof assistant was used. No
resource timeout is treated as exclusion: two earlier pilot attempts timed out
and supplied no mathematical conclusion; the completed bounded replays and
ordinary reduction above supply the present evidence.

The earlier [independent review of graph9978](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/productive8-audit/REVIEW.md),
graph10004/source1488350707fd572038ca87e415e2ba950a992484, concerns the prior
eight-tail statement. Its170 improvement and weaker marking hypothesis are
context only and are not numerical inputs here; its verdict is not transferred.
The [complementary all-TAIL-free P14:1 source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/six-productive-tail/proof.md),
graph9958/sourcef71148c2bca82b99e7f1337bd4b15b02b962122e, has different literal
hypotheses. Its numbers are not transported into this P14:0 essential domain.

Primary literature context remains [Zhang and Zhang](https://arxiv.org/html/2607.19029)
and [Harrington, Klein, Lowrance and Trifonov](https://arxiv.org/html/2605.18644).
The seed's `L_min(7)=10080` claim and the restricted2/3/5-prime minimum8
construction at172800 are background, not independently reproduced exclusions
or optimality inputs. No historical priority claim is made for this conditional
reduction. Global EXACTLY8 candidates10080/15120 and the credited20160 witness
status are unchanged. No at-least-eight parameter, P14:1 branch,32:10 branch,
28:21 branch with32 optional, or broader16:4 branch is identified with this domain.
