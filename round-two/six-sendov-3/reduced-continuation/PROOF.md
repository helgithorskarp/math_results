# Sparse continuation equations and the fifth degree-nine boundary coefficient

Actual author **six-sendov-3**, role **researcher**, 2026-10-01.
Complete ordinary author proof with finite exact identities. Independent
review of this extension is pending. The universal-minimum interpretation
uses the explicitly cited structural theorem8921, now independently
confirmed by review8955 within its inherited premises. No effective collar or continuation to an interior radius is proved.

## 1. The result and its dependency boundary

For a degree-nine complex polynomial with all original roots in the closed
unit disk and a marked root a, put F=sum_j |a-zeta_j|^(-1), with criticals
counted with multiplicity and zero denominators interpreted as infinity.
Normalize to a monic polynomial with a=1-eta>0. Let m(eta) be the infimum
over all such complex polynomials with this marked root. Define

\[
\begin{gathered}
c=\cos(\pi/9),\quad d=2c^2-1,\quad y=[3(1+c)]^{-1},\\
H_0=14y,\quad U_0=-8(2/3-y),\quad \rho=(c-5)/3,\\
u_z=(U_0+\rho H_0)/8,\quad u_p=u_z-\rho H_0/2,\\
C=8/3+y,\quad B_*=2311/108+(4934/27)c-(1976/9)c^2,\\
C_3=-60800959/17496-(307083769/17496)c+(10980067/486)c^2,\\
C_4=340367352475/839808+(808137564635/419904)c
                           -(1052841914857/419904)c^2.
\end{gathered}                                                        \tag{1}
\]

These constants, including the fourth coefficient and first critical jet
below, are prior results. The new coefficient is

\[
\boxed{C_5=-\frac{8304485822364161}{181398528}
          -\frac{6510273073800785}{30233088}c
          +\frac{2123849893841477}{7558272}c^2},\qquad
-3636.117842<C_5<-3636.117840.                                 \tag{2}
\]

**Theorem.** The six-real-critical/one-conjugate-pair disk-root family
selected near eta=0 has a unique local stationary minimizing branch,
whose value is

\[
8+C\eta+B_*\eta^2+C_3\eta^3+C_4\eta^4+C_5\eta^5+O(\eta^6).    \tag{3}
\]

This branch, its two unit-root constraints and its scalar stationary
equation have the explicit finite rational-polynomial representation in
Sections2-4. Using [the structural theorem8921](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/analytic-boundary/PROOF.md),
source ac6099018ea9e0e8e3092122db6ff24d549ebf32, artifact
bafkreig4fbumy4uayhto3w7hxj5mmppvn2kuddzmqlnol3leov7ffyq52m,
this branch is the unique minimum over **all complex competitors** in an
existential collar. Thus (3) is the Taylor expansion of m there. In
particular there are K,eta0>0 such that every disk-root polynomial obeys

\[
F\ge8+C\eta+B_*\eta^2+C_3\eta^3+C_4\eta^4+C_5\eta^5-K\eta^6
\quad(0<\eta<\eta_0),                                        \tag{4}
\]

and the exact minimizing family attains (3) at every such radius. Since
C5<0, the quartic truncation is not a universal lower bound in any
boundary collar. The directly constructed feasible tangent family
already supplies this counterexample without adopting the universal
minimum interpretation. This is an asymptotic statement; it does not resolve
the stronger first-power inequality at all interior radii.

The core new calculation depends on8921 for universal coverage and
analyticity of the complex minimum. Its independent confirming
[review8955](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/analytic-minimizer-audit/REVIEW.md),
source af8744b970f35769564fba7cb7c53377281661ca, artifact
bafkreicbjud6tbvj536oy4q7jrstcff4koxixzbdvpss6u7a2l2z7jfgmi, was
read in full from the committed graph and exact source before publication.
It confirms the ordinary analytic bridges within the named inherited
premises and sharpens exact stability; it proves no fifth coefficient. That parent's reviewed second-order
inputs8619/8684 and inherited7190 retain attribution. We give a direct
ordinary analytic construction of the symmetric branch here, so its
existence and its coefficient (2) do not require universal coverage.
The previously known coefficients C3 and C4 are reproduced as validation.
The fourth result8841, confirmed by8883, is **not needed to infer (2)**:
the first jet is rederived by scalar stationarity in Section5. Neither
this reproduction nor the known first jet is new mathematics.

The repeated-real-critical derivative template and root perturbation
method are credited to [Miller, math/0505424v3](https://arxiv.org/abs/math/0505424v3),
for a different nearest-critical objective. Chebyshev identities and the
analytic implicit function theorem are standard. The contribution here
is the explicit reduction for the first-power minimizer and its new
checked fifth coefficient. Historical priority is not asserted.

## 2. A sparse primitive and two exact unit-root constraints

Use three real variables v=(x,y1,T), with reference

\[
(x,y_1,T)=(u_z,u_p,H_0/2).
\]

The letter y1 is a variable; y in (1) is a fixed constant. Define

\[
r=\eta x,\quad s=\eta y_1,\quad \Delta=r-s,\quad
A=1-\eta-r,\quad D=1-\eta-s,\quad W^2=D^2+\eta T.             \tag{5}
\]

The positive choices A>0,T>0,W>0 hold in a fixed neighborhood for
sufficiently small positive eta. With X=z-r set

\[
Q(X)=X^9+\tfrac94\Delta X^8
                  +\tfrac97(\Delta^2+\eta T)X^7,\qquad
p(z)=Q(z-r)-Q(A).                                          \tag{6}
\]

Direct differentiation gives

\[
p'(z)=9(z-r)^6[(z-s)^2+\eta T],\quad p(1-\eta)=0,\quad
F=6/A+2/W.                                                 \tag{7}
\]

This normalization matters: both the9/4 and9/7 in (6) follow from
integrating the derivative factors, and the anchor is exactly1-eta.
The coefficients of p are polynomials over the rationals in eta,x,y1,T.
Write p(z)=sum_{j=0}^9 p_j z^j. Let T_j(t),U_j(t) denote the classical
Chebyshev polynomials of the first and second kinds and put

\[
I(t)=\sum_{j=1}^9p_jU_{j-1}(t),\qquad
R(t)=\sum_{j=0}^9p_jT_j(t).                                 \tag{8}
\]

For t in(-1,1), write z=t+i sqrt(1-t2). Then

\[
p(z)=R(t)+i\sqrt{1-t^2}\,I(t).                             \tag{9}
\]

Thus I(t)=R(t)=0 is **exactly** the assertion that p has the conjugate
unit-root pair with abscissa t. Near the reference family choose
t3 near-1/2 and t4 near-c. These intervals are disjoint.

At eta=0, p=z9-1, so I=U8, R=T9-1. At t_k^0=cos(2pi k/9), k3,4,

\[
I(t_k^0)=R(t_k^0)=0,\qquad
I_t(t_k^0)=-9/(1-(t_k^0)^2)\ne0,\qquad R_t(t_k^0)=0.        \tag{10}
\]

The phase equation I=0 therefore determines t_k(eta,x,y1,T) uniquely
and real analytically on a fixed neighborhood. At eta0 the phase is
t_k0 for every parameter. Hence R evaluated at that phase vanishes
at eta0, and

\[
E_k(\eta,x,y_1,T)=-R(t_k(\eta,x,y_1,T))/(9\eta)              \tag{11}
\]

extends analytically through zero. This is a quotient of the entire
analytic map, not an approximate equation for a moving root. E=0 is
equivalent to the exact unit-root constraint for every eta>0.

The coefficient of eta in p is

\[
p_1^{\rm jet}(z)=9-\tfrac98(6x+2y_1)(z^8-1)
                                +\tfrac97T(z^7-1).         \tag{12}
\]

Put (A3,B3)=(3/2,3/2) and (A4,B4)=(1+c,1-d). Since R_t=0
at (10), phase motion does not affect the first radial coefficient.
Therefore

\[
E_k(0,x,y_1,T)=-1-\tfrac18 A_k(6x+2y_1)+\tfrac17 B_kT.      \tag{13}
\]

The normal Jacobian on y1,T has determinant

\[
\det\begin{pmatrix}-A_3/4&B_3/7\\-A_4/4&B_4/7\end{pmatrix}
                    =3(c+d)/56>0.                         \tag{14}
\]

Consequently E3=E4=0 solves y1=Y(eta,x), T=V(eta,x) uniquely
and analytically. At eta0,

\[
Y(0,x)=(U_0-6x)/2,\qquad V(0,x)=H_0/2.                   \tag{15}
\]

At every sufficiently small positive eta and every x in a fixed
neighborhood of u_z, this construction gives a legal disk-root
polynomial with exactly the four active roots on the unit circle.
Indeed its four unit roots are given by (9). The other root maps at
the simple ninth roots are analytic. Their first half squared-modulus
radials at omega1,omega2 are strictly negative, independent of x by
(12),(15), as the exact independent root audit checks. Their conjugates
have the same slopes. The marked root is exactly1-eta. All nine roots
remain distinct by the simple-root theorem. Uniformity follows by
shrinking a fixed parameter neighborhood; none of the other roots
can leave the disk there. Thus this is an actual implicit family, not
only a truncated polynomial satisfying constraints to fifth order.

## 3. The one-dimensional stationary equation

Let Phi(eta,x) be (7) after inserting (15)'s analytic normal solution.
It is analytic in eta,x near(0,u_z), since A,W are positive at zero.
Direct expansion gives

\[
\Phi(0,x)=8,\qquad \Phi_{[1]}(x)=C,\qquad
\Phi_{[2]}(x)=B_*+12(x-u_z)^2.                             \tag{16}
\]

Here [j] means the coefficient of eta^j, without a factorial.
Define the analytic scaled objective

\[
G(\eta,x)=[\Phi(\eta,x)-8-C\eta]/\eta^2.                  \tag{17}
\]

At eta0, G_x=24(x-u_z) and G_xx=24. The equation G_x=0
has a unique analytic solution x=x_min(eta) near u_z, and G_xx
stays positive on a fixed neighborhood for sufficiently small eta.
Thus this is the unique local symmetric minimum. If8921 is adopted,
its universal minimizing polynomial has this symmetry, saturates the
same four roots, lies in this neighborhood and is stationary there.
It therefore coincides with this unique branch. No conclusion about
universal competitors beyond the parent's collar follows from (17).

For completeness, (16)'s finite identity has a simple degree bound.
The leading normals in (15) are affine/constant in x, and p_[1]
is independent of x. The first phase corrections are therefore
independent of x. The uncorrected p_[2] is of degree at most two
in x. The linear normal solve (14) preserves this degree, and
R_t=0 prevents a second phase correction from entering the radial
equations at that order. Expanding (7) then gives a polynomial of
degree at most two for Phi_[2]. The checker's exact second-order
dual variable about u_z checks its complete constant, linear and
quadratic coefficients (Bstar,0,12). This proves the whole identity,
not only a numerical Hessian at one point. It also agrees with the
credited symmetric restriction of the second-order cost8619/8684.

## 4. A finite rational-polynomial stationary system

There is no need to carry analytic root maps as black boxes in a
continuation calculation. Treat t3,t4 and W as additional variables.
For each k3,4 and each v_j in(x,y1,T), define the polynomial

\[
N_{k,j}=\frac{R_{v_j}(t_k)I_t(t_k)-R_t(t_k)I_{v_j}(t_k)}{\eta}.
                                                                  \tag{18}
\]

The numerator is **literally divisible by eta**: p at eta0 is z9-1
independently of the three parameters, so both parameter derivatives
have an eta factor. Equation(18) is polynomial division by a known
factor; it introduces no equation singularity for eta>0.

Where I_t is nonzero, differentiating the phase equation gives
dt_k/dv_j=-I_vj/I_t, and differentiating (11) gives

\[
\partial E_k/\partial v_j=-N_{k,j}/(9I_t(t_k)).             \tag{19}
\]

The objective derivatives from (7), in this three-variable space, are

\[
\nabla F=\eta(6/A^2,\ 2D/W^3,\ -1/W^3).
\]

Multiplying this row by the nonzero W3*A2/eta gives the polynomial row
P=(6W3,2DA2,-A2). At every point where I_t(t3),I_t(t4) and the
normal minor of N are nonzero, the exact constrained stationary
condition is

\[
S:=\det\begin{pmatrix}
6W^3&2DA^2&-A^2\\
N_{3,x}&N_{3,y_1}&N_{3,T}\\
N_{4,x}&N_{4,y_1}&N_{4,T}
\end{pmatrix}=0.                                           \tag{20}
\]

Indeed the tangent space to the two constraints is one-dimensional,
and stationarity means that the objective gradient is in their row
span. Equation(19) and the nonzero rescaling prove both directions.
It follows that the exact stationary system consists of **six
rational-polynomial equations in six real unknowns** x,y1,T,t3,t4,W:

\[
I(t_3)=R(t_3)=I(t_4)=R(t_4)=0,\qquad
W^2-D^2-\eta T=0,\qquad S=0.                              \tag{21}
\]

Here eta is a parameter. All coefficients are rational, with no
cosine constant in the equations themselves; c selects the initial
branch only. The coefficient construction (6),(8),(18),(20) is a
finite explicit description and does not require expanding a large
determinant. The conditions A,T,W>0, t3,t4 in the specified disjoint
intervals, I_t nonzero and the normal rank condition must be retained.
The system also has other algebraic solutions; we assert no global
classification of them and no completeness for arbitrary complex
polynomials from this system alone. At eta0 it is degenerate; the
desingularized analytic equation (17), with Hessian24, selects the
unique branch.

## 5. The first minimizing jet and why it suffices for C5

An exact dual-number differentiation of the eta3 coefficient in
Phi gives

\[
\Phi_{[3]}'(u_z)=\ell_1
 =79312/81+(902885/162)c-(187712/27)c^2.                     \tag{22}
\]

Differentiating G_x(eta,x_min(eta))=0 at zero yields

\[
x_{\min}'(0)=-\ell_1/24=\alpha
 =-9914/243-(902885/3888)c+(23464/81)c^2.                    \tag{23}
\]

This is the previously known first real-critical jet, now recovered
from the reduced scalar equation. It is used without assuming the
fourth theorem's proof. The independent old fourth coefficient is
subsequently reproduced, which is validation rather than novelty.

Consider the exact feasible normal solution from Section2 with

\[
x_{\tan}(\eta)=u_z+\alpha\eta.                             \tag{24}
\]

By analyticity, x_tan-x_min=O(eta2). Taylor's formula in x, using
G_x(eta,x_min)=0 and a bounded G_xx on a fixed neighborhood, gives

\[
\Phi(\eta,x_{\tan})-\Phi(\eta,x_{\min})
=\eta^2O((x_{\tan}-x_{\min})^2)=O(\eta^6).                \tag{25}
\]

Thus the exact unit-root normal solution along the **first** tangent
already determines every objective coefficient through eta5. There
is no need to guess or optimize a second critical jet, or to discard
an untracked normal correction. The checker additionally inserts a
unit eta2 term into x_tan and reconstructs all normals anew: its
complete objective series through eta5 is unchanged. This finite
cancellation validates (25) but does not substitute for its ordinary
analytic proof. Changing alpha by1 instead increases the fourth
coefficient by exactly12, a control on the stationary correction.

## 6. Exact recursive calculation and independent root audit

Write y1=sum y_j eta^j, T=sum T_j eta^j and
t_k=t_k0+sum_{j>=1} tau_kj eta^j along (24). At step j, all
earlier coefficients are fixed. The coefficient of eta^j in R(t_k)
depends linearly on the two unknown normal coefficients y_(j-1),
T_(j-1), with the fixed matrix

\[
M=\begin{pmatrix}9A_3/4&-9B_3/7\\9A_4/4&-9B_4/7\end{pmatrix}.
                                                                  \tag{26}
\]

The coefficient tau_kj does not enter, because R_t at eta0 is zero.
After solving the two real equations, the eta^j phase residual is
removed by tau_kj, with coefficient -9/(1-(t_k0)^2) from (10).
At j1 the leading normals are already (15); only the phase is
adjusted. Both matrices are invertible by (10),(14). Induction proves
that this exact recursion yields the Taylor coefficients of the
unique analytic normal solution. At every step the checker verifies
**all** phase and real residual coefficients up to that step, not
only the newly solved one.

Five steps determine y1,T through eta4 and the phases through eta5.
Insert these into (7). The resulting objective coefficients are
exactly 8,C,Bstar,C3,C4 and (2). Arithmetic is in
Q[c]/(8c3-6c-1), and the intended real embedding is isolated by
exact rational bisection on(3/4,1). This yields the enclosure in(2).

The independent route in root_audit.py multiplies the six linear
derivative factors and the quadratic factor, integrates all z
coefficients and anchors at1-eta. It uses neither (6) nor Chebyshev
evaluation to form this polynomial. Every polynomial coefficient
matches the sparse calculation. It then solves the original simple
complex roots recursively: if a provisional root series near omega
has eta^j residual b_j, set its new coefficient to -omega*b_j/9,
because the limiting derivative is9*omega8 and omega9=1.
Conjugate multiplication checks every coefficient of
(|root|2-1)/2 through eta5 is zero for both active pairs. The real
parts of these actual roots agree with the independently generated
Chebyshev abscissas coefficient by coefficient. The roots at omega1,
omega2 separately have strictly negative first radial coefficients.
All these calculations are exact in cubic/quadratic-Gaussian fields.
No floating-point root or solver result is proof input.

Combining this finite identity with (25) proves (3). The branch is
analytic, so its Taylor error is O(eta6) in a fixed collar. Adopting
8921 identifies this branch with m, which proves the uniform
competitor lower bound (4). Independently, C5<0 and the exact feasible
tangent family disprove a quartic-truncation lower bound in every collar.

## 7. What a continuation obstruction would mean

The equations now supply exact quantities to monitor. Along a
positive-eta local branch one needs positive A,T,W, distinct simple
original roots, t3,t4 strictly between-1 and1 and distinct, nonzero
phase derivatives, an invertible two-normal Jacobian, positive reduced
objective curvature, and all other original roots strictly inside.

More precisely, suppose this branch is defined on [eta1,eta*) with
0<eta1<eta*<1. If its parameters remain bounded and the quantities
just listed stay uniformly away from their failure boundaries,
including a positive lower bound for the original-root derivatives,
then it extends analytically through eta*. The phase and normal
implicit solves, followed by the scalar stationary solve, have
uniformly bounded inverse derivatives on the compact closure.
Differentiating these equations bounds parameter derivatives; the
branch has a limit at eta*. The ordinary implicit function theorem
at that limit extends it. Root simplicity and the strict disk
inequalities preserve the same root regime. This is a standard
compact continuation criterion applied to the explicit equations.

Thus a finite obstruction to **this local representation** can be
parameter escape, loss of a positive distance/opening, root collision
or phase merger, vanishing phase/normal Jacobian, loss of local
curvature, or another original root reaching the circle. A vanishing
Jacobian can be a coordinate failure rather than nonexistence.
No first actual obstruction or positive interior endpoint is located
here. A different complex family could acquire a smaller value
without any degeneration of this symmetric branch. Consequently
continuation of (21) alone does not extend8921's universal collar.

## 8. Evidence and remaining obligations

The source regenerates the compact fixture from definitions and compares
it in full, including JSON types, in normal and optimized Python.
Mathematical mutations of the coefficient, anchor, primitive, normal
determinant, minimizing jet, unit-root branch and fifth normal correction
are rejected. Missing, malformed and mathematically altered fixtures
also fail. Commands, counts and hashes are in README.md.

Analytic root maps, division of analytic functions by known vanishing
orders, both implicit function arguments, uniform feasibility, the
Taylor value estimate (25), and the compact continuation criterion
are ordinary written mathematics. The checker verifies finite algebra;
it is not a proof-assistant kernel and does not prove universal
competitor coverage. The latter is the openly stated8921 dependency.
Independent review of this extension remains pending; parent8921 is
independently confirmed by8955 within its inherited premises.
The full first-power endpoint, an effective boundary collar and a
verified continuation interval remain open.
