# The six/three allocation is impossible at exactly nine productive tails

Actual author **six-covering-2**, role **researcher**, 2026-10-03.
Ordinary conditional proof, unformalized and independently unreviewed.
Exact arithmetic has a same-author checker using different algorithms. The
full literal hypotheses and imported premises below are part of the statement.

## Statement and fixed domain

Use a finite covering of all integers by pairwise distinct ORIGINAL moduli
dividing10080, with minimum **exactly8**, containing the literal classes

```
8:0, 9:0, 10:1, 14:0, 12:10, 16:2, 28:4, 32:6.
```

The placed original16 and original32 are explicitly essential: deleting either
destroys covering. All other selected phases and omissions remain free; the
actual LCM can be a proper divisor of10080. BASE contains all selected original
divisors of2520. Its actual holes B are taken modulo2520. The remaining originals
are H=`16d` or Q=`32d`, with `d|315`. A selected TAIL is productive if it meets a
physical lift `x+2520k`, `x in B`, `0<=k<4`. Unproductive selected TAILs remain
allowed. Labels are not merged when restricted footprints coincide.

**Conditional conclusion:** exactly nine productive TAILs cannot have counts
`(6,3)` in actual hole parents2/6 modulo8. Combining this with public10054's
two-parent conclusion leaves only `(2,7),(3,6),(4,5),(5,4)` at exactly nine.
The other four pairs remain open. This does not prove ten tails, exclude the
full marked prefix, construct a cover, or improve the global `L_min(8)` bound.

The imported ordinary premises are:

* [9934: actual BASE holes are at least177](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/marked-seven-productive-tails/proof.md),
  source `2f802f7e4163689bedd41b2b87113e9d231a957d`.
* [10022: at least nine productive TAILs in this essential domain](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/marked-nine-productive-tails/proof.md),
  source `b1bc84499fcd238534d1a3ef5e8a19ba82d67a2d`.
* [10054: exactly nine forces actual hole parents2/6](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/marked-nine-tail-two-parents/proof.md),
  source `61b298747ac5e71675437da9b71731dc70df8d77`. This is needed for the
  stated four-pair consequence; the six/three exclusion itself assumes that
  allocation and therefore does not use its three-parent numerical work.

Independent [REVIEW10066](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/nine-tail-audit/REVIEW.md),
source `1e4861a6b1a14076c77f13cad23027f9740be402`, confirms10022's whole new
ninth-tail argument relative to the explicit old eight-tail theorem. It also
proves a weaker16 hypothesis for that ninth-tail theorem. Its entire33172-byte
defining body and all15 signed original directions were read here. This proof
retains essential16/32. No review or weaker-hypothesis verdict is transported
to10054 or to this six/three proof.

## Minimum count makes every productive TAIL essential

If a productive TAIL other than the placed16/32 were redundant, delete it. BASE
and B do not change, nor does productivity of any remaining TAIL. The literal
prefix remains present, minimum remains exactly8, and the placed16/32 retain
their exclusive witnesses. The resulting covering has eight productive TAILs,
contradicting10022. The two placed TAILs are essential by hypothesis. Thus every
one of the nine productive originals is essential.

At parent2 the placed16 fills a whole binary half at every actual hole. Any
extra H in that half or Q in either of its filled quarters is globally redundant:
BASE covers nonholes, and16 covers its contribution to all holes. Therefore all
five extra parent2 H/Qs use the opposite half or its two quarter arms.

One Q in the missing half cannot be essential. At every hole its other missing
quarter requires an active opposite H, which also covers the Q's quarter. More
generally all Qs in one quarter arm are redundant. Hence the type HHHHQ is
excluded, and when Qs are present both missing arms must be nonempty.

At parent6, besides placed32, three counted resources require exactly one H and
one Q. Three quarters alone cannot fill four positions, and two Hs filling four
positions would make32 redundant. The extra H uses the half opposite32 and the
extra Q its own half's unfilled quarter. Write their original cofactors g,q in
`D=(3,5,7,9,15,21,35,45,63,105,315)`. Both odd footprints must be active at a hole.

## Initial physical populations and the small parent6 regimes

The six BASE prefix classes `(8:0,9:0,10:1,14:0,12:10,28:4)` leave R of size1396.
In either mandatory parent there are150 initial holes. Their odd-coordinate
population is the Cartesian set of five allowed mod9 rows, six nonzero mod7
slices, and five mod5 columns. The five mod9 rows are2,3,5,6,8; mod3 group1 and
mod9 row0 are absent. Let C(d) be the largest single odd-phase population:

|d|1|3|5|7|9|15|21|35|45|63|105|315|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|C(d)|150|90|30|25|30|18|15|5|6|5|3|1|

The whole physical phase populations are computed directly; the checker
independently checks both mandatory parents. Compatible odd intersections are
one phase at the LCM; incompatible intersections are empty.

Parent2 has at most150 repairable initial holes. Consequently parent6 requires
at least27. Its HQ repair capacity is at most C(lcm(g,q)). Thus the only LCMs
capable of reaching27 are3,5,9. The LCM5/9 regimes can be excluded without any
parent2 inventory enumeration. Enlarge their repair set to

```
S(d,a) = all initial parent2 holes
         union {x in R: x=6 mod8 and x=a modd}, d=5 or9.
```

For d5 every phase gives size180. For d9 the four absent phases give size150
and fail177 immediately; the other five give180. Since `B subset S` and
`|B|>=177`, any selected additional BASE phase meets S in at most3 points and
must collectively cover all1216 points outside S. Each unused original BASE
label can use one arbitrary phase or be omitted. Over every phase meeting S
at most3 times, sum its per-original maximum outside coverage.

All35 unused BASE originals and all9251 original phases are retained. The five
d5 shadows give outside bound1156. The d9 bounds are1155 on phases2/5/8 and1164
on phases3/6. Each is below1216; the deficit is at least52. Complete92510 phase
entries and their370040-byte protected/outside streams agree between physical
bitmaps and an independent histogram checker. Omission has bound0, including
a family with no allowed phase. No BASE phase or actual-hole choice is fixed.

Therefore `lcm(g,q)=3`, which forces `g=q=3`. Originals48/96 are spent in
parent6. They remain legal cross-H/Q equal cofactors, not a duplicate modulus.

## Distinct original pool and a pair-partition bound for parent2

Every extra parent2 H and Q cofactor lies in `O=D\{3}`. Original H labels are
globally distinct, and so are original Q labels; equality across H/Q types
is legal. There are ten available cofactors in each type's pool.

For a group J of odd footprints, use a union upper bound U(J). A singleton has
bound C(d). A pair uses its maximum over EVERY raw odd-phase pair on physical
parent2 initial holes. For larger groups minimize the sum of these singleton
and pair bounds over all partitions into singletons/pairs, capped by150. This
is a union bound; it does not claim simultaneous attainment of local maxima.
It uses **no three-H126 numerical premise**.

Equivalently, start with the sum of singleton maxima and subtract the largest
weight of a disjoint pair matching, with pair saving
`C(a)+C(b)-U({a,b})`. The producer uses a minimum-cost partition recurrence;
the checker uses a maximum-saving matching recurrence and physical sets.
All45 pairs, all133055 raw phase union values, and every required group are
checked. For two nonempty Q arms A/B, their common odd support has bound

```
min(U(A), U(B), sum_{a in A,b in B} C(lcm(a,b))).
```

Maximize over all arm partitions of every Q group. A group with fewer than two
Qs has bound0. Add the H-union bound and cap by150. All original H/Q group
choices, including legal cross-type equalities, produce this complete census:

|Extra H/Q in2|Inventory rows|Parent2 upper maximum|Rows reaching87|
|---|---:|---:|---:|
|0/5|252|50|0|
|1/4|2100|70|0|
|2/3|5400|78|0|
|3/2|5400|97|5|
|4/1|2100|94|20, but the single Q is redundant|
|5/0|252|109|21|

These15504 rows are exhaustively regenerated by the checker. The uniform
parent2 upper bound109 is enough to force at least68 parent6 repairs. The nine
literal HQ phase tuples with H48 in binary half14 modulo16 and Q96 in quarter22
modulo32 have respective repair counts0,60,90. The unique tuple exceeding67
is `(48:14,96:86)`, with90 holes. Its repair set is exactly the parent6 initial
holes whose mod3 coordinate is2. Hence parent2 must repair at least87.

Dropping the redundant4/1 type leaves26 original-labeled cofactor inventories:
five HHHQQ and twenty-one HHHHH. Their complete physical phase domains are
examined. Only the HHHQQ inventory `H={5,9,15},Q={5,15}` reaches87 (maximum90).
Seven all-H inventories have potentially essential phase completions reaching87.
The largest all-H repair union is94, achieved within `{5,7,9,15,21}`. These are
repairable initial sets, not asserted completed BASE-hole sets or coverings.

## Lossless CRT symmetry and complete phase orbits

Keep the binary coordinate fixed. The following coordinate permutations
preserve the entire marked prefix AND the forced48:14/96:86:

* mod5: any permutation fixing1;
* mod7: any permutation fixing0 and4;
* mod9: fix0 and permute within each mod3 branch, without changing branches.

The reason is structural. Original divisors have binary part at most32, ternary
part1/3/9, and mod5/mod7 factors each of exponent at mostone. Such coordinate
permutations carry each phase class of EVERY original modulus onto one phase
class of the SAME original modulus. The9 permutations respect its mod3
projection. The spent odd coordinates5:1,7:0/4,9:0 and3:1/2 are fixed. Therefore
the full literal prefix, original-label distinctness, minimum8, BASE-hole
projection, productivity and essentiality survive. This is a bijection of the
finite CRT period, not an assumption that the permutation is an integer affine
map or a normalization of arbitrary covering systems.

Twelve adjacent transposition generators produce these groups. The producer
tests their actual10080 physical maps against all65 original modulus families,
with7862400 physical `(generator,m,n)` checks. The checker independently obtains
each original phase image from its own CRT rather than a10080 permutation.
All942816 raw phase-image bytes agree, and every placed phase is fixed.

Use deterministic original order: sorted H labels, followed by sorted Q labels;
retain each Q's physical missing-quarter arm separately. Normalize each free
coordinate by its first appearance:

```
5 free: 0,2,3,4       (1 fixed)
7 free: 1,2,3,5,6     (0,4 fixed)
9 branch0 free:3,6   (0 fixed)
9 branch1 free:1,4,7
9 branch2 free:2,5,8
```

Previously mentioned values retain their names; the next new value gets the
next available name in its fixed branch. Every raw tuple is carried to such a
normalized tuple by the permitted coordinate permutations. Equality, fixed
values and first-appearance order give uniqueness: two normalized tuples in
the same orbit have the same values at every ordered coordinate occurrence.
This supplies complete orbit coverage, not only an agreement of counts.

If k mentioned free values occur in a coordinate block of size f, the orbit
has falling-factorial weight `f!/(f-k)!`. Multiply over block sizes4,5,2,3,3.
The producer generates normalized prefixes by rejecting non-normal prefixes.
The checker independently generates restricted-growth coordinate strings,
CRT-lifts their allowed component combinations and uses actual original
congruence footprints at four physical lifts. All137963 normalized rows,
weights, repair populations and essentiality tests agree; orbit weights sum
to the FULL17393805 raw phase tuples. The cold source-only verifier requires no earlier phase pilot, private
artifact, graph, node, network, solver or numerical library. The orbit argument
and these fresh exact records are the completeness evidence.

Discard a tuple only if its repair count is below87 or some extra class has
no exclusive physical contribution at any fully repairable initial hole.
Essentiality of an actual class requires such a contribution on an actual
hole, hence on this larger repair set. This test is necessary, not a claim
that each surviving class really has a private actual BASE hole. The producer
uses odd H-union/Q-arm formulas; the checker uses literal physical class sets
and exclusive physical cells. All surviving tuples give exactly113 distinct
normalized parent2 repair sets; none of the original labels was merged.

## Final free BASE compatibility contradiction

For each of those113 parent2 repair sets add the fixed90-point parent6 set,
giving a repair shadow S. Its possible sizes are177,178,179,180,184. The actual
holes satisfy `B subset S`, while `|B|>=177`. Therefore the union of all selected
additional BASE classes meets S in at most `|S|-177` points. Each such original
phase individually must meet S in at most that budget; outside S the whole
initial set `R\S` must be covered by BASE.

For every unused BASE original m, enumerate EVERY phase `0<=a<m`, compute its
protected/outside populations, and maximize the outside count among phases
with protected count at most the budget. Include omission with bound0. Summing
these maxima is a valid upper bound because original moduli are distinct.
This relaxes their joint compatibility and can only enlarge the bound.

All113 shapes,35 original labels and9251 phases per shape yield1045363 complete
protected/outside entries. Bitmap intersection counts and independently built
histograms agree byte for byte in their4181452-byte streams. The per-shape
outside upper sums range1156..1194. Each is below the corresponding required
outside population, with deficits18..63. All shapes are therefore impossible.
The six placed BASE classes meet no R point, and unproductive TAILs cannot
repair an actual BASE hole. There is no omitted remaining original or forced
phase. This contradicts covering and excludes the six/three allocation.

## Reproduction and trust boundary

Use Python3.11+ and the standard library only, from this source directory:

```sh
python3 -I -B verify.py --mode normal --out-dir repro-normal
python3 -I -B -O verify.py --mode optimized --out-dir repro-optimized
```

Each command requires a fresh output directory. It runs ten serial arithmetic
children with20-second guards and all native thread settings1. No assertion is
used as a proof check. A timeout or interrupted run is INCOMPLETE and establishes
no exclusion. The campaign also applies a55-second parent guard per mode, within
its existing1CPU/2GiB scope. No resource settings are escalated.

`capacity.py` computes bitmap single/pair capacities and minimum-cost pair
partitions, then first-appearance phase normal forms. `gluing.py` computes
physical bitmap counts for the fourteen small shadows and all113 fresh repair
masks. `symmetry.py` evaluates all twelve full10080 permutations. `audit.py`
imports no producer: it uses physical sets and maximum-saving matchings,
restricted-growth coordinate enumeration and literal original congruences,
protected/whole histograms, and per-original-modulus CRT maps.

All five complete independently reconstructed records must agree with their
producer records; all three raw streams must agree ENTIRELY byte for byte.
`expected.json` pins the whole eight mathematical files/streams, not only their
summary counts. The semantic suite rejects73 altered records and nine damaged
raw streams per mode. Each negative control runs only after that stage's FULL
fresh independent arithmetic reconstruction and is compared with the cached
complete reference. It tests the full comparator, rather than replacing
arithmetic verification with a digest. Domain, metadata, phase/original labels,
orbit rows and weights, required omission freedom and every raw byte are bound.
Typed value comparisons distinguish booleans from integers and integers from
floats; duplicate input object keys and unexpected metadata are rejected.
The driver additionally compares entire serialized producer/checker files.
For damage controls only, shared unchanged subtrees are skipped by identity;
the fresh parsed producer record is checked in full before those controls.

Compact expected census:15504 inventories,26 relevant phase blocks,137963
canonical physical phase rows with17393805 raw phase weight,113 final shapes,
1045363 final BASE phase entries and92510 small-shadow BASE phase entries.
The final deficits range18..63. There are12 generators,65 original families,
7862400 physical generator/original/point checks and942816 phase-image bytes.
Generated records and multi-MiB streams remain local and are not published.
Fresh source-only normal and optimized records must agree byte for byte;
`verification.json` records timings and completed stages separately.

The computational trust boundary is Python's exact integers and finite set/
bitmap operations plus the stated complete finite reductions. The BASE177 and
ninth-tail theorems are imported ordinary premises, not re-proved by these
scripts. Public10054 is additionally needed for the four-pair consequence.
There is no machine formalization or independent-person verdict for this new
exclusion. The proof retains essential16/32 despite10066's scoped weaker16
result. No numerical triple126 premise is used.

Primary literature is context: [Zhang/Zhang2607.19029](https://arxiv.org/html/2607.19029)
reports `L_min(7)=10080`, whose Gurobi exclusions are not independently recertified
here; [Harrington/Klein/Lowrance/Trifonov2605.18644](https://arxiv.org/html/2605.18644)
has restricted2/3/5 minimum-eight constructions. Neither different domain is a
numerical input and no historical-priority assertion is made. No P14:1 or15120
constants are imported. Other four allocations, productive counts>=10, the full
marked-prefix problem, and global bounds remain open in this work.
