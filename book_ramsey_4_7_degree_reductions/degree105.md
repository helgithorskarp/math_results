# A degree-seven vertex forces 106–115 edges

Author: **six-books-1**, role **researcher**, 2026-09-30.

**Theorem.** Let G be any simple graph on 22 vertices with red edge
codegrees at most three and complement-blue edge codegrees at most six.
If G has a red degree-seven vertex, then **106 <= e(G) <= 115**.
In particular, witnesses with 97..105 or 116..121 edges have minimum
red degree at least eight. The unrestricted Ramsey gap remains 22–23.

The new step excludes exactly 105 edges. Its proof combines incidence
rigidity, a precisely identified classical spectral classification,
and a small complete check of seven-vertex graphs. It does not assume
uniqueness of the degree-seven vertex or classify arbitrary 22-vertex
graphs. No historical priority is asserted.

## 1. Notation and the two scalar branches

Use the [capacity lemma](capacity.md) and the identities in
[single_degree7.md](single_degree7.md), Sections 1–2. Fix a red
degree-seven root v, put A=N_B(v), |A|=14, B=N_R(v), |B|=7,
and let P be the six-regular blue adjacency on A. Let M be the red
14 by 7 cross-incidence matrix, with row sums k and column sums
6+sigma, sigma in {0,1}^7. Put t=sum sigma. Let L be red adjacency
on B, h=L1, e=e(G[B]). All spines inside A are saturated. We have

    1 <= k_a <= 4,  0 <= h_b <= 3,
    e(G)=98+e+t,
    MM^T=3E+diag(k+3)-P^2+diag(k)P+P diag(k)-5P,
    (P+I)k=21*1+M sigma,                           (1)
    s_a=2e-21+10k_a-k_a^2-2(Mh)_a >= (7+k_a) mod 2.

For a row of size k=1,2,3,4, respectively, the last inequality gives

    e >= 6+Mh,  e >= 3+Mh,  e >= Mh,  e+1 >= Mh.    (2)

Here s_a is the total incident unused capacity at a. Put S=M^TM.
Define C by C_bb=6+sigma_b and, for distinct b,c,

    C_bc = 2-(L^2)_bc                         if L_bc=1,
    C_bc = h_b+h_c+sigma_b+sigma_c-1-(L^2)_bc  if L_bc=0.

Then F=C-S has zero diagonal and nonnegative integer off-diagonal
entries, precisely the unused capacities of the spines in B. Put
U=sum_{b<c}F_bc. Direct row summation and the total-capacity identity give

    (C1)_b=9h_b+2e-h_b^2-2(Lh)_b
            +t+(6-h_b)sigma_b-(L sigma)_b,           (3)
    2U=32e-3 sum h_b^2+13t-2 h^T sigma-sum k_a^2.   (4)

Suppose e(G)=105, so e+t=7. At integer k,
(k-3)(k-4)>=0, and at nonnegative integer h,
h^2>=h and (h-1)(h-2)>=0. Thus

    2U <= 32e-3 max(2e,6e-14)+6(7-e)-126.

For e=0,...,7 these upper bounds are
-84,-64,-44,-24,-10,-2,6,14. Only (e,t)=(6,1),(7,0) remain.
Let a_i count rows of size i, i=1,2. Then

    a_4=t+2a_1+a_2,
    sum k_a^2=126+7t+6a_1+2a_2.                    (5)

If (e,t)=(6,1), (4) permits only these profiles:

* h has one zero and six twos, sigma is on the zero, U=0 and all
  rows have size three except one of size four;
* h has two ones and five twos. If sigma is on a leaf, U=2-3a_1-a_2;
  otherwise U=1-3a_1-a_2. In either case a_1=0.

Indeed sum h=12 and sum h^2 can be only 22 or 24. At 22 the first
ordinary profile is forced. At 24, positivity requires h^T sigma=0;
the only profile with a zero is (0,2,2,2,2,2,2).

If (e,t)=(7,0), h has j ones, j threes and 7-2j twos, j=0,1,2,
and

    U=7-3j-3a_1-a_2.                              (6)

For example, if n_i counts the h-values, sum h=14 gives
n_3=n_1+2n_0, and sum h^2=28+6n_0+2n_1<=32, proving this list.

## 2. Two matrix identities for exceptional rows

Put r=k-3*1 and u=M^T r. If t=0, (1) gives Pr=-r and sum r=0.
Multiplying the Gram identity by r gives the exact identities

    M u=4r+P(r^2),
    ||u||^2=4||r||^2-sum r_a^3.                  (7)

The square r^2 here is entrywise. These statements do not impose
regularity on the rows.

If t=1 and a_1=0, let z be the unique sigma-column. Then r has
a_2+1 entries +1, a_2 entries -1, and zeros elsewhere. Write
n=2a_2+1 and n_z=sum_{r_a!=0}M_az. Since Pr=M_z-r,

    ||u||^2=4n-5+3u_z+2n_z,
    u_z is odd.                                  (8)

For the first equality, expand r^T MM^T r using (1),
||Pr||^2=7+n-2u_z, r^TPr=u_z-n, and
(r^2)^TPr=n_z-1. For parity, r^TPr is even because P is symmetric
with zero diagonal, whereas n is odd.

We record two consequences of (7) when a_1=0,t=0.

**One size-two row is impossible.** There is then one size-four row
H and one size-two row T. On these two exceptional positions Pr=-r
forces a blue edge. Equation (7) at H requires H dot u=5, whereas
H dot u=4-|H intersect T|<=4.

**Two size-two rows are impossible.** There are two size-four rows
H_1,H_2 and two size-two rows T_1,T_2. The induced P on these four
positions is either two blue matched H--T edges or a blue K4:
if the H--H edge is absent/present, each H has one/two T neighbors;
the same total forces the T--T edge absent/present.

In the matching case, (7) says each H dot u=5 and T dot u=-3.
Let c_H=|H_1 intersect H_2| and c_T=|T_1 intersect T_2|.
Summing the resulting equations gives c_H=c_T=c and each row's
total cross-intersection equals c-1. Thus c=1 or 2. At c=1 the
two H rows cover all seven points but both T rows are disjoint from
them. At c=2 the T rows are identical, making each H's total cross
intersection even, whereas c-1=1. Both are contradictions.
In the K4 case, the required dot products are 7 and -1, giving
c_H-c_T=4. Hence H_1=H_2 and T_1,T_2 are disjoint. Each T must
have total cross intersection one, again impossible with two identical H.

## 3. Eliminate (e,t)=(6,1)

First eliminate the zero-degree profile. Its isolated column z has
S_zz=7 and, since U=0, S_zb=C_zb=2 for every other column.
Thus (S1)_z=19. But S1=M^T k and every k>=3, so (S1)_z>=21.

Now h has leaves p,q and five degree-two vertices. Let z be the
sigma-column, and put R=C1-3*(6*1+sigma). Then

    u+F1=R.                                      (9)

There are only a_2=0,1 when h_z=2, and a_2=0,1,2 when h_z=1.
Every size-four row contains a leaf, by (2): four degree-two
points would have Mh=8>e+1=7.

**a_2=0.** Let H be the unique size-four row, at position a.
Equation (1) gives M_z=(P+I)e_a: z occurs exactly on a and its
six blue neighbors. In particular z is in H.
For any nonspecial leaf whose neighbor has degree two, (3) gives
R<=-1, contradicting (9) because u=H and F1 are nonnegative.
Thus the two leaves are adjacent and the other vertices form C5.

If z is a leaf, the other leaf has R=0 and is absent from H.
The red cross spine az has unused capacity three: PM_az=6 and
ML_az=0. But H has one leaf and three degree-two points, giving
s_a=1 in (1). Contradiction.

If h_z=2, the two C5 neighbors of z have R=0 and are absent from H.
At z, R_z=2, u_z=1, so (F1)_z=1. Since U=1, F is one unit
edge. The red spine az again has unused capacity three. Formula
(1) forces H to contain both leaves, with s_a=3. Thus H consists
of z, the two leaves, and a nonneighbor w of z on C5. The unique
defect edge joins z to the omitted other nonneighbor, so S_zw=C_zw=4.
But M_z=(P+I)e_a gives PM_aw=S_zw-1=3, while ML_aw=0.
Red cross spine aw therefore has an additional unit defect,
exceeding s_a=3. Contradiction.

**a_2=1 and h_z=2.** Here U=0. If the leaves are not adjacent,
a leaf next to z has R=-2, below u's minimum -1. Every other
leaf has R=-1, requiring the size-two row to contain both leaves
and both size-four rows to avoid them. This violates their weighted cut.
Thus B is K2+C5. At z, (9) gives u_z=2, contrary to (8).

**a_2=1 and h_z=1.** If the leaves are adjacent, R_z=3 and
(F1)_z<=U=1 give u_z=2, again violating (8).
Otherwise the nonspecial leaf has R=-1. It is in the size-two row
and in neither size-four row. Both size-four rows must therefore
contain z. Parity in (8) forces the size-two row also to contain z,
so it is {p,q}, u_z=1 and n_z=3. Equation (8) requires ||u||^2=16,
whereas for these two H rows and T={p,q},
||H_1+H_2-T||^2=6+2|H_1 intersect H_2|<=14.

**a_2=2 and h_z=1.** Here U=0. If the leaves are adjacent, (9)
gives u_z=3, u at the other leaf zero, and u=1 on the five
degree-two points. Thus ||u||^2=14, while (8) gives at least 30.
If the leaves share a neighbor, that neighbor has R=4, above u's
maximum three. Otherwise (9) gives u-values
1,-1,2,3,1,1,1: their squared norm is 18, while (8) gives
18+2n_z>=20. All cases are excluded. Therefore **t=0,e=7**.

## 4. All fourteen rows have size three

Use the h-profile j and budget (6). If j=0, every h=2 and (2)
excludes size-one rows. If j=2, the budget already forces a_1=0.
If j=1, a size-one row is possible only with a_1=1,a_2<=1.
Let its point be p. At that row Pr=-r forces the number of blue
neighbors of size four minus the number of size two to be two.
Consequently P(r^2)<=2+2a_2 there. Equation (7) gives
u_p<=-6+2a_2, whereas u_p>=-2-a_2. These contradict a_2<=1.
Thus a_1=0 in all cases.

Put a=a_2. Then sum u=2a and ||u||^2=8a by (7). The cases
a=1,2 were excluded in Section 2. At t=0 the entries of C1 are
even by (3). If U=1, F1 has value one at the endpoints of its
single unit edge and zero elsewhere. Hence u=C1-18*1-F1 has
squared norm congruent to two modulo four, contradicting ||u||^2=8a.
This excludes j=2 (only a=0,1) and j=1,a=3.

For j=1,a=4, U=0 and u=C1-18*1. If the leaf p is adjacent to
the degree-three point q, u_p=-2 and u_q=4. All four size-four
rows would contain q and, by (2), also p. This makes u_p>=0.
Otherwise the nonzero u-values are either four twos or 4,2,2,
whose squared norms 16 or 24 are below 8a=32.
Thus at j=1 only a=0 remains.

For j=0, (3) gives C1=20*1, so u=2*1-F1 and U=7-a.
If a>=5, then 0<=u<=2 and ||u||^2<=2 sum u=4a<8a.
If a=4, -1<=u<=2; the integer inequality u^2<=u+2 gives
||u||^2<=2a+14=22<32.
If a=3, put f=F1. Then sum f=8, max f<=U=4, and the norm
identity would require sum f^2=28. With max f<=3 this sum is at
most 24. With one entry four and no second four it is at most
16+3^2+1=26; with two entries four it equals 32. Again impossible.
Therefore in every remaining case **k=3*1 and sigma=0**.

## 5. A classical classification leaves two line graphs

Now

    MM^T=3E+6I+P-P^2.                             (10)

On the subspace perpendicular to 1 this is positive semidefinite,
so every nonprincipal eigenvalue of P is in [-2,3]. Thus P is
connected, since a second eigenvalue six would contradict (10).
Its least eigenvalue is exactly -2: rank M<=7 leaves at least seven
kernel dimensions; on those P has eigenvalues 3 or -2. If all were
3, trace P would be at least 6+7*3-6*2>0.

Here we use an external classical theorem, rather than claim a new
spectral classification. Bussemaker–Cvetkovic–Seidel,
[*Graphs related to exceptional root systems*](https://pure.tue.nl/ws/portalfiles/portal/4386333/696566.pdf),
Theorem 1.12 and Proposition 5.10 (printed pp. 5 and 27), imply that a
connected regular graph with least eigenvalue -2 is a line graph,
a cocktail-party graph, or an exceptional graph with order
2(d+2), 3(d+2)/2, or 4(d+2)/3. At d=6 these orders are 16,12,32/3,
never 14. A cocktail-party graph of order 14 has degree 12.
Consequently **P is a line graph**. This established classification
is a proof dependency; its historical enumeration is not rerun here.

Write P=L(H), with H connected and simple and with 14 edges. Along
each edge xy of H, d_H(x)+d_H(y)=8. If H is nonbipartite this
forces degree four everywhere, and hence seven vertices.
If H is bipartite, its two part-degrees r,s have r+s=8 and each
divides 14. Only 1,7 is possible; connectedness then gives one
seven-edge star, not 14 edges. Thus H is a four-regular graph on
seven vertices. Its complement Q is two-regular, either **C7 or C3+C4**.

## 6. The binary incidence matrix is forced

Let N be the 7 by 14 vertex-edge incidence matrix of H. Then
N^TN=P+2I and NN^T=4I+H=3I+E-Q. From (10),

    MM^T=N^T(2I+Q-E/4)N.                          (11)

The middle matrix is positive semidefinite: on 1 its eigenvalue is
9/4, and on 1-perpendicular its eigenvalues are 2+lambda(Q)>=0.
Thus im M is contained in im N^T. Every column of M has the form
N^T x, meaning that its value on an H-edge ij is x_i+x_j in {0,1}.
Its sum is six, so sum x_i=3/2.

Every vertex of either H lies in a triangle: for complement C7 use
{i,i+2,i+4}; for complement C3+C4 use an H-edge inside the four-set
and any point of the three-set. On a triangle,
x_i=(M_ij+M_ik-M_jk)/2 lies in {-1/2,0,1/2,1}.
Connectedness makes all x_i integral or all half-integral, and
sum x_i=3/2 excludes the integral case. Therefore x_i is -1/2 or
1/2, with exactly two negative positions. They cannot be adjacent
in H, so they form an edge of Q. The column of M is precisely
the indicator of the six H-edges avoiding that Q-edge.

Columns of M are distinct. Equal columns would give seven common
red pages on a red B-spine, or at least eight common blue pages
in A on a blue B-spine. Both are forbidden. There are seven
possible Q-edges and seven columns, so every Q-edge occurs once.
This forces M up to column permutation. All such permutations
are covered by allowing every labeled seven-vertex graph on B.

## 7. Complete small final check

For each of the two Q, take A to be the 14 edges of H=complement Q,
P the line-graph adjacency, and B to be the seven Q-edges. Join
v red to B and blue to A, color A-A by complementing P, and use
the forced M just obtained. The only free edges are the 21 pairs
within B. They must have exactly seven red edges.

The [main checker](degree105_check.py) visits all binom(21,7)=116,280
choices for each Q. Exactly 66,090 have maximum red B-degree at most
three, as required by the root spines. Testing all B-spines retains
one choice for Q=C7 and 24 for Q=C3+C4. Every one of these **25**
choices has exactly **14** violating blue cross spines, with at least
seven literal common blue pages. A compact record for every survivor,
including a spine and seven explicit pages, is in
[degree105_expected.json](degree105_expected.json).

The [independent checker](degree105_independent.py) imports no generator
code. It generates all seven-edge, maximum-degree-three B graphs by
binary edge recursion, constructs each literal 22-vertex graph, and
tests its root, B and cross spines with integer bitset intersections.
Its full survivor sets and compact books agree entry by entry with
the matrix-based implementation. Rejection by root or B spines is
already a book; all remaining choices fail a literal cross spine.
Thus the check excludes every completion of both forced templates.

Combining this 105-edge exclusion with the prior
[105–115 theorem](single_degree7.md) proves the stated 106–115 window.

## Reproduction, provenance and trust boundary

Python 3.11+, standard library only, from the repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 book_ramsey_4_7_degree_reductions/degree105_check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 book_ramsey_4_7_degree_reductions/degree105_independent.py
```

The main command also reproduces the primary 21-vertex fixture, audits
the 143,572 labeled scalar states against an independent histogram
weight, checks the new capacity row sums against literal pages,
controls the polynomial identities including their residuals, and
exhaustively checks the small exceptional-row argument. It verifies
the complete binary column domains of both line graphs.

The bridge from arbitrary G to the two templates is the written
unformalized proof above and the cited classical theorem. The two
implementations provide author cross-checks, not independent peer
review or formal verification. No floating-point solver, timeout,
UNKNOWN, imported catalogue, unpublished proof corpus or symmetry
restriction is used. The historical spectral classification is
accepted as published mathematics; its 187-graph enumeration is not
reproduced by these commands. No witness realizability or global
Ramsey endpoint is claimed.

The predecessor capacity lemma has an independent
[capacity review](../book_ramsey_4_7_capacity_review3/review.md), and
the previous uniqueness and 105–115 theorems have an independent
[degree-seven review](../book_ramsey_4_7_degree7_review2/REVIEW.md).
Those verdicts concern the earlier theorems. They do not review the
new incidence-rigidity argument or the 105-edge template exclusion.

Lidicky–McKinley–Pfender–Van Overberghe
[Table 1](https://arxiv.org/html/2407.07285v2) and Radziszowski's
[DS1.18 Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf), refreshed
2026-09-30, retain 22 <= R(B4,B7) <= 23. The known primary fixture
is attributed in [README.md](README.md); reproducing it is validation.
The global flag-algebra upper certificate is not replayed here.
