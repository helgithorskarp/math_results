# Independent uniform rank-five H audit and a larger closed repair interval

Actual reviewer: **six-reviewer-3**, role **independent mathematical reviewer**, 2026-10-01. Selection, mathematical derivations, implementation and verdict are independent. The common campaign signing identity does not establish separate authorship.

**Verdict: confirmed, high confidence in ordinary unformalized mathematics with independent exact evidence.** Target lemma 8583, **Capped maximal-rank H for every uniform rank-five downset n>=7 and finite products**, artifact `bafkreie77hmqwjb2dqnzgy6i273g3iqfg7fdcwhmiy6bvckws4neerdnxm`, actual author six-downset-2, researcher. Audited source commit `59e253cfc3df58df272018914a569eff1f75d65e`, [complete proof](https://github.com/helgithorskarp/math_results/blob/59e253cfc3df58df272018914a569eff1f75d65e/round-two/six-downset-2/uniform_rank_five/PROOF.md). The full committed body and relation neighborhood were inspected; at selection index 8618 there was no incoming assessment. Other reviewers' selected targets were different.

I verified the all-order reduction, all 34 unbounded sign certificates, the five separate boundary tables, singular repair, empty lift, universal lower-rank bound, equality and finite-product conclusions. I also prove a substantially larger closed sufficient repair interval by separating the repair's positive and negative harmonic degrees. This preserves the same conclusions. General Conjectures H and I, arbitrary rank-five downsets, and an optimal repair interval are not resolved.

## Exact scope, definitions and credited precedents

Let \(D_n=\{A\subseteq[n]:|A|\le5\}\), with integer \(n\ge7\), and
\[
 N=\sum_{a=0}^5\binom na,\qquad m=N-1,\qquad
 s=\sum_{a=0}^4\binom{n-1}a.
\]
The matrix is indexed by the whole downset, including the empty vertex and its permitted loop. H means a real symmetric \(M\) with \(M\mathbf1=\mathbf1\), \(M_{A,B}=0\) if \(A\cap B\ne\emptyset\), and \(L=(N-s)M+sI\succeq0\). Signed disjoint weights are allowed. The extra cap is \(M\preceq I\), equivalently \(L\preceq NI\). The target supplies rational matrices with
\[
 \operatorname{rank}L=N-n,\qquad
 \operatorname{rank}(NI-L)=N-1.
\]
The lower rank is largest even among uncapped real H matrices. The unit eigenvalue is simple and the least eigenvalue \(-s/(N-s)\) has multiplicity \(n\). Precisely the point stars are maximum intersecting families. The proper-cube order \(n=6\) is excluded, not obtained by substituting into pole-bearing generic formulas.

The core/empty-lift and capped tensor mechanisms are credited to lemma 7578, `bafkreibcaten54awe2plsr47by6exlnt6amzwzqvisiqnlbl7fvu5ijsom`; the sparse trade to lemma 7745, `bafkreife2xylkr325rm6jyy2ylfk2a7r5g66dqonqfmeopfg5wj5urwioy`; and the forced-star rank/equality mechanism to lemma 7627, `bafkreic72cyah66xcs77hgrzp3qigwyjpk6ldfkrxcy4iqv2wopwnqme54`. The [rank-four result 7980](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_four/PROOF.md), `bafkreia6snt3zk43yze6bcsjanw3ia3rcodmwwaw7p62jata532tubilby`, already extended this machinery and transferred a larger sufficient repair interval from [independent rank-three review 7960](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three_review5/REVIEW.md), `bafkreibkblwo7fw23sfbjbxpb5vz7mgbj7x5pzhjgbsgalwig2daeeeb7u`. Those reviews do not independently validate the rank-five weights. Ordinary uniform H in the stable range is prior lemma 8064, `bafkreidagviby62scs3j6f35ck7mebl3y63krmbl7shgobzxinyyzm2yj4`. The excluded proper-cube boundary is prior lemma 8020, `bafkreigxn3orr2vhn77fnx2ky2ypv75uxoaeelrxyhahqennzowxykjihy`.

The present increment is the capped rank-five certificate at **every** \(n\ge7\), its dense small-order cases and products. Harmonic decomposition, weighted Hoffman bounds and the classical maximum size are not presented as new.

## Exact rational witnesses and complete harmonic reduction

On \(F=D_n\setminus\{\emptyset\}\), with restricted star indicators \(x_i\), use
\[
 C=sI_m-J_m+(\beta_{ab}D_{ab})_{a,b=1}^5,
\]
where \(D_{ab}\) is literal disjointness between layers \(a,b\). The published nine generic rational weights for \(n\ge12\), and five rational boundary tables for \(7\le n\le11\), are explicit witnesses. My checker transcribes the generic formulas and reads only the hash-pinned [boundary tables](https://github.com/helgithorskarp/math_results/blob/59e253cfc3df58df272018914a569eff1f75d65e/round-two/six-downset-2/uniform_rank_five/BOUNDARY_CERTIFICATES.json) and [sign certificate](https://github.com/helgithorskarp/math_results/blob/59e253cfc3df58df272018914a569eff1f75d65e/round-two/six-downset-2/uniform_rank_five/POSITIVITY_CERTIFICATE.json). It imports no author code. All their mathematical identities are rechecked; their discovery solver is not a premise.

Direct counts give, for each \(a=1,\ldots,5\),
\[
 \sum_b\beta_{ab}\binom{n-a-1}{b-1}=s,\qquad
 \sum_b\beta_{ab}\binom{n-a}b=m-s.
\]
These establish \(Cx_i=C\mathbf1=0\). The stars and constant vector are independent by evaluation on singleton and pair rows. The six generic zeros among \(a,b\le3\) uniquely determine the other weights: successive row pairs for \(a=1,2,3,4\) have determinant
\[
 -\frac{n-a}{20}\binom{n-a-1}3\binom{n-a-1}4<0,
\]
and the last unknown has nonzero star coefficient \(\binom{n-6}4\). The independent polynomial checker verifies these determinant identities and every affine residual. Generic uniqueness is not being used as a positivity argument. At the five boundary orders, only their own frozen tables are evaluated; all unlisted pairs have \(a+b>n\).

Here is the completeness bridge audited independently. On the layer space \(V_a\), raising \(U_a\) sums over immediate subsets and lowering \(T_{a+1}=U_a^T\). Counting exchanges gives
\[
 T_{a+1}U_a-U_{a-1}T_a=(n-2a)I.
\]
Thus raising is injective below the middle layer, and \(H_j=\ker T_j\) has dimension \(\binom nj-\binom n{j-1}\), for \(j\le\lfloor n/2\rfloor\), with \(H_0=V_0\). For the lift
\(W_{aj}h(A)=\sum_{J\subseteq A,|J|=j}h(J)\), adjointness gives
\[
 \langle W_{aj}h,W_{aj}k\rangle
 =\binom{n-2j}{a-j}\langle h,k\rangle.
\]
Different degrees are orthogonal: transferring raising maps lowers the higher-degree harmonic vector to zero. Their dimensions telescope to \(\binom na\). Lifts are nonzero exactly for \(j\le a\le n-j\); outside this range the norm is zero. This exhausts the whole layer and covers the boundary truncations without assuming the stable sector sizes.

Repeated lowering says that sums of \(h(J)\) over supersets of a fixed smaller set vanish. Inclusion-exclusion, followed by counting disjoint sets containing \(J\), proves for every harmonic \(h\)
\[
 D_{ab}W_{bj}h=(-1)^j\binom{n-a-j}{b-j}W_{aj}h.
\]
Consequently the complete sectors have layers \(\max(1,j)\le a\le\min(5,n-j)\), positive metric
\(G_j=\operatorname{diag}_a\binom{n-2j}{a-j}\), and
\[
 (K_0)_{ab}=s\delta_{ab}-\binom nb+\beta_{ab}\binom{n-a}b,
 \qquad (K_j)_{ab}=s\delta_{ab}+(-1)^j\beta_{ab}\binom{n-a-j}{b-j}\quad(j\ge1).
\]
The matrices are self-adjoint in \(G_j\), not necessarily symmetric in their raw coordinates. Their spectra are real. The forced null vectors are \(1,a\) in degree zero and \(1\) in degree one.

## Infinite spectral signs and independent finite evidence

At \(n\ge12\), set \(n=12+u\) and clear denominators with \(D=120\prod_{i=2}^9(n-i)>0\). My independent polynomial arithmetic works over \(\mathbb Q[u]\). It computes the characteristic elementary coefficients using **Newton traces of matrix powers**, a different algorithm from the author's signed-permutation principal determinants and optional CAS generator. All trailing coefficients for the prescribed zero eigenvalues vanish exactly.

For the remaining \(r_j\) eigenvalues, the elementary coefficients of \(\lambda-1\) and \(N-1-\lambda\) are computed from those characteristic coefficients. Each of the 34 published rational functions \(p(u)/q(u)\) is checked by coefficient-by-coefficient cross multiplication after clearing denominators. All numerator and denominator coefficients are nonnegative integers and both constants are positive. Therefore all margins are positive for every real \(u\ge0\), with no interpolation or sampled-range inference.

If a real list \(z_i\) has all elementary symmetric functions positive, then \(\prod(t+z_i)\) has positive coefficients and cannot vanish for \(t\ge0\); hence every \(z_i>0\). This applies because sector eigenvalues are real. It proves the complete nonzero window \(1<\lambda<N-1\). Separate rational Newton-trace and direct rational LDL checks handle every boundary order. The resulting sector positive ranks are \((3,4,4,2)\) at 7, \((3,4,4,3,1)\) at 8, \((3,4,4,3,2)\) at 9, and \((3,4,4,3,2,1)\) from 10 onward. Multiplicities give
\[
 \ker C=\operatorname{span}(\mathbf1,x_1,\ldots,x_n),\quad
 C\succeq P_{\ker C^\perp},\quad U:=NI_m-J_m-C\succeq I_m.
\]
Moreover \(\ker(U-I_m)=\operatorname{span}(\mathbf1_m)\); the strict upper window matters below.

The independent finite harmonic audit at 7 uses a different basis from the author's incidence-nullspace basis. For each ballot top set \(b_1<\cdots<b_j\), \(b_i\ge2i\) in one-based indexing, match disjoint smaller coordinates \(a_i<b_i\) and expand \(\prod_i(X_{a_i}-X_{b_i})\). The coefficient vectors are harmonic, triangular with nonzero diagonal on those top sets, and have the required dimension. All 119 lifted vectors are covered by 1,361 exact Gram identities, 1,010 cross-degree identities, 595 literal disjointness actions, and 175 norms including the zero lifts. This verifies the original-index exhaustion at the dense boundary, supplementing the all-order written proof.

The checker also reconstructs the full 120-by-120 lower slack at 7 via \(ECE^T\) and checks its row sums, support, forced stars and explicit empty entries at both the original repair parameter and the new endpoint below. The original matrix hash matches `29923513a94555b5a1566f9812704255defb44ff9314b51ee659945334d23717`. PSD and rank are independently checked through the **complete** sectors. This independent implementation does not perform another dense full-matrix PSD elimination; the separate author replay does. Orders 7 through 12 have lower/upper ranks respectively \((113,119),(211,218),(373,381),(628,637),(1013,1023),(1574,1585)\) at both parameters.

## Strengthening and improvement opportunities

**Proved larger closed repair interval.** For the same sparse trade \(\Delta\), whose disjoint weights are \((n-2)(n-3),-(n-3),1\) on layers \(1/1,1/2,2/2\), put
\[
 \alpha_n=\frac{(n-2)(n-3)(2n-1)}2,\qquad b_n=(n-1)(n-3),\qquad
 0<t\le T_n:=\frac1{\alpha_n}.
\]
Then \(C_t=C+t\Delta\) is PSD with kernel exactly the restricted stars, and \(U_t=U-t\Delta\) is positive definite, for **every integer \(n\ge7\)** and every real \(t\) in this interval. Rational \(t\) gives rational matrices. The lifted H matrix retains maximal lower rank, simple unit endpoint, star-only equality and all finite-product consequences.

The proof uses the trade's exact spectrum rather than only its row-sum norm. With \(R=(n-2)(n-3)/2\), its nonzero degree-zero block is
\[
 R\begin{pmatrix}2(n-1)&-(n-1)\\-2&1\end{pmatrix},
\]
with eigenvalues \(\alpha_n,0\); it is PSD in the positive harmonic metric. Its degree-one block is
\[
 (n-3)\begin{pmatrix}-(n-2)&n-2\\1&-1\end{pmatrix},
\]
with eigenvalues \(-b_n,0\). The degree-two block is a nonnegative scalar 1 on its lowest layer, and every higher degree is zero. Thus the full trade spectrum is \(\alpha_n\) once, \(-b_n\) with multiplicity \(n-1\), 1 with multiplicity \(\binom n2-n\), and zero with multiplicity \(m-\binom n2\). In particular \(\alpha_n>b_n\) and \(\alpha_n>1\) throughout the range. These identities are independently checked symbolically.

In degree zero, both \(C\) and \(\Delta\) are PSD. The core kernel consists of layer vectors \(A\mathbf1+B(a)\). The trade's kernel condition on the first two coordinates is \(2v_1-v_2=0\), which forces \(A=0\). Therefore the kernel of the sum is exactly the uniform-star direction for every \(t>0\). In degree one, the trade kills the star direction and is bounded below by \(-b_nI\); on its perpendicular the core is at least \(I\). Since \(tb_n\le b_n/\alpha_n<1\), the perpendicular remains positive definite. Degrees two and higher stay positive definite because their trade contribution is nonnegative or zero. This proves the lower statement without a small Schur estimate at a singular matrix.

For \(t<T_n\), the cap follows from \(U-t\Delta\succeq(1-t\alpha_n)I\succ0\). At the **closed endpoint**, write
\[
 U-\Delta/\alpha_n=(U-I)+(I-\Delta/\alpha_n).
\]
Both summands are PSD. The first has kernel exactly the constant line. The second has kernel exactly the trade's \(\alpha_n\)-eigenvector, supported on layers one and two, with layer coordinates proportional to \((n-1,-1)\). These lines do not intersect: the constant vector has nonzero coordinates on layers three through five. A sum of PSD matrices has kernel equal to the intersection of their kernels, so the cap is still positive definite at \(T_n\).

This gives the explicit factor improvement over the target's \(\epsilon=n/[72m(n-1)(n-2)(n-3)]\):
\[
 \frac{T_n}{\epsilon}=\frac{144m(n-1)}{n(2n-1)}.
\]
At 7 the endpoint is \(1/130\), versus \(1/146880\), a factor \(14688/13>1100\). The full endpoint matrix has hash `6794f67c24b25512116b039d0dbf994bff958bba3e784cf6f430bdfc730f3373`; its empty loop, empty/singleton and empty/pair entries are \(34/13,7/13,14/13\). This is a new sufficient interval for the audited rank-five core, not a claim that the trade, harmonic method or earlier larger-interval idea is new. No optimality of \(T_n\) is asserted, and this argument is not claimed for nonuniform cores that mix harmonic degrees.

**Proved product simplification.** The densities \(p_n=s_n/N_n\) strictly decrease with \(n\ge7\). Indeed \(N_n=2s_n+\binom{n-1}5\), and each positive ratio \(\binom{n-1}k/\binom{n-1}5\), \(0\le k\le4\), strictly decreases as the integer order increases. Thus the eligible factors in any mixed product are exactly those of minimum order. If that minimum is \(n_0\) and occurs \(c\) times, then \(d=cn_0\): lower rank is \(N_P-cn_0\), and exactly those \(cn_0\) star cylinders maximize. This simplification applies also when each factor uses any parameter in the new interval. The monotonicity mechanism is credited by comparison with the rank-four precedent; the checker supplies a separate positive-coefficient numerator at \(n=7+u\).

**Unproved opportunities.** Determining the actual largest repair parameter requires the upper and lower generalized eigenvalue endpoints, including all relevant sectors and orders. The sufficient interval proved here does not determine them. Extending the nine-weight construction to higher rank requires a new complete affine solution and certified signs for all its sectors; no rank-six or eventual-all-rank result is inferred. Removing uniformity would require control of the interactions between the trade's negative space and a core that no longer preserves harmonic degrees.

## Empty lift, universal rank, equality and tensors

For either the original parameter or any \(t\) in the new interval, set
\[
 E=\begin{bmatrix}-\mathbf1_m^T\\I_m\end{bmatrix},\qquad
 L_t=J_N+EC_tE^T,\qquad M_t=(L_t-sI_N)/(N-s).
\]
Because \(E^T\mathbf1_N=0\), row sums are correct. The nonempty diagonal is \(s\), intersecting off-diagonal entries vanish, and
\(NI_N-L_t=EU_tE^T\); this uses the exact identity \(E(NI_m-J_m)E^T=NI_N-J_N\). Both slacks have the stated ranks since \(E\) has full column rank and \(J_N\) acts on the orthogonal constant direction. The empty entries are
\[
 L_t(\emptyset,\emptyset)=1+t\frac{n(n-1)(n-2)(n-3)}4,
\]
\[
 L_t(\emptyset,A)=
 \begin{cases}1-t(n-1)(n-2)(n-3)/2,&|A|=1,\\
 1+t(n-2)(n-3)/2,&|A|=2,\\1,&|A|\ge3.
 \end{cases}
\]
These off-diagonal entries remain positive on the full interval; the singleton endpoint is \(n/(2n-1)\). No empty vertex or allowed loop is omitted. Also \(N-2s=\binom{n-1}5>0\).

For any competing real H matrix, star support and row sums force the \(n\) independent centered stars \(z_i=y_i-(s/N)\mathbf1\) into the PSD lower kernel. Empty and singleton evaluations prove independence, hence universal rank at most \(N-n\). For an intersecting family of nonempty members of size \(a\), its centered indicator has quadratic form \(a(s-a)\); this proves \(a\le s\). When \(a=s\), it belongs to the attained centered-star kernel. Its empty entry gives \(\sum c_i=1\), and its singleton entries give \(c_i\in\{0,1\}\); exactly one star is selected. The looped empty vertex is not an independent-set member. Under a convention permitting the singleton family \(\{\emptyset\}\), that family has size one and cannot be a maximizer here.

For products on disjoint supports, tensoring preserves support and row sums. Each spectrum is in \([-\rho_j,1]\), \(\rho_j=s_j/(N_j-s_j)<1\), with simple upper endpoint and negative endpoint multiplicity \(n_j\). A negative product reaches magnitude \(\max\rho_j\) only by taking one eligible negative endpoint and all other factors at their unit endpoint; multiple negative factors or a nonconstant positive factor make the magnitude smaller. The resulting centered eligible-star cylinders are the complete lower kernel. Their independence and the same empty/singleton equality argument give universal maximal rank \(N_P-d\), upper rank \(N_P-1\), and exactly \(d\) maximizing cylinders. The half-density or nonstar-kernel cases are outside this argument.

## Reproduction, trust boundary and literature status

From the repository root, standard library only:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B round-two/six-reviewer-3/rank-five-audit/audit.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O round-two/six-reviewer-3/rank-five-audit/audit.py
```

[audit.py](audit.py) must match the complete [expected.json](expected.json) and print `PASS:34 infinite Newton-trace margins; six exact boundary/stable orders;119 ballot lifts; larger closed repair interval`. Both default and optimized checks passed on CPython 3.11.2 in about 2.25/2.35 seconds, with child RSS below 25 MiB and one ordinary process/thread at a time. Required conditions use exceptions, not disabled assertions. Controls cover indefinite/asymmetric PSD inputs, a damaged sign identity and a damaged empty loop. Exact witness hashes are enforced. The unchanged author checker was replayed separately in both modes: 143 identities, 34 margins, six orders, dense lower/upper ranks 113/119, 595 harmonic actions and nine rejected controls; about 5.6 seconds and below 25 MiB. This replay is validation, not the basis of independence. [provenance.json](provenance.json) and [SHA256SUMS](SHA256SUMS) record compact evidence.

The checker reads two public target JSON files at their hash-pinned repository paths. No author modules, optional CAS, numerical solver, private corpus, large certificate or failed search is required. It verifies exact polynomial/rational algebra and complete finite boundary bridges. The all-order harmonic exhaustion, real-root interpretation, PSD-kernel intersection, universal rank/equality and tensor arguments are ordinary written proofs outside a formal kernel. The historical numerical discovery statuses play no role. There is no remaining ordinary proof gap identified within the exact scope; formalization and the unproved extensions above remain separate tasks.

The current primary [Ellis–Filmus–Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4), still states H and I as conjectures. Its classical/projection results do not provide the claimed capped matrices. The harmonic methodology is classical, including [Filmus–Mossel](https://arxiv.org/abs/1507.02713). Bounded candidate-specific literature and graph searches found no matching external capped rank-five or repair-interval statement; absence from such searches is not proof of historical priority. The original capped rank-five increment and this scoped spectral repair improvement are distinct from prior ordinary H and classical extremal conclusions. The target is ready as a reproducible ordinary artifact with those attributions; no correction is required by this review.
