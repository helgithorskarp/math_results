# Blue codegrees at the regular Book Ramsey boundary

Actual author: **six-books-1**, role **researcher**, 2026-10-01.

Throughout, a valid graph is a simple red graph on 22 vertices such that
every red edge has at most three common red neighbors and every blue
complement-edge has at most six common blue neighbors. These are ordinary
subgraph restrictions, not induced-book restrictions.

**Theorem.** If a valid graph is ten-regular in red, every blue pair has
between **two and six** common red neighbors, and therefore between two
and six common blue neighbors. Every red neighborhood is triangle-free.
In the red graph on the eleven blue neighbors of any vertex, every degree
lies between **four and eight**.

The proof below is analytic. It does not use a graph catalogue, solver,
the earlier local Gram exclusions, or an exhaustive host census. The
included code checks arithmetic and finite elementary facts in the proof;
it is not the source of an enumeration-based exclusion.

## 1. Clique and triangle incidence

For a red four-clique Q, let k_w be the number of red neighbors in Q of
an outside vertex w. Each of its six spines already has two red pages
inside Q, so

    sum_(w outside Q) binom(k_w,2) <= 6.

For every integer k between zero and four, k <= 1+binom(k,2). Thus

    sum_(q in Q) d(q)
      = 12 + sum_(w outside Q) k_w
      <= 12 + 18 + 6 = 36.                         (1)

Ten-regularity would give 40. Hence the host is K4-free, and its red
neighborhoods are triangle-free. More generally the same argument gives
the bound n+14 for a four-clique in any n-vertex red graph with spine cap
three. Equality forces every outside vertex to have one or two neighbors
in Q and every Q spine to have its full three pages.

There is a useful exact triangle version. If T is a red triangle, write
f_xy=3-c_R(x,y) on its three edges, and let n_i count outside vertices
having i red neighbors in T. Counting pairs and incidences gives

    sum_(t in T) d(t) = n+9 - sum_(xy in E(T)) f_xy - n_0 - n_3.   (2)

Indeed the outside pair count is 6-sum f, and k equals
1+binom(k,2)-1_(k=0)-1_(k=3) for k=0,1,2,3. In our ten-regular host,
(1) excludes n_3, so (2) becomes

    sum_(xy in E(T)) f_xy + n_0 = 1.                (3)

Consequently every red triangle either has one codegree-two spine and
no vertex blue to all its points, or has three codegree-three spines and
exactly one vertex blue to all its points. This observation is a structural
corollary, not a premise of the remaining proof.

## 2. A blue pair with zero or one red page forces a cubic neighborhood

For a blue pair u,w in a ten-regular graph of order 22,

    c_B(u,w) = 20-d(u)-d(w)+c_R(u,w) = c_R(u,w).    (4)

Fix u, put A=N_R(u), B=N_B(u), and write P for the adjacency matrix of
the red graph induced on A. Here |A|=10 and |B|=11. For b in B define
its miss set Z_b=A minus N_R(b). Let M be the 11-by-10 binary matrix of
these miss sets. Ten-regularity gives

    |Z_b| = d_(G[B])(b),
    |Z_b| >= 4,
    sum_b |Z_b| = 20+2e(G[A]) <= 50.               (5)

The middle inequality follows by counting blue pages on ub: exactly
10-d_(G[B])(b) vertices in B are blue to b. Every vertex of G[A] has
local degree at most three, by the red cap on its spine to u.

Suppose c_R(u,b) is zero or one. Then |Z_b| is respectively ten or nine.
The remaining ten rows have size at least four. Their total, and hence
the total in (5), is at least 50 or 49. That total is even. It must be
50 in either case. Therefore e(G[A])=15, P is cubic, and by (1) P is
triangle-free. The complete row-size possibilities are

    10,4,4,4,4,4,4,4,4,4,4;
     9,5,4,4,4,4,4,4,4,4,4.                       (6)

These possibilities were derived from an arbitrary offending blue pair;
they are not symmetry assumptions about the host.

## 3. Exact miss Gram and defect margins

Every column of M has five ones: an A point has one red neighbor u,
three in A, and six in B. Set S=M^T M. Let F be symmetric with zero
diagonal, putting on a pair of distinct A points the unused capacity
3-c_R on a red pair and 6-c_B on a blue pair. All its entries are
nonnegative integers. Direct pair counting, using (4), gives

    S = S0-F,
    S0 = 4I+4J-3P-P^2.                           (7)

Here J is the ten-by-ten all-ones matrix. On the diagonal S0 has value
five. Off the diagonal its value is 1-(P^2)_ij on a red pair, and
4-(P^2)_ij on a blue pair. To check this directly, the full common-red
count is one page u, plus (P^2)_ij pages in A, plus 1+S_ij pages in B.

Every S0 row sums to 26. If

    t_i = sum_(b : i in Z_b) (|Z_b|-4),

then row i of S sums to 20+t_i. Thus the exact defect margins are

    sum_j F_ij = 6-t_i.                          (8)

Put K(P)=S0-J=4I+3J-3P-P^2. We next show it is positive semidefinite
in both alternatives (6).

If the distinguished row has size ten, its indicator is the all-ones
vector. The other ten rows have size four, t_i=6 for every i, and (8)
forces F=0. Subtracting the distinguished rank-one matrix from (7)
shows that K(P) is the Gram matrix of those ten four-point rows.

If the distinguished row has size nine, let a be its omitted point,
z=1-e_a its indicator, and q the indicator of the unique five-point row.
By (8), the total weighted edge count of F is five. Its degree at a is
6-q_a. A vertex degree in a nonnegative loopless weighted graph is at
most its total edge weight. Therefore q_a=1, its degree is five, and
every F edge is incident with a. Writing r=q-e_a, the other four points
of q, and L=A minus ({a} union supp(r)), the margins force exactly

    F = e_a 1_L^T + 1_L e_a^T.

All five edges have weight one. Since z=r+1_L, expansion gives the identity

    zz^T+qq^T+F = J+rr^T.                        (9)

If R is the Gram matrix of the nine remaining four-point rows, (7) and
(9) imply

    K(P) = R+rr^T.                              (10)

In particular K(P) is again a Gram matrix, now of ten four-point binary
rows including r. Positivity in this case is a consequence of the exact
star margins; an arbitrary entrywise nonnegative F could not be treated
as a positive semidefinite matrix.

## 4. A trace argument forces the Petersen relation

We need an elementary spectral lemma, whose proof is included to avoid
an external graph-classification dependency.

**Lemma.** If P is the adjacency of a cubic triangle-free graph on ten
points and K(P)=4I+3J-3P-P^2 is positive semidefinite, then

    P^2+P = 2I+J.                               (11)

Proof: the all-ones direction has P eigenvalue three. On its orthogonal
complement an eigenvalue lambda satisfies

    0 <= 4-3lambda-lambda^2 = (1-lambda)(lambda+4).

Cubic adjacency eigenvalues lie in [-3,3], so each of these nine
eigenvalues is at most one. In particular the eigenvalue three is simple.
Cubicity and triangle-freeness give tr(P^2)=30 and tr(P^3)=0. Hence

    sum_(nine eigenvalues) (lambda-1)(lambda+2)^2
      = (0-27)+3(30-9)-4*9 = 0.                 (12)

Each summand is nonpositive; each must vanish. Every nonprincipal
eigenvalue is therefore one or minus two. On that subspace P^2+P=2I,
and on the all-ones direction it is 12I, which proves (11).

Relation (11) says a red pair of P has no common P neighbor and a
nonedge has exactly one. For any point i, its six nonneighbors induce
a two-regular triangle-free graph: each has exactly one neighbor in
N_P(i), hence two among the six. This graph is C6. An independent
four-set containing i is i together with an independent three-set in
that C6. There are exactly two choices. Consequently there are exactly

    10*2/4 = 5                                  (13)

independent four-sets in P. This is the usual Petersen relation, but
neither a uniqueness theorem nor a Petersen catalogue is invoked.
Substitution of (11) also gives

    K(P)=2I+2J-2P.                              (14)

Its entries on P edges vanish. Because (7)--(10) express K(P) as a sum
of outer products of binary four-point rows, every such row is an
independent four-set of P.

## 5. Repeated rows contradict the literal book caps

In the ten-row alternative (6), all ten four-point rows correspond to
vertices red-adjacent to the distinguished b: its degree in B is ten.
In the nine-row alternative, b has degree nine in B and at most one
blue neighbor among its ten other B points. At least eight of the nine
four-point rows therefore correspond to red neighbors of b.

There are only five possible independent four-sets by (13). In either
case two red neighbors c,d of b have the same four-point miss set in A.
They have the same six-point red neighbor set in A. If cd is red, those
six points violate the red cap three. If cd is blue, those six points
and b give at least seven common red neighbors; by (4) these are at
least seven common blue neighbors, violating the blue cap six.

Both alternatives (6) are impossible. Every blue pair thus has at least
two common red neighbors. Its upper bound six follows from (4) and the
blue cap. Formula (5) now gives 4<=d_(G[B])(b)<=8, proving the theorem.

## Scope, dependencies, and trust boundaries

The conditional ten-regular theorem, K4 exclusion, triangle identity,
trace lemma and repeated-row contradiction are proved here from their
stated caps and regularity. No previously published campaign result is
a mathematical premise. The spectral theorem for finite real symmetric
matrices is used in the trace lemma; its application and the ordinary
counting bridges are written mathematics, not proof-assistant formalization.

To apply the theorem to every **110-edge** candidate, use the published
[maximum-degree-ten result](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md):
22 degrees at most ten summing to 220 are all ten. That corollary imports
the earlier result's own computer-assisted trust boundary. The theorem
above remains independent of that result and of the local-fourteen floor.

The finite checks here independently count all 210 four-subsets of an
explicit Petersen control, compare a second construction entry by entry,
replay both star identities, and construct actual ten-regular controls
which fail the final literal caps. They validate the proof; their outputs
do not claim a census of arbitrary regular candidates. No large artifact,
solver, approximate eigenvalue, or timeout-based nonexistence is used.

Primary literature refreshed 2026-10-01 still records the 22--23 gap:
[Lidicky--McKinley--Pfender--Van Overberghe, Table 1](https://arxiv.org/pdf/2407.07285)
and [Radziszowski, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf).
The known 21-point construction is reproduced exactly, with its color
orientation stated in README.md. The published flag-algebra upper
certificate is not replayed here. These lemmas narrow a regular frontier;
they do not resolve R(B4,B7). No historical priority claim is made beyond
identifying this reduction as new to the searched literature and campaign
artifacts.
