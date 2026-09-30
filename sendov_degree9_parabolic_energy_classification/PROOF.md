# Degree-nine parabolic energy classification and global quantitative stability

Actual author **six-sendov-3**, role **researcher**, 2026-09-30.
Complete ordinary written author proof with exact coefficient controls.
Independent review of this extension is pending. Analytic arguments and
coefficient-space completeness are outside a formal proof kernel.
The stationary branch, local Hessians, sextic concentration and classical
reciprocal matrix retain attribution.

## 1. Definitions and quantified results

Let \(p=c(z-a)\prod_{j=1}^8(z-z_j)\), \(c\ne0\), \(a\in[0,1]\),
\(|z_j|\le1\), \(z_j\ne a\). The marked root is simple; all other original
and critical algebraic multiplicities are allowed. Put
\[
a_0=5/8,\quad v=(1+a)^{-1},\quad
E=\sum|(a-z_j)^{-1}-v|^2,\quad
F=\sum_{p'(\zeta)=0}|a-\zeta|^{-1},\quad G=F-16v,
\quad\kappa=(1+a)(a-a_0).
\]
Small energy keeps all reciprocals finite. Rotation transfers the results
to a fixed nonreal marked root, using its modulus; scalar factors do not
matter.

The credited actual stationary branch is
\[
P_{a,e}=(z-a)(z+e^{i(7t+m_0)})(z+e^{i(-t+m_0)})^7,\quad E=e,
\]
\[
t^2=e/(56v^4)+O(e^2),\quad m_0=t^3b(a,t^2),\quad
b(a,0)=\beta(a)=(392-1197v+945v^2)/20.
\]
Its analytic mean and exact energy inversion are those of the
[local theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_finite_energy_local_minimum/PROOF.md),
independently confirmed in the
[finite-energy audit](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_finite_energy_review3/PROOF.md).
Write
\[
L(a)={1616a^2+1800a-1675\over224(1+a)^5},\qquad
a_*={10\sqrt{2198}-225\over404}<a_0.
\]
The constrained mean Hessian is \(10v^3+O(e)\), the coefficient of a
squared zero-sum seven-root split is \(t^2(L(a)+O(e))\), and each
constrained inward derivative is \(2v^2+O(e)\). These inputs are credited.

**Theorem 1 (every bounded scaled box).** For any compact
\(J\subset(a_*,1]\) and finite \(K>0\), there are \(t_{J,K}>0\) and
positive costs \(c_r,c_m,c_s\) depending only on \(J\) such that the
following holds for \(a\in J\), \(0<t<t_{J,K}\). In original-root coordinates
\[
z_A=-(1-\tau_A)e^{i(7T+M)},\quad
z_j=-(1-\tau_j)e^{i(-T+M+\eta_j)},\quad\sum_{j=1}^7\eta_j=0,
\]
solve the actual energy \(E=e(a,t^2)\) for \(T\) near \(t\). The whole
chart exists for
\[
\|\eta\|\le Kt^2,\quad |M-m_0|\le Kt^3,\quad
\tau_A+\sum\tau_j\le Kt^6,\qquad\tau_j\ge0,
\]
and throughout it
\[
F(p)-F(P_{a,e})\ge c_r(\tau_A+\sum\tau_j)
                 +c_m(M-m_0)^2+c_st^2\|\eta\|^2.             \tag{1}
\]
Equality forces the branch multiset. \(K\) is arbitrary finite; only
the threshold needs to shrink with it.

**Theorem 2 (parabolic global classification).** For every finite \(B>0\)
there is \(e_B>0\) such that
\[
0<e<e_B,\qquad 0\le a-a_0,\qquad (a-a_0)^2\le Be              \tag{2}
\]
imply that the global minimum of \(F\) on the full closed-disk level
\(E=e\) is attained precisely at \(P_{a,e}\) or its conjugate, modulo
root permutation and scalar. This includes \(a=a_0\), every independent
inward motion and critical collision. The minimum is the restriction
of the same real-analytic branch function of \((a,e)\).

**Theorem 3 (global entry at finite tolerance).** For every finite
\(B>0,D\ge0\), after decreasing an existential threshold \(e_{B,D}>0\),
every polynomial in (2) with
\[
F(p)\le F(P_{a,e})+De^3                                      \tag{3}
\]
has the coordinates in Theorem 1 after permutation and possibly
conjugation, with a finite scaled-box bound \(K_{B,D}\). In particular
(1) holds for every such polynomial. With
\(\mathcal X=F(p)-F(P_{a,e})\ge0\), it implies
\[
\sum\tau_j\le C\mathcal X,\qquad
|M-m_0|\le C\sqrt{\mathcal X},\qquad
\|\eta\|\le C\sqrt{\mathcal X/e}.                             \tag{4}
\]
Costs can be chosen on one fixed compact interval about \(a_0\); the
energy threshold can depend on \(B,D\). This covers any fixed positive
finite normalized tolerance, not only a vanishing tolerance.

No effective numerical neighborhood, arbitrary-energy classification,
arbitrary marked-radius global theorem, all-degree extension, historical
priority, or unrestricted first-power endpoint is asserted. Previous
basin coefficients do not change.

## 2. Credited support and analytic extension to any finite box

Use the construction of the
[preceding global-minimizer proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_global_energy_minimizers/PROOF.md),
graph **bafkreiddzdvkvddxc3ry5m5d4l3o6dyjox5ipcleimmknfr5la3cow3c7u**,
height **7839**, latest source
**c32c7afc246cef297d8776684d0c4e6f25128b09**.
Its new uniform bridge remains independently unreviewed. It supplied a
small fixed scaled box; the extension to every finite box is proved here.

The classical matrix \(N=\operatorname{diag}(u_j)(I+\mathbf1\mathbf1^T)\),
\(u_j=(a-z_j)^{-1}\), has critical reciprocals as eigenvalues.
Equivalently its characteristic polynomial is
\(C(q)=9R(q)-qR'(q)\), \(R(q)=\prod(q-u_j)\). Collapse has seven
eigenvalues \(v\) and a simple far eigenvalue \(9v\). Fixed external
Riesz contours give an analytic near block \(N_7\) and far root \(q_f\),
without internal near-root labels.

At the candidate put \(B_0=-e^{i(-t+m_0)}\), \(u=(a-B_0)^{-1}\),
\(c_0=iB_0u^2\). The credited holomorphic primitive, with \(f(0)=|u|\),
has
\[
f'(w)={c_0(\bar u+\bar c_0w)\over
       \sqrt{(u+c_0w)(\bar u+\bar c_0w)}}.
\]
The square root is positive at zero. Its scalar defect satisfies
\[
H(w)=|u+c_0w|-\Re f(w)=(\Im w)^2K_0(a,t,\Re w,\Im w),\quad K_0>0. \tag{5}
\]
All are uniformly analytic on one small disk for \(a\in J\). Let \(q_n\)
be the separated simple near root and set
\[
A=\Re\operatorname{tr}f((N_7-uI)/c_0)+|q_f|,\quad
w_n=(q_n-u)/c_0,\quad \Phi=A+H(w_n).
\]
The trace counts all seven near eigenvalues. Adding \(H(w_n)\) restores
the exact modulus of the simple near root, while the other six use the
harmonic minorant. Hence
\[
F\ge\Phi,\qquad F(P_{a,e})=\Phi(P_{a,e}).                     \tag{6}
\]
The credited local proof and independent audit show matching angular
first derivatives and Hessian at the candidate: its semisimple sixfold
angular compression is Hermitian in the normalized tangent direction,
and (5) makes the missing defect fourth angular order. No smoothness of
the true objective on a full mixed neighborhood is assumed.

Set
\[
\eta=t^2x,\quad\sum x_j=0,\quad M=m_0+t^3y,\quad \tau=t^6r.    \tag{7}
\]
Temporarily allow signed real \(r\). On any prescribed finite compact
box in \((x,y,r)\), \(T=ts\) makes \(E/t^2\) jointly analytic, with
value \(56v^4s^2\) at \(t=0\) and \(s\)-derivative \(112v^4>0\) at one.
The leading value is independent of the scaled variables. A uniform
analytic implicit function theorem gives the energy chart on each such
box by shrinking its \(t\)-range.

With \(P=I-\mathbf1\mathbf1^T/8\) and
\(\theta=(7,-1,\ldots,-1)\),
\[
N_7=vI-iv^2t\,P\operatorname{diag}(\theta)P+O(t^2).
\]
Its divided leading matrix has simple eigenvalue \(6\), eigenvector
\(\theta\), and sixfold eigenvalue \(-1\) on the balanced seven-root
subspace. The fixed divided gap is seven, independent of \(x,y,r\).
Fixed divided contours therefore construct \(q_n\) analytically on
every finite box, including \(t=0\). This uses no inverse shrinking
undivided gap or six internal labels. All normalized scalar arguments
in (5) tend to zero uniformly on a fixed box, preserving (6).

Write \(\mathcal D=\Phi-F(P_{a,e(a,t^2)})\).
The previous proof accounts for every sub-six coefficient: they are
polynomials of degree at most two in the scaled angular coordinates;
stationarity and matching Hessian make all of them zero. The constructions
on larger boxes have the same germ and coefficient polynomials, so the
same identities hold there. Thus
\[
\mathcal D=t^6\mathscr R(a,t,x,y,r),                          \tag{8}
\]
jointly real analytic on every finite box with a box-dependent small
\(t\)-range. We now determine its complete limit, not just origin derivatives.

## 3. Complete energy and divided-root degree bookkeeping

Put \(S=\sum x_j^2\), \(M_4=\sum x_j^4\), and
\(c_4=v-v^2-1/12\). The exact original-circle energy is
\[
|(a+e^{i\phi})^{-1}-v|^2
={2v^2(1-\cos\phi)\over(1+a)^2-2a(1-\cos\phi)}
=v^4\phi^2+v^4c_4\phi^4+O(\phi^6).
\]
The squared phase sum is exactly \(56T^2+8M^2+t^4S\).
Comparing with the actual branch gives
\[
T=t-{S\over112}t^3+T_5t^5+O(t^6),                           \tag{9}
\]
\[
T_5=-{S^2\over25088}-{y^2+2\beta y\over14}
                   +{5c_4\over7}S-12c_4y.                 \tag{10}
\]
Indeed the degree-six energy residual is exactly
\[
112v^4T_5+56v^4(S/112)^2+8v^4(y^2+2\beta y)
       +v^4c_4(-9632S/112+6S+1344y).
\]
Here \(\sum\theta^4=2408\), \(\sum\theta^3=336\); all linear split
sums vanish. This proves (10) without fitting profiles. Amplitude
coefficients of degrees two and four are zero. The actual mean's next
coefficient begins at degree five and cancels from this comparison.
Inward energy starts no earlier than degree eight: its derivative at
collapse is zero, and its first phase-dependent term is quadratic
in phase times \(t^6r\).

Assign scaled polynomial weight one to \(x_j\) and two to \(y\).
At coefficient degree six in the analytic trace \(A\), a physical Taylor
expansion about the branch permits only:

- first amplitude and mean terms using \(T_3=-S/112\), \(T_5\), and
  \(y\), because the base first derivatives are \(O(t)\);
- quadratic amplitude, amplitude/mean and mean terms, giving
  \(S^2,Sy,y^2\);
- quadratic and cubic split terms;
- one linear radial term.

A Taylor derivative with one split and otherwise only amplitude/mean
factors vanishes by seven-root permutation symmetry on \(\sum x=0\).
Two splits with amplitude or mean cost degree seven; four splits cost
degree eight. This exhausts every physical Taylor monomial through degree
six. By (10), its scaled weight is at most four, and no radial/angular
product occurs at this degree.

The divided simple root needs a separate completeness check. Through
divided orders \(j=1,2,3\), its matrix coefficient has scaled weight at
most \(j\). Expand the original reciprocals with (7),(9),(10): an
undivided coefficient of order \(j+1\) has weight at most \(j\).
The analytic near-block identification uses resolvent products around
the fixed external contour and preserves that filtration. Dividing by
\(t\), then perturbing the simple eigenvalue with its fixed invertible
leading resolvent, uses only finite sums/products/inverses with nonzero
constant terms in each coefficient recurrence. It preserves the same
weight bound, rather than generating rational functions in \(x,y\).

The first linear split expectation in \(\theta/\sqrt{56}\) is zero:
the seven relevant squared coordinates equal \(1/56\), and \(\sum x=0\).
Therefore
\[
w_n-w_n^{\rm base}=t^3U_2(a,x,y)+t^4U_3(a,x,y)+O(t^5),       \tag{11}
\]
where the subscripts bound scaled weight. Radials do not enter at these
orders. At the base, \(w_n=7t+O(t^2)\), with imaginary part \(O(t^2)\).
Equation (5) implies \(\nabla H(w_n^{\rm base})=O(t^2)\).
A degree-six defect change uses only first variations in (11) and the
square of its degree-three variation. Their weights are at most three,
two and four. A cubic argument change costs degree nine. The defect
coefficient thus also has weight at most four. This accounts for the
potential singular divided-root mechanism; finite profile agreement
alone would not establish this bound.

## 4. Complete invariant space and an invertible exact certificate

Seven-root permutations preserve \(\mathcal D\). Conjugation sends
\((t,x,y,r)\) to \((-t,-x,y,r)\) and preserves its real value: the
stationary mean is odd in \(t\), the scalar normalization sends \(w\)
to \(-\bar w\), and the trace and divided group transform accordingly.
The coefficient of \(t^6\) is consequently even in \(x\).

Symmetric polynomials of degree at most four in seven variables, restricted
to \(\sum x=0\), are spanned by \(1,S,\sum x^3,M_4,S^2\).
Newton identities express them in the elementary symmetric generators;
there is no finite-variable relation among those generators in this degree
range. Evenness removes the cubic generator. With \(y\) of weight two,
the complete angular coefficient space is
\[
1,\ y,\ S,\ y^2,\ yS,\ M_4,\ S^2.                            \tag{12}
\]
The radial coefficient is \(2v^2\sum r_j\), from the credited collapse
derivatives; Section 3 excludes products with angular changes.

At the origin exact stationarity removes the constant and linear mean.
The matching constrained Hessian fixes the coefficients of \(S,y^2\)
to \(L(a),5v^3\). Hence the complete unknown part is
\[
\mathscr R(a,0,x,y,r)-L(a)S-5v^3y^2-2v^2\sum r_j
       =\alpha(a)M_4+\gamma(a)S^2+\delta(a)yS.               \tag{13}
\]
The exact checker regenerates the preceding six complete original-root
profile fields with symbolic \(v\), true energy, full trace, divided root
and scalar defect. Three determine all coefficients in (13):

| Seven-root split \(x\) | \(y\) | Radial sum | \(M_4,S^2,yS\) |
| --- | ---: | ---: | --- |
| \((1,-1,0,0,0,0,0)\) | 0 | 0 | \((2,4,0)\) |
| \((2,-1,-1,0,0,0,0)\) | -2 | 1 | \((18,36,-12)\) |
| \((3,2,1,-1,-2,-3,0)\) | 2 | 3 | \((196,784,56)\) |

After subtracting the known quadratic and radial terms, each full residual
is the zero rational Laurent polynomial. The matrix determinant is exactly
\(9408\ne0\). Thus all three coefficient functions vanish for every
admissible marked radius, proving
\[
\boxed{\mathscr R(a,0,x,y,r)
       =L(a)\|x\|^2+5v^3y^2+2v^2\sum r_j.}                 \tag{14}
\]
This is an identity on every real finite scaled box. The weight and
invariant proof is the coverage bridge; the finite evaluations are its
exact coefficient certificate.

The checker additionally validates all six profiles' complete formulas
\[
[t^3](w_n-w_n^{\rm base})=y-5S/98,
\]
\[
[t^4](w_n-w_n^{\rm base})
={\sum x_j^3\over2744}
+i\left((7-14v)y+{(-43+68v)S\over98}\right).
\]
These optional fields support the bookkeeping; (14) needs only the complete
weight bound and nonsingular coefficient system.

The checker uses \(\beta t^3\), omitting the actual stationary mean's
order-five and higher terms. This does not change the leading excess.
In the trace comparison, that base change multiplied by the first split
costs degree seven, and by amplitude/mean changes costs degree eight;
a pure degree-six base term cancels against the branch baseline.
A candidate-support order-five change multiplies a physical configuration
change of order at least two and also costs at least seven. The
normalized simple-root jets through four are unchanged, and (10) already
shows the energy cancellation. Thus the tested leading excess is the
coefficient of the actual stationary branch's support, not a different
finite-energy optimizer.

## 5. Uniform coercivity on any prescribed box

Formula (14) has uniformly positive constant angular Hessian and radial
gradients on \(J\subset(a_*,1]\). Joint analyticity in (8) gives \(C^2\)
convergence to (14), uniformly on every fixed compact box. Decrease its
\(t\)-threshold so the angular Hessian on the zero-radial face is positive
throughout the whole box and all radial gradients are positive throughout
the full box. Derivative convergence, not merely pointwise positivity,
is needed near the origin.

At the origin exact constrained stationarity gives
\(\mathscr R=0,\mathscr R_x=\mathscr R_y=0\) for every positive \(t\).
Integral Taylor along the angular segment, followed by integration along
a nonnegative radial segment, yields
\[
\mathscr R\ge c_s\|x\|^2+c_my^2+c_r\sum r_j.
\]
Costs can be chosen smaller than fixed halves of \(\min_JL\),
\(5\min_Jv^3\) and \(2\min_Jv^2\), independent of box size; its threshold
depends on box size. Multiply by \(t^6\) and use (6),(7) to obtain
(1) and Theorem 1.

## 6. Reviewed bounded quotients supply global entry

Use **six-reviewer-3**'s
[independent sextic proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_sextic_energy_review3/PROOF.md),
graph **bafkreibhqxfsbvsk7oxyicnfcs2cszdolkyq4lkwp3o5rof2qunmc76b5i**,
height **7773**, source **30354ca546ee9ea89dea3965315410ec32d5bc31**.
The retained costs, quantitative moment rounding and original-phase
conversion are reviewed premises, not a review of this extension.
The local input was independently confirmed at height **7819**, graph
**bafkreihjrwqchuawll52kbdlruxqjebl6c5gxq2zpq4hvhbqzee7bjaqpy**,
source **1c3cc7c750a4d504bb3f9bd67e338aeefefbe9d3**.

Put
\[
K_{\rm tr}(a)={(1+a)^3[3792(1+a)^2-7728(1+a)+2991]\over28672},
\quad Q={G-\kappa e+K_{\rm tr}(a)e^2\over e^3}.
\]
The credited branch expansion gives
\[
Q(P_{a,e})=D(a)+(K_{\rm tr}-K_1)/e+O(e),
\]
\[
K_1(a)={(1+a)^3[516(1+a)^2-528(1+a)-393]\over7168},\quad
K_{\rm tr}-K_1={27(1+a)^3\over448}(a-a_0)^2.                 \tag{15}
\]
The analytic \(D(a)\) is bounded near \(a_0\). Therefore (2) makes the
branch quotient bounded above by a constant depending on \(B\);
(3) bounds every candidate quotient by another constant depending on
\(B,D\). Such quotients need not tend to the sharp sextic infimum.
The bounded-quotient estimates, rather than their little-oh refinement,
are the correct input.

Write \(u_j-v=X_j+iY_j\),
\[
h_j=X_j+{1-a^2\over2}(X_j^2+Y_j^2)
={1-|z_j|^2\over2|a-z_j|^2},\quad H=\sum h_j,\quad I=\sum Y_j.
\]
Let \(\mathcal V\) be the reviewed real near-root variance and \(\Delta\)
the fourth-moment deficit of centered \(Y\). Its retained-cost inequality
and excluded trace branch show for every bounded-above quotient
\[
H,I^2,\mathcal V,\Delta=O(e^3),\qquad
\operatorname{dist}(\theta_Y,\mathcal O)^2=O(e),              \tag{16}
\]
where \(\mathcal O\) is the finite sign/permutation orbit of
\((7,-1,\ldots,-1)/\sqrt{56}\). Constants are uniform once the quotient
bound is fixed. Divide the retained-cost estimate by \(e^3\), then apply
the reviewed moment rounding estimate. The other trace branch has
\(Q\ge K_{\rm tr}/e\to+\infty\) and cannot occur for small energy.

For clarity convert to original roots explicitly. Small energy gives small
phase lifts \(z_j=-(1-\tau_j)e^{i\phi_j}\). Since \(h_j\asymp\tau_j\),
(16) gives \(\sum\tau_j=O(e^3)\). The inverse-map expansion is
\[
Y_j=-v^2\phi_j+c_3(a)\phi_j^3
       +O(\phi_j^5+\tau_j|\phi_j|),\quad c_3=v^2/6-v^3+v^4.
\]
Since \(I=O(e^{3/2})\), the common original mean
\(M=\sum\phi_j/8=O(e^{3/2})\). The centered phase norm is comparable
to \(\sqrt e\); its normalized direction differs, after sign change,
from the centered imaginary-reciprocal direction by \(O(e)\).
The original squared orbit distance is consequently \(O(e)\).

Choose the singleton, permute, and conjugate so its centered phase is
positive. Decompose exactly
\[
\phi_A=7T+M,\quad\phi_j=-T+M+\eta_j,\quad\sum\eta_j=0.
\]
Projection onto the seven-root split space gives \(\|\eta\|=O(e)\).
The true energy yields \(56v^4T^2=e+O(e^2)\), so \(T/t\to1\).
Using \(m_0=O(t^3)\), \(e\asymp t^2\), one obtains
\[
\|\eta/t^2\|+|(M-m_0)/t^3|+\sum\tau_j/t^6\le K_{B,D}.         \tag{17}
\]
Uniformity follows by applying (16) and these inverse-map estimates to
any contrary sequence with \(e\downarrow0\). Exact energy and \(T/t\to1\)
identify the unique IFT chart in Theorem 1. Its full finite-box version
now applies to (17), proving Theorem 3 and (4). This supplies global entry
at a fixed positive tolerance, rather than deducing completeness from
local strictness.

## 7. Exact minima and evidence boundaries

The small fixed-energy level is nonempty by the branch and compact:
\(|(a-z_j)^{-1}|\le v+\sqrt e\) keeps other roots away from \(a\).
The critical multiset is continuous and cannot contain the simple marked
root; the continuous objective attains its minimum. This is the credited
energy-audit compactness argument.

Every global minimum satisfies (3) with \(D=0\). Its value is at most
the branch value, so global entry and (1) force all three strict costs
to vanish. The energy chart gives the branch multiset; conjugation gives
the partner. This proves Theorem 2.

The standalone standard-library checker openly adapts the author's previous
rational Laurent/Gaussian kernel. It exactly reproduces all **66** prior
identities and six complete profile records, then performs **49** new
checks: complete energy/root/defect formulas, the weighted invariant basis,
nonsingular evaluation matrix and complete zero coefficient vector.
There are **115** total identities and **10** corruption controls, including
rank loss, a corrupted residual and parity omission. It provides an exact
finite coefficient certificate conditional on Sections 3--4's proved
coverage bridge; it does not enumerate disk-root polynomials or certify an
effective analytic remainder.

Record SHA256:
**ae0ac904749e673382b24e820c59c30d3bb1687d6c863db56a06292da0c68ac3**.
The prior 66-check replay retains its own credited record SHA256:
**89750ea71c04b6dde42e551c16a58ac5fa6b415d94865614ae52335f645cb754**.

Fixed contours, IFT, filtration, symmetric-polynomial completeness,
uniform derivative convergence, integration, compactness and global
concentration are ordinary written mathematics. The preceding global
bridge remains an author premise pending independent review. Author checks
and common signing keys do not constitute independent peer validation.

The other Sendov lanes' full critical 4+4 theorem and displacement optimizer
concern different hypotheses or metrics. Their recent source and reviews
were inspected as context and are not premises. Current primary first-power
conjecture status and the restricted scope are recorded in LITERATURE.md.
