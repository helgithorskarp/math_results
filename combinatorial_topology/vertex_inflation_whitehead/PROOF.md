# Relative collapse and Whitehead inheritance for vertex inflations

## 1. Statement

Let K be a finite abstract simplicial complex of dimension at most two,
and let m_v be a positive integer for each vertex. Its **vertex inflation**
I=K(m) has vertices (v,c), 0<=c<m_v. A set is a face if its original
vertices are distinct and form a face of K. Write K_0 for the copy with
all c=0, and S={v:m_v>1}. Empty complexes and isolated vertices are allowed.
Links below include isolated link vertices. A forest may be empty.

Consider the following three conditions:

1. For every v in S, the graph lk_K(v) is a forest.
2. Each edge uv with u,v in S is contained in at most one triangle of K.
3. No triangle of K has all three vertices in S.

**Relative-collapse theorem.** These conditions are equivalent to the
existence of a sequence of elementary triangle/free-edge collapses,
removing no face of K_0, whose result is K_0 together with vertices and
edges. Moreover, when they hold, one such sequence has the following
property for **every** subcomplex Y of I: keep a collapse exactly when
its triangle is still in Y. These retained steps are valid elementary
collapses and remove every triangle of Y outside K_0. They leave
(Y intersect K_0) together with vertices and edges.

When any condition fails, I contains an explicitly described simplicial
2-sphere whose nonzero integral homology class is in the kernel of the
deflation H_2(I;Z) -> H_2(K;Z). In particular, I is not aspherical.

Here and below a disconnected complex is called aspherical when every
component is aspherical. Define W(X) to mean that every connected
simplicial subcomplex of X is aspherical. Then:

    I is aspherical  <=>  K is aspherical and conditions 1--3 hold;
    W(I)             <=>  W(K) and conditions 1--3 hold.

More precisely, when conditions 1--3 hold, every subcomplex Y of I is
aspherical if and only if Y intersect K_0 is componentwise aspherical.
Thus an aspherical vertex inflation cannot create a counterexample to
Whitehead's subcomplex conjecture from a base satisfying that conjecture.
For an aspherical I, any nonaspherical Y must already have a nonaspherical
component in Y intersect K_0. This is a statement about this operation,
not a resolution of Whitehead's general conjecture.

## 2. Inflating a forest

Let L be a finite forest and inflate some of its vertices. Suppose that
every inflated vertex has degree at most one in L and no edge of L has
both endpoints inflated. The resulting graph is again a forest:

- copies of an isolated vertex remain isolated;
- an inflated leaf becomes several leaves with the same neighbor;
- the other edges and vertices do not change.

This also describes disconnected forests, including a component consisting
of one edge. The last hypothesis prevents that edge from becoming a
complete bipartite graph with a cycle.

Build I from K_0 by adding the extra copies one at a time, in any order.
Immediately before adding a copy a of v, its prospective link is the
inflation of lk_K(v) with the currently present multiplicities of its
neighbors. It is a graph, since dim K<=2. Condition 1 makes its base a
forest. If a neighbor u has already been duplicated, the degree of u in
lk_K(v) is the number of triangles containing uv, hence is at most one
by condition 2. An edge uw of lk_K(v) cannot have two duplicated
endpoints, since that would give a triangle vuw entirely in S,
contrary to condition 3. The preceding observation makes every
prospective link a forest.

## 3. Collapsing the added cones

Adding a new copy a attaches a*L along its base L, where L is its
prospective forest link. If x is a leaf of a nontrivial component of L
and y is its neighbor, collapse triangle axy through edge ax. That edge
belongs to exactly one triangle of the new cone and to no triangle of
the older complex, because a is new. This removes one edge of the link.
Continue peeling leaves. Once all edges of L are removed, the added
part has only edges and the vertex a. No vertex is removed. At no point
is a face of the older complex deleted.

To collapse the **final** inflation, process copies in reverse order of
their addition. Later copies have already had all their triangles removed.
Their remaining edges cannot obstruct a triangle/free-edge collapse:
being a coface of an edge in a 2-complex requires a triangle, and a
different edge is not such a coface. Accordingly the leaf argument
applies to the triangles belonging to the next copy. Every nonoriginal
triangle is assigned to its latest-added vertex and is removed once.
This constructs the required sequence without removing original faces.

Fix this entire sequence and a subcomplex Y. Process its pairs (tau,e)
in the same order. If tau is absent, do nothing. If tau is present, e
is present because Y is a subcomplex. No other remaining triangle of Y
contains e: every earlier removed ambient triangle was either absent
from Y or removed from Y at its own step, and e was free among the
remaining ambient triangles. Earlier skipped steps may leave **edges**
in Y, but cannot leave an obstructing triangle. The pair is therefore
an elementary collapse in Y. No original face is removed. At the end
the only triangles left belong to Y intersect K_0, as asserted.

This argument proves a restriction property of the particular collapse
sequence; it does not assume that arbitrary homotopy equivalences
restrict to homotopy equivalences on subcomplexes.

## 4. Three spherical obstructions

Choose two copies, denoted v_0,v_1, whenever v is duplicated. Additional
faces in I may be omitted when specifying a subcomplex.

**A link cycle.** If lk_K(v) contains a simple cycle C, the selected
subcomplex {v_0,v_1}*C is the suspension of a polygon, hence a 2-sphere.
Choose the original copies of the vertices of C. Its oriented fundamental
cycle is v_0*C - v_1*C. Deflation makes these two cones identical, so
their oriented 2-chains cancel.

**Two triangles on a duplicated edge.** Suppose uv lies in distinct
triangles uvw and uvz, with u,v duplicated. Then

    {u_0,u_1} * {v_0,v_1} * {w_0,z_0}

is an octahedral 2-sphere subcomplex. Its fundamental 2-chain is the join
of the three signed zero-cycles. Deflation kills each of the first two
zero-cycles, so the deflated 2-chain is zero.

**A fully duplicated triangle.** If uvw is a triangle and all three
vertices are duplicated, the join

    {u_0,u_1} * {v_0,v_1} * {w_0,w_1}

is again an octahedral 2-sphere, with deflated fundamental chain zero.

In all three cases the fundamental chain is nonzero and has zero
boundary. Since I has no 3-simplices, it is a nonzero integral H_2 class.
The sphere inclusion consequently cannot be nullhomotopic: a
nullhomotopic map induces zero in reduced homology. Thus pi_2(I) is
nonzero in the relevant component. We do **not** infer nonasphericity
merely from H_2(I) being nonzero; aspherical surfaces can have nonzero
H_2. The spherical representative is essential.

These classes also prove necessity in the relative-collapse theorem.
If I collapsed relative to K_0 onto K_0 plus a graph, inclusion of K_0
would induce an isomorphism on H_2: adding only 0- and 1-simplices does
not change the group of 2-cycles. Deflation is a left inverse of that
inclusion and would have zero kernel on H_2(I), contradicting the class
constructed above.

Each condition is independently necessary, even for contractible K:
clone the apex of a cone over a polygon for condition 1; clone the two
endpoints of the common edge in two filled triangles for condition 2;
clone all vertices of a single filled triangle for condition 3.
The other two conditions hold in each respective example.

## 5. Asphericity and subcomplex inheritance

We use an elementary CW fact: adjoining only vertices and edges to a
complex A gives a componentwise aspherical space precisely when A is
componentwise aspherical. One may view the result as a graph of spaces
whose vertex spaces are the components of A and whose edge spaces are
points. Each connected component is homotopy equivalent to a wedge of
its constituent components of A and a graph. This follows by choosing
paths within each component between its finitely many attaching points,
then using homotopy invariance of edge attachment and collapsing a
spanning tree of the connecting graph. In particular each constituent
is a homotopy retract. If they are aspherical, the universal cover is
a tree of contractible vertex spaces joined by intervals and is
contractible. These arguments include isolated new vertices and empty A.

Under conditions 1--3, apply this fact after the collapses in section 3,
first to I, then to every Y. The deflation I->K also has the canonical
section K_0, so independently, asphericity of I implies asphericity of K.
Section 4 excludes asphericity whenever a condition fails. This proves
the first equivalence and the more precise assertion about Y.

If W(K) and the conditions hold, each Y intersect K_0 has aspherical
components; hence every connected Y is aspherical. Conversely W(I)
implies W(K), since K_0 is a subcomplex, and also excludes all the
sphere subcomplexes from section 4. This proves the second equivalence.

## 6. Relation to known results and evidence

Vertex inflation and its absolute homotopy decomposition are classical.
The Björner--Wachs--Welker inflation formula already implies the absolute
asphericity criterion above in dimension two. We make no novelty claim
for that formula or for a new general asphericity test. The specific
increment of this note is the explicit relative collapse, its validity
on **arbitrary** subcomplexes, and the resulting Whitehead inheritance
statement. The elementary proof does not use the poset fiber theorem.
See [SOURCES.md](SOURCES.md) for precise attribution and search limits.

The written proof is the evidence for arbitrary finite K and arbitrary
positive multiplicities. The exact checker constructs and replays finite
collapse or sphere certificates and computes binary boundary ranks by a
separate method. These finite checks validate the implementation and
small cases; they do not decide whether an arbitrary input K is
aspherical and are not a proof-assistant formalization or independent
peer review.
