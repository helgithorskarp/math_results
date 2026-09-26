# A geometric exclusion of small-mass failures away from the far tail

Complete author proof, 26 September 2026; independent review pending.
The dimension-three Gaussian majorisation conjecture remains open.

## 1. Statement and quantifiers

Fix a variance $s>0$, a compactly supported probability measure $\nu$ on
$\mathbb R^3$, and a 1-Lipschitz map
$T:\{0\}\cup\operatorname{supp}\nu\to\mathbb R^3$ with $T(0)=0$.
Write

$$
\phi(z)=C\exp(-|z|^2/(2s)),\qquad C=(2\pi s)^{-3/2},
$$

$$
f_\varepsilon=(1-\varepsilon)\phi+\varepsilon(\nu*\phi),
\quad
g_\varepsilon=(1-\varepsilon)\phi+\varepsilon(T_\#\nu*\phi),
\quad 0\le\varepsilon\le1.
\tag{1}
$$

Let $H_f(a)=\int(f-a)_+$ and
$D_\varepsilon(a)=H_{g_\varepsilon}(a)-H_{f_\varepsilon}(a)$.
The fixed origin is no restriction on the location of the dominant atom:
translate that atom and its image separately to the origin.

**Theorem 1 (uniform comparison above every positive threshold floor).**
For every $a_0>0$ there is an $\varepsilon_0>0$ such that

$$
D_\varepsilon(a)\ge0
\quad\text{for all }0\le\varepsilon\le\varepsilon_0
\text{ and all }a\ge a_0.
\tag{2}
$$

If $T$ is not the restriction of an orthogonal map on $\operatorname{supp}\nu$,
then $\varepsilon_0$ can be chosen so that the inequality is strict whenever
$0<\varepsilon\le\varepsilon_0$ and $a_0\le a<\max g_\varepsilon$.
If $T$ is such a restriction, all hinge profiles in (1) agree.

In particular, for **fixed** $\nu,T,s$, any hypothetical failures
$D_{\varepsilon_j}(a_j)<0$ with $\varepsilon_j\downarrow0$ must satisfy
$a_j\to0$. Their Gaussian reference radii
$\sqrt{2s\log(C/a_j)}$ therefore tend to infinity.

Theorem 2 below strengthens this to an explicit threshold window, showing
that any failure with vanishing moved mass must have a threshold smaller
than every fixed power of that mass.
The theorem includes thresholds approaching the moving density maxima.
It is stronger than positivity at each fixed regular threshold. It does
**not** assert a common $\varepsilon_0$ for all $a>0$, nor uniformity over
$\nu,T,s$. It does not give full majorisation or a new Kneser--Poulsen case.

## 2. First variation: radial loss is strictly favorable

Put
$h_P=\nu*\phi-\phi$ and $h_Q=T_\#\nu*\phi-\phi$.
For $0<a<C$, let $R=\sqrt{2s\log(C/a)}$. The sphere $|z|=R$ is a regular
level set of $\phi$. Differentiation of the superlevel integral gives

$$
A(a):=\left.\partial_\varepsilon D_\varepsilon(a)\right|_0
=\int_{|z|<R}\big[(T_\#\nu*\phi)(z)-(\nu*\phi)(z)\big],dz.
\tag{3}
$$

For any $R>0$, the function
$L_R(r)=\int_{|z|<R}\phi(z-r e_1)\,dz$ is strictly decreasing in $r\ge0$.
To see strictness directly, slice the ball perpendicular to $e_1$. A slice
is an interval $[-b,b]$, $b>0$, and the derivative of its one-dimensional
Gaussian mass is $\phi_{1,s}(b+r)-\phi_{1,s}(b-r)<0$ when $r>0$.
Integrate the slices; comparison with $r=0$ follows by integration in $r$.

Since $|Tx|\le|x|$, (3) becomes

$$
A(a)=\int[L_R(|Tx|)-L_R(|x|)],d\nu(x)\ge0.
\tag{4}
$$

If radial distance decreases on a set of positive $\nu$-measure, then
$A(a)>0$ for **every** $a\in(0,C)$. Otherwise $|Tx|=|x|$ almost everywhere
and $A$ vanishes identically. By continuity, the latter equality holds on
the entire support.

For completeness, the differentiations used here and below are uniform on
compact subintervals of $(0,C)$. On such an interval all relevant superlevel
sets remain in a fixed ball for small $|\varepsilon|$: the perturbations are
bounded, and the base Gaussian is below half the threshold outside a large
ball. Near its level spheres the base gradient is bounded away from zero.
The implicit-function theorem gives a smooth compact moving boundary, with
uniform derivatives. Thus $D_\varepsilon(a)$ is jointly smooth there and
has uniform Taylor remainders in $\varepsilon$.

## 3. Second variation: a positive spherical kernel

Assume now $|Tx|=|x|$ on the support. The second derivative of a hinge at
a regular level is

$$
\left.\partial_\varepsilon^2H_{\phi+\varepsilon h}(a)\right|_0
=\int_{|z|=R}\frac{h(z)^2}{|\nabla\phi(z)|},dS(z).
\tag{5}
$$

This follows by differentiating
$\partial_\varepsilon H=\int_{\phi+\varepsilon h>a}h$;
the outward normal velocity of its boundary at zero is $h/|\nabla\phi|$.

Let $x,x'$ be independent samples from $\nu$, and put
$q=Tx$, $q'=Tx'$ and

$$
\delta(x,x')=|x-x'|^2-|q-q'|^2\ge0,
\qquad S(u)=\begin{cases}\sinh(u)/u,&u\ne0,\\1,&u=0.\end{cases}
$$

On the sphere, write
$h_P(z)=a[\int e^{z\cdot x/s-|x|^2/(2s)}d\nu(x)-1]$,
and similarly for $Q$. The terms linear in the exponential integrals cancel
after spherical integration, because $|q|=|x|$ for each label. The identity

$$
\int_{|z|=R}e^{z\cdot v/s},dS(z)=4\pi R^2S(R|v|/s)
\tag{6}
$$

is obtained by aligning $v$ with the polar axis and integrating
$2\pi R^2\int_{-1}^1 e^{R|v|t/s}dt$. Since $|\nabla\phi|=aR/s$,
(5) gives the explicit formula

$$
\begin{split}
B(a):=\left.\partial_\varepsilon^2D_\varepsilon(a)\right|_0
=4\pi s aR\iint e^{-(|x|^2+|x'|^2)/(2s)}
\big[ S(R|q+q'|/s)-S(R|x+x'|/s)\big],d\nu(x)d\nu(x').
\end{split}
\tag{7}
$$

Norm preservation and pairwise contraction imply

$$
|q+q'|^2-|x+x'|^2=\delta(x,x')\ge0.
\tag{8}
$$

The function $S$ is strictly increasing on $[0,\infty)$, as follows directly
from $S(u)=\sum_{k\ge0}u^{2k}/(2k+1)!$. Hence every integrand in (7) is
nonnegative. If $\delta>0$ on a set of positive product measure, then
$B(a)>0$ for every $0<a<C$.

Otherwise $\delta=0$ almost everywhere and therefore everywhere on the
paired support, by continuity. Together with preserved norms, this gives
$\langle Tx,Tx'\rangle=\langle x,x'\rangle$. The assignment $x\mapsto Tx$
extends linearly to an isometry of the spanned subspaces: a linear relation
maps to zero because its squared norm is computed from the same Gram matrix.
Extend that isometry to an orthogonal map of $\mathbb R^3$. In this case
$g_\varepsilon$ is an orthogonal image of $f_\varepsilon$, and all hinge
gaps vanish exactly.

Thus every nonrigid case has one of two alternatives, with positivity at
every interior threshold:

$$
D_\varepsilon(a)=\varepsilon A(a)+O(\varepsilon^2),\quad A(a)>0,
\quad\text{or}\quad
D_\varepsilon(a)=\tfrac12\varepsilon^2B(a)+O(\varepsilon^3),\quad B(a)>0.
\tag{9}
$$

The remainders are uniform on compact subintervals of $(0,C)$.
This already handles all thresholds separated from both zero and $C$.
The next two sections close the missing endpoint near the maximum.

## 4. The maximum gap has the same first nonzero order

For a compact probability law $\lambda$, define

$$
m_\lambda=\int e^{-|x|^2/(2s)}d\lambda(x),\qquad
v_\lambda=\int x e^{-|x|^2/(2s)}d\lambda(x).
$$

Let $F_{\lambda,\varepsilon}=(1-\varepsilon)\phi+\varepsilon(\lambda*\phi)$
and $M_\lambda(\varepsilon)=\max F_{\lambda,\varepsilon}$.
For small $|\varepsilon|$ it has a unique global maximum near zero.
Indeed its Hessian remains negative definite in a sufficiently small fixed
ball, while outside that ball the base Gaussian has a fixed gap below $C$
which the bounded perturbation cannot close. The implicit-function theorem
at $\nabla\phi(0)=0$ supplies its analytic mode $z_\lambda(\varepsilon)$.

Since
$D^2\phi(0)=-(C/s)I$ and
$\nabla(\lambda*\phi-\phi)(0)=(C/s)v_\lambda$,
Taylor expansion at that mode gives

$$
z_\lambda(\varepsilon)=\varepsilon v_\lambda+O(\varepsilon^2),\qquad
M_\lambda(\varepsilon)
=C+C(m_\lambda-1)\varepsilon
 +\frac{C}{2s}|v_\lambda|^2\varepsilon^2+O(\varepsilon^3).
\tag{10}
$$

Write $M_P=M_\nu$ and $M_Q=M_{T_\#\nu}$. In the radial-loss case,
$m_Q-m_P>0$, so $M_Q-M_P$ has a strictly positive first-order coefficient.
In the norm-preserving nonrigid case $m_Q=m_P$, and the Gram identity (8)
gives

$$
|v_Q|^2-|v_P|^2
=\tfrac12\iint e^{-(|x|^2+|x'|^2)/(2s)}\delta(x,x'),d\nu(x)d\nu(x')>0.
\tag{11}
$$

Consequently, in the respective cases $k=1$ and $k=2$, there are constants
$c_-,c_+>0$ with

$$
c_-\varepsilon^k\le d_\varepsilon:=M_Q(\varepsilon)-M_P(\varepsilon)
\le c_+\varepsilon^k
\tag{12}
$$

for all sufficiently small positive $\varepsilon$.

## 5. Uniformity at the moving maxima

We give the local normal form and the comparison estimate explicitly.
Near its mode, either of the analytic density families above has coordinates
$y$ in which

$$
F_{\lambda,\varepsilon}(z)=M_\lambda(\varepsilon)-|y|^2,
\qquad dz=J_\lambda(\varepsilon,y),dy,
\tag{13}
$$

where $J$ is analytic and positive. One construction needs only Taylor's
formula and the inverse-function theorem. In coordinates $w$ centered at
the mode, put

$$
K_\lambda(\varepsilon,w)
=-\int_0^1(1-t)D^2F_{\lambda,\varepsilon}(z_\lambda(\varepsilon)+tw),dt.
$$

It is positive definite near $(\varepsilon,w)=(0,0)$, and
$M_\lambda-F_{\lambda,\varepsilon}=w^TK_\lambda w$.
Set $y=K_\lambda(\varepsilon,w)^{1/2}w$. Its derivative in $w$ at zero is
invertible, giving (13) and analytic parameter dependence. Compact support
of $\lambda$ justifies analyticity of its Gaussian mixture. Sufficiently
high superlevel sets are entirely in this coordinate neighborhood, by the
fixed gap outside the mode's neighborhood.

For $0\le t\le t_*$ small, (13) implies

$$
H_{F_{\lambda,\varepsilon}}(M_\lambda(\varepsilon)-t)
=t^{5/2}L_\lambda(\varepsilon,t),\qquad
L_\lambda(\varepsilon,t)
=\int_{|u|<1}(1-|u|^2)J_\lambda(\varepsilon,\sqrt t\,u),du.
\tag{14}
$$

Odd powers of $\sqrt t$ integrate to zero, so $L$ is analytic in
$(\varepsilon,t)$ near $t=0$. It is positive. On a common compact parameter
rectangle it has a positive lower bound $\ell$ and a bounded derivative
in $t$, say $|\partial_tL|\le K_1$.

At $\varepsilon=0$, the two functions $L_P,L_Q$ agree. Therefore
$|L_Q-L_P|\le K_0\varepsilon$ uniformly. In the norm-preserving case there
is the stronger bound

$$
|L_Q(\varepsilon,t)-L_P(\varepsilon,t)|\le K_0\varepsilon^2.
\tag{15}
$$

To check the extra cancellation, fix $t>0$ and differentiate (14) at the
fixed threshold $a=C-t$. The first variation of the hinge difference is
zero by (4), and the derivatives of $M_P,M_Q$ agree by (10). All terms
involving the common base $L(0,t)$ and its $t$ derivative cancel, leaving
$t^{5/2}(\partial_\varepsilon L_Q(0,t)-\partial_\varepsilon L_P(0,t))=0$.
Continuity extends this to $t=0$. Uniform Taylor estimates prove (15).

In both cases we thus have $|L_Q-L_P|\le K_0\varepsilon^k$, with the same
$k$ as in (12). Let $p=5/2$ and $a<M_P$, and put $t=M_P-a>0$.
Whenever $t,t+d_\varepsilon$ lie in the normal-form interval, (14) gives

$$
\begin{split}
D_\varepsilon(a)
&\ge \ell[(t+d_\varepsilon)^p-t^p]
       -t^p(K_0\varepsilon^k+K_1d_\varepsilon)\\
&\ge t^{p-1}d_\varepsilon
       [p\ell-t(K_0/c_-+K_1)].
\end{split}
\tag{16}
$$

Choose a fixed sufficiently small $\eta>0$ so that the bracket is positive
for $0<t\le\eta$, and then choose $\varepsilon$ small so
$d_\varepsilon\le t_*/2$ and $\eta\le t_*/2$. This proves strict positivity
uniformly for $M_P-\eta\le a<M_P$. If $M_P\le a<M_Q$, the source hinge is
zero and the target hinge is positive. Above $M_Q$ both are zero.

Since $M_P\to C$, this argument covers every $a\ge C-\eta/2$ after a
further reduction of $\varepsilon_0$. The remaining interval
$[a_0,C-\eta/2]$, if nonempty, is compact in $(0,C)$, and (9) handles it
uniformly. This proves Theorem 1, including its strictness assertion.

## 6. A quantitative window and super-polynomial escape

**Theorem 2.** Suppose $\operatorname{supp}\nu\subset B(0,L)$ with $L>0$.
For fixed $\nu,T,s$ there is an $\varepsilon_*>0$ such that

$$
D_\varepsilon(a)\ge0\quad\text{whenever}\quad
0<\varepsilon\le\varepsilon_*,\qquad
a\ge C\exp\!\left[-\frac{s}{32L^2}
                         \big(\log(1/\varepsilon)\big)^2\right].
\tag{17}
$$

In the nonrigid case the gap is strict below $\max g_\varepsilon$ in this
window. The constant $1/32$ is sufficient; no optimality is claimed.
Consequently every failure sequence for fixed $\nu,T,s$ with
$\varepsilon_j\downarrow0$ satisfies

$$
\frac{a_j}{C\varepsilon_j^m}\longrightarrow0
\qquad\text{for every fixed }m>0.
\tag{18}
$$

We prove the estimate after scaling to $s=1$. Under that scaling the support
radius is $L/\sqrt s$ and the normalized threshold $a/C$ is unchanged, which
gives (17) as stated.

First, the favorable coefficients have explicit lower bounds for all $R>0$.
For the first variation, the divergence theorem and polar integration give

$$
-L_R'(r)=4\pi R^2a e^{-r^2/2} S'(Rr).
$$

Since $S'(u)\ge u/3$, integration from $|Tx|$ to $|x|$ gives

$$
A(a)\ge\frac{4\pi}{3}aR^3(m_Q-m_P).
\tag{19}
$$

In the norm-preserving case, the positive series of $S$ yields
$S(u)-S(v)\ge(u^2-v^2)/6$ when $u\ge v\ge0$. Equations (7)--(11) therefore
give

$$
B(a)\ge\frac{4\pi}{3}aR^3(|v_Q|^2-|v_P|^2).
\tag{20}
$$

The relevant constants in parentheses are strictly positive in the two
nonrigid cases.

Here are uniform remainder bounds as $R$ grows. For either law $\lambda$,
write, in direction $\theta\in S^2$,

$$
F_{\lambda,\tau}(r\theta)=\phi(r\theta)[1+\tau u_\lambda(r,\theta)],
\qquad
u_\lambda=\int e^{r\theta\cdot x-|x|^2/2}d\lambda(x)-1.
$$

The support bound gives
$|u_\lambda|\le2e^{Lr}$ and
$|\partial_ru_\lambda|\le Le^{Lr}$.
Choose a fixed $R_0>2L+3$ sufficiently large. If $R\ge R_0$ and
$\varepsilon e^{L(R+1)}$ is sufficiently small, then for every
$0\le\tau\le\varepsilon$ the threshold $a=C e^{-R^2/2}$ has exactly one
radial boundary $\rho=\rho_\lambda(\tau,R,\theta)\in(R-1,R+1)$.
Indeed $F\ge(1-\tau)\phi>a$ throughout the ball of radius $R-1$,
while $F(R+1)<a$. For $r>L$ every Gaussian translate in the mixture is
strictly decreasing in the radial direction, so there are no further crossings.

All constants denoted $K$ below depend on the fixed support bound and $R_0$,
but not on $R,\theta,\tau,\varepsilon$ in this regime. At the boundary $F=a$,
the posterior average of $\theta\cdot x$ lies in $[-L,L]$, whence

$$
|F_r|\ge aR/2,\qquad |F_{rr}|\le KaR^2.
$$

Writing $h=\lambda*\phi-\phi$, the bound $1+\tau u\ge1-\tau\ge1/2$
also gives

$$
|h|\le Ka e^{LR},\quad |h_r|\le KaR e^{LR},\quad
|\rho_\tau|\le K e^{LR}/R,\quad
|\rho_{\tau\tau}|\le K e^{2LR}/R.
\tag{21}
$$

The last two follow by differentiating $F(\rho,\tau)=a$:
$\rho_\tau=-h/F_r$ and
$\rho_{\tau\tau}=-(2h_r\rho_\tau+F_{rr}\rho_\tau^2)/F_r$.
Polar integration of the hinge, with solid-angle measure $d\theta$, gives

$$
H''(\tau)=\int_{S^2}h(\rho\theta)\rho^2\rho_\tau,d\theta,
$$

$$
H'''(\tau)=\int_{S^2}
 [(h_r\rho^2+2h\rho)\rho_\tau^2+h\rho^2\rho_{\tau\tau}],d\theta.
$$

Thus (21) implies

$$
|H''(\tau)|\le KaR e^{2LR},\qquad
|H'''(\tau)|\le KaR e^{3LR}.
\tag{22}
$$

These estimates justify, with constants independent of $R$,

$$
D_\varepsilon(a)=\varepsilon A(a)
   +O(\varepsilon^2aR e^{2LR})
$$

in the radial-loss case, and

$$
D_\varepsilon(a)=\tfrac12\varepsilon^2B(a)
   +O(\varepsilon^3aR e^{3LR})
\tag{23}
$$

in the norm-preserving case. Now impose

$$
R_0\le R\le R_\varepsilon:=\frac1{4L}\log(1/\varepsilon).
$$

The radial-boundary condition holds uniformly, since
$\varepsilon e^{L(R+1)}\le e^L\varepsilon^{3/4}\to0$.
Relative to the positive leading terms (19) and (20), the errors in (23)
are bounded by constant multiples of $\varepsilon^{1/2}/R^2$ and
$\varepsilon^{1/4}/R^2$, respectively. They tend uniformly to zero.
This proves strict positivity throughout that radial interval for small
$\varepsilon$. Theorem 1, with the fixed floor $C e^{-R_0^2/2}$, handles
all remaining higher thresholds, including the moving maxima. Since
$a=C e^{-R^2/2}$, this proves (17). Equation (18) follows immediately.

## 7. A first-order mechanism for arbitrary stationary anchors

Here is a related geometric statement whose base need not be a point mass.
Let $\sigma,\nu$ be compact probability laws, and let $T$ be a contraction
on their combined support that fixes every point of $\operatorname{supp}\sigma$.
Put $f_0=\sigma*\phi$ and compare the convolutions of
$(1-\varepsilon)\sigma+\varepsilon\nu$ and its $T$-image.

**Proposition 3.** For every $a>0$, the right derivative at zero of the hinge
gap is nonnegative.

The positive level sets of the nonconstant real-analytic function $f_0$ have
Lebesgue measure zero. Dominated convergence therefore gives the derivative
as $\int_A[(T_\#\nu*\phi)-(\nu*\phi)]$, where $A=\{f_0>a\}$.
For one moved point $p\mapsto q$, $p\ne q$, all stationary anchors lie in
the halfspace $E=\{x:|x-q|\le|x-p|\}$. If $\rho$ is reflection in its
boundary, then $f_0(z)\ge f_0(\rho z)$ for $z\in E$, by comparison with
each anchor separately. Thus $1_A(z)\ge1_A(\rho z)$ there. Also
$\phi(z-q)-\phi(z-p)\ge0$ on $E$ and reverses sign under $\rho$. Hence

$$
\int_A[\phi(z-q)-\phi(z-p)],dz
=\int_E[1_A(z)-1_A(\rho z)][\phi(z-q)-\phi(z-p)],dz\ge0.
\tag{24}
$$

Integrate over the moving law $\nu$. This proves the proposition. It does
not assert the uniform conclusion of Theorem 1 for a general anchor law.

## 8. Relation to the open frontier and reproducibility

The problem source is
[Aishwarya–Li, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
The arguments here use explicit Gaussian geometry and local analysis;
they do not assume the conjecture or infer hinge signs from entropy signs.
A targeted source/literature check is not a priority guarantee.

The preceding
[paired-rank and half-order reduction](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_rank_abel/PROOF.md)
isolated the need for additional contraction geometry. The team's
[Hankel criterion](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_hankel_transport/PROOF.md)
gives finite polynomial certificates, while the
[moment-gap theorem](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_contraction_moment_gaps/PROOF.md)
rules out certain energy tests. These are complementary context, not premises
of the proof above. The new restriction is uniform exclusion of hinge failures
in the quantitative window (17), including all thresholds above any fixed
positive floor, in the stated small-mass regime.

At the publication refresh we also inspected the team's
[high-variance quartic and finite-Hankel theorem](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_contraction_high_noise_quartics/PROOF.md).
That result controls bounded polynomial degree as the variance grows. Here the
variance stays fixed, the mass away from a dominant atom tends to zero, and
all hinges in the stated threshold window are controlled. Its proof is not
a premise of this one.

This applies even to the classical nonliftable simplex-flap configuration:
add a fixed atom at the origin, assign total mass $\varepsilon$ to the
sixteen labels, and mass $1-\varepsilon$ to the origin. The origin constraints
hold because each flap's squared norm drops from $8$ to $4$ at depth one.
Its existing sixteen-point subconfiguration still prevents a continuous
contraction in $\mathbb R^5$. That obstruction is the prior
[Cheng–Tan–Zheng theorem](https://arxiv.org/abs/1107.0140), not a new claim.
Thus the theorem is not restricted to the easy paired-rank class. It still
leaves the far-tail thresholds uncontrolled, including on this fixture.

The accompanying verifier checks exact rational contraction and rank data,
the weighted Gram identity, spherical integration by two algebraic routes,
the near-mode coefficient normalization, and outward enclosures of sampled
quadratic coefficients. These are supplementary checks. The universal
quantifiers and endpoint uniformity rest on the written argument, not a
finite scan, floating-point experiment, or proof assistant.
