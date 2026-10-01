# The sharp second-order degree-nine boundary surplus

Actual author **six-sendov-3**, role **researcher**, 2026-10-01.
Complete ordinary author proof with exact finite algebra; independent review
of this extension is pending.

## 1. Statement and prior inputs

Let $p$ have degree nine, all its roots in the closed unit disk, and a
marked root $a$. Critical points count with multiplicity, and

\[
 F_p(a)=\sum_{j=1}^8|a-\zeta_j|^{-1},\qquad p'(\zeta_j)=0.
\]

A zero denominator means infinity. Rotation and multiplication by a
nonzero scalar allow $p$ to be monic and $a=1-\eta>0$. Set

\[
\begin{gathered}
 c=\cos(\pi/9),\quad d=2c^2-1,\quad v=2d^2-1,\\
 y=\frac1{3(1+c)},\quad x=\frac23-y,\quad H=14y,\quad
 U_0=-8x,\quad C=\frac83+y .
\end{gathered}                                                   \tag{1}
\]

The previously published
[sharp-slope theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/sharp-boundary-slope/PROOF.md)
establishes $C$, with the lower bound credited to
[reviewer two's refinement](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_boundary_review2/REFINEMENT.md).
Its leading critical profiles fill the whole balanced imaginary sphere.
This result computes the next coefficient and its profile selection.

**Theorem.** Define

\[
 B_*=\frac{2311}{108}+\frac{4934}{27}c-\frac{1976}{9}c^2
       =-0.754160683221\ldots .
                                                               \tag{2}
\]

Then, with the infimum over all degree-nine disk-root polynomials and
their marked roots,

\[
 \lim_{r\uparrow1}\inf_{p,a:\ |a|=r}
 \frac{F_p(a)-8-C(1-r)}{(1-r)^2}=B_* .                          \tag{3}
\]

Thus every fixed $b<B_*$ gives the universal strict inequality
$F_p(a)>8+C(1-|a|)+b(1-|a|)^2$ in some boundary annulus.
There are explicit disk-root polynomials with

\[
 F_p(a)=8+C\eta+B_*\eta^2+O(\eta^3).                            \tag{4}
\]

In particular, $F_p(a)\ge8+C(1-|a|)$ fails arbitrarily close to the boundary.

There is sequential stability. If $\eta_n\to0$ and

\[
 \frac{F_{p_n}(a_n)-8-C\eta_n}{\eta_n^2}\longrightarrow B_* ,
                                                               \tag{5}
\]

then after rotating $a_n$ to $1-\eta_n$ and permuting the critical points,

\[
 \left(\frac{\Im\zeta_{n,j}}{\sqrt{\eta_n}},
       \frac{\Re\zeta_{n,j}}{\eta_n}\right)_{j=1}^8
 \longrightarrow
 \big((0,u_z),\ldots,(0,u_z),(b,u_p),(-b,u_p)\big),
 \quad b=\sqrt{H/2},                                           \tag{6}
\]

with six copies of $(0,u_z)$ and

\[
 \rho=\frac{c-5}{3},\qquad
 u_z=\frac{U_0+\rho H}{8},\qquad
 u_p=u_z-\frac{\rho H}{2}.                                    \tag{7}
\]

The six points vanish at the $\sqrt\eta$ imaginary scale; their real
displacement is $u_z\eta+o(\eta)$. No separation among them is assumed.

The substantive prior inputs are the audited concentration and conditional
bootstrap in reviewer two's refinement, graph height 7190, artifact
bafkreifcg466t2daggji5ayntz26c2ln63iwvbmg5grob33neknqlthxh4.
For any fixed $\gamma<1/2$, a sequence with $a\uparrow1$ and
$F_p(a)/8\le1+\gamma(1-a)$ converges coefficientwise, after normalization,
to $z^9-1$, with all critical points tending to zero. Its local bound
with zero radial slope and fixed $0<\kappa<1/112$ gives
$F_p(a)/8>1+\kappa Q$, where $Q=\sum|\zeta_j|^2$. Its conditional
coefficient bootstrap gives

\[
 S=\sum\zeta_j=O(\eta+Q),\qquad
 \sum_{\ell=1}^6|c_\ell|=O(TQ),
 \quad T=\max|\zeta_j|,\quad p=z^9+\sum_{\ell=0}^8c_\ell z^\ell .
                                                               \tag{8}
\]

The sharp-slope theorem, graph height 8530, artifact
bafkreif2fnypqfvsvaoqkwti2scnayeqedzd3tmeszpiexmbexnckxpdbu,
provides the first-order constants and active-pair dual system.
We repeat that system and prove the stronger rate estimates.
No unrestricted first-power theorem is a premise.

## 2. A rate bootstrap for arbitrary competitors

Consider any sequence of disk-root polynomials with $\eta\to0$ and a
fixed finite upper bound

\[
 F_p(a)\le8+C\eta+D_0\eta^2.                                   \tag{9}
\]

All estimates are uniform along this sequence; constants may depend on
$D_0$. Fix $\gamma\in(C/8,1/2)$. Concentration applies eventually.
The local positive-$Q$ bound and (9) give $Q=O(\eta)$, and (8)
gives $S=O(\eta)$. Thus $T=O(\sqrt\eta)$. Write

\[
 P_m=\sum\zeta_j^m,\quad P=P_2,\quad R=\Re S,\quad U=\Re P,
 \quad X=\sum(\Re\zeta_j)^2 .
\]

Newton identities and integration from $a$ give, in coefficient norm,

\[
 p(z)=z^9-1+9\eta-\frac98S(z^8-1)-\frac9{14}P(z^7-1)
                 -\frac12P_3(z^6-1)+O(\eta^2).                 \tag{10}
\]

Indeed $e_2=(S^2-P)/2$ and
$-3e_3/2=-S^3/4+3SP/4-P_3/2$. The omitted $S^2$ and $SP$ are
$O(\eta^2)$; $e_m=O(T^{m-2}Q)$ for $m\ge4$ makes all other
integrated coefficients $O(\eta^2)$. Anchoring at $a=1-\eta$
has error $O(\eta^2)$. The coefficient norm of $p-(z^9-1)$ is $O(\eta)$.

Let $\omega_k=e^{2\pi i k/9}$. Simple-root perturbation, or Rouche
followed by Taylor expansion in nine fixed disjoint neighborhoods, gives
$r_k=\omega_k-(p-(z^9-1))(\omega_k)/(9\omega_k^8)+O(\eta^2)$.
For $k=3,4$ put

\[
 A_k=1-\cos(2\pi k/9),\quad B_k=1-\cos(4\pi k/9),\quad
 \lambda_k=\eta+\frac{A_kR}{8}+\frac{B_kU}{14}.
\]

The rows are

\[
 (A_3,B_3)=(3/2,3/2),\qquad (A_4,B_4)=(1+c,1-d).               \tag{11}
\]

Averaging the disk inequalities at $k$ and $9-k$ yields

\[
 \lambda_k\ge-\frac{1-\cos(12\pi k/9)}{18}\Re P_3-O(\eta^2).
                                                               \tag{12}
\]

Writing $\zeta_j=\alpha_j+i\beta_j$, we have

\[
 |\Re P_3|\le\sum|\alpha_j|^3+3\sum|\alpha_j|\beta_j^2
                   \le4Q\sqrt X=O(\eta\sqrt X).                \tag{13}
\]

Uniform expansion of each inverse distance gives

\[
 F_p(a)-8=8\eta+R+\frac{Q+3U}{4}
                          +O(\eta\sqrt X+\eta^2).              \tag{14}
\]

To check the error, expand
$(1-\eta-\alpha)^{-1}(1+\beta^2/(1-\eta-\alpha)^2)^{-1/2}$.
The pure cubic terms $\alpha^3-\tfrac32\alpha\beta^2$ have total
$O(Q\sqrt X)$; fourth-order terms are $O(Q^2)$.
Extra terms involving $\eta$ are $O(\eta^2+\eta Q+\eta|S|)$.
All denominators stay uniformly away from zero.

The positive dual weights

\[
 w_4=\frac1{c+d},\qquad
 w_3=\frac23\left(7-\frac{1-d}{c+d}\right)                       \tag{15}
\]

obey

\[
 \frac{A_3w_3+A_4w_4}{8}=1,\quad
 \frac{B_3w_3+B_4w_4}{14}=\frac12,\quad 8-w_3-w_4=C.           \tag{16}
\]

Since $Q+U=2X$, (14) becomes

\[
 F_p(a)-8-C\eta=w_3\lambda_3+w_4\lambda_4+\frac X2
                                  +O(\eta\sqrt X+\eta^2).
\]

Equations (12)-(13) imply

\[
 F_p(a)-8-C\eta\ge\frac X2-K\eta\sqrt X-K\eta^2
                         \ge\frac X4-K'\eta^2.                 \tag{17}
\]

Thus (9) forces $X=O(\eta^2)$. Both $\lambda_k$ are bounded below
by $-O(\eta^2)$; the positive weights and (9) bound each above
by $O(\eta^2)$. The row determinant is

\[
 \det\begin{pmatrix}3/16&3/28\\(1+c)/8&(1-d)/14\end{pmatrix}
       =-\frac{3(c+d)}{224}\ne0 .
\]

Using $xA_3+yB_3=xA_4+yB_4=1$, solving gives

\[
 R=U_0\eta+O(\eta^2),\qquad U=-H\eta+O(\eta^2).                 \tag{18}
\]

The unaveraged conjugate-pair inequalities imply

\[
 \left|\frac{\Im S}{8}\sin\theta_k+
          \frac{\Im P}{14}\sin2\theta_k-
          \frac{\Im P_3}{18}\sin6\theta_k\right|=O(\eta^2),
 \quad \theta_k=2\pi k/9,\quad k=3,4.                          \tag{19}
\]

The sine rows are invertible:
$\sin2\theta_3/\sin\theta_3=-1$ and
$\sin2\theta_4/\sin\theta_4=-2c$. Since $P_3=O(\eta^{3/2})$,

\[
 \Im S=O(\eta^{3/2}),\qquad \Im P=O(\eta^{3/2}).                \tag{20}
\]

This required no analytic critical-point labeling. Define bounded real
vectors and scalars

\[
\begin{gathered}
 h_j=\beta_j/\sqrt\eta,\quad u_j=\alpha_j/\eta,\quad
 J_3=\sum h_j^3,\quad J_4=\sum h_j^4,\quad
 J_{21}=\sum h_j^2u_j,\quad U_2=\sum u_j^2,\\
 W=(R-U_0\eta)/\eta^2,\quad D=(U+H\eta)/\eta^2,\quad
 V=\Im S/\eta^{3/2},\quad B=\Im P/\eta^{3/2}.
\end{gathered}                                                   \tag{21}
\]

They satisfy

\[
 \sum h_j=O(\eta),\quad \sum h_j^2=H+O(\eta),\quad
 \sum u_j=U_0+O(\eta),\quad B=2\sum h_ju_j .                    \tag{22}
\]

Also $\Im P_3=-\eta^{3/2}J_3+O(\eta^{5/2})$. Dividing (19) by
$\eta^{3/2}$ and solving gives

\[
 V=\frac47B+O(\sqrt\eta),\qquad
 B=-\frac{7(2c+1)}9J_3+O(\sqrt\eta).                            \tag{23}
\]

Here $\sin6\theta_3=0$, $\sin6\theta_4=-\sqrt3/2$, and
$\sqrt3/\sin(\pi/9)=2(4c^2-1)$. Every subsequential limit of $(h,u)$
therefore satisfies

\[
 \sum h_j=0,\quad \sum h_j^2=H,\quad
 \sum u_j=U_0,\quad \sum h_ju_j=LJ_3,\quad
 L=-\frac{7(2c+1)}{18}.                                      \tag{24}
\]

This is the necessary rate reduction for every competitor with bounded
above second-order surplus.

## 3. The fourth-order polynomial and radial cost

Write $\epsilon=\sqrt\eta$. Along a sequence satisfying (9), Newton
identities give the uniform coefficient expansion

\[
 p=z^9-1+\epsilon^2g_2+\epsilon^3g_3+\epsilon^4g_4+O(\epsilon^5),
                                                               \tag{25}
\]

even though the bounded quantities in (21) may vary with $\epsilon$.
Here

\[
\begin{aligned}
 g_2(z)&=9+9x(z^8-1)+9y(z^7-1),\\
 g_3(z)&=i\left[-\frac98V(z^8-1)-\frac9{14}B(z^7-1)
                                      +\frac12J_3(z^6-1)\right],\\
 g_4(z)&=-36-9U_0+\frac92H-\frac98W(z^8-1)
                 +\frac9{14}(U_0^2-D)(z^7-1)\\
 &\quad+\left(-\frac34U_0H+\frac32J_{21}\right)(z^6-1)
                 +\left(\frac9{40}H^2-\frac9{20}J_4\right)(z^5-1).
\end{aligned}                                                   \tag{26}
\]

Indeed $\Re P_3=-3\epsilon^4J_{21}+O(\epsilon^6)$,
$\Re P_4=\epsilon^4J_4+O(\epsilon^6)$, and their imaginary
errors after the displayed leading terms are $O(\epsilon^5)$.
Also $S^2=U_0^2\epsilon^4+O(\epsilon^5)$,
$SP=-U_0H\epsilon^4+O(\epsilon^5)$, and
$P^2=H^2\epsilon^4+O(\epsilon^5)$. Terms involving $e_m$,
$m\ge5$, are $O(\epsilon^5)$. Anchoring contributes
$-36-9U_0+9H/2$ in $g_4$. No expansion of each individual critical
point was assumed.

At a ninth root $\omega$, put

\[
 \delta_1=-\frac{g_2(\omega)}{9\omega^8},\quad
 \delta_{3/2}=-\frac{g_3(\omega)}{9\omega^8},\quad
 \delta_2=-\frac{g_4(\omega)+g_2'(\omega)\delta_1+
                           36\omega^7\delta_1^2}{9\omega^8}.
\]

Uniformly,
$r=\omega+\epsilon^2\delta_1+\epsilon^3\delta_{3/2}
+\epsilon^4\delta_2+O(\epsilon^5)$.
At the active pairs $k=3,4$, $\delta_1/\omega=iT_k$ with
$T_k=x\sin\theta_k+y\sin2\theta_k$.
Their half squared-modulus coefficient at $\epsilon^4$, averaged
across each conjugate pair, is

\[
 R_k=\mathcal T_k-\frac{A_kW}{8}-\frac{B_kD}{14},
 \qquad R_k\le O(\epsilon),                                  \tag{27}
\]

where

\[
\begin{aligned}
 \mathcal T_k={}&4+U_0-\frac H2+\frac{B_kU_0^2}{14}
 +(1-\cos6\theta_k)\left(-\frac{U_0H}{12}+\frac{J_{21}}6\right)\\
 &+(1-\cos5\theta_k)\left(\frac{H^2}{40}-\frac{J_4}{20}\right)
 +\mathcal K_k,\\
 \mathcal K_k={}&\frac92T_k^2-
             T_k(8x\sin\theta_k+7y\sin2\theta_k).
\end{aligned}                                                   \tag{28}
\]

The $\epsilon^3$ radial terms cancel in this average because $g_3$
is purely imaginary times a real polynomial. The curvature includes
both second-order displacement and $|\delta_1|^2/2$.
For exact arithmetic, writing
$r_k=\sin2\theta_k/\sin\theta_k$ and $s_k=\sin^2\theta_k$ gives

\[
 \mathcal K_k=-\left(\frac72x^2+6xyr_k+\frac52y^2r_k^2\right)s_k,
 \quad(r_3,s_3)=(-1,3/4),\quad(r_4,s_4)=(-2c,1-c^2).
                                                               \tag{29}
\]

The harmonic table is

| $k$ | $1-\cos6\theta_k$ | $1-\cos5\theta_k$ |
| --- | --- | --- |
| 3 | $0$ | $3/2$ |
| 4 | $3/2$ | $1-v$ |

By (16), (27) implies

\[
 W+\frac D2\ge w_3\mathcal T_3+w_4\mathcal T_4-o(1).            \tag{30}
\]

The inverse-distance expansion in the exact coordinates (21) gives

\[
 \frac{F_p(a)-8-C\eta}{\eta^2}
 =W+\frac D2+\frac{U_2}{2}+8+2U_0-\frac{3H}{2}
                         -\frac{3J_{21}}2+\frac{3J_4}{8}+o(1).
                                                               \tag{31}
\]

Before substituting moment deviations, its terms are
$8+\eta(8+\sum u-\tfrac12\sum h^2)
+\eta^2(8+2\sum u+U_2-\tfrac32\sum h^2-\tfrac32J_{21}
+\tfrac38J_4)+O(\eta^3)$.
The exact identities $\sum u=U_0+\eta W$ and
$\sum h^2=H+\eta(U_2-D)$ yield (31).

## 4. A sharp real-vector inequality and the finite optimization

For any real vector with $\sum h_j^2=H>0$, we claim

\[
 J_4\le\frac{H^2}{2}+\frac{J_3^2}{2H}.                        \tag{32}
\]

Normalize $H=1$ and put $t_j=h_j^2$, $\sum t_j=1$. If
$\sum t_j^2\le1/2$, the claim is immediate. Otherwise
$m=\max t_j>1/2$. The triangle inequality gives

\[
 |J_3|\ge m^{3/2}-(1-m)^{3/2}\ge2m-1,
\]

using $\sum_{j\ne j_{\max}}t_j^{3/2}\le(1-m)^{3/2}$.
For the second inequality set $a=\sqrt m$, $b=\sqrt{1-m}$.
Then $(a^3-b^3)/(a^2-b^2)=(1+ab)/(a+b)\ge1$, since
$(1+ab)^2-(a+b)^2=a^2b^2\ge0$.
Finally

\[
 2\sum t_j^2-1\le2(m^2+(1-m)^2)-1=(2m-1)^2\le J_3^2.
\]

This proves (32). Under balance $\sum h_j=0$, equality holds only
at a single opposed pair with squared coordinates $H/2$, all others
zero. Indeed $1/2<m<1$ makes the above ratio strictly greater than
1, and $m=1$ contradicts balance. In the other case, equality
requires $\sum t_j^2=1/2$, $J_3=0$, and $m\le1/2$. Thus
$\sum t_j(1/2-t_j)=0$, forcing two nonzero coordinates of equal
squared size; balance makes their signs opposite. These profiles
give equality.

Let $\mathcal T_k^0$ be (28) with $J_{21}=J_4=0$. By (30)-(31)
the surplus has a lower bound, up to $o(1)$, by

\[
 \mathcal B(h,u)=K_0+\frac{U_2}{2}+\rho J_{21}+\sigma J_4,       \tag{33}
\]

where

\[
\begin{gathered}
 K_0=8+2U_0-\frac{3H}{2}+w_3\mathcal T_3^0+w_4\mathcal T_4^0,\\
 \rho=-\frac32+\frac{w_4}{4}=\frac{c-5}{3},\qquad
 \sigma=\frac38-\frac{(3/2)w_3+(1-v)w_4}{20},\\
 \alpha=\sigma-\frac{\rho^2}{2},\quad
 \beta=\frac{(L+\rho)^2}{2},\quad
 K_1=K_0+\frac{(U_0+\rho H)^2}{16}.
\end{gathered}                                                   \tag{34}
\]

Take any subsequential limit of the bounded vectors in (21), so (24)
holds exactly. The constant vector and $h$ are orthogonal, with squared
norms $8,H$. Projecting $g=u+\rho h^2$ onto them gives

\[
 \mathcal B(h,u)=K_1+\alpha J_4+\beta\frac{J_3^2}{H}
 +\frac12\left\|u+\rho h^2-\frac{U_0+\rho H}{8}{\bf1}
                         -\frac{(L+\rho)J_3}{H}h\right\|^2 .
                                                               \tag{35}
\]

Here $h^2$ denotes coordinatewise squares. Exact cubic-field algebra gives

\[
\begin{aligned}
 \alpha&=-\frac{527}{360}+\frac{41}{90}c+\frac{13}{90}c^2<0,\\
 \beta&=\frac{1369}{648}+\frac{74}{81}c+\frac8{81}c^2,\qquad
 \beta+\alpha/2>0,\\
 K_1+\alpha H^2/2&=B_* .
\end{aligned}                                                   \tag{36}
\]

Using (32) in the direction supplied by $\alpha<0$ proves

\[
 \mathcal B(h,u)\ge B_*+
          (\beta+\alpha/2)\frac{J_3^2}{H}\ge B_* .              \tag{37}
\]

Equality requires $J_3=0$, $J_4=H^2/2$, and zero residual in (35).
Consequently $h$ is the opposed pair in (6). The unique minimizing
real correction is

\[
 u_j=\frac{U_0+\rho H}{8}
                 +\frac{(L+\rho)J_3}{H}h_j-\rho h_j^2,         \tag{38}
\]

giving (7) on that pair.

Every sequence with bounded above second-order surplus has this compact
subsequence reduction, and (30)-(37) bound each limiting surplus below
by $B_*$. An alleged sequence below $B_*-\varepsilon$ contradicts
(37); even if its surplus initially tends to negative infinity, (21)
and (31) first make it bounded. This proves the lower bound in (3).

For (5), equality holds at every convergent subsequence of $(h,u)$.
The only limits are the permutations in (6). Compactness and the finite
permutation set prove (6) for the full sequence. No effective stability
constant is claimed.

## 5. An explicit all-disk attaining family

The following construction works for every sufficiently small $\eta>0$.
Define $u_z,u_p$ by (7), and
$U_2^*=6u_z^2+2u_p^2$, $J_{21}^*=Hu_p$, $J_4^*=H^2/2$.
Insert these into (28) to obtain $\mathcal T_3^*,\mathcal T_4^*$.
Let $W_*,D_*$ solve the nonsingular equations

\[
 \frac{A_kW_*}{8}+\frac{B_kD_*}{14}=\mathcal T_k^*,\quad k=3,4,
 \qquad \gamma_*=\frac{U_2^*-D_*}{2H}.                         \tag{39}
\]

Their exact normal forms are

\[
\begin{aligned}
 u_z&=-37/36+(20/9)c-(20/9)c^2,\\
 u_p&=47/36-(92/9)c+(92/9)c^2,\\
 W_*&=2512/27+(5840/9)c-(21392/27)c^2,\\
 D_*&=-4270/27-(29492/27)c+(4012/3)c^2,\\
 \gamma_*&=13/36+(1253/72)c-(50/3)c^2 .
\end{aligned}                                                   \tag{40}
\]

Use the fixed inward repair $M=100$:

\[
\begin{gathered}
 A(\eta)=u_z\eta+(W_*/8)\eta^2+100\eta^3,\qquad
 B(\eta)=u_p\eta+(W_*/8)\eta^2+100\eta^3,\\
 q_\eta'(z)=9(z-A(\eta))^6
       \left((z-B(\eta))^2+\frac H2\eta(1+\gamma_*\eta)^2\right),
 \qquad q_\eta(z)=\int_{1-\eta}^z q_\eta'(w)\,dw .
\end{gathered}                                                   \tag{41}
\]

This is a monic degree-nine real polynomial, with six critical points
at $A(\eta)$ and one at each of
$B(\eta)\pm i\sqrt{H/2}\sqrt\eta(1+\gamma_*\eta)$.
Its coefficients are polynomials in $\eta$.

Here is the complete original-root containment argument. At $\eta=0$,
the roots are the nine simple roots of $z^9-1$, so each branch is
analytic in $\eta$ in a fixed neighborhood. The branch at 1 is
exactly $1-\eta$. For $k=1,2$ and their conjugates, the first half
squared-modulus coefficient is $-1+xA_k+yB_k<0$, as in the
sharp-slope theorem. At $k=3,4$, (39) makes the coefficient of
$\eta^2$ zero as well as that of $\eta$. From the defining factors,

\[
 \frac{|r_k(\eta)|^2-1}{2}=\mathcal R_k\eta^3+O(\eta^4),        \tag{42}
\]

where

\[
\begin{aligned}
 \mathcal R_3
    &=-5378807/10368-(19292351/10368)c+(345355/144)c^2<0,\\
 \mathcal R_4
    &=-3572867/186624+(4372007/10368)c-(1667129/2592)c^2<0 .
\end{aligned}                                                   \tag{43}
\]

These are exact field expressions. To reproduce them, write
$q_\eta=z^9-1+\eta p_1+\eta^2p_2+\eta^3p_3+O(\eta^4)$.
Its root displacements are

\[
\begin{aligned}
 t_1&=-p_1(\omega)/(9\omega^8),\\
 t_2&=-[p_2(\omega)+p_1'(\omega)t_1+36\omega^7t_1^2]/(9\omega^8),\\
 t_3&=-[p_3(\omega)+p_2'(\omega)t_1+p_1'(\omega)t_2+
       p_1''(\omega)t_1^2/2+72\omega^7t_1t_2+
       84\omega^6t_1^3]/(9\omega^8),\\
 \mathcal R_k&=\Re(t_3/\omega)+\Re(t_1\overline{t_2}).
\end{aligned}
\]

The checker multiplies and integrates (41) independently and verifies
these formulas, the vanishing coefficients, and both signs (43).
Real coefficients give identical moduli for the reflected branches
$k=6,5$. All nine branches have now been covered. Their strict negative
leading coefficients and Taylor remainders give one small interval of
positive $\eta$ on which every root is strictly inside the disk.

For small $\eta$, the exact critical distances give

\[
 F_{q_\eta}(1-\eta)=
 \frac6{1-\eta-A(\eta)}
 +\frac2{\sqrt{(1-\eta-B(\eta))^2+
                             (H/2)\eta(1+\gamma_*\eta)^2}} .
                                                               \tag{44}
\]

Its expansion is (4), by (31),(35),(39) or direct scalar expansion of
(44), which is separately checked. Since $B_*<0$, this also proves
the straight-line failure. The construction exists for every sufficiently
small $\eta$, proving the upper bound in (3).

## 6. Evidence and scope

The self-contained Python standard-library checker establishes the full
generic anchored polynomial through $\epsilon^4$ with seven independent
balanced imaginary coordinates and eight arbitrary coordinates in each
of the real second-order, imaginary third-order, and real fourth-order
corrections. Its generic derivative has 536 terms and its anchored
polynomial 1110 terms. A separate $K[\eta,z]$ implementation derives
the explicit factor construction, its active-root radial expansions,
and inverse-distance objective from their definitions. Active ninth
roots are evaluated in exact quadratic Gaussian extensions of the cubic
field. Rational bisection isolates $c\in(3/4,1)$ and proves every
strict sign; rounded decimals are not premises.

These are author finite-algebra checks. The concentration and bootstrap
inputs retain their prior attribution. The rate estimates, vector inequality,
compactness, root arguments and remainders are ordinary mathematical proofs,
not machine-checked analytic certificates. Independent review of this
extension is pending. No solver, numerical root search, enumeration or
private proof corpus is used.

The full first-power endpoint in the middle annulus, an effective boundary
radius, a quantitative stability constant, and the inequality at exact
quadratic coefficient $B_*$ remain outside this result. The ordinary
Sendov assertion and quadratic Tang--Zhang theorem are prior literature.
