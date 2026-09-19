# Excluding the nine-cubic complement at eighteen vertices

Research note, 19 September 2026. Human combinatorial proof; independent
review is outstanding. Computation is supplementary.

## Result and conventions

**Theorem.** There is no finite flag generalized homology 5-sphere on
18 vertices whose one-skeleton complement has minimum degree three and
exactly nine vertices of degree three.

Together with the [previous nine-vertex reduction](../charney_davis_18_nine_high_degree/PROOF.md),
this proves that every such sphere has maximum vertex degree at least 14,
and, if its maximum degree is 14, at least **ten** vertices attain it.
The number ten is not asserted sharp. The full eighteen-vertex
Charney--Davis inequality is not established here.

Generalized homology spheres are over a field, and every face link,
including the empty-face link, must have sphere homology in the appropriate
dimension. Neighborhoods below are open neighborhoods in the complement H.
Write

    q_v = deg_H(v),  T = number of unordered triangles of H,
    t_v = number of H-edges within N_H(v),
    a = gamma_2(Delta),  b = gamma_3(Delta),
    L_v = gamma_2(lk_Delta(v)),
    E_uv = gamma_2(lk_Delta(uv))  when uv is not an H-edge.

We use h_Delta(t) = sum_i gamma_i t^i(1+t)^(6-2i).

## Inputs and counting identities

The following external inputs are used in addition to elementary counting.

1. Davis--Okun, [Theorem 11.2.1](https://arxiv.org/pdf/math/0102104),
   proves gamma_2 >= 0 for flag rational homology 3-spheres.
   Thus E_uv >= 0. The face-link identity for a homology 4-sphere Y is
   2 gamma_2(Y) = sum_v gamma_2(lk_Y(v)), and therefore L_v >= 0.
2. A flag homology (d-1)-sphere has at least 2d vertices, with equality
   precisely for the cross-polytope boundary. A vertex having exactly one
   nonneighbor makes the sphere a suspension. Links in a flag complex are
   induced complexes. See Labbé--Nevo, Lemmas 2.1, 2.4 and 3.2 in
   [arXiv:1612.01169v2](https://arxiv.org/pdf/1612.01169v2).
3. Labbé--Nevo, Theorem 3.5(i), implies: if the minimum complement degree
   is three and a degree-three vertex has a suspension link, then
   Delta = Gamma * C_6, with Gamma a flag homology 3-sphere. In that case
   b = 2 gamma_2(Gamma) >= 0.
4. The ell=2 base case of Labbé--Nevo, Theorem 5.2 and its proof, classifies
   flag homology spheres with gamma-polynomial 1+2t. In dimension four
   they are the triple suspension of C_6, or the double suspension of the
   eight-vertex 2-sphere obtained by subdividing an edge from a suspension
   vertex to a cycle vertex in the suspension of C_5. Explicit complements
   of these two links are given below. This classification, not an
   enumeration of arbitrary graphs, is an external trust boundary.

For the coefficient field, finite field-homology spheres are rational
homology spheres: universal coefficients force all lower rational Betti
numbers to vanish, and the Euler characteristic forces the top rational
Betti number to be one. Apply this argument to every face link. Thus the
rational input in item 1 applies. This uses the full local definition above.

For an eighteen-vertex sphere, direct face counts give

    a = 39 - |E(H)|,
    b = 230 + (1/2) sum_v q_v(q_v-11) - T,
    L_v = a+8 + q_v(q_v-19)/2 + sum_(u in N(v)) q_u - t_v,
    sum_v L_v = 3b+4a
              = 846 + (1/2) sum_v q_v(3q_v-37) - 3T.             (1)

For example, count independent triples of H by inclusion-exclusion and
use gamma_2 = f_1-9f_0+48 and
gamma_3 = f_2-6f_1+22f_0-64. For a vertex link use
gamma_2 = f_1-7f_0+30. These derive (1) without a classification assumption.

Two further elementary observations will be useful. Nonadjacent vertices
of H cannot have identical neighborhoods: either would become a cone
vertex in the other's link. Also, if b<0, two nonadjacent degree-three
vertices cannot have two common H-neighbors. Otherwise, by item 3 their
nonsuspension links would contain a vertex with at most one nonneighbor;
zero makes a cone and one makes a suspension.

## Eight numerical possibilities

Assume that exactly nine vertices have degree three. Call this set C.
Vertex links have at least ten vertices, so every other degree is in
{4,5,6,7}. Let n_j be its multiplicity. Since sum L_v >= 0, (1) gives

    5 n_5 + 7 n_6 + 6 n_7 + 3T <= 18,
    n_4+n_5+n_6+n_7 = 9.

The even degree sum also requires n_5+n_7 odd. Enumerating these few
nonnegative integers gives exactly this table:

| Degrees above three | a | Allowed T | b |
|---|---:|---:|---:|
| 4^8 7 | 6 | 0,...,4 | -4-T |
| 4^6 7^3 | 3 | 0 | -4 |
| 4^7 6 7 | 5 | 0,1 | -5-T |
| 4^8 5 | 7 | 0,...,4 | -5-T |
| 4^6 5 7^2 | 4 | 0 | -5 |
| 4^7 5 6 | 6 | 0,...,2 | -6-T |
| 4^6 5^2 7 | 5 | 0 | -6 |
| 4^6 5^3 | 6 | 0,1 | -7-T |

In particular b<0 in every row. Every vertex in C therefore has a
nonsuspension link. Let Q be the degree-four vertices, and R those of
degree at least five. For v in R, put c_v=|N(v) intersect C|. Formula (1)
can be rewritten as

    L_v = A_(q_v) + sum_(w in N(v) intersect R)(q_w-4) - c_v-t_v,
    A_5=A_6=a-7,   A_7=a-6.                                  (2)

For h in Q the corresponding formula is

    L_h = a-6 + sum_(w in N(h) intersect R)(q_w-4) - c_h-t_h.    (3)

## Seven exclusions

We give every case, including the possibilities for the small induced
graph H[R]. This keeps the finite reduction independent of computation.

**4^8 7.** Let r have degree seven. Equation (2) says L_r=-c_r-t_r,
so r has seven neighbors in Q, forming an independent set U. Its link
has ten vertices and is a cross-polytope boundary. Hence H on its vertex
set B=C union {w}, where w is the remaining quartic vertex, is a perfect
matching. Vertex w has one cubic matching partner and three neighbors
in U. Its neighbor-degree sum is 15, while (1) gives
L_w=-16+15-t_w<0.

**4^6 7^3.** Equation (2) forces every vertex of H[R] to have a neighbor
there. Since T=0, H[R] is a three-vertex path. Each leaf has c=t=0 and
is adjacent to all six vertices of Q. The center has c<=3 and therefore
at least two neighbors in Q. Any such neighbor makes a triangle with a
leaf, a contradiction.

**4^7 6 7.** Both high-degree vertices must be adjacent by (2).
For each, c+t<=1. They have at least four and five Q-neighbors,
respectively, so share at least two. These give two triangles, but T<=1.

**4^6 5 7^2.** Here T=0. Formula (2) requires the degree-five vertex to
be adjacent to a degree-seven vertex, and each degree-seven vertex to the
other degree-seven vertex. Thus H[R] is a path with a degree-seven center.
The degree-five leaf has c=t=0 and four Q-neighbors; the center has c<=2
and at least three Q-neighbors. On six vertices these overlap, making a
triangle.

**4^7 5 6.** The two high-degree vertices must be adjacent. At the
degree-six vertex (2) gives c=t=0, so it has five Q-neighbors. At the
degree-five vertex c+t<=1, so it has at least three Q-neighbors. Their
Q-neighborhoods must be disjoint because t=0 at the degree-six vertex,
but |Q|=7.

**4^6 5^2 7.** Since T=0, (2) forces H[R] to be the path whose center
has degree seven. Its c<=1 gives at least four Q-neighbors. Each leaf
has c<=1 and at least three Q-neighbors. Again their neighborhoods overlap
on six vertices, contradicting T=0.

**4^6 5^3.** Formula (2) rules out isolated vertices of H[R], so this
graph is a path or triangle. For a path, each leaf has c=t=0 and four
Q-neighbors. The center has c+t<=1. Its Q-neighborhood is disjoint from
both leaf neighborhoods; this forces c=1, exactly two center Q-neighbors,
and the same four Q-neighbors for both leaves. The two leaves then have
identical full H-neighborhoods, impossible. For a triangle, (2) and t>=1
give c=0 and t=1 at each high-degree vertex. Each has three Q-neighbors,
and these three sets must be pairwise disjoint. Nine vertices would be
required in Q, which has six.

## The remaining pattern 3^9 4^8 5

Let r be the unique degree-five vertex. Equation (2) gives L_r=-c_r-t_r,
so r has five quartic neighbors U, with U independent, and L_r=0.
Let W=Q minus U, of size three. The vertex set of lk(r) is
B=C union W, of size twelve. This link has gamma-polynomial 1+2t,
so input 4 leaves two possibilities for K=H[B].

Each u in U has three neighbors in B. By (3),

    L_u=2-c_u-t_u >= 0,

so at least one of them belongs to W. Thus there are at least five edges
between U and W. For w in W the number of its U-neighbors is 4-deg_K(w).

### Type I: the triple suspension of C_6

Here K is the disjoint union of the complement of C_6 and three copies
of K_2. Each consecutive pair in that C_6 is nonadjacent in K and has
two common K-neighbors. Such a pair cannot both belong to C by the
nonsuspension observation above. At most three of the six vertices can
belong to C, so at least three belong to W. Since |W|=3, all of W is in
this component, where every K-degree is three. The total number of
U--W edges is consequently three, contradicting the lower bound five.

### Type II: a subdivided suspension of C_5, suspended twice

The nontrivial component of K has eight vertices. Label its four
degree-three vertices A,B,C0,D, forming the cycle A-B-C0-D-A.
The other edges are the paths

    A-p-q-C0,       B-r0-s-D.

Thus it is K_4 with two opposite edges each subdivided twice. The remaining
four vertices of K form two separate edges. These descriptions are also
obtained directly by taking the complement after the stated subdivision.

The pairs {A,C0} and {B,D} each have two common neighbors, so at least one
vertex of each pair belongs to W. A W-vertex of K-degree three contributes
one U--W edge; a vertex of K-degree two contributes two; an endpoint of a
separate edge contributes three. To reach at least five U--W edges, W
must consist of exactly two of the degree-three vertices, one from each
opposite pair, and one endpoint w of a separate edge. Relabel the cycle
so those first two vertices are A,B.

Vertex A has three K-neighbors:
B (quartic), D (cubic), and p (cubic). Its fourth full H-neighbor is in U
and is quartic. Its neighbor-degree sum is therefore 4+3+3+4=14.
Formula (1), with a=7 and q_A=4, yields

    L_A = -15+14-t_A = -1-t_A < 0.

This final contradiction proves the theorem. QED.

## Scope and next frontier

The new statement excludes all twenty triangle-count cases in the eight
rows, by a human proof. It uses the published small-link classification;
the accompanying script checks explicit representatives and arithmetic,
not the completeness of that topological classification. No solver,
sphere census, formal proof assistant, or independent review is claimed.

Combined with the prior note, a negative eighteen-vertex Charney--Davis
example must have at least ten cubic complement vertices. The present
argument stops at that frontier. The full eighteen-vertex inequality and
the sharp multiplicity bound remain open within this research program.
Targeted searches of the primary literature found no matching refinement;
this is search-relative novelty, not a claim of historical priority.
