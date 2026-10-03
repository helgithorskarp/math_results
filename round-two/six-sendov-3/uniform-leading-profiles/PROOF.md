# Uniform realization of every optimal leading critical profile

Actual author **six-sendov-3**, role **researcher**, 2026-10-03.
Complete ordinary author proof, **UNFORMALIZED and independently UNREVIEWED**.
The exact calculations below corroborate finite identities; they do not
formalize the analytic implicit-function or compactness arguments.

## Statement, novelty and credited inputs

For a monic degree-nine polynomial with a marked root $a=1-\eta$, put
$F_p(a)=\sum_{j=1}^8|a-\zeta_j|^{-1}$, with all eight critical points
counted with multiplicity. Set

\[
\begin{gathered}
c=\cos(\pi/9),\quad d=2c^2-1,\quad e=2d^2-1,\quad
y=\frac1{3(1+c)},\quad x=\frac23-y,\\
H=14y,\quad U_0=-8x,\quad C=\frac83+y,\quad
k=-\frac{7(1+2c)}{18},\quad\rho=\frac{c-5}{3},\quad\ell=k+\rho,\\
\alpha=-\frac{527}{360}+\frac{41}{90}c+\frac{13}{90}c^2,
\qquad\tau=\frac{\ell^2}{2},\\
B_*=\frac{2311}{108}+\frac{4934}{27}c-\frac{1976}{9}c^2,
\qquad K_1=B_*-\frac{\alpha H^2}{2}.
\end{gathered}                                                    \tag{1}
\]

Let $\mathcal S=\{v\in\mathbb R^8:\sum v_j=0,\ \sum v_j^2=H\}$.
For $v\in\mathcal S$, define $J_3(v)=\sum v_j^3$, $J_4(v)=\sum v_j^4$ and

\[
\begin{split}
u_j(v)&=\frac{U_0+\rho H}{8}+\frac{\ell J_3(v)}H v_j-\rho v_j^2,\\
\mathcal K(v)&=K_1+\alpha J_4(v)+\frac{\tau J_3(v)^2}H .
\end{split}                                                       \tag{2}
\]

**Uniform realization theorem.** There are numbers $\eta_0>0$ and
$L<\infty$, independent of $v\in\mathcal S$, and an actual monic
degree-nine family $p_{v,\eta}$ for EVERY $v\in\mathcal S$ and
EVERY $0<\eta<\eta_0$, such that:

* all nine original roots are simple and strictly inside the unit disk;
  one is exactly $a=1-\eta$;
* all eight critical points count with multiplicity, and, uniformly in $v$,
  $\Im\zeta_j/\sqrt\eta=v_j+O(\eta)$ and
  $\Re\zeta_j/\eta=u_j(v)+O(\eta)$;
* the FIRST-power objective satisfies
  \[
  \left|F_{p_{v,\eta}}(1-\eta)-8-C\eta-\mathcal K(v)\eta^2\right|
       \le L\eta^3,                                             \tag{3}
  \]
  and, after decreasing the SAME common $\eta_0$ if necessary,
  \[
  F_{p_{v,\eta}}(1-\eta)\le8+C\eta+10\eta^2.                    \tag{4}
  \]

**Profile sharpness corollary, relative to the credited rate theorem.**
For ANY sequence of actual degree-nine closed-disk-root polynomials with
$\eta_n\downarrow0$, $F_{p_n}(1-\eta_n)\le8+C\eta_n+D\eta_n^2$
for one finite $D$, and ordered imaginary profiles
$\Im\zeta_{n,j}/\sqrt{\eta_n}\to v_j\in\mathcal S$, one has
\[
\liminf_n\frac{F_{p_n}(1-\eta_n)-8-C\eta_n}{\eta_n^2}
       \ge\mathcal K(v).                                       \tag{5}
\]
The new uniform family attains equality in the limit for each profile.
The attained profile costs have the exact maximum
\[
\mathcal K_{\max}=K_1+(43\alpha/56+9\tau/14)H^2,\qquad
9<\mathcal K_{\max}<10,
\]
only at permutations and overall sign reversals of
$\sqrt{H/56}(7,-1,-1,-1,-1,-1,-1,-1)$. This maximizes the least attainable
cost per profile; it is not an upper bound on all disk-root polynomials.
The expression (2), its minimizing real correction, and this lower-rate
mechanism are credited to8619/8684. The new conclusion is simultaneous
actual attainment for the entire sphere on ONE common collar and under
ONE common second-order budget, including collisions and nonconjugate
profiles. It is not a claim of a new formula for the old finite cost.

Prior8530, independently confirmed by8608, realized this entire sphere
with a common $O(\eta^{3/2})$ inward repair. Prior8619/8684 gave generic
fourth jets and the finite optimization, but its attaining family was
the opposed-pair profile. Prior8921/8955 supplied an exact analytic
constraint chart around that special profile. Prior10006 supplied one
asymmetric1+7 actual family and original-motion obstruction. These
results and ordinary implicit-function methods are credited. Here a
four-control chart works uniformly on the full balanced sphere. The
construction is self-contained; ONLY (5) uses the reviewed lower-rate
reduction from8619/8684. No global first-power inequality, explicit
numerical collar, optimal uniform upper constant10, or new verdict on
any preceding claim is asserted.

## The full actual polynomial and its fourth jet

Write $t=\sqrt\eta$ and $q_j=u_j+x$. Introduce four REAL controls
$M,b,G,\sigma$ and the full, untruncated critical points

\[
\zeta_j(t)=itv_j+t^2(u_j+\sigma v_j)
                   +it^3(G+bv_j)+t^4M,\qquad
p(z)=9\int_{1-t^2}^z\prod_{j=1}^8(w-\zeta_j(t))\,dw.             \tag{6}
\]

Thus $p$ is actually monic of degree nine, anchored at the marked root,
and its derivative contains ALL eight factors exactly. There is no
unproved passage from an abstract critical tuple to an original-root
polynomial. The controls will become analytic functions of $t$ and $v$.
All finite expansions in this section hold before that substitution.

Balance gives $\sum q_j=0$, $\sum v_jq_j=kJ_3$. Set

\[
\begin{split}
Q_2&=\rho^2(J_4-H^2/8)+(k^2-\rho^2)J_3^2/H,\\
U_2(\sigma)&=8x^2+Q_2+2\sigma kJ_3+\sigma^2H,\\
J_{21}(\sigma)&=-xH-\rho(J_4-H^2/8)+\ell J_3^2/H+\sigma J_3,\\
D&=U_2(\sigma)-2bH,\quad B=2(kJ_3+\sigma H),\quad V=8G,\quad W=8M.
\end{split}                                                       \tag{7}
\]
These are respectively the actual real-correction squared norm and
mixed moment. Directly summing the powers of (6) gives

\[
\begin{aligned}
P_1&=U_0t^2+iVt^3+Wt^4,\\
P_2&=-Ht^2+iBt^3+Dt^4+O(t^5),\\
P_3&=-iJ_3t^3-3J_{21}(\sigma)t^4+O(t^5),\\
P_4&=J_4t^4+O(t^5).
\end{aligned}                                                      \tag{8}
\]
Newton identities and integration from $1-t^2$ now give the ENTIRE
polynomial coefficient map through fourth order:

\[
p(z)=z^9-1+t^2g_2(z)+t^3g_3(z)+t^4g_4(z)+O(t^5),                \tag{9}
\]
where

\[
\begin{aligned}
g_2&=9+9x(z^8-1)+9y(z^7-1),\\
g_3&=i[-9G(z^8-1)-(9/7)(kJ_3+\sigma H)(z^7-1)
                                      +(J_3/2)(z^6-1)],\\
g_4&=-36-9U_0+9H/2-9M(z^8-1)+(9/14)(U_0^2-D)(z^7-1)\\
&\quad+[-3U_0H/4+3J_{21}(\sigma)/2](z^6-1)
                          +[9H^2/40-9J_4/20](z^5-1).
\end{aligned}                                                      \tag{10}
\]
The finite checker replays the prior33-variable full eight-factor
calculation, with536 derivative terms and1110 anchored terms and
identical whole-map hashes. It then derives (7)--(10) in a separate
seven-variable moment layer, comparing every coefficient. This replay
is validation, not new research. The formal moment substitutions are
just summation of $1,v,v^2,v^3,v^4$ over eight coordinates; no sampled
profile or assumed moment realizability is used in the universal proof.

## All nine original branches and four control equations

Let $\omega_k=\exp(2\pi ik/9)$. At $t=0$, (6) is $z^9-1$, for every
profile and every bounded control. Its nine roots are simple. The
analytic root theorem supplies branches $r_k(t;v,M,b,G,\sigma)$ near
$\omega_k$. On compact sets of profiles and controls the same nine
disjoint neighborhoods and a common small interval work. Their jets are

\[
\begin{aligned}
r_k&=\omega_k+t^2L_k+t^3T_k+t^4Z_k+O(t^5),\\
L_k&=-g_2(\omega_k)/(9\omega_k^8),\quad
T_k=-g_3(\omega_k)/(9\omega_k^8),\\
Z_k&=-[g_4(\omega_k)+g_2'(\omega_k)L_k
                          +36\omega_k^7L_k^2]/(9\omega_k^8).
\end{aligned}                                                      \tag{11}
\]
Put $n_k=(|r_k|^2-1)/2$, $\theta_k=2\pi k/9$. The FULL individual
second and third half-normal coefficients are

\[
\begin{split}
[t^2]n_k&=-2y(\cos\theta_k+1/2)(\cos\theta_k+c),\\
[t^3]n_k&=G\sin\theta_k+\frac{kJ_3+\sigma H}{7}\sin2\theta_k
                                     -\frac{J_3}{18}\sin3\theta_k.
\end{split}                                                       \tag{12}
\]
Here $k$ in the fraction is the CONSTANT in (1); branch indices are
subscripts. The active indices are3,4,5,6. For $G_0=kJ_3/7$, $\sigma_0=0$,
all FOUR individual cubic normals vanish exactly. For branch3 use
$\sin2\theta_3=-\sin\theta_3$, $\sin3\theta_3=0$; for branch4 use
$\sin2\theta_4=-2c\sin\theta_4$ and
$\sin3\theta_4=(4c^2-1)\sin\theta_4$. Reflected branches have opposite
odd normals. The other FIVE second coefficients are strictly negative,
including the anchored branch0, whose coefficient is $-1$.

For $j=3,4$ define $A_j=1-\cos\theta_j$, $B_j=1-\cos2\theta_j$:

\[
(A_3,B_3)=(3/2,3/2),\qquad(A_4,B_4)=(1+c,1-d).
\]
Let $U_2=U_2(0)$, $J_{21}=J_{21}(0)$ and define

\[
\begin{split}
\mathcal T_j={}&4+U_0-H/2+B_jU_0^2/14
 +(1-\cos6\theta_j)(-U_0H/12+J_{21}/6)\\
&+(1-\cos5\theta_j)(H^2/40-J_4/20)+\mathcal C_j,\\
\mathcal C_j={}&-(7x^2/2+6xy r_j+5y^2r_j^2/2)s_j,\\
(r_3,s_3)&=(-1,3/4),\qquad(r_4,s_4)=(-2c,1-c^2),\\
R_j&=\mathcal T_j-B_jU_2/14.
\end{split}                                                       \tag{13}
\]
The symbols $r_j,s_j$ in (13) are fixed trigonometric ratios, not the
original-root branches. Formula (11), including BOTH its nonlinear
root term and modulus curvature $|L_j|^2/2$, yields

\[
[t^4]n_j=R_j-A_jM+(HB_j/7)b,\qquad\sigma=0.                    \tag{14}
\]
The same fourth coefficient holds at the reflected index. Choose
$(M_0(v),b_0(v))$ to solve these two expressions equal to zero. The
matrix with rows $(-A_j,HB_j/7)$ has determinant
$D_E=3H(c+d)/14>0$. Explicitly

\[
M_0=\frac{H(B_3R_4-B_4R_3)}{7D_E},\qquad
b_0=\frac{A_3R_4-A_4R_3}{D_E}.                                \tag{15}
\]
Thus these controls are continuous bounded polynomial functions of
$J_4$ and $J_3^2$ on the entire sphere. No division by $J_3$, a
coordinate gap, or a separation parameter occurs.

We now use the FULL polynomial (6), not its truncated jet. For $j=3,4$
form the desingularized REAL analytic functions

\[
E_j=\frac{n_j+n_{9-j}}{2t^4},\qquad
O_j=\frac{n_j-n_{9-j}}{2t^3}.                                  \tag{16}
\]
Their extensions at $t=0$ exist for all controls near the starting
graph. The first normal is zero; both second normals vanish; the
third normals have opposite signs. Moreover for fixed real controls
$p(-t,z)=\overline{p(t,\overline z)}$, so
$n_{9-j}(-t)=n_j(t)$. Consequently the two numerators have precisely
the required divisibility and $E_j,O_j$ are EVEN analytic functions
of $t$. At $t=0$, $O_j$ is the third expression in (12), and $E_j$ is
the fourth expression with $U_2(\sigma),J_{21}(\sigma)$ in (13).

At $(G,\sigma,M,b)=(G_0,0,M_0,b_0)$ solve

\[
O_3=O_4=0,\qquad E_3=E_4=-t^2.                                \tag{17}
\]
Order the rows as $(O_3,O_4,E_3,E_4)$ and columns as $(G,\sigma,M,b)$.
At $t=0$ the Jacobian is block triangular. Its odd block has rows
$(\sin\theta_j,(H/7)\sin2\theta_j)$ and determinant

\[
D_O=\frac H7\sin\theta_3\sin\theta_4(1-2c)\ne0.                \tag{18}
\]
Its even block is exactly the matrix in (14), with determinant $D_E$.
The upper right block is zero because $M,b$ first enter the fourth
jet. Both nonzero determinants are INDEPENDENT of the profile.
The lower left block may depend on the profile and need not vanish.

The parameterized real analytic implicit-function theorem therefore
gives solutions $G,\sigma,M,b$ near their starting values. For the
uniform assertion, the starting graph over $\mathcal S$ is compact,
all its coefficients and derivatives are continuous, and the inverse
Jacobian norms are bounded. Choose a finite cover of local profile
charts, and shrink their neighborhoods to a common tube and time
interval. Local uniqueness in that tube identifies the solutions on
overlaps. Equivalently, the standard uniform implicit-function proof
uses the bounded inverses and a common derivative-continuity modulus
on this compact graph. This supplies ONE positive interval and bounded
analytic controls for ALL profiles. No distinctness of the $v_j$ is
needed. Because (17) is even in $t$ and the solution is unique in the
tube, its four controls are even too. Uniformly,

\[
G=G_0+O(t^2),\quad\sigma=O(t^2),\quad
M=M_0+O(t^2),\quad b=b_0+O(t^2).                              \tag{19}
\]

For $t>0$, (16)--(17) give EXACTLY $n_3=n_4=n_5=n_6=-t^6<0$.
At the other five branches, the strictly negative second coefficients
in (12) and uniform Taylor bounds give $n_j<0$ on a smaller common
interval. The branch0 is exactly $1-t^2$ by anchoring and uniqueness.
All nine disjoint simple branches are strictly inside the disk. This
closes actual original-root feasibility for every profile, with critical
collisions allowed. The interval remains existential; neither finite
jet algebra nor compactness here certifies an explicit numerical width.

## The attained profile cost and one common second-order budget

The first-power binomial expansion of the ACTUAL squared critical
distances in (6), through $t^4$ and before closing, gives

\[
F=8+Ct^2+
[8M-bH+8+2U_0+U_2(\sigma)-3H/2-3J_{21}(\sigma)/2+3J_4/8]t^4
     +O(t^6).                                                  \tag{20}
\]
The remainder is even for fixed controls. After substituting (19),
the coefficient of $t^2$ is still exactly $C$ for ALL controls, so
changes in the controls contribute only $O(t^6)$ to (20).
Set $w_4=1/(c+d)$, $w_3=(2/3)(7-(1-d)w_4)$. They satisfy
$\sum w_jA_j=8$, $\sum w_jB_j=7$. Equations (13)--(15) therefore
give $8M_0+(U_2-2b_0H)/2=\sum w_j\mathcal T_j$. Substitution into
(20), or the entire exact objective map in maps.py, gives exactly
$\mathcal K(v)$ in (2). The identity is the known projection formula
from8619, now attained at every profile by the new actual chart.

The four controls, coefficients and critical distances are analytic
near the compact starting graph, and the distances there are1. Shrink
the common interval so every distance is at least1/2. Uniform analytic
Taylor bounds then give one finite $L$ in (3). This also proves the
critical asymptotics in the statement from (6),(19).

To obtain the sharp common profile maximum, first recall and prove the
classical finite-population skewness bound
\[
J_3^2\le\frac9{14}H^3.                                       \tag{21}
\]
The real sphere $\mathcal S$ is compact. At a maximum or minimum of
$J_3$, Lagrange multipliers apply because the two constraint gradients
$\mathbf1,v$ are independent ($H>0$ and balance). Thus
$3v_j^2=A+Bv_j$ for all coordinates; there are at most two distinct
values. There cannot be only one, since balance would force $H=0$.
If one value occurs $r$ times, $1\le r\le7$, the other is
$-r/(8-r)$ times it. Direct balance/norm/cube summation gives
\[
\frac{J_3^2}{H^3}=\frac{(8-2r)^2}{8r(8-r)}.
\]
The complete seven-count table is $9/14,1/6,1/30,0,1/30,1/6,9/14$.
This proves (21) and its equality characterization: exactly the1+7
profiles and their permutations/signs. The skewness bound and ordinary
Lagrange method are credited classical facts, not declared new research.
The checker verifies all seven counts by two direct rational formulas.

The exact centered-square identity, also checked as a WHOLE map, is
\[
D(v):=J_4-H^2/8-J_3^2/H
 =\sum_j(v_j^2-H/8-(J_3/H)v_j)^2\ge0.                        \tag{22}
\]
Since $\alpha<0$ and $\alpha+\tau>0$, the attained cost satisfies the
exact nonnegative-defect identity
\[
\mathcal K_{\max}-\mathcal K(v)
 =(\alpha+\tau)(9H^2/14-J_3^2/H)-\alpha D(v).                 \tag{23}
\]
Equality in (23) forces equality in (21), hence the1+7 profiles; those
profiles also have $D(v)=0$ and attain equality. Rational isolation of
$c$ in the physical embedding gives $9<\mathcal K_{\max}<10$ exactly.
The1+7 specialization also reproduces the coefficient of10006 after
subtracting its strict fourth-order repair cost
$(w_3+w_4)/[12(1+c)]^2$. This is a credited baseline check, not a
claim that the former repaired coefficient is optimal.

Thus EVERY attained profile cost is bounded above by the SAME constant
$\mathcal K_{\max}<10$. Its strict gap to10 and the common remainder
$L$ in (3) allow one shrinkage of $\eta_0$, proving (4).10 is a convenient
upper budget; the exact maximum concerns the coefficient function (2),
not an optimal finite-collar budget or a numerical collar width.

Finally, for (5), the credited8619 rate reduction, independently
confirmed by8684, gives bounded real corrections and the limiting
constraints $\sum u=U_0$, $\sum v_ju_j=kJ_3$. Its complete fourth
normal lower estimate is

\[
\mathcal K(v)+\frac12\left\|u+\rho v^2-
\frac{U_0+\rho H}{8}{\bf1}-\frac{\ell J_3}{H}v\right\|^2,
                                                                  \tag{24}
\]
up to $o(1)$ along convergent subsequences. For any subsequence attaining
the liminf, bounded corrections have a further convergent subsequence.
Moment continuity and the nonnegative squared term give (5). The old
rate proof also bounds the surplus below, excluding negative-infinite
escape. Our controls select exactly the zero-residual correction (2),
and (3) attains the credited lower expression for each fixed profile.
This is the sole part of the proof dependent on that prior rate theorem.

## Reproduction and limits

maps.py checks the ENTIRE33-variable literal baseline, seven-variable
moment maps, all nine root substitutions, all individual normals,
both Jacobian blocks, complete closing maps and full FIRST-power
objective, over $\mathbb Q[\omega,i]/(\omega^6+\omega^3+1,i^2+1)$.
It verifies conjugate reversal at all nine branches. No root search,
floating-point premise, solver or incomplete enumeration is involved.
verify.py compares the entire typed record and rejects mathematical
damage before fixture comparison; validate.py covers normal/optimized
and isolated source-only execution plus external record/source damage.

The analytic theorems, uniform patching, original containment, remainder
and imported lower-rate reduction are ordinary written arguments, not
machine-checked certificates. Review of8619 or8921 does not review this
new whole-sphere chart. This theorem proves an asymptotic actual
realization and profile classification; it does not prove the global
degree-nine first-power endpoint or an explicit all-eta collar.
