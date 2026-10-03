# Actual nonzero-skew attainment and the maximal third-budget motion

Actual author **six-sendov-3**, role **researcher**, 2026-10-03.
Complete ordinary author proof, **unformalized and independently unreviewed**.
Exact finite calculations are same-author corroboration. Shared signing
identity does not establish independent authorship or review. Prior constants,
the necessary cost and the canonical motion maps retain their named credit;
see [LITERATURE.md](LITERATURE.md) and [dependencies.json](dependencies.json).

## 1. Domain, credited constants and the new result

All polynomials are complex monic of degree nine. All **nine original roots**
lie in the **closed** unit disk, the marked root is real \(a=1-\eta>0\),
and all **eight critical points** are counted with multiplicity. Put
\[
 F=\sum_{l=1}^8|a-\zeta_l|^{-1},\qquad
 T_\eta=(F-8-C\eta-B_*\eta^2)/\eta^3,
 \qquad\lambda_\eta=\eta^{-2}\sum_l(\Im\zeta_l)^3.
\]
A zero reciprocal denominator means infinity. This is the FIRST-power
objective. Rotation and nonzero scalar multiplication provide the same
statements for a marked root of modulus \(1-\eta\).

Use the credited constants
\[
\begin{gathered}
c=\cos(\pi/9),\quad y=1/[3(1+c)],\quad x=2/3-y,\quad H=14y,\quad b^2=H/2,\\
U_0=-8x,\quad C=8/3+y,\quad
k=-7(1+2c)/18,\quad\rho=(c-5)/3,\quad d=3k+\rho,\\
u_z=-37/36+20c/9-20c^2/9,\quad u_p=u_z-\rho H/2,\\
\alpha=-527/360+41c/90+13c^2/90<0,\quad
\tau=(k+\rho)^2/2,\quad\kappa=\tau+10\alpha/27>0,\\
W_*=2512/27+5840c/9-21392c^2/27,\quad w_2=W_*/8,\\
D_*=-4270/27-29492c/27+4012c^2/3,\\
\Gamma=13/36+1253c/72-50c^2/3,\\
B_*=2311/108+4934c/27-1976c^2/9,\\
T_*=-60800959/17496-307083769c/17496+10980067c^2/486\in(-19,-18).
\end{gathered}                                                    \tag{1}
\]
The first two boundary coefficients and stationary profile are credited to
8619; the sharp third coefficient and full necessary cost are 10152, now
independently confirmed by reviewer four's **10182 relative to its precisely
retained 10156/8619/10127 premises**. That relative review is not a verification
of every complete ancestor or of this new nonzero-skew leaf.

The all-nine motion constants and harmonics are credited to
[10113](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/quadratic-root-motion/PROOF.md),
with the scoped independent
[10156 assessment](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/quadratic-motion-audit/REVIEW.md).
Set \(\omega_j=e^{2\pi ij/9}\), \(j=0,\ldots,8\),
\[
 L_j=-\omega_j/3-x-y/\omega_j,
\quad W_j=\frac i{18}[(3+4c)\omega_j-(1+2c)(1+\omega_j^{-1})-\omega_j^{-2}].
                                                               \tag{2}
\]
The credited fixed \(d_j\) is defined by the real primitive in Section 3.
The credited ideal maximum is
\[
 \Phi(t)=\sqrt{\mathcal A+\mathcal B t+\mathcal Q t^2},\quad t\ge0,
\]
\[
\begin{split}
\mathcal A&=-13638695/972-16011613c/243+20901119c^2/243>0,\\
\mathcal B&=\sin(\pi/9)(1448+6982c-8224c^2)/243>0,\\
\mathcal Q&=(8+25c+20c^2)/162>0.
\end{split}                                                     \tag{3}
\]
Thus \(\max_j|d_j+\lambda W_j|=\Phi(|\lambda|)\), strictly
increasing in \(|\lambda|\). The ideal winner is label 7 for positive
\(\lambda\), label 2 for negative \(\lambda\), and both at zero;
the other seven labels are strictly smaller. These comparisons are prior
10113 mathematics, not new constants or harmonic claims here.

**New actual attainment.** For every finite \(R\), an explicit family
\(p_{\eta,r}\), \(|r|\le R\), has all nine originals simple and
**strictly** inside the disk for every sufficiently small positive \(\eta\),
uniformly in \(r\), and
\[
\begin{split}
\lambda_\eta&=3Hr+O_R(\eta),\\
F_{p_{\eta,r}}&=8+C\eta+B_*\eta^2+
       [T_*+9H\kappa r^2]\eta^3+8\eta^{7/2}+O_R(\eta^4),\\
Z_j&=\omega_j+\eta L_j+\eta^2[d_j+3HrW_j]+O_R(\eta^3).
\end{split}                                                     \tag{4}
\]
Consequently the necessary nonzero-skew payment
\((\kappa/H)\lambda^2\) is physically sharp for **every fixed real**
\(\lambda\), on the actual original-disk domain.

**New maximal envelope and complete limiting skew set.** Fix any real
\(T>T_*\), and write
\[
 \mathcal P_{\eta,T}=\{p\text{ as above}:T_\eta\le T\},\quad
 \Lambda=\sqrt{H(T-T_*)/\kappa}>0,
\]
\[
 R_\eta(p)=\max_{0\le j\le8}
       |Z_j-\omega_j-\eta L_j|/\eta^2.
\]
For all sufficiently small positive \(\eta\), the class is nonempty,
the maximum exists, and
\[
 \boxed{\max_{p\in\mathcal P_{\eta,T}}R_\eta(p)
                  =\Phi(\Lambda)+O_T(\sqrt\eta).}              \tag{5}
\]
The set of limits of \(\lambda_\eta\) along actual competitors in
this **exact** cut is exactly \([-\Lambda,\Lambda]\). Each value,
including both endpoints, is realized by a family in the exact cut for
**every** sufficiently small positive \(\eta\). This does not assert
an exact finite-\(\eta\) interval or an optimal error coefficient.

Maximizing sequences also obey the tangent and individual-normal rigidity
in Section 6. The constructions and maximal envelope are new relative to
the inspected campaign/source record. Historical priority is not asserted.
The unrestricted degree-nine first-power conjecture remains unresolved.

## 2. Explicit genuinely complex critical family

Let \(r\in\mathbb R\) and define real polynomials of \(r\):
\[
\begin{split}
\mu(r)&=\mu_0+\mu_2r^2,&
\beta(r)&=\beta_0+\beta_2r^2+\beta_4r^4,\\
\nu(r)&=\nu_1r+\nu_3r^3,&
\sigma(r)&=\sigma_1r+\sigma_3r^3,
\end{split}
\]
with the following **complete** coefficients:
\[
\begin{array}{ll}
\mu_0=-17403419/34992-45702565c/17496+180635c^2/54,&
\mu_2=35/81-2086c/81+616c^2/27,\\
\beta_0=-1162307/23328-5484833c/11664+52426519c^2/93312,&
\beta_2=14537/1512-3889c/756-1661c^2/756,\\
\beta_4=-2/49-4c/49-2c^2/49,&\\
\nu_1=-17983/972-25711c/486+4564c^2/81,&
\nu_3=28/81+56c/81,\\
\sigma_1=-1967/81+5479c/432-5375c^2/162,&
\sigma_3=-55/189+11c/63+88c^2/189.
\end{array}                                                     \tag{6}
\]
The zero-skew values \(\mu_0,\beta_0\) retain their 10152 credit.
Put \(\epsilon=\sqrt\eta\),
\[
 q_1(r)=\Gamma-4r^2/(3H),\quad v_2(r)=3kHr/7,
\]
\[
\begin{split}
A&=(u_z-ir/3)\eta+(w_2+iv_2)\eta^2+
                  (\mu+i\nu)\eta^3+\eta^{7/2},\\
B&=(u_p+ir)\eta+(w_2+iv_2)\eta^2+
                  (\mu+i\nu)\eta^3+\eta^{7/2},\\
K&=i[1+q_1\eta+\beta\eta^2]+dr\eta+\sigma\eta^2,\\
 p'_{\eta,r}(z)&=9(z-A)^6[(z-B)^2-b^2\eta K^2],\\
 p_{\eta,r}(z)&=\int_{1-\eta}^zp'_{\eta,r}(v)\,dv.
\end{split}                                                     \tag{7}
\]
This is an actual monic polynomial with exact marked root \(1-\eta\).
Its critical points are **six copies of** \(A\) and the two points
\(B\pm b\sqrt\eta K\). For nonzero \(r\), no conjugacy of
the critical or original roots is imposed. Feasibility is established
below on all nine original branches, not inferred from an arbitrary tuple.
The coefficients are polynomials in \(\epsilon\) and \(r\).
All critical distances tend uniformly to 1 on any compact \(r\)-interval,
so all reciprocal Taylor expansions and remainders below are valid there.

The term \(-4r^2/(3H)\) pays the small-coordinate imaginary norm.
Indeed the imaginary centers contribute \(8r^2\eta^2/3\) to
\(\sum(\Im\zeta)^2\); the pair-scale term cancels that contribution
in the coefficient determining \(D_*\). The real pair splitting
\(\pm bdr\eta^{3/2}\) is the required projection-optimal tangent.
The common imaginary \(v_2\eta^2\) enforces the actual signed mean.
Dropping any of these changes the active original constraints or objective.

## 3. All four individual third-normal repairs

Temporarily omit the common \(\eta^{7/2}\) term. The polynomial
coefficients are then analytic in \(\eta\). Here is a complete finite
recipe for its jets, also supplying direct verification of (6).
For each \(l=1,\ldots,8\), its full critical power sum is
\[
 P_l=6A^l+2\sum_{0\le j\le l,\ j\ {m even}}
              {l\choose j}B^{l-j}(b^2\eta K^2)^{j/2}.
\]
Reduce only after retaining every coefficient through \(\eta^3\).
Use
\[
 e_0=1,\quad me_m=\sum_{l=1}^m(-1)^{l-1}e_{m-l}P_l,
\quad p'=9\sum_{m=0}^8(-1)^me_mz^{8-m},
                                                               \tag{8}
\]
integrate, and subtract the primitive at **exactly** \(1-\eta\).
Write the result as \(z^9-1+\eta g_2+\eta^2g_4^r+\eta^3g_6^r\).
These are full complex polynomials with all ten original-polynomial
columns retained. The identities are
\[
 g_2=9+9x(z^8-1)+9y(z^7-1),\quad
 g_4^r=g_4^0+3Hr\,Q(z),
\]
\[
 Q(z)=\frac i2[(1+2c)(z^8+z^7-2)+(z^6-1)],
\]
\[
\begin{split}
g_4^0={}&-36-9U_0+9H/2-9W_*(z^8-1)/8
 +9(U_0^2-D_*)(z^7-1)/14\\
 &+(-3U_0H/4+3Hu_p/2)(z^6-1)
 +(9H^2/40-9H^2/40)(z^5-1).
\end{split}                                                     \tag{9}
\]
The last displayed column vanishes exactly; it is not silently discarded.
This defines the credited
\[
 d_j=-[g_4^0(\omega_j)+g_2'(\omega_j)L_j+36\omega_j^7L_j^2]
                    /(9\omega_j^8).
\]
The second original coefficient is \(D_j=d_j+3HrW_j\). The third is
\[
 E_j=-[g_6^r(\omega_j)+(g_4^r)'(\omega_j)L_j+g_2'(\omega_j)D_j
 +g_2''(\omega_j)L_j^2/2+72\omega_j^7L_jD_j+84\omega_j^6L_j^3]
                    /(9\omega_j^8),
\]
and the third half-normal is
\[
 N_{j,3}=\Re(E_j/\omega_j)+\Re(L_j\overline{D_j}).             \tag{10}
\]
Thus every forcing term below has an explicit finite polynomial definition,
not a numerical fit or assumed feasible tangent.

Let \(A_3=B_3=3/2\), \(A_4=1+c\), \(B_4=2-2c^2\),
\(\theta_j=2\pi j/9\). At fixed \(r\), variations of
\((\mu,\beta,\nu,\sigma)\) have the following **individual**
third-normal rows, derived by differentiating the defining product:
\[
 (-A_j,\ B_jH/7,\ \sin\theta_j,\ H\sin2\theta_j/7),
                  \quad j=3,4,5,6.                            \tag{11}
\]
For example the common imaginary shift contributes
\(-9i\nu(z^8-1)\) to \(g_6\), hence
\(\nu\sin\theta_j\) to the half-normal. The real pair correction
\(\sigma\) contributes \(-9iH\sigma(z^7-1)/7\), giving the last
column. Common real and pair-scale columns follow in the same direct way.
The rows at conjugate labels have opposite sine columns and equal real
columns. Pair sums and **signed differences** therefore form two blocks:
\[
 M_{\rm even}=\begin{pmatrix}-3/2&3H/14\\-(1+c)&(2-2c^2)H/7\end{pmatrix},
 \quad\det M_{\rm even}=2c-1>0,
\]
\[
 M_{\rm odd}=\begin{pmatrix}1&-H/7\\1&-2cH/7\end{pmatrix},
 \quad\det M_{\rm odd}=-H(2c-1)/7\ne0.                       \tag{12}
\]
The two positive sines have been divided out in the odd block. This proves
the full four-constraint rank; a pair-average-only repair is insufficient.

For completeness let \(a_j(r)\) be the average of the two coefficients
(10), and let \(y_j(r)\) be their signed half-difference divided by
\(\sin\theta_j\), computed with all four repairs zero. Substitution
in (8)--(10), reducing with \(8c^3-6c-1=0\), gives the whole-polynomial
identities
\[
 a_j=A_j\mu-B_jH\beta/7,\quad j=3,4,
 \qquad y_3=-\nu+H\sigma/7,\quad y_4=-\nu+2cH\sigma/7,       \tag{13}
\]
where the right sides use precisely the complete polynomials (6).
The actual forcing vectors are also recorded coefficient by coefficient
in [EXPECTED.json](EXPECTED.json). Equations (11)--(13) prove that (6)
repairs **all four individual** third coefficients simultaneously. The
first and second coefficients at these four labels are zero by (9).
All nine complete equations from composition with the original polynomial
are separately reconstructed by [skew.py](skew.py); neither only a count
nor a record hash licenses these identities.

## 4. Strict containment on all nine branches and the FIRST-power cost

Restore the common real \(\epsilon^7\) term in (7). Its first
coefficient effect is
\[
 p_{\epsilon,r}=p^0_{\epsilon,r}-9\epsilon^7(z^8-1)+O_R(\epsilon^8).
\]
Because \(p_0=z^9-1\), the individual root coefficient at order
\(\epsilon^7\) changes by \(1-\omega_j\). Its half-normal
coefficient is \(\cos\theta_j-1\). Thus, on the four active labels,
\[
 N_3=N_6=-\tfrac32\epsilon^7+O_R(\epsilon^8),\quad
 N_4=N_5=-(1+c)\epsilon^7+O_R(\epsilon^8).                   \tag{14}
\]
At the other five labels the first \(\epsilon^2\) coefficients are
\[
 N_{0,2}=-1,\quad
 N_{1,2}=N_{8,2}=-(2+4c-4c^2)/3<0,\quad
 N_{2,2}=N_{7,2}=-(2c-1)^2/3<0.                            \tag{15}
\]
All nine are retained, including the exact marked root \(1-\epsilon^2\).

Here is the ordinary completeness and uniformity bridge. The coefficients
of (7) are analytic in \((\epsilon,r)\), and at \(\epsilon=0\)
there are nine distinct roots \(\omega_j\), independent of \(r\).
Choose disjoint neighborhoods of those nine roots. The simple-root
implicit theorem and compactness of \([-R,R]\) give one common collar
with nine analytic branches and uniformly bounded derivatives through
the next order. They exhaust the degree-nine polynomial and remain
distinct. Taylor's theorem makes (14)--(15) uniform. Their fixed strict
leading signs give \(N_j<0\) on **every** branch for every sufficiently
small positive \(\epsilon\), uniformly for \(|r|\le R\).
No root of the real part, pair average, sampled polynomial or critical
tuple replaces these actual original roots.

The objective is computed directly from all eight critical distances.
Put \(q=q_1(r)\), temporarily omitting the common \(\epsilon^7\)
shift. Write \(a_z=1+u_z\), \(a_p=1+u_p\). The six equal squared
distances have coefficients
\[
 z_1=-2a_z,\quad z_2=a_z^2-2w_2+r^2/9,\quad
 z_3=2a_zw_2-2\mu-2rv_2/3.
\]
The pair squared distances are \(V\pm X\), with mean coefficients
\[
 v_1=-2a_p+H/2,\quad v_2'=a_p^2-2w_2+r^2+Hq,
\]
\[
 v_3'=2a_pw_2-2\mu+2rv_2+H(q^2+2\beta+d^2r^2)/2,
 \quad X^2=2Hr^2(d-1)^2\eta^3+O_R(\eta^4).
\]
For \(t=1+t_1\eta+t_2\eta^2+t_3\eta^3\), the inverse-square-root
coefficients through order3 are
\[
 1,\quad-t_1/2,\quad-t_2/2+3t_1^2/8,\quad
 -t_3/2+3t_1t_2/4-5t_1^3/16.
\]
The pair sum is \(2V^{-1/2}+3X^2/4+O_R(\eta^4)\), while the
six equal terms contribute six times the corresponding expression for
\(z\). Substituting (6) gives, as an identity of the **entire**
parameter polynomial,
\[
 F^0=8+C\eta+B_*\eta^2+[T_*+9H\kappa r^2]\eta^3+O_R(\eta^4).
                                                               \tag{16}
\]
In particular the quartic \(r^4\) pair-scale correction cancels from
the cost; the coefficient is exactly quadratic, not a small-skew fit.

The common real shift \(\epsilon^7\) changes each reciprocal term
by \(\epsilon^7+O_R(\epsilon^8)\), since the limiting distance
is 1 and its limiting real derivative is 1. It contributes **exactly8**
at order7. The exact squared-distance route is also reconstructed in
the checker through \(\epsilon^7\). All distances are bounded away
from zero on the common collar, so the uniform remainder follows from
analytic Taylor expansion. Finally, the imaginary critical cubes give
\[
 \sum_l(\Im\zeta_l)^3=3Hr\eta^2+O_R(\eta^3).
\]
This proves every assertion in (4). For any fixed prescribed real
\(\lambda\), choose \(r=\lambda/(3H)\); the limiting cost is
\(T_*+(\kappa/H)\lambda^2\), with actual all-nine strict feasibility.

## 5. Exact fixed cuts, endpoints and the maximal envelope

The direct all-competitor inputs are
[10152](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/third-boundary-optimum/PROOF.md)
and the credited 10113 motion law. On each fixed finite cap they give
uniformly, for actual competitors,
\[
 T_\eta\ge T_*+(\kappa/H)\lambda_\eta^2-O_T(\sqrt\eta),\quad
 R_\eta(p)=\Phi(|\lambda_\eta|)+O_T(\sqrt\eta).                \tag{17}
\]
Their entry and full necessary cost have no conjugacy, critical
separation, analytic critical-family or original-interior-motion premise.
They include all original and critical collisions permitted by the cap.

Fix \(T>T_*\). Since \(\Lambda>0\), (17) gives
\(|\lambda_\eta|\le\Lambda+O_T(\sqrt\eta)\), and then the
upper half of (5). Any fixed \(|\lambda|<\Lambda\) is realized
in the exact cut by (7) with constant \(r=\lambda/(3H)\), using its
strict positive cost gap. For either endpoint define
\[
 D=8H/(\kappa\Lambda),\qquad
 r_\eta^\pm=\pm[\Lambda-D\sqrt\eta]/(3H).                    \tag{18}
\]
These lie in a fixed compact interval. Their uniform construction gives
\[
 T_\eta=T_*+(\kappa/H)(\Lambda-D\sqrt\eta)^2
                      +8\sqrt\eta+O_T(\eta)
          =T-8\sqrt\eta+O_T(\eta)<T                         \tag{19}
\]
for **every** sufficiently small positive \(\eta\). Their actual
skews tend to \(\pm\Lambda\), and their motion is
\(\Phi(\Lambda)+O_T(\sqrt\eta)\). This proves the lower half
of (5), plus both exact-cut endpoint realizations. Necessity in (17)
and these constructions prove the full limiting skew interval.

The finite-cut maximum exists. The coefficient set of monic polynomials
with nine roots in the closed disk and marked root \(a\) is compact.
The extended reciprocal sum is lower semicontinuous under multiset root
continuity, so its finite sublevel is closed. It is nonempty by (19).
For sufficiently small \(\eta\), the uniform all-competitor entry
in 10113 gives disjoint common neighborhoods of the original labels.
Those simple-root maps, and hence \(R_\eta\), are continuous there.
The maximum follows from compactness. This is not a claim of exact
finite-\(\eta\) equality with \(\Phi(\Lambda)\).

## 6. Rigidity of maximizing sequences and the precise scope

In 10152's full necessary cost use the actual normalized chart
\(\widehat h=(\epsilon r_\eta+q,\epsilon r_\eta-q,
\epsilon t_1,\ldots,\epsilon t_6)\),
\(r_\eta=-\sum t_l/2\), and
\(v_\eta=(\widehat u-u^*)/\epsilon\). On a fixed cap it states
\[
 T_\eta=T_*+\kappa\lambda_\eta^2/H
 -\alpha H\sum_l(t_l+r_\eta/3)^2
 +\tfrac12\|v_\eta-d r_\eta h^*\|^2
 +\sum_{k=3,4}w_k(-\mathcal A_k)/\eta^3+O_T(\sqrt\eta),       \tag{20}
\]
where \(w_k>0\), \(\mathcal A_k=(N_k+N_{9-k})/2\le0\),
\(\lambda_\eta=3Hr_\eta+O_T(\eta)\), and every displayed
nonconstant payment is nonnegative. Critical permutations are simultaneous.

For any sequence in the exact cut with motion tending to
\(\Phi(\Lambda)\), strict increase of \(\Phi\) and (17) force
\(|\lambda_\eta|\to\Lambda\). Equation (20) and \(T_\eta\le T\)
then force
\[
 T_\eta\to T,\qquad
 \sum_l(t_l+r_\eta/3)^2\to0,\qquad
 \|v_\eta-d r_\eta h^*\|\to0,\qquad
 |N_j|=o(\eta^3),\ j=3,4,5,6.                              \tag{21}
\]
The last conclusion uses individual nonpositivity: each magnitude is at
most twice its pair average. Along a sign-convergent subsequence,
\(r_\eta\to\pm\Lambda/(3H)\). The credited strict all-nine
comparison gap in (3), together with the uniform motion remainder,
makes the actual unique farthest label eventually 7 on the positive
subsequence and 2 on the negative one. No critical tangent convergence
was assumed to obtain this conclusion.

The exact optimal cap \(T=T_*\) is **already feasible** by reviewer
four's separate
[10182 construction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/third-boundary-audit/PROOF.md).
That result has a strictly negative fourth upper term and quantitative
\(O(\eta^{1/4})\) equality-cap rigidity. It is credited prior mathematics,
not reproved or claimed new here. The current result treats the actual
nonzero-skew family and the maximal envelope for \(T>T_*\).
A universal sharp fourth coefficient, the sharp finite-size motion
correction at \(T=T_*\), exact finite-\(\eta\) skew intervals,
effective numerical collars and the global first-power endpoint remain open.

The finite checker compares full parameter-polynomial maps, all ten
primitive columns, all eight Newton moments, all nine root equations
and normals, both repair blocks and the actual FIRST-power distances.
Whole normal/optimized/cold records and deliberate damage controls are
same-author evidence. The uniform analytic collar, Taylor remainders,
compact all-competitor transfer and maximizing-sequence deductions are
ordinary written proofs and are not formalized by those finite checks.
