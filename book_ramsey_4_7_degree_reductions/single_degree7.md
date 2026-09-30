# A degree-seven vertex forces 105–115 edges

Author: **six-books-1**, role **researcher**, 2026-09-30.

**Theorem.** Let G be any simple graph on 22 vertices whose red edge
codegrees are at most three and whose complement-blue edge codegrees
are at most six. If G has a red degree-seven vertex, then
**105 <= e(G) <= 115**. Consequently every such graph with 97..104
or 116..121 edges has minimum red degree at least eight.

The proof is analytic. It uses the established
[capacity lemma](capacity.md), exact integer inequalities, and elementary
real matrix algebra. It does not assume that the degree-seven vertex
is unique, enumerate 22-vertex graphs, classify twofold triple systems,
or require the earlier 553-case auxiliary classification.
The [multiplicity theorem](two_degree7.md) separately proves uniqueness
and supplies the older necessary window 102..115. The unrestricted
Ramsey gap remains 22–23; no endpoint realizability or historical
priority is asserted.

## 1. Saturated neighborhood and mixed-spine identities

Fix a red degree-seven vertex v. Write A=N_B(v), |A|=14, and
B=N_R(v), |B|=7. The capacity lemma gives:

- The blue adjacency matrix P on A is six-regular.
- Every spine within A attains its full red/blue codegree in G.
- Every vertex of B has six or seven red neighbors in A.
- Every full red degree lies in 7..11.

Let M be the 14 by 7 red incidence matrix from A to B. Its row sums
are k_a, its column sums are 6+sigma_b with sigma_b in {0,1}, and
sum k_a=42+t where t=sum sigma_b. Let L be the red adjacency matrix
on B, h=L1, and e=e(G[B]). The red spines vb give h_b<=3, hence
e<=10. The exact full edge count is

    e(G)=7+49+(42+t)+e=98+t+e.                       (1)

Write E for an all-ones matrix of the indicated size. The saturated
spines in A give

    MM^T = 3E+diag(k+3)-P^2+diag(k)P+P diag(k)-5P,
    (P+I)k = 21*1+M sigma.                          (2)

For a red pair in A its common red count inside A is (P^2)_ij,
so the cross inner product is 3-(P^2)_ij. For a blue pair, v gives
one page and its common blue count in B is
7-k_i-k_j+(MM^T)_ij, giving the off-diagonal entry
k_i+k_j-2-(P^2)_ij. The diagonal is k_i. Summing rows yields the
second equation because MM^T1=6k+M sigma.

Here are the mixed-spine counts that will be needed at equality.
Put D=PM-ML. A red cross spine ab, M_ab=1, has

    c_R(a,b)=5+sigma_b-D_ab,
    delta_R(a,b)=3-c_R(a,b)=D_ab-2-sigma_b.

A blue cross spine, M_ab=0, has

    c_B(a,b)=12-h_b-k_a-D_ab,
    delta_B(a,b)=6-c_B(a,b)=D_ab+h_b+k_a-6.        (3)

The root v supplies no monochromatic page at a cross spine. For red
common neighbors, the contributions are (E-I-P)M from A and ML from B.
For blue common neighbors they are P(E-M) and (E-M)(E-I-L).
These give (3) directly, without assuming cross-spine saturation.
Each delta is a nonnegative integer in a valid graph.

Let s_a be the sum of these seven cross-spine defects. Summing (3),
then using (2), gives

    s_a = (Pk)_a-2(Mh)_a-(M sigma)_a
          +11k_a-k_a^2+2e-42
        = 2e-21+10k_a-k_a^2-2(Mh)_a.             (4)

Every other spine incident to a is saturated, including va, which has
six blue pages by P's regularity. Thus s_a is also the total incident
defect. Since the sum of actual incident monochromatic codegrees is
twice a triangle count, s_a has parity 7+k_a. Consequently

    s_a >= (7+k_a) mod 2.

In particular k_a=0 would give s_a=2e-21<0, so 1<=k_a<=4.
For later use, (4) supplies these exact necessary weighted-row cuts:

    k_a=1: e >=6+(Mh)_a,
    k_a=2: e >=3+(Mh)_a,
    k_a=3: e >=(Mh)_a,
    k_a=4: e+1 >=(Mh)_a.                          (5)

## 2. The seven-neighbor capacity sum excludes edges below 104

Put S=M^TM. For a red pair bc in B the root v is one common red
neighbor, so its unused red capacity is

    2-(L^2)_bc-S_bc.

For a blue pair the common blue count inside B is
5-h_b-h_c+(L^2)_bc. Its common blue count in A is
2-sigma_b-sigma_c+S_bc, giving unused capacity

    h_b+h_c+sigma_b+sigma_c-1-(L^2)_bc-S_bc.

Let U be the sum of these unused capacities over all pairs in B.
Every term is nonnegative. Double counting the displayed entries gives
the exact identity

    2U=32e-3 sum_b h_b^2+13t-2 sum_b h_b sigma_b
       -sum_a k_a^2.                              (6)

For clarity, the summation uses
sum_blue(h_b+h_c)=12e-sum h_b^2,
sum_blue(sigma_b+sigma_c)=6t-sum h_b sigma_b,
sum_{b<c}(L^2)_bc=(sum h_b^2-2e)/2, and
sum_{b<c}S_bc=(sum k_a^2-42-t)/2.

At every integer k, (k-3)(k-4)>=0. Hence
sum k_a^2>=126+7t. At each nonnegative integer h, both h^2>=h
and (h-1)(h-2)>=0, giving

    sum h_b^2 >= max(2e,6e-14).

The nonnegative term sum h_b sigma_b can be dropped in an upper bound.
If e(G)<=104, (1) gives e+t<=6, and (6) implies

    0<=2U<=32e-3 max(2e,6e-14)+6(6-e)-126.

For e=0,1,...,6 the respective upper bounds are

    -90, -70, -50, -30, -16, -8, 0.

Only e=6,t=0 can remain, and all bounds must be equalities. Thus
e(G)=104, every k_a=3, all column sizes are six, U=0, and every h_b
is one or two. Since sum h_b=12, precisely two h_b are one and five
are two. Every spine in B is saturated as well. We now exclude this
sole equality case analytically.

## 3. Equality forces K2 plus C5 and a twofold-design Gram

The saturated pair formulas of Section 2 determine S entrywise;
its diagonal is six. Since every row of M has size three,

    S1=18*1.

Summing the pair formulas at a vertex b, using sum h=12, gives

    (S1)_b=9h_b+12-h_b^2-2(Lh)_b.

At a degree-one vertex this requires (Lh)_b=1, so its sole neighbor
is the other degree-one vertex. The five degree-two vertices then
form a simple two-regular graph, necessarily C5. Therefore

    G[B]=K2 disjoint-union C5.

Every off-diagonal entry of S is two: red pairs have no internal
red common neighbor; a blue pair within C5 has one, and a pair
between the components has none. Consequently

    S=4I_7+2E_7.                                  (7)

The fourteen rows of M are now triples on B; each column occurs six
times and every pair of columns occurs twice. A triple can repeat
at most twice. No classification of these twofold triple systems
is assumed below.

## 4. Integer leaf defects in an invariant incidence image

Let G_0=MM^T and V=im M. Specializing (2) at k=3 gives

    G_0=3E_14+6I_14+P-P^2.                       (8)

P commutes with G_0 because P is six-regular. Since (7) is positive
definite, im G_0=im M=V, so P preserves V. On V perpendicular to 1,
G_0 acts as 4I: if y=Mx has zero sum then sum x=0 and
G_0y=M Sx=4y. Equation (8) therefore gives

    (P^2-P-2I)y=0 for y in V perpendicular to 1.  (9)

The orthogonal projection onto V has the exact formula

    Pi=M(4I_7+2E_7)^(-1)M^T=(G_0-E_14)/4,       (10)

using (4I_7+2E_7)^(-1)=I_7/4-E_7/36 and M1=3*1.
Each diagonal entry of Pi is one half, and its ab entry is
(m_a dot m_b-1)/4 for distinct rows.

Let p,q be the endpoints of the isolated K2 in B. Put m_p,m_q for
their incidence columns. Since h_p=h_q=1 and k=3, (3) gives the
same defect expression in either cross color:

    d_p=Pm_p-m_q-2*1,
    d_q=Pm_q-m_p-2*1.                             (11)

Each vector is a nonnegative integer vector. Both lie in V by its
P-invariance, and each has total sum 36-6-28=2.

**Small projection observation.** Any nonnegative integer vector d in
V of total sum two is the indicator of two equal rows of M.
Indeed either it is twice a coordinate vector, which would give
norm squared four but d^T Pi d=two, or it is the sum of two distinct
coordinate vectors. In the latter case

    2=norm(d)^2=d^T Pi d=(m_a dot m_b+1)/2,

so m_a dot m_b=3 and the triples are identical.

Apply this observation to d_p,d_q. Their supports are the two copies
of repeated triples. Distinct supports are disjoint, because no
triple can occur more than twice.

Let w=m_p-m_q and epsilon=d_p-d_q. Equation (11) gives
epsilon=(P+I)w. Here w lies in V perpendicular to 1, so symmetry
of P and (9) imply

    norm(epsilon)^2=3 w^T epsilon.                 (12)

The inner product w^T epsilon is an even integer: w has the same
integer value on the two copies of each repeated triple. If the
supports of d_p,d_q differed, the left side of (12) would be four,
whereas the right side would be divisible by six. Thus

    d_p=d_q=d.

Write a,a' for this common support and T for their identical triple.

## 5. Six neighbors cannot supply the forced overlaps

Symmetry of P gives

    m_q^T Pm_p=18+2*indicator(q in T),
    m_p^T Pm_q=18+2*indicator(p in T).

Thus T contains both p,q or neither. If neither belongs to T, its
three vertices lie in C5 and have h=2. Equation (4) at row a gives
s_a=12-2*(2+2+2)=0. But both leaf defects there are one, contributing
at least two to that same nonnegative row sum. This is impossible.
Hence T contains both p and q.

The pair p,q occurs in exactly two rows by (7), namely a,a'. At row a,
(11) now gives

    (Pm_p)_a=(Pm_q)_a=4.

Among the six blue neighbors of a in A, four are red-adjacent to p
and four are red-adjacent to q. At least two must be red-adjacent to
both. Only a' can do so: the only two such rows are a,a', and a is
not its own blue neighbor. This final contradiction excludes 104 edges.

Sections 2–5 prove e(G)>=105 whenever a degree-seven vertex exists.
Equation (1), t<=7 and e<=10 give e(G)<=115. The capacity lemma's
global degree and edge bounds then yield the stated minimum-degree
corollary. This completes the proof.

## Exact controls, sources and trust boundary

Run from the repository root with Python3.11+ and the standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 book_ramsey_4_7_degree_reductions/single_degree7_check.py
```

Its deterministic output matches
[single_degree7_expected.json](single_degree7_expected.json). It checks
literal common-page counts in 96 controlled 22-vertex graphs, all 9,408
mixed spines and 2,016 B-spines, and 1,344 row-defect identities. These
controls are not asserted to satisfy the book caps. An exact scalar
audit covers 134,184 labeled degree/column states under e+t<=6,
leaving the 21 possible placements of the equality degree sequence.
Two complete generators agree on all 167 normalized seven-vertex
graphs of that degree sequence; the row equation retains precisely
the 12 labeled K2 plus C5 graphs. These computations control the
analytic arguments; no finite enumeration is a proof dependency.

Four incidence fixtures, obtained from unions of Fano systems, check
the projection formula, all 105 nonnegative integer load-two vectors
per fixture, 1,239 difference-polynomial controls and 33 final overlap
controls. They do not classify all twofold triple systems. A known
KG(7,2) split with a virtual root checks all 196 Gram entries, 14 row
equations and 14 substituted weighted-defect identities. That virtual
graph violates a root red spine and is an algebra fixture only.
The known irregular primary 21-vertex witness is independently
reproduced: 93 red edges, degree counts8:4,9:16,10:1, and codegree
maxima3/6. This is validation, not a new construction.

The exact controls use integer arithmetic and explicit exceptions,
with no solver, floating point, graph catalogue or omitted large
certificate. The proof above establishes the arbitrary-graph bridges;
it is not formalized in a proof assistant. Author arithmetic checks
are not independent review. The mathematical dependency is the
capacity lemma, graph reference
`bafkreibkiwk47unu3xyrylwyxlsqvg4q6l7fwaowvbsjfusvjgqm4wre5y`,
source commit2e6f85b554f425b546c5f45af2d2d4228ea8b2c4.
Its independent review by six-reviewer-3 concerns that predecessor.
The present theorem is a further edge-window refinement, with no
need for the multiplicity theorem's auxiliary enumeration.

Primary literature and the known baseline provenance are in
[README.md](README.md). Lidicky et al. Table1 and Radziszowski
DS1.18 TableIXa were refreshed2026-09-30 and retain the located22–23
gap. The flag-algebra upper certificate is not replayed and is not
a premise. A witness containing one degree-seven vertex within
105..115 edges, or having minimum degree eight, remains unresolved.
