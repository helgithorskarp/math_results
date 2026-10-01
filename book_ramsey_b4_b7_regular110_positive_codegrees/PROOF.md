# Positive red codegrees at the regular Book Ramsey boundary

Actual author: **six-books-3**, role **researcher**, 2026-10-01.

Let G be a simple red graph on 22 vertices. Assume every red edge has
at most three common red neighbors and every edge of the blue complement
has at most six common blue neighbors. These are ordinary, noninduced
book constraints. A codegree below always means the number of common
red neighbors of the specified red edge.

**Exact computer-assisted theorem.** If G is ten-regular, every red
edge has codegree **two or three**. At every vertex the red-neighborhood
degree counts `(n0,n2,n3)` are consequently one of

    (0,0,10), (0,2,8), (0,4,6).

The subgraph D consisting of red edges of codegree two has vertex
degrees **0, 2, or 4**. If s=e(D) and T is the number of red triangles,
then

    s = 330 - 3T,    s in {0,3,6,...,42},    96 <= T <= 110.

The new exclusion is codegree zero. The previously published
[neighborhood floor](../book_ramsey_b4_b7_regular110_neighborhood_floor/PROOF.md)
allowed `(1,1,8)`, which this theorem removes. Codegree one and the
other local pattern exclusions are recounted below. This local theorem
is self-contained and assumes no automorphism or connectedness of G.
The preceding [maximum-degree-ten theorem](../book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md)
implies that every valid 22-vertex graph with **110 red edges** is
ten-regular. Thus the theorem covers that entire edge boundary, while
leaving other edge counts and this boundary's three surviving local
patterns unresolved. The located Ramsey interval remains
**22 <= R(B4,B7) <= 23**.

## 1. Miss incidence and its exact budgets

Fix v. Its ten red neighbors form A and its eleven blue neighbors form B.
Let J=G[A], with adjacency matrix P and degrees h_i. The red spine vi
gives h_i<=3. For b in B write

    Z_b = A \ N_G(b), z_b=|Z_b|,
    M_bi=1 if i in Z_b, t_i=sum_b M_bi.

Regularity and the blue spine vb give

    t_i=h_i+2,    d_{G[B]}(b)=z_b>=4.

Put H=sum_i h_i=2e(J). The total number of misses is H+20, so H>=24;
also H<=30. Hence 12<=e(J)<=15 and

    e(G[B])=e(J)+10.                                      (1)

For i!=j in A define epsilon_ij as three minus the actual common red
count when ij is red, or six minus the actual common blue count when
ij is blue. These are nonnegative integers; put epsilon_ii=0. The actual
miss Gram matrix S=M^t M satisfies

    S_ii=h_i+2,
    S_ij=h_i+h_j-5-(P^2)_ij-epsilon_ij  if ij is red,
    S_ij=h_i+h_j-2-(P^2)_ij-epsilon_ij  if ij is blue.       (2)

For a red pair, its common red neighbors comprise v, its common
J-neighbors, and 11-t_i-t_j+S_ij vertices of B. A blue pair has
8-h_i-h_j+(P^2)_ij common blue neighbors in A and S_ij in B. This proves
(2). Every S-entry is nonnegative, and S is positive semidefinite.

A red local edge therefore needs h_i+h_j>=5. Local degree one is
impossible, since its incident edge would have degree sum at most four.
Local degree-two points are adjacent only to degree-three points. On
each 2--3 edge both the common local count and epsilon are zero.
Two isolated local points would have a negative blue entry in (2),
so n0<=1. These facts and the even degree sum give exactly the six
initial histograms

    (0,0,10), (0,2,8), (0,4,6), (0,6,4), (1,1,8), (1,3,6).

For later use let u_i=sum_{b:i in Z_b}(z_b-4), and E=(epsilon_ij).
Before subtracting E, the row sum in (2) is 7h_i+H-16-(Ph)_i.
The actual row sum is 4(h_i+2)+u_i. Thus

    (E1)_i=3h_i+H-24-(Ph)_i-u_i.                          (3)

## 2. A paired-root bridge closes the isolated case

Suppose x is isolated in J. Equivalently, the red edge vx has codegree
zero. The two miss rows containing x will be denoted Z_p,Z_q, with
p,q in B. Equation (2) gives S_xl=0 at every local degree-two point l
and S_xc<=1 at every cubic point c. Hence Z_p,Z_q contain no degree-two
point and their cubic subsets are disjoint. If their union contains k
cubic points, then

    z_p+z_q=k+2,    k<=n3.                                (4)

The red neighbors of x are exactly `{v}` together with C=B\{p,q}.
Vertex v is isolated in the neighborhood at x, because v is blue to
all of B. The other nine local degrees are at most three. Their degree
sum is even, so **e(G[C])<=13**. This upper bound uses only the red
spine cap and regularity.

Let r=1 if pq is red and r=0 otherwise. Deleting p,q from G[B] and
using (1), (4), and d_B(p)=z_p, d_B(q)=z_q gives the exact identity

    e(G[C])=e(J)+8-k+r.                                  (5)

If e(J)=12, its isolated histogram is `(1,3,6)`; then k<=6 and (5)
gives e(G[C])>=14, a contradiction. If e(J)=13, its isolated histogram
is `(1,1,8)`; now k<=8, and e(G[C])<=13 forces **k=8 and r=0**.
Thus every possible isolated neighborhood has exactly one degree-two
point and eight cubic points; all eight cubic points are covered by
the two disjoint isolated miss rows. Their sizes are **5+5 or 6+4**,
since each size is at least four and their sum is ten. The other nine
miss rows all have size four: the total miss count is 46 and the two
distinguished rows already use ten.

This bridge is why the two row-size cases below cover every isolated
neighborhood. A partial assumption that eight points are covered is
not made in the theorem.

Let F be the graph on the eight cubic points. It is triangle-free:
on an edge of a triangle, (2) gives S_ij<=1-1=0. No two points of that
triangle could share either isolated miss row. Yet its three points
must be covered by those two rows, contradicting the pigeonhole
principle. The two neighbors of the unique low point are nonadjacent,
because a 2--3 edge cannot have a common local neighbor. Label them
F-points 0,1. F has degrees **2,2,3,3,3,3,3,3** and eleven edges.

## 3. The complete residual Gram family

Order the nine nonisolated columns as the low point followed by F-points
0,...,7. Put lambda_i=1 for i=0,1 and zero otherwise; these are their
numbers of low neighbors. The isolated point has u_x=2 and incident
slack zero by (3). The low point belongs to neither distinguished row,
has u=0, and has incident slack two. Equation (3) gives a cubic point
incident slack **2+lambda_i-u_i**.

In the 5+5 case each cubic point is in one row of excess one, so the
slack degree vector on the nine columns is

    (2; 2,2,1,1,1,1,1,1).                                (6)

There are 35 partitions of eight points into two four-point blocks;
choose the block containing point 0 to remove interchange duplication.
In the 6+4 case let Q be the five cubic points in the size-six row.
There are 56 choices. A cubic point in Q has excess two and every
other cubic point has excess zero, so the slack degrees are

    d_low=2,    d_i=lambda_i if i in Q,
                         lambda_i+2 if i not in Q.        (7)

The entire slack is a loopless integer multigraph with these degrees,
allowing repeated edges. It has six edges in (6) and five in (7).
For each pair its weight is at most the entry in (2) before subtracting
epsilon; this is exactly the necessary nonnegativity of full S.
Every such weighted graph is retained. No simplicity, connectivity,
host symmetry, or restriction on its support is imposed.

Let S0 be (2) before subtracting epsilon. Delete the isolated column
and the two distinguished rows from M, obtaining a nine-by-nine binary
matrix M'. All its rows and columns have sum four. For indicators a,b
of the two complementary cubic blocks, extended by zero on the low
coordinate, the necessary residual matrix is

    S'=S0[nonisolated]-E[nonisolated]-aa^t-bb^t=(M')^t M'. (8)

It has diagonal four and row sums sixteen and must be positive
semidefinite. The finite theorem is stronger: every matrix in this
complete necessary family is indefinite. States with negative entries
in S' remain in the census; neither an entry filter nor a rank or
determinant test is used to establish the contradiction.

## 4. Enumeration, certificates, and coverage

[generate.py](generate.py) enumerates all labeled triangle-free F graphs
with the specified degrees and absent edge 01 by choosing each vertex's
whole remaining neighbor set. It obtains **1800** masks. The explicit
S6 action on points 2,...,7, fixing 0 and 1 separately, partitions the
entire mask set into the four disjoint orbits below. Bits encode the
lexicographic pairs of 0,...,7, starting with bit zero for 01; the
smallest integer mask is the representative. Interchanging the marked
points is not additionally quotiented. Any actual pair of low neighbors
can be relabeled to 0,1, so this normalization covers all local cores.

| F mask | Orbit size | 5+5 matrices | 6+4 matrices |
| ---: | ---: | ---: | ---: |
| 7818320 | 360 | 11025 | 547 |
| 7834192 | 720 | 11025 | 588 |
| 15434592 | 360 | 11025 | 588 |
| 15436104 | 360 | 11025 | 588 |
| Total | 1800 | 44100 | 2311 |

All **46,411** normalized matrices have a strict negative integer
quadratic form. [negative_vectors.json](negative_vectors.json) contains
**80** reusable vectors, of length nine and maximum absolute coordinate
**489**, indexed by representative and row-size case. Exact Fraction
congruence produces a vector only when the existing pool does not
already reject a state. The obstruction is the literal signed integer
sum `sum_ij S'_ij q_i q_j < 0`, which is checked independently of that
congruence algorithm. The positive diagonal four also supplies a
positive form, so the matrices are indefinite.

[verify.py](verify.py) imports no generator code on its default command.
It instead backtracks over each of the 28 binary F edge bits, filters
triangles at the complete graph, and checks explicit orbit coverage
against the entire 1800-mask set. It independently backtracks over
integer edge weights, reconstructs the full retained matrix by degree
classes and literal F-neighbor intersections, subtracts the two blocks,
and checks every integer negative form. The optional `--compare` command
also compares the full core and slack sets and every state matrix entry
against the generator, before comparing deterministic streamed hashes.
Both implementations agree completely. Weighting by the exact F orbit
sizes gives **20,888,640** states with the fixed marked-point labeling;
this is not a census of unrestricted full 22-vertex graphs.

[checks.py](checks.py) validates the incidence, outside-degree, and
incident-slack identities on 252 circulant ten-regular graphs, and on
4368 graphs built from all four F types and all 91 block choices, both
colors of pq, and six binary residual controls per choice. It checks
the paired-root edge budget and every residual entry literally. These
graphs can violate book caps and have signed slack; they test identities
and decoding, not nonexistence. Seven forged inputs are rejected,
including unit-vector pools whose recorded hash is updated so that
the literal quadratic check must reject the forgery. Guards remain
active under `python3 -O`.

The finite census and checker are two implementations by the same
author, not independent peer review or formalization. The incidence,
paired-root, normalization, and completeness bridges above are written
mathematics. No external graph catalogue, PSD solver, numerical
eigenvalue, timeout, or incomplete search is relied upon.

## 5. The three remaining local histograms

The finite contradiction and Section 2 exclude every local isolated
point, so every red edge has codegree two or three. For completeness,
the analytic exclusion of `(0,6,4)` from the preceding neighborhood
floor is as follows. Let L be its six degree-two points and C its four
cubic points. All twelve edges run between L,C; all eleven miss rows
have size four. Formula (3) forces slack zero on each pair incident
with L. A red L--C pair has S_lc=0, while a blue L--C pair has S_lc=3.
The twelve blue mixed pairs therefore require 36 joint misses. Two
low points with identical neighborhoods cannot share a miss row.

In a four-point miss row put k=|Z intersection C|. When k=3 its one
low point would need two neighbors in the one remaining cubic point,
which is impossible. When k=2 both low points would choose the same
complementary cubic pair, forbidden by their zero joint miss entry.
Thus k=0,1,4 and each row supplies at most k(4-k)<=3 mixed misses.
Eleven rows supply at most 33, contradicting 36. This leaves precisely
the three displayed histograms, with 15,14,13 neighborhood edges.

The number of incident D-edges at a vertex is exactly its number of
local degree-two points, namely 0,2,4. Summing red edge codegrees gives
3T=2s+3(110-s)=330-s. Summing local neighborhood edge counts gives
3T>=22*13, hence T>=96; the red spine cap gives T<=110. Thus s is a
multiple of three between zero and 42. These are necessary constraints,
not existence assertions for the remaining values or local patterns.

## 6. Sources and dependency boundary

Primary sources were reopened live on 2026-10-01:
[Lidicky--McKinley--Pfender--Van Overberghe, Table 1](https://arxiv.org/html/2407.07285v2)
and [Radziszowski DS1.18, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf).
The primary 21-vertex matrix was fetched and exactly reproduced during
this pass: 93 red edges, degree counts 8:4/9:16/10:1, red cap three and
blue cap six. The original-file SHA256 is
`3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55`;
[baseline21.rows](baseline21.rows) is the complemented red fixture
checked by checks.py. This is validation of a known construction.
The literature's global flag-algebra certificate is not replayed.

The local regular theorem above has no historical spectral-classification
premise. Applying it to e(G)=110 uses the preceding maximum-degree-ten
result, whose [independent audit](../book_ramsey_degree11_gram_review1/REVIEW.md)
is committed at height 8060. That audit does not review this theorem.
The teammate's [slack-eight degree exclusion](../book_ramsey_4_7_degree_reductions/slack8.md)
at height 8090 concerns the other end of the 97--110 edge range and is
complementary context, not a premise. Claims about the combined global
minimum degree eight still retain the earlier degree-seven and
uniform-incidence dependencies; this theorem makes no new assertion
about those dependencies. Exact commands and hashes are in README.md.
No Ramsey endpoint or historical priority claim is made.
