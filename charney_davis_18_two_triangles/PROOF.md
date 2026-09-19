# At most two triangles in the ten-cubic complement

19 September 2026. A conditional structural theorem for flag generalized
homology spheres, proved combinatorially. Independent review is outstanding.

## Statement and scope

Let Delta be a finite flag generalized homology 5-sphere over a field, and
suppose the complement H of its one-skeleton has degree sequence
`3^10 4^8`. Write C and Q for the cubic and quartic vertices, respectively,
J=H[C], e=|E(J)|, and T for the number of triangles of H. Then:

1. J has no triangles or 4-cycles, and 7<=e<=10.
2. If e=10, J is one of C_10, C_5 disjoint union C_5, or
   Theta(1,4,4) disjoint union K_2. Here Theta(1,4,4) consists of three
   internally disjoint paths, of lengths 1, 4, and 4, between two vertices.
3. T<=2. Consequently gamma(Delta)=(1,6,8,-2-T) and gamma_3 belongs to
   {-4,-3,-2}.
4. At least two quartic vertices have suspension links. More precisely,
   every quartic vertex whose link has gamma_2=0 has a suspension link.

The [preceding profile reduction](../charney_davis_18_ten_cubic_rigidity/PROOF.md)
shows why this degree sequence is the remaining case with exactly ten cubic
vertices. The present theorem assumes the degree sequence directly and does
not depend on that reduction's finite case table. It does not establish
existence or nonexistence of this profile, or the full eighteen-vertex
Charney--Davis inequality. The three displayed graphs are necessary
possibilities for J at e=10, not constructed sphere examples.

Every face link, including the empty-face link, must have the homology of
the appropriately dimensional sphere over the chosen field.

## Inputs and notation

All neighborhoods below are open neighborhoods in H unless subscripted J.
Put q_v=deg_H(v), t_v=|E(H[N(v)])|, and

    L_v = gamma_2(lk_Delta(v)),
    E_uv = gamma_2(lk_Delta({u,v}))  when uv is not an edge of H.

Both quantities are nonnegative. For E_uv this is the three-dimensional
case of [Davis--Okun, Theorem 11.2.1](https://arxiv.org/abs/math/0102104).
For L_v use the face-counting identity
`2 gamma_2(Y)=sum_x gamma_2(lk_Y(x))` for a homology 4-sphere Y.
The rational-homology input applies over any field here: universal
coefficients imply vanishing of lower rational Betti numbers when the
corresponding field homology vanishes, and the Euler characteristic fixes
the top rational Betti number. Apply this to every face link. No claim
that integral homology is torsion-free is needed.

We use [Labbé--Nevo](https://arxiv.org/pdf/1612.01169v2), Lemmas 2.1, 3.2,
3.4, Theorem 3.5(i), and the ell=2 base case of Theorem 5.2. In particular:

- Vertex links in a flag homology sphere are induced. Deleting a vertex
  link leaves the vertex itself and an acyclic induced complex on its
  nonneighbors (Lemma 2.1(iv)).
- A vertex with exactly one nonneighbor makes a flag homology sphere a
  suspension; a vertex with no nonneighbors makes it a cone.
- If a minimum-antipode vertex has a suspension link and the minimum
  antipode number is p>1, the sphere is a join Gamma*C_(p+3).
- A flag homology 3-sphere on ten vertices with gamma_2=0 is a suspension:
  the ell=2 classification gives either Sigma^2 C_6 or Sigma S_8, where
  S_8 is obtained by subdividing a suspension-to-cycle edge of Sigma C_5.

Face counting, or the formulas in the
[nine-high-degree proof](../charney_davis_18_nine_high_degree/PROOF.md), gives

    |E(H)|=31,     gamma(Delta)=(1,6,8,-2-T).                 (1)

For v in C put d_v=deg_J(v), and for q in Q put c_q=|N(q) intersect C|.
The same direct vertex-link count gives

    L_v=4-d_v-t_v                  (v in C),
    L_q=2-c_q-t_q                  (q in Q).                 (2)

For completeness, the general local formula at n=18 and gamma_2(Delta)=8 is
`L_v=16+q_v(q_v-19)/2+sum_(w in N(v))q_w-t_v`, which reduces to (2).

Several consequences will be used throughout.

**Antipodes and triangles.** For cubic v, the independence complex of
H[N(v)] is acyclic on three vertices. It is connected only when that graph
has at most one edge. Thus t_v<=1. Also no triangle of H contains two
cubic vertices and one quartic vertex: at that quartic vertex c_q>=2 and
t_q>=1 would contradict L_q>=0.

**Common neighbors.** Two nonadjacent cubic vertices have at most one
common neighbor in H. Otherwise one has complement degree at most one
in the other's link. Degree zero is impossible, and degree one would
make that cubic link a suspension. By Theorem 3.5(i), Delta would then be
Gamma*C_6, with Gamma a homology 3-sphere, and gamma_3(Delta)=
2 gamma_2(Gamma)>=0. This contradicts (1). Consequently J has no
4-cycles: a chordless one violates the common-neighbor bound, while a
chorded one makes some cubic vertex lie in two triangles.

**Edge count.** If X=|E_H(C,Q)|, (2) implies c_q<=2 and hence

    X=30-2e<=16,       e>=7.                                (3)

## Two exact edge-link formulas

For nonadjacent u,v in C let A=N(u) minus N(v), B=N(v) minus N(u), and
z=|E_H(A,B)|. The sets A and B are disjoint. Then

    E_uv=L_u+L_v-4-z,                  if N(u) intersect N(v) is empty,
    E_uv=L_u+L_v+1-q_w-z,             if N(u) intersect N(v)={w}. (4)

In particular the subtraction in the second formula is 2 when w is
cubic and 3 when w is quartic.

Here is a direct derivation that also fixes the counting convention for z.
Let B_u=V(H) minus ({u} union N(u)), and similarly B_v, and W=B_u intersect
B_v. The two vertex links have fourteen vertices, so
`L_u=23-|E(H[B_u])|`. If the common neighborhood is empty, W has ten
vertices and

    |E(H[W])|=|E(H[B_u])|+|E(H[B_v])|-31+z.

If the common neighborhood is {w}, W has eleven vertices and the right
side gains q_w. These edge-count identities follow by partitioning V(H)
into B_u intersect B_v, the two differences, and the common neighborhood.
Finally gamma_2 of a homology 3-sphere on k vertices with m complement
edges is binom(k,2)-m-5k+16. Substitution proves (4).

## A vertex of degree three in J sees its component within distance two

Suppose d_u=3. Then all H-neighbors of u lie in C and L_u<=1. If a vertex
v has distance three from u in J, their full H-neighborhoods are disjoint.
The middle edge of a shortest three-edge path contributes to z in (4).
Since d_v>=1, L_v<=3, and hence E_uv<=1+3-4-1<0. This is impossible.
A longer distance would contain a vertex at distance three. Therefore
the entire J-component of u lies within distance two of u.

If v is in another component with d_v>=2, (4) again gives
E_uv<=1+2-4<0. Thus all other components are isolated vertices or isolated
edges. If t_u=1, then L_u=0, and the same argument excludes even an
isolated edge outside the component of u.

## There are no cubic triangles

First suppose a triangle contains a vertex u with d_u=3. Its neighbors
in J can be named a,b,c so that ab is the single edge among them. Every
other vertex in this component lies at distance two from u and is adjacent
to exactly one of a,b,c, by the preceding section and the common-neighbor
bound. Call these vertices children of their unique parent, and call
their set B.

For v in B let s=deg_(J[B])(v), so d_v=1+s. In the second formula (4) for
u,v the common vertex is v's parent and L_u=0. Each neighbor of v in B
with that same parent contributes to t_v; each with a different parent
contributes to z. Thus t_v+z>=s and

    0<=E_uv=2-d_v-t_v-z<=1-2s.

Hence s=0: all children are leaves. The vertices a and b have at most one
child each, while c has at most two. If a or b has a child, that parent
itself has degree three in J, so its component must lie within distance
two of it. A child of c would have distance three, and therefore c then
has no children. In every case |B|<=2. The component has at most six
edges, and every other vertex is isolated because t_u=1. This contradicts
e>=7.

It remains to consider a triangle all of whose vertices have J-degree
two. It is a component of J. Each of its vertices has exactly one quartic
neighbor, and these three quartic neighbors are distinct (a shared one
would give a triangle with two cubic vertices). Each triangle vertex
has L=1.

If v outside this component had d_v>=2, it would have at most one
quartic neighbor. Choose a triangle vertex u whose quartic neighbor
is not adjacent to v. Then N(u) and N(v) are disjoint, so
E_uv<=1+2-4<0. Thus all other components have maximum degree one, giving
e<=3+floor(7/2)=6, another contradiction. J is triangle-free.

## The edge bound and its equality cases

If J has maximum degree at most two, then e<=10. Equality means J is
2-regular; since triangles and 4-cycles are absent, its only possibilities
on ten vertices are C_10 and C_5 disjoint union C_5.

Otherwise choose u with d_u=3 and denote its three neighbors by a_1,a_2,a_3.
There are no edges among them. Every other vertex in the component is a
child of exactly one a_i. Put k_i for the number of children of a_i;
0<=k_i<=2. Let B be the set of all children.

For v in B, put s=deg_(J[B])(v). Triangle-freeness means every such edge
joins different branches. In (4) the common vertex is its parent;
L_u=1, d_v=1+s, and z>=s. Consequently

    0<=E_uv<=3-d_v-s=2-2s.

Thus J[B] is a matching, and no child has J-degree three.

If all k_i<=1, put k=k_1+k_2+k_3<=3 and s=|E(J[B])|<=floor(k/2).
The component has 4+k vertices and 3+k+s edges. All remaining components
are isolated vertices or edges. Hence

    e<=3+k+floor(k/2)+floor((6-k)/2)<=8.                      (5)

If, say, k_1=2, a_1 also has degree three. Every child in another branch
must be adjacent to a child of a_1; otherwise it would have distance
three from a_1. Since J[B] is a matching, all those children are matched
to distinct children of a_1. Neither other branch can have two children:
if k_2=2, the pair a_1,a_2 would have common neighbor u, both L-values
one, and at least two cross-neighborhood edges, contradicting (4).
Therefore k_2,k_3<=1. Set r=k_2+k_3 in {0,1,2}. The component has 6+r
vertices and 5+2r edges, and

| r | component vertices | component edges | maximum total e on ten vertices |
|---|---:|---:|---:|
| 0 | 6 | 5 | 7 |
| 1 | 7 | 7 | 8 |
| 2 | 8 | 9 | 10 |

For r=2 the component is exactly Theta(1,4,4), and e=10 requires the two
remaining vertices to form K_2. This proves all the claimed edge bounds
and equality cases. The same argument shows that when e>=9, at most two
vertices of J have degree at most one: this is immediate from
sum_v(2-d_v)=20-2e when the maximum degree is two, and otherwise the only
possibility is Theta(1,4,4) with either two isolated vertices or one K_2.

## Counting the remaining triangles

Every triangle of H now has either one cubic and two quartic vertices,
or three quartic vertices. Denote their numbers by U and V, respectively.
Thus T=U+V and sum_(q in Q)t_q=2U+3V. Summing (2) over Q and using (3),

    0<=sum_(q in Q)L_q=16-X-2U-3V=2e-14-2U-3V.             (6)

If e<=8, this already gives T<=1. If e>=9, a cubic vertex on a mixed
triangle has at least two quartic neighbors and hence J-degree at most
one. Since t_v<=1 and there are at most two such vertices, U<=2.
As e<=10, (6) gives 2U+3V<=6. A value U+V>=3 would then require
U=3,V=0, which is impossible. Hence T<=2. This proves (3) of the theorem.

## Zero-gamma quartic links are suspensions

We record explicitly the small-sphere consequence used here.

**Lemma.** A flag homology 4-sphere Y on thirteen vertices with
gamma_2(Y)=0 is a suspension.

**Proof.** Its complement has
`binom(13,2)-(7*13-30)=17` edges, so its average complement degree is
34/13<3. The minimum complement degree is therefore one or two.
If it is one, Y is a suspension. Otherwise choose a degree-two vertex v,
let L=lk_Y(v), and let M be the link of the edge formed by v's two
antipodes. Lemma 3.4 of Labbé--Nevo gives

    0=gamma_2(Y)=gamma_2(L)+gamma_1(M).

Here L is a ten-vertex homology 3-sphere, and M is a flag homology
2-sphere. Both terms are nonnegative, by Davis--Okun and the minimum
vertex bound for flag homology spheres. Thus gamma_2(L)=0. By the
ell=2 classification cited above, L is a suspension. Theorem 3.5(i)
now gives Y=Gamma*C_5, where Gamma is a homology 2-sphere with
gamma_1(Gamma)=gamma_1(Y)-1=2. But then gamma_2(Y)=2, a contradiction.
This excludes minimum complement degree two. QED.

Every quartic vertex link in Delta has thirteen vertices. By (6) their
eight nonnegative integral L-values sum to at most six. At least two
therefore vanish, and the lemma makes those links suspensions.

There are stronger conditional counts: if T=2 and (U,V)=(2,0), at least
six quartic links are suspensions; if (U,V)=(1,1), at least seven are;
if (U,V)=(0,2), all eight are. These follow from (6) and e<=10.

## Evidence and limits

The proof is the argument above, with the stated primary-source inputs.
`verify.py` supplies exact checks of the edge-link formulas against induced
edge counts, all small rooted configurations used after the radius-two
reduction, the numerical triangle bound, and the two classified small-link
models. Its data do not certify that any candidate graph is a sphere.
No solver, catalogue-completeness assumption, or formal proof assistant is
part of the theorem's proof. The earlier exploratory graph screen is not
needed and is not distributed as proof evidence.

Primary-literature searches on the publication date checked the relevant
small-vertex results of Labbé--Nevo and Nevo--Petersen and the Davis--Okun
input. The suspension lemma is presented as a consequence of those
results, not as an independent classification. No global priority claim
is made for the eighteen-vertex conditional constraints.
