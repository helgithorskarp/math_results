# An exact asymmetric obstruction to the 208/9 angular extension

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.
Ordinary written author proof with an exact finite arithmetic certificate.
Independent review is pending; no proof-assistant formalization is claimed.

The [triple-pair theorem](../triple-angular-persistence/PROOF.md), source
`4587f5f3776a0ec8c22d43ec8b264c8b48915218`, graph8672, proves the sharp
bound \(208/9\) **only on its symmetric triple family**. It explicitly
leaves a universal extension open. The proposed universal extension
fails, including at profiles with eight distinct slopes. The published
restricted theorem and its separate global interval near \(a_3\) are
not contradicted.

This is an obstruction in the original-root angular problem associated
with degree-nine first power. It is not a counterexample to the
first-power Tang--Zhang conjecture.

## 1. Statement

For real balanced norm-one slopes \(\theta\in\mathbb R^8\), set
\[
e=\mathbf1/\sqrt8,\quad P=I-ee^T,\quad
H=P\operatorname{diag}(\theta)P|_{e^\perp},\quad
w=\operatorname{diag}(\theta)e,
\]
\[
X=\sum\theta_j^4,\qquad
\eta=64\sum_{\lambda\text{ distinct}}\|\Pi_\lambda w\|^4,
\qquad J_R=RX-\eta.
\]
Full eigenspace projections are used, including at collisions. The
uniform four-plus-four profile has \(X=1/8,\eta=1\), and hence
\(J_{\rm unif}=R/8-1\).

**Theorem 1 (compact asymmetric counterexample).** Let \(u\) consist
of three copies each of \(1+10\sqrt3\) and \(1-10\sqrt3\), and the
two entries \(7,-13\). Then \(\theta=u/\sqrt{2024}\) is balanced
and norm one, and
\[
X=\frac{601}{4232},\qquad
\eta=\frac{46573202983}{78109350583},\qquad X-\frac18=\frac9{529}.
\tag{1}
\]
In particular,
\[
\boxed{\eta-1+\frac{208}{9}(X-1/8)
                  =-\frac{823964384}{78109350583}<0.}
\tag{2}
\]
Any universal inequality \(\eta\ge1-C(X-1/8)\) must therefore have
\[
\boxed{C\ge C_{\rm ex}:=\frac{3504016400}{147654727}
          >\frac{208}{9}},\quad
C_{\rm ex}-\frac{208}{9}=\frac{823964384}{1328892543}.
\tag{3}
\]
This is a necessary lower bound, not a proposed sharp universal constant.

**Theorem 2 (eight distinct slopes).** The eight slopes
\[
\frac{c+10\sqrt3}{45},\quad \frac{c-10\sqrt3}{45}
       \quad(c=1/2,1,3/2),\qquad \frac7{45},\quad-\frac{13}{45}
\tag{4}
\]
are all distinct, balanced and norm one, and also violate the inequality
with \(C=208/9\). Thus neither repeated original slopes nor repeated
compression eigenspaces are necessary for failure.

**Corollary 3 (uniform angular transition obstruction).** For Theorem 1's
fixed profile,
\[
J_R(\theta)-J_{\rm unif}=
                  \frac9{529}(R+C_{\rm ex}).
\tag{5}
\]
Consequently the uniform profile is not a global angular maximizer for
any \(R>-C_{\rm ex}\). At \(R=-208/9\) it is beaten by the exact
positive amount \(823964384/78109350583\).
The symmetric crossing profile \(r=21/136,t=5/136\) from graph8672 has
the same value as the uniform profile at this parameter, so it is also
globally suboptimal. Its previously proved strict local stability remains
valid. Thus the whole explicit local band in that theorem cannot be
upgraded to a global optimizer interval.

For the credited radius-dependent angular functional
\[
K_a=B_d+C_dJ_{R(d)},\quad d=1+a,\quad
C_d=\frac{d^3(4d+1)^2}{8192}>0,\quad
R(d)=\frac{16(48d^2-40d-53)}{(4d+1)^2},
\tag{6}
\]
the uniform profile cannot be globally optimal at any physical radius
\(a>a_{\rm ex}\), where \(a_{\rm ex}\) is the unique positive root
\[
\boxed{5295721648a^2+8514352856a-584718545=0.}
\tag{7}
\]
Exact rational evaluation isolates it as
\[
0.0659677<a_{\rm ex}<0.0659678.
\]
It is strictly smaller than the symmetric-family comparison radius
\(a_*=(3\sqrt{34}-16)/20\) from graph8672. We do not claim that the
uniform profile is globally optimal below \(a_{\rm ex}\), that this
bound is sharp, or that the exhibited profile is stationary or extremal.

The radius interpretation (6) is credited to
[graph8160](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_moving_pair_comparison_boundary/PROOF.md)
and [review8230](https://github.com/helgithorskarp/math_results/blob/main/sendov_moving_pair_threshold_review3/REVIEW.md).
The counterexamples to the stated inequality on \(\mathcal S\) are
self-contained finite algebra and do not require the analytic disk
reduction or the spectral-square optimizer theorem.

## 2. Unnormalized compression and the active cubic

Work first with \(u\), \(N=\sum u_j^2\),
\(D_u=\operatorname{diag}(u)\),
\(H_u=PD_uP|_{e^\perp}\), and \(w_u=D_ue\). Balance gives
\(w_u\in e^\perp\). Normalization multiplies \(H_u,w_u\) by
\(N^{-1/2}\) without changing any eigenspace projection. If
\(\rho_i^u=8\|\Pi_iw_u\|^2\), then
\[
\eta=\frac{\sum_i(\rho_i^u)^2}{N^2},\qquad
X=\frac{\sum u_j^4}{N^2}.
\tag{8}
\]

For Theorem 1 put
\[
A=z^2-2z-299,\quad B=z^2+6z-91,\quad f=A^3B.
\]
The roots of \(A\) are \(1\pm10\sqrt3\); those of \(B\) are
\(7,-13\). Direct expansion or the quadratic-field root moments gives
\[
\sum u_j=0,\quad N=2024,\quad
S_3:=\sum u_j^3=3552,\quad S_4:=\sum u_j^4=581768.
\tag{9}
\]
For example, the outer pair contributes
\(3\cdot2(1+300)=1806\) to the second moment; the inner contribution
is \(49+169=218\). The bracket \(17/10<\sqrt3<7/4\), proved by
squaring, separates all four original levels.

The characteristic polynomial of \(H_u\) is
\[
g=f'/8=A^2h,\qquad h=z^3+4z^2-149z-156.
\tag{10}
\]
For completeness, for \(z\) away from the diagonal spectrum the
cofactor formula in an orthonormal basis beginning with \(e\) gives
\[
\det(zI-H_u)=\det(zI-D_u)\,e^T(zI-D_u)^{-1}e
            =f(z)\frac18\sum_j\frac1{z-u_j}=f'(z)/8.
\]
It holds polynomially everywhere. The two repeated outer eigenspaces
are the sum-zero vectors on their three-coordinate blocks. Each is
orthogonal to \(w_u\), which is constant on its block, so their
coupling weights are zero. The remaining three eigenvalues are the
roots of \(h\). They are simple and strictly between the four original
levels: the logarithmic derivative \(\sum m_j/(z-u_j)\) decreases
strictly from positive infinity to negative infinity in each gap.
In particular the active roots are real and distinct.

## 3. Three-moment calculation of the weight sum

Let the three active eigenvalues be \(\lambda_i\), with weights
\(\rho_i=\rho_i^u\). Spectral decomposition and the fact that the
other weights vanish give
\[
\sum\rho_i=N,\quad \sum\rho_i\lambda_i=S_3,\quad
\sum\rho_i\lambda_i^2=S_4-N^2/8.
\tag{11}
\]
Indeed the three expressions are respectively
\(8\|w_u\|^2\), \(8w_u^TH_uw_u\), and
\(8\|H_uw_u\|^2\). For the last one, \(H_uw_u=PD_uw_u\),
so \(8\|PD_uw_u\|^2=S_4-N^2/8\). No unproved symmetry of the
active weights is used.

Newton identities for (10) give the active root power sums
\[
(p_0,p_1,p_2,p_3,p_4)=(3,-4,314,-1384,51698).
\]
Let \(V\) be the matrix whose \(i\)-th column is
\((1,\lambda_i,\lambda_i^2)^T\), and put
\[
\mu=(2024,3552,69696)^T,
\quad G=VV^T=
\begin{pmatrix}
3&-4&314\\-4&314&-1384\\314&-1384&51698
\end{pmatrix}.
\tag{12}
\]
The Vandermonde matrix \(V\) is invertible. Equations (11) say
\(V\rho=\mu\); hence
\[
\sum_i\rho_i^2=\mu^TG^{-1}\mu.
\tag{13}
\]
Exact three-by-three arithmetic gives
\[
\det G=14643444=12\cdot1220287,
\quad \mu^T\operatorname{adj}(G)\mu=35768219890944,
\]
\[
\boxed{\sum_i\rho_i^2=\frac{2980684990912}{1220287}.}
\tag{14}
\]
Dividing (14) and \(S_4\) by \(N^2\) proves (1). The rational
calculations in (2)--(3) now follow directly. An equivalent unnormalized
negative certificate is
\[
\boxed{9\sum_i\rho_i^2+208S_4-35N^2
                       =-\frac{474603485184}{1220287}<0.}
\tag{15}
\]
The coefficient 35 arises by multiplying
\(\eta-1+(208/9)(X-1/8)\) by \(9N^2\).

## 4. Independent residue certificate

The Schur complement in the same basis \((e,e^\perp)\) gives
\[
f/g=z-w_u^T(zI-H_u)^{-1}w_u
    =z-\frac18\sum_i\frac{\rho_i}{z-\lambda_i}.
\]
At an active root, therefore,
\[
\rho_i=-8f(\lambda_i)/g'(\lambda_i)
      =-8A(\lambda_i)B(\lambda_i)/h'(\lambda_i).
\tag{16}
\]
All denominators here are nonzero. The following polynomial is an exact
certificate of the three residues:
\[
q(z)=\frac{1807004888-4876192z-9460696z^2}{1220287},
\qquad qh'+8AB\equiv0\pmod h.
\tag{17}
\]
Consequently \(q(\lambda_i)=\rho_i\). The Newton trace
\(\sum_iq(\lambda_i)^2\), using the five power sums above, reproduces
(14). Independently, the companion matrix of \(h\) gives exactly
\(\operatorname{tr}(q(C_h)^2)\) with the same value. These two
residue-based checks and (13)'s three-moment inverse are separate routes
in the standalone certificate. The moment route does not obtain its
weight vector by inverting \(h'\) or evaluating the residues.

## 5. An explicit counterexample with eight distinct slopes

For the unnormalized roots in (4), write
\[
f_d(z)=\prod_{c\in\{1/2,1,3/2\}}
                 [(z-c)^2-300]\,(z^2+6z-91).
\tag{18}
\]
The roots in each of the two outer groups are separated by their
different rational centers. The same squared bracket for \(\sqrt3\)
places those groups strictly beyond \(7\) and below \(-13\), so all
eight roots are distinct. Their mean is zero, and
\[
N_d=2025=45^2,\qquad S_{4,d}=2334297/4.
\]
Their normalized values are therefore exactly (4). The full derivative
polynomial \(g_d=f_d'/8\) has seven simple real roots by interlacing.
There are no inactive repeated compression slots.

In the rational quotient \(\mathbb Q[z]/(g_d)\), compute
\[
q_d=-8f_d(g_d')^{-1}\pmod {g_d}.
\]
The inverse exists; its Bezout certificate is checked exactly.
The Schur-complement identity in Section 4 identifies
\(q_d(\lambda_i)\) with every compression weight. Newton sums and
an independent seven-by-seven companion trace then give the exact
negative certificate
\[
9\operatorname{tr}(q_d(C_{g_d})^2)+208S_{4,d}-35N_d^2
=-\frac{1746288997284374824819986419052268279175827203851276237295}
 {7980145913653001587422178012567716983879010063343874}<0.
\tag{19}
\]
`verify.py` regenerates (18), derives the inverse and residue polynomial,
checks the congruence, compares both traces and reproduces the complete
fraction (19). Thus (19) is an exact finite certificate, rather than a
floating root computation. Dividing it by \(9N_d^2>0\) proves
Theorem 2. The large numerator is a single rational value, not an
enumeration corpus or an externally trusted numerical datum.

## 6. Radius obstruction and scope

Equation (5) follows by substituting (3) in
\(J_R(\theta)-J_{\rm unif}=R(X-1/8)+1-\eta\).
For (6),
\[
R'(d)=\frac{2048(2d+3)}{(4d+1)^3}>0\quad (1\le d\le2).
\]
Moreover \(208/9<C_{\rm ex}<144/5\), and \(R(1)=-144/5\), so
\(R(1+a)=-C_{\rm ex}\) has a unique physical root. Clearing its
positive denominator \(147654727(4d+1)^2\) in \(R(d)+C_{\rm ex}\)
gives exactly 32 times the polynomial in (7). That quadratic is strictly
increasing for \(a\ge0\), and has opposite signs at
\(659677/10^7\) and \(659678/10^7\), certifying the stated bracket.
Monotonicity also gives \(a_{\rm ex}<a_*\). This proves Corollary 3.

The counterexample disproves a possible extension of the sharp
symmetric-family affine bound. It establishes a necessary universal
constant and an upper obstruction for uniform angular optimality.
It neither locates the true global transition nor solves the full
lower-radius optimizer. It does not invalidate the global triple-pair
interval near \(a_3\), whose proof and existential scope remain as
published, or the sharp restricted comparison at \(a_*\).

All 31 exact records and four damage controls are regenerated from the
stated rational inputs. The checker uses only the Python standard library
and no floating point, external solver, data corpus or imported proof
certificate. The finite root/compression identification and radius
interpretation are ordinary written arguments outside a formal kernel.
The stronger complex first-power endpoint and actual finite-energy disk
optimizer classification remain unresolved by this work.
