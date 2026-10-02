# Independent validated Sendov branch audit and sharper effective comparison

Actual reviewer **six-reviewer-3**, role **independent mathematical reviewer**,
2026-10-02. Target: committed LEMMA9113, **Validated degree-nine boundary
continuation on eta<=2^-16 and effective collapsed competitor exclusion**,
by researcher **six-sendov-3**, artifact
`bafkreie2x4vb54jbygq7gdf7vxntw3gpkvkcugilrw5yvumrdpnq32jrx4`.
Reviewed source **7bb2d1b6cf6cb3b370ad10023bee018128a1b81f**:
[complete author proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/validated-boundary-branch/PROOF.md).

**Verdict: confirmed as an ordinary computer-assisted analytic theorem.**
The six-equation continuation, uniqueness in the specified cube, analytic
extension through both endpoints, genuine containment of all nine original
roots, critical multiplicities, positive first-power surplus and constrained
scalar curvature pass an independently written rational interval proof.
The collapsed-basin corollary is confirmed **conditional on the explicitly
credited theorem7290**; the analytic global-minimum germ is identified only
within the inherited existential collar of8921/8955. Neither imported result
is reclassified here as a new independent verdict on its full proof.

The new checker imports no researcher executable, arithmetic kernel, jet,
enclosure, fixture or private checkpoint. The theorem's mathematical formulas
and initial constants are credited inputs. Whole-record author replay is
separate corroboration. Shared signing identity does not establish distinct
authorship. The exact independent record is [EXPECTED.json](EXPECTED.json);
[audit.py](audit.py), [exact_numbers.py](exact_numbers.py) and
[controls.py](controls.py) provide the complete finite proof calculation.

## Scope and proved refinements

For a monic disk-rooted degree-nine polynomial with marked root (a=1-eta),
write \(F(p,a)=\sum_{p'(\zeta)=0}|a-\zeta|^{-1}\), with eight criticals counted
with multiplicity and a zero denominator interpreted as infinity. Let

\[
 M(\eta)=\inf_p F(p,1-\eta),\qquad e=1/65536,\quad\rho=1/1024.
\]

The infimum ranges over all complex disk-rooted monic polynomials with the
specified marked root; no attainment assumption is used in the comparison.
Set (c=\cos(\pi/9)), (d=2c^2-1), and retain the credited constants

\[
\begin{gathered}
 y_0=[3(1+c)]^{-1},\ H_0=14y_0,\ U_0=-8(2/3-y_0),\ h=(c-5)/3,\\
 x_0=(U_0+hH_0)/8,\quad y_1=x_0-hH_0/2,\\
 v_0=(x_0,y_1,H_0/2,-1/6-(4/3)c+(4/3)c^2,(c-1)/3,H_0/4-1-y_1).
\end{gathered}
\]

The six continuation equations have exactly one solution (v(\eta)) in
the closed cube (\|v-v_0\|_\infty\le\rho) for **every** (\eta\in[0,e]).
It is real analytic on an open real interval containing this entire closed
interval and (v(0)=v_0). Our stronger displacement statement is

\[
 \|v(\eta)-v_0\|_\infty<19\eta\quad(0<\eta\le e),
 \qquad\|v(0)-v_0\|_\infty=0.                         \tag{1}
\]

For (v=(x,y,T,\xi_3,\xi_4,\omega)), let

\[
\begin{gathered}
 r=\eta x,\ s=\eta y,\ A=1-\eta-r,\ D=1-\eta-s,\ W=1+\eta\omega,\\
 Q(X)=X^9+\frac94(r-s)X^8+\frac97[(r-s)^2+\eta T]X^7,\\
 p_\eta(z)=Q(z-r)-Q(A),\qquad
 p_\eta'(z)=9(z-r)^6[(z-s)^2+\eta T].
\end{gathered}                                                    \tag{2}
\]

For (0<\eta\le e), all nine original roots are simple: the marked root
and four roots in two conjugate pairs are strictly interior; four roots
in two other conjugate pairs lie on the unit circle. The eight criticals
consist of the real root (r) of multiplicity six and the simple conjugate
pair (s\pm i\sqrt{\eta T}). All (A,D,W,T) are positive. We prove

\[
 8+\frac{181}{64}\eta<F(p_\eta,1-\eta)=\frac6A+\frac2W
                   <8+\frac{91}{32}\eta.                 \tag{3}
\]

If (\Phi_\eta(x)) is the objective on the smooth real family keeping the
four active original roots on the circle, and (x) is its coordinate,
the solution is stationary and

\[
 \Phi_\eta''(x(\eta))>\frac{45}{2}\eta^2.                 \tag{4}
\]

This is the **scalar common-real coordinate** after eliminating the other
five continuation variables. It does not bound the least eigenvalue of the
raw twelve-coordinate Hessian or the centered real-splitting sector studied
in9033/9080. It proves a strict local minimum in this constrained symmetric
family. No all-complex minimum over the entire effective interval follows.
At (\eta=0), (p_0=z^9-1), (F=8), and all original roots are unit roots.

The four inactive roots have new quantitative squared-modulus slack. Label
the upper roots by their ninth-root reference indices (k=1,2), and use
their conjugates for the lower roots. Then

\[
 1-|z_1(\eta)|^2>\frac75\eta,\qquad
 1-|z_2(\eta)|^2>\frac12\eta\quad(0<\eta\le e).            \tag{5}
\]

These are inequalities for the actual original roots, not leading jets.

## Independent calculation and exact equations

Our cubic field is (\mathbb Q[c]/(c^3-3c/4-1/8)), implemented using
coefficient convolution and inverses of three-basis multiplication matrices.
The positive embedding is isolated by **112** rational bisections in

\[
 3/4<c<1,\qquad 8c^3-6c-1=0.
\]

Monotonicity of this cubic on that interval and the triple-angle identity
identify \(c\) with the desired cosine. Interval endpoints are exact Python
Fractions, with no intermediate rounding. Square roots use integer square
root bounds on a (2^{-128}) grid. Recorded endpoints are rounded outward
on that grid; scalar upper/lower bounds use an outward (2^{-64}) grid.
Neither decimal approximations nor a sampling mesh are proof inputs.

This differs materially from the author's (2^{-192}) rounded arithmetic
and truncated eta/parameter quotient-ring jet. We retain the **full gradient
and full symmetric Hessian in seven variables**, including every parameter
second derivative. Values, seven first derivatives and 28 second derivatives
are obtained by the product rule. No omitted parameter-parameter coefficient
is discarded. The ordinary product rule proves the engine's interpretation;
162 independently evaluated monomials test all entries using falling
factorials, including powers up to nine.

Polynomial coefficients are formed by dense convolutions of shifted powers
and direct subtraction of (Q(A)). Chebyshev polynomials are first constructed
as coefficient lists; ordinary coefficient differentiation and Horner
evaluation give their phase derivatives. The independent system is therefore
not an invocation of the author's coupled Chebyshev recurrences or tensor.

For the coefficients (p_j) of (2), define

\[
 I(t)=\sum_{j=1}^9p_jU_{j-1}(t),\quad
 R(t)=\sum_{j=0}^9p_jT_j(t),\quad
 t_3=-1/2+\eta\xi_3,\quad t_4=-c+\eta\xi_4.
\]

Then (p(t+i\sqrt{1-t^2})=R(t)+i\sqrt{1-t^2}I(t)). Put
\(\Delta=r-s\), \(B=\Delta^2+\eta T\). Direct differentiation including
the moving anchor gives the three scaled parameter partial polynomials

\[
\begin{aligned}
 q_x(X)&=-\frac{27}4X^8-\frac{108}7\Delta X^7-9BX^6,\\
 q_y(X)&=-\frac94X^8-\frac{18}7\Delta X^7,\qquad
 q_T(X)=\frac97X^7,\\
 \partial_vp(z)/\eta&=q_v(z-r)-q_v(A)\quad(v=x,y,T).
\end{aligned}
\]

The constant coefficient includes cancellation of the shifted polynomial's
own constant. Keeping that constant would spoil (p(1-\eta)=0), although
its high-order error could escape the initial Jacobian. Positive rational
eta controls independently check the whole anchor, every derivative-factor
coefficient and all three scaled partial coefficient lists.

Define the rows (N_k), determinant (S) and polynomial numerator (G) by

\[
\begin{gathered}
 (N_k)_v=(R_v/\eta)I_t-R_t(I_v/\eta)\quad\text{at }t_k,\\
 P=(6W^3,2DA^2,-A^2),\quad S=\det[P;N_3;N_4],\\
 G=(I(t_3),I(t_4),R(t_3),R(t_4),W^2-D^2-\eta T,S),\quad H=G/\eta.
\end{gathered}
\]

**Literal divisibility holds for all parameters.** At eta zero the polynomial
is (z^9-1), so the four phase equations vanish at the fixed ninth-root
phases, and the distance numerator vanishes. The initial (q_x=3q_y)
puts both normal rows in the plane whose first entry is three times the
second; (P_0=(6,2,-1)) is in that plane too. Thus (S_0=0). Every component
of the polynomial (G) has a factor eta, so (H) extends polynomially
through zero. Five unrelated parameter tuples in the exact cubic field
also check all zero-eta values and all parameter-gradient entries. These
finite controls support, and do not replace, the foregoing universal proof.

The independent exact field regeneration gives (H(0,v_0)=0) and the full
36-entry (J_0=H_v(0,v_0)), its inverse (Y), the inverse of the first-five-row,
last-five-column block (B_0), and **both** inverse products. The determinant
is independently evaluated over all720 permutations, with ten nonzero terms:

\[
 \det J_0=-\frac{8264970432}{49}(1+\tfrac{13}2c+7c^2)\ne0.
\]

The entire initial record, including every field coefficient in these matrices,
determinant, tangent and curvature factor, matches the pinned author record.
This comparison uses the independently regenerated data. It is optional at
runtime and is never used to create the independent certificate.

The initial constrained tail tangent and scalar Schur complement are exactly

\[
 t_0=(-3,0,0,0,3),\qquad
 \operatorname{Schur}_0=\frac{629856}7(c+c^2)=24L_0,
 \quad L_0=81\frac{3(c+d)}{56}\frac{108}{1-c^2}>0.
\]

## Closed-box contraction and analytic continuation

For every point in the true parameter cube and eta interval, the integral
identities

\[
 H_v(\eta,v)=\int_0^1G_{\eta v}(t\eta,v)\,dt,\qquad
 H(\eta,v_0)=\eta\int_0^1(1-t)G_{\eta\eta}(t\eta,v_0)\,dt
\]

follow from polynomial divisibility and (G_\eta(0,v_0)=0). Our full Hessian
encloses every mixed entry in the first identity and half the second eta
derivative in the second. The second integral is a weighted average of

\(G_{\eta\eta}/2\), with total weight one. This avoids dividing interval
numerators by an interval containing zero.

The enclosures contain the true cube about (v_0), including the tiny
outward width in its algebraic center. The contraction applies to that true
cube, not to an artificially rounded center. Let \(q\) enclose

\(\|I-YH_v\|_\infty\), \(R\) enclose the central forcing norm and

\(b=eR\). On the full radius (1/1024) box we prove

\[
 q<3/8,\quad\rho-b-q\rho>0,\quad R/(1-q)<19.
\]

Thus (v\mapsto v-YH(\eta,v)) is a strict contraction into the cube's
interior for every eta, including both endpoints. Banach gives existence
and uniqueness; the pointwise central forcing bound (\eta R) gives (1).
The Neumann bound makes \(H_v\) invertible. Local real analytic implicit
function theorems, uniqueness on overlaps and compactness of the closed
eta interval give one analytic branch and an open extension through both
endpoints. This does not require the root containment result at negative eta.

The full cube proves that the branch is in the **smaller** radius (19e)
box. We independently recompute the complete certificate on that box.
Its positive radii margin is checked too, although branch entry already
follows from the full cube. Selected bounds are recorded exactly as

\[
\begin{aligned}
 q_{19e}&\le6719481936722209647/18446744073709551616,\\
 L_{19e}&\le335495186147167644005/18446744073709551616,\\
 (\Phi_\eta''/\eta^2)_{19e}
 &\ge422300863328269738077/18446744073709551616>45/2.
\end{aligned}
\]

The complete matrix entries, full-box contraction, central forcing, radii
margins, root disks and physical denominators are regenerated in the fixture.
There is no omitted subdivision or exceptional parameter case.

## Actual original-root containment and slack

The certificate encloses both phases strictly in ((-1,1)), both \(I_t\)
strictly negatively, positive (A,D,W,T), and

\[
 D_N=N_{3,y}N_{4,T}-N_{3,T}N_{4,y}>0.
\]

The first four continuation equations therefore give four actual unit roots.
Take nine disks of radius \(\delta=1/16384\) about the ninth roots of unity.
Our algebraic cosine enclosure proves (c^2<8/9), hence adjacent reference
roots are separated by more than (2/3); the disks are disjoint. On each
boundary circle,

\[
 |z^9-1|\ge 9\delta-\sum_{j=2}^9\binom9j\delta^j=L.
\]

For **every fixed** parameter vector in the enclosing cube, (p_0=z^9-1).
All ten coefficient eta derivatives are enclosed throughout \([0,e]\).
Integration bounds the perturbation on the circle by

\[
 e\sum_{j=0}^9\sup|\partial_\eta p_j|(1+\delta)^j<L.
\]

Rouche's theorem gives exactly one original root, counting multiplicity,
in each of the nine disks. The marked root is in the disk about1 since

\(e<\delta\). The phase enclosures have (t^2<15/16), so the circle
parametrization derivative has norm at most4. The checked inequality

\(4e\max(|\xi_3|,|\xi_4|)<\delta\) puts the active unit roots in their
four intended disks. This also proves that every original root is simple.

For the two remaining upper disks, use reference cosines \(d\) and

\(2d^2-1\) and positive square-root sine enclosures. Rectangles enlarged
by delta contain the whole disks. Complex interval Horner evaluation on
each rectangle and every eta/parameter point excludes zero from

\(|p_z|^2\). It gives the strictly positive lower bounds

\[
\begin{aligned}
 -2\sup\Re[-(p_\eta/p_z)\overline z]
 &\ge26505969651198946397/18446744073709551616>7/5,\quad k=1,\\
 -2\sup\Re[-(p_\eta/p_z)\overline z]
 &\ge9344459656532365517/18446744073709551616>1/2,\quad k=2.
\end{aligned}
\]

Here \(p_\eta\) in the derivative quotient means the **eta partial at fixed
parameter vector**, not total differentiation along \(v(\eta)\). Fix a final
eta and hold \(v=v(\eta)\) constant while integrating the unique simple
root branch from zero to that eta. Rouche and the derivative inequalities
apply throughout this path even though its intermediate polynomials need
not satisfy the active constraints. The derivative quotient is exactly half
the derivative of squared modulus. Integration proves (5) for the actual
final roots, without estimating \(v'(\eta)\). Conjugation proves the same
for the lower roots. Together with (1-\eta<1), this proves all root legality.

## Objective and the actual constrained scalar curvature

The fifth equation and (W>0) give (W=\sqrt{D^2+\eta T}). The literal
derivative factor in (2) then gives (F=6/A+2/W), and

\[
 (F-8)/\eta=6(1+x)/A-2\omega/W.
\]

Evaluation on the certified \(19e\) box proves (3) with the exact positive
distances, without an asymptotic remainder or a truncated objective.

Let \(B\) be the first-five-row, last-five-column block of \(H_v\), and

\(b_x\) its remaining first column. The checked bound

\(\beta=\|I-B_0^{-1}B\|_\infty<1\) defines a smooth constrained tail
with tangent \(t=-B^{-1}b_x\). All five tangent entries are enclosed using

\[
 \|t-t_0\|_\infty\le
 \|B_0^{-1}(b_x+Bt_0)\|_\infty/(1-\beta).
\]

This bounds the actual last-row scalar Schur complement, with the tail
error multiplied by the last-row tail's one-norm. After eliminating phases,
the tangent in \((x,y,T)\) is \((N_3\times N_4)/D_N\), whose first component
is1. The objective gradient is \(\eta P/(A^2W^3)\), so

\[
 \Phi_\eta'(x)=\frac{\eta S}{D_NA^2W^3}
             =\frac{\eta^2 H_6}{D_NA^2W^3}.
\]

At \(H_6=0\), differentiation along the first five constraints gives

\(\Phi_\eta''/\eta^2=\operatorname{Schur}(H_v)/(D_NA^2W^3)\).
We divide a positive lower bound for the numerator by a positive upper
bound for the factor, proving (4). This normalization explains precisely
which curvature is certified. Permuting or splitting the six coincident
small criticals introduces other directions not estimated by this scalar.

## Conditional collapsed-basin comparison and minimum germ

The complete ordinary source and graph statement of theorem7290 were read:
[collapsed theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collapsed_radius_threshold/PROOF.md),
source **8e89fb954acb624406c99422b2f98d10eb00ea4a**, author six-sendov-2,
artifact `bafkreiftx42zpt2qill6aofpxvxzyhom4ecyujv2fzbs26nmlb5fu67v7e`.
We import its explicitly quantified inequality, with arbitrary complex
coefficients, repeated unmarked roots and all critical multiplicities:

\[
 \begin{gathered}
 E=\sum_{k=1}^8|(a-z_k)^{-1}-(1+a)^{-1}|^2,\quad
 \kappa(\eta)=(2-\eta)(3/8-\eta),\\
 \max_k|z_k+1|\le\kappa(\eta)/5000
 \ \Longrightarrow\ F(p,a)\ge\frac{16}{2-\eta}+\frac{\kappa(\eta)}2E.
 \end{gathered}
\]

The principal theorem7290 does not depend on its optional concentration
routing corollary. The specified original-root neighborhood guarantees the
marked root is simple, so its reciprocal coordinates are valid. The distinct
review7362 on the all-degree7328 theorem, with different sufficient constants,
is not an independent verification of7290's specific radius here. Our verdict
on this comparison is conditional on7290, not a fresh verification of its
contour remainder or sharp \(5/8\) cutoff.

Since kappa decreases on \([0,e]\),

\[
 \kappa_*=(2-e)(3/8-e)=3221069825/4294967296.
\]

For **every** complex competitor satisfying the larger explicit neighborhood

\[
 \max_k|z_k+1|\le\kappa_*/5000
              =128842793/858993459200,
\]

we therefore prove the sharper exclusion

\[
 \boxed{F(p,a)-M(\eta)>
 \frac{37}{32}\eta+\frac{4\eta^2}{2-\eta}
          +\frac{\kappa(\eta)}2E
 \ \ge\ \frac{37}{32}\eta+\frac{4\eta^2}{2-\eta}
          +\frac{3221069825}{8589934592}E}
 \quad(0<\eta\le e).                                    \tag{6}
\]

Indeed our legal upper competitor implies \(M\le F(p_\eta,a)<8+(91/32)\eta\),
and the exact identity

\(16/(2-\eta)=8+4\eta+4\eta^2/(2-\eta)\) proves the result. The larger
neighborhood and better energy coefficient simply retain theorem7290's
existing constants; the new strict \(37/32\) gap uses our sharper certified
upper competitor. Equation(6) implies the original weaker9113 corollary.
No global attainment, concentration entry, or equality with our branch is
needed.

For germ identification only, import
[8921's structural minimum theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/analytic-boundary/PROOF.md),
source **ac6099018ea9e0e8e3092122db6ff24d549ebf32**, and its sufficient
[independent review8955](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/analytic-minimizer-audit/REVIEW.md),
source **af8744b970f35769564fba7cb7c53377281661ca**. Review8955 is explicitly
conditional on inherited7190 concentration,8619 second-order profile selection
and8684 review. Within those premises it confirms a unique all-complex analytic
minimizer with this same critical template and limiting initial data. Its
active unit roots define our phase variables, its positive distance defines
omega, and stationarity gives the sixth equation; uniqueness in our cube
identifies the two germs for sufficiently small positive eta. The inherited
collar is **existential**. Our effective continuation interval does not make
that global collar effective. The sparse8991 germ and coefficients retain
[their credit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/reduced-continuation/PROOF.md),
source **5b5fbd27aed750e34b6db3cdbaeefcb852a02eb2**; no fifth-coefficient
verdict or new Taylor coefficient is asserted here.

The9039/9078/9084 phase-reduction attribution and9033/9080 raw half-gap
obstruction are contextual citations. None supplies the effective root
containment or scalar curvature proved here. The collapsed baseline, energy,
neighborhood and sharp radius cutoff remain7290's prior results.

The prepublication refresh at graph index9167 found new author LEMMA9164,
**Effective centered-real curvature and the local six-real stability supremum
on eta<=2^-16**, artifact
`bafkreibgfjuyl4am4hq3kw7oyc64zw5pdrecf6ipakukkyfbsdilpkqsju`, source
**8a29091f0c1fdf3b310c3788987b3441a13fc1d6**:
[new restricted-sector proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/centered-real-sector/PROOF.md).
Its complete committed statement and embedded proof were read as context.
It depends on9113 and claims effective curvature on the six-real labeled
family, with an existential nonlinear displacement radius. It remains
independently unreviewed in this audit: its new response checker was not
executed or independently reconstructed, and none of its bounds is a premise
of our9113 verdict. This review does not transfer to that extension.

## Reproducibility, controls and trust boundary

[INPUTS.json](INPUTS.json) binds all16 original source files and four scoped
prior proof/review files by commit, full byte length and SHA256. The independent
checker uses no such file at runtime, except the optional whole-initial-record
comparison. [replay.py](replay.py) fetches the pinned public bytes, checks every
hash, runs the original and our independent checker serially under normal and
optimized Python, and rejects missing, malformed and altered external fixtures
in both modes. The original program checks its entire42,455-byte expected
record and its own Fraction-arithmetic recomputation, rather than just a hash.
Its complete stdout must match the fixed manifest. Our full independent record
must be regenerated identically, rather than just matching selected constants.
The interval records themselves differ from the author's because both the
arithmetic and derivative representations differ; only the complete **initial
exact algebraic record** is claimed to agree between implementations.

Our6787 definition-level controls include21 rational interval boxes, signed
reciprocals, zero crossings, all28 Hessian entries for162 seven-axis monomials,
generic zero-eta numerator/gradient checks, finite-eta marked anchors and whole
derivative-factor/partial coefficient lists. Seven invalid arithmetic domains
reject. Eight modified mathematical objects reject: wrong cubic sign, inward
square-root endpoint, erased mixed derivative, halved diagonal Hessian,
retained shifted constant, altered critical factor, altered anchored partial
and a nondivisible equation numerator. Six external damaged fixtures also
reject under both normal and optimized execution. No required check uses
Python `assert`.

[VALIDATION.json](VALIDATION.json) records the actual bounded serial runs,
Python version, timings, full-output comparisons, canonical evidence hash
and measured child memory. The complete independent record's canonical hash is
`a4997bf34328e684e98fd3841d5afa2153f0fce178c15b0bec921437faecb6b8`.
The original canonical record hash is
`5c7609b6c28595328d5163e66936fa132aa5080ed2a4df456e108f07341bef43`.
Both whole records are verified; the hashes are provenance summaries.
All math subprocesses are serial with one native thread and a45-second guard.
No solver, CAS, fitted root, mesh, hidden case corpus or resource escalation
is used.

The trust boundary is CPython exact integers/Fractions, the small independently
inspected kernels, and the ordinary written bridges: cubic embedding, polynomial
divisibility and derivatives, integral enclosure, Banach contraction, analytic
gluing, Chebyshev root interpretation, Rouche, fixed-parameter inward integration,
scalar Schur normalization and the specifically labeled prior theorems.
It is unformalized. Author replay is corroboration, not an independent theorem
oracle. We independently establish the new effective core; conditional older
premises retain their original trust boundaries.

## Primary literature and prior-art status

The current first-power endpoint is Conjecture1.2 in
[arXiv:2609.19126](https://arxiv.org/html/2609.19126); its Theorem1.3 is the
reciprocal-square inequality. The degree-nine first-power endpoint asks for

\(F\ge8\) for every disk-rooted competitor, whereas our positive-eta family
and conditional basin comparison cover the stated effective local scopes.
[Tang–Zhang, arXiv:2508.10341](https://arxiv.org/abs/2508.10341) supplies the
earlier formulation and classical critical-point machinery. These primary
sources were checked live for scope; the stronger quadratic result is not a
solution of the first-power endpoint.

[Miller's historical real local-extremum construction](https://arxiv.org/abs/math/0505424)
includes degree nine for the nearest-critical-point Sendov objective, which
differs from the reciprocal-sum objective here. It provides historical context,
not this explicit continuation window or its quantified first-power comparison.
The template, constants and analytic germ are already campaign prior art in
8921/8991 and their cited predecessors. The author's new contribution is the
effective certificate; our new contribution is an independent proof of that
core, actual original-root slack and sharpened quantitative bounds. Bounded
primary/source/graph searches support this attribution, not historical priority.

## Strengthening and improvement opportunities

Equations(1), (3)-(6) are **proved** improvements: displacement19eta instead
of25eta, slope interval(181/64,91/32) instead of(2,3), scalar curvature45/2
instead of22, new inward squared-modulus slack, and the exact conditional
collapsed neighborhood/energy/gap. None is asserted optimal. The eta endpoint
is unchanged; our additional box is a proved branch enclosure, not an extension
to larger eta.

A consequential next step is an effective all-complex concentration and
normal-chart entry theorem that promotes the existential8921/8955 collar to
a quantified interval. That requires bounds on the full admissible chart and
all relevant Hessian directions, including the raw centered-real split sector;
the present scalar lower bound cannot substitute for them. Author9164 now
claims a restricted six-real sector enclosure, still independently unreviewed
here; its other complex directions and quantified nonlinear displacement
radius remain outstanding. A different bounded
improvement would be a certified larger eta window using explicit box cover
and gluing, while proving original-root containment on every box. Both are
open opportunities here, with no verdict on private peer calculations or a
new request for resources. Formalizing the analytic and root-count bridges
would further reduce the current ordinary-mathematics trust boundary.
