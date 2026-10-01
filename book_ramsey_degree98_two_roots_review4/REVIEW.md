# Independent review of the 98-edge two-root exclusion

Actual reviewer **six-reviewer-4**, role **independent mathematical reviewer**,
2026-10-01. Target: six-books-1's committed lemma **8208**,
**bafkreiggmsqvmcwndsvgcwyase5zquyiph4dqnia3zayw3vgdj6fqzurdq**,
[original proof](../book_ramsey_4_7_degree_reductions/degree98_two_roots.md),
reviewed source commit **af87c8a808b7ca7549aee6648499579832aa5ebe**.
The campaign shares a signing key; authorship and independence are established
by the named reviewer, independently selected target, and methods below.

**Verdict: confirmed, with an independent exact reproduction and a proved
uniform six-dimensional reduction.** No simple red graph on 22 vertices can
have degrees \(8^2,9^{20}\), red-edge common-neighbor counts at most three,
and complement-edge common-neighbor counts at most six. Books are ordinary
subgraphs. There is no connectedness or host automorphism assumption.
The written structural and lattice arguments are sound. All 282 forced
matrices are accounted for, including the 18 square-determinant exceptions.

The combined degree-count corollary is correct **conditional on** the credited
global degree range \(8,\ldots,10\) and budget \(3n_8+n_9\le30\).
This review independently proves the conditional two-root exclusion and
checks the corollary's algebra; it does not independently recertify the
entire budget-30 theorem 8164. No whole 98-edge boundary or Ramsey endpoint
is decided.

## 1. Audit of the graph-to-defect reduction

Let \(R\) be red adjacency, \(d=R\mathbf1\), \(e=98\). Set \(F_{ii}=0\)
and, for distinct vertices, \(F_{ij}=3-c_R(i,j)\) on red edges and
\(F_{ij}=6-c_B(i,j)\) on blue edges. Under the hypotheses \(F\) is a
symmetric nonnegative integer matrix. Direct complementary-neighbor counting
gives
\[
(R^2)_{ij}=d_i+d_j-14+(17-d_i-d_j)R_{ij}-F_{ij}\quad(i\ne j).
\]
Summing this identity and using \((R^2)\mathbf1=Rd\) proves
\[
f_i:=\sum_jF_{ij}
=2e-294+38d_i-d_i^2-2\sum_{j\in N_R(i)}d_j.
\]
Putting \(K=2R+D\), \(D=\operatorname{diag}(2d-17)\), cancels the
adjacency term on squaring:
\[
H:=K^2,\quad H_{ii}=(2d_i-17)^2+4d_i,\qquad
H_{ij}=4(d_i+d_j-14)-4F_{ij}\quad(i\ne j).
\]
These identities hold for signed defects of arbitrary 22-vertex graphs;
nonnegativity is used subsequently. They reproduce the parity-square
mechanism of 7970, not an assumed spectral classification.

Let \(A=\{a,b\}\) be the two degree-eight vertices and \(s_A(i)\) their
red incidence at \(i\). The incident formula becomes
\(f_i=2-(d_i-10)^2+2s_A(i)\). At either root, \(f_i\ge0\) forces
\(ab\) red and \(f_a=f_b=0\). Thus every defect touching a root is zero,
and \(ab\) has three common red neighbors. The other twenty vertices
partition into \(C,X,Y,Z\) of sizes \(3,4,4,9\), adjacent respectively
to both roots, just \(a\), just \(b\), or neither. Their defect row sums
are respectively \(5,3,3,1\).

Write \(u=e_a+e_b\), \(h=Ru\), \(v=e_a-e_b\), and
\(w=\mathbf1_X-\mathbf1_Y\). Root-to-other-vertex red codegrees equal
three even for blue spines, because their degree sum is 17 and their
defects vanish. Consequently
\[
R\mathbf1=9\mathbf1-u,\quad Ru=h,\quad Rh=6\mathbf1+5u;
\qquad
K\mathbf1=19\mathbf1-4u,\quad Ku=2h-u,\quad
Kh=12\mathbf1+8u+h.
\]
Here \(h\) has coordinates \(1,2,1,1,0\) on \(A,C,X,Y,Z\).
The full forced square is
\[
H=21I+16J-4(u\mathbf1^t+\mathbf1u^t)+4\operatorname{diag}(u)-4F.
\tag{1}
\]
Comparing its action on \(h\) with \(K^2h\), and using the row sums,
gives \(Fh=2\mathbf1-3u+h\), \(F\mathbf1=\mathbf1-3u+2h\), \(Fu=0\).
Thus the positive vector \(p=\mathbf1+h-2u\), taking values \(3,2,2,1\)
on \(C,X,Y,Z\), satisfies \(Fp=3p\).

A \(Z\) row has one unit defect; its weighted sum three forces its
neighbor into \(C\). Hence no defect joins \(Z\) to \(X,Y,Z\).
An \(X\) or \(Y\) row has sum three and weighted sum six; after excluding
\(Z\) and the zero root rows, every available weight is two or three.
It therefore has no defect into \(C\). At a \(C\) vertex, writing \(x\)
for its internal \(C\) weight and \(z\) for its number of \(Z\) leaves,
\(x+z=5\), \(3x+z=9\), so \(x=2,z=3\). Three loopless rows of degree
two uniquely force a unit \(C\)-triangle; the nine distinct \(Z\) leaves
split into three triples.

Finally \(Hv=25v\) and \(Kv=-3v+2w\). Commutation \(KH=HK\) forces
\(Hw=25w\), whence (1) gives \(Fw=-w\). Combining this with the
\(X/Y\) row sums forces internal degree one and cross degree two.
The internal blocks are unit perfect matchings, and \(M=F[X,Y]\) is
a nonnegative integer \(4\)-by-\(4\) matrix with all margins two.
This covers all defects compatible with a hypothetical host.

Relabel the entire \(R,F,H\) simultaneously: \(A=0,1\), \(C=2,3,4\),
\(X=5,\ldots,8\), \(Y=9,\ldots,12\), \(Z=13,\ldots,21\), with successive
leaf triples and matchings \((0,1),(2,3)\) within each side.
This is coordinate normalization; it asserts no red graph symmetry.
Every \(M\) is retained after normalization, and parallel defect
weights two are included.

## 2. Reviewer refinement: a uniform orthogonal decomposition

Let \(P\) be the adjacency matrix of the two internal matching edges and
\[
A_8=\begin{pmatrix}P&M\\M^t&P\end{pmatrix}.
\]
Its subspace \(U\) of vectors whose \(X\) and \(Y\) sums both vanish
has dimension six and is invariant, since all margins of \(M\) are two.
Let \(T\) be the integral action of \(A_8\) in the basis
\[
e_{X_i}-e_{X_3},\ e_{Y_i}-e_{Y_3}\quad(0\le i<3),\qquad
P_6=21I_6-4T.
\]
An action matrix in this unnormalized basis need not be symmetric.

The following seven mutually orthogonal invariant subspaces exhaust
the 22-dimensional space. Indicator vectors below are supported on
their named classes. For a coefficient vector \(t\in\mathbb Q^3\)
of sum zero, \(c(t)\) gives its values on \(C\), and \(\ell(t)\)
gives the same value on each corresponding leaf triple.

| Subspace | Dimension | Action of \(H\) |
|---|---:|---|
| Root contrast \(v\) | 1 | \(25\) |
| Sum-zero vectors within each of the three leaf triples | 6 | \(21I_6\) |
| \(c(t),\ell(t)\), with two independent sum-zero \(t\) | 4 | Two blocks \(B_2\) |
| Side-zero-sum space \(U\) | 6 | \(P_6\) |
| Side contrast \(w\) | 1 | \(25\) |
| \(\operatorname{span}(\mathbf1,u,h)\) | 3 | \(K_3^2\) |
| \(12\mathbf1_C-9(\mathbf1_X+\mathbf1_Y)+4\mathbf1_Z\) | 1 | \(9\) |

The fixed small blocks are
\[
B_2=\begin{pmatrix}25&-12\\-4&21\end{pmatrix},\qquad
K_3=\begin{pmatrix}19&0&12\\-4&-1&8\\0&2&1\end{pmatrix},
\]
\[
\det B_2=477,\quad \det(B_2-21I)=-48,\quad
\det K_3=-419,\quad \det(K_3^2-21I)=64.
\]
The actions follow directly from the triangle with leaf triples,
the matching/cross block, and (1). For example \(F c(t)=-c(t)+\ell(t)\)
and \(F\ell(t)=3c(t)\). The last vector is orthogonal to
\(\mathbf1,u,h\), has zero total sum, and is a 3-eigenvector of \(F\).
The cyclic block follows from the three displayed \(K\) actions.

The code supplies literal basis columns \(Q\). Its actual Gram blocks
have nonzero determinants \(2,27,81,16,8,408,1224\), proving that all
22 columns are independent. For every \(M\), it checks all 484 entries
of \(HQ=Q\,\operatorname{diag}(25,21I_6,B_2,B_2,P_6,25,K_3^2,9)\).
No floating eigenvalues are used.

Therefore, **for every one of the 282 forced forms**,
\[
\boxed{\det H=(138819843225)^2\det P_6},
\quad 138819843225=419\cdot75\cdot21^3\cdot477,
\tag{2}
\]
\[
\boxed{\dim\ker(H-21I)=6+\dim\ker T=12-\operatorname{rank}T}.
\tag{3}
\]
All other blocks avoid the eigenvalue 21. The determinant-square and
complete-kernel questions are thus reduced uniformly to six dimensions.

## 3. Independent completeness and exact arithmetic

[audit.py](audit.py) uses a third enumeration route: visit all \(3^9=19683\)
ternary top-left \(3\)-by-\(3\) interiors of \(M\). The prescribed margins
uniquely determine the first three entries of the fourth column, then
the fourth row. Reject a border outside \(0,\ldots,2\). Every admissible
matrix has exactly one such interior, so the resulting **282 distinct
matrices** are exhaustive. Neither author's row-composition nor
matching-pair generator, output, orbit representatives, or symmetry
factors select the reviewer domain.

Exact determinants use a signed subset expansion of the permutation
definition, with no divisions, Bareiss algorithm, or Gaussian elimination.
Ranks of \(T\) use the nonzero-minor criterion; each singular \(T\) has
a nonzero five-by-five minor. The complete reduced determinant distribution is:

| \(\det P_6\) | Number of \(M\) | Integer square? |
|---:|---:|---|
| 70812225 | 8 | yes |
| 73110081 | 16 | no |
| 78890625 | 8 | no |
| 83761025 | 32 | no |
| 85496961 | 32 | no |
| 87890625 | 2 | yes |
| 90603425 | 64 | no |
| 91243425 | 32 | no |
| 95890625 | 40 | no |
| 99045825 | 32 | no |
| 101330625 | 8 | no |
| 101626561 | 8 | yes |

By (2), 264 full determinants are nonsquares and cannot equal
\((\det K)^2\). Each of the other 18 has \(\det T\ne0\), so (3) makes
its complete 21-eigenspace exactly the six leaf-difference directions.
The optional matching-group orbit closure gives 16 orbits, with square
orbits of sizes 8,2,8; orbit counting is not needed for exclusion.

**Boundary caution:** 32 other forms have rank \(T=5\), and hence a
seven-dimensional 21-eigenspace. They all have nonsquare determinants.
The leaf space is not the whole eigenspace for every margin-two matrix.
The author's proof correctly performs the square-case split before
using lattice completeness; no gap is found here.

After independently generating the full domain, an optional passive
comparison agrees with every author \(M\), full determinant, floor
square root, square flag, and full \(F,H\) fingerprint in
[the original certificate](../book_ramsey_4_7_degree_reductions/degree98_two_roots_expected.json).
The complete reviewer output is [expected.json](expected.json).
Reduced-record stream SHA256:
**cc5333d383ddc66b07c1aeb91df178b1a9d1077c2ca4b18297eb872eb5eaeedf**.
Full literal \(M,F,H\) stream SHA256:
**69c42f11c9037888c017bcb983542bafc3d2b11266314f9b74d6bbb3d70b376b**.
The source specifies the canonical JSON/newline encodings.

## 4. Integral lattice obstruction and its hypotheses

For a square case let \(E=\ker(H-21I)\). It consists exactly of leaf
vectors with sum zero in each triple. Its full lattice
\(L=E\cap\mathbb Z^{22}\) has the alternative reviewer basis
\(e_{\mathrm{first}}-e_{\mathrm{second}},
e_{\mathrm{second}}-e_{\mathrm{last}}\) on each triple.
For a triple \((x,y,z)\) with \(x+y+z=0\), its integer coordinates are
\((x,-z)\). Thus this is the full lattice, not a sublattice of unproved
index. Its Gram matrix is
\[
G=\operatorname{diag}\left(
\begin{pmatrix}2&-1\\-1&2\end{pmatrix},
\begin{pmatrix}2&-1\\-1&2\end{pmatrix},
\begin{pmatrix}2&-1\\-1&2\end{pmatrix}\right),\qquad \det G=27.
\]

If a hypothetical red adjacency \(R\) exists, \(K\) commutes with \(H\),
so preserves \(E\). On \(E\), \(D=I\) because the support has degree
nine. Therefore \(R=(K-D)/2\) preserves \(E\), and its integer entries
preserve the full lattice \(L\). Its matrix \(S\) in the lattice basis
is integral, \(S^tG=GS\), and
\[
S^2+S-5I=0.
\tag{4}
\]
The irreducible rational polynomial \(x^2+x-5\), discriminant 21,
makes \(E\) a vector space of dimension three over its quadratic
field. Consequently the rational characteristic polynomial is
\((x^2+x-5)^3\) and \(\operatorname{tr}S=-3\).

Modulo two, \(G\) is a nondegenerate alternating form. In a symplectic
basis a self-adjoint matrix has equal diagonals in its two paired
blocks, and hence trace zero in \(\mathbb F_2\). This contradicts
the odd trace \(-3\). Every square case is excluded.
Rational quadratic roots do not suffice: the credited rational control
\(S_0=\left(\begin{smallmatrix}0&5/2\\2&-1\end{smallmatrix}\right)\)
is self-adjoint for
\(\left(\begin{smallmatrix}2&1\\1&2\end{smallmatrix}\right)\),
satisfies (4), and has trace \(-1\). Integrality is essential.

## 5. Reproduction, controls, and trust boundaries

[README.md](README.md) gives standalone standard-library commands.
Reviewer code imports no author module. No solver, floating-point
decision, historical graph census, omitted proof corpus, or timeout is
a premise. The complete finite domain takes approximately one second.

[controls.py](controls.py) compares the subset determinant with the literal
Leibniz definition on all 19683 ternary three-by-three matrices, includes
singular, negative, pivot, empty, and invalid-input controls, and
exhausts all 1024 self-adjoint matrices for the standard rank-four
symplectic form over \(\mathbb F_2\). It checks the concrete lattice
hypothesis examples in the next section.
[bridge.py](bridge.py) independently forms 84 degree-nine circulants
on 22 vertices, each with the edge \((0,1)\) removed. Their histograms
are \(8^2,9^{20}\); their defects are allowed to be signed.
Direct red and blue neighbor intersections check 19404 off-diagonal
identities, 1848 incident/parity identities, and 40656 full \(K^2\)
entries. These are algebraic controls, not admissible host certificates.

The credited [21-vertex fixture](baseline21.rows) is independently counted:
93 red edges, red/blue edge-codegree maxima 3/6. Its 441 entries are
checked against the freshly fetched and complemented
[original companion construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt).
This known lower-bound example is not new research.

Both original programs also pass sequentially under optimized Python.
The author's separate matching-pair implementation compares all 2538
internal-matching placements and rejects 18 alterations. Those are
credited author controls, reproduced here; the reviewer independence
comes from border completion, subset determinants, the uniform
decomposition and minor ranks. Reviewer normal and optimized complete
outputs are byte-identical. Versions, exact source hashes, commands,
runtime and memory evidence appear in [PROVENANCE.json](PROVENANCE.json)
and [VALIDATION.json](VALIDATION.json).

This is an exact computer-assisted proof with ordinary written reduction,
finite completeness, lattice invariance and trace arguments. None are
proof-assistant formalized. CPython integer arithmetic and the published
checker remain computational trust boundaries; the output hash is
provenance, not a replacement for running the checks.

## 6. Dependency scope, literature and novelty

For a valid 98-edge host, the credited degree-range theorem 8012,
independently reviewed in 8060, gives degrees \(8,\ldots,10\).
The named budget theorem 8164 gives \(3n_8+n_9\le30\).
Setting \(a=n_8,b=n_9,c=n_{10}\), the two counts
\(a+b+c=22\), \(8a+9b+10c=196\) yield
\(b=24-2a,c=a-2\). Nonnegativity gives \(a\ge2\), the budget
\(a+24\le30\) gives \(a\le6\), and this review removes \(a=2\).
Thus the target's **necessary** count list \(3\le a\le6\) follows.
Realizability is not asserted.

The [parity review 8018](../book_ramsey_parity_square_review3/REVIEW.md),
[degree review 8060](../book_ramsey_degree11_gram_review1/REVIEW.md),
[97-edge review 8140](../book_ramsey_97_boundary_review3/REVIEW.md), and
[first-slack review 8146](../book_ramsey_first_slack_review4/REVIEW.md)
are prior evidence, not reviews of this new 282-form claim.
The last audit confirms 53 predecessor forms; it does not itself
recertify all of [budget 8164](../book_ramsey_4_7_degree_reductions/slack8_remaining.md).
The 97-edge result explains the inherited lower edge bound but is not
needed for the fixed \(e=98\) conditional exclusion.
The later three-root claim 8252 is contextual downstream work and is
not audited here.

Primary literature refreshed live on 2026-10-01:
[Lidicky--McKinley--Pfender--Van Overberghe, Table 1](https://arxiv.org/html/2407.07285v2#S2)
retains \(22\le R(B_4,B_7)\le23\).
[Radziszowski's DS1.18 survey](https://www.cs.rit.edu/~spr/ElJC/sur.pdf)
is the April 24, 2026 edition.
[Dai--Lin's later constructions](https://arxiv.org/abs/2606.07214)
address other book parameter regimes and do not supply this histogram
exclusion. Exact searches for the two-root degree pattern and integral
trace mechanism found no identified prior instance; that is not proof
of priority. The graph-specific application and reviewer reduction are
potential research increments. Counting, invariant subspaces,
determinant squares, and alternating-form trace parity are classical.
The global published upper-bound certificate was not replayed.

## Strengthening and improvement opportunities

**Proved refinement, immediately usable:** equations (2) and (3) replace
282 full 22-dimensional determinant tests and 18 full kernel-rank tests
by determinants and minors of a single six-dimensional operator.
The same decomposition identifies the 32 extra-kernel cases and
clarifies exactly when the full leaf lattice argument applies.
It also gives a compact 12-row determinant certificate, rather than
requiring a large full-matrix corpus. This simplification does not
enlarge the excluded host class beyond the target theorem.

**Proved general lemma:** let \(G\) be an integral symmetric Gram matrix
with even diagonal and odd determinant. If an integral \(G\)-self-adjoint
endomorphism satisfies an irreducible quadratic
\(x^2+b x+c\) over \(\mathbb Q\), with \(b\) odd, then its rank is
divisible by four. Indeed the rational rank is \(2m\), its trace is
\(-bm\), and the alternating-form argument makes that trace even;
thus \(m\) is even. Positive definiteness is not needed for this lemma.
The target has rank six and \(b=1\), giving its contradiction.

The rank condition is sharp at four, including positive definite
even lattices of odd determinant. Set
\[
C=\begin{pmatrix}0&5\\1&-1\end{pmatrix},\
G_0=\begin{pmatrix}2&0\\0&10\end{pmatrix},\
B=\begin{pmatrix}1&1\\1&4\end{pmatrix},\
G_4=\begin{pmatrix}G_0&B\\B&G_0\end{pmatrix},\
S_4=\operatorname{diag}(C,C).
\]
Then \(S_4^tG_4=G_4S_4\), \(S_4^2+S_4=5I\),
\(\det G_4=205\), and \(\operatorname{tr}S_4=-2\).
The sum/difference decomposition gives \(G_0+B\) and \(G_0-B\),
positive definite of determinants 41 and 5, proving positivity.

Other hypotheses cannot simply be dropped: \(G_0,C\) already give
a rank-two odd-trace root if odd determinant is dropped; and
\(G=\left(\begin{smallmatrix}2&1\\1&4\end{smallmatrix}\right)\),
\(S=\left(\begin{smallmatrix}0&2\\1&0\end{smallmatrix}\right)\)
give rank two, odd Gram determinant seven, and \(S^2=2I\) if the
quadratic's linear coefficient is even. The rational example above
tests integrality, and a zero endomorphism solving the reducible
\(x(x+1)\) tests the need for irreducibility in the forced-trace step.

**Remaining opportunity, not proved:** an ordinary analytical
classification of the twelve reduced determinant values would remove
the remaining finite computation. A proof-assistant formalization
could instead certify border completion, the fixed decomposition and
the trace lemma. Applying the general lattice obstruction to other
degree histograms requires proving an entire invariant eigenspace,
its full integral lattice, and its Gram parity; recognizing a leaf
subspace or a square determinant alone is insufficient.
