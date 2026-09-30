# Independent finite-energy variation audit and the stability-curve slope

Actual author **six-reviewer-3**, role **independent mathematical reviewer**,
2026-09-30. This is ordinary written mathematics with independent exact
algebra evidence. Shared signing identity does not establish separate
authorship. The local-minimum theorem being audited is due to researcher
**six-sendov-3**; the first stability-curve correction below is derived in
this audit. No proof assistant, numerical proof input or enumeration is used.

## 1. Exact statement and parameter conventions

Let the marked root \(a\in[0,1]\) be simple and fixed, and let
\[
p(z)=c(z-a)\prod_{j=1}^{8}(z-z_j),\qquad c\ne0,\quad |z_j|\le1.
\]
Count every original and critical multiplicity algebraically. Put
\[
v=(1+a)^{-1},\quad E=\sum_{j=1}^{8}|(a-z_j)^{-1}-v|^2,
\quad F=\sum_{p'(\zeta)=0}|a-\zeta|^{-1},\quad G=F-16v.
\]
Simplicity of \(a\) excludes a critical point at \(a\), so all sums are
finite here. A nonreal marked root is first rotated to the positive real
axis; the same rotated-coordinate energy and assertion then apply.
Polynomials differing by a nonzero scalar and permutations of roots
represent the same configuration for strictness.

Write
\[
P(t,m;z)=(z-a)(z+e^{i(7t+m)})(z+e^{i(-t+m)})^7,
\quad \beta(v)=\frac{392-1197v+945v^2}{20}.
\]
The audited theorem gives an analytic fixed-energy stationary branch
\(m=w(a,e)t^3\), \(w=\beta+O(e)\), \(E(P)=e>0\),
\(t^2=e/(56v^4)+O(e^2)\). It is a strict local minimum under *every*
disk-root motion at the same \(a,e\) for any compact
\(J\subset(a_*,1]\) and uniformly sufficiently small positive energy,
where
\[
a_*=(10\sqrt{2198}-225)/404,
\quad L(v)=\frac{v^3(1616-1432v-1859v^2)}{224}.
\]
Below \(a_*\) it is an angular saddle at small energy. The neighborhood
of each configuration can depend on \(a,e\). The theorem is local and
does not classify global minimizers.

This audit confirms that statement and proves the additional expansion
\[
\ell(a,e)=L(v)+\frac{R(v)}{56v^4}e+O(e^2),                 \tag{1}
\]
where the zero-sum angular quadratic coefficient is \(t^2\ell(a,e)\) and
\[
R(v)=\frac{8056}{105}v^3-\frac{403051}{840}v^4
       +\frac{2175821}{1680}v^5-\frac{26103}{16}v^6
       +\frac{2550985}{3584}v^7.                         \tag{2}
\]
In a neighborhood of \((a_*,0)\), the analytic transition therefore is
\[
a_{\rm st}(e)=a_*+C_*e+O(e^2),\qquad
C_*=-\frac{4R(v_*)}{v_*^9(1432+3718v_*)},               \tag{3}
\]
\[
v_*=(40\sqrt{2198}-716)/1859,\qquad
\frac{15503}{125000}<C_*<\frac{4961}{40000}.
                                                                  \tag{4}
\]
These are exact rational bounds, equivalently \(0.124024<C_*<0.124025\).
In particular the branch at the *limiting* marked radius \(a=a_*\)
is a saddle for every sufficiently small positive energy. The actual
neutral curve \(a=a_{\rm st}(e)\) itself remains unclassified.

## 2. Stationarity, local coordinates and coverage

Put \(A=-e^{i(7t+m)}\), \(B=-e^{i(-t+m)}\), and
\(u_A=(a-A)^{-1}\), \(u=(a-B)^{-1}\). Differentiating the original
polynomial and removing \((z-B)^6\) gives
\[
Q(z)=9z^2-[8(a+A)+2B]z+B(a+A)+7aA.
\]
At \(t=m=0\), its simple roots are \(-1\) and
\(a-(9v)^{-1}\). The implicit function theorem supplies the simple
branches, with positive-real reciprocal constants \(v,9v\). Hence
\(F=6|u|+|q_n|+|q_f|\) and the family energy are analytic.

The generic quartic is credited to the preceding energy-basin result:
\[
\kappa=(1+a)(a-5/8),\quad
K_1(a)=(516v^{-5}-528v^{-4}-393v^{-3})/7168.
\]
Independent original-coordinate root recursion gives, for \(h=t^2\)
and \(m=wt^3\),
\[
E=56v^4h+O(h^2),\qquad
G=\kappa E-K_1E^2+h^3[P_0(v)+P_1(v)w+5v^3w^2]+O(h^4),
\]
\[
P_0=931v^3/2+15897v^4/8-168525v^5/32-9639v^6/8
                              +678993v^7/128,
\quad P_1=-196v^3+1197v^4/2-945v^5/2.
\]
The weighted order of \(m\) is three, so the complete sixth coefficient
has degree at most two in \(w\). Four rational values determine and
independently check it; this is not a sampling inference about arbitrary
configurations. These fields agree with the author’s complete coefficient
polynomials.

The analytic energy inverse \(h=H(a,e,w)\) exists because
\(E_h(a,0,w)=56v^4>0\). After subtracting \(\kappa e-K_1e^2\) and
dividing by \(e^3\), the removable quotient has a strictly positive
\(w\)-Hessian at its unique nearby minimum \(w=\beta(v)\).
Another implicit function theorem gives the actual \(w(a,e)\).
The derivatives stay nonzero on the compact interval \([0,1]\), so local
solutions patch uniquely with a common positive energy threshold.

At fixed energy, \(m_w=t^3(1+O(t^4))\); consequently the physical
mean second derivative is \(10v^3+O(e)\). Permutation symmetry kills
the first derivative of every zero-sum seven-block angular variation.
The energy gradient in the balanced physical \(t\)-direction is
\(E_t=112v^4t+O(t^3)>0\). Thus the branch is stationary in all eight
circle angles subject to its one energy constraint.

For fixed positive \(t\), the singleton and repeated block are distinct.
Every sufficiently nearby root multiset can be labeled with that singleton
and expressed uniquely in local phase lifts as
\[
z_A=-(1-\tau_A)e^{i(7\widetilde t+\widetilde m)},\quad
z_j=-(1-\tau_j)e^{i(-\widetilde t+\widetilde m+\eta_j)},
\quad \sum\eta_j=0,\quad \tau_A,\tau_j\ge0.
\]
The energy equation eliminates \(\widetilde t\). This covers independent
inward motion, common angular means and all six zero-sum split directions;
there is no real-coefficient or two-block restriction on the perturbation.

## 3. Why the critical collision causes no omitted direction

The self-contained determinant identity for the classical reciprocal
matrix is
\[
N=\operatorname{diag}(u_j)(I+\mathbf1\mathbf1^T),\quad
\det(qI-N)=9\prod(q-u_j)-q\frac{d}{dq}\prod(q-u_j).
\]
It also equals \(q^8p'(a-q^{-1})/p'(a)\). These are identities in
the polynomial coefficients and include all multiplicities. The
Cheung–Ng companion representation and spectral calculus are classical.

For positive small \(t\), the six-dimensional subspace with singleton
coordinate zero and sum of block coordinates zero has scalar eigenvalue
\(u\), and its real orthogonal projector \(P_B\) commutes with \(N\).
The remaining two reciprocal eigenvalues satisfy
\(q^2-(2u_A+8u)q+9u_Au=0\). Evaluation at \(q=u\) gives
\(7u(u_A-u)\ne0\). Thus the sixfold cluster is semisimple and isolated
from both other eigenvalues. Its external gap may shrink with energy;
the proof never assumes an internal gap or a uniform external gap.

For nonzero \(q_0,c\), define a holomorphic primitive near zero by
\[
f(0)=|q_0|,\qquad
f'(w)=\frac{c(\bar q_0+\bar c w)}
             {\sqrt{(q_0+cw)(\bar q_0+\bar c w)}}.
\]
The square root has positive constant \(|q_0|\). If
\(D(x,y)=|q_0+c(x+iy)|-\Re f(x+iy)\), direct differentiation gives
\(D(x,0)=D_y(x,0)=0\). Harmonicity of \(\Re f\) and
\(D_{xx}(x,0)=0\) give
\[
D_{yy}(x,0)=\Delta|q_0+cw|=|c|^2/|q_0+cx|>0.
\]
Taylor’s integral remainder therefore proves locally
\(c_0y^2\le D(x,y)\le C_0y^2\). This is a lower support on a
neighborhood, not merely a formal jet inequality.

A fixed external contour constructs the analytic Riesz projector of the
cluster. The intertwiner
\(T(s)=\Pi(s)P_B+(I-\Pi(s))(I-P_B)\) is the identity at zero and
invertible nearby. Conjugation gives the analytic cluster block
\(uI+cW(s)\), with \(c=iBu^2\), \(W(0)=0\). The compressed first
variation is unaffected by the intertwiner commutator, because the
background block is scalar. The power series of \(f(W)\) converges in a
small operator-norm neighborhood and its trace equals the sum of the
values on eigenvalues, even for defective blocks.

Consequently
\[
\Phi(s)=\Re\operatorname{tr}f(W(s))+|q_n(s)|+|q_f(s)|
\]
is real analytic, \(\Phi\le F\), and \(\Phi(0)=F(0)\).
The difference is \(O(\|s\|^2)\), so every first derivative of \(F\)
at the base exists and matches \(\Phi\).

For arbitrary *pure angular* perturbations the first derivative of \(W\)
is a real symmetric compression of the seven angular increments. Hence
\(\Im_{\rm Herm}W=O(\|s\|^2)\). If \(Wx=\lambda x\), then
\(\Im\lambda=x^*(\Im_{\rm Herm}W)x/(x^*x)\), without any normality
assumption. Every cluster eigenvalue has imaginary part \(O(\|s\|^2)\),
so the scalar support bound gives \(F-\Phi=O(\|s\|^4)\) on angular
motions. Therefore their angular quadratic forms agree. This establishes
the required collision-safe Hessian without assuming that \(F\) is twice
differentiable on a neighborhood of all mixed motions.

## 4. Independent paired-quartic reconstruction of the curvature

Split two of the seven equal roots by phases \(\epsilon,-\epsilon\).
Their squared zero-sum norm is \(S=2\). Directly from the original
polynomial,
\[
p_\epsilon'(z)=(z-B)^4
 [D_0(z)+\epsilon^2D_2(z)+O(\epsilon^4)],
\]
\[
D_0(z)=(z-B)^2Q(z),\quad
D_2(z)=(z-B)f'(z)+5f(z),\quad f(z)=Bz(z-a)(z-A).
\]
Normalize and substitute reciprocals:
\[
K_0(q)=q^4D_0(a-q^{-1})/D_0(a),\quad
K_2(q)=q^4D_2(a-q^{-1})/D_0(a)-K_0(q)D_2(a)/D_0(a).
\]
Then \(K_0=(q-u)^2(q-q_n)(q-q_f)\), and the simple reciprocal
second coefficients are
\[
d_n=-K_2(q_n)/K_0'(q_n),\qquad d_f=-K_2(q_f)/K_0'(q_f).
\]
The quartic’s monic coefficient of \(q^3\) gives the *total* second
trace. Subtracting \(d_n+d_f\) reconstructs the colliding cluster trace,
without the author’s cluster-residue formula. Its two nonzero first split
deviations have squared value
\[
-K_2(u)/[(u-q_n)(u-q_f)]=\frac57(iBu^2)^2.
\]
The full compression quadratic identity is
\[
\operatorname{tr}(P_B\operatorname{diag}(\eta)P_B)^2
       =\frac57\sum\eta_j^2+\frac1{49}(\sum\eta_j)^2.
\]
Thus the paired calculation applies to every zero-sum direction by
permutation invariance, not by finite directional testing.

For \(c=iBu^2\), its scalar cluster modulus curvature per \(S\) is
\[
\frac5{14}\left(\frac{|c|^2}{|u|}
                 -\frac{\Re(c\bar u)^2}{|u|^3}\right).
\]
Add the projection of the cluster second trace and the two simple shifts
to obtain \(\mathcal F_2\). For original-root angular derivatives
\(u'=iBu^2\), \(u''=-Bu^2-2B^2u^3\), the energy coefficient is
\[
\mathcal E_2=|u'|^2+\Re[(u-v)\overline{u''}].
\]
Solving the energy equation to second order subtracts the physical
multiplier: \(\mathcal H=\mathcal F_2-(F_t/E_t)\mathcal E_2\).
Both the cluster modulus curvature and this energy correction are
necessary; omitting either is not the audited quadratic form.

The independent checker obtains \(F_t,E_t\) by differentiating the
original residual at **fixed physical \(m\)**: \(A_t=7iA\),
\(B_t=-iB\), \(r_t=-Q_t(r)/Q_z(r)\), \(q_t=q^2r_t\).
It separately verifies agreement through order four with the derivative
along \(m=\beta t^3\). This avoids mistaking a surrogate-path derivative
for the constrained physical multiplier.

All lower Laurent coefficients cancel, and the complete leading polynomial
is \(L(v)\). At \(m=\beta(v)t^3\) the complete next polynomial is
\(R(v)\) in (2):
\[
\mathcal H(a,t,\beta t^3)=L(v)t^2+R(v)t^4+O(t^6).        \tag{5}
\]
The coefficient calculation is exact in \(\mathbb Q[v,v^{-1}]\), not
interpolation in \(v\). Input order ten supplies the reported sixth-order
mean and fourth-order curvature: division loses at most two \(t\)-orders,
while the simple original residual derivative has nonzero constant.
Recomputing with input order twelve gives identical complete coefficients.
The optional residue comparison uses the pinned author’s distinct original
residue/discriminant route at order twelve; both full \(t^4\) polynomials
agree. That secondary calculation is labeled as author-kernel reuse.

## 5. From the local Hessian to all-disk strictness

The two near-cluster trace terms have opposite apparent simple poles.
Their total trace is analytic, and the difference of their modulus
directions is \(O(t)\); consequently the apparent pole in
\(\mathcal F_2\) cancels. This is a removable analytic singularity in
\((a,t,m)\), including small nonzero common means. Also \(F_t,E_t\)
are divisible by \(t\) at fixed \(m\), and \(E_t/t\ne0\) nearby.
Thus \(\mathcal H\) is analytic. Conjugation gives
\(\mathcal H(a,-t,-m)=\mathcal H(a,t,m)\).

The inward derivatives of the touching support match those of \(F\).
Permutation symmetry reduces each repeated-block derivative to one seventh
of its common-block derivative. At collapse the direct original-root
calculation gives \(F_{\tau_j}=2v^2\), \(E_{\tau_j}=0\).
Analytic two-block derivatives and conjugation yield uniformly
\[
(F-\lambda E)_{\tau_j}=2v^2+O(e)>0,
\quad \lambda=F_t/E_t.
\]
This applies also at \(a=1\), because the marked root stays fixed.

In the energy chart, permutation symmetry removes the mixed Hessian of
the mean with the zero-sum block. The angular quadratic form is
\[
(5v^3+O(e))(\widetilde m-m)^2+t^2\ell(a,e)\sum\eta_j^2.
\]
On compact \(J\subset(a_*,1]\), its two coefficients have uniform
positive lower bounds after taking small enough energy. Taylor expansion
of the *analytic support* absorbs every mixed term containing an inward
depth into its positive linear derivative, by shrinking the neighborhood
for each \(a,e\). It absorbs the angular Taylor remainder into the
positive quadratic form. It therefore proves
\[
F(p)-F(P_{a,e})\ge c_r\sum\tau_j+c_m(\widetilde m-m)^2
                          +c_st^2\sum\eta_j^2.
\]
The constants can be uniform on \(J\); the neighborhood radius need not
be. Equality forces the same root multiset, because all retained terms
are nonnegative and vanish only at the branch. If the transverse sign
is negative, the paired constrained split decreases \(F\), while the
mean direction increases it. That gives a saddle, not a mere failure of
this sufficient proof.

## 6. Exact first correction of the transition

The true stationary mean differs from \(\beta t^3\) by \(O(t^5)\).
Analyticity and simultaneous conjugation imply
\(\partial_m\mathcal H(a,0,0)=0\), hence
\(\partial_m\mathcal H=O(|t|+|m|)\). Replacing the approximate mean by
the true one consequently changes \(\mathcal H\) by \(O(t^6)\).
Thus (5) has the same fourth coefficient on the true branch. Dividing by
\(t^2\) and substituting \(t^2=e/(56v^4)+O(e^2)\) proves (1).
All functions here are analytic near the transition, so these remainders
are uniform in a sufficiently small marked-radius neighborhood.

The positive root \(v_*\) of \(1859v^2+1432v-1616=0\) corresponds
to \(a_*\). At that point,
\[
\frac{d}{da}L((1+a)^{-1})
       =\frac{v_*^5(1432+3718v_*)}{224}>0.
\]
Implicit differentiation of \(\ell(a_{\rm st}(e),e)=0\) proves (3).
For a compact exact sign certificate, the checker isolates \(v_*\) by
\[
\frac{718987220224932689}{1152921504606846976}<v_*<
\frac{1437974440449865379}{2305843009213693952}.
\]
The quadratic has opposite strict signs at these endpoints and is strictly
increasing there. Fraction interval operations on the full polynomial
\(R\) and positive denominator in (3) prove (4), with no floating
rounding. In particular \(R(v_*)<0\), so (1) at \(a=a_*\) is strictly
negative for small positive energy. The positive mean curvature gives the
claimed saddle. No higher angular classification on the moving neutral
curve follows.

## 7. Evidence and mathematical boundaries

Python 3.11.2 standard library; independent checker imports no author,
campaign, solver or CAS module. It has 328 exact identities at input
order ten, 352 at order twelve, complete required fixtures, exact polynomial
comparison, a direct physical-multiplier check, all 49 compression
coefficients, and rational stability-slope bounds. Its arithmetic design
openly adapts this reviewer’s earlier exact checkers; simple-root recursion
and coefficient-trace reconstruction supply the new independent route.

The author’s 109-control fixture was reproduced separately. The optional
residue checker reads only the hash-pinned original source and supplies a
secondary comparison, not independent-author evidence. The ordinary
implicit-function, support inequality, Riesz-block, coverage, uniformity
and Taylor arguments above remain outside a formal proof kernel. Matching
formal coefficients alone would not prove those analytic steps.

The audit supplies no numerical energy threshold, effective local radius,
global fixed-energy minimizer classification, global outward-motion theorem,
unrestricted first-power endpoint or historical-priority proof. Prior
quartic/sextic basin results retain attribution; their universal moment and
coercivity theorems are not assumptions of this local proof. Turning their
asymptotic near-minimizer geometry into a uniform quantitative entry into
these shrinking neighborhoods remains a separate lemma.
