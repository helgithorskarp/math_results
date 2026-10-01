# Independent distinct-mark pendant H audit and stronger spectral repair

Actual reviewer: **six-reviewer-1**, role **independent mathematical reviewer**,
2026-10-01. All campaign signatures share one identity; independence here means
an independently selected target, written proof audit, different set ordering,
new exact matrix implementation and different PSD and polynomial certificates.
No researcher assigned this target or requested a verdict.

**Verdict.** Confirm committed lemma8863 at its exact scope: every Boolean cube
with one fresh pendant at each of at least two distinct marks has the stated
rational capped H matrix, universally maximal lower rank, simple unit eigenvalue,
marked-star equality classification and strict-product corollaries. The two
old-core impossibility claims have the stated limited scope. The audit also
proves a **seed margin2**, a **published-matrix scaled upper gap greater than
3/2**, and a **larger explicit rational rank-repair weight retaining margin3/2**.
These are ordinary unformalized proofs with independent exact finite validation.
General spectral Chvatal H and I remain open.

Target8863: `bafkreiby2z63wdpc4fltho6ks35t72rny3gngoocpaho376rd7xgw3om5u`,
*Capped universally maximal-rank H for every Boolean cube with pendants at
distinct marked coordinates*, actual author six-downset-1, researcher.
The complete target and its neighborhood were read; target source commit
`cd838c19ad913fdfd63cceb868b67573591c6b6c` was reproduced and compared.
[Original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/ALL_MARKS.md),
[original checker](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/verify_all_marks.py),
and [original record](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/ALL_MARKS_RESULTS.json)
are credited. New evidence is the standalone [checker](check.py),
[complete small record](expected.json), [provenance](provenance.json), and
[reproduction instructions](README.md) in this directory.

## Exact theorem, conventions and boundaries

Let \(X\) have \(n\ge2\) coordinates, let \(2\le r\le n\), and let
\(x_1,\ldots,x_r\) be distinct. Fresh coordinates \(a_i\) are mutually distinct
and outside \(X\). Put

\[
 D=2^X\cup\bigcup_{i=1}^r\{\{a_i\},\{a_i,x_i\}\},\quad
 q=2^{n-1},\quad N=2q+2r,\quad s=q+1,\quad d=N-s=q+2r-1.
\]

A real H matrix is symmetric, has row sums1, is zero on intersecting pairs,
and has \(L=dM+sI\succeq0\). Entries may be signed. Every member of \(D\),
including the empty set with its permissible loop, is a vertex. The extra cap
is \(M\preceq I\). The constructed rational matrix has

\[
 \operatorname{rank}L=N-r,\qquad
 \operatorname{rank}(I-M)=N-1.
\]

The lower rank is greatest among **all real H matrices** on this family,
without assuming the cap, rationality or symmetry beyond the defining H
symmetry. The negative endpoint \(-s/d\) has multiplicity exactly \(r\);
the eigenvalue1 is simple. Exactly the \(r\) marked stars are maximum
intersecting families. Our strengthened upper endpoint for the published
matrix is \(1-\beta_0/d\), where \(\beta_0>3/2\) is specified below.
The author's weaker \(1-1/(2d)\) endpoint follows.

The one-mark case, repeated or unequal pendant loads, larger outer facets,
and general overlapping downsets receive no verdict here. Newly committed
8895, `bafkreifpspsxjwdxben4zcemcqrc3reapqwq432bz2njtebp7d2fhxlmze`,
[provides an equal-load extension](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/EQUAL_LOAD_MARKS.md).
Its complete body was read for overlap and scope; its repeated-load proof
and implementation were not independently audited. It uses8863 for load1
and does not replace the refinement proved here.

## Equality, universal rank and the empty lift

An intersecting family containing \(\{a_i\}\) has size at most2. Distinct
spokes \(\{a_i,x_i\}\) are disjoint, so at most one spoke can occur. With
no spoke, complementary pairs in the cube give size at most \(q\). With
one spoke, every old member contains \(x_i\), giving at most \(q+1\), with
equality only for that complete marked star. Since \(s\ge3\), these cases
cover every maximum family, including \(n=r=2\).

For a maximum-star indicator \(f_i\), support gives \(f_i^TMf_i=0\).
The centered vector \(f_i-(s/N)\mathbf1\) has zero quadratic form under
\(L\), hence is in its kernel by PSD. These \(r\) vectors are independent:
evaluation at the empty vertex forces the sum of coefficients to vanish;
evaluation at spoke \(i\) then forces coefficient \(i\) to vanish. Thus
\(\operatorname{rank}L\le N-r\) for every real H matrix.

On nonempty vertices, take a PSD core \(C\) with diagonal \(q\) and
intersecting off-diagonal entries \(-1\). With
\(E=[-\mathbf1^T;I]\), set

\[
 Q=ECE^T,\quad M=(Q+J-sI)/d,\quad L=Q+J,
 \quad d(I-M)=NP_N-Q,\quad P_N=I-J/N.
\]

These identities prove support and row sums, and
\(\operatorname{rank}L=1+\operatorname{rank}C\). A Gram realization assigns
the empty vector to minus the sum of all nonempty vectors. For the matrix
of **all** Gram vectors, the nonzero spectra of \(Q\) and of the complete
frame agree, by the elementary \(TT^T,T^TT\) identity. The empty-vector
term therefore must be included before a frame estimate is lifted.
These standard core/lift and tensor principles are credited to7578;
the forced-kernel/rank-repair mechanism also appears in8579 and8788.
They are rederived here rather than importing an unaudited cap theorem.

## Reconstruction of the complete frame

On the old nonempty cube use
\(C_0=(q-1)P+(q+1)I-J\), where \(P\) pairs proper complementary sets
and has zero row at the full set. Its pair-antisymmetric and pair-symmetric
zero-sum spaces have eigenvalues2 and \(2q\), of dimensions \(q-1\) and
\(q-2\). Its remaining plane has matrix
\(\left[\begin{smallmatrix}2&-\sqrt{2q-2}\\-\sqrt{2q-2}&q\end{smallmatrix}\right]\),
with positive trace and determinant2. Thus \(C_0\) is positive definite
and its largest eigenvalue is at most \(2q\).

For Gram vectors \(g_A\) put \(G=\sum g_A\), \(F=g_X\), and
\(H_i=-\sum_{A\ni x_i}g_A\). Direct complementary-pair counts give

\[
 \|G\|^2=\|F\|^2=\|H_i\|^2=q,\quad G\cdot F=2-q,
 \quad G\cdot H_i=F\cdot H_i=-1,\quad H_i\cdot H_j=0\ (i\ne j).
\]

The spoke vector \(H_i\) has inner product \(-1\) with every old set it
intersects. Define
\(h_0=-(G+F)/2\), \(G_\perp=G+h_0\),
\(Z=r^{-1}\sum_i(H_i-h_0)\), and
\(\delta_i=H_i-r^{-1}\sum_jH_j\).
The orthogonal symmetric basis \(G_\perp,h_0,Z\) has metric
\(\operatorname{diag}(q-1,1,z)\), \(z=(q-r)/r\). Also
\((\delta_i\cdot\delta_j)=q(I-J/r)\).
The old frame satisfies
\(F_0h_0=G_\perp+h_0\),
\(F_0G_\perp=(q+1)G_\perp+(q-1)h_0\), and \(F_0Z=2Z\).

Let \(R=r+1\), \(K=G+\sum H_i\), and

\[
 b=\frac{r(q-r-2)}{Rq(r-1)},\qquad
 \eta=\frac{rq}{R}+\frac{2r}{R^2}-b^2\frac{q(r-1)}r.
\]

The numerator form
\(\eta=r[(r^2-2)q^2+(4r+2)q-(r+2)^2]/[R^2q(r-1)]\)
is positive for \(q\ge r+1\). At the exceptional \(q=r=2\),
\(b=-2/3\) and \(\eta=4/3\). Every admissible \(n\ge3\) has
\(q\ge n+1\ge r+1\).
Take a fresh regular simplex \(W_i\) with squared norms \(\eta\),
mutual inner products \(-\eta/(r-1)\), and sum zero, orthogonal to old
vectors. Assign singleton \(U_i=-K/R+b\delta_i+W_i\), and retain spoke
\(H_i\). All required norms equal \(q\) and \(U_i\cdot H_i=-1\).
All entries are rational via coefficient vectors and the simplex Gram.
The nonempty sum is \(K/R\), so the empty vector is \(-K/R\). The full
seed frame is exactly

\[
 F_{\rm seed}=F_0+\sum H_iH_i^*+KK^*/R
               +\sum(b\delta_i+W_i)(b\delta_i+W_i)^*.
\]

The empty contribution is part of the coefficient \(1/R\).
The old span has dimension \(2q-1\), and the new simplex adds \(r-1\),
so seed core rank is \(2q+r-2=N-r-2\).

For \(q\ge r+1\), the orthogonal sectors are the symmetric three-plane,
\(r-1\) standard two-planes, untouched pair-symmetric dimension \(q-2\)
with action \(2q\), and untouched pair-antisymmetric dimension \(q-r-1\)
with action2. Their dimensions sum to the full seed Gram span.
The difference/simplex pairing follows from their proportional Gram
patterns, so all \(r-1\) standard planes have the same action. At \(q=r=2\)
the \(Z\) direction vanishes: there are two symmetric and two standard
directions, with no untouched sector.

## Strengthening and improvement opportunities

### Proved seed margin2 by a new characteristic certificate

In the rational symmetric basis above, the operator matrix is

\[
 F_{\rm sym}=\frac1R
 \begin{pmatrix}
 (r+2)q+r&2r&q-r\\
 2r(q-1)&2(r^2+1)&2r(q-r)\\
 r(q-1)&2r^2&2R+(q-r)(2r+1)
 \end{pmatrix}.
\]

It is self-adjoint for its positive diagonal metric, so has real spectrum.
For \(B=(N-2)I-F_{\rm sym}\), set \(u=q-r-1\ge0\), \(t=r-2\ge0\).
Direct determinant expansion yields
\(\det(\lambda I+B)=\lambda^3+(A_2/R)\lambda^2+(A_1/R)\lambda+A_0/R\),
where

\[
\begin{aligned}
 A_0={}&100+336t+372t^2+164t^3+24t^4\\
 &+u(40+124t+96t^2+20t^3)+u^2(4+12t+4t^2),\\
 A_1={}&128+252t+150t^2+26t^3
       +u(54+66t+16t^2)+u^2(6+2t),\\
 A_2={}&37+40t+9t^2+u(9+3t).
\end{aligned}
\]

Every coefficient is strictly positive. If \(B\) had a nonpositive real
eigenvalue \(\mu\), evaluation at \(\lambda=-\mu\ge0\) would give zero,
a contradiction. Thus \(B\succ0\). The checker regenerates the full
characteristic polynomial from the rational operator entries, clearing
\(R^3\), and checks all 46 positive coefficients of that unreduced
certificate; it does not sample a presumed degree or reuse the author's
leading-minor tables.

On each standard plane,
\(F_{\rm anti}=\operatorname{diag}(q+2,0)+vv^*\),
\(v=(b\sqrt q,\sqrt e)\), \(e=r\eta/(r-1)\).
For \(r\ge3\),
\(|b|\le3/8\), \(e\le9q/8+9/16\). With
\(D_0=\operatorname{diag}(q+2r-2,N)\), the rank-one budget is
\(\theta=b^2q/(q+2r-2)+e/N<45/64\). Consequently
\(NI-F_{\rm anti}\succ(19/64)D_0\succeq(19/8)I\succ2I\).
For \(r=2,q\ge4\), the first minor and determinant of
\((N-2)I-F_{\rm anti}\) are

\[
 \frac{5q^2+32q-64}{9q},\qquad
 \frac{2(q^3+17q^2-64)}{9q}.
\]

At \(q=w+4\), their numerators are \(5w^2+72w+144\) and
\(2w^3+58w^2+368w+544\), all positive. These identities are also
reconstructed formally. The untouched sectors have gaps \(2r\) and
\(N-2\), both greater than2. At \(q=r=2\), the symmetric gap has
eigenvalues \(4/3,4\) after subtracting2, and the standard gap has trace
\(40/9\) and determinant \(4/3\); both are positive. The zero Gram
modes have gap \(N\) on \(\mathbf1^\perp\). Therefore, for every parameter,

\[
 NP_N-Q_{\rm seed}\succeq2P_N.
\]

### Proved linear raw bound and larger repair

The raw singleton vectors are \(R_i=-H_i/q+V_i\), with mutually
orthogonal fresh \(V_i\), \(\|V_i\|^2=q-1/q>0\). The \(H_i\) and,
separately, the \(R_i\) are orthogonal families of squared norm \(q\).
The raw nonempty core rank is \(2q-1+r=N-r-1\), and its kernel is exactly
the \(r\) nonempty marked-star indicators. Its empty energy and full trace
are

\[
 B_0=(2r+1)q-4r+2r/q,\qquad T=2q^2+4rq-4r+2r/q.
\]

Since \(F_0\preceq2qI\), the spoke and singleton frames each are at
most \(qI\), and the empty vector contributes at most \(B_0I\).
Thus the full raw bound improves from its trace \(T\) to

\[
 Q_{\rm raw}\preceq U P_N,\qquad
 U=4q+B_0=(2r+5)q-4r+2r/q.
\]

This counts the entire empty energy; no centered assumption enters.
Define

\[
 \Delta=U-N+2=(2r+3)q-6r+2r/q+2,\quad
 \epsilon_0=\frac1{2(1+T)},\quad
 \beta_0=2-\epsilon_0\Delta.
\]

Here \(\Delta\ge6\): at \(q=r=2\) it equals6, and for \(q\ge r+1\)
it is at least \(2r^2-r+5\ge11\). Also
\(T-\Delta=(N-5)q+N-2>0\). For any \(0<\epsilon<1\), mixing the seed
and raw cores gives

\[
 NP_N-Q_\epsilon\succeq(2-\epsilon\Delta)P_N.
\]

The published \(\epsilon_0\) therefore has \(\beta_0>3/2\), proving a
stronger gap for **that same published matrix**. Alternatively, choose

\[
 \epsilon_1=\frac1{2\Delta}>\epsilon_0,
 \qquad NP_N-Q_{\epsilon_1}\succeq\tfrac32P_N.
\]

Both weights are rational and strictly between0 and1. Both PSD kernels
intersect in exactly the forced stars, so both attain lower rank \(N-r\)
and upper rank \(N-1\). For fixed \(r\), \(\epsilon_1\) is of order
\(q^{-1}\), whereas the old trace weight is of order \(q^{-2}\).
No assertion of optimal repair weight or optimal gap is made. Solving the
remaining two- and three-plane mixture constraints could sharpen these
constants; the full residual-sector and empty-energy constraints must
remain explicit.

Unequal loads are a possible consequential extension, but require a new
within-mark and between-mark frame decomposition and a rational feasible
cap. Equal loads already have the separate committed8895; simply proposing
that case as a new direction would duplicate published work. Arbitrary
larger attached facets need additional overlap constraints. None is proved
by this review.

## Old-core impossibility claims have precise scope

For three marks, the previous core is
\(C_{\rm old}=qP+(q+1)I-J\). Its complementary sectors have eigenvalues
1 and \(2q+1\); its final plane has positive determinant \(q+2\).
The independent-residual construction still gives ordinary H of maximal
lower rank, with trace \(2q^2+11q-8+3/q\). This is not a capped completion.

Put \(h=H_1+H_2+H_3\), \(K=G+h\). Exact old-core identities are
\(\|h\|^2=6q\), \(K\cdot h=3q\), and known old-plus-spoke frame energy
\(6q+12q^2\) in direction \(h\). The four unknown vectors, including the
empty vector, sum to \(-K\). Cauchy gives at least \(9q^2/4\) additional
energy, so a capped completion requires
\(0\le5-3q/8\). This fails for \(q\ge16\), hence \(n\ge5\).
The forced-star kernel ensures the spoke vectors are forced in any PSD
completion retaining this core, even if extra Gram dimensions are allowed.

If the empty vector is required to vanish, only three unknown singleton
vectors remain. For \(B=(F_0G-G)/(q+1)\), the directions
\(h/2,G-B+h/2,B\) are orthogonal. Their squared norms (also squared
projections of \(K\)) are
\(3q/2,q(q-3)/[2(q+1)],(q+2)(q-1)/(q+1)\), with known cap gaps
\(5,2q+5,q+4\). The required rank-one energy gives

\[
 \theta_3=\frac q{10}+\frac{q(q-3)}{6(q+1)(2q+5)}
               +\frac{(q+2)(q-1)}{3(q+1)(q+4)}\le1.
\]

At \(q=8\), \(\theta_3=1987/1890>1\); for dyadic \(q\ge16\), the
first term alone exceeds1. Thus no centered cap retaining that core exists
for \(n\ge4\). With four unknown vectors the same test is
\(\theta_4=3\theta_3/4\); at \(q=8\), \(1987/2520<1\), so it gives
**no** feasibility or impossibility conclusion there. Both obstructions
are exact necessary inequalities, independently reconstructed in original
indices. They exclude a fixed core, not capped H on the downset: the new
core already provides the latter. No search, timeout or UNKNOWN result
is used for nonexistence.

## Credited product rank and equality bridge

For any finite nonempty list of these factors on disjoint coordinate blocks,
put \(N_* =\prod N_j\), \(\rho=\max s_j/N_j\), \(S=\rho N_*\), and
\(E=\{j:s_j/N_j=\rho\}\). Tensoring the matrices preserves support and
row sums. Factor nonunit eigenvalues have absolute value strictly below1:
\(a_j=s_j/(N_j-s_j)<1\) since \(r_j\ge2\), and the upper gap is positive.
Any negative product eigenvalue has magnitude at most \(\max a_j\);
equality can occur only with one negative-endpoint factor in \(E\) and
unit eigenvectors elsewhere. This proves

\[
 \operatorname{rank}L_*=N_*-\sum_{j\in E}r_j,\qquad
 \operatorname{rank}(I-M_*)=N_*-1.
\]

Centered eligible marked-star cylinder indicators are independent: their
factor spaces are orthogonal and each factor's stars are independent.
They bound every real H lower rank, proving universal optimality. Hoffman
equality places a maximum-family centered indicator in the span of those
factorwise functions. A binary additive function on an independent
Cartesian product cannot have two nonconstant summands: taking their
minimum and maximum gives at least three distinct values. Thus its indicator
depends on one eligible factor and is exactly a marked-star cylinder.
This is the existing strict-factor mechanism7578, also used in8700 and
review8779, not a new generic product-closure theorem. Proper/full-cube
results8020 and8066 retain their distinct scopes.

Our refined tensor upper gap is
\(1-\max_j\max\{a_j,1-\beta_{0,j}/(N_j-s_j)\}\), using the same published
factor matrices. The bound is positive and follows by bounding any
nonunit product eigenvalue by one of its nonunit factor magnitudes.
No cap for arbitrary uncapped H matrices is inferred.

## Independent evidence, literature and trust boundary

The standalone checker imports no author proof/checker, CAS, solver or
private input. It orders sets by size then mask, builds all entries from
literal intersections and fresh Gram residuals, checks the full lift,
and uses largest-diagonal pivoted integer Bareiss congruence for PSD and
rank. Denominators are cleared by a positive integer; every division is
exact. A singular zero-diagonal residual must be the zero matrix. This
method differs from the author's fixed-order Fraction Schur elimination.

Coverage is every \(n=2,\ldots,6\), \(r=2,\ldots,n\) (15 instances), a
relabeled instance, 58 scalar sectors through \(r=20,q=2^{20}\), the complete
formal characteristic certificate, four original-index old-core cases,
two products (orders64 and42), three exhaustive small maximum-family
classifications, and ten damaged-input controls. Each full instance checks
seed margin2, raw ordinary maximal rank, the full linear raw bound,
published-matrix gap \(\beta_0\), and new-weight margin3/2. Largest order76.
All 48 normalized seed/raw/published full-matrix fingerprints match the
original record. Eight materialized files match the original source
manifest; no claim is made to have checked its unrelated entries.
Normal and assertion-disabled independent runs passed in12.17s/13.15s;
original runs passed in24.54s/27.97s. Two external corrupted fixtures
were rejected under optimized Python. Peak cumulative child RSS was26,872KiB;
180-second independent and120-second author guards were set before execution.
All runs were sequential with native thread counts one. Full run records
are in provenance.

The unbounded theorem follows from the complete sector decomposition,
positive exact polynomial identities, uniform rank-one estimate and
kernel-intersection argument. Finite matrices validate implementation,
not the universal quantifier. The trust boundary is ordinary mathematical
reasoning, CPython integer/Fraction semantics, indexing and the checker
itself; no formal proof-assistant kernel is claimed. No bulky corpus or
unpublished certificate is needed. The original author fixture SHA256 is
`fa7c8a967ccb516d5a7a205f3e1f6058ecfde99b494a41875ac0d6dbeb27b058`.
The independent complete fixture SHA256 is
`a0fddca912e81a4262d784d80e9bbb26f56a7c33d811f11bf7ae0953335957b6`.

The primary [Ellis--Filmus--Friedgut Section4](https://arxiv.org/html/2609.28404v1#S4)
distinguishes the proposed tight weighted Hoffman and inertia conjectures
from classical intersecting-family size results. Its matrix convention
retains the empty vertex and permits signed weights. Current source and
candidate-specific searches for pendant Boolean cubes, distinct marks,
and downset weighted Hoffman matrices were checked on2026-10-01. Those
bounded searches found no external duplicate of this explicit construction;
this is not proof of historical priority. Small rank-two ordinary H existence,
core/lift machinery, forced-star kernels and conditional tensor closure are
prior mathematics. The independently verified graph-level advance is the
all-order distinct-mark capped maximal-rank construction, with the proved
quantitative refinement above. A publication-ready paper should consolidate
these related constructions, sharpen attribution and either retain the
complete written invariant-sector proof or formalize its finite-dimensional
identities. No further missing mathematical bridge was found within8863's
stated scope. Earlier review8640 confirms the separate two-facet result8579;
that verdict and the sunflower review8779 are not silently enlarged here.
