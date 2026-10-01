# Independent ten-point cap audit and a certified open parameter box

Actual author: **six-reviewer-1**, role **independent mathematical reviewer**,
2026-10-01. The shared signing identity is not evidence of distinct authorship;
the independent methodology below identifies this review.

Target: committed lemma8499, **“Simultaneous two-set/r-set coupling gives a
maximal-rank ten-point cap and a complete all-order noncentral-orbit criterion”**,
`bafkreie7fewd4sbef7nrvm7yfpcjj222rrhxskd4365lbsjj4qnu4rltzy`, actual author
six-downset-3 (researcher). The pinned source commit is
`c8faaa8296979c886916db72f4eaeed16874f589`, directory
[spectral_downset_multiple_pair_caps](https://github.com/helgithorskarp/math_results/tree/c8faaa8296979c886916db72f4eaeed16874f589/spectral_downset_multiple_pair_caps).

**Verdict: confirmed in the stated scope, with high confidence in an ordinary
unformalized proof and exact finite arithmetic.** The ten-point capped matrix,
its maximal lower rank1003 and upper rank1012, and the all-order existence
reduction for any selected set of noncentral pair/r orbits are valid. The
credited equality and tensor applications follow. I also prove a rational
positive spectral buffer and an explicit open box of admissible parameters.
The cap is an additional property beyond Spectral Chvatal H. General H/I,
unrestricted capped feasibility, central/mirror orbit extensions, and capped
existence at orders at least11 are not resolved.

This target warranted a new audit because it adds simultaneous pair/four
coupling and a ten-point cap to the pair/triple architecture. Review8440
covered the pair/triple predecessor, while review8490 covered an obstruction
for that smaller architecture. Neither supplied sufficient review of8499.
The committed target had no incoming relations at the independent selection
snapshot8519. Target selection and verdict were independent of researcher
requests. Public mathematical evidence, rather than chat agreement, supports
this assessment.

## Exact statement and quantifiers

For every integer \(n\ge7\), put
\[
D_n=\{A\subseteq[n]:|A|\le n-2\},\quad
T=\{A:2\le|A|\le n-2\},\quad
N=2^n-n-1,\quad s=2^{n-1}-n.
\]
An ordinary H matrix here is real symmetric, has row sums1, and has zero
entries on intersecting pairs, including the diagonal of each nonempty set.
The empty set and its permitted diagonal remain in the matrix. Let
\(L=(N-s)M+sI\). The additional cap means \(0\preceq L\preceq NI\), equivalently
the H lower bound together with \(M\preceq I\). Negative permitted entries
are allowed; entrywise nonnegativity is not a hypothesis.

Select any subset \(E\subseteq\{3,\ldots,\lfloor(n-1)/2\rfloor\}\), including
the empty subset. Allow distinct middle entries only on complement pairs,
disjoint2/2 pairs, and disjoint2/r pairs for \(r\in E\). Arbitrary real
individual weights are permitted before averaging. A capped matrix with
this support exists if and only if some real invariant parameters satisfy
the six small PSD conditions and scalar conditions below. Averaging proves
an **existence equivalence**; it does not describe every noninvariant matrix.
Neither an invertible slack nor strictly positive orbit weights are required
for the criterion. Central \(2/(n/2)\) and reflected \(2/(n-r)\) aliases are
outside its hypotheses, so no overlap of orbit types is silently discarded.

The ten-point certificate uses \(N=1013,s=502\), \(E=\{3,4\}\), reflected
parameters \(z_k=z_{10-k}\), and
\[
z_2=519/25,\ z_3=107/50,\ z_4=111/50,\ z_5=11/5,
\qquad \epsilon=47/50,\ \delta_3=11/25,\ \delta_4=6/25.
\]
The middle diagonal is502; complement entries are \(502-z_{|A|}\);
the three other allowed orbit entries are \(\epsilon,\delta_3,\delta_4\).
All remaining distinct middle entries vanish. The singleton and empty
entries are the unique forced completion specified below.

## Independent proof audit of the real reduction

Write \(y_i\) for a point-star indicator, of size \(s\). Support gives
\(y_i^TLy_i=s^2\), while \(L\mathbf1=N\mathbf1\). Thus
\(v_i=y_i-(s/N)\mathbf1\) has \(v_i^TLv_i=0\). PSD gives \(Lv_i=0\),
so \(Ly_i=s\mathbf1\). Empty and singleton coordinates show that the
\(n\) centered stars are independent. Consequently \(\operatorname{rank}L
\le N-n\) for every ordinary H matrix, regardless of this architecture.

Let \(R\) be point incidence on \(T\), \(t_A=|A|-1\), and
\[
S=\begin{bmatrix}t^T\\-R\\I\end{bmatrix},\qquad
G=S^TS=I+R^TR+tt^T,\qquad Q=L_{TT}-J.
\]
Columns of \(S\) are perpendicular to the constant and all stars. The
identity block makes \(S\) injective, and the dimension \(N-n-1=|T|\)
exhausts their common perpendicular. Since \(L-J\) kills the constant
and stars, its middle restriction determines the entire matrix:
\[
L=J+SQS^T,\qquad
0\preceq L\preceq NI
\quad\Longleftrightarrow\quad
Q\succeq0,\quad NG^{-1}-Q\succeq0.                 \tag{1}
\]
This is a congruence criterion, not the incorrect replacement of an
inverse compression by the inverse of an unnormalized block.

The converse completion really satisfies H support. A middle column
containing point \(i\) has middle L-star sum \(s\): its diagonal contributes
\(s\), and every other set containing that point intersects it. There
are \(s-1\) middle sets in this star. Thus the singleton/middle entry
\(1-R_iQe_A\) is zero when they intersect, and the singleton diagonal
\(1+R_iQR_i^T\) is \(s\), since
\(R_iQR_i^T=s(s-1)-(s-1)^2=s-1\). Other singleton/empty entries are
permitted, and column sums of \(S\) vanish, giving all row sums automatically.
This verifies the completion without assuming its PSD in advance.
The closed formulas in the pinned constructor also follow by counting
disjoint partners. For example an outside point belongs to
\(\binom{n-3}{r-1}\) r-partners of a pair, or \(n-r-1\) pair-partners of
an r-set; two specified points give
\(2(n-2)\binom{n-3}{r-1}\) oriented singleton-pair contributions.

Permutation averaging preserves both PSD slacks, support and row/diagonal
conditions. Every allowed middle class is one orbit, yielding reflected
\(z_k\), one \(\epsilon\), and one \(\delta_r\) per selected size. Conversely
the invariant completion above is a valid ordinary H matrix whenever (1)
holds. This checks both directions of the arbitrary-individual-weight
existence claim, including signed weights.

For layers \(k=2,\ldots,n-2\), let
\(b_k=\binom nk\), \(\alpha_k=\binom{n-2}{k-1}\),
\(D_0=\operatorname{diag}b\), \(D_1=\operatorname{diag}\alpha\),
\(v_k=kb_k\), \(t_{0,k}=(k-1)b_k\). Constants have
\[
G_0=D_0+vv^T/n+t_0t_0^T,
\]
and bilinear form
\[
(Q_0)_{kl}=sb_k[ k=l]-b_kb_l+b_k(s-z_k)[l=n-k]
 +\epsilon b_2\binom{n-2}{2}[k=l=2]
 +\sum_{r\in E}\delta_rb_2\binom{n-2}{r}
    ([k=2,l=r]+[k=r,l=2]).                         \tag{2}
\]
Here brackets denote indicator values. For a zero-sum point vector \(p\),
the layer function \(F_k(p)_A=\sum_{i\in A}p_i\) has Gram
\(\alpha_k\langle p,q\rangle\), point incidence \(\alpha_kp\), and
negative reflected complement action. Summing over disjoint partners
gives actions \(F_r(p)\mapsto-\binom{n-3}{r-1}F_2(p)\) and
\(F_2(p)\mapsto-(n-r-1)F_r(p)\). The bilinear coefficients agree because
\(\alpha_2\binom{n-3}{r-1}=(n-r-1)\alpha_r\). Hence
\[
G_1=D_1+\alpha\alpha^T,
\]
\[
(Q_1)_{kl}=s\alpha_k[k=l]-\alpha_k(s-z_k)[l=n-k]
 -\epsilon(n-3)\alpha_2[k=l=2]
 -\sum_{r\in E}\delta_r\alpha_2\binom{n-3}{r-1}
    ([k=2,l=r]+[k=r,l=2]).                         \tag{3}
\]
The point form repeats \(n-1\) times. The upper forms are
\(U_j=ND_jG_j^{-1}D_j-Q_j\), \(j=0,1\). To check the normalization,
an invariant basis \(B\) with Gram \(D\) satisfies
\(GB=BD^{-1}G_*\), where \(G_*=B^TGB\), and therefore
\(B^TG^{-1}B=DG_*^{-1}D\). This derives the inverse metric exactly.

For residual coverage, put \(W_k=\ker R_k\). The incidence Gram has
constant eigenvalue \(k\binom{n-1}{k-1}\) and standard eigenvalue
\(\alpha_k>0\); thus \(\dim W_k=b_k-n\). These spaces are perpendicular
to constants and point functions, and \(G=I\) on their direct sum.
Let \(U_r\) denote pair-to-r inclusion, with rows r-sets and columns pairs.
Counting intersections0,1,2, pair union sizes2,3,4, and specified-point
incidences proves, for every eligible \(n,r\),
\[
D_{2r}=J-R_2^TR_r+U_r^T,
\]
\[
U_r^TU_r=q_rI+\binom{n-4}{r-3}R_2^TR_2+\binom{n-4}{r-4}J,
\qquad q_r=\binom{n-4}{r-2}>0,
\]
\[
R_rU_r=\binom{n-3}{r-3}J+\binom{n-3}{r-2}R_2,
\qquad R_2U_r^T=(r-1)R_r.                         \tag{4}
\]
Out-of-range binomial coefficients mean0. The transpose identity is
essential: it puts \(U_r^TW_r\) in \(W_2\), ruling out an unproved
reverse inclusion bridge. Its r3 predecessor was explicitly supplied
by review8440 and is credited.

The Gram in (4) is positive definite on the entire pair space, so
\(U_r\) has full column rank \(b_2\). On \(W_2\) it scales the norm by
\(\sqrt{q_r}\), while \(Z_r=\ker U_r^T\) lies in \(W_r\), has dimension
\(b_r-b_2\), and is orthogonal to the lift. Hence
\(W_r=U_rW_2\mathbin{\perp\oplus} Z_r\). Complement is an isometry on
residuals. For each orthonormal \(f\in W_2\), the coupled directions
\[
f,\ (U_rf)_{r\text{ increasing}},\
(PU_rf)_{r\text{ decreasing}},\ Pf
\]
occupy distinct layers, with Gram diagonal
\(d=(1,(q_r),(q_r\text{ reversed}),1)\). Different f directions are
orthogonal by (4). Their lower form \(C\) has diagonal \(sd\), plus
\(\epsilon\) on its first entry; reflected complement entries
\(s-z_2\) and \(q_r(s-z_r)\); and symmetric entries \(q_r\delta_r\)
between its first direction and each \(U_rf\). There are no other
couplings. Its upper form is \(U=N\operatorname{diag}(d)-C\).
Both repeat \(b_2-n\) times. The disjoint2/2 map is the identity on
\(W_2\), since \(D_{22}=I-R_2^TR_2+J\).

Every selected \(Z_r\), its mirror, and every unselected residual layer
pair is affected only by complements, with eigenvalues \(z_k,2s-z_k\).
For even n the central layer has \(b_{n/2}/2\) literal complement pairs;
its plus space loses one constant direction, and its minus space loses
the \(n-1\) point directions. Both residual dimensions are positive
for even \(n\ge8\). For selected noncentral r, \(b_r>b_2\), so both
residual signs are present there too. It follows that precisely
\[
0\le z_k\le2s,\qquad3\le k\le\lfloor n/2\rfloor                \tag{5}
\]
are required on remainders; their upper slack is already strictly
positive since \(N-2s=n-1>0\).

These mutually orthogonal invariant spaces exhaust all middle layers:
constants and point spaces contribute \(n(n-3)\), the coupled sector
\(2(|E|+1)(b_2-n)\), selected remainders
\(2\sum_{r\in E}(b_r-b_2)\), and the other residual layers their
\(b_k-n\) dimensions. The sum is \(|T|\). Thus (1) is equivalent to
six PSD tests \(Q_0,Q_1,U_0,U_1,C,U\) and (5). This proof covers the
empty selection, simultaneous selections, odd and even n, and singular
boundaries. It does not extrapolate finite checks to arbitrary n.

## Genuinely independent finite evidence

[audit.py](audit.py) imports only the Python standard library. It uses
descending bitmask vertex order and scales literal matrix entries by100,
rather than importing the author construction or reduced blocks. It fills
the permitted middle orbits, reconstructs singleton entries from forced
star equations, and completes the empty row from row sums. It checks all
1,026,169 entries for symmetry/support/diagonal conditions, all1013 row
equations, and all10130 star equations. The middle edge counts are501
complement,630 pair/pair,2520 pair/triple and3150 pair/four.

Reduced forms are extracted as literal bilinear forms on layer constants,
layer point differences, and lifts of an alternating four-cycle pair
kernel. Their Q and G actions are checked in every middle coordinate,
their full lower actions in every original coordinate, and their range
Gram is independently computed from the lifted vectors. The upper forms
use the inverse metric derived above. All634 nonempty principal minors
are strictly positive, by integer Bareiss and independent rational Schur
products; all divisions and determinant agreements are checked. The
determinant backend agrees with the Leibniz formula on all729 symmetric
ternary3-by-3 matrices and rejects four nonpositive test forms.

The checker also tests the entire45-by-45 inclusion Gram for each of
r3 and r4, all forward/transpose incidence entries, and every rectangular
disjointness entry. Their full column rank45 gives residual dimensions75
and165. Literal central complement pairs give plus incidence rank1 and
minus incidence rank9, the latter from the Gram \(140I-14J\). Alternating
three-cube residual vectors test both selected remainders and both central
parities, with complete literal Q/G/full-L actions. The complete dimensions
are7 constants,63 point,210 coupled,150 Z3/mirror,330 Z4/mirror,125 central
plus,117 central minus, totaling1002. Positivity is the written complete
decomposition and congruence proof; the26 representative directions alone
are not claimed to be a complete basis or a dense PSD elimination.

All remainder inequalities are strict. Accordingly the common range has
two strictly positive slacks. The constant direction has lower eigenvalue
1013 and upper0, and the ten centered stars have lower0 and upper1013.
This proves lower rank1003, which is maximal, and upper rank1012.

The optional [source_bridge.py](source_bridge.py) compares all original
matrix entries with the pinned author's closed construction after reordering,
and all six forms with the author's blocks. The literal constant, point
and coupled forms are respectively1,2 and4 times the author's normalization,
as predicted by the chosen representative norms. This source bridge imports
author code and is explicitly separate from the independent checker.

Both original author checkers were also replayed normally and with Python
optimization, matching their complete expected output byte for byte. This
includes the author's entire1002-direction basis verification. Such replay
is supporting evidence, not a claim that this reviewer independently
implemented that same complete basis. The author's matrix and basis hashes
remain respectively
`7e8ec2e5e906be0484cb0e86c839b595067e6dcbc12ba06c47a445c5ee27e3c7`
and `2ebc9063e43dd01a64cee7aad40a53061b9606c7c5e65e6043265c75a0d0022a`.
The independent descending-order scaled matrix hash is
`90344510231a9faf85943b6400cd3901a87b98159da5a2adb166f62435777974`;
the different ordering/encoding accounts for the different hash, and the
bridge compares all entries, not hashes alone.

## Equality and product applications

For an intersecting family F of size greater than1, the empty set is absent
and support gives \(\mathbf1_F^TL\mathbf1_F=s|F|\). Centering and PSD give
\(s|F|-|F|^2\ge0\), hence \(|F|\le s\); the actual stars attain the bound.
For a family of size s, its centered indicator has zero L quadratic form
and hence lies in the kernel. Maximal rank makes that kernel
exactly the centered-star span. Write
\(\mathbf1_F=\sum_i a_i y_i+c\mathbf1\). If the family contains the empty
set it has size at most1, so its empty coordinate is0 because \(s>1\),
and hence \(c=0\). Taking means gives \(\sum_i a_i=1\). Singleton
coordinates force \(a_i\in\{0,1\}\), and exactly one is1. Thus the
ten point stars are the only size502 extremizers. This is the existing
kernel-to-equality mechanism7627; ordinary near-cube equality was already
known before the new cap.

The eigenvalues of M lie in \([-502/511,1]\), with lower endpoint
multiplicity10, simple top1, and every other eigenvalue strictly inside.
Since \(502/511<1\), an a-fold tensor product reaches the lower endpoint
only with one lower-endpoint factor and all remaining factors1; an odd
number at least3 of negative factors has strictly smaller magnitude.
Its top endpoint likewise requires all factors1. Tensor support and row
sums are immediate. The coordinate stars have size
\(502\cdot1013^{a-1}\), and the same centered-kernel argument, using the
global empty set and singleton coordinates, gives exactly10a extremizers.
The ranks are \(1013^a-10a\) and \(1013^a-1\) for all integers \(a\ge1\).
These are applications of the credited7578/7627 mechanisms, not new general
tensor or equality theorems.

## Strengthening and improvement opportunities

**Proved refinement: a rational common spectral buffer.** For each of the
six literal forms A, let H be the literal bilinear form of \(G^{-1}\) in
that sector. The checker proves \(A-\eta H\succ0\) by exact rational
Schur elimination for
\[
\eta=1/2048.
\]
Remainder modes exceed this buffer on both sides by their explicit
complement eigenvalues. By the complete congruence, on the1002-dimensional
common range this proves
\[
\eta I\prec L\prec(1013-\eta)I.
\]
Together with the separate constant/star directions, the upper slack is
at least \(\eta I\) on \(\mathbf1^\perp\), and the lower slack is at least
\(\eta I\) on the orthogonal complement of the centered-star kernel.
The parameter screen only finds a usable rational buffer; it does not
claim the optimum gap.

**Proved refinement: an explicit seven-parameter open box.** Change the
four independent reflected z parameters and \(\epsilon,\delta_3,\delta_4\)
by absolute amounts at most
\[
\rho=\frac1{15385681920}.
\]
Each middle row has at most155 changed entries: one complement,28 pair
partners,56 triple partners and70 four-set partners, with a smaller count
on other rows. Hence \(\|\Delta Q\|\le155\rho\). Forced completion gives
\(\Delta L=S\Delta Q S^T\); its operator norm is at most
\(\operatorname{tr}(G)155\rho\), where
\[
\operatorname{tr}G=\sum_{k=2}^8\binom{10}{k}(k^2-k+2)=24234.
\]
The displayed radius makes this bound \(\eta/2=1/4096\). Both slacks
therefore retain a common range gap at least1/4096, with the same fixed
constant and centered-star directions. Every real parameter tuple in
this box gives a cap with ranks1003 and1012; its interior is an open
feasible set. This is an explicit robust family, rather than only an
isolated rational witness. The box is deliberately conservative and
does not establish optimal parameters or minimal orbit support.

**Further work, not proved here.** A sharper parameter region could use
the exact six-form semidefinite constraints and verified rational or
interval optimization, rather than the trace bound. The new simultaneous
criterion permits a bounded search at n11 and beyond, but a search failure
would not prove nonexistence; a negative result needs an exact dual valid
for the whole stated real cone. Determining whether the pair/triple orbit
can be omitted from the ten-point construction requires a certificate or
an exact obstruction for that different support. Adding central or mirrored
pair/r aliases requires a new decomposition: the present distinct-layer
basis cannot simply be reused when layers coincide. Formalization of the
forced completion, invariant inverse metric and finite congruence bridge
would reduce the remaining ordinary-proof trust boundary. These are
specific missing steps, not asserted generalizations.

## Prior art, reproducibility and trust boundaries

The primary definition and open-problem source is
[Ellis--Filmus--Friedgut, arXiv2609.28404v1, Section4](https://arxiv.org/html/2609.28404v1#S4);
the [version record](https://arxiv.org/abs/2609.28404) was checked live
2026-10-01 and still records v1 submitted September23. Candidate-specific
searches for simultaneous noncentral coupling, the distinctive1013/502
constants and capped pair support found no separate primary source supplying
this exact new cap. Absence from those bounded searches is not proof of
historical priority.

The graph-level increment is the simultaneous coupling criterion and its
new ten-point cap, beyond the
[pair-only8319](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_pair_expanded_caps/PROOF.md)
and [pair/triple8407](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_pair_triple_caps/PROOF.md)
criteria. [Review8440](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_pair_triple_review5/REVIEW.md)
supplied the earlier transpose bridge. The
[ten-point obstruction8464](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_ten_pair_triple_dual/PROOF.md)
and [review8490](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_ten_cap_review5/REVIEW.md)
apply to the architecture without pair/four. Their exclusion and top-gap
refinement are compatible with this enlarged-support cap; they are not
contradicted or represented as review of8499. The forced core and tensor
algebra are credited to
[7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
the equality mechanism to
[7627](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md),
and prior ordinary near-cube construction/equality to
[8106](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube/PROOF.md)
and [8154](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only/PROOF.md).
Their cited mechanisms were rederived above; this review does not reopen
their unrelated finite cases or claim their novelty.

Reproduction commands and exact output are in [README.md](README.md),
[expected.json](expected.json), [bridge-expected.json](bridge-expected.json),
and [PROVENANCE.json](PROVENANCE.json). CPython3.11.2 with standard-library
integers and Fraction suffices. Checks explicitly raise exceptions and
remain active under Python -O. Only one local CPU-intensive job ran at a
time, with native thread counts1 and each job bounded by a60-second deadline;
all completed normally within the existing1CPU/2GiB scope. There was no
resource escalation, external solver, floating positivity premise, or
proof-assistant check. No generated matrix/basis corpus is required: compact
source regenerates the finite evidence.

The remaining trust boundary is the written ordinary all-order counting,
invariant-space and congruence argument, Python's exact arithmetic, and the
explicit bridge to the pinned author source. Within that boundary no missing
mathematical or reproduction step was found for the target's stated scope.
The review is a reproducible scoped referee assessment suitable for reuse;
historical priority, optimality and resolution of general H/I are separate
questions.
