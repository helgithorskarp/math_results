# The exceptional profile is impossible

## 1. Self-contained finite incidence theorem

Let `V` be a twelve-point set. There do not exist families `A,B` satisfying
all of the following conditions:

1. `A` consists of twelve distinct five-subsets; every point has degree five.
2. `B` consists of eight distinct six-subsets; every point has degree four.
3. Every pair of `V` is contained in a member of `A`.
4. Every triple of `V` is contained in a member of `A` or `B`.
5. Every triple is contained in at most two members of `A`.
6. Every pair is contained in at most five members of `A` and `B` together.

This finite theorem is the new result proved by the computation below.
It imports no earlier classification or solver result. The application
to a twenty-block covering imports the two facts specified in Section 9.

Write `alpha(p,q)` and `beta(p,q)` for pair multiplicities in `A` and `B`.
Fix `p` in `V`. The five `A` blocks containing `p`, after deleting `p`,
give five distinct four-subsets `R_i` of the other eleven points. The four
`B` blocks through `p` give four distinct five-subsets `S_j` there.

The `R_i` cover all eleven points, by condition 3. For a remaining point
`x`, its nonempty column support is the set of indices `i` with `x in R_i`.
There are eleven such columns, with total weight twenty, and each of the
five rows has weight four. Two column supports intersect in at most two
rows, by condition 5. Distinct rows intersect in at most three points.

Two remaining points form a pair missed by every `R_i` exactly when their
column supports are disjoint. Let `G` be this missed-pair graph. Condition 4
requires the four `S_j` to cover its edges.

For each remaining point `x`, its combined degree in `R` and `S` is at most
five, by condition 6. It is also at least three: adjoin a new symbol `h` to
each `R_i`. These five five-subsets together with the four `S_j` cover every
pair of the twelve-point set `{h} union (V minus {p})`. A block containing
`x` covers only four of its eleven incident pairs.

Thus the complete local problem has explicit degree bounds

```
max(0, 3 - |column(x)|) <= degree_S(x) <= 5 - |column(x)|.
```

## 2. Complete census of the through systems

`census.py` represents a column of weight at least three by its support in
the five rows. Call these heavy supports. Each may appear only once:
two equal supports of size at least three violate condition 5. Any two
heavy supports have intersection at most two.

Relative to eleven nonempty columns of weight one, there are nine excess
incidences. Every heavy support uses at least two, so there are at most four
heavy supports. Exhaust all subsets of the sixteen supports of weights
three, four, or five, subject to the excess budget and row degree bounds.
Take the least image under all 120 row permutations. There are 22 heavy-set
types. This is a normalization of the five rows, not an assumption about
automorphisms of a global covering.

For a fixed heavy set `H`, let `m_ij` be the number of weight-two columns on
row pair `{i,j}`. Their total is forced to be

```
sum m_ij = 9 - sum_(c in H) (|c|-1).
```

Enumerate every nonnegative ten-entry vector with this sum. Impose only:

- the remaining degree at each row is nonnegative;
- `m_ij` plus the number of heavy supports containing `{i,j}` is at most
  three, because the four-subset rows are distinct.

The singleton count in each row is its remaining degree to four. These
conditions reconstruct exactly eleven columns. Quotient the edge vectors
by the stabilizer of `H` in the explicit row-permutation group. This gives
exactly **736** through-system types. Their maximum row-overlap counts are
2 types of overlap one, 390 of overlap two, and 344 of overlap three.

The independent census does not use heavy supports or multigraphs.
It adjoins four-element rows one at a time, splitting the current column
cells according to membership in the new row. For every cell of size `n`,
it tries every split from zero through `n`, with total new-row size four.
It retains only distinct rows, pair-of-column multiplicity at most two,
and enough remaining incidences to cover the zero cell. Canonicalization
uses every permutation of the currently constructed rows.

The successive numbers of states are `1,4,19,157,736`. Every new row in a
completion determines one of the enumerated cell splits, and a relabeling
of a partial system transports all its extensions. Hence the incremental
quotient is complete. Its final canonical state set agrees entry-for-entry
with the heavy-support census.

## 3. Complete local completions

For each of the 736 types, `local.py` decides whether four five-subsets can
cover `G`. There are 462 possible five-subsets. Represent each by the mask
of graph edges it covers. Duplicate masks and masks contained in another
may be removed for this necessary relaxation, which allows repetition.

For uncovered edges `U` and allowance `k`, the exact recurrence accepts
empty `U`, rejects nonempty `U` at `k=0`, and tests a single candidate
directly at `k=1`. Otherwise it chooses an uncovered edge and branches on
every candidate covering that edge. Every possible cover has such a block.
The count of uncovered edges cannot exceed `k` times the maximum remaining
single-block coverage. Also, a vertex of remaining graph degree `d` needs
at least `ceil(d/4)` more incidences; their sum cannot exceed `5k`.
These are necessary bounds, and memoization changes no choice.

Exactly **22** through types admit a four-block cover. For these,
`complete.py` enumerates every actual set of four distinct five-subsets
satisfying the displayed point-degree bounds. This second enumeration uses
all 462 blocks, including those whose coverage masks were dominated.
The earlier relaxed recurrence is only a necessary pruning oracle.

It again branches on a missed edge, tries every possible next block, and
tracks actual point degrees. It imposes no increasing-index restriction
that could conflict with the chosen edge. Complete unordered solutions
are deduplicated only after being found. There are exactly **72** labelled
completions across the fixed 22 through representatives. `LOCAL.json`
records these small fixtures and is checked against the regenerated result.

### Independent dual completion enumeration

`audit_local.py` assigns to each of the eleven points a four-bit signature,
indicating which away blocks contain it. The signature has weight within
the displayed bounds and at least `ceil(degree_G(x)/4)`. Signatures on
adjacent vertices of `G` must intersect. Each of the four row bits must
occur exactly five times.

The recursion exhausts all these assignments. A full away-row symmetry is
handled by permuting rows that have identical histories on the already
assigned points. In each such class, the next signature selects an initial
segment; every assignment has a representative of this form. Distinct
histories are never interchanged by this normalization. Point-domain and
remaining row-capacity tests are necessary conditions only.

This gives no completion for the other 714 types and the same entire set
of 72 completions for the 22 positive types. It uses neither the primal
set-cover recurrence nor its coverage-mask dominance reduction.

## 4. Exactly 36 pointed-link classes

Any point automorphism of a fixed through system permutes its five rows.
Conversely, a row permutation preserving the multiset of column supports
can be lifted by every bijection between the corresponding column classes.
`symmetry.py` lists all 120 row permutations and every such column-class
bijection, and explicitly checks each resulting point action.

Apply this full group to the 72 completions. There are **36** orbits,
recorded in `LINKS.json`. Through systems belonging to different census
classes cannot be identified. Within a fixed through system, the explicit
group is the full point automorphism group, so this quotient loses no link.

Every resulting link has a point `q` with `alpha(p,q)>=3`. This fact is
checked from the complete positive catalogue; the earlier sharp local
obstruction is not an extra premise of the present finite theorem.
Choose `q` with largest `alpha`, then smallest `beta`, then smallest label.
Choosing a specific such point only fixes a branch of a hypothetical
global system; no global symmetry is assumed.

## 5. Joining two complete links

Normalize the first low point to `p=11`. A template supplies its five
through rows and four away rows after deleting `p`. Restore `p` to obtain
five fixed members of `A` and four fixed members of `B`.

For the second point `q`, try each of the 36 local templates and every
marked column having the required pair `(alpha(p,q), beta(p,q))`. The
marked column must map to `p`.

The two complete links share exactly `alpha` through blocks and `beta`
away blocks. After deleting both centers, these are respectively
three-subsets and four-subsets of ten remaining points. For each family,
try every correspondence between source and target shared rows. A point's
membership signature in these shared rows determines its column cell.
Cell sizes must agree. Within every matched cell, enumerate every bijection.

This exhausts every point relabeling that could identify the shared blocks:
any such map induces one of the row correspondences, preserves its cell
signatures, and restricts to one of the enumerated cell bijections.

Restore both complete links and take their union. It has `10-alpha`
through blocks and `8-beta` away blocks. Reject a union only if:

- some through degree exceeds five or away degree exceeds four;
- a through triple already has multiplicity greater than two;
- a combined pair already has multiplicity greater than five.

All these conditions are inherited directly from Section 1. Equal unions
are deduplicated by exact sorted block lists, not by an unproved isomorphism
test. The 36 roots give 31880 raw embeddings, 872 compatible embeddings,
and **254 distinct partial systems counted separately by root**.

No survivor has `alpha=4` or `5`. Every survivor has `(alpha,beta)=(3,1)`.
Thus every survivor has seven through blocks and seven away blocks.

### Independent joining audit

The audit uses all 72 labelled completions for both centers, without the
36-class orbit reduction. It backtracks over point bijections directly.
Point degrees in the two colored shared-row families must agree; after
each point assignment, every source row must still have a target row with
the same assigned membership pattern. At a complete bijection, distinct
source rows have distinct images, so preservation with equal family sizes
is equality of the two colored row families.

This procedure uses neither shared-row permutations nor their column-cell
bijection product. For each of the 36 representative roots it reproduces
the primary compatible unions entry-for-entry. It also processes every
other labelled root and closes all of its unions independently.

## 6. The eighth away block is forced

Every remaining block avoids both centers, because their complete point
links have already been fixed. A survivor has exactly one away block left.
For a point `x`, let `d(x)` be four minus its current away degree.

If some `d(x)` exceeds one, a single additional block cannot repair it.
This excludes **142** of the 254 partial systems. For the other **112**,
the eighth away block is exactly `{x : d(x)=1}`. Its size is six because
the total away deficit is `8*6-7*6=6`. It avoids both centers, so is distinct
from every already fixed away block.

After inserting it, five through blocks remain. Each is a five-subset of
the ten points outside the two centers. There are exactly **252** candidates.

## 7. Small exact weight certificates

For each of these 112 cases, let `U` consist of:

- every pair not covered by the seven fixed through blocks;
- every triple not covered by those through blocks and the eight fixed
  away blocks.

Each member of `U` must be covered by a remaining through block. A pair is
a requirement because of condition 3; a triple because of condition 4.
Pairs and triples may be weighted together: for any family covering them,
the sum of block capacities is at least their total weight.

`weights.json` assigns positive integer weights to some members of `U`,
with every unlisted member having weight zero. The verifier checks that
every listed set is genuinely required and every weight is a positive
integer. For total weight `W`, it checks the capacity `M` against **all**
252 five-subsets, with no further restrictions on their point margins,
pair multiplicities, or through-triple multiplicities.

Every certificate satisfies

```
W > 5 M.
```

Five remaining blocks have total capacity at most `5M`, a contradiction.
Across all certificates there are 1995 weighted sets, maximum weight five,
and minimum strict gap one. All 28224 capacity checks are exact integer
computations. The certificate file is approximately 23 KB.

Floating-point linear programming discovered weights, which were reduced
to small integers afterward. No LP answer or rational reconstruction is a
premise: the complete published certificates are checked exactly.

## 8. Independent final exclusion and trust

The audit does not read `weights.json`. For every joined system from all
72 labelled roots, it independently reconstructs the away degree deficits
and the forced final block. It then uses a complete set-cover recurrence
on all 252 five-subsets and all uncovered pair/triple requirements. Repeated
rows and dominated coverage replacement are allowed in this relaxation.
Even five unrestricted rows cannot cover the requirements.

The main and audit proof paths use different local censuses, different
completion encodings, different joining algorithms, and different final
obstructions. Both share the mathematical local-link reduction, exact
input parameters, and Python/hardware trust. Matching implementations are
internal validation rather than external peer review. The theorem is not
formalized in a proof assistant.

The result assumes completeness of the written finite loops and the
normalization arguments just given. Neither program contains a deadline,
node cap, heuristic stopping criterion, or solver dependency. Small stored
fixtures are reconstructed and compared, not trusted as census axioms.

## 9. Application to the exceptional covering profile

Suppose twenty six-subsets cover all triples of a thirteen-point set and
have profile `(12,9^12)`. Let `h` be the point of degree twelve. Delete `h`
from its twelve incident blocks to obtain `A`; the eight blocks avoiding
`h` form `B` on the other twelve points.

At any low point `p`, its link is a nine-block `(12,5,2)` covering. Import
the earlier theorem that every point in such a link has degree at most
five. Thus the original codegrees `lambda(h,p)` are at most five. Their
sum is sixty, so all twelve equal five. This gives through degree five
and away degree four at every low point. The same theorem gives combined
low-pair multiplicity at most five.

The original covering gives pair coverage by `A` and triple coverage by
`A union B`. Import the earlier through-triple exclusion: no low triple is
contained in three through rows. These are precisely all the hypotheses
of the finite theorem, giving the contradiction.

The two imported theorems are separate assurance boundaries. The optimal
link degree bound has an independent accepting review. The through-triple
bound is the orbit-52 closure together with its stated predecessors; its
large upstream SAT corpus is not independently replayed here. Neither
the earlier six-class two-intersection census nor the residual optima table
is needed as a premise of the new finite obstruction.

Finally, every point of a twenty-block covering has degree at least nine,
using `C(12,5,2)=9`. The thirteen degrees sum to 120, so their excess over
nine sums to three. The three possible profiles were
`(10^3,9^10)`, `(11,10,9^11)`, and `(12,9^12)`. Removing the last leaves the
first two. The argument does not show whether either remaining profile is
possible, and does not settle `C(13,6,3)`.
