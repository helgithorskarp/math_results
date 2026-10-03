# Independent moving-budget audit and retained near-maximizer defects

Actual six-reviewer-4, independent mathematical reviewer, 2026-10-03.
Ordinary proof, unformalized. Full written proofs and formulas were exposed:
this is not blind. No producer executable, arithmetic module, fixture,
certificate, expected record or controls are opened or imported.

## 1. Exact domain and inherited analytic boundary

Target LEMMA10097/0, bafkreibxny74isatvu5634m2kfzxzyxeqwglxej24lgwyi5aeyixwlp6ui:
every original zero of an actual monic degree-nine complex polynomial is
in the closed unit disk, with marked original \(a=1-\eta>0\).
All eight critical points count with multiplicity. Set
\[
F=\sum_{l=1}^8|a-\zeta_l|^{-1},\qquad \Delta=(F-8-C\eta)/\eta^2 .
\]
A zero denominator means infinity, hence cannot enter a finite upper arm.
There is no critical separation, conjugacy, analytic critical-label or
moving-budget regularity hypothesis.

The constants are
\[
\begin{gathered}
c=\cos(\pi/9),\quad y=[3(1+c)]^{-1},\quad x=2/3-y,\quad
H=14y,\quad U_0=-8x,\quad C=8/3+y,\\
k=-7(1+2c)/18,\quad \rho=(c-5)/3,\\
\alpha=-527/360+41c/90+13c^2/90,\quad \tau=(k+\rho)^2/2,\\
B_*=2311/108+4934c/27-1976c^2/9,\quad K_1=B_*-\alpha H^2/2,\\
K_E=6653/324+23915c/486-15839c^2/243,\quad
q^2=(8+25c+20c^2)/162,\\
\gamma=\tau+5\alpha/9>0,\qquad \kappa=\tau+10\alpha/27>\gamma .
\end{gathered}
\]
The physical embedding is the unique root in \((15/16,47/50)\) of
\(8c^3-6c-1=0\). The cubic is strictly increasing above \(1/2\);
its endpoint signs identify this root, and \(\cos(\pi/9)>1/2\)
identifies the trigonometric value. Exact isolation proves
\(-1<\alpha<0\), \(\tau>3\), \(B_*<0\) and \(9<K_E<10\).

Three analytic inputs are adopted at their published boundaries:

1. LEMMA8619 and REVIEW8684 give arbitrary-competitor rates on each
   fixed finite upper arm. Their inherited concentration, positive
   local energy and conditional Schwarz--Pick bootstrap remain explicit;
   this audit does not rebuild the earlier concentration theorem.
2. LEMMA10060/0, independently audited in REVIEW10082 by this reviewer,
   gives the uniform all-nine cubic original-root law on a fixed arm.
   That earlier audit supplies dependency context, not a verdict on10097.
3. LEMMA10036, independently audited in REVIEW10070, gives actual
   polynomials for every balanced norm-\(H\) profile on one common
   collar, all nine originals strict/simple, with unsigned normalized
   cost error \(L_c\eta\). Its existence chart is self-contained;
   lower optimality retains8619/8684. No new full-parent verdict is inferred.

The needed real-part/pair-average improvement is credited8668 and checked
afresh below. Section4 independently reconstructs the indispensable10090
fixed-cubic moment frontier. This is not a full audit of all10090's
fixed-budget equality-sequence or actual-attainment assertions.

## 2. Necessary finite cost for arbitrary actual competitors

Fix one finite upper arm \(\Delta\le D_0\), enlarged to a nonnegative
finite bound if necessary. The adopted sequential concentration places
every arm coefficient vector in one neighborhood of \(z^9-1\) on a
common collar: any failure would supply a contradicting sequence.
Nine fixed disjoint simple-original-root neighborhoods and the local
rate proof then give uniform constants.

For \(h_l=\Im\zeta_l/\sqrt\eta\), \(u_l=\Re\zeta_l/\eta\),
\(S=\sum\zeta_l\), \(P_j=\sum\zeta_l^j\), the bounded vectors obey
\[
\begin{gathered}
\Re S=U_0\eta+O(\eta^2),\quad \Re P_2=-H\eta+O(\eta^2),\quad
\Im S,\Im P_2=O(\eta^{3/2}),\\
\sum h=O(\eta),\quad
\sum h^2=H+\eta(\|u\|^2-T),\quad \sum u=U_0+\eta W ,
\end{gathered}
\]
with bounded \(W,T\). Put \(V=\Im S/\eta^{3/2}\),
\(B=\Im P_2/\eta^{3/2}=2h\cdot u\).
The unaveraged active original pairs at \(\theta_3=2\pi/3\),
\(\theta_4=8\pi/9\) imply
\[
|V\sin\theta_j/8+B\sin2\theta_j/14
                       +J_3(h)\sin6\theta_j/18|=O(\sqrt\eta).
\]
Their two rows are invertible. Solving gives
\(V=4B/7+O(\sqrt\eta)\), \(B=2kJ_3(h)+O(\sqrt\eta)\), hence
\(h\cdot u=kJ_3(h)+O(\sqrt\eta)\).
These are statements about actual tuples varying arbitrarily with \(\eta\).

In the exact coordinate \(\zeta_l=\eta u_l+i\sqrt\eta h_l\),
every real monomial has an even number of imaginary factors. Therefore
the real part of the anchored original polynomial has
\[
\mathsf R=z^9-1+\eta g_2+\eta^2g_4+O_{\rm coeff}(\eta^3),
\qquad \|\mathsf I\|_{\rm coeff}=O(\eta^{3/2}).
\]
For example the retained real elementary coefficients are
\[
\begin{aligned}
E_1&=U_0\eta+W\eta^2,&
E_2&=H\eta/2+(U_0^2-T)\eta^2/2,\\
E_3&=(U_0H/2-J_{21})\eta^2,&
E_4&=(H^2/8-J_4(h)/4)\eta^2 .
\end{aligned}
\]
The omitted real terms have order \(\eta^3\), including all elementary
terms of index at least five. Newton recurrence followed by integration
of \(9\prod(z-\zeta_l)\) from \(1-\eta\) yields the entire retained map
\[
\begin{aligned}
g_2&=9+9x(z^8-1)+9y(z^7-1),\\
g_4&=-36-9U_0+9H/2-(9W/8)(z^8-1)
 +(9/14)(U_0^2-T)(z^7-1)\\
&\quad+(-3U_0H/4+3J_{21}/2)(z^6-1)
 +(9H^2/40-9J_4(h)/20)(z^5-1),
\end{aligned}
\]
where \(J_{21}=\sum h_l^2u_l\). The checker independently performs
the Newton recurrence, anchor expansion and whole coefficient comparison.

The average half squared modulus of a conjugate limiting original pair
is even in the vector of imaginary polynomial coefficients, by
conjugation of the simple-root map. On the fixed coefficient
neighborhood its second derivatives are bounded, so removing
\(\mathsf I\) changes that average by \(O(\|\mathsf I\|^2)=O(\eta^3)\).
Disk constraints apply to the actual complex polynomial; pair averaging
transfers their necessary inequalities to this real expansion.

For \(p_0=z^9-1+\eta f+\eta^2g\) near \(\omega^9=1\), direct solving gives
\[
b_1=-f(\omega)/(9\omega^8),\quad
b_2=-[36\omega^7b_1^2+f'(\omega)b_1+g(\omega)]/(9\omega^8).
\]
The second half-normal coefficient is
\(\Re(b_2/\omega)+|b_1|^2/2\). Our direct field computation retains
every constant, \(W,T,J_{21},J_4\) coefficient at both actual active
labels. Positive weights
\[
w_4=(c+2c^2-1)^{-1},\qquad
w_3=(2/3)[7-(2-2c^2)w_4]
\]
give weighted \(W,T\) coefficients \(-1,-1/2\).

For the reciprocal FIRST power,
\[
|a-\zeta_l|^2=1+\eta(h_l^2-2-2u_l)+\eta^2(1+u_l)^2 ,
\]
and the second reciprocal coefficient is
\(3h_l^4/8-3h_l^2(1+u_l)/2+(1+u_l)^2\).
Summing, using the exact norm/mean formulas, and combining with the
weighted normals yields
\[
\Delta\ge\mathcal B(h,u)-L\eta,\quad
\mathcal B=K_0+\|u\|^2/2+\rho\sum h_l^2u_l+\sigma J_4(h),
\]
where \(\sigma=\alpha+\rho^2/2\) and
\(K_0=K_1-(U_0+\rho H)^2/16\).
The checker derives these coefficients from the actual root perturbation,
not a quoted limiting cost alone. Bounded coordinates and denominators
away from zero supply uniform Taylor errors.
This is a finite-radius estimate, not an inference from a liminf.

## 3. Exact projection with its signed mixed error

Center and normalize
\[
v=\sqrt{H/\|h-\bar h\mathbf1\|^2}(h-\bar h\mathbf1).
\]
On a smaller common collar it is defined, balanced, of norm-squared \(H\),
and \(v-h=O(\eta)\). Put
\[
\widehat u=u+(U_0-\sum u_l)\mathbf1/8,\qquad
\varepsilon=v\cdot\widehat u-kJ_3(v)=O(\sqrt\eta),
\]
\[
u_{\min,l}(v)=(U_0+\rho H)/8+(k+\rho)J_3(v)v_l/H-\rho v_l^2,\qquad
K(v)=K_1+\alpha J_4(v)+\tau J_3(v)^2/H.
\]
Expanding the original coordinate square, without sampling profiles, gives
\[
\mathcal B(v,\widehat u)
=K(v)+\|\widehat u-u_{\min}(v)\|^2/2
                         +(k+\rho)J_3(v)\varepsilon/H.
\]
With \(s_0=(U_0+\rho H)/8\), \(b_0=(k+\rho)J_3(v)/H\), its full
unconstrained defect is
\[
s_0[\sum\widehat u-U_0+\rho(\|v\|^2-H)]
-s_0b_0\sum v-b_0^2(\|v\|^2-H)/2.
\]
The checker expands the complete invariant polynomial before imposing
balance, norm and mean. Replacing \(\widehat u\) by \(u\) costs \(O(\eta)\)
in the bounded square. Therefore for a common \(L_0\),
\[
\boxed{\Delta\ge K(v)+\|u-u_{\min}(v)\|^2/2
               -L_0\sqrt\eta\,|J_3(v)|-L_0\eta .}             \tag{A}
\]
The coefficient one-half retains the full residual. Its signed error
keeps the cubic-moment factor required for the joint budget range.

## 4. Complete fixed-cubic moment frontier

For a balanced norm-\(H\) real eight-vector, extrema of \(J_3\) on the
compact sphere have at most two coordinate values: independent gradients
\(\mathbf1,v\) and Lagrange multipliers give one common quadratic.
For counts \(n,8-n\), all seven cases give
\[
J_3^2/H^3=(8-2n)^2/[8n(8-n)]
=9/14,1/6,1/30,0,1/30,1/6,9/14.
\]
One value is impossible. Thus \(|J_3|\le J_*=H^{3/2}\sqrt{9/14}\),
with only1+7 at either extreme.

Fix a cubic level and maximize \(J_4\) on its compact fiber.
At a maximum with at least three distinct values, the three gradients
\(\mathbf1,v,v^2\) are independent by a Vandermonde minor.
Every coordinate solves one cubic
\(F(t)=4t^3-3\lambda t^2-2\mu t-\nu\).
Hence there are exactly three distinct roots \(r_1<r_2<r_3\).
A repeated outer value provides a unit-coordinate difference tangent to
all three constraints with constrained Hessian \(2F'(r_i)>0\).
This contradicts a maximum on the actual smooth constraint manifold.
Among all21 ordered positive multiplicities totaling8, only \((1,6,1)\)
survives. No assertion that a finite two-coordinate change preserves
all three constraints is used.

The profile is consequently six copies of \(m\), and \(-3m\pm r\).
Balance and norm give \(r^2=H/2-12m^2\), and middle ordering gives
\(r>4|m|\). Thus \(z=m^2/H<e=1/56\). Literal eight-coordinate sums give
\[
J_3=168m^3-9Hm,\quad J_4=H^2/2+30Hm^2-840m^4.
\]
Set \(g(z)=\sqrt z(9-168z)\), \(Q(z)=1/2+30z-840z^2\).
Then \(J_3^2/H^3=g(z)^2\), \(J_4/H^2=Q(z)\).
The continuous \(g\) is strictly increasing on \([0,e]\), from0 to
\(\sqrt{9/14}\); every cubic level is realized, with a unique parameter
and the sign of \(m\) choosing the cubic sign.

Singular two-value fibers need a separate calculation. Their coordinate
quadratic gives \(J_4/H^2=1/8+J_3^2/H^3\). At the same cubic level
the candidate's excess is
\[
Q(z)-1/8-g(z)^2=(1-56z)^2(3/8-9z)>0\quad(0\le z<e).
\]
At \(e\), the complete cubic classification already forces1+7.
These exhaust all maxima, including the opposed-pair profile at zero.
Thus \(H^2Q(z)\) is the global fixed-cubic quartic maximum, exactly
at the six+1+1 orbit and its limits. This independently proves the
essential10090 frontier without importing its program.

Put
\[
P(z)=(30\alpha+81\tau)z+(-840\alpha-3024\tau)z^2+28224\tau z^3 .
\]
Since \(\alpha<0\), for \(s=|J_3(v)|=H^{3/2}g(z)\),
\[
K(v)=B_*+H^2P(z)+(-\alpha)\mathcal D_4(v),\qquad
\mathcal D_4(v)=H^2Q(z)-J_4(v)\ge0 .                         \tag{B}
\]
The derivative is \(P'=(1-56z)(30\alpha+81\tau-1512\tau z)\).
Its second factor is at least \(30\alpha+54\tau>0\);
\(B_*+H^2P(e)=K_E\).

## 5. Endpoint-safe secants, strict concavity and optimal constants

Define \(f(H^{3/2}g(z))=H^2P(z)\), a continuous strictly increasing
function on \([0,J_*]\). Direct complete coefficient comparison gives
\[
P'-\gamma(g^2)'=-15\alpha(1-56z)^2\ge0,\qquad
\kappa(g^2)'-P'=-560\alpha z(1-56z)\ge0 .
\]
Integrating without dividing by vanishing endpoint derivatives gives
\[
\frac{\gamma}{H}(s_2^2-s_1^2)
\le f(s_2)-f(s_1)
\le\frac{\kappa}{H}(s_2^2-s_1^2)
\quad(0\le s_1\le s_2\le J_*).                             \tag{C}
\]

Additional proved conclusion: these global constants are optimal, and
the cost is strictly concave as a function of cubic-square.
For \(w=s^2\) in the open interval,
\[
\frac d{dw}f(\sqrt w)
=\frac1H\,\frac{30\alpha+81\tau-1512\tau z}{81-1512z}.
\]
The denominator stays at least54. Differentiation of this ratio with
respect to \(z\) has numerator \(45360\alpha<0\).
Since \(w\) increases in the interior, the derivative decreases strictly.
Its one-sided endpoint values are \(\kappa/H,\gamma/H\).
Continuity and integration extend strict concavity to the closed interval.
No second derivative at the merged endpoint is asserted.
Secants approaching the endpoints show that the upper constant cannot
decrease and the lower cannot increase. Every curve value is attained
by a balanced profile; no priority claim or effective physical collar
is inferred from this refinement.

Let \(s_\delta=f^{-1}(\delta)\) below saturation and \(J_*\) above it.
From(C),
\[
0\le s_{\delta_2}-s_{\delta_1}
\le\sqrt{H(\delta_2-\delta_1)/\gamma}\quad
(0\le\delta_1\le\delta_2).                                  \tag{D}
\]
Clipping only reduces the necessary cost interval.

## 6. Uniform exact-cut envelope and the joint limit

Fix \(D_{\max}>B_*\), using one common arm also covering the construction.
Write \(t=\sqrt\eta\), \(\delta=D-B_*\). From(A),(B),
\(f(s)\le\delta+L_0ts+L_0t^2\).
If \(s>s_\delta\), (C) gives
\[
s^2-s_\delta^2\le\nu ts+\nu t^2,\qquad \nu=L_0H/\gamma.
\]
Solving yields, in every case including saturation,
\[
s\le s_\delta+C_ut,\qquad C_u=(\nu+\sqrt{\nu^2+4\nu})/2.      \tag{E}
\]
The adopted all-nine cubic law, with \(h-v=O(\eta)\), gives for the
ORIGINAL physical displacement functional
\[
R=\max_j|Z_j-B_j(\eta)|/\eta^{3/2},\qquad |R-qs|\le L_rt,     \tag{F}
\]
where \(B_j(\eta)=\omega_j+\eta(-\omega_j/3-x-y/\omega_j)\).
The checker independently confirms the complete nine-label norm table,
\(q\), and maximizing labels2,7. Its analytic all-root remainder remains
the explicitly adopted10060 input. Thus every competitor obeys
\(R\le A(D)+(qC_u+L_r)\sqrt\eta\), with \(A(D)=qs_\delta\).
No attainment of the supremum is needed.

Choose \(\Lambda>L_c\), and require \(\delta\ge\Lambda\eta\).
Use the profile at curve cost \(\delta'=\delta-\Lambda\eta\), clipped
at \(K_E-B_*\). Its exact least cost is
\(B_*+\min(\delta',K_E-B_*)\le B_*+\delta'\).
The uniform actual chart supplies
\(|\Delta-K(v)|\le L_c\eta\), so the actual polynomial has
\(\Delta<D\), all nine originals strict/simple, for every eligible
moving \(D,\eta\), including \(\delta'=0\).
All chart/error/label constants are common. Equations(D),(F) give
\[
M_D(\eta)\ge A(D)-[q\sqrt{H\Lambda/\gamma}+L_r]\sqrt\eta .
\]
Shrink the common collar to make the displayed budget interval nonempty.
This proves nonemptiness and
\(|M_D(\eta)-A(D)|\le L\sqrt\eta\) uniformly for
\(B_*+\Lambda\eta\le D\le D_{\max}\), including exactly \(D=K_E\).
It establishes no fixed zero-slack quartic endpoint repair.

At zero, \(g(z)^2=81z+O(z^2)\), \(P(z)=81\kappa z+O(z^2)\).
Therefore
\(A(B_*+\delta)=q\sqrt{H\delta/\kappa}[1+O(\delta)]\).
For any positive function \(\delta(\eta)\to0\) with
\(\delta(\eta)/\eta\to\infty\), the exact moving class is eventually
nonempty, and division gives relative error
\(O(\delta+\sqrt{\eta/\delta})\to0\).
No continuity, monotonicity or exchange of pointwise limits is needed.
The critical \(\delta=O(\eta)\) layer remains unresolved.

## 7. Additional retained quartic and original real-correction stability

On the same fixed upper arm, suppose \(B_*\le D\le K_E\) and an actual
competitor satisfies \(R\ge A(D)-\epsilon\), \(\epsilon\ge0\).
Let \(s_D=s_{D-B_*}\), \(h_\epsilon=(\epsilon+L_rt)/q\).
Equation(F) gives \(s\ge s_D-h_\epsilon\), while (E) gives
\(s\le s_D+C_ut\). Retaining the nonnegative terms in(A),(B) yields
\[
\begin{split}
(-\alpha)\mathcal D_4(v)+\tfrac12\|u-u_{\min}(v)\|^2
&\le\frac{2\kappa}{qH}s_D\epsilon
+\left[\frac{2\kappa L_r}{qH}+L_0\right]s_Dt
+L_0(C_u+1)t^2 .                                           \tag{G}
\end{split}
\]
Indeed, if \(s\le s_D\), (C) gives
\(\delta-f(s)\le(\kappa/H)(s_D^2-s^2)\le2\kappa s_Dh_\epsilon/H\).
If \(s>s_D\), the cost difference is negative and can be replaced by zero.
Substitute into(A),(B) to obtain(G) in both cases.

For near-supremizers \(R\ge M_D-\epsilon\), replace \(\epsilon\) in(G)
by \(\epsilon+L\sqrt\eta\), using the established lower envelope.
On a joint shrinking cut \(\delta\gg\eta\), near-supremizers within
\(O(\sqrt\eta)\) consequently satisfy
\[
\mathcal D_4(v)+\|u-u_{\min}(v)\|^2
=O(\sqrt{\eta\delta}+\eta).
\]
This retains actual original real corrections and the complete quartic
defect, rather than only the cubic amplitude. The bound includes \(D=K_E\).
It is not asserted above \(K_E\): unused excess budget may pay for a
nonzero real correction. A uniform distance to the merged profile orbit
or an optimal stability constant needs a separate quantitative
fixed-cubic moment-defect argument and is not claimed.

## 8. Evidence and limits

Independent Fraction arithmetic realizes \(\mathbb Q(c)\) and
\(T=i\sin(\pi/9)\), \(T^2=c^2-1\).
A Newton recurrence/anchor expansion checks the whole retained real
polynomial; direct simple-root solving checks both complete physical
support maps; literal eight-coordinate sums check all retained moments;
sparse invariant expansion checks the entire unconstrained projection.
Complete polynomial identities, all seven two-value and21 ordered
three-value cases, secants, curvature, endpoint values, first-power
scalar coefficients and every original cubic norm are regenerated.
Rational root isolation identifies every embedding sign.

These finite calculations corroborate the identities. Constraint-manifold
completeness, concentration, uniform root derivatives, implicit-function
existence, Taylor bounds, compactness and the continuum envelope proof
remain ordinary mathematics with the adopted boundaries stated above.
No global first-power endpoint, effective collar, finite-radius optimizer,
minimum-budget feasibility or optimal next boundary coefficient is proved.

