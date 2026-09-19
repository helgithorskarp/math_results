# Rigidity of the ten-cubic complement at eighteen vertices

19 September 2026. A combinatorial proof with an explicit finite case table
on at most four vertices and reproducible exact checks. Independent review
of this contribution is outstanding.

## Theorem

Let Delta be a finite flag generalized homology 5-sphere over a field.
Assume that its one-skeleton complement H has 18 vertices, minimum degree
three, and exactly ten vertices of degree three. Then its degree sequence
is necessarily

    3^10 4^8.

Equivalently, if the maximum one-skeleton degree is fourteen and exactly
ten vertices attain it, all eight remaining vertices have degree thirteen.
Moreover, with T the number of triangles of H,

    gamma(Delta) = (1,6,8,-2-T),       0 <= T <= 8.

This is a conditional structural theorem. It asserts neither existence of
such a sphere nor the eighteen-vertex Charney--Davis inequality. The
remaining profile is not excluded here. The preceding
[ten-high-degree theorem](../charney_davis_18_ten_high_degree/PROOF.md)
shows why exactly ten is the next frontier, but is not needed to prove
the conditional theorem above.

Every face link, including the empty-face link, is required to have the
homology of a sphere of the appropriate dimension. Neighborhoods are open
neighborhoods in H. Put

    q_v=deg_H(v), t_v=e(H[N_H(v)]), a=gamma_2(Delta),
    b=gamma_3(Delta), L_v=gamma_2(lk_Delta(v)).

## Established inputs

Face counting, with h(t)=sum_i gamma_i t^i(1+t)^(6-2i), gives

    a=39-|E(H)|,
    b=230+(1/2)sum_v q_v(q_v-11)-T,
    L_v=a+8+q_v(q_v-19)/2+sum_(u in N(v))q_u-t_v,
    sum_v L_v=3b+4a
              =846+(1/2)sum_v q_v(3q_v-37)-3T.                  (1)

These identities were derived in the
[nine-high-degree note](../charney_davis_18_nine_high_degree/PROOF.md)
and independently reconstructed in its
[ACCEPT review](../charney_davis_18_review1/README.md).
They also follow directly from independent-triple inclusion-exclusion in H
and gamma_2=f_1-7f_0+30 in a vertex link.

We use L_v>=0. This follows from Davis--Okun,
[Theorem 11.2.1](https://arxiv.org/abs/math/0102104), and the identity
2 gamma_2(Y)=sum_x gamma_2(lk_Y(x)) for a flag homology 4-sphere Y.
The rational-coefficient hypothesis causes no restriction here: universal
coefficients and vanishing lower field homology imply vanishing lower
rational homology for each finite face link; its Euler characteristic then
forces top rational Betti number one.

From [Labbé--Nevo](https://arxiv.org/pdf/1612.01169v2) we use:

- The minimum of 2d vertices for a flag homology (d-1)-sphere, with equality
  only for the cross-polytope boundary; hence q_v<=7 here.
- A flag homology sphere with gamma_1=1 is an iterated suspension of C_5
  (Lemma 3.3).
- If the minimum complement degree is three and a cubic vertex has a
  suspension link, Delta=Gamma*C_6 and b=2gamma_2(Gamma)>=0
  (Theorem 3.5(i), together with Davis--Okun).
- The ell=2 base case in the proof of Theorem 5.2: a twelve-vertex flag
  homology 4-sphere with gamma=1+2t has precisely two types. Its complement
  is either (I) the complement of C_6 plus three disjoint edges, or
  (II) K_4 with two opposite edges each subdivided twice, plus two disjoint
  edges. Type II is obtained by suspending twice the edge subdivision of
  a suspension-to-cycle edge of the suspension of C_5.

In particular, whenever b<0, two nonadjacent cubic vertices of H cannot
have two common neighbors. Otherwise one becomes a vertex with complement
degree at most one in the other's link. Degree zero makes that link a cone;
degree one makes it a suspension, contrary to the preceding input.
Also, nonadjacent vertices of H cannot have identical neighborhoods,
since that too makes a cone vertex in a link.

## A reusable bound for a set of higher-degree vertices

This lemma does not assume that there are exactly ten cubic vertices.
Partition V(H) into C={q=3}, Q={q=4}, and R={q>=5}. Let K=H[R], n=|Q|,
h_v=deg_K(v), and tau_v=e(K[N_K(v)]). For v in R define

    k_v=a+8+q_v(q_v-11)/2
          +sum_(w in N_K(v))(q_w-4)-tau_v,
    D_v=k_v-q_v+h_v.                                          (2)

For every subset S of R,

    0 <= sum_(v in S)L_v <= sum_(v in S)D_v+n alpha(K[S]),       (3)

where alpha is the graph independence number. In particular,

    k_v>=0,    D_v+n>=0,
    D_u+D_v+n>=0 whenever uv is an edge of K.                  (4)

**Proof.** Write c_v=|N(v) intersect C| and y_v=|N(v) intersect Q|.
Then c_v+y_v=q_v-h_v. Equation (1) gives

    L_v=k_v-c_v-(t_v-tau_v)=D_v+y_v-(t_v-tau_v).

For q in Q set B_q=N(q) intersect R. Among the triangles counted in
t_v-tau_v are those with other vertices q and w in R; for a fixed q
they contribute deg_(K[B_q])(v) if v is in B_q. Discarding the other
nonnegative triangle contributions gives the upper bound

    sum_(v in S)D_v
       +sum_(q in Q)sum_(v in S intersect B_q)(1-deg_(K[B_q])(v)).

For any fixed B_q, the nonisolated vertices in K[B_q] contribute at most
zero. Its isolated vertices lying in S are independent in K[S]. Each
inner sum is therefore at most alpha(K[S]), proving (3).
Finally k_v>=0 follows already from L_v=k_v-c_v-(t_v-tau_v)>=0.
The singleton and edge instances of (3) give the rest of (4). QED.

Thus neighboring high-degree vertices can be incompatible even when their
individual link bounds are feasible. Only the singleton and edge instances
are needed in this proof, while (3) remains available for larger frontiers.

## The complete small case reduction

Now |C|=10. Let n_j count the vertices of degree j. Equation (1) and parity
give

    n_4+n_5+n_6+n_7=8,
    5n_5+7n_6+6n_7+3T<=26,
    n_5+n_7 is even,
    a=8-(n_5+2n_6+3n_7)/2,
    b=-2-n_5-n_6-T<0.                                        (5)

There are eighteen possibilities for the degree multiset on R, including
R empty, and |R|<=4. For a candidate graph K on R compute (2), and reject
it if any k_v<0, if its triangle count exceeds the bound on T in (5), or
if a singleton or edge inequality in (4) fails.

[CASE_TABLE.md](CASE_TABLE.md) displays the entire remaining table after
the first two filters, including a negative singleton/edge witness for
every numerical exclusion. Its graph encoding and color-preserving
symmetry rule are explicit. The finite coverage is independently checkable:
there are at most 64 labeled graphs to consider for any row. Alternatively,
all graphs on four vertices have the eleven shapes listed there, as seen
by splitting by edge count and taking complements.

Exactly these cases survive (4):

| Full degree sequence | a | Graph K on R |
|---|---:|---|
| 3^10 4^8 | 8 | empty vertex set |
| 3^10 4^7 6 | 7 | one vertex |
| 3^10 4^6 5^2 | 7 | two isolated vertices, or one edge |
| 3^10 4^4 5^4 | 6 | K_(1,3), or C_4 |

The following structural arguments eliminate the last three rows.

## One sextic vertex: a facet has too few ridge completions

Let r have degree six in the profile 3^10 4^7 6. Equation (1) gives
L_r=-c_r-t_r, so its six neighbors form an independent set A of quartic
vertices. The link of r has eleven vertices and gamma_1=1, so its
complement on B=V(H) minus ({r} union A) is C_5 plus three disjoint edges.
The set B consists of ten cubic vertices and the last quartic vertex w.

If w has internal degree k in H[B], then k is one or two. Its full
neighbor-degree sum is 3k+4(4-k)=16-k, so

    L_w=1-k-t_w>=0.

Consequently k=1. Thus all five C_5 vertices are cubic. Each has exactly
one neighbor in A; each of the other cubic vertices in B has two, and w
has three.

Since A is H-independent, it is a six-vertex facet of Delta. Every ridge
A minus {a}, for a in A, lies in exactly two facets: its link is a
homology 0-sphere, hence has exactly two vertices. Besides a, the other
completion must be an outside vertex x with N_H(x) intersect A contained
in {a}. Vertex r meets all of A, and every vertex in B meets A. Therefore
the second completion must have N_H(x) intersect A={a}. Only the five
C_5 vertices can do this. Distinct ridges require distinct such vertices,
so six ridges would need at least six completions. Contradiction.

## Two quintic vertices

Let r,s have degree five, with six quartic vertices and a=7.

First suppose r,s are nonadjacent in H. At either vertex (1) gives
L=-c-t, so N(r) consists of five independent quartic vertices and L_r=0.
The twelve-vertex link of r has gamma=1+2t. Its complement consists of
the ten cubic vertices, s, and the remaining quartic vertex w.

In type I, consecutive vertices of the underlying C_6 are nonadjacent
in its complement and have two common neighbors. Thus at least three
of those six vertices must be noncubic. Only s,w are available, impossible.
In type II, the two opposite pairs of the four degree-three core vertices
each require a noncubic member. Hence s,w occupy two adjacent core
positions. Vertex s has internal neighbors w and two cubic vertices,
and its other two neighbors are quartic vertices in N(r). Its neighbor-
degree sum is 4+3+3+4+4=18, so L_s=-20+18-t_s<0. Contradiction.

Now suppose r,s are adjacent. Equation (1) gives

    L_r=1-c_r-t_r,       L_s=1-c_s-t_s.

Thus each c is at most one. Their quartic neighborhoods have sizes
4-c_r and 4-c_s in a set of size six. If both c's are zero, they share
at least two neighbors, giving t_r>=2. If exactly one c is one, they
share at least one, contradicting t=0 at that vertex. Therefore both
c's are one, both t's are zero, and the two quartic neighborhoods are
disjoint triples.

The link of r again has gamma=1+2t. Its complement has nine cubic
vertices and the three quartic neighbors of s. Those three quartics are
independent, since t_s=0. In type I all three would have to occupy the
six-vertex core, meeting every edge of the underlying C_6. A three-vertex
cover of C_6 is one of its two alternating triples; such a triple is a
triangle in the complement of C_6. In type II at least one quartic must
occupy each opposite pair of degree-three core vertices, and those two
positions are adjacent. Both possibilities contradict independence.

## Four quintic vertices

Here a=6 and there are four quartic vertices. If K is a star, each leaf
has k_v=0, so it has no cubic neighbor, no triangle, and is adjacent to
all four quartic vertices. The three leaves have identical full
neighborhoods (the center and the four quartics), impossible in a sphere.

Suppose K=C_4. Each high-degree vertex r has

    L_r=1-c_r-t_r>=0

because there are no triangles within K. If c_r=0, then r has three
quartic neighbors, while each of its two neighbors in K has at least
two. Each such pair shares a quartic vertex, producing two different
triangles through r. This is impossible. Hence every c_r=1 and t_r=0,
and each high-degree vertex has two quartic neighbors.

Adjacent vertices of K have disjoint quartic neighborhoods, so opposite
vertices have the same two quartic neighbors. Their cubic neighbors
must be different, since otherwise their full neighborhoods would be
identical. Adjacent vertices also have different cubic neighbors since
t_r=0. Thus the four cubic neighbors are distinct.

Fix r and let s be the opposite vertex of K. The link of r has twelve
vertices and gamma=1+2t. In its complement, s has internal degree one:
only its cubic neighbor remains. The two quartic vertices remaining
in this link have internal degree at most two, because both their
quintic neighbors were deleted. Consequently every internal degree-three
vertex of this link complement is cubic in H.

Type I has six degree-three core vertices, with nonadjacent pairs having
two common neighbors. Type II has four such core vertices, including
the two opposite pairs with that property. Either type violates the
nonsuspension condition for cubic vertices. This excludes the last case.

Only 3^10 4^8 remains. Substituting in (1) and (5) gives a=8, b=-2-T,
and 3T<=26, proving the theorem. QED.

## Limits

The new ingredient is (3), followed by a displayed finite classification
of at most four colored vertices and the structural exclusions above.
The Python checks reproduce all entries, independently generate the
small graphs by shapes, and audit the explicit link models. They do not
prove the imported sphere classifications or formalize the topological
arguments. The previous independent review covers the prior note only.

This pass stops at the single remaining ten-cubic profile. It does not
increase the proved lower bound of ten high-degree vertices to eleven.
Targeted primary-literature and graph searches found no matching result;
that is a search-relative assessment, not a priority claim.
