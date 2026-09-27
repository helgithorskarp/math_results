# A uniform middle-sign certificate at a dominant-atom boundary

Author proof, 27 September 2026. Independent review and formalization are
pending. The unrestricted three-dimensional question remains open.

The preceding small-mass theorem fixes the rare law and the contraction
before choosing how small the mass must be. Here the mass bound is explicit
and uniform over **all** rare laws and contractions in a bounded region.
The margin is proportional to the actual pair-distance loss, even when
all distances to the dominant atom are preserved. The support radius and
variance are fixed; they need not satisfy the earlier high-noise condition.

## 1. Statement

Let `nu` be any probability measure in `B(0,R)` in `R^3`, and let
`T:{0} union supp(nu) -> R^3` be 1-Lipschitz with `T(0)=0`. Set

\[
 \mu_\alpha=(1-\alpha)\delta_0+\alpha\nu,\quad
 f=\mu_\alpha*\gamma_s,\quad g=T_\#\mu_\alpha*\gamma_s,\quad
 C_s=(2\pi s)^{-3/2},
\]
\[
 H(u)=\int(g-C_su)_+-\int(f-C_su)_+,\qquad
 d=\frac{\mathbb E[|X-X'|^2-|TX-TX'|^2]}s,
 \quad X,X'\stackrel{\rm iid}{\sim}\mu_\alpha.
 \tag{1}
\]

The two hinge integrals are over `R^3`. An atom and its image at arbitrary
locations can be translated separately to this normalization.
Write `rho=R/sqrt(s)>0`. For any finite `L>0`, define

\[
 W=\rho+\sqrt{2L+1},\qquad c=4\rho\sqrt{2L},
\]
\[
 P=220+45c+105L+2c^2+10cL,\qquad
 \alpha_*(\rho,L)=\min\left\{\frac14,
                   \frac{e^{-\rho W}}{2\rho^2P}\right\}.
 \tag{2}
\]

**Theorem 1.** If `0<=alpha<=alpha_*(rho,L)`, then for every
`exp(-L)<=u<=1`, with `ell=-log u`,

\[
 \boxed{
 H(u)\ge \frac{u d e^{-5\rho^2}}{6\sqrt\pi}
                      (\ell-2\alpha)_+^{3/2}\ge0.}
 \tag{3}
\]

There is no atom-count bound, minimum rare-atom weight, covariance lower
bound, geometric genericity condition, or positive lower bound on `d`.
The rare law can be nonatomic. For `d=0`, the entire hinge curve is zero.
The case `R=0` has this trivial conclusion without using (2).

**Corollary 2 (an exact fixed-variance middle region).** At `s=1`, for
every `nu` in `B(0,1)`, every anchored contraction as above and
`0<=alpha<=2^(-21)`,

\[
 H(u)\ge0\quad(u\ge2^{-11}),\qquad
 \boxed{H(u)\ge2^{-24}d\quad(2^{-11}\le u\le1/4).}
 \tag{4}
\]

This is an actual sign and a loss-normalized middle margin, not a modulus
conditional on unknown positive samples. It covers a full prior region
uniformly over the remaining geometry. The ratio `R^2/s=1` is outside the
previous radius-only hypothesis `R^2/s<=1/2`. The dominant-mass restriction
is explicit and substantial; no statement for general prior weights is
being inferred.

Neither (3) nor (4) signs the thresholds below its displayed floor.
Combining with independently certified lower endpoints gives full
majorisation only if the two ranges overlap. There is no assertion that
the general rational-frontier tail cutoff overlaps (4), and no new
Kneser--Poulsen consequence is claimed.

## 2. A local form of the lifted Abel identity

Scale to `s=1` and henceforth write `R` for the dimensionless radius `rho`.
Let `Delta(x,x')=|x-x'|^2-|Tx-Tx'|^2`. For `0<=t<=1`, define

\[
 Z_t(x)=(\sqrt{1-t}x,\sqrt t\,Tx)\in\mathbb R^6,
 \qquad K_x(z)=e^{-|z-Z_t(x)|^2/2},
\]
\[
 Q_t(z)=\mathbb E K_X(z),\quad V_t(z)=-\log Q_t(z),\quad
 h_t(z)=\frac{\mathbb E[\Delta(X,X')K_X(z)K_{X'}(z)]}{Q_t(z)^2}.
 \tag{5}
\]

In particular `0<=h_t<=4R^2`, `V_t>=0`, and
`{V_t<=w}` is contained in `B(0,R+sqrt(2w))`.
The exact [replica/Hankel identity](../gaussian_majorisation_hankel_transport/PROOF.md)
is, for integers `k>=2`,

\[
 a_{k-2}:=\int_0^1u^{k-2}H(u)\,du
 =\frac{\sqrt{k}}{32\pi^3}
           \int_0^1\int_{\mathbb R^6} e^{-kV_t(z)}h_t(z)\,dz\,dt.
 \tag{6}
\]

This identity does not require high noise or global convexity of `V_t`.
We record how it can be used on a finite level interval without assuming
regularity at distant levels. Put `Phi(ell)=exp(ell)H(exp(-ell))` and

\[
 \Psi(\ell)=\int_0^\ell(\ell-v)\Phi(v)\,dv.
\]

Then

\[
 \boxed{\Psi(\ell)=\frac1{16\pi^3\sqrt\pi}
    \int_0^1\int_{\mathbb R^6}(\ell-V_t(z))_+^{1/2}h_t(z)\,dz\,dt.}
 \tag{7}
\]

To verify this, take the Laplace transform at integer `k>=2`. Two
integrations in `ell` divide the left transform by `k^2`, so (6) gives
`k^(-3/2)/(32pi^3)` times the spatial integral in (6). The right transform
is the same because `Gamma(3/2)=sqrt(pi)/2`. The right side of (7) is
continuous and has polynomial growth, by the support bound following (5).
The left side is continuous and at most exponential, since `|H|<=1`.
Equality of these integer Laplace transforms implies equality everywhere:
with `u=exp(-ell)`, the difference multiplied by `u` is integrable on
`[0,1]` and has every polynomial moment zero. Polynomial approximation
and then continuity conclude the argument. Fubini is justified separately
by absolute integrability on the left and nonnegativity on the right.

Suppose on the sublevels needed for `0<=w<=L` each `V_t` has one minimum
`z_t^*`, of value `v_t^*`, and is strictly convex on a ball containing
those sublevels and their segments from the minimum. Along each ray let
`r=r(w-v_t^*,theta)` solve `V_t(z_t^*+r theta)=w`. Set

\[
 A_t(w)=\int_{S^5}\frac{h_t(z_t^*+r\theta)r^5}
                         {(V_t)_r(z_t^*+r\theta)}\,d\theta
                  \quad(w>v_t^*),
 \tag{8}
\]

and set it to zero below the minimum. If `A_t=O((w-v_t^*)^2)` and
`A_t'=O(w-v_t^*)` at the minimum, polar coordinates in (7), followed by
two differentiations, give the **local** identity

\[
 \Phi(\ell)=\frac1{32\pi^3\sqrt\pi}
   \int_0^1\int_0^\ell\frac{A_t'(w)}{\sqrt{\ell-w}}\,dw\,dt
                         \quad(0\le\ell\le L).
 \tag{9}
\]

The stated modal bounds remove boundary atoms. Local smoothness and the
uniform estimates below justify differentiation, also after integrating
in `t`. No coarea regularity or convexity above this finite level range
is used. Formula (9) agrees with the earlier
[high-noise normalization](../gaussian_majorisation_high_noise_window/PROOF.md);
(7) explains the localization needed in the present large-radius setting.

## 3. Dominant mass controls posterior curvature on the needed sublevels

Fix `t` and suppress its subscript. The normalized mixture factor is

\[
 Q(z)=e^{-|z|^2/2}p(z),\qquad
 p(z)=1-\alpha+\alpha\mathbb E_\nu
               e^{z\cdot Z_t(X)-|Z_t(X)|^2/2}.
 \tag{10}
\]

Since `|Z_t(X)|<=R`, Gaussian differentiation yields

\[
 0\preceq D^2\log p(z)=\operatorname{Cov}_z(Z_t(X)),\qquad
 \|D^2\log p(z)\|\le
          \frac{\alpha R^2e^{R|z|}}{1-\alpha}.
\]

For `alpha<=1/4`, on `B(0,W)` this is bounded above by

\[
 \delta:=2\alpha R^2e^{RW}\le P^{-1}.
 \tag{11}
\]

Thus `(1-delta)I<=D^2V<=I` on this ball. A global minimum of `V`
exists, and every stationary point has `z=E_z Z_t(X)`, hence `|z|<=R`.
Strict convexity on `B(0,W)` therefore gives a unique global minimum
`z_*`. Moreover

\[
 |z_*|\le R,\qquad0\le v_*\le V(0)\le-\log(1-\alpha)
                                      \le2\alpha\le1/2.
 \tag{12}
\]

Every sublevel with `w<=L+1/2` lies in `B(0,W)`. These sets are convex,
and the ray from `z_*` meets their boundaries exactly once. On a ray
write

\[
 B(r\theta)=\log p(z_*+r\theta)-\log p(z_*)-r\theta\cdot z_*.
\]

Here `grad log p(z_*)=z_*`. Consequently

\[
 V(z_*+r\theta)-v_*=r^2/2-B(r\theta),\quad
 0\le B\le\delta r^2/2,\quad0\le B_r\le\delta r,
 \quad0\le B_{rr}\le\delta.
 \tag{13}
\]

For `v=w-v_*>0`, put `r_0=sqrt(2v)`, `q=r/r_0`,
`a=V_r/r`, and `b=V_rr`. As long as `v<=L`, all points in question
lie in the preceding sublevels and

\[
 1\le q\le(1-\delta)^{-1/2}\le1+\delta,\qquad
 1-\delta\le a,b\le1.
 \tag{14}
\]

The last bound on `q` is valid for `delta<=1/4`, which follows from
`P>=220`. These estimates and boundedness of the kernels on this compact
ball also prove the two modal bounds used in (9), uniformly in `t`.

## 4. Angular averaging supplies the sign

Assume `d>0`. Normalize the pair-loss measure to the probability law

\[
 d\eta(x,x')=d^{-1}\Delta(x,x')\,d\mu_\alpha(x)d\mu_\alpha(x').
\]

For a fixed pair write `S=Z_t(x)+Z_t(x')` and
`E=(|Z_t(x)|^2+|Z_t(x')|^2)/2`. Its contribution to `h/d` is

\[
 \frac{e^{z\cdot S-E}}{p(z)^2}
 =C_{x,x'}\exp\{r\theta\cdot\beta-2B(r\theta)\},\quad
 \beta=S-2z_*,\quad
 C_{x,x'}=\frac{e^{z_*\cdot S-E}}{p(z_*)^2}.
 \tag{15}
\]

In particular `|beta|<=4R` and `C_(x,x')>=exp(-5R^2)`. The latter
uses `E<=R^2`, `|z_*|<=R`, `|S|<=2R`, and
`p(z_*)<=exp(R|z_*|)`. The prefactor is independent of `theta`.

Differentiate the single-pair coarea integrand `h_pair r^5/V_r`, using
`d/dw=V_r^(-1)d/dr`. The exact first-derivative formula, also recorded in
the [loss-proportional continuity proof](../gaussian_loss_normalized_hinges/PROOF.md),
shows that after dividing by `C_(x,x') r_0^2` the integrand is

\[
 e^{r\theta\cdot\beta-2B}\,F,\qquad
 F=\frac{q^3}{a^2}u_\theta
       -\frac{2q^2rB_r}{a^2}
       +q^2\left(\frac5{a^2}-\frac b{a^3}\right),
 \quad u_\theta=r_0\theta\cdot\beta.
 \tag{16}
\]

The corresponding quadratic-potential integrand is
`exp(u_theta)(u_theta+4)`. Its angular average is positive:

\[
 \int_{S^5}e^{u_\theta}(u_\theta+4)\,d\theta
       \ge4\int_{S^5}e^{u_\theta}\,d\theta\ge4\pi^3.
 \tag{17}
\]

The first inequality pairs antipodal points and uses `x sinh(x)>=0`;
the second uses `cosh(x)>=1`. Individual rays need not have the sign in
(17). Keeping the angular average is essential to this estimate.

Here are explicit perturbation budgets. With the `c` in (2), let

\[
 U=c+5L,\quad V_0=72+12c+20L,\quad
 J=3V_0+2U(c+4).
 \tag{18}
\]

By (13)--(14), `|u_theta|<=c` and

\[
 |r\theta\cdot\beta-2B-u_\theta|\le\delta U,
 \qquad |F-(u_\theta+4)|\le\delta V_0.
 \tag{19}
\]

For the second bound, the coefficient of `u_theta` differs from one
by at most `12delta`, since `q<=1+delta`, `a>=1-delta` and
`delta<=1/4`. The `B_r` term is at most `19delta L`, using
`q^2/a^2<=25/9<3` and `r^2<=25L/8`. For the final term,

\[
 |a^{-2}-1|\le4\delta,\quad
 |b a^{-3}-1|\le11\delta,\quad
 |q^2-1|\le9\delta/4,
\]

which give a total error at most `71delta`. These bounds are dominated
by (18). The first inequality in (19) follows from
`|r-r_0||beta|<=delta c` and `2B<=delta r^2<=25delta L/8`.

Expansion gives

\[
 4+U+J=220+45c+105L+2c^2+10cL=P.
 \tag{20}
\]

Thus `delta<=1/P` implies `delta U<1` and `delta J<1`. For `|x|<=1`,
`exp(x)<=3` and `|exp(x)-1|<=2|x|`. Keeping the factor
`exp(u_theta)` rather than bounding it by its maximum, (19) gives

\[
 \left|e^{r\theta\cdot\beta-2B}F-e^{u_\theta}(u_\theta+4)\right|
                   \le\delta J e^{u_\theta}.
 \tag{21}
\]

By (17), its integral is at least
`(4-delta J) integral exp(u_theta)`, in particular at least `2pi^3`.
Multiply back by the prefactor and `r_0^2=2v`, and average the positive
pair-loss measure. This proves, uniformly in `t`,

\[
 \boxed{A_t'(v_t^*+v)\ge4\pi^3d e^{-5R^2}v
                                      \quad(0<v\le L).}
 \tag{22}
\]

The exact loss factor is retained even if it arises only from pairs
of rare labels. No comparison of an absolute Taylor remainder with an
arbitrarily small first or second variation is needed.

Insert (22) into (9), use
`integral_0^h v/sqrt(h-v) dv=4h^(3/2)/3`, and then (12). It follows that

\[
 H(e^{-\ell})\ge
 \frac{e^{-\ell}d e^{-5R^2}}{6\sqrt\pi}
       \int_0^1(\ell-v_t^*)_+^{3/2}\,dt
 \ge\frac{e^{-\ell}d e^{-5R^2}}{6\sqrt\pi}
                                      (\ell-2\alpha)_+^{3/2}.
\]

This is (3). When `d=0`, the nonnegative replica integrals in (6) vanish;
polynomial approximation identifies `H=0` everywhere. This also covers
`alpha=0` without defining the normalized loss measure.

## 5. Exact constants for a non-collapsed middle interval

Take `R=1`, `L=8`. Then `c=16`, `P=3572` and
`W=1+sqrt(17)<41/8`. The elementary bounds

\[
 e<11/4,\qquad e^{1/8}\le8/7
 \quad\Longrightarrow\quad e^{41/8}<161051/896<256
\]

give, at `alpha=2^(-21)`,

\[
 2\alpha P e^W
 <\frac{143818543}{234881024}<1.
 \tag{23}
\]

For instance `e<11/4` follows by summing through degree four and bounding
the remainder by `(1/120)/(1-1/6)=1/100`; the other bound follows from
the exponential series and `1/j!<=1`. Thus (2) holds. All smaller alpha
also qualify. Furthermore `e>8/3` and `2^13>3^8` imply
`e^8>2^11`, so every `u>=2^(-11)` lies in the signed range (or is above
one, where both hinges vanish).

On `2^(-11)<=u<=1/4`, we have `ell>=log 4>1` and
`ell-2alpha>3/4`. Hence `(ell-2alpha)^(3/2)>1/2`.
Using `e<3` and `sqrt(pi)<2` in (3),

\[
 H(u)\ge\frac{d}{2^{11}\cdot2\cdot243\cdot12}
                                      \ge2^{-24}d.
 \tag{24}
\]

The integer comparisons are checked in the companion script. This proves
Corollary 2, including every intermediate threshold in its intervals.

## 6. A control with zero radial loss and paired rank six

This control illustrates a boundary the uniform estimate covers; the
theorem is not inferred from it. Put six equally weighted rare source
sites at `e1,-e1,e2,-e2,e3,-e3`. Their target sites are

\[
 y(u,v)=\frac{(1-u^2-v^2,2u,2v)}{1+u^2+v^2},
\]

in the corresponding order, for

\[
 (u,v)=(0,0),(1/8,0),(0,1/8),(-1/8,0),(0,-1/8),(1/8,1/8).
 \tag{25}
\]

Add the fixed dominant origin and choose `alpha=2^(-21)`. Every rare
source and target has norm one, so every anchor-to-rare loss is zero.
All rare-pair losses are positive; their minimum is `730/429`.
The determinant of the six paired rows `(x_i,y_i)` is
`-15616/9062625`, so the paired affine rank is six. In particular a
scalar-defect certificate would force `e dot x_i=f dot y_i` from the
zero anchor losses, contradicting this determinant for unit `e,f`.
This only excludes that specified sufficient criterion, not all known
positive classes or alternative contracting motions.

The rare-pair mean loss and the full loss are exactly

\[
 B=\frac{2366536}{1254825},\qquad
 d=\alpha^2B=\frac{295817}{689847339162009600}.
 \tag{26}
\]

Corollary 2 therefore provides an exact positive middle certificate even
though the first variation in the rare mass vanishes. No numerical hinge
quadrature is used. A global 1-Lipschitz extension, if desired for the
paper's global-map formulation, follows from the same standard Kirszbraun
premise as the finite frontier. The hinge theorem itself needs only the
displayed finite contraction.

## 7. Handoff, attribution, and trust

The [previous small-mass theorem](../gaussian_majorisation_small_mass/PROOF.md)
already established signed threshold windows for each fixed rare law,
contraction and variance, including a logarithmic-square far-tail escape
window. It explicitly did not provide uniformity over those data. We do
not claim that fixed-configuration conclusion as new. The present gain is
the radius-controlled **uniform** mass budget, actual normalized margin,
and a local coarea argument that handles vanishing leading coefficients
without selecting a new budget for each rare packet.

For the finite-certificate lane, (4) excludes this entire dominant-prior
region on `[2^(-11),1/4]` at variance one, for every bounded rare packet in
the unit ball. Thresholds above that interval are also signed. This is
uniform over geometry and small loss, but it leaves the lower thresholds
and general prior weights open. It neither improves R2's separate
[rational cell](../gaussian_frontier_middle_cell/PROOF.md) nor
assumes that cell's numerical certificate. R3's
[signed endpoints](../gaussian_prior_localization/SIGNED_ENDPOINTS.md)
can be combined only after an actual range-overlap check.

The newer [full-dimensional prior cell](../gaussian_frontier_prior_cell/PROOF.md)
keeps mass at least `7/52` in each of six source boxes; it has a different
prior region and already signs all thresholds there. The
[deep-flap cell](../gaussian_deep_flap_cell/PROOF.md) also signs all
thresholds, for its fixed sixteen-site prior and coordinate boxes. Neither
is a premise or an outcome of the present uniform dominant-atom theorem.

`verify.py` checks the perturbation-budget algebra, the exact rational
constant chain (23)--(24), every pair of the control, its determinant and
its loss normalization. Its finite arithmetic is exact. The continuum
coarea localization, angular estimate, probability-law quantifiers and
Gaussian identities remain the written author proof; there is no formal
proof-assistant claim or independent review of this new result.
