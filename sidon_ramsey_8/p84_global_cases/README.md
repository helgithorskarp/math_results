# A complete global case decomposition for balanced P84

**Exact computer-assisted reduction, with partial case exclusions.** Every
partition of `[84]` into four integer Sidon eleven-sets and four Sidon ten-sets,
up to reflection, belongs to one of **1,211 explicitly indexed unresolved
cases** in `cases.csv`. Conversely, a solution to any of these cases is such a
partition. The cases have global coverage; they impose no retained seed class
or bounded repair neighborhood.

There is no P84 witness or complete P84 exclusion here. The campaign interval
remains **81 <= SR(8) <= 85**. The preceding
[P84 profile theorem](../p84_profiles/README.md) makes balanced P84 equivalent
to unrestricted eight-class P84. That preceding theorem is a dependency only
for this unrestricted interpretation, not for the balanced reduction below.

## Reproduction

Python 3.11+ (standard library) and GCC/G++ with C++20 and unsigned 128-bit
integers suffice for the mathematical reduction and all 213 new cover
exclusions. From this directory:

```sh
python3 reproduce.py --work /tmp/p84-global-cases --jobs 4
sha256sum -c SHA256SUMS
```

This regenerates the full eleven-catalog by two algorithms, rechecks the ten
weight bound, enumerates all global and anchored four-tuples, checks every
per-case reflection identity, and verifies every selected residual by two
complete cover algorithms. It compares every ten-catalog entry and every
negative decision, and exercises both methods on six positive controls.
Expected final output includes `verified: true` and `unresolved_cases: 1211`.
Use a fresh work directory outside the source tree. Python optimized mode is
rejected because assertions check evidence. Generated catalogs, CNFs, traces,
binaries, and logs remain in the work directory.

For additional SAT semantic checks, install `python-sat==1.9.dev15` in a local
virtual environment and use that interpreter:

```sh
python reproduce.py --work /tmp/p84-global-cases-sat --jobs 4 --sat-checks
```

No solver result is a premise of the reduction or of the 213 cover exclusions.
The SAT checks cover all 4,097 counter assignments through length eight and
55,340 small coloring assignments across both the difference and pair-sum
encodings, with symmetry enabled and disabled. A separate P14 check covers
all eight unlabeled partitions of profile `(5,5,4)`, verifying the anchor
normalization and the earlier-orbit prohibition. Published P80 witnesses are
accepted by both encodings at shifts zero and four, exercising labels up to
83. These tests supplement the encoding proof below; they do not exhaust P84.

## Complete anchor reduction

Use labels `0,...,83`. Let `v` be the symmetric nonnegative integer weights in
`../p84_profiles/weights.txt`. Their sum is `W = 15,685,948`.
Full enumeration verifies that all 35,250,764 Sidon ten-sets have weight at
most 1,999,990, hence at most `M = 2,000,000`. Pair sums include repeated
summands throughout.

Let `L` be the complete catalog of 30,510 eleven-sets. Reflection
`r(x)=83-x` pairs its members into 15,255 two-element orbits. No eleven-set
can be fixed by reflection: reflection has no fixed point and an invariant
set therefore has even size. In each orbit choose the set with the smaller
84-bit membership mask as the canonical representative. Rank the orbits by
decreasing weight, breaking ties by this canonical mask. Ranks start at zero;
rows `2*j` and `2*j+1` of `orbit_catalog.txt` are the canonical representative
and its reflection, respectively.

In a balanced partition the four eleven-classes have total weight at least

`T = W - 4*M = 7,685,948`.

Choose their least-ranked orbit `j`. Its weight is the largest of the four,
so `4*v(A_j) >= T`. Exactly 1,488 orbits satisfy this inequality. Reflect the
whole partition if needed so that the canonical representative `A_j` is a
class. The remaining three eleven-classes belong to orbits of rank at least
`j`; the remaining four classes are tens.

Define case `j` by these exact conditions: fix `A_j`, cover its 73-point
complement by three elevens and four tens, and prohibit every earlier-orbit
eleven-class. Every balanced partition belongs to this case family after at
most one reflection. Its case index is uniquely determined by its four
eleven-classes and is invariant under reflection. A case can still have
multiple color assignments for one reflected partition; no one-to-one count
of SAT models is claimed.

## Exhaustive packing audit and closed cases

Before covering any residual, enumerate all disjoint unordered four-tuples
of eleven-sets with total weight at least `T`. There are **125,576,811**.
For orbit `j`, define:

- `R_j`: number of such tuples whose least orbit is `j`;
- `F_j`: number of those tuples containing the canonical representative;
- `B_j`: number containing both members of orbit `j`;
- `H_j`: number fixed as a four-set family by reflection.

The two independent traversal organizations verify, for every eligible `j`,

`R_j = 2*F_j - B_j`.

Indeed reflection bijects the tuples containing the canonical representative
with those containing its mirror, and the intersection consists exactly of
tuples containing both. The catalog is ordered in consecutive orbit pairs,
so the anchored traversal chooses three later rows disjoint from row `2*j`.
The global traversal uses recursively filtered candidate vectors; the
anchored traversal uses fixed-depth loops and union-mask tests. All pruning
bounds replace unchosen weights by larger available weights and retain
threshold equality. They have shared authorship and the same mathematical
weight reduction; they are not external independent reviews.

| Exact quantity | Value |
| --- | ---: |
| Eligible reflection orbits | 1,488 |
| Orbits occurring in a qualifying packing | 1,424 |
| Global tuples, sum of R_j | 125,576,811 |
| Anchored tuples, sum of F_j | 62,861,452 |
| Tuples containing both minimal-orbit members, sum of B_j | 146,093 |
| Reflection-fixed four-set families, sum of H_j | 2,639 |
| Cases empty at the packing stage | 64 |
| Nonempty cases with F_j <= 100 | 213 |
| Anchored tuples in these 213 cases | 5,959 |
| Distinct forty-point residuals from these tuples | 5,959 |
| Ten-set occurrences on those residuals | 999,039 |
| Completable residuals | 0 |
| Remaining unresolved anchor cases | 1,211 |

The 64 packing-empty cases cannot contain a partition. For each of the 213
nonempty cases with `F_j <= 100`, the complete anchored tuple list is checked
against the independently derived histogram. Each tuple leaves 40 points.
Both algorithms enumerate every Sidon ten-set on that residual, then test
whether four disjoint tens cover it. Every residual fails. Thus these 213
entire global cases are excluded, not merely selected assignments within
them. The other 1,211 cases retain **62,855,493 anchored packings**.

The 213 exclusions remove only about **0.0095%** of anchored packings, despite
closing roughly 15% of the nonempty anchor cases. The principal result is a
verified global decomposition and an executable complete-case protocol;
this modest tail exclusion is not evidence that the whole computation is
nearly finished.

`complete40.cpp` reuses the two previously checked enumeration methods from
`../p80_extension_barrier/verify.cpp`, with the ambient range set to 84.
Method zero builds increasing sets through unused positive differences and
branches on a residual point lying in the fewest available tens. Method one
fixes the minimum and maximum of each ten-set and checks unordered pair sums;
its cover search always branches on the least uncovered point. Both are
complete because some chosen class must contain the selected uncovered
point. At the last class, cardinality forces ten points and pair sums are
checked directly. Sorted catalogs are serialized as exact integer masks and
compared entry by entry; the binary traces are reproducible but not committed.

## Global SAT formulation and case generation

Generate the single formula covering all balanced partitions:

```sh
python3 encode.py --output /tmp/p84-global-cases/p84.cnf
```

It has **62,340 variables and 181,236 clauses**. Point-color variables occupy
the first `84*8` positions. For each color, a pair variable represents that
both endpoints of one positive-difference pair have that color. Each
positive difference may occur at most once within a color. Repeated positive
differences are equivalent to repeated unordered pair sums, including
three-term progressions arising from a repeated summand, so these constraints
express exactly the integer Sidon property. Differences having only one
possible pair need no constraint.

Each point has exactly one color. Sequential counters bound class sizes
above by `(11,11,11,11,10,10,10,10)`; since these bounds sum to 84, every size
is exact. The counters propagate the assertion that a prefix contains at
least `j` selected variables and forbid a `(k+1)`st selection. Actual prefix
counts always supply a satisfying auxiliary assignment when the bound holds.
Within each equal-size color group, minima are increasing; any partition
admits such a relabeling. No ordering is imposed between unequal-size groups.

Generate any indexed case, for example case zero:

```sh
python3 encode.py --case 0 \
  --catalog /tmp/p84-global-cases/orbit_catalog.txt \
  --weights ../p84_profiles/weights.txt \
  --output /tmp/p84-global-cases/case0.cnf
```

The anchor is removed and the profile becomes `(11,11,11,10,10,10,10)`.
For every earlier-orbit eleven-set `B` disjoint from the anchor and each of
the three remaining large colors `c`, add the clause
`OR(x in B) NOT color(x,c)`. Since that class has exactly eleven elements,
this prohibits precisely the class `B`. An earlier set intersecting the
anchor cannot be a remaining class, so it needs no clause. This is a complete
encoding of the case conditions, with no positive catalog selector variables.
The generator checks the supplied orbit ordering but relies on catalog
completeness; `reproduce.py` establishes that completeness separately.

The alternate `--kind sums` encoding derives forbidden monochromatic sets
directly from equal unordered pair sums. `decode` verifies each returned
class using the defining pair sums, exact sizes, and the earlier-orbit
prohibitions. Anchor metadata also checks that all 84 points are covered.
For solver experiments, use explicit local executable paths if needed:

```sh
python3 run_solver.py /tmp/p84-global-cases/case0.cnf --seconds 300 \
  --kissat /path/to/kissat --checker /path/to/drat-trim
```

The wrapper checks every SAT witness and requires a verified DRAT trace
before reporting checked UNSAT. Interrupted or time-limited runs are UNKNOWN.
A 300-second global pilot and a 120-second case-zero pilot both returned
UNKNOWN. Neither closed a case. Small free controls P14 and P24 returned
verified witnesses; the `(5,5,5)` P15 control produced a checked UNSAT proof.
The `(7,6,6,6)` P25 control also remained UNKNOWN after 30 seconds. These
measurements caution against escalating a generic SAT time limit solely
because the CNF is smaller. `sat_measurements.json` records them.

## Evidence and trust boundary

`cases.csv` is the complete compact case ledger, with zero-based orbit ranks
and explicit `packing_empty`, `cover_excluded`, or `unresolved` status.
`validation.json` records the fresh final reproduction and its measured
runtime. `SHA256SUMS` includes reused source dependencies. No earlier raw
catalog, SAT verdict, LP optimizer, seed template, or private input is needed
for the balanced reduction or its 213 cover exclusions.

This is exact computer-assisted mathematics. It trusts the written reduction,
source implementations, exact integer arithmetic, compiler/runtime, and
completed runs. The new results are internally cross-checked, not externally
reviewed or proof-assistant formalized. Historical novelty is not asserted.
The broader primary-literature context and the externally reviewed P85 result
are documented in the [parent contribution](../README.md).
