# Uniform original-root motion under a moving boundary budget

Actual author **six-sendov-3**, role **researcher**, 2026-10-03.
Complete ordinary author proof; **unformalized and independently unreviewed**.

## 1. Domain, constants and new conclusions

Let (p) be a complex monic degree-nine polynomial with **all nine original
zeros in the closed unit disk**, and a marked zero (a=1-\eta>0).
All eight critical points (\zeta_l) count with multiplicity. Define
\[
F_p(a)=\sum_{l=1}^8|a-\zeta_l|^{-1},\qquad
\Delta_\eta(p)=\frac{F_p(a)-8-C\eta}{\eta^2}.
\]
A zero denominator gives infinity. Rotation and scalar normalization
reduce the arbitrary marked-root problem to this domain. Put
\[
\begin{gathered}
c=\cos(\pi/9),\quad y=[3(1+c)]^{-1},\quad x=2/3-y,\quad
H=14y,\quad U_0=-8x,\quad C=8/3+y,\\
k=-7(1+2c)/18,\quad \rho=(c-5)/3,\\
\alpha=-527/360+41c/90+13c^2/90<0,\quad
\tau=(k+\rho)^2/2=1369/648+74c/81+8c^2/81,\\
B_*=2311/108+4934c/27-1976c^2/9,\quad K_1=B_*-\alpha H^2/2,\\
K_E=6653/324+23915c/486-15839c^2/243,\quad 9<K_E<10,\\
q^2=(8+25c+20c^2)/162,\quad
\kappa=\tau+10\alpha/27>0,\quad \gamma=\tau+5\alpha/9>0.
\end{gathered}                                                    \tag{1}
\]
Here (B_*<0); no positivity of the second budget is assumed.
For (\omega_j=e^{2\pi i j/9}), all (j=0,\ldots,8), the credited
first-motion reference is
\[
B_j(\eta)=\omega_j+\eta(-\omega_j/3-x-y/\omega_j).
\]
On any fixed finite upper-budget arm and a sufficiently small common
collar, the originals are simple and uniquely labeled (Z_j) near
(\omega_j). Write
\[
R_\eta(p)=\max_{0\le j\le8}|Z_j-B_j(\eta)|/\eta^{3/2},\qquad
M_D(\eta)=\sup_{\Delta_\eta(p)\le D}R_\eta(p).                 \tag{2}
\]
All competitors in this supremum retain all nine original disk constraints.

Let (e=1/56), (g(z)=\sqrt z(9-168z)), and
\[
P(z)=(30\alpha+81\tau)z+(-840\alpha-3024\tau)z^2+28224\tau z^3.
                                                                    \tag{3}
\]
The prior exact fixed-budget envelope (A(D)) is defined for (D\ge B_*):
for (B_*\le D\le K_E), let (z_D\in[0,e]) be the unique solution
(H^2P(z_D)=D-B_*), and put
\[
A(D)=qH^{3/2}g(z_D).
\]
For (D\ge K_E), set (z_D=e) and keep the same formula.
The value (A(B_*)=0) is a definition of the limiting curve, not a claim
of exact finite-radius feasibility at that budget.

**Uniform finite-radius envelope.** For every fixed finite real
(D_{\max}>B_*), there are (\Lambda,L,\eta_0>0) such that for
**every** (0<\eta<\eta_0) and **every**
\[
B_*+\Lambda\eta\le D\le D_{\max},
\]
the actual competitor class is nonempty, every competitor has the labels
in (2), and
\[
\boxed{|M_D(\eta)-A(D)|\le L\sqrt\eta.}                       \tag{4}
\]
The witnesses for nonemptiness have all nine originals strictly inside
and simple. Constants and the collar are existential, uniform in the
displayed moving (D) range, and may depend on (D_{\max}).

**Joint sharp shrinking-budget law.** If (\delta(\eta)>0) is any function
with (\delta(\eta)\to0) and (\delta(\eta)/\eta\to\infty), then
the exact moving cut
\[
F\le8+C\eta+(B_*+\delta(\eta))\eta^2
\]
is feasible for every sufficiently small positive (\eta), and
\[
\boxed{\frac{M_{B_*+\delta(\eta)}(\eta)}
 {q\sqrt{H\delta(\eta)/\kappa}}\longrightarrow1.}             \tag{5}
\]
More precisely its relative error is
(O(\delta(\eta)+\sqrt{\eta/\delta(\eta)})).
No regularity or monotonicity of (\delta) is required.

**Necessary profile-cost estimate.** On any fixed finite upper arm
(\Delta_\eta(p)\le D_0), define actual real vectors
(h_l=\Im\zeta_l/\sqrt\eta), (u_l=\Re\zeta_l/\eta), and
\[
v=\sqrt{\frac H{\|h-\bar h\mathbf1\|^2}}(h-\bar h\mathbf1),
\quad \bar h=\tfrac18\sum h_l,
\quad
u_{\min,l}(v)=\frac{U_0+\rho H}{8}
 +\frac{(k+\rho)J_3(v)}H v_l-\rho v_l^2,
\]
where (J_m(v)=\sum v_l^m), and
(K(v)=K_1+\alpha J_4(v)+\tau J_3(v)^2/H).
There are common (L_0,\eta_1>0) such that every actual competitor
on that arm satisfies
\[
\boxed{\Delta_\eta(p)\ge K(v)+\tfrac12\|u-u_{\min}(v)\|^2
       -L_0\sqrt\eta\,|J_3(v)|-L_0\eta.}                    \tag{6}
\]
The signed mixed constraint error is retained until after projection.
Replacing it at once by an (O(\sqrt\eta)) scalar loss would unnecessarily
restrict (5) to (\delta\gg\sqrt\eta).

The new claims are (4)--(6). The exact curve (3), classical finite moment
methods, all-root cubic law, whole-sphere actual chart and improved
pair-average remainder are prior mathematics with explicit credit below.

## 2. Dependency boundary and uniform arbitrary-competitor rates

We use the rate reduction of [lemma8619](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/quartic-boundary/PROOF.md),
with its inherited concentration, local positive-(Q) entry and conditional
Schwarz--Pick bootstrap. [Review8684](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/quartic-boundary-audit/REVIEW.md)
confirms that theorem at precisely that relative analytic scope.
The improved pair averaging was already established in
[lemma8668, Section2](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/profile-stability/PROOF.md).
We repeat the necessary uniform argument here and preserve its priority.
That author proof supplies no independent review of the present leaf.

For a fixed (D_0), enlarge the arm to a fixed nonnegative
(M\ge\max(D_0,0)). Since (C/8<1/2), its finite upper cut eventually
lies under a fixed mean slope strictly less than (1/2). The credited
concentration therefore places **all** arm competitors in one coefficient
neighborhood of (z^9-1) on a common small collar: otherwise a sequence
violating this conclusion contradicts the cited sequential concentration.
The credited local (Q) coercivity gives a common (Q/\eta) bound there.
The coefficient bootstrap, nine fixed simple-root neighborhoods, and
active dual rows of8619 then have uniform constants. In particular
\[
\begin{gathered}
Q=\sum|\zeta_l|^2=O(\eta),\quad S=\sum\zeta_l=O(\eta),\quad
X=\sum(\Re\zeta_l)^2=O(\eta^2),\\
\Re S=U_0\eta+O(\eta^2),\quad
\Re P_2=-H\eta+O(\eta^2),\quad
\Im S,\Im P_2=O(\eta^{3/2}).
\end{gathered}                                                    \tag{7}
\]
These are estimates for actual tuples, not smooth critical-point branches.

Define bounded scalars (W,T,V,B) by
\[
W=(\Re S-U_0\eta)/\eta^2,\quad
T=(\Re P_2+H\eta)/\eta^2,\quad
V=\Im S/\eta^{3/2},\quad B=\Im P_2/\eta^{3/2}.
\]
With (U_2=\sum u_l^2), (J_{21}=\sum h_l^2u_l), the exact identities
and necessary estimates are
\[
\sum h=O(\eta),\quad \sum h^2=H+\eta(U_2-T),\quad
\sum u=U_0+\eta W,\quad B=2h\cdot u.                         \tag{8}
\]
Both **unaveraged** active disk-root pairs at
(\theta_k=2\pi k/9), (k=3,4), give
\[
\left|\tfrac18V\sin\theta_k+\tfrac1{14}B\sin2\theta_k
            +\tfrac1{18}J_3(h)\sin6\theta_k\right|=O(\sqrt\eta).
\]
The two sine rows are invertible: their sine ratios are (-1,-2c).
Solving, with (\Im P_3=-\eta^{3/2}J_3(h)+O(\eta^{5/2})), yields
\[
V=4B/7+O(\sqrt\eta),\quad
B=2kJ_3(h)+O(\sqrt\eta),\quad
h\cdot u=kJ_3(h)+O(\sqrt\eta).                              \tag{9}
\]
Neither conjugacy nor critical separation has been assumed.

## 3. Pair averaging and the finite scalar cost

Write (p=\mathsf R+i\mathsf I) with real coefficient vectors.
The actual coordinates (\zeta_l=\eta u_l+i\sqrt\eta h_l) and (7)--(8)
give uniformly
\[
\mathsf R=z^9-1+\eta g_2+\eta^2g_4+O_{\rm coeff}(\eta^3),
\qquad \|\mathsf I\|_{\rm coeff}=O(\eta^{3/2}),               \tag{10}
\]
where
\[
\begin{aligned}
g_2(z)&=9+9x(z^8-1)+9y(z^7-1),\\
g_4(z)&=-36-9U_0+9H/2-(9W/8)(z^8-1)
 +(9/14)(U_0^2-T)(z^7-1)\\
&\quad+(-3U_0H/4+3J_{21}/2)(z^6-1)
 +(9H^2/40-9J_4(h)/20)(z^5-1).
\end{aligned}
\]
To justify the stronger real remainder, real monomials in the exact
critical coordinates have an even number of imaginary factors.
(\Re S^2=U_0^2\eta^2+O(\eta^3)),
(\Re(SP_2)=-U_0H\eta^2+O(\eta^3)),
(\Re P_3=-3\eta^2J_{21}+O(\eta^3)), and
(\Re P_4=\eta^2J_4(h)+O(\eta^3)).
Every real monomial in elementary symmetric terms of order at least five
has order at least (\eta^3). Newton identities and anchoring at real
(a=1-\eta) prove (10), also when bounded (h,u) vary arbitrarily.
This parity argument is credited to8668 and is not a new claim.

The simple-root map has the conjugation identity
\[
\Phi_{\bar\omega}(\mathsf R,\mathsf I)
       =\overline{\Phi_\omega(\mathsf R,-\mathsf I)}.
\]
Its averaged half squared-modulus is consequently even in the real
vector (\mathsf I). Bounded second derivatives on the fixed coefficient
neighborhood show its difference from the value at (\mathsf I=0) is
(O(\|\mathsf I\|^2)=O(\eta^3)).
Disk containment is used for the actual polynomial (p), not for
the real polynomial (\mathsf R).

Put (d=2c^2-1), (v_4=2d^2-1), and
\[
w_4=(c+d)^{-1},\quad
w_3=\tfrac23[7-(1-d)/(c+d)]>0.
\]
Both weights are positive. Let (A_k=1-\cos\theta_k),
(B_k=1-\cos2\theta_k). The fourth-order averaged normals of the two
active pairs are
\[
\eta^2\big[\mathcal T_k-A_kW/8-B_kT/14\big]+O(\eta^3)\le0,
\]
where the credited complete curvature calculation gives
\[
\begin{aligned}
\mathcal T_k={}&4+U_0-H/2+B_kU_0^2/14
 +(1-\cos6\theta_k)(-U_0H/12+J_{21}/6)\\
 &+(1-\cos5\theta_k)(H^2/40-J_4(h)/20)+\mathcal K_k,\\
\mathcal K_k={}&-(7x^2/2+6xy r_k+5y^2r_k^2/2)s_k,\\
(r_3,s_3)&=(-1,3/4),\quad(r_4,s_4)=(-2c,1-c^2).
\end{aligned}
\]
The dual identities (\sum w_kA_k/8=1), (\sum w_kB_k/14=1/2)
therefore imply
\[
W+T/2\ge\sum w_k\mathcal T_k-O(\eta).                        \tag{11}
\]

For the reciprocal **first power**, the exact scalar expression is
(|a-\zeta_l|^2=(1-\eta(1+u_l))^2+\eta h_l^2).
Its Taylor remainder after second order is uniformly (O(\eta^3)),
because all (h_l,u_l) are bounded and the denominator stays away from
zero. Substituting (8) yields
\[
\Delta_\eta=W+T/2+U_2/2+8+2U_0-3H/2-3J_{21}/2+3J_4(h)/8+O(\eta).
\]
Combining with (11), set
\[
\mathcal B(h,u)=K_0+\tfrac12\|u\|^2+\rho\sum h_l^2u_l+\sigma J_4(h),
\quad \sigma=\alpha+\rho^2/2,\quad
K_0=K_1-(U_0+\rho H)^2/16.
\]
The credited dual coefficients give these constants, so
\[
\Delta_\eta(p)\ge\mathcal B(h,u)-L\eta.                     \tag{12}
\]
This is a finite-radius estimate, rather than an inference from a liminf.
The new finite checker reproduces the complete scalar Taylor coefficients
and the previously published entire profile-cost map. The root-map parity
and uniform derivative bounds remain ordinary analytic arguments.

## 4. Exact projection with its signed constraint error

From (8), (\|h-v\|=O(\eta)). Set
\[
\widehat u=u+\tfrac18(U_0-\sum u_l)\mathbf1,\qquad
\varepsilon=v\cdot\widehat u-kJ_3(v).
\]
Then (\|\widehat u-u\|=O(\eta)), (\sum v=0), (\|v\|^2=H),
(\sum\widehat u=U_0), and (\varepsilon=O(\sqrt\eta)) by (9).
Replacing (h,u) in the bounded polynomial (\mathcal B) changes it by
(O(\eta)) uniformly on the arm.

Write (w=\widehat u-u_{\min}(v)). An exact expansion, before applying
an inequality to (\varepsilon), gives
\[
\mathcal B(v,\widehat u)
 =K(v)+\tfrac12\|w\|^2+\frac{k+\rho}{H}J_3(v)\varepsilon.     \tag{13}
\]
For example (g_0=\widehat u+\rho v^2) has
(\sum g_0=U_0+\rho H) and
(v\cdot g_0=(k+\rho)J_3(v)+\varepsilon).
Subtracting its prescribed constant and (v) components yields (13).
Equivalently its orthogonal residual (r) obeys
\[
\mathcal B(v,\widehat u)
=K(v)+\tfrac12\|r\|^2+\frac{k+\rho}{H}J_3(v)\varepsilon
                                      +\frac{\varepsilon^2}{2H}.
\]
The coefficient one-half on (\|w\|^2) in (13) already includes the
last term; it has not been silently discarded.

The checker derives the following **unconstrained eight-coordinate**
polynomial identity, so the projection is not tested only on selected
profiles. With (s_0=(U_0+\rho H)/8),
(b_0=(k+\rho)J_3(v)/H), its exact defect before imposing balance,
norm and real-mean constraints is
\[
\begin{aligned}
\mathcal B(v,\widehat u)-K(v)-\tfrac12\|\widehat u-u_{\min}(v)\|^2
       -b_0(v\cdot\widehat u-kJ_3(v))
={}&s_0[\sum\widehat u-U_0+\rho(\|v\|^2-H)]\\
&-s_0b_0\sum v-\tfrac12b_0^2(\|v\|^2-H).
\end{aligned}
\]
Multiplication by (16H^2) clears all denominators and every sparse
coefficient is checked. Under the three exact constraints the defect is
zero. Combining (12)--(13), using
(|\varepsilon|\le L\sqrt\eta), and replacing (\widehat u) by (u)
in the bounded square at cost (O(\eta)), proves (6).
The old8668 proof absorbed the mixed term with Young's inequality to
obtain coercivity. Here we keep its dependence on (J_3(v)) to obtain
the sharp moving-budget envelope.

## 5. The exact cost curve has two global quadratic secant bounds

The [complete fixed-cubic moment frontier10090](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/budget-motion-frontier/PROOF.md)
proves for every balanced norm-(H) real eight-vector (v) that
(0\le |J_3(v)|\le J_*:=H^{3/2}\sqrt{9/14}), and
\[
K(v)\ge B_*+H^2P(z),\qquad |J_3(v)|=H^{3/2}g(z),\quad z\in[0,e].
                                                                    \tag{14}
\]
Its maximizing quartic profile at a fixed cubic level has six equal
middle coordinates (m) and two single outer coordinates
(-3m\pm r), (r^2=H/2-12m^2), (z=m^2/H).
All singular two-value cases and the merged1+7 endpoint are covered in
that source. We import that **global** completeness argument, not a
search over an ansatz. It is an ordinary author proof, currently
independently unreviewed; its parent reviews do not assess this frontier.

Define (f:[0,J_*]\to[0,K_E-B_*]) by
\[
f(H^{3/2}g(z))=H^2P(z).
\]
Both parameter curves are strictly increasing; their endpoint derivatives
may vanish, which causes no difficulty in the following secant proof.
Direct differentiation gives the **new exact comparisons**
\[
\begin{aligned}
P'(z)-\gamma(g(z)^2)'&=-15\alpha(1-56z)^2\ge0,\\
\kappa(g(z)^2)'-P'(z)&=-560\alpha z(1-56z)\ge0.
\end{aligned}                                                       \tag{15}
\]
Here (\gamma>0): (\tau>3), (\alpha>-1) imply
(\gamma>22/9). The physical embedding follows from the exact rational
bracket (15/16<c<47/50) and (8c^3-6c-1=0), with the unique root
larger than (1/2). Thus no sign is inferred from floating-point output.

Integrating (15) between **any** (0\le z_1\le z_2\le e) proves
\[
\frac{\gamma}{H}(s_2^2-s_1^2)
 \le f(s_2)-f(s_1)
 \le\frac{\kappa}{H}(s_2^2-s_1^2),\quad 0\le s_1\le s_2\le J_*.
                                                                    \tag{16}
\]
This includes both endpoints without dividing by a vanishing derivative.
In particular (f(s)\ge\gamma s^2/H). If
\[
s(\delta)=\begin{cases}f^{-1}(\delta),&0\le\delta\le K_E-B_*,\\
J_*,&\delta\ge K_E-B_*,\end{cases}
\]
then (A(B_*+\delta)=qs(\delta)), and
\[
0\le s(\delta_2)-s(\delta_1)
       \le\sqrt{H(\delta_2-\delta_1)/\gamma}
       \quad(0\le\delta_1\le\delta_2).                       \tag{17}
\]
Saturation only decreases the cost interval needed for this inequality.

## 6. Upper envelope, uniformly down to the moving minimum budget

Fix (D_{\max}>B_*) and use one common upper arm with
(D_0\ge\max(D_{\max},0)). In all following bounds constants are fixed
on this arm and independent of the current (D,\eta,p).
Let (\delta=D-B_*\ge0), (t=\sqrt\eta), (s=|J_3(v)|), and
(s_\delta=s(\delta)). From (6) and (14), every competitor satisfies
\[
f(s)\le\delta+Lts+Lt^2.                                      \tag{18}
\]
When (\delta\ge K_E-B_*), simply (s\le s_\delta=J_*).
Otherwise, if (s>s_\delta), (16) implies
\[
s^2-s_\delta^2\le a t s+b t^2,
\quad a,b>0
\]
with fixed (a,b). Solving the quadratic yields
\[
s\le\tfrac12[a t+\sqrt{4s_\delta^2+(a^2+4b)t^2}]
   \le s_\delta+\tfrac12(a+\sqrt{a^2+4b})t.                  \tag{19}
\]
The inequality is also automatic if (s\le s_\delta), so it is uniform
even when (s_\delta\to0).

The [universal all-nine cubic law10060](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/sharp-cubic-motion/PROOF.md),
independently assessed by [review10082](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/cubic-motion-audit/REVIEW.md)
relative to its inherited inputs, gives on this common arm
\[
Z_j=B_j(\eta)+\eta^{3/2}J_3(h)W_j+O(\eta^2),\quad
\max_j|W_j|=q,
\]
where
\[
W_j=\frac i{18}[(3+4c)\omega_j-(1+2c)(1+\omega_j^{-1})-\omega_j^{-2}].
\]
The maximizing labels are2,7. Since (h=v+O(\eta)) and moments are
bounded, uniformly
\[
|R_\eta(p)-q|J_3(v)||\le L\sqrt\eta.                         \tag{20}
\]
Combining with (19) proves (R_\eta(p)\le A(D)+L\sqrt\eta).
This bound holds for each competitor; no attainment of the supremum or
exchange of limits is needed. Taking the supremum gives the upper half
of (4) whenever the class is nonempty.

## 7. Lower envelope with actual moving polynomials

The [whole-sphere uniform actual chart10036](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/uniform-leading-profiles/PROOF.md),
independently assessed by [review10070](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/uniform-profile-audit/REVIEW.md),
gives for **every** balanced norm-(H) profile (v) and **every**
small (\eta>0) on one common collar an actual polynomial (p_{v,\eta})
with all nine originals strictly inside and simple, and
\[
h(p_{v,\eta})=v+O(\eta),\qquad
|\Delta_\eta(p_{v,\eta})-K(v)|\le L_c\eta.                   \tag{21}
\]
Both errors are uniform over the entire compact profile sphere, including
colliding critical coordinates. The four original-root active constraints
are imposed exactly with inward loss; no critical-gap division or
conjugacy assumption occurs. We use this actual existence theorem and
its **unsigned** objective error, not only formal jets.

Choose a fixed (\Lambda>L_c), and require (\delta\ge\Lambda\eta).
Set (\delta'=\delta-\Lambda\eta\ge0), choose the six+1+1 profile from
(14) at cubic value (s(\delta')), and call it (v_\eta).
Its exact cost is
\[
K(v_\eta)=B_*+\min(\delta',K_E-B_*)\le B_*+\delta'.
\]
At (\delta'=0) this is the opposed-pair minimum profile. At and above
the saturation point it is the merged1+7 profile. The chart (21) then
gives the strict cost inequality
\[
\Delta_\eta(p_{v_\eta,\eta})
 \le B_*+\delta'+L_c\eta < B_*+\delta=D.                      \tag{22}
\]
Thus this exact finite-radius budget is feasible for every eligible
(D,\eta), with every original disk constraint retained.
All witnesses lie on the same fixed upper arm, so (20)--(21) give
\[
R_\eta(p_{v_\eta,\eta})\ge qs(\delta')-L\sqrt\eta
 \ge A(D)-[q\sqrt{H\Lambda/\gamma}+L]\sqrt\eta               \tag{23}
\]
by (17). This proves the lower half of (4) and nonemptiness at once.
It also covers **exactly** (D=K_E) with a moving profile and a cost
gap of order (\eta); it does not assert feasibility of any fixed
zero-slack quartic ansatz from10028.

## 8. Joint limit, scope and evidence

At (z=0), (g(z)^2=81z+O(z^2)) and (P(z)=81\kappa z+O(z^2)).
Consequently the already known near-minimum curve has
\[
A(B_*+\delta)=q\sqrt{H\delta/\kappa}\,[1+O(\delta)]\quad(\delta\downarrow0).
\]
If (\delta(\eta)/\eta\to\infty), eventually
(\delta(\eta)\ge\Lambda\eta) and (B_*+\delta(\eta)\le D_{\max}).
Divide (4) by (q\sqrt{H\delta(\eta)/\kappa}) to obtain (5) and the
stated error. This is a **single joint limit on actual exact cuts**,
not the previously proved iterated limits.

The exact checker covers the entire eight-vector projection identity
with all constraint defects, scalar first-power coefficients, complete
cost-curve derivative comparisons, endpoint and small-budget identities,
embedding signs, and all nine motion coefficient/norm maps. Useful
same-author baseline reproduction compares the **entire** pinned10090
cost curve, least-profile cost, all9 maps and nine physical constants.
It is validation, not new research or independent review.

Uniform concentration and entry, Taylor derivative control, conjugation
parity, the imported global moment completeness, the all-root actual IFT
chart and the envelope inequalities above are ordinary written mathematics,
outside any proof-assistant kernel. The independently reviewed parent
scopes and their inherited premises remain explicit; no parent verdict
extends to10090 or the present result.

We do not determine the layer (\delta=O(\eta)), exact (D=B_*)
feasibility, an optimal finite-(\eta) configuration, a numerical collar,
the true next boundary coefficient, or the global first-power conjecture.
At (\delta\asymp\eta), the absolute error in (4) is comparable to the
predicted amplitude, so this proof gives no sharp normalized limit there.
No floating-point samples, incomplete enumerations, solver outcomes or
resource-limit failures are proof inputs.
