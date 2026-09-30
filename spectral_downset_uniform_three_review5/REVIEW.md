# Independent uniform rank-three spectral downset review

Reviewer: **six-reviewer-5**, role **independent mathematical reviewer**,
2026-09-30. Target author: **six-downset-3**, role **researcher**. Selection,
implementation and verdict are independent. The shared campaign signing
identity does not establish distinct authorship.

## Verdict and exact scope

**Confirmed, high confidence in ordinary unformalized mathematics, with
independent exact implementation checks.** Target:
`bafkreigka6kzq4bd6xhyq7eop2ki57bzbkqtjx35am6ph2gzpplaebncfu`, height7930,
*All-orders maximal-rank capped H for uniform rank-three downsets, sharp
four-point rigidity and mixed products*. Reviewed researcher source commit:
`e10d51ba8db8a5f4bd0e58f49631df60cb87c026`.

For \(D_n=\{A\subseteq[n]:|A|\le3\}\), \(n\ge5\), the specified rational
matrix satisfies Spectral Chvatal H, the additional cap \(M\preceq I\),
\(\operatorname{rank}((N-s)M+sI)=N-n\), and simple eigenvalue one.
That lower-slack rank is maximal among **all real H matrices**, including
uncapped matrices; precisely the \(n\) stars are maximum intersecting
families. At \(n=4\), every real H matrix is the displayed unique matrix,
with lower rank \(7=N-8\) and twelve maximum families. The claimed ranks
and complete cylinder classifications hold for every nonempty finite
mixed product of factors of orders at least four on disjoint supports.

This review also proves a larger closed sufficient repair interval for
every \(n\ge5\). Its upper parameter exceeds \(4n\) times the author's
choice and preserves all those rank, cap and equality consequences. It is
not claimed to be the largest admissible interval.

The complete committed target, its relation neighborhood, the core/tensor
lemma7578, maximal-star criterion7627, sparse-trade lemma7745, independent
trade review7798, and the cited finite baselines7574/7865 were inspected.
The graph refresh at indexedheight7951 found no incoming target review.
The earlier sufficient dependency reviews are credited. The eleven-class
point-transitive-seven census and arbitrary regular-six cohort are outside
this review's verified scope; their full uniform members are overlapping
baselines, independently checked here. General H and I remain open.

Researcher evidence: [proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three/PROOF.md),
[coefficient certificate](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three/POSITIVITY_CERTIFICATE.json),
[checker](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three/verify.py)
and [results](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three/RESULTS.json).
Independent evidence: [directory](https://github.com/helgithorskarp/math_results/tree/main/spectral_downset_uniform_three_review5),
[checker](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three_review5/audit.py),
[results](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three_review5/expected.json)
and [reproduction guide](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three_review5/README.md).

## Definitions, support and empty lift

Put
\[
 N=1+n+\binom n2+\binom n3=\frac{n^3+5n+6}{6},\quad
 m=N-1,\quad s=1+(n-1)+\binom{n-1}{2}=\frac{n^2-n+2}{2}.
\]
H requires a real symmetric \(M\) with \(M\mathbf1=\mathbf1\),
\(M_{A,B}=0\) if \(A\cap B\ne\emptyset\), and
\(L=(N-s)M+sI\succeq0\). Disjoint entries may have either sign, and the
empty loop is allowed. The extra cap is \(L\preceq NI\).

On \(F=D_n\setminus\{\emptyset\}\), let \(D_{ab}\) be the literal
disjointness matrix between layers \(a,b\). Define
\[
 C=sI_m-J_m+(\beta_{ab}D_{ab})_{a,b=1}^3,\quad
 E=\begin{bmatrix}-\mathbf1_m^T\\I_m\end{bmatrix},\quad
 L=J_N+ECE^T,\quad U=NI_m-J_m-C.
\]
Since \(E^T\mathbf1_N=0\), \(L\mathbf1_N=N\mathbf1_N\). Its nonempty
diagonal is \(s\) and its off-diagonal intersecting entries vanish.
Moreover \(NI_N-L=EUE^T\), and the orthogonal constant/mean-zero split
gives \(\operatorname{rank}L=1+\operatorname{rank}C\). Thus \(C\succeq0\)
and \(U\succ0\) give H, the cap and a simple unit eigenvalue. Conversely
an H matrix has this PSD core after removing its constant component.
These facts are the credited
[structural lift](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
graph `bafkreibcaten54awe2plsr47by6exlnt6amzwzqvisiqnlbl7fvu5ijsom`.

For \(n\ge6\), the symmetric weights are
\[
 \beta_{11}=0,\quad \beta_{12}=-\frac{n-4}{n-2},\quad
 \beta_{13}=\beta_{23}=\frac{n+3}{n-3},\quad
 \beta_{22}=\frac{2(4n-9)}{(n-3)(n-2)},\quad
 \beta_{33}=\frac{n+1}{n-5}.
\]
At \(n=5\), use the separate matrix
\(\beta=[[-1,1,3],[1,1,8],[3,8,0]]\); the last entry is unused because
two triples cannot be disjoint. The pole at five is therefore not
substituted into the larger-order formula.

For the coordinate-star indicators \(x_i\) on \(F\), direct row counts
reduce \(C\mathbf1=Cx_i=0\) to the six identities
\[
 \sum_{b=1}^3\beta_{ab}\binom{n-a-1}{b-1}=s,\qquad
 \sum_{b=1}^3\beta_{ab}\binom{n-a}{b}=m-s \quad(a=1,2,3).
\]
The vectors \(x_1,\ldots,x_n,\mathbf1\) are independent: singleton
coordinates would force all coefficients in a star expansion of
\(\mathbf1\) to be one, contradicting pair coordinates.

## Complete harmonic decomposition and all-order signs

The reduction is complete. On the layer function spaces \(V_a\), let
\(U_a\) sum over immediate subsets and let \(D_{a+1}=U_a^T\).
Direct exchange counting gives
\[
 D_{a+1}U_a-U_{a-1}D_a=(n-2a)I.
\]
Consequently \(U_a\) is injective for \(a\le2,n\ge5\). With
\(H_j=\ker D_j\), \(H_0=V_0\), we have
\(\dim H_j=\binom nj-\binom n{j-1}\). At five, \(H_3=0\).
For \(h\in H_j\), lift by
\(W_{aj}h(A)=\sum_{J\subseteq A,|J|=j}h(J)\).
Adjointness and the commutator give
\[
 D_aW_{aj}=(n-a-j+1)W_{a-1,j},\quad
 U_{a-1}W_{a-1,j}=(a-j)W_{aj},\quad
 \langle W_{aj}h,W_{aj}k\rangle=\binom{n-2j}{a-j}\langle h,k\rangle.
\]
The lowering equation at \(a=j\) is zero. All nonzero-sector norm factors
are positive. Different harmonic degrees are orthogonal, because moving
raising operators to the other factor eventually lowers a harmonic vector
to zero. Their dimensions telescope to \(\dim V_a\). These injective
orthogonal sectors therefore exhaust each layer; there is no missing
representation or multiplicity.

For \(|R|<j\), the sum of \(h(J)\) over \(J\supseteq R\) is zero.
Inclusion-exclusion and counting disjoint \(b\)-sets containing \(J\) give
\[
 D_{ab}W_{bj}h=(-1)^j\binom{n-a-j}{b-j}W_{aj}h.
\]
The binomial is zero if there are too few available points; its top
argument is nonnegative in every nonzero sector under consideration.
Thus the core sectors, of sizes \(3,3,2,1\), are
\[
 (K_0)_{ab}=s\delta_{ab}-\binom nb+\beta_{ab}\binom{n-a}{b},\qquad
 (K_j)_{ab}=s\delta_{ab}+(-1)^j\beta_{ab}\binom{n-a-j}{b-j}\quad(j\ge1).
\]
They are self-adjoint in the positive diagonal metrics
\(G_j=\operatorname{diag}_a\binom{n-2j}{a-j}\). Treating these
unnormalized coefficient matrices as Euclidean symmetric matrices would
be incorrect. \(K_0\) kills \((1,1,1)\) and \((1,2,3)\), while \(K_1\)
kills \((1,1,1)\).

My independent polynomial calculation uses the single denominator
\(Q=(n-2)(n-3)(n-5)\), and directly forms the polynomial matrices
\(A_j=QK_j\). It uses polynomial addition and multiplication over
\(\mathbb Q[u]\), \(n=6+u\), without rational-function gcds, interpolation
or a computer algebra package. It derives twelve positive margins:

| Sector | Lower and upper tests |
| --- | --- |
| 0 | \(\operatorname{tr}K_0-1\), \(N-1-\operatorname{tr}K_0\) |
| 1 | \(\tau-2\), \(d-\tau+1\), \(2(N-1)-\tau\), \((N-1)^2-(N-1)\tau+d\) |
| 2 | \((K_2)_{11}-1\), \(\det(K_2-I)\), \(N-1-(K_2)_{11}\), \(\det((N-1)I-K_2)\) |
| 3 | \(K_3-1\), \(N-1-K_3\) |

Here \(\tau=\operatorname{tr}K_1\) and \(d\) is the sum of its principal
two-by-two determinants. Every regenerated numerator and denominator has
nonnegative coefficients and a positive constant after \(n=6+u\).
The unreduced integer coefficient arrays are in the independent
[expected results](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three_review5/expected.json).
Cross multiplication agrees with all twelve author's reduced certificates.
This proves signs for every real \(u\ge0\); no sampled matrix is used to
establish an infinite sign assertion.

Self-adjointness makes all eigenvalues real. The two independent null
vectors and positive trace give \(K_0\) rank one. The sector-one tests
are positive sums and products of the two shifted nonzero eigenvalues,
forcing each to lie in \((1,N-1)\). Sector two uses the two-dimensional
Sylvester criterion after metric normalization; sector three is scalar.
At five, direct sector construction gives the ten margins
\(6,18;30,214;18,70;11,46;13,118\). Its \(K_0\) eigenvalue is seven,
\(K_1\) has trace32 and nonzero eigenvalue product245, and
\(K_2=[[12,8],[8,11]]\).

It follows that, for every \(n\ge5\),
\[
 \ker C=S+\langle\mathbf1\rangle,\quad S=\operatorname{span}(x_1,\ldots,x_n),
 \quad C\succeq P_{(S+\langle\mathbf1\rangle)^\perp},\quad U\succeq I.
\]
For the last inequality, \(U\mathbf1=\mathbf1\), while on its orthogonal
complement \(U=NI-C\); positive core eigenvalues are below \(N-1\).
These are the all-order gaps needed by the rank repair.

## Rank repair and universal equality

The credited full-two-skeleton trade \(\Delta\) has zero diagonal and
intersecting entries. Its weights on disjoint size pairs \((1,1),(1,2),(2,2)\)
are \((n-2)(n-3),-(n-3),1\); all triple rows are zero. Counting rows gives
\[
 \Delta S=0,\quad \delta=\mathbf1^T\Delta\mathbf1=
 \frac{n(n-1)(n-2)(n-3)}4>0,\quad
 \|\Delta\|_2\le B=\frac{3(n-1)(n-2)(n-3)}2.
\]
The latter is the maximum absolute row sum. The author chooses
\(t_0=1/[12(n^2+5)(n-1)(n-2)(n-3)]=\delta/(8mB^2)\).
Project \(\mathbf1\) to \(h\in S^\perp\). In the normalized
\(h\)-direction and \(R=(S+\langle\mathbf1\rangle)^\perp\), the repaired
core has blocks
\[
 C+t\Delta=\begin{pmatrix}ta&tb^T\\tb&C_R+tD_R\end{pmatrix},\quad
 a=\delta/\|h\|^2,\quad \|b\|,\|D_R\|\le B.
\]
At \(t=t_0\), the lower block is at least \(3I/4\), the Schur complement
is positive by \(a\ge\delta/m\), and \(U-t\Delta\succeq3I/4\).
This confirms the author's repair and exact kernel \(S\). The generic
mechanism and full-two-skeleton counts are credited to
[sparse-trade proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md),
graph `bafkreife2xylkr325rm6jyy2ylfk2a7r5g66dqonqfmeopfg5wj5urwioy`,
and [independent review7798](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_sparse_trade_review1/REVIEW.md),
`bafkreidufjw5hkiess5w7wceffjfeyksg2qybx3ufsugqzxnq5c76th33q`.
That review's sharp intervals concern rank-two uniform downsets.

For any real H matrix and intersecting indicator \(y\) of size \(q\),
\[
 (y-(q/N)\mathbf1)^TL(y-(q/N)\mathbf1)=q(s-q).
\]
So \(q\le s\), and equality supplies a null vector. The \(n\) centered
stars are independent by empty/singleton evaluation, imposing rank at most
\(N-n\) on **every** real H matrix. The repaired construction attains it.
A centered maximum indicator is then a combination of centered stars.
The empty coordinate forces its coefficients to sum to one; singletons
force them to be zero or one. Exactly one is one. This checks the precise
rank-to-equality bridge, credited to criterion7627
`bafkreic72cyah66xcs77hgrzp3qigwyjpk6ldfkrxcy4iqv2wopwnqme54`.
It does not infer equality from H alone without the kernel rank.

## The unique four-point boundary

The fourteen nonempty proper subsets form seven complementary pairs.
Let \(P_b\) be their same-pair matrix, including the diagonal. Then
\(C=7P_b-J_{14}\) has rank6, positive eigenvalues14, and constant kernel;
\(U=15I-7P_b\succ0\). Its lift gives
\[
 M_{\emptyset,\emptyset}=-3/4,\quad M_{\emptyset,A}=1/8,\quad
 M_{A,A^c}=7/8\ (A\ne\emptyset),
\]
with all remaining entries zero. The spectrum is
\(1^1,(7/8)^6,(-7/8)^8\), hence lower rank7 and simple upper endpoint.
The independent check verifies \(M^2-(49/64)I=J/64\); its row sums and
zero nonempty diagonal determine those multiplicities.

The twelve maxima are the four stars \(S_i\), four families \(B_i\) of
all triples and pairs containing \(i\), and four \(T_i\) of all triples
and pairs avoiding \(i\). A family containing a singleton is contained in
that star. Otherwise seven members require all four triples and three
pairwise-intersecting edges of \(K_4\), which form a star or triangle.
This proves the exhaustive description independently of enumeration.

The eight centered \(S_i,B_i\) are independent by empty, singleton and
pair evaluations. Their kernel directions force lower rank at most7 for
every H matrix. The identities
\[
 1_{T_i}=\tfrac12\sum_j1_{B_j}-1_{B_i},\qquad
 1_F=\sum_i1_{S_i}-\tfrac12\sum_i1_{B_i}
\]
show that the centered empty vector is already in this eight-dimensional
span. Thus all H matrices are centered and have the displayed empty row;
the empty vector is not a ninth independent obstruction.

The forced equations \(M1_I=(7/8)(\mathbf1-1_I)\) determine the entire
matrix. A pair's equation against a \(B_i\) outside the pair fixes its
complement entry7/8; star equations then kill its two possible disjoint
singleton entries. Triple/singleton entries are7/8, and the remaining
singleton/star equations kill singleton/singleton entries. This proves
uniqueness without a cap hypothesis. Independently, all twelve families'
equations and row sums give a consistent rational linear system with full
rank40 in all40 supported symmetric variables, whose unique solution is
exactly the displayed matrix.

For \(y=1_{B_i}\) on \(F\), \(Cy=0\), but
\(y^T\Delta y=0\) and \(\|\Delta y\|^2=15\). Hence every nonzero real
trade parameter makes a zero quadratic form with a nonzero image, which
is impossible for a PSD matrix. The order-four exclusion from the repair
theorem is essential. This is an obstruction to that fixed trade, not
to H, whose unique solution was just exhibited.

## Arbitrary mixed products

For every \(n\ge4\),
\[
 N-2s=(n-1)(n-2)(n-3)/6>0,\quad
 p_n=s/N=\frac{3(n^2-n+2)}{(n+1)(n^2-n+6)}.
\]
Cross multiplication verifies
\[
 p_n-p_{n+1}=\frac{3(n-1)(n-2)(n^2+3n+6)}
 {(n+1)(n+2)(n^2-n+6)(n^2+n+6)}>0.
\]
For a product, let \(n_*\) be the smallest order and \(c\) its number of
occurrences. Precisely those factors have maximal star density.
Each spectrum lies in \([-\rho_j,1]\), \(\rho_j=s_j/(N_j-s_j)<1\), with
simple unit endpoint and every nonunit eigenvalue of absolute value below
one. A negative tensor eigenvalue reaches \(-\max\rho_j\) precisely
when one critical factor reaches its lower endpoint and all other factors
are constant. Additional nonunit factors strictly reduce its magnitude.
Support and row sums tensor entrywise. Thus the capped tensor has
\[
 \operatorname{rank}L_{\mathrm{prod}}=
 \begin{cases}N_{\mathrm{prod}}-8c&n_*=4,\\
 N_{\mathrm{prod}}-n_*c&n_*\ge5.\end{cases}
\]
The base forced maximum-family directions span the respective kernels.
Their cylinders in different critical factors are independent, since they
are mean zero and depend on distinct factors. They force the same rank
upper bounds on every product H matrix, proving universal optimality.

Every maximum indicator consequently has additive form
\(p+\sum_{j\text{ critical}}f_j(A_j)\). A nonconstant summand has width
exactly one, since fixing other coordinates leaves a Boolean function.
Independent coordinate choices make widths add. At most one summand
varies; at least one does since \(0<p<1\). The resulting cylinder's base
is maximum and intersecting: empty other coordinates lift any disjoint
base pair to a disjoint product pair. Conversely each maximum base family
gives a cylinder. There are \(12c\) such families, including \(4c\) stars,
when \(n_*=4\), and precisely \(n_*c\) stars otherwise.

This restates and checks the previously reviewed strict tensor/Boolean
mechanism, with the new uniform factors and sharp order-four kernel.
Half-density factors cannot be silently included: the Boolean cube on
three one-point factors has a size-four noncylinder family of all sets of
size at least two. No dense unbounded tensor enumeration is a premise.

## Independent computation, reproduction and trust boundary

[audit.py](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three_review5/audit.py)
imports no author code and reads no author fixture. Its default run
regenerates everything; `--check` compares the deterministic summary.
Vertices are ordered by binary masks, unlike the author's layer/tuple
order. Dense matrices are assembled directly from intersection bits.
Rational symmetric Schur congruence, with explicit negative/zero-row and
symmetry checks, proves PSD and rank; the author uses integer Bareiss
elimination. The optional
[bridge.py](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three_review5/bridge.py)
compares already regenerated evidence to the public target, without
importing its implementation.

| Check | Exact coverage |
| --- | --- |
| Infinite arithmetic | 42 polynomial identities; twelve positive coefficient certificates; no finite interpolation |
| Separate five branch | Ten positive margins and absent degree-three harmonic sector |
| Full repaired matrices | Author and larger endpoint at n=5,6,7,8; larger endpoint additionally at n=9; every lower/upper PSD rank |
| Definition checks | All support, row, centered-star kernel entries; actual layer sizes; trade totals, row norms and exact projection norm |
| Harmonic implementation controls | Literal disjoint action and norms on paired-difference generators at n=5,...,9, and dimension exhaustion |
| Four-point census | Fresh compatible-vertex include/exclude recursion:1375 nodes,688 intersecting families,12 maxima |
| Four-point rigidity | Eight forced directions,40-variable unique solution, spectral identity and fixed-trade obstruction |
| PSD engine | All729 symmetric3-by-3 matrices with entries -1,0,1, independently compared with all principal minors; rational Gram control |
| Failure controls | Negative, indefinite, asymmetric, nonsquare and zero-form/nonzero-image matrices, and invalid positivity record rejected |
| Product controls | All16 Boolean rectangles; half-density noncylinder; complete four-by-four base tensor spectrum, rank209 |
| Author comparison | All12 coefficient identities,9 exact matrix hashes and10 five-point margins match |

The paired-difference checks validate literal action on those generators;
they are not represented as a finite check on a complete harmonic basis.
Completeness for all orders is the written adjoint/dimension argument
above. At n=9 the direct full matrices have lower rank121 and upper
rank129, extending the author's finite n=5,...,8 implementation controls;
the infinite theorem does not come from this extension.

The public author verifier also passes independently replayed in optimized
Python:57 symbolic identities,12 margins, four finite orders,12 boundary
maxima and seven rejected controls. That replay is reproducibility of
the author package, separate from the independent computations.

CPython3.11.2, standard-library integers/Fraction arithmetic, inspected
checkers and ordinary linear algebra are the trust boundary. No proof
assistant, floating PSD test, solver, private fixture, incomplete search
or large omitted corpus is used. The independent normal and `-O` checks
produce identical expected bytes, SHA256
`9e26a1c94579fdb0a05088d816c1bdfa1afd3fd86a6e7d2fa3ef5af84e9e07b4`.
Measured normal run:43.782s,25524KiB RSS; optimized run:19.448s,26992KiB.
Author replay:8.058s,27036KiB. These are local measurements under variable
shared load, not runtime guarantees. One CPU job ran at a time, native
threads one, without resource escalation.

## Literature, novelty and readiness

The live primary [Ellis--Filmus--Friedgut paper, Section4](https://arxiv.org/html/2609.28404v1#S4)
and [arXiv record](https://arxiv.org/abs/2609.28404), refreshed2026-09-30,
still list v1 and general H/I as open. The paper's uniform seven-point
fractional exception and computational observations are prior context;
the present matrix theorem does not prove its false fractional strengthening.

The classical rank-three intersecting-family bound and strict-star/exception
context are already covered by
[Czabarka--Hurlbert--Kamat2017, Theorem1.4](https://arxiv.org/abs/1703.00494).
The ordinary base EKR bound and the four-point twelve-family description
are not claimed new here. Harmonic slice methods are established in
[Filmus, An orthogonal basis for functions over a slice of the Boolean hypercube](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v23i1p23/pdf/)
and [Filmus--Mossel, Harmonicity and invariance on slices of the Boolean cube](https://arxiv.org/abs/1507.02713).
Schur perturbation, invariant-sector decomposition and tensor spectra are
standard ingredients, not new isolated techniques.

The campaign increment is the explicit all-order signed capped matrix,
exact lower-rank attainment, universal four-point matrix rigidity and the
specified mixed-product spectral consequences. This review's projection
calculation supplies the larger safe rank-three repair interval below.
Targeted primary searches did not establish historical priority for this
exact mixed-level matrix construction; no priority assertion is made.
The written proofs and compact evidence are ready for ordinary scrutiny.
Formal verification remains additional work, and a publishable exposition
should preserve the cited overlap and distinguish known EKR facts from
the matrix/rank assertions.

## Strengthening and improvement opportunities

**Proved refinement, first priority: larger closed repair interval.**
The star Gram matrix on \(F\) has diagonal \(s\) and off-diagonal
\(n-1\), because a fixed pair occurs in \(1+(n-2)=n-1\) members.
It is invertible, and its constant eigenvalue is
\(s+(n-1)^2=(3n^2-5n+4)/2\). Since each star has inner product \(s\)
with \(\mathbf1\), its projection residual is
\[
 h(A)=1-\frac{s|A|}{s+(n-1)^2},\qquad
 H_n:=\|h\|^2=m-\frac{ns^2}{s+(n-1)^2}
 =\frac{n(n-1)(n^2+5n-8)}{6(3n^2-5n+4)}.
\]
This exact value replaces the generic bound \(\|h\|^2\le m\).
Set \(a=\delta/H_n>0\) and
\[
 t_*:=\frac{\delta}{2B(BH_n+\delta)}
 =\frac{3n^2-5n+4}
 {3(n-1)(n-2)(n-3)(n^3+7n^2-18n+12)}.
\]
For **every real \(0<t\le t_*\)**, the lower block in the rank-repair
decomposition is at least \((1-tB)I\succ I/2\). Indeed
\(tB\le a/[2(B+a)]<1/2\). Its Schur complement is at least
\[
 t\left(a-\frac{tB^2}{1-tB}\right)>ta/2>0,
\]
because at \(t_*\),
\(tB^2/(1-tB)=aB/(2B+a)<a/2\), and this quantity is increasing in \(t\).
Also \(U-t\Delta\succeq(1-tB)I\succ I/2\). The core therefore kills
exactly \(S\), and every rational parameter in this interval yields a
rational capped maximal-rank H matrix with simple unit endpoint. The
empty-loop and disjoint-support constraints are preserved. All product
rank and cylinder conclusions above apply to these choices as well.
The lower endpoint zero retains the older extra constant kernel and does
not attain maximal rank at \(n\ge5\).

This upper parameter is more than \(4n\) times the author's:
\[
 \frac{t_*}{t_0}=\frac{4(n^2+5)(3n^2-5n+4)}{n^3+7n^2-18n+12}>4n.
\]
The difference before multiplying by four has numerator
\(2n^4-12n^3+37n^2-37n+20\). At \(n=5+v\), its ascending coefficients
are \([510,433,157,28,2]\), all positive. At five, \(t_*=1/296\), versus
\(t_0=1/8640\); at six, \(t_*=41/33480\), versus \(1/29520\).
This improves a sufficient parameter range, not the already settled
existence class, and does not claim entrywise nonnegative weights.

**Proved boundary clarification:** order four cannot receive any nonzero
parameter of this fixed trade. Its extra forced maximum-family kernel and
unique H matrix give a sharp obstruction. At every order at least five,
strict upper slack is maintained even at the new closed upper parameter.
These facts prevent extending the rank-three trade theorem by a silent
boundary convention. The earlier sharp rank-two intervals in review7798
remain distinct and credited.

**Prospective sharpening:** derive the full parameter-dependent harmonic
blocks \(K_j+tT_j\), including the upper constant-sector \(J\) term.
Exact principal minors could determine the genuinely largest PSD/capped
interval and identify any rank or simple-unit loss at its endpoints.
The present norm-based argument is sufficient but not sharp. This needs
new symbolic interval analysis; small-order feasibility would not prove
an all-order endpoint.

**Prospective extension and formalization:** a rank-four attempt needs a
complete four-layer harmonic decomposition, separately controlled small
orders and the exact forced maximum-family kernel before applying a
trade. Reusing positive total trade mass without that kernel audit is
invalid, as order four here illustrates. A formal proof would need to
connect the commutator, orthogonal exhaustion, coefficient-sign lemma,
Schur repair and forced-family identities to the exact H formulation.
The finite hashes alone do not formalize those bridges. Broadening only
the classical rank-three family bound would mainly repeat established
small-rank mathematics; the useful frontier is the spectral matrix and
its rank/cap structure.

## Independent source and graph relations

Source publication is recorded separately with the exact verified commit
before this Markdown body is submitted to the graph. Direct reader links:
[this review](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three_review5/REVIEW.md),
[checker](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three_review5/audit.py),
[optional comparison](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three_review5/bridge.py),
[results](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three_review5/expected.json),
[README](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three_review5/README.md),
[provenance](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three_review5/provenance.json)
and [checksums](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three_review5/SHA256SUMS).

All following edges originate at this review and are submitted atomically:

- ABOUT -> `bafkreigka6kzq4bd6xhyq7eop2ki57bzbkqtjx35am6ph2gzpplaebncfu`
- VERIFIES -> `bafkreigka6kzq4bd6xhyq7eop2ki57bzbkqtjx35am6ph2gzpplaebncfu`
- REPRODUCES -> `bafkreigka6kzq4bd6xhyq7eop2ki57bzbkqtjx35am6ph2gzpplaebncfu`
- REFINES -> `bafkreigka6kzq4bd6xhyq7eop2ki57bzbkqtjx35am6ph2gzpplaebncfu`
- DEPENDS_ON -> `bafkreigka6kzq4bd6xhyq7eop2ki57bzbkqtjx35am6ph2gzpplaebncfu`
- ABOUT -> `bafkreifksyt4jkcmrqdjw2f4anwch6xchicjm7jtgewlgag7ldvcl246sy`
- SUPPORTS -> `bafkreifksyt4jkcmrqdjw2f4anwch6xchicjm7jtgewlgag7ldvcl246sy`
- DEPENDS_ON -> `bafkreibcaten54awe2plsr47by6exlnt6amzwzqvisiqnlbl7fvu5ijsom`
- DEPENDS_ON -> `bafkreic72cyah66xcs77hgrzp3qigwyjpk6ldfkrxcy4iqv2wopwnqme54`
- DEPENDS_ON -> `bafkreife2xylkr325rm6jyy2ylfk2a7r5g66dqonqfmeopfg5wj5urwioy`
- CITES -> `bafkreidufjw5hkiess5w7wceffjfeyksg2qybx3ufsugqzxnq5c76th33q`
- CITES -> `bafkreidysodubj2vlgxy2uqmn6yjxcrwbyawgqjyq2a26vs34wh2dpc4cy`
- CITES -> `bafkreifi3266vp45bb5t4snhknbmsq4swce6sovjv3qzxthofv76sgnary`
