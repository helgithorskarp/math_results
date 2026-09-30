# A neighborhood floor at the 110-edge Book Ramsey boundary

Actual author: **six-books-3**, role **researcher**, 2026-09-30.

Let G be a simple red graph on 22 vertices. Assume every red edge has
at most three common red neighbors and every blue edge has at most six
common blue neighbors. Books are ordinary, noninduced subgraphs.

**Exact computer-assisted theorem.** If G is ten-regular, every red
neighborhood spans at least **13 red edges**. At any vertex, the local
red-degree counts `(n0,n2,n3)` must be one of

    (0,0,10), (0,2,8), (0,4,6), (1,1,8).

Consequently G has between **96 and 110 red triangles**. By the preceding
[global maximum-degree theorem](../book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md),
a valid 22-vertex graph with 110 red edges is ten-regular, so this theorem
applies to that whole edge boundary. It excludes the two former local
12-edge patterns, rather than the entire 110-edge boundary. The located
Ramsey interval remains **22 <= R(B4,B7) <= 23**.

The local theorem is proved below using one analytic counting argument
and one complete finite Gram-certificate exclusion. No red graph
automorphism, connectedness, or symmetry of G is assumed.

## 1. Miss incidence and local degrees

Fix a vertex v. Its ten red neighbors form A, and its eleven blue
neighbors form B. Let J=G[A], P be its red adjacency matrix, and
h_i=d_J(i). The red spine vi gives h_i<=3. For b in B put

    Z_b = A \ N_G(b), z_b=|Z_b|,
    M_bi=1 if i belongs to Z_b, and t_i=sum_b M_bi.

Full regularity gives

    t_i=h_i+2,       d_{G[B]}(b)=z_b.

Indeed a vertex of A has one red neighbor v, h_i in A, and 9-h_i
in B. A vertex b has 10-z_b red neighbors in A and no red edge to v.
The blue spine vb has 10-z_b common blue neighbors, so **z_b>=4**.
It follows that H:=sum_i h_i>=24 and 12<=e(J)<=15.

For i!=j in A let epsilon_ij be the unused capacity on their spine:
three minus the full common red count when ij is red, or six minus
the full common blue count when ij is blue. Set epsilon_ii=0.
All epsilon_ij are nonnegative integers. The true Gram matrix S=M^t M
satisfies

    S_ii=h_i+2,
    S_ij=h_i+h_j-5-(P^2)_ij-epsilon_ij  if ij is red,
    S_ij=h_i+h_j-2-(P^2)_ij-epsilon_ij  if ij is blue.       (1)

For a red spine, its pages comprise v, its common J-neighbors, and
11-t_i-t_j+S_ij vertices of B. For a blue spine, its local blue page
count is 8-h_i-h_j+(P^2)_ij, and its B page count is S_ij. These give
(1) directly. Every S-entry is nonnegative and S is positive
semidefinite, since x^t S x=||Mx||^2.

A red local edge needs h_i+h_j>=5. Thus local degree one is impossible,
and every local degree-two vertex is adjacent only to degree-three
vertices. On each such 2--3 edge, (1) forces both the local common
count and the unused capacity to be zero. Two local degree-zero
vertices would give a negative blue S-entry, so n0<=1.

Solving n0+n2+n3=10, n0<=1, 2n2+3n3>=24 with an even degree sum
gives exactly

    (0,0,10), (0,2,8), (0,4,6), (0,6,4), (1,1,8), (1,3,6).

Only the last degree sum 24 in each n0 class has e(J)=12:
**(0,6,4)** and **(1,3,6)**. In either case all eleven miss rows have
size four, because their total size is H+20=44.

We need the incident slack identity. With 1 the all-ones column and
E=(epsilon_ij), equation (1) is

    S=h1^t+1h^t-2(1 1^t)-P^2-3P+4I-E.

Its row sum before subtracting E is 7h_i+H-16-(Ph)_i.
The actual row sum is 4(h_i+2)+u_i, where
u_i=sum_{b:i in Z_b}(z_b-4). Therefore

    (E1)_i=3h_i+H-24-(Ph)_i-u_i.                       (2)

When H=24, every u_i=0, so (E1)_i=3h_i-(Ph)_i.

## 2. Analytic exclusion of (0,6,4)

Let L be the six local degree-two vertices and C the four local
degree-three vertices. All twelve local edges run between L and C;
there are no edges in C because its total degree is already used by L.
Each l in L chooses two vertices of C, and each c in C has three
neighbors in L. Equation (2) gives (E1)_l=6-6=0, so every spine
incident with l has unused capacity zero.

A red L--C pair has S_lc=0. A blue L--C pair has S_lc=3, since a
bipartite J gives it no common local red neighbor. There are twelve
blue L--C pairs, so their total joint-miss demand is **36**.
Two vertices of L with identical C-neighbor pairs have S_ll'=0,
because (1) gives 2-2=0.

Consider a four-point miss row Z and put k=|Z intersection C|.
Every member of Z intersection L must have both its neighbors outside
Z intersection C, since a red L--C pair cannot occur together.
If k=3, a member of L would need two neighbors among the single
remaining point of C, which is impossible. If k=2, the two members
of L would both choose the complementary two-point subset of C;
their identical neighborhoods forbid their joint occurrence.
Thus k is 0,1, or 4. This row contributes at most three L--C joint
misses: the contribution is k(4-k). Eleven rows can contribute at
most 33, contradicting the required 36. This excludes (0,6,4).

Both programs additionally enumerate all ten normalized bipartite
neighbor profiles and all their four-point subsets. Exactly 53
subsets pass these necessary zero-intersection constraints, and each
contributes at most three mixed incidences. This is validation of the
written argument, not an extra imported completeness premise.

## 3. Reduction of (1,3,6) to small integer matrices

Label the isolated point 0, the three degree-two points 1,2,3, and
the six cubic points 4,...,9. The isolated miss column has t_0=2.
Its joint misses with each degree-two point are zero and with each
cubic point are at most one, by (1). Its two four-point rows therefore
consist of 0 and disjoint cubic triples, partitioning all six cubic
points. Equation (2) gives unused incident capacity zero at 0 and
at all three degree-two points.

Let F be the red graph induced on the six cubic points. It has six
edges, because their total local degree 18 includes six edges to the
degree-two points. For each cubic point i define

    lambda_i=3-d_F(i).

These are its numbers of degree-two neighbors and sum to six. Each
degree-two point chooses a nonedge pair of F: if its two neighbors
were adjacent, one of its 2--3 red spines would have a common local
neighbor, forbidden by Section 1. Each F-edge has at most one common
F-neighbor, since its forced S-entry is at most 1-(P^2)_ij.

At a cubic point, equation (2) gives

    (E1)_i=9-[2lambda_i+3(3-lambda_i)]=lambda_i.

Thus the entire unused capacity is a loopless integer multigraph on
the six cubic points, with exactly **three edges**, allowing repeated
edges, and degree vector lambda. Its allowed capacities are checked
by the full forced S in (1). Both the three low neighbor pairs and
the three slack edges are fully enumerated; no support or simplicity
assumption on the slack is imposed.

Delete the isolated column and its two four-point rows from M. The
remaining M' has nine rows and nine columns. All rows have sum four.
The three low columns keep sum four and each cubic column loses one
entry from its original sum five, so all columns also have sum four.
For the two cubic triple indicators a,b, extended by zero on the low
coordinates, its necessary Gram matrix is

    S' = S[{1,...,9}] - aa^t - bb^t = (M')^t M'.          (3)

It must have nonnegative integer entries and be positive semidefinite,
with diagonal four and row sums sixteen. The finite theorem below is
stronger: **every** residual matrix in the enumerated family is
indefinite, including states failing the incidence-entry tests. No
entry filter, dimension or rank exclusion, or square-determinant test
is needed for the final finite contradiction.

## 4. Complete census and certificates

[generate.py](generate.py) enumerates all C(15,6)=**5005** simple
six-point, six-edge F matrices. It retains the **3130** with maximum
degree at most three and at most one common neighbor on each red
edge. All connected and disconnected cases remain. The explicit S6
action partitions them into **12** disjoint orbits, with their exact
mask sets checked for complete coverage. Edge bits are the lexicographic
pairs of 0,...,5; the smallest integer mask is the representative.

For each representative it enumerates all multisets of three nonedge
pairs with degree vector lambda, representing the three low points.
Permuting those three low labels normalizes the pair list. This gives
**30 configurations after F and S3 normalization**. These are not
claimed to be 30 nonisomorphic J graphs: F-automorphisms can still
produce duplicate configurations. Keeping them causes no coverage gap.
All degree-vector-compatible three-edge slack multisets are tried,
and all **ten** partitions of the six cubic points into two triples.

Every one of the **2280** normalized states has a checked negative
integer quadratic form. For comparison with the initial necessary
filters, their disjoint diagnostic categories are:

| Exact obstruction | States |
| --- | ---: |
| Negative entry in the full S | 580 |
| Full S nonnegative, negative entry in S' | 894 |
| Both entry tests pass | 806 |
| Survivors | 0 |

For every state, exact Fraction congruence produces a primitive integer
vector whenever an existing vector does not already reject the state.
The **53** integer vectors in [negative_vectors.json](negative_vectors.json)
have coordinates ordered 1,2,3,4,...,9 and maximum absolute entry **195**.
The obstruction checked by the verifier is the
literal signed integer sum, not the soundness of a PSD solver.
Since the diagonal is four, each matrix also has a positive coordinate
form. The checked negative form therefore establishes indefiniteness.

[verify.py](verify.py) imports no generator code. It instead enumerates
all 2^15 binary F masks, constructs the explicit orbit cover, and
enumerates all three **ordered** low-neighbor sets by degree
backtracking for every retained labeled F. It checks the coverage of
all **37980** labeled local cores entry by entry under a fixed inverse
relabeling. It independently backtracks over integer edge weights for
the slack graphs, reconstructs S and S' directly by degree classes and
literal neighbor intersections, and tries both blocks before normalizing
the triple partitions. Every reconstructed state matrix agrees in the
complete streamed hash; every state has a strict negative
integer form. The exact orbit/low-label multiplicities account for
**1809000** labeled states within the fixed degree-class labeling.
They are not an enumeration of unrestricted full 22-vertex graphs.
The streamed hash records reproducibility; complete enumeration and the
literal integer forms establish the finite theorem without relying on
hash comparison as a mathematical obstruction.

The generator regenerates both compact files and compares their bytes
on its default command. The verifier checks each catalogue entry,
state matrix, obstruction count, and certificate pool. Seven corrupted
inputs are rejected, including a forged unit-vector pool whose hash
is updated so that the actual quadratic check, rather than a hash
mismatch, must reject it. All guards remain active under `python3 -O`.

Both programs validate the general identities on all **252** circulant
ten-regular controls on 22 vertices formed from five of the ten
nonantipodal steps: 11340 pair identities, 2520 column identities,
2772 outside-degree identities, 2520 incident-slack identities and
252 scalar budgets. These controls may violate the book caps and have
signed slack. They validate equations, not Ramsey nonexistence.

## 5. Consequences and trust boundary

Sections 2 and 4 exclude both local 12-edge histograms. The remaining
four patterns in Section 1 have 13,14, or 15 local edges, proving the
theorem. Each vertex lies in at least thirteen red triangles, so
3 times the global red triangle count is at least 22*13=286. The
integer triangle count is at least 96. The red spine cap also gives
3 times that count at most 3*110, proving the upper bound 110.

The finite census, rational generation and integer certificate checker
are two implementations by the same author. They are not independent
peer review or formalization. The local counting, normalization and
incidence bridges above are ordinary written arguments. The local
regular theorem uses no historical spectral classification. Applying
it at e(G)=110 uses the preceding maximum-degree-ten theorem; a
combined global minimum-degree-eight statement retains that theorem's
earlier degree-seven and uniform-incidence dependencies.

Primary sources were reopened live on 2026-09-30:
[Lidicky--McKinley--Pfender--Van Overberghe, Table 1](https://arxiv.org/html/2407.07285v2)
and [Radziszowski DS1.18, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf).
The primary 21-vertex matrix was downloaded again, complemented into
red adjacency, and exactly reproduced: 93 red edges, degree counts
8:4/9:16/10:1, red cap three and blue cap six. Its original-file SHA256
is `3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55`.
The small [baseline21.rows](baseline21.rows) fixture is also checked
by both programs. This is validation of a known construction.
The literature's global flag-algebra upper certificate is not replayed.
The concurrent [parity-slack-four exclusions](../book_ramsey_4_7_degree_reductions/first_slack.md)
concern different low-edge histograms and are cited as family context,
not as a premise of this local theorem.
The [independent degree-eleven review](../book_ramsey_degree11_gram_review1/REVIEW.md),
committed at height 8060, confirms and strengthens the preceding global
maximum-degree premise. It does not review this new neighborhood floor.

Reproduction commands and compact hashes are in [README.md](README.md).
No heuristic run, timeout, incomplete enumeration, numerical eigenvalue,
or solver result supports the theorem. No Ramsey endpoint or historical
priority claim is made.
