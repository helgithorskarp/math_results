# Quantitative boundary profiles and the next critical scale

Actual author **six-sendov-3**, role **researcher**, 2026-10-01.
Complete ordinary author proof; independent review of this extension is
pending. Constants below are existential, not effective numerical bounds.

## 1. Exact scope

Let $p$ have degree nine, all original roots in the closed unit disk,
and marked root $a$. Define $F_p(a)=\sum_{j=1}^8|a-\zeta_j|^{-1}$,
counting critical multiplicity; a zero denominator means infinity.
Rotate and normalize so $p$ is monic and $a=1-\eta>0$. Put

\[
\begin{gathered}
c=\cos(\pi/9),\quad d=2c^2-1,\quad v=2d^2-1,\quad
y=\frac1{3(1+c)},\quad x=\frac23-y,\quad H=14y,\quad U_0=-8x,\\
C=\frac83+y,\quad
B_*=\frac{2311}{108}+\frac{4934}{27}c-\frac{1976}{9}c^2,\quad
\rho=(c-5)/3,\\
u_z=(U_0+\rho H)/8,\quad u_p=u_z-\rho H/2,\quad b=\sqrt{H/2}.
\end{gathered}                                                    \tag{1}
\]

Let $\mathcal M$ be the finite set of simultaneous permutations of

\[
h^*=(b,-b,0,\ldots,0),\qquad
u^*=(u_p,u_p,u_z,\ldots,u_z).
\]

For $h_j=\Im\zeta_j/\sqrt\eta$, $u_j=\Re\zeta_j/\eta$, set

\[
\mathcal D_\eta(p)^2
=\min_{(h^*,u^*)\in\mathcal M}
           \big(\|h-h^*\|^2+\|u-u^*\|^2\big),\qquad
E_\eta(p)=\frac{F_p(a)-8-C\eta-B_*\eta^2}{\eta^2}.              \tag{2}
\]

**Quantitative profile theorem.** There is a universal $\kappa>0$.
For every fixed $M\ge0$, there are $K_M>0$ and $\eta_M>0$ such that
every such polynomial with $0<\eta<\eta_M$ and

\[
F_p(a)\le8+C\eta+M\eta^2                                     \tag{3}
\]

satisfies

\[
E_\eta(p)\ge\kappa\mathcal D_\eta(p)^2-K_M\eta.                \tag{4}
\]

The coefficient $\kappa$ is not claimed sharp. The squared-distance power
in (4) is optimal, as proved by actual disk-root families below.

**Uniform cubic-order remainder for the boundary minimum.** There are
$K,\eta_0>0$ such that for every degree-nine disk-root polynomial,

\[
F_p(a)\ge8+C\eta+B_*\eta^2-K\eta^3,\qquad 0<\eta<\eta_0.       \tag{5}
\]

Consequently, writing the infimum over all marked roots of modulus $r$,

\[
\inf_{p,a:\ |a|=r}F_p(a)
=8+C(1-r)+B_*(1-r)^2+O((1-r)^3).                            \tag{6}
\]

**The next critical scale.** For every fixed finite $T$, a family with
$F_p(a)\le8+C\eta+B_*\eta^2+T\eta^3$ has
$\mathcal D_\eta(p)=O(\sqrt\eta)$. After a suitable permutation,

\[
\begin{array}{ll}
j=1,2:&
\Im\zeta_j=\pm b\sqrt\eta+O(\eta),\quad
\Re\zeta_j=u_p\eta+O(\eta^{3/2}),\\
j=3,\ldots,8:&
\Im\zeta_j=O(\eta),\quad
\Re\zeta_j=u_z\eta+O(\eta^{3/2}).
\end{array}                                                   \tag{7}
\]

An explicit family has $\mathcal D_\eta(p)\asymp\sqrt\eta$ while obeying
such a fixed third-order budget. Thus this profile rate and the order
$\eta$ of the six small imaginary coordinates cannot be improved in general.
No optimal third-order boundary coefficient is established.

The substantive dependency is the
[sharp second-order theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/quartic-boundary/PROOF.md),
graph lemma8619,
bafkreicgkxmkaequm4yqqzg2tb7rjna6a245ipqejfri6nwiwjgwcwhrqy,
source f8df996dba7bfec1d05eb6731b3b8e667ca8f860.
Its first-order constants, moment cost and attaining family retain credit.
Its inherited concentration and bootstrap are the reviewed inputs7190;
the first-order theorem8530 has independent review8608. None of those
reviews audits this new extension.

## 2. Uniform bounds and a sharper pair-averaged remainder

For any fixed $M$ in (3), Section2 of the second-order proof gives uniformly

\[
\begin{gathered}
Q=\sum|\zeta_j|^2=O(\eta),\quad S=\sum\zeta_j=O(\eta),\quad
X=\sum(\Re\zeta_j)^2=O(\eta^2),\\
R=\Re S=U_0\eta+O(\eta^2),\quad
U=\Re P=-H\eta+O(\eta^2),\quad P=\sum\zeta_j^2,\\
\Im S,\Im P=O(\eta^{3/2}).
\end{gathered}                                                   \tag{8}
\]

Here and below the $O$ constants may depend on $M$, while all profiles
and correction moments remain bounded. To make this uniform rather than
merely sequential: reviewed concentration under a fixed mean slope less
than $1/2$ places every polynomial in (3) in one common neighborhood
of $z^9-1$ for sufficiently small $\eta$; otherwise a violating
sequence contradicts concentration. Reviewed local positive-$Q$
coercivity gives a common $Q/\eta$ bound. The coefficient bootstrap and
the fixed-root Taylor estimates then have uniform constants in that
neighborhood. The estimate
$F-8-C\eta\ge X/4-K\eta^2$ and the two invertible active rows give
the remaining bounds (8), with common constants. Thus no compactness
assumption about smooth critical branches is being added.

Use the exact coordinates $h,u$ of (2) and define

\[
\begin{gathered}
J_3=\sum h_j^3,\quad J_4=\sum h_j^4,\quad
J_{21}=\sum h_j^2u_j,\quad U_2=\sum u_j^2,\\
W=(R-U_0\eta)/\eta^2,\quad D=(U+H\eta)/\eta^2,\quad
V=\Im S/\eta^{3/2},\quad B=\Im P/\eta^{3/2}.
\end{gathered}
\]

All are bounded, and

\[
\sum h=O(\eta),\quad \sum h^2=H+\eta(U_2-D),\quad
\sum u=U_0+\eta W,\quad
h\mathbin{\cdot}u=LJ_3+O(\sqrt\eta),\quad
L=-7(2c+1)/18.                                               \tag{9}
\]

The last estimate comes from both unaveraged active disk-root pairs,
as in the second-order proof, and is needed in its stated rate.

Write $p=\mathsf R+i\mathsf I$, where both polynomials have real
coefficients. A stronger coefficient expansion than the combined
$O(\eta^{5/2})$ remainder is

\[
\mathsf R=z^9-1+\eta g_2+\eta^2g_4+O_{\rm coeff}(\eta^3),
\qquad \|\mathsf I\|_{\rm coeff}=O(\eta^{3/2}),                 \tag{10}
\]

with

\[
\begin{aligned}
g_2&=9+9x(z^8-1)+9y(z^7-1),\\
g_4&=-36-9U_0+9H/2-(9W/8)(z^8-1)
 +(9/14)(U_0^2-D)(z^7-1)\\
&\quad+(-3U_0H/4+3J_{21}/2)(z^6-1)
 +(9H^2/40-9J_4/20)(z^5-1).
\end{aligned}                                                   \tag{11}
\]

Here is the real-part improvement. Each critical point is exactly
$\eta u_j+i\sqrt\eta h_j$, with bounded real $h,u$. Products with
an even number of imaginary factors contribute only integer powers
of $\eta$ to real coefficients. For example
$\Re S^2=U_0^2\eta^2+O(\eta^3)$,
$\Re(SP)=-U_0H\eta^2+O(\eta^3)$,
$\Re P_3=-3\eta^2J_{21}+O(\eta^3)$ and
$\Re P_4=\eta^2J_4+O(\eta^3)$.
For $e_m$, $m\ge5$, every real monomial has order at least $\eta^3$.
Newton identities and anchoring at real $a$ give (10)-(11).
The imaginary sum is $\sqrt\eta\sum h=O(\eta^{3/2})$;
all other imaginary derivative coefficients start at this order or later.
The bounds hold for moving bounded parameters. Parity is not an
assumption that the family $p_\eta$ is analytic in $\sqrt\eta$.

Now fix an active ninth root $\omega$, with conjugate $\bar\omega$.
The simple-root map in a fixed coefficient neighborhood gives roots
$\Phi_\omega(\mathsf R,\mathsf I)$ and

\[
\Phi_{\bar\omega}(\mathsf R,\mathsf I)
  =\overline{\Phi_\omega(\mathsf R,-\mathsf I)}.
\]

Consequently the averaged half squared-modulus

\[
\mathcal A_\omega(\mathsf R,\mathsf I)
=\frac{|\Phi_\omega(\mathsf R,\mathsf I)|^2+
       |\Phi_{\bar\omega}(\mathsf R,\mathsf I)|^2-2}{4}
\]

is even in the real coefficient vector $\mathsf I$. Uniform second
derivative bounds for this root map imply

\[
\mathcal A_\omega(\mathsf R,\mathsf I)
=\frac{|\Phi_\omega(\mathsf R,0)|^2-1}{2}
                      +O(\|\mathsf I\|_{\rm coeff}^2)
=\frac{|\Phi_\omega(\mathsf R,0)|^2-1}{2}+O(\eta^3).           \tag{12}
\]

This argument uses no disk containment for the real polynomial
$\mathsf R$; containment is applied only to the actual roots of $p$.
It also treats arbitrary complex competitors, without reflection symmetry.

At $\theta_k=2\pi k/9$, $k=3,4$, put
$A_k=1-\cos\theta_k$, $B_k=1-\cos2\theta_k$. From (10)-(12),
the same root curvature calculation as the second-order proof gives

\[
\mathcal A_k=\eta^2\left(\mathcal T_k-\frac{A_kW}{8}
                                    -\frac{B_kD}{14}\right)+O(\eta^3),
\]

where

\[
\begin{aligned}
\mathcal T_k={}&4+U_0-H/2+B_kU_0^2/14
 +(1-\cos6\theta_k)(-U_0H/12+J_{21}/6)\\
&+(1-\cos5\theta_k)(H^2/40-J_4/20)+\mathcal K_k,\\
\mathcal K_k={}&-(7x^2/2+6xyq_k+5y^2q_k^2/2)s_k,\\
(q_3,s_3)&=(-1,3/4),\qquad(q_4,s_4)=(-2c,1-c^2).
\end{aligned}                                                   \tag{13}
\]

Since $\mathcal A_k\le0$, the positive dual weights
$w_4=1/(c+d)$, $w_3=(2/3)(7-(1-d)/(c+d))$ give

\[
W+D/2\ge w_3\mathcal T_3+w_4\mathcal T_4-O(\eta).              \tag{14}
\]

The scalar formula
$|a-\zeta_j|^2=(1-\eta(1+u_j))^2+\eta h_j^2$
has a uniform integer-power expansion. It yields

\[
\frac{F-8-C\eta}{\eta^2}
=W+D/2+U_2/2+8+2U_0-3H/2-3J_{21}/2+3J_4/8+O(\eta).
\]

Combining with (14), define

\[
\mathcal B(h,u)=K_0+U_2/2+\rho J_{21}+\sigma J_4,\quad
\sigma=3/8-((3/2)w_3+(1-v)w_4)/20,                           \tag{15}
\]

where $K_0=8+2U_0-3H/2+\sum w_k\mathcal T_k^0$ and
$\mathcal T_k^0$ is (13) with $J_{21}=J_4=0$. We obtain the
uniform estimate

\[
E_\eta(p)\ge\mathcal B(h,u)-B_*-K_M\eta.                       \tag{16}
\]

## 3. Quantitative coercivity of the limiting profile cost

On the balanced sphere $\sum h=0$, $\|h\|^2=H$, the credited cost has

\[
\alpha=\sigma-\rho^2/2=-527/360+(41/90)c+(13/90)c^2<0,\quad
\beta=(L+\rho)^2/2=1369/648+(74/81)c+(8/81)c^2 .
\]

Put $\mu=\beta+\alpha/2>0$ and

\[
G(h)=\alpha(J_4-H^2/2)+\beta J_3^2/H.                        \tag{17}
\]

The prior inequality $J_4\le H^2/2+J_3^2/(2H)$ gives
$G\ge\mu J_3^2/H\ge0$, with $G=0$ exactly at permutations of $h^*$.
We prove a global squared-distance gap

\[
G(h)\ge k_h\,\operatorname{dist}(h,\{h^*\})^2                 \tag{18}
\]

for one $k_h>0$ on the balanced sphere.
Near $(b,-b,0,\ldots,0)$, take six small coordinates $t$, put
$S_t=\sum t_j$, $T_t=\sum t_j^2$, and use the exact chart

\[
s=-S_t/2,\quad q=\sqrt{b^2-T_t/2-S_t^2/4},\quad
h=(s+q,s-q,t_1,\ldots,t_6).
\]

The positive square root enforces balance and norm and covers a
neighborhood. Direct expansion gives

\[
J_3=3Hs+O(\|t\|^3),\quad J_4=H^2/2+H(4s^2-T_t)+O(\|t\|^4),
\]

and therefore

\[
G(h)=H[-\alpha T_t+(9\beta+4\alpha)s^2]+O(\|t\|^4).           \tag{19}
\]

Exact field arithmetic gives $9\beta+4\alpha>0$, so the quadratic
form is positive definite in all six variables. Chart distance is
comparable to $\|t\|$, proving (18) locally. Permutations cover all
finitely many minima. On their compact complement, $G$ has a strictly
positive minimum and distance is bounded. This proves (18) globally.

Normalize the approximate constraints of actual profiles:

\[
\widehat h=\sqrt{\frac H{\|h-\bar h{\bf1}\|^2}}(h-\bar h{\bf1}),
\quad \bar h=\frac18\sum h,\qquad
\widehat u=u+\frac{U_0-\sum u}{8}{\bf1}.
\]

Equations (8)-(9) give
$\|\widehat h-h\|+\|\widehat u-u\|=O(\eta)$.
The denominator stays positive, and
$\sum\widehat h=0$, $\|\widehat h\|^2=H$, $\sum\widehat u=U_0$.
Replacing $(h,u)$ by $(\widehat h,\widehat u)$ in the bounded polynomial
$\mathcal B$ costs $O(\eta)$. Also

\[
\delta=\widehat h\mathbin{\cdot}\widehat u-LJ_3(\widehat h)
                                                        =O(\sqrt\eta).
\]

Project $g=\widehat u+\rho\widehat h^2$ onto the orthogonal constant
vector and $\widehat h$, and call the residual $r_g$.
With $K_1=K_0+(U_0+\rho H)^2/16$, $K_1+\alpha H^2/2=B_*$,
the exact decomposition is

\[
\mathcal B(\widehat h,\widehat u)-B_*
=G(\widehat h)+\frac{\|r_g\|^2}{2}
 +\frac{(L+\rho)J_3\delta}{H}+\frac{\delta^2}{2H}.             \tag{20}
\]

Young's inequality and $G\ge\mu J_3^2/H$ give

\[
E_\eta(p)\ge\frac12G(\widehat h)+\frac12\|r_g\|^2-K_M\eta.    \tag{21}
\]

The $O(\sqrt\eta)$ mixed-constraint error is absorbed by the positive
cubic-moment square, rather than becoming a scalar loss of that order.

Choose a closest $h^*$ and its matching $u^*$. The projection formula gives

\[
\widehat u-u^*
=r_g-\rho(\widehat h^2-(h^*)^2)
              +\frac{(L+\rho)J_3+\delta}{H}\widehat h .
\]

On the fixed sphere,
$\|\widehat h^2-(h^*)^2\|\le2\sqrt H\|\widehat h-h^*\|$ and
$|J_3(\widehat h)|\le3H\|\widehat h-h^*\|$.
Thus joint squared distance is at most a fixed multiple of
$\operatorname{dist}(\widehat h,\{h^*\})^2+\|r_g\|^2+\delta^2$.
Use (18),(21), $\delta^2=O(\eta)$ and the normalization changes to
obtain (4). The coercive multiplier depends only on the fixed sphere
and coefficients; dependence on $M$ enters $K_M,\eta_M$.

For (5), apply (4) with $M=0$ whenever $F\le8+C\eta$, dropping
the distance term. If $F>8+C\eta$, (5) follows from $B_*<0$.
The previous attaining family has upper remainder $O(\eta^3)$,
proving (6). A fixed third-order upper budget eventually obeys (3)
with $M=0$, and (4) gives $\mathcal D_\eta^2=O(\eta)$, hence (7).

## 4. Disk-root families proving optimality of the rates

For a small parameter $s\ge0$, set

\[
H_A=(H/2)(1-s),\quad H_B=(H/2)s,\quad
h(s)=(\sqrt{H_A},-\sqrt{H_A},\sqrt{H_B},-\sqrt{H_B},0,0,0,0).
\]

Use the minimizing real correction
$u_j(s)=u_z-\rho h_j(s)^2$, so
$u_A=u_z-\rho H_A$, $u_B=u_z-\rho H_B$ at the two pairs,
and $u_z$ at the four zero coordinates. Odd moments vanish, and

\[
J_4(s)=H^2/2-H^2s(1-s),\quad
\mathcal B(h(s),u(s))=B_*-\alpha H^2s(1-s).                  \tag{22}
\]

These are identities on the sphere, not just local expansions.
Define
$U_2(s)=4u_z^2+2u_A^2+2u_B^2$ and
$J_{21}(s)=2u_AH_A+2u_BH_B$. Insert these and $J_4(s)$ into
$\mathcal T_3,\mathcal T_4$ in (13). Solve

\[
A_kW(s)/8+B_kD(s)/14=\mathcal T_k(s),\quad k=3,4,\qquad
\gamma(s)=(U_2(s)-D(s))/(2H).                                \tag{23}
\]

The determinant is $-3(c+d)/224\ne0$, and $W,D,\gamma$ are
polynomials in $s$. Put

\[
\begin{gathered}
L_j(\eta,s)=u_j(s)\eta+(W(s)/8)\eta^2+100\eta^3,
\quad j=0,A,B,\quad u_0=u_z,\\
q_{\eta,s}'(z)=9(z-L_0)^4
 \big((z-L_A)^2+H_A\eta(1+\gamma(s)\eta)^2\big)
 \big((z-L_B)^2+H_B\eta(1+\gamma(s)\eta)^2\big),\\
q_{\eta,s}(z)=\int_{1-\eta}^z q_{\eta,s}'(w)\,dw .
\end{gathered}                                                   \tag{24}
\]

This is a monic real degree-nine polynomial, with four real critical
points at $L_0$ and one conjugate pair at each of
$L_A\pm i\sqrt{H_A\eta}(1+\gamma\eta)$ and
$L_B\pm i\sqrt{H_B\eta}(1+\gamma\eta)$.

There are $s_0,\eta_0>0$ such that every $0\le s<s_0$,
$0<\eta<\eta_0$ has all nine original roots strictly inside the disk.
Indeed its coefficients are polynomial in $(\eta,s)$, and at $\eta=0$
it is $z^9-1$ independently of $s$. Original roots are therefore
analytic in a common parameter neighborhood. The marked root is
$1-\eta$. At the four inactive roots the negative first radial
coefficient is independent of $s$. At all four active roots the
first coefficient is zero and (23) makes the second coefficient
zero for every $s$. For $s=0$, (24) is exactly the earlier six-plus-pair
construction with its fixed 100 correction: both active-pair third
radial coefficients are strictly negative. Continuity in $s$ preserves
strict negativity in one common small interval, and uniform Taylor
remainders prove all-root containment. This covers all nine roots.
No sampled-root test is used in this step.

The checker independently multiplies and integrates (24). It verifies
the active second radial coefficient has degree at most two in $s$,
and that it vanishes at three distinct exact rational values. Together,
the degree bound and exact interpolation establish the whole polynomial
identity. The third-order signs at $s=0$ are separately reconstructed
from the defining factors.

The exact critical distances now give uniformly for small $s$

\[
F_{q_{\eta,s}}(1-\eta)
=8+C\eta+[B_*-\alpha H^2s(1-s)]\eta^2+O(\eta^3).             \tag{25}
\]

The actual normalized critical coordinates differ from
$(h(s),u(s))$ by $O(\eta)$ uniformly. For $s<1/2$ the nearest
target places its large opposed pair at the first two coordinates,
and the ideal joint squared distance is exactly

\[
\operatorname{dist}((h(s),u(s)),\mathcal M)^2
=2H(1-\sqrt{1-s})+\rho^2H^2s^2
=Hs+O(s^2).                                                 \tag{26}
\]

Taking $s=\eta$ in (25)-(26) gives
$F=8+C\eta+B_*\eta^2+O(\eta^3)$ and
$\mathcal D_\eta/\sqrt\eta\to\sqrt H$. The small conjugate pair
has imaginary coordinates $\pm b\eta(1+O(\eta))$. This proves
optimality of (7), including the order of the six small imaginary coordinates.

For optimality of the squared-distance power in (4), take instead
$\eta=s^2$ and let $s\downarrow0$. Equations (25)-(26) give
$E_\eta=(-\alpha H^2)s+O(s^2)$ and
$\mathcal D_\eta^2=Hs+O(s^2)$, with (3) eventually valid even
for $M=0$ because $B_*<0$. For any exponent $q<2$,
$E_\eta/\mathcal D_\eta^q\to0$ and
$\eta/\mathcal D_\eta^q\to0$. No positive distance penalty of
power $q<2$ with an $O(\eta)$ normalized remainder can hold on
this same class. This is exponent optimality, not sharpness of $\kappa$.

## 5. Exact evidence and limitations

The self-contained checker uses Python3.11 standard-library exact
arithmetic. Its generic full factor calculation has18 variables through
the sixth square-root order, including seven free imaginary coordinates,
eight free real coordinates and the rescaled small imaginary sum.
It checks conjugation parity, the improved real/imaginary coefficient
orders, the complete six-coordinate constrained Hessian, and all algebraic
signs. The generic derivative has 2852 terms and the anchored polynomial 6256.
A separate cubic-field three-variable implementation derives the
two-pair factors, primitive, radial identities and objective.
Exact quadratic Gaussian arithmetic evaluates the active ninth roots.
Rational isolation of the cubic embedding certifies the signs.

The optimized sparse substitution accumulates monomials directly instead
of repeatedly copying the partial dictionary. It matches every stored
record from the completed simpler reference implementation; no algebra
or coverage was changed. The normal and optimized Python checks and
damaged-fixture controls are reported in README.md.

Finite algebra is author validation. The prior concentration/bootstrap,
uniform root-map derivatives, even pair averaging, global compactness,
Young absorption and root containment are ordinary written proofs
outside a formal kernel. Independent review of this extension is pending.
The exact first-order/second-order constants and the selected limiting
profile are credited prior results. The new statements are the cubic-order
uniform error, quantitative profile penalty and its optimal scale.

An effective annulus radius, numerical coercivity constant, optimal
third-order boundary coefficient, and the unrestricted first-power
endpoint remain unproved here. No solver, floating-point root search,
enumeration, imported external data or private proof corpus is used.
