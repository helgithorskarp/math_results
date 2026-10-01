# The unique analytic degree-nine first-power boundary minimizer

Actual author **six-sendov-3**, role **researcher**, 2026-10-01.
Complete ordinary author proof, with a separate exact finite checker.
Independent review of this extension is pending. Every boundary collar in
this proof is existential. The full first-power conjecture remains open.

## 1. The statement and its credited inputs

For a degree-nine polynomial whose original roots lie in the closed unit
disk, a marked root a, and its eight critical points counted with algebraic
multiplicity, put

\[
 F_p(a)=\sum_{j=1}^8|a-\zeta_j|^{-1}.
\]

A zero denominator means infinity. Normalize p to be monic and rotate the
marked root to a=1-eta>0. Define the credited constants

\[
\begin{gathered}
 c=\cos(\pi/9),\quad d=2c^2-1,\quad v=2d^2-1,\quad
 y=\frac1{3(1+c)},\quad x=\frac23-y,\quad H_0=14y,\quad U_0=-8x,\\
 C=\frac83+y,\quad \rho=(c-5)/3,\quad L=-7(2c+1)/18,\\
 u_z=(U_0+\rho H_0)/8,\quad u_p=u_z-\rho H_0/2,
 \quad b=\sqrt{H_0/2},\\
 B_* =\frac{2311}{108}+\frac{4934}{27}c-\frac{1976}{9}c^2.
\end{gathered}                                                    \tag{1}
\]

**Theorem.** There is eta0>0 such that, for each 0<eta<eta0, there is
exactly one monic degree-nine disk-root polynomial p_eta with marked root
1-eta minimizing F over *all complex* such polynomials. There are real
analytic functions u0(eta), u1(eta), Y(eta), defined on a neighborhood of
zero, with u0(0)=u_z, u1(0)=u_p, Y(0)=b, such that

\[
 p_\eta'(z)=9(z-\eta u_0(\eta))^6
       [(z-\eta u_1(\eta))^2+\eta Y(\eta)^2],\qquad
 p_\eta(z)=\int_{1-\eta}^z p_\eta'(w)\,dw.                    \tag{2}
\]

Thus p_eta has real coefficients analytic in eta, and its critical
multiset consists exactly of six coincident real points and one nonreal
conjugate pair. Its original roots near exp(plus/minus2pi i/3) and
exp(plus/minus8pi i/9) are on the unit circle. The other four unmarked
original roots and the marked root are strictly inside. All nine original
roots are simple. The minimum m(eta) is real analytic at zero and

\[
 m(\eta)=8+C\eta+B_*\eta^2+C_3\eta^3+O(\eta^4),\qquad
 C_3=-\frac{60800959}{17496}-\frac{307083769}{17496}c
                       +\frac{10980067}{486}c^2.              \tag{3}
\]

The coefficients in (3) are prior results, not new coefficients here.
Analyticity, exact uniqueness at each radius, saturation of four original
roots, and the exact6+2 critical structure are the new conclusions.

There is also a stability bound with no truncated-series error. Put
w4=1/(c+d), w3=(2/3)[7-(1-d)w4], and delta=min(w3,w4)/4>0.
For every fixed finite real T there is eta_T>0 such that every competitor
with

\[
 F_p(1-\eta)\le8+C\eta+B_*\eta^2+T\eta^3,
 \qquad 0<\eta<\eta_T                                      \tag{4}
\]

can be labeled as in Section2 and satisfies

\[
 F_p(1-\eta)-m(\eta)
 \ge \delta\sum_{k=3,4}\sum_{s=\pm}(-a_k^s)
       +\frac{\eta^2}{256}\|z-z_\eta\|^2.                    \tag{5}
\]

Here a_k^s=(|r_k^s|^2-1)/2 are the four actual active original-root
radials, z is the twelve-vector of the six small criticals' normalized
imaginary and real coordinates, and z_eta is that vector for (2).
Their labeling and the norm are specified below. Neither numerical
constant is asserted sharp; the collars are not effective.

The direct mathematical premises are:

* [The second-order theorem8619](https://github.com/helgithorskarp/math_results/blob/f8df996dba7bfec1d05eb6731b3b8e667ca8f860/round-two/six-sendov-3/quartic-boundary/PROOF.md),
  independently confirmed by [review8684](https://github.com/helgithorskarp/math_results/blob/691ea3f4eaa4b06b46ab0aded63903d81d95c668/round-two/six-reviewer-1/quartic-boundary-audit/REVIEW.md): the sharp second infimum limit, sequential profile selection, bounded-budget moment bootstrap, all-disk upper family, finite cost and its global joint gap1/128. These suffice for the structural theorem and (5).
* [The cubic theorem8751](https://github.com/helgithorskarp/math_results/blob/52a408f210846d246b5c8dfd890cc142d480d2c4/round-two/six-sendov-3/cubic-boundary/PROOF.md),
  independently confirmed by [review8781](https://github.com/helgithorskarp/math_results/blob/94cbfb364599e5cfa0cf866723c5f9717f38bc39/round-two/six-reviewer-1/cubic-boundary-audit/REVIEW.md): the already known third Taylor coefficient in (3). Its stronger cubic-bootstrap rates are useful context but unnecessary for this structural proof.

The concentration/bootstrap in [review7190](https://github.com/helgithorskarp/math_results/blob/d16c8df095d88b344063fd9c87f39be57e408cd7/sendov_degree9_first_power_boundary_review2/REFINEMENT.md)
and the first-order slope8530, reviewed8608, remain attributed inherited
inputs of8619/8684. Profile theorem8668, reviewed8718, is an inherited input
of the separately cited third-coefficient result. The author's fourth-coefficient claim8841 is useful
context, independently unreviewed at the pass-start refresh, and is not
a premise of this structural proof. Ordinary analytic implicit function
theorems and compactness are used outside the exact checker.

The major-claim refresh subsequently found independent review8883,
artifact bafkreiez7pp3s3zoxyr66r5pkbitn3sytvxxrsj373rjrxhsjwe4t5cirq,
[source7bf51b77755026292db72084d8338698e2f43925](https://github.com/helgithorskarp/math_results/blob/7bf51b77755026292db72084d8338698e2f43925/round-two/six-reviewer-1/fourth-boundary-audit/REVIEW.md).
It confirms8841 and proves an optimal one-half fourth-profile penalty
with a fifth-order remainder. It explicitly leaves exact minimizer
uniqueness and analyticity unproved. These are complementary prior
results; neither the fourth coefficient nor its new reviewed penalty
is needed for the structural proof here.

## 2. A chart covering arbitrary near-optimal critical configurations

Set eta=epsilon^2 and write zeta_j=eta*u_j+i*epsilon*h_j with real h,u.
The reference point is

\[
 h^*=(b,-b,0^6),\qquad u^*=(u_p,u_p,u_z^6).
\]

Let z=(h3,...,h8,u3,...,u8), with reference zstar=(0^6,u_z^6).
Take four normal variables U,H,V,M, with reference (U0,H0,0,0), and set

\[
\begin{aligned}
 m_h&=(\eta V-\sum_{j=3}^8h_j)/2,&
 s_h&=\sqrt{(H-\sum_{j=3}^8h_j^2)/2-m_h^2},\\
 h_1&=m_h+s_h,&h_2&=m_h-s_h,\\
 m_u&=(U-\sum_{j=3}^8u_j)/2,&
 d_u&=(M-2m_hm_u-\sum_{j=3}^8h_ju_j)/(2s_h),\\
 u_1&=m_u+d_u,&u_2&=m_u-d_u.
\end{aligned}                                                  \tag{6}
\]

Use the positive square root. These formulas are analytic on a fixed
neighborhood, since s_h=b>0 at the reference point. They give exactly

\[
 \sum u=U,\quad\sum h^2=H,\quad\sum h=\eta V,\quad h\cdot u=M. \tag{7}
\]

Conversely every nearby pair h,u with h1>h2 is represented by (6), using
the moments (7). For eta>0 this is a nonsingular coordinate chart on the
sixteen labeled real critical coordinates. The labeling selects the
large positive and negative imaginary criticals as1,2. The remaining six
can be permuted freely, including collisions. No analytic critical
labeling for a competitor is assumed.

The monic polynomial associated with (6) is defined by multiplying its
eight derivative factors and integrating from1-eta. This covers every
monic competitor in the chart. Its coefficients are analytic in epsilon
and the parameters; replacing epsilon by -epsilon conjugates them.
Since sum(h)=eta V, its perturbation from z^9-1 has no epsilon term.
The coefficientwise leading expansion is

\[
 p=z^9-1+\epsilon^2 g_2+i\epsilon^3 I_3+O(\epsilon^4),
\]
\[
\begin{aligned}
 g_2(z)&=9-\frac{9U}{8}(z^8-1)+\frac{9H}{14}(z^7-1),\\
 I_3(z)&=-\frac{9V}{8}(z^8-1)-\frac{9M}{7}(z^7-1)
                          +\frac{J_3}{2}(z^6-1),\quad J_3=\sum h^3.
\end{aligned}                                                  \tag{8}
\]

In these leading coefficients the parameters and h are evaluated at
eta=0. The exact Newton/integration check separately verifies (8).

All nine limiting original roots omega_k=exp(2pi i k/9) are simple.
The analytic root theorem gives nine disjoint, uniform root maps in
epsilon and the real chart parameters. Let r_k^+,r_k^- be the maps near
omega_k,bar(omega_k), for k=3,4, and define

\[
 E_k=\frac{a_k^++a_k^-}{2\eta},\qquad
 O_k=\frac{a_k^+-a_k^-}{2\epsilon^3\sin\theta_k},
 \qquad\theta_k=2\pi k/9.                                    \tag{9}
\]

The numerators are respectively even and odd in epsilon. The even one
vanishes to order2. The odd one vanishes to order3 by (8), so both
quotients extend *real analytically in eta* through zero. This divisibility
uses the whole coefficient/root map, not termwise guesses for individual
critical branches. Also sin(theta_k)>0 and

\[
 a_k^\pm=\eta E_k\pm\eta^{3/2}\sin\theta_k O_k.                \tag{10}
\]

## 3. Inverting the four actual root constraints

Linearizing a simple root at z^9-1 gives radial change -Re(g(omega))/9.
Consequently the extended maps (9) at eta=0 are

\[
\begin{aligned}
 E_k&=-1-A_kU/8+B_kH/14,\\
 O_3&=V/8-M/7,\\
 O_4&=V/8-2cM/7+(1-4c^2)J_3/18,
\end{aligned}                                                  \tag{11}
\]

where (A3,B3)=(3/2,3/2), (A4,B4)=(1+c,1-d).
At the reference point these four values are zero. The even normal
Jacobian on U,H has determinant3(c+d)/224>0. The odd normal Jacobian
on V,M has determinant(1-2c)/56<0. At the reference point J3=0 and
its derivatives in U,H,V,M are zero: h1=-h2 and all small h vanish.
Thus the full four-normal Jacobian is invertible.

The analytic implicit function theorem now solves U,H,V,M uniquely as
analytic functions of (eta,z,E3,E4,O3,O4), on one fixed product
neighborhood of (0,zstar,0). Shrink that neighborhood as needed below.
At eta=0, E=O=0 imposes exactly

\[
 \sum h=0,\quad\|h\|^2=H_0,\quad\sum u=U_0,\quad h\cdot u=LJ_3,
 \qquad V=8M/7.                                               \tag{12}
\]

The other original-root branches stay inside for small positive eta
uniformly on this neighborhood whenever the four active radials are
nonpositive. Indeed the first radial slopes at omega1,omega2 and their
conjugates are strictly negative at the reference point; continuity of
(8) preserves this strictness in a sufficiently small neighborhood.
The branch at1 is exactly1-eta by the anchor. Nine disjoint simple root
maps exhaust the roots. Thus E=O=0 is a legal disk-root polynomial for
every z in the fixed neighborhood and every sufficiently small eta>0.

## 4. Strict removal of all four original-root slacks

The exact reciprocal objective is analytic in eta and h,u near the
reference point, since each distance squared is

\[
 (1-\eta(1+u_j))^2+\eta h_j^2
\]

and is near1. Uniform expansion gives

\[
 F=8+\eta(8+U-H/2)+O(\eta^2).                                \tag{13}
\]

At eta=0, the even equations (11) solve U,H independently of z and O.
The positive dual weights satisfy

\[
 \sum w_kA_k/8=1,\quad\sum w_kB_k/14=1/2,\quad8-\sum w_k=C.
\]

Hence, after the normal inversion,

\[
 \mathcal F(\eta,E,O,z)
   =8+\eta(C-w_3E_3-w_4E_4)+\eta^2\widetilde G(\eta,E,O,z),   \tag{14}
\]

with an analytic Gtilde having uniformly bounded first derivatives on a
smaller fixed product neighborhood. In particular F_O=O(eta^2), not
merely O(eta). Using the invertible relation (10) at fixed eta>0,

\[
 \frac{\partial\mathcal F}{\partial a_k^\pm}
 =\frac{\mathcal F_{E_k}}{2\eta}
       \pm\frac{\mathcal F_{O_k}}{2\eta^{3/2}\sin\theta_k}
 =-w_k/2+O(\sqrt\eta)\le-w_k/4.                              \tag{15}
\]

Uniformity follows from the fixed analytic neighborhood; the sine
denominators are fixed positive constants. For feasible a_k^pm<=0,
replace every a_k^pm by (1-t)a_k^pm,0<=t<=1, keeping z fixed. This
scales E and O by1-t, so remains within the chosen normal neighborhood.
The active roots remain in the disk, as do all other roots by Section3.
Integrating (15) yields the exact comparison

\[
 \mathcal F(\eta,E,O,z)-\mathcal F(\eta,0,0,z)
 \ge\delta\sum_{k,s}(-a_k^s).                                \tag{16}
\]

Thus a minimizer in the chart saturates all four actual original-root
constraints. This step treats independent conjugate-root radials for
complex competitors; it does not assume a real polynomial.

## 5. A positive twelve-dimensional Hessian on the boundary stratum

Write F(eta,0,0,z)=8+C eta+eta^2 G(eta,z). The analytic function at zero
is *exactly* the reviewed finite cost evaluated at the eta=0 chart:

\[
 G(0,z)=\mathcal B(h,u)
       =K_0+\frac12\|u\|^2+\rho\sum h^2u+\sigma\sum h^4,      \tag{17}
\]

\[
 K_0=-2609/405-(2000/81)c+(12964/405)c^2,
 \quad\sigma=3/8-[(3/2)w_3+(1-v)w_4]/20.
\]

For completeness, this equality follows from the attributed generic
fourth-order Newton jet of8619/8684. Along the boundary-stratum chart let
U=U0+eta W+O(eta^2), H=H0+eta H1+O(eta^2), and D=||u||^2-H1.
The two zero averaged second radials give
A_k W/8+B_k D/14=T_k(h,u), where

\[
\begin{aligned}
 T_k={}&4+U_0-H_0/2+B_kU_0^2/14+\mathcal K_k\\
 &+(1-\cos6\theta_k)(-U_0H_0/12+J_{21}/6)\\
 &+(1-\cos5\theta_k)(H_0^2/40-J_4/20),\\
 \mathcal K_k&=-[(7/2)x^2+6xyq_k+(5/2)y^2q_k^2]s_k,\\
 (q_3,s_3)&=(-1,3/4),\qquad(q_4,s_4)=(-2c,1-c^2).
\end{aligned}
\]

The scalar second coefficient is
W+D/2+||u||^2/2+8+2U0-3H0/2-3J21/2+3J4/8.
Taking the weighted equality gives (17). The possibly nonzero imaginary
epsilon^3 jet does not enter this averaged epsilon^4 radial coefficient:
its first-order contribution is odd between the conjugate branches, and
its quadratic contribution starts at epsilon^6. The checker verifies the
generic anchored jet, the root curvature and every dual coefficient.

Review8684 proves on the whole exact manifold (12) that

\[
 \mathcal B(h,u)-B_*\ge\operatorname{dist}((h,u),\mathcal O)^2/128,
\]

where O is the finite simultaneous permutation orbit of(hstar,ustar).
Choose the chart neighborhood small enough that its nearest orbit point
is(hstar,ustar). The twelve free coordinates are retained exactly in(6),
so that distance is at least||z-zstar||. Thus G(0,z)>=Bstar+
||z-zstar||^2/128. Differentiability gives grad G(0,zstar)=0 and

\[
 D_z^2G(0,zstar)\succeq I/64.                                \tag{18}
\]

The analytic implicit function theorem applied to grad_z G=0 gives a
unique analytic stationary branch z_eta with z_0=zstar. Shrink a fixed
convex z-ball and the eta interval so that its Hessian satisfies
D_z^2G(eta,z)>=I/128 throughout the ball and z_eta stays in its interior.
Integration along the segment from z_eta to z gives

\[
 G(\eta,z)-G(\eta,z_\eta)\ge\|z-z_\eta\|^2/256.              \tag{19}
\]

This proves uniqueness and (5) throughout the chart by (16).
The full twelve-variable finite tangent Hessian is also separately
expanded by the author checker. Its positive quadratic form agrees with (18),
and that calculation is a finite check rather than a replacement for
the inherited global gap or the analytic argument.

## 6. Why all globally competitive complex polynomials are covered

The independently reviewed second-order theorem supplies an all-disk
family p_upper(eta) at every sufficiently small positive eta, with
F_upper=8+C eta+Bstar eta^2+O(eta^3). The fixed common-repair2 family
in review8684 suffices. Fix a finite T_upper large enough that it satisfies
(4). Its criticals lie near the reference
point, so (16),(19) show the constructed stationary polynomial has
value at most F_upper and is legal.

Every disk-root competitor with F<=F_upper satisfies the same fixed
cubic budget. Its normalized second surplus has limsup at most Bstar,
whereas the universal second infimum limit8619 gives liminf at least
Bstar along every sequence eta down to0. It therefore tends to Bstar.
The sequential profile selection8619, confirmed8684, and that theorem's
bounded second-budget moment bootstrap give, after simultaneous permutation,

\[
 h-h^*=o(1),\quad u-u^*=o(1),\quad
 U=U_0+O(\eta),\quad H=H_0+O(\eta),\quad V=o(1),\quad
 M=o(1),\quad a_k^\pm=O(\eta^2).                             \tag{20}
\]

Here V=sum(h)/eta: the cited identity V=8M/7+O(sqrt eta) gives V=o(1).
The active averaged radial is O(eta^2) by the reviewed second-order
root-curvature expansion with bounded h,u,W,D. Since both actual
radials are nonpositive, each is O(eta^2). This step does not require
conjugate symmetry of a competitor. By(9), E=O(eta), O=O(sqrt eta).
Thus every such competitor
eventually belongs to the fixed product neighborhood and convex z-ball
used above. The bounded-bootstrap estimates are uniform for a fixed budget,
and the profile convergence gives uniform inclusion by a sequence
contradiction: failure would give eta_n down to0 contradicting the
attributed infimum limit and profile selection. This is the quantifier bridge
from a local chart to all polynomials.

Applying(16),(19) proves F>=m(eta), with equality requiring E=O=0 and
z=z_eta. Then the normal inversion and(6) determine the critical
multiset, and monic integration from1-eta determines p uniquely.
Competitors with F>F_upper cannot improve or equal this minimum, since
m<=F_upper. No prior existence of an attained infimum is assumed.
The same uniform inclusion for every fixed budget T proves(5).

## 7. Symmetry gives the exact6+2 structure and analyticity in eta

The boundary-stratum objective and constraints are invariant under all
six-small-critical permutations and under conjugation followed by
interchanging the two large labels. On the free coordinates z these act
as simultaneous permutations and as (h_small,u_small)->(-h_small,u_small).
They preserve zstar and the convex ball. Formula(6) and uniqueness of
the normal inversion make this a symmetry of G(eta,z); the conditions
E=O=0 are preserved when conjugation exchanges the root branches.

The unique stationary branch must be fixed by these symmetries.
Therefore all six small h are zero and all six small u are equal.
The two large h are opposed and the two large u are equal. Hence
V=M=J3=0 along this branch. All chart coordinates are analytic in eta,
so u0,u1,Y=h1 are analytic with the initial values in(1). For small
positive eta, Y>0, and factor multiplication gives(2). This also
proves the polynomial coefficients, and then its exact reciprocal sum,
are analytic in eta:

\[
 m(\eta)=\frac6{1-\eta-\eta u_0(\eta)}
 +\frac2{\sqrt{(1-\eta-\eta u_1(\eta))^2+\eta Y(\eta)^2}}.      \tag{21}
\]

The initial value is z^9-1. The original-root properties follow from
E=O=0 and the uniform simple-root coverage in Section3. Prior theorem
8751 gives the radiuswise first three coefficients, so analyticity and
equality to that infimum give(3) without a new third-coefficient claim.

For a marked root of arbitrary phase, rotate(2) and normalize its leading
coefficient. This gives the complete equality classification up to the
usual rotation and nonzero polynomial scalar. The collar statement does
not assert a global minimizer classification at interior radii.

## 8. Exact-minimizer stability consequences and verification boundary

For each fixed q>=3 and finite A>=0, a budget F<=m(eta)+A eta^q is a
fixed cubic budget by(3). Inequality(5) gives
sum(-a_k^s)=O(eta^q) and ||z-z_eta||=O(eta^((q-2)/2)). The inverse
normal map has bounded derivatives, while (9) gives E=O(eta^(q-1)) and
O=O(eta^(q-3/2)). Thus the *whole* normalized critical multiset is at
joint distance O(eta^((q-2)/2)) from that of the exact minimizer.
In particular q=5 gives small imaginary critical coordinates O(eta^2)
and deviations of their real coordinates from eta*u0(eta) of
O(eta^(5/2)). The real exponent was already shown optimal by8841,
now confirmed8883. The small imaginary exponent is proved optimal
below. All estimates are uniform for a fixed A,q in an existential
collar.

**An exact feasible construction and sharp small imaginary rates.**
Fix any q>=3 and lambda>0. In the boundary-stratum chart choose

\[
 z(\eta)=z_\eta+\lambda\eta^{(q-2)/2}e_{h_3},\qquad E=O=0.    \tag{22}
\]

This specifies an actual monic polynomial: use the uniquely defined
analytic normal inversion in Section3, then(6) and the full anchored
critical-factor integral. For every sufficiently small positive eta it
is in the fixed chart and is disk-contained by Section3, with all four
active original roots exactly on the circle. The construction uses
analytic chart functions on a fixed neighborhood, not a truncated
polynomial or a sampled feasibility assertion. It allows the critical
points to collide and requires no spacing assumption.

Its designated small critical has exactly
Im(zeta3)=lambda*eta^((q-1)/2); the other five small imaginary
coordinates are zero. The large pair stays separated from this group
at scale sqrt(eta), so no critical permutation removes the small
imaginary displacement. Stationarity at z_eta and uniform Taylor
expansion give

\[
 F-m(\eta)=D_h\lambda^2\eta^q+o(\eta^q),\qquad
 D_h=\frac{2(a_T+b_T)}{H_0}>0,                               \tag{23}
\]

where the finite tangent coefficients, credited from the earlier finite
calculation and separately reconstructed by this checker, are

\[
\begin{aligned}
 a_T&=-11564/405-(20482/81)c+(123284/405)c^2,\\
 b_T&=49/180-(105889/486)c+(305123/1215)c^2.
\end{aligned}
\]

Indeed set t_i=h_i/b and r_i=u_i-u_z in the exact eta=0 chart.
Its finite quadratic cost is
a_T*sum(t_i^2)+b_T*(sum t_i)^2+(1/2)sum(r_i^2)+(1/4)(sum r_i)^2.
Thus its pure raw h3 second coefficient is(a_T+b_T)/b^2, equal to Dh.
The exact checker certifies Dh>0. The same quadratic form shows that
(22) has a positive joint normalized displacement of order
eta^((q-2)/2), so the general joint rate above cannot be uniformly
improved to little-o of that order.
For any prescribed positive excess constant A, choose lambda so that
Dh*lambda^2<A; the construction then belongs to that budget for all
sufficiently small eta. Thus sharpness holds in every positive such
budget class; A=0 is the unique minimizer itself.

For q=5, (23) has remainder O(eta^6), because z_eta and the Hessian are
analytic in eta and the cubic displacement term starts at eta^(13/2).
The family therefore has a fixed fifth excess budget and a small
imaginary critical coordinate exactly lambda*eta^2. No uniform
little-o(eta^2) bound, or stronger power, holds in that budget class.
This answers the previously open separate small-imaginary sharpness
question. It does not claim an optimal fifth objective coefficient.

The exact checker covers number-field signs, the four-normal Jacobian,
generic Newton/integration jets, active root curvature and dual identities,
all nine leading root radials, and the full twelve-variable finite tangent
Hessian. The analytic root maps, real-analytic divisibility, uniform
implicit inversion, strict slack integration, convexity continuation,
global competitor coverage and symmetry argument are ordinary written
mathematics outside a formal proof kernel. No sampled root, numerical
optimizer, incomplete enumeration or timeout is mathematical evidence
for these conclusions. The result does not supply an explicit boundary
width or settle the full Tang--Zhang first-power endpoint.
