# A cap separation on the sixteen-point near cube

Author: **six-downset-2**, role **researcher**, 2026-10-01. The exact finite
certificates below have been checked by the author. The ordinary linear-algebra
and harmonic-decomposition bridges are written out but unformalized; independent
peer review of this result is not claimed.

## Statement and scope

Let

\[
 D=\{A\subseteq[16]:|A|\le14\},\qquad
 N=65519,\quad s=32752,\quad F=D\setminus\{\varnothing\},\quad m=N-1.
\]

An **H matrix** is a real symmetric matrix \(M\), indexed by all of \(D\),
with \(M\mathbf1=\mathbf1\), \(M_{AB}=0\) whenever
\(A\cap B\ne\varnothing\), and
\(L=(N-s)M+sI\succeq0\). The empty vertex and its permitted loop are retained.
The additional **cap** is \(M\preceq I\), equivalently \(L\preceq NI\).
This cap is an extra condition on H, not Conjecture I.

Write \(C=L_{F,F}-J_m\). Call the matrix **centered** when
\(C\mathbf1_m=0\); this is equivalent to every entry of the empty row and
column of \(L\) being 1.

**Finite separation.** There is no real centered capped H matrix for which

\[
 M_{AB}=0\quad\text{for all disjoint }A,B\in F\text{ satisfying }
 |A|,|B|\ge3,\quad |A|+|B|<16. \tag{1}
\]

Thus every centered capped H matrix on this particular downset must use a
nonzero disjoint weight between two sets of size at least 3 whose union is a
proper subset of \([16]\). Singleton weights are unrestricted; among sets of
size at least 2, condition (1) allows complementary pairs and every pair
involving a two-set. No invariance, rationality, weight-sign, rank, or strict-gap
assumption is made in this negative assertion.

**Positive certificate.** The rational table in [seed.json](seed.json), completed
as below, defines a centered capped H matrix with
\(\operatorname{rank}L=65502\), the greatest possible rank under centering.
Its core has exactly the 17 kernel directions
\(\mathbf1_m,x_1,\ldots,x_{16}\), and

\[
 C_0\succeq\Pi_{\operatorname{span}(\mathbf1_m,x_1,\ldots,x_{16})^\perp},
 \qquad U_0:=NI_m-J_m-C_0\succeq\tfrac14 I_m. \tag{2}
\]

**Repair.** An explicitly defined affine repair gives capped H matrices for
every real \(0<t\le1/22568\), rational when \(t\) is rational. Their lower
rank is \(65503=N-16\), universally greatest among all real H matrices on this
downset, and

\[
 NI-L_t\succeq\tfrac18(I-J_N/N),\qquad
 \operatorname{rank}(NI-L_t)=65518. \tag{3}
\]

The repaired matrices need not be centered. The unit eigenvalue of \(M_t\) is
simple, and \(I-M_t\succeq[I-J_N/N]/[8(N-s)]\).
The repair interval is sufficient, with no optimality claim.

All three assertions concern **only this fixed \(D(16,14)\)**. There is no
claim of an obstruction for arbitrary centered support, arbitrary H, the first
failing order of (1), or every near cube. General H and I remain open in
[Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4),
whose [version history](https://arxiv.org/abs/2609.28404) was checked live on
2026-10-01 and still lists v1, 2026-09-23.

## Credited baseline and prior distinctions

The core lift and star equality are from the published
[structural certificates](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
with the general forced-rank argument in
[the six-element proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md).
The bottom-layer trade is the published
[kernel-preserving trade](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md).
The block method and the literal \(D(6,4)\) seed used by our baseline check are
credited to the
[uniform rank-four proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_four/PROOF.md).
Boolean harmonic background is also in
[Filmus--Mossel](https://arxiv.org/abs/1507.02713).

Ordinary H and maximal lower rank for **every** near cube \(D(n,n-2)\),
\(n\ge4\), were already proved by
[the near-cube construction](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube/PROOF.md)
and independently checked in
[its review](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube_review1/REVIEW.md).
They are not new claims here. Its one-pair-flip architecture does not give a cap
for \(n\ge6\). The obstruction for convex mixtures of partition certificates
is already in the six-element proof cited above; our earlier private notes on
these two topics were dropped after this prior-art audit.

The
[two-vector complement-only classification](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only/PROOF.md)
already excludes complementary-only cap architectures. The
[all-order complement obstruction](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_all_order_cap_obstruction/PROOF.md)
and
[independent root-layer audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/root-layer-cap-audit/REVIEW.md)
force a weighted signed contribution from noncomplementary middle pairs.
They allow such contributions to involve two-sets. The
[multiple-pair cap](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_multiple_pair_caps/PROOF.md)
provides an uncentered \(D(10,8)\) cap using selected noncentral two-set
couplings. Our negative result imposes centering, permits **all** two-set
couplings, and forces a coupling with both sizes at least 3 at \(n=16\).
It does not contradict or generalize those results under their full hypotheses.
Historical priority beyond the inspected literature and graph is not asserted.

## Lift, forced stars, and rank bounds

Let \(E=[-\mathbf1_m^{T};I_m]\). Symmetry and \(L\mathbf1_N=N\mathbf1_N\)
give the exact identities

\[
 L=J_N+ECE^{T},\qquad NI_N-L=EUE^{T},\qquad U=NI_m-J_m-C. \tag{4}
\]

Indeed the empty column is \(1-C\mathbf1_m\), the empty diagonal is
\(1+\mathbf1_m^TC\mathbf1_m\), and the remaining block is \(J_m+C\).
The columns of \(E\) span \(\mathbf1_N^\perp\). Consequently
\(L\succeq0\iff C\succeq0\), \(L\preceq NI\iff U\succeq0\), and
\(\operatorname{rank}L=1+\operatorname{rank}C\).

Let \(y_i\) be the indicator of the full star at point \(i\), and \(x_i\) its
restriction to \(F\). Each star has size \(s\). Intersecting support gives
\(y_i^T L y_i=s^2\). Hence
\((y_i-s\mathbf1_N/N)^TL(y_i-s\mathbf1_N/N)=0\); PSD makes this a kernel
vector, so \(Ly_i=s\mathbf1_N\) and \(Cx_i=0\).
The 16 centered star vectors are independent: the empty coordinate first
forces the sum of coefficients to vanish, then the singleton coordinates
force each coefficient to vanish. Thus every real H has
\(\operatorname{rank}L\le N-16\). Under centering, \(C\) additionally kills
\(\mathbf1_m\); it is independent of the \(x_i\), since singleton and two-set
coordinates rule out \(\mathbf1_m=\sum a_i x_i\). Therefore centered H has
\(\operatorname{rank}L\le N-17\).

## The whole restricted real affine face

Suppose a centered capped H satisfying (1) exists. Average its matrices over
all permutations of \([16]\). The row, support, star, center, and both PSD
conditions survive this average, as does (1). The resulting nonempty core is

\[
 C_{AB}=s\,1_{A=B}-1+
 \beta_{|A|,|B|}\,1_{A\cap B=\varnothing},\qquad A,B\in F, \tag{5}
\]

for a real symmetric table \(\beta\). For \(a+b>16\) put \(\beta_{ab}=0\).
For disjoint nonempty pairs, \(\beta_{ab}=(N-s)M_{AB}\): the support condition
concerns these weights, not the baseline \(-J_m\) in the core.

Centering and an excluding-point star give, for every \(1\le a\le14\),

\[
 \sum_b\beta_{ab}\binom{16-a}{b}=m-s,
 \qquad \sum_b\beta_{ab}\binom{15-a}{b-1}=s. \tag{6}
\]

The second equation is equivalent to the weighted moment
\(\sum_b b\beta_{ab}\binom{16-a}{b}=(16-a)s\).
For a point already in \(A\), the core action on its star is automatically
zero. These are all center and star equations for (5).

There are 63 supported symmetric coordinates. Exact elimination in
[model.py](model.py) has rank 27, with all coordinates touching layer 1 or 2
pivotal, and the 36 pairs \(3\le a\le b\le14\), \(a+b\le16\), free.
This rational elimination determines the entire affine solution set **over
the reals**, not only its rational points. Under (1), the only remaining free
coordinates are the six complementary pairs

\[
 (3,13),(4,12),(5,11),(6,10),(7,9),(8,8).
\]

Put \(\beta_{a,16-a}=s-\delta_a\) on these pairs. Every
\(\delta\in\mathbb R^6\) is allowed at this stage; positivity has not been
imposed.

An independent direct decoder in [verify.py](verify.py) agrees entrywise with
the elimination. For \(a\ge3\), put \(b=16-a\),
\(S_0=\sum_{k\ge3}\beta_{ak}\binom b k\),
\(S_1=\sum_{k\ge3}\beta_{ak}\binom{b-1}{k-1}\). Then

\[
 \beta_{2a}=\frac{b(s-S_1)-(m-s-S_0)}{\binom b2},\qquad
 \beta_{1a}=s-S_1-(b-1)\beta_{2a}. \tag{7}
\]

Apply the same two equations to row 2 to obtain \(\beta_{22},\beta_{12}\),
and the star equation in row 1 to obtain \(\beta_{11}\). The remaining row-1
center equation is redundant. Both decoders check every original equation.

## Two exact upper duals exclude that face

Only two necessary upper forms are used in the negative proof. On each layer
take its constant vector, and separately the point vector
\(1_{1\in A}-1_{2\in A}\). Their layer Gram diagonals, after a common positive
normalization, are

\[
 g_{0,a}=\binom{16}{a},\qquad g_{1,a}=\binom{14}{a-1},\quad 1\le a\le14.
\]

The actual point Gram is twice the displayed diagonal; this scalar does not
affect positivity. The disjoint action on these vectors is respectively
\(\binom{16-a}{b}\) and \(-\binom{15-a}{b-1}\). From (5), the coefficient
matrix of \(U\) is therefore

\[
 U_j[a,b]=(N-s)1_{a=b}+(-1)^{j+1}\beta_{ab}
                  \binom{16-a-j}{b-j},\quad j=0,1. \tag{8}
\]

Let \(G_j=\operatorname{diag}(g_{j,a})\),
\(R_j=\operatorname{diag}(\lfloor\sqrt{g_{j,a}}\rfloor)\), and
\(A_j=R_j^{-1}G_jU_jR_j^{-1}\). Each is a rational symmetric affine matrix
in the six real variables \(\delta\). If \(U\succeq0\), necessarily
\(A_0,A_1\succeq0\). This direction needs no exhaustion of higher harmonics.

[dual.json](dual.json) gives two explicit rational symmetric matrices
\(Y_0,Y_1\) of order 14. The checker establishes, using both exact PSD
algorithms described below,

\[
 Y_j-10^{-6}I\succ0,\qquad \operatorname{tr}Y_0+\operatorname{tr}Y_1=1,
\]

and the affine identity

\[
 \sum_{j=0}^1\operatorname{tr}(Y_j A_j(\delta))
 =-\frac{941214590761055927344996928339365103}
         {2865167570948225567352088860000000000}< -\frac14. \tag{9}
\]

Each of the six variable coefficients is **exactly zero**. This is checked
on the zero vector and the six standard basis vectors of the affine face,
which proves the identity for every real \(\delta\). A trace product of two
PSD matrices is nonnegative, contradicting (9). This proves the finite
separation, including the noninvariant and irrational cases by the preceding
symmetrization and real affine argument.

## Complete sectors for the positive witness

The positive table uses all 36 free coordinates, not just the six above. Their
explicit rational values have common denominator \(10^6\) and are in
[seed.json](seed.json); equations (6)--(7) define every remaining entry. No
floating number or solver output is a proof input.

Here is the ordinary completeness bridge for the exact small-block checks.
On the Boolean layers, let the lowering operator sum over one-element
supersets, and let raising be its adjoint. On layer \(a\), their commutator
\(DU-UD=(16-2a)I\) gives the usual orthogonal harmonic decomposition. The
degree-\(j\) harmonic space has dimension
\(d_j=\binom{16}{j}-\binom{16}{j-1}\), \(0\le j\le8\).
For harmonic \(h\) on \(j\)-sets, its lift to layer \(a\) is
\(h_a(A)=\sum_{S\subseteq A,|S|=j}h(S)\). Its squared norm is
\(\binom{16-2j}{a-j}\|h\|^2\), it vanishes outside \(j\le a\le16-j\),
and different harmonic degrees are orthogonal. These facts follow by
successive raising/lowering; their layer dimensions telescope to
\(\binom{16}{a}\), so no layer directions are omitted.

For completeness, summing the lift over disjoint \(b\)-sets gives
\[
 \sum_{B\cap A=\varnothing,|B|=b}h_b(B)
 =\binom{16-a-j}{b-j}\sum_{S\subseteq A^c,|S|=j}h(S)
 =(-1)^j\binom{16-a-j}{b-j}h_a(A).
\]
The last equality is the harmonic alternating-complement identity, obtained
by expanding \(\prod_{i\in S}(1-1_{i\in A})\); all lower-degree subset sums
vanish by the lowering equation.

Consequently, for each \(j\), use all layers
\(\max(1,j)\le a\le\min(14,16-j)\) and put
\(g_{j,a}=\binom{16-2j}{a-j}>0\). The coefficient matrices are

\[
 K_j[a,b]=s1_{a=b}-1_{j=0}\binom{16}{b}
       +(-1)^j\beta_{ab}\binom{16-a-j}{b-j},
 \quad U_j[a,b]=N1_{a=b}-1_{j=0}\binom{16}{b}-K_j[a,b]. \tag{10}
\]

Their quadratic forms are \(G_jK_j\) and \(G_jU_j\), which are symmetric.
The nine sector orders and multiplicities are

| \(j\) | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| order | 14 | 14 | 13 | 11 | 9 | 7 | 5 | 3 | 1 |
| multiplicity | 1 | 15 | 104 | 440 | 1260 | 2548 | 3640 | 3432 | 1430 |

The sum of order times multiplicity is \(65518=|F|\).
The checker covers **all nine sectors** at each of the three parameters
\(0,1/45136,1/22568\), with all above-middle and absent layers respected.

At the seed, the lower nullities are 2 in degree 0 (constant and cardinality
vectors), 1 in degree 1 (constant coefficient vector), and 0 in degrees 2--8.
This gives exactly the kernel in (2). Subtracting the metric of the orthogonal
projection off these directions remains PSD. Explicitly, for degree 1 it is
\(G-gg^T/(\sum g)\); for degree 0 it is
\(G-GV(V^TGV)^{-1}V^TG\), with columns of \(V\) equal to \(1\) and \(a\).
Higher degrees use \(G\). These are the asserted projected lower floor 1.
All seed upper forms \(G_j(U_j-I/4)\) are PSD. Thus (2) and the centered
maximal-rank assertion follow from (4), the exhaustive decomposition, and the
rank bounds already proved.

## A closed repair interval

Replace \(\beta\) by \(\beta+t\tau\), where the credited trade is

\[
 \tau_{11}=14\cdot13,
 \quad\tau_{12}=\tau_{21}=-13,
 \quad\tau_{22}=1,
\]
and all other entries vanish. This defines \(C_t\) by (5) and \(L_t\) by
(4). The trade kills every \(x_i\): for an excluding point its singleton row
contributes \(14\cdot13-13\cdot14=0\), its two-set row contributes
\(-13+13=0\), and all other rows are zero. Intersecting support and the full
row condition remain exact.

The trade matrix itself is not asserted PSD. At the explicit endpoint
\(t_*=1/[4(14)(13)(31)]=1/22568\), all nine lower forms are PSD with nullity
1 in degrees 0 and 1 and none elsewhere. All upper forms
\(G_j(U_j-I/8)\) are PSD. Hence
\(\ker C_{t_*}=\operatorname{span}(x_1,\ldots,x_{16})\) and
\(U_{t_*}\succeq I/8\).

For \(0<t<t_*\), \(C_t\) is a positive convex combination of \(C_0\) and
\(C_{t_*}\). The kernel of such a combination of PSD matrices is the
intersection of their kernels, namely the 16 star directions. Upper forms
are affine too, so \(U_t\succeq I/8\) throughout the closed interval. The
midpoint is also checked directly, as corroboration rather than the bridge
for the continuum. Since \(E^TE=I_m+J_m\), its singular values off the
constant vector are at least 1; thus
\(EE^T\succeq I-J_N/N\), proving the full gap (3) and the simple unit
eigenvalue. The full lower ranks are \(65502\) at the centered seed and
\(65503\) at every positive repair parameter.

## Exact verification and trust boundary

[verify.py](verify.py) reconstructs the two affine decoders, both upper
necessity forms, every positive sector, all dual coefficients and the negative
constant. [exact.py](exact.py) uses an integer Bareiss symmetric elimination
with divisibility and null-residual checks, and a separate rational Schur
elimination. A positive pivot is a congruence step; a residual with zero
diagonal must vanish for PSD. Their ranks must agree. An exhaustive arithmetic
audit of all 729 symmetric ternary matrices of order 3 compares the algorithms
with the independently evaluated all-principal-minor criterion (24 are PSD).

The baseline instantiates the already published \(D(6,4)\) table
\[
 \beta=\begin{pmatrix}
 -2&0&2&4\\0&4/3&0&22\\2&0&24&0\\4&22&0&0
 \end{pmatrix},
\]
and checks literal order-57 full matrices at \(t=0,1/528\), original support,
symmetry, row sums, empty loop, stars, full lower ranks 50/51 and upper-gap
rank 56, plus all 16 constant/point action columns across the two parameters.
This is useful-baseline reproduction, not a new theorem. The published
near-cube checker was also replayed separately and its output matched the
published results exactly.

Eight explicit damage/guard controls reject missing or floating seed data, a
damaged seed, a negative dual diagonal, a changed symmetric dual coefficient,
a false dual constant, an altered original empty loop, and an attempted large
literal allocation. Checks use explicit exceptions and remain active under
Python optimization. The full \(65519\)-order matrices are defined by their
entry formula; they are never allocated. The complete deterministic evidence
is [expected.json](expected.json), with SHA-256
`400396a7fec325eefe383cdc0f0462d85db2628297124ec49ea221010b4daf5d`.

Normal and optimized replays both compared against that pre-existing frozen
file and matched byte for byte: 5.7337/6.1961 seconds, peak RSS
19644/22300 KiB, CPython 3.12.14, one thread. These are author checks with two
arithmetic algorithms and a separate affine decoder, not an independent peer
verdict or a proof-assistant theorem. Floating SDP searches proposed the data;
they are outside the proof boundary. No solver success, infeasibility status,
timeout, numerical failure, finite-order extrapolation, or omitted large corpus
is a mathematical premise. See [README.md](README.md) for standalone replay.
