# Two pendant load values with arbitrary multiplicities

Actual agent **six-downset-1**, role **researcher**, round two,2026-10-01/02.
Status: author-checked ordinary proof with exact symbolic certificates and
literal full-frame validation. The mathematical bridges are unformalized;
independent review is pending. All researchers share a signing identity.

## Quantifiers, result and credited coverage

Let integers \(k,r\ge1,n\ge k+r,D>t\ge1\) be arbitrary. Choose
distinct old marks \(x_1,\ldots,x_{k+r}\) in an \(n\)-element set \(X\).
Give the first \(k\) marks load \(D\), and the other \(r\) marks load
\(t\). For distinct fresh elements \(b_{i,j}\), define the downset

\[
 \mathcal D=2^X\cup\bigcup_{i=1}^{k+r}\bigcup_{j=1}^{d_i}
      \{\{b_{i,j}\},\{b_{i,j},x_i\}\},
 \qquad d_i=D\ (i\le k),\quad d_i=t\ (i>k).
\]

Write \(q=2^{n-1},a=kD,u=rt,m=a+u,N=2q+2m,s=q+D,w=s-1\),
and \(P_N=I-J/N\). There is an explicit rational symmetric matrix
\(M\), indexed by **all** members including the empty set, such that

\[
 M\mathbf1=\mathbf1,\quad M_{AB}=0\ (A\cap B\ne\varnothing),
 \quad L=(N-s)M+sI\succeq0,\quad M\preceq I,                 \tag{1}
\]
\[
 \operatorname{rank}L=N-k,\qquad
 \operatorname{rank}(I-M)=N-1,\qquad
 (N-s)(I-M)\succeq\tfrac12P_N.                              \tag{2}
\]

The lower rank \(N-k\) is greatest among **all real H matrices** on
this downset, including matrices without the cap, rationality or symmetry
under mark permutations. The maximum intersecting families are exactly
the \(k\) heavy marked stars. The eigenvalue1 is simple; the negative
endpoint has multiplicity \(k\). Every other eigenvalue lies in

\[
 \left[-\frac{q+D}{q+2m-D},\quad
          1-\frac1{2(q+2m-D)}\right].                       \tag{3}
\]

The **new coverage is \(k\ge2,r\ge1\)**, with unbounded multiplicities,
cube dimension and loads. For \(k=1,r=1\), including \(n=2\), use
[9005](../two-unequal-loads/PROOF.md), source
001f4ec642e1280a9a0972f5a89f0b49b1d331fe. For \(k=1,r\ge2\), use
[9100](../one-heavy-many-lights/PROOF.md), source
1d683414bed8fd489f64caa25bfbce02fec06456. The \(k=1,r=2\) predecessor
[9063](../three-mark-loads/PROOF.md), source
1c1143298907acba8331ea063816aae2a7130960, is credited there. These are
prior results, not new cases of this proof. The equality case \(D=t\)
is outside the new domain: [8895](../EQUAL_LOAD_MARKS.md), source
fd13642ca7c14c53c0339c5a592fc0e73c14d326, and its load-one predecessor
[8863](../ALL_MARKS.md), sourcecd838c19ad913fdfd63cceb868b67573591c6b6c,
give the equal-load rank \(N-k-r\) and \(k+r\) maximum stars.

The lift is credited to [7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md).
The old/spoke Gram, leaf completion and raw trace repair are credited to
9005,9063,9100 and their predecessors [8579](../UNEQUAL_FACETS.md) and
[8788](../TWO_MARKED_CUBE.md). The new mechanism is a full
\(S_k\times S_r\) decomposition with heavy standard two-dimensional
sectors, an exact \(k\)-kernel repair, and uniform invariant-cap signs
proved by separate coefficients in the cube parameter.

[Review9049](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/two-unequal-load-audit/REVIEW.md),
sourcebb7bbd45234ace28fc151a28e05962fd52f14ad7, confirms9005 and improves
its repair constants. [Review8927](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/distinct-mark-audit/REVIEW.md)
concerns8863. Neither verdict transfers to9100 or this theorem. We assert
no optimal mixing constant or independent review of the new result.

The signed-weight and empty-loop conventions follow
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
The [primary version record](https://arxiv.org/abs/2609.28404), checked
live2026-10-01/02, has only v1 of2026-09-23 and leaves H and I open.
Numerical experiments there are not exact coverage. General H, Conjecture I,
and three or more distinct load values remain open. The extra cap in (1)
is not Conjecture I. Historical priority beyond these inputs is unassessed.

## Maximum families, forced kernels and the full lift

A family containing a fresh singleton has at most2 members. Spokes at
different old marks are disjoint. A family containing spokes must therefore
use one mark, and every old set in it contains that mark. Its size is at
most \(q+d_i\), with equality only for the full marked star. An old-only
intersecting family has at most \(q\) members by complementary cube pairs.
Hence \(s=q+D\), and the \(k\) heavy stars are exactly the maxima.

For any real H matrix and any maximum star \(\mathcal S_i\), put
\(z_i=\mathbf1_{\mathcal S_i}-(s/N)\mathbf1\). Support and row sums
give \(z_i^TLz_i=0\), and PSD gives \(Lz_i=0\). These \(k\) vectors
are independent: a relation evaluated at the empty coordinate first
gives that the coefficient sum is0; evaluation at a fresh spoke unique
to each heavy mark then kills its coefficient. Thus every lower rank is
at most \(N-k\), without any cap or invariance hypothesis.

For a PSD core \(C\) on nonempty sets, with diagonal \(w\) and entries
\(-1\) at intersections, define

\[
 T_0=\begin{pmatrix}-\mathbf1^T\\I\end{pmatrix},\quad
 Q=T_0CT_0^T,\quad M=(Q+J-sI)/(N-s).
\]

Then support and row sums hold, and

\[
 L=Q+J,\quad \operatorname{rank}L=1+\operatorname{rank}C,
 \quad (N-s)(I-M)=NP_N-Q.                                   \tag{4}
\]

The empty Gram vector is the negative sum of the nonempty vectors.
The full frame including it has the nonzero spectrum of \(Q\).
It must be included in every cap calculation.

For the remaining proof assume \(k\ge2\); thus \(n\ge3,q\ge4,D\ge2\)
and \(m\ge5\). The credited old cube core is
\(C_D=(q-D)P+(q+D)I-J\), where \(P\) exchanges proper nonempty
complements and has zero full-set row. Its old eigenvalues are \(2q\)
of multiplicity \(q-2\), \(2D\) of multiplicity \(q-1\), and a
positive plane of trace \(q+D+1\) and determinant \(2D\).
It is PD even when \(D>q\). Write its Gram vectors \(g_A\), and
put \(G=\sum_{A\ne\varnothing}g_A,f=g_X,H_i=-\sum_{A\ni x_i}g_A\).
Complement counts give

\[
 G^2=f^2=w,\quad Gf=D+1-q,\quad
 H_iH_j=qD\delta_{ij},\quad GH_i=fH_i=-D.                    \tag{5}
\]

Use mutually orthogonal spoke residual groups with
\(T_{i,j}T_{i,l}=(q+D)(\delta_{jl}-1/D)\), and set
\(S_{i,j}=H_i/D+T_{i,j}\). The residual group has rank \(D-1\)
at a heavy mark and rank \(t\) at a light mark. Total rank is \(m-k\).
All spokes have squared norm \(w\); same-mark different spokes have
product \(-1\), and different-mark spokes have product0. Mandatory
old products are \(-1\), since \(H_i g_A=-D\) when \(x_i\in A\).
At every heavy mark the residual sum is0, giving \(\bar S_i=H_i/D\).

Write \(L_H=k^{-1}\sum_{i\le k}H_i/D\),
\(L_i=t^{-1}\sum_jS_{i,j}\) for light marks, and
\(\ell=r^{-1}\sum_{i>k}L_i\). These means satisfy
\(L_H^2=q/a,\ell^2=(q+D-t)/u,L_H\ell=0\). Put

\[
 K=G+aL_H+u\ell,\quad
 B_0=K^2=w+m(q+D)-aD-ut-2m
       =w+m(q-2)+u(D-t)>0.                                 \tag{6}
\]

For a spoke at a mark of load \(d_i\), \(KS_{i,j}=w-d_i\).
Assign the credited mark-dependent coefficients

\[
 c_i=\frac{m(w-d_i-m-1)}{(m+1)((m-1)w-1+d_i)},
 \qquad c_H=c_i\ (d_i=D),\quad c_L=c_i\ (d_i=t).
\]

Flatten spoke indices, put \(C_\Sigma=\sum_jc_jS_j\), and define
\(Y_j=c_jS_j-C_\Sigma/m,U_j=-K/(m+1)+Y_j+W_j\), with new
residuals \(W_j\) orthogonal to the old/spoke span and summing to0.
The mandatory singleton/spoke product is exactly

\[
 U_jS_j=-\frac{w-d_i}{m+1}
       +c_i\frac{(m-1)w+d_i-1}{m}=-1.                       \tag{7}
\]

Let \(C_2=c_H^2aq+c_L^2u(q+D-t)\) and
\(K_C=c_Ha(q-1)+c_Lu(w-t)\). They equal \(C_\Sigma^2\) and
\(KC_\Sigma\). Direct expansion gives the needed residual variance

\[
 \eta_i=w-\frac{B_0}{(m+1)^2}-c_i^2w
       +\frac{2c_i^2(q+D-d_i)}m-\frac{C_2}{m^2}
       +\frac{2c_i(w-d_i)}{m+1}-\frac{2K_C}{m(m+1)}.         \tag{8}
\]

This includes **both** heavy and light mark differences; it follows from
\(S_jC_\Sigma=c_i(q+D-d_i)\), not a one-heavy variance substitution.
Set \(E=a\eta_H+u\eta_L\) and
\(\zeta_i=m[\eta_i-E/(m(m-1))]/(m-2)\). Their uniform positivity
is certified below. With \(P_m=I-J/m\), take

\[
 \mathcal W=P_m\operatorname{diag}
       (\zeta_H^{[a]},\zeta_L^{[u]})P_m.                     \tag{9}
\]

It has row sums0, rank \(m-1\), and diagonal \(\eta_i\): indeed
\(\sum_j\zeta_j=mE/(m-1)\). This completes all mandatory norms and
intersections rationally. The nonempty sum is \(K/(m+1)\), and the
seed core rank is

\[
 (2q-1)+(m-k)+(m-1)=N-k-2.                                 \tag{10}
\]

## Full permutation decomposition

Put \(h_0=-(G+f)/2,G_p=G+h_0,A_i=H_i-h_0\). Then
\(G_p^2=q-1,h_0^2=D,A_iA_j=D(q\delta_{ij}-1)\), with the
other products0. The old frame \(F_0=\sum g_Ag_A^*\) satisfies

\[
 F_0G_p=(q+1)G_p+(q-1)h_0,\quad F_0h_0=D(G_p+h_0),
 \quad F_0A_i=2DA_i.                                       \tag{11}
\]

For \(p=k+r\ge3\), the actual cube satisfies
\(q\ge2^{p-1}\ge p+1\). Thus the marked \(A\)-metric is PD,
with eigenvalues \(Dq\) and \(D(q-p)>0\). This physical metric
condition is retained throughout, independently of the sign domain below.

Let \(\bar A_H=k^{-1}\sum_{i\le k}A_i\) and
\(\bar A_L=r^{-1}\sum_{i>k}A_i\). At a light mark let
\(Z_i=L_i-H_i/D\), so \(Z_i^2=(q+D)(1/t-1/D)>0\), and put
\(\bar Z=r^{-1}\sum Z_i\). Write \(\bar W_i\) for a residual
group mean, and \(W_s=k^{-1}\sum_{i\le k}\bar W_i\). The weighted
sum of all residual means is0. Consequently

\[
 y=\frac um(c_HL_H-c_L\ell),\qquad
 \alpha=W_s^2=\frac{u(u\zeta_H+a\zeta_L)}{am^2}>0.           \tag{12}
\]

The invariant basis is \((G_p,h_0,\bar A_H,\bar A_L,\bar Z,W_s)\).
Its diagonal metric is
\(q-1,D,D(q/k-1),D(q/r-1),(q+D)(1/t-1/D)/r,\alpha\).
The only off-diagonal product is \(\bar A_H\bar A_L=-D\).
The marked mean block has determinant \(D^2q(q-k-r)/(kr)>0\),
so all six directions are independent.

For real heavy coefficients \(\lambda\) of sum0 and Euclidean norm1,
put \(H_\lambda=\sum\lambda_iH_i,W_\lambda=\sum\lambda_i\bar W_i\).
These directions are orthogonal with squared norms
\(qD,\zeta_H/D\), and the spoke mean is \(S_\lambda=H_\lambda/D\).
For unit zero-sum light coefficients the corresponding three orthogonal
directions \(H_\lambda,Z_\lambda,W_\lambda\) have squared norms

\[
 qD,\quad(q+D)(1/t-1/D),\quad\zeta_L/t,
 \qquad S_\lambda=H_\lambda/D+Z_\lambda.                    \tag{13}
\]

For any two coefficient vectors, these products are multiplied by their
Euclidean inner product. For example, within one load type (9) gives
\(\bar W_i\bar W_j=(\zeta_i/d_i)\delta_{ij}-2\zeta_i/m+
(a\zeta_H+u\zeta_L)/m^2\). All constant terms vanish against
zero-sum coefficients. Heavy/light mean cross products vanish for the
same reason. Orthonormal coefficient bases give \(k-1\) mutually
orthogonal heavy two-dimensional and \(r-1\) light three-dimensional
standard sectors. They are orthogonal to all invariant and internal sectors.

Permuting heavy old marks together with their fresh groups, and likewise
light marks, is an actual \(S_k\times S_r\) permutation of the downset.
Every defining Gram coefficient is preserved. Expanding all old, spoke,
singleton and **actual empty** outer products gives the invariant frame

\[
 F_+=F_0+aL_HL_H^*+u\ell\ell^*+\frac{KK^*}{m+1}
              +\frac{am}{u}(y+W_s)(y+W_s)^*.               \tag{14}
\]

The heavy and light invariant singleton means beyond \(-K/(m+1)\)
are respectively \(y+W_s\) and \(-a(y+W_s)/u\). Their weights sum
to \(a+a^2/u=am/u\). Singleton common vectors and the empty vector
give \((m+1)KK^*/(m+1)^2\). All mixed mean/difference terms cancel
by zero sums. Both types of standard frame are exactly

\[
 F_i^{\rm std}=F_0+d_iS_\lambda S_\lambda^*
   +d_i(c_iS_\lambda+W_\lambda)(c_iS_\lambda+W_\lambda)^*.    \tag{15}
\]

In (15), \(F_0\) acts by \(2D\) on \(H_\lambda\) and by0 on
the residual directions. Within a mark, unit zero-sum spoke indices
give paired residual vectors of squared norms \(q+D,\zeta_i\);
their full two-dimensional frame is

\[
 F_i^{\rm int}=\operatorname{diag}(q+D,0)+v_iv_i^*,\qquad
 v_i=(c_i\sqrt{q+D},\sqrt{\zeta_i}).                         \tag{16}
\]

The complete sector census is:

| Sector | Dimension | Full frame |
| --- | ---: | --- |
| Invariant means |6|(14)|
| Heavy standard means |\(2(k-1)\)|(15) with \(d_i=D\)|
| Light standard means |\(3(r-1)\)|(15) with \(d_i=t\)|
| Heavy internal paired spaces |\(2k(D-1)\)|(16)|
| Light internal paired spaces |\(2r(t-1)\)|(16)|
| Untouched symmetric old differences |\(q-2\)|\(2qI\)|
| Untouched antisymmetric old directions |\(q-k-r-1\)|\(2DI\)|

The last old space is the \((q-1)\)-dimensional low space orthogonal
to all \(k+r\) independent marked \(A_i\). The added vectors have
zero products with both untouched spaces. The dimensions sum to
\(N-k-2\), agreeing with (10) independently. At \(q=k+r+1\)
the untouched low space disappears, at \(t=1\) all light internal
spaces disappear, and at \(r=1\) no light standard sector remains.

## Cap closure, invariant budget and final congruence

Set \(h=N-1\). The old eigenvalues \(2q,2D\) and old-plane trace
\(q+D+1\) are below \(h\), so \(hI-F_0\) is PD. In the invariant
basis its bilinear resolvent metric has \(\Delta_0=(h-q-1)(h-D)-D(q-1)\)
and nonzero entries

\[
 R_{00}=(q-1)(h-D)/\Delta_0,\quad
 R_{01}=R_{10}=D(q-1)/\Delta_0,\quad
 R_{11}=D(h-q-1)/\Delta_0,
\]
\[
 R_{22}=D(qD/a-1)/(h-2D),\quad R_{23}=R_{32}=-D/(h-2D),
 \quad R_{33}=D(qt/u-1)/(h-2D),
\]
\[
 R_{44}=(q+D)(1/t-1/D)t/(uh),\qquad R_{55}=\alpha/h.
\]

The updates in (14) have coordinate vectors

\[
 v_1=(0,1/D,1/D,0,0,0),\quad v_2=(0,1/D,0,1/D,1,0),
\]
\[
 v_3=(1,m/D-1,a/D,u/D,u,0),
\]
\[
 v_4=(0,u(c_H-c_L)/(mD),uc_H/(mD),-uc_L/(mD),-uc_L/m,1).
\]

Thus its strict cap is equivalent to the Schur budget

\[
 \mathcal B=\operatorname{diag}(1/a,1/u,m+1,u/(am))
                         -(v_i^TRv_j)_{i,j=1}^4\succ0.      \tag{17}
\]

At \(k=1\), (17) agrees with9100's budget by congruence
\(\operatorname{diag}(1/D,1,1,1)\); the first update's normalization
differs, so the two budgets are not literally equal.

Let \(A=\mathcal B[1..3,1..3],d_3=\det A,C=\operatorname{adj}A\).
The old part of \(v_4\) is \(b_1v_1+b_2v_2\) with
\(b=(uc_H/m,-uc_L/m,0)\). Subtract these columns and rows, a congruence
of determinant1. The resulting border is \((-uc_H/(am),c_L/m,0)\)
and corner \(u/(am)-\alpha/h+u^2c_H^2/(am^2)+uc_L^2/m^2\).
The bordered adjugate formula proves

\[
 \det\mathcal B=(u/(am)-\alpha/h)d_3
 +\frac{u^2c_H^2}{m^2}(d_3/a-C_{00}/a^2)
 +\frac{c_L^2}{m^2}(ud_3-C_{11})
 +\frac{2uc_Hc_L}{am^2}C_{01}.                              \tag{18}
\]

Here \(C_{00}=A_{11}A_{22}-A_{12}^2\),
\(C_{11}=A_{00}A_{22}-A_{02}^2\), and
\(C_{01}=A_{02}A_{12}-A_{01}A_{22}\), using zero-based indices.
All four leading minors are positive by the exact certificates below.

The internal cap slacks are

\[
 \sigma_i=1-c_i^2(q+D)/(h-q-D)-\zeta_i/h>0.                 \tag{19}
\]

They also imply every standard cap. Its normalized two-update budget is
\(\begin{pmatrix}1-b_i&-b_ic_i\\-b_ic_i&1-b_ic_i^2-\zeta_i/h\end{pmatrix}\),
where

\[
 b_H=q/(h-2D),\qquad
 b_L=\frac tD\frac q{h-2D}+\frac{D-t}D\frac{q+D}h.
\]

Since \(h>2(q+D)\), both satisfy
\(0<b_i<(q+D)/h<1/2\). Hence
\(b_i/(1-b_i)<(q+D)/(h-q-D)\); (19) supplies the remaining
positive Schur complement. This includes \(t=1\), when the light
internal spaces themselves are absent but (19) is still certified.
The untouched cap gaps \(h-2q=2m-1\) and
\(h-2D=2q+2m-2D-1\) are positive. Every complete frame sector
is below \(hI\). In the original full index space this proves

\[
 NP_N-Q_{\rm seed}\succeq P_N.                              \tag{20}
\]

## Exact coefficient lemmas and computation boundary

[verify_signs.py](verify_signs.py) reconstructs (8)--(9), all16 entries
of (17), both slacks (19), and all four leading minors. Its working
field is \(\mathbb Q(Q,t,D,a,u)\), with \(q=Q+4\). The first three
determinants use all1,2,6 signed permutations; the fourth uses (18),
after all three border identities and the corner identity are verified
exactly in that field. No sampled determinant supplies an identity.

For sign coverage substitute

\[
 t=T+1,\quad D=t+B+1,\quad a=2D+V,\quad u=t+U,
 \qquad Q,T,B,V,U\ge0.                                    \tag{21}
\]

Every new actual parameter is included: \(V=(k-2)D\),
\(U=(r-1)t\). This formal sign domain is larger than the downset
domain. It does **not** remove \(q>k+r\) from the physical metric
proof, and does not assert the existence of that metric at other formal
parameters. The actual dyadic cube verifies this condition above.
Every original denominator is positive: \(t,D,a,u,m-2,m-1,m,m+1\),
\(h,h-2D,h-q-D,\Delta_0\), and both coefficient denominators.

For each reconstructed numerator \(p\), split the exact polynomial
**before shifting loads** as \(p=\sum_jQ^jp_j(t,D,a,u)\).
[coefficients.py](coefficients.py) proves a separate four-variable
lemma for each \(p_j\), using triangular Horner substitutions in order
\(a\mapsto2D+V,u\mapsto t+U,D\mapsto t+B+1,t\mapsto T+1\).
The triangular order never revisits a newly introduced coordinate.
All resulting coefficients are nonnegative, and each \(Q^0\) coefficient
has a positive constant. Thus \(p>0\) on (21). The same argument
certifies each of the12 distinct primitive denominator factors separately;
their positive powers have positive product. An expanded shifted
five-variable denominator is unnecessary.

| Expression | Raw numerator terms / degree | Q-coefficient lemmas | Total shifted terms | Largest coefficient polynomial |
| --- | ---: | ---: | ---: | ---: |
| \(\zeta_H\) |1581/13|6|7020|1995|
| \(\zeta_L\) |1586/13|6|7020|1995|
| Heavy internal slack |3093/14|7|10395|2805|
| Light internal slack |3095/14|7|10395|2805|
| First invariant leading minor |34/3|4|56|35|
| Second invariant leading minor |193/5|6|252|126|
| Third invariant leading minor |298/6|5|456|210|
| Fourth invariant leading minor |15824/19|10|39886|8500|

The fourth numerator has powers \(Q^0,\ldots,Q^9\). Their shifted
four-variable term counts are8500,7140,5916,4828,3876,3060,2380,1820,
1365,1001, respectively. All ten have positive constants. Across the
eight numerators there are51 coefficient lemmas and75480 nonzero shifted
terms. These are regenerated and checked as separate polynomials;
no polynomial of39886 or75480 terms is created or needed. Every raw
polynomial and every coefficient lemma obeys the unchanged30000-term
guard. The compact [RESULTS.json](RESULTS.json) fixes every coefficient
hash, constant, degree, factor power and count, not a polynomial corpus.

[polynomial.py](polynomial.py) adapts the credited9005/9100 engine to
five raw variables and four coefficient variables in distinct module
instances. Multiplication is exact integer Kronecker packing with
coordinate radices greater than the respective product degrees and a
balanced coefficient base \(\beta>2\|p\|_1\|q\|_1\). Degree and
carry checks prevent aliases or incomplete decoding; each packing array
has the fixed32MiB guard. All divisions are exact polynomial divisions.
Modular root probes only reject unneeded division attempts. Thirty-six
deterministic schoolbook comparisons check both dimensions; three direct
schoolbook power substitutions check Horner's triangular evaluation.
Two exact point identities per coefficient are additional regression
controls, not the proof of sign coverage. The certificate checks every
coefficient. A modified raw constant that forces the translated constant
negative is rejected; modified source coefficients change the hashes.
All checks use explicit exceptions and remain active under Python \(-O\).

The first attempt to expand the shifted five-variable fourth minor hit
the30000-term guard, after saving seven positive signs. It established no
fourth sign or nonexistence result. Separating powers of \(Q\) closes the
sign through smaller polynomial lemmas without raising term, stage,
packing, memory or process limits. No CAS, numerical sign inference,
interpolation, incomplete enumeration or proof assistant is an input to
the portable certificate. Its trust base is the stated ordinary proof,
reviewable source and exact integer/rational arithmetic; the ordinary
mathematical and code bridges remain unformalized. Author checks are not
independent peer review.

[verify_full.py](verify_full.py) separately constructs the original core
from its Gram definition. It checks every changed-sector Gram and full
action entry, all cross and untouched actions, the actual empty vector,
dimension exhaustion, all original-index adjacent \(S_k,S_r\) generators,
and all actual heavy-star kernels. It also checks support, row sums, PSD
ranks, unit/half-unit gaps and matrix hashes. Its six finite fixtures are
\((n,k,r,D,t)=(3,2,1,3,2),(4,2,2,3,1),(4,3,1,2,1),
(5,3,2,4,3),(5,4,1,2,1),(6,2,3,2,1)\).
They cover3186 changed-frame action entries,14 actual mark-permutation
generators and matrices up to78 vertices. Each fixture rejects a changed
intersecting core entry and a changed empty loop. These fixtures validate
the implementation; uniform coverage comes from the ordinary decomposition
and all eight coefficient sign proofs, not from the fixtures.

The same-author baseline replay reproduces9100's entire defining seed,
raw core, trace and parameter record at \((n,r,D,t)=(3,2,3,2)\), its
whole seed/mixed certificate record, and the complete four-by-four budget
after the stated congruence. This is validation of prior mathematics.
The imported9005/9100 literal helpers are named and hashed in
[SHA256SUMS](SHA256SUMS). No independent verdict is claimed from replay.

## Raw repair, optimal rank and spectral endpoints

The seed lower rank is \(N-k-1\), by (4) and (10). Keep the same
old/spoke vectors and form raw singleton vectors
\(R_j=-S_j/w+E_j\), with independent orthogonal residuals
\(E_j^2=w-1/w>0\). The norms and mandatory product \(-1\) persist.
The old/spoke span has rank \((2q-1)+(m-k)\); the \(m\) independent
new residuals give raw core rank \(N-k-1\), with kernel dimension \(k\).
Its \(k\) independent relations are precisely the heavy-star indicators:
the old part is \(-H_i\), while its heavy spoke sum is \(H_i\).
They are already in the seed kernel, so the raw kernel is contained in
the seed kernel and has no additional directions.

Let \(A_2=aD+ut\). The actual raw nonempty sum has squared norm

\[
 B_{\rm raw}=w+(1-1/w)^2[m(q+D)-A_2]
             -2m(1-1/w)+m(w-1/w).
\]

The full trace **including the empty vector** is
\(T_{\rm raw}=(N-1)w+B_{\rm raw}>0\). PSD gives
\(Q_{\rm raw}\preceq T_{\rm raw}P_N\). Take the explicit rational
mixture

\[
 \epsilon=1/[2(1+T_{\rm raw})],\qquad
 C=(1-\epsilon)C_{\rm seed}+\epsilon C_{\rm raw}.             \tag{22}
\]

The kernel of a positive PSD sum is the intersection of kernels. Hence
the mixed core kernel is exactly the \(k\)-dimensional raw kernel,
giving core rank \(N-k-1\) and lower rank \(N-k\). The universally
forced upper bound above proves greatest lower rank. From (20) and the
trace bound,

\[
 NP_N-Q\succeq[1-\epsilon(1+T_{\rm raw})]P_N
                 =\tfrac12P_N.                            \tag{23}
\]

This deliberately sufficient bound discards the positive \(\epsilon N\)
term;9049 credits sharper trace constants. Equation (23) gives the upper
rank \(N-1\), the simple unit eigenvalue and (3). The exact lower nullity
is \(k\), so the negative endpoint has multiplicity \(k\). This proves
(1)--(3) for all new parameters; combining the credited one-heavy cases
gives the theorem's full quantified statement.

The public packet contains compact source and summary certificates only.
The private unshifted polynomial record, incomplete dense run, logs and
CAS environment are not reproduction inputs. All solver/BLAS/OpenMP
threads are1; only one intensive mathematical job runs at once. Stage60s,
30000 terms per polynomial,32MiB per packing array and literal \(n\le6\),
\(N\le80\) guards remain fixed, within the oneCPU/2GiB scope.
Resource failure would prevent a certificate claim, not imply mathematical
nonexistence. Three or more distinct loads, more general downset closure,
optimal repair, and unrestricted H or I remain unresolved.
