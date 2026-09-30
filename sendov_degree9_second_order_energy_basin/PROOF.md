# The second-order universal degree-nine energy basin

Author **six-sendov-3**, role **researcher**, 2026-09-30.
Ordinary written author proof with exact symbolic algebra controls;
independent review pending, not proof-assistant formalized.
Prior sharp quartic, moment inequality, matrix and cubic trace results
are credited in LITERATURE.md. No historical-priority claim.

## 1. Quantified results

Let \(p(z)=c(z-a)\prod_{j=1}^8(z-z_j)\), \(c\ne0\), with a simple
marked root \(a\in[5/8,1]\), and \(|z_j|\le1\). Coefficients may be
complex. Repeated other roots and critical points are allowed; count
derivative zeros with algebraic multiplicity. Put
\[
 a_0=5/8,\quad d=1+a,\quad v=1/d,\quad \kappa=d(a-a_0),
\]
\[
 \delta_j=(a-z_j)^{-1}-v=x_j+iy_j,\quad E=\sum|\delta_j|^2,
 \quad G=\sum_{p'(\zeta)=0}|a-\zeta|^{-1}-16v,
\]
\[
 C_*={560235\over8388608},\qquad
 K_{\rm tr}(a)={d^3(3792d^2-7728d+2991)\over28672},
\]
\[
 \boxed{D_*={520320727875\over6734508720128}},\qquad
 \boxed{\Gamma={2965647537471488\over20111391661725}}.       \tag{1}
\]
The marked root's simplicity makes all reciprocals finite. Rotating the
polynomial gives the same result for a marked root of modulus \(a\),
with energy and phases computed in the rotated coordinates.

**Theorem 1 (sharp joint sextic envelope).** Over this entire polynomial
class,
\[
 \boxed{\lim_{\rho\downarrow0}\inf_{\substack{
     a_0\le a\le a_0+\rho\\0<E\le\rho}}
       {G-\kappa E+K_{\rm tr}(a)E^2\over E^3}=D_*.}         \tag{2}
\]
Take \(\rho<3/8\); the infimum includes all disk-root motions, not a
specified family or bounded number of distinct roots. Equivalently there
is an error \(\varepsilon(\rho)\to0\) such that throughout that set,
\[
 G\ge\kappa E-K_{\rm tr}(a)E^2+
                            (D_*-\varepsilon(\rho))E^3.   \tag{3}
\]
At \(a=a_0\) this supplies the sharp cubic correction to the credited
sharp quartic. It does not claim that \(K_{\rm tr}(a)\) is sharp away
from the cutoff. No numerical neighborhood or rate for
\(\varepsilon(\rho)\) is supplied.

Let \(\mathcal R_E(a)\) be the supremum of all \(r\ge0\) for which
every such polynomial with \(E\le r\) has \(G\ge0\).

**Theorem 2 (second-order universal basin).** As \(a\downarrow a_0\),
\[
 \boxed{\mathcal R_E(a)={\kappa\over C_*}
                                  +\Gamma\kappa^2+o(\kappa^2).} \tag{4}
\]
The previously established leading limit and \(O(\kappa^2)\) error
are prior work. The additions are the exact second coefficient, sharp
joint sextic envelope, and nonlinear mean optimization. These concern
squared reciprocal energy, not an optimal maximum-root displacement
basin or the unrestricted first-power endpoint.

## 2. Credited cubic input and the sharpness reduction

Write \(b=1-a^2\), \(A_0=\sum x_j\), \(I_0=\sum y_j\), and
\[
 h_j=x_j+{b\over2}(x_j^2+y_j^2)
       ={1-|z_j|^2\over2|a-z_j|^2}\ge0,\quad H_0=\sum h_j.
\]
Use the prior cubic trace proof, including its retained fourth-moment
deficit and the bounded-real-part reduction. If
\(A_0\ge\kappa E/2\), trace gives \(G\ge\kappa E\).
Otherwise \(\sum|x_j|\le E\); uniformly all near critical reciprocals
have real displacement \(O(E)\) and imaginary displacement \(O(\sqrt E)\).
Let \(M_k=\sum_{\rm near}(q-v)^k\), where seven roots are selected by
the fixed contour \(|q-v|=1/2\), and let
\[
 \mathcal V=\sum_{\rm near}
       \left(\Re(q-v)-{\Re M_1\over7}\right)^2.
\]
For \(\eta_j=y_j-I_0/8\), put
\[
 \Delta_4={43\over56}\left(\sum\eta_j^2\right)^2-\sum\eta_j^4\ge0,
 \qquad A(d)=-{d^3(96d^2-196d+67)\over512}<0.
\]
The credited stronger branch bound gives, with one uniform constant,
\[
 G\ge\kappa E-K_{\rm tr}(a)E^2+H_0+I_0^2/256+
                  \mathcal V/(2v)+(-A(d))\Delta_4-CE^3.   \tag{5}
\]
Its analytic and all-disk proof is a cited author result awaiting
independent review; the prior independent angular audit gives no verdict
on this extension.

Consider any sequence \(a\to a_0\), \(E\to0\) for which the quotient
in (2) is bounded above by a fixed finite constant. It eventually lies
on the second branch: the trace branch would give a quotient at least
\(K_{\rm tr}(a)/E\to+\infty\). Equation (5) then forces
\[
             H_0,I_0^2,\mathcal V,\Delta_4=O(E^3).        \tag{6}
\]
In particular, for \(\mu_2=\sum\eta_j^2\),
\(\mu_2/E\to1\). The balanced normalized direction
\(\theta=\eta/\sqrt{\mu_2}\) approaches the finite orbit
\[
 \mathcal O=\{\pm\text{ permutations of }(7,-1,\ldots,-1)/\sqrt{56}\}.
                                                               \tag{7}
\]
Indeed \(\Delta_4/\mu_2^2=O(E)\to0\); compactness and the existing
scalar fourth-moment inequality with its singleton/seven equality set
give (7). No unproved rate of approach or root-label continuity is needed.

## 3. Absorbing sixth-order real-part terms against variance

For a near reciprocal write \(q=v+r+is\), with \(r=O(E)\),
\(s=O(\sqrt E)\). Direct real scalar Taylor expansion gives
\[
\begin{aligned}
 |q|-\Re q={}&-{\Re((q-v)^2)\over2v}
     +{\Re((q-v)^3)\over6v^2}-{\Re((q-v)^4)\over8v^3}
     +{3\Re((q-v)^5)\over40v^4}-{\Re((q-v)^6)\over16v^5}\\
 &+{r^2\over2v}-{r^3\over6v^2}-{r^2s^2\over4v^3}+O(E^4).
\end{aligned}                                                   \tag{8}
\]
Equivalently, the weighted terms in the scalar expansion are
\(s^2/(2v)-rs^2/(2v^2)-s^4/(8v^3)+r^2s^2/(2v^3)
+3rs^4/(8v^4)+s^6/(16v^5)\). Uniform analyticity and \(v\ge1/2\)
bound every omitted term of weight at least eight.

Put \(m=\Re M_1/7\), \(\nu_j=r_j-m\). Then
\(\sum\nu_j=0\), \(\sum\nu_j^2=\mathcal V\), and
\[
 \sum r_j^2=7m^2+\mathcal V,\quad
 \sum r_j^3=7m^3+O(E\mathcal V),
\]
\[
 \sum r_j^2s_j^2
       =m^2\sum s_j^2+O(E^2\sqrt{\mathcal V}+E\mathcal V).
\]
Also \(\sum s_j^2=-\Re M_2+\sum r_j^2\), so replacing the first
term of the last display by \(-m^2\Re M_2\) has error \(O(E^4)\).
These estimates need only \(|r_j|\le CE\), \(|s_j|\le C\sqrt E\).
For example \(\sum|\nu_j|^3\le CE\mathcal V\), and Cauchy–Schwarz
bounds \(|m\sum\nu_js_j^2|\le CE^2\sqrt{\mathcal V}\).

Define the **analytic** lower functional
\[
\begin{aligned}
 \mathcal L_6={}&2A_0-{\Re M_2\over2v}+{\Re M_3\over6v^2}
    -{\Re M_4\over8v^3}+{3\Re M_5\over40v^4}-{\Re M_6\over16v^5}\\
 &+{(\Re M_1)^2\over14v}-{(\Re M_1)^3\over294v^2}
      +{(\Re M_1)^2\Re M_2\over196v^3}+\ell_f,
 \qquad\ell_f=|q_f|-\Re q_f.
\end{aligned}                                                    \tag{9}
\]
The far root is simple, with real part uniformly positive. It can be
written \(q_f=9v+2\sum\delta_j-M_1\), hence is analytic without
additional near-root labels. Its scalar modulus is real analytic.
The fixed external gap establishes joint analyticity of all \(M_k\).

Summing (8), the error in (9) is bounded in magnitude by
\(CE\mathcal V+CE^2\sqrt{\mathcal V}+CE^4\), apart from the exact
positive term \(\mathcal V/(2v)\). Young's inequality absorbs
\(CE^2\sqrt{\mathcal V}\) against \(\mathcal V/(8v)\), at cost
\(CE^4\). Shrinking the uniform neighborhood absorbs \(CE\mathcal V\)
against another \(\mathcal V/(8v)\). Thus on the second branch,
\[
             G\ge\mathcal L_6+\mathcal V/(4v)-CE^4.       \tag{10}
\]
This is a uniform analytic comparison for every root configuration,
including critical collisions and defective companion matrices.

## 4. Disk boundary comparison and symmetric Taylor coefficients

The near boundary solution of \(x+b(x^2+y^2)/2=0\) is
\[
 f_a(y)=-{by^2\over1+\sqrt{1-b^2y^2}}
       =-{b\over2}y^2-{b^3\over8}y^4-{b^5\over16}y^6+O(y^8).
                                                               \tag{11}
\]
This formula is analytic uniformly, including \(b=0\). Let
\(x_j^b=f_a(y_j)\), \(E_b=\sum((x_j^b)^2+y_j^2)\).
The exact slack factorization is
\[
 h_j=(x_j-x_j^b)[1+b(x_j+x_j^b)/2].
\]
Hence \(x_j\ge x_j^b\) and
\(x_j-x_j^b=h_j(1+O(E))\) in the second branch. The segment between
these vectors still has real parts \(O(E)\).
From (9), or its conjugation-even weighted Taylor series,
\(\partial\mathcal L_6/\partial x_j=2+O(E)\) there. All other terms
have real-part derivative of weight at least two, including \(\ell_f\).
Consequently, for \(\mathcal B(a,y)=\mathcal L_6(a,x^b(y),y)\),
\[
 \mathcal L_6(a,x,y)\ge\mathcal B(a,y)+(2-CE)H_0,
                   \quad |E-E_b|\le CEH_0.               \tag{12}
\]
This is where arbitrary inward motions are covered.

The function
\[
 W(a,y)=\mathcal B(a,y)-\kappa E_b+K_{\rm tr}(a)E_b^2
\]
is analytic, permutation invariant, and unchanged under \(y\mapsto-y\).
Its Taylor expansion through degree six is
\[
        W=\alpha(a) I_0^2+Q_4(a,y)+Q_6(a,y)+O(\|y\|^8),
                  \qquad\alpha(a)={5\over64v}.            \tag{13}
\]
For the quadratic mean term, the near loss contributes \(I_0^2/(128v)\)
and the far first imaginary coefficient is \((9/8)I_0\), contributing
\(9I_0^2/(128v)\). Their sum explains \(\alpha\).
The far term has no balanced quartic contribution: its imaginary part
starts at degree three when \(I_0=0\).

The credited balanced quartic gives
\(Q_4(a,\eta)=(-A(d))\Delta_4\). Centering a symmetric quartic yields
\[
 Q_4(a,\eta+(I_0/8)\mathbf1)
    =(-A(d))\Delta_4+c(a)I_0\sum\eta_j^3
       +O(I_0^2\|\eta\|^2+I_0^4).                        \tag{14}
\]
The coefficient of \(I_0\) is a symmetric balanced cubic; its complete
invariant space is spanned by \(\sum\eta_j^3\). This proves the form
of (14) for every balanced direction, not merely sampled profiles.

At the cutoff the exact coefficients needed are
\[
 \alpha_0={65\over512},\quad c_0=-{318565\over2097152},\quad
 S_0:=Q_6(a_0,\theta_0)={717042898065\over6734508720128},
 \qquad\theta_0=(7,-1,\ldots,-1)/\sqrt{56}.               \tag{15}
\]
Here is a complete coefficient calculation using an actual reciprocal
boundary family, not an unquantified numerical fit. Set
\(y=(7,-1,\ldots,-1)t+\rho t^3\mathbf1\), use (11), and recover
\(z_j=a_0-(v_0+x_j^b+iy_j)^{-1}\). These are genuine unit-circle
roots for small real \(t\). For the two distinct reciprocals \(u_A,u_B\),
six critical reciprocals equal \(u_B\), and the other two solve
\[
                  q^2-(2u_A+8u_B)q+9u_Au_B=0.            \tag{16}
\]
The square root with constant term \(8v_0\) determines near and far
branches. Direct rational series expansion through degree six gives
\[
 { [t^6](G+C_*E^2)\over56^3}
       =S_0-{955695\over411041792}\rho
                              +{65\over1404928}\rho^2.   \tag{17}
\]
On this profile \(\mathcal V=O(t^8)\), and (8)–(9) show that
\(G=\mathcal L_6+O(t^8)\). Its centered second and third moments are
\(56t^2\) and \(336t^3\); its imaginary mean is \(8\rho t^3\).
Thus the linear coefficient in (17) is \((3/196)c_0\), and the quadratic
coefficient is \(64\alpha_0/56^3\), proving (15).
The invariant-space argument justifies the unique global quartic mean
coefficient. The sixth coefficient is required only on the limiting
singleton/seven orbit; permutation and sign invariance give the same
\(S_0\) on that whole orbit. No full sextic invariant classification
or finite-root enumeration is inferred from (17).

The standalone checker obtains (16) both from reciprocals and by direct
differentiation of the original polynomial, checks both critical branches,
the unit-circle jets, (8), and the exact variance correction. It also uses
a formal first-order common mean to check \(c_0\) by the independent
linear-in-mean quartic coefficient. Every identity is in exact polynomial
arithmetic, with the mean parameter symbolic.

## 5. Universal sharp sextic minimum

On sequences considered in section 2, (6) gives
\(I_0=O(E^{3/2})\), \(\|\eta\|=O(\sqrt E)\).
The centering remainder in (14) is \(O(E^4)\); centering \(Q_6\)
changes it by \(O(|I_0|E^{5/2})=O(E^4)\).
Equations (10)–(14), \(a\to a_0\), and \(|E-E_b|\le CEH_0\) give
\[
\begin{aligned}
 G-\kappa E+K_{\rm tr}(a)E^2\ge{}&
  (2-o(1))H_0+\mathcal V/(4v)+(-A(d))\Delta_4\\
 &+\alpha_0 I_0^2+c_0 I_0\sum\eta_j^3
                         +Q_6(a_0,\eta)+o(E^3).          \tag{18}
\end{aligned}
\]
The energy replacement error is at most
\(C(\kappa+E)EH_0=o(E^3)\). No assumption on the ratio
\((a-a_0)/E\) is needed.

Put \(q=I_0/E^{3/2}\), which is bounded. From (7),
\[
 {\sum\eta_j^3\over E^{3/2}}\to\sigma{3\over\sqrt{14}},
 \qquad {Q_6(a_0,\eta)\over E^3}\to S_0,
\]
after subsequence selection, where \(\sigma=\pm1\) denotes the orbit
sign. Continuity of a polynomial supplies these limits. Completing the
remaining mean square in (18) yields the lower limit
\[
 S_0-{c_0^2(9/14)\over4\alpha_0}=D_* .                  \tag{19}
\]
The nonnegative inward, variance and moment costs cannot reduce it.
Every bounded-above candidate quotient therefore has lower limit at least
\(D_*\); unbounded-above candidates cannot lower the infimum. More formally,
the prior uniform cubic bound supplies a common finite lower bound on the
quotient; take an approximate minimizing sequence and apply this argument.

Equation (17) is minimized by \(\rho_*=102921/4096\), realizes (19),
and supplies the opposite infimum bound with actual disk polynomials.
This proves (2), including full original-root coverage.

## 6. Actual phase optimization and the second basin coefficient

A simpler original-coordinate extremal family is
\[
 p_{a,t}(z)=(z-a)
     (z+e^{i(7t+\beta_*t^3)})(z+e^{i(-t+\beta_*t^3)})^7,
                    \qquad\boxed{\beta_*=112/169}.        \tag{20}
\]
At \(a_0\), its exact normalized sextic polynomial in a general
common phase coefficient \(\beta\) is
\[
 D(\beta)={526974298435\over6734508720128}
       -{313742585\over105226698752}\beta
       +{53022496865\over23570780520448}\beta^2.           \tag{21}
\]
Its unique minimum is \(D_*\) at \(\beta_*\). This is a genuine
nonlinear mean correction to the preceding balanced singleton/seven path.
The coordinate agreement with (17) is exact: with
\(c_3=v_0^2/6-v_0^3+v_0^4\),
\[
 \rho={v_0^2\beta-42c_3\over v_0^6},\qquad
 D(\beta)=D_{\rm circle}(\rho).
\]
Here \((7,-1)^3=43(7,-1)+42\mathbf1\), so the centered cubic
direction only reparametrizes the same singleton/seven direction.

In (20), \(F,E\) are real analytic in \((a,h)\), \(h=t^2\),
near \((a_0,0)\). The six repeated critical reciprocals and the two
simple residual branches in (16) have positive real constants, so their
scalar moduli are analytic. Conjugating \(t\mapsto-t\) gives evenness.
Moreover \(E=56v^4h+O(h^2)\), so it is an analytic local coordinate.
The credited singleton coefficient \(K_1\) satisfies
\(K_{\rm tr}-K_1=27d^3(d-13/8)^2/448\). The new family has
\[
 {G\over E}=\kappa-K_1(a)E+D_*E^2+
                       O((a-a_0)E^2+E^3).               \tag{22}
\]
The coefficient of \(E^2\) is continuous in \(a\) and equals \(D_*\)
at the cutoff. The checker independently verifies the mixed identity
with symbolic \(a=a_0+\lambda t^2\), including the full changing energy.

The implicit function theorem gives an actual analytic crossing
\(E^*(a)>0\) for \(a>a_0\) small, since the derivative of \(G/E\)
with respect to \(E\) at the cutoff is \(-C_*\). Its gap is negative
just above that crossing, hence \(\mathcal R_E(a)\le E^*(a)\).
Exact differentiation gives
\[
 K'_{\rm tr}(a_0)=K'_1(a_0)={5953701\over7340032},
 \quad a-a_0=\kappa/d_0+O(\kappa^2),\quad d_0=13/8.
\]
Expanding (22) therefore gives
\[
 E^*(a)={\kappa\over C_*}+\left(
       {D_*\over C_*^3}-{K'_{\rm tr}(a_0)\over d_0C_*^2}\right)
                                   \kappa^2+O(\kappa^3),
\]
and the coefficient in parentheses is exactly \(\Gamma\) in (1).

For the universal lower bound fix any \(\gamma<\Gamma\) and set
\(r_\gamma=\kappa/C_*+\gamma\kappa^2\). Apply (3) with
\(\rho=\max\{a-a_0,r_\gamma\}\to0\). For every \(0<E\le r_\gamma\),
\[
 {G\over E}\ge\kappa-K_{\rm tr}(a)E+
                                      (D_*-\varepsilon(\rho))E^2.
\]
The right side decreases throughout this small energy interval. Its
value at \(r_\gamma\) is
\(C_*(\Gamma-\gamma)\kappa^2+o(\kappa^2)>0\).
The case \(E=0\) is the exact collapsed polynomial with zero gap.
Thus \(\mathcal R_E(a)\ge r_\gamma\) eventually. Combining every
\(\gamma<\Gamma\) with the actual upper crossing proves (4), without
assuming a worst polynomial exists or treating its supremum endpoint
as a failure.

The unshifted \(\beta=0\) family's second crossing coefficient exceeds
\(\Gamma\) by the exact positive amount
\(2199023255552/663012911925\). The preceding upper crossing is therefore
improved at second order, while its leading constant remains credited.

## 7. First correction to the fixed-energy minimum

The prior independent review by **six-reviewer-3**, graph height 7649,
proved attainment and the leading fixed-level variational limit. The
following refines that result; it is not covered by that earlier verdict.
For \(\lambda>0\), define
\[
 V(a,\lambda)=\min_{E=\lambda\kappa}{G\over E^2},
                         \qquad a>a_0.
\]
For every compact interval \(J\subset(0,\infty)\), the energy levels
are nonempty and the minima are attained for all sufficiently small
\(a-a_0>0\), uniformly for \(\lambda\in J\). The new first correction is
\[
 \boxed{\sup_{\lambda\in J}\left|
 {V(a,\lambda)-(1/\lambda-C_*)\over\kappa}
       -\left(\lambda D_*-{5953701\over11927552}\right)
                         \right|\longrightarrow0.}       \tag{23}
\]
This includes positive-gap minimizers below the basin threshold.

For completeness, attainment needs no new compactness assertion. At a
fixed energy \(e>0\), every reciprocal satisfies
\(|(a-z_j)^{-1}|\le v+\sqrt e\), so the energy level is a closed
subset of the compact disk product, separated from \(z_j=a\). The
critical multiset is continuous in the polynomial coefficients, even at
collisions, and no critical point equals the simple marked root. Thus
the objective is continuous and attains its minimum. The analytic inverse
of the energy in (20) realizes every small positive \(e\), giving
nonemptiness uniformly on \(J\). These are the credited review's arguments.

On \(E=\lambda\kappa\), (3) gives the uniform lower bound
\[
 V(a,\lambda)\ge1/\lambda-K_{\rm tr}(a)
                    +\lambda\kappa(D_*-\varepsilon(\rho)),
 \qquad\rho=\max\{a-a_0,(\max J)\kappa\}\longrightarrow0.
\]
Realize the same level in (20). Equation (22) gives the uniform upper bound
\[
 V(a,\lambda)\le1/\lambda-K_1(a)+\lambda\kappa D_*+O(\kappa^2).
\]
The exact identity \(K_{\rm tr}-K_1=O((a-a_0)^2)=O(\kappa^2)\)
therefore sandwiches the minimum as
\[
 V(a,\lambda)=1/\lambda-K_{\rm tr}(a)
                                +\lambda\kappa D_*+o(\kappa),
\]
uniformly on \(J\). Using
\(K'_{\rm tr}(a_0)/d_0=5953701/11927552\) proves (23).
The earlier leading variational result is credited; only this correction
is asserted as an addition.

## 8. Rigidity of sextically sharp sequences

Suppose \(a\to a_0\), \(E\to0\) and the quotient in (2) tends to
\(D_*\). Equation (18) and its completed square imply
\[
 H_0/E^3\to0,\quad\mathcal V/E^3\to0,\quad\Delta_4/E^3\to0,
\]
and, along every subsequence with a fixed limiting orbit sign
\(\sigma\) as in (7),
\[
        {I_0\over E^{3/2}}\to
                    \sigma{14703\over8192\sqrt{14}}.    \tag{24}
\]
This is a forced nonlinear reciprocal mean, not a zero-mean restriction.
For original roots \(z_j=-(1-\tau_j)e^{i\phi_j}\) near collapse,
\(H_0\asymp\sum\tau_j\), so \(\sum\tau_j=o(E^3)\).
The inverse boundary map gives, uniformly,
\[
 \sum\phi_j=-d^2I_0-c_3(a)d^8\sum y_j^3
                                      +O(E^{5/2}+H_0\sqrt E),
 \quad c_3(a)=v^2/6-v^3+v^4.
\]
Consequently
\[
       {\sum\phi_j\over E^{3/2}}\to
                     -\sigma{28561\over32768\sqrt{14}}. \tag{25}
\]
These are necessary conditions for sextic sharpness; no rate of orbit
convergence, full exact-extremizer classification, or sign test for
arbitrary paths at a crossing is claimed.

## 9. Evidence and remaining boundaries

The exact checker works in \(\mathbb Q[X][i][t]/(t^7)\). It checks
the scalar sextic identity, the analytic/variance correction, five actual
two-block profiles, the original phase and reciprocal mean optima, the
mixed moving-radius identity, and the exact basin conversion. It recovers
unit-circle jets and differentiates the original polynomials directly.
It reproduces the useful preceding quartic baseline before new coefficients.
The kernel is openly adapted from this author's prior checker and imports
no campaign module. These are author algebra controls, not independent review.

The uniform analytic bounds, variance absorption, slack monotonicity,
invariant-space and classical moment equality arguments, minimizing-sequence
coverage and analytic crossing are ordinary written proofs outside a formal
kernel. Finite profiles establish the stated coefficient identities only
with the written invariant-space arguments; they do not enumerate all roots.
No floating samples, solver timeout, UNKNOWN or incomplete enumeration supply
a theorem. No numerical neighborhood/error rate, all-degree sharp sextic
formula, optimal maximum-root basin, global first-power endpoint or historical
priority is asserted.
