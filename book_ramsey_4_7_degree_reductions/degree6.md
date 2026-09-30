# Exact exclusion of degree six

Author: six-books-1, researcher. This strengthens the analytic degree
range 6..12 to 7..12. The finite classification below is an exact
computer-assisted lemma with a written completeness reduction.

## 1. Complete normalization of the fifteen-vertex graph

Section 7 of proof.md shows that degree six in a hypothetical
22-vertex witness forces its blue neighborhood H to have parameters
(v,k,lambda)=(15,8,3): eight-regular, with exactly three common
neighbors at every edge. Every edge belongs to a triangle. For
any triangle, degree-sum equality forces every outside vertex to
have exactly one or two neighbors in the triangle. H has no K4.

Fix and order a triangle T={t0,t1,t2}. For i=0,1,2, let S_i consist
of vertices adjacent only to t_i in T, and D_i of vertices adjacent
to the other two vertices of T. Each edge of T has the third
triangle vertex and exactly two outside common neighbors, so
|D_i|=2. Each t_i has six outside neighbors, of which four are
in the other two D classes, so |S_i|=2. These six two-vertex
classes partition the twelve vertices outside T. Assign arbitrary
labels within each class; no assumption about automorphisms is made.

Every local graph H[N(t_i)] is cubic, because edge codegrees of H
are three, and is triangle-free, because H has no K4. For
{i,j,k}={0,1,2}, its vertices are

    {t_j,t_k} union S_i union D_j union D_k.

Its five fixed edges are t_j t_k, the two t_j--D_k edges and the
two t_k--D_j edges. Each D class is independent: an edge in D_i,
together with t_j,t_k, would make K4. All remaining possible edges
of this local graph are the one S_i edge, eight S_i--(D_j union D_k)
edges and four D_j--D_k edges. Cubicity requires seven of these
thirteen edges. The generator tries every seven-element subset
and retains exactly the cubic triangle-free local graphs: 16.

Each vertex of D_i has two neighbors in S_j union D_k from the
cubic local graph at t_j, and two in S_k union D_j from the local
graph at t_k. These sets are disjoint. Together with its two
neighbors in T, these give six neighbors. The only other possible
neighbors are the two vertices of S_i. Degree eight forces both
S_i--D_i edges at that vertex; hence all four edges between S_i
and D_i are present.

Each S_i vertex now has one neighbor in T, three in its local
graph at t_i, and two in D_i. Its remaining two neighbors must
be in S_j union S_k. Thus the cross edges on the six S vertices
form a simple 2-regular graph, with no edge within any S class.
Trying every six-element subset of its twelve possible edges
and checking degrees gives exactly 20 such graphs.

The three local edge-variable sets are disjoint from one another,
from the forced edges, and from the cross-S edges. Every normalized
H is therefore covered by the Cartesian product

    16^3 * 20 = 81,920 candidates.

The code also generates the same local patterns by the two cases
whether the S_i pair is adjacent, and the same cross-S graphs by
six-cycles and pairs of triangles. It compares both sets entry by
entry. These independent generation descriptions are detailed in
the source; none discards a graph by an unproved symmetry rule.

## 2. Finite result and explicit isomorphism certificates

The exact enumeration retains 32 candidates with edge codegree
three everywhere. For each it verifies an explicit grid description:
three disjoint independent five-sets partition the vertices into
rows, and five disjoint independent three-sets partition them
into columns, each meeting every row once. Every pair is then
checked against the rule

    uv is an edge iff its rows differ and its columns differ.

Thus every retained candidate is isomorphic to the direct product
K3 tensor K5, equivalently the complement of the 3 by 5 rook graph.
This graph is itself known; no novelty for its existence is claimed.
The assertion established here is the complete small-parameter
classification under the proved normalization.

Both bitset intersections and literal neighbor-list membership
checks decide edge-regularity for every one of the 81,920 candidates
and agree entry by entry. The deterministic counts, candidate-stream
hash and accepted-stream hash are in degree6_expected.json. The
full search uses only compact source and standard-library integers;
no SAT solver, external graph catalogue, floating point, or large
proof certificate is used.

## 3. Six attachment vertices cannot complete it

Suppose a hypothetical witness contains a degree-six vertex v.
Write A=N_G(v), |A|=6, and B for its fifteen blue neighbors. By
the classification, G[B] has the grid description above.

Every edge of G[B] already has three common neighbors in B.
Consequently R_a=N_G(a) intersect B is independent for each a in A.
An independent set in this grid graph lies in one row or one
column. Indeed, two distinct vertices in an independent set
share a row or a column. If they share a row and different
columns, any third vertex outside that row would need to share
both different columns in order to be nonadjacent to both,
which is impossible. The argument for a shared column is the
same. Empty sets and singletons cause no exception.

Now consider two vertices of B in the same row. Their edge is
blue. They have three common blue neighbors in B, namely the
other vertices of that row; no vertex in a different row is blue
to both because their columns differ. The vertex v is one further
common blue neighbor. At most two vertices of A may be blue to
both. Hence at least four of the six A vertices must be red to
at least one endpoint of each such row pair.

There are 3*binomial(5,2)=30 row pairs, so these requirements demand
at least 30*4=120 incidences (a,row pair), where R_a meets that
pair. An independent set in one row meets at most ten row pairs.
An independent set in one column has at most three vertices,
one per row; each vertex meets four row pairs, for at most twelve
incidences in total. Each of the six a therefore contributes at
most twelve, giving at most 72 incidences. Since 72<120, degree
six is impossible.

Combining this with proof.md yields 7<=d_G(v)<=12 for every
hypothetical 22-vertex (B4,B7)-avoiding graph. The edge bounds
97..123 and defect cuts still apply. Existence at order 22 remains
unresolved.

## Reproduction and trust boundary

Run with Python 3.11+ and no external packages:

    python3 book_ramsey_4_7_degree_reductions/degree6_check.py

Compare the output with degree6_expected.json. The completeness
normalization and the final 120-versus-72 attachment obstruction
are analytic arguments, not proof-assistant formalizations. The
finite classification relies on Python exact integer/list operations
and the inspected generators and certificate checks. No independent
peer-review verdict is claimed.
