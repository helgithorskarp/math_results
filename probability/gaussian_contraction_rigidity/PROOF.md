# Rigidity and stability of Gaussian entropy under contractions

Author proof, 22 September 2026. Independently unreviewed and not formalized.
All logarithms are natural. Gaussian entropy monotonicity, including its
moment-free form, is prior work; see SOURCES.md. The contributions proposed
here are its complete equality classification, explicit quantitative rigidity,
the sharp stability exponent, and a sharp posterior bound at order infinity.

## 1. Statement

Let $n\ge1$, $s>0$, and let $\mu$ be a Borel probability measure on
$\mathbb R^n$. Let $T:\mathbb R^n\to\mathbb R^n$ be 1-Lipschitz.
Write $X\sim\mu$, $Y=T(X)$, and

$$
\gamma_{m,s}(z)=(2\pi s)^{-m/2}e^{-|z|^2/(2s)},\qquad
f=\mu*\gamma_{n,s},\quad g=(T_\#\mu)*\gamma_{n,s}.
$$

For $\alpha\in(0,\infty)\setminus\{1\}$ put
$h_\alpha(f)=(1-\alpha)^{-1}\log\int f^\alpha$;
$h_1(f)=-\int f\log f$ and $h_\infty(f)=-\log\|f\|_\infty$.
These Gaussian mixtures have bounded, positive densities, so the entropies
are bounded below. They are finite for $\alpha>1$, including infinity.
For $0<\alpha\le1$, infinity is permitted.

Set

$$
\Delta(x,x')=|x-x'|^2-|T(x)-T(x')|^2\ge0.
$$

**Theorem A (equality).** For every $\alpha\in(0,\infty]$,
$h_\alpha(f)\ge h_\alpha(g)$, the known entropy comparison.
Whenever $h_\alpha(f)<\infty$, equality holds if and only if there are
$Q\in O(n)$ and $b\in\mathbb R^n$ such that $T(x)=Qx+b$ for $\mu$-almost
every $x$. Equivalently this identity holds on $\operatorname{supp}\mu$.
No moment, density, or full-dimensional support assumption is required.
An equality of two infinite entropies is not covered. At order zero both
densities have full support and infinite support-volume entropy.

For the quantitative statement, assume $\operatorname{supp}\mu\subseteq
B(a,R)$ with $R>0$. Translations let us take $a=0$ and $T(0)=0$ without
changing any quantity below. Put

$$
D=\iint\Delta\,d\mu\,d\mu,\qquad G_\alpha=h_\alpha(f)-h_\alpha(g).
$$

Define, for finite $\alpha>0$,

$$
C_\alpha=
\begin{cases}
(2/\alpha)^n\exp(\alpha R^2/(2s)),&0<\alpha<1,\\
1,&\alpha\ge1,
\end{cases}
\qquad
c_\alpha=
\frac{\exp[-\tfrac12\max(2,\alpha)(1+R/\sqrt{s})^2]}
{2^{n+2}n!\,s\,C_\alpha},
\tag{1}
$$

and $c_\infty=e^{-4R^2/s}/(4s)$.

**Theorem B (quantitative rigidity).** For every $\alpha\in(0,\infty]$,

$$
G_\alpha\ge c_\alpha D.
\tag{2}
$$

If additionally $\operatorname{Cov}(X)\succeq\kappa I_n$, $\kappa>0$, then

$$
\inf_{Q\in O(n),\,b\in\mathbb R^n}
\mathbb E|T(X)-QX-b|^2
\le\frac{2R^2}{\kappa}D
\le\frac{2R^2}{\kappa c_\alpha}G_\alpha.
\tag{3}
$$

For each fixed $\alpha\in(0,\infty]$ and $s>0$, the resulting exponent
$1/2$ for root mean square distance cannot be replaced by any larger
exponent uniformly over laws and contractions with fixed radius and a fixed
positive lower covariance bound. This failure occurs already in dimension
one, and also in each fixed dimension by taking products.
The constants (1) are explicit sufficient constants, not claimed optimal.

**Theorem C (sharp maximum-density bound).** No boundedness or moment
assumption is needed. Choose any point $z$ maximizing $f$ and define the
posterior probability measure

$$
d\nu_z(x)=\frac{\gamma_{n,s}(z-x)}{f(z)}\,d\mu(x).
$$

Then

$$
G_\infty\ge\frac1{4s}\iint\Delta(x,x')\,d\nu_z(x)d\nu_z(x').
\tag{4}
$$

The coefficient $1/(4s)$ is optimal for this posterior-weighted inequality.

## 2. Compact input: an exact dissipation identity

We first assume $\mu$ has bounded support and $T(0)=0$.
Use the classical doubled-dimensional contraction, also used by
Aishwarya--Li:

$$
c_t(x)=\left(\frac{x+T(x)}2+\cos(\pi t)\frac{x-T(x)}2,\,
                  \sin(\pi t)\frac{x-T(x)}2\right),\quad0\le t\le1.
\tag{5}
$$

For any two input points, direct expansion gives

$$
|c_t(x)-c_t(x')|^2
=\cos^2(\pi t/2)|x-x'|^2+\sin^2(\pi t/2)|T(x)-T(x')|^2,
\tag{6}
$$

and therefore

$$
(c_t(x)-c_t(x'))\cdot(\dot c_t(x)-\dot c_t(x'))
=-\frac\pi4\sin(\pi t)\Delta(x,x').
\tag{7}
$$

In dimension $2n$ let

$$
q_t(z)=\int\gamma_{2n,s}(z-c_t(x))\,d\mu(x),\qquad
w_t(z)=\frac{\int\dot c_t(x)\gamma_{2n,s}(z-c_t(x))\,d\mu(x)}{q_t(z)}.
$$

Differentiating the Gaussian mixture gives the continuity equation
$\partial_tq_t=-\operatorname{div}(q_tw_t)$. Differentiating the posterior
expectation in space gives

$$
\operatorname{div}w_t(z)
=\frac1s\{\mathbb E_{t,z}[\dot c_t\cdot c_t]
                    -\mathbb E_{t,z}\dot c_t\cdot\mathbb E_{t,z}c_t\}
=-\frac{\pi\sin(\pi t)}{8s}\frac{M_t(z)}{q_t(z)^2},
\tag{8}
$$

where the expectations are under the posterior density
$\gamma_{2n,s}(z-c_t(x))/q_t(z)$ relative to $\mu$, and

$$
M_t(z)=\iint\Delta(x,x')\gamma_{2n,s}(z-c_t(x))
                         \gamma_{2n,s}(z-c_t(x'))\,d\mu(x)d\mu(x').
\tag{9}
$$

Indeed, covariance is half the expectation of the product of two
independent differences, and (7) applies. No spatial differentiability of
$T$, or single-valued velocity on a self-intersecting image, is needed:
the displayed posterior is defined on the original input labels.

Put $I_\alpha(t)=\int q_t^\alpha$. Integration by parts in the continuity
equation gives

$$
I_\alpha'(t)=-(\alpha-1)\int q_t^\alpha\operatorname{div}w_t,
\qquad
\frac{d}{dt}h_\alpha(q_t)
=\frac{\int q_t^\alpha\operatorname{div}w_t}{I_\alpha(t)}.
\tag{10}
$$

At $\alpha=1$ the second identity follows directly by differentiating
$-\int q_t\log q_t$, and its denominator is $I_1(t)=1$.
For precision, if the centers and their velocities are uniformly bounded,
$q_t$ has Gaussian upper and lower tail bounds, $w_t$ is bounded, and
$|\nabla q_t|/q_t+|\partial_tq_t|/q_t\le C(1+|z|)$.
The derivatives of $w_t$ are bounded by posterior covariances of bounded
quantities. Thus all differentiations are dominated by a polynomial times
$e^{-c|z|^2}$ for each fixed $\alpha>0$; for Shannon the additional
$|\log q_t|$ is at most quadratic. Applying integration by parts first
with smooth cutoffs supported on balls and sending the radius to infinity
justifies (10), including $\alpha<1$. All entropies here are finite.

At the endpoints $q_0=f\otimes\gamma_{n,s}$ and
$q_1=g\otimes\gamma_{n,s}$. Entropy additivity cancels the extra Gaussian.
Consequently, for all finite $\alpha>0$,

$$
\boxed{\quad
G_\alpha=\frac\pi{8s}\int_0^1\sin(\pi t)
 \frac{\displaystyle\int_{\mathbb R^{2n}}q_t(z)^{\alpha-2}M_t(z)\,dz}
      {\displaystyle\int_{\mathbb R^{2n}}q_t(z)^\alpha\,dz}\,dt .
\quad}
\tag{11}
$$

In particular $G_\alpha\ge0$. Formula (8) retains the pairwise distortion
in the posterior-divergence method of Aishwarya--Li rather than only its
sign. The doubled-dimensional path is prior work; neither ingredient's
qualitative monotonicity is asserted to be new.

## 3. Arbitrary input and equality at finite orders

Here is a direct truncation argument included for completeness, not a
claim of a new moment-free comparison. Let
$\mu_j=\mu|_{B(0,j)}$, $m_j=\mu(B(0,j))$, and discard any initial zero
masses. The unnormalized convolutions
$f_j=\mu_j*\gamma_{n,s}$ and $g_j=(T_\#\mu_j)*\gamma_{n,s}$ increase
pointwise to $f$ and $g$. Apply the compact comparison to $\mu_j/m_j$.
For $\alpha\ne1$, the common factors $m_j^{-\alpha}$ cancel in the
comparison of the power integrals. Monotone convergence gives the
inequality for arbitrary $\mu$, including infinite power integrals when
$0<\alpha<1$.

To handle Shannon convergence, set $M=(2\pi s)^{-n/2}$ and
$\eta_M(u)=u\log(M/u)+u$, with $\eta_M(0)=0$.
This is nonnegative and nondecreasing on $[0,M]$.
Writing $H(f_j)=-\int f_j\log f_j$,

$$
H(f_j)=\int\eta_M(f_j)-(\log M+1)m_j,\qquad
h_1(f_j/m_j)=H(f_j)/m_j+\log m_j.
\tag{12}
$$

Monotone convergence applies to the first integral. Thus normalized
Shannon entropies converge, in the extended real sense, to the endpoint
entropies. The same is true of normalized finite-order Rényi entropies
by power monotone convergence. Every entropy is bounded below by
$-\log M$, so none of these limits involves an indeterminate integral.
This proves the known arbitrary-law comparison at every finite order.

Assume now $h_\alpha(f)<\infty$. Then $h_\alpha(g)<\infty$ as well.
For each conditional law $\mu_j/m_j$ use (11). The lifted unnormalized
densities increase to $q_t$, and the unnormalized versions of (9)
increase to $M_t$. After division by $m_j$ or $m_j^2$ respectively, the
normalized versions still converge to those same limits.
The denominators in (11) converge by monotone convergence and
normalization. They are positive and finite: for $\alpha>1$ use the
uniform Gaussian density bound; for $\alpha=1$ they equal one.
For $0<\alpha<1$, compact monotonicity along (5) gives
$I_\alpha(t)\le I_\alpha(0)$ after taking the truncation limit, and the
right side is finite by endpoint tensorization and the hypothesis.

Fatou's lemma, on $(0,1)\times\mathbb R^{2n}$, now gives the lower bound
(11) with equality replaced by $\ge$. We do not assert equality in this
noncompact dissipation formula. If $\Delta>0$ on a set of positive
$\mu\otimes\mu$ measure, the strict positivity of every Gaussian factor
implies $M_t(z)>0$ for every $0<t<1$ and every $z$. The Fatou lower
bound is then strictly positive. Thus entropy equality implies
$\Delta=0$ almost everywhere.

Conversely, this last condition forces distance preservation on the entire
support: $\Delta$ is continuous and $\operatorname{supp}(\mu\otimes\mu)
=\operatorname{supp}\mu\times\operatorname{supp}\mu$.
Choose affinely independent $x_0,\ldots,x_d$ spanning the affine hull
of the support. Polarization shows that $x_i-x_0\mapsto T(x_i)-T(x_0)$
extends linearly to an isometry of the two $d$-dimensional spans.
For any other support point, its distances to these anchors fix its
projection onto the image span, while its distance to $T(x_0)$ leaves
zero squared orthogonal residual. Thus it has the same affine isometric
image. Extend orthonormal bases to obtain $Q\in O(n)$ and add the
translation $b$. The singleton case is immediate.
An ambient rigid motion preserves isotropic Gaussian entropy, proving
both implications of Theorem A at finite orders.

## 4. Explicit compact constants

By (6) with $x'=0$, all lifted centers lie in $B(0,R)\subset\mathbb R^{2n}$.
Set $U=(2\pi s)^{-n}$ and
$A=(1+R/\sqrt{s})^2/2$. On $|z|\le\sqrt{s}$, every mixture kernel lies
between $L=Ue^{-A}$ and $U$. Hence

$$
M_t(z)\ge L^2D,\qquad
q_t(z)^{\alpha-2}M_t(z)\ge
U^\alpha e^{-\max(2,\alpha)A}D.
\tag{13}
$$

For $\alpha\ge1$, $I_\alpha(t)\le U^{\alpha-1}$.
For $0<\alpha<1$, the inequality
$|z-c|^2\ge|z|^2/2-|c|^2$ gives

$$
q_t(z)\le U e^{R^2/(2s)}e^{-|z|^2/(4s)},\qquad
I_\alpha(t)\le U^{\alpha-1}(2/\alpha)^n e^{\alpha R^2/(2s)}.
\tag{14}
$$

Finally $U\,|B_{2n}(0,\sqrt{s})|=1/(2^n n!)$ and
$\int_0^1\sin(\pi t)\,dt=2/\pi$. Substitution of (13)--(14)
in (11) proves (1)--(2) for finite orders.

## 5. Order infinity, with a sharp coefficient

The convolution of a finite measure with a continuous function vanishing
at infinity is continuous and vanishes at infinity. This follows by
restricting the measure to a sufficiently large compact set and uniformly
bounding the remaining mass. Therefore $f$ attains a positive maximum at
some $z$. Its derivatives can be computed under the integral because
Gaussian derivatives are bounded. The posterior $\nu_z$ has moments of
every order: $|x|^k\gamma_{n,s}(z-x)$ is bounded for fixed $z,k$.
The equation $\nabla f(z)=0$ gives $\mathbb E_{\nu_z}X=z$.
Lipschitzness also gives finite posterior moments of $T(X)$.

Let $y=T(z)$,
$r(x)=|x-z|^2-|T(x)-y|^2\ge0$, and
$m=\mathbb E_{\nu_z}(T(X)-y)$. For every $h\in\mathbb R^n$,

$$
\frac{g(y+h)}{f(z)}
=\mathbb E_{\nu_z}\exp
 \left(\frac{r(X)+2h\cdot(T(X)-y)-|h|^2}{2s}\right)
\ge\exp\left(\frac{\mathbb E_{\nu_z}r+2h\cdot m-|h|^2}{2s}\right).
\tag{15}
$$

This is Jensen's inequality; the exponent is integrable by the posterior
moment bounds. Take $h=m$ and use

$$
\iint\Delta\,d\nu_z\,d\nu_z
=2\{\mathbb E_{\nu_z}|X-z|^2-\operatorname{Var}_{\nu_z}(T(X))\}
=2\{\mathbb E_{\nu_z}r+|m|^2\},
\tag{16}
$$

where $\operatorname{Var}$ denotes the trace of the covariance.
Equations (15)--(16) imply (4). In particular they also prove monotonicity
at infinity and, because $\nu_z$ and $\mu$ have the same null sets,
the equality characterization of Theorem A at infinity.

For compact support in $B(0,R)$, the posterior barycenter equation places
$z$ in its closed convex hull, hence $|x-z|\le2R$. Since
$f(z)\le(2\pi s)^{-n/2}$,

$$
d\nu_z/d\mu\ge e^{-2R^2/s}.
$$

Thus (4) gives $G_\infty\ge e^{-4R^2/s}D/(4s)$, as stated.

For sharpness of (4), take $n=1$, equal masses at $\pm a$ with
$0<a\le\sqrt{s}$, and $T=0$. The input density is proportional to
$e^{-(u^2+a^2)/(2s)}\cosh(au/s)$. For $u>0$ its logarithmic derivative
is $-u/s+(a/s)\tanh(au/s)\le(-1+a^2/s)u/s\le0$.
Symmetry gives a mode at zero, with posterior equal to the original law.
Here $G_\infty=a^2/(2s)$ and $\mathbb E_{\nu_z\otimes\nu_z}\Delta=2a^2$.
Equality in (4) proves the claimed optimal coefficient.

## 6. From pairwise distortion to a rigid motion

Center $X$ and $Y$. Regard their coordinate features as operators
$A,B:\mathbb R^n\to L^2(\mu)$, with
$(Au)(x)=u\cdot(x-\mathbb EX)$ and the analogous definition for $B$.
The kernel of $AA^*-BB^*$ is the difference of centered Gram kernels.
If $J$ denotes orthogonal projection in $L^2(\mu)$ off the constants,
double centering of squared distances gives

$$
H=AA^*-BB^*=-\tfrac12J\Delta J,\qquad
\|H\|_{\rm HS}^2\le\tfrac14\iint\Delta^2\,d\mu\,d\mu
\le R^2D.
\tag{17}
$$

Here $J\Delta J$ denotes the integral operator with the doubly centered
kernel, and $0\le\Delta\le4R^2$. Orthogonal projections contract the
Hilbert--Schmidt norm.

Right-multiply $B$ by an orthogonal matrix so that $A^*B$ becomes
symmetric positive semidefinite; a singular value decomposition gives
such a choice even when it is singular. This does not change $BB^*$,
and amounts exactly to allowing the orthogonal alignment in (3).
Let $U=A+B$ and $V=A-B$. Then

$$
\|H\|_{\rm HS}^2
=\tfrac12\operatorname{tr}(U^*U\,V^*V)
 +\tfrac12\operatorname{tr}((U^*V)^2).
\tag{18}
$$

Indeed $H=(UV^*+VU^*)/2$, and expansion of its squared norm gives (18).
The symmetry of $A^*B$ makes $U^*V=A^*A-B^*B$ symmetric, so the second
trace is nonnegative. Furthermore
$U^*U=A^*A+B^*B+2A^*B\succeq A^*A\succeq\kappa I_n$.
Since $V^*V$ is positive semidefinite,

$$
\|H\|_{\rm HS}^2\ge\tfrac\kappa2\|A-B\|_{\rm HS}^2.
$$

Restoring the means by a translation and using (17) proves (3).

## 7. Optimality of the stability exponent

Fix $s>0$, let $0<\varepsilon\le1/4$, and put masses
$(1-\varepsilon)/2,(1-\varepsilon)/2,\varepsilon$ at $-1,1,2$.
Let $T(x)=\max(-1,\min(1,x))$ on the real line. Direct calculation gives

$$
\operatorname{Var}(X)=1+3\varepsilon-4\varepsilon^2\ge1,\quad
D=6\varepsilon(1-\varepsilon),\quad
\inf_{Q\in\{-1,1\},b}\mathbb E|T(X)-QX-b|^2
=\varepsilon(1-\varepsilon).
\tag{19}
$$

For the last identity, $Y-X$ is zero except at the point 2, where it
is $-1$, and $\operatorname{Cov}(X,Y)=1+\varepsilon-2\varepsilon^2>0$,
so $Q=1$ is the optimal sign. The radius is the fixed number 2.

For every fixed finite $\alpha>0$, $G_\alpha=O(\varepsilon)$ as
$\varepsilon\downarrow0$. Here are the analytic details. The two
densities are respectively $(1-\varepsilon)f_0+\varepsilon\gamma_{1,s}(\cdot-2)$
and $(1-\varepsilon)f_0+\varepsilon\gamma_{1,s}(\cdot-1)$, with
$f_0=(\gamma_{1,s}(\cdot+1)+\gamma_{1,s}(\cdot-1))/2$.
They dominate $f_0/2$. For $0<\alpha<1$, the absolute derivative of
their $\alpha$ power is bounded by a constant times
$f_0^{\alpha-1}(f_0+\gamma_{1,s}(\cdot-2)+\gamma_{1,s}(\cdot-1))$.
This is integrable: each factor product has an upper bound of the form
$C\exp[-\alpha u^2/(2s)+C|u|]$. For $\alpha>1$, Gaussian upper tails
give the same integrability for the power derivative. For $\alpha=1$,
the derivative of $-f\log f$ is dominated by a quadratic polynomial
times a sum of shifted Gaussians, since $|\log f|\le C(1+u^2)$.
Thus the entropy functions are locally Lipschitz in $\varepsilon$ at
zero (the positive power integrals stay away from zero).
For $\alpha=\infty$, the sup norms are Lipschitz in $\varepsilon$ and
stay positive, so their logarithms have the same property.

Theorem B and (19) also give $G_\alpha\ge c\varepsilon$.
Consequently the entropy loss is of order $\varepsilon$ while the
optimal root mean square rigid-motion error is of order
$\sqrt{\varepsilon}$. Any proposed uniform exponent $\beta>1/2$ fails.

For dimension $n>1$, append $n-1$ independent symmetric signs and let
$T$ act only on the first coordinate. The radius is $\sqrt{n+3}$ and
the covariance is at least $I_n$. The centered cross-covariance is
diagonal positive, so the optimal orthogonal alignment is the identity;
the error in (19) is unchanged. Gaussian product entropy additivity
leaves the entropy gap unchanged as well.

## 8. Evidence and limits

The proof is analytic. Standard measure theory, elementary Gaussian
calculus, integration by parts with cutoffs, and finite-rank operator
algebra remain the unformalized trust boundary. No numerical claim is
used to infer a universal statement.

The accompanying exact verifier checks path and centering identities,
the sharpness family, finite Procrustes inequalities, and integer-order
Gaussian entropy losses using a replica formula different from the
dissipation proof. The latter losses and the displayed constants are
enclosed using rational Taylor series with explicit remainders.
This corroborates finite fixtures only. It is neither a proof assistant
formalization nor an independent research review.

This result concerns Gaussian entropy. It does not prove the geometric
Kneser--Poulsen conjecture or the arbitrary-dimensional majorization
conjecture in Aishwarya--Li's September 2026 preprint.
