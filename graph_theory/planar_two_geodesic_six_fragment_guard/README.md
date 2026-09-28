# Six-vertex fragments in the weighted two-geodesic guard rule

All graphs here are finite and simple, with unit edge lengths. Vertex
masses are arbitrary nonnegative real numbers. A singleton is a
geodesic. A union of paths is *half-balanced* when every component left
by deleting its vertices has at most half the total mass.

The [earlier dynamic guard theorem](../planar_two_geodesic_four_guard/README.md)
handles a four-vertex guard whose residual components have at most five
vertices, with a nonclique condition at order five. The following
extension permits certain six-vertex fragments. The replacement paths
cover the **entire** heavy fragment; this point is essential. The
[withdrawn eight-residual claim](../planar_two_geodesic_eight_residual/README.md)
failed because its replacement paths removed only half the fragment's
mass and allowed the primary vertices to return.

## Robust six-vertex tilings

Call a connected six-vertex graph \(C\) *robustly \(P_3\)-tileable* if
every connected spanning edge subgraph \(J\subseteq C\) has a
partition of its six vertices into two induced three-vertex paths.
An induced \(P_3\) in \(J\) is an ambient geodesic in any unit-edge
graph whose induced graph on these six vertices is \(J\): its endpoints
are nonadjacent, so their distance is exactly two.

**Exact finite classification.** Up to isomorphism, precisely five
connected six-vertex graphs are robustly \(P_3\)-tileable:

| Type | Labeled graphs on \(\{0,\ldots,5\}\) |
| --- | ---: |
| Double star with adjacent degree-three centres | 90 |
| Tree with one degree-three centre and arm lengths \(3,1,1\) | 360 |
| Six-vertex path \(P_6\) | 360 |
| Four-cycle with one pendant leaf at each of two opposite cycle vertices | 180 |
| Six-cycle \(C_6\) | 60 |

Thus the five classes comprise 1,050 labeled graphs. The
[standard-library checker](verify.py) enumerates all \(2^{15}=32{,}768\)
labeled simple graphs on six vertices. It computes robustness by
one-edge-deletion induction and independently by a Boolean subset
transform that marks every graph containing a connected, non-tileable
spanning edge subgraph. These methods agree on every mask. It then
canonicalizes each robust graph over all \(6!\) vertex permutations
and checks the five displayed orbit sizes. This exact finite step
classifies the tiling condition; it is not an enumeration of all
planar graphs or all vertex masses.

Membership of the five displayed types can also be checked directly.
Each of the three trees partitions into two induced \(P_3\)s, and no
tree edge can be deleted while keeping all six vertices connected.
Deleting one edge of \(C_6\) produces \(P_6\). The only deletable
edges of the four-cycle gadget are its cycle edges; deleting one
produces the listed tree with arm lengths \(3,1,1\). Repeated
connected deletions therefore stay within the table. The exhaustive
step is needed only to exclude other six-vertex types.

## All-order guard theorem

**Theorem.** Let \(G\) be any finite simple unit-edge graph. Suppose
\(S\subseteq V(G)\) has at most four vertices. Every component of
\(G-S\) must have at most six vertices; every component of order five
must be noncomplete; and every component of order six must be one of
the five robustly \(P_3\)-tileable graphs above. Then **every spanning
edge subgraph** \(H\subseteq G\), under **every** nonnegative real
vertex-mass assignment, has a half-balanced separator equal to the
union of at most two shortest paths in \(H\).

**Proof.** Let the total mass be \(W\). If no component of \(H\) has
mass greater than \(W/2\), use the empty separator. Otherwise let
\(K\) be the unique heavy component. Pair the vertices of \(S\cap K\)
and take at most two \(H\)-geodesics through them, using a singleton
when necessary. If their union balances, stop. Otherwise its unique
heavy residual component \(D\) lies in one component \(C\) of
\(G-S\).

If \(|D|\leq4\), pair its vertices into at most two \(H\)-geodesics
that cover \(D\). If \(|D|=5\), the connected induced graph \(H[D]\)
is noncomplete: either \(D=C\) and the order-five hypothesis applies,
or \(D\) lies in a six-vertex component from the table, each of which
has at most six edges. A connected noncomplete graph contains an
induced \(P_3\). This is an \(H\)-geodesic, and another \(H\)-geodesic
joins the two remaining vertices, covering \(D\). If \(|D|=6\), then
\(D=C\), and \(H[D]\) is a connected spanning edge subgraph of the
robust graph \(G[C]\). Its two induced \(P_3\)s are \(H\)-geodesics
and cover \(D\). In every case the **replacement** pair covers all
of \(D\), so every component left in \(H\) has mass at most
\(W-w(D)<W/2\). This includes disconnected spanning subgraphs,
zero masses, and geodesics that pass outside \(D\). \(\square\)

For planar \(G\), the order-five nonclique condition is automatic.
The five-type test therefore supplies an all-spanning terminal for
[witness-edge descent](../planar_two_geodesic_edge_deletion16/README.md).
It is a sufficient condition, not a classification of all graphs with
weighted two-geodesic half balance.

## A strictly larger planar guard family

Start with the octahedron: an equatorial four-cycle
\(0,1,2,3,0\) and two nonadjacent poles \(4,5\), each joined to all
four equator vertices. In a face incident with the edge \(01\), add
\(r\) disjoint gadgets. Each gadget has six new vertices
\(a,b,c,d,e,f\), the cycle
\(a b c d e f a\), and attachment edges \(0a,1f\). Draw each
gadget as a path from \(0\) to \(1\) and then add \(af\) inside the
face bounded by that path and \(01\). Insert the next gadget in the
remaining face incident with \(01\). This gives a simple
biconnected planar graph \(G_r\) with \(6+6r\) vertices and
\(12+8r\) edges. The equatorial guard leaves two singleton poles and
\(r\) induced six-cycles, so the theorem applies for every \(r\geq1\).

Biconnectivity holds at every ear count. Deleting one core vertex leaves
the octahedron connected; each gadget remains attached through at
least one of \(0,1\). Deleting one gadget vertex leaves its cycle as a
connected path with at least one of its two distinct attachments,
while the core and the other gadgets stay connected.

For \(r\geq5\), this family is **not covered by any four-vertex
five-fragment guard**: four deleted vertices meet at most four of the
disjoint six-cycles, leaving one entire connected six-cycle. This
strictly extends the earlier guard sufficient condition, without
claiming priority over other positive classes or a solution to
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).

## Reproduce and scope

Using Python 3.11 or later, from the repository root run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  graph_theory/planar_two_geodesic_six_fragment_guard/verify.py
```

The checker is self-contained and uses only the standard library. It
checks all six-vertex masks by two algorithms, the five isomorphism
classes and orbit sizes, and an explicit spherical rotation system,
biconnectivity, and residual fragments for \(G_r\) with
\(1\leq r\leq8\). It also directly rejects all 58,905 four-vertex
five-fragment guards in \(G_5\); the pigeonhole proof above covers
every \(r\geq5\). Expected summary:

```text
six-vertex connected=26704 individually tiled=22360 robust=1050 unlabeled_classes=5
canonical class counts: [(121, 90), (122, 360), (246, 180), (692, 360), (1880, 60)]
cycles=8 vertices=54 edges=76 faces=24 biconnected=yes
PASS
```

The all-order guard implication and family construction are written
proofs. Exact computation is used only for the five-type tiling
classification and finite audits of the displayed family. No claim
is made for arbitrary positive edge lengths.
