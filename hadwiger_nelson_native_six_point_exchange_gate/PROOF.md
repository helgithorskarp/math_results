# Exact closure of the native six-point exchange gate

## Statement and geometry

Use the exact host H and fixed base B defined in README.md and pinned by
SOURCE_PINS.json. Write F = H minus B. The graph on any point set contains
**every** pair at Euclidean distance one. Points are distinct; a crossing of
drawn edges creates no new vertex. The coordinates are actual real plane
points in a multiquadratic field, not abstract graph labels with an assumed
realization.

**Theorem.** For every S subset F with |S| <= 6,
chi(H[B union S]) <= 4.

**Corollary.** For every R subset B and S subset F with |S| <= 6,
chi(H[(B minus R) union S]) <= 4. In particular, a six-point insertion followed
by one old-point deletion cannot attain a five-chromatic 508-point graph.
The corollary follows by restricting a colouring from the theorem.

No assertion concerns selections using more than six F points, points outside
H, arbitrary sub-509 unit-distance graphs, or any lower bound on the HN number.

The exact pinned geometry reconstructs H from A and its oriented unit steps.
Coordinates have denominator 96 and the compact form

```
x = (a + b sqrt5 + c sqrt33 + d sqrt165)/96,
y = (e sqrt3 + f sqrt15 + g sqrt11 + h sqrt55)/96.
```

The independent Cartesian radical routine rebuilds the points and all
7,677,321 unordered pairs. Complete point and edge hashes are checked by the
pinned parent loader. The result is 3,919 points and 29,125 strict unit edges.
The base B is the explicit sorted 503-element pinned list. Its match with the
Parts record drawing was independently reviewed in the native-contact parent;
this theorem needs only that explicit list and the present positive words.

## Positive words and the minimum-degree reduction

There are 166 distinct partial four-colourings w_i of H, each retaining B.
For every retained edge uv the verifier checks w_i(u) != w_i(v).
Let O_i be the free points omitted by w_i. A set B union S with no four-colouring
must meet every O_i. Associate to each free point v the bit mask
M(v) = {i : v belongs to O_i}; a set S is unaccounted for by these positive
words exactly when the union of its point masks covers all indices.

Suppose a counterexample of size at most six exists. Choose T subset S minimal
such that B union T has no four-colouring. T is nonempty because B is coloured
by every w_i. Every v in T has at least four neighbours in B union T: otherwise
a colouring after deleting v extends to it using one of four available colours.

There are 585 free points with at least four neighbours in B. Pad T to exactly
six points using unused points from this pool. The resulting S' still contains
a non-four-colourable subgraph and every new point has degree at least four in
B union S'. Thus it suffices to cover all six-element free selections satisfying

```
d_B(v) + degree in H[S'] of v >= 4     for every v in S'.
```

For a component C of H[S'], this condition is determined entirely by C and B.
Call a connected free set qualified when it satisfies that condition.

## Large connected components

Every connected six-vertex graph contains a spanning tree of one of the six
unlabelled tree shapes. They are: the five-leaf star, the six-vertex path, the
broom of degrees 4,2,1,1,1,1, the double star of degrees 3,3,1,1,1,1, and the
two three-arm trees with arm lengths (3,1,1) and (2,2,1).

`tree_six.cpp` maps each tree injectively into the free unit graph. It removes
only tree automorphisms: leaf order, path reversal, center swap, or equal-arm
swap. Therefore every six-vertex connected set occurs at least once. The code
always tests degree using **all induced free edges**, including edges not in
the mapped tree. At a prefix of k assigned vertices, each current vertex can
gain at most 6-k neighbours; the degree pruning uses precisely this safe bound.

The qualified map counts in the stated shape order are:

| Shape | Qualified maps | Uncovered |
|---|---:|---:|
| Star | 108,070 | 0 |
| Path | 13,875,371 | 0 |
| Broom | 2,835,645 | 0 |
| Double star | 2,333,001 | 0 |
| Arms (3,1,1) | 11,218,756 | 0 |
| Arms (2,2,1) | 11,348,724 | 0 |

Maps can share a vertex set. A separate ESU connected-set enumeration uses the
minimum vertex as root, an extension list, and neighbours exclusive of the
already assigned prefix. This is a different organization of the search: each
connected set has one growth branch. It counts 21,289,412 qualified six-point
sets after 127,004,782 depth-six visits. Every one is covered by one of the
original 126 words. Full small-graph entry comparisons test both mechanisms,
including all six trees as deliberately uncovered positive instances.

`smaller_trees.cpp` enumerates the one, two and three spanning-tree shapes on
three, four and five vertices respectively, then canonicalizes and deduplicates
the qualified images. Their 18,965 / 175,654 / 1,856,054 entries match a separate
ESU list entrywise. These finite lists contain every possible smaller component.

## Component completions

There are 585 qualified singletons H_1, and 2,549 qualified free edges H_2.
An edge is qualified exactly when both endpoints have at least three neighbours
in B. Let P_2 consist of H_2 and every pair of distinct H_1 points. It has
172,058 entries. It includes all possible two-point component remainders.

A completion table indexes an item j under bit i precisely when its vertex
set meets O_i. Intersecting the table's postings for every still missing bit
returns exactly those completion items that cover all the missing bits.
There are no floating-point operations or solver premises in this check.

The following joins have no uncovered entries under the original 126 words:

1. Each qualified connected quintuple with every H_1 singleton.
2. Each qualified connected quadruple with every P_2 item.
3. Each qualified connected triple with every other qualified connected triple.

These contain partitions 5+1, 4+2, 4+1+1 and 3+3. Extra cross edges and overlaps
are allowed by the joins, enlarging the checked domain rather than omitting
any genuine component partition.

For a triple followed by components of size at most two, use singleton/pair
atoms as defined below. The remaining budget is three. Pick an omission index
still uncovered by the triple. Some atom in any completion must hit it. Try
all such atoms: after a singleton use P_2, and after a pair use H_1. This is an
exhaustive branching argument. It covers both 3+2+1 and 3+1+1+1, including
all ways the selected omission index can be hit.

Thirteen distinct six-point unions survive the original words. Every union
is covered by an added positive word. `positive_cases.json` supplies their
full 509-point four-colourings in sorted B-union-S order; verification also
rebuilds the actual induced edge set and checks each complete word directly.
Overlaps are not silently discarded: the public verifier checks every union
returned by the join, and observes that the residual unions all have six points.

## Components of size at most two

If every component has at most two vertices, each singleton has d_B >= 4.
Each pair has both endpoints of base degree at least three. A pair with both
base degrees at least four is represented by its two singleton atoms.
The remaining 1,238 pairs, at least one endpoint having base degree exactly
three, are cost-two atoms. Together with the 585 cost-one singletons this gives
1,823 atoms. Each atom mask is the union of its point masks.

Every genuine selection with these component sizes yields a set of atoms of
total cost six covering every omission index. Permitting overlaps or unwanted
cross edges is harmless for the necessary-condition direction. Repeated atoms
cannot add coverage and can be removed from any proposed cover.

`cover_six.cpp` recursively chooses an uncovered index and tries every atom of
affordable cost that covers it. After choosing an atom, it removes all indices
covered by that atom and subtracts its cost. The empty remainder succeeds; zero
capacity with a nonempty remainder fails. Induction on capacity proves the
recursion complete. Memoization caches only failed (remainder, capacity)
states; its storage cap can reduce performance but cannot alter the answer.

The weighted recursion reports no cover after 57,690,746 calls and 1,372,341
stored failed states. (The discovery ordering of the same words used 124 more
calls; the verdict is independent of word order.)

`split_cover.cpp` separately exhausts zero, one, two and three distinct pair
atoms. With q pairs selected it uses an exhaustive singleton-cover recursion
of capacity 6-2q. At q=3 it directly checks the union of the three pair masks.
This algorithm uses a different decomposition from the weighted recursion.
All four cases fail; the singleton recursion makes 76,546,138 calls with
2,345,228 stored states. These two finite computations establish the required
absence of an atom cover. A native SAT UNSAT response, MILP infeasibility,
timeout or floating-point optimum is never used as a proof step.

All partitions of six have now been covered. This contradicts the existence
of S' and proves the theorem and its old-point exchange corollary.

## Arithmetic and validation boundaries

The geometry calculation uses unbounded Python integers in the independent
basis of Q(sqrt3,sqrt5,sqrt11). The finite set searches use unsigned 64-bit masks:
two blocks for 126 words, four allocated blocks for up to 256. Shift positions
are reduced modulo 64. Five-vertex IDs use 12 bits per vertex with n <= 4096;
only 60 bits are packed. The six-vertex enumeration uses an array, never a
72-bit value in a 64-bit integer. Degree counts fit an ordinary int; all
native statistics fit unsigned 64-bit integers. Memory has no semantic role.

Twenty small graph cases compare complete sets with brute-force combinations,
including 398 positive uncovered sets. Ninety brute-force cover instances
include 74 positive cases and word widths 1,5,65,128,166,256. They validate
both exact cover algorithms and cost cases through six. Four malformed positive
words are rejected. C++ undefined-behaviour sanitization passes these controls.
The full frozen verifier also runs with Python assertions disabled.

These are author-run independent algorithms and definition-level controls.
Independent-author review and formal proof are not claimed. Source transcription,
explicit completeness arguments, compiler/interpreter execution and positive
certificate checking remain the trust boundary.

## One changed-geometry construction pilot

The separate pilot uses rho' = (7+i sqrt(51))/10, of norm one. Coordinates are
in Q(sqrt3,sqrt11,sqrt17), with denominator 120 and compact basis

```
x = (a + b sqrt17 + c sqrt33 + d sqrt561)/120,
y = (e sqrt3 + f sqrt51 + g sqrt11 + h sqrt187)/120.
```

The radius-squared 5/3 shell of L has 36 points. For a point p on that shell,
|p-rho' p|^2 = (5/3)(2-2(7/10)) = 1, giving a concrete reason to test this
new direction. The pilot regenerates L from the pinned source using Cartesian
radical multiplication, then multiplies by rho' and deduplicates exact tuples.
An independent generic multiplication table reconstructs every squared distance.
There are 3,919 points and 29,096 complete unit edges. The supplied 3,919-digit
word is proper on all of them, proving this alternative host four-colourable.
That is a second, separately scoped failed construction gate, not a deduction
about other shells or rotations. Its full graph and SAT discovery logs remain
local; the public positive word and exact generator suffice for reproduction.
