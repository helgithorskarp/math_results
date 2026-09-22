# Sparse one-skeleta make triangle collapse a matroid

Let K be a finite abstract simplicial complex of dimension at most two. Write
G=K^(1), and assume the **hereditary planar edge bound**

    |E(G[U])| <= 3|U|-6   for every U subset V(G) with |U|>=3.       (H)

In particular, every planar simple graph satisfies (H). K need not be flag,
pure, connected, or embedded in the plane. A collapse to a graph below uses
only elementary pairs (edge, triangle), where the edge belongs to exactly
one remaining triangle. Deleting a triangle means deleting its interior and
retaining all its edges and vertices. Empty complexes are allowed.

## Theorem

For every field F and every subset A of the triangles of K, the following
are equivalent:

1. The columns of the oriented boundary matrix d2 indexed by A are independent
   over F.
2. K^(1) union A collapses to a graph.
3. Every maximal sequence of free-edge/triangle collapses on that complex
   removes all triangles.

These independent sets are the same over every field. Their matroid circuits
are precisely the triangle sets of subcomplexes that are triangulated
2-spheres. In particular, every minimal nonzero 2-cycle support is an actual
triangulated sphere, not merely homotopy equivalent to one.

Consequently, the minimum number of triangles whose deletion permits collapse
to a graph is beta2(K). All deletion sets attaining that cardinality are exactly
the complements of bases of d2. Given any nonnegative real triangle costs,
heaviest-first greedy independence testing produces a basis whose complement
has minimum deletion cost among **all** feasible deletion sets. The same
minimum is attained for the total cost of critical triangles in an acyclic
discrete Morse matching on K. One can simultaneously obtain critical cell
counts (beta0,beta1,beta2). No costs on critical edges or vertices are optimized.

Each connected component is homotopy equivalent to a wedge of circles and
2-spheres. Thus it is aspherical exactly when H2(K;F)=0, equivalently when it
collapses to a graph. Every subcomplex of an aspherical K satisfying (H) also
collapses to a graph. This is a restricted consequence, not a resolution of
the general Whitehead conjecture.

## 1. The closed-core inequality

Let C be a connected pure nonempty 2-dimensional subcomplex with no edge of
triangle degree one. Put v=f0(C), e=f1(C), f=f2(C). Every edge has degree at
least two, so 3f>=2e. Its vertex set has at least three elements and (H) gives
e<=3v-6. Therefore

    chi(C) = v-e+f >= v-e/3 >= 2.

Over any field, chi(C)=1-beta1(C)+beta2(C); hence beta2(C)>=1.
This argument is an elementary special case of the Euler/incidence machinery
used in sparse-complex topology; see [CFH] and [B] in SOURCES.md.

If a maximal free-edge peeling sequence leaves triangles, their pure support
has a connected component C as above. Since there are no 3-simplices, inclusion
of a subcomplex injects its H2: both H2 groups are kernels of boundary maps,
with no quotient by 3-boundaries. Thus an H2-acyclic complex cannot leave such
a core. Elementary collapses preserve homology, proving 1=>3. The implication
3=>2 is immediate; 2=>1 follows because a graph has zero H2. This also proves
the equivalence for every subcomplex, since (H) is hereditary under deletion
of vertices and edges. Order independence of top-dimensional peeling itself
is classical; the new ingredient here is its equivalence with linear
independence under (H), not a new collapse algorithm.

## 2. Circuits are spheres

Take an inclusion-minimal support Z of a nonzero 2-cycle over any field F,
and retain just its triangles and their faces. Every edge has degree >=2:
a single incident nonzero coefficient cannot have zero boundary there.
The triangle adjacency graph, joining triangles sharing an edge, is connected;
otherwise restriction to one adjacency component is a smaller cycle.
Moreover beta2(Z;F)=1: two independent cycles can be linearly combined to
cancel any chosen nonzero triangle coefficient, producing a smaller nonzero
cycle. Thus Z is connected and chi(Z)=2-beta1(Z;F)<=2.

Equality throughout the closed-core inequality now forces

    chi(Z)=2,   e=3v-6,   f=2v-4,   deg_Z(edge)=2 for every edge.

The link of each vertex is a disjoint union of cycles. Split that vertex
into one vertex for each link component. This standard normalization yields
a closed triangulated surface; it remains connected because triangle
adjacency is connected and none of its adjacencies was split. If s is the
total number of additional vertices, its Euler characteristic is 2+s.
A connected closed surface has Euler characteristic at most two. Hence s=0
and the normalized surface is S2. Thus Z was already a triangulated sphere.

Conversely, the triangles of a triangulated sphere form a minimal dependence
over every field: the oriented fundamental cycle exists over Z, and deleting
any triangle kills the kernel, as coefficients propagate across the connected
dual graph. Therefore circuits, and hence independent sets, agree over every
field. This does not assert total unimodularity of arbitrary submatrices or
relative boundary maps.

## 3. Homotopy and the aspherical subcomplex consequence

If H2(K;F) is nonzero, choose a sphere circuit S and any triangle sigma in S.
In L=K minus int(sigma), the loop boundary(sigma) bounds the disk
S minus int(sigma). Attaching sigma is therefore a null-homotopic 2-cell
attachment, giving K homotopy equivalent to L wedge S2 in that component.
Removing sigma decreases beta2 by exactly one (its column was in the span
of the other columns), and leaves (H) valid. Iterate, then use Section 1 to
collapse the final complex to a graph. This proves the wedge description
and in particular torsion-free integral homology.

A component with a sphere summand is not aspherical, since that sphere is
a homotopy retract with nonzero pi2. A graph is aspherical. Thus asphericity
is equivalent to zero H2 in this class; H2 injectivity under subcomplex
inclusion then proves the asserted hereditary collapse property. Wedge
decomposition and related sparse Whitehead consequences have substantial
prior literature [B, CFH]; they are consequences here, not our priority claim.

## 4. Exact weighted deletion and the prior HeCS algorithm

Fix the 1-skeleton and let T be the triangle set. By Section 1, feasible
retained triangle sets are exactly the independent sets of the column matroid
of d2. Its rank is r=|T|-beta2(K). Thus every feasible deletion removes at
least beta2 triangles, and equality holds precisely for basis complements.

The ordinary maximum-weight matroid greedy algorithm sorts T by decreasing
cost and retains a column exactly when it increases rank. For completeness,
at every prefix of this order the retained set is maximal independent in
that prefix, so it has prefix rank. Any independent competitor has at most
that many elements in each prefix. Summation by parts with nonincreasing
nonnegative weights proves the greedy set has at least the competitor's
total weight (ties contribute zero). Hence its complementary deletion cost
is minimum. Nonnegative weights ensure an optimum can be extended to a basis;
with zero costs there can also be optimal non-basis retained sets.

Savostianov--Tudisco--Guglielmi [STG], Algorithm 6.1, already propose
heaviest-first addition tested by free-edge collapse. Under (H), Section 1
makes their accept/reject decision identical to column-matroid greedy.
Thus the result supplies an **exact optimality domain for that existing
algorithm**, and permits a boundary-rank oracle instead of repeated peeling.
Neither their algorithm nor the abstract matroid greedy theorem is new here.
We claim no optimal Hodge-Laplacian condition number or performance benchmark.

## 5. Critical triangles and perfect matchings

Delete a complement D of a maximum-weight basis, then collapse all retained
triangles. Match the resulting edge/triangle pairs. Viewed in the full K,
triangles of D are unmatched, hence have no incoming upward matched arc in
the Hasse diagram; they cannot create a directed cycle. Collapse pairs are
acyclic by their chronological order. In the remaining graph choose a rooted
spanning tree in each component and match each nonroot vertex with its
parent edge. Such a tree matching is acyclic. A directed cycle in a graded
Hasse diagram with a matching would alternate between just two adjacent
dimensions: at its minimum rank, an upward matched arc must be followed by
a downward unmatched arc. Thus combining these two matching levels preserves
acyclicity. Counts are c0=beta0, c2=|D|=beta2 and c1=beta1 by Euler's identity.

Conversely, in any acyclic matching, every noncritical triangle is matched
to a distinct edge. For triangles A and B draw A->B when A differs from B
and contains B's matched edge. A directed cycle here would be a directed
cycle in the matched Hasse diagram. Therefore this auxiliary graph is a DAG.
At a source B, its matched edge is contained in no other remaining matched
triangle. Peel that pair and continue in source order. Hence the set of
matched triangles is independent over every field. Its retained cost cannot
exceed the maximum-weight basis cost proved in Section 4. This establishes
the global lower bound on critical-triangle cost, including matchings with
extra critical cells, and the construction attains it.

## Hypothesis and validation boundaries

The hereditary condition cannot be replaced by the total edge count alone:
the six-vertex triangulation of RP2 has 15 edges and 10 triangles, no free
edges and H2(RP2;Q)=0. Add one isolated vertex: the total count is now
15=3*7-6, while its six-vertex subset still violates (H). This is a precise
counterexample to that weakened hypothesis. The code includes it as a
rejection test, not as an instance of the theorem.

The algorithms are polynomial in the boundary-matrix size when (H) is known
to hold. The supplied small-instance validator checks (H) by all vertex
subsets and is exponential; no polynomial recognition claim is made.
Finite code audits supplement the proof and do not prove its universal scope.
The proof is ordinary mathematics, not proof-assistant formalized or externally
peer reviewed by this package. Priority is unresolved beyond the searched
sources; see the explicit attribution boundary in SOURCES.md.
