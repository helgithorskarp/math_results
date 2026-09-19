# Excluding the ten-cubic complement by suspension compatibility

19 September 2026. A combinatorial proof, with its dependency boundary
listed in [PREMISES.md](PREMISES.md). Independent review is outstanding.

## Theorem and corollary

**Theorem.** No finite flag generalized homology 5-sphere over a field has
one-skeleton complement of degree sequence `3^10 4^8`.

**Corollary.** If the one-skeleton of an eighteen-vertex flag generalized
homology 5-sphere has maximum degree fourteen, at least **eleven** vertices
attain that degree.

The corollary also uses the preceding
[ten-high-degree theorem](../charney_davis_18_ten_high_degree/PROOF.md) and
[ten-cubic profile reduction](../charney_davis_18_ten_cubic_rigidity/PROOF.md).
The first gives at least ten cubic complement vertices when its minimum
degree is three; the second forces the excluded degree sequence when
there are exactly ten. The main theorem below assumes that degree sequence
directly. The full eighteen-vertex Charney--Davis inequality is not proved;
profiles with eleven or more cubic vertices remain outside this theorem.

A generalized homology sphere here has the appropriate sphere homology
in every face link, including the empty-face link.

## Established constraints used in this proof

Suppose, for contradiction, that H is such a complement. Let C and Q be
its ten cubic and eight quartic vertices. Write J=H[C], d_v=deg_J(v),
e=|E(J)|, c_q=|N_H(q) intersect C|, t_v=|E(H[N_H(v)])|, and
L_v=gamma_2(lk_Delta(v)). Neighborhoods below are open.

We use the following parts of the
[preceding structural proof](../charney_davis_18_two_triangles/PROOF.md):

1. J has no triangles or 4-cycles, and 7<=e<=10.
2. No triangle of H has two cubic vertices. Two nonadjacent cubic
   vertices have at most one common H-neighbor.
3. L_q=2-c_q-t_q>=0 for q in Q. In particular c_q<=2; if c_q=2 then
   L_q=t_q=0, and the link of q is a suspension.
4. If J has a degree-three vertex a, its component has the following
   form: a has three independent neighbors a_1,a_2,a_3; all remaining
   vertices of the component are children of unique a_i; and edges among
   the children form a matching between different branches. Every other
   component is an isolated vertex or isolated edge.
5. For nonadjacent cubic u,v with disjoint full H-neighborhoods,

       gamma_2(lk_Delta({u,v}))=L_u+L_v-4-z>=0,              (1)

   where z counts H-edges between those neighborhoods. For d_v=2 one has
   L_v=2 and exactly one quartic neighbor, which we denote by f(v).

These are structural and local-link statements; the numerical bound
T<=2 is not needed here. To indicate their provenance: face counting
gives gamma_3(Delta)=-2-T and L_v=4-d_v-t_v for v in C. The
three-dimensional Davis--Okun theorem gives the nonnegative edge-link
quantities. Vertex-link nonnegativity follows from
`2 gamma_2(Y)=sum_x gamma_2(lk_Y(x))` in dimension four. A cubic suspension
link would, by Labbé--Nevo's minimum-antipode join theorem, force
gamma_3>=0; this proves the common-neighbor restriction. The source derives
(1), the triangle exclusion, and the rooted component description by
explicit edge counts. In particular its distance-three contradiction and
matching conclusion do not use a graph catalogue.

For clarity, the small-sphere step in item 3 is also recalled. If a
thirteen-vertex flag homology 4-sphere Y has gamma_2(Y)=0, its complement
has seventeen edges and hence minimum degree one or two. Degree one
makes Y a suspension. In the degree-two case, the antipode identity gives
`0=gamma_2(L)+gamma_1(M)`, with L a ten-vertex homology 3-sphere. Both
terms are nonnegative. The small gamma_1=2 classification makes L a
suspension, and the minimum-antipode join theorem gives Y=Gamma*C_5,
where Gamma is a homology 2-sphere with gamma_1=2. This would give
gamma_2(Y)=2, a contradiction. The precise primary references and field
hypotheses are recorded in PREMISES.md.

Since the cubic vertices have total degree thirty, their quartic
incidences number

    X=|E_H(C,Q)|=30-2e.                                     (2)

Let p be the number of quartic vertices with c_q=2, and let n_0 be the
number with c_q=0. Counting the eight quartic vertices gives

    p=X-8+n_0>=22-2e>=2.                                   (3)

The central issue is therefore how a quartic with two cubic neighbors
can have a suspension link.

## A local suspension-compatibility lemma

The following argument is graph-local: apart from the existence of the
suspension pair, it uses only degrees three/four, J being triangle-free,
the common-neighbor restriction, and c_q+t_q<=2 for quartic vertices.

**Lemma.** Let q in Q have cubic neighbors x,y. Then there are cubic
vertices u,v of J-degree two such that

    x -- u -- v -- y                                        (4)

is a three-edge path in J. If N_H(q)={x,y,r,s}, with r,s in Q, then after
possibly interchanging r,s,

    N_H(u)={x,v,r},    N_H(v)={u,y,s}.                       (5)

In particular, the two quartic neighbors of q are exactly the unique
quartic neighbors of the two internal vertices of the path.

**Proof.** Since c_q=2, item 3 gives t_q=0 and a suspension link. Set
A=N_H(q)={x,y,r,s}; it is independent in H. The complement of the link
is H[B], where B=V(H) minus ({q} union A). A suspension pair is an
isolated edge uv in H[B]. Consequently

    N_H(u) minus {v} = S subset A,
    N_H(v) minus {u} = R subset A,

where |S| is two or three according as u is cubic or quartic, and likewise
for |R|.

If u,v are both quartic, each of S,R has size three and contains at
least one of x,y. Thus c_u>=1 and |S intersect R|>=2 gives t_u>=2.
This contradicts c_u+t_u<=2.

If u is cubic and v quartic, R has size three and contains at least one
of x,y. Along with the cubic neighbor u this gives c_v>=2. But
|S intersect R|>=1 gives a triangle through uv, so t_v>=1, again a
contradiction. The reversed orientation is identical.

Thus u,v are cubic. No triangle contains their edge uv, so S and R
are disjoint two-element sets partitioning A. If one contained both
x,y, those nonadjacent cubic vertices would have two common neighbors:
q and that endpoint of uv. This is forbidden. Each of S,R therefore
contains one cubic and one quartic vertex, which proves (4)--(5). QED.

Two immediate consequences will be used without assuming any further
topology:

- The cubic neighbors of a quartic counted by p lie in the same component
  of J, have no common J-neighbor, and must be endpoints of (4).
- A fixed unordered cubic pair can belong to at most one such quartic:
  two of them would be two common H-neighbors of that nonadjacent pair.

## Components containing a J-degree-three vertex are impossible

Choose a degree-three vertex a of J and use the rooted description in
item 4. A path (4) must have a middle edge whose endpoints both have
J-degree two. There are only two possibilities inside this component.

- The middle edge joins a parent a_i to one of its children b. For a_i
  to have degree two, its other neighbor must be a. Thus one endpoint
  of (4) is a, which has no quartic neighbor. It cannot be x or y.
- The middle edge joins two matched children from different branches.
  The endpoints of (4) are their parents a_i,a_j. If either parent has
  degree three it again has no quartic neighbor. Otherwise both have
  degree two, and they share the J-neighbor a. They cannot additionally
  share q.

Edges incident with a cannot be middle edges of (4), and there are no
other types of edge. Outside this component, isolated vertices and edges
do not contain such a path. Therefore no quartic can have two cubic
neighbors, contradicting p>=2 in (3).

We have proved that J has maximum degree at most two. All its components
are paths (including isolated vertices) and cycles of length at least five.

## A distance-three rule for vertices of J-degree two

Suppose u,v have J-degree two, are nonadjacent in J, have no common
J-neighbor, and a J-edge joins their J-neighborhoods. If f(u) differed
from f(v), their full H-neighborhoods would be disjoint. Formula (1),
with L_u=L_v=2 and z>=1, would then give a negative edge-link gamma_2.
Thus

    f(u)=f(v).                                             (6)

In particular, this applies to endpoints of a three-edge segment in a
path component. It also applies to vertices three steps apart on any
cycle of length at least six.

## There are no cycle components

On a cycle of length at least seven, fix a vertex v_i. The vertices
v_(i-3) and v_(i+3) are distinct. By (6), all three have the same unique
quartic neighbor, contradicting c_q<=2.

On C_6, (6) forces the quartic labels around the cycle to be

    A, B, D, A, B, D,

where A,B,D are distinct. (Adjacent cubic vertices cannot share a
quartic neighbor.) The compatibility lemma applied to A forces its
quartic neighbors to be B,D, whichever of the two length-three paths
between the opposite A-labeled vertices provides its suspension pair.
Applied to B it forces its quartic neighbors to be A,D. Hence A,B,D
form a triangle in H. But c_A=2 forces t_A=0, a contradiction.

Finally, a C_5 component cannot contain a cubic neighbor of any quartic
counted by p. A three-edge path within C_5 has endpoints with a common
J-neighbor, contradicting the compatibility lemma's common-neighbor
restriction. Such a path cannot leave the component either.

We use the following elementary bound on path components. Each of their
vertices is incident with at most one quartic counted by p. An internal
vertex has only one quartic neighbor. An endpoint has only one possible
partner at path-distance three, and that cubic pair cannot share two
quartics. An isolated vertex has no possible partner. Consequently a
set of path components on m vertices can account for at most floor(m/2)
quartics counted by p.

If J has one C_5 and five vertices in path components, then p<=2 and
e<=9. Formula (3) gives p>=4, a contradiction. If J consists of two
C_5 components, then p=0 contradicts (3). These are all possibilities
after the longer cycles have been removed.

Thus J is a disjoint union of paths.

## Path components give the final contradiction

Let k>=1 be the number of path components, counting isolated vertices.
Since J has ten vertices, e=10-k, and (3) yields

    p>=2+2k.

The path bound just proved gives p<=floor(10/2)=5. If k>=2 these
inequalities are incompatible.

If k=1, J=P_10. Number its vertices v_0,...,v_9 in order. The internal
vertices v_1,v_4,v_7 all have J-degree two. Applying (6) to v_1,v_4 and
then v_4,v_7 makes all three share their unique quartic neighbor. This
again contradicts c_q<=2. No J remains, proving the theorem. QED.

## Evidence and limits

The proof eliminates all possible components, including all three named
ten-edge families C_10, C_5+C_5, and Theta(1,4,4)+K_2. Its main new result
is the local compatibility lemma, not a numerical refinement or a search
through attachments.

`verify.py` checks all 100 local suspension-pair incidence patterns,
the two types of middle edge in small rooted models, and the elementary
path/cycle rules. It is corroborative and does not establish spherehood
or replace the written universal arguments. No solver or external graph
catalogue is used. The predecessor proofs, including their imported
topological theorems, are explicit mathematical dependencies. The older
independent ACCEPT review covers only the nine-high-degree result;
this proof and the later dependencies remain unreviewed.
