# Compact mean-width rigidity and eventual Gaussian majorisation

Author proof, 27 September 2026. Independent review of this extension is
pending. The compact rigidity theorem below is self-contained. Its Gaussian
consequence additionally uses the two accepted team results identified in
Section 4 and [INPUTS.json](INPUTS.json).

**Main consequence.** For every compactly supported probability measure
$\mu$ on $\mathbb R^3$ and every 1-Lipschitz map $T:\mathbb R^3\to\mathbb R^3$,
there is a finite $s_0=s_0(\mu,T)$ such that

\[
 \mu*\gamma_s\preceq T_\#\mu*\gamma_s\qquad\text{for every }s\ge s_0.
 \tag{1}
\]

Here $\gamma_s$ has covariance $sI_3$, and $f\preceq g$ means
$\int(f-b)_+\le\int(g-b)_+$ for every $b>0$. Thus the cutoff is simultaneous
in all thresholds. No atomicity, uniform Lipschitz gap, covariance lower
bound, or lower density bound is assumed. This does **not** settle the
unrestricted all-variance conjecture.

The missing ingredient is strict mean-width decrease for arbitrary compact
contractions, including diffuse supports. Section 5 also proves strict
large-equal-radius Kneser--Poulsen inequalities for arbitrary compact sets
of centers. The constants are conservative, and historical priority for the
compact extensions has not been established.

At the publication refresh, R3's independently accepted
[support-cap theorem](../gaussian_support_cap_localization/PROOF.md), graph6520,
already provided eventual majorisation throughout the positive support-width
sector. Theorem 2 below supplies its missing strict-width hypothesis for
every nonisometric compact contraction. The cap-mass join is credited to
that prior theorem, not claimed as another new mechanism.

## 1. An integrable exponential rigidity lemma

For a real symmetric $d\times d$ matrix $A$, put
$L_A=\sum_{i,j}A_{ij}\partial_i\partial_j$ and $Q_A(v)=v^TAv$.

**Lemma 1.** Suppose $d\ge1$, $h:\mathbb R^d\to\mathbb R$ is globally
Lipschitz, $h(z)\ge c|z|$ for some $c>0$, and

\[
 L_Ah=0\quad\text{in distributions},\qquad
 Q_A(\nabla h)\ge0\quad\text{almost everywhere}.
 \tag{2}
\]

Then $A=0$. No definiteness assumption on $A$ is needed.

**Proof.** Let $u=e^{-h}$. Then $u>0$, $u\in L^1$, and the gradient of
$h$ is bounded almost everywhere. Convolve $h$ with a smooth nonnegative
unit-mass mollifier supported in $B(0,\varepsilon)$, obtaining $h_\varepsilon$.
The Lipschitz bound gives uniform convergence $h_\varepsilon\to h$,
uniformly bounded gradients, and $\nabla h_\varepsilon\to\nabla h$ almost
everywhere. Also $L_Ah_\varepsilon=0$ and
$h_\varepsilon(z)\ge c|z|-C\varepsilon$. The smooth chain rule gives

\[
 L_Ae^{-h_\varepsilon}
 =e^{-h_\varepsilon}Q_A(\nabla h_\varepsilon).
\]

Dominated convergence, using the exponential decay and bounded gradients,
passes this identity to distributions and gives

\[
 L_Au=uQ_A(\nabla h)=:v,\qquad v\in L^1,\quad v\ge0.
 \tag{3}
\]

The mollified quadratic form need not have a sign; only its almost-everywhere
limit is used. Choose $\eta\in C_c^\infty$ with $0\le\eta\le1$, equal to one
on $B(0,1)$ and zero outside $B(0,2)$, and put $\eta_R(z)=\eta(z/R)$.
Then

\[
 \int v\eta_R=\int uL_A\eta_R\longrightarrow0,
\]

because $\|L_A\eta_R\|_\infty\le C_A/R^2$. Dominated convergence on the
left implies $\int v=0$, so $v=0$ and $L_Au=0$.

For each $i,j$, test the latter identity against $z_i z_j\eta_R$:

\[
 0=\int uL_A(z_i z_j\eta_R)
   \longrightarrow 2A_{ij}\int u.
 \tag{4}
\]

Indeed the differentiated test functions are uniformly bounded: on the
derivative annulus $|z|\le2R$, their terms have sizes $1$, $|z|/R$, or
$|z|^2/R^2$. Pointwise they converge to $L_A(z_i z_j)=2A_{ij}$, so $u\in L^1$
justifies the limit. Since $\int u>0$, every $A_{ij}$ vanishes. $\square$

Both qualifications matter. A seminorm on a larger ambient space need not
be coercive; it must first be restricted to its essential span. Also
$h(a,b)=|a+b|+|a-b|$ is coercive and satisfies
$(\partial_a^2-\partial_b^2)h=0$, but its gradient quadratic form takes both
signs, so it does not satisfy (2).

## 2. Compact Gaussian-width comparison and its equality case

For a nonempty compact set $K\subset\mathbb R^n$ let

\[
 w_G(K)=\mathbb E\sup_{x\in K}G_n\cdot x,
\]

where $G_n$ is a standard Gaussian. This width is translation invariant.

**Theorem 2.** Let $T:K\to\mathbb R^m$ be 1-Lipschitz on a nonempty compact
$K\subset\mathbb R^n$. Then

\[
 w_G(TK)\le w_G(K),
 \tag{5}
\]

and equality holds if and only if
$|Tx-Tx'|=|x-x'|$ for every $x,x'\in K$.

**Proof of comparison and the equality implication.** Set

\[
 S=\{(x,Tx):x\in K\},\quad C=\operatorname{conv}S,\quad
 H(a,b)=h_C(a,b)=\max_{x\in K}(a\cdot x+b\cdot Tx),
\]
\[
 J_0=\operatorname{diag}(I_n,-I_m),\qquad L=\Delta_a-\Delta_b.
\]

$S$ and $C$ are compact, and $H$ is convex and globally Lipschitz. We first
show that $LH$ is a nonnegative distribution. For finitely many
$s_i=(x_i,Tx_i)\in S$ and $\beta>0$, let

\[
 H_\beta(z)=\beta^{-1}\log\sum_i e^{\beta z\cdot s_i},\qquad
 \pi_i=\frac{e^{\beta z\cdot s_i}}{\sum_j e^{\beta z\cdot s_j}}.
\]

Direct differentiation gives

\[
 LH_\beta=\frac\beta2\sum_{i,j}\pi_i\pi_j
       \bigl(|x_i-x_j|^2-|Tx_i-Tx_j|^2\bigr)\ge0.
 \tag{6}
\]

Let $\beta\to\infty$ to obtain the support function of the finite graph.
Then approximate the compact graph by finite subsets in Hausdorff distance.
Support functions converge uniformly on compact sets, so both limits pass
to distributions. Therefore $LH\ge0$.

For independent standard Gaussians set

\[
 W(t)=\mathbb E H(\sqrt t\,G_n,\sqrt{1-t}\,G'_m),\qquad 0<t<1.
\]

The Gaussian density $\rho_t$ satisfies $\partial_t\rho_t=\tfrac12L\rho_t$,
and hence

\[
 W'(t)=\tfrac12\langle LH,\rho_t\rangle\ge0.
 \tag{7}
\]

Here is the integrability justification for this distributional pairing.
The Hessian of a convex Lipschitz function is a positive semidefinite
matrix of locally finite measures; its trace $\Delta H$ dominates the
absolute value of $LH$. Testing $\Delta H$ against scaled cutoffs and
integrating once by parts with bounded $\nabla H$ gives
$\Delta H(B(0,R))=O(R^{n+m-1})$ for $R\ge1$. Thus Gaussian pairings are
finite. Cutoffs permit integration by parts in (7); the boundary errors
vanish by Gaussian decay. Differentiation of $\int H\rho_t$ is dominated
on every compact subinterval of $(0,1)$, since $H$ has linear growth.

$W$ extends continuously to the endpoints, with $W(0)=w_G(TK)$ and
$W(1)=w_G(K)$. This proves (5). If these endpoints agree, $W$ is constant.
The positive Radon measure $LH$ then pairs to zero with a strictly positive
Gaussian density. Consequently

\[
 LH=0\quad\text{on }\mathbb R^{n+m}.
 \tag{8}
\]

Now put $V=\operatorname{span}(C-C)$ and

\[
 h(z)=H(z)+H(-z)=h_{C-C}(z).
\]

If $V=\{0\}$, the original graph is a singleton and the conclusion is
immediate. Otherwise $h$ depends only on the orthogonal projection onto
$V$. On $V$ it is coercive: the symmetric convex body $C-C$ contains a
relative neighborhood of zero, so $h(z)\ge c|z|$ for $z\in V$, for some
$c>0$. It remains globally Lipschitz there.

In an orthonormal basis of $V$ let $A$ be the compression of $J_0$ to $V$.
Equation (8), applied also to $H(-z)$, implies $L_A(h|_V)=0$. To see that
restriction introduces no assumption, use orthogonal coordinates
$V\oplus V^\perp$. The function $h$ is constant in the second coordinate;
all derivatives involving it vanish. Testing with a product function of
unit integral in that coordinate leaves precisely $L_A$ on $V$.

At almost every $z\in V$, both restricted support functions $H(z)$ and
$H(-z)$ are differentiable. Their exposed points $s_+(z)$ and $s_-(z)$
belong to $S$. Indeed a maximum over $C=\operatorname{conv}S$ is achieved
over compact $S$, and differentiability gives uniqueness. Restriction to
$V$ does not lose uniqueness: $C$ lies in a translate of $V$, and distinct
points of $C$ have distinct projections onto $V$. Thus

\[
 \nabla_Vh(z)=s_+(z)-s_-(z)\in V,
\]
\[
 Q_A(\nabla_Vh)
 =|x_+-x_-|^2-|Tx_+-Tx_-|^2\ge0.
 \tag{9}
\]

Lemma 1 implies $A=0$. Therefore $v^TJ_0v=0$ for every $v\in V$.
Every difference $(x-x',Tx-Tx')$ lies in $V$, proving preservation of
every pair distance.

Conversely, a distance-preserving map on $K$ extends to an affine isometry
between its affine span and that of its image. To verify this, fix a point
of $K$ and use the polarization identity to see that all inner products
of difference vectors are preserved. The resulting linear isometry of
their spans is well-defined and maps every point correctly. Gaussian
width is unchanged by an isometric embedding and translation. This proves
the equality converse. $\square$

In equal ambient dimensions the isometry extends to a Euclidean isometry
of the full ambient space. For $K\subset\mathbb R^3$, with normalized area
measure $\sigma$ on $S^2$, define

\[
 m(K)=\int_{S^2}h_K(\theta)\,d\sigma(\theta).
\]

Then $w_G(K)=\mathbb E|G_3|\,m(K)$; conventional mean width is $2m(K)$.
Consequently a nonisometric compact contraction has

\[
 \omega:=m(K)-m(TK)>0.
 \tag{10}
\]

Finite strictness is the prior theorem of Gorbovickis. Its direct compact
limit supplies only a weak inequality; the exponential argument above is
the additional equality analysis used here.

## 3. A uniform large-parameter tail for arbitrary full-support laws

This is the elementary cap-mass argument of R3's cited support-cap theorem,
included with our normalization to display the cutoff. The new premise is
the unconditional positivity of (10), proved above.

Let $K=\operatorname{supp}\mu$ be compact, $\nu=T_\#\mu$, and suppose $T$
is nonisometric on $K$. Let $\omega>0$ be (10) and $\varepsilon=\omega/2$.
Choose a finite $\varepsilon/2$-net $x_1,\ldots,x_N$ in $K$, and define

\[
 m_*:=\min_j\mu(B(x_j,\varepsilon/2))>0.
 \tag{11}
\]

Positivity follows from the definition of support, with no density or atom
assumption. For any $\theta\in S^2$, take a point of $K$ maximizing
$\theta\cdot x$ and a net point within $\varepsilon/2$ of it. Every point
in the corresponding ball is within $\varepsilon$ of the maximizer. Thus
for every $\lambda>0$,

\[
 \log\int e^{\lambda\theta\cdot x}\,d\mu(x)
 \ge\lambda h_K(\theta)-\lambda\varepsilon+\log m_*.
\]

The upper bound for $\nu$ is $\lambda h_{TK}(\theta)$. Hence, writing

\[
 J(\lambda)=\int_{S^2}\left(
 \log\int e^{\lambda\theta\cdot x}\,d\mu(x)
 -\log\int e^{\lambda\theta\cdot y}\,d\nu(y)\right)d\sigma,
\]

we obtain the uniform tail

\[
 J(\lambda)\ge\tfrac\omega2\lambda+\log m_*.
 \tag{12}
\]

This step uses the support of the law, not an arbitrary larger set on which
the map happens to be defined.

## 4. Eventual full majorisation for every compactly supported law

Translate the source and target separately so both supports lie in
$B(0,R)$, with $R>0$. For example use an input support ball $B(a,R)$ and
translate the output by $T(a)$. These translations preserve $J$, $\omega$,
the pair losses, and Gaussian hinges. Define

\[
 D=\iint\bigl(|x-x'|^2-|Tx-Tx'|^2\bigr)\,d\mu(x)d\mu(x').
\]

If $T$ is nonisometric on $K$, then $D>0$: the continuous nonnegative
integrand is positive at some pair in $K\times K$, and full support gives
positive product measure to a neighborhood of that pair. Also $D\le4R^2$.

The accepted [spherical-sinc comparison](../gaussian_spherical_sinc_comparison/PROOF.md),
Theorem A, gives for all $\lambda>0$

\[
 J(\lambda)\ge\frac{D\lambda^2}{12}e^{-4\lambda R}.
 \tag{13}
\]

Set

\[
 \lambda_0=\frac1{2R},\qquad
 \lambda_1=\max\left\{\lambda_0,
                \frac{2(1+\log(1/m_*))}{\omega}\right\},\qquad
 \kappa=\frac{D}{48R^2}e^{-4R\lambda_1}>0.
 \tag{14}
\]

For $\lambda\in[\lambda_0,\lambda_1]$, (13) is at least $\kappa$.
For $\lambda\ge\lambda_1$, (12) is at least one, which exceeds $\kappa$
because $D\le4R^2$. Thus $J(\lambda)\ge\kappa$ for every
$\lambda\ge1/(2R)$.

The accepted [eventual endpoint](../gaussian_majorisation_eventual_endpoint/PROOF.md),
Theorem 1, states that this uniform gap implies all-threshold majorisation
for $s\ge R^2\max\{8,44/\kappa\}$. Since $\kappa\le1/12$, the explicit
choice

\[
 \boxed{\quad s_0=44R^2/\kappa\quad}
 \tag{15}
\]

proves (1). If $T$ is isometric on $K$, an ambient Euclidean isometry maps
$\mu$ to $\nu$, so all hinges are equal at every variance. This also handles
singleton supports and $R=0$.

Equivalently, the qualitative conclusion follows immediately by applying
R3's support-cap Corollary 2 to (10). Its Section 5 then has the following
new structural consequence: every fixed nonisometric bounded contraction
lies in the sector admitting a finite rational support-cover certificate,
provided genuine cover and mass bounds are supplied. This is existence of
a certificate for each fixed pair, not an algorithm extracting such bounds
from an unspecified law or a uniform complexity estimate.

The endpoint theorem itself combines the spherical-tail estimate at small
thresholds with the high-noise window at the remaining thresholds. The
independent acceptance of that package and both independent acceptances of
(13) are pinned in [INPUTS.json](INPUTS.json). They do not constitute review
of the new compact rigidity proof.

The cutoff depends on the actual law and map, through $\omega$ and the
finite-cover mass $m_*$. No uniform cutoff for an unrestricted family is
claimed. Noncompactly supported laws and variances below this cutoff remain
outside this conclusion. A bounded positive finite measure follows by
normalizing its total mass and rescaling the hinge threshold.

## 5. Strict large-radius KP for arbitrary compact center sets

For nonempty compact $K\subset\mathbb R^3$ put

\[
 U_K(r)=\bigcup_{x\in K}\overline B(x,r),\qquad
 I_K(r)=\bigcap_{x\in K}\overline B(x,r).
\]

**Theorem 3.** If $T:K\to\mathbb R^3$ is a nonisometric contraction, then
for every sufficiently large common radius $r$,

\[
 |U_{TK}(r)|<|U_K(r)|,\qquad |I_{TK}(r)|>|I_K(r)|.
 \tag{16}
\]

More precisely, separately translate $K,TK$ into $B(0,R)$, and use
$\omega=m(K)-m(TK)>0$. It suffices that

\[
 r\ge\max\{2R,16R^2/\omega\}.
 \tag{17}
\]

Isometric contractions give equality at all radii.

**Proof.** For $r\ge2R$, each ball with center $x\in B(0,R)$ contains the
origin. Its radial endpoint in direction $\theta$ is

\[
 \theta\cdot x+\sqrt{r^2-|x|^2+(\theta\cdot x)^2}
 =r+\theta\cdot x+e_x(\theta),\qquad
 -R^2/r\le e_x(\theta)\le0.
 \tag{18}
\]

The bound follows by rationalizing the square-root difference. Taking a
maximum or minimum over compact $K$ shows that the radial functions of
the union and intersection are respectively

\[
 \rho_U=r+h_K(\theta)+e_U(\theta),\quad
 \rho_I=r-h_K(-\theta)+e_I(\theta),\qquad -R^2/r\le e_U,e_I\le0.
\]

The union is star-shaped about zero and has no gaps on each ray because
all its constituent balls contain zero. The intersection has the stated
minimum radial endpoint. Both radial functions are continuous.

For $|k|\le R$, $-R^2/r\le e\le0$, and $r\ge2R$, one has
$|k+e|\le3R/2$ and

\[
 \begin{aligned}
 |(r+k+e)^3-r^3-3r^2k|
 &\le3rR^2+\tfrac{27}{4}rR^2+\tfrac{27}{8}R^3\\
 &\le\tfrac{183}{16}rR^2<12rR^2.
 \end{aligned}
\]

Integrating $\rho^3/3$ over the sphere, with ordinary area measure, gives

\[
 \left||U_K(r)|-\tfrac{4\pi}3r^3-4\pi r^2m(K)\right|
 \le16\pi R^2r,
\]
\[
 \left||I_K(r)|-\tfrac{4\pi}3r^3+4\pi r^2m(K)\right|
 \le16\pi R^2r.
 \tag{19}
\]

Therefore each difference in the desired direction in (16) is at least
$4\pi\omega r^2-32\pi R^2r$. Under (17) it is at least
$2\pi\omega r^2>0$. $\square$

Gorbovickis previously proved strict large-equal-radius union/intersection
inequalities for finite configurations. Here the new-to-campaign scope is
arbitrary compact families, with a self-contained uniform radial remainder.
This statement concerns common radii only, not arbitrary individual radii
or all radii. It does not rely on unreviewed newer all-variance classes.

## 6. Verification boundary

[verify.py](verify.py) uses exact rational arithmetic to check the finite
posterior identity, Gaussian interpolation normalization, exponential chain
rule coefficients, quadratic moment tests, null graph spans, essential-span
and gradient-sign negative controls, and the cutoff constants. It does not
certify distributional limits or the universal theorems by enumeration.
Those steps are proved above and require mathematical review. No numerical
integration, simulation, solver, hidden corpus, or new formalization is used.
