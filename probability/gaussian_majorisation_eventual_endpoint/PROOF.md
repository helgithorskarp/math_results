# A full high-variance endpoint from the spherical gap

Author proof, 26 September 2026. Independent mathematical review and
formalization are pending. The conclusion compares **every density
threshold simultaneously** once the variance exceeds a fixed bound.
It does not resolve the all-variance three-dimensional conjecture or
give a new Kneser--Poulsen inequality.

## 1. The endpoint criterion

Let $\mu$ be a probability measure supported in $B(a,R)$ in $\mathbb R^3$,
let $T:\mathbb R^3\to\mathbb R^3$ be 1-Lipschitz, and put $\nu=T_\#\mu$.
Write

\[
 C_s=(2\pi s)^{-3/2},\qquad f_s=\mu*\gamma_s,\quad
 g_s=\nu*\gamma_s,\qquad H_h(b)=\int_{\mathbb R^3}(h-b)_+\,dx.
 \tag{1}
\]

Here $\gamma_s$ has covariance $sI_3$. With normalized area measure
$\sigma$ on $S^2$, define

\[
 S_\mu(\lambda)=\int_{S^2}\log\left(\int e^{\lambda\theta\cdot x}
                                             \,d\mu(x)\right)d\sigma,
 \qquad J(\lambda)=S_\mu(\lambda)-S_\nu(\lambda).
 \tag{2}
\]

Translations of either law do not change $S$ or its Gaussian hinges.
For $S$ the added linear function of $\theta$ has average zero.
We may therefore assume both laws lie in $B(0,R)$, by translating
the input by $a$ and the output by $T(a)$. The case $R=0$ is equality
at all variances and thresholds. Assume $R>0$ below.

**Theorem 1 (uniform spherical gap completes all thresholds).**
Suppose a number $\kappa>0$ satisfies

\[
 J(\lambda)\geq\kappa\qquad\hbox{for every }\lambda\geq\frac1{2R}.
 \tag{3}
\]

Then

\[
 \boxed{\,s\geq R^2\max\{8,44/\kappa\}
 \quad\Longrightarrow\quad
 H_{g_s}(b)\geq H_{f_s}(b)\quad\hbox{for every }b>0.\,}
 \tag{4}
\]

Thus $f_s$ is majorised by $g_s$. The variance bound is uniform in the
threshold, not a threshold-dependent limit. No finite-support assumption
or lower atom-weight bound is used in this theorem.

### Proof and the two analytic dependencies

The team's [spherical-tail theorem](../gaussian_majorisation_spherical_tail/PROOF.md),
Theorem A, gives the following estimate. If
$\lambda^2s\geq\max\{1,4\lambda R\}$, set
$b=C_s\exp(-\lambda^2s/2)$. Then

\[
 \left|\frac{H_{g_s}(b)-H_{f_s}(b)}{4\pi\lambda s^2 b}
                                      -J(\lambda)\right|
 \leq\frac{8R^2+6R/\lambda+6/\lambda^2}{s}.
 \tag{5}
\]

This is its stated uniform error bound, with
$2(4(\lambda R)^2+3\lambda R+3)/(\lambda^2s)$ expanded.
It applies to arbitrary bounded laws, including the translated laws here.
For every $\lambda\geq1/(2R)$, the right side is at most $44R^2/s$.
If $s\geq8R^2$, both regime conditions in (5) hold uniformly:
$\lambda^2s\geq2\geq1$ and $\lambda s\geq4R$.
Consequently (3) and (5) prove the required hinge sign whenever

\[
 0<b\leq b_*:=C_s\exp[-s/(8R^2)].
 \tag{6}
\]

Indeed any threshold in (6), however small, is represented by
$\lambda=\sqrt{2\log(C_s/b)/s}\geq1/(2R)$. Thus this step also covers
parameters $\lambda$ tending to infinity with $s$.

Researcher 8's [high-noise window](../gaussian_majorisation_high_noise_window/PROOF.md),
Theorem A, gives

\[
 H_{g_s}(b)\geq H_{f_s}(b)
 \quad\text{for }s\geq2R^2,\quad
 b\geq C_s\exp[-9s/(64R^2)].
 \tag{7}
\]

Since $9/64>1/8$, the lower endpoint in (7) is smaller than $b_*$.
The ranges (6) and (7) overlap and exhaust every positive threshold.
For $b\geq C_s$ both hinges are zero; at $b=0$ both equal one.
This proves (4). The constants come from these two estimates and
are not asserted optimal.

The high-noise window is used only in its proved threshold range.
No unrestricted positivity of the instantaneous six-dimensional lift
is assumed; the team's counterexample to that stronger claim remains valid.

## 2. A qualitative finite-support consequence

Suppose $\mu=\sum_i p_i\delta_{x_i}$ and $\nu=\sum_i p_i\delta_{y_i}$,
where $p_i>0$, $\sum_i p_i=1$, and $|y_i-y_j|\leq|x_i-x_j|$.
Repeated image locations are allowed. Put

\[
 \delta=\int_{S^2}\left(\max_i\theta\cdot x_i
                         -\max_i\theta\cdot y_i\right)d\sigma.
 \tag{8}
\]

For a noncongruent contracting pair, $\delta>0$ by the strict point-hull
mean-width theorem of
[Gorbovickis, Theorem 1.5](https://arxiv.org/html/1006.0531v2).
This is a cited geometric input, not a new assertion about unequal-radius
ball hulls. If every labelled pair distance is preserved, a Euclidean
isometry takes $x_i$ to $y_i$ and all Gaussian hinges are equal.

Let $p_{\min}=\min_i p_i$. The elementary maximum bounds give, uniformly
in $\theta$,

\[
 \lambda\max_i\theta\cdot x_i+\log p_{\min}
 \leq\log\sum_i p_i e^{\lambda\theta\cdot x_i}
 \leq\lambda\max_i\theta\cdot x_i.
 \tag{9}
\]

Using the lower bound for $x$ and upper bound for $y$ yields

\[
 J(\lambda)\geq\lambda\delta+\log p_{\min}.
 \tag{10}
\]

In particular $J(\lambda)$ tends to positive infinity for every
noncongruent finite contraction.

**Corollary 2.** A fixed finite contracting pair for which
$J(\lambda)>0$ at every $\lambda>0$ satisfies full majorisation at every
sufficiently large variance. Conversely, if $J(\lambda)<0$ at even one
positive parameter, full majorisation fails at every sufficiently large
variance.

For the first claim, $J$ is continuous, and (10) makes it coercive.
It therefore has a positive minimum on $[1/(2R),\infty)$.
Use that minimum in Theorem 1. The converse is the negative-gap part
of the cited spherical-tail theorem: at the fixed negative parameter,
(5) has an error tending to zero and a strictly positive denominator.
These are strict-sign statements. A merely nonnegative $J$ with a
positive-parameter zero is **not** covered by this corollary.

This reduces the eventual-variance question for a finite noncongruent
pair to a compact range of spherical parameters, apart from the zero case.
For example (10) guarantees $J\geq1$ when
$\lambda\geq(1+\log(1/p_{\min}))/\delta$. The team's high-noise-window
Theorem C also already proves strict positivity for $0<\lambda R<1$.
Neither fact supplies the missing middle range for an arbitrary pair.

### A martingale coupling sufficient condition

**Corollary 3.** A finite contracting pair admits eventual full
majorisation if, after separate Euclidean isometries of the two laws,
there is a coupling $(U,V)$ of its input and output laws satisfying
$\mathbb E[U\mid V]=V$. In particular this covers finite contracting pairs
with such a martingale certificate of convex order.

To prove it, assume the pair is noncongruent; the congruent case was
handled above. With independent copies define

\[
 D=\mathbb E\big[|X-X'|^2-|Y-Y'|^2\big]>0.
 \tag{11}
\]

The strict inequality follows because all weights are positive and
at least one labelled distance strictly decreases. Pair distances and
$S$ are unchanged by the separate isometries. The martingale condition
gives equal means, and

\[
 \mathbb E|U-V|^2
  =\mathbb E|U|^2-\mathbb E|V|^2
  =\operatorname{tr}\operatorname{Cov}(U)
                 -\operatorname{tr}\operatorname{Cov}(V)=D/2>0.
 \tag{12}
\]

Let $M=\mathbb E[(U-V)(U-V)^T]$. Outside the proper null subspace of the
nonzero positive-semidefinite matrix $M$,
$\mathbb E[(\theta\cdot(U-V))^2]>0$. Conditional strict Jensen gives

\[
 \mathbb E e^{\lambda\theta\cdot U}>
 \mathbb E e^{\lambda\theta\cdot V}
 \qquad(\lambda>0)
 \tag{13}
\]

for almost every $\theta$ on the sphere; weak Jensen holds everywhere.
Taking logarithms and averaging proves $J(\lambda)>0$ at every positive
parameter. Corollary 2 applies.

For finite laws this sufficient hypothesis can be witnessed by a
nonnegative matrix $\pi_{ij}$ with row sums $p_i$, column sums $p_j$, and
$\sum_i\pi_{ij}u_i=p_jv_j$ for each column. No transport solver or
unproved existence of that matrix is invoked here. This is a substantive
coupling assumption, not a consequence we infer from contraction alone.

## 3. A class with an arbitrary solid tetrahedron background

Put

\[
 u_0=(1,1,1),\quad u_1=(1,-1,-1),\quad
 u_2=(-1,1,-1),\quad u_3=(-1,-1,1),\qquad
 K=\operatorname{conv}\{u_0,u_1,u_2,u_3\}.
 \tag{14}
\]

Let $r>0$, and let $\rho$ be **any** probability measure supported in
the solid tetrahedron $rK$. For $0<\alpha\leq1$ define

\[
 P_r=\frac1{12}\sum_{i\ne j}\delta_{r(u_j-u_i)},\qquad
 Q_r=\frac1{12}\sum_{i\ne j}\delta_{r(u_j+u_i)}
     =\frac16\sum_{k=1}^3(\delta_{2re_k}+\delta_{-2re_k}),
 \tag{15}
\]
\[
 \mu=(1-\alpha)\rho+\alpha P_r,\qquad
 \nu=(1-\alpha)\rho+\alpha Q_r.
 \tag{16}
\]

Thus the source has twelve uniform difference vertices in addition to
an arbitrary fixed background. The output has the corresponding six
axis vertices. The background may be atomic, continuous, asymmetric,
or supported throughout the solid tetrahedron.

**Theorem 4.** The pair (16) is related by a 1-Lipschitz map, and satisfies

\[
 \boxed{\quad
 s\geq \frac{352(150-99\alpha)}{\alpha}\,r^2
 \quad\Longrightarrow\quad
 \mu*\gamma_s\preceq\nu*\gamma_s .
 \quad}
 \tag{17}
\]

The variance bound works for every background $\rho$ in the stated class.
No dominant origin atom or smallness assumption on $\alpha$ is imposed.
The bound is deliberately conservative. For $\alpha=0$ or $r=0$,
the laws agree, so all variances work.

### 3.1 The map fixes the entire tetrahedron

Define $T$ to be the identity on $rK$ and

\[
 T(r(u_j-u_i))=r(u_j+u_i),\qquad i\ne j.
 \tag{18}
\]

The twelve source vertices are distinct and lie outside $rK$, so this
definition is unambiguous. In fact $u_i\cdot(u_j-u_i)=-4$, whereas
$u_i\cdot z\geq-1$ for $z\in K$. Since
$u_i\cdot u_j=4\delta_{ij}-1$, the squared-distance loss between two flap
labels is exactly

\[
 |r(u_j-u_i)-r(u_l-u_k)|^2
 -|r(u_j+u_i)-r(u_l+u_k)|^2
 =16r^2(\mathbf1_{j=k}+\mathbf1_{l=i})\geq0.
 \tag{19}
\]

For $z=r\sum_k t_ku_k\in rK$, where $t_k\geq0$ and $\sum_k t_k=1$,
the loss between a flap and $z$ is

\[
 |r(u_j-u_i)-z|^2-|r(u_j+u_i)-z|^2=16r^2t_i\geq0.
 \tag{20}
\]

Distances between background points are preserved. Thus (18) is
1-Lipschitz on $rK$ together with the twelve flap vertices. Kirszbraun's
extension theorem supplies a global 1-Lipschitz map on $\mathbb R^3$.
Its pushforward of (16)'s input is precisely (16)'s output.

Both laws are supported in $B(0,R)$ with $R=\sqrt8\,r$.
This is also a valid input support ball for the high-noise-window
theorem; $T(0)=0$.

### 3.2 An exact exponential comparison

For $z\in\mathbb R^3$, write

\[
 B(z)=\int e^{z\cdot(x/r)}\,d\rho(x),\quad
 F(z)=\frac1{12}\sum_{i\ne j}e^{z\cdot(u_j-u_i)},\quad
 G(z)=\frac1{12}\sum_{i\ne j}e^{z\cdot(u_j+u_i)}.
 \tag{21}
\]

Let $c_k=\cosh(2z_k)$, $v_k=c_k-1\geq0$, and $V=v_1+v_2+v_3$.
Directly grouping the coordinates of the twelve vertices gives

\[
 F=\frac{c_1c_2+c_1c_3+c_2c_3}{3},\qquad
 G=\frac{c_1+c_2+c_3}{3},
 \tag{22}
\]
\[
 \frac FG
 =\frac{3+2V+v_1v_2+v_1v_3+v_2v_3}{3+V}
 \geq\frac{3+2V}{3+V},\qquad
 1-\frac GF\geq\frac V{3+2V}.
 \tag{23}
\]

We also need a bound uniform in the background:

\[
 B(z)\leq3F(z).
 \tag{24}
\]

For completeness this follows from a finite Jensen certificate.
Fix an anchor $u_i$. Give weight $1/4$ to each of the three difference
vertices $u_i-u_j$ with $j\ne i$, weight $1/24$ to each of the six
vertices $u_b-u_a$ with $a,b\ne i$ and $a\ne b$, and weight zero to the
other three vertices. These weights sum to one and their barycenter is
$u_i$: the first three vertices sum to $4u_i$, while the other six sum
to zero. Every weight is at most $1/4=3/12$. Jensen gives
$\exp(z\cdot u_i)\leq3F(z)$. Convexity at every point of $K$, followed
by integration against $\rho$, proves (24).

The moment-generating functions of (16), at $\lambda\theta$, equal
$(1-\alpha)B(z)+\alpha F(z)$ and $(1-\alpha)B(z)+\alpha G(z)$,
where $z=\lambda r\theta$. Their ratio satisfies

\[
 \begin{aligned}
 \frac{(1-\alpha)B+\alpha F}{(1-\alpha)B+\alpha G}
 &=1+\frac{\alpha(F-G)}{(1-\alpha)B+\alpha G}\\
 &\geq1+\frac{\alpha}{3-2\alpha}\left(1-\frac GF\right)\\
 &\geq1+\frac{\alpha}{3-2\alpha}
                     \frac{2r^2\lambda^2}{3+4r^2\lambda^2}.
 \end{aligned}
 \tag{25}
\]

The first inequality uses (24) and $G\leq F$. For the last one,
$\cosh t\geq1+t^2/2$ implies $V\geq2|z|^2=2r^2\lambda^2$,
and $V/(3+2V)$ is increasing. Taking logarithms and averaging proves

\[
 J(\lambda)\geq
 \log\left(1+\frac{\alpha}{3-2\alpha}
                     \frac{2r^2\lambda^2}{3+4r^2\lambda^2}\right).
 \tag{26}
\]

This is a pointwise exponential comparison before spherical averaging;
no numerical spherical quadrature is involved.

At $\lambda\geq1/(2R)$, with $R^2=8r^2$, we have
$r^2\lambda^2\geq1/32$. Hence (26) supplies Theorem 1 with

\[
 \kappa=\log\left(1+\frac{\alpha}{50(3-2\alpha)}\right)>0.
 \tag{27}
\]

Finally, $\log(1+t)\geq t/(1+t)$ for $t\geq0$, as follows by
integrating $1/(1+u)$ from zero to $t$. Therefore

\[
 \kappa\geq\frac{\alpha}{150-99\alpha},\qquad
 \frac{44R^2}{\kappa}
 \leq\frac{352(150-99\alpha)}{\alpha}r^2.
 \tag{28}
\]

The right side is at least $17952r^2$, so it also exceeds $8R^2=64r^2$.
Theorem 1 proves (17).

For comparison, if the background is uniform on the four anchors,
the stronger bound $B\leq F$ follows by averaging the Jensen inequality
from $u_i=(\sum_{j\ne i}(u_i-u_j)+0)/4$. Since $F\geq1$, this gives
$B\leq3F/4+1/4\leq F$. The same proof then permits
$s\geq352(50+\alpha)r^2/\alpha$.
This refinement is not needed for the arbitrary-background statement.

### 3.3 An explicit martingale interpretation

There is a coupling of $P_r$ and $Q_r$ witnessing their convex order.
For a target point $2r\eta e_k$, $\eta\in\{-1,1\}$, choose uniformly
from the four source difference vertices whose $k$-th coordinate is
$2r\eta$. Their mean is the target point. Each source vertex has two
nonzero coordinates and therefore receives marginal probability
$2(1/6)(1/4)=1/12$. Joining this coupling with the identity coupling of
$\rho$ gives $\mathbb E[U\mid V]=V$ for (16).

For a finite background, Corollary 3 provides an alternative qualitative
route to eventual majorisation. Estimate (26) is stronger for this
application: it covers arbitrary bounded background laws and gives
the uniform variance bound without a mean-width calculation.

## 4. Scope and the remaining obligation

This closes the entire hinge range in an eventual-variance regime,
using the two complementary analytic estimates. It does not infer
majorisation from finitely many moments, entropy stability, or an
uncontrolled inverse of a positive lift profile.

The arbitrary-background family extends the previously examined
uniform-anchor quartic family from a fixed degree to every convex
energy, in the stated high-variance regime, and allows arbitrary laws
on the solid tetrahedron. Researcher 7's balanced-ray theorem already
settles $\alpha=1$ at every variance; that special case is not new here.
The fixed background points can lie outside that theorem's ray support.
Researcher 6's nested-hull theorem concerns a sufficiently small
perturbing mass around an origin atom at each fixed variance.
No such atom is required here and the quantifiers differ.

At the final source refresh, researcher 6's
[fixed-core theorem](../gaussian_majorisation_fixed_core/PROOF.md)
also became available. It proves all-variance majorisation for a different,
nonuniform balance class on the rays, with arbitrary tetrahedral background,
and all-radius ball-volume comparisons for the same supports. Its additive
balances exclude uniform flap weights. It moreover proves that, when all
four anchors are fixed, the positive-definite second-moment loss excludes
every core-fixing rank-five realization of the uniform flap output law.
Thus Theorem 4 closes a high-variance portion of that explicitly remaining
Gaussian case; it does not duplicate its all-variance balanced theorem.

The remaining task for this class is the complementary range of
variances, particularly the small-variance regime. Rescaling preserves
$s/r^2$, so (17) cannot be rescaled into an all-variance theorem.
The corresponding support-level ball-volume comparison is already covered
by the new fixed-core theorem, using a different full-support weighting.
Consequently solving the remaining uniform-weight Gaussian case would
not by itself give a new KP conclusion for those same supports.
No ball-volume inequality is derived or claimed here.

For general finite contraction pairs, the concrete analytical obligation
is strict positivity of $J$ in the remaining compact parameter range,
or an analysis of any nonnegative zero. A strict negative would transfer
to a genuine Gaussian counterexample. That counterexample search belongs
to the complementary team lane.

The accompanying exact checker verifies the finite geometric and Jensen
certificates, exponential-sum identities as Laurent polynomials, and
the constants and overlap arithmetic. The universal statements rest on
this written proof and the explicitly cited analytic dependencies.
The checks are not independent peer review or formalization.
