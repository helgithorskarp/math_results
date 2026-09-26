# Signed Gaussian tail corrections and a deficit-stability obstruction

Author proof, 26 September 2026. Independent review and formalization are
pending. This identifies a precise obstruction to a proposed functional
bridge and supplies the next signed invariant at zeros of the spherical
test. It is **not** a counterexample to Gaussian majorisation. The explicit
examples below are injective homotheties, for which majorisation holds.

## 1. Normalization and the question about stability

Let \(\gamma_s\) have covariance \(sI_3\), let
\(C_s=(2\pi s)^{-3/2}\), and write

\[
 H_f(a)=\int_{\mathbb R^3}(f-a)_+\,dx,\qquad
 Q_f(a)=1-H_f(a)=\int\min\{f,a\}\,dx.
 \tag{1}
\]

For a bounded probability law \(\xi\), define

\[
 S_\xi(\lambda)=\int_{S^2}\log\mathbb E_\xi e^{\lambda\theta\cdot X}
       \,d\sigma(\theta),\qquad \lambda>0,                     \tag{2}
\]

where \(\sigma\) is normalized area measure. For an input/output pair
\((\mu,\nu)\), set

\[
 a_{s,\lambda}=C_s e^{-\lambda^2s/2},\qquad
 N_s(\lambda)=\frac{H_{\nu*\gamma_s}(a_{s,\lambda})
                         -H_{\mu*\gamma_s}(a_{s,\lambda})}
                        {4\pi\lambda s^2a_{s,\lambda}},
 \quad J(\lambda)=S_\mu(\lambda)-S_\nu(\lambda).
 \tag{3}
\]

The team's [spherical-tail theorem](../gaussian_majorisation_spherical_tail/PROOF.md)
proves, when both laws lie in \(B(0,R)\), that

\[
 |N_s(\lambda)-J(\lambda)|
 \le\frac{8R^2+6R/\lambda+6/\lambda^2}{s}
 \quad\text{if }\lambda^2s\ge\max\{1,4\lambda R\}.             \tag{4}
\]

For a contraction \(\nu=T_\#\mu\), its mean squared-distance loss is

\[
 D=\mathbb E[|X-X'|^2-|TX-TX'|^2]\ge0.                         \tag{5}
\]

One possible bridge from quantitative entropy rigidity to all thresholds
would strengthen (4) by replacing its fixed support-scale error with a
quantity tending to zero with \(D\), uniformly over \(\lambda\). The
next theorem rules this out, even at each fixed variance and for a fixed
strict linear contraction. It does not rule out bounds retaining a
substantial dependence on \(\lambda\), or other routes to majorisation.

## 2. A fixed-variance obstruction with an injective contraction

**Theorem A.** Fix \(s>0\), \(R>0\), \(0<\alpha<1\), and \(0<b<R\).
For \(\lambda\to\infty\), put

\[
 p=e^{-b\lambda},\qquad
 \mu_\lambda=(1-p)\delta_0+p\delta_{Re_1},\qquad
 \nu_\lambda=(1-p)\delta_0+p\delta_{\alpha Re_1}.
 \tag{6}
\]

The image map is the fixed global contraction \(T(x)=\alpha x\),
injective on the two-point support. With the pair-dependent quantities
in (3), one has

\[
 \boxed{\quad
 \lim_{\lambda\to\infty}[N_s(\lambda)-J(\lambda)]
 =-\frac b{4s}\big[(R-b)_+-(\alpha R-b)_+\big]<0.
 \quad}                                                       \tag{7}
\]

In particular, take \(\alpha=1/4\), \(b=R/2\),
\(p_m=2^{-m}\), and \(\lambda_m=2m\log2/R\). Then, at every fixed
\(s>0\),

\[
 \boxed{\quad s[N_s(\lambda_m)-J(\lambda_m)]\longrightarrow-R^2/16,
 \qquad D_m=\frac{15}{8}p_m(1-p_m)R^2\longrightarrow0.\quad}     \tag{8}
\]

Thus there is no bound
\(|N_s(\lambda)-J(\lambda)|\le\omega(D)\), uniform in bounded
contraction pairs and all sufficiently large \(\lambda\), for **any**
function \(\omega(d)\to0\), even if that function depends on the
fixed \(R,s\). In particular a uniform bound \(CD/s\), or any
positive power of \(D\) in its place, is impossible. The support-scale
order \(R^2/s\) in (4) cannot be replaced uniformly by a coefficient
vanishing with the contraction deficit. No optimal constant in (4) is
claimed.

### 2.1 A single moving-weight law

We prove (7) by treating
\(\xi_\lambda=(1-e^{-b\lambda})\delta_0+e^{-b\lambda}\delta_{re_1}\)
for any fixed \(r>0,b>0\). Set \(f_\lambda=\xi_\lambda*\gamma_s\)
and \(a=a_{s,\lambda}\). We claim

\[
 \frac{Q_{f_\lambda}(a)}{4\pi\lambda s^2a}
 =\frac{s\lambda^2}{3}+1+S_{\xi_\lambda}(\lambda)
       -\frac{b(r-b)_+}{4s}+o(1).                             \tag{9}
\]

The remainder tends to zero with \(r,b,s\) fixed. This is a
moving-weight, fixed-variance limit; it is not obtained by substituting
varying parameters into a fixed-law expansion.

Write \(z=\theta\cdot e_1\). Under normalized area measure on \(S^2\),
\(z\) is uniform on \([-1,1]\). For large \(\lambda\), the
superlevel set of \(f_\lambda\) is a radial graph with radius

\[
 \rho_\lambda(\theta)=s\lambda+d_\lambda(z),\qquad |d_\lambda(z)|\le r.
 \tag{10}
\]

Indeed the Gaussian distance bounds put its boundary between
\(s\lambda-r\) and \(s\lambda+r\). Every smaller radius is above
the level; outside radius \(r\), the radial logarithmic derivative is
at most \(-(\rho-r)/s<0\). Once \(s\lambda>2r\), these facts give
one boundary on each ray and no missing inner component.

At that boundary the exact equation is

\[
 \lambda d_\lambda
 =\log\left[1-e^{-b\lambda}+
  \exp\left(\lambda(rz-b)+\frac{r d_\lambda z-r^2/2}{s}\right)\right]
       -\frac{d_\lambda^2}{2s}.                              \tag{11}
\]

Put \(h(z)=(rz-b)_+\). For \(p=e^{-b\lambda}\le1/2\), the
elementary estimate of log-sum-exp by the larger exponent, together with
(10), gives the uniform bound

\[
 |\lambda(d_\lambda-h)|\le2\log2+2r^2/s.                     \tag{12}
\]

For example, replacing \(\log(1-p+e^{x+A})\) by \(x_+\) costs
at most \(|\log(1-p)|+|A|+\log2\); here
\(|A|\le3r^2/(2s)\), and the remaining quadratic costs at most
\(r^2/(2s)\). In particular \(d_\lambda\to h\) uniformly.
Equation (11), at each \(z\ne b/r\), then implies

\[
 \lambda(d_\lambda-h)\longrightarrow
 \begin{cases}
 (rh z-r^2/2-h^2/2)/s,&rz>b,\\
 0,&rz<b.
 \end{cases}                                                 \tag{13}
\]

The first case follows by dominance of the rare exponential, and the
second by convergence of the logarithm to zero. The exceptional latitude
has spherical measure zero, including when \(b=r\). Bound (12)
justifies integration of these limits by dominated convergence.

### 2.2 The signed constant comes from radial volume

The normalized volume term in \(Q_f(a)\) is

\[
 \int_{S^2}\frac{(s\lambda+d_\lambda)^3}{3s^2\lambda}\,d\sigma
 =\frac{s\lambda^2}{3}
       +\lambda\mathbb E_z d_\lambda
       +\frac{\mathbb E_z d_\lambda^2}{s}+o(1).               \tag{14}
\]

Also, with \(L_\lambda(z)=\log(1-e^{-b\lambda}+e^{\lambda(rz-b)})\),

\[
 S_{\xi_\lambda}(\lambda)=\mathbb E_zL_\lambda(z),\qquad
 \mathbb E_z[L_\lambda-\lambda h]\longrightarrow0.             \tag{15}
\]

The latter follows pointwise away from the exceptional latitude, with
the uniform bound \(2\log2\). Combining (13)--(15), the constant
left after subtracting \(s\lambda^2/3+S_{\xi_\lambda}(\lambda)\)
from (14) is zero if \(b\ge r\). If \(0<b<r\), it is

\[
 \begin{aligned}
 &\frac1{2s}\int_{b/r}^1
   \left(\frac32r^2z^2-2rbz+\frac12b^2-\frac12r^2\right)dz\\
 &\hspace{35mm}=-\frac{b(r-b)}{4s}.                           \tag{16}
 \end{aligned}
\]

This elementary signed integral is the source of the nonzero limit.

### 2.3 The exterior mass contributes only a common constant

For any law in \(B(0,r)\), at its boundary \(\rho=s\lambda+d\)
with \(|d|\le r\), radial differentiation gives, for \(w\ge0\),

\[
 e^{-(\rho+r)w/s-w^2/(2s)}
 \le\frac{f((\rho+w)\theta)}a
 \le e^{-(\rho-r)w/s-w^2/(2s)}.                              \tag{17}
\]

Consequently the exterior mass on that ray, divided by
\(a s^2\lambda\), equals an integral which, on setting
\(v=\lambda w\), tends to \(\int_0^\infty e^{-v}dv=1\).
This convergence is uniform in direction and in the bounded law:
for \(s\lambda\ge4r\), the upper exponential is at most
\(e^{-v/2}\), and the factor
\((\rho+v/\lambda)^2/(s^2\lambda^2)\) is bounded by a fixed
multiple of \((1+v)^2\) once \(s\lambda^2\ge1\). These integrable
bounds justify the limit, while both exponential bounds in (17) have
the same pointwise limit. Combining with (14)--(16) proves (9).
Subtract (9) for \(r=R\) and \(r=\alpha R\), using (1), to prove (7).

### 2.4 The example is also close in entropy and ordinary distance

The original coupling gives
\(W_1(\mu_\lambda,\nu_\lambda)\le p(1-\alpha)R\to0\).
For fixed \(s\), write differential entropy as \(h(f)=-\int f\log f\).
Translation-mixture concavity gives \(h(\nu_\lambda*\gamma_s)\ge h(\gamma_s)\).
For the centered input convolution, nonnegativity of relative entropy
to \(\gamma_s\) gives

\[
 h(\mu_\lambda*\gamma_s)-h(\gamma_s)
 \le \frac{p(1-p)R^2}{2s}.                                  \tag{18}
\]

The finite Gaussian-mixture entropies are well-defined. The map
\(x\mapsto\alpha x\) admits a continuous contracting motion, so
its entropy gap has the usual nonnegative sign; alternatively the
one-dimensional theorem applies to the nontrivial coordinate. Hence

\[
 0\le h(\mu_\lambda*\gamma_s)-h(\nu_\lambda*\gamma_s)
 \le\frac{p(1-p)R^2}{2s}\longrightarrow0.                     \tag{19}
\]

Thus an entropy modulus cannot repair the failed uniform estimate either.
This concerns the **normalized** error (3); its denominator tends rapidly
to zero. It does not contradict continuity or known rigidity bounds for
the unnormalized hinges. In fact both densities converge in \(L^1\)
to \(\gamma_s\), and the original majorisation is true at every threshold.

## 3. The next signed coefficient for a fixed law

We now keep the law and \(\lambda>0\) fixed and let \(s\to\infty\).
For a bounded law \(\xi\), let

\[
 L(\lambda,\theta)=\log\mathbb E e^{\lambda\theta\cdot X},\quad
 \dot L=\partial_\lambda L,\quad
 B(\lambda,\theta)=
   \frac{\mathbb E|X|^2e^{\lambda\theta\cdot X}}
        {\mathbb E e^{\lambda\theta\cdot X}}.
\]

Define the signed functional

\[
 \boxed{\quad
 \mathcal C_\xi(\lambda)=\int_{S^2}
 \left[-\frac B2+\frac{(L+1)\dot L}{\lambda}
                   +\frac{L^2/2+L}{\lambda^2}\right]d\sigma.
 \quad}                                                       \tag{20}
\]

**Theorem B.** Uniformly over laws in \(B(0,R)\), for \(\lambda\)
in any fixed compact subinterval of \((0,\infty)\),

\[
 \frac{Q_{\xi*\gamma_s}(a_{s,\lambda})}{4\pi\lambda s^2a_{s,\lambda}}
 =\frac{\lambda^2s}{3}+1+S_\xi(\lambda)
       +\frac1s\left[\frac1{\lambda^2}+\mathcal C_\xi(\lambda)\right]
       +O(s^{-2}).                                           \tag{21}
\]

The implicit constant depends only on \(R\) and that compact interval.
It is not asserted uniform as \(\lambda\to\infty\).
For a pair, subtracting gives

\[
 N_s(\lambda)=J(\lambda)
    +\frac{\mathcal C_\mu(\lambda)-\mathcal C_\nu(\lambda)}s
    +O(s^{-2}).                                               \tag{22}
\]

*Proof.* Put \(t=1/s\), and define
\(F_t(u,\theta)=\log\mathbb E\exp(u\theta\cdot X-t|X|^2/2)\).
The radial boundary is \(\rho=su\), where

\[
 u^2=\lambda^2+2tF_t(u,\theta).
\]

Its derivative with respect to \(u\) at \(t=0,u=\lambda\) is
\(2\lambda>0\). Uniform implicit Taylor expansion gives

\[
 u=\lambda+t\frac L\lambda
     +t^2\left[-\frac B{2\lambda}
               +\frac{L\dot L}{\lambda^2}
               -\frac{L^2}{2\lambda^3}\right]+O(t^3).         \tag{23}
\]

Here \(\partial_tF_t|_0=-B/2\). Its normalized volume term
\(u^3/(3\lambda t)\) is therefore

\[
 \frac{\lambda^2}{3t}+L
    +t\left[-\frac B2+\frac{L\dot L}{\lambda}
                           +\frac{L^2}{2\lambda^2}\right]+O(t^2).
 \tag{24}
\]

For the exterior mass use \(\rho+w\), with \(w\ge0\). Its
normalized value on the ray is exactly

\[
 I(t)=\int_0^\infty\frac{(u+tw)^2}{\lambda}
 e^{-uw-tw^2/2+F_t(u+tw,\theta)-F_t(u,\theta)}\,dw.
 \tag{25}
\]

At \(t=0\), \(I(0)=1\). Using \(u'(0)=L/\lambda\), its
first derivative is the integral of

\[
 e^{-\lambda w}\left[2L/\lambda+2w
    +\lambda(\dot L-L/\lambda)w-\lambda w^2/2\right].
\]

The elementary exponential moments give

\[
 I(t)=1+t\left[\frac L{\lambda^2}
                     +\frac{\dot L}{\lambda}+\frac1{\lambda^2}\right]
              +O(t^2).                                      \tag{26}
\]

For rigor, all derivatives of \(F_t\) needed in (23)--(26) are bounded
uniformly by constants depending only on \(R\), because they are
moments or cumulants of the bounded variables \(\theta\cdot X\) and
\(|X|^2/2\) under positive real exponential tilts. The implicit
derivatives of \(u\) are also uniformly bounded on the stated compact
\(\lambda\)-interval, for sufficiently small \(t\ge0\).
For (25), \(|\partial_uF_t|\le R\) and \(u-tR\ge\lambda/2\)
for small \(t\). Differentiating its integrand up to order two is
then dominated by a fixed polynomial in \(w\) times
\(e^{-\lambda w/2}\). The remaining Gaussian factor is at most one.
One-sided Taylor expansion under the integral is therefore justified,
including its uniform \(O(t^2)\) remainder. Summing (24) and (26),
then averaging, proves (21).

For a point mass at \(x\), \(L=\lambda\theta\cdot x\),
\(\dot L=\theta\cdot x\), and \(B=|x|^2\). Spherical averaging
in (20) gives zero. This checks the translation-invariant normalization.
More generally \(\mathcal C\) is translation invariant because it
is the uniquely determined coefficient in (21), whose other terms are
translation invariant. \(\square\)

## 4. An explicit negative coefficient, with positive majorisation

For \(\xi=(1-p)\delta_0+p\delta_{re_1}\), let \(v=\lambda r\) and

\[
 \ell_+=\log(1-p+pe^v),\qquad \ell_-=\log(1-p+pe^{-v}).
\]

The coefficient has the closed form

\[
 \boxed{\quad
 \mathcal C_\xi(\lambda)=r^2\left[
 -\frac{\ell_+-\ell_-}{4v}
 +\frac{\ell_+^2+\ell_-^2}{4v^2}
 +\frac{\ell_++\ell_-}{2v^2}\right].\quad}                    \tag{27}
\]

To verify it, let \(\ell(z)=\log(1-p+pe^{vz})\) and let \(P(z)\)
be the tilted probability of the second atom. Then
\(\ell'=vP\), \(B=r^2P\), and
\(\dot L=rzP\). If \(V(\ell)=\ell^2/2+\ell\), the last two
terms in (20), apart from their common factor \(r^2/v^2\), integrate
as \((zV(\ell(z)))'\). The first integrates using \(\ell'=vP\).
This gives (27) with the normalized factor \(1/2\).

For a fully specified fixed-law example, let \(m\ge12\),
\(p=2^{-m}\), \(\ell=m\log2\), \(\lambda=2\ell/R\), and use
the injective pair in (6) with \(\alpha=1/4\). Then

\[
 \boxed{\quad\mathcal C_\mu(\lambda)-\mathcal C_\nu(\lambda)
                         \le-R^2/32.\quad}                   \tag{28}
\]

Here is an exact elementary certificate. For the input, \(v=2\ell\),
so
\(\ell_+=\ell+\log(1+p-p^2)\in[\ell,\ell+p]\) and
\(\ell_-=\log(1-p+p^3)\in[-2p,0]\). Thus

\[
 \mathcal C_\mu/R^2
 \le-1/16+\frac{1+p}{8\ell}+\frac{5p^2+2p}{16\ell^2}.
 \tag{29}
\]

For the output, its exponent is \(v=\ell/2\),
\(0\le\ell_+\le\sqrt p\), and \(-2p\le\ell_-\le0\).
The absolute value of (27) is therefore at most

\[
 \frac{|\mathcal C_\nu|}{R^2}\le\frac1{16}
 \left[\frac{\sqrt p+2p}{4v}
       +\frac{p+4p^2}{4v^2}+\frac{\sqrt p+2p}{2v^2}\right].    \tag{30}
\]

The inequalities \(\log2\ge2/3\), \(\ell\ge8\),
\(p\le1/4096\), and \(\sqrt p\le1/64\) make the sum of (29)
and (30) at most
\(-803606519/17179869184<-1/32\). The log bound follows, for example,
from \(\log2=2\sum_{j\ge0}(1/3)^{2j+1}/(2j+1)\).
All remaining arithmetic is rational. This certifies the negative
high-variance correction for every fixed member of the family; (7)
separately proves the stronger fixed-variance instability.

## 5. What the coefficient says at a spherical zero

Equation (22) supplies an additional test not present in the leading
criterion. If, for a fixed bounded contraction pair and \(\lambda_0>0\),

\[
 J(\lambda_0)=0,\qquad
 \mathcal C_\mu(\lambda_0)-\mathcal C_\nu(\lambda_0)<0,
 \tag{31}
\]

then Gaussian majorisation fails at \(a_{s,\lambda_0}\) for every
sufficiently large \(s\). No pair satisfying (31) is supplied here.
The examples of Section 4 have a positive leading gap, so their negative
coefficient does not yield such a counterexample.

There is a complementary completion criterion for a finite, noncongruent
contracting pair with positive atom weights. Suppose \(J(\lambda)\ge0\)
for all \(\lambda>0\), and

\[
 \mathcal C_\mu(\lambda)-\mathcal C_\nu(\lambda)>0
 \quad\text{at every positive zero of }J.                     \tag{32}
\]

Then full majorisation holds for all sufficiently large variances.
To see this, separately center both laws in a common radius-\(R\) ball.
The strict point-hull mean-width argument in the team's
[eventual-endpoint proof](../gaussian_majorisation_eventual_endpoint/PROOF.md),
Section 2, gives \(J(\lambda)\to+\infty\). Choose
\(\Lambda>1/(2R)\) so that \(J\ge1\) on \([\Lambda,\infty)\).
The uniform error (4) controls that whole ray for large \(s\).

On the compact interval \([1/(2R),\Lambda]\), the zero set of \(J\)
is compact, and the continuous coefficient difference has a positive
minimum there by (32), if the zero set is nonempty. It remains positive
on a neighborhood of that zero set. Uniformity of (22) gives
\(N_s\ge0\) on the neighborhood for large \(s\); on its compact
complement \(J\) has a strictly positive minimum, which handles the
rest. If the zero set is empty, use that last argument on the entire
interval. Finally the team's
[high-noise hinge window](../gaussian_majorisation_high_noise_window/PROOF.md)
covers thresholds above \(C_s e^{-9s/(64R^2)}\), while the parameter
range \(\lambda\ge1/(2R)\) covers thresholds below
\(C_s e^{-s/(8R^2)}\). These ranges overlap. This proves the assertion.

Thus the previously unresolved zero case has a precise next signed
obligation. If both leading and next coefficients vanish, these results
do not decide the case. Theorem A also shows why the coefficient or
the remainder cannot be assumed small merely because entropy and mean
distance loss are small, uniformly across all thresholds.

## 6. Scope and validation

No unrestricted spherical sign, full arbitrary-contraction theorem, or
new Kneser--Poulsen case is proved. The explicit negative quantities are
approximation errors or correction coefficients, **not hinge gaps**.
The existing entropy-rigidity, signed-window, and spherical-tail theorems
remain valid. The obstruction specifically closes a proposed uniform
vanishing-deficit refinement of (4).

The exact checker verifies the signed angular integral, the formal
boundary/volume/exterior-mass coefficients, translation normalization,
the rational margin in (28), and concrete contraction/entropy constants.
It uses no floating-point arithmetic or imported certificates. The
universal limits and remainders are justified by the analytic arguments
above; finite algebraic checks are supplementary, not independent review
or a proof-assistant formalization. See [SOURCES.md](SOURCES.md).
