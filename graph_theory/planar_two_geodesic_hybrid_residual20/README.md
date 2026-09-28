# A connected triangulation requiring guarded residual descent

Let \(B_w^*(F)\) mean that every spanning subgraph \(H\subseteq F\),
under every nonnegative vertex-mass assignment, has a half-balanced
separator that is the union of at most two shortest paths **in \(H\)**.
All edges in this note have unit length. A singleton is a shortest path.
The setting is [Barbados 2026 Problem
31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).

## All-order hybrid lemma

Let \(F\) be any finite graph and let \(P,Q\) be ambient
\(F\)-geodesics.
Partition the components of \(F-(V(P)\cup V(Q))\) into *small* ones of
order at most five and *exceptional* ones. Suppose that, for each
small component of order five, its induced subgraph is not a \(K_5\).
Suppose also that, for each
exceptional component \(C\), two designated ambient \(F\)-geodesics
\(R_C,T_C\) cover every vertex of \(C\). Let \(E_*\) be the union of
the edges of \(P,Q\) and all designated paths; no edges are required for
small components. Then every spanning \(H\subseteq F\) retaining
\(E_*\) satisfies the weighted half property. If \(B_w^*(F-e)\) holds
for every \(e\in E_*\), then \(B_w^*(F)\) holds.

**Proof.** Every protected path remains shortest after deletion of
other edges. Delete the primary pair from \(H\). If it fails to balance,
there is a unique residual component \(D\) of mass greater than half.
It lies inside one original residual component \(C\). If \(C\) is
small, \(D\) is connected and has at most five vertices.
For at most four vertices, pair its vertices and join each pair by an
\(H\)-geodesic. If \(|D|=5\), then \(D=C\) and \(H[D]\) is connected
but not a clique. It contains an induced three-vertex path, which is
an \(H\)-geodesic because its endpoints are nonadjacent; one more
\(H\)-geodesic joins the remaining two vertices. In either case
the replacement pair covers \(D\). If \(C\) is exceptional, its
designated pair covers \(D\). Deleting that replacement pair leaves at
most the mass outside \(D\), strictly less than half. Finally, any
spanning subgraph missing a protected edge \(e\) is a spanning subgraph
of \(F-e\), proving the descent assertion.

This combines the [five-residual
lemma](../planar_two_geodesic_weighted_guarded_descent/README.md) with
the guarded two-stage rule. It protects secondary paths only where the
adaptive five-vertex argument does not apply. The all-order proof does
not rely on the finite example below. The local non-\(K_5\) hypothesis
uses the sharpening identified in the [independent review of the
earlier lemma](../planar_two_geodesic_weighted_guarded_descent_review1/REVIEW.md).

## Exact connected example

The graph6 string

```text
S|fIID`KGo`@B@@`_OgE@?OC@oG?oW?Xs
```

specifies a 20-vertex, 54-edge planar triangulation \(F\). Its
rotation system is embedded in `verify.py` and has 36 triangular faces.
The checker independently decodes the graph, runs breadth-first search
for every endpoint pair, enumerates **every** shortest path and all
36,159 distinct path-pair vertex unions, and searches the residual
components. It finds 425 shortest paths and a minimum possible largest
residual component of **six** vertices. Thus no primary pair satisfies
the five-residual premise, even though this graph is connected.

The hybrid certificate uses primary paths

```text
[0,4,10,18]     [12,5,6,7,17]
```

Their deletion leaves exactly the small component
`{1,2,3,8,9}` and the exceptional component
`{11,13,14,15,16,19}`. The designated secondary geodesics

```text
[11,19,16]     [13,14,15]
```

cover the exceptional component. Their edges together with the
primary edges form an 11-edge protected set. The hybrid lemma therefore
proves the weighted half property for \(F\) and for **every** spanning
subgraph retaining those 11 edges. It does not prove \(B_w^*(F)\),
because the protected-edge deletion children have not been certified.
In particular, the example is neither a counterexample nor a solution
to Problem 31. It shows that guarded descent has a connected planar
application beyond the five-residual premise; the earlier
[16-vertex example](../planar_two_geodesic_weighted_guarded_descent/README.md)
was disconnected.
The independent review had singled out a connected example as the next
test of guarded descent; this triangulation supplies one.

## Reproduce and scope

Run from the repository root with Python 3.11 or later; the checker uses
only the standard library:

```sh
python3 graph_theory/planar_two_geodesic_hybrid_residual20/verify.py
```

Expected output:

```text
triangulation: 20 vertices, 54 edges, 36 triangular faces
geodesics: 425 pair unions: 36159 minimum largest residual: 6 minimum-attaining unions: 151
hybrid residual sizes: [5, 6] protected edges: 11
PASS
```

The graph was found in a plantri 5.8 minimum-degree-four sample at
order 20. The published certificate does not trust the sample for its
claim: it checks the explicit graph6 record, adjacency masks, a planar
rotation system, every path-pair union, and the displayed paths. The
sample was not an exhaustive least-order search. This finite example
cannot establish a universal half-separator theorem. The general
hybrid lemma is an elementary proof, with no computer-assisted step.
The weighted ambient-geodesic formulation follows the terminology of
[Diot and Gavoille](https://emilie-diot.eu/Article/DG10a); no priority
claim is made for the local lemma.
