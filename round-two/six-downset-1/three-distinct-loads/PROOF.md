# Three strictly unequal pendant loads

Actual author and executing agent: **six-downset-1**, role **researcher**,
round two, 2026-10-02. Status: author-checked ordinary proof with exact
symbolic certificates and original-index validation. The full-frame,
dimension, kernel and repair arguments are explicitly unformalized.
Independent review is pending. All campaign workers share a signing identity.

## Quantified result and prior coverage

Let integers \(n\ge3,D>t>v\ge1\) be arbitrary. Choose three distinct
marks \(x_0,x_1,x_2\) in an \(n\)-element set \(X\). Put
\((d_0,d_1,d_2)=(D,t,v)\), and choose distinct fresh elements
\(b_{i,j}\), \(0\le i\le2,1\le j\le d_i\). The downset is

\[
 \mathcal D=2^X\cup\bigcup_{i=0}^2\bigcup_{j=1}^{d_i}
       \{\{b_{i,j}\},\{b_{i,j},x_i\}\}.
\]

Write \(q=2^{n-1},m=D+t+v,N=2q+2m,s=q+D,w=s-1,h=N-1\),
and \(P_N=I-J/N\). There is an explicit rational symmetric matrix \(M\)
on **all** of \(\mathcal D\), including its actual empty vertex, such that

\[
 M\mathbf1=\mathbf1,\qquad M_{AB}=0\quad(A\cap B\ne\varnothing),
 \qquad L=(N-s)M+sI\succeq0,\qquad M\preceq I,              \tag{1}
\]
\[
 \operatorname{rank}L=N-1,\quad \operatorname{rank}(I-M)=N-1,
 \quad (N-s)(I-M)\succeq\tfrac12P_N.                       \tag{2}
\]

The lower rank \(N-1\) is greatest among **all real H matrices**, including
uncapped and irrational matrices with no invariance assumption. The heavy
\(D\)-star is the unique maximum intersecting family. Both the negative
endpoint and the eigenvalue1 are simple. Every nonunit eigenvalue lies in

\[
 \left[-\frac{q+D}{q+2m-D},\quad
             1-\frac1{2(q+2m-D)}\right].                   \tag{3}
\]

The new coverage is exactly **three distinct values, one mark per value**.
The two-value arbitrary-multiplicity result
[9153](../two-load-types/PROOF.md), source
733fd3c0067e8dd56a2c68a12361b50abe65fe42, has separate coverage, including
all three-mark profiles with exactly two values. The profile \((D,t,t)\)
was covered earlier by [9063](../three-mark-loads/PROOF.md), source
1c1143298907acba8331ea063816aae2a7130960. Its one-heavy extension
[9100](../one-heavy-many-lights/PROOF.md), source
1d683414bed8fd489f64caa25bfbce02fec06456, allows arbitrarily many equally
loaded light marks. The two-mark predecessor
[9005](../two-unequal-loads/PROOF.md), source
001f4ec642e1280a9a0972f5a89f0b49b1d331fe, covers two arbitrary unequal
loads. These are prior results, not new cases of this theorem.

Equal values are outside the strict domain here. The equal-load results
[8895](../EQUAL_LOAD_MARKS.md), source
fd13642ca7c14c53c0339c5a592fc0e73c14d326, and
[8863](../ALL_MARKS.md), source cd838c19ad913fdfd63cceb868b67573591c6b6c,
retain their distinct rank and maximum-star counts. The full lift is
credited to [7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md).
The old/spoke Gram, rational singleton completion and trace repair are
credited to9005,9063,9100,9153 and their predecessors
[8579](../UNEQUAL_FACETS.md) and [8788](../TWO_MARKED_CUBE.md).
The new mechanism has nine mean directions, two independent singleton
contrasts, a six-update budget and a second-compound determinant identity.

[Review9049](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/two-unequal-load-audit/REVIEW.md)
confirms9005 and improves its trace repair. Its source is
bb7bbd45234ace28fc151a28e05962fd52f14ad7.
[Review8927](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/distinct-mark-audit/REVIEW.md)
concerns8863. Neither verdict transfers to this theorem or9153.
We assert no optimal repair constant or independent review of the new result.

The signed-weight and empty-loop conventions are those of
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
Their [version record](https://arxiv.org/abs/2609.28404), checked live
2026-10-02, still lists only v1 of2026-09-23, with H and I conjectural.
The classical maximum-star theorem does not provide H/I matrices.
General H/I, three-value arbitrary mark multiplicities, four or more
values, and optimal repair remain open here. The extra cap is not
Conjecture I. Historical priority beyond the cited inputs is unassessed.

## Maximum family, rank ceiling and full lift

An intersecting family containing a fresh singleton has at most2 members.
Spokes at different old marks are disjoint. A family containing spokes
therefore uses one mark, and every old set in it contains that mark. Its
size is at most \(q+d_i\), with equality only for the complete marked star.
Old-only families have size at most \(q\) by complementary cube pairs.
Thus \(s=q+D\), with a unique maximum star \(\mathcal S_0\).

For any real H matrix, put
\(z=\mathbf1_{\mathcal S_0}-(s/N)\mathbf1\). Support and row sums
give \(z^TLz=0\); positivity gives \(Lz=0\). Since \(z\ne0\),
every lower rank is at most \(N-1\), without a cap or rationality hypothesis.

For a PSD core \(C\) on nonempty sets, diagonal \(w\) and entries
\(-1\) at intersections, use the credited lift

\[
 T_0=\begin{pmatrix}-\mathbf1^T\\I\end{pmatrix},\quad
 Q=T_0CT_0^T,\quad M=(Q+J-sI)/(N-s).
\]

It gives support and row sums on the full index set, and

\[
 L=Q+J,\quad \operatorname{rank}L=1+\operatorname{rank}C,
 \quad (N-s)(I-M)=NP_N-Q.                                 \tag{4}
\]

The actual empty Gram vector is the negative nonempty sum. The complete
Gram frame, including this vector, has the nonzero spectrum of \(Q\).
It cannot be omitted in a cap calculation. The empty loop is permitted;
the weights may be signed.

## Rational Gram construction

The old nonempty cube core is
\(C_D=(q+D)I+(q-D)P-J\), where \(P\) exchanges proper nonempty
complements and has zero full-set row. Its spectrum has \(2q\) with
multiplicity \(q-2\), \(2D\) with multiplicity \(q-1\), and a positive
plane of trace \(q+D+1\) and determinant \(2D\). In particular it is
PD even when \(D>q\). For its Gram vectors put
\(G=\sum_{A\ne\varnothing}g_A,f=g_X,H_i=-\sum_{A\ni x_i}g_A\).
Direct complement counts give

\[
 G^2=f^2=w,\quad Gf=D+1-q,\quad H_iH_j=qD\delta_{ij},
 \quad GH_i=fH_i=-D.                                     \tag{5}
\]

Take mutually orthogonal spoke residual groups, orthogonal to the old
space, with
\(T_{i,j}T_{i,l}=(q+D)(\delta_{jl}-1/D)\), and set
\(S_{i,j}=H_i/D+T_{i,j}\). The heavy residual group has rank \(D-1\),
and each lighter group has rank \(d_i\); their total is \(m-1\).
All spokes have squared norm \(w\), same-mark distinct product \(-1\),
and different-mark product0. Their mandatory old products are \(-1\).

Let \(L_i=d_i^{-1}\sum_jS_{i,j}\). Then

\[
 L_0=H_0/D,\quad L_i^2=(q+D-d_i)/d_i,\quad L_iL_j=0\ (i\ne j).
\]

Put \(K=G+\sum_i d_iL_i\). Directly,

\[
 B_0=K^2=w+m(q+D)-\sum_i d_i^2-2m
     =w+m(q-2)+t(D-t)+v(D-v)>0,
 \quad KS_{i,j}=w-d_i.                                   \tag{6}
\]

Use the credited rational coefficients

\[
 c_i=\frac{m(w-d_i-m-1)}{(m+1)((m-1)w-1+d_i)},\qquad
 C_\Sigma=\sum_i d_ic_iL_i.
\]

The old/spoke part of singleton \(U_{i,j}\) is
\(-K/(m+1)+c_iS_{i,j}-C_\Sigma/m\). Its mandatory own-spoke
product is exactly \(-1\), because

\[
 -\frac{w-d_i}{m+1}
       +c_i\frac{(m-1)w+d_i-1}{m}=-1.                    \tag{7}
\]

Write \(C_2=\sum_i d_ic_i^2(q+D-d_i)\) and
\(K_C=\sum_i d_ic_i(w-d_i)\). The missing singleton squared norm is

\[
 \eta_i=w-\frac{B_0}{(m+1)^2}-c_i^2w
      +\frac{2c_i^2(q+D-d_i)}m-\frac{C_2}{m^2}
      +\frac{2c_i(w-d_i)}{m+1}-\frac{2K_C}{m(m+1)}.         \tag{8}
\]

Set \(E_\eta=\sum_i d_i\eta_i\) and
\(\zeta_i=m[\eta_i-E_\eta/(m(m-1))]/(m-2)\). Their strict
positivity is certified below. On the flattened \(m\) singleton indices
use residual Gram

\[
 \mathcal W=P_m\operatorname{diag}
       (\zeta_0^{[D]},\zeta_1^{[t]},\zeta_2^{[v]})P_m.      \tag{9}
\]

Its row sums are0, rank is \(m-1\), and diagonal is exactly \(\eta_i\):
\(\sum_i d_i\zeta_i=mE_\eta/(m-1)\). Take residual vectors
\(W_{i,j}\), orthogonal to the old/spoke space, and complete

\[
 U_{i,j}=-K/(m+1)+c_iS_{i,j}-C_\Sigma/m+W_{i,j}.
\]

This is a rational defining Gram matrix: every mandatory norm and
intersection product holds. Its nonempty sum is \(K/(m+1)\), so the
actual empty vector is \(-K/(m+1)\). The seed core rank is

\[
 (2q-1)+(m-1)+(m-1)=N-3.                                  \tag{10}
\]

## Exhaustive frame decomposition

Put \(h_0=-(G+f)/2,G_p=G+h_0,A_i=H_i-h_0\). Then
\(G_p^2=q-1,h_0^2=D,A_iA_j=D(q\delta_{ij}-1)\), with other
products0. The old frame \(F_0=\sum_Ag_Ag_A^*\) satisfies

\[
 F_0G_p=(q+1)G_p+(q-1)h_0,\quad F_0h_0=D(G_p+h_0),
 \quad F_0A_i=2DA_i.                                     \tag{11}
\]

The marked block is PD because the actual \(q\ge4>3\); its eigenvalues
are \(Dq,Dq,D(q-3)\). Let \(Z_i=L_i-H_i/D\) for \(i=1,2\).
They are mutually orthogonal and orthogonal to old vectors, with norms
\((q+D)(1/d_i-1/D)>0\).

Let \(W_i=d_i^{-1}\sum_jW_{i,j}\). Their weighted sum is0 and

\[
 W_iW_j=\frac{\zeta_i}{d_i}\delta_{ij}
      -\frac{\zeta_i+\zeta_j}m+\frac{\sum_l d_l\zeta_l}{m^2}. \tag{12}
\]

The directions \(W_0,W_1\) are independent. Indeed a dependence is a
coefficient vector constant within the first two residual groups and0
on the third. By positivity in (9) it must be constant on all groups,
hence identically0. The nine mean directions are
\((G_p,h_0,A_0,A_1,A_2,Z_1,Z_2,W_0,W_1)\).

Put \(\sigma_i=c_iL_i-C_\Sigma/m+W_i\). Their weighted sum is0.
Expanding all old, spoke, singleton and **actual empty** outer products
gives the complete mean frame

\[
 F_+=F_0+\sum_i d_iL_iL_i^*+\frac{KK^*}{m+1}
                      +\sum_i d_i\sigma_i\sigma_i^*.      \tag{13}
\]

The singleton mixed common terms vanish by the weighted relation; the
\(m\) common singleton vectors plus the empty vector give \(KK^*/(m+1)\).
Eliminating \(\sigma_2=-(D\sigma_0+t\sigma_1)/v\) leaves the weight

\[
 W_c=\operatorname{diag}(D,t)+\frac1v
       \begin{pmatrix}D^2&Dt\\Dt&t^2\end{pmatrix},\qquad
 W_c^{-1}=\operatorname{diag}(1/D,1/t)-J_2/m.              \tag{14}
\]

At each mark, a unit zero-sum spoke-index direction gives orthogonal
residuals \(T,W\) of squared norms \(q+D,\zeta_i\). Its frame is

\[
 F_i^{\rm int}=\operatorname{diag}(q+D,0)+u_iu_i^*,\quad
 u_i=(c_i\sqrt{q+D},\sqrt{\zeta_i}).                       \tag{15}
\]

Mean/internal and different internal cross products vanish by zero sums.
There are no mark-multiplicity standard sectors: there is one mark of
each value. Untouched symmetric old differences have dimension \(q-2\)
and action \(2qI\). The old low space orthogonal to the three independent
\(A_i\) has dimension \(q-4\), action \(2DI\), and zero products with
every added vector. The exhaustive census is

| Sector | Dimension |
| --- | ---: |
| Mean sector |9|
| Paired internal sectors |\(2(m-3)\)|
| Untouched high space |\(q-2\)|
| Untouched low space |\(q-4\)|
| Total |\(N-3\)|

At \(n=3\), the low space is absent; at \(v=1\), its internal sector
is absent. The scalar cap for that mark is still certified.

## Six-update budget and two-contrast congruence

All old eigenvalues are below \(h=N-1\), since \(h>2q,2D,q+D+1\).
The bilinear resolvent metric \(R\) of \((hI-F_0)^{-1}\), in the nine
mean directions, has plane block

\[
 \frac1\Delta\begin{pmatrix}(q-1)(h-D)&D(q-1)\\
                D(q-1)&D(h-q-1)\end{pmatrix},\qquad
 \Delta=(h-q-1)(h-D)-D(q-1)>0.                             \tag{16}
\]

The marked block is \(D(q\delta_{ij}-1)/(h-2D)\), the \(Z\)-block
has diagonal \((q+D)(1/d_i-1/D)/h\), and the \(W\)-block is (12)
restricted to0,1 and divided by \(h\). Every cross block is0.
If \(B_{\rm old}\) is the old-frame action matrix, the exact metric
identity is \(R(hI-B_{\rm old})=G_{\rm mean}\).

For updates \((L_0,L_1,L_2,K,\sigma_0,\sigma_1)\), let \(V\) denote
their coordinate matrix. The strict mean cap is equivalent to

\[
 \mathcal B=H^{-1}-V^TRV\succ0,\quad
 H^{-1}=\operatorname{blockdiag}(1/D,1/t,1/v,m+1,W_c^{-1}).  \tag{17}
\]

The old part of \(\sigma_\alpha\) is \(\sum_i b_{i\alpha}L_i\), where
\(b_{i\alpha}=c_i\delta_{i\alpha}-d_ic_i/m\), \(\alpha=0,1\).
Append a zero coefficient for \(K\). Subtract these old parts from both
last columns and rows, a determinant-one congruence. With
\(D_4=\operatorname{diag}(1/D,1/t,1/v,m+1)\), it gives

\[
 \widetilde{\mathcal B}=\begin{pmatrix}A&X\\X^T&E\end{pmatrix},\quad
 X=-D_4b,\quad E=W_c^{-1}-G_W/h+b^TD_4b.                  \tag{18}
\]

Here \(A\) is the first four-update budget, \(G_W=(W_\alpha W_\beta)\),
and the last row of \(X\) is0. All entries in (16)--(18) are reconstructed
by [symbolic.py](symbolic.py), and all36 congruence entries are checked
physically by [verify_full.py](verify_full.py).

Let \(d_4=\det A,C=\operatorname{adj}A,Y=X^TCX\). Then

\[
 d_5=d_4E_{00}-Y_{00},\qquad
 d_6=d_4\det E-E_{11}Y_{00}-E_{00}Y_{11}+2E_{01}Y_{01}+\mathfrak C, \tag{19}
\]
\[
 \mathfrak C=\sum_{I,J}\det X_I\det X_J(-1)^{\sum I+\sum J}
                      \det A[J^c,I^c],\quad
 I,J\in\{\{0,1\},\{0,2\},\{1,2\}\}.                     \tag{20}
\]

These follow by expanding \(d_4\det(E-Y/d_4)\) and Jacobi's complementary
minor identity \(\det Y=d_4\mathfrak C\). The zero last border row leaves
exactly nine second-compound terms. The reconstructed formulas divide by
no \(d_4\) and avoid a720-term rational determinant expansion. Their
derivation initially assumes \(d_4\ne0\), guaranteed by the first four
positive minors; the resulting polynomial identities also extend elsewhere.

[verify_generic.py](verify_generic.py) independently checks these identities
over19 free symbols: symmetric four-by-four \(A\), six free \(X\) entries
with last row0, and symmetric two-by-two \(E\). Schoolbook integer
polynomials verify16 adjugate identities, (19) against all120/720
determinant permutations, and Jacobi's identity. The sixth generic polynomial
has193 terms. A wrong cross-term sign is rejected. This exact generic
identity check uses a different arithmetic implementation; it is a
same-author check, not independent review or formalization.

The three internal cap slacks are

\[
 1-c_i^2(q+D)/(h-q-D)-\zeta_i/h>0.                         \tag{21}
\]

The untouched gaps \(h-2q\) and \(h-2D\) are positive. Thus three
\(\zeta_i\) signs, three slacks (21), and six leading minors of (18)
exhaustively prove every full-frame eigenvalue below \(h\). In the actual
full index space this gives the seed unit gap

\[
 NP_N-Q_{\rm seed}\succeq P_N.                            \tag{22}
\]

## Exact uniform signs and trust boundary

[verify_signs.py](verify_signs.py) regenerates (8), (12), (16)--(21)
over \(\mathbb Q(Q,D,t,v)\), with \(q=Q+4\). Sign coverage uses

\[
 D=t+B+1,\qquad t=v+T+1,\qquad v=V+1,
 \qquad Q,B,T,V\ge0.                                     \tag{23}
\]

Every actual parameter is included. The separate physical condition
\(q>3\) in the marked metric holds on every actual cube. Every primitive
denominator factor used by the certificate is also certified strictly
positive after (23), including the coefficient denominators, \(m-2,m-1,m\),
\(m+1,h,h-2D,h-q-D\) and \(\Delta\).

For the first eleven rational functions, split each exact raw numerator
into powers of \(Q\), then use triangular Horner shifts in order
\(D\mapsto t+B+1,t\mapsto v+T+1,v\mapsto V+1\). Every coefficient
is nonnegative, with a positive constant in the \(Q^0\) coefficient.
The fifth raw numerator has23949 terms, within the30000-term guard.

For the sixth, (19) gives six **factored** summands
\(d_4E_{00}E_{11},-d_4E_{01}E_{10},-E_{11}Y_{00},-E_{00}Y_{11},
2E_{01}Y_{01},\mathfrak C\). Exact division cancels common factors before
products. Take the least common primitive denominator, multiply by missing
positive factors, and convolve as separate \(Q\)-coefficient polynomials.
No expanded raw four-variable sixth numerator is constructed. Each raw
or shifted load coefficient is an ordinary three-variable polynomial with
the same term and packing guards. The21 coefficients \(Q^0\) through
\(Q^{20}\) have load degrees44 through24. After (23) they all have
nonnegative coefficients, and the \(Q^0\) constant is positive. Therefore
the common numerator is strictly positive, and so is its denominator.

| Sign | Raw numerator terms | Q-coefficient lemmas | Shifted terms across separate coefficients |
| --- | ---: | ---: | ---: |
| Each of three \(\zeta_i\) |4104|8|5270|
| Heavy internal slack |5746|9|6600|
| Each light internal slack |5745|9|6600|
| Mean minor1 |34|4|34|
| Mean minor2 |121|6|121|
| Mean minor3 |315|8|315|
| Mean minor4 |470|7|471|
| Mean minor5 |23949|14|25507|
| Mean minor6 |Separate coefficients only|21|176234|

The twelve functions use111 coefficient lemmas and238292 total shifted
terms across separate polynomials. For the sixth, the21 raw load
coefficients total150348 terms; their maximum is12309, and their shifted
maximum is16154. These totals are not expanded polynomials or raised
guards. [RESULTS.json](RESULTS.json) records every coefficient hash,
constant, degree, factor power and count, rather than a polynomial corpus.

[polynomial.py](polynomial.py) retains the credited exact integer Kronecker
algorithm, with variable radices beyond product degrees, balanced base
larger than twice the coefficient \(\ell_1\) product bound, and checked
carry completion. All factor cancellation uses exact polynomial division;
modular probes only reject divisibility attempts. Separate module instances
hold the raw four-variable and coefficient three-variable engines.
Thirty-six schoolbook multiplication controls check both dimensions, nine
independent raw schoolbook products check the \(Q\) convolution, and three
direct-power substitutions check triangular Horner evaluation. Exact
physical evaluations at three fixtures are additional regressions, not
proofs of identities or uniform signs. Changed fingerprints and an actually
negative translated \(Q^0\) constant are rejected. Normal and optimized
Python compare the complete frozen result, not a subset.

No CAS, floating point, interpolation, private saved polynomial, cache,
database or solver output is a reproduction input. The ordinary geometric
and linear-algebra bridges above are not proof-assistant formalizations.
The stage/coefficient guard remains60s, every ordinary polynomial has at
most30000 terms, every packing array at most32MiB, with one intensive
mathematical job and one solver/BLAS/OpenMP thread. An earlier dense sixth
expansion reached the term guard and was preserved privately as incomplete
work. The coefficient reformulation supplies the exact proof without raising
resources. Such a failure never means mathematical nonexistence.

## Full raw repair and greatest rank

The credited raw singleton is \(-S_{i,j}/w\) plus its own independent
residual of squared norm \(w-1/w>0\). Its core has rank
\((2q-1)+(m-1)+m=N-2\). Its only relation is the heavy star:
\(-H_0+\sum_jS_{0,j}=0\). It is also in the seed kernel. Thus the
PSD kernel intersection under any strictly positive mixture is precisely
that star, so the mixed core rank is \(N-2\).

The actual raw empty energy and full raw trace are

\[
 B_{\rm raw}=w+(1-1/w)^2[m(q+D)-\sum_i d_i^2]
       -2m(1-1/w)+m(w-1/w),\quad T_{\rm raw}=(N-1)w+B_{\rm raw}.
\]

Put \(\epsilon=1/[2(1+T_{\rm raw})]\), and mix the two rational cores
as \(C=(1-\epsilon)C_{\rm seed}+\epsilon C_{\rm raw}\).
Since \(Q_{\rm raw}\succeq0,Q_{\rm raw}\mathbf1=0\), its trace gives
\(Q_{\rm raw}\preceq T_{\rm raw}P_N\). Equation (22) implies

\[
 NP_N-Q\succeq[1-\epsilon(T_{\rm raw}-h)]P_N
                         \succeq\tfrac12P_N.              \tag{24}
\]

The full lower rank is \(1+(N-2)=N-1\), attaining the all-real ceiling.
The half-unit upper gap gives \(\operatorname{rank}(I-M)=N-1\) and a simple unit
eigenvalue. The lower kernel is the unique centered maximum-star indicator,
so the negative endpoint is simple. This proves (1)--(3).

The construction is noncentered: the seed nonempty sum is \(K/(m+1)\),
with positive empty energy (6); the mixed empty energy is the positive
convex combination of the seed and raw energies. This supplies no kernel
map to a near-cube downset, and transfers no near-cube support conclusion.

## Literal validation and reproducibility

[verify_full.py](verify_full.py) builds every original set and complete
rational core. It checks all81 mean resolvent entries, all36 congruence
entries, every mean/internal/cross Gram and full-frame entry, the actual
empty contribution, both untouched spaces and dimension exhaustion,
the actual heavy-star kernels, seed/raw/mixed ranks and full gaps.
It also checks (19)--(20) by separate rational elimination. Fixtures are

| \(n,D,t,v\) | \(q\) | \(N\) | Changed-frame entries |
| --- | ---: | ---: | ---: |
|3,3,2,1|4|20|225|
|4,4,3,1|8|32|361|
|5,5,3,2|16|52|529|
|3,7,5,4|4|40|1225|
|6,3,2,1|32|76|225|

All2565 entries and ten intersecting-entry/empty-loop damages are checked.
The fourth fixture has \(D>q\), hence negative proper-complement old
coefficients; the fifth checks the existing largest literal cube guard.
Omitting the actual empty contribution changes the mean frame in every
fixture. The complete constructor also agrees with9153 on a credited
two-value baseline; this is validation, not new mathematics.

The literal guards \(n\le6,N\le80\) bound the finite verifier only.
Uniform coverage follows from the ordinary exhaustive decomposition and
the exact coefficient proof, not those fixtures. Use CPython3.11+ and
the standard library; commands and compact expected fields are in
[README.md](README.md). [SHA256SUMS](SHA256SUMS) pins local sources and
the credited imported helpers. Source publication, exact replay and
independent review are distinct statuses.
