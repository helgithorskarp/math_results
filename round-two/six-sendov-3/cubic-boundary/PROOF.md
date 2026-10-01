# The third degree-nine first-power boundary coefficient

Actual author **six-sendov-3**, role **researcher**, 2026-10-01.
Complete ordinary author proof with exact finite algebra; independent review
of this extension is pending. Boundary collars and remainder constants are
existential. The explicit profile-penalty coefficient is not asserted sharp.

## 1. Statements and credited inputs

Let p have degree nine and all original roots in the closed unit disk.
For a marked root a define

\[
F_p(a)=\sum_{j=1}^8 |a-\zeta_j|^{-1},
\]

with critical multiplicities counted and a zero denominator meaning infinity.
Normalize p to be monic and rotate a to a=1-eta>0. Put

\[
\begin{gathered}
c=\cos(\pi/9),\quad d=2c^2-1,\quad v=2d^2-1,\quad
y=\frac1{3(1+c)},\quad x=\frac23-y,\quad H=14y,\quad U_0=-8x,\\
C=\frac83+y,\quad B_*=\frac{2311}{108}+\frac{4934}{27}c-\frac{1976}{9}c^2,\\
\rho=(c-5)/3,\quad u_z=(U_0+\rho H)/8,\quad u_p=u_z-\rho H/2,\quad b=\sqrt{H/2}.
\end{gathered}                                                     \tag{1}
\]

Both C and Bstar and the selected profile below are credited prior results.
The new exact third coefficient is

\[
C_3=-\frac{60800959}{17496}
     -\frac{307083769}{17496}c+\frac{10980067}{486}c^2<0.           \tag{2}
\]

Write h_j=Im(zeta_j)/sqrt(eta), u_j=Re(zeta_j)/eta, and let
\(\mathcal M\) be the finite simultaneous-permutation set of

\[
h^*=(b,-b,0,\ldots,0),\qquad
u^*=(u_p,u_p,u_z,\ldots,u_z).
\]

Write \(\mathcal D_\eta=\operatorname{dist}((h,u),\mathcal M)\),
the joint Euclidean distance, and abbreviate it as Deta in prose.

**Quantitative cubic theorem.** For every fixed finite real T there are
positive K_T,eta_T such that every such polynomial with

\[
0<\eta<\eta_T,\qquad
F_p(a)\le 8+C\eta+B_*\eta^2+T\eta^3                           \tag{3}
\]

satisfies

\[
F_p(a)-8-C\eta-B_*\eta^2-C_3\eta^3
\ \ge\ \frac{\eta^2}{1024}\mathcal D_\eta^2-K_T\eta^4.         \tag{4}
\]

The numerical coefficient is uniform in T. The collar and error constant
may depend on T; no numerical collar is supplied.

**Universal boundary minimum.** There are K,eta0>0 such that all degree-nine
disk-root polynomials with 0<eta<eta0 obey

\[
F_p(a)\ge8+C\eta+B_*\eta^2+C_3\eta^3-K\eta^4.                 \tag{5}
\]

At every sufficiently small eta an explicit all-disk family has
F=8+C eta+Bstar eta2+C3 eta3+O(eta4). Consequently

\[
\inf_{p,a:\ |a|=r}F_p(a)
=8+C(1-r)+B_*(1-r)^2+C_3(1-r)^3+O((1-r)^4).                \tag{6}
\]

Equivalently the normalized radius-wise third infimum tends to C3.
Since C3<0, the exact quadratic line 8+C eta+Bstar eta2 is not a
universal lower bound, even arbitrarily near the boundary.

**Finer profile rate.** Every fixed fourth-order upper budget
F<=8+C eta+Bstar eta2+C3 eta3+U eta4 forces Deta=O(eta).
After permutation, the large pair has imaginary coordinates
plus/minus b sqrt(eta)+O(eta^(3/2)) and real coordinates
up eta+O(eta2). The other six have imaginary coordinates
O(eta^(3/2)) and real coordinates uz eta+O(eta2).
The joint O(eta) profile rate is optimal: the attaining family has
Deta/eta tending to a positive explicitly given constant.
Individual coordinate exponents are not all asserted optimal.

The primary direct input is the author's
[quantitative second-order profile theorem8668](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/profile-stability/PROOF.md),
artifact bafkreif5f6ahrnzovf43wsut4mtjz5kdbyzsh2ouxqxcxm22nhkaylynzy,
source3f74956df840a6763e34087e87323ded361cd1d0.
Its quantitative gap supplies Deta=O(sqrt eta) under (3).
The
[independent reviewer-one audit8684](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/quartic-boundary-audit/REVIEW.md),
artifact bafkreib53wtjf5wvfzzpcuvssztl776tvxzukaexx55f7vwgilg46w645a,
source691ea3f4eaa4b06b46ab0aded63903d81d95c668,
supplies the exact feasible finite-cost coercivity1/128 used below.
It confirms parent8619 and its all-root attainment, while explicitly
not auditing8668. Its common-repair threshold is for a fixed
one-parameter family and is not a global third coefficient.
The reviewed concentration/bootstrap7190 remain inherited prerequisites.
The full dependencies were read and useful exact baselines reproduced.

Before publication, the independent
[profile audit8718](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/profile-stability-audit/REVIEW.md),
artifact bafkreiasqdzisb6tzsm4y2ikn5jzhvwrs6ooravwdrokpmg7ky5nzmrmtq,
source fbccce294ae6dd2928951a7c89d7a0b7476d70b8,
confirmed8668 and proved that its original-polynomial second-order penalty
can be any fixed coefficient below1/128. It also transfers the finite
coercivity by exact mixed-constraint projection and Young's inequality.
That technique and the parent confirmation retain attribution. The new
content here is the sharper residual (18), retained normalization cost,
exact third optimum, fourth-order remainder and finer fourth-budget rate.
Audit8718 explicitly does not audit this cubic extension.

## 2. Preliminary rates and the active-slack equality

Fix T and assume (3). As Bstar<0, this eventually lies in the second-order
budget M=0 of8668. Its theorem gives, after a permutation,

\[
\|h-h^*\|+\|u-u^*\|=O(\sqrt\eta).                             \tag{7}
\]

All following constants may depend on T, while the reference constants
and finite-cost coefficient are fixed. Write S=sum zeta_j, P=sum zeta_j2,
P_m=sum zeta_j^m and

\[
\begin{gathered}
R=\Re S=U_0\eta+\eta^2W,\quad
\Re P=-H\eta+\eta^2D,\quad
J_k=\sum h_j^k,\quad J_{21}=\sum h_j^2u_j,\quad U_2=\sum u_j^2,\\
V=\Im S/\eta^{3/2},\quad B=\Im P/\eta^{3/2}=2h\cdot u,\quad
L=-7(2c+1)/18 .
\end{gathered}
\]

The prior bounded-budget bootstrap gives bounded W,D,h,u and

\[
\sum h=\eta V,\quad \sum h^2=H+\eta(U_2-D),\quad
\sum u=U_0+\eta W,\quad V=4B/7+O(\sqrt\eta).                 \tag{8}
\]

At the limiting profile J3=h dot u=J5=sum(h3 u)=sum(h u2)=0.
These are bounded polynomials in h,u, so (7) bounds them by O(sqrt eta).
Therefore B=O(sqrt eta), V=O(sqrt eta), and

\[
\Im S,\Im P=O(\eta^2),\qquad \sum h=O(\eta^{3/2}).            \tag{9}
\]

The full imaginary coefficient vector I of p=Rpoly+iI is O(eta2).
Indeed Im P3=O(eta2), while the leading imaginary monomials in e4,e5
vanish at the selected profile and their O(sqrt eta) variation puts them
at O(eta3). Higher monomials start no earlier than eta^(7/2).
Products involving ImS or ImP do not change the leading O(eta2) bound.
Newton identities and real anchoring preserve these orders.

Use theta_k=2pi k/9, k=3,4, and

\[
(A_3,B_3)=(3/2,3/2),\quad (A_4,B_4)=(1+c,1-d),\quad
w_4=(c+d)^{-1},\quad w_3=\tfrac23[7-(1-d)/(c+d)].
\]

Both weights are positive, with sum wA/8=1 and sum wB/14=1/2.
Let a_k^plus,a_k^minus denote half squared-modulus minus one of the
actual original roots near the active conjugate pair, and Aavg_k their
average. Thus each a_k^plus/minus<=0. The prior root curvature formula is

\[
Aavg_k=\eta^2[\mathcal T_k(h,u)-A_kW/8-B_kD/14]+O(\eta^3).    \tag{10}
\]

Its full T expression is recalled in Section4. Set s_k=-Aavg_k/eta2>=0.
Let

\[
\mathcal B(h,u)=K_0+\|u\|^2/2+\rho J_{21}+\sigma J_4,\quad
\sigma=\frac38-\frac{(3/2)w_3+(1-v)w_4}{20},                 \tag{11}
\]

with the credited constant
\(K_0=-2609/405-(2000/81)c+(12964/405)c^2\). The scalar
identity and (10) give the equality up to a controlled error

\[
\frac{F-8-C\eta-B_*\eta^2}{\eta^2}
=\mathcal B(h,u)-B_*+\sum w_ks_k+O(\eta).                    \tag{12}
\]

There is no dropped nonnegative slack in this equality.
At the reference profile,

\[
\nabla_u\mathcal B=u_z{\bf1},\quad
\nabla_h\mathcal B=2(\rho u_p+\sigma H)h^*.                   \tag{13}
\]

Equations (7)-(8) and Taylor's formula imply Bcost-Bstar=O(eta):
the u linear term is uz etaW, the h linear term uses
2hstar dot(h-hstar)=eta(U2-D)-||h-hstar||2, and the quadratic
Taylor remainder is O(eta). The left side of (12) is bounded above
by T eta. Hence the positive weighted slacks satisfy s_k=O(eta).
Each a_k^plus/minus lies between -O(eta3) and zero, because its
nonpositive partner and their average have that bound. Thus

\[
|a_k^\mathrm{plus}|+|a_k^\mathrm{minus}|=O(\eta^3).           \tag{14}
\]

This holds for arbitrary complex competitors and uses no critical symmetry.

## 3. The sharpened imaginary-moment constraint

For a simple nonagon root omega, the root map Phi_omega(Rpoly,I)
in a fixed coefficient neighborhood satisfies
Phi_baromega(Rpoly,I)=conjugate(Phi_omega(Rpoly,-I)).
The half-difference of the two radial quantities is odd in I.
Uniform derivative bounds and Rpoly-(z9-1)=O(eta) give

\[
\tfrac12(a_k^\mathrm{plus}-a_k^\mathrm{minus})
=\ell_k(I)+O(\eta\|I\|+\|I\|^3),                            \tag{15}
\]

where ell is the linearization at z9-1. This error is O(eta3) by (9).
Newton identities give

\[
I=-\tfrac98\Im S(z^8-1)-\tfrac9{14}\Im P(z^7-1)
   -\tfrac12\Im P_3(z^6-1)+O_\mathrm{coeff}(\eta^3).          \tag{16}
\]

Here Im P4=O(eta3) since sum(h3 u)=O(sqrt eta);
Im P5=O(eta3) since J5=O(sqrt eta); and the omitted products
of low moments have at least eta3 imaginary order. Also exactly
Im P3=-eta^(3/2)J3+3eta^(5/2)sum(h u2), whose error is O(eta3).
Using (14)-(16) yields

\[
\left|\frac{\Im S}{8}\sin\theta_k+
\frac{\Im P}{14}\sin2\theta_k-
\frac{\Im P_3}{18}\sin6\theta_k\right|=O(\eta^3).             \tag{17}
\]

The sine ratios are -1 and -2c, so the rows are invertible.
After dividing by eta^(3/2), solving them gives

\[
V=4B/7+O(\eta^{3/2}),\quad
B=-7(2c+1)J_3/9+O(\eta^{3/2}),\quad
h\cdot u-LJ_3=O(\eta^{3/2}).                                \tag{18}
\]

This is the completeness bridge that rules out a cubic gain from an
uncontrolled imaginary phase. It does not assume an analytic family of
critical points. Original-root maps are analytic in their coefficient
neighborhood, and all remainder bounds hold for moving bounded parameters.

## 4. The full real eta3 polynomial and dual cost

Introduce U3=sum u3, J22=sum h2u2, J41=sum h4u and J6=sum h6.
The new generic real expansion is

\[
Rpoly=z^9-1+\eta g_2+\eta^2g_4+\eta^3g_6+O_\mathrm{coeff}(\eta^4). \tag{19}
\]

The first two terms retain their prior formulas:

\[
\begin{aligned}
g_2={}&9+9x(z^8-1)+9y(z^7-1),\\
g_4={}&-36-9U_0+9H/2-(9W/8)(z^8-1)
+(9/14)(U_0^2-D)(z^7-1)\\
&+(-3U_0H/4+3J_{21}/2)(z^6-1)
+(9H^2/40-9J_4/20)(z^5-1).
\end{aligned}
\]

Write g6=K6+sum c_n(z^n-1), n=3,...,7. Its complete coefficients are

\[
\begin{aligned}
K_6={}&84+(63/2)U_0-(27/2)H-9W+(9/2)(U_0^2-D)\\
&-(9/2)U_0H+9J_{21}+(9/8)H^2-(9/4)J_4,\\
c_7={}&9U_0W/7,\\
c_6={}&-U_0^3/4+3(U_0D-HW)/4-U_3/2,\\
c_5={}&(9/5)(U_0^2H/4-HD/4-U_0J_{21}+3J_{22}/2),\\
c_4={}&-(9/4)(U_0H^2/8-HJ_{21}/2-U_0J_4/4+J_{41}),\\
c_3={}&3(H^3/48-HJ_4/8+J_6/6).                              \tag{20}
\end{aligned}
\]

To derive this, use
Re P3=-3eta2J21+eta3U3,
Re P4=eta2J4-6eta3J22+O(eta4),
Re P5=5eta3J41+O(eta4), and Re P6=-eta3J6+O(eta4).
Imaginary low moments are O(eta2), so their products in real coefficients
start at eta4. Every real monomial in e7,e8 starts at eta4.
Newton recurrence then gives every displayed coefficient; anchoring at
1-eta supplies K6. The checker verifies the full identity with ten
independent real and six independent imaginary moment symbols.

For use in (10), the credited expression is

\[
\begin{aligned}
\mathcal T_k={}&4+U_0-H/2+B_kU_0^2/14
+(1-\cos6\theta_k)(-U_0H/12+J_{21}/6)\\
&+(1-\cos5\theta_k)(H^2/40-J_4/20)
-(7x^2/2+6xyr_k+5y^2r_k^2/2)t_k,\\
(r_3,t_3)&=(-1,3/4),\quad (r_4,t_4)=(-2c,1-c^2).
\end{aligned}
\]

By s_k=O(eta), the two invertible active rows now imply

\[
W=W_*+O(\mathcal D_\eta+\eta),\quad
D=D_*+O(\mathcal D_\eta+\eta),                              \tag{21}
\]

where the credited exact values are

\[
W_*=2512/27+(5840/9)c-(21392/27)c^2,\quad
D_*=-4270/27-(29492/27)c+(4012/3)c^2.
\]

Indeed T(h,u)-T(hstar,ustar)=O(Deta), by bounded polynomial moments.
All g4,g6 coefficients therefore differ from their limiting values
by O(Deta+eta), while g2 is fixed.

Let Rkstar be the third half squared-modulus coefficient for
z9-1+eta g2+eta2g4star+eta3g6star near the active omega_k.
It is completely specified by the implicit equations

\[
\begin{aligned}
t_1&=-g_2(\omega)\omega/9,\\
t_2&=-[g_4(\omega)+g_2'(\omega)t_1+36\omega^7t_1^2]\omega/9,\\
t_3&=-[g_6(\omega)+g_4'(\omega)t_1+g_2'(\omega)t_2
+g_2''(\omega)t_1^2/2\\
&\hspace{30mm}+72\omega^7t_1t_2+84\omega^6t_1^3]\omega/9,\\
R_k^*&=\Re(t_3\bar\omega+t_1\bar t_2).                       \tag{22}
\end{aligned}
\]

The pair average is even in I and differs from its real-polynomial value
by O(||I||2)=O(eta4). Uniform simple-root expansion of (19) and (21)
therefore gives

\[
W+D/2\ge\sum w_k\mathcal T_k+
\eta\sum w_kR_k^*-O(\eta\mathcal D_\eta+\eta^2).              \tag{23}
\]

No disk hypothesis is imposed on Rpoly; only the actual p roots give
the disk inequalities.

Expand each exact squared distance
(1-eta(1+u))2+eta h2. After substituting the exact mean/norm identities,
the additional scalar eta3 coefficient at the limiting profile is

\[
f_3^*=2W_*-\tfrac32(U_2^*-D_*)+
\sum_j[(1+u_j^*)^3-3(h_j^*)^2(1+u_j^*)^2
+\tfrac{15}{8}(h_j^*)^4(1+u_j^*)-\tfrac5{16}(h_j^*)^6].
\]

The scalar coefficient's variation is O(Deta+eta). Combining it with
(23) yields

\[
F\ge8+C\eta+\eta^2\mathcal B(h,u)
+\eta^3[f_3^*+\sum w_kR_k^*]
-O(\eta^3\mathcal D_\eta+\eta^4).                            \tag{24}
\]

## 5. Exact feasible projection and normalization correction

Balance and normalize h and adjust the mean of u:

\[
\widehat h=\sqrt{H/\|h-\bar h{\bf1}\|^2}(h-\bar h{\bf1}),\quad
\bar h=\tfrac18\sum h,\quad
\widehat u=u-\eta W{\bf1}/8 .
\]

They differ from h,u by O(eta), have exact zero h-mean,
h-norm squared H, and u-mean sum U0. Their mixed residual
delta=hat h dot hat u-LJ3(hat h) is O(eta^(3/2)) by (9),(18):
the norm correction is O(eta), while J3 and h dot u are O(sqrt eta);
the h-mean correction is O(eta^(3/2)).
Set

\[
\widetilde u=\widehat u-\delta\widehat h/H .
\]

The pair (hat h,tilde u) satisfies all four exact finite constraints.
The independent finite coercivity theorem8684 applies:

\[
\mathcal B(\widehat h,\widetilde u)-B_*
\ge \tfrac1{128}\operatorname{dist}((\widehat h,\widetilde u),\mathcal M)^2.
\]

The exact cost change on reversing this last projection is
delta(L+rho)J3/H+delta2/(2H)=O(eta2).
Distance to a fixed set is1-Lipschitz and the total projection is O(eta),
so its squared distance is at least Deta2/2-O(eta2). Consequently

\[
\mathcal B(\widehat h,\widehat u)-B_*
\ge\mathcal D_\eta^2/256-O(\eta^2).                          \tag{25}
\]

It remains essential to retain the first normalization correction.
Let k=rho up+sigma H. By (13), Taylor expansion around the limiting
profile, (8), and (21), gives

\[
\mathcal B(h,u)-\mathcal B(\widehat h,\widehat u)
=\eta\Theta_*+O(\eta\mathcal D_\eta+\eta^2),\quad
\Theta_*=u_zW_*+k(U_2^*-D_*).                               \tag{26}
\]

For detail, the u linear term is exactly uz etaW.
Also 2hstar dot(h-hhat)=eta(U2-D)+O(eta Deta+eta2),
because hhat has norm squared H and h-hhat=O(eta).
The gradient variation and quadratic Taylor error cost
O(eta Deta+eta2). Finally replace W,D,U2 by their limiting values
using (21).

Exact cubic-field arithmetic proves

\[
\Theta_*+f_3^*+\sum w_kR_k^*=C_3.                            \tag{27}
\]

The checker obtains this independently of the explicit-family objective.
Insert (25)-(27) into (24). We obtain a lower gap
eta2Deta2/256-K eta3Deta-K eta4.
Young's inequality absorbs K eta Deta into Deta2/512 plus
a T-dependent multiple of eta2. This proves the stronger coefficient
1/512 and hence the stated1/1024 in (4).
The transfer preserves a universal numerical coefficient while its
collar/error constants remain existential.

For (5), use (4) with T=0 whenever F<=8+C eta+Bstar eta2.
Otherwise (5) follows since C3<0. Infinite F is immediate.
The upper family below proves (6) at every sufficiently small radius.
A fixed fourth-order budget eventually satisfies (3) with T=0,
because C3<0; (4) then gives Deta=O(eta), yielding the listed coordinates.

## 6. The attaining family and all-nine-root coverage

Use the credited gamma=(U2star-Dstar)/(2H)
=13/36+(1253/72)c-(50/3)c2 and the new constants

\[
\begin{aligned}
m&=-17403419/34992-(45702565/17496)c+(180635/54)c^2,\\
\theta&=-1162307/23328-(5484833/11664)c+(52426519/93312)c^2 .
\end{aligned}
\]

Set

\[
\begin{gathered}
L_0=u_z\eta+(W_*/8)\eta^2+m\eta^3+10\eta^4,\quad
L_p=u_p\eta+(W_*/8)\eta^2+m\eta^3+10\eta^4,\\
q'_\eta(z)=9(z-L_0)^6
\big[(z-L_p)^2+(H/2)\eta(1+\gamma\eta+\theta\eta^2)^2\big],\\
q_\eta(z)=\int_{1-\eta}^zq'_\eta(w)\,dw .                    \tag{28}
\end{gathered}
\]

This full defining formula, not merely a truncated jet, is monic degree nine
with marked root1-eta. Its eight critical points are six copies of L0
and Lp plus/minus i b sqrt(eta)(1+gamma eta+theta eta2).

The two new free corrections have affine third-coefficient responses

\[
p_3(m,\theta)=p_3(0,0)-9m(z^8-1)+(9H/7)\theta(z^7-1).
\]

At each active pair, the third radial coefficient is
Rk100-Ak(m-100)+(H Bk/7)theta. The displayed constants solve both
equations exactly. The objective third coefficient changes by
8(m-100)-H theta, giving the same C3 as (27).
This two-parameter cancellation is distinct from the fixed-common-repair
threshold credited to8684.

The checker multiplies and integrates the full factors through eta4 with
m,theta independent before substitution. It solves original-root coefficients
in two ways: explicit Taylor recursion and an independent complete polynomial
residual iteration. They agree at all nine ninth roots and all retained orders.
The marked branch is exactly1-eta. The four inactive branches have negative
first half squared-modulus coefficients. All four active branches have first,
second and third coefficients zero; the common10 eta4 correction makes their
fourth coefficients strictly negative, certified in the chosen real cubic
embedding. Every conjugate and the marked branch is checked individually.

At eta=0, q=z9-1 has nine simple roots. Formula (28) has coefficients
polynomial in eta, hence original roots are analytic in a common interval.
The finite set of strictly negative leading radial coefficients and their
uniform Taylor remainders put every root strictly inside the disk for all
sufficiently small positive eta. There is no sampled-root coverage argument.

The exact critical distances yield

\[
F_{q_\eta}(1-\eta)
=\frac6{1-\eta-L_0}
+\frac2{\sqrt{(1-\eta-L_p)^2+(H/2)\eta(1+\gamma\eta+\theta\eta^2)^2}}
=8+C\eta+B_*\eta^2+C_3\eta^3+O(\eta^4).
\]

Its normalized profile has

\[
\mathcal D_\eta/\eta\longrightarrow
\sqrt{H\gamma^2+W_*^2/8}>0 ,
\]

because h=(1+gamma eta+O(eta2))hstar and
u=ustar+(Wstar/8)eta times the constant vector+O(eta2).
Thus the joint fourth-budget rate cannot be improved to o(eta).

## 7. Evidence and remaining boundaries

The self-contained standard-library checker uses a full eighteen-symbol
Gaussian-rational moment ring through eta3 and a separate
Q[c]/(8c3-6c-1)[eta,z,m,theta] kernel through eta4.
Exact quadratic Gaussian extensions evaluate every ninth root.
Rational cubic-embedding isolation proves all signs. Complete fixtures,
mathematical mutation controls and all-nine-root residual checks are described
in README.md. It imports no prior source and uses no numerical root input.

This is an ordinary author proof with exact algebraic validation. The
inherited concentration/bootstrap, root-map derivative bounds, active-slack
and odd-root bootstrap, projection/Taylor/Young estimates and all-root
analytic containment remain outside a formal kernel. Author validation is
not independent review of this extension. Reviewer8684's finite cost,
parent confirmation and fixed-family threshold retain attribution.
Reviewer8718's confirmation of8668 and numerical second-order transfer
are also prior work; neither audit establishes the new cubic theorem.

The full first-power endpoint away from the boundary, an effective numerical
collar, the sharp profile-penalty constant and the fourth optimal boundary
coefficient remain unproved here. No solver timeout, incomplete enumeration
or process limit is used as mathematical evidence.
