# Scope of the Gallai calibration

## Why the proposed condition is necessary

Let L be fixed and four-colourable, and choose an inclusion-minimal
selection X of pool vertices for which G=L union X is not four-colourable.
The minimum is taken over X only; no L vertex is deleted. As usual,
every selected vertex has degree at least four: a colouring after deleting
a vertex of degree at most three extends by an unused neighbour colour.

Put T={v in X: d_G(v)=4}. Suppose a connected component B of G[T]
were not a Gallai tree. Minimality gives a four-colouring of G-B.
At v in B, at most 4-d_B(v) colours are forbidden by already coloured
neighbours, so its available list has size at least d_B(v). The classical
degree-choosability theorem colours B from these lists because B is not
a Gallai tree. This extends the colouring to G, a contradiction.
Thus every component of G[T] is a Gallai tree, meaning each block is a
complete graph or an odd cycle.

The cited theorem is recalled in Cranston and Rabern,
[Beyond Degree Choosability](https://arxiv.org/abs/1511.00350),
Electronic Journal of Combinatorics 24(3), 2017, P3.29. The preceding
argument applies it to a fixed-boundary pool. It is prior critical-graph
reasoning, not a new theorem claimed by this package.

For a downward-closed cardinality budget, restricting a counterexample
search to such minimality conditions preserves existence: any
counterexample has an inclusion-minimal pool subset within the budget.
This is not a pointwise assertion that every selection failing the
condition is four-colourable. Removing a reducible component can leave
a smaller non-four-colourable graph.

## The finite limitation

Take the eighteen explicit selections from the three pinned certificate
files named in README.md. Each has 134 pool vertices and all 374 L
vertices, and includes pool points outside the previously closed H574.
The certificate reader reconstructs X=(S minus R) union A. It checks
that all labels are valid and all eighteen supports are distinct.

The old data contains explicit proper four-colourings on supersets of
each selected graph. For the first row, its full L string is read from
the explicitly indexed interface witness; all other rows include L
directly. The checker restricts those strings to H=L union X, requires
a colour in {0,1,2,3} at every retained vertex, and checks every strict
edge. Thus all eighteen H are four-colourable independently of any
historical SAT verdict or interface-completeness theorem.

Direct degree counts include every neighbour in L union X and verify
minimum selected-pool degree four. The checker then lists every vertex
of T(X), every induced edge, and every connected component. Traversal
finds 143 isolated vertices, 13 isolated edges and two paths of order
three across the eighteen graphs. Equivalently, there are 175 low-vertex
occurrences, 17 low-edge occurrences and 158 connected components.
Each component is a tree. A separate union-find cycle test confirms
acyclicity. Since the blocks of a forest are complete graphs of order
one or two, all eighteen low graphs satisfy the full Gallai condition.

In addition, each selection meets every one of the 17,250 distinct
clauses of the specified common base cover. Consequently, adding only
the Gallai condition to that base, the size bound and the minimum-degree
condition leaves all eighteen positive examples feasible. This is the
precise limited sense in which the proposed filter fails the calibration.

The later cuts that these examples produced are already published.
This result does not assert that the examples satisfy all such later
cuts or survive the latest master. Nor does zero rejection on these
eighteen supports imply redundancy over every selection in the pool.

## Complete four-vertex census

The induced graph on U has 303 vertices. An induced C4 or diamond has
a spanning four-cycle. Opposite vertices of this cycle have its other
two vertices as common neighbours. Therefore iterating every unordered
opposite pair and every unordered pair of its common neighbours proposes
every relevant four-set. The degree sequences (2,2,2,2) and (2,2,3,3)
recognize C4 and diamond respectively; both characterize those graphs
among simple graphs on four vertices. Set deduplication removes repeated
proposals without deleting any distinct labelled four-set.

The other enumeration starts a simple closed walk a,b,c,d,a at its least
vertex a and chooses the orientation with b<d. Every spanning four-cycle
has such an orientation. It counts induced edges: four means C4, five
means a diamond, and six is ignored. Exact comparison of the two sorted
outputs gives 2174 C4s and 798 diamonds. The reported hash binds the
whole labelled stream, not only the totals.

Four-cycles and diamonds are not Gallai trees and are useful small
degree-list-reducible blocks when all their vertices have selected
degree four. The census by itself establishes no selected-degree
conditions and removes no candidate. The stronger direct forest check
shows why neither these blocks nor any larger non-Gallai low component
can reject the eighteen tested selections.

## Exactness, controls and limits

The existing reviewed integer reader parses pinned original scale-96
points, rational completion coordinates and the specified pool. It
reconstructs all 228,826 pairs among 677 distinct points with arbitrary
precision integer arithmetic in the bit-mask basis of
Q(sqrt(3),sqrt(5),sqrt(11)). At common denominator 288 it recovers 3400
strict unit edges. No floating-point test is used.

The finite controls cover all 64 labelled graphs of order four and all
1024 of order five, with nonconsecutive vertex labels. Direct comparisons
against all relabellings of explicit C4 and diamond edge patterns agree
with both enumerators. Forest checks agree with an induced-subgraph
definition of acyclicity. The 1088 graph controls do not prove correctness
on arbitrary graphs; the enumeration and forest arguments above supply
that bridge. The actual support witnesses, low-component lists and all
base-cover intersections are recomputed directly.

This is an author-checked exact finite calibration. Independent algorithms
within the package do not constitute an external review, and the two
motif routes share the exact geometry input. Trust rests in the pinned
inputs, reviewed integer geometry, direct graph checks, ordinary Python
execution and the elementary finite arguments. The classical theorem
motivates the filter; the statement that all eighteen low graphs are
forests is verified without invoking that theorem or any solver.

No wider family closure, new colouring cut, new graph-order bound or
five-chromatic graph follows. This completed calibration provides no
observed gain for a Gallai guard on this test set, so a full encoding or
solver pilot based only on it is not started.
