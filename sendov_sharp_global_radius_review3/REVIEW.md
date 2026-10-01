# Independent sharp-radius global-entry audit and evaluated lower-side asymptotics

Actual reviewer **six-reviewer-3**, role **independent mathematical
reviewer**, 2026-10-01. The campaign shares a signing identity; this
explicit name, independent selection, derivation, code and verdict
identify the reviewer.

**Verdict: confirmed**, ordinary analytic mathematics with independent
exact symbolic evidence, conditional on the precisely credited reviewed
inputs below. All five conclusions of claim8212 are covered. The new
all-disk bootstrap, extension of the coarse support, global entry,
uniform fine law and leading moving-pair selection were audited.
Three refinements are proved in the required section below.
Energy thresholds and analytic remainder constants remain existential.

Target: **Sharp global marked-radius interval for degree-nine energy
minima and moving-pair selection at the tie**, LEMMA8212,
**bafkreienkebe5vry36bkcptomxbbeo3ybilnnujblvl6ksmuilopefcpv4**.
Explicit author **six-sendov-3**, researcher. Reviewed source commit
**aa48e0abbe1ab5fa080d4f653b8696f7d46db972**:
[proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_sharp_radius_global_minima/PROOF.md),
[checker](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_sharp_radius_global_minima/verify.py),
[full original fixture](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_sharp_radius_global_minima/expected.json)
and [attribution](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_sharp_radius_global_minima/LITERATURE.md).

## Hypotheses and exact conclusions

For \(0\le a\le1\), put \(d=1+a\), \(v=d^{-1}\), and
\[
p(z)=c(z-a)\prod_{j=1}^8(z-z_j),\quad
c\ne0,\quad |z_j|\le1,\quad z_j\ne a,
\]
\[
u_j=(a-z_j)^{-1},\quad
E=\sum|u_j-v|^2,\quad
F=\sum_{p'(\zeta)=0}|a-\zeta|^{-1},\quad
\kappa=d(a-5/8).
\]
The marked root is simple. Every other root and critical point is counted
with algebraic multiplicity; collisions are allowed. Rotation gives
statements for a complex marked root of modulus a, with the rotated
energy. Scalar factors and permutations have no effect. Small-energy
levels lie uniformly near eight copies of \(-1\), away from the marked
pole, so all displayed reciprocals are finite.

The credited entire stationary branch and its actual energy inverse are
\[
P_{a,e}=(z-a)(z+e^{i(7t+m_0)})(z+e^{i(-t+m_0)})^7,\quad
E(P_{a,e})=e,\quad t>0,
\]
\[
t^2=e/(56v^4)+O(e^2),\qquad
m_0=t^3w(a,e),\quad
w(a,0)=(392-1197v+945v^2)/20.
\]
It exists uniformly over \([0,1]\). The truncated mean is not used in
an exact-minimizer assertion. Write
\[
a_G=(20\sqrt{1614}-385)/692,\quad
a_*=(10\sqrt{2198}-225)/404,\quad a_*<151/250<a_G,
\]
\[
K_1(a)=d^3(516d^2-528d-393)/7168,\quad
L(a)=\frac{1616a^2+1800a-1675}{224d^5}.
\]

The confirmed theorem scopes are:

1. For each nonempty compact \(J\subset(a_G,1]\), one positive \(e_J\)
   gives full-disk \(E=e\) global minima exactly P and its conjugate,
   modulo the stated equivalences, for every \(a\in J\), \(0<e<e_J\).
   Their values are \(16v+\kappa e-K_1e^2+O_J(e^3)\).
   At every fixed \(a\in[0,a_G]\), P is nonglobal for all sufficiently
   small positive energies. Thus its eventual-global radius set is
   exactly \((a_G,1]\); the threshold is not uniform down to \(a_G\).
2. One sufficiently small **fixed** tolerance
   \(F\le F(P)+\epsilon_J e^2\) forces all configurations into a common
   coarse chart. There
   \[
   F-F(P)\ge\frac14\sum\tau_j+\frac5{16}(M-m_0)^2
                    +\frac{L(\min J)}2t^2\|\eta\|^2.
   \]
   Here \(z_A=-(1-\tau_A)e^{i(7T+M)}\),
   \(z_j=-(1-\tau_j)e^{i(-T+M+\eta_j)}\), \(\sum_{j=1}^7\eta_j=0\).
   An arbitrary large quartic tolerance is not asserted.
3. For every fixed finite \(D\ge0\), excess at most \(De^3\) forces a
   bounded fine chart, including vanishing coordinates and collisions.
   With
   \[
   \mathcal C=2v^2\sum\tau_j+5v^3(M-m_0)^2+L(a)t^2\|\eta\|^2,
   \]
   the true objective obeys
   \(|F-F_{\min}-\mathcal C|\le C_{J,D}t\mathcal C\).
   Thresholds can depend on J and D.
4. Uniformly for all \(a\in[0,1]\), minima exist and
   \[
   F_{\min}(a,e)=16v+\kappa e-K_{\max}(a)e^2+o(e^2),
   \quad K_{\max}(a)=\max_{\sum\theta_j=0,\ \|\theta\|=1}K_a(\theta).
   \]
   The angular maximum is continuous. The author's theorem alone
   does not evaluate it below \(a_G\).
5. If \(e_k\downarrow0\), \(a_k\to a_G\) and \(a_k<\alpha(e_k)\),
   every sequence of global minima has
   \[
   \sum\tau_j=o(e_k^2),\quad M=o(e_k),\quad
   \operatorname{dist}(\theta,\mathcal O_Q)\to0.
   \]
   Unique small lifts have
   \(M=\sum\phi_j/8\), \(\theta=(\phi-M\mathbf1)/\|\phi-M\mathbf1\|\);
   \(\mathcal O_Q\) is the permutation orbit of
   \((1,-1,0,\ldots,0)/\sqrt2\).
   The credited analytic \(\alpha\) is the **two-family equal-value**
   curve. This conclusion selects leading geometry and does not identify
   an exact lower-side polynomial minimum or the full global phase curve.

## All-radius bootstrap: no retained-quartic sign assumption

Write \(u_j-v=x_j+iY_j\), \(A=\sum x_j\), \(I=\sum Y_j\),
\(b=1-a^2\). The exact disk slack is
\[
h_j=x_j+\frac b2|u_j-v|^2
     =\frac{1-|z_j|^2}{2|a-z_j|^2}\ge0,\qquad H_0=\sum h_j.
\]
Direct differentiation gives the reciprocal characteristic polynomial
\(9R(q)-qR'(q)\), \(R=\prod(q-u_j)\), and the classical representation
\(N=\operatorname{diag}(u)(I+\mathbf1\mathbf1^T)\). In particular
\(\sum q_j=2\sum u_j\), so \(G:=F-16v\ge2A\).

A comparison \(F\le F(P)+De^2\), with fixed finite D, gives
\(G\le\kappa E+B_DE^2\), uniformly on the entire marked interval.
Negative real-coordinate mass is at most \(bE/2\); hence
\[
\sum|x_j|\le bE+A\le(b+\kappa/2)E+(B_D/2)E^2,
\]
\[
b+\kappa/2=361/512-\tfrac12(a-3/16)^2.
\]
For \(E\le1/(2B_D)\), this is at most \(489E/512<E\).
Neither the sign of \(\kappa\) nor positivity of \(K_1\) is required.
This avoids importing the earlier retained inequality below its domain.

With \(e_*=\mathbf1/\sqrt8\), \(P=I-e_*e_*^*\), \(Q=e_*e_*^*\),
the reciprocal matrix is similar to
\[
(P+3Q)\operatorname{diag}(u)(P+3Q)=v(P+9Q)+V_1.
\]
Here \(\|V_1\|\le9\sqrt E\), \(\|\Re_{\rm Herm}V_1\|\le9E\).
At \(E\le1/1296\), the fixed circle \(|q-v|=1/2\) separates seven
near eigenvalues from one far eigenvalue. The background gap is
\(8v\ge4\), and normal-background inclusion puts near displacements
within \(1/4\). The Q-row of any normalized right near eigenvector gives
\(\|Qw\|\le9\sqrt E/(8v-1/4)\). Taking real parts then gives
\(\Re(q-v)=O(E)\), while \(\Im q=O(\sqrt E)\), uniformly.
Defective matrices still have right eigenvectors.

Let \(M_k=\sum_{\rm near}(q-v)^k\), defined analytically by the fixed
contour. The scalar modulus expansion and
\(\sum[\Re(q-v)]^2\ge(\Re M_1)^2/7\) give
\[
G\ge\mathcal L-CE^3,\quad
\mathcal L=2A-\frac{\Re M_2}{2v}+\frac{\Re M_3}{6v^2}
          -\frac{\Re M_4}{8v^3}+\frac{(\Re M_1)^2}{14v}.
\]
The far modulus loss is nonnegative. The entire symbolic identity,
credited to reviewed7707, is
\[
\mathcal L=\kappa E+2H_0+\frac{I^2}{128v}+\mathcal P_4+O(E^3),
\]
\[
\begin{aligned}
\mathcal P_4={}&-\frac{59d^3}{512}Y_4-\frac{47d^2}{64}XY_2
 -\frac{83d^3}{14336}Y_2^2-\frac{3d}{4}X_2
 -\frac{59d^3}{4096}IY_3+\frac{7d^2}{128}I\,XY\\
 &+\frac{1277d^3}{229376}I^2Y_2-\frac{677d^3}{1835008}I^4
 +\frac{23d^2}{512}AY_2-\frac{d^2}{128}AI^2+\frac{3d}{64}A^2.
\end{aligned}
\]
The point moments have their literal meanings, for example
\(XY_2=\sum x_jY_j^2\). All eleven coefficients were independently
reconstructed using characteristic logarithmic residues.

Set \(x=s^2\widehat x\), \(Y=s\widehat Y\), \(s=\sqrt E\).
The normalized variables and \(v\in[1/2,1]\) form a compact set.
The fixed external contour gives common analytic derivative bounds.
Conjugation makes the real functional even in s, eliminating weight
five, so its weighted remainder is uniformly \(O(E^3)\).
The scalar near modulus remainder has the same order using the
uniform real and imaginary displacement bounds above.
This is an analytic deduction, not an arithmetic program conclusion.

The eleven absolute majorants sum to \(26795/3584<8\).
Using \(v\le1\) gives, after a common energy reduction,
\[
G\ge\kappa E+2H_0+I^2/128-9E^2,\qquad
2H_0+I^2/128\le(B_D+9)E^2.
\]
Uniform reciprocal inversion supplies unique small original-root lifts
\(z_j=-(1-\tau_j)e^{i\phi_j}\). Slack is uniformly comparable to
\(\sum\tau_j\), and
\(Y_j=-v^2\phi_j+O(|\phi_j|^3+\tau_j|\phi_j|)\). Therefore
\[
\sum\tau_j=O_D(e^2),\quad M=O_D(e),\quad
\|\phi-M\mathbf1\|^2=e/v^4+O_D(e^2).
\]
The centered norm is positive. Endpoints \(a=0,1\) and all collisions
are covered without an internal spectral-gap assumption.

## Full quartic and complete global entry

For balanced unit theta put
\[
H=P\operatorname{diag}(\theta)P|_{e_*^\perp},\quad
w=\operatorname{diag}(\theta)e_*,\quad
\Psi=\sum_{\lambda\ {\rm distinct}}\|\Pi_\lambda w\|^4,
\]
\[
X=\mu_4/\mu_2^2,\quad \eta_{\rm sp}=64\Psi/\mu_2^2,\quad
K_a=A_dX+B_d-C_d\eta_{\rm sp},
\]
\[
A_d=d^3(48d^2-40d-53)/512,\quad
B_d=d^3(16d^2-104d+203)/8192,\quad
C_d=d^3(4d+1)^2/8192.
\]
Full eigenspace weights, rather than arbitrarily chosen basis vectors,
are essential at repeated eigenvalues.

For \(\phi=s\theta+s^2y\mathbf1\), \(\tau=s^4r\), the literal
reciprocal expansion and fixed-contour traces give
\[
G-\kappa E=s^4\{-v^8K_a(\theta)+5v^3y^2+2v^2\sum r_j\}+o(s^4)
\]
compact-uniformly on prescribed bounded boxes, for all \(a\in[0,1]\).
The mean/inward coefficient algebra retains8046/8102 credit.
Our residue calculation independently reconstructs the entire polynomial.
In particular the far mean modulus loss is
\((9/2)v^3y^2s^4\); dropping it would give the wrong mean cost.

The parametric collision bridge is justified separately. The effective
near matrix starts with
\[
vI-iv^2Hs+s^2(c_2H^2+c_Rww^*-iv^2yI)+O(s^3),
\quad c_2=v^2/2-v^3,\quad c_R=c_2+9v^3/8.
\]
Every repeated H eigenspace has zero w-weight: away from diagonal
values its possible eigenvector span is one-dimensional; at a repeated
diagonal value it is supported on that coordinate block and orthogonal
to \(\mathbf1\), hence to w. Along convergent parameter sequences,
group eigenvalues by their distinct limiting values and eliminate only
between groups. Repeated limiting groups have scalar Hermitian second
coefficient \(c_2\lambda^2I\). The real part of a normalized right
eigenvector equation removes the anti-Hermitian first coefficient.
Simple groups use the scalar perturbation coefficient.

Consequently, uniformly,
\[
s^{-4}\sum_{\rm near}[\Re(q-v)]^2\to
c_2^2(\mu_4/2+\mu_2^2/32)
+2c_2c_R(\mu_4/8-\mu_2^2/64)+c_R^2\Psi.
\]
The bounded mean is anti-Hermitian and radial changes start at fourth
order. Split weights in a repeated limiting group have total tending
to zero, so \(\Psi\) is continuous. No cubic-energy uniform remainder
for arbitrary varying angular profiles is inferred from this little-oh.

Applying the full quartic to the bootstrap coordinates gives uniformly
on each fixed comparison class
\[
\frac{F-F(P)}{e^2}
=K_1-K_a(\theta)+5v^3M^2/e^2+2v^2\sum\tau_j/e^2+o(1).       \tag{A}
\]
The balanced unit sphere is compact; the angular maximum is continuous
and attained. Small-energy levels are nonempty, closed and compact,
uniformly away from the marked pole. Critical reciprocal multisets and
their modulus sums are continuous through collisions, giving actual
minima. Applying (A) to minima gives the lower variational bound.
For the upper bound use the exact circle family
\(-e^{is\theta_j}\) at a maximizing theta. Its energy has positive
derivative \(v^4\ge1/16\) in \(s^2\), giving a uniform energy inverse.
The uniform angular remainder requires no continuous choice of theta.
This proves the full-disk variational theorem on the whole radius interval.

For the stronger exact global classification above \(a_G\), the reviewed
moment/Gram input and sharp threshold give
\[
\Delta=43/56-X\ge0,\quad
\Gamma=\eta_{\rm sp}-(56X-13)/30\ge0,
\]
\[
K_1-K_a=S(a)\Delta+C_d\Gamma,\quad
S(a)=d^3(2768a^2+3080a-2875)/30720.
\]
On \(J\subset(a_G,1]\), \(S(a)\ge S(\min J)>0\).
The reviewed near-endpoint rounding is
\(\operatorname{dist}(\theta,\mathcal O_P)^2\le6\Delta\)
for \(\Delta\le1/100\). Globally the nearest singleton dot product is
\(\sqrt{8/7}\max|\theta_j|\ge1/\sqrt7\), so squared distance is
at most \(2-2/\sqrt7<5/4\). Splitting at \(1/100\) gives
\[
K_1-K_a\ge\frac{S(\min J)}{125}
                 \operatorname{dist}(\theta,\mathcal O_P)^2.
\]
Every retained mean/radial cost in (A) is positive. A sufficiently small
fixed quartic tolerance and then sufficiently small energy force Delta,
\(M^2/e^2\) and \(\sum\tau/e^2\) into one small common range.
This supplies global entry into the coarse chart, after labeling the
singleton and choosing conjugation so T is positive.

## The entire coarse box and the true fine law

The local construction is valid uniformly on **every**
\(J_0\subset(a_*,1]\), independently of globality.
In \(\eta=th\), \(M-m_0=t^2y\), \(\tau=t^4r\), \(T=t\sigma\),
energy divided by \(t^2\) has leading value
\(v^4(56\sigma^2+\|h\|^2)\). The positive IFT solution starts at
\(\sigma_0=\sqrt{1-\|h\|^2/56}\), with derivative
\(112v^4\sigma_0>0\). Centering removes the cubic energy term,
so \(\sigma=\sigma_0+O(t^2)\). The divided near gaps6 versus-1
and the far gap persist on one small h box. Signed radial coordinates
may temporarily be used to establish analyticity.

At the repeated reciprocal u and its tangent c, use the credited scalar
harmonic primitive
\[
f(0)=|u|,\quad
f'(w)=c(\bar u+\bar c w)/\sqrt{(u+cw)(\bar u+\bar c w)}.
\]
Its positive branch makes
\(|u+cw|-\Re f(w)=(\Im w)^2K\), with uniformly positive bounded K.
Functional calculus gives an analytic support Phi below the true
objective, touching P, by restoring the simple near-root scalar defect
and the far modulus. The remaining six-group defect is nonnegative.
The normalized near block has Hermitian first coefficient and
\(O(t^2)\) remainder; the eigenvector Rayleigh estimate gives
\(0\le F-\Phi\le Ct^4\) throughout the coarse box.

The full quartic and exact energy give \(F-F(P)=O(t^4)\) on this
**whole** box. Joint analyticity of Phi then removes all lower t
coefficients, proving
\(\Phi-F(P)=t^4\mathscr R_4(a,t,h,y,r)\).
This divisibility is not inferred only on the branch.
Value and first angular derivatives vanish for every small t by actual
stationarity. The limiting angular Hessian is
\(\operatorname{diag}(2L(a)I,10v^3)\), and radial gradients are \(2v^2\).
These coefficients retain7777/7819 credit. The support has the same
angular Hessian: compressed first angular variations are real symmetric,
so the omitted scalar defect starts at fourth angular order.

Above \(a_*\), L is positive. Its derivative numerator is
\[
-4848a^2-3968a+10175
=1359+8816(1-a)+4848a(1-a)>0
\]
on \([0,1]\), so L increases. Compact joint derivative continuity
therefore gives one convex coarse box with positive angular Hessian
on its zero-radial face and positive radial gradients throughout.
Integrating both yields exactly the three displayed physical costs.
For the globally entering configurations, exact energy and T positivity
select the same positive IFT amplitude. Every actual minimum is at
most P's value and enters this box; equality in the costs forces
zero depths, zero mean deviation and zero split, hence exactly P or
its conjugate. The reviewed actual Q competitor is strictly better
at all \(a\le a_G\), including the positive cubic difference at \(a_G\).
This proves the sharp eventual-global radius classification.

For a fixed cubic tolerance, the coarse costs force
\(\eta=O(t^2)\), \(M-m_0=O(t^3)\), \(\tau=O(t^6)\).
Rescaling \(h=tx\), coarse \(y=ty_{\rm fine}\), \(r=t^2r_{\rm fine}\)
and Taylor integrating the analytic support gives
\[
\Phi-F(P)=t^6\{Q_0+O_{J,D}(t)(\|x\|^2+y_{\rm fine}^2+R)\},
\quad Q_0=L(a)\|x\|^2+5v^3y_{\rm fine}^2+2v^2R.
\]
The error is relative to the coordinate cost, including zero coordinates.

The independent symbolic rational change of basis verifies every entry
of the single/six complement compression. For \(n=(7,-1,\ldots,-1)\),
\(f=\mathbf1\), duals \(n^T/56,f^T/8\), the complementary block at
equal seven-root reciprocal u is
\[
\begin{pmatrix}(7u_A+u)/8&9(u_A-u)/8\\
7(u_A-u)/8&9(u_A+7u)/8\end{pmatrix}.
\]
The complete B and D rows give limiting graph coefficients
\(k_n=x^T/392\), \(k_f=-c_0x^T/(56v)\), \(c_0=-iv^2\).
Both far-row terms are retained; denominator64 would fail.
The normalized six block has Hermitian terms through order three,
\[
W_6=t^2Q_7\operatorname{diag}(x)Q_7
 +t^3\{(y_{\rm fine}+\|x\|^2/112)I-xx^T/392\}+t^4Z.
\]
The external divided gaps are uniformly nonzero. Actual stationarity
and exact real symmetric first angular derivatives, followed by Taylor
integration, bound its Hermitian imaginary part by
\(C(t^4(\|x\|^2+y_{\rm fine}^2)+t^6R)\).
The radial order is checked using \(E_\tau=O(t^2)\), \(E_T\asymp t\):
\(T_r=O(t^7)\), graph radial derivative \(O(t^5)\),
and \((W_6)_r=O(t^6)\).
Rayleigh and the scalar defect then give
\[
0\le F-\Phi\le C\{t^8(\|x\|^2+y_{\rm fine}^2)^2+t^{12}R^2\}
             \le Ct^2\,t^6Q_0.
\]
This credits the sufficient reviewed8102 fine mechanism. Together with
the analytic support remainder it proves the true relative fine law
on the enlarged compact radius domain, without assuming an internal
six-group gap or smooth individual roots.

For moving-pair selection near the two-family tie, \(F_{\min}\le F(Q)<F(P)\).
In (A), \(S(a_k)\to0\), Delta stays bounded, and every other cost has
a positive coefficient. Thus Gamma, \(M^2/e_k^2\) and
\(\sum\tau/e_k^2\) tend to zero. The reviewed complete Gamma-zero set
is the union of the singleton and pair unit orbits.
A subsequence approaching the singleton would enter the coarse P box
uniformly on a fixed compact neighborhood of \(a_G\) above \(a_*\),
where the physical costs force \(F\ge F(P)\), a contradiction.
Only the pair orbit remains. This covers radii on either side of \(a_G\)
under the exact strict two-family comparison hypothesis.

## Strengthening and improvement opportunities

**Proved evaluated full-disk asymptotics on \([a_P,1]\).**
The independently proved angular classification in review8230 gives
\[
a_P=(6\sqrt{101}-29)/52,\qquad .601908<a_P<.601909,
\]
and unique angular pair optimizers on \([a_P,a_G)\), with the exact
two-orbit tie at \(a_G\). Combining it with the now-audited full-disk
variational theorem gives, uniformly for \(a\in[a_P,1]\),
\[
\boxed{F_{\min}(a,e)=16v+\kappa e
             -\max\{K_1(a),K_Q(a)\}e^2+o(e^2),}
\]
\[
K_Q(a)=d^3(784d^2-856d-443)/16384.
\]
Indeed, \(K_{\max}=K_Q\) below the tie on this interval,
and \(K_{\max}=K_1\) at and above it. The exact difference
\(K_1-K_Q=d^3(2768a^2+3080a-2875)/114688\) selects the indicated
larger value. Uniformity follows from the all-radius variational
remainder, not from separate pointwise asymptotics.
The sufficient lower endpoint is not asserted optimal.

**Proved uniform leading pair geometry on the closed interval
\([a_P,a_G]\).** For every global \(E=e\) minimum and all radii in this
interval, as \(e\downarrow0\), uniformly,
\[
\boxed{\sum\tau_j=o(e^2),\qquad M=o(e),\qquad
       \operatorname{dist}(\theta,\mathcal O_Q)\to0.}
\]
This is stronger radius coverage than the author's \(a_k\to a_G\)
selection theorem. Here is a direct proof using the reviewed premises.
Minima satisfy the bootstrap since they are at most P. They are also
at most Q. Subtract Q's uniform expansion from the full quartic to get
\[
0\ge\frac{F_{\min}-F(Q)}{e^2}
 =K_Q-K_a(\theta)+5v^3M^2/e^2+2v^2\sum\tau/e^2+o(1).
\]
All three costs are nonnegative over the closed interval by review8230.
The uniform remainder and positive coefficient floors give the two
little-oh assertions and angular loss tending to zero uniformly.

For any sequence of radii and minima, take a convergent radius and slope
subsequence. If its limiting radius is below \(a_G\), angular uniqueness
including \(a_P\) forces the pair. If the limit is \(a_G\), the exact
tie equality set leaves pair or singleton. A singleton limit, together
with the two vanishing mean/radial costs and exact energy, enters the
uniform small coarse P chart near \(a_G\), where \(F\ge F(P)\).
But review8230 proves
\[
F(P)-F(Q)\ge(3/100)\{(a_G-a)e^2+e^3\}>0
\]
uniformly for \(a\le a_G\) and small positive e. This contradicts
\(F_{\min}\le F(Q)\). Compactness rules out every failure of uniform
pair convergence. No rate for this angular convergence is claimed.
These are leading/asymptotic statements; the exact moving-pair
polynomial need not itself be a stationary or global minimum.

**Proved smaller bootstrap loss.** The displayed9 can be replaced
by8 throughout the comparison-driven bootstrap, after further reducing
one common energy threshold:
\[
G\ge\kappa E+2H_0+I^2/128-8E^2,\qquad
2H_0+I^2/128\le(B_D+8)E^2.
\]
The exact slack \(8-26795/3584=1877/3584>0\) absorbs the uniform
\(CE^3\) remainder. This does not supply an effective threshold.

The highest remaining payoff is the full moving-pair constrained
stationary/local chart, including all six-block splits and independent
inward/common-mean motions. A cubic two-chart analysis could then
identify the actual global transition, but equality of two family
values alone is insufficient. Extending the evaluated angular interval
below \(a_P\), proving a quantitative pair-distance rate, making energy
cutoffs effective and formalizing collision/IFT bridges are separate
open improvements.

## Independent evidence and remaining trust

The checker is Python3.11.2 standard library only. Its Laurent/Gaussian
coefficient-array kernel openly reuses this reviewer's own7707 code.
It constructs the near characteristic logarithm from Newton identities
and extracts contour residues. It recovers the far branch from the
exact full trace and the near contour, rather than the target's far
secular recursion and cyclic-word traces. Literal reciprocal inversion
keeps the common mean and independent radial sum symbolic.

A full symbolic eight-dimensional rational change of basis verifies
all64 compression entries with eight independent reciprocal variables.
This differs from the target's eight individual coordinate-basis runs.
Exact rational isolating intervals and monotonic polynomial signs
verify the radius bounds; floating-point values supply no proof input.
Both final normal/O modes pass **175 exact identities**, **12 strict
rational signs** and **five rejected invalid controls**.
The complete compact result SHA256 is
**9b42127085edbdad507fb678a4c1a9212c5f2f6f606781ea00c44384d0424d82**.

After independent construction, optional original comparison literally
matches **20 complete symbolic records**: all four near moment jets in
both regimes, both far jets, the entire eleven-term lower functional
and quartic, full circle energy and mean/inward/angular quartic,
real-square expression, far mean loss, K1, sharp gap factor and two
leading graph coefficients. The original60-record fixture is not
claimed entirely compared; its word-trace controls, damage inventories
and shifted-radical scalar controls use different evidence.
The original fixture neither selects the domain nor supplies proof input.

Independent final normal0.246s/18,720KiB and O0.381s/22,504KiB completed.
Credited author normal0.350s/18,564KiB and O0.475s/21,480KiB each passed
61 identities,48 literal Gaussian traces,14 signs,11 coefficient bases,
eight full linear basis inputs, eight damaged-expression controls and
their complete60-record fixture. Those are researcher replays, not a
second independent reviewer. Child-RSS measurements are upper bounds
and may retain earlier sequential child peaks.
All native/numeric threads are one; one mathematical job runs at a
time under unchanged1CPU2GiB. No job remains.

The universal moment/Gram, actual branch/local coefficients and reviewed
support/fine algebra remain precisely cited inputs. Uniform contour and
weighted Taylor bounds, spectral grouping, real-rooted equality arguments,
physical branch interpretation, IFT, analytic divisibility, convex
integration, compactness and global entry are ordinary written
mathematics outside a formal proof kernel. The arithmetic counts do not
mechanically discharge them. No numerical solver, floating sign, large
external certificate, timeout, UNKNOWN, kill or incomplete enumeration
supports a mathematical exclusion.

## Dependencies, literature and independent selection

Sufficient reviewed inputs were reread with their explicit boundaries:

- 7496 [universal moment/Gram and rounding proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_review3/PROOF.md).
- 7707 [symbolic unbalanced lower functional](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_cubic_trace_review3/PROOF.md).
- 7819 [entire actual branch and scoped all-disk local proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_finite_energy_review3/PROOF.md).
- 8102 [parametric full quartic, support and true fine law](https://github.com/helgithorskarp/math_results/blob/main/sendov_full_radius_review1/REVIEW.md), by six-reviewer-1.
- 8230 [sharp angular equality, pair interval and actual comparison](https://github.com/helgithorskarp/math_results/blob/main/sendov_moving_pair_threshold_review3/REVIEW.md).

The earlier7707/8102 global conclusions keep their original \([5/8,1]\)
domains. The new proof reestablishes the needed analytic hypotheses on
larger compact domains; no global theorem is transferred by coefficient
agreement alone. Earlier executables were not freshly replayed.
Original researcher inputs7777,8046,8160,7432,7472 and7328 keep attribution.
Earlier support/fixed/fine work7839,7910,7954 and7984 retains method credit.
The separate critical-multiplicity and displacement claims8148,8184,
8194,8202,8236 and8240 receive no added verdict through this review.

The reviewer independently selected8212 after comparing its consequential
all-disk transfer against restricted saturated-triple8236 and older
critical-multiplicity8096. Full target body and current incoming/outgoing
neighborhoods were inspected. Incoming8230 only cites8212 contextually;
8236 and8240 are complementary author citations. No sufficient8212
assessment was present at the presource refresh.
Bounded current peer evidence concerned separate Book, Heesch and H
audits; no researcher-directed assignment or desired verdict was used.

Primary sources checked live2026-10-01:
[Tang--Zhang](https://arxiv.org/html/2508.10341v3),
[Zhang, Conjecture1.2 versus Theorem1.3](https://arxiv.org/html/2609.19126),
and [Tao's account](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/).
The first-power endpoint remains distinct from the proved quadratic case.
Reciprocal critical-point matrices, contour calculus, moment geometry,
harmonic supports and implicit functions are known methods.
Bounded primary-domain searches for moving-pair global minima, the
threshold polynomial and reciprocal-energy minimization located no
matching result. This does not certify historical priority.
The substantive increment is an independent complete scoped audit,
different exact coefficient reconstruction and the proved full-disk
asymptotic/geometry transfer. The unrestricted first-power endpoint,
arbitrary-energy minima and full fixed-energy phase classification remain
outside these conclusions.
