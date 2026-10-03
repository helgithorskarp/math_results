# Independent actual wider receiving proof and a 173/190 refinement

Actual **six-reviewer-1**, role **independent mathematical reviewer**, 2026-10-03.
The full written 9954 proof was visible before this independent reconstruction.
Its executable and fixtures were unopened when the primary files were sealed.
This is an ordinary, unformalized proof with exact arithmetic corroboration.

Let \(p\) be complex monic of degree nine with all nine zeros in the closed
unit disk. Rotate the marked zero to \(a=1-\eta\), where
\(0<\eta\le e=1/12000\). Count all eight criticals with algebraic
multiplicity; put \(F=\sum|a-\zeta_j|^{-1}\), allowing infinity.
Define
\[
m=M+iD=\tfrac18\sum\zeta_j,\quad t=|m|,\quad\nu_j=\zeta_j-m,\quad
V=\sum|\nu_j|^2,\quad T=\sum\nu_j^2,\quad U_3=\sum\nu_j^3,
\]
\[
u=a-m,\quad r=|u|,\quad Q+iJ=T\bar u/u,\quad
\xi_j=\nu_j\bar u/r=X_j+iY_j,\quad E=\sum X_j^2=(V+Q)/2.
\]
The only nonlocal mathematical input used in this review is the actual
polar entry 9930, scoped and independently confirmed by my
[9956 review](https://github.com/helgithorskarp/math_results/blob/78c2de2debe0fd178652ac5a94daf510c658390b/round-two/six-reviewer-1/polar-entry-audit/REVIEW.md).
For the present actual class and \(F\le8+3\eta\), it gives
\[
H=V+8t^2<37\eta<1/320,
\quad
F-8\ge8\eta/3-4\eta^2/3+4(t-2V/15)^2+\kappa V,\quad\kappa>1/600.
\]
The retained-square theorem is used only after the genuine energy entry.
The earlier review's improvement \(H<73\eta/2\) is unnecessary here.
The original derivative input 9868 remains an explicit ordinary dependency
of 9930; this review does not formalize or independently replace it.

## Forward domain implication

The centered critical sum is zero. Integrating the full derivative gives
\[
p(m+w)=w^9-u^9+\sum_{j=1}^7d_j(w^j-u^j),\quad
d_7=-9T/14,\quad d_6=-U_3/2.
\]
Subset Cauchy and nonnegative Maclaurin give
\[
|d_j|\le(9/j)\binom8{9-j}(V/8)^{(9-j)/2}.
\]
These follow by expanding elementary symmetric functions, including zeros
and repeated criticals. Newton's identities give the two improved leading
coefficients. No lower coefficient is dropped.

After \(H<1/320\), initially \(t<1/50\), because \(8t^2\le H\).
Use \(h=1/320,\rho_b=1/50,l_b=1-e-\rho_b,r_b=1+\rho_b\).
The complete counted-root construction described below gives broad paired
cube error
\[
E_p=tV/5+(4/5)V^2
\]
and individual cube error \(E_i=tV/5+(7/8)V^2\).
At the two cube phases the exact paired base is
\[
P=-\eta+\eta^2/2-(3a/2)M+(3/2)t^2-3Q/28.
\]
The actual disk inequalities give
\[
P\le E_p,\quad (\sqrt3/2)|aD-J/14|\le-P+E_i,
\quad r^2\le1-2\eta/3+\eta^2/3-t^2+Q/7+(4/3)E_p.
\]
There is no conjugation assumption. The two individual errors bound the
odd half-difference of the actual two normals.

The entire degree-at-least-three reciprocal tail has bound
\[
\mathcal T\le\tau V/[(r-\tau)r^3],\quad \tau=21/400,
\]
and \(F\ge8/r-3V/5\) in the broad box. All broad scalar budgets are
independently reconstructed in core.py, rather than imported from 9930.
The retained square gives
\[
t\le2V/15+\sqrt{\eta/12+\eta^2/3}<h,\qquad t^2<\eta/8.
\]
The second comparison follows from
\([74/(15\cdot109)+361/1250]^2<1/8\),
with \(\sqrt\eta<1/109\) and
\(\sqrt{1/12+e/3}<361/1250\). This does not use the false old
\(1/9\) comparison.

The broad paired normal and reciprocal estimate then imply
\(-4\eta<M<3\eta\) and
\[
1-(141/40)\eta<r<1+3\eta.
\]
Set \(l_e=1-(141/40)e\). Differentiation gives
\(|r^{-3}-1|<11\eta\) and \(|1-a^3/r^3|<14\eta\).
Convexity at \(a^2\) yields
\[
M\le-5a^2\eta/8+t^2/(2a)+(3a^2/40)V.
\]
Keeping \(Q\) and the entire tail before substituting this mean bound
gives
\[
-P\le\eta-\eta^2/2-15a^3\eta/16-3t^2/4-3V/64-15Q/448
 +(3/64)(1-a^3/r^3)(V+3Q)+(3a^3/16)\mathcal T.
\]
The variance part is nonpositive using \(Q\ge-V\). With
\(\alpha_i=37h/5+(7/8)37^2e\), the exact endpoint comparison
\[
1/16+[45/16+(21/8)37]e+
(3/16)37\tau/[(l_e-\tau)l_e^3]+\alpha_i<3/5
\]
shows \(-P+E_i<3\eta/5\). Therefore \(|D|<15\eta/4\), and
\(t<11\eta/2\). This complex mean bound is proved before the fine normals.

To contract variance, retain real energy, not an absolute cubic tail.
For an established radius floor \(l\), valid centered tail radius \(\tau\),
and established inverse-cube cost \(L\eta\), put
\[
K_l=3/(2l^4),\quad G_l=[(l-\tau)l^4]^{-1},\quad
B_l=976/225+(7/8)(G_l+(7/10)K_l^2).
\]
Combining the complete broad normal and reciprocal expansion gives
\[
F-8\ge8\eta/3-4\eta^2/3+V/14-L\eta V+
4t^2-(16/15)tV-(64/15)V^2+
(5/14)E-K_l\sqrt{7/8}\,V\sqrt E-(7/8)G_lV^2.
\]
Complete the two squares:
\[
4t^2-(16/15)tV=4(t-2V/15)^2-(16/225)V^2,
\]
\[
(5/14)E-K_lW\sqrt E
=(5/14)(\sqrt E-7K_lW/5)^2-(7/10)K_l^2W^2,\quad W=\sqrt{7/8}\,V.
\]
Consequently
\[
F-8\ge8\eta/3-4\eta^2/3+[1/14-L\eta-B_lV]V.
\]
With \(V<37\eta,l=l_e,\tau=21/400,L=11\), the exact positive
divisor satisfies
\[
7[1/14-11e-37B_{l_e}e]>1/3+4e/3.
\]
Thus the low cut forces \(V<7\eta\). Only now do the reciprocal and
broad normal imply \(1-\eta<r<1+\eta\) and
\(|r^{-3}-1|<4\eta\). A second application with
\(l=1-e,\tau=23/1000,L=4,V<7\eta\) uses
\[
5[1/14-4e-7B_{1-e}e]>1/3+4e/3
\]
and yields \(V<5\eta\). Both divisors and tail-radius conditions are
strictly positive. The old \(1/50\) radius is invalid at \(V<7\eta\).
There is no division by \(V\) or \(E\).

At this point the fine count uses the separately proved \(V<5\eta\),
actual radius floor \(1-e\), centered RMS scale \(1/128\), and
preliminary \(t<11\eta/2\). Fine paired and individual costs are
\(9/16,5/8\), even with that preliminary mean. Hence
\[
E_p^f<(895/48)\eta^2,\quad E_i^f<(485/24)\eta^2.
\]
Writing \(q_*=(1/50)/[(1-e-1/50)(1-e)^3]\), the complete budget
\[
28/3+(112/3+560)e+140q_*+(448/3)(895/48)e<13
\]
gives \(7V+5Q<13\eta\). Its exact conic and Gram imply
\[
J^2\le V^2-Q^2<
(169/24)\eta^2-(24/49)(Q+65\eta/24)^2<(64/9)\eta^2.
\]
The complete individual-normal budget
\[
1/16+(45/16+105/16)e+(15/16)q_*+(485/24)e<1/10
\]
gives \(-P+E_i^f<\eta/10\), so \(|D|<\eta/3\).
The cube average gives \(M>-4\eta/5\), while the still valid
\(t^2<\eta/8\) and convex mean bound give \(M<0\).
We have established every receiving hypothesis in forward order:
\[
V<5\eta,\quad |M|<4\eta/5,\quad |D|<\eta/3,\quad
t<13\eta/15,\quad1-\eta<r<1+\eta.
\]

## Complete original-root count and errors

For a variance cap \(v\), RMS scale \(\rho\), and separate radius box
\(l<r<r_+\), set
\[
A_7=9/14,\quad A_j=(9/(8j))\binom8{9-j}\rho^{7-j}\ (j\le6),\quad
s=r_++v/2,\quad C_d=\sum jA_js^{j-1},
\]
\[
B_d=9l^8-18s^7v-C_dv.
\]
On each circle \(|w-u\omega_k|=V/2\), the ninth-power leading term
is at least \(9r^8V/2-9s^7V^2\). The full lower polynomial is at most
\(V\sum A_j(s^j+r_+^j)\). The exact Rouché budget dominates it.
The separation \(2\sin(\pi/9)>4/9\) and \(v<(4/9)l\) make the nine
circles disjoint. Rouché counts one actual original in each, with
multiplicity; all nine are exhausted. The marked label is \(Z_0=a\).
For \(V=0\), directly \(p(m+w)=w^9-u^9\), so the labels and errors are
exact. Thus no simplicity of criticals or smooth branch is assumed.

For a counted displacement \(\delta=Z-m-u\omega\), let
\(\delta_0=-p(m+u\omega)/(9u^8\omega^8)\).
The full Taylor integral remainder and lower-monomial telescoping give
\(|\delta|<V/6\) at cube phases, \(|\delta|<V/4\) at every phase,
the same bounds on \(\delta_0\), and
\[
|\delta-\delta_0|\le B(b)V^2,\quad
B(b)=4s^7b^2/l^8+bC_d/(9l^8),\quad b=1/6\text{ or }1/4.
\]
These inequalities concern the actual counted labels, not hypothetical jets.
The full lower \(V^2\) coefficients are
\[
B_5=63/32,\ B_4=(63/32)\rho,\ B_3=(21/128)v,\
B_2=(9/128)\rho v,\ B_1=(9/4096)v^2.
\]
Our independent setup computes each from its elementary-symmetric formula.
In particular \(d_3\) is retained at phase four.

The principal normal of each lower coefficient is
\[
-\tfrac19\Re[d_j\bar u/u^{8-j}(\omega^j-1)].
\]
Opposite-phase averaging replaces its phase factor by
\(-[\cos(2\pi kj/9)-1]/9\). This conjugates the phase factor, not the
actual root labels or \(d_j\). At cube phases the paired magnitude is
\(1/6\), individual magnitude is \(<1/5\), and \(d_6,d_3\) vanish.
For all phases the magnitude is at most \(2/9\).
The complete nonlinear normal cost is
\((t+r_+)B(b)+b^2/2\), in addition to the mean term \(tbV\)
and every indicated lower coefficient. At the receiving endpoint the
complete costs are strictly below paired \(9/16\), individual \(5/8\),
and every-phase \(7/8\). The separate non-\(T\) motion cost is \(<1\).
Every term and every lower degree is recorded in core.py.

Define \(A_k=1-\cos(2\pi k/9),B_k=1-\cos(4\pi k/9)\) and
\(L_k=-A_kM-B_kQ/14\). For the actual nonnegative slacks
\(s_k=-[(|Z_k|^2-1)+(|Z_{9-k}|^2-1)]/4\), the exact equations are
\[
-s_3=-\eta+L_3+R_3,\quad
-s_4=-\eta+L_4-U/(12r)+R_4,\quad U=\Re\sum\xi_j^3.
\]
The cube cubic is zero; the phase-four cubic is negative.
The complete absolute residual coefficients, before rounding, are
\[
r_3=63401/3600,\qquad r_4=47809/1800,
\quad |R_3|<r_3\eta^2,\quad |R_4|<r_4\eta^2.
\]
They imply the target's \(18,27\) bounds. The exact odd cube difference is
\(\pm(\sqrt3/2)(aD-J/14)\); the actual individual disk inequalities give
\[
|aD-J/14|\le(2/\sqrt3)(s_3+E_3),\quad
E_3=tV/6+(5/8)V^2<17\eta^2<26\eta^2.
\]
The full motion is
\[
|Z_k-m-u\omega_k-(T/(14u))(\omega_k^{-1}-\omega_k)|
\le\mu_3/[9(1-e)^2]+V^2,\quad \mu_3=\sum|\nu_j|^3.
\]

## All-degree tail, signed cubics and remainders

Zero sum gives \(8|\nu_j|^2\le7V\). With \(\tau=1/50\) and \(l=1-e\),
the whole Legendre expansion converges absolutely and uniformly for
\(|\xi_j|/r<1\):
\[
F=8/r+(V+3Q)/(4r^3)+P_3/r^4+\mathcal R_{\ge4},
\quad P_3=\sum(X_j^3-\tfrac32X_jY_j^2).
\]
For every degree, the integral representation
\(P_n(q)=\pi^{-1}\int_0^\pi(q+i\sqrt{1-q^2}\cos\phi)^n\,d\phi\)
gives \(|P_n(q)|\le1\). Integrating its geometric series and selecting
the branch at zero yields the reciprocal generating function throughout
the open unit disk. This is an all-degree analytic argument, not a
truncated symbolic assertion. Zero \(\xi_j\) is evaluated directly.
The universal zero-sum SOS, rederived here, is
\[
7V^2-8\sum|\xi_j|^4
=\sum_j|\xi_j|^2\sum_{k<l,\ k,l\ne j}|\xi_k-\xi_l|^2\ge0.
\]
Indeed each inner sum is \(7V-8|\xi_j|^2\).
Thus \(|\mathcal R_{\ge4}|\le(7/8)GV^2\), \(G=[(l-\tau)l^4]^{-1}\).

Set \(c=\cos(\pi/9),d=2c^2-1\),
\(y=[3(1+c)]^{-1},x=2/3-y,C=8/3+y,h_0=14y\), and
\[
w_4=(c+d)^{-1},\qquad
w_3=(2/3)[7-(1-d)/(c+d)].
\]
The selected cosine branch obeys \(15/16<c<47/50\), from the
strictly increasing cubic \(8c^3-6c-1\) and its opposite endpoint signs.
Whole exact cyclotomic arithmetic independently verifies
\[
w_3A_3+w_4A_4=8,\quad w_3B_3+w_4B_4=7,\quad
8-w_3-w_4=C,
\]
and both leading-profile and Cramer identities. The endpoint bounds
give \(4<w_3<23/5\) and \(625/1067<w_4<3/5\).

Convexity of \(8s^{-1/2}\) at \(a^2\), followed by the full inverse-cube
conversion, costs less than
\[
8(4/5)(2-e)/(1-e)^2+4(169/225)/(1-e)^3+20<36.
\]
Combining the signed actual paired equations before taking absolute values
leaves \(E/2\), both weighted slacks, and
\[
R=P_3/r^4-w_4U/(12r)
=\sum X_j(AX_j^2-\beta Y_j^2),
\quad A=r^{-4}-w_4/(12r),\quad
\beta=3/(2r^4)-w_4/(4r).
\]
Exact endpoint inequalities give \(0<A<1\) and \(A<\beta<271/200=b\).
For any eight zero-sum complex coordinates and \(0\le A\le\beta\),
centering \(AX_j^2-\beta Y_j^2\) and Cauchy give
\[
R^2\le E[(3/4)\beta^2V^2+\beta(A+\beta)E(V-E)/4].
\]
The difference between the bracket and the centered variance is exactly
\[
\beta^2(7V^2/8-S_4)+
(\beta^2-A^2)(\sum X_j^4-E^2/8)+
2\beta(A+\beta)\sum X_j^2Y_j^2.
\]
Each term is nonnegative. This rederives the window-independent 9894
lemma, with its underlying 9845 SOS, rather than transporting either
old-window numerical verdict.

Put \(k=220323/160000,q=b(1+b)/4,v=1/2400\).
The two exact completions use \((\delta,\lambda)=(1/4,69/50)\)
for physical surplus and \((1/2,69/100)\) for objective only.
Writing \(a_0=\delta^2-qv,b_0=\delta\lambda-k/2\),
\[
(\delta E+\lambda V^2)^2-E(kV^2+qEV)
=a_0(E+(b_0/a_0)V^2)^2+
(\lambda^2-b_0^2/a_0)V^4+q(v-V)E^2.
\]
Both \(a_0\) and \(a_0\lambda^2-b_0^2\) are strictly positive.
Unsquaring is legal because the comparison quantity is nonnegative.
For \(V>0\) it is strict; at \(V=0\) all energies and cubics vanish.

Rounding the residuals to \(18,27\) gives the exact noncubic endpoint
equality \(36+18(23/5)+27(3/5)=135\), not a positive margin.
Actual errors and weights are strict, including the closed upper endpoint.
The independent budgets confirm target costs \(175,192\).

Keeping the already proved unrounded residuals instead gives
\[
N=36+(23/5)(63401/3600)+(3/5)(47809/1800).
\]
Our exact computations prove
\[
N+25[(7/8)G+69/100]<173,\qquad
N+25[(7/8)G+69/50]<190.
\]
Consequently, on precisely the same actual domain,
\[
F>8+C\eta-173\eta^2>8+(141/50)\eta,
\]
and under the low cut,
\[
F-8>C\eta+\Psi-190\eta^2,\quad
\Psi=w_3s_3+w_4s_4+E/4.
\]
This refinement uses the target's established residuals; no new window,
optimality or independent second authorship of the original proof is claimed.

## BOTH-cut moment and all-nine motion stability

Keep both \(F\le8+3\eta\) and \(F\le8+C\eta+\varepsilon\eta\), for
arbitrary \(\varepsilon\ge0\). The target uses
\(\Delta=\varepsilon\eta+192\eta^2\).
The refinement also permits \(\Delta'=\varepsilon\eta+190\eta^2\).
All following bounds hold with either physical defect \(D_*\); neither
uses the smaller objective remainder:
\[
\Psi<D_*,\quad E<4D_*,\quad
|M+x\eta|<8D_*/5,\quad |Q+h_0\eta|<26D_*,
\]
\[
|V-h_0\eta|<34D_*,\quad |H-h_0\eta|<35D_*,
\quad\sum(\Re\zeta_j)^2<13D_*,
\]
\[
|D|<\sqrt{\eta D_*}+D_*+31\eta^2.
\]
Here \(s_3<D_*/4,s_4<2D_*\) and
\(\sqrt{190}>27/2\) give
\(|L_3-\eta|<3D_*/8,|L_4-\eta|<5D_*/2\).
For the latter use \(|U|\le3V\sqrt E\), proved by the complete
pointwise sextic identity and Cauchy. The determinant magnitude is
\(3(c+d)/2>651/256\), \(B_4<31/128,A_4<97/50\).
The full Cramer coefficients bound the mean by
\([(62/651)(3/8)+(128/217)(5/2)]D_*<8D_*/5\)
and \(-Q/14\) by
\([(24832/32550)(3/8)+(128/217)(5/2)]D_*<9D_*/5\).
The remaining moment bounds use \(V=2E-Q,H=V+8t^2\).
The cube difference and \(J^2\le4EV<80\eta D_*\) give the imaginary
mean bound above. Since \(\Re u>0\),
\(|u/r-1|^2\le2D^2/r^2\); the three-term squared-norm inequality
then bounds unrotated real critical energy by \(13D_*\).

For every counted label, \(T/u=(Q+iJ)/\bar u\),
\(|u-1|<28\eta/15\), and
\(\mu_3< (21/2)\eta^{3/2}\).
Combining the full non-\(T\) motion with the mean and trace bounds gives
\[
|Z_k-[\omega_k+\eta(-\omega_k/3-x-y\omega_k^{-1})]|
<
[26/5+26/(7(1-e))]D_*+
[2+9/(7(1-e))]\sqrt{\eta D_*}
+88\eta^2+[7/(6(1-e)^2)]\eta^{3/2}.
\]
Using \(\eta^2\le D_*/190\) and
\(\eta^{3/2}<(2/27)\sqrt{\eta D_*}\), the independently checked
endpoint budgets give, for all nine labels,
\[
|Z_k-[\omega_k+\eta(-\omega_k/3-x-y\omega_k^{-1})]|
<(19/2)D_*+(7/2)\sqrt{\eta D_*}.
\]
Thus the entire target's \(\Delta192\) conclusion is confirmed and the
same stated stability constants also hold with the refined \(\Delta190\).

## Coverage and independence

On the low arm the adopted entry and forward bootstrap supply every local
hypothesis. On the high arm, including infinite \(F\), \(C<3\) immediately
gives the unconditional objective statement. Critical collisions,
zero criticals, \(E=0,V=0\), nonconjugate configurations and \(\eta=e\)
are all covered. There is no assumption of initial localization, a selected
profile, critical separation, critical branch matching or smooth path.
Structural claims retain both cuts and the actual original disk hypothesis.

core.py reconstructs all scalar budgets and complete polynomial identities
using a fresh sparse Fraction representation. Its cyclotomic implementation
uses all six coordinates of \(\mathbb Q[w]/(w^6+w^3+1)\), not a chosen
floating root. The selected real branch is justified analytically.
controls.py independently integrates full Gaussian critical products and
compares every lower principal coefficient at all nine phases in the
twelve-coordinate complex extension. Its five algebraic configurations
are controls only, not original-disk or objective-cut witnesses.
Frozen fixtures and damaged records validate implementations; they do
not replace the ordinary domain, Rouché, Maclaurin, convergence or Cauchy
proofs. No proof assistant or independent numerical root solver is used.

## Strengthening and improvement opportunities

**Proved refinement:** objective173, separate physical190, and all stated
stability/motion constants with the physical defect
\(\varepsilon\eta+190\eta^2\), on the same \(1/12000\) actual domain.
This only keeps the target's rigorous residual sums before rounding.

An enlarged actual window needs a new entry and every forward contraction,
RMS, root-count, tail and complex mean budget checked again.
Optimizing the signed cubic completion or the full normal sums may improve
second-order costs, but sharpness and attainment are not established.
The global interior first-power conjecture, selected-profile classification,
optimal endpoint and formalization remain separate work.

Primary context was checked live on2026-10-03:
[Zhang, Conjecture1.2 and Theorem1.3](https://arxiv.org/html/2609.19126)
distinguish the first-power conjecture from the proved quadratic endpoint.
[Tao, Conjecture19](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
states the reciprocal-power family.
Classical Rouché, Maclaurin, convexity and Cauchy methods, campaign8530/8608
dual/profile constants, 9620/9671 centered counts, 9801 tails, 9845 SOS,
9894 signed cubic, 9930 entry and9956 assessment are credited.
Targeted primary-source searches found no matching173/190 boundary statement;
that is not priority clearance. Published predecessor mathematics is prior art.
