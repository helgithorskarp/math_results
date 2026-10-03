# The four marked low-neighborhood shapes

Actual author **six-books-3**, role **researcher**, 2026-10-03.

This is the ordinary local coverage lemma used by the explicit profile7
exclusion in PROOF.md. It is an elementary small-graph classification,
with two complete same-author enumeration mechanisms; no historical
priority, independent-person review or proof-assistant formalization is
claimed. On its own it does not exclude a whole22-point host.

Let J be a triangle-free simple graph on nine points, with one distinguished
degree-two point w and every other degree three. Suppress w: its two
distinct neighbors u,v are nonadjacent, because J has no triangle. Replacing
u-w-v by uv gives a simple cubic graph C on eight points with a marked
edge e=uv. Every triangle of C contains e. Conversely subdividing such
an edge eliminates every triangle and gives precisely this degree sequence.

C is connected. A component of a simple cubic graph has at least four
vertices. If an eight-point cubic graph were disconnected it would be two
four-point cubic components, both K4. Their triangles cannot all contain
one marked edge.

Every triangle of C contains e, so their number is at most two: the
endpoints of e have just two additional neighbors each. If there were two
triangles, their union would be a diamond with four vertices and five
edges. Its two degree-two vertices have one outside edge each, while
the endpoints of e already have degree three. Since C has twelve edges,
the four outside vertices would induce five edges. A triangle-free graph
on four vertices has at most four edges: a fifth edge in a four-cycle is
a diagonal creating a triangle, while a graph with no cycle has at most
three edges. Thus an outside triangle would avoid e, a contradiction.

If C has exactly one triangle T, its three vertices each have one outside
neighbor. These three neighbors are distinct, since a shared neighbor of
two triangle vertices would create another triangle. The remaining five
points induce a triangle-free graph with six edges and degrees2,2,2,3,3.
A triangle-free five-point graph with six edges is K2,3. Indeed, an odd
cycle would have length five and use every point; its required extra edge
would be a chord producing a triangle. Therefore it is bipartite, and six
edges force a2/3 bipartition with all cross edges. C is consequently a
triangle whose three vertices are matched to the three degree-two points
of K2,3. The marked edge must be a triangle edge; all three are equivalent
under the actual permutations of this explicitly defined local graph.

If C has no triangle, it has a four-cycle. Otherwise, from any root its
three neighbors and their six other neighbors would all be distinct,
requiring ten points: overlaps would create a triangle or four-cycle.
Each four-cycle point has one outside neighbor, so exactly four edges
cross to the remaining four points. The outside induced graph has four
edges and no triangle; it is another four-cycle. Thus the cut is a perfect
matching between two four-cycles.

Normalize the matching so the first cycle is0-1-2-3-0 and its partners
are4,5,6,7. There are three possible outside four-cycles. One has the
same order as the first cycle and gives the cube Q3. The other two orders
are exchanged by a symmetry of the first cycle and give the Wagner graph,
explicitly the cycle0-1-...-7-0 plus the four opposite edges i-(i+4).
The supplied literal normalized graph transports also check this step.
In a cube, coordinate permutations and translations are transitive on
edges. In the Wagner graph, rotations/reflections are transitive on cyclic
edges and separately on opposite edges. A cyclic edge belongs to one
four-cycle and an opposite edge to two, so the two marked classes differ.

There are exactly four marked neighborhoods: subdivide a cube edge;
subdivide a Wagner cyclic edge; subdivide a Wagner opposite edge; or
subdivide a triangle edge in the triangle/K2,3 core. Isomorphisms of J
must preserve its unique degree-two point and hence its suppressed marked
edge. The four J representatives are pairwise distinguished by
(total four-cycles, four-cycles containing w): (4,0),(3,0),(2,0),(4,1).
Their row masks are generated in root_cut/neighborhoods.py and independently supplied by root_cut/check_rows.py.
They all satisfy the stated degree, connectedness and triangle hypotheses.

Two complete finite domains corroborate, and give a reproducible certificate
for, this ordinary classification. The producer fills all labelled simple
cubic-eight degree margins in lexicographic vertex order, with no triangle
or connectedness pruning. At each step its combinations select every still
needed incident edge to later vertices. A feasible graph follows exactly
one branch; a degree shortage among remaining positive margins cannot occur
on its branch. All19355 labelled cubic graphs are generated. Every edge
belonging to every triangle is subdivided. A full literal vertex bijection
transports every resulting graph and its marked edge to one of the four
representatives. This gives50400 labelled marked neighborhoods.

The distinct physical generator chooses the distinguished ninth point's
two neighbors among all28 choices, then fills the other eight degree-three
margins, rejecting a triangle immediately when its last edge is added.
It reads no cubic graph or producer inventory. All50400 resulting adjacency
tuples agree entry by entry with the producer set; there are no duplicates.
Completeness follows because a target's marked neighbors are selected, its
remaining degree choices occur in the recursive combinations, and none of
the degree/triangle tests can reject it. The same author wrote both algorithms;
this is not external review or proof-assistant formalization.

The complete adjacency-tuple inventory is1692001 canonical bytes, SHA256
`57f2a5e464354eb427d1818589988a038335a42ed05709b8f3118d4dd785f4f8`.
Class counts are10080 cube,20160 Wagner cyclic,10080 Wagner opposite and
10080 triangle/K2,3. The entire mathematical result agrees under normal
Python and Python-O. Work totals1067360 recursion/branch/witness charges,
under the same2M/40s internal/45s child limits, threads1 and one intensive
mathematical child. No stopped or incomplete domain supplies these counts.
The large inventory regenerates in the chosen local work directory; only compact source is distributed.

For profile7 this leaves FOUR local shapes with the degree-two point's
prescribed low type. Root0's other eight types are the multiset
{3,5,5,7,9,9,11,13} in numeric four-bit masks. Types ALONE have
8!/(2!*2!)=10080 assignments per representative. They do not specify
which type5 and type9 point carries the row2 and row3 deficit. Including
these marks makes all eight tags distinct:

    (3,4),(5,0),(5,16),(7,0),(9,0),(9,64),(11,0),(13,0),

where a tag is (low-type mask, entire deficit-column code). The distinguished
point has tag(3,1). Therefore each representative has8!=40320 fully marked
assignments BEFORE any admissible label quotient,161280 in total. One must
not use the40320 TYPE-only total as a complete marked-frame domain.

Equivalently fix the displayed eight distinct tags at point labels0..7
and tag(3,1) at8. The COMPLETE50400 labelled graph inventory just generated
already covers every fully marked physical root0 neighborhood. Its literal
transports to the four representatives give an independent normal-form
description; no additional type-assignment computation is assumed. No individual neighborhood is asserted to lift to a host; the separate complete cut proof in PROOF.md excludes all50400. Every actual profile7 host would
choose such a tagged graph and satisfy the marked root cut in PROOF.md.
This necessary interface assumes no actual host automorphism. The complete necessary high-to-high cut is excluded in PROOF.md, so no B-high graph can complete it.
