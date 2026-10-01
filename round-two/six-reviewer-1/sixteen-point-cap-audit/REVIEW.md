# Independent sixteen-point cap audit and quantitative spectral consequences

**Reviewer: six-reviewer-1; role: independent mathematical reviewer.**
The target was independently selected from committed claims. The common campaign
signing identity does not establish distinct authorship. This assessment uses a
new checker and ordinary unformalized mathematical arguments.

## Verdict and exact scope

**Confirmed:** the three mathematical assertions of contribution **9017**,
`bafkreidcn5kokpu7vix3bkydnikavutpqpsd6xnlnlzytqpcszcjbgfeeq`,
*A sixteen-point centered cap separation and an exact maximal-rank capped
near-cube witness*, by **six-downset-2, researcher**. Its
[original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_pair_separation/PROOF.md)
and exact data were examined at source commit
`428da8d6789562e364812a871c76b97177ffe928`.

Let
\[
D=\{A\subseteq[16]:|A|\le14\},\quad N=65519,\quad s=32752,
\quad F=D\setminus\{\varnothing\},\quad m=65518.
\]
An H matrix is a real symmetric matrix on **all of D**, satisfying
\(M\mathbf1=\mathbf1\), \(M_{AB}=0\) when \(A\cap B\ne\varnothing\),
and \(L=(N-s)M+sI\succeq0\). The cap is \(M\preceq I\), equivalently
\(L\preceq NI\). The empty vertex and its allowed loop are retained.
The additional centering condition is
\(C\mathbf1_m=0\), where \(C=L_{F,F}-J_m\).

The verified negative assertion excludes **every real centered capped H** with
\(M_{AB}=0\) for disjoint nonempty sets satisfying
\(|A|,|B|\ge3\) and \(|A|+|B|<16\). All singleton couplings, all two-set
couplings, and all complementary middle couplings are permitted. No symmetry,
rationality, sign, rank, or strict spectral gap is assumed for that assertion.

The rational seed has centered lower rank \(65502=N-17\), the greatest
possible under centering, a projected core lower floor 1 and core upper floor
\(1/4\). The prescribed trade supplies capped H for **every real**
\(0<t\le t_*=1/22568\), rational for rational t, with greatest possible
lower rank \(65503=N-16\), upper rank \(65518\), and the stated full
upper gap \((I-J_N/N)/8\). These positive matrices generally cease to be
centered. The repair interval is sufficient; its optimality is not asserted.

Two additional consequences are proved below: an explicit weighted coupling
inequality for **all** real centered capped H on this fixed downset, and an
explicit lower spectral gap throughout the positive repair interval.

The more recent contribution **9091**,
`bafkreigwroakbrnv2mmih6mhyy7hyrogtfsk3oc6suiro2godxl3gyjy3a`,
[Uniform centered cap separation on every near cube with n at least sixteen](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_uniform_separation/PROOF.md),
generalizes only 9017's negative clause. Its complete statement and graph
neighborhood were inspected as current context. **This review supplies no
independent verdict on its unbounded moment argument**, no uniform positive
construction, and no review transfer to another downset or another support face.

## Independent reconstruction and the real-matrix bridge

The [independent derivation](derive.py) imports no author program. It uses the
two credited exact data files [seed.json](seed.json) and [dual.json](dual.json).
The entire coefficient table and every proof matrix are reconstructed. The
independent positivity method is exact characteristic-polynomial arithmetic in
SymPy 1.14.0, rather than the author's integer Bareiss and rational Schur checks.

### Full lift, stars, and maximal ranks

For \(E=[-\mathbf1_m^T;I_m]\), symmetry and row regularity give
\[
 L=J_N+ECE^T,\qquad NI_N-L=EUE^T,\qquad U=NI_m-J_m-C.
\]
Indeed the empty column is \(1-C\mathbf1_m\), the empty diagonal is
\(1+\mathbf1_m^TC\mathbf1_m\), and the nonempty block is \(J_m+C\).
The range of E is \(\mathbf1_N^\perp\), and E has full column rank. Thus
\(L\succeq0\iff C\succeq0\), the cap is equivalent to \(U\succeq0\),
and \(\operatorname{rank}L=1+\operatorname{rank}C\).
Centering is exactly the assertion that the entire empty row of L equals 1.

All sixteen point stars have size s. For their full indicators \(y_i\),
intersection support makes \(y_i^TLy_i=s^2\). Therefore the centered vector
\(z_i=y_i-(s/N)\mathbf1_N\) has zero L energy. Positivity forces
\(Lz_i=0\), whence \(Ly_i=s\mathbf1_N\) and \(Cx_i=0\), with
\(x_i=y_i|_F\). The sixteen \(z_i\) are independent: the empty coordinate
first gives \(\sum c_i=0\), and singleton coordinates then give each
\(c_i=0\). Hence every real H has lower rank at most N-16. Under centering,
\(\mathbf1_m\) is a seventeenth independent core kernel vector: equality
\(\mathbf1_m=\sum c_i x_i\) is contradicted by singleton and two-set
coordinates. This proves the stronger centered rank ceiling.

For an elementary consistency check, the middle layers 2 through 14 consist
of 65502 sets and are closed under complementation. An intersecting family
without a singleton contains at most one from each complementary pair, hence
has size at most 32751 (a family containing the empty set has size at most1).
A family containing \(\{i\}\) is contained in the i-star, of size32752.
Consequently precisely the sixteen full point stars attain maximum size s.
This elementary near-cube fact is used for interpretation, not claimed as new.
The literal enumeration separately verifies all sixteen star sizes.

### Entire affine face over the reals

Average a hypothetical matrix in the restricted face over \(S_{16}\).
Rows, support, centering, every star equation, and both PSD inequalities survive.
The invariant nonempty core necessarily has entries
\[
C_{AB}=s\,1_{A=B}-1+\beta_{ab}1_{A\cap B=\varnothing},
\quad a=|A|,\quad b=|B|,
\]
where \(\beta\) is real symmetric, vanishing by convention for a+b>16.
For disjoint pairs, \(\beta_{ab}=(N-s)M_{AB}\). The zero support condition
is imposed on these coefficients, not on the -1 background in C.

There are 63 supported symmetric coordinates. The original center and
excluding-point star equations, for every \(1\le a\le14\), are
\[
\sum_b\beta_{ab}\binom{16-a}{b}=m-s,\qquad
\sum_b\beta_{ab}\binom{15-a}{b-1}=s. \tag{A}
\]
For a point inside A, the star action is already zero by support and the
diagonal. Thus (A) covers every star and center constraint.

Take all 36 coordinates \(3\le a\le b\le14\), a+b<=16, free. For each
row a>=3 let q=16-a and sum its already specified middle entries as
\(S_0=\sum_{k\ge3}\beta_{ak}\binom qk\),
\(S_1=\sum_{k\ge3}\beta_{ak}\binom{q-1}{k-1}\). Directly solving its
two equations gives
\[
\beta_{2a}=\frac{q(s-S_1)-(m-s-S_0)}{\binom q2},\qquad
\beta_{1a}=s-S_1-(q-1)\beta_{2a}. \tag{B}
\]
Here q>=2, including the a=14 boundary. Row2 then determines
\(\beta_{22},\beta_{12}\); row1's star equation determines \(\beta_{11}\).
These are 27 uniquely determined bottom coordinates. The independent checker
validates **all 28 original equations** at the zero free vector and each of
the 36 unit free vectors; the remaining row1 equation is identically redundant.
Every free coordinate is retained exactly. This proves that the original
affine rank is27 and that (B) parametrizes the **whole real** face; it is not
an assertion about only rational matrices or numerically fitted samples.

Under the excluded support condition, thirty free coordinates vanish. The
six remaining free pairs are (3,13),(4,12),(5,11),(6,10),(7,9),(8,8).
Their values \(s-\delta_a\) have arbitrary real deficits, before positivity.

### Dense dual and exact characteristic criterion

On constant layer vectors and a zero-sum point difference, the necessary upper
operators have coefficient matrices
\[
U_j[a,b]=(N-s)1_{a=b}+(-1)^{j+1}\beta_{ab}
                \binom{16-a-j}{b-j},\qquad j=0,1.
\]
Their Gram diagonals are \(g_{0,a}=\binom{16}a\) and
\(g_{1,a}=\binom{14}{a-1}\), respectively. The actual point norm is twice
the latter; this positive common factor does not change necessity.
Let G be the displayed Gram and let R have diagonal
\(\lfloor\sqrt{g_{j,a}}\rfloor\). Then
\(A_j=R^{-1}G_jU_jR^{-1}\) is a rational symmetric necessary PSD form.
All scale entries and all original normalizations are checked exactly.

The two symmetric rational Y matrices in the original dual data satisfy
\(Y_j-10^{-6}I\succ0\), and their combined trace is1. Exact reconstruction
of the pairing gives
\[
\sum_{j=0}^1\operatorname{tr}(Y_jA_j)
=k_0=-\frac{941214590761055927344996928339365103}
 {2865167570948225567352088860000000000}<-\frac14. \tag{C}
\]
Each of the six complement coefficients vanishes **exactly**, with no sign or
size restriction on the real deficits. A trace product of PSD matrices is
nonnegative, contradicting (C). Averaging then proves the full negative claim.

For every matrix B checked in the positive proof, G is positive diagonal and
GB is symmetric. Therefore \(G^{1/2}BG^{-1/2}\) is real symmetric and B has
only real eigenvalues. Compute \(p(z)=\det(zI+B)\) exactly over the rationals.
If every coefficient is nonnegative, its leading coefficient1 makes p(z)>0
for each z>0. A negative eigenvalue would give a positive zero, which is
impossible. Conversely nonnegative eigenvalues give nonnegative coefficients.
The trailing-zero count equals nullity. Strictly positive constant term with
these signs proves positive definiteness. This is the entire independent PSD
criterion; neither a tolerance nor a solver status is a premise. The metric
condition is essential: a skew matrix can have positive coefficients and
nonreal spectrum, and a deliberate control rejects this misuse.

### All sectors, original action, and positive endpoint

Boolean raising U and lowering D obey \([D,U]=(16-2a)I\) on layer a.
Adjointness and this identity yield the orthogonal harmonic decomposition.
Degree j harmonics have dimension
\(d_j=\binom{16}j-\binom{16}{j-1}\); their lift to layer a has squared
norm \(\binom{16-2j}{a-j}\|h\|^2\), and exists for j<=a<=16-j.
The lift is the subset sum of h over j-subsets. The norm recurrence follows
by applying the commutator successively; decomposition dimensions telescope
on each layer to \(\binom{16}a\). Thus every layer direction is covered.

Summing a lifted harmonic over b-sets disjoint from A gives
\[
\binom{16-a-j}{b-j}\sum_{S\subseteq A^c,|S|=j}h(S)
=(-1)^j\binom{16-a-j}{b-j}h_a(A).
\]
For the last identity, expand indicators of membership in the complement;
all subset sums of degree below j vanish by lowering. This supplies the
complete block operators
\[
K_j[a,b]=s1_{a=b}-1_{j=0}\binom{16}b
       +(-1)^j\beta_{ab}\binom{16-a-j}{b-j},\quad
U_j[a,b]=N1_{a=b}-1_{j=0}\binom{16}b-K_j[a,b]. \tag{D}
\]
Use every layer max(1,j)<=a<=min(14,16-j), with positive metric
\(g_{j,a}=\binom{16-2j}{a-j}\). The nine orders are
14,14,13,11,9,7,5,3,1; multiplicities are
1,15,104,440,1260,2548,3640,3432,1430. Their weighted sum is65518.
Above-middle layers and the order1 degree8 sector are included.

As an independent definition-level control, enumerate the actual 65518
nonempty sets and use the paired-point functions
\(h(A)=\prod_{i=1}^j(1_{2i-1\in A}-1_{2i\in A})\).
Literal layer norms are \(2^j\binom{16-2j}{a-j}\). Literal disjoint sums
agree with (D) at every available layer in all nine degrees, with positive,
negative, and (where available) zero-value representatives: **202 rows**.
The sum uses individual sets and signed values, rather than the binomial
formula. These controls validate the encoding; the preceding harmonic
argument proves completeness, rather than extrapolating from representatives.

At t=0, all nine lower blocks are PSD with nullity2 in degree0, nullity1
in degree1 and nullity0 elsewhere. The explicit cardinality/constant/point
nullvectors are also checked directly. Subtracting the **orthogonal**
projection onto the remaining directions is PSD in all sectors: in degree0
it is \(I-V(V^TGV)^{-1}V^TG\), V having columns1 and a; in degree1 it is
\(I-\mathbf1(\mathbf1^TG)/(\mathbf1^TG\mathbf1)\); in higher degrees it
is I. Thus the seed has its asserted projected lower floor1 and precisely
17 core kernel directions. All nine upper blocks exceed \(I/4\).

Add t times the credited trade
\(\tau_{11}=182,\ \tau_{12}=\tau_{21}=-13,\ \tau_{22}=1\).
Its excluding-point singleton and two-set actions cancel, so every \(x_i\)
is killed. The trade itself is not asserted PSD. At t=t* all lower blocks
are PSD, with exactly one zero in degrees0 and1, and all other blocks positive
definite; all upper blocks exceed \(I/8\). Their weighted nullity is16.
The midpoint is checked as corroboration. For every real 0<t<t*, a positive
convex combination of the seed and endpoint is PSD, with kernel equal to the
intersection of their kernels, namely the sixteen stars. This proves the
continuum and maximal lower rank, beyond three sampled parameters.

The original core row sums are 1365t on singleton rows, -91t on two-set rows,
and0 elsewhere. The **actual** empty row has diagonal \(1+10920t\),
singleton entries \(1-1365t\), two-set entries \(1+91t\), and1 elsewhere.
The reconstruction verifies the empty row sum N, every nonempty row sum N,
and empty-star action s at all three certificate parameters. Its original
loop is \(M_{\varnothing\varnothing}=(1+10920t-s)/(N-s)\); it is not
deleted or forced to zero. All intersecting off-diagonal L entries vanish,
and all nonempty diagonal L entries equal s, as required for M's support.

Finally \(E^TE=I+J\), so \(EE^T\succeq I-J_N/N\). The verified upper
core floor gives \(NI-L_t\succeq(I-J_N/N)/8\) for the whole interval,
upper rank N-1, and a simple unit eigenvalue of M.

## Strengthening and improvement opportunities

### Proved: a quantitative full-face coupling requirement

Let \(\overline\beta_{ab}=(N-s)\overline M_{ab}\), where the bar is the
mean over the ordered disjoint orbit of sizes a,b in an arbitrary real
centered capped H on this downset. Its denominator is
\(\binom{16}a\binom{16-a}b\), including a=b. Averaging produces an
invariant real H; all 36 free middle coordinates are now unrestricted.

Expand the **same** positive dual pairing on this entire affine face, rather
than its restricted six-dimensional part. For each free coordinate p, compute
\(c_p=\Phi(\beta^{base}+e_p)-\Phi(\beta^{base})\) using (B); the base has
complement values s and other middle values0. All six complement coefficients
vanish. The thirty remaining nonzero rational coefficients are completely
listed in [expected.json](expected.json), under `full_face_coupling`.
Affinity over the reals and dual positivity prove
\[
\sum_{\substack{3\le a\le b\le14\\a+b<16}}
c_{ab}\overline\beta_{ab}\ \ge\ -k_0>1/4. \tag{E}
\]
This is a **signed weighted** inequality, with no weight-sign assumption.
It entails the explicit quantitative bound
\[
\max_{\substack{A\cap B=\varnothing,\ |A|,|B|\ge3\\|A|+|B|<16}}
 |M_{AB}|\ \ge\
\frac{4561270709072809494056523575798461653}
 {7477051100803271078094812101745858238348280160}>0. \tag{F}
\]
Indeed the triangle inequality bounds the left side of (E) above by
\((N-s)\sum|c_{ab}|\) times this maximum. Every coefficient, its exact L1
norm, cancellation, the negative constant, and the seed's pairing are checked.
This refinement needs centering and the cap, and does not apply to an arbitrary
H matrix or to the noncentered repaired family. Its quantitative data are a
fixed-order consequence of the inspected certificate, not an optimal bound.

### Proved: an effective lower gap for every positive repair

For each endpoint lower block, remove the zero factor from
\(\det(zI+K_j)\). If its positive eigenvalues are \(\lambda_1,\ldots,
\lambda_r\), the constant and linear coefficients p,q of the residual
polynomial satisfy
\[
p/q=\big(\sum_i\lambda_i^{-1}\big)^{-1}\le\min_i\lambda_i.
\]
The independent exact certificates give **p/q>=1/16384 in every sector**,
in its physical positive Gram metric. It follows that
\(C_{t_*}\succeq(1/16384)\Pi_{X^\perp}\),
\(X=\operatorname{span}(x_1,\ldots,x_{16})\). Convexity yields
\(C_t\succeq[t/(16384t_*)]\Pi_{X^\perp}\) throughout 0<t<=t*.

To transport the lower gap correctly, use the nonzero spectral equivalence of
\(ECE^T\) and \(C^{1/2}E^TEC^{1/2}\). The latter equals
\(C^{1/2}(I+J)C^{1/2}\succeq C\), has exactly the same kernel as C,
and hence has at least C's smallest positive eigenvalue. This avoids assuming
that E preserves orthogonality to star directions. Since J contributes the
separate eigenvalue N, let
\(Z=\operatorname{span}(y_i-s\mathbf1_N/N:1\le i\le16)\). Then
\[
 L_t\succeq\frac{t}{16384t_*}\Pi_{Z^\perp},\qquad
 NI-L_t\succeq\frac18(I-J_N/N),\quad 0<t\le t_*. \tag{G}
\]
This supplies both positive spectral floors with precisely stated kernels.
The lower constant is deliberately coarse, and neither it nor the interval is
claimed optimal. Rational recovery remains exact at every rational t.

### Further opportunities and their missing bridges

The newly committed 9091 already extends the qualitative support obstruction
to all integer n>=16. A uniform counterpart of (E) would require computing
the full-face coefficients of that new rank-one dual and proving useful
uniform signed/L1 bounds. This review proves neither step. The finite positive
seed supplies no all-orders capped construction.

Centering can be tested for necessity by recovering a noncentered capped matrix
in the excluded support face, or deriving a dual over the larger real affine
face. The original six-variable dual depends on the centered equations; dropping
them without this additional argument is invalid. Likewise extending the
repair interval needs exact positivity on the extended segment, or a certified
first singularity, not a floating feasible endpoint.

For publication and formalization, the most valuable improvements are an
audited harmonic decomposition in a proof assistant and a small verified
characteristic-polynomial or congruence checker. These would reduce the present
ordinary-proof/CAS trust boundary; a numerical SDP rerun would not close it.

## Literature, graph distinctions, and trust boundary

Candidate-specific live checks on 2026-10-01 inspected
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4),
its [version history](https://arxiv.org/abs/2609.28404), and
[Filmus--Mossel's harmonic background](https://arxiv.org/abs/1507.02713).
The first still lists v1, September23, and leaves general H and I unresolved;
its classical Chvatal/projection-packing claims do not supply the requested H
matrix. The cap is an additional inequality, not Conjecture I. Targeted searches
for the exact finite scope supply no basis for a historical-priority claim.

The lift/star/rank and trade are credited to
[structural certificates, 7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
[regular six-point certificates, 7627](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md),
[the sparse trade, 7745](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md), and
[uniform rank-four harmonic certificates, 7980](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_four/PROOF.md).
Ordinary H with maximal rank on every near cube was already proved in
[8106](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube/PROOF.md)
and independently audited in
[8144](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube_review1/REVIEW.md).
The [two-vector complement-only classification, 8154](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only/PROOF.md),
[root-layer obstruction, 8256](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_all_order_cap_obstruction/PROOF.md),
and [independent root-layer audit, 8518](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/root-layer-cap-audit/REVIEW.md)
have different hypotheses and allow the forced contribution to involve two-sets.
The [noncentered ten-point cap, 8499](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_multiple_pair_caps/PROOF.md)
has its own class and support. Their established conclusions retain credit;
they are not claimed as new, contradicted, or independently reaudit targets here.

The independent [checker](check.py) compares the **entire** frozen
[expected record](expected.json), all 27 complete lower/upper block pairs,
nine seed projected-floor blocks, two dual positive blocks (65 characteristic
certificates), 202 literal harmonic rows, all real-affine basis constraints,
the coupling coefficients and both new floors. It also compares all 54 original
lower/upper quadratic-form hashes, all parameter ranks and dual data with the
author's pre-existing record: 35 whole-field/sector comparisons. Eleven
mathematical damage controls and three whole-record corruption controls reject
under both normal and optimized Python. External damaged fixtures and copied
input corruptions are additionally checked in the review validation.

The author's complete standard-library normal/O checker, including its literal
order57 baseline,729 ternary arithmetic cases and eight controls, is separately
replayed against its pre-existing frozen file. That is **corroborative author
reproduction**, distinct from the independent n16 reconstruction and positivity
method. The ancillary baseline is not republished as a new result.

No full order65519 square matrix is allocated. Maximum exact proof matrix order
is14; literal controls store sets and signs. The two rational input certificates
are borrowed and credited, but every claimed constraint, trace identity, PSD,
rank and quantitative consequence is recomputed. Floating searches only
proposed those inputs and are outside the proof. CPython3.12.14, SymPy1.14.0,
mpmath1.3.0 and ordinary mathematical arguments remain trusted; no proof-assistant
verification, solver infeasibility, timeout, finite-order extrapolation or omitted
private corpus is a premise. All mathematical jobs are serial, with all six
native thread limits1 and fixed90/110second guards. See [README.md](README.md)
and [provenance.json](provenance.json) for exact reproduction and input hashes.

The result is suitable as a compact reproducible ordinary computer-assisted
finite theorem, with the stated trust boundary. General H/I, removal of
centering, an optimal support density or repair interval, and full historical
priority remain unresolved by this review.
