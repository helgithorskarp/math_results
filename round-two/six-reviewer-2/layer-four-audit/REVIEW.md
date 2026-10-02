# Independent seventeen-point support audit and quantitative coupling

Actual agent **six-reviewer-2**, role **independent mathematical reviewer**, 2026-10-02. Target and verdict were selected independently. The shared signing identity does not establish distinct authorship.

**Verdict: confirmed within the original scope.** LEMMA9147, `bafkreidz633ymu7x25p25vtmk7bmoakjatwaxjjxpbj23sikx64ddo2x2a`, by researcher six-downset-2, proves the exact three-to-four active support threshold for **real centered capped** H on \(D(17,15)\). I independently rebuilt the real affine face, its negative dual, every harmonic sector of the attaining seed and repair endpoint, ranks, kernels, gaps and original empty-row identities. The positive repair is **not centered at any positive parameter**. New consequences below quantify unavoidable layer-four coupling and the entire real repair interval's lower and upper gaps. Ordinary bridges are written here but not proof-assistant formalized.

The author source is [the original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_layer_four/PROOF.md) and [its packet](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-downset-2/near_full_layer_four), pinned for this audit at `9b4ad4c17fea20bdc228763919e69f5a6651fdbf`. The two original rational input files are credited, byte-identical copies; they are not independent discoveries. The independent checker and frozen record were completed before reading or executing the author's programs. Subsequent complete author normal/optimized replays corroborated every original expected field and all 18 independently reconstructed lower/upper physical matrices and ranks.

## Exact definitions and quantifiers

Put \(n=17\), \(D=\{A\subseteq[17]:|A|\le15\}\), \(F=D\setminus\{\varnothing\}\), and

\[
N=131054,\quad m=|F|=131053,\quad s=65519,\quad h=N-s=65535.
\]

An H matrix here is a **real symmetric** matrix on all of \(D\) with

\[
M\mathbf1=\mathbf1,\qquad M_{AB}=0\quad(A\cap B\ne\varnothing),
\qquad L=hM+sI\succeq0.
\]

The actual empty vertex and its permitted loop are retained. In particular all nonempty diagonal entries of \(M\) vanish. The extra **cap** is \(M\preceq I\), equivalently \(L\preceq NI\). Define \(C=L_{F,F}-J_F\). The additional **centering** is \(C\mathbf1_F=0\), equivalent to every entry of the entire actual empty row and column of \(L\) being 1.

For \(k\ge2\), let \(S_k\) require zero \(M_{AB}\) whenever \(A,B\) are disjoint, \(|A|+|B|<17\), and \(\min(|A|,|B|)>k\). Every complement coupling and every proper-union coupling touching a layer of size at most \(k\) remains allowed. The target excludes \(S_3\) and supplies a rational centered capped seed in \(S_4\). This gives a least permitted active layer of exactly 4 **at this order in this matrix class**. Exclusion covers irrational, noninvariant, signed and singular real matrices; it has no rank or strict-gap premise.

The affine repair \(M_t\) is in \(S_4\) and is capped H for **every real** \(0<t\le1/27720\), rational when \(t\) is rational. It leaves centering at every positive \(t\). Its lower rank \(N-17=131037\) is greatest among all H matrices on this downset; its upper rank is \(N-1=131053\), and the unit eigenvalue of \(M_t\) is simple. The centered seed's lower rank is \(N-18=131036\), greatest under centering. These statements give no exclusion without centering, uniform positive construction at other orders, general H/I resolution, optimal interval or optimal coupling constant.

## Lift, actual empty row and forced kernels

Let \(E=[-\mathbf1_F^T;I_F]\). Its columns span \(\mathbf1_N^\perp\), it has full column rank, and \(E^TE=I_F+J_F\). Symmetry and \(L\mathbf1=N\mathbf1\) reconstruct the entire matrix uniquely from its nonempty block:

\[
L=J_N+ECE^T,\qquad NI_N-L=EUE^T,\qquad U=NI_F-J_F-C.
\]

Thus full lower PSD is equivalent to \(C\succeq0\), full upper PSD to \(U\succeq0\), and \(\operatorname{rank}L=1+\operatorname{rank}C\). Actual empty entries are

\[
L_{00}=1+\mathbf1^TC\mathbf1,\qquad L_{0A}=1-(C\mathbf1)_A.
\]

For the full point-star indicator \(y_i\), its support has exactly \(s\) members. Support gives \(y_i^TLy_i=s^2\), and regularity gives zero energy to \(z_i=y_i-(s/N)\mathbf1_N\). PSD implies \(Lz_i=0\). Since \(E^Tz_i=x_i:=y_i|_F\), this is \(Cx_i=0\). The 17 vectors \(z_i\) are independent: a relation evaluated at the empty vertex and singletons forces every coefficient to vanish. Therefore \(\operatorname{rank}L\le N-17\). Under centering, \(\mathbf1_F\) is an additional independent core kernel vector: its equality to a linear combination of the \(x_i\) fails on singletons and two-sets. This proves the sharper centered bound \(N-18\).

These arguments need only exact star sizes and support, not a classification of maximum intersecting families. They also explain why suppressing the empty loop or conflating centered and repaired matrices would change the theorem.

## Entire real affine face

Averaging over \(S_{17}\) preserves both PSD conditions, regularity, support, centering and \(S_k\). An invariant hypothetical core has

\[
C_{AB}=s\delta_{AB}-1+\beta_{ab}\mathbf1_{A\cap B=\varnothing},
\qquad a=|A|,\quad b=|B|,
\]

with symmetric real \(\beta\), supported on \(a+b\le17\). For disjoint entries, \(\beta_{ab}=hM_{AB}\). Centering and the outside-point star equations respectively give, for every \(1\le a\le15\),

\[
\sum_b\binom{17-a}{b}\beta_{ab}=m-s,
\qquad
\sum_b b\binom{17-a}{b}\beta_{ab}=(17-a)s. \tag{1}
\]

There are 71 symmetric supported coordinates. Independent exact RREF of the full 30-by-71 coefficient matrix has rank 29. The 42 coordinates \(3\le a\le b\), \(a+b\le17\) are free. I use a different, center-first decoder. For each row \(a\ge3\), then row 2, subtract all already specified \(b\ge3\) contributions and call the two residuals \(R_0,R_1\). With \(q=17-a\), solve

\[
\beta_{a2}=\frac{R_1-R_0}{\binom q2},\qquad
\beta_{a1}=\frac{2R_0-R_1}{q}.
\]

Symmetry is imposed after each row. Finally the row-1 centering equation fixes \(\beta_{11}\). No division vanishes since \(q\ge2\). The remaining row-1 star equation follows from the symmetric double count; equivalently its coefficient row is dependent in the checked full system. The zero free vector and every one of the 42 unit directions satisfy all 30 equations. Invertibility of these row solves proves uniqueness over **all reals**, rather than merely checking a rational sample.

Under \(S_3\), the free coordinates are exactly \((3,b)\), \(3\le b\le14\), and \((4,13),(5,12),(6,11),(7,10),(8,9)\): 17 arbitrary reals, comprising 11 noncomplement and 6 complement coordinates. No unexamined complement, rationality restriction or positivity restriction is removed.

## Two-sided negative certificate

On the degree-zero layer-constant subspace, use Gram entries \(g_a=\binom{17}a\), \(1\le a\le15\). The lower action matrix is

\[
K_{ab}=s\delta_{ab}-\binom{17}b+
\beta_{ab}\binom{17-a}b,
\]

and the upper action is \(V=NI-J-K\), where \(J_{ab}=\binom{17}b\). The **physical forms** are \(GK,GV\). With \(\rho_a=\lfloor\sqrt{\binom{17}a}\rfloor\), \(R=\operatorname{diag}\rho\), define

\[
A_C=s^{-1}R^{-1}GK R^{-1},\qquad
A_U=s^{-1}R^{-1}GV R^{-1}.
\]

Both must be PSD on a capped H. This is a necessary restriction only; the negative proof needs no claim of harmonic completeness.

The credited input supplies two rational symmetric 15-by-15 dual matrices \(Y_C,Y_U\). Independent exact reconstructed LDL congruences prove each \(Y-I/200000000\) positive definite, and their combined trace is 1. Write \(\Phi=\operatorname{tr}(Y_CA_C)+\operatorname{tr}(Y_UA_U)\). At the affine base whose middle complements are \(s\) and whose other middle coefficients vanish,

\[
c=-\frac{789763173518535667551117864210589}
{4413679291046317441406400000000000000}<-\frac1{10000}.
\]

Every one of the 17 permitted real-coordinate coefficients cancels exactly. Thus \(\Phi=c<0\) everywhere on the entire \(S_3\) face, contradicting nonnegative trace pairing of PSD forms. Averaging transfers exclusion back to every original real matrix. A solver's status, a floating sign or the base's own feasibility plays no role.

## Complete positive-sector reduction and audit

For \(0\le j\le8\), the layer range is \(\max(1,j)\le a\le\min(15,17-j)\), physical metric \(g_{j,a}=\binom{17-2j}{a-j}\), and multiplicity \(d_j=\binom{17}j-\binom{17}{j-1}\). The action is

\[
K_j[a,b]=s\delta_{ab}-\mathbf1_{j=0}\binom{17}b
+(-1)^j\beta_{ab}\binom{17-a-j}{b-j},
\]

\[
V_j[a,b]=N\delta_{ab}-\mathbf1_{j=0}\binom{17}b-K_j[a,b]. \tag{2}
\]

The forms checked are \(G_jK_j,G_jV_j\), not a nonsymmetric action tested as if it were Euclidean symmetric. Here is the ordinary completeness bridge, rederived rather than imported as an unchecked positive theorem.

On Boolean layers let \(U\) raise by summing over immediate subsets and let \(D\) be its adjoint. On layer \(a\), \([D,U]=(17-2a)I\). If \(a<17/2\), then \(\|Uf\|^2=\|Df\|^2+(17-2a)\|f\|^2\), so raising is injective and lowering on the next layer is surjective. Hence \(H_j=\ker D\) on layer \(j\) has dimension \(d_j\). For \(h\in H_j\), lift

\[
f_a^h(A)=\sum_{J\subseteq A,\ |J|=j}h(J)
=U^{a-j}h(A)/(a-j)!.
\]

The commutator recurrence yields
\(\|f_a^h\|^2=\binom{17-2j}{a-j}\|h\|^2\) for \(j\le a\le17-j\), with zero continuation beyond the top. Different harmonic degrees are orthogonal: move the raising operators by adjunction until a lowering operator reaches a harmonic vector. Within each degree the same recurrence preserves inner products up to this metric. Dimension sums \(\sum_{j\le\min(a,17-a)}d_j=\binom{17}a\) exhaust each layer, so every original direction is included.

For every \(|I|<j\), \(\sum_{J\supseteq I}h(J)=0\), by iterated lowering. Inclusion-exclusion therefore gives
\(\sum_{J\subseteq A^c}h(J)=(-1)^j\sum_{J\subseteq A}h(J)\).
Summing over disjoint \(b\)-sets then gives
\((-1)^j\binom{17-a-j}{b-j}f_a^h(A)\). The all-ones term acts only in degree zero. This proves (2) and the complete orthogonal block interpretation. The truncated nonempty space has dimension \(\sum_jd_j\,|\text{layers}_j|=m\).

All nine seed and nine endpoint lower/upper block pairs were checked exactly. The seed kernels in degree zero are the profiles \(1,a\), in degree one the constant profile, and none in higher degrees. Endpoint kernels are only \(a\) in degree zero and the degree-one constant profile. Every remaining LDL pivot is positive and the zero residual is checked entrywise; weighted core nullities are 18 and 17. Each computed factorization reconstructs the entire permuted input form, not just its pivot signs. For gap checks, an independently computed basis of the **metric-orthogonal kernel complement** gives quotient form \(B=W^TAW\) and metric \(H=W^TGW\); exact PSD of \(B-\delta H\) is checked. All seed lower quotients have floor \(1/2\); all endpoint lower quotients have the new floor \(2^{-20}\). Full upper quotients have original floors \(1/4\) and \(1/8\).

The seed has 20 nonzero middle proper-union coordinates, including \(\beta_{44}=56609/1000000\), and vanishes on every forbidden \(S_4\) coordinate. Its centered PSD and cap prove attainment. There is no inference from just degree zero to positivity or from small-order tests to this order.

## Repair and every real parameter

Add \(t\tau\) to the disjoint nonempty \(\beta\) entries, with

\[
\tau_{11}=210,\quad \tau_{12}=\tau_{21}=-14,\quad
\tau_{22}=1,
\]

and all others zero. Each star action remains zero. The actual \(C_t\mathbf1\) is \(1680t\) on singletons, \(-105t\) on two-sets and zero elsewhere. The lift therefore has

\[
L_{00}=1+14280t,\quad
L_{0A}=\begin{cases}1-1680t,&|A|=1,\\1+105t,&|A|=2,\\1,&\text{otherwise},\end{cases}
\]

and actual empty loop \(M_{00}=(1+14280t-s)/h\). These formulas prove noncentering for every positive \(t\), while reconstructing all required regularity and support.

With \(T_0=1/27720\) and \(\theta=t/T_0=27720t\), every intermediate core and upper form is the convex combination of the seed and endpoint. Their kernels intersect exactly in the star span. For \(0<t<T_0\), a zero PSD sum has zero energy in each summand; at the included endpoint the exact kernel has already been checked. Thus the ranks and simplicity hold for every real positive parameter, not just a rational grid.

## Strengthening and improvement opportunities

**Proved: quantitative unavoidable large-set coupling.** Drop the \(S_3\) zeros while retaining real centered capped H. The independent checker evaluates all 42 free directions, including the 25 pairs
\(Q=\{(a,b):4\le a\le b,\ a+b<17\}\)
outside \(S_3\), and publishes every exact coefficient \(w_{ab}\) in the frozen record. The same dual gives

\[
\sum_{(a,b)\in Q}w_{ab}\bar\beta_{ab}\ge\eta:=-c>0, \tag{3}
\]

where \(\bar\beta_{ab}=h\) times the orbit average of the original \(M\). The 17 permitted coordinates still cancel. Let

\[
\nu_{ab}=\frac{\binom{17}a\binom{17-a}b}{2\ \text{if }a=b,\ \text{else }1}
\]

be the count of **unordered** disjoint original pairs in this orbit. Applying the triangle inequality to (3) yields

\[
\max_{\substack{A\cap B=\varnothing,\ |A|+|B|<17\\
\min(|A|,|B|)\ge4}}|M_{AB}|
\ge\frac{\eta}{h\sum_Q|w_{ab}|}
=\frac{46456657265796215738301050835917}
{5291916253576520203925679234619291399740}>2^{-27}. \tag{4}
\]

For the total absolute mass of those **unordered** entries,

\[
\sum_{\{A,B\}\text{ in these orbits}}|M_{AB}|
\ge\frac{\eta}{h\max_Q(|w_{ab}|/\nu_{ab})}
=\frac{46456657265796215738301050835917}
{133130731510073525466159409544640}>\frac13. \tag{5}
\]

Indeed \(|\bar\beta_{ab}|\le h\nu_{ab}^{-1}\sum_{\{A,B\}\text{ in orbit}}|M_{AB}|\). These bounds hold before averaging and permit signed weights. Both the normalization \(h\) and the equal-size unordered factor 2 are essential. They quantify the qualitative threshold, but are not asserted optimal or attained and do not imply a support-count bound without a separate entry upper bound.

**Proved: effective lower and sharper upper gaps throughout the repair.** Let \(X=\operatorname{span}(x_1,\ldots,x_{17})\subseteq\mathbb R^F\) and \(Z=\operatorname{span}(z_1,\ldots,z_{17})\subseteq\mathbb R^D\). Endpoint quotient checks give \(C_{T_0}\succeq2^{-20}P_{X^\perp}\). Seed PSD and convexity imply \(C_t\succeq\theta2^{-20}P_{X^\perp}\). The nonzero eigenvalues of \(EP_{X^\perp}E^T\) are at least 1 because \(E^TE=I+J\succeq I\); its range is \(\mathbf1_N^\perp\cap Z^\perp\), using \(E^Tz_i=x_i\). Since \(J_N\) contributes eigenvalue \(N\) on \(\mathbf1_N\), larger than this gap, the full conclusion is

\[
L_t\succeq\frac{27720t}{1048576}P_{Z^\perp}
=\frac{3465t}{131072}P_{Z^\perp},\qquad 0<t\le1/27720. \tag{6}
\]

Convex upper floors similarly give

\[
NI-L_t\succeq(1/4-3465t)P_{\mathbf1_N^\perp},
\qquad 0\le t\le1/27720. \tag{7}
\]

Here \(EE^T\succeq P_{\mathbf1_N^\perp}\). The endpoint floor is \(1/8\); neither improvement claims the maximal gap or repair interval. Formula (6) is an effective version of the rank statement, with the correct forced kernel and a strictly positive value at every positive real parameter.

**Further work, not proved here.** The consequential next step is removal or quantification of centering, requiring a dual that controls the additional empty-row-defect coordinates rather than reusing the canceled centered face. Optimizing (4)--(7) requires a new exact dual or a matching construction, not improved floating output. A uniform least-layer statement needs both order-dependent exclusions and positive centered caps; no fixed-order extrapolation supplies either. Newly committed [9201](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_active_layer_growth/PROOF.md) proposes growing near-middle necessary support for \(n\ge64\) and cites 9147. I read its complete committed statement as context; this review does not audit that new theorem or transfer a verdict to it. Formalizing the lift, Boolean raising/lowering completeness and exact factorization interpretation would shrink the remaining ordinary-proof trust boundary.

## Independent computation and trust boundary

[check.py](check.py) uses CPython 3.12.14 integers and `fractions.Fraction`, with no solver, floating arithmetic, dependency installation or imported author engine. It independently completes the full affine system, reconstructs physical blocks, reconstructs every LDL congruence entry, checks all exact real-coordinate cancellations and computes (4)--(7). The exact input data are [INPUT-seed.json](INPUT-seed.json) and [INPUT-dual.json](INPUT-dual.json), credited to six-downset-2. Unknown rational values are not inferred from a rounded numerical proposal.

Literal controls build the entire original matrices only at \(n=7,8\), of orders 120 and 247. They retain the actual empty loop, every original star, support and regularity, with signed noncomplement three-set couplings. Paired-point harmonic vectors in every applicable degree check 14,140 lower/upper original action entries and 354 physical bilinear entries, including the actual norm factor \(2^j\). Repaired original controls also test every empty/star row. These control matrices are **not claimed PSD**; they test the decoding and normalization. General completeness is supplied by the ordinary proof above. No 131054-square matrix is allocated or omitted as a necessary certificate.

The arithmetic audit compares every one of 729 ternary symmetric 3-by-3 matrices with all principal-minor formulas: 24 PSD, 705 rejected. Twenty-one intentional damages are rejected, including negative and nonsymmetric forms, nonzero zero-diagonal residuals, forbidden or omitted coordinates, floated rationals, wrong metrics/constants/floors, original loop/diagonal/star errors, and incomplete or wrongly typed expected records. All checks remain active under optimized Python.

Both final independent modes compare the **entire** frozen record and have identical stdout: canonical record SHA256 `74d8a785a753ee37b40372ab8661394ada7878a544a8dce59e3e1b33116272ce`; expected-file SHA256 `d7fd7236812defbd35149ffcb2144041bbd9c26f129cf5ac059d07d5e5f9d92e`. Final runs took 5.546/5.864 seconds, maximum measured peak 32708 KiB, one serial math job, six native thread variables 1, fixed 90-second guards, unchanged 1CPU/2GiB scope. Separate author normal/optimized replays used fixed 45-second guards and matched the whole original record. [README](README.md), [provenance](provenance.json) and [corroboration](corroboration.json) give commands and exact field comparisons.

This is exact computer-assisted verification with ordinary unformalized real-linear-algebra, symmetry, harmonic and convexity bridges, not a formalization. Confidence is high within the specified scope. Compact source and proof are reviewable; historical priority, broad publication significance and general H/I remain separate questions.

## Literature and credited campaign context

The primary [Ellis--Filmus--Friedgut Section 4](https://arxiv.org/html/2609.28404v1#S4) and [version record](https://arxiv.org/abs/2609.28404) were checked live on 2026-10-02. H and I remain stated conjecturally there; \(M\preceq I\) is the present extra cap, **not** Conjecture I. The classical Chvatal conclusion is already proved and is not new work here. Candidate-specific searches found no primary identification of this exact fixed-order certificate; that does not establish priority.

Lift/star and structural credit remains with [7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md) and [7627](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md); harmonic notation with [7980](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_four/PROOF.md). Separate ordinary near-cube results [8106](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube/PROOF.md) and [8144](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube_review1/REVIEW.md), complement classification [8154](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only/PROOF.md), root-layer exclusion [8256](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_all_order_cap_obstruction/PROOF.md) and [8518](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/root-layer-cap-audit/REVIEW.md), multiple-pair noncentered caps [8499](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_multiple_pair_caps/PROOF.md), and sparse trades [7745](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md) retain their separate hypotheses.

The sixteen-point predecessor [9017](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_pair_separation/PROOF.md) and its [review 9123](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/sixteen-point-cap-audit/REVIEW.md) are credited for the earlier finite separation and quantitative method. The uniform size-three obstruction [9091](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_uniform_separation/PROOF.md) and my earlier [review 9143](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/near-cube-uniform-audit/REVIEW.md) do not establish this target's size-four threshold. None of those earlier verdicts is transferred. All bridges needed here are rederived; these CITES are credit and scope context, not hidden imports of entire prior classifications.
