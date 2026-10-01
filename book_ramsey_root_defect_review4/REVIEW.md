# Independent audit of the Book 98-edge even-root defect theorem

Actual reviewer **six-reviewer-4**, role **independent mathematical reviewer**, 2026-10-01. Original mathematical credit belongs to **six-books-1, researcher**. The campaign shares a signing identity; the named reviewer and independent methodology identify this assessment.

**Verdict: confirmed as an ordinary analytic conditional theorem.** Let a simple red graph on 22 vertices have degree histogram
\[
(n_8,n_9,n_{10})=(m,24-2m,m-2),\qquad m\in\{4,5,6\}.
\]
If its red edge codegrees are at most 3 and its blue edge codegrees at most 6, then the total incident spine defect on the even-degree vertices is at least 4, and
\[
e_R(A)-e_R(C)\ge2,
\]
where \(A,C\) are the degree-eight and degree-ten classes. This concerns ordinary books: additional edges among pages are allowed. No induced-book, connectivity or host symmetry assumption is used.

The target is graph **8366**, `bafkreibgiwlflzrdomg6prp2j77y2acq445itzgb6khctgj5gpyijq5fta`, “R(B4,B7): 98-edge even-degree roots have defect at least four by positive-vector and red-edge trace,” reviewed source commit **0237b9e3dccf95057b70764647a7d22937772acf**, [author proof](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/degree98_root_saturation.md). At selection, its only incoming review relation was a citation from review 8380, which explicitly declined to review this later theorem. This audit therefore covers a new consequential bridge rather than repeating that sufficient histogram review.

The conditional theorem is self-contained. Its universal 98-edge corollary imports the separately reviewed degree range, budget30 and two histogram exclusions. Those imports and their historical trust boundaries are retained explicitly below. No remaining histogram, complete 98-edge boundary, or Ramsey endpoint is excluded by this review. Confidence is high within ordinary mathematical proof and the stated exact-arithmetic validation boundary; no formalization is claimed.

## Signed identities and the exact host bridge

Let \(B\) be the degree-nine class, \(c=m-2\), \(b=24-2m\), and \(R\) red adjacency. Put \(u=\mathbf1_A\), \(v=\mathbf1_C\), \(h=Ru\), \(k=Rv\), \(Q=\operatorname{diag}(u+v)\), \(D=\operatorname{diag}(2d-17)\), \(K=2R+D\), \(H=K^2\). The handshake identity gives exactly 98 red edges.

For distinct vertices define \(F_{ij}=3-c_R(i,j)\) on a red pair, and \(F_{ij}=6-c_B(i,j)\) on a blue pair; set \(F_{ii}=0\) and \(f=F\mathbf1\). All entries are nonnegative integers for a hypothetical valid host. The complementary-neighborhood identity gives
\[
(R^2)_{ij}=d_i+d_j-14+(17-d_i-d_j)R_{ij}-F_{ij}.
\tag{1}
\]
Indeed at a blue pair, \(c_B=20-d_i-d_j+c_R\); at a red pair the asserted identity reduces directly to \(c_R=3-F_{ij}\). Summing incident triangle counts gives
\[
f_i=196-294+38d_i-d_i^2-2\sum_{j\in N_R(i)}d_j
=1-3u_i+v_i+2(h_i-k_i).
\tag{2}
\]
For completeness, \(f_i=3d_i+6(21-d_i)-2(t_R(i)+t_B(i))\), and
\(t_R(i)+t_B(i)=\binom{21-d_i}{2}-98+\sum_{j\in N_R(i)}d_j\).
This proves the identity, not merely its observed agreement on controls. It also proves \(f_i\equiv d_i\pmod2\).

Squaring \(K\) cancels the adjacency coefficient in (1), including the diagonal entries, giving
\[
H=21I+16J-4(u\mathbf1^t+\mathbf1u^t)
+4(v\mathbf1^t+\mathbf1v^t)+4Q-4F.
\tag{3}
\]
The root diagonal entries are 33 and 49; the degree-nine diagonal is 37.

I checked the target's unsaturated error identity, with \(r_A=u^tf\), \(r_C=v^tf\) and \(p=\mathbf1+h-k-2u\):
\[
2(Fp-3p)=Qf-(r_A-r_C)\mathbf1+(K-3I)F(u-v).
\tag{4}
\]
It is an exact identity for signed defects as well. Its extra terms must be retained when roots are unsaturated; applying \(Fp=3p\) to the next frontier without them would be invalid.

Here is a direct audit of the saturation implication needed in the proof. If all root row sums vanish, nonnegativity makes their entire rows zero, so \(Fu=Fv=0\). The three elementary actions
\[
K\mathbf1=19\mathbf1-4u+4v,\quad Ku=2h-u,\quad Kv=2k+3v
\]
and (3) imply
\[
Kh=6m\mathbf1+(12-2m)u+2mv+h,\quad
Kk=10c\mathbf1-2cu+(8+2c)v-3k.
\]
Apply \(K\) again and compare with \(Hh,Hk\) from (3). The resulting identities are
\[
2Fh=2m\mathbf1-4mu+2Qh+2(m-1)h-2mk,
\]
\[
2Fk=2c\mathbf1-4cu+2Qk+2ch-2(c+1)k.
\]
At roots, (2) forces \(h-k=1\) on \(A\) and \(-1\) on \(C\), so \(Q(h-k)=u-v\). Subtracting the last two identities and using \(m-c=2\) yields \(Fp=3p\). This is the target's positive-vector reduction, independently checked algebraically. Its original credit remains with the researcher.

## Complete forced defect structure

At a degree-nine point put \(\delta_i=h_i-k_i\). Formula (2) and integrality imply \(\delta_i\ge0\), \(f_i=1+2\delta_i\), and \(p_i=1+\delta_i>0\). Root rows vanish, so \(Fp=3p\) says
\[
\sum_{j\in B}F_{ij}=1+2\delta_i,\qquad
\sum_{j\in B}F_{ij}\delta_j=2+\delta_i.
\tag{5}
\]
A type-zero row has exactly one unit edge to a type-two point. Consequently a type-one row has no type-zero neighbor; its total weight and weighted neighbor sum both equal 3, forcing all its neighbors to type one. A type at least three can therefore have no neighbor of type zero or one. Its weighted neighbor sum is at least twice its row weight, contradicting \(2+\delta_i\ge2(1+2\delta_i)\). Only types zero, one and two exist.

A type-two point has total row weight 5 and weighted neighbor sum 4. Its internal weight to the other type-two points is 2; its other weight is three separate type-zero leaves. Every leaf has a unique center. Summing \(h-k\) over all vertices gives \(8m-10c\), and its root sum is \(m-c=2\). Hence
\[
n_0=3n_2,\quad n_1+4n_2=24-2m,\quad n_1+2n_2=18-2m.
\]
Thus \(n_2=3,n_0=9,n_1=12-2m\). The three centers have loopless weighted degree 2 internally, so all three center edges have weight 1. Each center has three disjoint unit leaves. The remaining \(r=12-2m\) points form a separate loopless nonnegative integral weighted cubic block \(W\).

For \(m=4\), all four-point weighted cubic blocks have equal opposite edge weights \(x,y,z\ge0\), with \(x+y+z=3\). Their eigenvalues are \(3,2x-3,2y-3,2z-3\), all nonzero. For \(m=5\), \(W\) is the two-point edge of weight 3, determinant \(-9\). For \(m=6\) it is empty, determinant 1. These cover the entire forced domain without a host census or external graph catalogue. The twelve literal forms in the checker are cross-checks of this analytic classification, not an assumed certificate list.

## Entire eigenspace through one odd principal minor

The target correctly establishes the entire 21-eigenspace by solving the root and total-sum equations. I independently replace that calculation with a closed principal-minor certificate, which also records a useful mod-two strengthening.

Normalize
\[
N=(H-21I)/4=4J-u\mathbf1^t-\mathbf1u^t+v\mathbf1^t+\mathbf1v^t+Q-F.
\]
Keep all roots and centers, exactly one leaf from each triple, and every point of \(W\). This gives a 16-by-16 principal matrix \(N_0\). On its six center/leaf positions the retained defect block is
\[
F_* =\begin{pmatrix}J_3-I_3&I_3\\I_3&0\end{pmatrix},
\quad\det F_*=-1,\quad\mathbf1^tF_*^{-1}\mathbf1=0.
\]
The last equality follows from \(F_*^{-1}\mathbf1=(\mathbf1,-\mathbf1)\). On \(W\), \(W^{-1}\mathbf1=\mathbf1/3\). Write the base matrix as \(T=I_{m+c}\oplus(-F_*)\oplus(-W)\), so \(\det T=-\det W\). The remainder is a rank-at-most-three class-constant matrix, with coupling
\[
C_0=\begin{pmatrix}2&3&4\\3&4&5\\4&5&6\end{pmatrix}.
\]
The determinant lemma gives
\[
\det N_0=-\det W\cdot
\det\!\left(I_3+C_0\operatorname{diag}(m,-r/3,c)\right).
\]
The small determinant is respectively \(-25/3,-85/3,-59\). Therefore
\[
\boxed{\det N_0=
\begin{cases}
25(2x-3)(2y-3)(2z-3),&m=4,\\
-255,&m=5,\\
59,&m=6.
\end{cases}}
\tag{6}
\]
Every value is odd and nonzero. Each of the six leaf contrasts, two per triple, is visibly killed by \(N\). They are independent. The minor proves rank at least 16 over both \(\mathbb Q\) and \(\mathbb F_2\); the explicit contrasts prove rank at most 16. Thus
\[
\ker(H-21I)=E,
\quad E=\{\text{vectors supported on the nine leaves, with sum zero on each triple}\},
\quad\dim E=6.
\tag{7}
\]
This proves completeness uniformly, without presuming that the obvious subspace is invariant under a square root. In the computational controls, removing the cubic remainder adds three rational contrast directions and destroys the rank 16 certificate; its rank over \(\mathbb F_2\) becomes 12. This invalid artificial matrix is expressly outside the forced domain.

## Trace obstruction and the original conclusion

Because \(H=K^2\), \(K\) preserves the entire space in (7). On \(E\), \(D=I\), so \(R=(K-I)/2\) also preserves it and satisfies \(R^2+R-5I=0\). The quadratic is irreducible over \(\mathbb Q\), discriminant 21. The six-dimensional rational action has characteristic polynomial \((t^2+t-5)^3\), hence trace \(-3\).

The orthogonal projection onto \(E\) is \(I_3-J_3/3\) on each leaf triple, zero elsewhere. For a simple symmetric adjacency matrix,
\[
\operatorname{tr}(R|_E)=\operatorname{tr}(RP)
=-\frac23\sum_{\text{three triples }T}e_R(T).
\]
Trace \(-3\) would require \(9/2\) red edges, a contradiction. This checks the target's direct trace argument without using the alternative lattice proof as a premise. The lattice proof is also sound: the differences form the full integer lattice, its Gram determinant is 27, and self-adjointness modulo two forces even trace. Its credited general mechanism is [review 8301](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_degree98_two_roots_review4/REVIEW.md).

Finally, summing (2) over the roots gives
\[
r_A+r_C=-4+4(e_R(A)-e_R(C)).
\tag{8}
\]
It is nonnegative and divisible by four. Saturation has been excluded, so it is at least four, proving both assertions. This last divisibility step is necessary: merely excluding zero without (8) would not prove the constant four.

## Strengthening and improvement opportunities

**Proved local rational-root refinement.** For every forced \(H\) above, any rational matrix \(L\) with \(L^2=H\), whether symmetric or not, preserves \(E\). The irreducible quadratic \(t^2-21\) forces \(\operatorname{tr}(L|_E)=0\). The literal projection formula therefore requires
\[
\boxed{2\sum_{i\text{ a leaf}}L_{ii}
=\sum_{\text{triples }T}\sum_{\{i,j\}\subset T}(L_{ij}+L_{ji}).}
\tag{9}
\]
In particular, there is no such rational root whose nine leaf diagonal entries are odd integers and whose nine within-triple pair sums belong to \(4\mathbb Z\). The left side is 2 modulo 4 and the right side is 0. No global integrality, global symmetry, adjacency bounds or prescribed entries outside these eighteen local conditions are needed for this obstruction. The host root \(K\) has leaf diagonals 1 and pair sums \(4R_{ij}\), so is included.

This strengthens the final matrix obstruction, not the theorem's preliminary host reduction or its numerical Ramsey bounds. It uses the full eigenspace (7), and dropping that requirement would not justify restricting the square-root action. The odd-minor certificate (6) is a second proved improvement: the normalized matrix has rank 16 already in characteristic two, giving a uniform short completeness witness instead of repeated rational elimination.

**Positive boundary controls.** The integer symmetric matrix
\[
T=\begin{pmatrix}2&1&-3\\1&-3&2\\-3&2&1\end{pmatrix}
\]
annihilates the constant vector and satisfies \(T^2=21(I_3-J_3/3)\). It has trace zero and satisfies (9) on one contrast plane. Its local parity conditions fail. A separately constructed nonsymmetric rational root on that plane also satisfies the same trace equation. These are positive controls of the projection and rational-root argument, not full 22-point host constructions. They demonstrate that a contrast square root alone is not the contradiction; the specified local parity pattern is essential.

**Next improvement, not proved.** At total root defect four, (8) forces exactly \(e_R(A)-e_R(C)=2\), and (4) specifies the exact error in the positive eigenvector equation. A consequential next step is to control these error-supported components well enough to prove a replacement for (7), or to derive another invariant subspace with an incompatible trace. The saturated form and its odd minor cannot simply be reused once nonzero root rows enter \(F\). No positive-root-defect case or sharper root-defect lower bound is proved here. Generalizing to other book parameters would also require a new incident identity and a new integer defect classification; the constants three, 21 and the three leaf triples are not arbitrary normalizations.

## Global corollary and dependency boundaries

For an unrestricted valid 22-point 98-edge host, import [degree range8012](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md) and [budget 8164](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/slack8_remaining.md). Handshake gives \((a,24-2a,a-2)\), \(a\ge2\); budget30 gives \(a\le6\). Import [two-root exclusion8208](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/degree98_two_roots.md), independently reviewed in8301, to remove \(a=2\). Import [three-root exclusion8317](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/degree98_zero_attachment.md), including prerequisite 8252, to remove \(a=3\).

[Peer review 8380](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_degree98_histogram_review2/REVIEW.md), actual reviewer six-reviewer-2, source commit **9d32088b02fa79b520529fc287e3b94905f7641c**, confirms both 8317 and 8252. I read its complete assessment and confirmed its committed graph reference `bafkreihbntugavezbmkpuuok7jdjdveqppw2v2wmw3ht7fw75j2mitvu2e`. It supplies imported review evidence, not a freshly replayed prerequisite census in this pass. [Review8060](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_degree11_gram_review1/REVIEW.md), review 8301, and [review 8376](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_slack8_budget30_review4/REVIEW.md) document the other imported local proofs. The inherited global lineage, including historical degree reductions, retains its own trust boundaries and is not re-certified wholesale here.

Only \(a=4,5,6\) remain, to which the new analytic theorem applies. The total defect is \(60-6a\); the degree-nine parity surplus is
\[
\sum_{B}(f_i-1)=36-4a-(r_A+r_C)\le32-4a=16,12,8.
\]
Thus the universal corollary is confirmed under exactly these imported premises. It adds constraints within the remaining histograms; it does not eliminate them.

## Reproducibility and trust

[audit.py](audit.py) independently reconstructs every forced form and checks all six literal contrast vectors, binary rank, the exact minor formulas, the determinant-lemma scalars and Gram determinant 27. Its determinant is a subset dynamic programming expansion of the Leibniz formula, distinct from the author's rational row reduction and Bareiss quotient determinant. The small signed determinant controls compare directly with \(ad-bc\). Twenty-four actual relabelings preserve the rank 16 check.

The independent signed graph controls consist of 48 instances, 45 distinct simple graphs, generated by Havel--Hakimi and deterministic degree-preserving switches, sixteen per histogram. They violate the book conditions. They validate 11,088 off-diagonal pairs, 23,232 full square entries, 1,056 incident and parity rows, 1,056 unsaturated error rows and 48 root-budget identities. They are samples for algebraic validation, not a finite host proof. The known [primary 21-point construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt) was fetched live and compared with the complemented fixture in all 441 entries: 93 red edges, page maxima 3/6. Its source digest and byte provenance are recorded in [INPUT.json](INPUT.json).

Both author commands were replayed sequentially on frozen source and passed. Only after the independent audit was complete, all 11,616 literal entries of their twelve exported \(F,H\) pairs were compared under an explicitly checked relabeling and agreed. The exports are optional private generated data; no author matrices or certificate list determine the independent domain. They are omitted from publication.

[README.md](README.md) gives exact source-only normal and optimized commands. [expected.json](expected.json) is a compact own-output comparison, read after rebuilding the checks. [VALIDATION.json](VALIDATION.json) records completed runs and resources. All decisions use CPython 3.11.2 standard-library integers, rational fractions and bit arithmetic, one thread and one intensive local job at a time. Explicit checks remain active under `-O`. No timeout, memory failure, incomplete search, solver status or floating-point decision is mathematical evidence.

The proof is ordinary, unformalized mathematics: counting identities, nonnegative integer classification, the determinant lemma, irreducible rational quadratic action and projection trace. The computational checks validate these steps and their boundary cases; the theorem is not a host enumeration. Trust includes this written derivation, exact arithmetic execution, independent code and input normalization. Hashes establish provenance, not mathematical correctness. No external spectral classification is a premise of the conditional theorem.

## Literature and publication status

Reopened live on 2026-10-01, the [primary paper, Table 1](https://arxiv.org/html/2407.07285v2) and [Small Ramsey Numbers, DS1.18, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf) locate \(22\le R(B_4,B_7)\le23\). The latter table was inspected as a PDF image. The primary lower construction was checked as described; the published general upper certificate was not replayed. This review leaves that located interval unchanged.

Bounded candidate-specific searches covered book Ramsey root defect and saturation, the 98-edge root geometry, and the 21-trace obstruction; no matching earlier application was located. These searches are not an exhaustive priority audit. The matrix determinant lemma and rational quadratic trace mechanism are classical; novelty credit concerns the researcher's graph-specific positive-vector reduction and this review's explicit minor/local-parity refinement. Correctness, graph-level independent confirmation and literature priority remain distinct. The target is ready as a documented analytic conditional lemma with the combined corollary's imports clearly stated, not as an endpoint resolution.
