# The true degree-nine excess and sharp uniform stability costs

Actual author **six-sendov-3**, role **researcher**, 2026-09-30.
Complete ordinary written author proof; independent review of this extension
is pending. Exact algebra validates universal matrix coefficients; uniform
analysis and cited global completeness remain outside a formal proof kernel.

The new result bounds the missing six-point harmonic support defect through
collisions, and consequently identifies the **true** objective excess with
uniform relative error, including at coordinates tending to zero. The
stationary branch, its local coefficients and the complete limiting harmonic
support are credited inputs, not new coefficient discoveries.

## 1. Definitions and results

Let `p=c(z-a) product_(j=1)^8(z-z_j)`, `c!=0`, have simple fixed marked
real root `a in[0,1]`, eight other closed-unit-disk roots with `z_j!=a`,
and every other original and critical algebraic multiplicity allowed and
counted. Define
\[
v=(1+a)^{-1},\quad E=\sum|(a-z_j)^{-1}-v|^2,\quad
F=\sum_{p'(\zeta)=0}|a-\zeta|^{-1},\quad G=F-16v.
\]
Scalars do not matter; rotation gives the version at a marked root of
modulus `a`. The credited actual stationary original-root branch is
\[
P_{a,e}=(z-a)(z+e^{i(7t+m_0)})(z+e^{i(-t+m_0)})^7,\quad E=e,
\]
\[
e=e(a,t^2)=56v^4t^2+O(t^4),\quad t>0,\quad
m_0=t^3 b(a,t^2),\quad b(a,0)=(392-1197v+945v^2)/20.
\]
Use the entire actual mean and exact energy inversion from
[the local theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_finite_energy_local_minimum/PROOF.md),
independently confirmed by
[the local audit](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_finite_energy_review3/PROOF.md).
Put
\[
L(a)={1616a^2+1800a-1675\over224(1+a)^5},\quad
a_*={10\sqrt{2198}-225\over404}<5/8.
\]

Fix any compact `J subset(a_*,1]` and finite `K>0`. In the exact energy
chart write
\[
z_A=-(1-\tau_A)e^{i(7T+M)},\quad
z_j=-(1-\tau_j)e^{i(-T+M+\eta_j)},\quad\sum_{j=1}^7\eta_j=0,
\]
\[
\eta=t^2x,\quad M=m_0+t^3y,\quad\tau=t^6r,\quad
\|x\|\le K,\quad |y|\le K,\quad\sum r_j\le K,\quad r_j\ge0.  \tag{1}
\]
The exact energy `E=e(a,t^2)` selects the positive amplitude `T` near `t`.
Let `Phi` be the credited touching harmonic support, defined in Section 2.

**Theorem 1 (uniform missing defect).** After choosing a `J,K`-dependent
positive threshold, throughout (1), including all six-group collisions,
\[
0\le F-\Phi\le C_{J,K}t^8.                                 \tag{2}
\]
More precisely, with `A=||x||^2+y^2`, `R=sum r_j`,
\[
0\le F-\Phi\le C_{J,K}\bigl(t^8 A^2+t^{12}R^2\bigr).        \tag{3}
\]
The stronger vanishing-coordinate estimate is needed for a relative,
rather than merely additive, normal form.

**Theorem 2 (sharp relative excess).** With possibly smaller threshold,
\[
\mathcal C=2v^2\sum\tau_j+5v^3(M-m_0)^2+L(a)t^2\|\eta\|^2,
\]
\[
\boxed{\bigl|F(p)-F(P_{a,e})-\mathcal C\bigr|
                       \le C_{J,K}t\mathcal C.}             \tag{4}
\]
In particular this is a two-sided positive cost estimate, valid uniformly
even when the scaled coordinates shrink with `t`. It establishes
\[
{F-F(P_{a,e})\over t^6}\longrightarrow
L(a)\|x\|^2+5v^3y^2+2v^2\sum r_j                            \tag{5}
\]
on every fixed bounded box, with the relative control in (4). Each of
the three leading coefficients is attained in a corresponding pure split,
mean or single-inward coordinate family. No higher coefficient is asserted.

**Theorem 3 (global sharp near-minimizers on the rectangle).** Take one
fixed `delta_0,e_0>0` and small positive quartic tolerance from
[the preceding fixed-rectangle theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_fixed_rectangle_minimizers/PROOF.md).
They can be decreased once so that the marked interval lies in `J`.
For every finite `D>=0` there exists `e_D>0` such that for every
\[
0\le a-5/8\le\delta_0,\qquad0<e<\min(e_0,e_D),              \tag{6}
\]
every full-disk polynomial with `E=e` and
\[
F(p)\le F(P_{a,e})+De^3                                    \tag{7}
\]
has (1) for a finite `K_D`, after root permutation and possibly conjugation,
and satisfies (4). The rectangle has **no** bound on `(a-5/8)^2/e`.
Here `F(P)` is the exact full-disk minimum by the cited rectangle theorem.
Equivalently, if
\[
\mathcal C_E=2v^2\sum\tau_j+5v^3(M-m_0)^2+
{1616a^2+1800a-1675\over12544(1+a)}e\|\eta\|^2,
\]
then throughout this entire near-minimizer class,
\[
\bigl|F-F_{\min}-\mathcal C_E\bigr|\le C_D\sqrt e\,\mathcal C_E. \tag{8}
\]
Constants remain existential. This does not extend (4) to arbitrary
coarse-box configurations or arbitrary quartic excess tolerances.

## 2. Credited analytic support and energy chart

The classical matrix
\[
N=\operatorname{diag}(u_j)(I+\mathbf1\mathbf1^T),\quad
u_j=(a-z_j)^{-1},
\]
has the eight critical reciprocals as eigenvalues; its characteristic
polynomial is `9R(q)-qR'(q)`, `R(q)=product(q-u_j)`.
At the actual branch put
\[
u_A=(a+e^{i(7t+m_0)})^{-1},\quad
u=(a+e^{i(-t+m_0)})^{-1},\quad c=-i e^{i(-t+m_0)}u^2,
\quad c_0=c(a,0)=-iv^2.
\]
The six-dimensional subspace
\[
W_B=\{(0,w_1,\ldots,w_7):\sum w_j=0\}
\]
is both a left and right scalar eigenspace of the branch matrix, with
eigenvalue `u`. Its real orthogonal projector `P_B` is fixed, independent
of `a,t`. The two complementary eigenvalues are a single near root
`q_n` and the far root `q_f`, with
\[
q_n-u=7c_0t+O(t^2),\qquad q_f-u=8v+O(t).                   \tag{9}
\]

The credited uniform scalar primitive satisfies
\[
f(0)=|u|,\qquad f'(w)=
{c(\bar u+\bar c w)\over\sqrt{(u+cw)(\bar u+\bar c w)}},
\]
\[
0\le H(w)=|u+cw|-\Re f(w)=(\Im w)^2K_0(a,t,w)
                                  \le C(\Im w)^2.           \tag{10}
\]
The branch choices and disk can be uniform on `J`. The touching support
is the exact moduli of the two simple roots plus the real holomorphic
trace on the other six. Equivalently it is the full seven-point near
trace plus the restored simple-near scalar defect, as in
[the global bridge](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_global_energy_minimizers/PROOF.md)
and its
[independent audit](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_global_energy_review4/PROOF.md).
It obeys `F>=Phi` and touches at the branch. For any matrix block
`uI+cW_6` selecting the six roots, trace invariance gives the exact identity
\[
F-\Phi=\sum_{\lambda\in\operatorname{spec}(W_6)}H(\lambda),  \tag{11}
\]
counting algebraic multiplicity. Neither simplicity nor diagonalizability
inside the six-group is required.

The exact fine energy chart and its joint analyticity on every prescribed
finite box are credited to
[the parabolic proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_parabolic_energy_classification/PROOF.md).
The needed amplitude bookkeeping is
\[
S=\|x\|^2,\qquad T=t-{S\over112}t^3+O(t^5).                \tag{12}
\]
All radial coordinates may temporarily be signed for analytic arguments.
The common phase changes from the repeated branch root by
\[
\phi_j-(-t+m_0)=t^2x_j+t^3m+O(t^5),\quad m=y+S/112,
\]
and the singleton phase changes by `t^3(y-S/16)+O(t^5)`.
Taylor expansion of the reciprocal, with derivative `c` at the repeated
root, therefore gives
\[
u_j-u=c(t)(t^2x_j+t^3m)+O_{J,K}(t^4).                      \tag{13}
\]
Radial perturbations enter these reciprocals at order six and energy
amplitude at order seven; they do not enter the displayed coefficients.

## 3. A fixed rational complementary basis and a divided Riccati IFT

Set `Q=I_7-11^T/7` on the seven repeated-root coordinates and use the
fixed complementary vectors
\[
n=(7,-1,\ldots,-1)^T,\quad f=\mathbf1_8,\quad
\|n\|^2=56,\quad\|f\|^2=8,\quad n^Tf=0.
\]
Their coordinate dual rows are `n^T/56` and `f^T/8`. The resulting
decomposition is `W_B plus span(n,f)`; it has no parameter-dependent
internal gauge. In this basis write
\[
N=\begin{pmatrix}A&B\\D&C\end{pmatrix},\quad
A=uI+\Delta A,\ B=\Delta B,\ D=\Delta D,\ C=C^{(0)}+\Delta C.
\]
Every `Delta` is jointly analytic and `O(t^2)` on the fixed scaled box.
The exact baseline complementary matrix is
\[
C^{(0)}=\begin{pmatrix}
(7u_A+u)/8&9(u_A-u)/8\\
7(u_A-u)/8&9(u_A+7u)/8
\end{pmatrix}.                                             \tag{14}
\]
Because `u_A=v+7c_0t+O(t^2)` and `u=v-c_0t+O(t^2)`,
\[
C^{(0)}-uI=\begin{pmatrix}
7c_0t+O(t^2)&9c_0t+O(t^2)\\
7c_0t+O(t^2)&8v+c_0t+O(t^2)
\end{pmatrix}.                                             \tag{15}
\]

Let `X=Q diag(x) Q` on the balanced subspace. Direct compression of
the complete original matrix, using `(I+11^T)w=w` for `w in W_B`, gives
\[
\Delta A=c(t)t^2X+c(t)t^3mI+O(t^4),                         \tag{16}
\]
\[
\Delta B_n=-c_0t^2x+O(t^3),\quad
\Delta B_f=9c_0t^2x+O(t^3),
\]
\[
\Delta D_n=-c_0t^2x^T/56+O(t^3),\quad
\Delta D_f=c_0t^2x^T/8+O(t^3).                              \tag{17}
\]
These are formulas for all balanced `x`. Singleton changes do not
affect them at this order because their phase change is `O(t^3)`.

Seek an invariant graph `w -> (w,Kw)`, with its two complementary rows
\[
K_n=t k_n,\qquad K_f=t^2 k_f.
\]
The graph equation is exactly
\[
D+CK-KA-KBK=0.                                             \tag{18}
\]
Divide **each row** by `t^2`. Every resulting expression is jointly
analytic through zero: (15)--(17), `Delta A=O(t^2)` and the powers in
`K` account for every term. At zero the equations are
\[
-c_0x^T/56+7c_0 k_n=0,
\qquad c_0x^T/8+7c_0 k_n+8v k_f=0.                         \tag{19}
\]
For every balanced coordinate, the unknown Jacobian is triangular
with diagonal `7c_0,8v`, nonzero uniformly on `J`. Thus the analytic
IFT, uniformly on every prescribed bounded box by compactness and
uniqueness, gives a graph with
\[
k_n(a,0,x,y,r)=x^T/392,\quad
k_f(a,0,x,y,r)=-c_0x^T/(56v).                              \tag{20}
\]
The far row includes the fixed-basis coupling `7c_0k_n` in (19).
Ignoring it would incorrectly replace `56v` by `64v`. This basis
dependence does not alter the third-order effective six-block, since
the far feedback first enters at degree four.

The restriction of `N` to the graph is exactly `A+BK`, represented
in the **fixed natural Euclidean space** `W_B`. Its eigenvalues have
algebraic multiplicity six. The remaining two eigenvalues are those
of `C-KB`; this follows by the graph shear block triangularization.
Since `C-KB=C^(0)+O(t^2)`, those simple roots remain separated from
the graph roots by (9) for small positive `t`. Consequently this is
precisely the six-group used by (11), not an arbitrary invariant subset.
No internal eigenvalue labels, shrinking-gap resolvent inverse or
normality of the perturbed matrix is assumed.

## 4. The complete normalized matrix through degree three

Define
\[
W_6={A+BK-uI\over c(t)}.
\]
Equations (16)--(20) yield the all-coordinate identity
\[
\boxed{W_6=t^2Q\operatorname{diag}(x)Q+
t^3\left[(y+S/112)I-{xx^T\over392}\right]+t^4Z(a,t,x,y,r),} \tag{21}
\]
on `W_B`, with `Z` jointly analytic on each prescribed finite box.
The only order-three feedback is
`(-c_0t^2x)(t x^T/392)`, divided by `c(t)`. The `c(t)` tangent
coefficient in `Delta A` cancels under normalization; the far feedback,
higher graph coefficients, quadratic original reciprocal terms and all
radials start at degree four or later. This accounts for all terms.

Both displayed coefficient matrices are real symmetric, hence Hermitian.
A merely real nonsymmetric coefficient would be insufficient for the
next bound. Here their symmetry is explicit and is checked symbolically
in all six independent balanced coordinates. There is no unidentified
parameter-dependent similarity correction, since (18) fixes the graph
coordinates in the original `W_B` space.

Write `Im_Herm W=(W-W*)/(2i)`. Equation (21) gives
`||Im_Herm W_6||<=C_{J,K}t^4`. For every eigenvalue and right eigenvector,
\[
\Im\lambda={w^*\operatorname{Im}_{\rm Herm}W_6w\over w^*w},
\]
so all six normalized critical eigenvalues have imaginary part `O(t^4)`.
This remains valid at defective points; every eigenvalue has a right
eigenvector, and repeated values are counted algebraically in (11).
The scalar bound (10) proves (2).

For an independent trace consistency check, the order-three cluster
coefficient in (21) has trace
\[
6y+5S/98.
\]
The previously exact simple-near shift is `y-5S/98`; the total is `7y`.
This is a consistency check, not the proof of matrix coverage or symmetry.

## 5. A defect bound that vanishes at the coordinates' origin

For fixed positive `t`, at `x=y=r=0`, the graph is `K=0`, `A=uI` and
`W_6=0`. Its first angular derivative is just `Delta A'/c`, because
`B=K=0` kills the first feedback derivative. On every pure angular
variation, `du_j=c dphi_j` for the repeated roots, with real `dphi_j`.
Thus this first derivative is exactly a real symmetric compression,
also after the real exact-energy elimination. Therefore the value and
all first `x,y` derivatives of `Im_Herm W_6` are zero at the origin.
Equation (21) and joint analyticity show that these same vanishings
hold for `Im_Herm Z` at `t=0` as well.

Radial derivatives have extra powers uniformly throughout a bounded
fine box. The exact reciprocal energy obeys
`E_tau_j=O(t^2)`, while `E_T` is comparable to `t`. Since `tau=t^6r`,
implicit differentiation gives `T_r_j=O(t^7)`. Consequently every
raw original-matrix derivative with respect to `r_j` is `O(t^6)`.
Differentiate the divided graph equations (18): their uniformly
invertible unknown Jacobian and the `t^2` division give
`(k_n)_r,(k_f)_r=O(t^4)`, hence `K_r=O(t^5)`. Differentiation of
`A+BK` then gives
\[
(W_6)_{r_j}=O(t^6),\qquad (\operatorname{Im}_{\rm Herm}Z)_{r_j}=O(t^2). \tag{22}
\]
All statements use analytic derivatives on the signed radial box;
uniformity is by compactness, not separate sample paths.

Taylor integration on the zero-radial angular face, followed by
integration on the radial segment, proves
\[
\|\operatorname{Im}_{\rm Herm}W_6\|
                    \le C_{J,K}\bigl(t^4(\|x\|^2+y^2)+t^6\sum|r_j|\bigr).
\]
Use the Rayleigh estimate and (10)--(11); the square of the last
bound is at most a constant times `t^8 A^2+t^12 R^2`. This proves (3).
On a fixed box it is in particular bounded by
\[
C_{J,K}t^8(\|x\|^2+y^2+R).                                 \tag{23}
\]

## 6. Relative true-excess form and optimal leading costs

The complete limiting support from
[the parabolic theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_parabolic_energy_classification/PROOF.md)
is a credited premise:
\[
\Phi-F(P_{a,e})=t^6\mathscr R(a,t,x,y,r),\quad
\mathscr R(a,0,x,y,r)=Q_0=L(a)\|x\|^2+5v^3y^2+2v^2R.       \tag{24}
\]
This full all-coordinate limit required the prior weighted-degree,
invariant-space and nonsingular exact certificate, not profile agreement
alone. It was separately reproduced here with the unchanged full fixture.

On each prescribed compact box, joint analyticity implies the difference
`R-Q_0` and its derivatives through order two are `O(t)`. At the
angular origin on `r=0`, value and first angular derivatives are exactly
zero for every `t`, by branch stationarity and support contact. Integrate
the angular Hessian difference along the zero-radial segment, then the
radial gradient difference along a nonnegative radial segment. This gives
\[
|\mathscr R-Q_0|\le C_{J,K}t(\|x\|^2+y^2+R).                \tag{25}
\]
Since `L>0` on `J`, `Q_0` is uniformly comparable to this last coordinate
cost. Add the missing defect bound (23) to (24)--(25) and multiply by
`t^6`. The true objective now obeys (4). The stronger defect estimate,
rather than an additive `O(t^8)` alone, makes this uniform when all
coordinates tend to zero. It also proves (5).

The leading coefficients cannot be increased in their respective pure
coordinate costs. Fix an `a in J`. Take any fixed nonzero balanced
`x` with `y=r=0`; then (5) gives `L(a)||x||^2`. Take `y!=0` with
`x=r=0`; the limit is `5v^3 y^2`. Finally take `r_j>0` for one
inward coordinate and all other coordinates zero; it is `2v^2r_j`.
The exact energy chart makes every family an actual admissible disk-root
polynomial for small `t`. This sharpness concerns the leading small-energy
costs, not effective finite-energy constants or new values of local Hessians.

## 7. Entire-rectangle global finite-tolerance refinement

The preceding fixed-rectangle theorem supplies exact full-disk minima,
one small quartic tolerance `epsilon_0 e^2`, global coarse entry and
positive uniform physical costs on (6). For fixed finite `D`, shrink
energy so `De^3<=epsilon_0e^2`. Every configuration in (7) is therefore
in that coarse chart and obeys its three-cost lower bound. Since its
excess is at most `De^3`,
\[
\sum\tau_j=O_D(e^3),\quad |M-m_0|=O_D(e^{3/2}),\quad
\|\eta\|=O_D(e).                                          \tag{26}
\]
Uniform comparison `t^2` with `e` converts (26) into (1) with a fixed
finite `K_D`. The exact energy chart is the same unique positive-amplitude
chart, so Theorem 2 applies after a `D`-dependent threshold decrease.
This proves Theorem 3 with no bounded `delta^2/e` hypothesis. It uses
the newer rectangle completeness, not the bounded sextic quotient
corollary outside its scope.

Finally `t^2=e/(56v^4)+O(e^2)` changes the split coefficient to that
in `C_E` with relative error `O(e)`, uniformly on the compact marked
interval. Since `t=O(sqrt e)`, (4) implies (8). The three coefficients
retain their earlier attribution. The new content is the uniform
two-sided true-objective law for the entire global near-minimizer class.

## 8. Validation and scope

The standalone standard-library exact checker openly adapts this author's
previous sparse rational polynomial kernel. It compresses the full eight
by eight original matrix in a fixed rational complementary basis, checks
the entire scalar eigenspace and two-dimensional baseline block, derives
both forward/backward leading couplings and the divided Riccati equations,
and checks the complete third-order normalized six-block coefficient in
all six independent balanced coordinates. The arbitrary tangent coefficient
`c_1` cancels symbolically. Symmetry is checked as a full matrix identity;
the normalized coefficients contain only real angular coordinates. It uses
neither critical-root samples nor floating eigenvectors.

Corruption controls distinguish the rank-one feedback, fixed complementary
coupling, exact energy elimination, tangent normalization and the failure
of real antisymmetry to be Hermitian. Missing/malformed/altered fixtures
must fail under optimization. The separately replayed previous 115-check
fixture is validation, not new research or independent review.

The written Riccati IFT, uniform remainders and radial derivatives,
scalar norm support, Rayleigh bounds, relative-error integration and
cited completeness remain ordinary mathematics. The new proof and the
parabolic/fixed-rectangle author extensions remain independently unreviewed;
reviews of their older premises do not supply a verdict on this extension.
No new basin coefficient, effective cutoff, arbitrary coarse-box sharp law,
arbitrary-energy/radius global result, all-degree theorem, historical
priority or unrestricted first-power endpoint is asserted.
