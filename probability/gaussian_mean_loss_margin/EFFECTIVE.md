# Quantitative polarization and explicit mean-loss cutoffs

27 September 2026. Complete author proof, pending independent review.
This makes the constants in [the preceding theorem](PROOF.md) effective
on its entire stated parameter range. The new step is a quantitative
reflection comparison on the **actual** source top set, stable under
removal of a small mass. It avoids a quantitative regularity assumption on
level sets and eliminates the compactness step.
The original theorem has been independently
[accepted](../gaussian_mean_loss_margin_review2/REVIEW.md); that review does
not assess the present constructive continuation.

**Concurrent result.** The prepublication refresh found R3's
[effective mean-loss theorem](../gaussian_effective_mean_loss/PROOF.md),
graph6426, source `f171c499bc0ed272d1b6fd5f78d57968d1578b62`.
It already makes the same full family effective, by an interval-component
argument, and gives better constants in its worked threshold example.
The present contribution is an alternative proof through the quantitative
midpoint and robust-polarization inequalities in Sections 2--4, together
with a compressed integer certificate. It claims no additional signed
region or priority for making the mean-loss theorem effective.

For example, at unit Gaussian variance, centered source radius `R<=1`,
source covariance at least `I/32`, and mean pair loss `D<=2^-567`,

\[
 L_g(v)-L_f(v)\ge2^{-69}vD\quad(0<v\le4\pi/3).           \tag{1}
\]

This is a uniform theorem over bounded laws and contractions, including
arbitrarily small atom masses and diffuse laws. The constants are very
conservative. A positive covariance floor and finite upper volume bound
remain hypotheses. Full dimension-three majorisation, covariance collapse,
and a uniform low-threshold sign remain open.

## 1. A rational certificate for arbitrary parameters

Use unit variance, `C=(2pi)^(-3/2)`, and the notation of PROOF.md:
center `X`, Procrustes-align the centered image `Y`, and put

\[
 |X|\le R,\quad\operatorname{Cov}(X)\succeq\kappa I,
 \quad h=Y-X,\quad M=\mathbb E|h|^2,
 \quad\Delta=|X-X'|^2-|Y-Y'|^2\ge0,
 \quad D=\mathbb E\Delta.                               \tag{2}
\]

Fix `R,kappa,r>0`; the volume range is `0<v<=omega_3 r^3`, where
`omega_3=4pi/3`. A nonempty source class necessarily has `3kappa<=R^2`.
No numerical approximation of a top set will be used.

Here is a sufficient rational certificate. Let positive rational numbers
`c_0,b,K_0,K_1,K_2,L,alpha_*,delta_2,delta_1,c_*,D_*` satisfy the following
inequalities. Exponentials only appear in this specification; Section 6
replaces all of them by compressed integer formulas.

\[
\begin{split}
 c_0&\le\frac1{64}e^{-(r+R)^2/2-(r+3R)^2},\\
 b&\le\frac1{128}e^{-(r+R)^2/2-(r+4R)^2-2R^2},\\
 K_0&\ge2R^2/\kappa,\qquad K_1\ge16R/\kappa,\\
 K_2&\ge2R e^{(r+R)^2},\qquad L\ge96R^3/\kappa+6R,
\end{split}                                                   \tag{3}
\]

\[
\alpha_*\le\min\left\{\frac12,\frac\kappa{8R^2},
 \frac\kappa{16R}e^{-(r+6R)^2/2},
 \frac\kappa{48R^2}e^{-(r+4R)^2-(r+R)^2}\right\},         \tag{4}
\]

\[
\begin{split}
 c_*&\le\min(c_0,b/8),\\
 \delta_2&\le\min\{1,R,c_*/(4K_1)\},\\
 \delta_1&\le\min\left\{\delta_2/2,\frac{\delta_2^2}{12R},
   \frac{\kappa\delta_2^2}{576R^3},
   \frac{b\kappa\delta_2^2}{48R^2}\right\},
\end{split}                                                   \tag{5}
\]

\[
\boxed{D_*\le\min\left\{
 \frac{\kappa^3}{8R^4},\quad
 \frac{\alpha_*\delta_1^2}{K_0},\quad
 \frac{\kappa\delta_2}{16R(1/2+12R^2K_0/\delta_1^2)},\quad
 \frac{c_*\delta_2^4}{8L^2K_0^2},\quad
 \frac{c_*^2\delta_2^4}{64K_2^2K_0^3}
 \right\}.}                                               \tag{6}
\]

All these choices can be made strictly positive for every positive
`R,kappa,r`. The displayed constants are sufficient, not optimal.

**Theorem 1 (effective full-rank margin).** If (2)--(6) hold and
`0<D<=D_*`, then for every `0<v<=omega_3 r^3`,

\[
 \boxed{\ \frac1v\int_{E_f(v)}(g-f)\ge(c_*/2)D.\ }        \tag{7}
\]

Here `E_f(v)` is the actual source top set, and the tested-set statement
uses the aligned image. It implies the same profile margin and
`H(u)>=(c_*/2)v(u)D` whenever `v(u)=|{f>Cu}|` belongs to the stated
range. Empty source superlevels already have `H(u)>=0`. For `D=0`,
rigidity gives equality. Scaling by `sqrt(s)` gives the fixed-variance
version with normalized loss `D/s`, radius `R/sqrt(s)`, covariance floor
`kappa/s`, and volume `v/s^(3/2)`.

## 2. The midpoint reflection inequality

Let a bounded measurable set `E` be polarized toward `y` under the
reflection `sigma` that exchanges distinct `x,y`. Thus
`1_E(z)>=1_E(sigma z)` on the half-space `P` containing `y`.
Put `m=(x+y)/2`, `l=|x-y|`, and `e=(x-y)/l`, so
`x=m+(l/2)e`, `y=m-(l/2)e`. Write

\[
 k_E(w)=\int_E\gamma(z-w)\,dz.
\]

For `z=m-te+w` in `P`, where `t>0` and `w` is orthogonal to `e`,

\[
 \gamma(z-y)-\gamma(z-x)
  =2e^{-l^2/8}\gamma(z-m)\sinh(lt/2)
  \ge lt e^{-l^2/8}\gamma(z-m).
\]

Multiply by the nonnegative indicator difference and integrate paired
points. The integral of `t gamma(z-m)` against that difference equals
`-partial_e k_E(m)`. Therefore

\[
 \boxed{\ k_E(y)-k_E(x)\ge
             l e^{-l^2/8}[-\partial_e k_E(m)].\ }          \tag{8}
\]

This uses only the classical two-point rearrangement pairing and
`sinh(t)>=t`. It converts a finite reflection displacement to a derivative
at its midpoint. In particular it supplies an explicit version of the
one-point constant in PROOF.md, without compactness or a mode limit.

## 3. Polarization survives a small exceptional mass

We need a version of (8) for the actual source top set when only most
centers lie on the favorable side. Let `mu` satisfy (2), let `E=E_f(v)`
with `0<v<=omega_3 r^3`, and put

\[
 B=r+2R,\quad a_0=C e^{-(r+R)^2/2},\quad
 w=e^{-(r+4R)^2},\quad w_1=e^{(r+R)^2}.                  \tag{9}
\]

The credited top-set estimates give `E subset B(0,B)` and its level
`a>=a_0`. Suppose a subset of source labels has mass `1-alpha`,
`alpha<=alpha_*`, and conditional law `nu` satisfying

\[
 \operatorname{Cov}(\nu)\succeq(\kappa/2)I.
\]

The conditional mean need not be zero. Its centered radius is at most
`2R`. Let `x in B(0,R)`, `y in B(0,2R)` with `x!=y`, and suppose

\[
 |y-z|\le|x-z|\quad(z\in\operatorname{supp}\nu).          \tag{10}
\]

Use the midpoint notation from Section 2, and set

\[
 b_z=(m-z).e\ge0\quad(z\in\operatorname{supp}\nu),
 \quad\bar b=\int b_zd\nu(z),\quad q=2l\bar b.
\]

The one-dimensional variance argument in PROOF.md, Section 3.1, applied
to the centered conditional law gives

\[
 q\ge\frac\kappa{2R}l,\qquad \bar b\ge\frac\kappa{4R}.    \tag{11}
\]

### 3.1. Polarization of the actual set

For a reflected pair `z,sigma z` with at least one point in `E`, both
points have norm at most `B+3R`, since `|m|<=3R/2`. Their distances to
any source center are at most `B+4R`. If `z in P`, put
`t=(m-z).e>0`. For a favorable center `a`,

\[
 \gamma(z-a)-\gamma(\sigma z-a)
 \ge 2t b_a C e^{-(B+4R)^2/2}.
\]

Indeed the ratio of the two kernels is `exp(2t b_a)` and
`exp(u)-1>=u`. For any exceptional center, the absolute difference is
at most `2t C`, because `||partial_e gamma||_infinity<=C`.
It follows that

\[
 f(z)-f(\sigma z)\ge2tC\left[
 (1-\alpha)e^{-(r+6R)^2/2}\bar b-\alpha\right]>0,         \tag{12}
\]

by (4), (11), and `alpha<=1/2`. If the unfavorable reflected point were
in `E` and the favorable one were not, (12) would be a contradiction.
Thus the ACTUAL source top set is polarized toward `y`. No comparison
between two different optimizing sets is needed.

### 3.2. The midpoint derivative keeps the favorable bias

The posterior identity (PROOF.md, equation (9)) gives

\[
 -\frac{\partial_e k_E(m)}v
 =\frac a v\int_E\int b_z
        \frac{\gamma(u-m)\gamma(u-z)}{f(u)^2}\,d\mu(z)du.
                                                               \tag{13}
\]

For `u in E`, the ratio in (13) is between `w` and `w_1`. The lower
bound follows from `|m|<=3R/2`, `|z|<=R`, `|u|<=B`; the upper bound
uses `f>=a_0`. On exceptional centers `|b_z|<=5R/2<=3R`. Hence

\[
 -\frac{\partial_e k_E(m)}v
 \ge a[(1-\alpha)w\bar b-3R\alpha w_1]
 \ge\frac{a_0w\bar b}{4}.                              \tag{14}
\]

For the second inequality, (4) ensures
`3R alpha w_1<=w kappa/(16R)<=((1-alpha)w bar b)/2`.
Combine (8), (14), `l<=3R`, `C>1/16`, and (3). This proves

\[
 \boxed{\ \frac{k_E(y)-k_E(x)}v\ge bq.\ }                \tag{15}
\]

This is a finite, quantitative comparison on the original law's top set.
It permits arbitrary shapes, critical levels, and volumes tending to
zero. Gaussian analyticity and regular-value approximation justify (13)
as in the credited proof; boundary-gradient lower bounds are unnecessary.

## 4. Repairing the approximate contraction of one rare label

The aligned map obeys `|Y(x)|<=2R` on the source ball. Split the labels at
two displacement scales:

\[
 A_i=\{|h|\le\delta_i\},\quad B_i=A_i^c,\quad
 \alpha_i=\mu(B_i)\le K_0D/\delta_i^2\quad(i=1,2).
                                                               \tag{16}
\]

The smaller core `A_1` supplies the favorable background. By (4), (6),
`alpha_1<=alpha_*`, and its conditional covariance is at least `kappa/2`.
Its conditional source mean `m_1` has norm at most `2alpha_1 R`.

Fix a rare label `x in B_2`, and write `y=Y(x)`, `l=|y-x|>delta_2`.
For any background label `a in A_1`, pair contraction implies

\[
 |y-a|^2\le|x-a|^2+\eta,\qquad \eta=6R\delta_1.           \tag{17}
\]

To see this, replace `Y(a)` by `a` in the target distance and use
`|y-a|<=3R`, `|Y(a)-a|<=delta_1`. Put

\[
 t=\eta/l^2\le1/2,\qquad y_t=(1-t)y+tx.
\]

The quadratic interpolation identity gives exactly

\[
 |y_t-a|^2=(1-t)|y-a|^2+t|x-a|^2-t(1-t)l^2
          \le|x-a|^2.                                  \tag{18}
\]

Thus `y_t` satisfies (10) for the small core. It stays in `B(0,2R)`,
moves by `|y_t-y|=eta/l`, and satisfies `|y_t-x|>=delta_2/2`.
Let

\[
 q_t=\mathbb E_{A_1}(|x-X'|^2-|y_t-X'|^2),\qquad
 q(x)=\mathbb E\Delta(x,X')=|x|^2-|y|^2+D/2.
\]

Equation (11) implies

\[
 q_t\ge q_{\min}:=\kappa\delta_2/(4R).                   \tag{19}
\]

The conditional mean bound, the two centered full-law means, and the
repair distance imply

\[
 |q(x)-q_t|
 \le D/2+12R^2\alpha_1+6R\eta/\delta_2
 \le\kappa\delta_2/(8R)=q_{\min}/2.                     \tag{20}
\]

The third constraint in (6) bounds the first two terms by
`kappa delta_2/(16R)`; the third bound for `delta_1` in (5) bounds the
last term by the same quantity. In particular `q(x)<=2q_t`.

Equation (15) compares `x` to `y_t` on the actual top set. The kernel
has `||grad k_E||_infinity<=Cv<=v`, so the repair costs at most
`eta/delta_2` after division by `v`. The last bound in (5) gives
`eta/delta_2<=b q_min/2`. Therefore

\[
 \frac{k_E(Y(x))-k_E(x)}v
 \ge bq_t-\eta/\delta_2
 \ge(b/2)q_t\ge(b/4)q(x)\quad(x\in B_2).                \tag{21}
\]

All estimates in this section are explicit and uniform; no subsequence
or limiting background has been invoked.

## 5. Combining the bulk and rare losses

Here are the credited bulk estimates, with all constants and scope
retained. The Procrustes inequality gives `M<=K_0D`. The unrounded estimate `M<=2R^2D/kappa` and the first constraint
in (6) ensure `E[XY^T]>=kappa I/2`. Conditioning on `A_2`, its
covariance stays at least `kappa/2`, and the conditional alignment and
translation change `Y` by at most `L alpha_2`. Consequently

\[
 \int_{A_2}|h|^2d\mu
 \le(32R/\kappa)\delta_2D+2L^2\alpha_2^2.                \tag{22}
\]

For clarity, this follows from the conditional Procrustes bound
`M_cond<=8R delta_2 D/(kappa(1-alpha_2)^2)` and the pointwise core loss
`Delta<=8R delta_2`. The global and conditional centered cross-covariances
differ in Frobenius norm by at most `12alpha_2 R^2`. Optimal alignment
therefore differs from identity by at most `48alpha_2 R^2/kappa`, and
the translation costs at most `6alpha_2 R`. This proves (22) with the
stated `L`. The error is quadratic in `alpha_2`.

Write `D_AB=integral_(A x B) Delta dmu dmu` without normalization. The
actual-top-set first variation, symmetrized on `A_2 x A_2`, and the
Gaussian Hessian bound give

\[
 \frac1v\int_{A_2}[k_E(Y(x))-k_E(x)]d\mu(x)
 \ge c_0D_{A_2A_2}-K_1\delta_2D
                   -L^2\alpha_2^2-K_2\alpha_2\sqrt M.   \tag{23}
\]

Indeed the positive symmetrized integrand is
`Delta+|h-h'|^2`; the mixed core/rare derivative has absolute bound
`2RC exp((r+R)^2) alpha_2 sqrt(M)`. The Taylor remainder is at most
`C/2` times (22). Inequalities (3) use `C<1` and a lower bound for its
positive coefficient, so (23) follows from the same first-variation
identity used at graph6180 and in PROOF.md.

Integrating (21) over `B_2` gives
`(b/4)(D_B2A2+D_B2B2)`. Since
`D=D_A2A2+2D_A2B2+D_B2B2` and `c_*<=min(c_0,b/8)`, these positive
terms together are at least `c_*D`. The three error budgets are

\[
 K_1\delta_2D\le(c_*/4)D,\quad
 L^2\alpha_2^2\le(c_*/8)D,\quad
 K_2\alpha_2\sqrt M\le(c_*/8)D.                         \tag{24}
\]

The last two follow from (16) and the last two constraints in (6).
Subtracting proves (7). Critical positive levels are included through the
regular-value approximation already used for the posterior identity.
This completes the effective theorem. QED.

## 6. A compressed integer schedule

For `z>0` rational, write `F(z)=floor(log_2 z)` and `G(z)=ceil(log_2 z)`.
These integers are computed by comparisons of numerator and denominator
bit lengths, without floating point. Put

\[
\begin{array}{ll}
 e_0=\lceil(r+R)^2/2+(r+3R)^2\rceil,&
 e_b=\lceil(r+R)^2/2+(r+4R)^2+2R^2\rceil,\\
 e_p=\lceil(r+6R)^2/2\rceil,&
 e_g=\lceil(r+4R)^2+(r+R)^2\rceil,\\
 e_w=\lceil(r+R)^2\rceil.&
\end{array}
\]

Since `e<4`, `exp(-z)>=2^(-2 ceil z)` and
`exp(z)<=2^(2 ceil z)` for `z>=0`. Also `1/16<C<1`, using
`3<pi<22/7`. Define

\[
\begin{split}
 a_0&=6+2e_0,\quad a_b=7+2e_b,\\
 k_0&=G(2R^2/\kappa),\quad k_1=G(16R/\kappa),\\
 k_2&=G(2R)+2e_w,\quad \ell=G(96R^3/\kappa+6R),\\
 A&=\max\{1,-F(\kappa/(8R^2)),\
            2e_p-F(\kappa/(16R)),\
            2e_g-F(\kappa/(48R^2))\},\\
 h&=\max(a_0,a_b+3),\\
 t_2&=\max\{0,-F(R),h+2+k_1\},\\
 t_1&=\max\{t_2+1,2t_2+G(12R),\
          2t_2-F(\kappa/(576R^3)),\
          a_b+2t_2-F(\kappa/(48R^2))\},\\
 j&=1+\max\{-1,G(12R^2)+k_0+2t_1\}.
\end{split}                                               \tag{25}
\]

Then take

\[
\begin{split}
 N=\max\{&0,G(8R^4/\kappa^3), A+2t_1+k_0,\
 &t_2+j-F(\kappa/(16R)),\
 &h+4t_2+3+2\ell+2k_0,\
 &2h+4t_2+6+2k_2+3k_0\},\qquad M_*=h+1.                 \tag{26}
\end{split}
\]

The choices
`c_0=2^-a_0`, `b=2^-a_b`, `K_i=2^k_i`, `L=2^ell`,
`alpha_*=2^-A`, `c_*=2^-h`, `delta_i=2^-t_i`, and `D_*=2^-N`
satisfy (3)--(6). The bound for the sum in the third denominator of (6)
is `1/2+12R^2 K_0/delta_1^2<=2^j`. This proves the schedule, including
all rounding directions. The symbol `a_0` in (25) is an integer exponent,
not the Gaussian level lower bound in (9).

| Radius R | Covariance floor kappa | Volume radius r | N | Margin exponent M_* |
|---|---|---|---:|---:|
| 1 | 1/32 | 1 | 567 | 69 |
| 1/2 | 1/384 | 9/2 | 967 | 123 |
| 3 | 3/32 | 1 | 2900 | 401 |

Each row proves `integral_E(g-f)>=2^-M_* vD` whenever `D<=2^-N`
and `0<v<=omega_3 r^3`. These are sufficient cutoffs, not observed
Gaussian signs or optimized constants. The bit representation of `N`
is small even when `2^N` would be far too large to construct.

## 7. The exact consumer interface

[effective.py](effective.py) implements (25)--(26). For rational
`R,kappa,r` it returns the exponents and their intermediate budget record.
An optional finite rational input checker verifies the source radius,
covariance floor, common probability weights and every pair contraction,
then computes the normalized loss exactly. It returns:

- `ISOMETRIC_ZERO` if the loss is zero;
- `SIGNED_BOUNDED_VOLUME` if `D<=2^-N`;
- `UNRESOLVED` if that last guard fails.

The failed guard does not supply a counterexample. The test
`ceil(log_2 D)<=-N` avoids constructing `2^N`, and all geometry checks
are rational. The checker does not approximate a Gaussian mixture or
optimize a top set.

For a threshold endpoint `u_0=2^-m`, `m>=1`, choose
`r=R+ceil(sqrt(2m))`. Because `log 2<1`, every nonempty source superlevel
with `u>=u_0` lies in `B(0,r)`. The same guard therefore signs all these
hinges. In particular, the second table row gives `H>=0` for
`u>=1/64` when `R<=1/2`, `Cov(X)>=I/384` and `D<=2^-967`.
On `[1/64,1/2]`, that source top set contains `B(0,1/2)`; its volume
exceeds `1/2`. Hence the stronger explicit bound there is

\[
 H(u)\ge2^{-124}D.                                      \tag{27}
\]

The covariance floor and loss cutoff are the hypotheses. No smallness of
`E Delta^2/D` is assumed. The preceding five-point rare-fold calibration,
scaled by `1/6`, has the required radius and covariance but a fixed second
to first loss ratio `13/63`; it eventually satisfies this new guard as
its rare mass tends to zero. That fold already has a geometric sign;
it tests the nonredundancy of the guard rather than discovering a class.

The tests in [effective_check.py](effective_check.py) compare the compressed
schedule with expanded rational inequalities (3)--(6), check finite inputs
and an exact repair identity, and reject damaged data. Their expected
record is [EFFECTIVE_EXPECTED.json](EFFECTIVE_EXPECTED.json). Finite checks
are not an independent proof of the analytic inequalities or review of
this author theorem.

## 8. What this closes for the shared frontier

The formerly unspecified small-loss neighborhood6414 now has explicit
rational guards on the SAME full-rank bounded family, both here and in
the concurrent theorem6426. R2 can evaluate the present compressed guard
before requesting Gaussian moments; R3's paired cubature preserves radius,
source covariance and mean loss, so it also preserves this guard when the
relevant marginal moments are retained. No extra mixed fourth-moment
features are needed for this particular guard.

An independently uniform low-threshold sign reaching `u_0` would combine
with the threshold version to give all-threshold comparison for every
input passing the guard in that family. Without that additional premise,
only the stated volume/threshold range is signed. The remaining compact
middle problem has positive loss above this explicit cutoff. Neither the
large size of N nor its compact encoding establishes those missing signs.
