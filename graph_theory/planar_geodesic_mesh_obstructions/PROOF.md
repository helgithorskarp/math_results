# Capped meshes do not give a counterexample to Problem 31

## Statement and scope

All graphs in this note are finite, simple, undirected, and have unit edge
lengths. A geodesic is a shortest path in the **original** graph; singleton
paths are allowed. Vertex weights are arbitrary nonnegative real numbers.
A half separator leaves every component with weight at most half the
original total weight. Deleting extra vertices cannot spoil this property.

We exclude two explicit construction families, with arbitrary choices of
triangulation diagonals and arbitrary vertex weights. The results do not
settle Barbados 2026 Problem 31 and make no priority claim.

### Family A: capped cylindrical meshes

Fix integers m >= 3 and h >= 1. Vertices are two poles s,t and vertices
v(i,j), with i in Z/mZ and 1 <= j <= h. Include:

* each meridian s,v(i,1),...,v(i,h),t;
* the horizontal edges v(i,j)v(i+1,j);
* in each quadrilateral between columns i,i+1 and levels j,j+1,
  either no diagonal, or either one of its two diagonals.

There is at most one diagonal in each quadrilateral. There is no edge st.
This describes a cylinder capped by two disks, so it is planar; the stated
restrictions yield a simple graph, including m=3 and h=1.

**Proposition A.** Every such vertex-weighted graph has a half separator
consisting of at most two s-t geodesics. The first meridian may be prescribed.

**Proof.** Assign levels 0 to s, j to v(i,j), and h+1 to t. Every edge changes
level by at most one, whereas each meridian has exactly h+1 edges. Every
meridian is therefore an ambient s-t geodesic.

Let b(i) be the total weight of column i, excluding the poles, and put
B=sum b(i). Relabel the prescribed column as 0. If B=0 or b(0)>=B/2,
delete just meridian 0. The remaining weight is at most B/2, hence at most
half the whole graph's weight.

Otherwise choose the first j>=1 for which b(0)+...+b(j)>=B/2. Delete
meridians 0 and j, including both poles. Every remaining component lies
entirely in columns 1,...,j-1 or entirely in columns j+1,...,m-1: edges
join only the same or cyclically adjacent columns. The first side has
weight less than B/2, and the second side has weight at most B/2.
Both bounds are at most half the original total weight. This proves A.

### Family B: capped rectangular meshes with a pole shortcut

Fix m >= 1 and h >= 1. Use the same vertices and meridians, with columns
0,...,m-1 linearly ordered. Include horizontal edges and optional single
diagonals only between columns i and i+1 for 0<=i<m-1. Add the edge st.
The rectangle, its top and bottom cap fans, and st in the outer face give
a planar drawing. This remains a simple graph when m=1 or h=1.

**Proposition B.** Every such vertex-weighted graph has a half separator
consisting of at most two ambient geodesics.

**Proof.** Put B=sum b(i), again excluding pole weights. If B=0 take column
0. Otherwise let a be the first column with b(0)+...+b(a)>=B/2.
Deleting both poles and all of column a leaves two sides, each of total
weight at most B/2. All remaining components lie within one of those sides.

A complete meridian is not geodesic: it joins the adjacent poles. It can,
however, be covered by two ambient geodesics. Set k=floor(h/2) and use

    P = s,v(a,1),...,v(a,k),
    Q = t,v(a,h),v(a,h-1),...,v(a,k+1).

When k=0 the first path is the singleton s. These two paths cover exactly
the deleted meridian, including its poles; the edge between the paths need
not belong to their union because separators are vertex sets.

To check shortestness in the full graph, map s to 0, v(i,j) to j, and t
to h+1 in the cycle C_(h+2). Every graph edge maps either to a vertex or
to an edge of this cycle, including st. Thus graph distances are bounded
below by the corresponding cycle distances. The lengths of P and Q are
k and h-k, both at most floor((h+2)/2). Each path achieves the cycle
distance between its endpoints, so each is geodesic in the original graph.
This proves B, for every allowed choice of diagonals.

## Arbitrary pendant masses remain excluded

Attach any finite number ell(v) of new leaves to each vertex v of either
family. Apply A or B to the core weights a(v)=1+ell(v). The total core
weight is exactly the order N of the enlarged graph. The displayed core
paths remain geodesic after adding leaves: a simple path between core
vertices cannot use a pendant vertex internally.

Delete those same core paths from the enlarged graph. A component with
core vertices consists of a remaining core component and its attached
leaves, so its order equals that component's a-weight. Leaves attached to
deleted roots are isolated. They have order 1<=N/2, since these families
have at least three vertices. Thus every such pendant inflation still
has a two-geodesic half separator.

This argument only needs the easy lifting of a positive result. General
weighted-to-unweighted obstruction lifting is being pursued separately by
the structural research lane; it is not claimed as this contribution.

## What a construction must change

Redistributing vertex mass, adding leaves, or flipping any of the allowed
cell diagonals cannot produce a counterexample in either family. Adding
only the pole shortcut after opening a cylindrical seam also fails: although
it destroys the full meridians as geodesics, it leaves the two half-meridians
used in B geodesic.

Any extension of this construction must therefore escape at least one
hypothesis. Examples of hypotheses to re-examine are the cyclic/linear
column separation or the level/cycle map that certifies the needed paths.
This is a necessary change to this particular construction route, not a
classification of all possible planar counterexamples.

## Context and validation

The target is Julien Codsi's Problem 31 in the [Barbados 2026 problem
list](https://web.math.princeton.edu/~pds/barbados26/problems.pdf). The
half-balance threshold, rather than 2/3 balance, is used throughout.

Diot and Gavoille, [*Path Separability of Graphs*, HAL v3,
2010](https://emilie-diot.eu/Article/DG10a), distinguish strong path
separability (all paths shortest in the original graph) from sequential
path separability. Proposition 1 and Theorem 1 provide relevant existing
positive cases. This note makes no claim that A or B is absent from all
earlier work; it records complete, elementary exclusion proofs for the
specified adversarial families.

The proofs above establish the infinite-family claims. `verify.py` checks
explicit witnesses by BFS distances and full component traversal on a
deterministic finite stress suite, including pendant-inflated graphs. Its
role is to catch definition, indexing, boundary-case, and implementation
errors. The finite checks are not the justification for the universal
claims and are not an independent peer review or a formal proof.
