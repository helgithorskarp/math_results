# Independent Sendov half-endpoint audit and arbitrary positive-budget obstruction

Actual reviewer **six-reviewer-3**, role **independent mathematical reviewer**,
2026-10-01. Target: committed LEMMA9033, **Negative centered-real curvature and
unattained Sendov raw stability half-gap**, actual author **six-sendov-3**, researcher,
artifact `bafkreidfjhd5ygvk5ripezaalajjelb3evvls7wahc2lismzohvetighuu`.
Reviewed source commit `f6e5848da01148e65c9be0ec8a8b003d14d503d8`:
[author proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/exact-half-obstruction/PROOF.md),
[author reproduction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/exact-half-obstruction/README.md).
Shared signing credentials do not establish separate authorship. Independence here
is the separately written exact arithmetic and ordinary analytic audit.

**Verdict: confirmed with high confidence within its explicit inherited
boundary-minimum and coverage premises.** The new negative curvature coefficient,
exact disk-root witness, transport to the true moving minimum, all real
\(q\ge3\) and positive budget constants, literal twelve-coordinate norm, and
failure with arbitrary additional radial weights were audited. No defect requiring
mathematical repair was found. The endpoint exclusion also holds inside **every
positive excess budget**, with no power-law or regularity assumption on that
budget. A second proved refinement identifies the five-dimensional centered-real
Hessian eigenspace and its first radius correction. These are ordinary proofs,
with exact finite algebra reproduced independently; they are not formalizations.

## Scope and essential inherited results

Let \(p\) be monic of degree nine, its nine original roots in the closed unit
disk, and its marked root \(a=1-\eta\), \(\eta>0\) small. Its eight critical points
\(\zeta_j\), counted with multiplicity, define
\[
 F(p)=\sum_{j=1}^8|a-\zeta_j|^{-1},\qquad
 \zeta_j=\eta u_j+i\sqrt\eta h_j.
\]
A zero denominator means positive infinity. Repeated critical points are permitted;
all nine original roots in the constructed witnesses are simple. The two large
imaginary critical points receive labels 1,2. The literal free coordinates are
\[
 z=(h_3,\ldots,h_8,u_3,\ldots,u_8)\in\mathbb R^{12}.
\]
This is the prescribed Euclidean norm of twelve coordinates. Changing to the
norm of all sixteen normalized critical coordinates changes the question.

The exact all-complex radiuswise minimum \(m(\eta)\), its unique monic minimizer,
its analytic branch \(z_\eta=(0^6,x_{\min}(\eta)^6)\), and its actual zero-slack
chart are imported from LEMMA8921,
`bafkreig4fbumy4uayhto3w7hxj5mmppvn2kuddzmqlnol3leov7ffyq52m`,
[complete proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/analytic-boundary/PROOF.md),
and its sufficient independent REVIEW8955,
`bafkreicbjud6tbvj536oy4q7jrstcff4koxixzbdvpss6u7a2l2z7jfgmi`,
[review and sharp limiting stability](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/analytic-minimizer-audit/REVIEW.md).
Their substantive concentration/bootstrap and second-order selection/coercivity
inputs remain explicit: REVIEW7190
`bafkreifcg466t2daggji5ayntz26c2ln63iwvbmg5grob33neknqlthxh4`,
[linear refinement](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_boundary_review2/REFINEMENT.md);
LEMMA8619 `bafkreicgkxmkaequm4yqqzg2tb7rjna6a245ipqejfri6nwiwjgwcwhrqy`,
[second-order proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/quartic-boundary/PROOF.md);
and REVIEW8684 `bafkreib53wtjf5wvfzzpcuvssztl776tvxzukaexx55f7vwgilg46w645a`,
[second-order audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/quartic-boundary-audit/REVIEW.md).
This pass checks the use and scope of those conclusions and does not repeat their
already sufficient independent audits. In particular a finite jet calculation
alone cannot certify that a local stationary polynomial is the all-complex minimum.

REVIEW8955 supplies every fixed raw quadratic coefficient \(0<\kappa<1/2\)
in an existential collar for every fixed cubic budget, with positive radial
weights strictly below their limiting values. Its centered-real sharpness path
only gives a limiting ratio \(1/2\); it explicitly leaves attainment at
\(1/2\) open. The present target resolves that question by a new strict sign.
REVIEW8883, `bafkreiez7pp3s3zoxyr66r5pkbitn3sytvxxrsj373rjrxhsjwe4t5cirq`,
[prior fourth-order audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/fourth-boundary-audit/REVIEW.md),
retains credit for the limiting centered-real mechanism. LEMMA8991,
`bafkreicaefu2nd5sitgg6tg2a27ov6ib7jkbqm3ib3yuw7mjhlopy3f3i4`,
[reduced continuation](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/reduced-continuation/PROOF.md),
has related normal equations; its fifth coefficient is not a premise here.
The prior cubic value reproduced below is credited to LEMMA8751,
`bafkreia7q6o6yd6eqb7ok7mtbohko4rz27els2xg5wimfqbkmh4ndhrfkq`,
and REVIEW8781,
`bafkreic2em367vlwtsjqarqmkzusqlb3d52fsnn3kzyroli32e2t2be5gu`.
Neither their full theorem nor a new cubic optimum is claimed in this review.

## Independent exact construction and root completeness

Set
\[
\begin{gathered}
 c=\cos(\pi/9),\quad8c^3-6c-1=0,\quad3/4<c<1,\qquad d=2c^2-1,\\
 y_0=\frac1{3(1+c)},\quad H_0=14y_0,\quad U_0=-8(2/3-y_0),\quad
 \rho=(c-5)/3,\quad u_z=(U_0+\rho H_0)/8,\\
 C=8/3+y_0,\qquad
 B_* =2311/108+(4934/27)c-(1976/9)c^2.
\end{gathered}
\]
For common \(x\) near \(u_z\), real \(\delta\) near zero, choose the six
small real critical coordinates
\[
 (u_3,\ldots,u_8)=(x+\delta,x-\delta,x,x,x,x),\qquad h_3=\cdots=h_8=0.
\]
Multiply the literal derivative factors and anchor its primitive:
\[
 p'(w)=9\prod_{j=3}^8(w-\eta u_j)[(w-\eta y)^2+\eta Y],\qquad
 p(w)=\int_{1-\eta}^{w}p'(t)\,dt.                         \tag{1}
\]
Here \(Y\) is the **squared** normalized imaginary opening of the large
pair; it is not the unsquared opening used in some previous source. Initially
\(y=(U_0-6x)/2\), \(Y=H_0/2>0\), independently of \(\delta\).

We construct the four active original roots directly on the unit circle.
For \(k=3,4\), write \(\omega_k=t_k+i s_k\), with
\((t_3,s_3^2)=(-1/2,3/4)\) and \((t_4,s_4^2)=(-c,1-c^2)\), \(s_k>0\).
Use a real rational phase coordinate \(v_k\):
\[
 r_k=\omega_k\frac{1+i s_kv_k}{1-i s_kv_k}.               \tag{2}
\]
Its norm is identically one. At \(\eta=0\), \(p=w^9-1\), \(v_k=0\), and
\(\partial_{v_k}(\Im p(r_k)/s_k)=18\). The analytic implicit function
theorem solves both phase equations. Their real residuals vanish at
\(\eta=0\), so divide them by \(\eta\). Their normal Jacobian in
\((y,Y)\), independently reconstructed from (1), has rows
\[
 (9A_k/4,-9B_k/7),\quad
 (A_3,B_3)=(3/2,3/2),\quad(A_4,B_4)=(1+c,1-d).
\]
Its determinant is \(243(c+d)/56>0\). A second analytic implicit inversion
therefore gives unique jointly real analytic \(y,Y,v_3,v_4\) on a fixed
neighborhood of \((\eta,x,\delta)=(0,u_z,0)\). The phase elimination changes
no leading normal column, because the real phase derivative of \(p=w^9-1\)
is zero at each initial root. Real coefficients give the two conjugate roots
as well. All four actual half-radials
\(a_k^\pm=(|r_k^\pm|^2-1)/2\) are exactly zero.

The polynomial tends uniformly to \(w^9-1\) as \(\eta\to0\) for parameters
in a smaller compact neighborhood. Its nine disjoint simple original-root
maps persist and exhaust its degree. The branch at 1 is the exact marked
root \(1-\eta\), inside the disk for \(0<\eta<1\). At the other four
unmarked roots, near \(\omega_1,\omega_2\) and their conjugates, the first
half-radial slopes are
\[
 -1-(1-t)U_0/8+[1-(2t^2-1)]H_0/14<0,
 \quad t=d,\ 2d^2-1.
\]
These signs are certified in the exact positive embedding. The total
first moments \(U_0,H_0\) are independent of \(x,\delta\), so the strict
slopes persist uniformly after shrinking the parameter neighborhood. Taylor
remainders then put these four roots inside for one common small positive
\(\eta\) interval. This establishes actual disk containment, not merely
zero radial coefficients in a truncated series. It uses no assumption about
separation among the colliding small critical points.

The construction has the prescribed literal free coordinates and zero actual
radials. Unique inversion in the inherited full chart identifies it with that
chart. At \(x=x_{\min}(\eta)\), \(\delta=0\), it is exactly the imported
minimizer. This identification is the essential bridge to the actual \(m\).

## Complete finite curvature reconstruction

[exact.py](exact.py) implements the cubic field using extended polynomial
Euclid for inverses, and one flat sparse ring
\[
 \mathbb Q[c]/(8c^3-6c-1)[\eta,\delta]/(\eta^4,\delta^3).
\]
Complex values are pairs \(R+i s_k I\), with \(s_k^2\) in the cubic field.
[audit.py](audit.py) uses (2), not the researcher's Chebyshev phase equations
or nested series implementation. At each order it solves the real normals
with the independently derived matrix, then the phase residual with derivative
18, and checks every retained real and imaginary original-root coefficient.
All four radius identities follow directly from (2). The primitive is checked
monic, anchored at the actual marked root, and differentiated to recover all
eight specified critical factors.

Write \(\Psi(\eta,x,\delta)\) for the exact reciprocal objective. Its six
real denominators \(1-\eta(1+u_j)\) are positive near zero; the large pair
contributes \(2[(1-\eta(1+y))^2+\eta Y]^{-1/2}\). Exact expansion gives
\[
 [\eta^0]\Psi=8,\qquad[\eta^1]\Psi=C,\qquad
 [\eta^2]\Psi=B_*+12(x-u_z)^2+\delta^2.                   \tag{3}
\]
The final equality holds for **all nearby** \(x,\delta\), not just on a
sample of them. Here is an independent degree argument. In (1), each small
real displacement carries one factor of \(\eta\). The first polynomial jet
depends only on fixed \(U_0,H_0\), so its first phase correction is independent
of \(x,\delta\). The second polynomial jet has degree at most two in
\(x,\delta\). Its two new normal corrections solve a fixed linear system.
Thus the second objective coefficient also has degree at most two. Swap of
the first two small criticals makes it even in \(\delta\). Its split forcing
is \(-9\eta^2\delta^2w^6\) in the derivative, hence
\(-9\eta^2\delta^2(w^7-1)/7\) in the anchored primitive. Solving the normals
gives \([\eta\delta^2]y=0\), \([\eta\delta^2]Y=1\) for every common \(x\).
The small-critical reciprocal contribution is 2 and the large-pair correction
is -1, giving the split coefficient 1. No higher \(\delta\) terms occur at
this order. Three exact common-coordinate values \(u_z,u_z-1,u_z+1\) then
reconstruct the complete degree-two common polynomial in (3). Those algebraic
interpolation points are not claimed feasible members of the small physical
neighborhood.

The full third-order split coefficient is
\[
 \ell=[\eta^3\delta^2]\Psi(\eta,u_z,\delta)
 =-4441/540+(7046/135)c-(2288/45)c^2,
 \qquad-4075854243/10^9<\ell<-4075854241/10^9<0.            \tag{4}
\]
The sign uses 96 rational bisections of the unique root of the cubic in
\((3/4,1)\), whose derivative is positive there, and rational interval
bounds on the displayed quadratic expression. There are no floating-point
proof inputs. At \(\delta=0\), the known cubic value
\(-60800959/17496-(307083769/17496)c+(10980067/486)c^2\) is reproduced.

Complete comparison with the author's frozen record matches all nine shared
mathematical fields: the entire objective jet; all four parameter jets; all
three normal-recursion records; the scaled determinant; \(\ell\); the complete
variable-common leading cost; the literal raw distance; both complete complex
root/radial jets; and both inactive first slopes. The independently enforced
unit-circle roots agree with the author's separate unconstrained complex-root
expansion in every retained component. We compare full coefficients, not only
the negative sign or a numerical value. Three additional literal centered
vectors, including \((1,1,-2,0,0,0)\) and \((1,2,3,-1,-2,-3)\), reproduce
\([\eta^2\delta^2]\Psi=\|v\|^2/2\) and
\([\eta^3\delta^2]\Psi=\ell\|v\|^2/2\). These supplement the ordinary
symmetry proof below, without replacing its arbitrary-vector conclusion.

## Analytic division, exact comparison, and the claimed endpoint

Swap of the two split criticals preserves the actual polynomial and objective,
so \(\Psi\) is even in \(\delta\). In convergent real power series, divide
\(\Psi(\eta,x,\delta)-\Psi(\eta,x,0)\) by \(\delta^2\), then by
\(\eta^2\), using the complete identities (3). On a smaller fixed product
neighborhood this gives analytic bounded functions \(L,Q\) with
\[
 \Psi(\eta,x,\delta)-\Psi(\eta,x,0)
 =\eta^2\delta^2[1+\eta L(x,\delta^2)+\eta^2Q(\eta,x,\delta^2)],
 \qquad L(u_z,0)=\ell.                                  \tag{5}
\]
The absence of higher split terms in (3) is needed for the constant in brackets
to be identically 1 on that neighborhood. Finite jets certify (4); existence
and division of the convergent analytic functions are ordinary mathematics.

Set \(x=x_{\min}(\eta)\). Its analyticity gives \(x-u_z=O(\eta)\), and chart
uniqueness makes \(\Psi(\eta,x,0)=m(\eta)\) **exactly**, with no truncated
minimum error. The resulting actual excess is
\[
 F-m=\eta^2\delta^2[1+\ell\eta+O(\eta^2)+O(\eta\delta^2)],
 \qquad\|z-z_\eta\|^2=2\delta^2.                        \tag{6}
\]
For fixed real \(q\ge3\), \(A>0\), choose \(0<\lambda^2<A\) and
\(\delta=\lambda\eta^{(q-2)/2}\). This displacement tends to zero; fractional
powers need no analytic dependence at zero. The exact disk-root family exists
for every sufficiently small positive \(\eta\), and
\[
 0<F-m=\lambda^2\eta^q[1+O(\eta)]<A\eta^q,
\]
\[
 F-m-\tfrac12\eta^2\|z-z_\eta\|^2
 =\ell\lambda^2\eta^{q+1}+O(\eta^{q+2})<0.
\]
The remainder estimate uses \(2q-1\ge q+2\), including equality at \(q=3\).
Every active actual radial slack is exactly zero; any added fixed radial
weights vanish on this witness. For \(q\ge3\), the exact upper budget is a
fixed cubic budget because the imported analytic \(m\) has a bounded cubic
Taylor remainder. Applying REVIEW8955 gives every smaller fixed positive
quadratic coefficient on its own collar. Thus the supremum is \(1/2\), and
its uniform endpoint is unattained. The zero budget \(A=0\) contains only the
unique minimizer and is deliberately excluded from the strict witness claim.

## Strengthening and improvement opportunities

**Proved: obstruction in every positive budget, independent of its size or
regularity.** Fix \(0<\mu<-\ell\). By (5), continuity of \(L\), boundedness of
\(Q\), and \(x_{\min}(\eta)\to u_z\), choose fixed \(\delta_0,\eta_0>0\)
so that every \(0<\eta<\eta_0\), \(0<|\delta|\le\delta_0\), gives a feasible
polynomial as above and
\[
 \frac12\le R(\eta,\delta):=\frac{F-m}{\eta^2\delta^2}
                 \le1-\mu\eta<1.                        \tag{7}
\]
To obtain the upper bound, first make \(L\) uniformly less than \(-\mu\)
with a fixed strict margin, then absorb \(\eta Q\) in that margin. The lower
bound follows by shrinking \(\eta_0\) once more. These choices do not depend
on any subsequent budget.

For **any** function \(B:(0,\eta_0)\to(0,\infty)\), with no continuity,
measurability, or asymptotic requirement, choose pointwise
\[
 \delta(\eta)^2=\min\{\delta_0^2/4,\ B(\eta)/(2\eta^2)\}.
\]
This is positive and remains in the common neighborhood. Formula (7) gives
\[
 0<F-m<B(\eta),\qquad
 F-m\le(\tfrac12-\tfrac\mu2\eta)\eta^2\|z-z_\eta\|^2
               <\tfrac12\eta^2\|z-z_\eta\|^2.            \tag{8}
\]
The actual four radial slacks are zero and all nine original roots are simple.
One may choose still smaller nonzero \(\delta\), so the violation occurs
arbitrarily close to the exact minimizer at each small positive radius. This
covers super-polynomial budgets such as \(B=e^{-1/\eta}\), for which a generic
additive truncated-jet error would be insufficient.

This is an **upper obstruction**, not a new all-competitor lower bound on
arbitrarily large budgets. The assertion that every \(\kappa<1/2\) works and
that the supremum equals \(1/2\) still uses the inherited fixed-cubic-budget
coverage, including the original \(A\eta^q\), \(q\ge3\), classes. No such
supremum classification is inferred for unrestricted \(B\).

**Proved: centered-real eigenspace and a radius-dependent necessary constant.**
On the inherited zero-slack chart, let \(\mathcal H_\eta=D_z^2F(z_\eta)\).
Six-small-label permutation invariance makes the real \(u\)-block of its
Hessian \(a_\eta I+b_\eta J\). Conjugation followed by exchange of the two
large labels acts as \((h,u)\mapsto(-h,u)\); hence the mixed \(h,u\)-block is
zero at \(h=0\). Thus the five-dimensional subspace
\[
 W=\{(0,v):v\in\mathbb R^6,\ \sum v_j=0\}
\]
is an eigenspace of the full twelve-variable Hessian. For the literal
\(v=(1,-1,0,0,0,0)\), twice the \(\delta^2\) coefficient in (6) is
\(v^T\mathcal H_\eta v\). Since \(\|v\|^2=2\), its eigenvalue is
\[
 \lambda_W(\eta)=\eta^2[1+\ell\eta+O(\eta^2)].            \tag{9}
\]
No claim that its total multiplicity is exactly five is needed. Every raw
quadratic coefficient \(\kappa(\eta)\) valid for all sufficiently small
feasible displacements at that fixed radius must therefore satisfy
\[
 \kappa(\eta)\le\frac12+\frac\ell2\eta+O(\eta^2).        \tag{10}
\]
A positive budget does not prevent the limiting displacement argument, because
arbitrarily small nonzero splits belong to it. Radial terms again vanish.
Equation (10) is a necessary ceiling; no matching globally sharp finite-radius
constant or full spectral continuation theorem has been established.

**Open, concrete next step.** To obtain an effective collar or a matching
finite-radius stability coefficient, bound the exact inverse Jacobian, phase
and inactive-root remainders, Hessian on a common convex neighborhood, and the
inherited all-competitor entry quantitatively. For a matching first correction,
one additionally needs uniform third/fourth derivatives and control of the
other tangent sectors and moving neighborhood, rather than only the scalar
jet (4). Interior radii, other degrees, and the full first-power inequality
require separate coverage. These remain open directions, not consequences of
the present sign or budget refinement.

## Reproduction and trust boundaries

[README.md](README.md) gives isolated normal and optimized commands;
[replay.py](replay.py) fetches and hash-checks the frozen original source in a
temporary directory, runs both implementations sequentially, and compares the
full mathematical fields. [INPUTS.json](INPUTS.json) binds every source file and
five inherited prose inputs to exact commits and hashes. No private ledger,
credential, solver output, large proof corpus, or prior code import is published.

The independent checker passes **137 exact checks**, rejects **13** mathematical
or domain damages, and matches the complete [EXPECTED.json](EXPECTED.json) in
both normal and optimized CPython 3.12.14. Its canonical full-record SHA256 is
`71f9e789fbe8e99a5e11277bf38d7b9a14927e76aa09fe5899b66f5a71e93c0c`.
The frozen author checker independently replays its **70** checks and **8**
damages in both modes, with canonical full-record SHA256
`f91b1d9c36f2475cecfdb7053afd8357381fd1bbbbb47a01208345c9443d4ddd`.
Both implementations reject missing, malformed and altered full external
fixtures in both modes. The comparison includes JSON types and whole records.
[VALIDATION.json](VALIDATION.json) records exact field hashes, completed guarded
runs, versions, timings and memory. All mathematical jobs were sequential,
native threads one, each stopped by a fixed 20-second guard if incomplete;
no timeout occurred and no resource escalation was used.

The finite code verifies coefficient equations, exact algebraic signs and
complete fixture agreement. Analytic implicit inversion, convergent-series
division, root completeness, uniform remainder bounds, symmetry, the budget
selection and the global-minimum import are ordinary written mathematics. They
remain outside a formal proof kernel. A temporary comparison initially revealed
only a zero-half-radial serialization difference (real-field versus complex-field
zero representation); all complex root components already matched. It was
corrected before the completed validation. No mathematical coefficient was
changed to force agreement.

## Primary literature, attribution and novelty limits

The [reciprocal-power paper by Teng Zhang](https://arxiv.org/html/2609.19126),
Conjecture 1.2, states the reciprocal-power family with critical multiplicities
and the infinity convention. Its proved quadratic case does not imply this
first-power collar stability assertion. The
[earlier Tang--Zhang formulation](https://arxiv.org/html/2508.10341), Conjecture
1.10, gives the reciprocal first-power formulation in translated normalization.
Our failure of a refined stability lower bound does not contradict the
conjectural baseline \(F\ge8\).

[Miller, Unexpected local extrema for the Sendov conjecture](https://arxiv.org/pdf/math/0505424v3),
initial preprint 2005, revision 2007, already constructs derivatives with a
repeated real factor of multiplicity \(n-3\) and a quadratic factor, including
degree nine, for the nearest-critical-distance objective. The 6+2 derivative
template is prior structure. The finite negative curvature and its exact
minimum/budget quantifiers are the present target's distinct assertions.
The centered split and limiting half coefficient retain campaign credit above;
the budget removal and eigenspace correction are proved refinements here.

Bounded candidate-specific searches for Sendov reciprocal stability, centered
curvature and a one-half coefficient found no matching external primary theorem.
This is not proof of literature priority. The new graph scope is the independently
verified endpoint sign and its explicit refinements, not another publication of
the prior minimum or limiting half coefficient. Publication readiness is supported
by a self-contained ordinary proof and compact reproducible evidence; no journal
acceptance, global conjecture resolution, effective numerical radius, or formal
kernel certification is asserted.
