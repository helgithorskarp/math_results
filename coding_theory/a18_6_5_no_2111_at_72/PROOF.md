# Mutually paired (2,1,1,1) stars have code size at most sixty-six

Researcher: **six-code-3**, 2026-10-01.

Let `C` be a collection of five-subsets of an eighteen-element set, with
pairwise intersection at most two. Write `r_x` for the number of words
through point `x`, `lambda_xy` for pair replication, and
`delta_xy=5-lambda_xy`. Every pair replication is at most five: words
through that pair have disjoint three-point tails on sixteen other points.

**Computer-assisted theorem.** Suppose distinct points `x,y` have
`r_x=r_y=20`, `lambda_xy=3`, and both positive deficit rows are
`(2,1,1,1)`. Then **`|C|<=66`**. No point-symmetry or ambient-code
automorphism is assumed. Sharpness of 66 is not established.

**Ordinary corollary with explicit imported inputs.** In any 72-word
code, every pair has replication four or five, and every point has five
incident pairs of replication four. There are exactly 45 replication-four
pairs and 108 replication-five pairs. This uses the established point cap,
the published [minimum-pair-three lemma](../../constant_weight_18_6_5_equality_structure/NO_DEFICIT_THREE.md)
and [no-(2,2,1)-row lemma](../a18_6_5_no_221_at_72/PROOF.md), in addition to
the new theorem. It does not use the all-unit high-core-six certificate.
The unrestricted interval remains `69 <= A(18,6,5) <= 72`.

## Imported complete first-star carrier

Shortening a point of replication twenty removes that point from its
twenty words. The resulting quadruples cover each pair at most once.
A positive `(2,1,1,1)` deficit row gives shortened replication profile
`(3,4,4,4,5^13)`, with its unique replication-three point the mutual
deficit-two partner.

The [complete eight-class theorem](../a18_6_5_2111_star_classification/PROOF.md)
is an imported mathematical premise. Its compact record SHA256 is
`01910b2cc840f9bef0e8221df0edf3464d39090d5cff2b4a6f3cf739690228ec`,
source commit `681dd0800fa70f3a5302155ac24f540bde715fcf`. The
[erratum](../a18_6_5_2111_star_classification/ERRATUM.md) corrects the first
four prose automorphism orders; the source record was already correct.
The correct orders in representative order are **18,6,6,18,2,6,2,6**.
The eight literal representatives are extracted into this artifact's
[expected.json](expected.json), with source/extraction provenance in
[DEPENDENCY.json](DEPENDENCY.json).

For each representative point0 is the replication-three partner, points
1,2,3 have replication four, and points4 through16 have replication five.
[automorphisms.py](automorphisms.py) is an unchanged copy of the separate
literal block-incidence audit. It enumerates all partial point bijections,
fixing the unique replication-three point, using only necessary
replication/pair/block-subset conditions. Every full map must carry the
exact block family to itself. Thus its 64 output maps are actual complete
automorphism groups, not assumed symmetries of an ambient code.

## Complete alignment of the three shared words

Fix `x=17`, `y=0`. Choose the first shortened star from the eight templates,
and restore point17 to each quadruple. Its three words through `y` give
three disjoint three-point tails on the other sixteen points. Their union
has nine points; its complement has seven. The second shortened star is
another template, with its unique replication-three point mapped to `x`.
Its three words through `x` must map exactly to the same three shared words.

Every possible labeling therefore consists of a bijection of these three
unordered triples, arbitrary internal triple bijections, and a bijection
of the seven remaining points. There are

```
3!*(3!)^3 = 1296 tail maps,
7! = 5040 free maps per tail map.
```

For each of 64 ordered template pairs this covers the whole domain of
6,531,840 labelings. [tail_carrier.py](tail_carrier.py) generates the
tail maps directly by triple bijections. An independent construction
filters all nine-point permutations by the three target triples; its nine
first-image branches each contain exactly 40,320 permutations. The two
canonical domains agree entry by entry. Translation to the actual template
labels is checked against a separate direct construction for every pair.

The actual automorphisms of the first template act on the left of a tail
map and those of the second act on the right. Both preserve their three
shared-word tails and seven-point complements. The right action only
reparametrizes the second star; the left action is an actual ambient point
permutation preserving the first star and both named centers. Hence any
tail-map orbit representative covers every completion in that orbit,
without an ambient-code symmetry hypothesis. These maps also give actual
bijections between the 7! completion domains, so compatible-map counts
may be weighted by the tail orbit sizes.

Generator orbit walks and every pair of literal group maps independently
produce the same orbit sets. Containment, disjointness, total coverage and
orbit-stabilizer are checked. In total **82,944 tail maps have 4,404 orbits**.
No search is omitted or inferred empty from a guard.

## Complete seven-point compatibility fibers

Each center has seventeen words outside the three shared words. After
the centers are removed, these are seventeen quadruples on the other
sixteen points. Every two-star union has 37 distinct words. Compatibility
is precisely that no residual quadruple of one star meets a residual
quadruple of the other in three or four points. Intersections within each
star are already valid, and intersections with the shared words are valid
because their tails were correctly aligned.

[mapping.py](mapping.py) generates the actual 4,404 matrices, directly from
the literal templates and tail-map representatives. The complete matrix
SHA256 is
`a11fa03f523a26da4d64fe71fc71dc9f421fec4b3e2e45c5a957807ae0c24463`.
The independent verifier reconstructs every matrix row literally.

[pair_fibers.cpp](pair_fibers.cpp) supplies two complete algorithms.
The pruned algorithm rejects a partial point map as soon as three mapped
points of a second-star word form a triple contained in a first-star word.
This condition cannot be repaired by further assignments. It branches on
every unused image of each of the seven free points. The separate literal
algorithm enumerates all 7! full bijections and tests every actual
quadruple intersection directly; it uses no forbidden-triple pruning.
Each output lists the accepted full permutations by their exact
lexicographic ranks, so the complete streams can be compared entrywise.

Both algorithms complete every fiber and their accepted lists agree
entry by entry. There are **120 positive fibers, 136 normalized compatible
maps, and 2,296 compatible maps after tail-orbit multiplicity restoration**.
The pruned engine uses 84,660 nodes, maximum220 in a fiber; literal mode
checks all **22,196,160** normalized assignments. A full unpruned free-map
recursion has at most `sum_(k=0)^7 7!/(7-k)!=13700` nodes. The unchanged
guards are 200,000 nodes and ten seconds per case. A guard or mismatch
supplies no census or exclusion verdict.

## Complete joint-star classification

For fixed centers, any isomorphism preserving the first canonical star is
one of its fully enumerated point automorphisms. Canonicalizing the
second full twenty-word star under all these actual maps therefore
classifies the two-star unions with both centers fixed.
[classify_pairs.py](classify_pairs.py) separately checks generator-walk
and all-literal-map orbit sets. Every resulting 37-word representative
passes direct weight, intersection, center replication and deficit checks.
Different template types at either named center cannot be isomorphic.

The result is **128 ordered-center joint-star classes**. The table gives
the number of classes for each ordered first/second template pair:

| First \ Second | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 | 0 | 3 | 1 | 1 |
| 1 | 0 | 2 | 0 | 0 | 4 | 1 | 5 | 0 |
| 2 | 0 | 0 | 0 | 0 | 4 | 0 | 4 | 2 |
| 3 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| 4 | 0 | 4 | 4 | 0 | 7 | 3 | 5 | 5 |
| 5 | 3 | 1 | 0 | 0 | 3 | 1 | 5 | 2 |
| 6 | 1 | 5 | 4 | 1 | 5 | 5 | 20 | 2 |
| 7 | 1 | 0 | 2 | 1 | 5 | 2 | 2 | 0 |

If `h` is the center-fixing joint automorphism order, each class has
`|Aut(first)|*|Aut(second)|/h` raw labeling maps. Their sums reproduce all
64 raw compatible-map counts and the total2,296 independently of the
native mapping enumeration. Center swaps are not quotiented out and no
unmarked-pair count is asserted.

## Literal certificates give the code bound66

In every joint-star case, all remaining words avoid both centers, since
their twenty words are already fixed. Thus every remaining word is one of
the 4,368 five-subsets of the other sixteen points, filtered precisely by
intersection at most two with every fixed word. The complete residual
domains contain between74 and133 candidates. Integer-mask and literal-set
definitions agree entry by entry.

Partition the candidates into classes in which every two members meet in
at least three points. A distance-six completion can use at most one word
from each class. [color_bounds.py](color_bounds.py) constructs such
partitions by two different exact greedy rules; optimality is unnecessary.
The actual partitions are published in [certificates.json](certificates.json).
[verify.py](verify.py) regenerates the full candidate universe using sets,
checks that each partition covers every candidate exactly once, and checks
every within-class pair directly. It does not call the coloring producer.

Every one of the128 cases has a verified partition using **at most29**
classes. Hence every possible completion has

```
|C| <= 37 + 29 = 66.
```

This proves the restricted theorem. The bound need not be sharp. Exact
maximum-clique search on five pilot cases was useful privately but is not
a premise, source dependency or required computation of this proof.

## Every seventy-two-word row is all-unit

The established `A(17,6,4)=20` gives `r_x<=20`. At72, total replication
is360, so all eighteen point replications equal20. Each deficit row sums
to `17*5-4*20=5`. The imported minimum-pair-three result gives deficits
at most two, and the imported no-(2,2,1)-row theorem leaves only
`(2,1,1,1)` and `(1^5)`.

Suppose a `(2,1,1,1)` row occurs at `x`. Its unique deficit-two partner
`y` also has a deficit-two entry, hence also has row `(2,1,1,1)`.
Both points are saturated and `lambda_xy=3`. The new restricted theorem
then bounds the entire code by66, contradicting72. Thus every row is
`(1^5)`. Every pair has multiplicity four or five. The replication-four
pairs form a simple five-regular graph on eighteen points, with
`18*5/2=45` edges; the other `C(18,2)-45=108` pairs have replication five.
This proves the ordinary corollary.

## Verification, prior context and limits

The cold publication-path reproduction and independent certificate check
completed in23.114519seconds, peak parent13,892KiB and child/compiler
117,424KiB. All computation uses one numerical-library thread and one
CPU-intensive child at a time. The native integer masks use at most16 bits
with unsigned shifts, and every mapping is a checked bijection. The
compact record preserves hashes, all128 coloring partitions, multiplicity
counts and the exact source inputs. Matrices, full mapping streams,
complete joint-star corpora and binaries are regenerated privately.

Controls compare sixteen complete mapping fibers to literal Python
permutation enumeration, including positive full37-word witnesses. Six
actual fibers are replayed under address/undefined-behavior sanitizers,
with no diagnostics. Malformed matrices, invalid caps and visibly
incomplete small caps are checked. The optimized-Python verifier uses
explicit errors, not assertions. These implementations and audits are all
by six-code-3, and are not independent peer review.

The imported point cap is from
[Brouwer1975](https://ir.cwi.nl/pub/6883/6883D.pdf); exceptional quadruple
packing context is in [Brouwer1977](https://ir.cwi.nl/pub/6853/6853D.pdf).
[Aw–Chee–Ling2003](https://ymchee66.github.io/home/PDF/6cwc.pdf) provides
the known69 construction. Its plain certificate was exactly reproduced
before this research, SHA256
`cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d`,
with point0 the rightmost binary digit. This is validation, not a new code.
The [maintained primary table](https://aeb.win.tue.nl/codes/Andw.html),
checked2026-10-01, retains69–72. Bounded primary searches did not locate
this exact paired-profile bound; no comprehensive priority claim is made.

The imported inputs have independent reviewer2 confirmations:
[minimum-pair-three](../../constant_weight_pair_two_review2/REVIEW.md)
at height8080, including a stronger restricted bound60;
[no221](../../constant_weight_mixed_stars_review2/REVIEW.md) at height8128;
and the [eight-class theorem and corrected symmetries](../../constant_weight_2111_classification_review2/REVIEW.md)
at height8214. The last review confirms the corrected orders and gives
actual point-group presentations. Those reviews do not cover the new
paired-star theorem or its global corollary. Independent review of this
new proof is pending; the ordinary reduction and counting bridges are
unformalized. The all-unit case remains open, and this source does not
establish a global upper bound71.
