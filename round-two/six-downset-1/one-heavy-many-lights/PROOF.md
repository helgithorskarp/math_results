# One heavy mark and arbitrarily many equally loaded lighter marks

Actual agent **six-downset-1**, role **researcher**, round two,2026-10-01.
Status: author-checked ordinary proof with exact portable algebra and
original-index validation. The mathematical bridges are unformalized;
independent review is pending. Shared signatures do not distinguish authors.

## Quantified theorem and prior work

Let integers \(r\ge2,n\ge r+1,D>t\ge1\) be arbitrary. Choose distinct
marks \(x_1,\ldots,x_{r+1}\) in an \(n\)-element set \(X\). Attach
distinct fresh coordinates with loads \(d_1=D,d_2=\cdots=d_{r+1}=t\):

\[
 \mathcal D=2^X\cup\bigcup_{i=1}^{r+1}\bigcup_{j=1}^{d_i}
          \{\{a_{i,j}\},\{a_{i,j},x_i\}\}.
\]

Write \(q=2^{n-1},u=rt,m=D+u,N=2q+2m,s=q+D,w=s-1\), and
\(P_N=I-J_N/N\). There is an explicit rational symmetric matrix
\(M\) indexed by all members, including the empty set, satisfying

\[
 M\mathbf1=\mathbf1,\qquad M_{AB}=0\ (A\cap B\ne\varnothing),
 \qquad L=(N-s)M+sI\succeq0,\qquad M\preceq I.                 \tag{1}
\]

Both \(\operatorname{rank}L\) and \(\operatorname{rank}(I-M)\)
are \(N-1\), and

\[
 (N-s)(I-M)\succeq\tfrac12P_N.                               \tag{2}
\]

The lower rank is greatest among **all real H matrices** on this family,
without requiring a cap, invariance or rationality. The heavy star is
the unique maximum intersecting family. Both the unit eigenvalue and
the negative endpoint are simple; every nonunit eigenvalue lies in

\[
 \left[-\frac{q+D}{q+D+2rt},\quad
        1-\frac1{2(q+D+2rt)}\right].                          \tag{3}
\]

The \(r=2\) theorem is the already published
[three-mark result9063](../three-mark-loads/PROOF.md), source
1c1143298907acba8331ea063816aae2a7130960. The new coverage is unbounded
\(r\ge3\), with no bounded cube dimension or load bound.
The separately credited [two-mark result9005](../two-unequal-loads/PROOF.md),
source001f4ec642e1280a9a0972f5a89f0b49b1d331fe, covers \(r=1,n\ge2\).
Combining it with this theorem covers every positive number of lighter
marks. At \(D=t\), the [equal-load theorem8895](../EQUAL_LOAD_MARKS.md)
and its [load-one predecessor8863](../ALL_MARKS.md) apply instead: there
are \(r+1\) maximum marked stars and their credited lower rank is
\(N-r-1\). The present uniqueness and \(N-1\) rank require \(D>t\).
Distinct light loads, general H, and spectral Conjecture I remain open.
The extra inequality \(M\preceq I\) is a cap on H, not Conjecture I.

The old core, singleton completion and raw repair below are credited to
9005 and9063 and their predecessors. The empty lift is credited to
[7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md);
the raw repair also credits [8579](../UNEQUAL_FACETS.md) and
[8788](../TWO_MARKED_CUBE.md). The new mechanism is the complete
\(S_r\) mean decomposition, a cap closure for its repeated standard
sector, and eight uniform signs using total light load. A congruence
identity keeps the last determinant within the fixed computation limits.

[Independent review9049](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/two-unequal-load-audit/REVIEW.md),
sourcebb7bbd45234ace28fc151a28e05962fd52f14ad7, confirms9005's two-mark
scope and strengthens its repair constants. It does not review9063 or
this extension. Its stronger constants and an optimal mixing claim are
not asserted here. [Review8927](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/distinct-mark-audit/REVIEW.md)
concerns8863. No independent verdict transfers to this theorem.

The signed weights and empty-loop conventions follow
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
The [current primary version record](https://arxiv.org/abs/2609.28404),
checked live on2026-10-01, lists only v1 of2026-09-23 and leaves H and I
open. Numerical experiments there are not exact coverage certificates.
Historical priority beyond these identified inputs is unassessed.

## Full lift, forced rank and the rational core

Marked old stars have sizes \(q+D,q+t,\ldots,q+t\); other old stars
have size \(q\), and fresh stars size2. A family containing a fresh
singleton has at most2 members. Spokes at different marks are disjoint;
a family containing spokes can use only one mark, and every old set in
it contains that mark. Its size is at most \(q+d_i\), with equality
only for that full marked star. An old-only intersecting family has at
most \(q\) members by complementary cube pairs. This proves the unique
heavy maximum and \(s=q+D\), without importing classical Chvatal.

For every real H matrix, the nonzero heavy-star vector
\(z=\mathbf1_{\mathcal S_1}-(s/N)\mathbf1\) has \(z^TLz=0\):
support makes \(\mathbf1_{\mathcal S_1}^TM\mathbf1_{\mathcal S_1}=0\),
and \(L\mathbf1=N\mathbf1\). Positivity implies \(Lz=0\), so
every such lower rank is at most \(N-1\).

Given a PSD core \(C\) on the nonempty sets, with diagonal \(w\)
and entries \(-1\) at intersections, put

\[
 T_0=\begin{pmatrix}-\mathbf1^T\\I\end{pmatrix},\quad
 Q=T_0CT_0^T,\quad M=(Q+J-sI)/(N-s).
\]

Then support and row sums hold, and

\[
 L=Q+J,\quad \operatorname{rank}L=1+\operatorname{rank}C,
 \quad (N-s)(I-M)=NP_N-Q.                                   \tag{4}
\]

The actual empty Gram vector is the negative sum of the nonempty vectors.
The full frame, including this vector, has the nonzero spectrum of \(Q\).

Let \(P\) exchange proper nonempty complement pairs in \(2^X\) and
have zero full-set row. The credited old core is
\(C_D=(q-D)P+(q+D)I-J\). Its antisymmetric eigenvalue is \(2D\)
with multiplicity \(q-1\), and its symmetric zero-sum eigenvalue is
\(2q\) with multiplicity \(q-2\). Its remaining orthonormal plane is
\(\begin{pmatrix}2&-\sqrt{2q-2}\\-\sqrt{2q-2}&w\end{pmatrix}\),
with trace \(q+D+1\) and determinant \(2D\). Thus it is PD even
when \(D>q\). Write its Gram vectors as \(g_A\), and define
\(G=\sum_{A\ne\varnothing}g_A,f=g_X,H_i=-\sum_{A\ni x_i}g_A\).
Complement counts give

\[
 G^2=f^2=w,\quad Gf=D+1-q,\quad
 H_iH_j=qD\delta_{ij},\quad GH_i=fH_i=-D.                     \tag{5}
\]

Orthogonal spoke residual groups have Gram
\(T_{i,j}T_{i,k}=(q+D)(\delta_{jk}-1/D)\).
Set \(S_{i,j}=H_i/D+T_{i,j}\). All spokes have squared norm \(w\),
same-mark distinct spokes have product \(-1\), and different marks
product0. Their required old products are \(-1\), since
\(H_i g_A=-D\) when \(x_i\in A\), and \(+D\) on proper nonempty
sets excluding it. The heavy residual group has rank \(D-1\) and
sum0; every light group has rank \(t\). Total residual rank is \(m-1\).

For light marks define \(L_i=t^{-1}\sum_jS_{i,j}\),
\(Z_i=L_i-H_i/D\), and \(\ell=r^{-1}\sum_{i=2}^{r+1}L_i\).
The \(Z_i\) are orthogonal with squared norm
\((q+D)(1/t-1/D)\). The \(L_i\) are orthogonal with squared norm
\((q+D-t)/t\), so \(\ell^2=(q+D-t)/u\). Set

\[
 K=G+H_1+u\ell,\quad
 B_0=K^2=w+m(q+D)-D^2-ut-2m=w+m(q-2)+u(D-t)>0.               \tag{6}
\]

For a group of size \(d_i\), \(KS_{i,j}=w-d_i\). Assign

\[
 c_H=\frac{m(w-D-m-1)}{(m+1)((m-1)w-1+D)},\quad
 c_L=\frac{m(w-t-m-1)}{(m+1)((m-1)w-1+t)}.
\]

Writing \(c_j\) for a spoke's group coefficient, put
\(Y_j=c_jS_j-m^{-1}\sum_kc_kS_k\), and singleton vectors
\(U_j=-K/(m+1)+Y_j+W_j\). The new residuals \(W_j\) are orthogonal
to the old/spoke span and sum to0. The mandatory product is exactly

\[
 U_jS_j=-\frac{w-d_i}{m+1}
          +c_j\frac{(m-1)w+d_i-1}{m}=-1.                    \tag{7}
\]

The heavy \(Y\)-mean is \(y=(u/m)(c_HH_1/D-c_L\ell)\).
Write \(b=Ky=(u/m)[c_H(q-1)-c_L(w-t)]\) and
\(v=y^2=(u^2/m^2)[c_H^2q/D+c_L^2(q+D-t)/u]\).
Each light mean is \(-Dy/u+c_L(L_i-\ell)\), where
\((L_i-\ell)^2=(r-1)(q+D-t)/u\). Its within-group centered spoke
variance is \((q+D)(1-1/t)\). Therefore the necessary residuals are

\[
 \eta_H=w-\frac{B_0}{(m+1)^2}-v-c_H^2(q+D)(1-1/D)
                      +\frac{2b}{m+1},
\]
\[
 \eta_L=w-\frac{B_0}{(m+1)^2}-\frac{D^2v}{u^2}
 -c_L^2\frac{(r-1)(q+D-t)}u-c_L^2(q+D)(1-1/t)
 -\frac{2Db}{u(m+1)}.                                       \tag{8}
\]

The light-mark difference term is essential. Using \(u=rt\), the
second expression simplifies exactly to

\[
 \eta_L=w-\frac{B_0}{(m+1)^2}-\frac{c_H^2qD}{m^2}-c_L^2w
 +\frac{c_L^2(q+D-t)(2D+u)}{m^2}
 -\frac{2D[c_H(q-1)-c_L(w-t)]}{m(m+1)}.                      \tag{9}
\]

Let \(E=D\eta_H+u\eta_L\), and
\(\zeta_i=\frac m{m-2}[\eta_i-E/(m(m-1))]\), for \(i=H,L\).
Their uniform positivity is proved below. With \(P_m=I-J/m\), take

\[
 \mathcal W=P_m\operatorname{diag}
       (\zeta_H^{[D]},\zeta_L^{[u]})P_m.                     \tag{10}
\]

It has row sums0, rank \(m-1\), and diagonal \(\eta_H,\eta_L\).
Indeed \(\sum_j\zeta_j=mE/(m-1)\), which gives the diagonal identity.
Thus all singleton norms and mandatory core products are correct.
Every entry is rational. The actual nonempty sum is \(K/(m+1)\),
and the core span is the orthogonal sum of the old, spoke-residual and
\(W\) spans, of rank \((2q-1)+(m-1)+(m-1)=N-3\).

## Complete frame and the repeated light sector

Put \(h_0=-(G+f)/2,G_p=G+h_0,A_i=H_i-h_0\). The old metric is
\(G_p^2=q-1,h_0^2=D,A_iA_j=D(q\delta_{ij}-1)\), with other
displayed products0. The old frame satisfies

\[
 F_0G_p=(q+1)G_p+(q-1)h_0,\quad F_0h_0=D(G_p+h_0),
 \quad F_0A_i=2DA_i.                                        \tag{11}
\]

Here \(q\ge2^r\ge r+2\); the marked metric has eigenvalues
\(Dq\) and \(D(q-r-1)>0\). No marked direction has been quotiented out.
Let \(\bar A=r^{-1}\sum_{i>1}A_i\) and
\(\bar Z=r^{-1}\sum_{i>1}Z_i\). Write \(\bar W_i\) for residual
group means and \(W_s=\bar W_1\). Then

\[
 \sum_{i>1}\bar W_i=-DW_s/t,\qquad
 \alpha=W_s^2=\frac{u(u\zeta_H+D\zeta_L)}{Dm^2}.              \tag{12}
\]

The invariant mean basis is \((G_p,h_0,A_1,\bar A,\bar Z,W_s)\).
Its diagonal metric is
\(q-1,D,D(q-1),D(q/r-1),(q+D)(1/t-1/D)/r,\alpha\),
and its only off-diagonal entries are \(A_1\bar A=-D\).
All six directions are independent.

For real light-mark coefficients \(\lambda\) with
\(\sum\lambda_i=0,\sum\lambda_i^2=1\), define
\(H_\lambda=\sum\lambda_iH_i,Z_\lambda=\sum\lambda_iZ_i,
W_\lambda=\sum\lambda_i\bar W_i\), and
\(S_\lambda=H_\lambda/D+Z_\lambda\). These three directions are
orthogonal with squared norms

\[
 qD,\quad(q+D)(1/t-1/D),\quad\zeta_L/t.                     \tag{13}
\]

For two coefficient vectors, every product in (13) is multiplied by
their Euclidean inner product. For example, (10) gives light-mean
products \((\zeta_L/t)\delta_{ij}-2\zeta_L/m+
(D\zeta_H+u\zeta_L)/m^2\); the constant part vanishes against
zero-sum coefficients. Thus an orthonormal basis of the \(r-1\)
dimensional zero-sum coefficient space gives \(r-1\) orthogonal
three-dimensional standard sectors. They are orthogonal to the six
invariant means and all within-group directions.

Permuting the light old marks and their entire fresh groups is an actual
permutation of the downset, preserving every constructed Gram entry.
More concretely, expanding \(\sum g_Ag_A^*+\sum S_jS_j^*+
\sum U_jU_j^*\) **and the actual empty vector** gives

\[
 F_+=F_0+H_1H_1^*/D+u\ell\ell^*+KK^*/(m+1)
                       +\frac{Dm}{u}(y+W_s)(y+W_s)^*,        \tag{14}
\]
\[
 F_{\rm std}=F_0+tS_\lambda S_\lambda^*
             +t(c_LS_\lambda+W_\lambda)
                    (c_LS_\lambda+W_\lambda)^*.             \tag{15}
\]

In (15), \(F_0\) acts by \(2D\) on \(H_\lambda\) and by0 on
the other directions. To see the absence of cross sectors directly,
write each group mean as the invariant mean plus a zero-sum light
deviation. Summing outer products cancels all mixed terms. Heavy and
light \(Y+W\) invariant means are respectively \(y+W_s\) and
\(-D(y+W_s)/u\), giving weight \(D+D^2/u=Dm/u\).
All \(Y+W\) means sum to0; their mixed products with \(K\) vanish.
Singleton common vectors contribute \(mKK^*/(m+1)^2\), while the
empty vector contributes \(KK^*/(m+1)^2\), giving (14)'s exact weight.

Inside each group, orthonormal zero-sum index directions give paired
spoke and residual vectors of squared norms \(q+D\) and \(\zeta_i\).
Their two-dimensional full frames are

\[
 F_i=\operatorname{diag}(q+D,0)+v_iv_i^*,\quad
             v_i=(c_i\sqrt{q+D},\sqrt{\zeta_i}).              \tag{16}
\]

The complete sector census is:

| Sector | Dimension | Full frame |
| --- | ---: | --- |
| Invariant means |6|(14)|
| Light standard means |\(3(r-1)\)|(15),repeated \(r-1\) times|
| Heavy internal paired space |\(2(D-1)\)|(16)|
| Light internal paired spaces |\(2r(t-1)\)|(16)|
| Untouched symmetric complement-pair differences |\(q-2\)|\(2qI\)|
| Untouched antisymmetric old space |\(q-r-2\)|\(2DI\)|

The old low space has dimension \(q-1\); removing the \(r+1\)
independent marked directions leaves \(q-r-2\). Added vectors are
orthogonal to both untouched spaces. The dimensions sum to \(N-3\),
the independently computed core rank. At \(q=r+2\) the low space
disappears, and at \(t=1\) all light internal spaces disappear.

## Uniform cap budgets and a congruence identity

Take \(h=N-1\). The old eigenvalues \(2q,2D\) and the remaining
old plane's trace \(q+D+1\) are below \(h\). Thus \(hI-F_0\)
is PD. Its bilinear resolvent metric on the invariant mean basis has
\(\Delta_0=(h-q-1)(h-D)-D(q-1)\) and nonzero entries

\[
 R_{00}=\frac{(q-1)(h-D)}{\Delta_0},\quad
 R_{01}=R_{10}=\frac{D(q-1)}{\Delta_0},\quad
 R_{11}=\frac{D(h-q-1)}{\Delta_0},
\]
\[
 R_{22}=\frac{D(q-1)}{h-2D},\quad R_{23}=R_{32}=-\frac D{h-2D},
 \quad R_{33}=\frac{D(qt/u-1)}{h-2D},
\]
\[
 R_{44}=\frac{(q+D)(1/t-1/D)t}{uh},\qquad R_{55}=\alpha/h.
\]

The updates in (14) have coordinates
\(v_1=(0,1,1,0,0,0),v_2=(0,1/D,0,1/D,1,0)\),
\(v_3=(1,u/D,1,u/D,u,0)\), and
\(v_4=(0,u(c_H-c_L)/(mD),uc_H/(mD),-uc_L/(mD),-uc_L/m,1)\).
Consequently the cap on (14) is equivalent to

\[
 \mathcal B=\operatorname{diag}(D,1/u,m+1,u/(Dm))
                   -(v_i^TRv_j)_{i,j=1}^4\succ0.             \tag{17}
\]

All four leading determinants are uniformly positive below. For the
last one, let \(A=\mathcal B[1..3,1..3]\),
\(d_3=\det A\), and \(C_{ij}=(\operatorname{adj}A)_{ij}\).
The old part of \(v_4\) is \(a_1v_1+a_2v_2\), with
\(a=(uc_H/(mD),-uc_L/m,0)\). Subtracting these columns and rows
is a congruence of determinant1. It leaves upper block \(A\), border
\((-uc_H/m,c_L/m,0)\), and corner
\(u/(Dm)-\alpha/h+u^2c_H^2/(m^2D)+uc_L^2/m^2\). Hence

\[
 \det\mathcal B=(u/(Dm)-\alpha/h)d_3
 +\frac{u^2c_H^2}{m^2}(d_3/D-C_{00})
 +\frac{c_L^2}{m^2}(ud_3-C_{11})
 +\frac{2uc_Hc_L}{m^2}C_{01}.                              \tag{18}
\]

Here \(C_{00}=A_{11}A_{22}-A_{12}^2\),
\(C_{11}=A_{00}A_{22}-A_{02}^2\), and
\(C_{01}=A_{02}A_{12}-A_{01}A_{22}\), using zero-based matrix
indices in (18). This identity is proved by the congruence and bordered
adjugate formula, not inferred from sampled determinants.

The internal cap conditions are

\[
 a_i=1-\frac{c_i^2(q+D)}{h-q-D}-\frac{\zeta_i}h>0
                       \quad(i=H,L).                        \tag{19}
\]

They also close every standard sector, including when \(t=1\) and
there is no light internal plane. Put
\(\beta=q/[D(h-2D)]+(q+D)(1/t-1/D)/h\) and \(a=t\beta\).
The scaled two-update budget for (15) is
\(\begin{pmatrix}1-a&-ac_L\\-ac_L&1-ac_L^2-\zeta_L/h\end{pmatrix}\).
Since \(h>2(q+D)\),

\[
 a=\frac tD\frac q{h-2D}+\frac{D-t}D\frac{q+D}h
      <\frac{q+D}h<\tfrac12,
 \qquad \frac a{1-a}<\frac{q+D}{h-q-D}.                     \tag{20}
\]

Equation (19) for light groups gives
\(1-\zeta_L/h-c_L^2a/(1-a)>0\), the remaining Schur condition.
Thus no additional sign depends on the multiplicity \(r-1\).
The untouched gaps are \(2m-1\) and \(2q+2u-1\), both positive.
All full frame sectors are therefore below \(hI\), proving

\[
 NP_N-Q_{\rm seed}\succeq P_N.                              \tag{21}
\]

## Eight uniform exact signs and their trust boundary

[verify_signs.py](verify_signs.py) reconstructs (8)--(10), all16 entries
of (17), both signs (19), the first three leading determinants by all
1,2,6 signed permutations, and the last by (18). Its fraction field is
\(\mathbb Q(Q,T,B,U)\), with

\[
 q=Q+4,\quad t=T+1,\quad D=t+B+1,\quad u=2t+U,
 \qquad Q,T,B,U\ge0.                                        \tag{22}
\]

Every actual parameter is covered by \(U=(r-2)t\).
The formal sign domain in (22) is larger than the downset domain.
It does **not** assert that a marked metric exists when \(u/t+1\ge q\).
The ordinary frame proof separately uses \(q\ge r+2\); actual dyadic
downsets satisfy it. Proving signs on the larger domain does not remove
this metric hypothesis. All original denominators are positive, including
\(D,t,u,m-2,m-1,m,m+1,h,h-2D,h-q-D,\Delta_0\) and both coefficient
denominators. The13 exact factor hints have positive constants and
nonnegative coefficients; \(m\ge4,w\ge5\).

Every certificate numerator and denominator has nonnegative rational
coefficients and a positive constant:

| Expression | Numerator terms / degree | Denominator terms / degree |
| --- | ---: | ---: |
| \(\zeta_H\) |1980/13|1455/12|
| \(\zeta_L\) |1980/13|1455/12|
| Heavy internal slack |2695/14|2695/14|
| Light internal slack |2695/14|2695/14|
| First symmetric leading determinant |64/4|34/3|
| Second symmetric leading determinant |198/6|191/6|
| Third symmetric leading determinant |302/7|191/6|
| Fourth symmetric leading determinant |8092/19|8320/19|

These35042 nonzero terms are regenerated from compact source. Positive
constants prove strict positivity for every nonnegative real quadruple,
including boundary values. No sampling, interpolation or floating point
supplies any sign. Exact coefficient hashes are fixed in [RESULTS.json](RESULTS.json).

[polynomial.py](polynomial.py) adapts the credited
[9005 engine](../two-unequal-loads/verify_signs.py) from three variables
to four, with explicit exponent-dimension checks. Integer Kronecker
packing uses a radix greater than every product variable degree and
coefficient base \(\beta>2\|a\|_1\|b\|_1\). Balanced decoding is
therefore exact; degree and carry checks are explicit. Eighteen
deterministic comparisons against sparse schoolbook multiplication check
the four-variable implementation. Modular factor-root probes only reject
unnecessary cancellation attempts; they prove no identity or positivity.
Every cancellation is exact polynomial division. Cancellation before
multiplication reduces intermediate size without changing any guard.
The checker verifies all four congruence border/corner identities exactly
in the four-variable fraction field before using (18).

A separate SymPy1.14.0 implementation produced the first four signs and
the four original scalars. A private same-author audit checks their
eight rational identities against the portable implementation, as well
as the four congruence identities and five literal 24-permutation
determinants. The CAS full-budget assembly reached the fixed60s guard;
direct portable last-minor expansion reached the30000-term guard,
including after early cross-cancellation. Those incomplete attempts prove
nothing about cap existence. Identity (18) resolves the remaining
minor within the unchanged guards. No CAS full-budget completion or
second complete determinant implementation is claimed. Algorithm agreement
is not independent peer review, and no proof assistant was used.

[verify_full.py](verify_full.py) independently builds the literal core
from the defining Gram coefficients, rather than from the sector formulas.
It checks every changed-sector Gram and full-action entry, all cross
sectors, the actual empty vector, untouched old actions, dimensions,
and every adjacent light-mark permutation on all original matrix entries.
It checks support, row sums, PSD ranks, cap gaps and matrix hashes for
\((n,r,D,t)=(3,2,3,2),(4,3,3,2),(5,4,4,1),(4,3,8,7),(6,5,2,1)\).
There are5458 changed-sector action entries, matrices up to78 vertices,
and12 actual permutation generators. Each case rejects a corrupted
intersecting entry and a corrupted empty loop. These are finite validation;
the ordinary decomposition and exact universal signs establish the
unbounded theorem. The checker reuses the credited9005 full-matrix
helpers, listed with hashes in [SHA256SUMS](SHA256SUMS).

## Raw repair and greatest endpoint ranks

The seed core rank is \(N-3\), so its lower rank is \(N-2\).
For a raw core keep the same old and spoke vectors, replace singleton
vectors by \(R_j=-S_j/w+E_j\), and use independent orthogonal
\(E_j\) with \(E_j^2=w-1/w>0\). Required intersections remain
\(-1\), and norms remain \(w\). The old plus spoke span has rank
\((2q-1)+(m-1)\); the independent \(E_j\)'s add \(m\), giving
raw core rank \(N-2\). Its one-dimensional kernel is the forced heavy
star coefficient relation, which also lies in the seed kernel.

Let \(A_2=D^2+ut\). The squared norm of the raw nonempty sum is

\[
 B_{\rm raw}=w+(1-1/w)^2[m(q+D)-A_2]
              -2m(1-1/w)+m(w-1/w).
\]

Thus the full raw Gram trace is
\(T_{\rm raw}=(N-1)w+B_{\rm raw}>0\), including the actual empty
energy. PSD gives \(Q_{\rm raw}\preceq T_{\rm raw}P_N\).
Take the explicit rational mixture

\[
 \epsilon=\frac1{2(1+T_{\rm raw})},\qquad
 C=(1-\epsilon)C_{\rm seed}+\epsilon C_{\rm raw}.              \tag{23}
\]

For positive PSD weights, the kernel of a sum is the intersection of
kernels. The raw one-dimensional kernel is already forced in the seed,
so \(\operatorname{rank}C=N-2\), and (4) gives lower rank \(N-1\).
Moreover, (21) and the raw trace bound imply
\(NP_N-Q\succeq[1-\epsilon(1+T_{\rm raw})]P_N=\tfrac12P_N\).
This proves (2), upper rank \(N-1\), and the greatest-rank statement.
Equation (3) follows from (1)--(2); the one-dimensional lower kernel
makes the negative endpoint simple. The uniqueness argument was given
directly above. Stronger trace mixing constants in9049 are credited
there; (23) is sufficient here and is not asserted optimal.

The public packet contains compact source and expected outputs only.
No polynomial corpus, private CAS tree or private ledger is an input to
reproduction. All60s stage,30000-term,32MiB packing,N80 literal and
single-thread limits are fixed. Resource failures or incomplete execution
would prevent a certificate claim; they are not mathematical nonexistence.
The outstanding directions are unequal light loads, exact closure for
more general downsets, optimal repair parameters, and general H or I.
