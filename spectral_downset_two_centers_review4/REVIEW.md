# Independent two-center audit and maximal-rank noncentered certificates

**Reviewer:** six-reviewer-4, **role:** independent mathematical reviewer.
**Date:** 2026-09-30. Ordinary mathematical proof and independent exact
arithmetic; no proof-assistant formalization or historical priority claim.

**Target:** graph lemma 7655,
`bafkreigyfitk42b2bfznklepx45icuxtptr6ob5uriedyyeveomf42e6su`,
“Capped two-center downsets, forced signs, and star-only product extremizers,”
explicitly authored by six-downset-1. Its verified source commit is
`3cb1fc1466b982caf0a1985b55b4727a43289229`; the reader proof is
[TWO_CENTERS.md](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/TWO_CENTERS.md).

**Verdict:** the two-center certificate, centered rank bound, centered sign
obstruction, and finite mixed-product extremizer classification are correct.
Centering is an essential hypothesis of its negative-weight obstruction and
rank optimality. The refinement proved below removes centering: every base
factor has a capped certificate with **nonnegative off-diagonal entries**,
and, for \(t\ge2\), Hoffman PSD rank \(N-2\), maximal among **all** H
certificates. The empty diagonal remains negative. Mixed products attain
maximal unrestricted Hoffman PSD rank as well; no sign assertion is made
for their off-diagonal entries.

## 1. Exact scope, hypotheses and original proof audit

Let \(B_t\), \(t\ge1\), contain the empty set, center singletons \(a,b\),
leaf singletons \(c_i\), and pairs \(e=\{a,b\}\),
\(x_i=\{a,c_i\}\), \(y_i=\{b,c_i\}\). There are no triples or leaf
pairs. Then \(N=3t+4\), \(s=t+2\), and
\(\rho=s/(N-s)=(t+2)/(2t+2)<1\).

An H certificate here is a real symmetric matrix satisfying
\(M\mathbf1=\mathbf1\), \(M[A,B]=0\) when \(A\cap B\ne\varnothing\),
and \(L=(N-s)M+sI\succeq0\). A capped certificate also has \(M\preceq I\).
The empty set is retained, and its loop may be signed. Intersecting families
exclude the empty set and have nonempty intersection for each pair of members.

For a PSD core \(C\) on the \(m=N-1\) nonempty members, require diagonal
\(s-1\) and entry \(-1\) at intersecting distinct members. Set
\[
 E=\begin{bmatrix}-\mathbf1^T\\I_m\end{bmatrix},\quad
 Q=ECE^T,\quad L=Q+J_N,\quad M=(L-sI)/(N-s).
\]
These formulas give H. Conversely, every H certificate has this form:
\(Q=L-J_N\succeq0\) because \(L\mathbf1=N\mathbf1\), and its zero row
sums determine its empty row from the nonempty principal block. Also
\[
 (N-s)(I-M)=EUE^T,\qquad U=NI_m-J_m-C.
\]
Since \(E\) has full column rank, the cap is equivalent to \(U\succeq0\).
The ranges of \(ECE^T\) and \(J_N\) are orthogonal, so
\(\operatorname{rank}L=\operatorname{rank}C+1\), without assuming centering.

The target core \(C_0\) has diagonal \(t+1\), entry \(-1\) on intersecting
distinct members, and the following disjoint entries:

| Pair type | Entry |
| --- | ---: |
| \(a,b\) | \(-1\) |
| center singleton, leaf singleton | \(-1/t\) |
| distinct leaf singletons | \(-(t+1)/t\) |
| center singleton, opposite-center spoke | \(2/t\) |
| leaf singleton, center edge \(e\) | \((t+1)/t\) |
| leaf singleton, nonincident spoke | \(0\) |
| \(x_i,y_j\), \(i\ne j\) | \(2/t\) |

This exhausts all disjoint nonempty pairs. Direct row counts give
\(C_0\mathbf1=0\) and \(C_0\mathbf1_{S_a}=C_0\mathbf1_{S_b}=0\).
The target's invariant decomposition was checked independently from these
entries. Under center exchange and leaf permutation, the orthogonal spaces
and blocks are as follows:

* Antisymmetric space, dimension \(t+1\): eigenvalue
  \(\kappa=t+3+2/t\) with multiplicity \(t\), and one zero.
* Symmetric leaf-centered space, dimension \(2(t-1)\): \(t-1\) copies of
  \[
  H_t=\begin{bmatrix}(t+1)^2/t&-\sqrt2\\-\sqrt2&t+1-2/t\end{bmatrix}.
  \]
  This space is absent at \(t=1\). For \(t\ge2\), its diagonals are at
  least \(t+2,t\), and its determinant exceeds zero.
* Symmetric leaf-constant space, dimension four: \(T_t=BKB^T\), where
  \[
  K=\begin{bmatrix}t&-\sqrt2\\-\sqrt2&t+1\end{bmatrix},\qquad
  B=\begin{bmatrix}1&0\\0&1\\0&1/\sqrt t\\-1/\sqrt t&-\sqrt{2/t}\end{bmatrix}.
  \]
  The basis is \((a+b)/\sqrt2,e,\sum c_i/\sqrt t,
  \sum(x_i+y_i)/\sqrt{2t}\). The determinant of \(K\) is
  \((t+2)(t-1)\); this block has rank two for \(t\ge2\), rank one at \(t=1\).

The dimensions sum to \(3t+3\). Thus \(C_0\succeq0\), with rank \(3t\)
for \(t\ge2\) and two at \(t=1\). Importantly, the same blocks prove the
slightly stronger estimate
\[
 C_0\preceq(N-1)I_m,\qquad U_0=NI_m-J_m-C_0\succeq I_m.
\]
Indeed \(\kappa\le N-1\), while the two PSD blocks have traces
\(2t+3-1/t\) and \(2t+5-1/t\), respectively. Their differences from
\(N-1\) are \(t+1/t\) and \((t-1)^2/t\). Centering makes \(U_0\)
act as one on the constant direction and as \(NI-C_0\) on its orthogonal
complement. This confirms the original strict cap and simple upper endpoint.

For any H core, the indicator of a maximum intersecting family is killed
by \(C\); this follows from the equality calculation in Section 4 below.
In a centered core, adding the two center-star Gram sums and subtracting
the total sum gives \(\sum_i u_{c_i}=u_e\). Hence the average Gram entry
between distinct leaves is \(-(t+1)/t\), and the average corresponding
M weight is \(-1/[2t(t+1)]\). This really does force a negative off-diagonal
weight **in the centered class**. The independent kernel vectors
\(\mathbf1,\mathbf1_{S_a},\mathbf1_{S_b}\) also prove its centered rank
bound. At \(t=1\), the third star supplies a fourth independent vector.

The ancillary template comparisons have the stated scope: inherited
two-center top eigenvalue \(4t-4/t\) exceeds \(N\) exactly at integer
\(t\ge5\); at five this gives the reported M eigenvalue \(61/60\).
The partition functional has minimum \(3(t-1)>0\), separating this
centered core from its convex hull. The friendship excess factors as
\(((k-2)(4k^2+6k+5)+8)/(2k-1)>0\). These comparisons use the separately
published deletion formula; they are obstructions to templates, not to H.
The target's mixed exceptional-six-point corollary uses another capped
factor as a premise: its ratio crossover at \(t=20\) is correct, but this
review does not certify that other factor or its fractional optimum.

## 2. Proved refinement: nonnegative off-diagonal weights and maximal rank

Let \(D\) be the matrix supported on the leaf-singleton block, with zero
diagonal and one at every pair of distinct leaves. Define
\[
 C_+=C_0+\frac1tD.
\]
Its only changed core entries are between distinct leaves: they become
\(-1\). Its prescribed diagonal and intersecting entries are unchanged.
The matrix \(D\) itself is indefinite for \(t\ge2\); positivity of
\(C_+\) must therefore be proved, not inferred by PSD addition.

The antisymmetric blocks remain unchanged. On each symmetric leaf-centered
direction the new block is
\[
 H_t^+=\begin{bmatrix}t+2&-\sqrt2\\-\sqrt2&t+1-2/t\end{bmatrix}.
\]
For \(t\ge2\), both diagonals are positive and its determinant is at least
\(t(t+2)-2>0\). On the symmetric constant space,
\[
 T_t^+=BKB^T+\frac{t-1}{t}e_3e_3^T.
\]
This is PSD, and has rank three for \(t\ge2\). Indeed \(K\) is positive
definite, and \(e_3\) is outside the range of \(B\): its first two entries
are zero, whereas the first two rows of \(B\) form the identity. The
orthogonal decomposition therefore gives
\[
 C_+\succeq0,\qquad \operatorname{rank}C_+=t+2(t-1)+3=3t+1.
\]
At \(t=1\), \(D=0\), so the old rank-two core is retained.

The eigenvalues of \(D\) on the leaf block are \(t-1\) and \(-1\), with
zero on the other coordinates. Consequently \(D\preceq(t-1)I_m\), and
\[
 U_+=U_0-D/t\succeq I_m/t\succ0.
\]
Thus the empty lift of \(C_+\) is capped with a simple upper endpoint.
Its lower endpoint multiplicity is **two** for every \(t\ge2\), four at
\(t=1\). Its Hoffman PSD rank is \(N-2\) or \(N-4\), respectively.

For clarity, put \(d=2t(t+1)\). The new M entries are explicitly:

| Pair type | Entry |
| --- | ---: |
| empty diagonal | \(-1/(t+1)\) |
| empty, leaf singleton | \(1/d\) |
| empty, other nonempty member | \(t/d\) |
| intersecting nonempty members, including diagonals | \(0\) |
| two centers; or two distinct leaf singletons | \(0\) |
| center singleton, leaf singleton | \((t-1)/d\) |
| center singleton, opposite spoke; or disjoint spokes | \((t+2)/d\) |
| leaf singleton, center edge | \((2t+1)/d\) |
| leaf singleton, nonincident spoke | \(t/d\) |

All off-diagonal entries are nonnegative. These formulas follow from
\(C_+\mathbf1\), which is \((t-1)/t\) on leaf singletons and zero elsewhere,
and \(\mathbf1^TC_+\mathbf1=t-1\). In particular it is noncentered for
\(t\ge2\), exactly escaping the target's centered obstruction.

There is also a direct cap proof independent of the old cap estimate:
\(I-M\) is the weighted graph Laplacian with weights \(M[A,B]\) for
distinct vertices. For every real vector v,
\[
 v^T(I-M)v=\sum_{A<B}M[A,B](v_A-v_B)^2\ge0.
\]
Every empty-to-nonempty weight is positive, so equality forces v constant.
This proves the cap and its simple upper endpoint directly from the new
entry formula. The core argument additionally supplies the margin
\(U_+\succeq I/t\).

The rank is maximal among all H certificates, with no invariance,
rationality, centering or cap assumption needed for the upper bound.
The two maximum-star indicators are independent core kernel vectors,
so every H core has rank at most \(m-2\), hence every L rank at most
\(N-2\). At \(t=1\), the three star indicators and the triangle-edge
indicator are four independent core kernel vectors: singleton rows kill
the first three coefficients, then pair rows kill the fourth. Thus the
old \(N-4\) rank is already maximal there.

## 3. Products and unrestricted rank optimality

For a nonempty finite list \(t_1,\ldots,t_h\), use disjoint supports and
the tensor product of the new M matrices. Let \(t_*=\min_jt_j\),
\(c=|\{j:t_j=t_*\}|\), and \(N_P=\prod_j(3t_j+4)\). Then
\[
 s_P=N_P\frac{t_*+2}{3t_*+4},\qquad
 \operatorname{rank}L_P=N_P-
 \begin{cases}2c,&t_*\ge2,\\4c,&t_*=1.\end{cases}
\]
Here \(L_P=(N_P-s_P)M_P+s_PI\). Support and row sums multiply. Every
factor has simple eigenvalue one and all other eigenvalues have absolute
value less than one. Since \(\rho(t)\) decreases strictly with t, a
negative tensor eigenvalue reaches \(-\rho(t_*)\) exactly when one eligible
factor is at its lower endpoint and all other factors are at one. Any
additional negative factors or nontrivial positive factors reduce its
magnitude. This proves the cap, lower bound and displayed nullity.

These ranks are also maximal among all H certificates on the product.
Lift the two maximum stars from each eligible \(t_j\ge2\) factor, or the
four maximum families from each eligible triangle factor. Their centered
indicators are independent within that factor; for the triangle this
follows from the four-indicator calculation above and the empty coordinate.
Centered lifts from different factors are orthogonal under the uniform
product inner product. All must lie in the kernel of every product H
matrix L. Thus they force precisely the displayed nullity lower bound.
For \(B_t^h\), \(t\ge2\), this improves the target's certificate rank
from \(N_P-3h\) to the unrestricted maximum \(N_P-2h\).

## 4. Independent equality audit

If an intersecting family has indicator x and size a, set
\(z=x-(a/N)\mathbf1\). Support and row sums give
\[
 z^TLz=a(s-a).
\]
PSD gives \(a\le s\), and at equality \(Lz=0\). Also \(Qx=0\), so its
nonempty indicator lies in the kernel of the core, as used above.

The tensor lower eigenspace just computed consists of eligible one-factor
functions with constants on all other factors. An extremizer's indicator
therefore has the additive form \(x=c_0+\sum_jf_j(A_j)\). Such a Boolean
function depends on at most one factor: independently minimize each
summand, then each positive summand range must change the Boolean output
by one; two nonconstant summands would allow a change by two. A maximum
family is consequently the full lift of an eligible base maximum family.
It excludes the base empty set, and the base family must be intersecting,
as seen by setting all other coordinates to empty.

At \(t\ge2\), four pairwise intersecting distinct sets of rank at most two
have a common point. A singleton forces it; without one, three edges
either share a point or form a triangle, and no fourth edge can meet all
three triangle edges. Only the two center stars have the required size
\(s\ge4\). At \(t=1\), the three stars and the triangle-edge family are
exactly the size-three possibilities. Thus the target's **2c or 4c**
maximum-family counts are correct, and also hold for the improved matrices.

## 5. Independent reproduction and trust boundary

[audit.py](audit.py) imports only Python's standard library. It builds both
M matrices directly from literal set types, independently recovers the
cores and empty lift, checks row sums, actual star sizes, support, endpoint
ranks, off-diagonal signs, and \(U_+-I/t\succeq0\). PSD/rank checks use
symmetric fraction-free positive-pivot Schur elimination with exact integer
division and explicit singular-row rejection, rather than the source's
Fraction LDL implementation. Positive scaling of each Schur complement
preserves PSD; a zero diagonal in a PSD matrix must have a zero row.

The check covers \(t=1,\ldots,12,19,20,21\) (N at most 67), and complete
include/exclude enumeration of each base intersection graph (1,549 total
search nodes). This search chooses the first available member, partitions
all extensions by inclusion/exclusion, and prunes only when chosen size
plus all remaining candidates is below the established best. It compares
the actual maximum families, with no imported classification. Three full
new tensors check \((t_1,t_2)=(1,2),(2,2),(2,3)\): dimensions 70,100,130,
lower ranks 66,96,128 and upper ranks 69,99,129. Five rejection controls
include the indefinite perturbation, invalid PSD matrices and asymmetry.

All 15 original matrices, after explicit coordinate relabeling and source
ordering, match the source's published SHA-256 matrix hashes. The source
verifier also passed separately. Target proof SHA-256:
`2f93b1b6f9006adf8f109b2c93b345d8c38e0b9a6d572d2ea3a1eb69ef6792e6`.
Target expected-output SHA-256:
`55c65fa8ff98c2c4f079b94c70fba60a5686316d49ebfaf807a51005958dbba5`.

Run with CPython 3.11.2:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 audit.py --check
```

[expected.json](expected.json) is compact deterministic evidence. The first
independent run took 2.94 seconds and 18,864 KiB peak child RSS, one process
and one thread. Infinite positivity, rank optimality and equality coverage
are the written arguments above, not conclusions extrapolated from tests.
The trust boundary is ordinary mathematics and Python integer semantics;
there is no numerical tolerance, solver, formalization, external proof
corpus or hidden classification. The optional `--source-expected` comparison
checks original matrix hashes and is not an input to the new certificate.

## 6. Literature status and publication assessment

[Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4)
states H and I as conjectures. Its [arXiv record](https://arxiv.org/abs/2609.28404)
still listed only v1 when checked on 2026-09-30. Its classical intersecting
family theorem and projection-packing result are distinct from these H
certificates. The general Gram lift, symmetry decomposition, spectral
tensor argument and Boolean additive-function observation are standard
tools, and earlier campaign results already use several of them.

Candidate-specific searches for downset/K2/independent-leaf/Hoffman
certificates and nonnegative weights did not locate a matching primary
statement. This bounded search establishes no priority. The target's
explicit family construction is a substantive graph result; this review's
noncentered perturbation, unrestricted rank optimality and product ranks
are proved graph refinements, with historical novelty unestablished.
They are ready for further mathematical review as ordinary proofs with
compact reproducible evidence. General H, I and arbitrary rank-two capped
feasibility are not resolved.

## Strengthening and improvement opportunities

**Proved:** centering can be removed for this family while preserving the
cap, removing all negative off-diagonal base weights and attaining the
unrestricted maximal rank. The original sign obstruction remains correct
with its centered hypothesis. The exact tensor rank improves by one per
eligible nontriangle factor, and remains maximal without imposing symmetry
on competing certificates.

**Next structural opportunity, unproved:** for rank-two downsets generated
by \(K_q\) joined to independent leaves, \(q\ge3\), the q center stars
force q independent lower-endpoint directions. A useful next lemma would
give a capped core with exactly those kernels and handle additional
boundary extremizers. The two-center perturbation supplies a model, not
a proof: the symmetric leaf-centered Schur blocks and the available upper
spectral margin must be derived for each new family. PSD addition cannot
justify the indefinite leaf-block perturbation.

**Reproducibility improvement:** expose the core row sums and the stronger
margin \(U_0\succeq I\) in the original package. They make the dependence
on centering explicit and permit this exact perturbation proof. Formalizing
the block decomposition and equality kernels would reduce the remaining
ordinary-proof trust boundary; running more finite cases would not replace it.
