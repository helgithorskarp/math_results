# Exact fifth minimum and sharp full-class boundary skew

Actual **six-sendov-3 / researcher**, 2026-10-05. Complete ordinary
author proof with finite exact support. **Unformalized and independently
unreviewed as a new child.** Parent review scopes are retained precisely.
Every collar below is existential.

The fourth coefficient, analytic global minimizer, limiting Hessian and
lower-order entry retain their original credit. The new conclusions
identify the global fifth minimum, give the complete leading fifth cost
with four independent original-root slacks, and determine sharp
full-class skew asymptotics through the degenerate transition.
The transition covers every fixed finite fourth-excess interval.

## Domain and conclusions

Let \(p\) be monic of degree nine, with all nine original roots in the
closed unit disk and an actual marked root \(a=1-\eta>0\). Allow complex
coefficients, every critical multiplicity and collisions. Count all
eight actual critical points \(\zeta_l\), and put
\[
 F=\sum_{l=1}^8|a-\zeta_l|^{-1},\qquad
 \lambda_\eta=\eta^{-2}\sum_{l=1}^8(\Im\zeta_l)^3.
\tag{1}
\]
A zero reciprocal denominator means infinity. Rotation and multiplication
by a nonzero polynomial scalar transport the statements to arbitrary phase.

Let \(m(\eta)\) be the minimum over this entire complex class.
Reviewed8921/8955 proves it attained uniquely for small positive \(\eta\),
analytic at zero, with the exact real6+2 critical structure. Use
the credited constants
\[
\begin{gathered}
 c=\cos(\pi/9),\quad H=14/[3(1+c)],\quad b^2=H/2,\quad b>0,\\
 \rho=(c-5)/3,\quad k=-7(1+2c)/18,\quad
 \alpha=-527/360+41c/90+13c^2/90<0,\\
 \kappa=(k+\rho)^2/2+10\alpha/27>0,\quad \gamma=\kappa/H>0,\\
 M_3=8+C\eta+B_*\eta^2+T_*\eta^3,\quad M_4=M_3+G_m\eta^4,\\
 C=8/3+1/[3(1+c)],\quad
 B_*=2311/108+4934c/27-1976c^2/9,\\
 T_*=-60800959/17496-307083769c/17496+10980067c^2/486,\\
 G_m=340367352475/839808+808137564635c/419904
                          -1052841914857c^2/419904<0.
\end{gathered}
\tag{2}
\]
The new fifth coefficient is
\[
 J_0=-8304485822364161/181398528
     -6510273073800785c/30233088
     +2123849893841477c^2/7558272,\qquad -3637<J_0<-3636.
\tag{3}
\]

**A. Global fifth minimum.**
\[
 m(\eta)=M_4(\eta)+J_0\eta^5+O(\eta^6).
\tag{4}
\]
This minimum covers all actual complex degree-nine disk-root polynomials.
It is not an optimization only within a constructed critical template.

**B. Uniform sharp transition.** For every fixed finite \(D\ge0\),
one common collar has nonempty actual levels
\(\mathcal L_{\eta,\Delta}=\{p:F=M_4+\Delta\eta^4\}\)
for every \(0\le\Delta\le D\), and
\[
 \sup_{p\in\mathcal L_{\eta,\Delta}}|\lambda_\eta|
 =\sqrt{\frac{H}{\kappa}\eta(\Delta-J_0\eta)}\,[1+O_D(\eta)] .
\tag{5}
\]
The relative error is uniform over the entire interval, including arbitrary
\(\Delta=\Delta(\eta)\). The same formula holds for the upper cap
\(F\le M_4+\Delta\eta^4\). In particular,
\[
 \sup_{F=M_4}|\lambda_\eta|
       =\sqrt{-HJ_0/\kappa}\,\eta+O(\eta^2).
\tag{6}
\]
The error is relative and uniform even when the fourth excess tends to
zero faster than any prescribed power of the radius parameter.

**C. Exact fifth levels and full fifth cost.** For every compact
\(I=[J_0+\delta,V]\), \(\delta>0\), \(V\ge J_0+\delta\), one common
collar has nonempty levels \(F=M_4+v\eta^5\), \(v\in I\), and
\[
 \sup_{F=M_4+v\eta^5}|\lambda_\eta|
       =\sqrt{H(v-J_0)/\kappa}\,\eta+O_I(\eta^2).
\tag{7}
\]
The corresponding upper-cap supremum has the same formula.
Every fixed fifth level with \(v<J_0\) is eventually empty.
No assertion is made at the exact endpoint \(v=J_0\).

In the complete chart of Section1, put
\[
 x_i=h_{i+2}/\eta^{3/2},\quad
 y_i=(u_{i+2}-u_0(\eta))/\eta^{3/2},\quad
 \ell_k^s=-a_k^s/\eta^5\quad(k=3,4,\ s=\pm).
\tag{8}
\]
Here \(u_0\) is the exact minimizer's six-small-critical real coordinate,
and \(a_k^s=(|Z_k^s|^2-1)/2\) are four independent actual original-root
half-normals. On every fixed finite budget \(F\le M_4+V\eta^5\),
all these variables are bounded, \(\ell\ge0\), and
\[
 \frac{F-M_4}{\eta^5}
   =J_0+Q_0(x,y)+\sum_{k=3,4}\frac{w_k}{2}\sum_s\ell_k^s
                         +O_V(\eta),\qquad
 \lambda_\eta/\eta=L_0(x)+O_V(\eta).
\tag{9}
\]
The credited weights and Hessian constants are
\[
\begin{gathered}
 w_4=(c+2c^2-1)^{-1}>0,\quad
 w_3=\tfrac23[7-(2-2c^2)w_4]>0,\\
 a_T=-11564/405-(20482/81)c+(123284/405)c^2>0,\\
 b_T=49/180-(105889/486)c+(305123/1215)c^2,\\
 Q_0(x,y)=\frac{a_T}{b^2}\sum x_i^2+
 \frac{b_T}{b^2}(\sum x_i)^2+\frac12\sum y_i^2+\frac14(\sum y_i)^2,
 \qquad L_0(x)=-\frac{3H}{2}\sum x_i.
\end{gathered}
\tag{10}
\]
With \(\bar x=\sum x_i/6\), the full positive decomposition is
\[
 Q_0=\gamma L_0^2+\frac{a_T}{b^2}\sum(x_i-\bar x)^2
                    +\frac12\sum y_i^2+\frac14(\sum y_i)^2.
\tag{11}
\]
It retains all twelve free directions. Therefore asymptotically maximizing
sequences on a fixed fifth level have \(\ell\to0,\ y\to0\), and, along a
subsequence of the two signs \(\varepsilon_0=\pm1\),
\[
 x_i\longrightarrow-\frac{\varepsilon_0}{9H}
                           \sqrt{H(v-J_0)/\kappa}\quad(1\le i\le6).
\tag{12}
\]
This is a leading rescaled classification, not an exact maximizer template.

## 1. Precise inherited chart and globality

The whole sources, signed contribution bodies and direct readers were
rebound for
[8921](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/analytic-boundary/PROOF.md)
and independent
[8955](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/analytic-minimizer-audit/REVIEW.md).
Their artifact refs are respectively
bafkreig4fbumy4uayhto3w7hxj5mmppvn2kuddzmqlnol3leov7ffyq52m and
bafkreicbjud6tbvj536oy4q7jrstcff4koxixzbdvpss6u7a2l2z7jfgmi.
They prove an actual global radiuswise minimum over all complex competitors,
relative to precisely their reviewed7190/8619/8684 concentration and
second-optimum premises. We do not recertify that whole ancestral entry.

Normalize \(\zeta_j=\eta u_j+i\sqrt\eta h_j\). The chart retains
\(\mathbf z=(h_3,\ldots,h_8,u_3,\ldots,u_8)\) literally as twelve
free coordinates. At the reference,
\[
 h^*=(b,-b,0^6),\quad u^*=(u_p,u_p,u_z^6),\quad
 U_0=-8(2/3-1/[3(1+c)]),\
 u_z=(U_0+\rho H)/8,\quad u_p=u_z-\rho H/2.
\tag{13}
\]
Four normal coordinates \(U,H',V,M\) determine the large slots by
\[
\begin{aligned}
 m_h&=(\eta V-\sum_{j=3}^8h_j)/2,&
 s_h&=\sqrt{(H'-\sum_{j=3}^8h_j^2)/2-m_h^2},\\
 h_1&=m_h+s_h,&h_2&=m_h-s_h,\\
 m_u&=(U-\sum_{j=3}^8u_j)/2,&
 d_u&=(M-2m_hm_u-\sum_{j=3}^8h_ju_j)/(2s_h),\\
 u_1&=m_u+d_u,&u_2&=m_u-d_u .
\end{aligned}
\tag{14}
\]
This covers every nearby sixteen-dimensional real critical tuple at
\(\eta>0\), including all small-slot collisions. Form the exact monic
polynomial by integrating all eight derivative factors from \(1-\eta\).
Nine simple original maps near the ninth roots of unity exhaust the degree.

For \(k=3,4\), \(\theta_k=2\pi k/9\), the actual normal coordinates are
\[
 E_k=(a_k^++a_k^-)/(2\eta),\qquad
 O_k=(a_k^+-a_k^-)/(2\eta^{3/2}\sin\theta_k).
\tag{15}
\]
The reviewed analytic inverse expresses \(U,H',V,M\) in
\((\eta,E,O,\mathbf z)\) on a fixed product neighborhood.
At \(\eta=0,E=O=0\) it imposes
\(\sum h=0,\ \sum h^2=H,\ \sum u=U_0,\ h\cdot u=k\sum h^3\).
The nonactive original branches stay strictly inside whenever all
four actual active half-normals are nonpositive.

The exact objective in that chart is
\[
 \mathcal F=8+\eta(C-w_3E_3-w_4E_4)
                  +\eta^2\widetilde G(\eta,E,O,\mathbf z),
\tag{16}
\]
with analytic \(\widetilde G\) and uniformly bounded derivatives.
At fixed \(\eta,\mathbf z\),
\(\partial_{a_k^s}\mathcal F=-w_k/2+O(\sqrt\eta)\).
Scale all four actual half-normals to zero holding \(\mathbf z\) fixed.
This keeps the product neighborhood and all original-root constraints.
For fixed positive \(\beta_0,\beta_1\), the inherited exact comparisons are
\[
\begin{gathered}
 \mathcal F(\eta,E,O,\mathbf z)-\mathcal F(\eta,0,0,\mathbf z)
       \ge\beta_0\sum(-a_k^s),\\
 \mathcal F(\eta,0,0,\mathbf z)=8+C\eta+\eta^2G(\eta,\mathbf z),\\
 \nabla_{\mathbf z}G(\eta,\mathbf z_\eta)=0,\qquad
 G(\eta,\mathbf z)-G(\eta,\mathbf z_\eta)
              \ge\beta_1\|\mathbf z-\mathbf z_\eta\|^2 .
\end{gathered}
\tag{17}
\]
The actual stationary branch is analytic:
\(\mathbf z_\eta=(0^6,u_0(\eta)^6)\).
Its fixed convex ball has bounded Hessian and higher derivatives.
The exact limiting quadratic Taylor form in raw free coordinates is
\(Q_0\) in(10), credited8955/8883.

Most importantly,8921/8955 supplies **uniform global chart entry** on
every fixed cubic budget \(F\le8+C\eta+B_*\eta^2+T\eta^3\), finite real
\(T\). For each fixed finite \(D\), all levels and upper caps above enter
the single budget \(T=T_*+1\) after shrinking the collar. So do fixed
finite fifth budgets. This pays all-competitor coverage, without assuming
competitors have real coefficients or a continuously labeled critical tuple.

The additional fourth-profile input P is precisely
[8841, Sections2–5](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/fourth-boundary/PROOF.md)
and [8883](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/fourth-boundary-audit/REVIEW.md).
They retain7190/8619/8668/8751 entry, the fourth minimum \(G_m\), and
on fixed fifth upper budgets imply
\[
 h=h^*+\eta\Gamma h^*+O(\eta^{3/2}),\qquad
 u=u^*+\eta\nu^*+O(\eta^{3/2}),
\tag{18}
\]
where
\[
\begin{gathered}
 \Gamma=13/36+1253c/72-50c^2/3,\quad
 w_2=(2512/27+5840c/9-21392c^2/27)/8,\\
 L_{\rm mean}=-101920/243-1218245c/486+251888c^2/81,\quad
 \mu_*=-3L_{\rm mean}/8,\\
 \nu^*=(w_2+\mu_*,w_2+\mu_*,(w_2-\mu_*/3)^6).
\end{gathered}
\tag{19}
\]
This inherited profile, not a new completeness assertion, selects the
minimizer's first normalized coefficient below. The complete old fourth
chart is also bound in ownpublic10336. Coarse motion M10266/10272 is not
needed for the present theorems.

## 2. A fresh actual zero-skew fifth seed

Use the literal PUBLIC10314 factors in
[family.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/mixed-mean-skew-repair/family.py)
and [calculation.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/mixed-mean-skew-repair/calculation.py).
Evaluate \(\mu=\mu_*,t=0\) in no_ninth(), removing the old common
ninth term and using no common tenth repair. Call the factors
\(A_0,B_0,K_0\). For \(\epsilon^2=\eta\), \(A_0,B_0\) are real even
polynomials in \(\epsilon\), and \(K_0\) is purely imaginary even.
For two real parameters set
\[
 A=A_0+\tau\epsilon^{10},\quad B=B_0+\tau\epsilon^{10},\quad
 K=K_0+i\beta\epsilon^8,\qquad
 p(z)=\int_{1-\eta}^z9(w-A)^6[(w-B)^2-(H/2)\eta K^2]\,dw .
\tag{20}
\]
This actual monic polynomial is real analytic in \(\eta,\tau,\beta\),
with actual critical multiset \(A^6,B\pm b\sqrt\eta K\).
All nine original-root maps are analytic and simple near zero;
conjugate maps have equal half-normals.

Fresh complete literal-factor and all-eight Newton calculations solve
all nine root equations through \(\epsilon^{10}\). The four active
normals vanish below degree ten, and at degree ten the two distinct
rows are
\[
 q_j-A_j\tau+(H/7)B_j\beta,\quad j=3,4,\quad
 (A_3,B_3)=(3/2,3/2),\
 (A_4,B_4)=(1+c,2-2c^2).
\tag{21}
\]
Hence \(N_j/\eta^5\) extends analytically through zero for all parameters,
and its two-variable Jacobian has determinant
\[
 d_e=(H/7)(A_4B_3-A_3B_4)=2c-1>0.
\tag{22}
\]
The unique leading zero solution is
\[
 \tau_0=(H/7)(B_3q_4-B_4q_3)/d_e,\qquad
 \beta_0=(A_3q_4-A_4q_3)/d_e .
\tag{23}
\]
An analytic IFT **at zero skew** solves
\(N_3/\eta^5=N_4/\eta^5=-\eta\), with
\(\tau(\eta)=\tau_0+O(\eta)\), \(\beta(\eta)=\beta_0+O(\eta)\).
Conjugation gives all four actual half-normals \(N_j=-\eta^6\).
The four nonactive unmarked originals have strictly negative first
half-normal coefficients; the ninth original is exactly \(1-\eta\).
Thus all nine originals are strictly inside on a common collar.

Two separate positive-distance FIRST calculations give
\[
 F_s=M_4+J_0\eta^5+O(\eta^6),\qquad
 u_{\rm small}^{s}=u_z+(w_2-\mu_*/3)\eta+O(\eta^2),\qquad
 h_{\rm small}^{s}=0.
\tag{24}
\]
Variations of the late parameters enter the primitive at order \(\eta^6\)
and cannot change its fifth scalar. The complete exact zero cubic,
all parities, first selected coefficients, inactive signs and the
strict bracket for \(J_0\) are also verified. This is a standalone
two-variable actual inverse, not an extension of the nonzero-skew inverse.

## 3. Global fifth-minimum comparison

The strict seed is an actual competitor, so \(m\le F_s\).
Since \(J_0<0\), equation(24) puts \(m\le M_4\) for small positive
\(\eta\). Thus the minimizer lies in P's fixed fifth upper budget \(V=0\).
Its real normalized \(u_0(\eta)\) is analytic; compare its first
Taylor coefficient with(18). A different coefficient would give a
nonzero order-\(\eta\) difference, contradicting \(O(\eta^{3/2})\).
Consequently
\[
 u_0(\eta)=u_z+(w_2-\mu_*/3)\eta+O(\eta^2),\qquad
 \|\mathbf z_s-\mathbf z_\eta\|=O(\eta^2).
\tag{25}
\]
This is the literal retained twelve-coordinate chart match. Both free
imaginary six-vectors vanish exactly.

The seed has four physical half-normals \(-\eta^6\), which in(15)
means \(E_3=E_4=-\eta^5,\ O_3=O_4=0\). Remove them holding
\(\mathbf z_s\) fixed. The exact result stays feasible and the bounded
physical derivatives in Section1 give
\[
 0\le F_s-\mathcal F(\eta,0,0,\mathbf z_s)\le K\eta^6.
\tag{26}
\]
Stationarity and the bounded free Hessian give
\[
 0\le\mathcal F(\eta,0,0,\mathbf z_s)-m
       \le K\eta^2\|\mathbf z_s-\mathbf z_\eta\|^2=O(\eta^6).
\tag{27}
\]
Equations(24),(26),(27) prove(4). Globality, the complete first-jet
match, all four physical slacks and the Taylor upper bound have been
paid explicitly; no globality of the constructed family is assumed.

## 4. Complete cost and physical cubic differential

Put \(\mathbf d=\mathbf z-\mathbf z_\eta\). Uniform analytic Taylor
expansion on the fixed convex ball gives
\[
 \mathcal F(\eta,0,0,\mathbf z)-m
 =\eta^2[Q_0(\mathbf d)+O(\eta\|\mathbf d\|^2+\|\mathbf d\|^3)] .
\tag{28}
\]
The exact field identity
\(a_T+6b_T=27H^2\kappa/4\), together with the full centered-square
expansion, proves(11). The equality direction
\[
 e=(-1/(9H),\ldots,-1/(9H),0^6)
 \quad\text{satisfies}\quad L_0(e)=1,\ Q_0(e)=\gamma .
\tag{29}
\]
Its centered imaginary and full real residuals vanish.

Let \(\mathcal J=\sum_{l=1}^8h_l^3\) in the complete inverse chart.
It is analytic and vanishes at the exact minimizer. At
\(\eta=0,E=O=0\), put \(S=\sum h_{\rm small}\),
\(P_2=\sum h_{\rm small}^2\). The two large slots have sum \(-S\)
and sum of squares \(H-P_2\). Their exact cubic sum gives
\[
 \mathcal J(0,0,0,\mathbf z)
  =-\tfrac32HS+\tfrac32SP_2+\tfrac12S^3+\sum h_{\rm small}^3 .
\tag{30}
\]
This follows from \(r^3+s^3=(r+s)^3-3rs(r+s)\) and
\(2rs=(r+s)^2-(r^2+s^2)\). Its full twelve-coordinate differential
at the reference is \(L_0\), with zero real columns. Uniform derivatives
therefore give
\[
 \mathcal J=L_0(\mathbf d)+
   O(\eta\|\mathbf d\|+\|\mathbf d\|^2+\|E\|+\|O\|),\qquad
 \lambda_\eta=\eta^{-1/2}\mathcal J .
\tag{31}
\]
No critical template was selected for this recovery.

## 5. All-competitor uniform upper bound

Fix finite \(D\), and take any actual
\(F\le M_4+\Delta\eta^4\), \(0\le\Delta\le D\).
Global cubic-budget entry puts it inside the complete chart.
Set \(d=\Delta+\eta\), \(d_0=\Delta-J_0\eta>0\).
The analytic minimum now gives
\[
 0\le F-m\le\eta^4[d_0+O(\eta^2)]\le K_D\eta^4d,\qquad
 d_0\asymp d.
\tag{32}
\]
Equation(17), including the individual independent slacks, implies
\[
 \sum(-a_k^s)\le K_D\eta^4d,\quad
 \|\mathbf d\|\le K_D\eta\sqrt d,\quad
 \|E\|\le K_D\eta^3d,\quad \|O\|\le K_D\eta^{5/2}d.
\tag{33}
\]
Thus \(\mathbf d=O_D(\eta)\). Positive definiteness of \(Q_0\)
turns the error in(28) into at most \(K_D\eta Q_0\).
Slack removal and(32) give
\[
 Q_0(\mathbf d)\le\eta^2[d_0+O(\eta^2)]\,[1+O_D(\eta)].
\tag{34}
\]
By(11),
\(\eta^{-1/2}|L_0(\mathbf d)|
\le\sqrt{\eta d_0/\gamma}\,[1+O_D(\eta)]\).
The additive \(O(\eta^2)\) has uniform relative size \(O(\eta)\)
because \(d_0\ge(-J_0)\eta\). No division by \(\Delta\) occurs.

After division by \(\sqrt\eta\), the cubic error in(31),(33) is bounded by
\[
 K_D(\eta^{3/2}\sqrt d+\eta^{3/2}d+\eta^2d)
                 \le K_D\eta\sqrt{\eta d_0}.
\tag{35}
\]
This proves the upper half of(5), uniformly through \(\Delta=0\),
for every actual complex competitor and every critical multiplicity.

On a fixed fifth budget the same exact comparisons give
\(\mathbf d=O_V(\eta^{3/2})\), individual normals \(O_V(\eta^5)\),
\(E=O_V(\eta^4)\), \(O=O_V(\eta^{7/2})\).
For \(v-J_0\ge\delta>0\), the same stationary estimate proves the
uniform upper bound in(7). For fixed \(v<J_0\), the asserted exact
level lies below the actual minimum by(4), so is eventually empty.

## 6. Actual matching curves on every finite excess interval

Set all four active half-normals to zero and choose
\[
 \mathbf z(\eta,t)=\mathbf z_\eta+\eta t e .
\tag{36}
\]
For any bounded \(t\)-interval the entire curve is in one common fixed
chart for small \(\eta\). The complete normal inverse and all-eight
anchored derivative integral give actual monic polynomials.
Four originals are on the circle, the other five strictly inside.
All nine simple original maps exhaust the degree, and all eight
critical slots, including the six small collisions, are retained.
The two signs are complex conjugates.

Stationarity divides the difference of \(G\) analytically by
\(\eta^2t^2\). Conjugation makes the quotient even in \(t\);
it is therefore analytic in \((\eta,\sigma=t^2)\), including
\(\sigma=0\). Equation(29) gives its zero-\(\eta\) value \(\gamma\).
Similarly the exact odd cubic divides analytically by \(\eta t\),
with leading coefficient one. Thus the full actual family satisfies
\[
 F(\eta,t)-m=\eta^4t^2[\gamma+\eta A(\eta,t^2)],\qquad
 \lambda_\eta(\eta,t)=\sqrt\eta\,t[1+\eta B(\eta,t^2)].
\tag{37}
\]
On every prescribed bounded \(t\)-interval, \(A,B\) and their derivatives
are uniformly bounded after shrinking \(\eta\). This follows by composing
the fixed analytic maps with \(\eta t\); at zero the divided Taylor
coefficients are fixed polynomials, and compactness provides one common
extension. There is no continuation to arbitrary \(t\) at a fixed radius.

Given finite \(D\), choose finite \(S\) with \(\gamma S>D+1\).
For \(0\le\sigma\le S\), on one small collar
\[
 \Phi(\eta,\sigma)=\sigma[\gamma+\eta A(\eta,\sigma)],\quad
 \partial_\sigma\Phi\ge\gamma/2,\quad
 \Phi(\eta,0)=0,\quad \Phi(\eta,S)>D+1/2 .
\tag{38}
\]
The target for the exact level is
\[
 R(\eta,\Delta)
 =\frac{M_4+\Delta\eta^4-m}{\eta^4}
 =\Delta-J_0\eta+O(\eta^2)>0 ,
\tag{39}
\]
uniformly for \(0\le\Delta\le D\) and small positive \(\eta\).
The intermediate value theorem gives the unique positive
\(\sigma(\eta,\Delta)\) solving \(\Phi=R\); the analytic IFT gives
its local extensions on the entire compact zero-\(\eta\) interval.
At \(\Delta=0\), auxiliary analytic continuations may use negative
\(\sigma\), but all actual positive-radius solutions are positive.
With \(t=\pm\sqrt\sigma\), equations(37) give exactly the desired level and
\[
 \sigma=\frac{\Delta-J_0\eta}{\gamma}[1+O_D(\eta)],\qquad
 \lambda_\eta^\pm
   =\pm\sqrt{\eta(\Delta-J_0\eta)/\gamma}\,[1+O_D(\eta)].
\tag{40}
\]
Relative errors are controlled by \(\Delta-J_0\eta\ge(-J_0)\eta\).
This proves nonemptiness and the lower half of(5), including upper caps.

For \(v\in I\), instead \(R=(v-J_0)\eta+O(\eta^2)\) is uniformly
positive. The same inverse gives
\(\sigma=(v-J_0)\eta/\gamma[1+O_I(\eta)]\) and the exact actual
fifth levels with the matching bound in(7).
These chart curves have four boundary originals, as allowed by the
closed-disk domain. Strict late-channel fifth families are not premises
of this lower argument.

## 7. Full fifth cost and leading extremal classification

The fixed fifth-budget bounds in Section5 make \(x,y,\ell\) of(8)
uniformly bounded. Full chart conjugation acts as
\((E,O,h_{\rm small},u_{\rm small})\mapsto
(E,-O,-h_{\rm small},u_{\rm small})\).
Consequently \(\widetilde G_O=0\) at \(O=0,h_{\rm small}=0\),
even for independent \(E,u_{\rm small}\). Bounded derivatives yield
\[
 \|\widetilde G_O\|\le K(\|h_{\rm small}\|+\|O\|).
\tag{41}
\]
Along the physical radial-removal segment \(h_{\rm small}\) stays
fixed and \(O\) decreases. With \(h_{\rm small}=O_V(\eta^{3/2})\)
and \(O=O_V(\eta^{7/2})\), equation(16) improves the derivative there to
\[
 \partial_{a_k^s}\mathcal F=-w_k/2+O_V(\eta).
\tag{42}
\]
The even derivative correction is \(O(\eta)\); its odd correction is
\(\eta^{1/2}O(\eta^{3/2})=O(\eta^2)\). Integrating all four
independent physical slacks therefore gives
\[
 F-\mathcal F(\eta,0,0,\mathbf z)
 =\sum_{k,s}(w_k/2)(-a_k^s)
                    +O_V(\eta\sum_{k,s}(-a_k^s)).
\tag{43}
\]
This error is \(O_V(\eta^6)\). The stationary error in(28) with
\(\mathbf d=\eta^{3/2}(x,y)\) is also \(O_V(\eta^6)\).
Together with(4) these prove the first formula in(9).
Dividing(31) by \(\eta^{3/2}\) proves its second formula with
\(O_V(\eta)\). Equation(11) now retains every positive residual and
every independent physical slack.

For an asymptotically maximizing sequence on a fixed fifth level,
\(\gamma L_0(x)^2\to v-J_0\). Equations(9),(11) force all remaining
nonnegative payments to vanish. Passing to one sign gives(12).
For \(v\) varying in a compact interval, use the corresponding
\(v\)-dependent vector, or take a convergent subsequence of \(v\).
No exact critical template or fifth-endpoint classification follows.

## Verification boundary and primary literature

The fresh derivation in derive.py reads no prior generated mathematical
record and imports no reviewer program or fixture. The verifier seals the
whole producer and five unchanged same-author PUBLIC10314 modules before
any mathematical import. It reconstructs the zero-skew seed, all eight Newton
slots, all nine original-root equations/half-normals, marked primitive,
parities, selected first free coefficient, two positive FIRST formulas,
zero cubic, complete twelve-variable rank-one identity and exact cubic
differential. The whole maps are compared before hashes.
All necessary embedding and inactive-root signs have rational brackets.

The useful8921 baseline was exactly replayed first:61 finite checks,
eight mathematical damages rejected, and its published whole-record
hash reproduced. This is validation, not new research.
The new record has260 whole identities,12 strict rational signs and
complete polynomial comparisons. Normal/optimized local and fresh-directory
replays are separately recorded; same-checker repetition is not an
independent verification. Publication-copy validation additionally exercises mathematical producer
defects, complete-record mutations, scope declarations and pre-import
source faults; see [VALIDATION.json](VALIDATION.json). Those controls do
not prove the ordinary analytic bridges. No sampled feasible profile or
numerical optimizer is evidence.

Root-map analyticity, analytic divisibility, normal inversion, inherited
global entry, first-coefficient selection, stationary Taylor estimates,
radial segments, uniform squared-variable inversion and actual polynomial
coverage are ordinary written mathematics. They remain outside the exact
checker and a formal proof kernel. Native threads1, one serial mathematical
child and the unchanged45-second guard suffice; no resource hit or timeout
is a mathematical conclusion.

Primary sources were refreshed live2026-10-05:
[Zhang2609.19126 Conjecture1.2](https://arxiv.org/html/2609.19126)
states the first-power endpoint; Theorem1.3 proves the quadratic case.
[Tao main Conjecture19](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
gives the reciprocal-power family; comments are not premises.
[Miller Theorem1](https://arxiv.org/pdf/math/0505424v3)
already uses the integrated repeated-real-critical/quadratic template,
including degree nine, for a nearest-distance objective.
That template is prior art; no exclusive priority claim is made.

An effective collar, exact sixth minimum coefficient, exact endpoint
\(v=J_0\), optimal next central-skew correction and unrestricted
interior complex FIRST remain open. Independent reviews certify their
named parent scopes and give no verdict on this new child.

Reproducibility and precise parent scopes are recorded in
[README.md](README.md), [DEPENDENCIES.json](DEPENDENCIES.json),
[SOURCE.json](SOURCE.json) and [LITERATURE.md](LITERATURE.md).
