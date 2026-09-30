# Neighborhood capacities: analytic degrees 7–11 and boundary cuts

Author: **six-books-1**, role **researcher**, 2026-09-30.

Let G be any simple graph on 22 vertices, with red edge codegrees at most
three and blue edge codegrees at most six. No symmetry or regularity
assumption is made. The following conclusions are proved analytically:

- Every red degree is between **7 and 11**. In combination with
  [proof.md](proof.md), the edge range improves to **97–121**.
- At a red degree-seven vertex, the induced blue graph on its fourteen
  blue neighbors is six-regular. Each of its seven red neighbors has six
  or seven red neighbors in that fourteen-vertex set. Every spine within
  that set has its full codegree: three if red, six if blue, in the full G.
- At a red degree-eleven vertex, its eleven-vertex red neighborhood has
  no isolated vertex, at most one vertex of local degree one, an odd
  number of local degree-two vertices from {1,3,5,7}, and all remaining
  vertices of local degree three. There are only eight possible local
  degree histograms; this is not an enumeration of graphs.

The degree-six exclusion here needs no finite classification. The earlier
[degree6.md](degree6.md) remains a separate, stronger description of the
equality case used in that earlier proof. None of these reductions decides
whether a 22-vertex witness exists.

## 1. A general capacity identity

Use color 1 for one of the two colors. Its maximum edge codegree is r;
the other color's maximum edge codegree is s. Fix a vertex v, let A be
its color-1 neighborhood of size d, and let B be the other n-1-d=q
vertices. Write J for the color-1 graph induced on A, e=e(J), h_i=d_J(i).
The spine vi implies h_i<=r.

For an edge ij of J, its remaining capacity for common color-1 neighbors
in B is r-1-c_J(i,j); the subtracted one is v. For a nonedge ij of J,
its color-2 codegree inside A is d-2-h_i-h_j+c_J(i,j). Its remaining
capacity for common color-2 neighbors in B is therefore
s-d+2+h_i+h_j-c_J(i,j). All these capacities are nonnegative.

Their sum C satisfies the exact identity

    2C = sum_i [(3d+r-s-4)h_i - 3h_i^2]
         + 2(s-d+2) binom(d,2).                       (1)

To prove it, sum the capacities separately over edges and nonedges.
The common-neighbor sums are 3t(J) over edges and
sum_i binom(h_i,2)-3t(J) over nonedges. Also
sum_{ij nonedge}(h_i+h_j)=sum_i h_i(d-1-h_i) and 2e=sum h_i.
Substitution gives (1); the triangle terms cancel.

For b in B put R_b=N_1(b) intersect A, Z_b=A\R_b, and z_b=|Z_b|.
The triangles with b and a spine in A consume

    f_b = e(J[R_b]) + e(complement(J)[Z_b])
        = e - sum_{i in Z_b} h_i + binom(z_b,2).       (2)

Each triangle consumes exactly one of the capacities being summed.
Consequently U=C-sum_b f_b is nonnegative. In fact U is exactly the sum
of the unused codegree capacities of all spines in A in the full graph.
Define nonnegative row costs

    delta_b = binom(r+1,2) - sum_{i in Z_b} h_i + binom(z_b,2)
            = (z_b-r)(z_b-r-1)/2 + sum_{i in Z_b}(r-h_i).

Both terms on the last line are nonnegative integers. Equations (1)–(2)
give the useful exact budget

    U + sum_b delta_b = D = C-q(e-binom(r+1,2)),       (3)
    2D = sum_i [(3d+r-s-4-q)h_i - 3h_i^2]
         + 2(s-d+2) binom(d,2) + qr(r+1).             (4)

In particular D>=0. These identities apply in either color.

## 2. Analytic degree bounds

For the red neighborhood, set n=22,r=3,s=6. A local degree lies in
{0,1,2,3}, so (4) has the rigorous upper bound

    2D <= d max_{0<=h<=3} [(4d-28)h-3h^2]
           + 2(8-d) binom(d,2) + 12(21-d).

At d=12,13,14 this is respectively -24,-99,-210, a contradiction.
Degrees at least fifteen are excluded directly: a graph on d vertices
of maximum degree three has a nonedge, and its blue codegree there is
at least d-2-3-3=d-8>=7. Thus the red degree is at most eleven.

For the blue neighborhood, set r=6,s=3 and d=the blue degree. Then

    2D <= d max_{0<=h<=6} [(4d-22)h-3h^2]
           + 2(5-d) binom(d,2) + 42(21-d).

For d=15,...,21 the respective upper bounds are
-48,-126,-240,-396,-600,-858,-1176. These exact seven integer values
are also included in capacity_expected.json and checked by
capacity_check.py, using two independent arithmetic evaluations.
This finite scalar check covers every possible blue degree at least
fifteen; it is not a graph enumeration. Hence the blue degree is at
most fourteen and the red degree is at least seven.

The previously proved lower edge bound 97 still applies. The upper
degree bound eleven implies 2e(G)<=22*11, hence e(G)<=121.

## 3. Equality at red degree seven

Its blue neighborhood has d=14, r=6,s=3, q=7. Equation (4) gives

    2D = sum_i (34h_i-3h_i^2) - 1344.

On the integers 0<=h<=6, 34h-3h^2 has unique maximum 96 at h=6.
Since 14*96=1344 and D>=0, every h_i is six and D=0. Equation (3)
therefore forces U=0 and every delta_b=0. With all h_i=6,
delta_b=(z_b-6)(z_b-7)/2. Thus z_b is six or seven. Here Z_b is
the red neighbor set of b in A. U=0 says every spine in A attains its
full permitted codegree in G. This proves all stated equality cuts.

## 4. The degree-eleven budget and scalar histograms

Now A is the eleven-vertex red neighborhood, r=3,s=6,q=10. Put
a_i=3-h_i and let n_j count the local degree-j vertices. Equation (4)
becomes

    2D = 21 - sum_i (3a_i^2-2a_i)
       = 21 - 21n_0 - 8n_1 - n_2.                   (5)

Equation (3) is, more explicitly,

    U + sum_b [(z_b-3)(z_b-4)/2 + sum_{i in Z_b} a_i] = D.   (6)

Also sum h_i is even. Enumerating the four degree counts n_0,...,n_3
(not graphs), and minimizing the row cost
by selecting the z largest local degrees for each z=0,...,11, leaves
exactly the following twelve necessary histograms:

    n_0=0, n_1=0, n_2 in {1,3,5,7};
    n_0=0, n_1=1, n_2 in {1,3,5,7};
    n_0=0, n_1=2, n_2 in {1,3,5};
    n_0=1, n_1=0, n_2=0;
    n_3=11-n_0-n_1-n_2 in every case.

This small integer coverage is completely reproduced by the checker.
It also follows directly from (5): if n_0=0, n_2 is odd and n_1<=2.
For n_1=0,n_2>=9 the best row cost is at least one, exceeding
D/10; for n_1=1,n_2=9 it is at least two, again exceeding D/10.
If n_0>0, the only nonnegative budget is n_0=1,n_1=n_2=0.

If two local degree-one vertices exist, they must be adjacent: at a
nonedge, blue codegree <=6 gives h_i+h_j-c_J(i,j)>=3. Their edge
can have at most two common red neighbors in B, since v is already
one. But their three candidate histograms have D<=2. Every outside
vertex missing either of the degree-one vertices incurs row cost at
least two. Thus at most one of the ten outside vertices can miss
either, and at least nine are common red neighbors, a contradiction.

It remains to exclude the isolated-vertex histogram.

## 5. Excluding an isolated vertex at degree eleven

Suppose J={a} disjoint-union H, with a isolated and H cubic on ten
vertices. Equation (5) gives D=0. By (6), every b in B is adjacent
to a, and Z_b is a subset of H of size three or four. Also U=0, so
every spine within A is saturated. In the full G, a has degree eleven,
with red neighborhood {v} union B; v is isolated there. Applying the
same zero budget at a shows that G[B] is also cubic on ten vertices.

For a red edge of H, at most 2-c_H common neighbors remain in B.
For each b, cubicity gives

    e(H[R_b]) = 15-3|Z_b|+e(H[Z_b])
              >= 3 + 3*1_{|Z_b|=3} + e(H[Z_b]).

Summing over the ten b and comparing with 30-3t(H) forces H to be
triangle-free, every |Z_b|=4, and every Z_b independent in H.
Interchanging a and v proves the same facts for G[B] and for the
column miss sets: every vertex of H has exactly four blue neighbors
in B, forming an independent set in G[B].

Let P be the adjacency matrix of H and M the 10 by 10 zero-one matrix
of blue cross edges from B to H. Its row and column sums are four.
For an H-edge, the corresponding columns have inner product zero.
For an H-nonedge, its blue codegree inside A is 3+c_H; saturation
in G therefore gives column inner product 3-c_H. The diagonal is four,
so, with I the identity and E the all-ones matrix,

    M^T M = 4I + 3E - 3P - P^2.                      (7)

This is an exact positive semidefinite Gram matrix. The eigenvalues
of the real symmetric cubic adjacency matrix P lie in [-3,3], by
|x^T P x|<=3 x^T x. For an eigenvector perpendicular to the all-ones
vector, with eigenvalue lambda, (7) implies
(1-lambda)(lambda+4)>=0, hence lambda<=1.

Select the all-ones eigenvalue three and call the remaining nine
eigenvalues lambda_i. Triangle-freeness and cubicity give
sum lambda_i^2=21 and sum lambda_i^3=-27. Consequently

    sum_i (lambda_i-1)(lambda_i+2)^2
      = -27 + 3*21 - 4*9 = 0.

Each term is nonpositive, so each lambda_i is 1 or -2. It follows
by the spectral theorem that P^2+P-2I=E: on the all-ones vector both
sides have eigenvalue ten, and on its orthogonal complement both
are zero. Thus every nonadjacent pair in H has exactly one common
neighbor. No catalogue or classification of cubic graphs is used.

For any independent four-set S in H, let t_w be the number of its
neighbors at each of the six vertices w outside S. Cubicity gives
sum t_w=12. Unique common neighbors of pairs in S give
sum binom(t_w,2)=6. Therefore sum (t_w-2)^2=0, so all six t_w are
two. Two independent four-sets cannot be disjoint: either of the
two vertices outside both would then have at least four neighbors.

The independent four-sets Z_b are consequently pairwise intersecting.
At any red edge bb' of the cubic graph G[B], its common red neighbors
in H number 2+|Z_b intersect Z_b'|>=3. Vertex a is one more common
red neighbor. This gives at least four, contradicting the red cap three.
The isolated-vertex histogram is impossible.

Exactly eight of the scalar histograms remain, as stated at the start.

## Scope, provenance and checks

The proof is an unformalized analytic proof with exact identities and
the ordinary real symmetric spectral theorem. The scalar histogram
coverage uses only four degree counts; it does not assume a graph
catalogue, exhaust arbitrary 22-vertex graphs, or settle the Ramsey gap.
The primary book-Ramsey literature and independently reproduced
21-vertex baseline are documented in [README.md](README.md). Those
primary sources were refreshed on 2026-09-30. This note makes no
priority claim for its elementary counting mechanism.

Run `python3 book_ramsey_4_7_degree_reductions/capacity_check.py`.
It checks capacities by literal edge/nonedge codegrees and by (1),
checks (2) for every subset of every labeled graph of orders zero
through five, verifies actual unused capacities at every root of
the valid primary baseline in both colors, reproduces all scalar
degree bounds and the twelve-to-eight histogram reduction, and
checks (7) on an exact Petersen incidence control. The latter is
a control for the algebra, not a dependency of the analytic proof.
