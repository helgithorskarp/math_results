# A distance-loss modulus for the whole Gaussian hinge curve

Author proof, 27 September 2026. Unformalized; independent review is
pending. The full three-dimensional Gaussian-majorisation question remains
open. This is a functional estimate for finite certification, not a new
positive map class. Its hypothesis is the fixed high-noise condition
`R^2/s <= 1/2`; no limit in that ratio is taken in the certificate below.

## 1. Statement and the missing sign

Let `mu` be a probability measure in `B(a,R)` in `R^3`, and let
`T:R^3 -> R^3` be 1-Lipschitz. At covariance `s I_3`, set

\[
 C_s=(2\pi s)^{-3/2},\quad f=\mu*\gamma_s,\quad
 g=T_\#\mu*\gamma_s,\qquad
 H(u)=\int(g-C_su)_+-\int(f-C_su)_+,\quad 0\le u\le1.
 \tag{1}
\]

The integrals in (1) are over `R^3`. Define the dimensionless loss

\[
 d=\frac1s\mathbb E\big[|X-X'|^2-|T(X)-T(X')|^2\big],
 \qquad \varepsilon=R^2/s,\quad \kappa=1-\varepsilon.
 \tag{2}
\]

Here `X,X'` are independent with law `mu`. Suppose
`0<epsilon<=1/2`. Put

\[
 c=4\sqrt{2\varepsilon/\kappa},\qquad
 K_\varepsilon=
 \frac{4+\sqrt{2\pi}}{16\sqrt\pi\,\kappa^3}
 e^{5\varepsilon+c^2/2}(c+2)^2[4+c(c+2)].
 \tag{3}
\]

**Theorem 1 (global modulus proportional to loss).** For all `u,v` in
`[0,1]`,

\[
 \boxed{|H(u)-H(v)|\le d K_\varepsilon |u-v|^{1/2}.}
 \tag{4}
\]

There is also a sharper bound in the log-threshold coordinate. Set

\[
 \Phi(\ell)=e^\ell H(e^{-\ell}),\quad
 q_L=c\sqrt L,\qquad
 P_\varepsilon(q)=8+\left(7+\frac{\varepsilon}{2\kappa}\right)q
                         +\frac54q^2,
\]
\[
 B_\varepsilon(L)=\kappa^{-3}e^{5\varepsilon+q_L}
                         P_\varepsilon(q_L),\qquad
 M_\varepsilon(L)=\frac{B_\varepsilon(L)\sqrt L}{16\sqrt\pi}.
 \tag{5}
\]

**Theorem 2 (middle-interval slope).** `Phi` is continuously
differentiable on `[0,infinity)`, with `Phi(0)=Phi'(0)=0`, and

\[
 \boxed{|\Phi'(\ell)|\le d M_\varepsilon(L)
                         \quad(0\le\ell\le L).}
 \tag{6}
\]

In particular

\[
 |\Phi(\ell)|\le
       \frac{d B_\varepsilon(\ell)\ell^{3/2}}{24\sqrt\pi}.
 \tag{7}
\]

If `d=0`, the entire hinge curve is zero. If `R=0`, the same conclusion
holds directly. No minimum atom mass, number of atoms, covariance lower
bound, or positive lower bound on `d` is assumed.

The new point is the factor `d` in the modulus, including arbitrarily
small losses. A previous absolute modulus did not have this factor.
Sections 5--6 turn it into finite middle-interval tests whose prescribed
resolution does not deteriorate merely because a map approaches an
isometry. They still require certified positive values or a positive
polynomial margin. Neither theorem establishes that missing sign for an
arbitrary contraction. In particular the fixed-variance rational frontier
with large radius is not covered by the high-noise hypothesis here.

## 2. Lift, coarea, and the derivative bounds

We use the exact lifted coarea identity of the earlier
[high-noise proof](../gaussian_majorisation_high_noise_window/PROOF.md),
whose normalization and modal boundary were audited in the
[small-radius review](../gaussian_small_radius_defect_review_frontier/REVIEW.md).
We supply the additional differentiation estimates needed here.

Scale space by `sqrt(s)` and translate the endpoints independently.
This preserves the normalized hinge curve and reduces to `s=1`,
`|X|,|T(X)|<=sqrt(epsilon)`. In this proof `d` is the resulting mean
pair loss. For `0<=t<=1`, let

\[
 Z_t(X)=(\sqrt{1-t}X,\sqrt t\,T(X))\in\mathbb R^6,
 \quad K_X(z)=e^{-|z-Z_t(X)|^2/2},
\]
\[
 Q(z)=\mathbb E K_X(z),\quad V(z)=-\log Q(z),\quad
 h(z)=\frac{\mathbb E[\Delta(X,X')K_X(z)K_{X'}(z)]}{Q(z)^2},
 \quad \Delta=|X-X'|^2-|T(X)-T(X')|^2.
 \tag{8}
\]

The subscript `t` is suppressed on these functions. If `d>0`, `h>0`.
The potential has a unique minimum `z_*`, of value `v_*`, and

\[
 \kappa I\preceq D^2V\preceq I,\quad |z_*|\le\sqrt\varepsilon,
 \quad0\le v_*\le\varepsilon/2.
 \tag{9}
\]

For a ray `z_*+r theta`, write

\[
 p=V_r,\quad b=V_{rr},\quad a=p/r,\quad g=(\log h)_r.
\]

For `r>0`, both `a,b` belong to `[kappa,1]`. Along the ray,

\[
 |g|\le4\sqrt\varepsilon,\quad
 -2\varepsilon\le g'\le4\varepsilon,\quad
 |V_{rrr}|\le2\varepsilon^{3/2},\qquad
 h(z_*+r\theta)\le d e^{5\varepsilon+4\sqrt\varepsilon r}.
 \tag{10}
\]

Indeed, `g` is the difference between the loss-weighted pair posterior
mean of `(Z+Z') dot theta` and twice the ordinary posterior mean of
`Z dot theta`. Differentiating gives

\[
 g'=\operatorname{Var}_{\Delta,z}((Z+Z')\cdot\theta)
                  -2\operatorname{Var}_{z}(Z\cdot\theta).
\]

The two variances are at most `4 epsilon` and `epsilon`, respectively.
The third derivative of `V` is minus the third centered posterior
moment of `Z dot theta`; its absolute value is at most
`2 sqrt(epsilon)` times its variance. For the last inequality in (10),
remove the common factor `exp(-|z|^2/2)` from each kernel. The numerator
is at most `d exp(2|z|sqrt(epsilon))`, while the denominator is at least
`exp(-2|z|sqrt(epsilon)-epsilon)`. Then use
`|z|<=sqrt(epsilon)+r`. These arguments work for arbitrary bounded laws.

For `w>v_*`, let `r=r(w-v_*,theta)` solve `V(z_*+r theta)=w`, and set

\[
 A_t(w)=\int_{S^5}\frac{h(z_*+r\theta)r^5}{p}\,d\theta;
 \qquad A_t(w)=0\quad(w\le v_*).
 \tag{11}
\]

The sphere area is `pi^3`. Since `d/dw=p^(-1)d/dr`, differentiation
of a single integrand `J=h r^5/p` gives

\[
 J_w=h\left[\frac{r^3g}{a^2}
                     +r^2\left(\frac5{a^2}-\frac b{a^3}\right)\right],
 \tag{12}
\]
\[
 \begin{split}
 J_{ww}=h\bigg[&\frac{(g^2+g')r^2}{a^3}
  +gr\left(\frac{10}{a^3}-\frac{3b}{a^4}\right)
  +\frac{20}{a^3}-\frac{15b}{a^4}+\frac{3b^2}{a^5}
  -\frac{V_{rrr}r}{a^4}\bigg].
 \end{split}
 \tag{13}
\]

On `[kappa,1]^2`, with `kappa>=1/2`,

\[
 0\le\frac5{a^2}-\frac b{a^3}\le\frac4{\kappa^2},\qquad
 0\le\frac{10}{a^3}-\frac{3b}{a^4}\le\frac7{\kappa^3},
\]
\[
 8\le\frac{20}{a^3}-\frac{15b}{a^4}+\frac{3b^2}{a^5}
                   \le\frac8{\kappa^3}.
 \tag{14}
\]

For the first two maxima take `b=kappa`, then `a=kappa`;
the derivatives in `a` are negative there. Their minima are nonnegative
by `5a-b>=0` and `10a-3b>=0`. For the last expression its derivative
in `a` is `-15(2a-b)^2/a^6`, so its minimum is bounded below by its
value at `a=1`, which is at least 8. Its maximum is at `a=kappa`,
then at an endpoint in `b` by convexity. The value at `b=1` is no larger
than at `b=kappa`, since their numerator difference is
`3(4kappa-1)(kappa-1)<=0`.

Write `v=w-v_*>0`. The radial estimate `r^2<=2v/kappa`, (10), and
(12)--(14) prove

\[
 |A_t'(v_*+v)|\le
 \frac{2\pi^3d}{\kappa^3}
    v e^{5\varepsilon+c\sqrt v}(4+c\sqrt v),
 \tag{15}
\]
\[
 |A_t''(w)|\le \pi^3d B_\varepsilon(L)
                  \quad(v_*<w\le L).
 \tag{16}
\]

For (16), use `|g^2+g'|<=20 epsilon` in (13). The four bounds are
`8`, `7q`, `5q^2/4`, and `epsilon q/(2kappa)`, with the common factor
`h/kappa^3` and `q=4 sqrt(epsilon)r<=q_L`.

These estimates are uniform in `t`. At the mode, `A_t=O(v^2)` and
`A_t'=O(v)`. Extending by zero, `A_t` is continuously differentiable;
`A_t'` is locally Lipschitz and its almost-everywhere derivative is the
extension of (13), integrated over the sphere. There is no boundary atom.
In particular (16) is a bound on a weak as well as a classical derivative.
It is not asserted that `A_t''` is continuous across the mode.

## 3. Abel inversion and the local slope

The exact earlier identity, including its constant, is

\[
 H(e^{-\ell})=\frac{e^{-\ell}}{32\pi^3\sqrt\pi}
       \int_0^1\int_0^\ell
            \frac{A_t'(w)}{\sqrt{\ell-w}}\,dw\,dt.
 \tag{17}
\]

For clarity, it follows from the moment identity

\[
 \int_0^1 u^jH(u)\,du=
 \frac{\sqrt{j+2}}{32\pi^3}
          \int_0^1\int_0^\infty e^{-(j+2)w}A_t(w)\,dw\,dt.
\]

Integration by parts has no modal atom because of (15); the Laplace
transform of `w^(-1/2)/sqrt(pi)` is `k^(-1/2)`. The right side of
(17) therefore has all the same polynomial moments as `H`.
Estimate (15) makes it integrable and continuous, also at `u=0` after
multiplication by `u`; uniqueness by polynomial approximation proves
(17). This is the normalization already audited in the cited review.

Since `A_t'(0)=0` and (16) bounds its weak derivative, differentiation
of its half integral gives

\[
 \Phi'(\ell)=\frac1{32\pi^3\sqrt\pi}
       \int_0^1\int_0^\ell
                 \frac{A_t''(w)}{\sqrt{\ell-w}}\,dw\,dt.
 \tag{18}
\]

One can justify this by first writing `A_t'(w)=integral_0^w A_t''(z) dz`
and using Fubini. A half integral of a bounded function is continuous,
including at zero, uniformly in `t` on compact intervals. Thus (18)
does not assume a regular level common to every time. Integrating (16)
over `w` proves (6). Applying the same estimate up to `ell` and
integrating `sqrt(w)` proves (7).

If `d=0`, all the nonnegative pair integrals in the moment identity
vanish, and the continuous hinge curve is identically zero. This also
handles the zero-loss case without division by `d`.

## 4. A global one-half modulus

Extend `A_t'` by zero to negative arguments, and put

\[
 \eta_t(w)=e^{-w/2}A_t'(w),\qquad
 k(v)=e^{-v/2}v^{-1/2}\quad(v>0),\qquad
 F_t=k*\eta_t.
\]

From (15), using `w=v_*+v` and `v_*>=0`,

\[
 \|\eta_t\|_\infty\le\pi^3d W_\varepsilon,\qquad
 W_\varepsilon=\frac2{\kappa^3}e^{5\varepsilon+c^2/2}
                         (c+2)^2[4+c(c+2)].
 \tag{19}
\]

Here is a direct global bound, without choosing a cutoff. For `j=2,3`,
the maximum of `r^j exp(-r^2/2+cr)` is at
`r_j=(c+sqrt(c^2+4j))/2<=c+sqrt(j)<=c+2`, and its exponential factor
is at most `exp(c^2/2)`. Apply this separately to `4r^2+cr^3` in
(15). No asymptotic assertion is used.

The positive decreasing kernel `k` has integral `sqrt(2pi)`. For
`h>=0`, translation of the kernel, extended by zero to the left, gives

\[
 |F_t(\ell)|\le\pi^3d W_\varepsilon\sqrt{2\pi},\qquad
 |F_t(\ell+h)-F_t(\ell)|
       \le4\pi^3d W_\varepsilon\sqrt h.
 \tag{20}
\]

Indeed its translation difference in `L1` is at most
`2 integral_0^h k(v) dv<=4 sqrt(h)`. Rewriting (17),

\[
 H(u)=\frac{\sqrt u}{32\pi^3\sqrt\pi}
                         \int_0^1 F_t(-\log u)\,dt.
\]

For `0<u<=v<=1`, use
`u log(v/u)<=v-u` and `sqrt(v)-sqrt(u)<=sqrt(v-u)` in (20).
The resulting constant is
`W_epsilon(4+sqrt(2pi))/(32sqrt(pi))`, exactly (3).
Continuity and `H(0)=0` include the endpoint `u=0`, proving Theorem 1.

## 5. Finite certificates on a non-collapsed middle interval

The following tests apply at the **same fixed variance** as Theorems
1--2. Supply signed endpoint controls

\[
 H(u)\ge0\quad\text{on }[0,a]\cup[b,1],\qquad0<a<b<1.
 \tag{21}
\]

For finite data the team's
[signed endpoints](../gaussian_prior_localization/SIGNED_ENDPOINTS.md)
give one possible source of (21), after the appropriate spatial/variance
normalization. The high-noise window gives an additional upper-threshold
control. The present result does not replace these hypotheses by a
positive absolute error.

**Log-grid test.** Let `ell_0=-log b<...<ell_n=-log a`. If `d>0`, obtain
rigorous lower bounds `Phi(ell_i)>=d m_i` with `m_i>=0`. It suffices that

\[
 m_i+m_{i+1}\ge
 M_\varepsilon(\ell_{i+1})(\ell_{i+1}-\ell_i)
                         \quad(0\le i<n).
 \tag{22}
\]

To prove this, propagate the two endpoint lower bounds into each interval
with the slope bound (6). The intervals reached with nonnegative lower
bound have lengths `m_i/M` and `m_(i+1)/M`; (22) makes them cover.
This proves `H>=0` on `[a,b]`, hence zero global defect by (21).
There is no unproved inference from sample signs alone.

The team's [relative hinge oracle](../gaussian_prior_localization/RELATIVE_HINGE.md)
uses a physical relative hinge with denominator `C_s u`.
Its adverse sign is opposite to ours, and our `Phi` is `C_s` times the
favorable relative hinge. These sign and scale factors must be applied
before using (22). An oracle enclosure must itself be rigorous; this note
does not certify values supplied from floating-point sampling.

**Moment test.** Use the existing complete-moment notation

\[
 a_j=\int_0^1u^jH(u)\,du,\quad
 b_{N,k}=(N+1)\binom Nk\sum_{r=0}^{N-k}(-1)^r\binom{N-k}r a_{k+r},
\]
\[
 P_N(u)=\sum_{k=0}^N\binom Nk u^k(1-u)^{N-k}b_{N,k}.
 \tag{23}
\]

These are the [previous global criterion's](../gaussian_majorisation_global_criterion/PROOF.md)
beta averages and Bernstein--Durrmeyer polynomial, not new moment tests.
Its elementary kernel variance bound, combined with (4), gives the new
loss-scaled error

\[
 \boxed{\|P_N-H\|_\infty
                  \le d K_\varepsilon(N+2)^{-1/4}.}
 \tag{24}
\]

In detail, take `J~Bin(N,u)` and conditionally
`U~Beta(J+1,N-J+1)`. Then `P_N(u)=E H(U)` and
`E(U-u)^2<=1/(N+2)`. Two applications of Jensen to (4) prove (24).

Consequently a certified polynomial bound

\[
 P_N(u)\ge d K_\varepsilon(N+2)^{-1/4}\quad(a\le u\le b)
 \tag{25}
\]

together with (21) proves **zero** global defect. In computation, an
upper enclosure of the constant in (25) and lower enclosures of the
coefficients suffice; polynomial nonnegativity on the interval still
requires an exact or validated certificate. This is not the assertion
that finitely many nonnegative beta tests alone imply majorisation.

If the actual middle margin satisfies `H(u)>=d eta` on `[a,b]`, with
`eta>0`, every degree obeying

\[
 N+2>(2K_\varepsilon/\eta)^4
 \tag{26}
\]

makes (25) strict. Thus the required degree is uniform as `d` tends to
zero, provided the **normalized** middle margin stays positive. The
prior absolute error gave no such uniformity. For exact finite inputs,
strictness also allows finite-precision moment enclosures and a finite
subdivision/Bernstein certificate of the polynomial bound. Neither a
universal normalized margin nor a uniformly practical degree is proved.
All `d=0` cases are decided directly by the zero-loss conclusion above.

## 6. Second-energy normalization and the accepted defect bound

The second moment can supply the normalizing loss scale. The same replica
identity gives

\[
 \frac{d e^{-\varepsilon}}{16\sqrt2}\le a_0
                           \le\frac d{16\sqrt2}.
 \tag{27}
\]

For two replicas the scatter is half their squared distance, at most
`2 epsilon`. The exponential in the replica integral is therefore in
`[exp(-epsilon),1]`; its remaining constant is `1/(16sqrt(2))`.
Thus (4), (6), and (24) remain valid on replacing `d` in an upper bound
by `16sqrt(2) exp(epsilon) a_0`. This is a functional bridge from second
energy to a modulus of the **actual** hinge curve. It is not a claim that
second-energy positivity supplies the missing middle sign.

Let `Delta=max(-H)_+` and `D_N=max(0,-min_k b_(N,k))`. The accepted
[high-noise window and small-radius defect](../gaussian_majorisation_high_noise_window/SMALL_RADIUS_DEFECT.md)
give `H>=0` on `[exp(-L_epsilon),1]` and `Delta<=E(epsilon)`, where

\[
 L_\varepsilon=\frac{(4-5\varepsilon)^2}
                         {32\varepsilon(1-\varepsilon)}.
\]

Our modulus and `H(0)=0`, together with (24), therefore give

\[
 \Delta\le\min\left\{E(\varepsilon),\;
 dK_\varepsilon e^{-L_\varepsilon/2},\;
 D_N+dK_\varepsilon(N+2)^{-1/4}\right\}.
 \tag{28}
\]

This preserves the existing exponential bound and adds errors vanishing
with the loss at fixed variance. Positive errors in (28) do not establish
zero defect; (22) or (25) supplies a genuine finite sign certificate only
when its explicitly stated margins have been verified.

The linear loss scale for the whole hinge curve cannot be replaced by
`o(d)` uniformly. At `s=1`, take `mu_r=(delta_(r e1)+delta_(-r e1))/2`
and map both sites to zero. Then `d=2r^2`, and for each fixed `ell>0`,

\[
 \lim_{r\downarrow0}\frac{H(e^{-\ell})}{d}
                =\frac{e^{-\ell}\ell^{3/2}}{3\sqrt\pi}>0.
 \tag{29}
\]

Indeed `f_r=gamma+(r^2/2)partial_11 gamma+O(r^4)` and the level sphere
of `gamma` at `C exp(-ell)` has radius `sqrt(2ell)`. Differentiating the
hinge there and integrating `partial_11 gamma` over that ball gives
(29). The level is regular, so this first variation is justified by
dominated convergence. This checks the leading normalization and
sharpness of the order in (4), **not** sharpness for the adverse defect.

## 7. Computational and dependency boundary

`verify.py` checks the differentiated identity (13) as a formal rational
Laurent-polynomial identity, the factorizations used in (14), and exact
rational instances of the compact-interval constants. It also gives an
exact interval enclosure for one nonzero-radius value of `M_epsilon(L)`.
The code does not verify Gaussian hinge signs or formalize coarea/Abel
inversion. Those analytic steps are the author proof above.

The seven-factor beta obligation is closed elsewhere and is not extended
here. No beta-sign assertion beyond that work is claimed. This packet
gives the finite-atomic and relative-oracle lanes a loss-scaled error
bound; the outstanding task is an actual positive normalized middle
margin or its failure. There is no new Kneser--Poulsen consequence and
no claim of full majorisation for all bounded three-dimensional laws.
