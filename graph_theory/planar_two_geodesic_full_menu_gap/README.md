# Half balance does not imply an unrestricted two-geodesic transversal

There is a **32-vertex simple planar graph with positive edge lengths**
having both of the following properties:

1. Every nonnegative vertex mass has a half-balanced separator equal to
   the union of at most two shortest paths in the original graph.
2. A specified family of **56 pairwise-intersecting connected vertex
   sets** cannot be met by the union of **any** two original-graph
   shortest paths, with arbitrary endpoints. Three such paths suffice.

The second assertion is checked against the **complete** catalog of
528 geodesics, including singletons, and all 139,656 unordered pairs
with repetition. It is not a failure of a selected path menu. Both
properties persist throughout a closed, full thirty-dimensional box of
core edge lengths, with arbitrary positive parent lengths and sufficiently
long remaining face edges.

This is an obstruction to the intersection-family strengthening used
in some separator proofs. It is **not a counterexample to
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf)**:
the graph satisfies the weighted half-balance target. The assertion
here concerns the stated positive edge-length metrics; an unweighted
version of this intersection-family gap is not asserted.

## The explicit graph and metric

The core I is the icosahedron on vertices 0,...,11:

```
0: 1 2 3 4 5       1: 0 2 5 6 10      2: 0 1 3 6 7
3: 0 2 4 7 8       4: 0 3 5 8 9       5: 0 1 4 9 10
6: 1 2 7 10 11     7: 2 3 6 8 11      8: 3 4 7 9 11
9: 4 5 8 10 11    10: 1 5 6 9 11     11: 6 7 8 9 10
```

Its twenty triangles are its faces. Sort their vertex triples
lexicographically and put a new vertex 12+f in face f, starting with f=0.
Join this vertex to all three face corners. This gives a spherical
triangulation G with 32 vertices, 90 edges and 60 faces. The checkers
independently reconstruct oriented face systems and verify vertex links.

In lexicographic order of the thirty unordered core edges, assign prices

```
809,756,790,846,813,797,804,756,808,804,
887,756,800,756,870,837,762,822,859,808,
835,756,812,802,945,756,833,827,775,832.
```

For marks 12,...,31 in order, choose parent corners

```
0,0,0,0,0,1,1,1,2,2,3,7,4,4,5,6,6,7,8,9.
```

Give each of these twenty parent edges length 189 and each of the forty
remaining face edges length 28094. The sum of all thirty core and twenty
parent lengths is 28093. Any two vertices have a path using only these
fifty cheaper edges, of length at most that sum. A shortest path therefore
cannot use a length-28094 edge. **Those long edges remain present for
connectivity and separator calculations.**

The graph, lengths, positive separator certificate and all 56 family
members are in the **2,847-byte [certificate.json](certificate.json)**.
Every family member is encoded by the integer
`sum(2^v for v in C)`, with vertex labels 0 through 31. Thus the file is
an explicit finite witness, not a seed requiring a search or private data.
Its SHA-256 is

```
e181b042fe8fba19c9a35e174e3f2d039393ecf534299a014a17fde48a9c7f0f
```

## Every mass has a half separator

Let the total nonnegative vertex mass be M. If some set of at most four
vertices has mass at least M/2, cover its vertices by two ambient shortest
paths between arbitrary paired vertices, allowing singleton paths. Their
union deletes at least M/2 mass, so all remaining components have mass at
most M/2. This includes the zero-total and equality cases.

Otherwise every component containing at most four vertices is strictly
lighter than M/2. Use the fifteen explicit candidate pairs in the
certificate. Suppose all fifteen fail half balance. For each pair, one
of its residual components of order at least five must then be heavy.
Two disjoint sets cannot both be strictly heavier than M/2.

The certificate's short `positive_trace` repeatedly applies this rule:
if all but one eligible component of a pair are disjoint from already
forced heavy sets, the remaining component is heavy. There are fifteen
such deductions. They force the following four sets to be heavy:

```
C0 = {0,12,13,14,15,16}
C1 = {2,3,7,12,14,17,20,21,22,23,29}
C2 = {3,7,15,20,22,23,27,29}
C3 = {1,6,10,13,17,18,19,21,27,28,31}.
```

Each vertex belongs to at most two of C0,C1,C2,C3. Consequently

    w(C0)+w(C1)+w(C2)+w(C3) <= 2M.

Four strict majorities would instead give a sum greater than 2M, a
contradiction. This proves the all-real-mass assertion. It is the
four-term integer dual certificate with all coefficients one from the
team's [mass-menu duality](../planar_two_geodesic_mass_menu_duality/README.md).

The separate audit does not use the propagation trace. It enumerates
all 8,192 choices of one eligible residual component from each of the
fifteen pairs. Exactly 8,191 choices contain two disjoint sets. The sole
remaining choice forces the four displayed strict majorities and is
excluded by their incidence inequality. This checks the complete finite
mass argument, rather than sampling possible masses. The four-vertex
repair above handles all discarded small components.

The fifteen pairs are alternatives; the separator uses just one pair,
or a pair covering a heavy set of at most four vertices.

## The connected family defeats every geodesic pair

Decode the 56 masks in `family`. The induced subgraph on each set is
connected in the full 90-edge graph. Every two members intersect, as
verified by all 1,540 pairwise intersections.

To certify the complete path quantifier, first observe that cheap face
vertices are leaves of the fifty-edge metric subgraph. A shortest path
between two vertices is therefore obtained by taking their parent
corners, following a core geodesic, and including a marked endpoint when
appropriate. Every endpoint pair has a unique geodesic. There are 496
unordered distinct endpoint pairs and 32 singleton paths, giving 528
paths in total. The independent audit additionally enumerates shortest
paths directly in the full graph from its exact all-pairs distances.
The two complete ordered catalogs agree entry for entry via SHA-256

```
fd069f47af0080c17b908b0b5f187dcc79d5bf0e4d2438325cd273f27a824174
```

For each of the 139,656 unordered geodesic pairs, the checker finds a
family member disjoint from their vertex union. Repetition includes all
single-path choices. Thus no choice of two ambient geodesics meets every
member of the family. This is a finite exact computation on the displayed
graph and family; no omitted path search, solver verdict, or probabilistic
claim is involved.

The three geodesics

```
(0),       (1,2,7),       (4,8,11)
```

together meet every family member. The family's geodesic transversal
number is therefore **exactly three**. No minimality claim is made for
the 32 graph vertices or the 56 family members.

As a direct check that this family cannot itself be realized entirely
by strict majorities, it contains the four masks

```
126977, 547504260, 680558728, 405020738.
```

They lie respectively inside C0,C1,C2,C3 and also have incidence at most
two per vertex. Their masses cannot all exceed M/2. Pairwise intersection
alone is therefore insufficient for the relevant mass inequalities.

## A full-dimensional region with the same complete catalog

Let c_e be the thirty integer prices above. For any common scale
lambda>0, allow independent core prices

    lambda(c_e-1/4) <= L_e <= lambda(c_e+1/4).                  (1)

Choose any positive parent-edge length at each of the twenty marks.
Let T be the sum of these parent lengths and all thirty chosen core
lengths. Give every nonparent face edge any length **strictly greater
than T**. The same graph, family and all-mass certificate retain both
properties throughout this region.

Here is an exact catalog-stability proof; scale lambda to one. The
unweighted core has diameter three. For an endpoint pair at hop distance
h<=3, some h-edge path costs at most h(945+1/4), whereas every longer
path costs at least (h+1)(756-1/4). The latter is strictly greater for
h=0,1,2,3. Only unweighted hop-geodesics can therefore be metric
geodesics. There are 162 such routes, counted with singletons and ties.

Each endpoint pair has a unique winning route P at the center prices.
For each alternative hop-geodesic Q, cancel common edges. The checker
verifies all 84 comparisons and obtains

    min_(P,Q) (c(Q)-c(P)) / |E(P) symmetric_difference E(Q)| = 1/2.

Changing each edge price by at most 1/4 leaves every difference positive.
Thus every core winner stays unique throughout (1). The bound 1/2 here
is the first possible catalog tie radius for these hop-route comparisons;
the theorem deliberately uses the smaller closed radius 1/4. No sharp
threshold for the intersection-family gap is claimed.

The separate audit proves the same stability by a different test. For
each center core geodesic P, it prices P's edges at their upper box bounds
and all other edges at their lower bounds. Deleting each edge of P in
turn and recomputing a shortest path gives 108 strict alternative-path
checks. Every different simple path omits some edge of P, so these checks
cover all competing core paths, including longer ones.

Finally, the nonparent lengths greater than T exclude those edges from
every geodesic, and parent lengths cancel in route comparisons for fixed
endpoints. The full catalog is unchanged. All residual components and
family incidences are combinatorial, so both assertions persist. This
region lies outside the earlier highly asymmetric
[icosahedral price box](../planar_two_geodesic_icosahedron_price_region/README.md),
even up to common rescaling.

## What this obstructs

A half separator for every mass need not supply a two-geodesic
transversal for every pairwise-intersecting connected family, even when
the choice ranges over **all** ambient geodesics. The earlier
[four-menu gap](../planar_two_geodesic_four_menu_gap/README.md)
separates these notions for a prescribed menu on an octahedron; the
present construction establishes the distinction for the unrestricted
path-pair catalog of a planar metric. Neither statement contradicts the
valid implication from intersection transversals to mass balance.

There is also a tree-decomposition consequence. For each connected
family member, the bags meeting it form a connected subtree of any tree
decomposition. These subtrees intersect pairwise, so the Helly property
of subtrees gives one bag meeting all 56 members. Such a bag cannot be
covered by two ambient geodesics. Hence **no tree decomposition of this
metric graph has every bag covered by two ambient geodesics**, despite
the all-mass half-separator property. This is a boundary of that stronger
proof strategy, not an obstruction to the separator itself.

## Reproduction and trust boundary

From the repository root, Python 3.11+ and standard library only:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_full_menu_gap/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_full_menu_gap/audit.py
```

The main checker builds the graph from two pentagonal rings, proves
catalog completeness using the cheap-leaf structure and core route
comparisons, checks all family incidences and geodesic pairs, and verifies
the integer positive proof trace. The separate audit imports no target
Python code. It builds the core from explicit adjacency, orients faces
by dual traversal, computes full-graph Floyd distances, enumerates the
ambient catalog, checks the adverse metric corners, and exhausts the
8,192 component choices. Both scripts finish in seconds on an ordinary
CPU. Exact compact outputs are in [expected.json](expected.json).

Discovery used bounded SMT/SAT searches, but their completeness or
UNSAT claims are not proof premises. The published result requires no
solver, private search history, external dataset or large proof trace.
The finite all-path and component-choice claims are computational; the
arbitrary-real-mass and metric-box conclusions use the written arguments
and their exact finite certificates. The separate audit is by the same
researcher; independent peer review is pending.

Primary background refreshed 29 September 2026:
[Diot and Gavoille, *Path Separability of Graphs*](https://emilie-diot.eu/Article/DG10a)
for weighted path-separator conventions, and the official Problem 31
above for the target. Targeted searches on brambles, path separability
and geodesic transversals did not establish historical priority for this
explicit unrestricted gap. No priority or general open-status claim is
made. The graph certifies half balance; it is not evidence that Problem 31
has a negative answer.
