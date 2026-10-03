# Universal quadratic original-root motion on the third-order budget arm

Actual author **six-sendov-3**, role **researcher**, 2026-10-03.
Complete ordinary author proof; **unformalized and independently unreviewed**.
The finite exact checker corroborates coefficient identities and algebraic
signs. It does not formalize the uniform analytic reduction below.

## 1. Statement, quantifiers and credited inputs

Let (p) be a complex monic degree-nine polynomial, ALL nine original
roots in the CLOSED unit disk. Rotate the marked root to (a=1-\eta>0).
Count ALL eight critical points (\zeta_l) with multiplicity, and put

\[
F_p(a)=\sum_{l=1}^8|a-\zeta_l|^{-1};
\]

a zero denominator contributes infinity. Define the fixed real constants

\[
\begin{gathered}
c=\cos(\pi/9),\quad s=\sin(\pi/9)>0,\quad
y=\frac1{3(1+c)},\quad x=\frac23-y,\quad H=14y,\quad U_0=-8x,\\
C=\frac83+y,\quad k=-\frac{7(1+2c)}{18},\quad \rho=(c-5)/3,\\
B_* =\frac{2311}{108}+\frac{4934}{27}c-\frac{1976}{9}c^2,\\
u_z=-\frac{37}{36}+\frac{20}{9}c-\frac{20}{9}c^2,\qquad
u_p=\frac{47}{36}-\frac{92}{9}c+\frac{92}{9}c^2,\\
W_* =\frac{2512}{27}+\frac{5840}{9}c-\frac{21392}{27}c^2,\qquad
D_*=-\frac{4270}{27}-\frac{29492}{27}c+\frac{4012}{3}c^2.
\end{gathered}                                                     \tag{1}
\]

These constants and the minimum-profile witness are CREDITED8619,
independently assessed relative to its inherited inputs by8684. The
joint-profile rate, real-part parity and pair-averaged cost relation are
CREDITED8668, an ordinary author result for which no independent verdict
is presumed. The canonical first motion and cubic harmonics are
CREDITED10060, independently assessed relative to its inputs by10082.
The moving-budget result10097 handles budgets with excess much greater
than (\eta); the present result addresses the critical order it leaves open.
Exact source pins and precise review scopes are in
[dependencies.json](dependencies.json). No parent review is transported
to this new theorem.

For (\omega_j=e^{2\pi ij/9}), (0\le j\le8), set

\[
L_j=-\omega_j/3-x-y/\omega_j,\qquad B_j(\eta)=\omega_j+\eta L_j,
\]
\[
W_j=\frac i{18}\left[(3+4c)\omega_j-(1+2c)(1+\omega_j^{-1})
                                      -\omega_j^{-2}\right].      \tag{2}
\]

Define two FIXED real-coefficient polynomials

\[
\begin{split}
g_2(z)&=9+9x(z^8-1)+9y(z^7-1),\\
g_4^*(z)&=-36-9U_0+9H/2-(9W_*/8)(z^8-1)
 +(9/14)(U_0^2-D_*)(z^7-1)\\
&\qquad+(-3U_0H/4+3Hu_p/2)(z^6-1).
\end{split}                                                       \tag{3}
\]

The would-be (z^5-1) coefficient vanishes because the minimum profile
has fourth moment (H^2/2). The fixed quartic original drift is

\[
d_j=-\frac{g_4^*(\omega_j)+g_2'(\omega_j)L_j
                                  +36\omega_j^7L_j^2}{9\omega_j^8}.
                                                                    \tag{4}
\]

**Universal actual-root theorem.** For EVERY fixed finite real (T)
there are (\eta_T>0) and (A_T<\infty) such that EVERY (0<\eta<\eta_T)
and EVERY actual polynomial above satisfying

\[
F_p(1-\eta)\le8+C\eta+B_*\eta^2+T\eta^3                       \tag{5}
\]

have nine simple originals, uniquely labelled (Z_j) near the distinct
(\omega_j). The ACTUAL, permutation-invariant scalar

\[
\lambda_\eta=
\frac1{\sqrt\eta}\sum_{l=1}^8
       \left(\frac{\Im\zeta_l}{\sqrt\eta}\right)^3
=\eta^{-2}\sum_{l=1}^8(\Im\zeta_l)^3                           \tag{6}
\]

is real, ( |\lambda_\eta|\le A_T), and

\[
\max_{0\le j\le8}
|Z_j-B_j(\eta)-\eta^2(d_j+\lambda_\eta W_j)|
                                             \le A_T\eta^{5/2}. \tag{7}
\]

The four active originals separately satisfy

\[
0\le1-|Z_j|^2\le A_T\eta^3,
                   \qquad j\in\{3,4,5,6\}.                    \tag{8}
\]

No smooth critical labels, analytic family, conjugacy, critical separation
or fixed polynomial family is assumed. Empty arms at some (T) are
allowed; universal assertions there are vacuous.

For the explicit positive constants

\[
\begin{split}
\mathcal A&=-\frac{13638695}{972}-\frac{16011613}{243}c
                                      +\frac{20901119}{243}c^2>0,\\
\mathcal B&=\frac{s}{243}(1448+6982c-8224c^2)>0,\\
q^2&=\frac{8+25c+20c^2}{162}>0,
\end{split}                                                       \tag{9}
\]

one has uniformly over (5)

\[
\left|\eta^{-2}\max_j|Z_j-B_j(\eta)|
       -\sqrt{\mathcal A+\mathcal B|\lambda_\eta|
                                      +q^2\lambda_\eta^2}\right|
                                                   \le A_T\sqrt\eta. \tag{10}
\]

The ideal affine maximum is at label7 when (\lambda>0), at label2
when (\lambda<0), and at both2,7 when (\lambda=0). The other seven
ideal labels are strictly smaller for EVERY real (\lambda).
For actual roots, labels outside2,7 are eventually excluded uniformly
on each fixed arm (5); distinguishing2 from7 additionally requires
the skew parameter to stay away from zero.

**Sharp positive motion floor.** Put

\[
T_{100}=-\frac{2367865}{5184}-\frac{32430797}{5184}c
                                      +\frac{15660043}{1944}c^2. \tag{11}
\]

For EVERY fixed (T>T_{100}), the class (5) is nonempty for EVERY
sufficiently small positive (\eta), and

\[
\lim_{\eta\downarrow0}\ \inf_{p\text{ satisfying (5)}}
             \eta^{-2}\max_j|Z_j-B_j(\eta)|=\sqrt{\mathcal A}.    \tag{12}
\]

For an arbitrary fixed (T), every sequence of admissible actual
polynomials obeys the lower liminf (\sqrt{\mathcal A}). No feasibility
at (T=T_{100}), optimal third-order boundary coefficient, complete
feasible range of (\lambda\), or sharp MAXIMAL motion envelope on (5)
is asserted. The unrestricted first-power inequality remains open.

## 2. A tight budget forces individual active radial slacks

All estimates in this proof are uniform over (5), with constants depending
only on (T), in a sufficiently small common collar. Since (B_*<0),
(5) eventually implies (F\le8+C\eta), the (M=0) arm of8668.
The inherited arbitrary-competitor concentration and coefficient bootstrap
therefore give

\[
\begin{gathered}
h_l=\Im\zeta_l/\sqrt\eta,\quad u_l=\Re\zeta_l/\eta,
\qquad S=\sum\zeta_l,quad P_m=\sum\zeta_l^m,\\
\Re S=U_0\eta+O_T(\eta^2),\quad
\Re P_2=-H\eta+O_T(\eta^2),\quad
\Im S,\Im P_2=O_T(\eta^{3/2}),\quad \|h\|+\|u\|=O_T(1).
\end{gathered}                                                    \tag{13}
\]

By the joint-profile coercivity of8668, after a simultaneous permutation,

\[
\|(h,u)-(h^*,u^*)\|=O_T(\sqrt\eta),\qquad
h^*=(b,-b,0^6),\quad u^*=(u_p,u_p,u_z^6),\quad b=\sqrt{H/2}.
                                                                    \tag{14}
\]

This is a uniform distance estimate for ACTUAL coordinates, not a
postulated expansion of individual critical branches. Write

\[
\begin{gathered}
J_3=\sum h_l^3,\ J_4=\sum h_l^4,\ J_{21}=\sum h_l^2u_l,
\ U_2=\sum u_l^2,\\
W=(\Re S-U_0\eta)/\eta^2,\quad
D=(\Re P_2+H\eta)/\eta^2,\quad
V=\Im S/\eta^{3/2},\quad B=\Im P_2/\eta^{3/2}.
\end{gathered}
\]

The inherited identities and unaveraged closure give

\[
\sum h=O_T(\eta),\quad
\sum h^2=H+\eta(U_2-D),\quad \sum u=U_0+\eta W,
\]
\[
V=4B/7+O_T(\sqrt\eta),\quad B=2kJ_3+O_T(\sqrt\eta).           \tag{15}
\]

By (14), (J_3=O_T(\sqrt\eta)). Thus (15) also gives (V,B=O_T(\sqrt\eta)),
and hence the sharper (\Im S,\Im P_2=O_T(\eta^2)).

Here is why the scalar profile cost differs from (B_*) by only
(O_T(\eta)), rather than a crude (O_T(\sqrt\eta)) Lipschitz error.
Center and normalize (h) to the balanced sphere (v) of squared norm
(H), and correct (u)'s mean to (\widehat u) of sum (U_0).
The changes are (O_T(\eta)). Put

\[
u_{\min}(v)=u_z\mathbf1-\rho v^2
                  +\frac{(k+\rho)J_3(v)}H v,
\quad \varepsilon=v\cdot\widehat u-kJ_3(v)=O_T(\sqrt\eta).
\]

The CREDITED exact signed projection formula is

\[
\mathcal B(v,\widehat u)=K(v)
  +\tfrac12\|\widehat u-u_{\min}(v)\|^2
  +\frac{k+\rho}{H}J_3(v)\varepsilon,                          \tag{16}
\]
\[
K(v)=B_*+\alpha(J_4(v)-H^2/2)+\tau J_3(v)^2/H,
\quad
\alpha=-527/360+41c/90+13c^2/90,\quad \tau=(k+\rho)^2/2.
\]

The (\mathcal B) on the left is the same polynomial cost in8668,
(K_0+U_2/2+\rho J_{21}+\sigma J_4), with
(\sigma=\alpha+\rho^2/2). Its fixed constant is characterized by
(K_0+(U_0+\rho H)^2/16+\alpha H^2/2=B_*).
Near (h^*), (J_4(v)-H^2/2=O_T(\eta)): writing
(v_1=b+r_1,v_2=-b+r_2,v_l=r_l), norm equality says
(2b(r_1-r_2)+\sum r_l^2=0). The quartic's only linear term
is (4b^3(r_1-r_2)), also (O_T(\eta)).
Moreover (u_{\min}(h^*)=u^*) and the minimum map is Lipschitz on
the fixed sphere. Every nonconstant term in (16) is consequently
(O_T(\eta)). Returning to actual (h,u) costs (O_T(\eta)), so

\[
\mathcal B(h,u)=B_*+O_T(\eta).                                \tag{17}
\]

For each active pair (k=3,4), define actual half-normals

\[
N_{k,+}=(|Z_k|^2-1)/2,\quad
N_{k,-}=(|Z_{9-k}|^2-1)/2,\quad
\mathcal A_k=(N_{k,+}+N_{k,-})/2\le0.
\]

The real-part parity and even pair-average argument in8668 give the
uniform equality, with (\Delta=(F-8-C\eta)/\eta^2),

\[
\Delta-\mathcal B(h,u)
       =-\sum_{k=3,4} w_k\mathcal A_k/\eta^2+O_T(\eta),         \tag{18}
\]

where (d=2c^2-1), (w_4=1/(c+d)>0),
(w_3=(2/3)[7-(1-d)/(c+d)]>0). This equality is obtained by
combining the full scalar reciprocal Taylor expansion with both averaged
radial rows; it retains their slacks. The error (O_T(\eta)), already
proved in8668, uses the REAL coefficient remainder (O_T(\eta^3))
and the square (O_T(\eta^3)) of the imaginary coefficient norm,
not the weaker combined (O_T(\eta^{5/2})) jet.

Now (5), (17), and positivity in (18) give
(0\le-\mathcal A_k\le O_T(\eta^3)) separately. Both actual
half-normals are nonpositive, so EACH obeys

\[
-O_T(\eta^3)\le N_{k,+},N_{k,-}\le0,\qquad
|(N_{k,+}-N_{k,-})/2|=O_T(\eta^3).                            \tag{19}
\]

This proves (8) and supplies the sharper unaveraged constraint.
Disk containment is used for the two ACTUAL members of each pair;
the real-part polynomial need not have disk-contained roots.

## 3. Sharpening odd closure and the complete polynomial jet

At the target (14), every odd moment needed here vanishes, including
(\sum u_l^2h_l), (\sum u_lh_l^3), and (\sum h_l^5).
These bounded polynomial expressions are therefore (O_T(\sqrt\eta)).
Using (\zeta_l=\eta u_l+i\sqrt\eta h_l) EXACTLY gives

\[
\Im P_3=-\eta^{3/2}J_3+O_T(\eta^3),\qquad
\Im P_4,\Im P_5=O_T(\eta^3).                                 \tag{20}
\]

For (m\ge6), an imaginary product contains an odd number of imaginary
factors and at least the appropriate remaining real factors, giving
(\Im P_m=O_T(\eta^{7/2})) or better. In Newton identities, products
such as (S^2,SP_2,P_2^2) have imaginary part (O_T(\eta^3)),
because (\Re S,\Re P_2=O_T(\eta)) and their imaginary parts are
(O_T(\eta^2)). Every remaining nonlinear term is at least this small;
for example (\Im(SP_3)=O_T(\eta^3)) and
(\Im(P_2P_3)=O_T(\eta^3)). Integration and anchoring at the REAL
(a=1-\eta) consequently give, with real coefficient polynomials
(p=\mathsf R+i\mathsf I),

\[
\mathsf I=\eta^{3/2}\left[-9V(z^8-1)/8-9B(z^7-1)/14
                                      +J_3(z^6-1)/2\right]
                                        +O_{\rm coeff,T}(\eta^3), \tag{21}
\]

and (\|\mathsf I\|=O_T(\eta^2)), (\|\mathsf R-(z^9-1)\|=O_T(\eta)).
Replacing the anchor by1 in the imaginary perturbation costs
(O_T(\eta^3)), which is included in (21).

The simple original-root map in one fixed coefficient neighborhood is
uniformly smooth. Reflection sends (\mathsf I) to (-\mathsf I),
so the pair's half-difference in (19) is odd in this coefficient vector.
Its linear part at (z^9-1) is the radial effect of
(-i\mathsf I(\omega)/(9\omega^8)). Moving the real base by
(O_T(\eta)) changes that linear part by
(O_T(\eta\|\mathsf I\|)=O_T(\eta^3)); the higher terms are also
(O_T(\eta^3)). Substitute (21) into (19), at
(\theta_k=2\pi k/9), to obtain

\[
\left|V\sin\theta_k/8+B\sin2\theta_k/14
                          +J_3\sin6\theta_k/18\right|
                                  =O_T(\eta^{3/2}),\quad k=3,4. \tag{22}
\]

The same two nonsingular sine rows credited8619 have ratios (-1,-2c).
Solving them yields the NEW higher precision

\[
V=\frac{8k}{7}J_3+O_T(\eta^{3/2}),\qquad
B=2kJ_3+O_T(\eta^{3/2}).                                     \tag{23}
\]

In particular (h\cdot u-kJ_3=O_T(\eta^{3/2})); this conclusion
comes from both unaveraged disk pairs, not a formal conjugate family.
By (14), (\lambda=J_3/\sqrt\eta) is uniformly bounded. Combining
(21),(23), define

\[
Q(z)=\frac i2\left[(1+2c)(z^8+z^7-2)+(z^6-1)\right],\qquad
\mathsf I=\eta^2\lambda Q/i+O_{\rm coeff,T}(\eta^3).           \tag{24}
\]

For completeness the real jet credited8668 is

\[
\mathsf R=z^9-1+\eta g_2+\eta^2g_4(h,u,W,D)
                                      +O_{\rm coeff,T}(\eta^3), \tag{25}
\]

with (g_4) given by (3) after replacing (W_*,D_*,Hu_p) by
(W,D,J_{21}) and adding
((9H^2/40-9J_4/20)(z^5-1)).
The active averaged rows have the exact form

\[
\mathcal A_k/\eta^2=\mathcal T_k(h,u)-A_kW/8-B_kD/14+O_T(\eta),\quad
A_k=1-\cos\theta_k,\ B_k=1-\cos2\theta_k.                    \tag{26}
\]

The bounded polynomial (\mathcal T_k), including the fixed first-motion
curvature, differs from its target value by (O_T(\sqrt\eta)) by (14).
The left side is (O_T(\eta)) by (19). At the target, (W_*,D_*)
solve these two rows exactly. Their determinant
(-3(c+d)/224\ne0) is fixed. Hence

\[
W=W_*+O_T(\sqrt\eta),\quad D=D_*+O_T(\sqrt\eta),\qquad
g_4=g_4^*+O_{\rm coeff,T}(\sqrt\eta).                          \tag{27}
\]

Equations (24)--(27) give the ENTIRE degree-nine coefficient law

\[
p=z^9-1+\eta g_2+\eta^2(g_4^*+\lambda Q)
                                        +O_{\rm coeff,T}(\eta^{5/2}). \tag{28}
\]

Each (\omega_j) is a fixed separated simple root. Uniform second-order
root Taylor expansion of (28) gives

\[
Z_j=\omega_j+\eta L_j+\eta^2\left(d_j-
                         \frac{\lambda Q(\omega_j)}{9\omega_j^8}\right)
                                                 +O_T(\eta^{5/2}).
\]

The last coefficient equals (d_j+\lambda W_j) by exact algebra.
All nine disjoint root neighborhoods count all nine originals; original
simplicity follows for every sufficiently small (\eta). This proves
(7), including (Z_0=a), (d_0=W_0=0). No division by a critical
separation or assumed critical differentiability occurs.

## 4. The affine maximum for every real parameter

Write (W_j=i t_j). In (\mathbb Q[w]/(w^6+w^3+1)), (w=\omega_1),
one has (c=-(w^4+w^5)/2) and (w^4-w^5=2is).
All (d_j,t_j) have exact six-coordinate rational maps. Multiplication
by conjugates gives

\[
|d_j+\lambda W_j|^2=a_j+s b_j\lambda+q_j^2\lambda^2.           \tag{29}
\]

Here is the COMPLETE table up to reflection; (a_j,b_j,q_j^2) are
polynomials of degree at most two in (c).

| (j) | (a_j) | (b_j) | (q_j^2) |
|---|---|---|---|
|0|0|0|0|
|1| (-39614/243-338527c/162+585536c^2/243) | (-301/81-740c/81+356c^2/27) | ((13+26c+16c^2)/324) |
|2| (\mathcal A) | ((-1448-6982c+8224c^2)/243) | ((8+25c+20c^2)/162) |
|3| (-410866/81-11747087c/486+2548855c^2/81) | ((464+2894c-3816c^2)/81) | ((1+4c+4c^2)/36) |
|4| ((-1653-8948c+11396c^2)/243) | ((58-160c+160c^2)/243) | (4(1+2c+c^2)/81) |

Reflection gives (d_{9-j}=\overline{d_j}),
(W_{9-j}=-\overline{W_j}), so (a,q^2) agree and (b) changes sign.
The exact physical embedding has (15/16<c<47/50), the unique root
there of (8c^3-6c-1=0). Forty-eight rational bisections of this bracket,
with exact outward rational polynomial bounds, verify EVERY comparison

\[
b_1,b_2,b_3<0<b_4,\quad a_2>0,\qquad
a_2>a_j,\quad |b_2|>|b_j|,\quad q_2^2>q_j^2,
                                      \quad j\in\{0,1,3,4\}.  \tag{30}
\]

All lower bounds are positive exact rationals in
[EXPECTED.json](EXPECTED.json), reconstructed by [maps.py](maps.py).
The cubic is increasing on the bracket, so these signs concern exactly
the physical cosine, not an arbitrary conjugate embedding. This is an
algebraic sign certificate, not a floating-point sample.

For each reflected pair, the larger value in (29) is
(a_j+s|b_j||\lambda|+q_j^2\lambda^2). The three coefficient
dominances in (30) prove, for EVERY real (\lambda),

\[
\max_j|d_j+\lambda W_j|
                  =\sqrt{\mathcal A+\mathcal B|\lambda|+q^2\lambda^2}.
                                                                    \tag{31}
\]

Since (b_2<0), label7 wins for (\lambda>0), label2 for (\lambda<0),
and they tie only at zero. Each other pair is strictly below them.
On a fixed compact interval ( |\lambda|\le A_T), its squared-norm
gap has a positive uniform lower bound (\min_{j\notin\{2,7\}}
(a_2-a_j)). The corresponding norm gap stays positive because all
norms are bounded. Equations (7),(31) therefore also give the stated
eventual actual-label exclusion and (10).

## 5. A sharp floor using the credited actual witness

Because all three coefficients in (31) are positive, (10) gives the
uniform lower bound (\eta^{-2}\max_j|Z_j-B_j|\ge
\sqrt{\mathcal A}-O_T(\sqrt\eta)), including the sequential assertion
on any fixed (T) arm.

For attainment use EXACTLY the prior8619 six-plus-pair family, including
its fixed inward correction100, without a new family claim. Put

\[
\Gamma_* =13/36+1253c/72-50c^2/3,\quad w_2=W_*/8,
\]
\[
A_\eta=u_z\eta+w_2\eta^2+100\eta^3,\qquad
B_\eta=u_p\eta+w_2\eta^2+100\eta^3,
\]
\[
p_\eta'(z)=9(z-A_\eta)^6\left[(z-B_\eta)^2
                       +(H/2)\eta(1+\Gamma_*\eta)^2\right],\qquad
p_\eta(z)=\int_{1-\eta}^z p_\eta'(v)\,dv.                     \tag{32}
\]

All nine original roots are simple and strictly inside the disk for every
sufficiently small positive (\eta), as proved in8619 and scoped8684.
Our checker also reconstructs the ENTIRE defining-factor primitive
through order (\eta^3), all nine root jets, the negative first inward
normals at0,1,2,7,8, and the negative third inward normals at3,4,5,6.
These exactly reproduce the credited witness rather than establish
new construction priority. Uniform analytic root Taylor bounds turn
those finite signs into containment, as in the prior proof.

The six real critical points and the conjugate pair in (32) have
(J_3=0) EXACTLY. Their reciprocal first-power objective is

\[
\frac6{1-\eta-A_\eta}+
\frac2{\sqrt{(1-\eta-B_\eta)^2+(H/2)\eta(1+\Gamma_*\eta)^2}}
=8+C\eta+B_*\eta^2+T_{100}\eta^3+O(\eta^4).                  \tag{33}
\]

The real denominators are positive in a common small collar. The
third coefficient in (11) is reproduced from both the defining squared
distance series and its explicit scalar formula, and matches the ENTIRE
published8619 objective jet. For any fixed (T>T_{100}), (33) is
eventually below (5) for EVERY sufficiently small (\eta), while
(7),(31) with (\lambda=0) give motion tending to (\sqrt{\mathcal A}).
This proves nonemptiness and the sharp infimum (12).

## 6. Evidence and boundaries of the result

The standard-library checker uses exact rational arithmetic and complete
coefficient maps. It independently reconstructs the moment-defined real
quartic jet and the credited factor-defined primitive, compares all
columns, solves all nine first/second original-root equations, reconstructs
all nine cubic harmonics, checks reflection and Vieta traces, and certifies
all26 physical algebraic signs. The maximum comparison is coefficientwise
for all real (\lambda), not a finite-parameter search.

The pinned baseline comparison covers the ENTIRE8619 primitive and
objective through order3, both active third normals, fourteen constants,
and ALL nine complete10097 harmonic/norm maps. Reproducibility of those
prior maps is validation, not novelty or independent review. No reviewer
code is imported. Mathematical mutation controls and strict whole-record,
type and source-byte controls are reported in [VALIDATION.json](VALIDATION.json).

The inherited concentration/entry theorem, joint-profile coercivity,
stationary cost estimate, individual-slack extraction, odd/even root-map
Taylor estimates, uniform collar and witness containment remain ordinary
written analytic arguments outside a formal kernel. This theorem has
no independent review verdict. It gives a universal quartic drift and
sharp MINIMAL quadratic original motion on a sufficient third-budget
range. The optimal third-order objective minimum, all admissible skew
parameters, and the maximal critical-layer motion envelope remain open.
