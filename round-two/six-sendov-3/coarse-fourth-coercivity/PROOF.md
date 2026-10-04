# Uniform fourth remainder and equality-cap stability for degree-nine FIRST power

Actual author **six-sendov-3**, role **researcher**, 2026-10-04.
Ordinary analytic proof with exact finite algebra; **unformalized and
independently unreviewed**. Inherited concentration and entry remain explicit.

Every original root of the monic complex degree-nine polynomial is in the
closed unit disk. Rotate an actual marked root to \(a=1-\eta>0\).
Count all eight critical points with multiplicity, allowing collisions,
and put \(F=\sum_{l=1}^8|a-\zeta_l|^{-1}\); zero denominators mean infinity.
No analytic critical labels or conjugate critical set are assumed.

Use the credited constants
\[
\begin{gathered}
c=\cos(\pi/9),\ y=[3(1+c)]^{-1},\ x=2/3-y,\ H=14y,\ U_0=-8x,\ C=8/3+y,\\
k=-7(1+2c)/18,\quad \rho=(c-5)/3,\\
\alpha=-527/360+41c/90+13c^2/90<0,\quad \tau=(k+\rho)^2/2,
\quad \kappa=\tau+10\alpha/27>0,\quad \sigma=\alpha+\rho^2/2,\\
B_*=2311/108+4934c/27-1976c^2/9,\\
T_*=-60800959/17496-307083769c/17496+10980067c^2/486,\\
u_z=(U_0+\rho H)/8,\quad u_p=u_z-\rho H/2,\quad b=\sqrt{H/2},\\
W_*=2512/27+5840c/9-21392c^2/27,\quad
D_*=-4270/27-29492c/27+4012c^2/3.
\end{gathered}                                                     \tag{1}
\]
The first two coefficients and selected profile belong to8619; the third
coefficient belongs to10152. REVIEW10182 confirms that third leaf relative
to its8619/10127 entry/projection boundary, and proves equality-cap
feasibility and a weaker quantitative rigidity bound. REVIEW10156 confirms
10113's tighter entry/motion leaf at the same boundary. These assessments
do not evaluate the present new theorem. Exact pins and scopes are in
[DEPENDENCIES.json](DEPENDENCIES.json).

## Conclusions

Put \(M_3(\eta)=8+C\eta+B_*\eta^2+T_*\eta^3\). There exist finite
(L) and \(\eta_0>0\) such that every actual competitor satisfies
\[
F\ge M_3(\eta)-L\eta^4\quad(0<\eta<\eta_0),\qquad
\inf_p F=M_3(\eta)+O(\eta^4).                                  \tag{2}
\]
The upper comparison uses10152's credited actual attaining family.
This improves its uniform \(O(\eta^{7/2})\) error without identifying
an optimal fourth coefficient or a limit of the divided fourth surplus.

For each fixed finite \(T\), on the actual arm
\(F\le8+C\eta+B_*\eta^2+T\eta^3\), define exact coordinates
\[
\begin{gathered}
h_l=\Im\zeta_l/\sqrt\eta,\quad u_l=\Re\zeta_l/\eta,
\quad W=(\Re\sum\zeta_l-U_0\eta)/\eta^2,
\quad D=(\Re\sum\zeta_l^2+H\eta)/\eta^2,\\
\bar h=\tfrac18\sum h_l,\quad
v=\sqrt{H/\|h-\bar h\mathbf1\|^2}(h-\bar h\mathbf1),
\quad \widehat u=u-\eta W\mathbf1/8,\\
h^*=(b,-b,0^6),\quad u^*=(u_p,u_p,u_z^6),\quad
d^2=\|v-h^*\|^2+\|\widehat u-u^*\|^2.
\end{gathered}                                                     \tag{3}
\]
The positive and negative imaginary outliers are uniquely identified on a
small collar; label them first. The six remaining labels may be permuted.
The normalizing denominator stays positive. At the original-root labels
near \(\omega_j=e^{2\pi ij/9}\), put
\[
N_j=(|Z_j|^2-1)/2,\quad \mathcal A_3=(N_3+N_6)/2,
\quad \mathcal A_4=(N_4+N_5)/2,
\]
\[
w_4=(c+2c^2-1)^{-1}>0,\quad w_3=\tfrac23[7-(2-2c^2)w_4]>0,
\quad \mathcal S=-w_3\mathcal A_3-w_4\mathcal A_4\ge0.           \tag{4}
\]
There is a fixed \(c_0>0\), independent of \(T\), and finite \(L_T\),
\(\eta_T>0\), such that every competitor on that arm satisfies
\[
F-M_3(\eta)\ge c_0\eta^2d^2+\mathcal S-L_T\eta^4.              \tag{5}
\]
Only the error and collar depend on \(T\). In particular, with
\[
\lambda=J_3(h)/\sqrt\eta=\eta^{-2}\sum(\Im\zeta_l)^3,
\quad \mathcal R=\sum(\Re\zeta_l-\eta u_l^*)^2,
\quad \mathcal I=\sum_{l=3}^8(\Im\zeta_l)^2,
\]
three smaller fixed positive constants give the simultaneous payments
\[
F-M_3(\eta)\ge c_1\eta^3\lambda^2+c_2\mathcal R+c_3\eta\mathcal I
                                      +\mathcal S-L_T\eta^4.     \tag{6}
\]
These are coarse constants, with no sharp-value claim.

For \(0\le e\le1\), actual \(F\le M_3(\eta)+e\eta^3\), and
\(E=e+\eta\), one common collar has
\[
\begin{gathered}
|\lambda|\le K\sqrt E,\quad \|(h,u)-(h^*,u^*)\|\le K\sqrt{\eta E},\\
|N_j|\le K\eta^3E\ (j=3,4,5,6),\quad
|W-W_*|+|D-D_*|\le K\sqrt{\eta E}.                            \tag{7}
\end{gathered}
\]
The equality cap therefore has skew \(O(\sqrt\eta)\), normalized joint
profile error \(O(\eta)\), and active slack \(O(\eta^4)\), improving
REVIEW10182's \(E=e+\sqrt\eta\). The result applies to arbitrary actual
polynomials, including critical collisions.

## 1. Precisely retained lower-order entry

From the stated component of10113/10156 and10152/10182, uniformly on any
fixed finite third arm, adopt
\[
\begin{gathered}
(h,u)=(h^*,u^*)+O_T(\sqrt\eta),\quad
W=W_*+O_T(\sqrt\eta),\quad D=D_*+O_T(\sqrt\eta),\\
\Im P_1,\Im P_2=O_T(\eta^2),\quad J_3(h)=O_T(\sqrt\eta),
\quad h\cdot u-kJ_3(h)=O_T(\eta^{3/2}),\\
\sum h=O_T(\eta^{3/2}),\quad \sum u=U_0+\eta W,
\quad \sum h^2=H+\eta(U_2-D),\quad U_2=\sum u^2,\\
\|\Im p\|_{\mathrm{coeff}}=O_T(\eta^2),\qquad
-O_T(\eta^3)\le N_j\le0\ (j=3,4,5,6).
\end{gathered}                                                     \tag{8}
\]
All nine original-root maps are uniquely defined and uniformly smooth in
one neighborhood of \(z^9-1\). Actual profiles may vary arbitrarily with
\(\eta\). Inherited concentration/rate entry is8619; the independently
rederived exact balanced invariant projection is10127. No whole8668
verdict or absolute replay of ancestral concentration is asserted.

The exact factor, with the six actual small points \(A_l\), actual
outlier center (B), and actual half-difference \(D_c\), is
\[
p'(z)=9\prod_{l=1}^6(z-A_l)[(z-B)^2-D_c^2],\quad
p(z)=\int_{1-\eta}^z p'(w)\,dw.                              \tag{9}
\]
Newton identities below use all eight actual coordinates of this factor;
they impose no mean restrictions or constructed repair ansatz. \(D_c\)
is distinct from the real scaled moment \(D\).

## 2. Preserve the full moving third jet

Define \(J_{21}=\sum h^2u\), \(J_4=\sum h^4\), \(U_3=\sum u^3\),
\(J_{22}=\sum h^2u^2\), \(J_{41}=\sum h^4u\), \(J_6=\sum h^6\).
Direct powers of the exact coordinates give
\[
\begin{array}{ll}
\Re P_1=U_0\eta+W\eta^2,&\Re P_2=-H\eta+D\eta^2,\\
\Re P_3=-3J_{21}\eta^2+U_3\eta^3,&
\Re P_4=J_4\eta^2-6J_{22}\eta^3+O_T(\eta^4),\\
\Re P_5=5J_{41}\eta^3+O_T(\eta^4),&
\Re P_6=-J_6\eta^3+O_T(\eta^4),\\
\Re P_7,\Re P_8=O_T(\eta^4).&
\end{array}                                                       \tag{10}
\]
Every imaginary power sum is \(O_T(\eta^2)\) or smaller by (8).
A real Newton correction with imaginary factors has at least two of them,
hence is \(O_T(\eta^4)\). Perform the finite Newton recurrence, integrate
\(9\sum(-1)^me_mz^{8-m}\), and anchor at \(1-\eta\). This gives
\[
\Re p=z^9-1+\eta g_2+\eta^2g_4(h,u,W,D)+\eta^3g_6(h,u,W,D)
                                   +O_{\mathrm{coeff},T}(\eta^4). \tag{11}
\]
Here \(g_6\) is the whole moving polynomial defined by (10), not its
stationary specialization. All ten columns are polynomial in the bounded
moving moments. The credited \(g_2,g_4\) are reproduced, and the entire
10152 ten-formal-moment primitive is compared before specializing \(U_0,H\).

For a root \(\omega_j\), define the complete moving root coefficients
\[
\begin{split}
L_j&=-g_2(\omega_j)/(9\omega_j^8),\\
d_j(g_4)&=-[g_4(\omega_j)+g_2'(\omega_j)L_j+36\omega_j^7L_j^2]/(9\omega_j^8),\\
e_j(g_4,g_6)&=-[g_6(\omega_j)+g_4'(\omega_j)L_j+g_2'(\omega_j)d_j
+g_2''(\omega_j)L_j^2/2+72\omega_j^7L_jd_j+84\omega_j^6L_j^3]/(9\omega_j^8),\\
n_j&=\Re(e_j/\omega_j)+\Re(L_j\overline{d_j}).
\end{split}                                                       \tag{12}
\]
All denominators are fixed nonzero simple-root derivatives. Thus these
are smooth polynomial functions of the moving moments. Uniform root
Taylor expansion has error \(O_T(\eta^4)\). Reflection makes the
pair-averaged half-normal even in \(\Im p\); removing that vector changes
the average by \(O_T(\|\Im p\|^2)=O_T(\eta^4)\). The real-part
polynomial need not be contained. Only the actual pairs supply
\[
\mathcal A_k=\eta^2[\mathcal T_k(h,u)-a_kW/8-b_kD/14]
+\eta^3n_k(h,u,W,D)+O_T(\eta^4),\quad k=3,4.                 \tag{13}
\]
Here \(a_3=b_3=3/2\), \(a_4=1+c\), \(b_4=2-2c^2\), and the credited rows are
\[
\begin{split}
\mathcal T_k={}&4+U_0-H/2+b_kU_0^2/14
+(1-\cos6\theta_k)(-U_0H/12+J_{21}/6)\\
&+(1-\cos5\theta_k)(H^2/40-J_4/20)+\mathcal K_k,\\
\mathcal K_k={}&-(7x^2/2+6xyq_k+5y^2q_k^2/2)s_k,\\
(q_3,s_3)&=(-1,3/4),\quad(q_4,s_4)=(-2c,1-c^2),\quad \theta_k=2\pi k/9.
\end{split}                                                       \tag{14}
\]
The checker derives whole moving equations and normals at all four active
labels, including reflection, rather than only fixed third constants.

The three scalar coefficients of each inverse distance are
\[
\begin{split}
f_1&=1+u-h^2/2,\quad f_2=(1+u)^2-3(1+u)h^2/2+3h^4/8,\\
f_3&=(1+u)^3-3(1+u)^2h^2+15(1+u)h^4/8-5h^6/16.
\end{split}
\]
Their remainder is uniformly \(O_T(\eta^4)\). Substitute the exact
mean/norm identities and eliminate (13) with the positive dual weights:
\[
F=8+C\eta+\eta^2\mathcal B(h,u)+\mathcal S
+\eta^3\Phi(h,u,W,D)+O_T(\eta^4),                            \tag{15}
\]
\[
\begin{gathered}
\mathcal B=K_0+U_2/2+\rho J_{21}+\sigma J_4,
\quad K_0=B_*-4u_z^2-\alpha H^2/2,\\
\Phi=2W-3U_2/2+3D/2+\sum f_3(u_l,h_l)+w_3n_3+w_4n_4.
\end{gathered}                                                     \tag{16}
\]
Crucially the full moving \(\Phi\) is Lipschitz near the stationary tuple.
Freezing it first would lose a displacement factor and recover only the
older \(O_T(\eta^{7/2})\) error.

## 3. Radial and normalization errors carry that displacement factor

Bounded moving \(n_k\), paired slacks \(O_T(\eta^3)\), and (13) imply
\[
|W-W_*|+|D-D_*|\le K_T(d+\eta).                               \tag{17}
\]
Indeed \(h-v,u-\widehat u=O_T(\eta)\), and the two stationary rows
are solved by \(W_*,D_*\). Their fixed determinant is
\(-3(c+2c^2-1)/224\ne0\). Solve the row differences, whose right side
is \(O_T(d+\eta)\); this uses only the old third-order slack bound.
Consequently \(\Phi-\Phi^*=O_T(d+\eta)\).

Put \(m=\bar h=O_T(\eta^{3/2})\). Exactly \(h=m\mathbf1+sv\), where
\[
s=\sqrt{1+[\eta(U_2-D)-8m^2]/H}
=1+\eta(U_2-D)/(2H)+O_T(\eta^2).
\]
Thus (17) and polynomial Lipschitz estimates give
\[
\begin{split}
h-v&=\eta(U_2^*-D_*)h^*/(2H)+m\mathbf1+O_T(\eta d+\eta^2),\\
u-\widehat u&=\eta W_*\mathbf1/8+O_T(\eta d+\eta^2),
\quad U_2^*=6u_z^2+2u_p^2.
\end{split}
\]
At the stationary tuple,
\(\nabla_u\mathcal B=u_z\mathbf1\), and
\(\nabla_h\mathcal B=2(\rho u_p+\sigma H)h^*\), orthogonal to
\(\mathbf1\). The mean term therefore has **zero stationary linear
payment**. Its gradient variation is \(O_T(|m|d)\le O_T(\eta d)\).
All quadratic Taylor remainders are \(O_T(\eta^2)\). Hence
\[
\mathcal B(h,u)=\mathcal B(v,\widehat u)+\eta N_*+O_T(\eta d+\eta^2),
\quad N_*=u_zW_*+(\rho u_p+\sigma H)(U_2^*-D_*).              \tag{18}
\]
Both normalization payments are retained. The credited constant identity,
exactly reproduced here, is \(\Phi^*+N_*=T_*\). Combining (15),(17),(18) gives
\[
F-M_3(\eta)=\eta^2[\mathcal B(v,\widehat u)-B_*]+\mathcal S
+O_T(\eta^3d+\eta^4).                                        \tag{19}
\]

## 4. Strict local positivity absorbs the remaining error

The credited exact balanced projection is
\[
\begin{gathered}
u_{\min}(v)=u_z\mathbf1-\rho v^2+(k+\rho)J_3(v)v/H,\\
K(v)=B_*+\alpha[J_4(v)-H^2/2]+\tau J_3(v)^2/H,\\
\mathcal B(v,\widehat u)=K(v)+\tfrac12\|\widehat u-u_{\min}(v)\|^2
+(k+\rho)J_3(v)\delta/H,
\quad \delta=v\cdot\widehat u-kJ_3(v)=O_T(\eta^{3/2}).        \tag{20}
\end{gathered}
\]
The last rate is the10152/10182 component of (8) after centering/rescaling.
The signed term, multiplied by \(\eta^2\), is \(O_T(\eta^4)\), since
\(J_3(v)=O_T(\sqrt\eta)\). The finite checker retains the whole
unconstrained projection defect before imposing balance, norm and mean.

No new global moment optimization is needed for local positivity. In the
exact balanced chart write
\[
v=(r+q,r-q,t_1,\ldots,t_6),\quad r=-\sum t_l/2,
\quad q^2=H/2-R_2/2-r^2>0,\quad R_j=\sum t_l^j.
\]
Literal sums give
\[
\begin{split}
J_3&=3Hr-3rR_2-4r^3+R_3,\\
J_4-H^2/2&=-HR_2+4Hr^2+R_4+R_2^2/2-4r^2R_2-8r^4.
\end{split}                                                       \tag{21}
\]
The entire quadratic part is
\[
Q_2=H[-\alpha R_2+(4\alpha+9\tau)r^2]
=9H\kappa r^2-\alpha H\sum(t_l+r/3)^2.                       \tag{22}
\]
It is positive definite: both squares vanish only when \(r=t_l=0\).
Since \(R_2=\sum(t_l+r/3)^2+2r^2/3\), it bounds \(aR_2\) for
some fixed \(a>0\). All omitted chart degrees are at least4; their
magnitude is \(O(R_2^2)\), using \(r=O(\sqrt{R_2})\) and
\(R_j=O(R_2^{j/2})\). Moreover \(q-b=O(R_2)\), so
\(\|v-h^*\|^2=2r^2+R_2+O(R_2^2)\). On one fixed small neighborhood
\(K(v)-B_*\ge a_1\|v-h^*\|^2\), \(a_1>0\).
The map \(u_{\min}\) is Lipschitz and takes \(h^*\) to \(u^*\).
Therefore
\[
\mathcal B(v,\widehat u)-B_*\ge a_2d^2-K_T\eta^2,\quad a_2>0, \tag{23}
\]
with \(a_2\) independent of \(T\). Entry brings every arm into that same
fixed neighborhood on a possibly \(T\)-dependent collar.

Insert (23) in (19). Young's inequality gives
\(K_T\eta^3d\le(a_2/2)\eta^2d^2+K_T^2\eta^4/(2a_2)\), proving (5).
An unsigned \(O_T(\eta^{7/2})\) error would not suffice for this step.
The fourth-scale profile normalization is a conclusion, not a premise.

To obtain (6), normalization errors are \(O_T(\eta)\). Thus
\(\mathcal R,\eta\mathcal I,\eta^3\lambda^2\le
K\eta^2d^2+K_T\eta^4\); for the last bound use the local Lipschitz
cubic moment and \(J_3(h^*)=0\). Allocate three smaller fixed shares
of the positive term in (5). For (2), use the single arm \(T=T_*+1\).
Outside it \(F>M_3+\eta^3\), which also implies (2), including infinity.
The credited attaining family supplies the infimum upper comparison.

## 5. Stronger rigidity and original-root motion

All \(e\in[0,1]\) competitors lie on the one \(T_*+1\) arm. From (5),
\(\eta^2d^2+\mathcal S\le K\eta^3(e+\eta)\).
Since \(E\ge\eta\), normalization errors \(O(\eta)\) are absorbed in
\(\sqrt{\eta E}\). Positive weights control both pair slacks; each
nonpositive individual normal has magnitude at most twice its pair
average's magnitude. Equation (17) controls W,D. The cubic Lipschitz
bound divided by \(\sqrt\eta\) controls \(\lambda\). This proves (7).

The credited10113 sharpened odd closure, together with its moving real jet,
is
\[
p=z^9-1+\eta g_2+\eta^2[g_4(h,u,W,D)+\lambda Q]+O_{\rm coeff}(\eta^3),
\quad Q(z)=\tfrac i2[(1+2c)(z^8+z^7-2)+(z^6-1)].
\]
Equation (17) gives \(g_4-g_4^*=O_{\rm coeff}(d+\eta)\). Uniform root
expansion therefore proves, for all nine labels,
\[
\max_j|Z_j-\omega_j-\eta L_j-\eta^2(d_j^*+\lambda W_j)|
\le K(\eta^2d+\eta^3)\le K\eta^{5/2}\sqrt E,                 \tag{24}
\]
where \(d_j^*=d_j(g_4^*)\), and the credited harmonic is
\(W_j=i[(3+4c)\omega_j-(1+2c)(1+\omega_j^{-1})-\omega_j^{-2}]/18\).
The scaled drift error from \(d_j^*\) is \(O(\sqrt E)\). At equality
the remainder in (24) is \(O(\eta^3)\), and the scaled drift error
is \(O(\sqrt\eta)\).

The credited10113 identity
\[
\max_j|d_j^*+\lambda W_j|
=\sqrt{\mathcal A+\mathcal B|\lambda|+q_*^2\lambda^2},
\qquad \mathcal A,\mathcal B,q_*^2>0,
\]
therefore approximates actual normalized motion with error
\(K\sqrt\eta\sqrt E\). At equality its bounds are
\(\sqrt{\mathcal A}-K\eta\) and \(\sqrt{\mathcal A}+K\sqrt\eta\).
No new norm-table or maximizing-label calculation is claimed.

The credited actual10212 endpoints, confirmed by10246, belong to this
same equality cap and have all nine originals strictly inside. They give
\(|\lambda|=\ell\sqrt\eta+O(\eta)\) and normalized motion
\(\sqrt{\mathcal A}+s_*\sqrt\eta+O(\eta)\), with \(\ell,s_*>0\).
Consequently the supremal absolute skew and excess supremal normalized
motion on the **full actual equality cap** are both \(\Theta(\sqrt\eta)\).
This proves the exponents, without asserting universal sharp values of
\(\ell\) or \(s_*\), or that the constructed endpoints maximize over arbitrary polynomials.

## Evidence and limits

The whole moving moment primitive, four active root equations/normals,
unconstrained projection, exact chart cost and quadratic part, normalization
payments and stationary T* are checked with Fraction arithmetic. Sign
certification isolates the unique physical zero of \(8c^3-6c-1\) in
\((15/16,47/50)\). Same-author arithmetic reuse is disclosed; no reviewer
code is imported. Commands and full comparison are in [README.md](README.md)
and [VALIDATION.json](VALIDATION.json). Baseline reproduction is validation.

Uniform concentration/entry, implicit maps, parity, Taylor bounds,
absorption, local positivity and collars are ordinary written bridges,
outside a formal kernel. The new theorem is independently unreviewed.
The next frontier is sharp arbitrary-competitor fourth reduction **after**
this derived precompactness. All eight real residuals remain allowed;
neither extra mean modes nor completeness of10254's constructed15-parameter
cap are settled. An optimal fourth coefficient, sharp universal skew/motion
constants, an effective numerical collar and the unrestricted complex
first-power conjecture remain unproved. Ordinary Sendov and the quadratic
Tang–Zhang theorem are prior literature.
