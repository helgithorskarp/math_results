# A positive defect vector excludes saturation of the even-degree roots at 98 edges

Author: **six-books-1**, role **researcher**, 2026-10-01. The campaign shares
a signing identity; this names the actual author. Status: an ordinary
analytic proof, with two exact author implementations validating its
identities and complete eigenspace. Independent peer review of this new
application is pending. No host-graph census or solver conclusion is a premise.

**Conditional theorem.** Let the red graph be a simple graph on 22 vertices
with degree histogram
\[
(n_8,n_9,n_{10})=(m,24-2m,m-2),\qquad m\in\{4,5,6\}.
\]
Suppose every red edge has at most three common red neighbors, and every
blue edge has at most six common blue neighbors. Define the nonnegative
integer spine defect \(F_{ij}\) by three minus the red page count on a red
edge, and six minus the blue page count on a blue edge; set \(F_{ii}=0\).
Put \(f=F\mathbf1\), and let \(A,B,C\) be the degree-eight, degree-nine,
degree-ten classes. Then
\[
\boxed{\sum_{i\in A\cup C}f_i\ge4},\qquad
\boxed{e_R(A)-e_R(C)\ge2}.
\tag{T}
\]
In particular, these even-degree roots cannot all be saturated.
Books are ordinary subgraphs; no induced, connectedness, red symmetry,
or host automorphism hypothesis is imposed.

**Combined corollary.** Crediting the prior degree-range theorem 8012,
budget theorem 8164 and histogram exclusions 8208/8317, (T) holds for
every valid 98-edge host. Its remaining degree histograms are still
\((4,16,2),(5,14,3),(6,12,4)\). The corresponding degree-nine parity
surpluses satisfy
\[
\sum_{i\in B}(f_i-1)\le16,12,8
\quad\hbox{respectively}.
\tag{C}
\]
This does not exclude any entire remaining histogram, the full 98-edge
boundary, or the Ramsey endpoint.

## 1. A signed identity and its saturation consequence

Write \(c=m-2\), \(b=24-2m\). Let \(R\) be red adjacency, \(d=R\mathbf1\),
\(u=\mathbf1_A\), \(v=\mathbf1_C\), \(h=Ru\), \(k=Rv\),
\(Q=\operatorname{diag}(u+v)\), and
\[
D=\operatorname{diag}(2d-17)=I-2\operatorname{diag}(u)+2\operatorname{diag}(v),
\qquad K=2R+D,\qquad H=K^2.
\]
All histograms in the theorem have exactly 98 red edges. The elementary
complementary-neighbor identities, as used in
[parity square 7970](parity_square.md), are
\[
(R^2)_{ij}=d_i+d_j-14+(17-d_i-d_j)R_{ij}-F_{ij}\quad(i\ne j),
\]
\[
f_i=196-294+38d_i-d_i^2-2\sum_{j\in N_R(i)}d_j
    =1-3u_i+v_i+2(h_i-k_i).
\tag{1}
\]
They hold even with signed defects when the page bounds are dropped.
Squaring \(K\) cancels the adjacency term, giving the entire matrix
\[
H=21I+16J-4(u\mathbf1^t+\mathbf1u^t)
       +4(v\mathbf1^t+\mathbf1v^t)+4Q-4F.
\tag{2}
\]
Its diagonal entries on \(A,B,C\) are 33,37,49.

Here is a useful identity that explicitly retains unsaturated-root errors.
Put \(r_A=u^tf\), \(r_C=v^tf\), and \(p=\mathbf1+h-k-2u\). Then
\[
\boxed{2(Fp-3p)=Qf-(r_A-r_C)\mathbf1+(K-3I)F(u-v).}
\tag{3}
\]
To check the bridge without assuming saturation, use
\[
K\mathbf1=19\mathbf1-4u+4v,\qquad Ku=2h-u,\qquad Kv=2k+3v.
\]
Apply (2) to \(u,v\) and use these last two equations:
\[
Kh=6m\mathbf1+(12-2m)u+2mv+h-2Fu,
\]
\[
Kk=10c\mathbf1-2cu+(8+2c)v-3k-2Fv.
\tag{4}
\]
Let \(a=e_R(A)\), \(z=e_R(C)\), \(t=e_R(A,C)\). From (1),
\(r_A=-2m+2(2a-t)\), \(r_C=2c+2(t-2z)\).
Comparison of \(K(Kh),K(Kk)\) with (2) applied to \(h,k\) gives
\[
2Fh=2m\mathbf1-4mu+2Qh+2(m-1)h-2mk-r_A\mathbf1+(K+I)Fu,
\]
\[
2Fk=2c\mathbf1-4cu+2Qk+2ch-2(c+1)k-r_C\mathbf1+(K-3I)Fv.
\tag{5}
\]
Substitute (1) and \(m-c=2\) into \(2Fp=2f+2Fh-2Fk-4Fu\)
to obtain (3). These are exact signed identities, not numerical estimates.

Assume for contradiction that \(f_i=0\) for all \(i\in A\cup C\).
Nonnegativity then makes every root row of \(F\) zero; hence
\(Fu=Fv=0\), \(Qf=0\), \(r_A=r_C=0\). Equation (3) gives
\[
Fp=3p.
\tag{6}
\]
At a root, (1) says \(h-k=1\) on \(A\), and \(h-k=-1\) on \(C\),
so \(p=0\) on the roots. On \(B\), set \(\delta_i=h_i-k_i\).
Here \(f_i=1+2\delta_i\ge0\) forces the integer \(\delta_i\ge0\),
and \(p_i=1+\delta_i>0\). Thus
\[
\sum_{j\in B}F_{ij}=1+2\delta_i,\qquad
\sum_{j\in B}F_{ij}\delta_j=2+\delta_i.
\tag{7}
\]

## 2. The forced defect graph, uniformly for all three histograms

A \(\delta=0\) row has one unit edge; (7) makes its neighbor have
\(\delta=2\). A \(\delta=1\) row has total weight three, no
\(\delta=0\) neighbor, and weighted neighbor sum three. All its
neighbors therefore have \(\delta=1\).
If \(\delta_i\ge3\), it can have neither a \(\delta=0\) nor a
\(\delta=1\) neighbor. Every available neighbor has \(\delta\ge2\),
contradicting
\(2+\delta_i\ge2(1+2\delta_i)\). Hence only \(0,1,2\) occur.

A \(\delta=2\) row has total weight five. Its internal weight on
the \(\delta=2\) class is exactly two by (7); its other weight is
three distinct unit leaves of type zero. These leaves are disjoint
between centers. If the three type counts are \(n_0,n_1,n_2\), then
\[
n_0=3n_2,\qquad n_1+4n_2=b,
\qquad n_1+2n_2=\sum_{B}\delta_i=18-2m.
\]
For the last equality, sum \(h-k\) over all vertices to get \(8m-10c\),
then subtract its root sum \(m-c\).
Consequently
\[
n_2=3,\qquad n_0=9,\qquad n_1=12-2m.
\tag{8}
\]
The three loopless type-two vertices have internal weighted degree two,
forcing a unit triangle. Each has its own three leaves. The remaining
\(12-2m\) type-one vertices form a separate nonnegative integer
loopless weighted cubic graph.

Its small block is invertible in every case:

* For \(m=4\), on four vertices the opposite edge weights agree.
  Write them \(x,y,z\ge0\), \(x+y+z=3\). The four eigenvalues are
  \(3,2x-3,2y-3,2z-3\), all nonzero. There are ten integer triples,
  but this algebraic argument covers them without an enumeration premise.
* For \(m=5\), the two vertices have one edge of weight three, giving
  eigenvalues \(3,-3\).
* For \(m=6\), the block is empty and supplies no kernel.

Let \(F_B\) be the block on \(B\). Its leaf rows force the three
center coordinates of any kernel vector to be zero. The center rows then
force sum zero on each leaf triple; the invertible small block forces all
remaining coordinates to vanish. Therefore
\[
\ker F_B=\{\text{leaf vectors with sum zero on each triple}\},\quad
\dim\ker F_B=6,
\tag{9}
\]
and every such vector has total sum zero.
There is also an explicit rational vector \(w\) with \(F_Bw=\mathbf1_B\):
assign 1 to each center, \(-1/3\) to each leaf, and \(1/3\) to each
type-one vertex. Each center row gives \(2-1=1\), each leaf gives 1,
and each cubic row gives 1. Its total sum is
\[
\gamma_c=\mathbf1_B^tw=(12-2m)/3=2(4-c)/3.
\tag{10}
\]

## 3. Completeness of the 21-eigenspace

This step establishes the **entire** eigenspace; a recognized leaf
subspace alone would not justify the lattice argument.
Take \(q\in\ker(H-21I)\), and write \(\zeta=\sum_Bq_i\).
The root rows of (2), with their zero defect rows, force a common
coordinate \(\alpha\) on \(A\) and \(\beta\) on \(C\). Their two equations are
\[
(1+2m)\alpha+4c\beta+3\zeta=0,\qquad
4m\alpha+(1+6c)\beta+5\zeta=0.
\tag{11}
\]
The coefficient determinant is
\(\Delta_c=5-4c^2\), nonzero for \(c=2,3,4\). Thus
\[
\alpha=\frac{2c-3}{\Delta_c}\zeta,\qquad
\beta=\frac{2c-1}{\Delta_c}\zeta.
\]
The \(B\) rows of (2) give
\[
F_Bq_B=(3m\alpha+5c\beta+4\zeta)\mathbf1_B
       =\nu_c\zeta\mathbf1_B,\qquad
\nu_c=\frac{2(1-c)}{\Delta_c}.
\tag{12}
\]
By (9)--(10), \(q_B-\nu_c\zeta w\in\ker F_B\) has total sum zero.
Hence \(\zeta=\nu_c\gamma_c\zeta\). The exact nonzero coefficients are

| \(m\) | \(c\) | \(\Delta_c\) | \(1-\nu_c\gamma_c\) |
|---:|---:|---:|---:|
| 4 | 2 | -11 | 25/33 |
| 5 | 3 | -31 | 85/93 |
| 6 | 4 | -59 | 1 |

It follows that \(\zeta=\alpha=\beta=0\), and \(q_B\in\ker F_B\).
Conversely, any vector in (9), extended by zero on the roots, has all
three class sums zero and is a 21-eigenvector of (2). Therefore
\[
E:=\ker(H-21I)
=\{\text{leaf vectors with sum zero on each of the three triples}\}.
\tag{13}
\]
In particular \(\dim E=6\) in all three histograms and all small cubic forms.

## 4. A red-edge trace contradiction

Because \(H=K^2\), \(K\) preserves the entire space \(E\).
Its vectors are supported on degree-nine vertices, so \(D=I\) on \(E\).
Therefore \(R=(K-D)/2\) preserves \(E\), and on this six-dimensional
rational space its action satisfies \(R^2+R-5I=0\).
The polynomial \(x^2+x-5\) is irreducible over \(\mathbb Q\), with
discriminant 21. Thus the rational characteristic polynomial on \(E\)
is \((x^2+x-5)^3\), and
\[
\operatorname{tr}(R|_E)=-3.
\tag{14}
\]

Let \(P\) be the orthogonal projection onto (13). On each leaf triple
it is \(I_3-J_3/3\); it is zero elsewhere. Since \(R\) preserves \(E\),
\(\operatorname{tr}(R|_E)=\operatorname{tr}(RP)\).
The zero adjacency diagonal and symmetry give the literal formula
\[
\operatorname{tr}(RP)=-\frac13\sum_{\text{leaf triples }T}\sum_{i\ne j\in T}R_{ij}
                       =-\frac23\sum_T e_R(T).
\]
Equation (14) would force \(\sum_Te_R(T)=9/2\), contradicting that
these are integer red-edge counts. This directly completes the
saturation contradiction; it uses no Gram determinant or finite census.

**Credited lattice alternative.** The earlier two-root argument and
reviewer four's general lemma give another contradiction on the same
entire eigenspace. The details follow to make the hypotheses explicit.

For each leaf triple use the two vectors
\(e_1-e_2,e_2-e_3\). A triple \((x,y,z)\) of integers with
\(x+y+z=0\) has integer basis coordinates \((x,-z)\).
Thus these six vectors are a basis of the **full** lattice
\(L=E\cap\mathbb Z^{22}\), with no unproved index assertion. Its Gram matrix is
\[
G=\operatorname{diag}\left(
\begin{pmatrix}2&-1\\-1&2\end{pmatrix},
\begin{pmatrix}2&-1\\-1&2\end{pmatrix},
\begin{pmatrix}2&-1\\-1&2\end{pmatrix}\right),\qquad\det G=27.
\]
The integer entries of the already invariant \(R\) preserve \(L\).
Its action \(S\) in this full lattice
basis is integral and \(S^tG=GS\). On \(E\), \(K=2R+I\), so
\[
(2S+I)^2=21I,\qquad S^2+S-5I=0.
\]
The polynomial \(x^2+x-5\) is irreducible over \(\mathbb Q\), with
discriminant 21. The six-dimensional rational space is a vector space
of dimension three over this quadratic field. Its characteristic
polynomial is \((x^2+x-5)^3\), forcing \(\operatorname{tr}S=-3\).

Modulo two, the even Gram diagonal and odd Gram determinant give a
nondegenerate alternating form. In a symplectic basis, writing
\(S=\left(\begin{smallmatrix}U&V\\W&X\end{smallmatrix}\right)\),
self-adjointness gives \(X=U^t\). Thus its trace is zero in
\(\mathbb F_2\), contradicting the odd trace \(-3\).
This alternative is the mechanism from [two-root result 8208](degree98_two_roots.md)
and the general rank-divisibility lemma proved by
[reviewer four in 8301](../book_ramsey_degree98_two_roots_review4/REVIEW.md).
The new application is the uniform positive-vector and complete-eigenspace
reduction for \(m=4,5,6\); no novelty is claimed for trace parity.

We have contradicted simultaneous root saturation. Finally, summing
(1) on the roots cancels \(t\) and gives, without saturation,
\[
\sum_{A\cup C}f_i=-4+4(e_R(A)-e_R(C)).
\tag{15}
\]
The sum is nonnegative and divisible by four; zero is now excluded.
This proves (T). Also \(\sum_i f_i=60-6m\), so
\(\sum_i(f_i-(d_i\bmod2))=36-4m\). Subtracting the root sum at least
four proves (C).

## 5. Reproduction and exact-check scope

Run sequentially with CPython 3.11 or later, standard library only:

```sh
python3 -O degree98_root_saturation_check.py --controls /tmp/book-root-controls.json
python3 -O degree98_root_saturation_independent.py --controls /tmp/book-root-controls.json
```

[The first program](degree98_root_saturation_check.py) deterministically
constructs 32 simple 98-edge signed controls per histogram using
Havel--Hakimi and degree-preserving switches. It checks all 44,352
off-diagonal codegree identities, all 46,464 square entries, 2,112
incident identities, 4,224 corrected \(K\)-actions, 4,224 general
\(F\)-actions, 2,112 entries of (3), and 96 instances of (15).
These 96 graphs violate the book conditions; no host census is inferred.
It also checks 96 literal red-edge projection trace identities.
It constructs all ten four-point weighted cubic blocks and the one
two-point and empty blocks, checks full rational ranks of \(H-21I\)
and \(F_B\), the six leaf directions, full Gram determinant, \(w\),
and the three root elimination constants.

[The separate program](degree98_root_saturation_independent.py) imports
no first-implementation module. It reads the same literal signed control
graphs, computes pages by bit intersections and the square by applying
the adjacency operator twice to each unit vector. It directly compares
all 46,464 graph-control defect entries and checks the record fingerprints.
Its small weighted graphs are generated by
independent margin checks on all four-valued upper triangles.
For the whole eigenspace it supplies six kernel vectors and computes
a nonzero **integral sixteen-dimensional quotient determinant** by
Bareiss elimination, independently of the first program's full rational
row reduction. It directly compares all 5,808 full \(F\) entries and
5,808 full \(H\) entries from the reproducible private export, plus
their canonical fingerprints and every rank, Gram and elimination record.
The records are in the compact
[expected summary](degree98_root_saturation_expected.json).

The credited rank-four positive-definite Gram control has determinant 205,
quadratic action \(S^2+S=5I\) and trace -2. A credited rational rank-two
control has odd Gram determinant three and trace -1, illustrating why
integrality is needed. The separate program checks the trace on all 21
elementary generators of the mod-two self-adjoint operators for the
literal six-dimensional leaf Gram. Removing the required cubic edges
from an artificial four-point remainder gives a nine-dimensional
eigenspace, detected by both methods; such a matrix violates the forced
row sums and is not an admissible form.

The final optimized CPython 3.11.2 runs completed sequentially in
1.306 s / 0.503 s, with child peak RSS 25,492 / 22,052 KiB, respectively.
All numerical thread limits were one, with one local research job at a time.

The written identities, positive-vector classification, full kernel,
lattice invariance and direct red-edge trace argument constitute the proof. These
computations validate that proof and are **not** exhaustive graph
certificates or proof-assistant formalizations. Both are author checks,
not independent peer reviews. The exported graph controls are optional
private generated data with the comparison matrices, omitted from publication and reproducible by the
first command. No floating-point decision, external package, historical
classification, timeout, or hidden proof corpus is used in this local theorem.

## 6. Dependencies, literature and frontier

The conditional theorem above is proved from its stated histogram and
page caps. The universal 98-edge corollary separately uses
[six-books-3's degree-eleven exclusion 8012](../book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md)
and [budget 8164](slack8_remaining.md). Their counts imply
\((n_8,n_9,n_{10})=(a,24-2a,a-2)\), \(2\le a\le6\).
[Two-root exclusion 8208](degree98_two_roots.md) removes \(a=2\),
and [zero-attachment exclusion 8317](degree98_zero_attachment.md),
with its explicitly credited dependency on 8252, removes \(a=3\).
Those earlier global results retain their own proof and classification
trust boundaries. Review 8301 confirms 8208 and proves the general
lattice lemma; it is not a review of 8317 or this application.

Primary literature checked live on 2026-10-01:
[Lidicky--McKinley--Pfender--Van Overberghe, Table 1](https://arxiv.org/html/2407.07285v2#S2)
and [Radziszowski's DS1.18 survey, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf)
give \(22\le R(B_4,B_7)\le23\). The paper's credited
[21-vertex construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
was freshly fetched, complemented off the diagonal and compared on all
441 entries with [the retained fixture](baseline21.rows): 93 red edges
and page maxima 3/6. That lower-bound validation is not new research.
Its freshly fetched raw SHA256 was
`3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55`.
The published upper-bound certificate was not rerun. No priority claim
is made beyond identifying the new graph-specific structural reduction.

Next frontier: the positive root-defect cases within the remaining
three histograms. Equation (3) supplies their exact error term.
Neither recognition of a six-dimensional leaf subspace nor the current
private root-shape census excludes those unsaturated cases.
