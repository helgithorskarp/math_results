# Independent two-parent equality reduction

Actual author: **six-reviewer-2**, independent mathematical reviewer, 2026-10-03.
Complete normal/optimized cold-source reconstruction and entry comparison
passed after the justified disjoint staging below. The earlier unsplit optimized
timeout remains incomplete and is not mathematical evidence. Target executable/
fixture is unopened and excluded from the executable-code audit.
This is an ordinary, unformalized, exact computer-assisted proof. The written
argument of LEMMA10054 was exposed; this audit is **not blind**. The primary
programs do not import that author's programs, fixtures, or expected outputs.

## Precise theorem

Let a finite distinct covering system have all original moduli dividing10080,
no modulus less than8, and contain exactly these marked congruences among its
freely chosen other originals:

\[
(8,0),(9,0),(10,1),(14,0),(12,10),(16,2),(28,4),(32,6).
\]

Let BASE consist of its selected moduli dividing2520 and let \(B\) be the
actual BASE holes modulo2520. A TAIL is a selected original \(16d\) or
\(32d\), \(d\mid315\), and is productive when it meets a lift
\(n+2520k\), \(n\in B\), \(0\leq k<4\).
Assume original32 is essential and **\(B\) has a point congruent to2 modulo8**.
Assume exactly nine original TAILs are productive.

Then the actual hole parents are exactly2 and6 modulo8. Their productive
TAIL counts are one of \((2,7),(3,6),(4,5),(5,4),(6,3)\).
These are necessary alternatives, with no assertion of realizability.

This proves LEMMA10054 on its original essential16/32 domain and extends it:
essential16 is replaced by a nonempty actual parent2. Placement16:2 remains.
Essential32 remains. The existence of a parent2 hole does not assert that16
is essential. The actual LCM can be a proper divisor of10080.
All other original phases, omissions, and unproductive TAILs remain free.

## Original-label and four-lift bridges

Every modulus outside BASE has2-adic valuation4 or5, hence is uniquely16d or32d
with odd d dividing315. BASE cannot distinguish the four lifts of any hole.
An H original16d hits either zero or two physical lifts; a Q original32d hits
zero or one. Their parent is the original residue modulo8.
Equal H/Q cofactors mean different original moduli and are legal. H labels are
globally distinct, and Q labels are globally distinct in the actual system.
The capacity computation allows Q labels to repeat between parents; this is
an upper-bound relaxation. It retains distinct Q labels inside each parent.
It makes no quotient of physical original phases or whole covering systems.

The placed16 fills one half in parent2, which needs another productive original.
Essential32 gives an actual hole in parent6. Its placed quarter needs at least
two additional originals. If all its additional productive originals were H,
every covered quartet would require both H halves; deleting32 would preserve
all hole lifts, and BASE already covers all other lifts. This contradicts
essential32. Thus some additional productive Q is required in parent6.
Every additional parent needs at least two originals. With exactly two these
must be opposite H halves. The six fixed BASE classes exclude parent0.

Consequently five hole parents need at least11 originals. Four hole parents
with nine productive originals have counts(2,3,2,2). For the mandatory pair,
the single extra H cofactor f in parent2 and H cofactor g in parent6 are
distinct. The extra Q cofactor q can equal either one. The capacity is at most
\(C(f)+C(\operatorname{lcm}(g,q))\). All1210 such labelled choices give at most120.
An additional two-H parent has capacity at most28, or25 for parent4. Thus four
parents allow at most176 initial holes. BASE has at least177 actual holes.

For three parents, the additional parent r is one of1,3,4,5,7 and the count
allocations are exactly(2,5,2),(3,4,2),(4,3,2),(2,4,3),(3,3,3),(2,3,4).
The programs independently derive all40 admissible H/Q type cases for odd r
and40 for r4. Redundant additional originals are allowed. No condition that
all productive originals be essential is imposed.

## Exact capacities and remaining numerical premise

Let R be the initial holes of the six fixed BASE classes modulo2520; it has
1396 points. For r and d, let \(N_r(d)\) be the greatest size of an odd residue
class modulo d in parent r of R. Every raw phase population is reconstructed
for all seven nonzero parents and all twelve divisors of315. Capacities agree
between parents2/6 and between the four odd parents, without normalizing
the phases of a whole covering system. Indeed, the full315-phase population
vectors agree for2/6 and for all four odd parents, and every such entry is0
or1. Thus their actual odd-shadow sets are identical within each group, not
merely their singleton maxima. Reusing a mandatory pair-union bound in parent6
is justified. Equivalently the literal prefix imposes the same odd exclusions
in2/6, and the same exclusions in the four odd parents; no phase normalization
of a whole covering is made.

The unused H and Q cofactor pools are each
\(D=(3,5,7,9,15,21,35,45,63,105,315)\).
For mandatory-parent H groups, the bound U is0 for empty groups, N for one,
the maximum of all literal odd phase unions for two, and for three the minimum
of126, the sum of singleton bounds, and each pair-union bound plus the remaining
singleton bound. All134915 pair-phase entries are freshly checked with bitmap
unions and independently with physical sets.

**The126 upper bound for three distinct unused H footprints is an explicit
numerical premise from LEMMA10022, independently rebuilt in REVIEW10066.**
This pass does not claim a new independent reconstruction of that entire
earlier triple-union package. It uses no new target numerical table as a premise.
The other older bounds BASE177, five-tail120, pair28/25 are freshly rebuilt here,
with credit to9934,9920,9978 respectively.

For BASE177, all270 raw phases of originals15 and18 are examined. For every
phase pair, the union already covered plus the maxima of every other unused
original BASE phase is an upper bound on additional coverage of R. The upper
coverage maximum is1219, hence at least177 holes. Omitting an original can
only reduce this upper bound. This fresh one-program reconstruction is
corroboration of the explicit earlier bound, not a second new blind proof of it.

## Local coverage and complete global allocation census

Four abstract quarters represent the four literal lifts; the two H halves
partition those quarters. Moving an additional H in parent2 to the missing
half only increases the repairable set. Moving a Q out of an already filled
quarter to a missing quarter does the same. Parent6 retains both H orientations
and all three missing Q arms. The unmarked parent retains both H orientations
and all four Q arms. The3853 complete inactive/active binary controls verify
these movements and the all-H redundancy implication. The permutation from
abstract quarters to physical lift indices is ordinary elementary CRT reasoning;
the final phase census uses literal lifts directly and does not assume it.

The first capacity implementation generates inclusion-minimal subsets of the
actual quarter-incidence variables that cover all four positions. Each such
subset has odd intersection capacity at most \(N_r\) at the LCM of its
original cofactors. The union bound over minimal covers is combined with
separate requirements in each missing half, using U for mandatory H unions.
For Q arms I,J their intersection of unions is bounded by the smaller of
their separate population sums and the sum of their pairwise LCM capacities.
The separate implementation explicitly expands the two half requirements and
their intersection, with no import of the minimal-cover generator.

Every H allocation is traversed with globally distinct original labels. The
first code chooses the three groups from successively shrinking pools. The
second first chooses the entire H subset then every ordered split. Canonical
row ordering matches every allocation entry, not merely a maximum or digest.
There are643610 allocations. The full maxima are:

| Counts2/6/r | Odd r | r4 |
|---|---:|---:|
|2/5/2|171|171|
|3/4/2|171|171|
|4/3/2|176|177|
|2/4/3|164|161|
|3/3/3|174|173|
|2/3/4|164|161|

The only allocation attaining177 is r4, counts(4,3,2), with extras H{5,9,15}
in parent2, H{3} and one Q in parent6, and H{7,21} in parent4. Its capacities
are72,90,15. The90 parent6 capacity forces the Q cofactor3. The sole remaining
productive original inventory is thus{16,32,48,80,96,112,144,240,336}.
No claim that the maxima are simultaneously attainable was used to exclude
the smaller capacities. The final survivor is checked physically next.

## Literal phases, actual holes, and protected BASE gluing

For every original phase in the correct parent, the two codes check all four
literal lifts at every initial hole. One uses four bitmap planes; the other
forms sets of actual physical residues and tests quartet inclusion. They agree
on every phase tuple, repairable set, and qualifying phase:

| Parent | Free originals | Raw tuples | Necessary capacity | Qualifying |
|---|---|---:|---:|---:|
|2|80,144,240|5400|72|40|
|6|48,96|72|90|1|
|4|112,336|588|15|20|

The sole parent6 phases are48:14 and96:86. All800 original-phase completions
give400 distinct repairable initial-hole sets S of size177. Any actual B must
be contained in one S. BASE177 implies B=S, without assuming the initial R
itself is an actual BASE-hole set. This distinction is essential.

Every selected BASE phase must avoid S entirely. For each of35 unused original
BASE moduli and every literal phase, the codes compare its protected and outside
counts. One subtracts protected histograms from whole R histograms; the other
uses literal set intersections and differences. Every3700400 phase entry,
every valid phase list, every per-original maximum, and every full row agree.
Omission is always available and has capacity0; no avoiding phase is forced
to exist. Original labels stay distinct, so the sum of their maxima is a valid
upper bound on the union they can cover outside S.

There are1219 required outside points. The computed BASE capacity sums range
from1069 to1168. Every shape therefore has a deficit of at least51. The six
fixed BASE originals cover none of R. Unproductive TAILs meet no actual hole
lift and cannot change B=S or help cover its complement by BASE. This excludes
the last three-parent possibility, completing the theorem.

## Scope and trust

Exact standard-library Python integer arithmetic; no solver, floating point,
network input, signing key, ledger, or generated opaque corpus is a mathematical
input. Full raw products and28MB records stay local and are regenerated.
EXPECTED.json pins reviewer-generated records only after fresh reconstruction.
Both normal and optimized cold-source runs must complete every child and
whole-file comparison. The disjoint staging proof is below. A timeout, missing file, or incomplete child is no
mathematical exclusion. The ordinary period, CRT, essentiality, redundancy,
moving-footprint, union-bound, and actual-hole bridges remain unformalized.

The result excludes exactly-nine systems with three or more hole parents in
this marked domain. It does not close any of the five two-parent allocations,
force ten productive tails, exclude the full prefix, normalize arbitrary
minimum-eight coverings to these marks, or improve global L_min(8).

## Bounded partition completeness

The twelve capacity partitions are the Cartesian product of r in{1,4} and the
six displayed parent-count allocations. A global labelled allocation has exactly
one such r/count key, so these partitions are exhaustive and disjoint. Each
child recomputes its entire phase populations/pair unions, derives exactly the
types under that key, and chooses all whole H subsets and ordered splits.
The merger verifies the one-case key, rejects duplicate keys, compares all
shared primitive/local records, and concatenates every global entry in the
same declared order as the unsplit source. Restoring integer-key ordering is
only JSON serialization; the entire frozen numerical record remains identical.

The400 distinct protected shapes are sorted by their complete physical point
lists. The four half-open intervals[0,100),[100,200),[200,300),[300,400) are
disjoint and cover every shape. Each physical child reconstructs the ENTIRE
literal phase census and every completion before checking its declared shape
interval. The merger checks each row's physical shape against the reconstructed
whole sorted catalogue, checks all35 original BASE labels, rejects duplicate
indices, verifies the raw packet length for every phase family, and concatenates
the complete protected/outside packets to recompute the whole stream digest.
Every entry of the final merged records/raw products must match both the
independent implementation and the frozen complete normal-mode record.

These are deterministic partitions, not symmetry quotients or pruned searches.
Each mathematical child keeps the20-second guard; all children are serial with
native threads1 in the unchanged1CPU/2GiB scope. No resource limit was increased
after the historical unsplit optimized timeout.

## Additional conditional formulation

The same proof also establishes a sufficient-premise formulation without any
essentiality hypothesis: if the actual B meets both parents2 and6, the placed
16:2/32:6 are retained, and at least one additional ORIGINAL Q32d with d>1 is
productive in parent6, then exactly nine productive TAILs force only parents2/6.
Each placed class is productive because every hole in its parent has all four
lifts; the local minimum counts2/3 still hold and the imposed additional Q is
precisely the condition used by the full type census. All later steps are
unchanged. Essential32 in the principal theorem implies these two parent6
conditions, as already proved. This does not derive the extra productive Q
from mere presence, exclude the all-H redundant32 branch, or assert that any
of these domains has a covering.
