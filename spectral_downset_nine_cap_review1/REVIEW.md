# Independent order-nine capped H audit and a strict 17-unit dual improvement

Actual reviewer **six-reviewer-1**, role **independent mathematical reviewer**.
The target's explicit author is **six-downset-3**, researcher. The common signing
identity does not identify these individuals. This is an independently selected,
scoped review, with a new exact quantitative refinement.

## Verdict and scope

**Confirmed:** the order-nine necessary layer compression, the rational dual,
the strict weighted signed-sum inequality, and exclusion of all capped H matrices
whose distinct middle support is confined to complements and disjoint two-set
pairs. The hypotheses permit arbitrary real individual signed entries and
singular PSD boundary matrices. No permutation invariance is needed.

**Proved refinement:** with the target's unchanged coefficients, the ordered sum
is strictly greater than
\[
\frac{7125250793269}{25371875000}
=\frac{6693928918269}{25371875000}+17.
\]
The best additional surplus implied by the six-dimensional PSD splitting alone
is strictly between 17 and 18. This bracket concerns that relaxation; it is not a
sharpness assertion for actual capped H matrices.

Target: committed lemma **8354**, artifact
`bafkreiftsgsebhk7nhxd7nd52qyxymysurirnwy6inwvxykjcqvbcd4ggu`,
“Exact order-nine cap dual forces middle support beyond complements and two-set
pairs.” Its [original proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_nine_pair_cap_dual/PROOF.md)
and [integer certificate](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_nine_pair_cap_dual/CERTIFICATE.json)
were audited at source commit **10619bd3247e76f320231b25e3556a5a8fb529fb**.
The entire committed body, relation neighborhood and cited 8319 construction
statement were read. At selection index 8369 and the substantive refresh at 8375,
8354 had no incoming independent assessment. Its extension from invariant orbit
weights to all individual signed weights and the possible uniform dual gap made
this a consequential review target.

The target also combines its order-nine exclusion with previously published
positive constructions at orders 6, 7, 8. **Those positive certificates and the
all-order sufficiency decomposition of 8319 were not freshly independently
verified here.** The “exactly 6,7,8 among 6..9” corollary retains that prior
dependency. This review needs no prior graph theorem for its order-nine verdict
or refinement. There is no claim about unrestricted capped feasibility at order
nine, about orders ten and above, or about resolving general H or I.

## Definitions and a self-contained necessity audit

Let \(D_9=\{A\subseteq[9]:|A|\le7\}\), \(N=502\), \(s=247\), and
\(T=\{A:2\le|A|\le7\}\), with 492 middle vertices. Assume \(M\) is real
symmetric, \(M\mathbf1=\mathbf1\), and \(M_{AB}=0\) whenever
\(A\cap B\ne\varnothing\), including nonempty diagonal entries. The empty
loop is retained. Set \(L=255M+247I\) and impose the additional cap
\(0\preceq L\preceq502I\). Thus every nonempty diagonal of \(L\) is 247,
its intersecting distinct entries vanish, and \(L\mathbf1=502\mathbf1\).

Each coordinate star has 247 members. For its indicator \(y_i\), all its
intersecting off-diagonal entries vanish, so \(y_i^TLy_i=247^2\).
The centered vector \(y_i-(247/502)\mathbf1\) has zero quadratic form.
For a real PSD matrix this implies a zero image, also at a singular boundary,
and therefore \(Ly_i=247\mathbf1\).

Let \(W=L-J\), where \(J\) is the all-ones matrix. Centering any vector
against \(\mathbf1\) gives \(W\succeq0\), \(W\mathbf1=0\), and
\(Wy_i=0\). Let \(Q=W[T,T]\), \(R_{iA}=1_{i\in A}\),
and \(t_A=|A|-1\). The star equations give
\(W_{:,\{i\}}=-\sum_{A\in T:i\in A}W_{:,A}\).
The zero row sums then give \(W_{:,\varnothing}=\sum_{A\in T}t_AW_{:,A}\).
By symmetry these identities determine every other block from \(Q\):
\[
L=J+SQS^T,\qquad
S=\begin{bmatrix}t^T\\-R\\I_{492}\end{bmatrix},\qquad
G=S^TS=I_{492}+R^TR+tt^T.
\]
Here \(Q\succeq0\), \(S\) has full column rank, \(G\succ0\), and
\(\mathbf1^TS=0\). Testing the upper cap on \(Sx\) yields
\(502G-GQG\succeq0\). Congruence by \(G^{-1}\) yields
\(Q\preceq502G^{-1}\). No inverse of a slack matrix is used.

Let \(F\) contain the six complete middle-layer indicators, in order 2 through
7. Write
\[
b=(36,84,126,126,84,36)^T,\quad D_0=\operatorname{diag}(b),\quad
v_k=kb_k,\quad (t_0)_k=(k-1)b_k,
\]
\[
G_0=F^TGF=D_0+vv^T/9+t_0t_0^T.
\]
The count of layer-\(k\) sets containing a given point is \(kb_k/9\).
Consequently \(GF=FD_0^{-1}G_0\), and
\(F^TG^{-1}F=D_0G_0^{-1}D_0\). The necessary compressed pair is
\[
A=F^TQF\succeq0,\qquad B=K-A\succeq0,\qquad
K=502D_0G_0^{-1}D_0\succ0.
\]
These are bilinear compressions, with the diagonal layer factors retained.
They hold before any permutation averaging. They do not assert sufficiency for
a full supported matrix.

## Independent exact dual and multiplicity audit

Retain the target's \(h=H/5000\), \(Y=P/25000000\), and
\(\Gamma=hh^T-Y\), where
\[
H=(5000,16099,16124,16124,16099,27218)^T,
\]
\[
P=\begin{bmatrix}
25000000&49730000&65915000&88235000&116595000&136090000\\
49730000&110560000&146510000&196130000&259177801&296980000\\
65915000&146510000&194225000&259983376&343530000&393650000\\
88235000&196130000&259983376&348045000&459875000&526970000\\
116595000&259177801&343530000&459875000&607705000&696340000\\
136090000&296980000&393650000&526970000&696340000&800300000
\end{bmatrix}.
\]
Our verifier uses the defining signed permutation sum for determinants and
cofactor adjugates for inverses. It imports no author code. This is independent
of the target's Bareiss, LDL, Gauss-Jordan and Woodbury arithmetic paths.
The six leading minors of \(P\), recomputed exactly, are
\[
25000000,\quad290927100000000,\quad21911310500000000000,
\]
\[
729627550416710400000000,\quad30280051290631363544400000000,\quad
962313991543375848025414400000000.
\]
Thus \(Y\succ0\). The cofactor inverses satisfy both left and right adjugate
identities for \(P\) and \(9G_0\), and the reconstructed \(K^{-1}\) has an
exact identity residual. The cancellations \(\Gamma_{2,2}=0\) and
\(\Gamma_{k,9-k}=0\) are checked individually.

Put \(C_0=247D_0-bb^T\). Since the middle diagonal is fixed and every
intersecting distinct entry of \(L\) vanishes,
\(A=C_0+E\), where \(E_{kl}\) is the sum of \(L_{AB}\) over **ordered**
distinct disjoint middle pairs of sizes \(k,l\). Exact cofactor arithmetic gives
\[
\operatorname{tr}(YK)+\operatorname{tr}(\Gamma C_0)
=-\beta,\qquad \beta=\frac{6693928918269}{25371875000}.
\]
Therefore
\[
h^TAh+\operatorname{tr}(YB)=-\beta+\operatorname{tr}(\Gamma E).
\]
The nonzero coefficients and the exhaustive unordered edge counts are:

| sizes | coefficient | unordered pairs |
|---|---:|---:|
| 2,3 | 6153/5000 | 1260 |
| 2,4 | 2941/5000 | 1260 |
| 2,5 | -1523/5000 | 756 |
| 2,6 | -361/250 | 252 |
| 3,3 | 148617801/25000000 | 840 |
| 3,4 | 28267569/6250000 | 1260 |
| 3,5 | 15862569/6250000 | 504 |
| 4,4 | 8219797/3125000 | 315 |

The checker enumerates all 7,071 unordered disjoint middle pairs independently.
Exactly 624 have zero coefficient: 378 disjoint two-set pairs and 246 complement
pairs. On unequal-size layers, the closed count is
\(\binom9k\binom{9-k}l\); on equal-size layers it is half that number.
Every displayed unordered edge contributes **twice** its coefficient in the
ordered sum, including edges within an equal-size layer. Cancellation occurs
for each individual excluded edge, not merely after orbit aggregation.
The two negative coefficients are essential: this is a specified weighted
signed-sum bound. It does not imply an unweighted nonnegative mass bound.

The original strictness argument is valid: equality in the nonnegative dual
would give \(\operatorname{tr}(YB)=0\), hence \(B=0\), so \(A=K\succ0\)
and \(h^TAh>0\), a contradiction. The stronger uniform gap below also proves
strictness directly. If every noncomplement, non-2/2 distinct middle entry
vanishes, the signed sum is zero, proving the target's architecture exclusion.

## Strengthening and improvement opportunities

### Proved: a uniform strict surplus of 17

The positive definiteness of \(Y\) permits more than an equality-exclusion
argument. Let
\[
u=h^TKh=\frac{8839592127077001}{88801562500},\qquad
C=K^{1/2}(hh^T-Y)K^{1/2}.
\]
The independently computed exact ratio is
\[
h^TY^{-1}h=
\frac{3846344544125935295259682805}{601446244714609905015884}>1.
\]
Indeed \(hh^T-Y\) is congruent to \(aa^T-I\), where
\(a=Y^{-1/2}h\), so it has one positive and five negative eigenvalues, with
no zero eigenvalue. The same inertia holds for \(C\). Denote its unique
positive eigenvalue by \(\lambda_+\).

For every \(0\preceq A\preceq K\), let
\(T_*=K^{-1/2}AK^{-1/2}\), so \(0\preceq T_*\preceq I\). In an eigenbasis
of \(C\), each diagonal of \(T_*\) lies in \([0,1]\); hence
\[
h^TAh+\operatorname{tr}(Y(K-A))
=\operatorname{tr}(YK)+\operatorname{tr}(CT_*)
\ge\operatorname{tr}(YK)+\sum_{\lambda_i(C)<0}\lambda_i(C)
=u-\lambda_+.
\]
Equality in this **relaxed minimization** is attained by taking \(T_*\) to be
the orthogonal projector onto the negative eigenspace of \(C\).

Define the exact rational matrices
\[
Z_d=Y+(u-d)K^{-1}-hh^T,\qquad
(K^{-1})_{kl}=\frac{(G_0)_{kl}}{502b_kb_l}.
\]
The common positive denominator used by our certificate is
\(g=22467505725000000\). The verifier reconstructs \(gZ_{17}\) from the
original integers, independently recomputes all six leading minors and compares
them with [the complete compact certificate](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_nine_cap_review1/CERTIFICATE.json).
All six are positive; the last is
\[
1015175396060297777912669657751370921817086239299963641232145983593923890078618972261263422046719936.
\]
Thus \(Z_{17}\succ0\). Congruence by \(K^{1/2}\) gives
\((u-17)I-C\succ0\), so \(\lambda_+<u-17\).
The dual is therefore **strictly greater than 17 uniformly over the entire
compressed PSD pair**. In the preceding affine identity this gives
\[
\sum_{\substack{A,B\in T,\ A\ne B,\ A\cap B=\varnothing\\
B\ne[9]\setminus A,\ (|A|,|B|)\ne(2,2)}}
\Gamma_{|A|,|B|}L_{AB}
>\frac{7125250793269}{25371875000}.
\]
Neither singularity of \(A\) or \(B\) nor signed individual entries alter
this conclusion.

### Proved: the relaxation's best surplus lies strictly below 18

On the same grid, \(gZ_{18}\) has its first five leading minors positive and
its determinant negative:
\[
-31934799211126338198383946393751795679277132843110669627357616815437206709648573167461135284153280064.
\]
Since \(u>18\), the five negative eigenvalues of \(C\) give five positive
eigenvalues of \((u-18)I-C\). The negative determinant forces its remaining
eigenvalue to be negative, hence \(\lambda_+>u-18\). We have proved
\[
17<\min_{0\preceq A\preceq K}
\bigl(h^TAh+\operatorname{tr}(Y(K-A))\bigr)
=u-\lambda_+<18.
\]
Thus a uniform surplus of 18 cannot follow from this PSD pair with this fixed
dual alone. This is a precise limitation of the relaxation, not a counterexample
to an 18-unit bound on actual supported capped H matrices: the minimizing
compressed pair need not extend to one.

### Prioritized next work, not proved here

The highest-value next feasibility question is whether **any** capped H exists
on \(D_9\) when more middle support is allowed. An exact full feasible completion,
or a dual valid for all those entries, is required; this exclusion settles
neither alternative. To improve the current quantitative constant further,
first add the omitted singleton-support/other invariant-block constraints, or
construct a rigorous spectral enclosure of \(\lambda_+\) for a sharper
rational surplus below 18. Root isolation or exact positive-definite tests can
do the latter, but do not enlarge the forbidden support architecture. Extending
the exclusion to \(n\ge10\) needs an order-dependent dual and a renewed
cancellation/PSD proof. Formalizing the real forced-star and spectral
minimization bridges would reduce the current unformalized trust boundary.

## Evidence, reproducibility and trust boundaries

[verify.py](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_nine_cap_review1/verify.py)
uses Python 3.10+ standard library only (executed CPython 3.11.2), exact integers
and fractions. No NumPy, solver, CAS, private optimization record, original
verifier import, or external corpus is a premise. The input dual is explicitly
credited to the target; every mathematical use of it is checked afresh.

Beyond the independent determinant/cofactor path, our checker builds the literal
502-coordinate columns of \(S\), checks all 492 centered columns and 4,428
star annihilations, the 36-entry compressed Gram, and all 2,952 entries of
\(GF=FD_0^{-1}G_0\). It assigns a different deterministic nonconstant signed
weight to every disjoint middle edge, forms \(J+SQS^T\) directly using its
\(t\) row, and verifies all 252,004 entries for symmetry, intersecting
zeroes and the fixed nonempty diagonal, all rows and every forced star equation.
The independently aggregated ordered signed sum matches the affine dual
identity exactly. This synthetic matrix has a negative dual functional and is
**an affine control, not a capped PSD witness**.

Twelve corrupt/domain inputs are rejected, including unsupported surplus 18,
asymmetric/indefinite duals, changed grid, shift entry/minors, scales and bound.
Six determinant controls include singular and row-swap cases. These controls
and all checks remain active under Python `-O`. The normal independent run took
1.0857 seconds and 23,864 KiB maximum RSS; `-O` took 1.2875 seconds and 24,816 KiB,
with byte-identical [RESULTS.json](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_nine_cap_review1/RESULTS.json).
Only one mathematical job ran at a time, with every native thread setting one,
under the unchanged resource scope.

Separately, the unmodified author checker was replayed normally and with `-O`;
both outputs equal its committed RESULTS bytes (SHA256
`d059e3e94b9384271fe9dbfec950b8b6b343759b88c4a83c7c3de02669f8b7b8`).
Its manifest was checked. Those replays corroborate reproducibility; they do
not supply the independence of our mathematical or arithmetic audit.

The real PSD necessity, zero-quadratic-form implication, inertia congruences,
trace positivity and spectral minimization above are written ordinary
mathematics. They have been audited but are **not proof-assistant formalized**.
No exhaustive search over real H matrices or formal theorem compilation is
claimed. Exact finite arithmetic validates its stated part; it does not replace
these analytic bridges. No gap was found in the scoped order-nine result.

## Literature, attribution and publication assessment

[Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4)
formulates H as tightness of the weighted Hoffman bound for every downset, and I
as tightness of the inertia bound. An upper cap \(M\preceq I\) is an added
restriction, absent from H. The [primary version record](https://arxiv.org/abs/2609.28404)
was checked live on 2026-10-01 and lists v1 of September 23. Ordinary Chvátal is
proved there; that does not resolve these two matrix conjectures.

The forced-star/core framework is credited to graph 7578, the sparse 6/7/8 cap
constructions to graph 8319, earlier finite signed duals to 8216, and the
all-order complement-only cap obstruction to 8256. Their public proofs are
[structural certificates](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
[pair-expanded caps](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_pair_expanded_caps/PROOF.md),
[geometric duals](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_geometric_duals/PROOF.md),
and [all-order complement-only obstruction](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_all_order_cap_obstruction/PROOF.md).
Ordinary near-cube H feasibility was already independently checked in
[review 8196](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only_review1/REVIEW.md);
it is not new progress from this review.

Candidate-specific live searches for the distinctive numerator, the 502/247
family and spectral H context revealed no matching external primary certificate.
That bounded result is not proof of historical priority. The review's concrete
addition over the committed target is independent validation and the exact
strict 17-unit refinement, together with a proved 17..18 relaxation bracket.
The scoped theorem has a compact reproducible proof package suitable for further
expert review; full H resolution, a broad classification or a publication
priority claim would exceed the evidence.
