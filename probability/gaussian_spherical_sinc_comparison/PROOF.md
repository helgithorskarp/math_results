# A spherical comparison theorem in dimension three

Author proof, 27 September 2026. Independent review is pending.

We prove that every bounded contraction in $\mathbb R^3$ has nonnegative
spherical log-moment gap, with an explicit positive lower bound whenever
average squared distance decreases. Combined with the team's independently
accepted endpoint theorem, this gives full Gaussian-convolution majorisation
at every sufficiently large variance for **every fixed finite contraction**.
We also obtain contraction monotonicity of the mean width of convex hulls of
balls with arbitrary individual radii in $\mathbb R^3$. A scaling corollary
extends eventual majorisation to all bounded laws under every uniform
Lipschitz bound strictly below one, with an explicit uniform variance bound.

The proof uses a positive divided difference of commuting spherical-mean
operators. It does not require an intermediate contracting motion, a
martingale coupling, a weight floor for the spherical comparison, or any
of the campaign's contact-event assumptions.

## 1. Precise statements and normalizations

Let $\sigma$ be probability area measure on $S^2$. For a bounded probability
measure $\mu$ and a 1-Lipschitz map $T:\mathbb R^3\to\mathbb R^3$, write
$\nu=T_\#\mu$ and

\[
 J(\lambda)=\int_{S^2}\left[
       \log\int e^{\lambda\theta\cdot x}\,d\mu(x)
       -\log\int e^{\lambda\theta\cdot T(x)}\,d\mu(x)\right]d\sigma(\theta).
 \tag{1}
\]

Let $X,X'$ be independent with law $\mu$ and put

\[
 d(x,x')=|x-x'|^2-|T(x)-T(x')|^2,\qquad
 D=\mathbb E\,d(X,X')\geq0.
 \tag{2}
\]

Translate the two configurations separately into $B(0,R)$, where $R>0$.
This is possible using a source containing ball $B(a,R)$ and its image
center $T(a)$. These translations change neither $J$ nor the pair losses.

**Theorem A (universal spherical sign).** For every $\lambda>0$,

\[
 \boxed{\quad J(\lambda)\ \geq\
              \frac{\lambda^2D}{12}e^{-4\lambda R}.\quad}
 \tag{3}
\]

In particular, $J(\lambda)>0$ at every positive parameter if $D>0$.
If $D=0$, $T$ is an isometry on $\operatorname{supp}\mu$, up to an ambient
Euclidean isometry, and $J$ vanishes identically. No atom-weight floor,
covariance floor, or small-loss condition is assumed in (3).

**Theorem B (every finite contraction is eventually majorising).**
Let $\mu=\sum_{i=1}^N w_i\delta_{p_i}$, $w_i>0$, $\sum_iw_i=1$,
and $\nu=\sum_iw_i\delta_{q_i}$, where
$|q_i-q_j|\leq|p_i-p_j|$. There is $s_0<\infty$ such that
for every $s\geq s_0$ and every $b\geq0$,

\[
 \int(\nu*\gamma_s-b)_+\,dx
       \ \geq\ \int(\mu*\gamma_s-b)_+\,dx,
 \qquad
 \gamma_s(x)=(2\pi s)^{-3/2}e^{-|x|^2/(2s)}.
 \tag{4}
\]

Thus the source convolution is majorised by the image convolution.
The bound in Section 5 is explicit in the data; it is not uniform over
all finite contractions. The theorem does not assert (4) at every variance.

**Theorem C (arbitrary-radius ball-hull mean width).** For the same finite
contracting configurations and arbitrary real numbers $r_1,\ldots,r_N$,

\[
 \int_{S^2}\max_i(r_i+\theta\cdot p_i)\,d\sigma(\theta)
 \ \geq\
 \int_{S^2}\max_i(r_i+\theta\cdot q_i)\,d\sigma(\theta).
 \tag{5}
\]

For nonnegative $r_i$, twice these integrals are the mean widths of
$\operatorname{conv}\bigcup_i B(p_i,r_i)$ and
$\operatorname{conv}\bigcup_i B(q_i,r_i)$, respectively.
This is a Kneser--Poulsen-type statement about convex-hull mean width.
It is not a union-volume or intersection-volume inequality.

**Theorem D (all uniform strict contractions, including diffuse laws).**
Let $|X-\mathbb EX|\leq R$, $V=\mathbb E|X-\mathbb EX|^2>0$, and let
$T$ have Lipschitz constant at most $c$, where $0<c<1$. Then (4) holds
for every threshold and every

\[
 \boxed{\quad s\geq\frac{4224R^4}{(1-c)V}.\quad}
 \tag{6}
\]

There is no atom-count, minimum-weight, covariance-eigenvalue, or martingale
hypothesis. The cutoff is uniform over laws of centered radius at most $R$,
scatter at least $V$, and maps of Lipschitz constant at most $c<1$.
The case $c=0$ is covered by the same bound by treating the image as a point.
This improves R2's strong-contraction factor to the actual Lipschitz
constant, as explained in Section 6.

## 2. A positive algebraic divided difference

View $P=(p_i)$ and $Q=(q_i)$ as $N$-by-$3$ real matrices. On functions
of $c=(c_1,\ldots,c_N)\in\mathbb R^N$, define

\[
 \begin{split}
 M_P(t)\phi(c)&=\int_{S^2}\phi(c+tP\theta)\,d\sigma(\theta),\\
 \Delta_P&=\sum_{a=1}^3\left(\sum_i p_{ia}\partial_{c_i}\right)^2.
 \end{split}
 \tag{7}
\]

All these constant-coefficient operators commute on polynomials.
The matrices need not have full rank; no inverse is used.

**Lemma 1.** For $t>0$ and $\phi\in C^2(\mathbb R^N)$,

\[
 M_P(t)\phi(c)-M_Q(t)\phi(c)
   =\frac1t\int_0^t r(t-r)
      M_P(t-r)M_Q(r)(\Delta_P-\Delta_Q)\phi(c)\,dr.
 \tag{8}
\]

The right side is a positive average of the function
$(\Delta_P-\Delta_Q)\phi$. The kernels themselves do not depend on
$\phi$, on the pair-distance ordering, or on an interpolation of Gram
matrices of rank at most three.

**Proof.** A coordinate of a uniform point of $S^2$ is uniform on
$[-1,1]$. Rotational invariance therefore gives, for each polynomial,
the finite operator expansion

\[
 M_P(t)=\sum_{k\geq0}\frac{t^{2k}\Delta_P^k}{(2k+1)!}.
 \tag{9}
\]

One can verify (9) first on powers of linear forms, using
$\mathbb E(\theta\cdot v)^{2k}=|v|^{2k}/(2k+1)$; such powers
span each homogeneous polynomial space by polarization.

Substitute (9) into the right side of (8). The coefficient of
$\Delta_P^i\Delta_Q^j(\Delta_P-\Delta_Q)$ is

\[
 \frac1{t(2i+1)!(2j+1)!}
  \int_0^t(t-r)^{2i+1}r^{2j+1}\,dr
   =\frac{t^{2i+2j+2}}{(2i+2j+3)!}.
 \tag{10}
\]

The beta integral in (10) is elementary repeated integration by parts.
For commuting $A,B$ the polynomial identity

\[
 (A-B)\sum_{i+j=k-1}A^iB^j=A^k-B^k
 \tag{11}
\]

now telescopes the right side into the difference of (9). This proves
(8) for every polynomial, without an infinite-series convergence argument.

To pass to $C^2$, fix $c,t,P,Q$ and a compact box whose interior contains
all $c+(t-r)P\theta+rQ\eta$, $0\leq r\leq t$, $\theta,\eta\in S^2$,
and the two separate endpoint spheres. Polynomials approximate $\phi$
and all its derivatives through order two uniformly on that box.
For completeness, apply tensor-product Bernstein polynomials after
affinely mapping a slightly larger box to $[0,1]^N$. Derivatives of order
at most two are Bernstein averages of the corresponding scaled forward
differences; the forward differences converge uniformly to the continuous
derivatives, and the binomial averages converge uniformly to each
continuous function. This proves the stated simultaneous approximation.
Both sides of (8) are continuous for this $C^2$ norm; the total scalar
weight on its right side is $t^2/6$. Taking the limit proves (8).
The approximating polynomials need not preserve any sign condition. $\square$

This is the commuting-operator form of the classical
Kirchhoff/Duhamel identity for the three-dimensional wave equation:
$tM_P(t)$ is its sine propagator, satisfying
$(tM_P(t))''=\Delta_P(tM_P(t))$. The proof above is finite algebra plus
approximation and needs no wave-equation uniqueness theorem.
On Fourier characters, $M_P(t)$ has multiplier
$\operatorname{sinc}(t|P^T\xi|)$, with $\operatorname{sinc}(0)=1$.
We assert positivity of the averaging operators in (8), not pointwise
positivity of the sinc multiplier. The same formula with uniform
$S^{d-1}$ averages is not asserted for $d\ne3$.

## 3. Submodularity gives the sign

Assume $\phi(c+a\mathbf1)=\phi(c)+a$ and
$\partial_{c_i c_j}\phi\leq0$ for $i\ne j$.
Differentiating the equivariance shows that every Hessian row sums to zero.
Set

\[
 K_{ij}=p_i\cdot p_j-q_i\cdot q_j,\qquad
 \delta_{ij}=|p_i-p_j|^2-|q_i-q_j|^2=K_{ii}+K_{jj}-2K_{ij}.
 \tag{12}
\]

Consequently

\[
 (\Delta_P-\Delta_Q)\phi
    =\sum_{i,j}K_{ij}\phi_{ij}
    =-\frac12\sum_{i,j}\delta_{ij}\phi_{ij}
    =-\sum_{i<j}\delta_{ij}\phi_{ij}.
 \tag{13}
\]

Every term in the last sum is nonnegative under contraction. Inserting
(13) into the positive average (8) proves

\[
 \boxed{\quad M_P(t)\phi(c)\geq M_Q(t)\phi(c)
           \quad\text{for every }t\geq0,\ c\in\mathbb R^N.\quad}
 \tag{14}
\]

For log-sum-exp $\phi(c)=\log\sum_iw_i e^{c_i}$, put
$\pi_i(c)=w_i e^{c_i}/\sum_jw_j e^{c_j}$. Its off-diagonal Hessian is
$-\pi_i\pi_j$. With $t=\lambda$, $c=0$, and $r=\lambda u$,
(8) gives the exact identity

\[
 \boxed{\quad
 J(\lambda)=\lambda^2\int_0^1u(1-u)
   \mathbb E_{\theta,\eta}\sum_{i<j}
      \delta_{ij}\,\pi_i(z)\pi_j(z)\,du,\qquad
 z_i=\lambda[(1-u)\theta\cdot p_i+u\eta\cdot q_i].
 \quad}
 \tag{15}
\]

Here $\theta,\eta$ are independent uniform points of $S^2$.
This is a direct nonlocal sign formula. In particular, it applies to
arbitrary unequal positive priors and paired configurations of affine
rank six. It assumes no path through contracting configurations.

For the ball-hull claim take
$\phi_\beta(c)=\beta^{-1}\log\sum_i e^{\beta c_i}$ in (14), with
$c_i=r_i$ and $t=1$. It has the same equivariance and nonpositive
off-diagonal Hessian. The elementary bound

\[
 0\leq\phi_\beta(c)-\max_i c_i\leq\frac{\log N}{\beta}
 \tag{16}
\]

allows passage to $\beta\to\infty$, proving (5). The support function
of the convex hull of the indicated balls is exactly
$\max_i(r_i+\theta\cdot p_i)$. No strictness is claimed in (5):
one ball can contain all the others.

## 4. Bounded measures and a quantitative gap

The continuum counterpart of (15) is

\[
 J(\lambda)=\frac{\lambda^2}{2}\int_0^1u(1-u)
   \mathbb E_{\theta,\eta}
   \frac{\displaystyle\iint d(x,x')e^{z(x)+z(x')}\,d\mu(x)d\mu(x')}
        {\displaystyle\left(\int e^{z(x)}\,d\mu(x)\right)^2}\,du,
 \quad
 z(x)=\lambda[(1-u)\theta\cdot x+u\eta\cdot T(x)].
 \tag{17}
\]

To justify it without infinite-dimensional differentiation, approximate
$\mu$ weakly by finite probability measures supported on its compact
support, using finite partitions of diameter tending to zero and one
representative from each cell of positive mass. Apply (15) to their
images under the continuous map $T$. On the compact product of the
support, $S^2$, $S^2$, and $[0,1]$, all integrands are uniformly
continuous. The numerator integrals and the MGF integrals therefore
converge uniformly; the denominators stay uniformly bounded away from
zero. This proves (17).

After the translations in Section 1, $|z(x)|\leq\lambda R$. The
Gibbs ratio in (17) is at least $e^{-4\lambda R}D$. Since
$\int_0^1u(1-u)\,du=1/6$, (17) proves (3), including its factor $1/12$.
Equivalently, $D=2\sum_{i<j}w_iw_j\delta_{ij}$ in the finite case.

If $D=0$, nonnegativity and continuity of $d$ imply $d=0$ on
$\operatorname{supp}\mu\times\operatorname{supp}\mu$: otherwise a
product of two relatively open support neighborhoods has positive
measure and strictly positive loss. A distance-preserving map on a
subset of Euclidean space is the restriction of an ambient Euclidean
isometry. One proof chooses an affine basis of the subset, identifies
the two Gram matrices using distances, and extends the resulting
isometry of their spans orthogonally. Distances to that basis determine
every other point. Hence the Gaussian convolutions, as well as (1),
are equal up to an ambient isometry. This also covers a single-point law.

The statements extend from probability measures to positive finite
measures by normalization; Gaussian hinge integrals satisfy
$H_{Mh}(b)=M H_h(b/M)$ when $M>0$.

## 5. Removing the remaining hypothesis of the finite endpoint theorem

The team's [endpoint theorem](../gaussian_majorisation_eventual_endpoint/PROOF.md),
independently [accepted at graph height 6048](../gaussian_majorisation_eventual_endpoint_review2/README.md),
proves that

\[
 J(\lambda)\geq\eta>0\quad(\lambda\geq1/(2R))
 \quad\Longrightarrow\quad
 s\geq R^2\max\{8,44/\eta\}\ \Longrightarrow\ (4)
 \text{ at every threshold.}
 \tag{18}
\]

Its proof joins the independently audited spherical-tail estimate to
the high-noise window, uniformly in the threshold. We use this precise
accepted implication, not a fixed-threshold limit.

For a finite noncongruent pair, let

\[
 \omega=\int_{S^2}\left(\max_i\theta\cdot p_i-
                              \max_i\theta\cdot q_i\right)d\sigma(\theta)>0.
 \tag{19}
\]

Strict positivity here is the classical theorem of
[Gorbovickis, Theorem 1.5](https://arxiv.org/html/1006.0531v2), already
used and independently checked in the endpoint contribution.
It is not inferred from a potentially nonuniform limit of (15).
Put $w_{\min}=\min_iw_i$ and $L=\log(1/w_{\min})$.
The elementary maximum bounds give

\[
 J(\lambda)\geq\lambda\omega-L.
 \tag{20}
\]

Define

\[
 \lambda_0=\frac1{2R},\qquad
 \lambda_1=\max\left\{\lambda_0,\frac{1+L}{\omega}\right\},
 \qquad
 \eta=\frac{D}{48R^2}\exp(-4R\lambda_1)>0.
 \tag{21}
\]

For $\lambda_0\leq\lambda\leq\lambda_1$, (3) gives $J\geq\eta$.
For $\lambda\geq\lambda_1$, (20) gives $J\geq1\geq\eta$;
indeed $D\leq4R^2$ implies $\eta\leq1/12$.
Thus (18) proves Theorem B with the explicit sufficient bound

\[
 \boxed{\quad s_0=\frac{44R^2}{\eta}.\quad}
 \tag{22}
\]

If $D=0$, congruence gives equality at every variance.
The weight floor and strict width theorem enter only this finite
large-$\lambda$ closure, not Theorem A.

For arbitrary diffuse bounded measures under a map of Lipschitz constant
one, pointwise strictness alone does not give a positive uniform infimum
of $J$ on the unbounded parameter ray. We do not assert that unrestricted
bounded-measure version of Theorem B. Uniform strict contractions admit
the following different closure.

## 6. Every uniform Lipschitz bound below one

Write $S_Z(\lambda)=\int_{S^2}\log\mathbb E e^{\lambda\theta\cdot Z}\,d\sigma$.
It is convex in $\lambda$ and $S_Z(0)=0$. Applying Theorem A to the
1-Lipschitz map $x\mapsto T(x)/c$ gives

\[
 S_{T(X)}(\lambda)=S_{T(X)/c}(c\lambda)
       \leq cS_{T(X)/c}(\lambda)\leq cS_X(\lambda).
 \tag{23}
\]

Hence $J(\lambda)\geq(1-c)S_X(\lambda)$ at every positive parameter.
No strong damping constant is lost in this comparison.

We use the elementary scatter bound and endpoint constants from R2's
[uniform Lipschitz package](../gaussian_uniform_lipschitz_certificate/PROOF.md),
independently [accepted](../gaussian_uniform_lipschitz_review/REVIEW.md).
Here is the short bound to make the corollary self-contained.
Center $X$. For $Z=\theta\cdot X$, $\mathbb EZ=0$ and $|Z|\leq R$,
so its MGF is nondecreasing for $\lambda\geq0$.
At $\lambda_0=1/(2R)$, the elementary Taylor bound
$e^z\geq1+z+z^2/4$ for $|z|\leq1/2$ and
$\log(1+u)\geq u/2$ for $0\leq u\leq1/16$ yield

\[
 S_X(\lambda)\geq S_X(\lambda_0)
   \geq\int_{S^2}\frac{\mathbb E(\theta\cdot X)^2}{32R^2}\,d\sigma
   =\frac{V}{96R^2},\qquad \lambda\geq\lambda_0.
 \tag{24}
\]

Thus $\eta=(1-c)V/(96R^2)$ meets (18).
Since $V\leq R^2$, the $44/\eta$ branch of that endpoint dominates,
giving exactly (6). Both laws lie in radius-$R$ balls: use the source
center $\mathbb EX$ and target center $T(\mathbb EX)$.
If the map is only specified on the support, the usual Lipschitz
extension into Euclidean space supplies that anchor.
For $c=0$, $S_{T(X)}=0$ and the same argument applies directly.

The scatter estimate and the constant 4224 are prior team work.
The new input is (23) with the actual Lipschitz constant $c$ in place
of R2's dimension-three loss factor $\sqrt{27}\,c$.
This covers every $c<1$, and allows arbitrary diffuse bounded laws.
It does not allow taking $c\uparrow1$ while keeping the displayed variance
bound finite.

## 7. Evidence and remaining frontier

The proof of Lemma 1 is universal algebra and $C^2$ approximation;
the later universal claims follow by exact differentiation and compact
limits. The accompanying standard-library checker separately integrates
moments of powers of affine linear forms: 750 exact rational identities
through degree 24, including zero-rank and equal-operator cases.
Controls reject reversing the sign, dropping the kernel, and changing
the sphere dimension. These finite checks do not prove universal quantifiers.

The checker also reconstructs the valid 24-site contraction underlying
R4's [two-body screw package](../gaussian_two_body_screw_obstruction/PROOF.md).
It checks all 276 pairs, the exact cross-loss formula, paired affine
rank six, and the Gram/Hessian identity for three positive posterior
vectors, including unequal ones. Its 156 equal and 120 strict pairs
give $D>0$. Consequently (15), (3), and Theorem B apply to this entire
positive-prior fixture family. The pending claim about impossibility
of a five-dimensional contracting motion is not an input to this proof.

The unrestricted all-variance dimension-three Gaussian-majorisation
problem remains open. The new claim rules out a negative spherical
log-MGF gap, or a positive-parameter zero at positive mean loss, as a
counterexample mechanism. It supplies an unconditional finite eventual
theorem, a uniform eventual theorem for every strict Lipschitz bound,
and an arbitrary-radius convex-ball-hull mean-width comparison.
It does not certify intermediate Gaussian hinges, union or intersection
volumes in dimension three, or independent acceptance of this manuscript.
The original PDE/contact and finite-geometry checkpoints are unchanged.
