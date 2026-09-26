# Sharp covariance-free rigidity for Gaussian entropy contraction

Author proof, 26 September 2026. Independent review pending.
All logarithms are natural, and all norms on Euclidean vectors are Euclidean.
The notation `HS` and `1` denotes Hilbert–Schmidt and trace norms.

## 1. Statement and relation to the source

Let `n>=1`, `R,s>0`, let `X` have any Borel probability law supported in
a closed ball of radius `R` in `R^n`, and let `T:R^n -> R^n` be 1-Lipschitz.
Let `X'` be an independent copy of `X`. Put

\[
\begin{split}
\Delta(x,x')&=|x-x'|^2-|T(x)-T(x')|^2,\qquad D=\mathbb E\Delta(X,X'),\\
\rho^2&=\inf_{Q\in O(n),\,b\in\mathbb R^n}
                  \mathbb E|T(X)-QX-b|^2,\\
G_\alpha&=h_\alpha(X+\sqrt{s}Z)-h_\alpha(T(X)+\sqrt{s}Z).
\end{split}                                                    \tag{1}
\]

Here `Z` is standard Gaussian, `h_alpha(f)=log(integral f^alpha)/(1-alpha)`
for finite `alpha!=1`, `h_1(f)=-integral f log f`, and
`h_infinity(f)=-log ||f||_infinity`. All these entropies are finite in the
stated bounded-support setting. Define

\[
b_\alpha=\begin{cases}
1/\alpha,&0<\alpha<1,\\
1,&1\le\alpha\le2,\\
\min\{\alpha/2,4\},&2<\alpha<\infty,\\
4,&\alpha=\infty.
\end{cases}                                                    \tag{2}
\]

**Theorem 1 (dimension-free entropy estimate).** For every positive order,
including Shannon and infinity,

\[
G_\alpha\ \ge\ \frac{e^{-b_\alpha R^2/s}}{4s}D.                 \tag{3}
\]

The coefficient does not depend on dimension. In particular it is bounded
below by `exp(-max(4,1/a) R^2/s)/(4s)` simultaneously for all `alpha>=a>0`.
Optimality of the coefficients in (3) is not claimed.

**Theorem 2 (sharp geometric inequality).** Independently of entropy,

\[
\rho^2\le\sqrt{2n}\,R\sqrt D.                                 \tag{4}
\]

For every fixed `n` and `R`, the coefficient `sqrt(2n)` cannot be reduced.
Consequently

\[
\boxed{\quad
\rho\le\bigl(8nR^2s\,e^{b_\alpha R^2/s}G_\alpha\bigr)^{1/4}.
\quad}                                                        \tag{5}
\]

**Theorem 3 (sharp exponent and dimension growth).** For each fixed
`n,R,s,alpha`, no exponent larger than `1/4` can replace `1/4` in a uniform
bound `rho<=C G_alpha^beta` over this class, even allowing `C` to depend on
all four fixed parameters. With `R,s,alpha` fixed and dimension variable,
the coefficient in a uniform fourth-root bound must grow at least as
`n^(1/4)`.

The [source](../gaussian_contraction_rigidity/PROOF.md) gives exponent `1/2`
under an additional lower bound on covariance and uses dimension-dependent
finite-order entropy constants. It also gives equality rigidity for
arbitrary, possibly unbounded laws. We extend its quantitative statement
to singular and arbitrarily poorly conditioned bounded laws. We do not
extend its arbitrary-law statement or claim a new qualitative entropy
comparison. The finite-order dissipation identity below is the source's
identity, with its classical lifted path explicitly credited.

## 2. A Gaussian-mixture overlap lemma in arbitrary dimension

Write

\[
\phi_c(z)=(2\pi s)^{-m/2}\exp(-|z-c|^2/(2s)),\quad
q(z)=\int\phi_c(z)\,d\nu(c),\quad I_\alpha=\int q^\alpha,
\]

where `nu` is any probability law on `B(0,R)` in `R^m`. For `a,b` in that
ball define

\[
K_\alpha(a,b)=\frac{\int q^{\alpha-2}\phi_a\phi_b}{I_\alpha}.
                                                                    \tag{6}
\]

For every finite positive order,

\[
K_\alpha(a,b)\ge e^{-b_\alpha R^2/s}.                            \tag{7}
\]

All integrals in (6) are finite. For example, the elementary bounds

\[
M e^{-(|z|+R)^2/(2s)}\le q(z)
 \le M e^{-((|z|-R)_+)^2/(2s)},\qquad M=(2\pi s)^{-m/2},           \tag{8}
\]

bound each integrand by `C exp(-alpha |z|^2/(2s)+C|z|)`.

### 2.1. Orders at most two

Let `J_alpha=integral phi_0^alpha`. For `alpha>=1`, Jensen's inequality
inside the mixture gives `I_alpha<=J_alpha`. For `0<alpha<1`, write

\[
q(z)=\phi_0(z)\int e^{z\cdot c/s-|c|^2/(2s)}d\nu(c).
\]

The probability density `phi_0^alpha/J_alpha` is Gaussian with variance
`s/alpha`. Concavity of the power, now applied to integration in `z`, and
the Gaussian moment-generating function yield

\[
\frac{I_\alpha}{J_\alpha}
\le\left(\int e^{(1-\alpha)|c|^2/(2\alpha s)}d\nu(c)\right)^\alpha
\le e^{(1-\alpha)R^2/(2s)}.                                    \tag{9}
\]

For `0<alpha<2`, Holder's inequality with exponents `2/alpha` and
`2/(2-alpha)` gives

\[
\int(\phi_a\phi_b)^{\alpha/2}
\le\left(\int q^{\alpha-2}\phi_a\phi_b\right)^{\alpha/2}
       I_\alpha^{(2-\alpha)/2}.
\]

The left side is `J_alpha exp(-alpha |a-b|^2/(8s))`. Rearrangement, also
valid directly at `alpha=2`, gives

\[
K_\alpha(a,b)\ge
 (J_\alpha/I_\alpha)^{2/\alpha}e^{-|a-b|^2/(4s)}.                 \tag{10}
\]

Use `|a-b|<=2R` and (9). The exponents become `R^2/(alpha s)` below order
one and `R^2/s` between orders one and two, proving (7) there.

### 2.2. A first bound for orders above two

Put `v=integral c dnu` and `r_2=integral |c|^2 dnu`. Jensen gives

\[
q(z)\ge\phi_0(z)e^{z\cdot v/s-r_2/(2s)}.
\]

For `alpha>2`, multiply its `(alpha-2)`-th power by `phi_a phi_b` and
integrate the resulting Gaussian. This proves

\[
\int q^{\alpha-2}\phi_a\phi_b\ge J_\alpha
\exp\left[-\frac{|a|^2+|b|^2+(\alpha-2)r_2
 -|a+b+(\alpha-2)v|^2/\alpha}{2s}\right]
\ge J_\alpha e^{-\alpha R^2/(2s)}.                              \tag{11}
\]

Since `I_alpha<=J_alpha`, this gives the `alpha/2` choice in (2).

### 2.3. A bound uniform in all orders above two

For `alpha>=2`, set `N(a,b)=integral q^(alpha-2) phi_a phi_b`, and let
`eta_(a,b)` be its normalized integrand as a probability density in `z`.
Let

\[
m(z)=\frac{\int c\phi_c(z)d\nu(c)}{q(z)}\in B(0,R).
\]

Differentiation and integration by parts, justified by (8), give

\[
\nabla_a\log N(a,b)=\frac{\mathbb E_\eta Z-a}{s},\qquad
\alpha\mathbb E_\eta Z=a+b+(\alpha-2)\mathbb E_\eta m(Z).
                                                                    \tag{12}
\]

Thus `E_eta Z` belongs to `B(0,R)`. Integrate the first identity along
the segment from `a` to `u`, keeping `b` fixed:

\[
\log\frac{N(u,b)}{N(a,b)}
\le\frac{R|u-a|+(|a|^2-|u|^2)/2}{s}\le\frac{2R^2}{s}.           \tag{13}
\]

For the last inequality put `r=|a|`, `t=|u|`: the numerator is at most
`R(r+t)+(r^2-t^2)/2`, which increases with `r<=R` and is at most
`3R^2/2+Rt-t^2/2<=2R^2`. Repeat for the other coordinate to obtain
`N(a,b)>=exp(-4R^2/s) N(u,v)` for all four centers in the ball.
Tonelli's theorem gives

\[
\iint N(u,v)d\nu(u)d\nu(v)=\int q^\alpha=I_\alpha.              \tag{14}
\]

Averaging proves `K_alpha(a,b)>=exp(-4R^2/s)`. Combining this with (11)
finishes the lemma, including noninteger orders. No replica formula or
integer-order extrapolation is used in this proof.

## 3. From the overlap lemma to entropy loss

Translate the input ball to `B(0,R)` and subtract `T(0)` from the output.
Define the classical doubled-dimensional path

\[
c_t(x)=\left(\frac{x+T(x)}2+\cos(\pi t)\frac{x-T(x)}2,
                 \sin(\pi t)\frac{x-T(x)}2\right),\quad 0\le t\le1.
                                                                    \tag{15}
\]

It starts at `(x,0)` and ends at `(T(x),0)`. Direct expansion gives

\[
|c_t(x)-c_t(x')|^2=
 \cos^2(\pi t/2)|x-x'|^2+\sin^2(\pi t/2)|T(x)-T(x')|^2.
                                                                    \tag{16}
\]

In particular `|c_t(x)|<=R` on the input support, because `T(0)=0`.
Let `q_t` be the Gaussian convolution of `c_t(X)` in dimension `2n`.
Let `w_t(z)` be the posterior mean of `dot c_t(X)` conditional on `z`.
The Gaussian derivative and the pair covariance identity imply

\[
\partial_tq_t=-\operatorname{div}(q_tw_t),\qquad
\operatorname{div}w_t(z)=-\frac{\pi\sin(\pi t)}{8s}
  \iint\Delta(x,x')\frac{\phi_{c_t(x)}(z)\phi_{c_t(x')}(z)}{q_t(z)^2}
                         d\mu(x)d\mu(x').                       \tag{17}
\]

Indeed, differentiating (16) gives the pair velocity product
`-pi sin(pi t) Delta/4`; posterior covariance contributes the factor
`1/(2s)`. Integration by parts in the continuity equation gives

\[
\frac{d}{dt}h_\alpha(q_t)=
 \frac{\int q_t^\alpha\operatorname{div}w_t}{\int q_t^\alpha},
                                                                    \tag{18}
\]

also at Shannon order, where the denominator is one. For clarity about
analytic hypotheses, centers and velocities in (15) are uniformly bounded;
`w_t` is bounded, its divergence is bounded, and
`|grad q_t|/q_t+|partial_t q_t|/q_t<=C(1+|z|)`. The two tail bounds (8)
give `|log q_t|<=C(1+|z|^2)`. Thus differentiated entropy integrands and
cutoff boundary terms are bounded by

\[
C_\alpha(1+|z|^k)e^{-\alpha |z|^2/(4s)}                         \tag{19}
\]

for a fixed finite `k`, uniformly in `t`, for every fixed positive order.
At Shannon order use `alpha=1` and the displayed logarithm bound. These
estimates justify differentiation, cutoffs tending to infinity, and (18)
even below order one. They also justify the differentiations in Section 2.

The auxiliary Gaussian entropy cancels between the endpoints. Hence the
source's exact compact dissipation identity becomes

\[
G_\alpha=\frac{\pi}{8s}\int_0^1\sin(\pi t)
 \iint\Delta(x,x')K_{\alpha,t}(c_t(x),c_t(x'))d\mu(x)d\mu(x')dt.
                                                                    \tag{20}
\]

Use (7), nonnegativity of `Delta`, and `integral_0^1 sin(pi t)dt=2/pi`.
This proves (3) for finite orders. For `alpha>=8`, (3) has the fixed
coefficient `exp(-4R^2/s)/(4s)`. The usual `L^p` norm limit for a bounded
probability density yields `h_alpha -> h_infinity`. Passing to that limit
proves the infinity case. This does not interchange an unbounded-order
limit with the dissipation integral.

## 4. A singular-safe Procrustes estimate

Center `X` and `Y=T(X)`. Define finite-rank feature operators
`A,B:R^n -> L^2(mu)` by `Au=u dot (X-EX)`, `Bu=u dot (Y-EY)`.
Put `P=AA*`, `Q=BB*`, and `H=P-Q`. All operators can be restricted to
the at most `2n` dimensional sum of their ranges.

The singular value decomposition gives the optimal Procrustes formula

\[
\rho^2=\operatorname{tr}P+\operatorname{tr}Q-2\|A^*B\|_1
      =\operatorname{tr}P+\operatorname{tr}Q-2\|\sqrt P\sqrt Q\|_1
      \le\|\sqrt P-\sqrt Q\|_{\rm HS}^2.                         \tag{21}
\]

The middle equality follows from equality of the nonzero squared singular
values of `A*B` and `sqrt(P)sqrt(Q)`. For the last inequality use
`||M||_1>=tr(M)` and expand the square. SVD is valid at every rank, and the
translation restores the means. No inverse covariance is used.

For completeness, the needed instance of the classical Powers–Stormer
inequality has a short finite-dimensional proof. Put
`S=sqrt(P)-sqrt(Q)` and `U=sqrt(P)+sqrt(Q)`. Then
`H=(SU+US)/2`. The self-adjoint contraction `sign(S)` gives

\[
\|H\|_1\ge\operatorname{tr}(\operatorname{sign}(S)H)
          =\operatorname{tr}(|S|U)\ge\operatorname{tr}(S^2).
                                                                    \tag{22}
\]

For the last step diagonalize `S`. The inequalities `U+S>=0`, `U-S>=0`
imply `U_ii>=|S_ii|` in that basis. This proves the last trace inequality
term by term, including zero eigenvalues. From (21)--(22) and Cauchy–Schwarz
for the at most `2n` singular values,

\[
\rho^2\le\|H\|_1\le\sqrt{2n}\|H\|_{\rm HS}.                   \tag{23}
\]

Let `J` be orthogonal projection in `L^2(mu)` off the constants. Double
centering of squared distances gives, as an equality of integral kernels,

\[
H=-\tfrac12J\Delta J.
\]

Orthogonal projection contracts the Hilbert–Schmidt norm. Since
`0<=Delta(x,x')<=|x-x'|^2<=4R^2`,

\[
\|H\|_{\rm HS}^2\le\tfrac14\iint\Delta^2d\mu d\mu
                   \le R^2D.                                  \tag{24}
\]

Equations (23)--(24) prove (4); combining with (3) proves (5).

## 5. One family proves all sharpness statements

Fix `a>0` and `0<epsilon<1`. Put mass `1-epsilon` at zero and mass
`epsilon/(2n)` at each of the `2n` points `+/-a e_j`. Take

\[
T(x_1,\ldots,x_n)=(|x_1|,\ldots,|x_n|).
\]

This is a global 1-Lipschitz map and the input radius is `a`. The only
positive losses are between opposite points on the same coordinate axis.
Each such squared-distance loss is `4a^2`. Consequently

\[
D=\frac{2a^2\varepsilon^2}{n},\quad
\operatorname{tr}\operatorname{Cov}(X)=a^2\varepsilon,\quad
\operatorname{tr}\operatorname{Cov}(Y)=a^2\varepsilon
                                    -\frac{a^2\varepsilon^2}{n}.
                                                                    \tag{25}
\]

The centered cross-covariance is zero, by cancellation of opposite signs.
Every orthogonal alignment has the same error, and

\[
\rho^2=a^2\varepsilon(2-\varepsilon/n),\qquad
\frac{\rho^2}{a\sqrt D}=\sqrt{2n}(1-\varepsilon/(2n)).           \tag{26}
\]

Taking `a=R` and sending `epsilon` to zero proves the optimality of the
constant in (4), in every dimension. Although the covariance is positive
for each `epsilon>0`, its least eigenvalue is `a^2 epsilon/n`, tending
to zero. This is consistent with the source's stronger exponent for a
fixed positive covariance lower bound.

### 5.1. Exact entropy expansion at each finite order

Set `A_0=a^2/s`, write `phi=phi_0`, and define

\[
u=\frac1{2n}\sum_j(\phi_{ae_j}+\phi_{-ae_j})-\phi,\qquad
w=\frac1{2n}\sum_j(\phi_{ae_j}-\phi_{-ae_j}).
\]

The smoothed input and output densities are respectively
`f_epsilon=phi+epsilon u` and `g_epsilon=phi+epsilon(u+w)`.
The function `u` is even in each coordinate. Each term of `w` is odd in
one coordinate and even in the others. Thus

\[
\int\phi^{\alpha-1}w=0,\qquad
\int\phi^{\alpha-2}uw=0.
\]

Completing the square in each Gaussian integral, with
`J_alpha=integral phi^alpha`, gives

\[
\frac{\int\phi^{\alpha-2}w^2}{J_\alpha}
 =\frac{e^{-A_0}}{2n}(e^{2A_0/\alpha}-1).                        \tag{27}
\]

Cross terms from different axes vanish by parity. Expanding the two power
integrals through second order, their first derivatives agree, so the
first-derivative squares cancel when taking logarithms. This gives

\[
G_\alpha=
 \frac{\alpha}{4n}e^{-A_0}(e^{2A_0/\alpha}-1)\varepsilon^2
 +o(\varepsilon^2),\qquad 0<\alpha<\infty.                       \tag{28}
\]

At order one, differentiate `-f log f` directly: the second derivative is
`-integral (partial_epsilon f)^2/f`. The coefficient of the difference is
`(1/2) integral w^2/phi`, exactly the value in (28) at `alpha=1`.

These are rigorous one-sided expansions, not a formal perturbation
argument. For `0<=epsilon<=1/2`, both densities dominate `phi/2` and are
bounded above by a fixed sum of Gaussian translates. Their first and
second power derivatives are dominated, for every fixed positive `alpha`,
by `C exp(-alpha |z|^2/(2s)+C|z|)`. The same holds for the Shannon second
derivative, with `alpha=1`; its first derivative permits an additional
quadratic polynomial from the logarithm. Dominated convergence gives
continuous second derivatives at zero. Positive power integrals justify
the logarithmic expansion.

### 5.2. Infinity order

The two perturbations converge to `phi` uniformly together with their
first two derivatives. All maximizers lie in an arbitrarily small fixed
ball about zero for sufficiently small `epsilon`: outside that ball the
strict maximum of `phi` has a fixed gap, whereas the perturbations are
uniformly `O(epsilon)`. Inside a sufficiently small ball the Hessian of
`phi` is strictly negative definite; this persists for the perturbations.
Thus each density has a unique global mode there. Symmetry fixes the input
mode at zero. The implicit function theorem gives the output mode

\[
z_\varepsilon=\varepsilon\frac{ae^{-A_0/2}}{n}(1,\ldots,1)
                  +O(\varepsilon^2),
\]

since `Hess phi(0)=-phi(0) I/s` and
`grad w(0)=phi(0) a e^(-A_0/2) (1,...,1)/(ns)`.
Also `f_epsilon(0)=g_epsilon(0)` because `w(0)=0`. The second-order
increase obtained by maximizing `g_epsilon` is therefore

\[
\max g_\varepsilon-g_\varepsilon(0)
 =\phi(0)\frac{A_0e^{-A_0}}{2n}\varepsilon^2+o(\varepsilon^2).
\]

Taking the logarithm of the ratio of maxima yields

\[
G_\infty=\frac{A_0e^{-A_0}}{2n}\varepsilon^2+o(\varepsilon^2).
                                                                    \tag{29}
\]

All coefficients in (28)--(29) are strictly positive. Equations (26),
(28), and (29) show `rho` is of order `epsilon^(1/2)` while the entropy
loss is of order `epsilon^2`. This excludes every exponent greater than
`1/4` for each fixed order. Writing `B_alpha(A_0)` for the coefficient
in (28) or (29) with `n=1`, we also obtain

\[
\lim_{\varepsilon\downarrow0}\frac{\rho^4}{G_\alpha}
       =\frac{4na^4}{B_\alpha(A_0)}.                            \tag{30}
\]

This proves the necessary `n^(1/4)` growth for uniform fourth-root bounds.
It does not assert optimality of the remaining prefactor in (5).

## 6. Evidence and limits

The proof uses Gaussian integration, Holder and Jensen inequalities,
cutoff integration by parts, SVD, the finite-dimensional Powers–Stormer
inequality, and the implicit function theorem. Section 4 proves the matrix
inequality used, and Section 3 spells out the domination requested in the
source review. No spectral gap, nonsingular covariance, density for the
input law, or finite support assumption enters the theorem.

The exact checker independently expands integer-order replica integrals
for the sparse family, checks distance loss and optimal errors, compares
finite entropy gaps with (3) using rational enclosures, and exercises
singular and noncommuting matrix cases. Those checks corroborate formulas;
they do not establish noninteger orders or limiting statements by sampling.
The claims are unformalized and await independent review. They do not
resolve Gaussian majorization or the geometric Kneser–Poulsen conjecture.
