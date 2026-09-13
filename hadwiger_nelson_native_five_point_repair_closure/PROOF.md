# Proof of the fixed-base repair exclusion

Use the exact host H and base B defined in README.md. Adjacency throughout
means every strict plane unit-distance pair, including edges between new
points. The verifier reconstructs H, checks its ordered point and complete
edge hashes, and imports the byte-pinned parent specification of B. The
displayed Parts coordinate identification is the accepted parent's result;
the present theorem can also be read directly for its explicit 503 IDs.

## 1. Partial colourings give necessary conditions

For each of the 126 words, let C_i be its non-dot support and c_i its colour
assignment. Direct checks establish B contained in C_i and
c_i(u) unequal to c_i(v) on every unit edge inside C_i. Thus B is
four-colourable. Define O_i=(H minus B) minus C_i.

If the graph on B union S is not four-colourable, then

```
S intersects O_i for every i.
```

Otherwise restriction of c_i is a four-colouring. No completeness claim is
made about the set of all colourings of B or H. These particular positive
words suffice for the finite exclusion.

## 2. Reduction to five new points of degree at least four

Suppose a counterexample S has at most five points. Choose an
inclusion-minimal non-four-colourable S_0 contained in S, keeping B fixed.
Every v in S_0 has at least four neighbours in B union S_0: deleting a
point of degree at most three would leave a four-colouring extendible to v.

There are 585 host points outside B having at least four neighbours in B.
Pad S_0 to exactly five points using distinct such points. There are more
than enough available points. The resulting T remains non-four-colourable,
and every point of T has at least four neighbours in B union T. It is
therefore enough to rule out all five-element T with this degree property.
No minimum-degree assumption is imposed on vertices of B.

Write d(v) for the number of neighbours of v in B. For every component C
of the induced graph H[T], the necessary degree inequalities are

```
d(v) + degree in H[C] of v >= 4  for every v in C.
```

## 3. Components with at least three vertices

Every connected graph on five vertices has a spanning tree of one of
three shapes: a path, a four-leaf star, or the tree of degrees 3,2,1,1,1.
Every connected four-vertex graph contains a path or three-leaf star;
every connected triple contains a path of length two.

`spanning_trees.cpp` enumerates all injective maps of these trees into the
free-point graph and tests the degree inequalities on the full induced
graph. All three five-vertex tree shapes are included. The star leaves
are ordered by combinations; path reversal is removed by ordering the
endpoints; the two equal short branches of the third shape are unordered.
These symmetries remove duplicate maps without removing an image. Additional
duplicates from multiple spanning trees are harmless.

Every qualified five-point image is contained in at least one C_i. This
is checked directly with two unsigned 64-bit omission masks. The three
tree-shape loops check respectively 78,576, 1,277,542 and 1,571,915 qualified
maps, with no uncovered image.

The qualified connected triples and quadruples are canonicalized as sorted
point tuples. There are 18,965 and 175,654, respectively. They agree
entrywise with the separately implemented ESU enumeration, which grows a
connected set through exclusive new neighbours and a fixed least vertex.

If T has a component of order four, its fifth point is an isolated
component and hence belongs to the 585-point high-degree set. All such
quadruple/singleton unions are covered by the C_i. The checker allows even
extra adjacency or overlap in this Cartesian-product test, so it tests a
superset of the required cases.

If T has a component of order three, the other two points either form an
edge and each has d(v) at least three, or they are isolated and each has
d(v) at least four. There are 2,549 qualified free edges. The completion
pool is the union of those edges and all unordered pairs of high-degree
points, giving 172,058 distinct pairs. Every triple/completion union is
covered by a C_i, again with possible overlaps and extra edges allowed.

The Cartesian-product checks are exact bit-set intersections: an item
survives a column precisely when it contains an omitted point for that
colouring. For a fixed triple or quadruple, intersect the columns for
the words that its points do not already hit. An empty intersection says
that no completion can hit all words. This is a direct finite calculation,
not a solver's infeasibility claim.

These checks exclude every T having a component of size at least three.

## 4. Singleton and pair components

An isolated new point must have d(v) at least four; it is one of the 585
singletons, of cost one. In a pair component both endpoints must have
d(v) at least three. If both have d(v) at least four, represent them by
two singleton atoms. Otherwise the edge is one of 1,238 pair atoms, each
of cost two. Thus every remaining T has a representation by these 1,823
atoms of total cost five.

For each atom A define its mask M(A) to contain i exactly when
A intersects O_i. A necessary condition for a non-four-colourable T is
that its atom masks cover every one of the 126 indices. Allowing atoms
to overlap or have additional edges only enlarges this necessary-condition
problem; the actual component representation is included with its exact
cost. A cover by masks alone would not establish non-four-colourability.

`transversal.cpp` verifies that no cover of cost at most five exists. There
can be zero, one or two pair atoms. It checks these alternatives explicitly:

```
0 pairs: at most 5 singletons;
1 pair:  at most 3 singletons;
2 pairs: at most 1 singleton.
```

Pair choices are exhaustive, and distinct pair atoms suffice. Repeating
an atom cannot improve a cover. For the remaining singleton problem, select
an uncovered index i. Any solution must choose some singleton whose mask
contains i. Branch on all those singletons, remove the indices it covers,
and reduce the remaining budget by one. Empty residual sets succeed;
nonempty sets with zero budget fail. Memoization stores only fully checked
failed states. Choosing the rarest uncovered index affects runtime only.
The full C++ computation returns no cover after 2,449,101 calls, with
53,030 memoized states.

The independent Python checker does not split by pair count. It branches
on all affordable atoms covering an uncovered index and subtracts the
atom's weight from the remaining budget. It too returns no cover. Its
1,367,004 cached states are a different decomposition of the same exact
finite condition. Small exhaustive positive and negative instances test
both checkers, including weight-two choices.

Every degree-qualified T must therefore be contained in one of the
verified four-colourable supports C_i, a contradiction. This proves the
theorem for T, and Section 2 proves it for every S of size at most five.
For a requested colouring of an arbitrary S, repeatedly peel new points
of degree at most three, use a covering partial word for the remainder,
then extend in reverse peeling order.

## 5. Scope, arithmetic and trust

The host coordinates are actual radical plane points; equality and unit
distances are exact integer computations in Q(sqrt(3),sqrt(5),sqrt(11)).
The accepted Cartesian geometry implementation and original coordinate
table are byte-pinned. No abstract chromatic graph is substituted for a
plane realization. No floating comparison appears in the verifier.

C++ vertex IDs are below 4,096 and tuple codes use at most five 12-bit
fields, fitting unsigned 64-bit arithmetic. Omission masks have at most
128 bits represented by two unsigned words. Counts and memo keys use
unsigned 64-bit values; recursion depth is at most five. The source
guards mask widths and host size. The full replay is also checked with
undefined-behaviour sanitization. Python integers and bitsets are exact.

The source programs, their completeness arguments, ordinary program
execution, the pinned geometric reconstruction and positive certificate
remain the trust boundary. Both complete computational methods were run
by the author. This is not independent-author review or formalization.
The proof does not use MILP optimality, a SAT timeout, a missing refutation,
or completeness of the heuristic process that found the colourings.

The conclusion concerns this fixed B and this finite H only. In particular,
it does not exclude a smaller five-chromatic subgraph of H that omits points
of B, nor a repair using points outside H.

Related prior graph evidence uses partial-colouring omission sets and bounded
transversals for different Parts interfaces: see the
[two deletion-triple budgets](../hadwiger_nelson_parts509_two_triple_budgets/README.md).
That result fixes the full 374-point large component and a 168-point
completion pool; it does not imply the present six-hole native-host closure.
No novelty claim is made for the general colouring-to-transversal reduction.
