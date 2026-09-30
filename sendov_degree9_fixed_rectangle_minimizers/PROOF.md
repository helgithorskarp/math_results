# Degree-nine minimizers on a fixed marked-radius and energy rectangle

Actual author **six-sendov-3**, role **researcher**, 2026-09-30.
Complete ordinary written author proof; independent review of this extension
is pending. The exact checker validates the universal polynomial identities,
not the analytic or global completeness arguments. No formal kernel is used.

The new step removes the restriction that `(a-5/8)^2/E` be bounded.
It uses a coarser chart, a collision-safe universal quadratic expansion, and
the retained costs themselves rather than their bounded-quotient corollary.
The stationary branch, its local derivatives, classical reciprocal matrix,
retained-cost inequality and quantitative moment rounding are credited inputs.

## 1. Definitions and quantified conclusions

Let `p=c(z-a) product_(j=1)^8(z-z_j)`, `c != 0`, with a simple marked
real root `a`, other roots in the closed unit disk, and `z_j != a`.
All other original and critical algebraic multiplicities are allowed.
Write
\[
a_0=5/8,\quad v=(1+a)^{-1},\quad \delta=a-a_0,\quad
\kappa=(1+a)\delta,\quad
E=\sum_j|(a-z_j)^{-1}-v|^2,\quad
F=\sum_{p'(\zeta)=0}|a-\zeta|^{-1},\quad G=F-16v.
\]
Scalar factors do not matter. Rotation transfers the conclusions to a
fixed nonreal marked root of modulus `a`. Only small energy is used.

The actual stationary branch from the
[local theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_finite_energy_local_minimum/PROOF.md),
independently confirmed by the
[finite-energy audit](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_finite_energy_review3/PROOF.md), is
\[
P_{a,e}=(z-a)(z+e^{i(7t+m_0)})(z+e^{i(-t+m_0)})^7,\quad E=e,
\]
\[
e=e(a,t^2)=56v^4t^2+O(t^4),\quad
m_0=t^3 b(a,t^2),\quad b(a,0)={392-1197v+945v^2\over20}.
\]
Take the positive small `t` determined by `e`. Its credited constrained
mean Hessian is `10v^3+O(e)`, its coefficient of a squared balanced
seven-root split is `t^2(L(a)+O(e))`, and each inward derivative is
`2v^2+O(e)`, where
\[
L(a)={1616a^2+1800a-1675\over224(1+a)^5},\qquad L(a_0)>0.
\]

**Theorem 1 (coarser uniform support).** There are a compact interval
`J` about `a_0` and positive `rho,t_0,c_r,c_m,c_s` such that, for `a in J`,
`0<t<t_0`, the exact energy chart
\[
z_A=-(1-\tau_A)e^{i(7T+M)},\quad
z_j=-(1-\tau_j)e^{i(-T+M+\eta_j)},\quad \sum_{j=1}^7\eta_j=0
\]
exists throughout
\[
\|\eta\|\le\rho t,\quad |M-m_0|\le\rho t^2,\quad
\sum_{j=A,1,\ldots,7}\tau_j\le\rho t^4,\quad\tau_j\ge0,       \tag{1}
\]
by solving `E=e(a,t^2)` for the positive amplitude `T` near `t`.
Throughout this chart,
\[
F(p)-F(P_{a,e})\ge c_r\sum\tau_j+c_m(M-m_0)^2
                                      +c_s t^2\|\eta\|^2.     \tag{2}
\]
Thus equality forces the same root multiset. All constants remain
existential, but the neighborhood has the stated uniform power scales.

**Theorem 2 (fixed rectangle).** There exist `delta_0,e_0>0` such that
for **every**
\[
0\le a-a_0\le\delta_0,\qquad 0<e<e_0,                       \tag{3}
\]
the full closed-disk `E=e` global minimizers of `F` are exactly `P_{a,e}`
and its conjugate, modulo root permutation and scalar factors. There is
no bound on `(a-a_0)^2/e`. The minimum is the restriction of the credited
real-analytic stationary-branch function of `(a,e)`.

**Theorem 3 (fixed quartic tolerance and global stability).** The constants
in (3) can be chosen along with a fixed `epsilon_0>0` so that every
admissible polynomial in this rectangle satisfying
\[
F(p)\le F(P_{a,e})+\epsilon_0 e^2                            \tag{4}
\]
has the coordinates (1) after permutation and possibly conjugation,
and satisfies (2). If `X=F(p)-F(P_{a,e})`, then `X>=0` and
\[
\sum\tau_j\le C X,\qquad |M-m_0|\le C\sqrt X,
\qquad\|\eta\|\le C\sqrt{X/e}.                              \tag{5}
\]
In particular every finite tolerance `D e^3`, `D>=0`, is covered after
decreasing the energy threshold to depend on `D`. The fixed `epsilon_0`
is small and existential; arbitrary positive quartic tolerances are not
asserted.

## 2. A universal quadratic expansion, without internal critical labels

The classical matrix
\[
N=\operatorname{diag}(u_j)(I+\mathbf1\mathbf1^T),\qquad
u_j=(a-z_j)^{-1},
\]
has the critical reciprocals as eigenvalues. Its characteristic polynomial
is `9R(q)-qR'(q)`, `R(q)=product(q-u_j)`. At collapse `z_j=-1`, its
eigenvalues are `v`, sevenfold on `1^perp`, and the simple far eigenvalue
`9v`. Fixed external Riesz contours give an analytic seven-dimensional
near block `N_7` and simple far root `q_f`. The intertwiner can be chosen
to be identity on `1^perp` at collapse. Since the compressed background
is scalar, its first variation is independent of the intertwiner's
commutator. All this counts multiplicities and needs no internal gap.

Put `P=I-11^T/8`. For arbitrary real original-circle phases
`z_j=-exp(i phi_j)`, let `M=sum(phi)/8`. At collapse,
\[
u_j=v-iv^2\phi_j+(v^2/2-v^3)\phi_j^2+O(\|\phi\|^3),
\]
\[
N_7=vI-iv^2 B+O(\|\phi\|^2),\quad
B=P\operatorname{diag}(\phi)P|_{\mathbf1^\perp},\quad
q_f=9v-9iv^2M+O(\|\phi\|^2).                              \tag{6}
\]
The first far variation follows from the exact total trace `2 sum u`
and `tr B=7M`. The real symmetric leading matrix `B` is essential.

Use the credited scalar harmonic support at the **collapsed** pair
`u=v,c=-iv^2`. Its primitive can here be written explicitly as
\[
f_0(w)=v\sqrt{1+v^2w^2}-iv\operatorname{arsinh}(vw),
\quad f_0(0)=v,\quad
f_0(w)=v-iv^2w+{v^3\over2}w^2+O(w^3).                    \tag{7}
\]
The branches are the ones analytic at zero. On a uniform small complex
disk its defect is
\[
0\le |v-iv^2w|-\Re f_0(w)=(\Im w)^2 K_0(a,w)\le C(\Im w)^2,
\quad K_0>0.                                               \tag{8}
\]
Define the real-analytic full near trace
\[
A_0=\Re\operatorname{tr}f_0((N_7-vI)/(-iv^2))+|q_f|.
\]
In the fixed collapse identification the normalized block is
`B+O(||phi||^2)`. Its imaginary Hermitian part is `O(||phi||^2)`.
For every right eigenvector `x` of any matrix `W`,
`Im lambda=x^* Im_Herm(W) x/(x^*x)`. Therefore **every** near normalized
eigenvalue has imaginary part `O(||phi||^2)`, uniformly through all
collisions and defective points. Equations (8) and trace calculus give
\[
0\le F-A_0\le C\|\phi\|^4.                                 \tag{9}
\]
No eigenbasis or individually analytic near-root labels are assumed.

Conjugation sends the normalized eigenvalues `w` to `-bar(w)` and the
far root to its conjugate. Since `f_0(-bar(w))=bar(f_0(w))`, the function
`A_0(phi)` is exactly even under simultaneous sign change. Thus its
linear and cubic Taylor polynomials vanish in **all** directions.
This is a parity statement for an analytic trace, not an assumption
that the true objective is analytic at the sevenfold collision.

For the quadratic term, (7) adds `v^3 tr(B^2)/2` to the near real trace.
The far modulus adds `(9/2)v^3 M^2` to its real part. The exact identity
\[
\operatorname{tr}(B^2)={3\over4}\sum\phi_j^2+M^2             \tag{10}
\]
holds for every phase vector: expand `sum_(ij) P_ij^2 phi_i phi_j`.
Adding the real total trace `2 sum Re u` therefore proves
\[
\boxed{F=16v+\kappa v^4\sum\phi_j^2+5v^3M^2
                                        +O(\|\phi\|^4).}   \tag{11}
\]
Indeed `v^2-13v^3/8=kappa v^4`. The remainder is uniform on one small
phase neighborhood and a compact marked interval. The analytic support
`A_0` has this same expansion. Exact rational polynomial verification
of (6)'s trace identities and (10)--(11) does not replace the uniform
argument (8)--(9).

## 3. Coarse energy chart and fixed divided single/six gap

Use the candidate parameter `t` and set
\[
\eta=t h,\quad \sum h_j=0,\quad M=m_0+t^2y,\quad
\tau=t^4r,\quad T=ts.                                      \tag{12}
\]
Allow signed real `r` temporarily. The exact function `E/t^2` is jointly
analytic in `(a,t,s,h,y,r)`, including `t=0`, where it equals
\[
v^4(56s^2+\|h\|^2).
\]
The desired value there is `56v^4`. Consequently, for `h` in a fixed
small ball, the leading positive amplitude is
\[
s_0(h)=\sqrt{1-\|h\|^2/56},\qquad
\partial_s(E/t^2)=112v^4s_0(h)>0.                           \tag{13}
\]
The analytic IFT gives the chart on one fixed small box. The absence
of a degree-three energy term shows `s=s_0(h)+O(t^2)`: the centered
leading phases sum to zero, the common mean is `O(t^2)`, boundary energy
is even in each phase, and radial motion starts at `t^4`. In fact
`E_tau=O(||phi||^2+||tau||)`; only the weaker fourth-order remainder
is needed here. These observations hold jointly in all coordinates.

The divided near displacement has leading matrix
\[
P\operatorname{diag}(7s_0,-s_0+h_1,\ldots,-s_0+h_7)P
                         |_{\mathbf1^\perp}.               \tag{14}
\]
At `h=0` it has a simple eigenvalue `6` on `(7,-1,...,-1)` and six
eigenvalues `-1` on the balanced seven-root split space. Small `h`
preserves fixed separated divided contours. The single near root `q_n`
and the six-group projector are jointly analytic in the coarse chart,
including `t=0`. This uses the fixed external near/far gap first, then
the divided single/six gap, and never an inverse shrinking undivided gap.

## 4. Joint fourth-order factor and uniform coercivity

Use the credited candidate-dependent touching support from
[the global bridge](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_global_energy_minimizers/PROOF.md)
and its
[independent audit](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_global_energy_review4/PROOF.md).
At the candidate's repeated root put
\[
u=(a+e^{i(-t+m_0)})^{-1},\qquad c=-i e^{i(-t+m_0)}u^2.
\]
Let `f` be the holomorphic primitive satisfying
\[
f(0)=|u|,\quad f'(w)=
{c(\bar u+\bar c w)\over\sqrt{(u+cw)(\bar u+\bar c w)}}.
\]
Its uniform scalar defect is `H(w)=(Im w)^2 K(a,t,w)`, `K>0`.
The analytic support
\[
\Phi=\Re\operatorname{tr}f((N_7-uI)/c)+|q_f|+H((q_n-u)/c)
\]
restores the simple near root's exact modulus. It obeys `F>=Phi` and
touches exactly at the actual branch. The traces count multiplicities.

In (12), on the full fixed small box, the normalized near block is
\[
(N_7-uI)/c=t(B(h)+I)+O(t^2),                                \tag{15}
\]
where `B(h)` is the real Hermitian matrix (14). The imaginary-part
Rayleigh estimate and scalar defect therefore show
\[
0\le F-\Phi\le Ct^4.                                       \tag{16}
\]
The same estimate holds for `F-A_0` in this chart: its normalized block
has Hermitian leading part `t B(h)`, and signed radial perturbations
are `O(t^4)`. Even when those signed roots leave the disk, the local
spectral and scalar identities still apply. Both supports are analytic.

The analytic `A_0` Taylor expansion from Section 2 and a bounded first
radial derivative give in this chart
\[
A_0=16v+\kappa v^4\sum\phi_j^2+5v^3M^2+O(t^4)
    =16v+\kappa e+O(t^4).                                 \tag{17}
\]
Here `M=O(t^2)` and the exact energy gives
`e=v^4 sum phi^2+O(t^4)`. Equations (16)--(17) give the same sub-four
jet for `Phi`. Subtract the branch, which has that sub-four jet too.
Joint analyticity, on the whole signed box, now proves
\[
\boxed{\Phi-F(P_{a,e(a,t^2)})=t^4\mathscr R_4(a,t,h,y,r).}   \tag{18}
\]
This accounts for every sub-four coefficient in every direction. It
does not extrapolate from profile computations or origin Hessians.

For positive `t`, the support has the credited constrained first
derivatives and angular Hessian at the branch. The six-group support
defect is fourth angular order there, as independently checked in the
finite-energy audit. Seven-root permutation symmetry makes the
mean/split mixed Hessian zero. Scale those actual derivatives in (12),
divide by `t^4`, and pass to zero using (18). One obtains at the origin
\[
\mathscr R_4=0,\quad (\mathscr R_4)_h=(\mathscr R_4)_y=0,
\quad (\mathscr R_4)_{hh}=2L(a)I,\quad
(\mathscr R_4)_{yy}=10v^3,\quad
(\mathscr R_4)_{hy}=0,\quad (\mathscr R_4)_{r_j}=2v^2.        \tag{19}
\]
The equalities for value and first angular derivatives hold for every
small `t`, and by analyticity at zero. The other displayed derivatives
are their `t=0` values. `I` here is the identity on the balanced split
space, not the reciprocal mean used below.

Since `L(a_0)>0`, compactness and joint derivative continuity choose
one small `J`, one small convex angular box and one radial box where
the angular Hessian on `r=0` is uniformly positive and every radial
gradient is uniformly positive. First integrate the angular Hessian
along the segment from the origin at `r=0`; then integrate the radial
gradients along the nonnegative segment. This gives
\[
\mathscr R_4\ge c_s\|h\|^2+c_my^2+c_r\sum r_j.
\]
Multiplication by `t^4` and (12) prove (2) and Theorem 1. No full formula
for `R_4(a,0,h,y,r)` is required, and positivity away from its small box
is not asserted.

## 5. Global entry directly from retained costs

Use the retained inequality in the
[independent cubic audit](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_cubic_trace_review3/PROOF.md),
also used explicitly in the
[independent sextic audit](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_sextic_energy_review3/PROOF.md).
Their hypotheses cover `a>=a_0` near the cutoff. Write
\[
u_j-v=X_j+iY_j,\quad H=\sum_j{1-|z_j|^2\over2|a-z_j|^2},
\quad I=\sum Y_j,\quad \xi=Y-(I/8)\mathbf1,
\]
\[
\Delta={43\over56}\|\xi\|^4-\sum\xi_j^4\ge0,\quad
A(d)=-{d^3(96d^2-196d+67)\over512}<0,\quad d=1+a.
\]
Let `V` be their nonnegative near-root real variance. If
`sum X>=kappa E/2`, the exact trace gives `G>=kappa E`. Otherwise
`sum|X|<=E` and, uniformly for `a` near `a_0` and small `E`,
\[
G\ge\kappa E-K_{\rm tr}(a)E^2+H+I^2/256+V/(2v)
                                               +(-A(d))\Delta-CE^3. \tag{20}
\]
No bounded sextic quotient is required by (20).

The credited actual branch has the uniform expansion
\[
G(P_{a,e})=\kappa e-K_1(a)e^2+O(e^3),
\]
\[
K_{\rm tr}={d^3(3792d^2-7728d+2991)\over28672},\quad
K_1={d^3(516d^2-528d-393)\over7168},\quad
K_{\rm tr}-K_1={27d^3\over448}\delta^2.                     \tag{21}
\]
Both coefficients are positive at `a_0`, equal to
`C_*=560235/8388608`. Choose the interval small enough that `K_1`
has a uniform positive lower bound; choose `epsilon_0` below one
quarter of that bound. For sufficiently small energy, (4) then lies
strictly below the trace branch `G>=kappa e`.

Subtract (20) from the branch upper comparison in (4), using (21):
\[
H+I^2/256+V/(2v)+(-A(d))\Delta
                   \le C(\delta^2+\epsilon_0+e)e^2.        \tag{22}
\]
All constants are uniform and independent of `delta^2/e`. In particular
`H,I^2,Delta<=C q e^2`, where `q=delta^2+epsilon_0+e`.
Since `sum|X|<=e`,
\[
\|\xi\|^2=e-\sum X_j^2-I^2/8=e+O(e^2),
\qquad\Delta/\|\xi\|^4\le Cq.                             \tag{23}
\]
The constants in `O(e^2)` are uniform for the small fixed interval and
tolerance. The credited quantitative moment rounding gives, when its
deficit is at most `0.01`, squared distance at most six times that
deficit from the finite sign/permutation orbit
`O={(7,-1,...,-1)/sqrt(56)}`. Choose `delta_0,epsilon_0` small, then
`e_0` small, so this deficit condition always holds. Thus
\[
\operatorname{dist}(\xi/\|\xi\|,\mathcal O)
                         \le C(\delta+\sqrt{\epsilon_0}+\sqrt e). \tag{24}
\]

Small energy localizes every original root near `-1`, with unique small
phase lifts `z_j=-(1-tau_j) exp(i phi_j)`. Uniformly `H` is comparable
to `sum tau_j`. The inverse-map expansion is
\[
Y_j=-v^2\phi_j+(v^2/6-v^3+v^4)\phi_j^3
                         +O(\phi_j^5+\tau_j|\phi_j|).       \tag{25}
\]
Consequently
\[
\sum\tau_j\le Cq e^2,\qquad
|M|\le C(\delta+\sqrt{\epsilon_0}+\sqrt e)e,
\quad M={1\over8}\sum\phi_j.                              \tag{26}
\]
Centering (25) changes the normalized direction, after sign reversal,
by `O(e)`; the centered phase norm is comparable to `sqrt e`. Pick the
singleton and conjugate if necessary so its centered phase is positive.
Decompose exactly
\[
\phi_A=7T+M,\quad \phi_j=-T+M+\eta_j,\quad\sum\eta_j=0.
\]
Projection onto the balanced seven-root split space and (24)--(26),
together with `e` comparable to `t^2` and `m_0=O(t^3)`, give
\[
\|\eta/t\|+|(M-m_0)/t^2|
                            \le C(\delta+\sqrt{\epsilon_0}+t),
\qquad \sum\tau_j/t^4\le C(\delta^2+\epsilon_0+t^2).        \tag{27}
\]
These are the coarse coordinates, not the earlier bounded-quotient
coordinates. Choosing the three small constants in order makes (27)
lie strictly inside the one fixed chart (1).

For completeness the actual amplitude belongs to the IFT branch too.
Let `h=eta/t`. Dividing its exact energy by `t^2` yields
`56(T/t)^2+||h||^2=56+O(t^2)` uniformly; the selected singleton gives
`T>0`. Hence `T/t=s_0(h)+O(t^2)`, which identifies the unique positive
chart solution from (13). This is not inferred just from local strictness.
Theorem 1 now applies to every polynomial in (4), proving Theorem 3
and the stability estimates (5).

## 6. Exact minima, attribution and evidence boundary

The full fixed-energy level is nonempty by the branch and compact.
Indeed small energy keeps every reciprocal `u_j` in a compact disk
about a positive `v` and bounds roots away from the marked root;
`z_j=a-1/u_j` is continuous there. The critical multiset is continuous
and cannot contain the simple marked root. The continuous objective
therefore attains its minimum. This is the credited compactness argument.
Every minimum has `F<=F(P)`, so (27) and (2) force all three costs to
vanish. The exact energy chart then gives the branch multiset. Both
conjugate multisets attain the same value. This proves Theorem 2.

The
[preceding parabolic theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_parabolic_energy_classification/PROOF.md)
covered every finite prescribed bound on `delta^2/e`; it did not imply
(3). Its full limiting fine-scale support is compatible with this proof,
but is not a prerequisite for the coarse factor (18). Review 7910
confirms the prior global bridge and one small parabolic window; no
independent verdict on this rectangle extension is inferred.

The standalone standard-library checker establishes exact universal
polynomial/matrix identities underlying (6), (10)--(13), (14)'s base
gap and (21), scalar-primitive parity, and positive local coefficients.
It uses all phase coordinates symbolically, rather than inferring
coverage from samples. Its corruption controls detect missing mean
cost, wrong trace compression, wrong energy norm, a collapsed divided
gap and an incorrect retained/branch correction. The previous 115-check
parabolic fixture was separately exactly replayed, with its original
record hash; that reproduction is validation, not new research.

Fixed contours, Rayleigh bounds, uniform scalar support, exact IFT,
fourth-order divisibility, continuity/integration, retained-cost
completeness and compactness are ordinary written analysis. Thresholds
are existential; neither effective constants nor a formal proof kernel
are claimed. No arbitrary-energy or arbitrary-radius classification,
unrestricted first-power endpoint, true-objective fourth-order equality,
all-degree extension, or historical priority is asserted. Previously
clarified basin coefficients and its right-sided analytic status do
not change.
