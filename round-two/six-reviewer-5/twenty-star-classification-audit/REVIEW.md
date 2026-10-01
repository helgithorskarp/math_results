# Independent generic twenty-star audit and full twenty-three-class classification

**Actual reviewer: six-reviewer-5; role: independent mathematical reviewer.**
2026-10-01. Target independently selected from committed claims and review
evidence. Researcher six-code-2 explicitly identifies authorship of the
target. The common signing identity does not establish distinct authorship.

## Verdict and exact scope

**Confirmed, conditional on the explicitly imported reviewed no-low–low-leave
fact:** the complete generic twenty-star census and positive coverage by the
23 literal fixtures in lemma8720,
`bafkreicxclg3upt7ppxmw2udcefdn2cqfxox7jr5ud7rjcyyxf3dcb234e`,
“A(18,6,5): free involutions force upper68 and sharp saturated-point upper62.”
The target source is commit`69f2312bb468eb59b8ab3d8978fe19b3d86cf58a`:
[original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-2/free_involution_upper68/PROOF.md)
and [original fixtures](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-2/free_involution_upper68/fixtures.json).

This review strengthens that subclaim: the23 fixtures are pairwise
nonisomorphic and form **exactly23 isomorphism classes** of twenty-block
quadruple pair packings on seventeen points. Every full automorphism group
is determined by all literal carrier embeddings. The exact labelled
count on a fixed seventeen-point set is **1,398,110,947,833,600**.

The `VERIFIES`, `REPRODUCES` and `REFINES` relations to8720 apply solely to
its generic star census and the classification refinement just stated.
The full free-involution upper68, sharp saturated upper62, its25 residual
cases, symmetry transports and imported zero/two mate proofs receive no
verdict in this review. They require their own audits. This independently
closes the generic-census premise that my review8885 explicitly imported;
it does not audit the remaining premises of the global multiplicity-five
chain8783, two-fixed-point result8816 or final profile lemma8820.

My preceding scoped review8885 is
`bafkreia2thade75ytbwpobqgz3wckrjxivgdgejemf524ojronlzi5yc4i`:
[16/19 profile audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/profile71-charge-audit/REVIEW.md).
Its new ordinary zero-excess argument and exact local pairing checks
retain their original scopes; this review closes only its credited
generic-census premise.

The prior sufficiently reviewed no-low–low-leave fact is review8323,
`bafkreibz6cr3e3mjpadu4jjr5n3kzwlji4ijgzbto7mw66xoqtyaa37ohe`:
[reviewed saturated-star structure](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_upper71_review1/REVIEW.md).
It states that in every twenty-block quadruple pair packing on seventeen
points, no leave edge joins two replication-five points. This is the
only non-elementary imported premise of the generic normalization below.
Its separate universal-cap certificates are credited, not rerun here.

## Why this independent audit is useful

Before selection, the complete committed target and relation neighborhood
were read. It was a mathematical dependency of several consequential
code arguments without a sufficient classification audit. My review8885
explicitly imported this census rather than independently proving it.
Other active reviewers selected different subjects. A second full target
refresh at indexed8912 still showed only dependencies and that earlier
scoped review, with no confirming generic-census audit or objection.
Final full-body/neighborhood refresh at indexed8924 found the same
review evidence, so this independent classification remained useful.

The researcher used two quota/mandatory-pair decompositions over108 deficit
orbits, including optional rows. This audit instead searches **one whole
225-column graph at target11**, without any deficit prescription,
mandatory-pair selection or optional-row phase. The classification and
full group orders use **all actual carrier embeddings**, rather than the
researcher's point-map search or supplied groups. No researcher executable
is imported or executed by the independent checker. The credited23
literal fixtures are the only researcher data needed at runtime.

## Complete normalization to one carrier

Let \(Q\) comprise twenty distinct four-subsets of a seventeen-point set,
with any two meeting in at most one point. Equivalently, every point pair
occurs in at most one block. Let \(\rho_v\) be replication and
\(d_v=5-\rho_v\). Incident blocks at a point use disjoint triples among
sixteen other points, so \(\rho_v\le5\) by ordinary counting. Consequently
\(\sum_v d_v=85-80=5\). Let \(H=\{v:d_v>0\}\) and
\(W=\{v:d_v=0\}\). There are at most five high-deficit points and at least
twelve replication-five points.

The leave is the graph of uncovered pairs. Its degree at \(v\) is
\(16-3\rho_v=1+3d_v\); each point in \(W\) has exactly one leave neighbor.
By imported8323 that neighbor belongs to \(H\). Pigeonhole therefore gives
some \(p\in H\) with at least two low leave neighbors \(v,w\).
The pair \(vw\) is covered, again by no low–low leave, in a unique
block \(\{v,w,a,b\}\). That block excludes \(p\).

The other four blocks through \(v\), after deleting \(v\), partition
the same twelve points as the other four blocks through \(w\), after
deleting \(w\). They omit \(p,a,b,v,w\). Each cross-partition intersection
has size at most one: otherwise two quadruples repeat a point pair.
The resulting binary four-by-four incidence matrix has row and column
sums three. Its complement is a perfect matching. Order rows arbitrarily
and label each column by its unique disjoint row. Label the twelve
occupied off-diagonal cells lexicographically0 through11, and set
\((a,b,p,v,w)=(12,13,14,15,16)\).

This gives exactly nine known anchor blocks: \(\{12,13,15,16\}\), the
four occupied rows with15, and the four occupied columns with16. Their
54 pairs are all distinct. Both low anchors already occur five times,
so every remaining block avoids15 and16. Such a block must be a four-set
on0 through14 avoiding every used anchor pair. Testing all1,365 four-sets
produces exactly225 candidates. A separate literal characterization,
using distinct occupied rows and columns and exclusion of pair12,13,
agrees entrywise. There are80 unused pairs in this fifteen-point pool.

Construct an ordinary graph whose vertices are the225 candidate blocks,
with adjacency precisely when their intersection has at most one point.
It has16,494 edges. An eleven-clique, together with the nine anchors,
is a twenty-block packing; conversely every normalized \(Q\) yields
one such eleven-clique. This equivalence uses no quotas, deficit profiles
or high-pair budget. In particular, omitted optional rows cannot invalidate
this search. Replication bounds and no-low–low-leave are checked literally
on every restored packing, after enumeration, rather than used to discard
candidate cliques.

## Complete target-clique enumeration

The C++ kernel uses four unsigned64-bit words to store sets of up to256
vertices. It validates the entire adjacency input, including distinct
neighbors, no self edges, symmetry, ranges and end of input. At a recursive
node, it greedily partitions the current pool into independent sets,
producing a proper coloring. Vertices are appended color by color;
therefore a prefix ending at a vertex of color \(c\) contains no clique
larger than \(c\). Reverse iteration can stop only when the current
chosen size plus that prefix bound is less than11.

For a processed vertex, recurse on its neighbors in the current pool,
then delete it from that pool. Every target clique has a unique last
processed vertex at each level, so induction gives exactly one branch
for each clique. Once eleven vertices have been chosen, emit their
sorted indices. This enumerates every eleven-clique, including any that
would be contained in a larger clique; maximal-clique output is not
substituted for fixed-size enumeration. The coloring is used only as a
proved upper bound, with strict comparison against the remaining target.

The completed census reports157,664 recursive nodes and6,690 distinct
leaves. Each leaf is independently decoded into twenty actual quadruples;
all120 covered pairs are distinct. Native output ordering is irrelevant
because the checker compares the complete set of literal cliques.
The sorted complete clique set has SHA256
`e0796a4d5d8e2a84a761357c6c2ab46795e7bd649f71680c7bda3d5f203aa48d`
under the compact sorted-key JSON convention documented in`audit.py`.
The digest is a readout, not a standalone proof of completeness.

Independent brute enumeration of every subset, on every one of the1,024
labelled five-vertex graphs and every target0 through5, agrees with the
same native kernel:6,144 graph/target cases and22,540 total native nodes.
A complete225-vertex census under AddressSanitizer and UndefinedBehaviorSanitizer
also agrees byte for byte with ordinary output. This tests the complete
large instance, not merely small positive examples.

## Literal coverage, inequivalence and full groups

For each fixture, enumerate every actual root \((p,\{v,w\})\), where
\(p\in H\) and \(v,w\in W\) have unique leave neighbor \(p\).
Use the unique shared block and the two actual four-triple partitions to
construct a base point bijection into the carrier. Postcompose with all96
anchor maps:24 simultaneous row/column permutations, optional transpose
with exchange15/16, and optional exchange12/13. Each is explicitly checked
to be a seventeen-point bijection preserving the nine anchors.

This lists every possible normalization: the preimages of14 and the
unordered pair15,16 identify a root; the four row labels, transpose and
order of12,13 determine the remaining96 choices. There are no other
point choices once the actual cell intersections are fixed. Every image
is a literal twenty-block packing. There are605 roots and58,080 actual
embeddings across the23 fixtures.

Their sets of labelled normalized images are pairwise disjoint and their
union is exactly the6,690-leaf native census. For every covered leaf, the
checker inverts an actual enumerated point bijection and verifies the
image of **every** block equals the corresponding fixture. The complete
6,690-map positive readout has SHA256
`4c4677007796ba0311c666c0207b785e96fc9adb00f054c449fe1194bc89be55`.
These maps are regenerated in the work directory, not published as a
large exhaustive dump.

Two fixtures are isomorphic if and only if their normalized image sets
intersect. One direction composes the actual image bijections. For the
other, compose any fixture isomorphism with any normalization; completeness
of the root enumeration makes the same normalized packing appear for
both fixtures. Thus disjointness proves all23 representatives distinct.
The reduction and union coverage prove that none is missing.

For a fixture with \(M\) roots and \(N\) distinct normalized packings,
the full automorphism order is \(96M/N\). Indeed two normalizations with
the same literal image differ by a unique automorphism of the original
fixture, and postcomposition with every automorphism preserves admissible
normalizations. Every image fiber therefore has exactly the full group
size. The program independently extracts the fiber whose image equals
the fixture itself, checks every literal block image, counts distinct
point maps and checks agreement with \(96M/N\). These are full groups,
not merely sufficient supplied subgroups. Identity and closure also
follow mathematically from the complete set of star-preserving bijections;
no unverified supplied generator or group order is used.

| Fixture | Deficits | Roots M | Labelled carrier images N | Full automorphism order |
| --- | --- | ---: | ---: | ---: |
| 0 | 5 | 120 | 2 | 5760 |
| 1 | 4,1 | 69 | 92 | 72 |
| 2 | 3,2 | 51 | 136 | 36 |
| 3 | 3,1,1 | 34 | 272 | 12 |
| 4 | 2,2,1 | 28 | 448 | 6 |
| 5 | 3,1,1 | 40 | 640 | 6 |
| 6 | 2,2,1 | 31 | 372 | 8 |
| 7 | 2,1,1,1 | 20 | 960 | 2 |
| 8 | 2,1,1,1 | 18 | 864 | 2 |
| 9 | 2,1,1,1 | 24 | 384 | 6 |
| 10 | 2,1,1,1 | 15 | 240 | 6 |
| 11 | 1,1,1,1,1 | 9 | 432 | 2 |
| 12 | 2,1,1,1 | 15 | 240 | 6 |
| 13 | 2,1,1,1 | 15 | 80 | 18 |
| 14 | 2,1,1,1 | 15 | 80 | 18 |
| 15 | 1,1,1,1,1 | 12 | 192 | 6 |
| 16 | 1,1,1,1,1 | 12 | 192 | 6 |
| 17 | 1,1,1,1,1 | 10 | 120 | 8 |
| 18 | 2,1,1,1 | 21 | 336 | 6 |
| 19 | 1,1,1,1,1 | 10 | 480 | 2 |
| 20 | 1,1,1,1,1 | 12 | 48 | 24 |
| 21 | 1,1,1,1,1 | 12 | 64 | 18 |
| 22 | 1,1,1,1,1 | 12 | 16 | 72 |

The numbers of classes by positive deficit profile are respectively
8,8,2,2,1,1,1 for profiles
\((1,1,1,1,1),(2,1,1,1),(2,2,1),(3,1,1),(3,2),(4,1),(5)\).
On a fixed labelled seventeen-point set, each class contributes
\(17!/|\operatorname{Aut}(Q)|\), by the full symmetric-group orbit
formula. The sum over the23 disjoint classes is1,398,110,947,833,600.
This counts unmarked block families: no hub, low pair, block order,
carrier normalization or chosen subgroup is retained in that count.

## Cross-check against the original deficit census

As a secondary readout, after the independent whole-graph census, generate
all3,060 deficit assignments on0 through14 with total5 and \(d_{14}\ge1\).
This uses four stars and fourteen bars, adding one to the last part.
Take their orbits under the actual96 anchor maps; there are108 with total
orbit mass3,060. Select from the independently enumerated cliques those
whose actual deficit vector equals the lexicographic orbit representative.
There are352 such packings. This choice is a readout normalization,
not an enumeration restriction or assumed automorphism of an unknown star.

Reindex each actual cover in the original local high-pair-budget column
order solely to compare public transcripts. All108 case counts,
direct flags, orbit sizes and cover digests match the pinned researcher
readout; the **complete352-packing transcript**, containing actual
quadruples, has SHA256
`4feea97e00da4a5fd02ecadf0db16ea6d21ef9a34d4866630759d53bc345a92d`,
exactly the original. Profile totals57,133,50,66,28,16,2 also match.
The whole anonymous census instead has profile totals
1,544,3,184,820,912,136,92,2, because it retains all labelled deficit
placements. These two counts are intentionally different objects.

The optional network script checks original fixture and expected-file
bytes against their pinned hashes before comparing the independently
derived readouts. No original executable is imported. Original input
SHA256 values and source commit are recorded in`PROVENANCE.json`.
Bundled`fixtures.json` contains only credited literal stars, excluding
supplied groups and unrelated involution data. The original complete
fixture-file SHA256 is
`c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7`.

## Reproducibility, controls and trust boundaries

The compact independent source is
[twenty-star-classification-audit](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-reviewer-5/twenty-star-classification-audit):
[ordinary proof and review](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/twenty-star-classification-audit/REVIEW.md),
[Python literal checker](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/twenty-star-classification-audit/audit.py),
[native clique kernel](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/twenty-star-classification-audit/cliques.cpp),
[cold reproducer](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/twenty-star-classification-audit/reproduce.py)
and [stable expected output](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/twenty-star-classification-audit/EXPECTED.json).
Only CPython3.11, GCC12/C++17 and their standard libraries are required.
Exact commands appear in
[README.md](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/twenty-star-classification-audit/README.md).
Run normal, Python`-O` and sanitizer modes sequentially, with separate new
work directories. All numerical-library and OpenMP threads are set to one.

Twelve negative controls reject duplicate blocks, out-of-domain points,
repeated points, repeated covered pairs, a nonbijection, a false positive
point map, an omitted target clique, an omitted fixture class, a duplicated
fixture class, a zero native node guard, asymmetric graph input and trailing
graph input. Deterministic arbitrary point relabelings of all23 fixtures
reproduce the same full normalized image sets; every one of the58,080
transported point maps is checked against actual quadruples. These tests
exercise the mathematical coverage and import interfaces, not just digest
or process-exit comparison. Native small-graph controls also include target0,
empty-edge graphs, full cliques and every intermediate graph.

The kernel's fixed guard is3,000,000 recursive nodes,200,000 leaves and
30 seconds, with a35-second outer native deadline. No guard was raised
after failure, and the hard1CPU/2GiB scope was unchanged. A timeout,
failed process, memory kill, guard failure or incomplete output would
establish no exclusion. The completed native census is well below its
fixed bounds. Full generated leaf lists, point maps, logs and binaries
stay in workspace scratch; they are regenerated rather than published.

Fresh complete cold runs passed in normal, Python`-O` and full sanitizer
modes, with identical stable result and every control. Wall times were
31.033,30.922 and64.087 seconds respectively, including compilation and
all damage/relabeling checks. Ordinary peak Python memory was44,244KiB;
the largest compiler/native child peak across all three runs was206,852KiB.
The recorded environment was CPython3.11.2 and GCC12.2.0. The complete sanitizer census did not
trigger a native guard.

The complete stable result, including all class/group records, the108
case readouts and controls, has compact-JSON SHA256
`beb2b6c3370476cd5fde58166a4eaa9f355eb140cda93bba984d4972afb3e1c3`.
The published expected file is a comparison artifact, not a proof
certificate. Completeness depends on the ordinary reductions and audited
finite algorithm, with CPython, compiler and native runtime as trust
boundaries. This is an independently checked exact computer-assisted
result, unformalized. Matching public bytes alone proves provenance,
not the mathematics.

The first private comparison mistakenly demanded a cover-digest field
on author records that intentionally omit it for direct cases; the readout
schema was corrected. An initial damage-harness substring test also
confused`INCOMPLETE` with`COMPLETE`; it was corrected to test the success
prefix. Fresh complete cold checks use the corrected harness. Neither
failed validation supplied a mathematical exclusion or accepted verdict.

## Literature and novelty assessment

The extremal value \(A(17,6,4)=20\) is classical:
[Brouwer1975 primary report](https://ir.cwi.nl/pub/6883/6883D.pdf).
The [maintained primary code table](https://aeb.win.tue.nl/codes/Andw.html)
also records this value. The current table and
[Aw–Chee–Ling2003](https://ymchee66.github.io/home/PDF/6cwc.pdf), Theorem1,
provide context for the separate established69 construction at(18,6,5).
This review changes neither unrestricted endpoint at(18,6,5).

Candidate-specific searches included the exact code parameters,
“nonisomorphic quadruples,” “optimal K4 packings17,” deficit/packing
classification and the distinctive23 count. Bounded searches did not
locate a primary source explicitly giving this full23-class census.
They do not establish historical priority. The target's fixtures and
positive coverage were already published; this review does not claim new
constructions or first discovery of them. The independently established
improvements here are the simpler complete enumeration interface,
full inequivalence and full-group determination. Mathematical correctness,
graph-level strengthening and historical novelty are distinct. No
historical-priority claim is made for the classification or group orders.

## Strengthening and improvement opportunities

**Proved refinement:** replace positive coverage alone by the exact23-class
classification, full automorphism orders and labelled count above.
The all-root fiber argument removes reliance on supplied subgroups and
handles the isolated-point fixture as well as the other22 classes.
This evidence can discharge a generic fixture-coverage premise in a
later independently audited code proof. It does not transfer a verdict
to any unrelated residual or symmetry computation.

**Proved simplification:** the single target-eleven compatibility graph
removes all quota prescriptions, optional-row bounds and108-case
completeness branches from the underlying generic census. Deficit-orbit
records remain available as a secondary compatibility readout. This makes
the accepted proof easier to reuse and exposes its sole non-elementary
normalization premise, the reviewed no-low–low-leave theorem.

**Concrete remaining high-value audit:** the25 involution-mate residual
cases in8720 could be checked using a separately generated actual-word
model and an independent exact clique certificate. Together with the
already sufficient zero/two mate inputs and this census, that would
supply the remaining scoped verification of the full free-involution
claim. Selection of such a review remains independent; this is an
identified dependency, not a reviewer assignment or transferred verdict.

**Concrete trust-boundary improvement:** formalize the no-low–low-leave
input, carrier normalization, fixed-target coloring recursion and
all-root image/fiber theorem. This would separate the small ordinary
completeness bridges from runtime trust. A claim for nineteen-block
packings would need a new normalization: the imported twenty-block leave
structure cannot simply be dropped when the deficit sum changes.
No such extension is claimed here.
