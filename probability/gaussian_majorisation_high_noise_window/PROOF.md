# A signed high-noise hinge window and a spherical comparison

Author proof, 26 September 2026. Independent review and formalization are
pending. The bounded-input Gaussian majorisation conjecture in dimension
three remains open. The result below compares **all hinges in an explicit
threshold interval**, rather than finitely many polynomial tests. It gives
no new Kneser--Poulsen case.

## 1. Statements

Let `mu` be a probability measure supported in `B(a,R)` in `R^3`, and let
`T:R^3 -> R^3` be 1-Lipschitz. The Gaussian has covariance `s I_3`. Set

\[
 C_s=(2\pi s)^{-3/2},\quad f=\mu*\gamma_s,\quad
 g=(T_\#\mu)*\gamma_s,\quad
 H_h(b)=\int(h-b)_+\,dx,
\]
\[
 D=\mathbb E\big[|X-X'|^2-|T(X)-T(X')|^2\big]\geq0,
 \qquad X,X'\text{ iid with law }\mu.
 \tag{1}
\]

If `R=0`, both densities are translates of the same Gaussian and every
hinge gap vanishes. Below assume `R>0` and write

\[
 \varepsilon=R^2/s,\quad \kappa=1-\varepsilon,\quad
 \beta=5-\kappa^{-1},\quad
 L_\varepsilon=\frac{\kappa\beta^2}{32\varepsilon}
 =\frac{(4-5\varepsilon)^2}{32\varepsilon(1-\varepsilon)}.
 \tag{2}
\]

**Theorem A (all hinges above an explicit cutoff).** If `s>=2R^2`, then

\[
 \boxed{H_g(b)\geq H_f(b)
 \quad\text{for every }b\geq C_s e^{-L_\varepsilon}.}
 \tag{3}
\]

In particular the simpler sufficient threshold is

\[
 b\geq C_s\exp\!\left(-\frac{9s}{64R^2}\right).
 \tag{4}
\]

The sharper exponent in (3) has the exact form

\[
 L_\varepsilon=\frac{s}{2R^2}-\frac34
                 +\frac{\varepsilon}{32(1-\varepsilon)}.
 \tag{5}
\]

Thus any counterexample at these variances must occur below the cutoff
in (3). Equivalently, every finite convex energy `U` with `U(0)=0` that
is affine on `[0,C_s exp(-L_epsilon)]` has the desired internal-energy
comparison. The result is uniform over all atom weights, arbitrary
bounded input laws, and all contractions with the stated support bound.

**Theorem B (quantitative interior gap).** Under the same assumptions,
put `u=e^(-l)` and

\[
 q=4\sqrt{\frac{2\varepsilon l}{\kappa}}.
\]

If `epsilon/2<=l<=L_epsilon`, then

\[
 \boxed{H_g(C_su)-H_f(C_su)
 \geq\frac{uD}{12s\sqrt\pi}\,
 e^{-5\varepsilon-q}(\beta-q)
 (l-\varepsilon/2)^{3/2}.}
 \tag{6}
\]

The right side is strictly positive if `D>0` and
`epsilon/2<l<L_epsilon`. This interval is nonempty for `epsilon<=1/2`.
No optimality of the constants is claimed.

For normalized area measure `sigma` on `S^2`, define

\[
 S_\mu(\lambda)=\int_{S^2}\log\left(\int e^{\lambda\theta\cdot x}
                                  \,d\mu(x)\right)d\sigma(\theta).
 \tag{7}
\]

**Theorem C (a signed spherical range).** For every `lambda>=0` with
`lambda R<=1`,

\[
 \boxed{S_\mu(\lambda)-S_{T_\#\mu}(\lambda)
 \geq\frac{D\lambda^2}{12}(1-\lambda R)e^{-4\lambda R}.}
 \tag{8}
\]

Here `s` no longer occurs. In particular the comparison is strict when
`D>0` and `0<lambda R<1`. This supplies a positive, quantitative range
for the team's [spherical tail test](../gaussian_majorisation_spherical_tail/PROOF.md).
It does not establish that test for every `lambda`, or the equivalent
arbitrary-radius ball-hull condition at all weights and parameters.

## 2. Exact representation before making estimates

Translate the input by `a` and the output by `T(a)`; hinges, `D`, and
`S` are unchanged. We may assume `|X|,|T(X)|<=R`. Use the usual lift

\[
 Z_t(X)=(\sqrt{1-t}X,\sqrt t\,T(X))\in\mathbb R^6,
 \qquad 0\leq t\leq1.
\]

It lies in `B(0,R)` and its pair distances have derivative `-Delta`, where
`Delta(X,X')=|X-X'|^2-|T(X)-T(X')|^2`.
Define normalized Gaussian kernels and a weighted pair kernel by

\[
 K_{t,x}(z)=e^{-|z-Z_t(x)|^2/(2s)},\quad
 Q_t(z)=\mathbb E K_{t,X}(z),\quad V_t(z)=-\log Q_t(z),
\]
\[
 M_t(z)=\mathbb E[\Delta(X,X')K_{t,X}(z)K_{t,X'}(z)],
 \qquad h_t(z)=\frac{M_t(z)}{Q_t(z)^2}.
 \tag{9}
\]

All these functions are smooth in `z`, and `0<=h_t<=4R^2`. If `D>0`,
then `h_t>0` everywhere. Let `C_6=(2 pi s)^(-3)` and

\[
 H(u)=H_g(C_su)-H_f(C_su),\quad
 d_k=C_s^{1-k}\left(\int g^k-\int f^k\right),\quad
 a_j=\frac{d_{j+2}}{(j+1)(j+2)}=\int_0^1 u^jH(u)\,du.
 \tag{10}
\]

The last identity follows by integrating each hinge first. The exact
lifted moment identity from the team's
[Hankel reduction](../gaussian_majorisation_hankel_transport/PROOF.md) is

\[
 a_j=\frac{C_6\sqrt{j+2}}{4s}
       \int_0^1\int_{\mathbb R^6}e^{-(j+2)V_t(z)}h_t(z)\,dz\,dt.
 \tag{11}
\]

For an independent normalization check, put `k=j+2` and
`Q_k(t)=sum_i |Z_t(X_i)-mean Z_t|^2`. Gaussian integration gives
`C_6 integral Q_t^(k-2) M_t = k^(-3) E[Delta_12 exp(-Q_k(t)/(2s))]`.
Differentiating the three-dimensional replica formula, using
`Q_k'(t)=-k^(-1)sum_(i<j)Delta_ij`, and exchangeability gives
`d_k=(k-1)k^(-3/2) E[Delta_12 integral_0^1 exp(-Q_k(t)/(2s))dt]/(4s)`.
Dividing by `k(k-1)` proves (11). Only the exponent, affine in `t`, is
differentiated; singular derivatives of the square roots at the endpoints
cause no difficulty. Bounded support justifies all exchanges.

If `D=0`, the nonnegative replica integrals vanish, so all `a_j=0`.
The continuous function `H` then vanishes by polynomial approximation.
All three theorems follow, with equality for A--B and by the limit below
for C. We henceforth assume `D>0`.

## 3. Strong convexity and the weighted coarea profile

Fix `t`, suppress its subscript, and let posterior expectations refer to
the probability law tilted by `K_(t,X)(z)`. Differentiating gives

\[
 \nabla V(z)=\frac{z-\mathbb E_z Z}{s},\qquad
 \nabla^2V(z)=\frac{I}{s}-\frac{\operatorname{Cov}_z(Z)}{s^2}.
\]

Since `|Z|<=R`, each directional posterior variance is at most `R^2`.
Consequently

\[
 \frac\kappa s I\preceq\nabla^2V\preceq\frac1s I.
 \tag{12}
\]

The potential has a unique minimizer `z_*`, with `|z_*|<=R` from its
gradient equation. If `v_*=V(z_*)`, then

\[
 0\leq v_*\leq\varepsilon/2.
 \tag{13}
\]

Indeed `Q<=1` and `Q(0)>=exp(-epsilon/2)`.
The gradient of `log h` is the difference between the weighted pair
posterior mean of `Z+Z'` and twice the ordinary posterior mean of `Z`,
divided by `s`. Thus

\[
 |\nabla\log h|\leq4R/s.
 \tag{14}
\]

A useful lower bound follows directly, without comparing to a posterior
value of `D`. Write the kernels with their common `exp(-|z|^2/(2s))`
factor removed. Their one-point expectation is at most
`exp(|z|R/s)`; the weighted two-point numerator is at least
`D exp(-2|z|R/s-epsilon)`. For `z=z_*+r theta`, this gives

\[
 h(z_*+r\theta)\geq D e^{-4Rr/s-5\varepsilon}.
 \tag{15}
\]

For `v>0` and `theta in S^5`, let `r=r(v,theta)>0` be the unique solution
of `V(z_*+r theta)=v_*+v`. With radial derivatives taken from `z_*`, (12)
implies

\[
 \frac{\kappa r^2}{2s}\leq v\leq\frac{r^2}{2s},\qquad
 \frac{\kappa r}{s}\leq V_r\leq\frac r s,
 \qquad \frac\kappa s\leq V_{rr}\leq\frac1s.
 \tag{16}
\]

Define the weighted level density, set to zero for `w<=v_*`, by

\[
 A(w)=\int_{S^5}
       \frac{h(z_*+r(w-v_*,\theta)\theta)\,r(w-v_*,\theta)^5}
            {V_r(z_*+r(w-v_*,\theta)\theta)}\,d\theta.
 \tag{17}
\]

Here `dtheta` is ordinary surface measure, of total area `pi^3`.
Polar coordinates, followed by the change from `r` to `V`, prove

\[
 \int_{\mathbb R^6}e^{-kV(z)}h(z)\,dz
        =\int_{v_*}^\infty e^{-kw}A(w)\,dw.
 \tag{18}
\]

This also explains the coarea terminology without requiring an
unproved regular-level assertion at the minimum. The bound (16) shows
`A(v_*+v)=O(v^2)` at zero. Away from zero it is differentiable, and
the following estimates imply `A'(v_*+v)=O(v+v^(3/2))`, uniformly in `t`.
In particular its extension is continuously differentiable at `v_*`.

For a ray let `J=h r^5/V_r`. From (12)--(14),

\[
 \frac{d}{dr}\log J
 =\partial_r\log h+\frac5r-\frac{V_{rr}}{V_r}
 \geq-\frac{4R}{s}+\frac\beta r.
 \tag{19}
\]

It follows that `A'(v_*+v)>=0` whenever

\[
 0\leq v\leq\frac{\kappa}{2s}
                  \left(\frac{\beta s}{4R}\right)^2
       =L_\varepsilon.
 \tag{20}
\]

For clarity about the derivative bounds used above, differentiation of
`J` with respect to `w` adds the factor `1/V_r`. Its absolute value is
at most
`h s^2 r^3/kappa^2 [4R/s+(5+1/kappa)/r]`.
Since `h<=4R^2` and `r` is comparable to `sqrt(v)` by (16), this is
`O(v+v^(3/2))` both near zero and at infinity. The constants are uniform
in `t`; they need not be uniform as `s/R^2` tends to its excluded boundary.

## 4. Inverting the square-root multiplier with its boundary term

Define the half derivative

\[
 F(l)=\frac1{\sqrt\pi}\int_{v_*}^l
                   \frac{A'(w)}{\sqrt{l-w}}\,dw
 \quad(l>v_*),\qquad F(l)=0\quad(l\leq v_*).
 \tag{21}
\]

The growth bounds in Section 3 justify absolute Fubini for every `k>0`.
The Gamma integral and integration by parts, with `A(v_*)=0`, give

\[
 \int_0^\infty e^{-kl}F(l)\,dl
 =k^{-1/2}\int_{v_*}^\infty e^{-kw}A'(w)\,dw
 =\sqrt{k}\int_{v_*}^\infty e^{-kw}A(w)\,dw.
 \tag{22}
\]

In particular **there is no omitted atom or boundary term at the mode**.
Keep the time subscript in (21) and set

\[
 \widetilde H(u)=\frac{C_6u}{4s}\int_0^1F_t(-\log u)\,dt,
 \qquad 0<u<1.
 \tag{23}
\]

Changing variables `u=exp(-l)` and using (11), (18), (22) shows
`integral_0^1 u^j tilde H(u)du=a_j` for every integer `j>=0`.
Both `H` and `tilde H` are continuous and integrable on `[0,1]`, with
value zero at the endpoints. For `tilde H`, this follows from the uniform
polynomial growth bounds for `F_t`, the vanishing at each `v_*(t)`, and
the factor `u`. Thus polynomial approximation identifies the two functions:

\[
 \boxed{H(u)=\frac{C_6u}{4s}\int_0^1F_t(-\log u)\,dt.}
 \tag{24}
\]

For example, one may integrate `H-tilde H` against polynomial
approximations to itself; its squared integral then vanishes.
This identifies the signed hinge itself, not merely a finite list of moments.

If `l<=L_epsilon`, then either `l<=v_*(t)` and `F_t(l)=0`, or every
argument in (21) satisfies `0<=w-v_*(t)<=L_epsilon`. In the latter case
(20) makes the whole integral nonnegative. Equation (24) proves (3)
for `0<u<1`. At `u>=1` both hinges are zero.

Finally the exact factorization

\[
 L_\varepsilon-\frac9{64\varepsilon}
 =\frac{(1-2\varepsilon)(23-25\varepsilon)}
        {64\varepsilon(1-\varepsilon)}\geq0
 \tag{25}
\]

proves (4), and elementary division gives (5). Also
`9/(64 epsilon)>epsilon/2` for `0<epsilon<=1/2`, so the interior
interval in Theorem B is nonempty. A convex energy affine up to the
cutoff is an affine function plus a nonnegative measure of hinges above
that cutoff. Equal masses cancel the affine part; approximation at the
upper endpoint gives the asserted energy consequence.

## 5. A quantitative lower bound for the same inverse

Fix `epsilon/2<=l<=L_epsilon`, and let
`r_l=sqrt(2sl/kappa)` and `q=4Rr_l/s`. For every `t` and every
`0<=v<=l-v_*(t)`, (16) gives `r<=r_l`, and `beta-q>=0`.
Differentiate (17), using (19), (15), and then `V_r<=r/s`:

\[
 \begin{aligned}
 A_t'(v_*+v)
 &\geq\int_{S^5}\frac{h r^5}{V_r^2}
                         \frac{\beta-q}{r}\,d\theta\\
 &\geq D e^{-5\varepsilon-q}(\beta-q)s^2
                              \int_{S^5}r^2\,d\theta\\
 &\geq2\pi^3s^3D e^{-5\varepsilon-q}(\beta-q)v.
 \end{aligned}
 \tag{26}
\]

The last step uses `r^2>=2sv`. Since `C_6=(8 pi^3s^3)^(-1)` and
`integral_0^W v/sqrt(W-v)dv=4W^(3/2)/3`, (21) yields

\[
 C_6F_t(l)\geq\frac{D}{3\sqrt\pi}
 e^{-5\varepsilon-q}(\beta-q)(l-v_*(t))^{3/2}.
 \tag{27}
\]

Insert this in (24) and use `v_*(t)<=epsilon/2` to obtain (6).
For the open interval in Theorem B, `q<beta`, so the strictness follows.

As a separate normalization check, take a formal centered kernel
`Q(z)=exp(-|z|^2/(2s))` and the constant weight `h=D`. Then
`C_6 A(l)=D l^2/2`, `C_6 F(l)=D l^(3/2)/Gamma(5/2)`, and
the moments of (24) are `D/[4s(j+2)^(5/2)]`. These are precisely the
zero-radius leading replica moments. This is a kernel check; a positive
constant deficit on a single-point contraction is not asserted to exist.

## 6. Pass to the team's spherical tail limit

Theorem A of the team's
[spherical-tail result](../gaussian_majorisation_spherical_tail/PROOF.md)
proves, for fixed bounded laws and fixed `lambda>0`,

\[
 \lim_{s\to\infty}
 \frac{H_g(C_se^{-\lambda^2s/2})-H_f(C_se^{-\lambda^2s/2})}
 {4\pi\lambda s^2 C_s e^{-\lambda^2s/2}}
 =S_\mu(\lambda)-S_{T_\#\mu}(\lambda).
 \tag{28}
\]

Its error is explicit and tends to zero; this is a dependency of the
present spherical corollary, not a new tail-limit claim. Its common
support bound is `R` after the separate translations already made.

Fix `0<lambda R<1` and let `l=lambda^2s/2`. Equation (5) shows that
`epsilon/2<l<L_epsilon` for all sufficiently large `s`. In (6),

\[
 \varepsilon\longrightarrow0,\quad \beta\longrightarrow4,
 \quad q\longrightarrow4\lambda R,
 \quad\frac{l-\varepsilon/2}{s}\longrightarrow\lambda^2/2.
\]

Divide (6) by the denominator in (28). Since
`4 pi lambda s^2 C_s=sqrt(2/pi) lambda sqrt(s)`, the right side tends to
`D lambda^2(1-lambda R)exp(-4lambda R)/12`. This proves (8) on the open
range. Continuity of the bounded-law log moment-generating integrals
in `lambda` gives both endpoints. For `D=0`, the preceding moment argument
gives zero hinge gaps at every variance, so (28) gives equality as well.

As `lambda` tends to zero, the coefficient `D lambda^2/12` agrees with
the direct covariance expansion of (7): the spherical average of
`theta theta^T` is `I_3/3`, and
`D=2(trace Cov(X)-trace Cov(T(X)))`. The extra factor in (8) is a
sufficient global estimate on the specified interval, not an optimal one.

## 7. Scope, obstruction, and next obligation

The half-order lift comparison alone does not imply majorisation.
The new input here is monotonicity of its **weighted coarea density**
up to a quantified level, followed by inversion with the boundary term
controlled. Mere positivity of the lift measure, entropy comparison, or
approximate rigid alignment is not used to infer a hinge sign.

The actual instantaneous-lift counterexample in the team repository
rules out an unrestricted pointwise positivity theorem. It has a very
large support-to-noise ratio. Here (12) and (20) impose `s>=2R^2` and
an explicit density-level restriction. We make no claim that `A'` or
its half derivative stays nonnegative beyond that range.

The new window concerns fixed arbitrary bounded laws as variance grows.
It is distinct from the team's small-mass theorem at fixed variance,
and from the preceding sparse-polynomial and finite Hankel results.
It does not by itself prove the whole first `3 by 3` Hankel matrix
positive: its quadratic test still integrates through the uncontrolled
low-density interval. Nor does (8) imply the arbitrary-offset ball-hull
comparison, which needs all positive `lambda`.

The remaining sign question is confined by (3) to
`0<b<C_s exp(-L_epsilon)` at high variance. In the tail parameter of
(28), (8) closes `lambda R<=1`; larger parameters and uniform transitions
between regimes remain open. A full Kneser--Poulsen implication requires
the still-missing small-variance/all-threshold comparison.

All universal assertions in this document rest on the analytic argument.
The accompanying checker independently audits constants and encloses
selected one-dimensional-mixture hinge integrals; those finite checks
do not prove the universal statements or constitute independent peer review.
