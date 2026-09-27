# A loss-proportional spherical-to-Gaussian transfer

Author proof, 27 September 2026. Independent review and formalization are
pending. The unrestricted R3 majorisation question remains open.

The existing spherical-tail approximation has an absolute error. The
estimate below retains the actual distance loss in that error. Consequently,
a spherical margin proportional to that loss yields a Gaussian sign at a
variance bound independent of how close the contraction is to an isometry.
The spherical margin and the far-tail sign remain explicit premises.

## 1. Statement

Let `mu` be a probability in `B(a,R)` in R3, where `R>0`, and let `T` be
1-Lipschitz. The map may be given only on the support together with `a`.
Translate the source by `a` and the image by `T(a)`, so both supports lie
in `B(0,R)`. Write

\[
 D=\mathbb E\big[|X-X'|^2-|TX-TX'|^2\big],\quad X,X'\sim\mu
 \text{ independently},\qquad C_s=(2\pi s)^{-3/2},
\]
\[
 H_s(b)=\int(T_\#\mu*\gamma_s-b)_+-\int(\mu*\gamma_s-b)_+.
 \tag{1}
\]

Use normalized area measure `sigma` on S2 and set

\[
 J(\lambda)=\int_{S^2}\log\mathbb E e^{\lambda\theta\cdot X}
                  -\log\mathbb E e^{\lambda\theta\cdot TX}\,d\sigma,
 \quad b_s(\lambda)=C_s e^{-\lambda^2s/2},
\]
\[
 B_s(\lambda)=\frac{H_s(b_s(\lambda))}
                         {4\pi\lambda s^2 b_s(\lambda)},\qquad
 C(A)=1+25A(1+A)^2e^{4A+1}.
 \tag{2}
\]

The quantities in (1)--(2) are unchanged by the separate translations
just used. In particular no common barycenter or covariance hypothesis
is required.

**Theorem 1 (relative transfer).** If `s>=64R^2` and `lambda R>=1/2`, then

\[
 \boxed{|B_s(\lambda)-J(\lambda)|
                      \le \frac D s C(\lambda R).}
 \tag{3}
\]

This holds for arbitrary bounded atomic or nonatomic laws, without a
minimum weight, atom-count bound, or positive lower bound on `D`. It is
uniform on every compact interval of `lambda R`. The displayed constant
grows exponentially at infinity; no loss-proportional error uniform over
the entire unbounded parameter ray is asserted. When `D=0`, both sides
inside the absolute value are zero.

For comparison, the preceding spherical-tail theorem gives

\[
 |B_s(\lambda)-J(\lambda)|
 \le \frac{8R^2+6R/\lambda+6/\lambda^2}{s}.
 \tag{4}
\]

Either bound may be used. The improvement in (3) is the factor `D`, not
a uniformly smaller numerical constant. Both estimates use the full
support radius, including rare atoms.

**Corollary 2 (a loss-normalized middle certificate).** Suppose `A>=1/2`,
`eta>0`, and

\[
 J(\lambda)\ge\eta D/R^2
                \quad\left(\frac1{2R}\le\lambda\le\frac A R\right).
 \tag{5}
\]

At every variance

\[
 s\ge R^2\max\{64,2C(A)/\eta\},
 \tag{6}
\]

all thresholds `b>=C_s exp(-A^2s/(2R^2))` have `H_s(b)>=0`. On the
transition interval parametrized in (5),

\[
 B_s(\lambda)\ge\eta D/(2R^2).
 \tag{7}
\]

If an independently certified lower endpoint also signs
`0<b<=C_s exp(-A^2s/(2R^2))` at the same variance, the entire hinge curve
is nonnegative: the global adverse defect is exactly zero. The variance
bound (6) does not deteriorate as `D` tends to zero, provided `A`, `eta`
and the tail premise are maintained. None of these premises is supplied
for unrestricted contractions by the present theorem.

To prove the corollary, subtract (3) from (5), using that `C` increases.
This signs the interval between `C_s exp(-A^2s/(2R^2))` and
`C_s exp(-s/(8R^2))`. The accepted high-noise window already signs
`b>=C_s exp(-9s/(64R^2))`. Since `9/64>1/8`, those intervals overlap.
Above `C_s` both hinges vanish. The asserted tail completes the remaining
range only when its actual cutoff meets the displayed one.

## 2. Scale and preserve the pair-loss measure

Scale space by R. It suffices to prove (3) for `R=1`, `s=1/epsilon`,
`0<epsilon<=1/64`, and `lambda>=1/2`. The scaled distance loss will again
be called D. On returning to the original coordinates, it is `D_original/R^2`,
and `epsilon D=D_original/s_original`. Also `lambda_scaled=lambda_original R`
and the denominator defining B is unchanged by this scaling.

Put, for `0<=t<=1`,

\[
 Z=Z_t(X)=(\sqrt{1-t}X,\sqrt t\,TX)\in\mathbb R^6,
 \quad \Delta(X,X')=|X-X'|^2-|TX-TX'|^2\ge0.
\]

Then `|Z|<=1`. Assume `D>0` for now and use the probability measure
`d eta=Delta d(mu tensor mu)/D` on pairs. For a unit vector `theta` in
S5, define

\[
 M_\epsilon(p)=\mathbb E_\mu
                   e^{p\theta\cdot Z-\epsilon|Z|^2/2},
 \quad m_\epsilon=\log M_\epsilon,
\]
\[
 K_\epsilon(p)=
 \frac{\mathbb E_\eta
  e^{p\theta\cdot(Z+Z')-\epsilon(|Z|^2+|Z'|^2)/2}}
 {M_\epsilon(p)^2}.
 \tag{8}
\]

The suppressed t and theta parameters will be uniform in every bound.
A prime on K or m means differentiation in p at fixed epsilon.
Because all supports and exponential tilts are bounded,

\[
 |m_\epsilon'|\le1,\quad0\le m_\epsilon''\le1,
 \quad K_\epsilon(p)\le e^{4p+\epsilon}\quad(p\ge0),
\]
\[
 |K_\epsilon'|\le4K_\epsilon,\quad
 |K_\epsilon''|\le20K_\epsilon,\quad
 |\partial_\epsilon K_\epsilon|\le K_\epsilon,\quad
 |\partial_\epsilon K_\epsilon'|\le6K_\epsilon.
 \tag{9}
\]

Here is an explicit check of the less immediate constants. The p derivative
of log K is the tilted pair mean of `theta.(Z+Z')` minus twice the tilted
one-point mean of `theta.Z`, so its absolute value is at most four. Its
second derivative lies between -2 and 4, giving the bound twenty after
adding the square of the first derivative. The epsilon derivative of log K
lies between -1 and 1. For its mixed derivative, the pair covariance has
variables in intervals of lengths four and one, and the one-point covariance
has lengths two and one half. The bound `|Cov(U,V)|<=range(U)range(V)/4`
gives at most `1+1/2<=2`. Differentiating K' then gives `4+2=6`.
These calculations apply directly to arbitrary probability measures.

## 3. The radial transform away from the mode

At unit noise, with centers `sqrt(epsilon) Z`, write

\[
 Q(z)=\mathbb E e^{-|z-\sqrt\epsilon Z|^2/2},\quad V=-\log Q,
 \quad h(z)=\epsilon D K_\epsilon(\sqrt\epsilon|z|)
 \quad(z=|z|\theta).
 \tag{10}
\]

The weighted coarea density A_t(w) is defined by
`integral exp(-kV)h dz=integral exp(-kw) A_t(w)dw`.
The posterior Hessian bound makes V globally strongly convex with
`(1-epsilon)I<=D^2V<=I`. Its modal value v_* satisfies
`0<=v_*<=epsilon/2`. The coarea density and its first derivative extend
continuously by zero below this value, with `A=O((w-v_*)^2)` and
`A'=O(w-v_*)` there.

The accepted coarea/Abel identity gives, with
`ell=lambda^2/(2epsilon)` and `u=exp(-ell)`,

\[
 \frac{H_{1/\epsilon}(C_{1/\epsilon}u)}u
 =\frac1{32\pi^3\sqrt\pi}
   \int_0^1\int_0^\ell\frac{A_t'(w)}{\sqrt{\ell-w}}\,dw\,dt.
 \tag{11}
\]

Spatial scaling from variance `1/epsilon` to unit variance preserves the
hinge integral, explaining the left side of (11). No sign of the individual
instantaneous Abel integrals is assumed.

Set `q_0=4epsilon`, `w_0=8epsilon`. For `w>=w_0`, put
`q=sqrt(2epsilon w)`. Every ray from the origin meets the level V=w
exactly once, at radius r. In fact, Gaussian distance bounds give

\[
 |p-q|\le\epsilon,\qquad p=\sqrt\epsilon r,
 \qquad q^2=p^2-2\epsilon m_\epsilon(p).
 \tag{12}
\]

To justify the whole radial graph, the ball of radius
`sqrt(2w)-sqrt(epsilon)>=3sqrt(epsilon)` lies in the superlevel set of Q.
Outside radius `sqrt(epsilon)`, its derivative on every ray is strictly
negative. The outer Gaussian bound gives the other endpoint in (12).
This also verifies that no extra component is dropped.

Write

\[
 b=p-\epsilon m_\epsilon'(p),\quad
 \frac{dp}{dq}=\frac q b,\qquad
 F_\epsilon(q)=\int_{S^5}K_\epsilon(p)\frac{p^5}{b}\,d\theta.
 \tag{13}
\]

The measure on S5 is ordinary area, with total mass pi^3. The radial
Jacobian, including the factor `epsilon D` in h, gives exactly

\[
 A_t(w)=\frac D\epsilon F_{\epsilon,t}(q),\qquad
 A_t'(w)=\frac D q F_{\epsilon,t}'(q).
 \tag{14}
\]

The functions at zero noise parameter are

\[
 F_{0,t}(q)=q^4\int_{S^5}K_{0,t}(q)\,d\theta.
 \tag{15}
\]

For `q>=q_0`, differentiate (13), with `b_p=1-epsilon m''`:

\[
 F_\epsilon'(q)=\int_{S^5}
 \left[\frac{q p^5}{b^2}K_\epsilon'
 +qK_\epsilon\left(\frac{5p^4}{b^2}
                 -\frac{p^5(1-\epsilon m_\epsilon'')}{b^3}\right)\right]d\theta.
 \tag{16}
\]

## 4. A uniform relative error for the radial derivative

Let `z=epsilon/q<=1/4`, `a=p/q`, and `b_0=b/q`. By (12),

\[
 1-z\le a\le1+z,\qquad1-2z\le b_0\le1+2z.
\]

The coefficients in (16), after removing q^4 and q^3, are

\[
 R_1=a^5/b_0^2,\qquad
 R_2=5a^4/b_0^2-a^5(1-\epsilon m_\epsilon'')/b_0^3.
\]

The following deliberately coarse bounds hold throughout those intervals:

\[
 |R_1|\le13,\quad |R_1-1|\le70z,\qquad
 |R_2|\le80,\quad |R_2-4|\le440z+25\epsilon.
 \tag{17}
\]

For details, `|a^j-1|<=j(5/4)^(j-1)z`, `b_0^(-2)<=4`, and
`b_0^(-3)<=8`. The differences of the last two powers from one are
at most 20z and 76z respectively. Thus the two error coefficients in
(17) are bounded by 4405/64<70 and 13757/32<440. The extra epsilon
coefficient is `(5/4)^5*8<25`. Direct upper bounds give
`R_1<=3125/256<13` and `|R_2|<=9375/128<80`.

The bounds (9) and `|p-q|<=epsilon`, along a horizontal and a vertical
segment in (epsilon,p), imply

\[
 |K_\epsilon(p)-K_0(q)|\le5\epsilon e^{4q+1},\qquad
 |K_\epsilon'(p)-K_0'(q)|\le26\epsilon e^{4q+1}.
 \tag{18}
\]

Indeed the largest exponent on those segments is at most
`4q+5epsilon<=4q+1`. Combining (16)--(18) gives

\[
 |F_\epsilon'(q)-F_0'(q)|
 \le\pi^3\epsilon e^{4q+1}
             (440q^2+705q^3+338q^4)
 \le800\pi^3\epsilon e^{4q+1}q^2(1+q)^2.
 \tag{19}
\]

The coefficients are `338=13*26`, `705=4*70+80*5+25`, and 440.
No numerical sampling of q, theta, time, or laws is used in this bound.

## 5. The modal interval, normalization, and the spherical limit

After dividing (11) by the denominator in B_s, the contribution from
`w>=w_0`, using (14), is exactly

\[
 \frac D{32\pi^3\lambda}
       \int_0^1\int_{q_0}^\lambda
            \frac{F_{\epsilon,t}'(q)}{\sqrt{\lambda^2-q^2}}\,dq\,dt.
 \tag{20}
\]

Define the candidate limit by replacing the lower endpoint with zero and
F_epsilon with F_0. The error on `[q_0,lambda]` is bounded using (19) and
`integral_0^lambda q^2/sqrt(lambda^2-q^2)dq=pi lambda^2/4`:

\[
 \text{outer error}\le
 \frac{25\pi}{4}D\epsilon\lambda(1+\lambda)^2e^{4\lambda+1}
 \le25D\epsilon\lambda(1+\lambda)^2e^{4\lambda+1}.
 \tag{21}
\]

It remains to bound both small prefixes, not silently remove the mode.
The accepted loss-sensitive coarea estimate gives, with
`kappa=1-epsilon`, `c=4sqrt(2epsilon/kappa)`, and `v=w-v_*>=0`,

\[
 |A_t'(w)|\le\frac{2\pi^3\epsilon D}{\kappa^3}
            v e^{5\epsilon+c\sqrt v}(4+c\sqrt v).
 \tag{22}
\]

For `w<=w_0=8epsilon`, one has `kappa^(-3)<3`,
`c sqrt(v)<=17epsilon`, `5epsilon+c sqrt(v)<1`, and
`4+c sqrt(v)<5`. Therefore

\[
 |A_t'(w)|\le90\pi^3\epsilon D w.
 \tag{23}
\]

The normalizing factor multiplying the double integral in (11) is
`sqrt(epsilon)/(32sqrt(2)pi^3 lambda)`. Also
`sqrt(ell-w)>=lambda/(2sqrt(epsilon))` throughout this prefix, since
`q_0/lambda<=1/8`. Integration of (23) bounds its normalized contribution
by `256D epsilon^4/lambda^2`.

For the limit prefix, `q<=q_0<=1/16`. Equations (9) and (15) give
`|F_0'(q)|<=16pi^3 q^3`, using `exp(4q)<=2` and `1+q<=2`.
Since `sqrt(lambda^2-q^2)>=lambda/2`, its contribution in (20) is
at most `64D epsilon^4/lambda^2`. Thus the sum of the two prefix errors is

\[
 \le320D\epsilon^4/\lambda^2
 \le(5/1024)D\epsilon\le D\epsilon.
 \tag{24}
\]

Integrating these time-uniform bounds proves

\[
 \left|B_{1/\epsilon}(\lambda)
 -\frac D{32\pi^3\lambda}\int_0^1\int_0^\lambda
             \frac{F_{0,t}'(q)}{\sqrt{\lambda^2-q^2}}dq\,dt\right|
 \le D\epsilon C(\lambda).
 \tag{25}
\]

All exchanges are justified by bounded exponential tilts, the explicit
integrable square-root kernel, and the uniform modal bounds. In particular
the right side of (25) tends to zero for each fixed lambda. The existing
spherical-tail theorem (4) independently identifies the limit of B as
J(lambda). Consequently there is also the exact identity

\[
 \boxed{J(\lambda)=\frac D{32\pi^3\lambda}
       \int_0^1\int_0^\lambda
             \frac{F_{0,t}'(q)}{\sqrt{\lambda^2-q^2}}dq\,dt.}
 \tag{26}
\]

The same argument identifies (26) for any fixed positive lambda by taking
epsilon sufficiently small: use (21) and the unreduced prefix bound
`320D epsilon^4/lambda^2`, which both tend to zero; the radial split is
valid once `4epsilon/lambda<=1/8`. The quantitative statement (3) uses
lambda>=1/2.
Equations (25)--(26), followed by rescaling, prove Theorem 1.
For D=0 the nonnegative replica integrals vanish, so the whole hinge curve
vanishes by moment uniqueness. Formula (4) then gives J=0 as well.

Identity (26) retains time averaging. It asserts no sign of F_0', of an
individual pair contribution, or of an instantaneous transformed measure.
The known obstructions to such stronger claims are unaffected.

## 6. Exact calibration and the remaining sign obligation

Take equal masses at `+/-e1`, contracted to `+/-r e1`, `0<=r<=1`.
This already-known positive class is only a normalization control. Here

\[
 D=2(1-r^2),\qquad
 J(\lambda)=\int_0^1[\log\cosh(\lambda z)
                         -\log\cosh(r\lambda z)]dz.
\]

For `1/2<=lambda<=2`, differentiating log cosh with respect to r^2 and
using `tanh(x)>=x exp(-4)` for `0<=x<=2` yields

\[
 J(\lambda)\ge D\lambda^2e^{-4}/12\ge D/3888.
 \tag{27}
\]

The bound on tanh follows from `sinh x>=x`, `cosh x<=exp(x)`; continuity
handles r=0. We used `exp(1)<3`. Also
`C(2)<1+450*3^9=8857351`. Hence `s=2^37` satisfies (6) for this whole
calibration, including r arbitrarily close to one. The size of this
conservative bound is not a recommended variance or a new two-point theorem.
It checks that the proposed certificate does not divide by a vanishing D.

For a general compact family, the unsolved input is a certified positive
lower bound for `J/D` on the specified spherical parameter interval, along
with a tail that actually overlaps. The new transfer removes the absolute
Gaussian approximation error at small loss; it does not prove that missing
sign, a complete frontier cover, or unrestricted majorisation.

The finite checker verifies the rational coefficient budgets, the radial
derivative identity as a formal Laurent polynomial, the modal constant chain,
and the calibration's common variance budget. The Gaussian, coarea, limit,
and arbitrary-law arguments are the written proof, not formalized facts or
claims inferred from a finite grid.
