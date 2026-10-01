# Arbitrary two unequal pendant loads at distinct Boolean-cube marks

Actual agent **six-downset-1**, role **researcher**, round two, 2026-10-01.
Status: complete author argument with portable exact algebra and original-index
validation; ordinary mathematical bridges are unformalized and independent
review is pending. This is a structural subclass result for spectral Chvatal H.

## Quantified statement and provenance

Let \(X\) have \(n\ge2\) coordinates, let \(x,y\in X\) be distinct, and
let the integers \(D>t\ge1\) be arbitrary. Attach \(D\) fresh coordinates at
\(x\) and \(t\) at \(y\), with all fresh coordinates distinct. Precisely,

\[
 \mathcal D=2^X\ \cup\
 \bigcup_{j=1}^{D}\{\{a_j\},\{a_j,x\}\}\ \cup\
 \bigcup_{j=1}^{t}\{\{b_j\},\{b_j,y\}\}.
\]

Put \(q=2^{n-1}\), \(m=D+t\), \(N=2q+2m\), \(s=q+D\), \(w=s-1\).
There is an explicit rational symmetric matrix \(\mathbf M\), indexed by
**all** members of \(\mathcal D\), including the empty set, such that

\[
 \mathbf M\mathbf1=\mathbf1,\qquad
 \mathbf M_{AB}=0\quad(A\cap B\ne\varnothing),\qquad
 L=(N-s)\mathbf M+sI\succeq0,\qquad \mathbf M\preceq I.
                                                               \tag{1}
\]

Its lower rank is \(N-1\), universally greatest among every real H matrix
on this family, including matrices without an upper cap. Its upper rank
is \(N-1\). Both the unit eigenvalue and the negative endpoint are simple,
and every nonunit eigenvalue belongs to

\[
 \left[-\frac{q+D}{q+D+2t},\
        1-\frac1{2(q+D+2t)}\right].                              \tag{2}
\]

The full scaled cap satisfies
\((N-s)(I-\mathbf M)\succeq P_N/2\), where \(P_N=I-J/N\).
The only maximum intersecting family is the heavy \(x\)-star.

The [equal-load construction8895](../EQUAL_LOAD_MARKS.md), source
fd13642ca7c14c53c0339c5a592fc0e73c14d326, supplies the modified cube
Gram, centered singleton idea, empty lift and raw trace rank repair.
The new step is the unequal mark-dependent completion and its **uniform
complete frame cap** for every two positive unequal integer loads.
The equal two-load case is already covered by8895 and the
[single-load result8863](../ALL_MARKS.md). Combining those prior results
with (1) covers all two positive integer loads at distinct cube marks;
the new argument here assumes strict inequality throughout.
It does not generalize the three-or-more-mark scope of8895.

The full lift and structural rank framework are credited to
[7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md);
the raw repair is also credited to
[8579](../UNEQUAL_FACETS.md) and [8788](../TWO_MARKED_CUBE.md).
Cube complementary-pair structure is credited through8895 to8020/8066.
[Balanced pendant closure8424](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/BALANCED_PENDANT_COMPLETION.md)
requires a maximum-star attachment and \(N=2s\); the present two-mark
family has \(N-2s=2t>0\). That same-mark iteration does not give this
unequal two-mark result.
[Linear-count completion8466](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/LINEAR_PENDANT_COMPLETION.md)
and [its boundary refinement8496](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/BOUNDARY_PENDANT_COMPLETION.md)
are prior maximum-star, large-pendant completion results. Their selected
attachment mark and sufficient-count hypotheses remain essential;
there is no historical first-existence claim here.
[Review8927](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/distinct-mark-audit/REVIEW.md)
concerns8863 and cites8895; no reviewer verdict is transferred here.

Primary conventions and the open spectral conjectures are in
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
The [arXiv record](https://arxiv.org/abs/2609.28404) was rechecked on
2026-10-01, immediately before this source preparation: only v1 of
2026-09-23 is listed. General H and I remain open.

## Family structure, universal lower rank and full lift

Old marked stars have sizes \(q+D\) and \(q+t\), other old stars size
\(q\), and fresh stars size2. An intersecting family with a fresh
singleton has at most2 members. Spokes at different marks are disjoint.
A family containing spokes can use only one mark, and its old members
must all contain that mark. It consequently has at most \(q+D\)
members, with equality only when it consists of every heavy spoke and
all \(q\) old sets containing \(x\). With no spokes or fresh singletons,
the complementary cube pairs give at most \(q\). Since \(D\ge2\), these
cases prove the asserted unique maximum family.

For any real H matrix, the centered indicator
\(z=\mathbf1_{\mathcal S_x}-(s/N)\mathbf1\) satisfies \(z^TLz=0\):
the support constraints give
\(\mathbf1_{\mathcal S_x}^T\mathbf M\mathbf1_{\mathcal S_x}=0\), and
\(L\mathbf1=N\mathbf1\). Positive semidefiniteness then gives \(Lz=0\).
The vector is nonzero, so every H matrix has lower rank at most \(N-1\).
No symmetry or sign restriction on disjoint entries is assumed.

For a PSD core \(C\) on the nonempty members, with diagonal \(w\) and
intersecting entries \(-1\), set

\[
 T_0=\begin{pmatrix}-\mathbf1^T\\I\end{pmatrix},\qquad
 Q=T_0CT_0^T,\qquad
 \mathbf M=(Q+J-sI)/(N-s).
\]

Then support and row sums hold, and

\[
 L=Q+J,\qquad \operatorname{rank}L=1+\operatorname{rank}C,\qquad
 (N-s)(I-\mathbf M)=NP_N-Q.                                    \tag{3}
\]

In Gram language the empty vector is the negative total nonempty sum.
The nonzero \(Q\) spectrum equals the spectrum of the **full** Gram
frame, including that empty vector.

## Rational seed Gram

On old nonempty cube members let \(P\) exchange the proper complement
pairs and have zero full-set row. Use

\[
 C_D=(q-D)P+(q+D)I-J.                                          \tag{4}
\]

Its pair-antisymmetric eigenvalue is \(2D\), of multiplicity \(q-1\);
its pair-symmetric zero-sum eigenvalue is \(2q\), of multiplicity \(q-2\).
The remaining orthonormal plane is
\(\begin{pmatrix}2&-\sqrt{2q-2}\\-\sqrt{2q-2}&w\end{pmatrix}\),
with positive trace \(q+D+1\) and determinant \(2D\).
Thus \(C_D\) is PD of rank \(2q-1\), even when \(D>q\).

Let \(g_A\) be old Gram vectors, \(G=\sum_{A\ne\emptyset}g_A\),
\(f=g_X\), \(H_1=-\sum_{A\ni x}g_A\), \(H_2=-\sum_{A\ni y}g_A\).
Complementary-pair counts give

\[
 G^2=f^2=w,\quad G\cdot f=D+1-q,\quad
 H_i^2=qD,\quad H_1\cdot H_2=0,\quad G\cdot H_i=f\cdot H_i=-D.
                                                               \tag{5}
\]

Also \(H_i\cdot g_A=-D\) when \(A\) contains its mark and \(+D\)
when a proper nonempty \(A\) excludes that mark.

For group sizes \(d_1=D,d_2=t\), choose new vectors \(T_{i,j}\),
orthogonal to the old span and to the other group, with Gram

\[
 T_{i,j}\cdot T_{i,k}=(q+D)(\delta_{jk}-1/D),\qquad
 S_{i,j}=H_i/D+T_{i,j}.                                       \tag{6}
\]

The heavy residual has rank \(D-1\) and sum zero. The light residual
has rank \(t\), since \(t<D\). Every spoke has squared norm \(w\);
same-mark distinct spokes have product \(-1\), different marks product
zero, and every mandatory old-spoke intersection has product \(-1\).

Write \(L_2=\sum_{j=1}^tS_{2,j}/t\) and \(Z=L_2-H_2/D\). Then
\(Z^2=(q+D)(1/t-1/D)>0\). The light centered internal residual is
orthogonal to \(Z\) and is a \((t-1)\)-simplex with frame eigenvalue
\(q+D\). The heavy spoke mean is \(H_1/D\).
Put

\[
 K=G+H_1+tL_2,\qquad
 B_0=K^2=w+m(q+D)-D^2-t^2-2m
       =w+m(q-2)+t(D-t)>0.                                    \tag{7}
\]

If a spoke belongs to a group of size \(d_i\), \(K\cdot S=w-d_i\).
Define

\[
 c_H=\frac{m(w-D-m-1)}{(m+1)((m-1)w-1+D)},\qquad
 c_L=\frac{m(w-t-m-1)}{(m+1)((m-1)w-1+t)}.
\]

Let \(c_j\) be the appropriate coefficient,
\(C_\Sigma=\sum_jc_jS_j\), and
\(Y_j=c_jS_j-C_\Sigma/m\). Their sum is zero. Assign singletons

\[
 U_j=-K/(m+1)+Y_j+W_j.                                       \tag{8}
\]

The new \(W\)'s will be orthogonal to all old and spoke vectors and
sum to zero. The required own-spoke product is already exact:

\[
 U_j\cdot S_j=-\frac{w-d_i}{m+1}
     +c_j\frac{(m-1)w+d_i-1}{m}=-1.
\]

These are the only mandatory singleton intersections.
All other products remain unrestricted.

The heavy mean of \(Y\) and the light mean are, respectively,

\[
 y=\frac t m(c_HH_1/D-c_LL_2),\qquad -D y/t .
\]

Put

\[
 b=K\cdot y=\frac t m[c_H(q-1)-c_L(w-t)],\qquad
 v=y^2=\frac{t^2}{m^2}
       \left[c_H^2q/D+c_L^2(q+D-t)/t\right].
\]

The required singleton residual squared norms are

\[
 \eta_H=w-\frac{B_0}{(m+1)^2}-v
            -c_H^2(q+D)(1-1/D)+\frac{2b}{m+1},
\]
\[
 \eta_L=w-\frac{B_0}{(m+1)^2}-\frac{D^2}{t^2}v
            -c_L^2(q+D)(1-1/t)-\frac{2D b}{t(m+1)}.
\]

Let \(E=D\eta_H+t\eta_L\), and define

\[
 \zeta_H=\frac m{m-2}\left[\eta_H-\frac E{m(m-1)}\right],\qquad
 \zeta_L=\frac m{m-2}\left[\eta_L-\frac E{m(m-1)}\right].          \tag{9}
\]

The universal algebra certificate below proves both strictly positive.
With \(P_m=I-J/m\), take the \(W\) Gram to be

\[
 \mathcal W=P_m\operatorname{diag}
    (\underbrace{\zeta_H,\ldots,\zeta_H}_{D},
     \underbrace{\zeta_L,\ldots,\zeta_L}_{t})P_m.                \tag{10}
\]

It is PD on the zero-sum index space, has rank \(m-1\), row sums zero,
and diagonal \(\eta_H,\eta_L\) as prescribed. The diagonal identity
follows from \(\sum_j\zeta_j=mE/(m-1)\).
Hence (8) has squared norm \(w\), completing the PSD seed core.
All Gram entries are rational; no vector square roots need to be
computed. The total nonempty sum is \(K/(m+1)\), so the actual empty
vector is \(-K/(m+1)\).

## Exhaustion of the full frame

Set \(h_0=-(G+f)/2\), \(G_p=G+h_0\), and \(A_i=H_i-h_0\).
Their metric is

\[
 G_p^2=q-1,\quad h_0^2=D,\quad
 A_i\cdot A_j=D(q\delta_{ij}-1),
\]

with all other displayed old products zero. The old frame \(F_0\) acts by

\[
 F_0G_p=(q+1)G_p+(q-1)h_0,\quad
 F_0h_0=D(G_p+h_0),\quad F_0A_i=2D A_i.                       \tag{11}
\]

Let \(W_s=\sum_{j\le D}W_j/D\). Its light mean is \(-DW_s/t\), and

\[
 \alpha=W_s^2=\frac{t(t\zeta_H+D\zeta_L)}{D m^2}>0.
\]

The group mean of \(Y_j+W_j\) is \(y+W_s\) on the heavy group and
\(-D(y+W_s)/t\) on the light group. Inside each group, the \(T\)
and \(W\) zero-sum spaces are paired orthogonally. The \(W\) frame
eigenvalues there are \(\zeta_H,\zeta_L\).

For \(q\ge4\) the complete Gram span has these orthogonal sectors:

| Sector | Dimension | Full frame on the sector |
| --- | ---: | --- |
| \(G_p,h_0,A_1,A_2,Z,W_s\) | 6 | \(F_{\rm sym}\) below |
| Heavy paired internal spaces | \(2(D-1)\) | \(D-1\) identical \(2\)-blocks |
| Light paired internal spaces | \(2(t-1)\) | \(t-1\) identical \(2\)-blocks |
| Untouched old pair-symmetric space | \(q-2\) | \(2q I\) |
| Untouched old pair-antisymmetric space | \(q-3\) | \(2D I\) |

The dimensions sum to \(N-3\). The high space consists of symmetric
differences between proper complementary pairs. The old low space
has dimension \(q-1\); removing its two independent \(A_i\) directions
leaves \(q-3\). At \(q=2\), \(A_1+A_2=0\), the symmetric dimension
is5, and both untouched spaces are absent. At \(t=1\), the light
internal sector is absent. These formulas still sum to \(N-3\).
Alternatively the rank count is
\((2q-1)+(m-1)+(m-1)=N-3\), from the old, spoke-residual and \(W\) spans.
This accounts for every direction, including the two boundary cases.

Expanding (8), including the empty vector, gives the symmetric frame

\[
 F_{\rm sym}=F_0+\frac{H_1H_1^*}{D}+tL_2L_2^*
             +\frac{KK^*}{m+1}
             +\frac{Dm}{t}(y+W_s)(y+W_s)^*.                  \tag{12}
\]

The \(KK^*/(m+1)\) term combines all singleton means with the
empty-vector energy. In a normalized heavy or light internal plane,
the full frame is

\[
 F_i=\operatorname{diag}(q+D,0)+u_i u_i^*,\qquad
 u_i=(c_i\sqrt{q+D},\sqrt{\zeta_i}).                            \tag{13}
\]

## Uniform symmetric and internal cap

Use \(h=N-1=2q+2m-1\). The old eigenvalues \(2q,2D\) are below \(h\);
the positive old two-plane has trace \(q+D+1<h\).
Thus \(D_0=hI-F_0\) is PD on the changed symmetric space, with
old eigenvalue zero on its two new directions.

In the possibly dependent generating list
\((G_p,h_0,A_1,A_2,Z,W_s)\), the bilinear resolvent metric
\(R_{ab}=\langle e_a,D_0^{-1}e_b\rangle\) is

\[
 \Delta_0=(h-q-1)(h-D)-D(q-1),
\]
\[
 R_{00}=\frac{(q-1)(h-D)}{\Delta_0},\quad
 R_{01}=R_{10}=\frac{D(q-1)}{\Delta_0},\quad
 R_{11}=\frac{D(h-q-1)}{\Delta_0},
\]
\[
 R_{ij}=\frac{D(q\delta_{ij}-1)}{h-2D}\ (i,j=2,3),\quad
 R_{44}=\frac{(q+D)(1/t-1/D)}h,\quad R_{55}=\frac\alpha h.
\]

All other entries vanish. At \(q=2\) this remains a bilinear resolvent
identity; it is not an inverse of the singular coordinate Gram.
The four update vectors for (12) have coordinates

\[
 v_1=(0,1,1,0,0,0),\qquad
 v_2=(0,1/D,0,1/D,1,0),
\]
\[
 v_3=(1,t/D,1,t/D,t,0),\qquad
 v_4=\left(0,\frac{t(c_H-c_L)}{mD},
             \frac{tc_H}{mD},-\frac{tc_L}{mD},
             -\frac{tc_L}m,1\right).
\]

The block Schur criterion, valid also for dependent update vectors, says
\(F_{\rm sym}<hI\) exactly when

\[
 \mathcal B=\operatorname{diag}(D,1/t,m+1,t/(Dm))
            -(v_i^TRv_j)_{i,j=1}^4\quad\text{is PD}.            \tag{14}
\]

All four leading determinants are positive by the universal exact
algebra below; Sylvester's criterion proves (14).
For (13), \(h-(q+D)>0\), and the rank-one Schur criterion is

\[
 1-\frac{c_i^2(q+D)}{h-q-D}-\frac{\zeta_i}h>0.                  \tag{15}
\]

Both heavy and light conditions are proved, including the unused
light expression at \(t=1\). The untouched gaps are \(2m-1>0\)
and \(2q+2t-1>0\). Consequently the **full** seed frame is below
\((N-1)I\), so (3) gives

\[
 NP_N-Q_{\rm seed}\succeq P_N.                                \tag{16}
\]

Directions outside the Gram span have frame eigenvalue zero and also
satisfy this cap. The seed core rank is \(N-3\), giving lower rank \(N-2\).

## Exact unbounded algebra and the computational trust boundary

[verify_signs.py](verify_signs.py) reconstructs (9), (15), and the
entire (14) over the fraction field of \(\mathbb Q[Q,T,B]\), with

\[
 q=Q+2,\qquad t=T+1,\qquad D=t+B+1,\qquad Q,T,B\ge0.             \tag{17}
\]

This domain covers every integer parameter in the statement and both
boundaries \(q=2,t=1\). Its four determinants are computed by complete
signed permutation sums, with1,2,6,24 summands. Every resulting numerator
and denominator has nonnegative rational coefficients and a positive
constant term:

| Expression | Numerator terms / degree | Denominator terms / degree |
| --- | ---: | ---: |
| \(\zeta_H\) | 440 /13 | 335 /12 |
| \(\zeta_L\) | 440 /13 | 335 /12 |
| Heavy expression (15) | 560 /14 | 560 /14 |
| Light expression (15) | 560 /14 | 560 /14 |
| First leading determinant | 33 /4 | 19 /3 |
| Second leading determinant | 79 /6 | 70 /6 |
| Third leading determinant | 103 /7 | 70 /6 |
| Fourth leading determinant | 1308 /19 | 1371 /19 |

Positive constants give strict positivity at every nonnegative real
\(Q,T,B\), not just at sampled or dyadic values. All original divisions
are legal: \(D,t,m,m-1,m-2,m+1,h,h-2D,h-q-D,\Delta_0\) and the
two displayed \(c_i\) denominators are positive. The small denominator
factor hints in the source likewise have nonnegative coefficients and
positive constants. They are optimization hints; every cancellation
uses verified exact polynomial division.

The multiplication optimization has an elementary exact bound. For
integer coefficient polynomials \(a,b\), choose exponent radix larger
than every individual variable degree in their product, encode
\((i,j,k)\) as \(i+rj+r^2k\), and choose coefficient base
\(\beta>2\|a\|_1\|b\|_1\). Integer multiplication followed by balanced
base-\(\beta\) decoding recovers every signed coefficient without
overlap or ambiguous carries. The source checks those degree and
coefficient bounds and compares18 deterministic multiplication fixtures
with sparse schoolbook arithmetic. Rational coefficient denominators
are tracked separately. Small modular factor-root tests only reject
unnecessary cancellation attempts; they never establish an identity
or a sign. Polynomial division and coefficient comparisons are exact.

During discovery, SymPy1.14.0 derived the same scalars and all16 matrix
entries over \(\mathbb Q(Q,T,B)\). Its direct last rational Bareiss step
hit a60-second cancellation guard. A denominator-cleared bordered
identity \(\det\begin{pmatrix}A&v\\v^T&c\end{pmatrix}
=c\det A-v^T\operatorname{adj}(A)v\) completed in3.98seconds and gave
a degree28 positive coefficient certificate. The separate portable
algorithm reconstructed every scalar/matrix entry, independently
verified all eight rational identities, and then reduced the final
sign to the degree19 source calculation above. The public reproduction
requires no CAS, no saved polynomial corpus, and no network input.
The timeout was an operational limit, never evidence of nonexistence.

The infinite bridge in (17) is coefficient positivity plus the ordinary
Schur/frame argument. It is not an extrapolation from the full-matrix
fixtures. The implementation and interpretation are author-checked
and unformalized; an independent reviewer has not certified this claim.

## Raw rank repair and final rational certificate

Retain the old and spoke vectors, but replace singleton \(j\) by
\(-S_j/w+E_j\), where the \(E_j\)'s are new independent orthogonal
vectors of squared norm \(w-1/w>0\).
Their own-spoke products are \(-1\) and their squared norms \(w\),
so they give an ordinary PSD H core \(C_{\rm raw}\).
Its rank is

\[
 (2q-1)+(m-1)+m=N-2.
\]

Its only core kernel is the heavy-star sum, since the heavy spoke sum
is \(H_1\) and cancels the old heavy-star vectors. The seed kills that
same sum. Thus any strict positive mixture has core rank \(N-2\) and
lower rank \(N-1\).

The raw actual empty energy and full trace are exactly

\[
 B_{\rm raw}=w+(1-1/w)^2[m(q+D)-D^2-t^2]
              -2m(1-1/w)+m(w-1/w),
\]
\[
 T_{\rm raw}=(N-1)w+B_{\rm raw}.
\]

As \(Q_{\rm raw}\succeq0\), \(Q_{\rm raw}\mathbf1=0\), and
\(\operatorname{tr}Q_{\rm raw}=T_{\rm raw}\),
\(Q_{\rm raw}\preceq T_{\rm raw}P_N\). Choose

\[
 \epsilon=\frac1{2(1+T_{\rm raw})},\qquad
 C=(1-\epsilon)C_{\rm seed}+\epsilon C_{\rm raw}.               \tag{18}
\]

This is a rational strict positive mixture. PSD mixture kernels
intersect, proving lower rank \(N-1\). From (16),

\[
 NP_N-Q\ \succeq\
 [1-\epsilon(1+T_{\rm raw})]P_N+\epsilon N P_N
 \ \succeq\ \tfrac12P_N.
\]

This proves the full cap, upper rank \(N-1\), and simple unit eigenvalue.
The forced lower kernel is one-dimensional, so the negative endpoint
\(-s/(N-s)\) is simple. Equations (2) and (1) follow.

## Literal validation and reproduction

[verify_full.py](verify_full.py) reconstructs all original-index rational
cores, the actual empty lift, seed and mixed PSD forms, ranks and scaled
gaps. It verifies every Gram and full frame action on the complete
changed sectors, all untouched old eigen-actions and dimension
exhaustion for
\((n,D,t)=(3,3,2),(2,8,7),(3,8,7),(4,5,1),(6,2,1)\).
These include \(q=2\), \(t=1\), \(D>q\), nearly equal loads, and an old
cube of order64. It rejects a changed intersecting core entry and a
changed empty loop. Those finite checks validate the source against
literal definitions; they do not provide the uniform quantifier.

Run from the repository root, with CPython3.11 or later on a POSIX host:

~~~sh
python3 -B round-two/six-downset-1/two-unequal-loads/verify_signs.py --expected round-two/six-downset-1/two-unequal-loads/RESULTS.json
python3 -B round-two/six-downset-1/two-unequal-loads/verify_full.py --expected round-two/six-downset-1/two-unequal-loads/RESULTS.json
~~~

Repeat with \(-O\) for the optimization-mode regression; checks use
explicit exceptions, not assertions. [RESULTS.json](RESULTS.json) records
compact exact coefficient fingerprints and full rational matrix hashes.
[SHA256SUMS](SHA256SUMS) covers the source and its two credited helper
files. All numerical thread counts were1 and only one mathematical job
ran at a time. No large private output, CAS libraries or credentials
are part of this source packet.
