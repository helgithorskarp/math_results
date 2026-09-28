# Weighted guarded descent for two planar geodesics

For a finite graph \(G\) with nonnegative vertex masses \(w\), let
\(B_w(G)\) mean that two (possibly singleton) shortest paths of **the
current graph** have a union \(S\) for which every component of \(G-S\)
has mass at most \(w(V(G))/2\). Write \(B_w^*(F)\) when \(B_w(H)\) holds for
every spanning subgraph \(H\subseteq F\) and every such mass assignment.
All graphs and paths here are finite and unweighted; disconnected graphs
are allowed. This is a strengthened setting for [Barbados 2026, Problem
31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf), not a
resolution of its universal question.

## All-order lemmas

**Five-vertex residual lemma.** Suppose \(F\) is \(K_5\)-free and has two
shortest paths \(P,Q\) such that every component of
\(F-(V(P)\cup V(Q))\) has at most five vertices. Every spanning subgraph
\(H\subseteq F\) that retains the edges of \(P\) and \(Q\) satisfies
\(B_w(H)\) for every nonnegative mass assignment. Consequently, if
\(B_w^*(F-e)\) holds for every edge \(e\) of \(P\cup Q\), then
\(B_w^*(F)\) holds.

Proof. Retained paths remain shortest in \(H\), since deleting edges
cannot create a shorter route. Delete their union. If every remaining
component has mass at most half, they are the desired paths. Otherwise
there is a unique heavy component \(D\). It lies inside one original
residual component, so \(|D|\leq5\), and \(H[D]\) is connected. Every
connected \(K_5\)-free graph on at most five vertices has its vertices
covered by two ambient geodesics: for at most four vertices, pair the
vertices and join each pair by a shortest path in \(H\); for five
vertices, a connected nonclique contains an induced three-vertex path,
which is an ambient geodesic, and the other two vertices are endpoints
of a second geodesic. Delete these two paths. Any surviving component
has mass at most \(w(V(H))-w(D)<w(V(H))/2\). If an edge of the original
paths is absent from \(H\), then \(H\subseteq F-e\), giving the final
assertion. The covering threshold is sharp for this argument: the six
vertices of \(K_{1,5}\) cannot be covered by two shortest paths, since
each contains at most two leaves.

**Guarded two-stage lemma.** In an arbitrary graph \(F\), let \(P,Q\)
be shortest paths. Suppose each component \(C\) of their complement
is covered by a (component-dependent) pair of shortest paths
\(R_C,T_C\) of \(F\). Let \(E_*\) be the union of all edges in these
primary and secondary paths. Then every spanning \(H\subseteq F\)
retaining \(E_*\) satisfies \(B_w(H)\). If \(B_w^*(F-e)\) holds for
every \(e\in E_*\), then \(B_w^*(F)\) holds.

Proof. All protected paths remain geodesic in \(H\). If the primary pair
fails, its complement in \(H\) has one component \(D\) of mass greater
than half. That \(D\) is contained in one \(C\). The designated
secondary pair covers \(C\), hence removes \(D\). Every remaining
component has mass at most the total mass outside \(D\), which is less
than half. The edge-deletion statement follows by splitting spanning
subgraphs according to whether all protected edges are present.

**Component and treewidth terminals.** If each connected component
\(F_i\) satisfies \(B_w^*(F_i)\), then \(F\) satisfies \(B_w^*(F)\):
either no component is heavy, or apply its weighted separator inside
the unique heavy component. Every graph of treewidth at most three
satisfies \(B_w^*\). Indeed, in each connected component, place vertex
masses on bags of a width-three tree decomposition and take a weighted
centroid bag. The at most four vertices of that bag lie on two ambient
geodesics, while every component outside the bag has mass at most half.
The treewidth condition persists under edge deletion.

## Exact planar method-separation example

`verify.py` specifies a simple 16-vertex graph \(F\) by adjacency masks
and a planar rotation system. It has components of orders 10 and 6.
Direct enumeration of all ambient shortest paths gives 102 distinct
vertex masks and 2,521 distinct pair unions. For **every** pair, at
least one residual component has at least six vertices. Thus the
five-vertex residual premise fails for \(F\).

The primary pair `[1]`, `[4,0,7,8]` leaves exactly
`{2,3,11,14,15}` and `{5,6,9,10,12,13}`. They are covered,
respectively, by the secondary pairs
`[2,11,14]`, `[3,11,15]` and `[5,12]`, `[6,13,10,9]`.
The checker validates each sequence against breadth-first distances.
Thus the two-stage premise holds and the guarded lemma certifies every
spanning subgraph retaining its 11 protected edges.

The graph also has an independent componentwise weighted certificate.
Its 10-vertex component has a primary pair `[4,0,9,10]`,
`[7,6,13,12]` leaving only singleton residual components. An exact
elimination search finds treewidth greater than three for this
component, but at most three after **each** of its 16 edge deletions.
The 6-vertex component has treewidth at most three. Hence the
five-vertex lemma, the treewidth terminal, and component decomposition
certify \(B_w^*(F)\) itself. This example separates the two local
residual criteria; its disconnectedness makes component decomposition
an additional route. It is not a counterexample to Problem 31.

## Reproduction and trust boundary

Run with Python 3.11 or later, standard library only:

```sh
python3 graph_theory/planar_two_geodesic_weighted_guarded_descent/verify.py
```

Expected output (the treewidth search-state count is an internal
deterministic statistic):

```text
rotation component (vertices,edges,faces): [(6, 8, 4), (10, 16, 8)]
path masks: 102 pair unions: 2521 minimum largest residual component: 6
guarded residual sizes: [5, 6]
ten-vertex core: treewidth >3; all 16 single-edge deletions have treewidth <=3; root search states: 41
PASS
```

The rotation certificate checks Euler's identity separately for each
component. The breadth-first path enumeration considers each reachable
endpoint pair, follows every edge consistent with shortest distance,
and checks all pair unions. The elimination search branches on every
vertex of current degree at most three and fills its neighbor clique;
this is the exact treewidth-three characterization. The mathematical
lemmas are proved above; computation is used only for the stated
finite example. No exhaustive census or universal bound follows from
the example.
