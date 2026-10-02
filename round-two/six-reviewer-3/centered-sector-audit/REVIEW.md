# Independent effective six-real Sendov curvature audit

Actual reviewer **six-reviewer-3**, role **independent mathematical reviewer**, 2026-10-02. Shared signing identity does not establish independent authorship. Independently selected committed **LEMMA9164**, `bafkreibgfjuyl4am4hq3kw7oyc64zw5pdrecf6ipakukkyfbsdilpkqsju`, source `8a29091f0c1fdf3b310c3788987b3441a13fc1d6`, after reading its full mathematical body, ten directed dependencies/context relations and incoming review evidence. The only incoming assessment at selection was CITES9174, whose full body expressly left9164 unreviewed. No researcher assignment or desired verdict was supplied.

**Verdict: confirmed at its stated six-real, pointwise-neighborhood scope.** The divided response, universal initial block, Euclidean factors2 and6, whole six-real Hessian and local supremum argument are correct. A new full-third-derivative certificate independently proves its original strict window and the sharper window below. The analytic bridges are ordinary unformalized mathematics. Branch legality and stationarity are attributed mathematical inputs from9113, independently audited in9174. This verdict imports no collapsed-basin or whole-window global-minimum assertion.

Reviewed [author proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/centered-real-sector/PROOF.md); necessary [branch9113](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/validated-boundary-branch/PROOF.md) and [independent branch review9174](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/certified-branch-audit/REVIEW.md). Every source version, full byte length and SHA256 is in [INPUTS.json](INPUTS.json).

## Exact statement and improved bounds

Let \(0<\eta\le e=1/65536\), \(a=1-\eta\), and let
\(v(\eta)=(x,y,T,\xi_3,\xi_4,\omega)\) be the actual branch9113.
Put \(A=1-\eta(1+x)\), \(D=1-\eta(1+y)\),
\(W=1+\eta\omega\), with \(W^2=D^2+\eta T\).
For six **labelled real** normalized critical positions \(u_j\) near
\(u_0=x\mathbf1\), define

\[
 p'_u(z)=9\prod_{j=1}^6(z-\eta u_j)[(z-\eta y)^2+\eta T],
 \qquad p_u(a)=0.                                      \tag{1}
\]

The four unit-root equations at phases
\(t_3=-1/2+\eta\xi_3\), \(t_4=-c+\eta\xi_4\),
\(c=\cos(\pi/9)\), and the distance equation determine five analytic
tail parameters locally. The physical objective is

\[
 f_\eta(u)=\sum_{j=1}^6\frac1{a-\eta u_j}+\frac2{W(u)},
 \qquad \|u-u_0\|^2=\sum_j(u_j-x)^2.                  \tag{2}
\]

At \(u_0\) the gradient vanishes. Its six-real Hessian has a least
eigenspace \(\{h\in\mathbb R^6:\sum_jh_j=0\}\) of dimension exactly five.
The **proved sharper** bounds on its eigenvalue are

\[
 \boxed{\eta^2(1-33\eta/8)<\lambda_W(\eta)
                    <\eta^2(1-129\eta/32).}           \tag{3}
\]

The common-real eigenvalue is greater than \(15\eta^2/4\).
Thus (3) implies the author's \(\eta^2(1-5\eta)<\lambda_W<\eta^2(1-3\eta)\)
and its least-eigenvalue statement. Define the local coefficient supremum
over \(k\ge0\) for which some genuine feasible parameter ball satisfies
\(f_\eta(u)-f_\eta(u_0)\ge k\eta^2\|u-u_0\|^2\). Then

\[
 \boxed{\kappa_{\rm real}(\eta)=\frac{\lambda_W}{2\eta^2},\qquad
  \frac12-\frac{33}{16}\eta<\kappa_{\rm real}(\eta)
                         <\frac12-\frac{129}{64}\eta.} \tag{4}
\]

Every smaller nonnegative coefficient has a neighborhood at each fixed
positive \(\eta\). Neither a numerical displacement radius, a uniform
radius in \(\eta\), nor attainment of the supremum is asserted. The
comparison is with the branch value throughout this effective interval.
The coordinates remain real and labelled; repeated critical points do
not give an injective coefficient coordinate map, and none is required.

## Inputs and independent method

Review9174, source `737a94a084ef91129443179fdc892fbb12d65b0f`, proves the
branch has nine simple original roots, four active unit roots and five
strictly interior roots, positive \(A,D,W,T\), and common-real stationarity.
It also proves

\[
 \|v(\eta)-v_0\|_\infty<19\eta,\qquad
                  \Phi_\eta''(x(\eta))>45\eta^2/2.     \tag{5}
\]

Only these effective branch facts are needed. Its separate corollaries
using7290 and the8921/8955 global-minimum germ are not premises of (3)-(4).
The original9164 requires only the larger radius \(\rho=1/1024\) and
scalar curvature \(22\eta^2\) from9113. The improved bounds use (5),
explicitly credited to9174.

The new [system.py](system.py) integrates the literal derivative product
in (1), using dense coefficient convolution and an independently imposed
marked-root anchor. It does not use the author's shifted Q template.
[third.py](third.py) retains all actual first, second and third partials
of seven axes: seven gradients,28 symmetric Hessian entries and84
symmetric third entries, including purely parameter triples. This differs
from the author's21-component eta-Taylor jet. In products, a Hessian pair
and gradient axis have multiplicity1,2 or3 according to how often that
axis occurs in the triple. Stored derivatives are literal derivatives,
not factorial-divided Taylor coefficients.

[exact_numbers.py](exact_numbers.py) is an **unchanged copy of this
reviewer's own already audited9174 cubic-field/Fraction/D2 kernel**, SHA256
`b4bc4115fba1f4d5d762ace5f2ef4d29f0f019a3ebf6b7817db9113ce013eb68`.
This reuse is explicit; it is not new independent authorship of that
kernel. The new polynomial, third-order and response code imports no
researcher executable. Cubic-field arithmetic is exact in
\(\mathbb Q[c]/(8c^3-6c-1)\). Interval arithmetic uses exact Fraction
endpoints,112 exact embedding bisections, outward64-bit scalar majorants
and outward128-bit **serialized** interval endpoints. No floating value
is used in a mathematical predicate. No eta mesh or near-zero interval
division appears in the proof.

## Divided response and the universal initial block

Set \(u=(x+\delta,x-\delta,x,x,x,x)\), \(\sigma=\delta^2\),
\(r=\eta x\), \(s=\eta y\). The literal critical product is exactly

\[
 p'_u(z)=9[(z-r)^6-\eta^2\sigma(z-r)^4]
                                      [(z-s)^2+\eta T]. \tag{6}
\]

Holding the tail fixed, \(\partial_\sigma p/\eta^2\) is the anchored
integral of \(-9(z-r)^4[(z-s)^2+\eta T]\). With \(X=z-r\),
\(\Delta=r-s\) and \(B_p=\Delta^2+\eta T\), that primitive is

\[
 -\frac97(X^7-A^7)-3\Delta(X^6-A^6)
                           -\frac95B_p(X^5-A^5).       \tag{7}
\]

The checker independently compares **all coefficients** of (7) with
literal integration and with distinct labelled-factor products at three
positive rational eta values. Those values lie outside the theorem's
window and are algebraic controls, not additional certified eta cases.
It checks both actual and forcing anchors, every derivative coefficient
and all five adjacent-transposition generators on six distinct real
inputs. The degree and anchor identify the monic family exactly.

For a real polynomial \(p=\sum b_jz^j\), its unit-root equations are
\(I(p,t)=\sum_{j\ge1}b_jU_{j-1}(t)=0\) and
\(R(p,t)=\sum b_jT_j(t)=0\); the actual imaginary part is
\(\sqrt{1-t^2}I\). The phases are strictly inside \((-1,1)\), so these
equations preserve both conjugate roots. Let \(G_c\) comprise the two
I rows, two R rows and the distance row. It vanishes at eta0 for every
nearby common tuple, so \(H_c=G_c/\eta\) extends analytically there.
Write \(B=D_{(y,T,\xi_3,\xi_4,\omega)}H_c\) and let \(U\) be the
four circle evaluations of (7) followed by0. Differentiating the sigma
constraints gives

\[
 \partial_\sigma\mathrm{tail}=\eta w,
                            Bw=-U.                   \tag{8}
\]

The subtraction at eta0 is justified for **all nearby parameters**.
The literal primitive expands as

\[
 p=z^9-1+\eta[9+b_8(z^8-1)+b_7(z^7-1)]+O(\eta^2),
 \quad b_8=-9(3x+y)/4,\quad b_7=9T/7.                 \tag{9}
\]

At \(\tau_3=-1/2\), \(\tau_4=-c\), its affine first-order constraints
are \(b_8U_7(\tau_k)+b_7U_6(\tau_k)+\xi_kU'_8(\tau_k)\),
\(9+b_8[T_8(\tau_k)-1]+b_7[T_7(\tau_k)-1]\), and
\(2\omega+2(1+y)-T\). The real phase term vanishes because
\(T'_9=9U_8\) and \(U_8(\tau_k)=0\). Their tail derivative is a
universal constant matrix \(B_0\). All25 entries are independently
compared with full derivative-tensor differentiation; three generic
parameter tuples additionally check parameter independence. The initial
forcing is the evaluation of \(-9(z^7-1)/7\), hence also universal.
Exactly \(w_0=(0,1,0,0,1/2)\) and \(B_0w_0=-U_0\).

Write \(B=B_0+\eta B_1\), \(U=U_0+\eta U_1\),
\(w=w_0+\eta w_1\). Equation (8) gives

\[
 Bw_1=-U_1-B_1w_0.                                    \tag{10}
\]

The initial vector \(w_1^*=w_1(0,v_0)\) is independently computed by
exact five-by-five Gaussian elimination. Both inverse products and all
eight initial-field records match the author in the optional comparison.
The identity

\[
 6(1+x_0)+2\omega_0-2(w_1^*)_\omega
   =\ell=-\frac{4441}{540}+\frac{7046}{135}c
                                      -\frac{2288}{45}c^2 \tag{11}
\]

is reproduced exactly. This coefficient and the asymptotic centered
sector belong to prior [9033](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/exact-half-obstruction/PROOF.md)
and [9080](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/half-endpoint-audit/REVIEW.md),
sources `f6e5848da01148e65c9be0ec8a8b003d14d503d8` and
`215d6ae7843624382f0784e3e4b836339885e4a3`. They are not new results here.

## Covered certificate and sharper component response

For each fixed \(v\), the full third tensor rigorously encloses

\[
 \begin{aligned}
 B&=\int_0^1G_{c,\eta,\mathrm{tail}}(t\eta,v)\,dt,\\
 B_1&=\int_0^1(1-t)G_{c,\eta,\eta,\mathrm{tail}}(t\eta,v)\,dt,\\
 U_1&=\int_0^1U_\eta(t\eta,v)\,dt.
 \end{aligned}                                       \tag{12}
\]

The middle enclosure uses actual third partials divided by2, a convex
average with weight \(2(1-t)\). Both rectangles cover the entire closed
eta interval and all such segments: one with radius1/1024 about the
exact \(v_0\), and one with radius \(19e\). The actual branch is inside
the latter by (5); no unproved contraction constant from9164 is used to
shrink this input box. The whole original window is independently proved
also on the larger rectangle.

Set \(Y=B_0^{-1}\), \(w^*=w_1^*\). Exact nonnegative majorants enclose

\[
 D^*_{ij}\ge |(I-YB)_{ij}|,\quad
 r_i^*\ge |Y[-U_1-B_1w_0-Bw^*]_i|,\quad
 \beta=\max_i\sum_jD^*_{ij}<1.                        \tag{13}
\]

For the actual error \(q=w_1-w^*\), (10) implies
\(|q|\le D^*|q|+r^*\). Since \(\beta<1\), the positive Neumann
series proves

\[
 |q|\le (I-D^*)^{-1}r^*.                              \tag{14}
\]

The checker computes this resolvent with exact Fractions, verifies both
inverse products and nonnegative entries, and rounds each response
component outward. It also checks every resulting component bound is at
most the scalar bound \(\max r^*/(1-\beta)\). This retains directional
information in the omega response and improves the scalar estimate.
The full values,25 inverse entries and all enclosure entries are in
[EXPECTED.json](EXPECTED.json). In particular the omega error bounds are

| Covered parameter radius | \(\beta\) upper bound | omega response error upper bound |
| --- | --- | --- |
| \(1/1024\) | \(62771061664898283/4611686018427387904\) | \(921473325933144717/18446744073709551616\) |
| \(19/65536\) | \(62401956996669693/4611686018427387904\) | \(80032619175124673/4611686018427387904\) |

The first scalar response error is less than9/20 and its beta is less
than1/50, independently recovering the author's quantitative margins.
Correlation between block and residual need not be retained: (13)-(14)
are valid simultaneous componentwise majorants for every actual point.

The small-real part of (2) along the split is
\(6/A+(2\eta^2/A^3)\delta^2+O(\delta^4)\).
By (8), the tail contribution to its sigma coefficient is
\(-2\eta^2w_\omega/W^2\). The direction has squared norm2, and its
second derivative is twice that coefficient. Therefore the centered
**eigenvalue equals the sigma coefficient**, namely

\[
 \lambda_W=\eta^2[2/A^3-2w_\omega/W^2].               \tag{15}
\]

With \(\alpha=1+x\) and \(w_\omega=1/2+\eta(w_1)_\omega\), exact
algebra removes the eta division:

\[
 L=\frac{\lambda_W/\eta^2-1}{\eta}
  =\frac{2\alpha(3-3\eta\alpha+\eta^2\alpha^2)}{A^3}
   +\frac{\omega(2+\eta\omega)}{W^2}
   -\frac{2(w_1)_\omega}{W^2}.                        \tag{16}
\]

The larger rectangle gives \(-5<L<-3\). On the certified \(19e\)
rectangle, exact outward endpoints are

\[
 \left[
 -\frac{699798251390185512782731597868884941501}
        {170141183460469231731687303715884105728},\quad
 -\frac{1374333894937654980185802385301245104595}
        {340282366920938463463374607431768211456}
 \right]\subset(-33/8,-129/32).                      \tag{17}
\]

All rational comparisons in (17), positive denominators and original
window predicates are executed. Equation (16) is valid through its
removable eta0 limit, while (3) is asserted only for positive eta.

## Genuine family, all real directions and local supremum

For general six real labels, \(G_c(0,u,\mathrm{tail})=0\): the anchored
primitive is \(z^9-1\), the phases are fixed ninth roots and the distance
row is0. Thus dividing by eta is analytically removable uniformly in
these variables. The actual tail block at every branch point is
invertible by (13). At each fixed positive eta the real analytic implicit
function theorem supplies a unique tail on an open real parameter ball.
The original nine roots at its center are simple by the input. Their
analytic continuations preserve the marked root and the four prescribed
unit roots; the other four roots remain strictly interior by continuity.
Positive \(T,A,W\), strictly interior phase abscissae and all six small
real distance denominators persist after shrinking that ball. These
facts prove genuine disk-rooted feasibility and analyticity of (2),
including repeated small criticals. The labelled parameter ball need
not map injectively to coefficients.

Permutation invariance of the literal product and uniqueness of the
local tail imply permutation invariance of \(f_\eta\). At the common
tuple all six gradient entries coincide, and their sum is
\(\Phi'_\eta(x)=0\) by the parent. Hence all vanish. A permutation
invariant six-real Hessian is \(a_\eta I+b_\eta J\). Equation (15)
identifies its centered eigenvalue, and its common-direction eigenvalue
is \(\Phi''_\eta/6\) because the all-ones direction has squared norm6.
Equation (5) gives \(\Phi''_\eta/6>15\eta^2/4\). Equation (3) gives
\(0<\lambda_W<\eta^2\). The common eigenvalue is strictly larger;
the least eigenspace is consequently exactly the centered five-space.
This computation counts multiplicity only in the six-real Hessian.

Fix eta and \(0\le k<\lambda_W/(2\eta^2)\). Hessian continuity gives
a sufficiently small convex feasible ball on which the least eigenvalue
is greater than \(2k\eta^2\). The integral Taylor identity at the
stationary point is

\[
 f_\eta(u_0+h)-f_\eta(u_0)
 =\int_0^1(1-t)h^TD^2f_\eta(u_0+th)h\,dt
 \ge k\eta^2\|h\|^2.                                \tag{18}
\]

Conversely, any proposed coefficient in such a neighborhood, restricted
to \(h=\delta(1,-1,0,0,0,0)\) and divided by its literal squared norm,
must satisfy \(k\le\lambda_W/(2\eta^2)\) as delta tends to0. Equations
(3), (18) and this necessity prove (4). The exact supremum conclusion
does not require proving its attainment.

## Reproduction and trust boundaries

[audit.py](audit.py) regenerates every field of the independent frozen
certificate. [controls.py](controls.py) checks19,471 exact predicates,
including162 monomials covering every seven-axis monomial of total
degree at most3 and pure powers4 through9, with all84 third partials
checked against falling-factorial differentiation. Seven damaged
mathematical objects reject: factorial confusion, a missing eta-eta
mixed derivative, distinct-triple multiplicity, an unanchored constant,
the missing eta split factor and the two metric factors.

[replay.py](replay.py) hashes all21 pinned mathematical/source inputs,
verifies unchanged own-kernel provenance, and runs author and independent
programs in separate processes. Entire initial algebraic records agree;
entire independent frozen records and outputs agree normally and under
`-O`. The author replay verifies its complete original fixture and its
own alternate Fraction arithmetic; those are source-bound corroboration,
not independent derivations. Six external malformed/missing/altered
independent fixtures reject across normal and optimized modes.
Canonical independent record SHA256:
`97eb991ae0d81f077e0497feea4f9e10d50e6857112aab021805996ec2a34f09`.
Original record SHA256:
`52c030292234fb15f1eea3c224e073942237bcffe06f00961e8d60e3dfaed9d2`.

[VALIDATION.json](VALIDATION.json) records CPython3.12.14, native threads1,
serial45-second child guards, original normal/O4.637/4.782 seconds,
independent normal/O3.252/3.081 seconds and peak child RSS21,088KiB.
No failed, timed-out or partial calculation is treated as a mathematical
nonexistence result. Exact arithmetic and finite source checks do not
formalize the ordinary analytic arguments above or the attributed parent
theorem. The shared key does not supply reviewer independence; the named
author, newly written method and disclosed own-kernel reuse do.

## Primary literature and prior-art scope

Primary [Teng Zhang2609.19126](https://arxiv.org/html/2609.19126) distinguishes
the first-power conjecture from its quadratic theorem; Conjecture1.2
contains the exponent1 case, while Theorem1.3 proves exponent2. Earlier
[Tang--Zhang2508.10341](https://arxiv.org/abs/2508.10341) provides the
first-power context. Neither theorem proves unrestricted first-power
stability. Current problem briefs and published campaign results remain
authoritative; no known ell coefficient, branch or asymptotic half-gap
is advertised as newly discovered here.

9033/9080 already establish the negative first curvature correction and
the raw half-endpoint obstruction in the inherited existential complex
germ.9164 makes a **restricted real** curvature interval and local
coefficient effective in eta. The present review proves (3)-(4) by a
new componentwise response estimate on the already certified9174 tube.
8991's minimum series and8921/8955's global-minimum germ are contextual:
their existential extent cannot be replaced by this whole explicit
interval.7290's collapsed contour theorem is also not used here.
9111 and9121 are complementary origin-polar/angular claims and are not
premises for this real-sector audit; no verdict is transferred to their
new extensions. The unrestricted degree-nine first-power endpoint, all
complex tangent sectors, mixed displacements and global competitor
entry across the effective window remain outside this verdict.

## Strengthening and improvement opportunities

**Proved:** (3) replaces5 and3 with33/8 and129/32; (4) gives the corresponding
sharper local-supremum interval. The common-real eigenvalue bound15/4
uses the already proved9174 scalar margin divided by6. Positive exact
componentwise Neumann majorants reduce the relevant omega response error
and give a reusable response method without interval division by eta.

**Concrete remaining work:** independently certify the odd/common-
imaginary and centered-imaginary sectors and their full constraint block
before asserting a twelve-coordinate lower bound. Bound third derivatives
of the genuinely eliminated full objective on an explicit displacement
box to make a nonlinear neighborhood width effective; the eta window
alone does not give this width. Whole-window global-minimum identification
requires all-competitor concentration and entry estimates beyond this
branch calculation. Sharper component boxes or eta-dependent tubes could
tighten (3), but the exact ell and the original spectral factors retain
their existing credit.
