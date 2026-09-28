# A four-vertex guard gives two weighted geodesics in every edge subgraph

All graphs here are finite and simple with **unit edge lengths**. Paths
of one vertex are allowed. For a graph \(G\), write \(B_{k,w}^*(G)\)
when every spanning subgraph \(H\subseteq G\), under every
nonnegative real vertex-mass assignment, has a half-balanced separator
that is the union of at most \(k\) shortest paths **in \(H\)**.

## Dynamic guard theorem

**Theorem.** Let \(k\geq1\), and let \(S\subseteq V(G)\) have at most
\(2k\) vertices. Suppose every component \(C\) of \(G-S\) has at most
\(2k+1\) vertices, and no component of order \(2k+1\) induces a
complete graph. Then \(B_{k,w}^*(G)\) holds.

**Proof.** First, every connected unit-edge graph \(D\) on at most
\(2k\) vertices can be covered by at most \(k\) ambient shortest
paths: pair its vertices and join each pair by a shortest path. If
\(|D|=2k+1\) and \(D\) is noncomplete, choose an induced three-vertex
path \(x,y,z\). Since \(x,z\) are nonadjacent, this is a shortest path
in the ambient graph. Pair the remaining \(2k-2\) vertices. This uses
at most \(k\) ambient geodesics and covers \(D\). Here “ambient”
means the current spanning subgraph, not the induced graph on \(D\).

Now fix any spanning \(H\subseteq G\) and any nonnegative vertex
masses of total \(W\). If every component of \(H\) has mass at most
\(W/2\), the empty separator works. Otherwise there is a unique
component \(K\) of mass greater than \(W/2\). Pair the vertices of
\(S\cap K\), using a singleton if necessary, and connect pairs by
\(H\)-geodesics. Their union \(X\) uses at most \(k\) paths and
contains \(S\cap K\). If deleting \(X\) is not balanced, its unique
heavy component \(D\) lies in \(K-S\), hence inside one original
component \(C\) of \(G-S\). It has at most \(2k+1\) vertices. If it
has exactly \(2k+1\), then \(D=C\), so connectedness and the
nonclique hypothesis let the preceding covering argument apply in
\(H\). It also applies when \(|D|\leq2k\). Choose at most \(k\)
\(H\)-geodesics covering \(D\). Their deletion leaves total mass at
most \(W-w(D)<W/2\), and hence is balanced. This proves the theorem
for every \(H\) and every mass assignment. \(\square\)

The paths covering the guard are chosen again in each edge subgraph;
no protected edge survives as a hypothesis. This makes the theorem a
terminal rule for [witness-edge induction](../planar_two_geodesic_edge_deletion16/README.md)
and for the [guarded-residual descent](../planar_two_geodesic_hybrid_residual20/README.md).
It is a structural all-spanning result, independent of graph order.

**Planar two-path corollary.** In a planar graph, no five-vertex
induced subgraph is \(K_5\). Therefore, if some set of at most four
vertices leaves components of order at most five, **every** spanning
subgraph has a two-geodesic half separator for **every** nonnegative
vertex weighting. This supplies an order-independent positive class
for [Barbados 2026 Problem
31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).

The unit-edge assumption matters to the induced-three-vertex-path
step. No claim is made for arbitrary positive edge lengths.
The nonclique condition cannot simply be dropped: for
\(G=K_{4k+1}\), any \(2k\)-vertex guard leaves one complete component
of order \(2k+1\), while \(k\) geodesics cover at most \(2k\)
vertices. Uniform masses then violate half-balance. This is the
complete-graph obstruction in Diot and Gavoille's Proposition 1(4).

## An infinite biconnected planar family beyond treewidth three

Start with the octahedron graph: an equatorial four-cycle
\(0,1,2,3,0\) and two nonadjacent poles \(4,5\), each adjacent to all
four equator vertices. For any \(r\geq1\), add \(r\) internally
vertex-disjoint paths of length six between the adjacent vertices
\(0,1\), drawn inside one face incident with edge \(01\). This gives
a simple biconnected planar graph \(G_r\) with \(6+5r\) vertices and
\(12+6r\) edges. The fixed guard \(S=\{0,1,2,3\}\) leaves the two
poles as singleton components and each added path's five internal
vertices as a separate nonclique component. Thus \(B_{2,w}^*(G_r)\)
holds for every \(r\).

Every \(G_r\) contains the octahedron as a subgraph. Its minimum
degree is four, whereas every graph of treewidth at most three is
three-degenerate. Hence \(G_r\) has treewidth at least four, so this
family is not covered by the [treewidth-three two-path
bound](https://emilie-diot.eu/Article/DG10a) of Diot and Gavoille.
This comparison does not claim priority over other known two-path
classes such as face-separable graphs.

## Reproduction and trust boundary

Run the standard-library Python 3.11 checker from the repository
root:

```sh
python3 graph_theory/planar_two_geodesic_four_guard/verify.py
```

It constructs \(G_r\) for \(r=1,2,3,4\), checks the fixed guard,
biconnectivity, edge counts, and an explicit spherical rotation system.
Expected output:

```text
ears=1 vertices=11 edges=18 faces=9 residuals=[1, 1, 5]
ears=2 vertices=16 edges=24 faces=10 residuals=[1, 1, 5, 5]
ears=3 vertices=21 edges=30 faces=11 residuals=[1, 1, 5, 5, 5]
ears=4 vertices=26 edges=36 faces=12 residuals=[1, 1, 5, 5, 5, 5]
PASS
```

The written proof establishes the
all-order weighted theorem; the program audits only the illustrative
finite family and does not enumerate vertex masses or spanning
subgraphs. The rotation is built by inserting each new path in the
face incident with edge \(01\), which also proves planarity for every
\(r\geq1\). The treewidth comparison uses the octahedron subgraph,
not a numerical treewidth package.
