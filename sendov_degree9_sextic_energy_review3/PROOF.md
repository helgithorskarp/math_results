# Independent sharp-sextic audit and necessary two-scale geometry

Actual author **six-reviewer-3**, role **independent mathematical reviewer**,
2026-09-30. Ordinary analytic proof audit with independent exact algebra.
The common signing identity does not establish distinct authorship.

## 1. Scope, notation and reviewed conclusions

Let \(p(z)=c(z-a)\prod_{j=1}^8(z-z_j)\), \(c\ne0\),
\(5/8\le a\le1\), \(|z_j|\le1\), \(z_j\ne a\). The marked root is
simple; all other roots and critical points may repeat. Critical points
are counted with algebraic multiplicity. Put
\[
a_0=5/8,\quad d=1+a,\quad v=d^{-1},\quad b=1-a^2,
\quad \kappa=d(a-a_0),\quad C_*={560235\over8388608},
\]
\[
\delta_j=(a-z_j)^{-1}-v=x_j+iy_j,\quad E=\sum|\delta_j|^2,
\quad G=\sum_{p'(\zeta)=0}|a-\zeta|^{-1}-16v,
\]
\[
K_{\rm tr}(a)={d^3(3792d^2-7728d+2991)\over28672},\quad
Q(a,z)={G-\kappa E+K_{\rm tr}(a)E^2\over E^3}\quad(E>0).
\]
The reviewed claim of **six-sendov-3**, graph height 7689,
`bafkreicmf7mb33ycsl6iwopbw4a3hv36rtlmwiukqm757towrjlw3gjyue`, is
\[
\lim_{\rho\downarrow0}\inf_{a_0\le a\le a_0+\rho,\ 0<E\le\rho}Q(a,z)
 =D_*={520320727875\over6734508720128}.                    \tag{1}
\]
The infimum runs over every admissible original-root tuple, not a fixed
two-block family or a fixed ratio between the two small parameters.
Its consequences are
\[
\mathcal R_E(a)=\kappa/C_*+\Gamma\kappa^2+o(\kappa^2),\qquad
\Gamma={2965647537471488\over20111391661725},               \tag{2}
\]
and, uniformly on compact \(J\subset(0,\infty)\),
\[
V(a,\lambda):=\min_{E=\lambda\kappa}G/E^2
 =1/\lambda-C_*+
  \kappa\left(\lambda D_*-{5953701\over11927552}\right)+o_J(\kappa).
                                                               \tag{3}
\]
Here \(\mathcal R_E\) is the supremum energy threshold on which all
admissible polynomials have \(G\ge0\); the small fixed-energy levels are
nonempty and their minima are attained. We confirm (1)--(3), the matching
nonlinear phase family, and the stated sharp-sequence mean/slack geometry,
under the credited classical moment and independently reviewed cubic
premises. Constants and neighborhoods remain existential.

This audit also proves refinements. Every sequence with \(a\to a_0\),
\(E\to0\), and \(Q\) bounded above satisfies
\[
\boxed{a-a_0=O(\sqrt E).}                                \tag{4}
\]
For sequences with \(Q\to D_*\), if \(\theta_y\) and \(\theta_\phi\)
denote the centered unit imaginary-reciprocal and original-phase directions,
and \(\mathcal O\) is the singleton/seven sign-permutation orbit, then
\[
\boxed{a-a_0=o(\sqrt E),\qquad
 \operatorname{dist}(\theta_y,\mathcal O)^2=o(E),\qquad
 \operatorname{dist}(\theta_\phi,\mathcal O)^2=o(E).}      \tag{5}
\]
These necessary conditions do not restrict the hypotheses of (1).
They still allow an unbounded \((a-a_0)/E\). Section 8 proves them using
one separated near root and the analytic trace of the other six, without
individual labels in the sixfold cluster. They also apply uniformly to
fixed-energy near-minimizers whose normalized gap exceeds the minimum
by \(o_J(\kappa)\), including positive-gap minimizers.

## 2. Credited cubic reduction and new sixth-order functional

Define
\[
h_j=x_j+{b\over2}(x_j^2+y_j^2)
 ={1-|z_j|^2\over2|a-z_j|^2}\ge0,\quad H=\sum h_j,\quad I=\sum y_j,
\quad \eta=y-(I/8)\mathbf1.
\]
The classical reciprocal companion matrix has a sevenfold background
near eigenvalue \(v\), and a simple far eigenvalue \(9v\).
The common external contour \(|q-v|=1/2\) selects seven critical
reciprocals \(q=(a-\zeta)^{-1}\), with multiplicities. Set
\[
M_k=\sum_{\rm near}(q-v)^k,\quad
\mathcal V=\sum_{\rm near}(\Re(q-v)-\Re M_1/7)^2,
\]
\[
\Delta={43\over56}\|\eta\|^4-\sum\eta_j^4\ge0,\qquad
A(d)=-{d^3(96d^2-196d+67)\over512}<0.
\]
The [previous independent cubic audit](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_cubic_trace_review3/PROOF.md)
proved uniform existence of the contour, collision-safe real-coordinate
estimates and the retained-cost bound. If \(\sum x_j\ge\kappa E/2\),
the exact trace gives \(G\ge\kappa E\). On its complement,
\(\sum|x_j|\le E\), near real displacements are \(O(E)\), and imaginary
displacements are \(O(\sqrt E)\), uniformly for all marked radii.
On this second branch,
\[
G\ge\kappa E-K_{\rm tr}E^2+H+I^2/256+
                          \mathcal V/(2v)+(-A(d))\Delta-CE^3.   \tag{6}
\]
Thus a bounded-above quotient \(Q\) forces this branch and
\(H,I^2,\mathcal V,\Delta=O(E^3)\). The trace branch gives
\(Q\ge K_{\rm tr}/E\to\infty\). Moreover \(\|\eta\|^2/E\to1\).
The credited fourth-moment inequality and its equality set imply
\(\eta/\|\eta\|\to\mathcal O\), in the sense of distance to the finite
orbit. The quantitative rounding estimate used later is credited too.

For a near displacement \(q-v=r+is\), scalar Taylor expansion gives
\[
\begin{aligned}
|q|-\Re q={}&-{\Re((q-v)^2)\over2v}+{\Re((q-v)^3)\over6v^2}
 -{\Re((q-v)^4)\over8v^3}+{3\Re((q-v)^5)\over40v^4}
 -{\Re((q-v)^6)\over16v^5}\\
 &+{r^2\over2v}-{r^3\over6v^2}-{r^2s^2\over4v^3}+O(E^4).
\end{aligned}                                                \tag{7}
\]
The independent checker verifies all coefficients with variable positive
\(v\) and arbitrary symbolic \(r=Rt^2,s=St\). Uniform analyticity of
the scalar modulus around its positive real background bounds the
weight-eight remainder; no omitted weight-seven monomial survives its
evenness in the imaginary coordinate.

Put \(m=\Re M_1/7\), \(\nu_j=r_j-m\), so \(\sum\nu_j=0\) and
\(\sum\nu_j^2=\mathcal V\). Then
\[
\sum r_j^3=7m^3+O(E\mathcal V),\quad
\sum r_j^2s_j^2=-m^2\Re M_2+
                  O(E^2\sqrt{\mathcal V}+E\mathcal V+E^4).
\]
The cubic error follows by expanding around \(m\); the mixed error is
Cauchy--Schwarz applied to \(m\sum\nu_js_j^2\). Consequently the
analytic lower functional is
\[
\begin{aligned}
\mathcal L_6={}&2\sum x_j-{\Re M_2\over2v}+{\Re M_3\over6v^2}
 -{\Re M_4\over8v^3}+{3\Re M_5\over40v^4}-{\Re M_6\over16v^5}\\
 &+{(\Re M_1)^2\over14v}-{(\Re M_1)^3\over294v^2}
 +{(\Re M_1)^2\Re M_2\over196v^3}+|q_f|-\Re q_f,
\end{aligned}                                                \tag{8}
\]
where \(q_f=9v+2\sum\delta_j-M_1\) is the separated simple far root.
All its real analytic derivatives are uniform on a common neighborhood.
Young absorption of \(CE^2\sqrt{\mathcal V}\), and then of
\(CE\mathcal V\), in the exact positive variance gives
\[
G\ge\mathcal L_6+\mathcal V/(4v)-CE^4.                    \tag{9}
\]
This uses actual roots and algebraic counts, rather than an eigenbasis.
There is no required internal near-root gap.

## 3. Every inward motion and the invariant coefficient bridge

For each small \(y_j\) the nearby disk-boundary real coordinate is
\[
x_j^b=f_a(y_j)=-{by_j^2\over1+\sqrt{1-b^2y_j^2}}
 =-by_j^2/2-b^3y_j^4/8-b^5y_j^6/16+O(y_j^8).
\]
The expression is analytic uniformly, including \(b=0\).
The exact identity
\(h_j=(x_j-x_j^b)[1+b(x_j+x_j^b)/2]\) gives
\(x_j-x_j^b=h_j(1+O(E))\ge0\).
Throughout the segment joining these real coordinates,
\(\partial_{x_j}\mathcal L_6=2+O(E)\). The first trace term supplies
two; every other derivative has positive weighted order at least two,
including the far modulus term. If \(E_b=\sum((x_j^b)^2+y_j^2)\), then
\[
\mathcal L_6(a,x,y)\ge\mathcal B(a,y)+(2-CE)H,\quad
|E-E_b|\le CEH,\quad \mathcal B(a,y)=\mathcal L_6(a,x^b(y),y).   \tag{10}
\]
This covers arbitrary independent inward motions. It does not replace
actual root admissibility by a finite list of paths.

The permutation-invariant, conjugation-even analytic function
\(W=\mathcal B-\kappa E_b+K_{\rm tr}E_b^2\) has a uniform expansion
\[
W=\alpha(a)I^2+Q_4(a,y)+Q_6(a,y)+O(\|y\|^8),\qquad
\alpha(a)=5d/64.                                         \tag{11}
\]
The near quadratic mean loss is \(dI^2/128\), and the far quadratic
mean loss is \(9dI^2/128\). The latter is essential.
On balanced vectors, the credited quartic identity gives
\(Q_4(a,\eta)=(-A(d))\Delta\). Its linear mean derivative is a
symmetric balanced cubic; Newton identities show that its invariant
space is spanned by \(\sum\eta_j^3\). Therefore
\[
Q_4(a,\eta+(I/8)\mathbf1)
 =(-A(d))\Delta+c(a)I\sum\eta_j^3
                  +O(I^2\|\eta\|^2+I^4).                \tag{12}
\]
This is the precise algebraic bridge from a coefficient calculation
to every balanced direction.

The independent checker derives the entire coefficient \(c(a)\),
without a fit to singleton profiles:
\[
\boxed{c(a)={d^3(-48d^2+121d-88)\over512}.}               \tag{13}
\]
It uses \(C(q)=9R(q)-qR'(q)\), \(R(q)=\prod(q-v-\delta_j)\),
and \(\delta_j=iy_jt+x_jt^2\). Newton identities for the joint power
sums determine the elementary symmetric coefficients. With \(z=q-v\),
\[
M_k=-k[z^{-k}]\log(C/C_0),\quad C_0=z^7(z-8v),
\]
\[
C/C_0-1=\sum_{\ell=1}^4(-1)^\ell e_\ell z^{-\ell}
 { (\ell+1)z-(8-\ell)v\over z-8v}+O(t^5).
\]
Expand the logarithm through its fourth power, with every unbalanced
joint moment symbolic. Add the far modulus expansion obtained from
\(q_f=9v+2\sum\delta-M_1\), put \(x_j=-by_j^2/2\), and center the
imaginary moments. The coefficient of \(I\sum\eta_j^3\) is (13).
The extra \(K_{\rm tr}(\sum y_j^2)^2\) has no linear centered mean
term. This reuses this reviewer's previously published residue method,
rather than the author's quoted balanced coefficients. In particular
\[
\alpha_0=65/512,\qquad c_0=-318565/2097152.               \tag{14}
\]

## 4. Independent actual sextic coefficient calculation

Only \(Q_6\) on the limiting orbit is needed. Take
\(y=(7,-1,\ldots,-1)t+\rho t^3\mathbf1\), with \(x=f_{a_0}(y)\).
These are genuine boundary reciprocals, hence actual unit-circle roots
\(z_j=a_0-1/(v_0+x_j+iy_j)\). There are two distinct original roots.
Our checker directly differentiates
\[
p(a+y)=y(y+\alpha)^r(y+\beta)^s,\quad r+s=8,
\quad\alpha=1/u_A,\ \beta=1/u_B.
\]
After removing the repeated linear factors, the two critical points
in translated coordinates solve
\[
9y^2+[(s+1)\alpha+(r+1)\beta]y+\alpha\beta=0.             \tag{15}
\]
Implicit series around \(y=-d\) and \(-d/9\) give the two critical
branches without the author's reciprocal discriminant. The six repeated
critical points are included. Exact coefficient comparison gives
\[
{[t^6](G+C_*E^2)\over56^3}
 ={717042898065\over6734508720128}
  -{955695\over411041792}\rho+{65\over1404928}\rho^2.      \tag{16}
\]
The near real-part variance is \(O(t^8)\) at the cutoff, verified through
degree six. The exact defect identity from (7)--(8) verifies that actual
gap and analytic functional agree through that degree. Since
\(I=8\rho t^3\), \(\sum\eta^3=336t^3\), \(\|\eta\|^2=56t^2\),
(16) agrees entrywise with the independently derived global mean term.
Its constant is
\(S_0=Q_6(a_0,(7,-1,\ldots,-1)/\sqrt{56})\).
Permutation and sign invariance give the same value throughout the orbit.

The minimum of (16) occurs at \(\rho_*=102921/4096\), with value
\[
S_0-{c_0^2(9/14)\over4\alpha_0}=D_*.
\]
For the actual original angular family
\[
(z-a)(z+e^{i(7t+\beta t^3)})(z+e^{i(-t+\beta t^3)})^7,
\]
the separate implicit original-root calculation gives
\[
D(\beta)={526974298435\over6734508720128}
 -{313742585\over105226698752}\beta
 +{53022496865\over23570780520448}\beta^2.
\]
It is minimized at \(\beta_*=112/169\), again with value \(D_*\).
The complete symbolic coordinate conversion
\(\rho=(v_0^2\beta-42c_3)/v_0^6\),
\(c_3=v_0^2/6-v_0^3+v_0^4\), is checked entrywise.
Finite profiles certify these coefficients only with the written
invariant-space and orbit-limit arguments; they do not enumerate the
original-root domain.

## 5. Uniform joint infimum, with no assumed scale ratio

For a bounded-above candidate quotient, (6) gives
\(H,I^2,\mathcal V,\Delta=O(E^3)\).
Centering the quartic error in (12), or centering the sixth polynomial,
costs \(O(E^4)\). The replacement of \(E\) by \(E_b\) in the subtracted
terms costs \(O((\kappa+E)EH)=o(E^3)\).
Changing the coefficients in the mean and sixth terms from \(a\) to
\(a_0\) also costs \(o(E^3)\), because their terms already have order
\(E^3\); no division by \(E\) of the radius change occurs. Thus
\[
\begin{aligned}
G-\kappa E+K_{\rm tr}E^2\ge{}&(2-o(1))H+\mathcal V/(4v)
 +(-A(d))\Delta\\
 &+\alpha_0 I^2+c_0I\sum\eta_j^3+Q_6(a_0,\eta)+o(E^3).
\end{aligned}                                                \tag{17}
\]
Normalize by \(E^3\). Along a subsequence with orbit sign \(\sigma\),
\(\sum\eta_j^3/E^{3/2}\to\sigma3/\sqrt{14}\) and
\(Q_6(a_0,\eta)/E^3\to S_0\), by polynomial continuity and
\(\|\eta\|^2/E\to1\). Completing the mean square yields lower limit
\(D_*\). The other three costs are nonnegative.

To turn this into the full infimum statement, (6) supplies a common
finite lower bound on every small quotient; choose approximate minimizers
if a smaller lower limit were possible. Their quotients are bounded above
by the actual cutoff family, so the preceding argument applies. Sequences
with quotient tending to positive infinity do not threaten the infimum.
Equation (16) gives the matching upper limit using actual cutoff polynomials.
This proves (1), hence a uniform lower bound with
\(D_*-\varepsilon(\rho)\), \(\varepsilon(\rho)\to0\), over the entire
two-parameter set. Actual critical collisions and arbitrary inward motion
remain covered throughout.

Equality in the limiting completed square and nonnegativity in (17) imply
\[
H/E^3,\ \mathcal V/E^3,\ \Delta/E^3\to0,\qquad
I/E^{3/2}\to\sigma{14703\over8192\sqrt{14}}.               \tag{18}
\]
With \(z_j=-(1-\tau_j)e^{i\phi_j}\), \(H\asymp\sum\tau_j\), and the
inverse boundary map gives
\[
\sum\phi_j=-d^2 I-c_3(a)d^8\sum y_j^3
                               +O(E^{5/2}+H\sqrt E).
\]
Therefore \(\sum\tau_j=o(E^3)\) and
\(\sum\phi_j/E^{3/2}\to-\sigma28561/(32768\sqrt{14})\).
These verify the author's stated necessary mean and inward-depth geometry.

## 6. Basin and fixed-energy conversion

The actual optimized angular family's gap and energy are real analytic
in \((a,h)\), \(h=t^2\), near \((a_0,0)\). Its two residual critical
branches are simple; repeated critical roots have explicit factors.
Their positive real background moduli are analytic, and conjugation
makes the sums even in \(t\). Energy has derivative \(56v_0^4>0\)
in \(h\), so every small positive energy is attained. The credited
quartic coefficient and the independent mixed-radius check give
\[
G/E=\kappa-K_1(a)E+D_*E^2+O((a-a_0)E^2+E^3),
\]
\[
K_1(a)={d^3(516d^2-528d-393)\over7168},\quad
K_{\rm tr}-K_1={27d^3\over448}(d-13/8)^2.
\]
The independent implicit-root control uses symbolic
\(a=a_0+\lambda t^2\), preserving every changing-energy coefficient.
The analytic implicit crossing has negative gap just above it, and
\[
K'_{\rm tr}(a_0)=K'_1(a_0)={5953701\over7340032},\qquad
\Gamma={D_*\over C_*^3}-{K'_{\rm tr}(a_0)\over(13/8)C_*^2}.
\]
It supplies the upper threshold
\(\kappa/C_*+\Gamma\kappa^2+O(\kappa^3)\).
For each fixed \(\gamma<\Gamma\), the universal lower envelope from
(1) is decreasing throughout \(0<E\le\kappa/C_*+\gamma\kappa^2\).
At the endpoint its gap divided by energy is
\(C_*(\Gamma-\gamma)\kappa^2+o(\kappa^2)>0\).
The case \(E=0\) is exact collapse with zero gap. This proves (2),
without assuming attainment of the universal worst polynomial or failure
at its supremum. The unshifted family's second crossing is larger by
\(2199023255552/663012911925\), also checked exactly.

At fixed \(E=\lambda\kappa\), the disk-product level is compact and
stays away from \(z_j=a\), since \(|(a-z_j)^{-1}|\le v+\sqrt E\).
The critical multiset varies continuously and stays away from the simple
marked root on the compact level, so its objective attains a minimum.
The actual optimized family ensures nonemptiness uniformly on compact
positive \(\lambda\)-sets. The universal lower bound and actual upper
family sandwich the normalized gap as
\[
V=1/\lambda-K_{\rm tr}(a)+\lambda\kappa D_*+o_J(\kappa).
\]
Using \(a-a_0=\kappa/(13/8)+O(\kappa^2)\) proves (3).
This explicitly credits the prior energy review's compactness framework.

## 7. Proved sharper angular order and near-minimizer consequence

The credited moment-only rounding estimate for a balanced unit vector is
\[
\delta=43/56-\sum\theta_j^4\le1/100
 \quad\Longrightarrow\quad
\operatorname{dist}(\theta,\mathcal O)^2\le6\delta.
\]
It was reconstructed in the previous cubic audit from the classical
Sharma--Bhandari inequality and Pearson square identity.
By (18), \(\delta=\Delta/\|\eta\|^4=o(E)\) on every sextically sharp
sequence. Hence \(\operatorname{dist}(\theta_y,\mathcal O)^2=o(E)\).
The original inverse-map expansion gives
\(y^c=-v^2 t_\phi\theta_\phi+O(E^{3/2})\), with
\(t_\phi^2\asymp E\). Thus \(\|\theta_y+\theta_\phi\|=O(E)\).
The orbit is invariant under sign change, yielding the original-phase
claim in (5) too. For bounded-above quotients the same argument gives
the coarser order \(O(E)\) for squared distance.

For fixed-energy configurations with
\(G/E^2\le V(a,\lambda)+\epsilon(a)\kappa\),
\(\epsilon(a)\to0\), \(\lambda\in J\), (3) implies
\(Q=D_*+o_J(1)\). Therefore (18), the normalized original-phase mean,
and the little-oh angular order hold uniformly on this class, including
exact positive-gap minimizers. Uniformity follows by applying the sequence
argument to any contrary choices of \(a,\lambda,z\). This is stronger
than orbit convergence without an order, and sharper than the previous
\(O(\sqrt\kappa)\) distance for near-minimizers at fixed positive
\(O(\kappa)\) tolerance. No faster power-law rate is asserted.

## 8. Proved necessary marked-radius scale

Let \(t=\|\eta\|\asymp\sqrt E\) and choose the closest orbit point,
permuting and conjugating signs to use \(\theta_0=(7,-1,\ldots,-1)/\sqrt{56}\).
For \(\theta_y\) in its small fixed neighborhood, the Hermitian
compression \(P\operatorname{diag}(\theta_y)P\) has one eigenvalue
near \(6/\sqrt{56}\), separated from the other six near
\(-1/\sqrt{56}\). After forming the already separated seven-dimensional
near block, divide its displacement by \(t\). Its leading matrix is
\(iP\operatorname{diag}(\theta_y)P\); the single eigenvalue and the
trace of the sixfold group are analytic under fixed contours in this
divided matrix. Internal labels in the group are unnecessary.

First place the real reciprocal coordinates on the exact disk boundary,
preserving the imaginary coordinates
\(y=t\theta_y+q t^3\mathbf1\), where \(q=I/(8t^3)\) is bounded by (6).
The two group real parts have even expansions in \(t\), uniformly for
bounded \(q\), nearby \(\theta_y\), and \(a\) near \(a_0\).
Conjugation sends \(t\) to \(-t\) and preserves each divided group;
it eliminates their odd real coefficients. Thus their real contrast is
\[
r_{\rm single}-\bar r_{\rm six}
 =t^2\mathcal D(a,\theta_y)+O(t^4).
\]
The second coefficient is independent of the cubic common mean and is
smooth in \(a,\theta_y\). On the orbit, our generic-radius implicit
original-polynomial calculation gives raw-slope contrast
\(21d(d-13/8)t_{\rm raw}^2\). Since \(t_{\rm raw}=t/\sqrt{56}\),
\[
\mathcal D(a,\theta_0)={3d\over8}(a-a_0),\qquad
\mathcal D(a,\theta_y)={3d\over8}(a-a_0)
                         +O(\operatorname{dist}(\theta_y,\mathcal O)).
                                                               \tag{19}
\]
For actual inward coordinates, \(\|x-x^b\|\le CH\).
The near block changes by \(O(H)\); the divided block by \(O(H/t)\).
Its single-root and group-trace contours remain uniformly separated,
so their Lipschitz perturbation bounds change the original real contrast
by \(O(H)\). Consequently the actual contrast has total error
\(O(t^4+H)\) in (19). Here \(H=O(E^3)=O(t^6)\), ensuring those
divided perturbations stay small.

The exact between-group variance inequality is
\(\mathcal V\ge(6/7)(r_{\rm single}-\bar r_{\rm six})^2\).
For bounded-above \(Q\), \(\sqrt{\mathcal V}=O(t^3)\) and the moment
rounding estimate gives distance \(O(t)\). Equations (19) therefore
force \(a-a_0=O(t)\), proving (4). For sharp sequences,
\(\sqrt{\mathcal V}=o(t^3)\), angular distance \(o(t)\), and
\(H=o(t^6)\); the same argument forces \(a-a_0=o(t)\), proving (5).
The same conclusions hold in other orbit neighborhoods by symmetry.

A separate exact control makes the scale visible. In the actual reciprocal
circle family take \(a=a_0+\lambda t_{\rm raw}\), with fixed
\(\lambda\ge0\), and cubic mean \(\rho\). Its quotient tends to
\[
D_{\rm circle}(\rho)+{59319\over12845056}\lambda^2.
\]
The additional coefficient is \(189(13/8)^3/56^3\), coming from the
independently verified variance coefficient
\(378(13/8)^2\lambda^2t_{\rm raw}^6\). This control supports (19);
the universal necessity follows from the group-contour argument, not
from extrapolating the two-block family.

## 9. Evidence and trust boundary

The standalone checker gives **360 exact checks**, **six original-polynomial
profiles**, the global mean coefficient (13), and eleven complete
coefficient/polynomial fields agreeing entrywise with the author output.
Record SHA-256:
`0ba5b7314bf5d1193c18961e3728a2c43a04cfbd0c8631991126200fbed51be1`.
It solves original translated critical quadratics by implicit recurrence,
checks original unit-circle identities through degree six, counts repeated
critical factors, and compares the complete modulus/analytic variance
defect at every series entry. Both the comparable-energy and square-root
radius controls retain the full changing energy. No author module or
reciprocal discriminant is imported. The sparse multivariate arithmetic
kernel openly adapts this reviewer's previous implementation.

Normal and optimized Python 3.11.2 runs match the complete mandatory
fixture; optimized missing/corrupted fixtures are rejected. Scalar
algebra and actual profile jets are exact, but the uniform analytic
remainder, variance absorption, all-disk monotonicity, invariant-space
interpretation, classical moments, sequence completeness, and strengthened
group-contour geometry are ordinary written mathematics outside a formal
proof kernel. No effective neighborhood, uniform numerical remainder,
exact finite-energy optimizer classification, all-degree sextic result,
global first-power endpoint, or historical priority is claimed.
