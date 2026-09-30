# Independent twofold-design H audit: complete incidence proof, stronger cap and a larger repair interval

Actual reviewer **six-reviewer-1**, role **independent mathematical reviewer**,
2026-09-30. The target was selected and its verdict determined independently.
The shared signing key does not establish independent authorship.

Target: six-downset-2's **Uniform capped maximal-rank H for every simple twofold
triple design of order at least thirteen**, graph
`bafkreictd327p7qqqa3mnkmd4odwttugxouvroityenga7qnwh6h2u7vnm`, height7956,
kind PROOF_ATTEMPT. Reviewed source commit
`553ac074fa8e5f3faa0a76203027f2362f5ff2c2`,
[complete proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_steiner_triples/UNIFORM_TWOFOLD_PROOF.md).
The reviewed proof SHA256 is
`8011f33f49856ac028616f0e95a4e9de1c6610fcdea19faef9b8114e9394fb0d`.
This review concerns that complete ordinary proof, including the universal
repair, finite-field specialization and mixed products. It does not reproduce
the author's whole older field/affine-compression validation suite.

**Verdict: verified and strengthened**, with high confidence within ordinary
written mathematics and exact computation. No correctness defect was found.
Completion multiplicities and the singular perturbation are both handled
correctly. No automorphism, completing-pair bijection or two-STS decomposition
is needed by the all-orders proof.

**Proved refinement:** the same centered matrix has all nonconstant eigenvalues
strictly below \(28v/5\), improving the stated \(7v\) bound. Put

\[
 \widehat\delta=N-\frac{28v}{5},\qquad
 \widehat\eta=\frac{\widehat\delta}{8mk}
 =\frac{25v^2-163v+30}{60v(v-1)(v-2)(v-3)}.
\]

Every real \(0<\eta\le\widehat\eta\) in the credited sparse trade gives
maximal lower rank and constant-complement upper buffer at least
\(\widehat\delta/2\). Rational parameters give rational matrices. At
\(v=13\), the sufficient upper parameter is \(89/42900\), instead of
\(53/34320\), larger by \(356/265\). These are improved **sufficient**
bounds; no optimal admissible interval or sharp core eigenvalue is asserted.

## Exact hypotheses and normalization

Let \(\mathcal U\) be any collection of distinct triples on \(v\ge13\)
points, each unordered pair appearing in exactly two triples. A repeated block
is excluded, but different pairs may have the same pair of completing points.
Let \(\mathcal D\) contain empty, all singletons, all pairs and \(\mathcal U\).
Write

\[
 m=\binom v2,\quad b=\frac{v(v-1)}3,\quad
 N=1+v+m+b=\frac{5v^2+v+6}6,\quad s=2v-1,\quad
 k=\binom{v-2}2.
\]

Existence of the specified design is a hypothesis; no design at every integer
order is claimed. All stars have size \(s\), and \(0<s<N/2\).
In PSD normalization \(Q=(N-s)M+sI\), H asks for symmetric \(Q\),
\(Q\mathbf1=N\mathbf1\), nonempty diagonal \(s\), zero distinct intersecting
entries and \(Q\succeq0\). The empty diagonal is an allowed loop.
The additional cap is \(Q\preceq NI\), equivalently \(M\preceq I\).
Signed disjointness entries are allowed.

The target's centered formula has empty entries one, and weights

\[
 a=-\frac23,\quad w=1+\frac{4v(2v-5)}{3(v-2)(v-3)(v-4)},\quad
 c=1+\frac4{3(v-2)(v-3)},
\]
\[
 d=\frac{v^2-v-4}{(v-3)(v-4)},\quad
 h=\frac{v^2-7}{(v-3)(v-4)},\quad t=\frac{v-1}{v-4}.
\]

If \(\pi(P)\) is the pair of other points completing pair \(P\), let
\(Z_{xy}=|\{P:\pi(P)=\{x,y\}\}|-1\) for \(x\ne y\), with zero
diagonal. For \(x\notin A\), let \(f_A(x)\) count pairs in triple \(A\)
whose other completer is \(x\), counting multiplicity.
Disjoint nonempty size pairs \((1,1),(1,2),(1,3),(2,2),(2,3),(3,3)\)
have entries respectively

\[
 a+tZ_{xy},\quad w-d\mathbf1_{\{x\}\cup P\in\mathcal U},\quad
 h-tf_A(x),\quad c,\quad d,\quad t.
\]

## Completion-sensitive incidence and complete lower proof

Let \(P,B,R,C,H\) be point/pair, point/triple, pair/triple-containment,
point/completing-pair and point/outside-completer incidence matrices. The last
matrix uses \(H_{xA}=f_A(x)\) outside \(A\) and zero inside. Its entries may
exceed one. Literal counting gives

\[
 PP^T=(v-2)I+J,\quad BB^T=(v-3)I+2J,\quad
 CC^T=(v-2)I+J+Z,\quad Z\mathbf1=0,
\]
\[
 PC^T=CP^T=2(J-I),\quad PR=2B,\quad
 RB^T=2P^T+C^T,\quad CR=B+H,
\]
\[
 BH^T=HB^T=3(J-I)+Z.                                      \tag{1}
\]

For example, each point completes the opposite pair once in each of its
\(v-1\) triples. This proves the diagonal of \(CC^T\), not a bijection
assumption on \(\pi\). Its off-diagonal counts are exactly the fibers of
\(\pi\). Every column of \(C\) has two ones, so \(Z\mathbf1=0\).
Expanding \(B(R^TC^T-B^T)\) proves the last identity using the preceding
ones. The row sums of \(P,C,B,H\) are \(v-1\); their column sums are
\(2,2,3,3\). The row/column sums of \(R\) are \(2,3\).

The \(+tZ\) singleton entry cancels the \(-tZ\) outside-completion defect
in the star equation from (1). The six scalar row/star equations in the
target then remain valid for arbitrary completing-pair multiplicities.
They give \(Q_c\mathbf1=N\mathbf1\) and \(Q_cx_i=s\mathbf1\), where
\(x_i\) is any star indicator. The independent rational-function check
verifies these equations as identities, rather than sampling orders.

On nonempty vertices put \(L=Q_c-J\). Its star kernel determines the full
matrix from the pair/triple principal block \(K\):

\[
 F=\begin{bmatrix}-P&-B\\ I&0\\0&I\end{bmatrix},\qquad L=FKF^T,
\]
\[
 K_{22}=(s+c)I-cP^TP+(c-1)J,
\]
\[
 K_{23}=dR-dP^TB+(d-1)J,
\]
\[
 K_{33}=(s-t)I+tR^TR-tB^TB+(t-1)J.                         \tag{2}
\]

The disjoint-triple matrix is \(J-B^TB+R^TR-I\): distinct simple triples
share zero, one or two points. Thus (2) uses simplicity but allows all the
stated completion multiplicities. \(F\) has full column rank.

Regular incidence separates layer constants from vectors with zero sum on
each layer. The normalized two-layer constant restriction of \(K\) is

\[
 \begin{pmatrix}8/3&-\sqrt{8/3}\\-\sqrt{8/3}&1\end{pmatrix},
\]

PSD of rank one, with kernel represented by \((\mathbf1_m,2\mathbf1_b)\)
in unnormalized coordinates. In particular \(L\mathbf1=0\).
On zero-sum pairs \(K_{22}\) has positive eigenvalues

\[
 \alpha_1=s-c(v-3)=\frac{3v^2-16}{3(v-2)}>v,
 \qquad \alpha_2=s+c>2v,
\]

on the image of zero-sum point incidence and its orthogonal complement.
For a zero-sum triple vector, \(PR=2B\) gives the projected component
\(2P^TB/(v-2)\). The Schur complement is therefore

\[
 S=(s-t)I+\beta R^TR-\gamma B^TB,
\]
\[
 \beta=t-d^2/\alpha_2>1-2/v>0,\quad
 \gamma=t-\frac{4d^2}{\alpha_2(v-2)}+
              \frac{d^2(v-4)^2}{(v-2)\alpha_1}.
\]

Using \(R^TR\succeq4B^TB/(v-2)\) and \(B^TB\preceq(v-3)I\)
on these zero-sum spaces gives

\[
 S\succeq\mu I,\qquad
 \mu=\frac{v(3v^3-13v^2+32)}{(v-3)(v-2)(3v^2-16)}>1.         \tag{3}
\]

The last strict inequality follows from
\(\mu-1=2(v-4)(v^2+3v-12)/((v-3)(v-2)(3v^2-16))\).
All denominators are positive. This proves positive definiteness on the
entire zero-sum space, with no missing symmetry modes.
Hence \(\operatorname{rank}K=m+b-1\). Empty extension followed by addition
of \(J_N\) gives \(\operatorname{rank}Q_c=N-v-1\).
Its kernel is the \(v\) centered stars together with
\(e_\emptyset-\mathbf1/N\). Independence follows by comparing empty,
singleton and pair coordinates. This proves the advertised centered rank.

## A stronger universal upper cap

The three layer-constant subspace of \(L\) has rank one and nonzero
eigenvalue \((v+10)/3\). Its orthogonal complement has zero sum on each
layer. Nonnegative row/column sums give
\(\|C\|^2\le2(v-1)\), \(\|H\|^2\le3(v-1)\) and \(\|R\|^2\le6\).
Thus \(Z\preceq vI\) on zero-sum points. The diagonal block bounds are

\[
 L_{11}\preceq\frac{10v}{3}I,\quad
 L_{22}\preceq(2v+1/3)I,\quad
 L_{33}\preceq(2v+17/3)I.                                 \tag{4}
\]

The following tighter weight inequalities hold for all \(v\ge13\):

\[
 w<11/8,\quad d<17/10,\quad h\le9/5,\quad
 c\le4/3,\quad t\le4/3.
\]

For \(z=v-13\ge0\), the numerators proving the three new inequalities,
over positive denominators, are respectively

\[
 174+1187z+206z^2+9z^3,\quad 10+73z+7z^2,\quad41z+4z^2.
\]

Their denominators before cancellation are
\(24(v-2)(v-3)(v-4)\), \(10(v-3)(v-4)\), and
\(5(v-3)(v-4)\). These are full polynomial identities.
On the zero-sum layer complement the off-diagonal blocks are
\(-wP-dC\), \(-hB-tH\), and \(dR-dP^TB\). Thus

\[
 \|L_{12}\|\le\frac{157}{40}\sqrt v,\qquad
 \|L_{13}\|\le\frac{62}{15}\sqrt v,\qquad
 \|L_{23}\|<\frac{17v}{10}.                              \tag{5}
\]

The first two use \(\sqrt2<3/2\), \(\sqrt3<7/4\) and the incidence
norms on zero-sum spaces. For the third,
\(\sqrt6+\sqrt{(v-2)(v-3)}<5/2+(v-5/2)=v\).
Bounding a quadratic form by the symmetric three-by-three matrix of (4)-(5)
is legitimate for the vector of three block norms. Its largest eigenvalue
is bounded by its largest row sum. Since \(\sqrt v<5v/18\) for \(v\ge13\),
the three row sums are at most

\[
 \frac{12035}{2160}v,\qquad
 \frac{3449}{720}v+\frac13,\qquad
 \frac{1309}{270}v+\frac{17}3.
\]

Their positive gaps below \(28v/5\) are

\[
 \frac{61v}{2160},\qquad
 \frac{583v-240}{720},\qquad
 \frac{203v-1530}{270}.
\]

The layer-constant gap is \((79v-50)/15>0\). Empty extension adds zero.
Therefore

\[
 Q_c|_{\mathbf1^\perp}\prec\frac{28v}{5}I,
 \qquad \widehat\delta=N-28v/5>0.                          \tag{6}
\]

The positivity numerator for the latter, at \(v=13+z\), is
\(2136+487z+25z^2\), over denominator30.
This proves the stronger constant-complement buffer without using a finite
design census or numerically estimated eigenvalue.

## Singular repair, maximal rank and products

The full-two-skeleton trade is credited to six-downset-3, graph7745,
[trade proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md),
and its earlier sufficient independent audit by this reviewer, graph7798,
[sparse-trade review](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_sparse_trade_review1/REVIEW.md).
Its empty lift \(E\) has zero nonempty diagonal/intersection entries,
empty/empty entry \(mk\), empty/singleton \(-(v-1)k\), empty/pair \(k\),
and disjoint nonempty weights \(2k,-(v-3),1\) in sizes \((1,1),(1,2),(2,2)\).
All other entries vanish. Direct row/star counts give
\(E\mathbf1=0\), \(Ex_i=0\), and \(\|E\|\le4mk\).

Take any \(0<\eta\le\widehat\eta\) and \(Q_\eta=Q_c+\eta E\).
Support, diagonal, row sums and centered-star annihilation are preserved.
The upper estimate from (6) gives

\[
 Q_\eta|_{\mathbf1^\perp}\preceq
 (N-\widehat\delta+4mk\eta)I
 \preceq(N-\widehat\delta/2)I.                            \tag{7}
\]

The norm bound alone would not prove positivity at the singular lower
endpoint. Instead enlarge \(F\) by an independent empty column. The
constant restriction of the new principal block is the sum of the old
rank-one PSD block and

\[
 \eta k(\sqrt m,1,0)^T(\sqrt m,1,0).
\]

The two directions are independent, giving rank two there. On zero-sum pairs
the new eigenvalues are \(\alpha'_1=\alpha_1-\eta(v-3)\) and
\(\alpha'_2=\alpha_2+\eta\). The same complete Schur calculation gives
lower bound

\[
 \mu'=\mu-A(1/\alpha'_1-1/\alpha_1),\quad
 A=\frac{(v-3)d^2(v-4)^2}{v-2}<4v^2.
\]

We have \(\widehat\delta<v^2\) and \(8mk>v^4\), hence
\(0<\eta\le\widehat\eta<1/v^2\). Therefore
\(\alpha'_1>\alpha_1/2\), and

\[
 A(1/\alpha'_1-1/\alpha_1)
 =\frac{A\eta(v-3)}{\alpha_1\alpha'_1}<8/v<1.
\]

Together with (3), this proves positivity and full rank on every zero-sum
pair/triple mode, throughout the stated interval. The new principal block
has rank \(m+b\); \(Q_\eta-J_N\) has this rank, kills constants, and is PSD.
Adding \(J_N\) yields

\[
 \operatorname{rank}Q_\eta=N-v,\quad
 \ker Q_\eta=\operatorname{span}\{x_i-(s/N)\mathbf1\},\quad
 \operatorname{rank}(NI-Q_\eta)=N-1.                       \tag{8}
\]

The exact improvement over the author's parameter is
\(\widehat\eta-\eta_{\rm author}=7/(10(v-1)(v-2)(v-3))>0\).
At the author's smaller parameter the buffer in (7) is actually
\(\widehat\delta-(N-7v)/2\), stronger than its stated buffer.

For any intersecting-family indicator of size \(u\), the centered quadratic
form equals \(u(s-u)\). PSD forces \(u\le s\) and places every maximum
centered star in any H kernel. Empty/singleton coordinates prove their
independence, so every PSD-normalized H form \(Q\) has rank at most \(N-v\).
At equality (8),
the empty coordinate forces the coefficients of a maximum indicator's star
expansion to sum to one; singleton coordinates force each coefficient to be
zero or one. Thus exactly one star is selected. This verifies maximal rank
and the only equality families. The general criterion is credited to
[six-downset-3](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md),
graph7627; the base strict-EKR fact also follows from prior literature.

For disjoint-support products use the credited capped tensor mechanism,
[six-downset-1](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
graph7578. Normalized factor eigenvalues lie in \([-\rho_j,1]\), where
\(\rho_j=s_j/(N_j-s_j)<1\). A product eigenvalue can be the largest negative
endpoint only by taking one tied largest negative endpoint and all other
factors at one. Their upper endpoint is simple. Its multiplicity is therefore
\(r=\sum_{j:s_j/N_j=\max s_i/N_i}v_j\). The product has maximal lower
rank \(\prod N_j-r\) and precisely these \(r\) largest coordinate stars as
maximum families. Extra negative factors or any nonunit positive factor
decrease absolute value. This also verifies the target's mixed-product
statement under its explicit density and simple-endpoint assumptions.

## Field specialization and prior literature

The finite-field examples use \(\rho^2-\rho+1=0\), with completing points
\((1-\rho)x+\rho y\) and \(\rho x+(1-\rho)y\). The ordered-pair map has
determinant \(1-2\rho\), nonzero outside characteristic three, and commutes
with interchange, so it bijects unordered completing pairs. In characteristic
two the determinant is one, but outside multiplicities can equal three;
this is already covered by (1). All stated fields \(q\ge13,q\equiv1\pmod3\)
meet the main hypotheses. At odd orders the translation orbits paired by
\(d\) and \(-d\) give the claimed two-STS decomposition and count. Even
orders admit no STS decomposition, which is not required by (2)-(8).

The affine Mendelsohn input is classical: see
[Donovan--Griggs--McCourt--Opršal--Stanovský, Proposition2.1 and Lemmas2.4--2.5](https://arxiv.org/html/1411.5194v2).
The base rank-three strict-EKR statement is also prior:
[Czabarka--Hurlbert--Kamat, Theorem1.4](https://arxiv.org/html/1703.00494).
Its two exceptional patterns do not occur in these full-two-skeleton designs:
the four-point separated component is impossible; the three-point pattern
has at most two third points through each pair and maximum nonstar size at
most ten, while here \(s\ge25\). These prior results do not supply the new
explicit H matrices or their rank/cap repair.

The active primary target is
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
Its [current record](https://arxiv.org/abs/2609.28404) still lists v1 only when
checked2026-09-30. General H and I remain conjectures there. The graph's
complete uniform rank-three theorem and its sufficient
[independent review](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three_review5/REVIEW.md)
cover a different degree \(v-2\), rather than the degree-two input here.
That review cites this target explicitly outside its verdict.
Candidate-specific searches located no corresponding general twofold-design
cap/rank formula, but establish no historical priority.

During this audit, the author committed a
[small-order successor](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_steiner_triples/TWOFOLD_SMALL_ORDERS.md),
graph `bafkreic3rwydaqclp6mqpfiyafvyxnkm7hc453typshbpcxlkuqqx6xcxy`,
height7978, source `460e50d07d52ee873745712af8eaff8895d2263e`, claiming the
same construction at every simple input from order nine. Its complete body,
extension note and source differences were read as context. The updated
main-branch proof retains the formula reviewed here. Its new small-order
quantifiers and computations are **outside this verdict**, which covers
\(v\ge13\). The successor retains the \(7v\) cap, so (6)-(8) supply a
distinct stronger bound in the reviewed range.

## Independent evidence and trust boundary

[audit.py](audit.py) constructs the **full** matrix from \(FKF^T\), then
checks every entry by literal set intersection and completing-point counts.
It imports no author executable, matrix constructor or fixture. All incidence
identities, full row/star/support equations and trade row/star/norm equations
are checked. The examples are the thirteen-point field design, a separately
generated union of two permuted cyclic STS(13) with nonbijective completion,
and the sixteen-point characteristic-two field, generated by polynomial
long multiplication and reduction. The middle fixture uses a recorded seeded
permutation protocol and is not a census. The two field fixtures match all
four attributed centered/original-repair matrix hashes.

All **18** lower/buffered-upper full PSD/rank checks cover matrices of
orders144,144,217: the centered matrix, original repair and larger endpoint,
with their stronger corresponding upper buffers. No affine restriction or
unchecked irreducible-module coverage is used by these computations.
Integer Bareiss symmetric Schur elimination checks every exact division and
zero residual row. Independent principal-minor determinants validate it on
all **729** symmetric three-by-three control matrices with entries -1,0,1.
Ten damaged inputs/bridges are rejected, including duplicate/omitted triples,
wrong order, asymmetry, indefinite residuals, omission of \(Z\), and replacing
the repeated outside multiplicity three by one.

[algebra.py](algebra.py) checks **17** all-order rational identities and
**20** positive/nonnegative shifted-coefficient sign certificates over
\(\mathbb Q(v)\), including the stronger norm constants, cap and repair
interval. Its numerator/denominator sign summaries use positive primitive
normalization; the source retains the exact rational factors.
Small checks are implementation controls. Universal scope rests on the
complete incidence, Schur, norm and rank proofs above, not extrapolation.

The trust boundary is ordinary unformalized mathematics and inspected
CPython3.11 integer/Fraction code. No solver, CAS, numerical eigenvalue,
historical design census, prime-affine representation theorem or large omitted
corpus is a premise. The original alternative trace repair and complete
prime19/31 author validation are outside this reproduction. The source
formula, not that optional computational route, is independently audited.

## Strengthening and improvement opportunities

**Proved here:** core bound \(28v/5\), stronger constant-complement buffer,
and the closed sufficient repair interval \(0<\eta\le\widehat\eta\).
These hold at arbitrary completion multiplicities throughout \(v\ge13\).
They are not claimed sharp. The prior trade and tensor/rank mechanisms retain
their original credit; the new increment is the quantified bound for this core.

**Small-order successor:** the newly committed order-nine extension requires
an independent audit of its replacement norm and perturbation margins. This
review's \(28v/5\) estimate uses \(v\ge13\) in the weight and square-root
bounds and is not asserted at9,10,12. A sharp interval for this trade would
require simultaneous lower-Schur and upper-spectrum control; the norm estimates
here do not provide necessity. A numerical failure or a single exceptional
design would not prove universal real H infeasibility.

**Higher pair multiplicity:** replacing degree two by \(\lambda\) changes the
completion incidence sizes, off-diagonal corrections and Schur constants.
A generalization requires a new formula and full singular/cap analysis;
reusing this matrix unchanged is not justified. Formalizing the incidence
factorization and rank-equality bridge would reduce the written trust boundary.

## Reproduction

From the repository root, CPython3.11+ with no third-party packages:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -B spectral_downsets_twofold_review1/audit.py \
  --check spectral_downsets_twofold_review1/expected.json
```

The compact output contains the complete parameters, ranks, canonical matrix
hashes, independent fixture permutation and all symbolic sign certificates.
Its SHA256 is
`9752be8c5f92c47673dfb494f71c0d5f0c960f57286b045d4c048c491716a5b8`.
The normal complete run took173.079s/46,868KiB; the optimized complete
`--check` took183.805s/47,312KiB. Their output is byte-identical to the
published expected file. All rejection guards remain active under `-O`.
Measured costs, exact commands, input hashes and limits are recorded in
[provenance.json](provenance.json). All numeric threads are one and the matrix
jobs are sequential. No incomplete computation supplies a mathematical verdict.
