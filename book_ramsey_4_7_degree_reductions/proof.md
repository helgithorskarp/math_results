# Proof of the reductions

This file preserves the first analytic reductions. The subsequent
[capacity proof](capacity.md) strengthens the universal degree range
to **7..11** and the edge range to **97..121**, with further necessary
structure at degrees seven and eleven. Its degree bounds are analytic
and do not depend on the finite classification in degree6.md.

Throughout, a red edge is an edge of G and a blue edge is an edge
of its complement. Red and blue edge codegrees are bounded by 3
and 6, respectively. Subgraphs and neighborhoods are induced when
an edge count or a degree within a vertex set is taken.

## 1. Triangle defects and integer cuts

Put m=e(G), d_v=d(v), q_v=21-d_v, and let t_R,t_B be the numbers
of monochromatic triangles. Define the nonnegative total defects

    S_R = sum_{uv red} (3-c_R(uv)) = 3m-3t_R,
    S_B = sum_{uv blue} (6-c_B(uv)) = 6(231-m)-3t_B.

Every nonmonochromatic triangle contributes two to sum_v d_v q_v.
Therefore

    t_R+t_B = 1540 - (1/2) sum_v d_v(21-d_v).

Using sum d_v=2m and x_v=d_v-10 gives the exact identity

    S_R+S_B = (3/2) (44 - sum_v x_v^2).                 (1)

For a vertex v, let s_v be the sum of defects of the 21 spines
incident to v. If A=N(v) and B=V(G)\(A union {v}), then

    s_v = 3d_v + 6q_v - 2e(G[A]) - 2e(complement(G)[B]).

Thus s_v is nonnegative and has the parity of d_v; in particular
s_v >= d_v mod 2. Also sum s_v=2(S_R+S_B). It follows from (1)
that

    3 sum_v x_v^2 + o <= 132,                         (2)

where o is the number of odd d_v. For any integer x,

    3x^2 + (x mod 2) >= 8|x|-4.

For |x|=0,1,2 this follows directly; for |x|>=3 it follows from
3x^2 >= 8|x|-4. Since d_v and x_v have the same parity, summing
this inequality in (2) yields sum |x_v| <= 27.5. This sum is an
even integer: |x_v| has the parity of x_v and sum x_v=2m-220 is
even. Hence sum |x_v| <=26, and

    194 <= sum_v d_v <=246,
    97 <= m <=123.                                    (3)

There is also a local form. Write X=sum x_v and
L_v=sum_{u in A} d_u - sum_{u in B} d_u. Counting degrees into
the three sets {v},A,B gives

    L_v = d_v + 2e(G[A]) - q_v(q_v-1)
          + 2e(complement(G)[B]).

Substituting this expression into s_v and then setting d_v=10+x_v
gives the exact identity

    s_v = X + 6 - 2x_v - x_v^2 - 2 sum_{u in N(v)} x_u. (4)

Its lower bound is s_v >= d_v mod 2. These identities require no
regularity or restriction on automorphisms.

## 2. The lower degree bound

We first record an elementary triangle inequality. If abc is a
triangle in an r-vertex graph H whose edge codegrees are at most
three, then

    d_H(a)+d_H(b)+d_H(c) <= r+9.                       (5)

Indeed, an outside vertex adjacent to j of {a,b,c} contributes j
to the left side and binomial(j,2) to the sum of the three edge
codegrees. For j=0,1,2,3, one has j<=1+binomial(j,2).
The six incidences within the triangle and its three contributions
to the codegree sum give (5).

Fix v. In its blue neighborhood B of size q=21-d_v, every vertex
has at most six blue neighbors inside B, because the blue edge
to v has codegree at most six. Consequently G[B] has minimum
degree at least q-7. If q>=16, this exceeds q/2, so G[B] has a
triangle: for any edge, the sum of its endpoint degrees exceeds q
and their neighborhoods must intersect. The triangle's degree sum
is at least 3q-21, whereas (5) bounds it by q+9. For q>=16 these
inequalities contradict each other. Thus q<=15 and d_v>=6.

## 3. Local structure for degrees 14 and 13

Let A=N(v) have size d and let J=G[A]. Every vertex of J has
degree at most three, by the red spine vu. For a nonedge ab of J,
writing h_a=d_J(a), h_b=d_J(b), and c_J(a,b) for their red
common-neighbor count in A, its blue codegree inside A is

    d-2-h_a-h_b+c_J(a,b) <=6.

Equivalently,

    h_a+h_b-c_J(a,b) >= d-8.                          (6)

If d>=15, there is a nonedge in J and its blue codegree is at
least d-8>=7, a contradiction. If d=14, (6) implies that every
nonadjacent pair has h_a=h_b=3 and c_J(a,b)=0. Every vertex has
a nonneighbor, so J is cubic. A graph in which no nonadjacent
pair shares a neighbor is a disjoint union of cliques: a shortest
path between nonadjacent vertices supplies a forbidden two-edge
subpath. Its cubic components would all be K4, impossible on
14 vertices.

Suppose now d=13. Equation (6) gives h_a+h_b-c_J(a,b)>=5 for
nonedges. Every vertex has a nonneighbor, so every h_a is 2 or 3.
The sum of degrees is even, so at least one vertex a has h_a=2.
Every nonneighbor b of a must have h_b=3 and c_J(a,b)=0. If
N_J(a)={p,q}, neither p nor q can be adjacent to any vertex
outside {a,p,q}, or that vertex would be a nonneighbor of a
with a common neighbor. Both p and q have degree at least two,
so pq is an edge. Thus {a,p,q} is an isolated K3. All its
nonneighbors have degree three, and

    J = K3 disjoint-union H,

where H is a cubic graph on ten vertices. Every nonedge of H
has at most one common neighbor, again by (6).

H has no K4 component. Otherwise the remaining six vertices
form a cubic graph F, and any nonadjacent pair in F has at least
3+3-(6-2)=2 common neighbors, a contradiction. Such a pair exists
because F is cubic on six vertices.

## 4. A packing lemma for the ten-vertex component

**Lemma.** Let H be cubic on ten vertices, with at most one common
neighbor at each nonedge, and with no K4 component. If Z is a
vertex set such that no nonadjacent pair in Z shares a neighbor
anywhere in H, then H[V(H)\Z] has at least five edges.

**Proof.** Every component of H[Z] is a clique: a shortest path
between nonadjacent vertices would give a prohibited two-edge
subpath. Each such clique has size one, two, or three, since a
K4 in a cubic graph would be a component of H.

Each clique component C has at least three distinct neighbors
outside Z. This is immediate for a singleton. For an edge C,
the two endpoints have four incidences to outside vertices; if
these incidences use just two outside vertices, those vertices
have two common neighbors and must be adjacent. The resulting
K4 is a component, forbidden. For a triangle C, each vertex
has one outside neighbor. If two vertices of C share that
neighbor w, its nonedge to the third vertex would have two common
neighbors unless w is adjacent to the third as well; again this
would be a K4 component. Thus the three neighbors are distinct.

The outside-neighbor sets of different clique components are
disjoint, since a shared vertex would be a common neighbor of
two nonadjacent vertices in Z. If there are k components and
z=|Z|, then 3k<=10-z. In particular k<=2, z<=4, and for z=4
the component sizes are (3,1) or (2,2), so e(H[Z])>=2. Cubicity
gives

    e(H[V(H)\Z]) = 15 - 3z + e(H[Z]).

For z<=3 this is at least six; for z=4 it is at least five.
The empty set causes no exception. This proves the lemma.

## 5. Exclusion of degree 13

Continue with the degree-13 neighborhood J=K3 disjoint-union H.
Its outside blue neighborhood B has eight vertices. For b in B
put R_b=N_G(b) intersect V(H) and Z_b=V(H)\R_b.

If a,c are nonadjacent in H and have a common neighbor in H,
their blue codegree inside A is exactly

    13-2-3-3+1=6.

Hence no outside vertex can be blue-adjacent to both. In
particular Z_b satisfies the packing lemma, and e(H[R_b])>=5.
Summing over the eight b gives

    sum_{b in B} e(H[R_b]) >=40.                      (7)

On the other hand, for every red edge ac in H, its common red
neighbors include v and c_H(a,c) vertices of H. It therefore
has at most 2-c_H(a,c) common red neighbors in B. Double
counting yields

    sum_{b in B} e(H[R_b])
      <= sum_{ac in E(H)} (2-c_H(a,c))
       =30-3t(H) <=30,                                (8)

contradicting (7). Degrees 13 and above have all been excluded.
Combining this with Section 2 proves 6<=d_v<=12.

## 6. An additional cut when d(v)=12

Now let J=G[N(v)] have twelve vertices. Equation (6) becomes
h_a+h_b-c_J(a,b)>=4 at nonedges. It rules out a vertex of degree
zero. If a has degree one and unique neighbor p, then all
nonneighbors b have degree three and c_J(a,b)=0. Thus p cannot
have other neighbors, and

    J = K2 disjoint-union H,

with H cubic on ten vertices. Here B has nine vertices. A blue
edge between a vertex of K2 and a vertex of H already has
12-2-1-3=6 common blue neighbors inside A. Therefore, if b in B
misses either vertex of K2, it must be red-adjacent to every
vertex of H. There are at most two such b: any edge of H already
has v as a red common neighbor. Any remaining b is red-adjacent
to both vertices of K2; there are at most two of these because
the K2 edge also has v as a red common neighbor. This would give
|B|<=4, contradicting |B|=9. Consequently J has minimum degree
at least two. Its maximum degree at most three was already
established by the spines incident to v.

## 7. The equality case when d(v)=6

Here B has fifteen vertices, and H=G[B] has minimum degree at
least eight. Every edge of H lies in a triangle: its endpoint
degree sum is at least sixteen, so its codegree is at least one.
Every vertex has an incident edge, so belongs to a triangle.
For each triangle, (5) gives

    24 <= degree sum <= 15+9=24.

Equality forces all three vertices to have degree eight in H,
and all three edges to have codegree three in H. Since every
vertex and every edge occurs in a triangle, H is eight-regular
and every edge has exactly three common neighbors. Equality in
the outside-vertex inequality used to prove (5) also says that
each outside vertex has exactly one or two neighbors in every
triangle. In particular H has no K4.

For a in N_G(v), its neighbor set R_a in B is independent in H:
otherwise an edge of H[R_a] would have its three common neighbors
in H plus the additional common neighbor a, violating the red
book constraint. This equality case is a further necessary
condition, not an existence assertion for H.

## Scope and open frontier

All arguments concern arbitrary simple 22-vertex graphs. This first
proof leaves degrees 6 through 12. The later [capacity proof](capacity.md)
reduces the remaining degrees to 7 through 11; neither their
realizability nor the value of R(B4,B7) is established. The historical
degree-12 and degree-six frontiers here have therefore been resolved
as local exclusions. The supplied code
checks arithmetic identities and the compact pattern calculation;
the mathematical proof above remains an unformalized analytic
trust boundary.
