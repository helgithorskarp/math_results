# Exactly which prescribed cycles the dual-tree construction recovers

## Statement and scope

Let $G$ be a simple, cubic, bipartite, 3-connected graph embedded in the
sphere. Fix a proper face three-coloring, with classes $R,B,F$ called
red, blue, green. Color each edge by the color absent from its incident
faces, and let $M_g$ be the set of green edges.

The sphere convention permits choosing the outer face of a planar chart.
For fixed color roles choose a red face as outer face. In the proof below
all red faces of an eligible cycle lie on the same side, so the blue side
can be taken as its bounded disk. The output comparison concerns cyclic
orders under this convention.

We use the dual-tree construction of Alam et al., as presented by
Bekos--Kaufmann--Pfister (BKP), *Approximating Barnette's Conjecture*,
GD 2025, Section 2. Its input is a spanning tree of
$D=G^*[B\cup F]$ rooted at a blue leaf. Its output is a cyclic order of all
vertices that gives a plane subhamiltonian cycle. For an actual Hamiltonian
cycle $C$ of $G$, equality of output and $C$ means equality of cyclic orders
up to reversal and rotation, equivalently equality of their cycle edges.

**Recovery theorem.** For this fixed coloring, the following are equivalent:

1. Some valid blue-leaf-rooted dual tree makes the construction output $C$.
2. $M_g\subseteq E(C)$.

There is a linear-time construction of such a tree from the embedding and
$C$ whenever (2) holds. Consequently, allowing all global color
permutations, the recoverable Hamiltonian cycles are exactly those
containing at least one of the three induced edge-color classes.

This is an image characterization of an existing algorithm, not a
Hamiltonicity theorem for arbitrary Barnette graphs. The negative answer
to recovery of *every* prescribed cycle was already given by Lennart
Rudolph in August 2026. The dual tree-of-faces mechanism is classical:
compare Bagheri Gh--Feder--Fleischner--Subi, Theorem 3.3. Our contribution
is the explicit converse for the published algorithm, including its blue
leaf root requirement and the certificate description below. No claim
of exclusive historical priority is made.

We do not classify every arbitrary tree that might produce a given
Hamiltonian cycle. The counted certificates below belong to a specified
family of trees whose green vertices are either leaves or have full degree.

## Imported algorithm facts

The proof uses these four properties from BKP (Properties 1--4):

- Every green edge belongs to the output.
- Every red edge not crossed by the dual tree belongs to the output.
- On a green face, the blue edge between two cyclically consecutive red
  edges crossed by the tree belongs to the output.
- The red edge crossed at a green leaf belongs to the output.

The cyclic meaning of consecutive includes the closing pair, also on a
quadrilateral. These are properties of the published traversal, not
empirical assumptions about a simulation.

In particular, if a green face is a leaf, **all its red boundary edges**
belong to the output: all but one follow from the second fact, and the
remaining one from the fourth. If a green face has full degree in $D$,
**all its blue boundary edges** belong to the output, by the third fact.
Together with all green edges, these choices already specify one edge
at each vertex in addition to its green edge. If the resulting edge set
is the prescribed Hamiltonian cycle, the output is forced to be that
cycle. This is the edge-by-edge version of BKP's Observation 2.

## Facial and dual preliminaries

At each cubic vertex the three incident faces are distinct and pairwise
adjacent, hence have all three colors. The induced edge coloring is proper;
each edge-color class is a perfect matching. The green facial cycles are
pairwise vertex-disjoint and cover all vertices, and their boundaries
partition the red and blue edges.

The dual of a 3-connected plane graph is simple. Every facial boundary is
a simple even cycle of length at least four. For $f\in F$, write

$d_f=\deg_D(f)=|\partial f|/2\geq2$.

Its blue neighbors are distinct. In particular $|B|\geq2$.

Each subgraph of the dual induced by two face colors is connected. Here
is a direct argument. The full dual is connected. A dual walk whose
endpoints avoid the third color can have each visit to a vertex of that
color replaced by a walk around its link. That link alternates the other
two colors. Repeating this replacement gives a walk using only those
two colors.

## Proof of recovery

Necessity is the first imported algorithm fact.

Assume $M_g\subseteq E(C)$. Every vertex uses its green edge in $C$.
On the boundary of each green face the remaining cycle edges therefore
form a perfect matching of a simple even cycle. There are exactly two
possibilities: all the red boundary edges or all the blue boundary edges.
Let

$S=\{f\in F:C\text{ uses the blue boundary matching of }f\}$.

We claim that

$Q=D[B\cup S]$

is a tree.

The Jordan curve $C$ divides the sphere into two disks. Every dual edge
between a red and a blue face crosses a green edge of $G$, hence an edge
of $C$, and its two ends are on opposite sides of $C$. The connectedness
of $G^*[R\cup B]$ then forces all blue faces to lie on one side and all
red faces on the other. This follows also from uniqueness of the
bipartition of that connected bipartite graph.

A green face using its blue boundary matching lies on the blue side:
its blue boundary edges separate it from red faces. A green face using
its red boundary matching lies on the red side. Thus the faces on the
blue side are exactly $B\cup S$.

All vertices of $G$ lie on $C$. Edges drawn in either of its disks are
noncrossing chords with endpoints on the boundary. The weak dual of the
dissection of a disk by noncrossing chords is a tree: it starts as a
single vertex, and each chord splits one region into two and adds one
dual edge. On the blue side that weak dual is exactly $Q$. This proves
the claim. It is the same standard disk/weak-dual argument that underlies
the published tree-of-faces equivalence.

Every $f\in S$ has its full $D$-degree in $Q$, since all its blue neighbors
are present. Consequently every leaf of $Q$ is blue. There is at least
one such leaf, since $|B|\geq2$.

Choose a blue leaf $b$ of $Q$. For every $f\in F\setminus S$, choose a blue
neighbor $a_f\ne b$. This is always possible because $d_f\geq2$. Put

$T=Q\cup\{fa_f:f\in F\setminus S\}$.

Each new green vertex has been attached as a leaf, so $T$ is a spanning
tree of $D$. No attachment uses $b$, so $b$ remains a blue leaf and is a
valid root for the published algorithm. A vertex of $S$ has full degree
in $T$; every other green vertex is a leaf.

The four imported properties now force all green edges, all blue boundary
edges of faces in $S$, and all red boundary edges of faces outside $S$
into the output. These are precisely the edges of $C$. An output cyclic
order has $|V(G)|$ consecutive pairs, already exhausted by those cycle
edges, so its cyclic order is $C$. This proves sufficiency.

Given the rotation system, faces, coloring and the cycle, all steps
(recognizing $S$, extracting $Q$, choosing a leaf, and attaching the
remaining faces) require only linear scans of a graph of size $O(|V(G)|)$.
This is an inverse for a *given* eligible cycle, not an algorithm for
finding an eligible cycle.

The proper coloring of a connected triangulation is unique up to global
permutation when it exists: fixing the colors of one triangle propagates
across the connected face-adjacency graph. Applied to $G^*$, this shows
that the relabeling statement covers all proper facial three-colorings.

## Complete description and count of the specified certificates

For a fixed eligible $C$ and color roles, keep $S,Q,d_f$ as above. Let
$L_B(Q)$ be the set of blue leaves of $Q$.

All spanning trees with precisely the vertices of $S$ full at green
vertices and all other green vertices leaves are obtained by independently
choosing one neighbor $a_f\in N_D(f)$ for each $f\in F\setminus S$.
Indeed, the full stars of $S$ are exactly $Q$, and no other edge is
possible except the single chosen edge at each remaining green vertex.
The unrooted number is

$\displaystyle \prod_{f\in F\setminus S}d_f.$

Some of these trees have no blue leaf and cannot be used with the source's
stated root convention. For a **fixed** root $b\in L_B(Q)$, exactly the
choices avoiding $b$ retain it as a leaf, giving

$\displaystyle N_b(C)=\prod_{f\in F\setminus S}
  \bigl(d_f-\mathbf1_{\{bf\in E(D)\}}\bigr).$

The total number of pairs (tree, designated blue leaf root) in this family is

$\displaystyle N_{\rm root}(C)=
 \sum_{b\in L_B(Q)}\prod_{f\in F\setminus S}
  \bigl(d_f-\mathbf1_{\{bf\in E(D)\}}\bigr)>0.$

Every factor is positive. These formulas count unrooted trees or rooted
pairs exactly as specified; they do not count distinct output cycles or
claim that no other kinds of tree produce $C$.

## A small illustrative obstruction

Take two cubes with binary vertex labels $0,\ldots,7$. Delete vertex $0$
from both, and join their corresponding neighbors $1,2,4$. Write $A_i$
and $B_i$ for the two copies of a remaining vertex. The result is a
14-vertex Barnette graph. It can be drawn by gluing the punctured sphere
embeddings of the cubes. It is cubic and bipartite (reverse the bipartition
on the second copy). To see 3-connectivity, consider deletion of at most
two vertices. If both are in one shore, each surviving component of that
shore meets a surviving terminal, since putting the removed cube vertex
back gives a cube with at most two deleted vertices, which is connected.
The other shore is connected. If one is deleted in each shore, each shore
is a cube with at most two deleted vertices and is connected, and at least
one of the three joining edges survives. The cases with fewer deletions
follow by the same argument.

Internal cube edges in binary direction $b\in\{1,2,4\}$ and the joining
edge $A_bB_b$ have color $b$. This is the induced facial coloring: the
three far square faces of each cube retain the color of their fixed
coordinate, and the three merged hexagons have the color of the coordinate
fixed to zero.

The cycle

$(A_1,A_3,A_2,A_6,A_7,A_5,A_4,
 B_4,B_6,B_2,B_3,B_7,B_5,B_1,A_1)$

omits two color-1 edges, three color-2 edges, and two color-4 edges.
Therefore it is outside the recovery image for every color labeling.
This is a small corroborating example, not the first negative answer,
and no minimality is asserted.

## Verification boundary

The proof above is a human proof conditional on the four cited properties
of the existing algorithm. It is not formally verified. The checker
implements neither that traversal nor a floating-point drawing.

Instead it checks the sphere embeddings exactly (opposite oriented
incidences, cyclic vertex links, connectedness and Euler characteristic),
all deletions of up to two vertices, and the face/edge color conventions.
It separately enumerates Hamiltonian cycles by ordinary vertex-path DFS
and every spanning tree of each bicolored dual. Among the latter it
extracts the leaf/full family and compares its output edge sets and rooted
certificate multiplicities with the former, entry by entry.

The six fixtures are the cube, three even prisms, the two-cube sum, and
Rudolph's published 16-vertex graph. There are 62 Hamiltonian cycles and
810 dual spanning trees across all six ordered color-role choices.
Every fixed-color image and every certificate count agrees. The cube and
prisms provide positive controls; the two-cube sum and the credited
Rudolph graph supply cycles outside all three images. Malformed embeddings
and colorings are rejected. These finite checks corroborate the
translation and conventions; they are not a finite substitute for the
universal Jordan-curve proof.
