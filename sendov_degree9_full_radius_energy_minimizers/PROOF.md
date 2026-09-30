# Global small-energy degree-nine minima on the full marked interval

Actual author **six-sendov-3**, role **researcher**, 2026-09-30.
Complete ordinary written author proof; independent review of this
extension is pending. Uniform analysis and cited completeness inputs
are outside a formal kernel. [LITERATURE.md](LITERATURE.md) specifies
primary sources, dependency credit and review boundaries.

The new step is a radius-parametric true angular quartic and its positive
global deficit. It removes the small marked-radius interval from the
previous global minimizer theorem. The moment inequality, spectral Gram
bound, actual stationary branch and local coefficients retain attribution.

## 1. Definitions and results

Let
\[
p(z)=c(z-a)\prod_{j=1}^8(z-z_j),\quad c\ne0,\quad
5/8\le a\le1,\quad |z_j|\le1,\quad z_j\ne a.
\]
The marked root is simple. All other original and critical algebraic
multiplicities are allowed and counted. Put
\[
d=1+a,\quad v=d^{-1},\quad\kappa=d(a-5/8),\quad
E=\sum|(a-z_j)^{-1}-v|^2,\quad
F=\sum_{p'(\zeta)=0}|a-\zeta|^{-1},\quad G=F-16v.
\]
Rotation gives the statement at any marked root of modulus `a`;
nonzero scalar factors do not affect `E,F`. The credited actual branch is
\[
P_{a,e}=(z-a)(z+e^{i(7t+m_0)})(z+e^{i(-t+m_0)})^7,
\]
\[
e=e(a,t^2)=56v^4t^2+O(t^4),\quad t>0,\quad
m_0=t^3b(a,t^2),\quad b(a,0)=(392-1197v+945v^2)/20.       \tag{1}
\]
Use the entire actual mean and exact energy inversion from
[the local theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_finite_energy_local_minimum/PROOF.md),
independently confirmed by
[the local audit](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_finite_energy_review3/PROOF.md).
The credited branch/local coefficients are
\[
K_1(a)={d^3(516d^2-528d-393)\over7168},\qquad
L(a)={1616a^2+1800a-1675\over224(1+a)^5}>0.               \tag{2}
\]

**Theorem 1.** One `e0>0`, independent of `a in[5/8,1]`, has the
following property: every `0<e<e0` has exact full-disk `E=e` minima
precisely `P_(a,e)` and its conjugate, modulo root permutation and scalar.
Uniformly on that entire marked interval,
\[
F_{\min}(a,e)=16v+\kappa e-K_1(a)e^2+O(e^3).              \tag{3}
\]
Consequently common `C,e0>0` give the sharpened universal inequality
\[
E\le e_0\quad\Longrightarrow\quad
G\ge\kappa E-K_1(a)E^2-CE^3.                             \tag{4}
\]
The quartic coefficient is optimal at each fixed radius. At `E=0` the
unique other-root multiset is eight copies of `-1`.

**Theorem 2.** There are one fixed sufficiently small `epsilon0>0`,
one possibly smaller `e0>0`, and positive uniform `c_r,c_m,c_s` such that
\[
E=e<e_0,\qquad F(p)\le F(P_{a,e})+\epsilon_0 e^2           \tag{5}
\]
puts every full-disk polynomial, after permutation and possibly
conjugation, into one fixed small coarse chart
\[
z_A=-(1-\tau_A)e^{i(7T+M)},\quad
z_j=-(1-\tau_j)e^{i(-T+M+\eta_j)},\quad\sum_{j=1}^7\eta_j=0,
\]
\[
\eta=th,\quad M-m_0=t^2y,\quad\tau=t^4r,\quad r\ge0,      \tag{6}
\]
and gives
\[
F-F(P_{a,e})\ge c_r\sum\tau_j+c_m(M-m_0)^2
                                      +c_st^2\|\eta\|^2. \tag{7}
\]
There is no smallness condition on `a-5/8` or bound on `(a-5/8)^2/e`.

**Theorem 3.** For every fixed finite `D>=0`, all full-disk `E=e`
polynomials with `F-F_min<=D e^3`, throughout `a in[5/8,1]` and for
sufficiently small energy depending on `D`, enter a fixed finite fine
box `eta=t^2x, M-m0=t^3y, tau=t^6r` and obey
\[
\mathcal C=2v^2\sum\tau_j+5v^3(M-m_0)^2+L(a)t^2\|\eta\|^2,
\qquad |F-F_{\min}-\mathcal C|\le C_Dt\mathcal C.          \tag{8}
\]
Equivalently replace the split coefficient by
`[(1616a^2+1800a-1675)/(12544(1+a))]e` and the relative error by
`C_D sqrt(e)`. This includes vanishing coordinates and every critical
collision. The fine law and its values are credited to
[the true-excess theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_true_excess_normal_form/PROOF.md);
the new conclusion is its full marked-interval global coverage.
Constants remain existential. Arbitrary quartic tolerances and energies
are outside these results.

## 2. Full radius-parametric angular quartic through collisions

For balanced real nonzero `theta`, define
\[
\mu_k=\sum\theta_j^k,\quad e_*=\mathbf1/\sqrt8,\quad
P=I-e_*e_*^*,\quad H=P\operatorname{diag}(\theta)P|_{e_*^\perp},
\quad w=\operatorname{diag}(\theta)e_*.
\]
Use full orthogonal projections onto distinct eigenspaces of `H`:
\[
\Psi=\sum_\lambda\|\Pi_\lambda w\|^4,\quad
X=\mu_4/\mu_2^2,\quad\eta_{\rm sp}=64\Psi/\mu_2^2.
\]
The invariants retain attribution to
[the angular author](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md)
and [independent angular audit](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_review3/PROOF.md).

For `z_j=-exp(i s theta_j)` the new formula is
\[
G=\kappa E-K_a(\theta)E^2+o(E^2),\qquad
K_a=A_dX+B_d-C_d\eta_{\rm sp},                            \tag{9}
\]
\[
A_d={d^3(48d^2-40d-53)\over512},\quad
B_d={d^3(16d^2-104d+203)\over8192},\quad
C_d={d^3(4d+1)^2\over8192}.                              \tag{10}
\]
The remainder is uniform on the balanced unit sphere and
`a in[5/8,1]`, including all spectral collisions. At `a=5/8` it is
exactly the credited `p(224X+122-90 eta_sp)`, `p=10985/33554432`.

Here is its coefficient derivation and uniform analytic bridge. The
classical critical-reciprocal matrix `N=diag(u)(I+11^T)` has
characteristic `9R(q)-qR'(q)`, `R=product(q-u_j)`.
It is similar to `B=S diag(u) S`, `S=P+3e_*e_*^*`. Its collapsed
background is `v(P+9e_*e_*^*)`, with external gap `8v>=4`.
The reciprocal expansion is
\[
u_j=v-iv^2\theta_js+c_2\theta_j^2s^2+ic_3\theta_j^3s^3
                                      +c_4\theta_j^4s^4+O(s^5),
\]
\[
c_2=v^2/2-v^3,\quad c_3=v^2/6-v^3+v^4,\quad
c_4=-v^2/24+7v^3/12-3v^4/2+v^5.                         \tag{11}
\]
The near invariant graph over `e_*^perp` gives the effective matrix
\[
T=vI-iv^2Hs+s^2(c_2H^2+c_Rww^*)+O(s^3),\quad
c_R=c_2+9v^3/8.                                         \tag{12}
\]
Indeed its second coefficient is `P B2 P-P B1 Q B1 P/(8v)`;
`P diag(theta^2) P=H^2+ww^*` gives (12).

Every repeated eigenspace of `H` has zero `w` weight:
`Hy=lambda y`, `y perpendicular e_*`, implies
`(diag(theta)-lambda I)y=sigma e_*`. At a diagonal value,
`sigma=0`, the vector is supported in that equal-value block and
`w*y=lambda e_*y=0`. Away from diagonal values the possible
eigenspace is one-dimensional. Thus the second coefficient on a
repeated eigenspace is exactly the scalar `c2 lambda^2 I`.
This proves the compact-uniform real-square limit
\[
s^{-4}\sum_{\rm near}[\Re(q-v)]^2
\longrightarrow c_2^2T_4+2c_2c_RU+c_R^2\Psi,             \tag{13}
\]
\[
T_4=\operatorname{tr}H^4=\mu_4/2+\mu_2^2/32,\qquad
U=w^*H^2w=\mu_4/8-\mu_2^2/64.
\]
For completeness, along any convergent sequence of radii and balanced
unit vectors, group the `H` eigenvalues by their distinct limiting
values. The orthogonal group projections converge. Eliminate
intergroup coupling in `(T-vI)/s` using only the fixed gaps between
these limiting groups. Each group matrix is
`-iv^2 H_group+s C_group+O(s^2)`. In a repeated limiting group,
`C_group` tends to `c2 lambda^2 I`. Taking real parts of a unit
right-eigenvector equation kills the anti-Hermitian first term and
gives the common scalar limit for `Re(q-v)/s^2`. A simple group has
the ordinary scalar limit. This proves sequential, hence compact,
uniformity without division by internal gaps. Also `Psi` is continuous:
a repeated limiting group's total weight tends to zero, and the sum
of squares of its split weights is at most that total squared.
This is the audited cutoff bridge with `v` now on a compact interval;
its scalar factors and external gaps remain uniformly nonzero.

Let `M_l=sum_near(q-v)^l` be analytic fixed-contour moments.
Near roots have `Re(q-v)=O(s^2)`, `Im q=O(s)` uniformly, by the
normal background and projected eigenvector equation. Scalar modulus
expansion gives
\[
\sum_{\rm near}(|q|-\Re q)=
-{\Re M_2\over2v}+{\sum[\Re(q-v)]^2\over2v}
 +{\Re M_3\over6v^2}-{\Re M_4\over8v^3}+O(s^6).           \tag{14}
\]
The balanced far root has imaginary part `O(s^3)` and loss `O(s^6)`.
The exact total trace is `2 sum u_j`.

For the full symbolic calculation put `z=q-v` and use Newton identities
to obtain `e_l` from the power sums of `u_j-v`. On the near contour,
\[
W={9R(q)-qR'(q)\over z^7(z-8v)}-1
=\sum_{l=1}^4(-1)^le_lz^{-l}{(l+1)z-(8-l)v\over z-8v}+O(s^5),
\]
\[
M_l=-l[z^{-l}]\log(1+W),\qquad
\log(1+W)=W-W^2/2+O(s^5).                               \tag{15}
\]
Balance makes `W=O(s^2)`. Terms beyond `e4` cannot affect order four;
expanding the far pole through `z^4` suffices. This is coefficient
algebra and contour integration, not interpolation from profiles.
Inserting (13)--(15) and subtracting exact `kappa E` gives
\[
[s^4](G-\kappa E)=\alpha_v\mu_4+\beta_v\mu_2^2+\gamma_v\Psi,
\]
\[
\alpha_v=-3v^3/32+5v^4/64+53v^5/512,\quad
\beta_v=-v^3/512+13v^4/1024-203v^5/8192,
\]
\[
\gamma_v=v^3/8+v^4/16+v^5/128=c_R^2/(2v).                \tag{16}
\]
Since `E=v^4 mu2 s^2+O(s^4)`, this is (9)--(10).
All moment variables and `v` remain symbolic in the new checker.
The real-square limit (13) is ordinary mathematics, not a formal certificate.

## 3. Positive angular gap on the entire interval

The credited moment and spectral Gram inequalities, including all
singular cases, give
\[
X\le43/56,\qquad\eta_{\rm sp}\ge(56X-13)/30.              \tag{17}
\]
Equality in the moment maximum is exactly the sign/permutation/scalar
orbit of `(7,-1,...,-1)`, where `eta_sp=1`. For unit vectors the reviewed
moment rounding gives `dist(theta,O)^2<6 Delta` when
`Delta=43/56-X<=1/100`, with the endpoint handled by classification.
These inequalities are inputs, not new claims of this paper.

Set `Gamma=eta_sp-(56X-13)/30>=0`. Exact algebra yields
\[
\boxed{K_1-K_a=S_d\Delta+C_d\Gamma,}\qquad
S_d={d^3(2768d^2-2456d-3187)\over30720}.                  \tag{18}
\]
For `d=13/8+q`, `q>=0`,
\[
2768d^2-2456d-3187=525/4+6540q+2768q^2>0.                \tag{19}
\]
Thus `S_d,C_d` have common positive lower bounds on `[5/8,1]`.
Equations (17)--(19) prove the exact maximum `K1` and its complete
one-plus-seven equality orbit at every radius in that interval.

Separate direct-polynomial controls use phases `n theta` repeated `m`
times and `-m theta` repeated `n` times, `m+n=8`. The critical
reciprocals are `uA^(m-1),uB^(n-1)` and the roots of
`q^2-[(m+1)uA+(n+1)uB]q+9uA uB=0`. Their scalar series give
\[
K_1-K_m={ (m-1)(7-m)\over448m(8-m)}d^3(48d^2-40d-53),
\qquad m=1,2,3,4.                                       \tag{20}
\]
The last polynomial is `35/4+116q+48q^2>0` at `d=13/8+q`.
These four controls agree exactly with the universal coefficient.
Coverage of all balanced vectors follows from (13)--(18), not the controls.

The complete angular range is also determined. Since `A_d>0`,
`X>=1/8` and `eta_sp<=1`,
\[
K_a\ge A_d/8+B_d-C_d=3d^3(d-1)^2/256.
\]
Here the spectral upper bound follows from the nonnegative weights
whose sum is `||w||^2=mu2/8`. Equality in the moment lower bound
forces four equal positive and four equal negative slopes. This
two-value vector has `Hw=0`, one active weight, and `eta_sp=1`, so it
attains equality. Continuity on the connected balanced unit sphere
therefore gives exactly the interval `[3a^2(1+a)^3/256,K1(a)]`, with
the balanced four/four minimum and singleton/seven maximum orbits.

## 4. Complete nonlinear mean and independent inward motions

Normalize `sum theta=0, ||theta||=1`. On any prescribed bounded box put
\[
\phi_j=s\theta_j+s^2y,\qquad z_j=-(1-s^4r_j)e^{i\phi_j},\quad r\ge0.
\]
The radial box may temporarily be signed for analytic calculations.
Uniformly in every coordinate and marked radius,
\[
G-\kappa E=s^4\{-v^8K_a(\theta)+5v^3y^2+2v^2\sum r_j\}+o(s^4). \tag{21}
\]
To account for every extra term, keep `mu2` symbolic and write
`R0=sum r_j`. The complete reciprocal power sums through order four are
\[
\begin{aligned}
s_1={}&(c_2\mu_2-8iv^2y)s^2+ic_3\mu_3s^3\\
 &+(8c_2y^2+c_4\mu_4+v^2R_0+3ic_3y\mu_2)s^4,\\
s_2={}&-v^4\mu_2s^2-2iv^2c_2\mu_3s^3\\
 &+\{(c_2^2+2v^2c_3)\mu_4-8v^4y^2-6ic_2v^2y\mu_2\}s^4,\\
s_3={}&iv^6\mu_3s^3+(-3v^4c_2\mu_4+3iv^6y\mu_2)s^4,\\
s_4={}&v^8\mu_4s^4.
\end{aligned}                                           \tag{22}
\]
They follow by Taylor expansion of the exact original reciprocals.
The energy quartic is `(c2^2-2v^2c3)mu4+8v^4y^2`; radial energy has
no fourth-order term. The far root's second imaginary coefficient is
`-9v^2y`, adding `(9/2)v^3y^2` to its modulus loss. In (12), mean
motion adds only the anti-Hermitian scalar `-iv^2y I` to the second
near coefficient, and inward motions start at fourth order. Thus (13)
has the same real-square limit, uniformly also in bounded `y,r`:
the repeated-group real-part argument is unchanged. Substitution of
(22) into the full traces (15), including the far modulus and exact
energy subtraction, gives precisely (21). The checker verifies the
entire identity rather than just the three pure coordinate directions.

## 5. A uniform small coarse chart on the whole marked interval

Extend the analytic mechanism of
[the rectangle proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_fixed_rectangle_minimizers/PROOF.md)
to the full compact interval; its former restricted statement is not
assumed to provide this extension. In (6), put `T=t sigma`. Exact
energy divided by `t^2` is jointly analytic on a signed small box,
including zero, with leading value `v^4(56sigma^2+||h||^2)`.
Consequently the positive branch is
\[
\sigma_0(h)=\sqrt{1-\|h\|^2/56},\quad
\partial_\sigma(E/t^2)=112v^4\sigma_0(h)>0,\quad
\sigma=\sigma_0+O(t^2).                                 \tag{23}
\]
There is no cubic energy term: leading phases are centered, mean starts
at order two, boundary energy is even in each phase, and radial energy
starts later. The analytic IFT is uniform on the compact marked interval.

The divided near matrix is led by the compression of
`diag(7sigma0,-sigma0+h_1,...,-sigma0+h_7)`. At `h=0` it has the
simple eigenvalue `6` and six copies of `-1`. These divided gaps and
the external near/far gap persist uniformly on one small `h` box.
The single near root and six-group projector are jointly analytic
through `t=0`, without an inverse internal undivided gap.

Use the credited touching scalar harmonic primitive at the branch
`u=(a+exp(i(-t+m0)))^-1`, `c=-i exp(i(-t+m0))u^2`. The full near
trace, with the simple near scalar defect restored and far modulus
added, gives an analytic support `Phi<=F` touching at the branch.
Explicitly take the branches analytic at zero in
\[
f(0)=|u|,\quad f'(w)={c(\bar u+\bar c w)\over
 \sqrt{(u+cw)(\bar u+\bar c w)}},\quad
H_{a,t}(w)=|u+cw|-\Re f(w)=(\Im w)^2K_0(a,t,w),
\]
where the square root's constant is `|u|` and `K0` is positive and
uniformly bounded on a common small disk. For the full near block
`N7`, simple near root `qn` and far root `qf`,
\[
\Phi=\Re\operatorname{tr}f((N_7-uI)/c)+|q_f|
                         +H_{a,t}((q_n-u)/c).
\]
The normalized near block has a Hermitian first coefficient, so its
Rayleigh bound and scalar squared-imaginary defect give
`0<=F-Phi<=Ct^4` on the whole coarse box, including signed radial
coordinates. At collapse the primitive is
`f0(w)=v sqrt(1+v^2w^2)-iv arsinh(vw)`. For arbitrary small phases,
the normal leading compression and `tr(P diag(phi)P)^2=
(3/4)sum phi^2+M^2` give the credited universal quadratic expansion
`F=16v+kappa v^4 sum phi^2+5v^3M^2+O(||phi||^4)`.
Its collapsed analytic support has the same expansion, also when
signed radial changes are `O(t^4)`. Since `M=O(t^2)` and exact
energy gives `e=v^4 sum phi^2+O(t^4)`, this proves
`F=16v+kappa e+O(t^4)` on the whole coarse box. All sub-four coefficients
of the analytic support difference therefore vanish jointly:
\[
\Phi-F(P_{a,e(a,t^2)})=t^4\mathscr R_4(a,t,h,y,r).         \tag{24}
\]
This is analytic divisibility on the whole box, not profile extrapolation.

The credited constrained derivatives, independently confirmed in the
local audit on every compact interval above `a_*`, give at the origin
\[
\mathscr R_4=0,\quad (\mathscr R_4)_h=(\mathscr R_4)_y=0,
\quad(\mathscr R_4)_{hh}=2L(a)I,\quad(\mathscr R_4)_{yy}=10v^3,
\quad(\mathscr R_4)_{hy}=0,\quad(\mathscr R_4)_{r_j}=2v^2.   \tag{25}
\]
Value and first angular derivatives vanish at every small `t`; the
other displayed derivatives are their limits at zero. Since `L>0`
on `[5/8,1]`, compactness and joint derivative continuity give one
fixed convex angular/radial box with positive angular Hessian on
`r=0` and positive radial gradients. Integrate the Hessian from the
origin on that face, then the radial gradients on the nonnegative
radial segment. This yields (7) uniformly on the full interval,
provided the configuration enters the chart. We prove entry next.

## 6. Full-disk global entry and exact minima

Use the independently reviewed retained cubic inequality on its full
`5/8<=a<=1` domain:
[independent cubic proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_cubic_trace_review3/PROOF.md).
Write `u_j-v=x_j+iY_j`, `I=sum Y_j`, and
\[
H_0=\sum {1-|z_j|^2\over2|a-z_j|^2}\ge0.
\]
If `sum x>=kappa E/2`, the trace gives `G>=kappa E`.
Otherwise its retained estimate implies
\[
G\ge\kappa E-K_{\rm tr}(a)E^2+H_0+I^2/256-CE^3,
\quad K_{\rm tr}={d^3(3792d^2-7728d+2991)\over28672}.      \tag{26}
\]
Only nonnegative variance and moment terms have been omitted.

The actual branch satisfies `G(P)=kappa e-K1 e^2+O(e^3)` uniformly.
The sign polynomial for `K1` at `d=13/8+q` is
`1785/16+1149q+516q^2`, so `K1` has a positive lower bound. Choose
`epsilon0` below one quarter of that bound. For small energy (5)
excludes the trace branch. Subtracting (26) from the upper comparison
and using bounded coefficients gives `H0+I^2<=C e^2` on the whole
marked interval. This proves bounded coarse parameters, not yet
closeness to the one-plus-seven orbit.

Small energy keeps all reciprocals near `v` and roots near `-1`, with
unique small lifts `z_j=-(1-tau_j)exp(i phi_j)`. Uniformly `H0` is
comparable to `sum tau`. Also
`Y_j=-v^2phi_j+O(phi_j^3+tau_j|phi_j|)`. Hence
\[
\sum\tau_j=O(e^2),\quad M={1\over8}\sum\phi_j=O(e),\quad
\|\phi-M\mathbf1\|^2=e/v^4+O(e^2).                       \tag{27}
\]
Set `s=||phi-M1||>0`, `theta=(phi-M1)/s`, `y=M/s^2`, `r=tau/s^4`.
These belong to one bounded box, independently of `a`. Thus (21)
applies with a single uniform little-oh. Using `e=v^4s^2+O(s^4)`
and subtracting the actual branch value gives
\[
{F-F(P)\over e^2}=K_1-K_a(\theta)
              +5v^3{M^2\over e^2}+2v^2{\sum\tau_j\over e^2}+o(1). \tag{28}
\]
All displayed terms are nonnegative; by (18) the first is at least
`S_d Delta`. Under (5), with one `omega(e)->0`,
\[
\Delta+M^2/e^2+\sum\tau_j/e^2\le C(\epsilon_0+\omega(e)).   \tag{29}
\]
Choose `epsilon0` smaller if necessary, then the common energy bound
small enough. Moment rounding now puts `theta` near the finite
singleton orbit. Select its singleton and conjugate if necessary
so its centered phase is positive. Decompose the phases exactly as
in (6). Moment rounding, the comparison of `t^2` with `e`, and
`m0=O(t^3)` give
\[
\|\eta/t\|+|(M-m_0)/t^2|
\le C\sqrt{\epsilon_0+\omega(e)}+O(t),\quad
\sum\tau_j/t^4\le C(\epsilon_0+\omega(e)).                \tag{30}
\]
These enter strictly inside Section 5's fixed box. The actual positive
amplitude is its IFT branch too: exact energy gives
`56(T/t)^2+||eta/t||^2=56+O(t^2)`, and the singleton choice gives
`T>0`, so `T/t=sigma0+O(t^2)`. This identifies (23), rather than
assuming entry from local strictness alone. Equation (7) proves Theorem 2.

The branch makes every small fixed-energy level nonempty. Reciprocals
lie in a compact disk about `v`, away from zero and any pole, and the
corresponding disk-root level is closed and compact. Critical-reciprocal
eigenvalue multisets and their modulus sums are continuous through
collisions. Thus a minimum is attained. Every minimum is at most the
branch value and satisfies (5), hence (7). Equality forces all three
costs to vanish and the branch or conjugate root multiset. This proves
Theorem 1. The analytic branch expansion gives (3)--(4); its actual
fixed-energy values show the quartic coefficient cannot be improved.

## 7. Entire-interval sharp true costs and evidence boundary

For fixed finite `D`, reduce energy so `D e^3<=epsilon0 e^2`.
Theorem 2 gives `sum tau=O_D(e^3)`, `|M-m0|=O_D(e^(3/2))`, and
`||eta||=O_D(e)`. Since `t^2` is uniformly comparable to `e`, every
configuration enters one finite fine box across `[5/8,1]`. The credited
true-excess theorem already applies on every compact `J subset(a_*,1]`,
so its relative law proves (8). Substitution of
`t^2=e/(56v^4)+O(e^2)` gives the stated energy version. This uses the
proved upper-defect refinement, not a lower support alone.

The new standalone checker reconstructs the complete radius-parametric
Newton/contour moments and angular/mean/radial quartic. It checks the
deficit factorization, positive shifted polynomials and four separate
direct-quadratic profiles. Coefficient records are distinguished from
checked identities. Missing/malformed/altered complete fixtures reject
under optimization. Baseline replay is validation, not new mathematics
or a new independent review.

The collision-uniform real-square limit, scalar expansion, spectral
Gram geometry, coarse IFT/support/divisibility, Taylor integration,
retained disk reduction and compactness are ordinary mathematics.
The new extension and its newer author premises remain independently
unreviewed; older reviews do not review this extension. No effective
thresholds, arbitrary-energy classification, unrestricted first-power
endpoint, all-degree theorem, new basin coefficient or historical
priority is asserted.
