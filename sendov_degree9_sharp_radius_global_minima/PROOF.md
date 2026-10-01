# The sharp marked-radius interval for degree-nine small-energy global minima

Actual author **six-sendov-3**, role **researcher**, 2026-10-01.
Complete ordinary written author proof; independent review of this extension
is pending. Exact algebra is reproducible separately from the analytic and
completeness arguments. [LITERATURE.md](LITERATURE.md) identifies the premises,
their actual authors, source commits and graph references.

The new mechanism is a comparison-driven, full-disk radial/mean bootstrap
valid on the entire marked interval. It does not require positivity of the
older retained trace quartic. It closes global entry above the sharp angular
threshold and selects the leading moving-pair geometry on the favorable
side of the previously proved two-family curve. The exact moving-pair
global minimum and the full transition curve remain unidentified.

## 1. Definitions and results

Let
\[
p(z)=c(z-a)\prod_{j=1}^8(z-z_j),\qquad c\ne0,\quad
0\le a\le1,\quad |z_j|\le1,\quad z_j\ne a.
\]
The marked root is simple. All other original and critical algebraic
multiplicities are allowed and counted. Put
\[
d=1+a,\quad v=d^{-1},\quad \kappa=d(a-5/8),\quad
E=\sum_j|(a-z_j)^{-1}-v|^2,\quad
F=\sum_{p'(\zeta)=0}|a-\zeta|^{-1},\quad G=F-16v.
\]
Rotation gives the same statements at a marked root of modulus `a`, using
the rotated energy. Scalar factors and permutations do not affect the
statements. At zero energy the other-root multiset is eight copies of `-1`.

The credited **entire actual stationary branch** is
\[
P_{a,e}=(z-a)(z+e^{i(7t+m_0)})(z+e^{i(-t+m_0)})^7,
\quad t>0,\quad E(P_{a,e})=e,
\]
\[
t^2={e\over56v^4}+O(e^2),\qquad
m_0=t^3w(a,e),\qquad
w(a,0)={392-1197v+945v^2\over20}.                    \tag{1}
\]
The actual stationary mean and energy inverse, uniformly defined on
`0<=a<=1`, are from graph7777 and independent local review7819. They are
never replaced by truncated means. Its uniform expansion is
\[
F(P_{a,e})=16v+\kappa e-K_1(a)e^2+O(e^3),\quad
K_1={d^3(516d^2-528d-393)\over7168}.                   \tag{2}
\]
Define the two distinct thresholds
\[
a_G={20\sqrt{1614}-385\over692},\qquad
a_*={10\sqrt{2198}-225\over404},\qquad a_*<151/250<a_G.
                                                               \tag{3}
\]
The sharp angular threshold and the exact separating signs in (3) are
credited to graph8160; local strictness above `a_*` retains7777/7819 credit.

**Theorem 1 (global radius classification).** For every nonempty compact
`J subset(a_G,1]` there is one `e_J>0` such that every `a in J` and
`0<e<e_J` has exact full-disk `E=e` minima precisely `P_(a,e)` and its
conjugate, modulo permutation and scalar. Uniformly on `J`, the minimum
has expansion (2). At each fixed radius in `[0,a_G]`, this actual branch
is nonglobal at every sufficiently small positive energy. Consequently
the marked radii where this branch is eventually globally minimizing
are exactly **`a_G<a<=1`**. The common threshold is allowed to depend on
`J`; no uniform positive threshold as `a downarrow a_G` is asserted.

**Theorem 2 (global entry and physical costs).** With `J` as above, one
sufficiently small `epsilon_J>0` and one possibly smaller `e_J>0` give:
every full-disk configuration with
\[
E=e<e_J,\qquad F\le F(P_{a,e})+\epsilon_J e^2           \tag{4}
\]
enters, after permutation and possibly conjugation, a single common small
coarse chart
\[
z_A=-(1-\tau_A)e^{i(7T+M)},\quad
z_j=-(1-\tau_j)e^{i(-T+M+\eta_j)},\quad\sum_{j=1}^7\eta_j=0,
\]
\[
\eta=th,\quad M-m_0=t^2y,\quad \tau=t^4r,\quad r\ge0.   \tag{5}
\]
Writing `a0=min J` and
\[
L(a)={1616a^2+1800a-1675\over224(1+a)^5},
\]
its physical excess satisfies
\[
F-F(P_{a,e})\ge {1\over4}\sum\tau_j
             +{5\over16}(M-m_0)^2
             +{L(a_0)\over2}t^2\|\eta\|^2.             \tag{6}
\]
The coefficients in (6) are explicit sufficient costs; the chart and
energy threshold remain existential. No arbitrary quartic tolerance is
claimed.

**Theorem 3 (true fine excess).** For each fixed finite `D>=0`, every
full-disk `E=e` configuration with `a in J` and
`F-F_min<=D e^3`, at a common sufficiently small threshold depending on
`J,D`, enters a bounded fine chart
\[
\eta=t^2x,\quad M-m_0=t^3y,\quad \tau=t^6r,
\]
and obeys
\[
\mathcal C=2v^2\sum\tau_j+5v^3(M-m_0)^2+L(a)t^2\|\eta\|^2,
\qquad |F-F_{\min}-\mathcal C|\le C_{J,D}t\mathcal C.    \tag{7}
\]
This includes vanishing coordinates and all critical collisions. The
coefficients and direct fine-law method retain independent review8102
credit; the new conclusion is global coverage above `a_G`. Replacing
`L(a)t^2` by
`[(1616a^2+1800a-1675)/(12544(1+a))]e` changes the relative error only by
`O_J(sqrt(e))`.

There are two further conclusions without a global optimizer
classification below `a_G`. Let `K_a(theta)` be the credited balanced
angular functional defined in Section 3 and set
\[
K_{\max}(a)=\max_{\sum\theta=0,\ \|\theta\|=1}K_a(\theta).
\]

**Theorem 4 (full-disk variational reduction).** Small fixed-energy minima
exist for every `0<=a<=1`, and uniformly on this entire interval
\[
F_{\min}(a,e)=16v+\kappa e-K_{\max}(a)e^2+o(e^2).         \tag{8}
\]
The function `K_max` is continuous. Above and at `a_G`, `K_max=K1`.
The definition in (8) is not an evaluation of the optimizer below `a_G`.
The full-disk to balanced-angular reduction is the new part of (8).

For the last result reuse graph8160's actual moving-pair construction
(originally graph7328)
\[
Q_{a,e}=(z-a)(z+1)^6[z^2+2(1-x)z+1],\quad
x={d^4e\over4+2ad^2e},\quad E(Q_{a,e})=e,
\]
and its actual analytic two-family equal-value curve
\[
\alpha(e)=a_G+c_{\rm eq}e+O(e^2),\quad
.132978<c_{\rm eq}<.132979.                            \tag{9}
\]
Near `(a_G,0)`, `F(Q)<F(P)` exactly when `a<alpha(e)`.

**Theorem 5 (moving-pair selection of global minima).** Let
`e_k downarrow0`, `a_k->a_G`, and `a_k<alpha(e_k)` for all sufficiently
large `k`. Choose any global full-disk `E=e_k` minimizer `p_k`. In its
unique small root lifts
\[
z_j=-(1-\tau_j)e^{i\phi_j},\quad
M={1\over8}\sum\phi_j,\quad
\theta={\phi-M\mathbf1\over\|\phi-M\mathbf1\|},
\]
one has
\[
\sum\tau_j=o(e_k^2),\qquad M=o(e_k),\qquad
\operatorname{dist}(\theta,\mathcal O_Q)\longrightarrow0,       \tag{10}
\]
where `O_Q` is the permutation orbit of
`(1,-1,0,0,0,0,0,0)/sqrt2`. In particular (10) holds at the exact
limiting radius `a=a_G`. This selects the leading original-root geometry;
it does **not** identify the exact moving-pair polynomial as the minimum
or identify `alpha` as the global phase curve.

## 2. The new comparison-driven radial and mean bootstrap

Fix any finite `D>=0` and suppose `F<=F(P_(a,e))+D e^2`, with `E=e>0`.
By (2), one `B=B_D>=1` gives uniformly for all `0<=a<=1`
\[
G\le\kappa E+BE^2.                                    \tag{11}
\]
Write
\[
u_j-v=x_j+iY_j,\quad A=\sum x_j,\quad I=\sum Y_j,\quad b=1-a^2,
\]
\[
h_j=x_j+{b\over2}|u_j-v|^2
 ={1-|z_j|^2\over2|a-z_j|^2}\ge0,\quad H_0=\sum h_j.
                                                               \tag{12}
Direct polynomial differentiation gives the characteristic identity
\[
\det(qI-N)=9R(q)-qR'(q),\quad
N=\operatorname{diag}(u)(I+\mathbf1\mathbf1^T),\quad R=\prod(q-u_j).
\]
Thus `sum q_j=2 sum u_j`, including all multiplicities, and
`G=2A+sum(|q|-Re q)>=2A`. Negative real-coordinate mass is at most
`bE/2`, by (12). Consequently
\[
\sum|x_j|\le bE+A\le(b+\kappa/2)E+(B/2)E^2,
\]
\[
b+\kappa/2={361\over512}-{1\over2}(a-3/16)^2.           \tag{13}
\]
Once `E<=1/(2B)`, this proves `sum|x_j|<=489E/512<E`.
There is no split into trace cases and no sign requirement on `kappa`.

We next extend the *unbalanced lower functional*, already exactly derived
and reviewed at graph7707, to this compact parameter domain. This uses its
symbolic identity and reestablishes its analytic hypotheses; its old
retained inequality on `[5/8,1]` is not applied below that domain.
Let `e_*=1/sqrt8`, `P=I-e_*e_*^*`, `Q=e_*e_*^*`, `S=P+3Q`.
The reciprocal matrix is similar to
\[
B=S\operatorname{diag}(u)S=v(P+9Q)+V,
\quad\|V\|\le9\sqrt E,
\quad\|\operatorname{Re}_{\rm Herm}V\|\le9E.            \tag{14}
\]
For `E<=1/1296` the fixed circle `|q-v|=1/2` separates seven near
eigenvalues from the simple far eigenvalue; the external gap is `8v>=4`.
For a normalized right near eigenvector `w`, the Q-row gives
`||Qw||<=9sqrt(E)/(8v-1/4)`. Taking real parts of its eigenvalue equation
then gives
\[
\operatorname{Re}(q-v)=8v\|Qw\|^2+w^*(\operatorname{Re}_{\rm Herm}V)w
=O(E),\qquad \operatorname{Im}q=O(\sqrt E).              \tag{15}
\]
All constants are uniform for `v in[1/2,1]`. Every eigenvalue has a right
eigenvector, so defective near clusters are covered.

Set `M_l=sum_near(q-v)^l` by the fixed contour, and let
`r_j=Re(q_j-v)`. These moments are analytic without labeling near roots.
Uniform scalar Taylor expansion using (15) gives
\[
\sum_{\rm near}(|q|-\operatorname{Re}q)
=-{\operatorname{Re}M_2\over2v}+{\sum r_j^2\over2v}
 +{\operatorname{Re}M_3\over6v^2}-{\operatorname{Re}M_4\over8v^3}
 +O(E^3).
\]
Since `sum r_j^2>=(Re M1)^2/7` and the far modulus loss is nonnegative,
\[
G\ge\mathcal L-CE^3,\quad
\mathcal L=2A-{\operatorname{Re}M_2\over2v}
 +{\operatorname{Re}M_3\over6v^2}-{\operatorname{Re}M_4\over8v^3}
 +{(\operatorname{Re}M_1)^2\over14v}.                    \tag{16}
\]
The credited complete eleven-term polynomial is
\[
\mathcal L=\kappa E+2H_0+{I^2\over128v}+\mathcal P_4+O(E^3),
                                                               \tag{17}
\]
where `X2=sum x^2`, `Y2=sum Y^2`, `XY=sum xY`, `XY2=sum xY^2`,
`Y3=sum Y^3`, `Y4=sum Y^4`, and
\[
\begin{aligned}
\mathcal P_4={}&-{59d^3\over512}Y4-{47d^2\over64}XY2
 -{83d^3\over14336}Y2^2-{3d\over4}X2
 -{59d^3\over4096}IY3+{7d^2\over128}I\,XY\\
 &+{1277d^3\over229376}I^2Y2-{677d^3\over1835008}I^4
 +{23d^2\over512}A\,Y2-{d^2\over128}AI^2+{3d\over64}A^2.
\end{aligned}                                                 \tag{18}
\]
For analytic uniformity put `x=s^2 xhat`, `Y=s Yhat`, `s=sqrt(E)`.
By (13), `||xhat||1<=1`, `||Yhat||2<=1`. This normalized set and
`v in[1/2,1]` are compact. The separated contour yields one analytic
neighborhood and bounded derivatives. The real functional is invariant
under conjugation `Y->-Y`, hence even in `s`; the weight-five term
vanishes and the weighted remainder is uniformly `O(s^6)=O(E^3)`.
This proves (17) on the extended domain, without an internal spectral gap.

The new checker obtains (18) instead from the simple far-root secular
equation and cyclic word traces, providing a different coefficient route
from the old residue calculation. It compares all eleven symbolic
coefficients, not sampled radii.

An elementary majorant suffices here. From `||x||1<=E`, `||Y||2<=sqrt E`,
\[
|A|\le E,\quad X2\le E^2,\quad Y2\le E,\quad
|XY|,|Y3|\le E^{3/2},\quad |XY2|,Y4\le E^2,
\quad |I|\le\sqrt{8E}<3\sqrt E.
\]
Bounding the eleven terms of (18), in displayed order, by multiples of
`E^2`, using `1<=d<=2`, gives respectively
\[
{59\over64},\ {47\over16},\ {83\over1792},\ {3\over2},\
{177\over512},\ {21\over32},\ {1277\over3584},\
{677\over3584},\ {23\over128},\ {1\over4},\ {3\over32}.
\]
Their sum is **`26795/3584<8`**. Thus (16)--(18), after reducing one
common energy threshold, imply
\[
G\ge\kappa E+2H_0+I^2/128-9E^2.
\]
Combining with (11) proves the new bootstrap
\[
\boxed{2H_0+I^2/128\le(B_D+9)E^2.}                    \tag{19}
\]
No positivity of the old radius-dependent trace quartic is needed.

Uniform reciprocal inversion gives unique small lifts
`z_j=-(1-tau_j)exp(i phi_j)`, `tau>=0`. Here `H0` is uniformly
comparable to `sum tau`, and
\[
Y_j=-v^2\phi_j+O(|\phi_j|^3+\tau_j|\phi_j|).
\]
Writing `M=sum phi/8`, (19) and the local inverse therefore give
\[
\sum\tau_j=O_D(e^2),\quad M=O_D(e),\quad
\|\phi-M\mathbf1\|^2=e/v^4+O_D(e^2).                  \tag{20}
\]
The centered norm is positive for small positive energy. This is a
uniform all-disk bootstrap on `[0,1]`, including `a=0,1` and collisions.

## 3. Complete mean/radial quartic and full-disk variational reduction

For balanced nonzero theta define
\[
H=P\operatorname{diag}(\theta)P|_{e_*^\perp},\quad
w=\operatorname{diag}(\theta)e_*,\quad
\Psi=\sum_\lambda\|\Pi_\lambda w\|^4,
\]
\[
\mu_l=\sum\theta_j^l,\quad X=\mu_4/\mu_2^2,\quad
\eta_{\rm sp}=64\Psi/\mu_2^2,
\quad K_a=A_dX+B_d-C_d\eta_{\rm sp},
\]
\[
A_d={d^3(48d^2-40d-53)\over512},\quad
B_d={d^3(16d^2-104d+203)\over8192},\quad
C_d={d^3(4d+1)^2\over8192}.
\]
All projections are onto full distinct eigenspaces. On any prescribed
bounded box, put `||theta||=1`, `sum theta=0`,
\[
\phi=s\theta+s^2y\mathbf1,\qquad \tau=s^4r.
\]
The reviewed symbolic-v full quartic at8046/8102 extends compact-uniformly
to all `a in[0,1]`:
\[
G-\kappa E=s^4\{-v^8K_a(\theta)+5v^3y^2+2v^2\sum r_j\}+o(s^4).
                                                               \tag{21}
\]
This includes independent radial coordinates. Signed bounded radial
coordinates can be used temporarily for the analytic construction.

We detail the parameter and collision bridge rather than importing an
old global theorem outside its domain. The literal reciprocal has the
uniform coefficients
\[
c_2=v^2/2-v^3,\quad c_3=v^2/6-v^3+v^4,\quad
c_4=-v^2/24+7v^3/12-3v^4/2+v^5.
\]
The near effective matrix is
\[
T=vI-iv^2Hs+s^2\{c_2H^2+c_Rww^*-iv^2yI\}+O(s^3),
\quad c_R=c_2+9v^3/8.                                  \tag{22}
\]
Every repeated H eigenspace has zero w-weight: its vectors satisfy
`(diag(theta)-lambda I)z=sigma e_*`; a repeated space is supported at a
repeated diagonal value, where `sigma=0` and `w*z=0`. Away from diagonal
values the eigenspace is one-dimensional. Group the H eigenvalues along
any convergent sequence by their distinct limiting values. The group
projections converge and elimination uses only fixed intergroup gaps.
At a repeated limiting value the Hermitian second coefficient is the
scalar `c2 lambda^2 I`; taking real parts of a right-eigenvector equation
gives that common coefficient even for arbitrarily small internal gaps.
The bounded mean in (22) is anti-Hermitian and leaves this argument
unchanged; radial changes start at order four. The same argument for
simple groups proves, compact-uniformly,
\[
s^{-4}\sum_{\rm near}[\operatorname{Re}(q-v)]^2
\longrightarrow c_2^2(\mu_4/2+\mu_2^2/32)
 +2c_2c_R(\mu_4/8-\mu_2^2/64)+c_R^2\Psi.               \tag{23}
\]
Repeated limiting groups have total w-weight tending to zero, so Psi is
continuous. The external gap remains at least4 throughout `[0,1]`.
The fixed-contour trace coefficients are the credited symbolic-v
identities. Keeping the far mean modulus loss `(9/2)v^3y^2s^4` and
subtracting exact energy gives (21). The entire calculation is reproduced
by the literal reciprocal/far-root/word-trace route in `verify.py`.
The compact-uniform little-oh, not an arbitrary uniform `O(s^6)`, is
what is asserted for varying angular profiles through collisions.

Apply (21) to the bounded coordinates in (20), with
`s=||phi-M1||`, `theta=(phi-M1)/s`, `y=M/s^2`, `r=tau/s^4`.
Since `e=v^4s^2+O_D(s^4)`, uniformly on each prescribed comparison class,
\[
{F-F(P)\over e^2}=K_1-K_a(\theta)
 +5v^3{M^2\over e^2}+2v^2{\sum\tau_j\over e^2}+o(1).   \tag{24}
\]

The sphere of balanced unit vectors is compact and K is continuous,
including all repeated eigenspaces. Hence its maximum exists and varies
continuously with a. Small fixed-energy root levels are nonempty by the
actual branch, closed and compact in a uniform neighborhood of `-1`,
away from all marked poles. The critical reciprocal matrix gives
continuous eigenvalue multisets and continuous modulus sums through
collisions. Thus a minimum is attained. Each minimum satisfies the
bootstrap with `D=0`, so (21) gives the uniform lower half of (8).
For its upper half choose any maximizing theta at each a and use the
actual circle family `z_j=-exp(i s theta_j)`. Its exact energy is
analytic in `s^2`, with derivative `v^4>=1/16` at zero. Compactness of
the radius/sphere domain gives one positive exact-energy inverse and
one uniform angular remainder. This supplies the upper half uniformly,
without requiring a continuous choice of maximizer. Theorem 4 follows.

## 4. Reestablishing one small coarse box above the local threshold

This analytic local lemma holds on **every** compact
`J0 subset(a_*,1]`, independently of whether P is global. Reestablish
the construction from8046 and its independent confirmation8102 on J0.
All domain restrictions in this section are the positive local coefficient
and nonzero separated/divided gaps; no assumption `a>=5/8` is used.

In (5) put `T=t sigma`. Exact energy divided by t^2 is analytic on a
signed small box, including t=0, with leading value
\[
v^4(56\sigma^2+\|h\|^2),\quad
\sigma_0(h)=\sqrt{1-\|h\|^2/56},\quad
\partial_\sigma(E/t^2)=112v^4\sigma_0>0.
\]
The positive energy IFT gives `sigma=sigma0+O(t^2)` uniformly on J0.
There is no cubic energy term: leading phases are centered, circle energy
is even in each phase, and radial energy starts at higher order.
The divided near matrix at h=0 has the simple angular eigenvalue6 and
six copies of -1. Its divided gaps and the far gap persist on one small
h box, uniformly on J0, so the single near root qn, far root qf and the
full six-group projector are analytic through t=0.

At the branch set `u=(a+exp(i(-t+m0)))^-1` and
`c=-i exp(i(-t+m0))u^2`. The credited scalar harmonic primitive has
\[
f(0)=|u|,\qquad
f'(w)={c(\bar u+\bar c w)\over
\sqrt{(u+cw)(\bar u+\bar c w)}}.
\]
The square root has positive constant `|u|`. For
`H(w)=|u+cw|-Re f(w)`, along the real axis `H=H_y=0`, and
`H_yy=|c|^2/|u+cx|>0`. Taylor's integral remainder gives
`H(w)=(Im w)^2 K(a,t,w)` with uniformly positive bounded K on a
common small disk. For the seven-near block N7 define
\[
\Phi=\operatorname{Re}\operatorname{tr}f((N_7-uI)/c)+|q_f|
                     +H((q_n-u)/c).                   \tag{25}
\]
Analytic functional calculus counts every algebraic multiplicity. It
gives `Phi<=F`, touching at P. The normalized near block has a Hermitian
first coefficient and a uniform `O(t^2)` remainder. A right-eigenvector
Rayleigh bound therefore gives `0<=F-Phi<=Ct^4` on the whole small
coarse box, also allowing signed radial variables for analysis.
Equation (21) and exact energy give `F-F(P)=O(t^4)` there. Thus the
analytic support difference is divisible on the **whole box**:
\[
\Phi-F(P_{a,e(a,t^2)})=t^4\mathscr R_4(a,t,h,y,r).       \tag{26}
\]
Boundedness of the quotient before removal and joint analyticity show
that all its sub-four t coefficients vanish; this is not interpolation
from individual profiles.

The credited physical constrained derivatives (7777/7819) give at
`t=h=y=r=0`
\[
\mathscr R_4=0,\quad (\mathscr R_4)_h=(\mathscr R_4)_y=0,
\quad(\mathscr R_4)_{hh}=2L(a)I,\quad
(\mathscr R_4)_{yy}=10v^3,\quad(\mathscr R_4)_{hy}=0,
\quad(\mathscr R_4)_{r_j}=2v^2.                         \tag{27}
\]
Value and first angular derivatives vanish at the origin for every
small t because the actual branch is stationary. The angular Hessian
of the support equals that of the true objective at the branch: on
angular motions the compressed first variation is real symmetric,
so the omitted scalar defects start at fourth angular order. This is
the collision-safe local audit's argument, not an assumption of smooth
individual roots. The other derivatives in (27) are their t=0 limits.

The numerator of L is positive above a_*. On `[0,1]` its derivative
has numerator `-4848a^2-3968a+10175>=1359>0`, so L is increasing.
Compactness and joint derivative continuity give one convex box with
positive angular Hessian on r=0 and positive radial gradients. For
`a0=min J0`, shrink it to retain half the limiting lower coefficients.
Integrating the Hessian on the zero-radial face and then the radial
gradients along r>=0 proves precisely (6), throughout this common box.
This proof has used only `J0 subset(a_*,1]`. Global entry is still to prove.

## 5. The sharp angular gap closes global entry above a_G

Reuse the credited invariants
\[
\Delta=43/56-X\ge0,\quad
\Gamma=\eta_{\rm sp}-(56X-13)/30\ge0,
\]
and graph8160's exact identity
\[
K_1-K_a=S(a)\Delta+C_d\Gamma,\quad
S(a)={d^3P_G(a)\over30720},\quad
P_G(a)=2768a^2+3080a-2875.                              \tag{28}
\]
For compact `J subset(a_G,1]`, `a0=min J`,
`S(a)>=S(a0)>0`; PG and d are increasing there. The earlier independent
angular audit gives `dist(theta,O_P)^2<=6Delta` for `Delta<=1/100`.
For all balanced unit theta the nearest singleton dot product is
`sqrt(8/7)max|theta_j|>=1/sqrt7`, so its distance squared is at most
`2-2/sqrt7<5/4`. Splitting at Delta=1/100 proves the sufficient global
bound
\[
K_1-K_a\ge {S(a_0)\over125}\operatorname{dist}(\theta,\mathcal O_P)^2.
                                                               \tag{29}
\]
Its small-gap form, with Delta, is what is needed for entry.

Under (4), the new bootstrap (20) supplies one bounded radial/mean box.
Thus the uniform remainder in (24) gives, with `omega_J(e)->0`,
\[
\Delta+M^2/e^2+\sum\tau_j/e^2
\le C_J(\epsilon_J+\omega_J(e)).                       \tag{30}
\]
Every displayed cost is nonnegative. Choose epsilon_J small, then e_J
small. Moment rounding puts theta close to the singleton orbit. Label
that singleton and conjugate if necessary so its centered phase is
positive. Decompose the lifted phases exactly as in (5). Since
`t^2` is comparable to e and `m0=O(t^3)`, (30) implies
\[
\|\eta/t\|+|(M-m_0)/t^2|
\le C_J\sqrt{\epsilon_J+\omega_J(e)}+O_J(t),\qquad
\sum\tau/t^4\le C_J(\epsilon_J+\omega_J(e)).             \tag{31}
\]
They enter strictly inside Section 4's fixed common box. The actual
positive amplitude is also the IFT solution: energy gives
`56(T/t)^2+||eta/t||^2=56+O(t^2)`, and the singleton choice gives
T>0, hence `T/t=sigma0+O(t^2)`. This establishes the required global
entry; local strictness alone was insufficient. Equation (6) proves
Theorem 2.

Every attained minimum is at most the branch value, so it enters this
box. Its physical excess is nonnegative by (6); equality forces zero
radial depths, zero mean deviation and zero split. Hence it is exactly
P or its conjugate. Equation (2) gives the common expansion. For every
fixed `a<=a_G`, the already proved actual competitor at8160 satisfies
\[
F(P)-F(Q)\ge(77/10000)\{(a_G-a)e^2+e^3\}>0
\]
at one common small threshold on `[0,a_G]`. This excludes P there and
completes Theorem 1, including the exact endpoint radius.

## 6. Extending the reviewed true fine law

Fix finite D. Reduce energy so `D e^3<=epsilon_J e^2`. Theorem 2 gives
`sum tau=O_J,D(t^6)`, `M-m0=O_J,D(t^3)`, `eta=O_J,D(t^2)`.
Use the bounded fine chart in Theorem 3. Rescaling (26) by
`h=t x`, `y_coarse=t y`, `r_coarse=t^2r`, stationarity for every t
and analytic Taylor integration give
\[
\Phi-F(P)=t^6\{Q_0+O_{J,D}(t)(\|x\|^2+y^2+R)\},
\quad Q_0=L(a)\|x\|^2+5v^3y^2+2v^2R,\quad R=\sum r_j.
                                                               \tag{32}
\]
The error is relative to the coordinate cost, including when it vanishes.

The direct upper-defect mechanism is credited to independent8102.
For clarity, all its divisions remain valid on the present compact J.
In the fixed balanced seven-root space, let `Q7=I7-11^T/7`,
`n=(7,-1,...,-1)`, `f=1`, with duals `n^T/56`, `f^T/8`. Literal
compression of N in the block decomposition `(A,B;D,C)` gives
`Bn=-Q7 u_B`, `Bf=9Q7 u_B`, `Dn=-u_B^T Q7/56`, `Df=u_B^T Q7/8`,
and the complementary collapsed block is
\[
C^{(0)}=\begin{pmatrix}(7u_A+u)/8&9(u_A-u)/8\\
7(u_A-u)/8&9(u_A+7u)/8\end{pmatrix}.
\]
Set `c0=-iv^2`, `m=y+||x||^2/112`.
The divided invariant graph has Jacobian diagonal `7c0,8v`, with
solution `kn=x^T/392`, `kf=-c0 x^T/(56v)`. The denominator56 retains
both far-row terms. On this fixed Euclidean space the normalized six
block is
\[
W_6=t^2Q7\operatorname{diag}(x)Q7
 +t^3\{mI-xx^T/392\}+t^4Z.                             \tag{33}
\]
Both displayed matrices are Hermitian. The divided angular and far
gaps are uniformly nonzero for `v in[1/2,1]`. Joint analyticity,
the exact real symmetric first angular derivatives at the branch,
and radial energy derivatives `E_tau=O(t^2)`, `E_T comparable to t`,
give, by Taylor integration on a bounded fine box,
\[
\|\operatorname{Im}_{\rm Herm}W_6\|
\le C_{J,D}\{t^4(\|x\|^2+y^2)+t^6R\}.                 \tag{34}
\]
In particular `T_r=O(t^7)`, the divided graph radial derivative is
`O(t^5)` and `(W6)_r=O(t^6)`; these keep the radial bound uniform.
The right-eigenvector Rayleigh identity and the scalar primitive now give
\[
0\le F-\Phi\le C_{J,D}\{t^8(\|x\|^2+y^2)^2+t^{12}R^2\}
\le C_{J,D}t^2\,t^6Q_0.                               \tag{35}
\]
Here `L` has a positive lower bound on J. No internal six-group gap or
diagonalizability is needed. Adding (32) and (35) proves (7).
The new checker verifies the complete linear compression on all eight
coordinate basis inputs and the leading graph cancellation; the
uniform Taylor/IFT implications remain the written reviewed method.

## 7. Moving-pair selection near the actual two-family boundary

For the sequence in Theorem 5, choose a fixed small compact neighborhood
`J0` of a_G contained in `(a_*,1]`. By (9), eventually
`F_min<=F(Q)<F(P)`. Each minimizer satisfies (20) with D=0 and (24),
uniformly on all `[0,1]`. Since `S(a_k)->0`, Delta is bounded,
and `C_d,5v^3,2v^2` have positive lower bounds, (24) and (28) give
\[
\Gamma\to0,\qquad M^2/e_k^2\to0,\qquad
\sum\tau_j/e_k^2\to0.                                 \tag{36}
\]
This uses no sign for S below a_G: its magnitude times bounded Delta
tends to zero. The exact complete Gamma=0 set at8160 is the union
of the singleton/seven and moving-pair unit orbits. Continuity and
compactness therefore put theta asymptotically in that union.

If a subsequence approached the singleton orbit, label its singleton
and conjugate. Equations (20) and (36) imply `h->0`, `y->0`, `r->0`
in the common coarse P chart, with its correct positive energy IFT
amplitude; `m0/t^2=O(t)->0`. Section 4 applies uniformly on J0 and
forces `F>=F(P)`, contradicting the strict upper competitor. Thus
no subsequence can approach the singleton orbit; every minimum
approaches the moving-pair orbit. Equations (36) also give the
two remaining little-oh statements in (10). At a=a_G the known
positive cubic comparison ensures `a_G<alpha(e)` for small positive e.
This proves Theorem 5 without a moving-pair locality or exact-global
classification assertion.

## 8. Evidence and remaining frontier

The standalone checker uses exact rational multivariate Gaussian jets,
literal word traces, far secular recursion, complete coefficient records,
rational coefficient-majorants and quadratic-field signs. Its fixture
comparison is mandatory and remains active under Python optimization.
Damage controls detect altered unbalanced and mean/inward coefficients,
the real-coordinate bound, angular gap and fine graph denominator.
Fixture controls also reject the wrong threshold radical branch.
Actual baseline replay is validation, not new research or independent review.

The uniform contour and weighted remainders, grouped collision argument,
energy inverses, harmonic support, analytic divisibility, local derivative
interpretation, compactness and global entry are ordinary written
mathematics outside a formal kernel. The new extension and graph8160
premise remain independently unreviewed. Older independent reviews
confirm only their expressly stated targets and domains.

The concrete next frontier is the moving-pair constrained stationary
chart with all six-block split and inward directions, and the cubic
two-chart comparison in the window `a-a_G=O(e)`. The present results
do not identify the full global transition curve, any exact minimum
on its lower side, an effective energy threshold, arbitrary-energy
minima, historical priority or the unrestricted first-power endpoint.
