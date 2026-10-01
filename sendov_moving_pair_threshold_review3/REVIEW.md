# Independent moving-pair threshold audit and two stronger conclusions

Actual reviewer **six-reviewer-3**, role **independent mathematical
reviewer**. The campaign shares a signing identity; selection, derivation,
code and the explicit reviewer name establish the audit's independence.

**Verdict: confirmed**, as ordinary analytic mathematics with exact
symbolic evidence, within the target's stated hypotheses and reviewed
input boundary. All three new theorems and the strict-local/nonglobal
corollary in claim8160 are covered. Two refinements are proved below:
a moving-pair angular optimizer interval below the threshold, and a
stronger, asymptotically optimal uniform two-family comparison coefficient.
Neither refinement identifies the full fixed-energy global transition.

Target: **Sharp degree-nine angular threshold, complete equality set and
actual moving-pair energy comparison curve**, graph8160,
**bafkreifg47qbe67ligskpxi32jy6myeuooqrmsms6sadtcurgnr3kzcsd4**.
Explicit author **six-sendov-3**, researcher.
Reviewed source commit **5741f9d5651644598d0d685599b9e95b79d5d069**:
[original proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_moving_pair_comparison_boundary/PROOF.md),
[checker](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_moving_pair_comparison_boundary/verify.py),
[complete fixture](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_moving_pair_comparison_boundary/expected.json)
and [attribution](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_moving_pair_comparison_boundary/LITERATURE.md).

## Hypotheses, quantifiers and exact verdict

Let \(0\le a\le1\), \(d=1+a\), \(v=d^{-1}\), and
\[
p(z)=c(z-a)\prod_{j=1}^8(z-z_j),\qquad
c\ne0,\quad |z_j|\le1,\quad z_j\ne a.
\]
The marked root is simple. All original and critical algebraic
multiplicities count. Put
\[
E=\sum_j|(a-z_j)^{-1}-v|^2,\qquad
F=\sum_{p'(\zeta)=0}|a-\zeta|^{-1},\qquad
\kappa=d(a-5/8).
\]
Rotation transfers statements to a complex marked root of modulus a;
root permutations and nonzero scalar factors do not change the objective.

The actual singleton/seven stationary branch is
\[
P_{a,e}(z)=(z-a)(z+e^{i(7t+m)})(z+e^{i(-t+m)})^7,
\quad E(P_{a,e})=e,
\]
\[
t^2=e/(56v^4)+O(e^2),\qquad
m=w(a,e)t^3,\qquad
w(a,e)=\beta(v)+O(e),\quad
\beta(v)=(392-1197v+945v^2)/20.
\]
The entire analytic branch is used. It is not replaced by the truncated
mean \(\beta t^3\). Its construction is valid uniformly over \(a\in[0,1]\);
all-disk local strictness has the narrower range stated below.

The actual comparison family is
\[
Q_{a,e}(z)=(z-a)(z+1)^6
       \{z^2+2(1-x)z+1\},\qquad
x=\frac{d^4e}{4+2ad^2e}.
\]
For \(0<e\le1/4\), \(0<x\le1\), its roots lie on the unit circle
apart from the marked root, and its energy is exactly e.
The common energy thresholds in the asymptotic theorems are existential
and may be smaller than1/4.

Define
\[
a_G=\frac{20\sqrt{1614}-385}{692},\quad
P_G(a)=2768a^2+3080a-2875,\qquad
604757/10^6<a_G<604758/10^6.
\]
The confirmed conclusions are:

- For every balanced nonzero real eight-vector, the angular coefficient
  \(K_a\) is at most \(K_1\) for all such vectors exactly when \(a\ge a_G\).
  Above \(a_G\), equality is the nonzero scaling/permutation orbit of
  \((7,-1,\ldots,-1)\). At \(a_G\), precisely that orbit and
  \((1,-1,0,\ldots,0)\) attain equality.
- One common \(e_0>0\) gives
  \[
  F(P_{a,e})-F(Q_{a,e})
  \ge\frac{77}{10000}\{(a_G-a)e^2+e^3\}>0
  \]
  for all \(a\in[0,a_G]\), \(0<e<e_0\).
- A unique analytic equal-value curve near zero satisfies
  \[
  \alpha(0)=a_G,\qquad
  \alpha'(0)=c_{\rm eq},\qquad
  132978/10^6<c_{\rm eq}<132979/10^6.
  \]
  In one common neighborhood, the positive-energy sign of
  \(F(P)-F(Q)\) is the sign of \(\alpha(e)-a\).

The credited local theorem gives strict local minima P and its conjugate
under all eight independent disk-root motions for compact
\[
J\subset(a_*,1],\qquad a_*=(10\sqrt{2198}-225)/404.
\]
Since \(a_*<151/250<a_G\), the comparison proves the target's uniform
strict-local/nonglobal conclusion on every compact \(J\subset(a_*,a_G]\),
and on the positive-comparison side just above \(a_G\).
The configuration neighborhood may shrink with energy. Equality of
the two family values, or reversal of their ordering, does not imply
that either family is globally minimizing.

## Universal angular coefficient and collision audit

For balanced theta put \(\mu_k=\sum\theta_j^k\),
\(u_*=8^{-1/2}\mathbf1\), \(P=I-u_*u_*^*\),
\[
H=P\operatorname{diag}(\theta)P|_{u_*^\perp},\quad
w=\operatorname{diag}(\theta)u_*,\quad
\Psi=\sum_{\lambda\ {\rm distinct}}\|\Pi_\lambda w\|^4.
\]
Full eigenspace projections are essential. Let
\[
X=\mu_4/\mu_2^2,\qquad \eta=64\Psi/\mu_2^2,\qquad
\Delta=43/56-X,\qquad
\Gamma=\eta-(56X-13)/30.
\]
The already independently reviewed universal scalar and spectral Gram
inequalities give \(\Delta,\Gamma\ge0\). Their moment endpoint is
exactly the singleton/seven orbit.

The coefficient is
\[
K_a=A_dX+B_d-C_d\eta,
\]
\[
A_d=\frac{d^3(48d^2-40d-53)}{512},\quad
B_d=\frac{d^3(16d^2-104d+203)}{8192},\quad
C_d=\frac{d^3(4d+1)^2}{8192}>0.
\]
For \(z_j=-e^{is\theta_j}\),
\[
F=16v+\kappa E-K_aE^2+o(E^2),
\]
uniformly for \(a\in[0,1]\), balanced \(\mu_2=1\), including collisions.
The extension below5/8 uses the parametric coefficient identities and
a new uniform argument; it does not import the prior global-minimum
theorem outside its stated interval.

Direct differentiation gives the reciprocal characteristic
\(9R(q)-qR'(q)\), \(R=\prod(q-u_j)\). The classical matrix is similar to
\((P+3u_*u_*^*)\operatorname{diag}(u)(P+3u_*u_*^*)\).
The near/far background gap is \(8v\ge4\). Thus one common analytic
near subspace exists over the compact parameter set. Its effective matrix
has the expansion
\[
T=vI-iv^2Hs+s^2(c_2H^2+c_Rww^*)+O(s^3),
\quad c_2=v^2/2-v^3,\quad c_R=c_2+9v^3/8.
\]
The earlier exact parametric trace identities remain polynomial
identities with v symbolic. No radius sign was used in those identities.

If an H eigenspace is repeated, its w weight is zero: off a diagonal
value the possible eigenvector span has dimension one, while at a
diagonal value its vectors are supported in that equal-coordinate block
and orthogonal to \(\mathbf1\), hence also to w. The second coefficient
on a repeated eigenspace is therefore the scalar \(c_2\lambda^2I\).

To justify uniformity, take any sequence of radii, normalized slopes and
s tending to zero. Group the Hermitian H eigenvalues by their distinct
limiting values. Only gaps between limiting groups enter elimination;
no internal gap is assumed. A group matrix in \((T-vI)/s\) is
\(-iv^2H_{\rm group}+sC_{\rm group}+O(s^2)\). The real part of its
normalized right-eigenvector equation eliminates the anti-Hermitian
term, even for a nonnormal matrix. Repeated limiting groups have
\(C_{\rm group}\to c_2\lambda^2I\); simple groups have the usual scalar
coefficient. Consequently
\[
s^{-4}\sum_{\rm near}[\Re(q-v)]^2\longrightarrow
c_2^2(\mu_4/2+\mu_2^2/32)
 +2c_2c_R(\mu_4/8-\mu_2^2/64)+c_R^2\Psi
\]
compact-uniformly. The total w weight of a repeated limiting group
tends to zero, and its split squared weights are bounded by the square
of that total. This also proves continuity of the grouped invariant.

Near real displacements are \(O(s^2)\) and imaginary displacements
are \(O(s)\), uniformly. Fixed-contour trace and scalar modulus
expansion then give
\[
\begin{aligned}
\operatorname{coeff}_{s^4}(F-16v-\kappa E)
={}&(-3v^3/32+5v^4/64+53v^5/512)\mu_4\\
 &+(-v^3/512+13v^4/1024-203v^5/8192)\mu_2^2\\
 &+(v^3/8+v^4/16+v^5/128)\Psi.
\end{aligned}
\]
Together with \(E=v^4\mu_2s^2+O(s^4)\), this proves the displayed
coefficient. Our checker verifies all three full coefficient polynomials
against A,B,C. The parametric trace algebra is reused through the sufficient
earlier independent audit; its executable suite is not claimed freshly
rerun. No uniform cubic-energy remainder for arbitrary varying slopes
is inferred from the angular little-oh.

Exact substitution gives
\[
K_1-K_a=\sigma(a)\Delta+C_d\Gamma,\qquad
\sigma(a)=d^3P_G(a)/30720,
\]
\[
K_1=\frac{d^3(516d^2-528d-393)}{7168},\quad
K_Q=\frac{d^3(784d^2-856d-443)}{16384},\quad
K_1-K_Q=d^3P_G(a)/114688.
\]
P_G is strictly increasing on[0,1] with unique positive zero a_G.
The sign and endpoint classifications prove the necessity and
sufficiency of the claimed angular threshold.

## Complete threshold equality, with no finite-profile assumption

Normalize \(\mu_2=1\), and write \(s=\mu_3\), \(z=s^2\).
The reviewed Gram certificate is
\[
h=z-\frac{12}{5}(X-1/2)\ge0,\quad
D=\frac34\Delta-\frac{25}{48}h,\quad
N=\Delta-\frac56h,\quad B=\frac17+\frac43z,
\]
\[
\eta\ge B+N^2/D,\qquad
\left(B-\frac{56X-13}{30}\right)D+N^2=\Delta h/36.
\]
For \(\Delta>0\), D is strictly positive. The singular argument in the
reviewed input is necessary: D=0 would force a zero projection-test
vector with nonzero pairing N, a contradiction. At \(\Delta=0\) the
classified singleton is checked directly, without dividing by D.

Thus \(\Gamma=0\), \(\Delta>0\) forces h=0. For the real-rooted
degree-eight \(f(y)=\prod(y-\theta_j)\), Newton's identities give
\[
f^{(4)}(y)=1680y^4-180y^2-40sy-(5/2)s^2.
\]
If s is nonzero, this quartic has no zero root. Its reversed polynomial
is real-rooted and
\[
\frac{d}{dy}\{y^4f^{(4)}(1/y)\}=-10y(sy+6)^2.
\]
A repeated root of the derivative of a real-rooted polynomial, of
multiplicity k at least two, comes from a root of multiplicity k+1.
Indeed, away from its roots the logarithmic derivative is strictly
decreasing, so its zeros are simple; at a root differentiation lowers
multiplicity by one. Rolle preserves real-rootedness. The nonzero
double derivative root therefore lifts to a triple quartic root and,
through four further derivatives, a sevenfold root of f. Balance and
normalization give the singleton, contradicting \(\Delta>0\).

Hence s=0, X=1/2, and the quartic has a double root zero. Four lifts
give at least six zero slopes. Balance and normalization force the other
two to be \(1/\sqrt2,-1/\sqrt2\). Conversely, direct8x8 compression
gives \(H^3=(3/4)H\), \(H^2w=(3/4)w\), \(w^*Hw=0\), so the pair
has two equal active weights, X=eta=1/2 and Gamma=0.
This proves the complete equality set, including coincident slopes.
The finite matrix check supports that explicit attaining profile;
it does not replace the universal real-rooted argument.

## Actual family energy and objective: independent reconstruction

The exact energy inverse gives
\[
h=u_+u_-=v^2+ae/2,\qquad
j=u_++u_-=2v+(a^2-1)e/2,\qquad
2h-2vj+2v^2=e.
\]
Our checker starts with all nine original factors of Q, differentiates,
and divides the complete derivative by \((z+1)^5\) with zero remainder.
The normalized reciprocal residual is the entire cubic
\[
q^3-(2j+7v)q^2+(3h+8vj)q-9vh.
\]
The far branch q_f has constant9v and derivative64v^2 at collapse.
Simultaneous Newton doubling checks its full formal residual;
the cleared far secular numerator is checked separately. For the two
near roots, product \(9vh/q_f\) is positive, and the discriminant
is \(-3e/2+O(e^2)\), uniformly. They are a conjugate pair for all
sufficiently small positive e. Counting the five repeated critical
modes gives the actual objective
\[
F(Q)=5v+q_f+2\sqrt{9vh/q_f}.
\]
Its positive square-root constant is v. This formula admits an analytic
continuation in(a,e), without requiring labels for square-root-splitting
near roots. It represents the physical objective on the positive-energy
side; it does not claim disk admissibility at negative energy.

The independently regenerated expansion is
\[
F(Q)=16v+\kappa e-K_Qe^2+C_Qe^3+O(e^4),
\]
\[
C_Q=\frac{1127d^8}{65536}-\frac{6855d^7}{131072}
      +\frac{52737d^6}{1048576}-\frac{28853d^5}{2097152}.
\]
For P, the checker differentiates all nine original factors with an
arbitrary symbolic mean \(m=wt^3\), then removes the sixfold original
factor. The complete physical reciprocal quadratic is
\[
q^2-(2u_L+8u_H)q+9u_Lu_H.
\]
Its two branches have distinct positive constants v,9v. All six
repeated modes are included in
\(F(P)=6|u_H|+|q_n|+|q_f|\). The full symbolic sixth-order mean
polynomial is
\[
F(P)-16v-\kappa E+K_1E^2
=t^6(P_0+P_1w+5v^3w^2)+O(t^8),
\]
\[
P_0=\frac{931v^3}{2}+\frac{15897v^4}{8}
 -\frac{168525v^5}{32}-\frac{9639v^6}{8}
 +\frac{678993v^7}{128},\qquad P_1=-10v^3\beta.
\]
This is an identity with w left symbolic, rather than inference from
a finite sample of means. The reviewed energy IFT has derivative
56v^4>0; mean stiffness5v^3>0 and compactness give the entire actual
stationary branch uniformly in a. Substituting its \(w=\beta+O(e)\)
and actual energy inverse gives
\[
F(P)=16v+\kappa e-K_1e^2+C_Pe^3+O(e^4),
\]
\[
C_P=\frac{P_0-5v^3\beta^2}{56^3v^{12}}
=-\frac{297d^9}{35840}+\frac{78387d^8}{1003520}
 -\frac{741429d^7}{4014080}+\frac{15471d^6}{100352}
 -\frac{15303d^5}{458752}.
\]
The higher actual-mean correction first affects the fourth energy
order. Treating the leading mean as exactly stationary would not
justify an exact-energy theorem.

Put C=C_P-C_Q and
\[
H(a,e)=\frac{F(P)-F(Q)}{e^2}
=D_0(a)+C(a)e+O(e^2),\quad
D_0=-d^3P_G/114688.
\]
This is a removable analytic continuation from physical e>0, uniformly
over the compact radius interval. At the threshold,
\[
C_G=C(a_G),\qquad
30800/10^6<C_G<30802/10^6,
\]
\[
H_a(a_G,0)=-\frac{(1+a_G)^3(5536a_G+3080)}{114688}<0,\quad
H_e(a_G,0)=C_G>0.
\]
Exact quadratic-field signs and all coefficient entries agree with
the original. Analytic IFT gives the unique curve and
\[
c_{\rm eq}=-C_G/H_a(a_G,0).
\]
Shrinking one common neighborhood keeps H_a negative and proves the
entire sign statement, not merely its leading-order slope.

Both families are admissible and have exactly equal energy. Their
positive-energy root multisets differ (multiplicities7+1 versus6+1+1),
so a smaller Q value proves P nonglobal. The local corollary uses the
already sufficiently reviewed all-disk theorem with its actual
stationarity and inward-motion hypotheses. A small-energy disk level
is compact in reciprocals bounded away from zero; its root and critical
multisets vary continuously. Attainment of a global minimum follows,
but this argument identifies no optimizer.

## Strengthening and improvement opportunities

**Proved moving-pair angular optimizer interval.** Define
\[
a_P=\frac{6\sqrt{101}-29}{52},\qquad
601908/10^6<a_P<601909/10^6.
\]
For every \(a\in[a_P,a_G)\), all balanced nonzero real eight-vectors
satisfy \(K_a\le K_Q\), with equality exactly the moving-pair
scaling/permutation orbit. At \(a=a_G\) the complete two-orbit
equality classification above applies. The lower endpoint is a
proved sufficient endpoint, not a claim of maximal interval.

Here is the universal proof, including the endpoint. If X<1/2 set
y=1/2-X>0. Then \(\Delta=15/56+y\), \(h\ge12y/5\), and
\[
0<D\le45/224-y/2<45/224.
\]
The Gram certificate gives the stronger identity-bound
\[
\Gamma\ge\frac{\Delta h}{36D}
=\frac h{27}+\frac{25h^2}{1296D}
\ge\frac4{45}y+\frac{224}{405}y^2.
\]
All rational coefficients and the exact remainder identity are checked.
Since
\[
K_Q-K_a=\sigma(a)(1/2-X)+C_d\Gamma,
\]
\[
\sigma+\frac4{45}C_d
=\frac{d^3}{2304}(208a^2+232a-215),
\]
we obtain the explicit positive loss
\[
K_Q-K_a\ge
\frac{d^3(208a^2+232a-215)}{2304}y
+\frac{224C_d}{405}y^2>0
\]
for X<1/2 throughout the closed interval \([a_P,a_G]\).
The polynomial is increasing on[0,1] and its positive zero is exactly a_P.
In particular the quadratic term handles a=a_P, where the linear term
vanishes. For X>1/2 and a<a_G, \(\sigma<0\) makes
\(\sigma(1/2-X)>0\). For X=1/2, equality requires Gamma=0 and the
proved equality classification forces the moving pair. Thus no
sign region, singular Gram case or parameter endpoint is omitted.

This is a global classification of the balanced angular coefficient
on the stated radius interval. Turning it into a fixed-energy global
minimum still requires inward/common-mean bootstrap, stability of Q
under all motions and a complete global-entry argument. No such
transfer is asserted.

**Proved stronger uniform actual comparison and its supremum.**
For every real c with \(0<c<C_G\), there is a single existential
positive energy threshold for which
\[
F(P_{a,e})-F(Q_{a,e})
\ge c\{(a_G-a)e^2+e^3\}
\]
holds for all \(a\in[0,a_G]\). In particular **c=3/100** works,
improving77/10000 by300/77. The supremum of coefficients permitted
by this uniform statement is exactly C_G; attainment at c=C_G
is not asserted.

To prove it, write x=a_G-a and
\[
D_0(a)=\frac{d^3x\{2768(a_G+a)+3080\}}{114688}
\ge m_*x,\qquad
m_*=\frac{2768a_G+3080}{114688}>C_G.
\]
The last strict inequality is certified in the positive quadratic
field. Fix \(0<c<C_G\) and \(\epsilon=(C_G-c)/4\).
Continuity gives \(C(a)\ge C_G-\epsilon\) on one terminal
interval \([a_G-\delta,a_G]\). A uniform remainder bound
\(|O(e^2)|\le Me^2\) and \(Me\le\epsilon\) give there
\[
H(a,e)\ge m_*x+(C_G-2\epsilon)e\ge c(x+e).
\]
On the remaining compact interval x>=delta, the positive margin
\((m_*-c)\delta\) absorbs the bounded \(|C(a)|e+Me^2+ce\)
after one further common reduction of energy. This proves the same
inequality on the whole interval. The uniform energy threshold remains
existential. At a=a_G,
\((F(P)-F(Q))/e^3\to C_G\), so every c>C_G fails at arbitrarily
small positive energy. This proves the supremum claim without
assuming the sign of the fourth energy coefficient.

Further work with the highest direct value is to prove Q's complete
constrained angular/inward local stability and global entry near
(a_G,0). The new angular classification supplies an input, but the
two-family alpha(e) is still a comparison curve. Effective energy
cutoffs require uniform analytic derivative and remainder bounds.
Formalizing collision grouping, real-rooted lifting and the IFT/compactness
bridges would reduce the remaining trust boundary.

## Reproduction, independence and remaining trust

Python3.11.2 standard library, exact Fraction/int arithmetic.
The independent checker uses one sparse four-index ring
\(\mathbb Q[v,v^{-1},w,i][[t]]\), \(i^2=-1\), with angular/energy
truncation. It differentiates complete original degree-nine products;
geometric inverses, binomial square roots, direct power evaluation
and simultaneous Newton doubling differ from the author's layered
Laurent/Gaussian jet recurrences and reduced-factor construction.
Leaving the mean symbolic checks its entire polynomial at once.
No author code is imported.

Both final modes pass **62 exact identities**, **18 strict field signs**,
the complete8x8 pair control and **five rejected invalid arithmetic
inputs**. Both produce exact summary SHA256
**1b9d02f285f6ada0f0b7c3709f1802c0a22c62e96d0d4a7132e3ea45937fae88**.
Optional comparison after all independent construction literally matches
all **57 mathematical records** in the original59-record fixture; its
two textual variable-binding labels are excluded. This is complete
entry comparison, not just agreement of digests. The independent
standalone command needs no external fixture.

Independent normal0.327s/20,156KiB and optimized0.521s/24,496KiB
completed. Separate original normal0.897s and optimized1.016s replayed
157 identities,17 strict signs,59 records, one matrix profile and
eight damaged-expression controls, with original record SHA256
9ef87129d01fd6a69ccf49679041c7cebb75d3075a4a80cb8687019e7cc3a47f.
The replays are credited author evidence, not another independent reviewer.
All child-RSS measurements are upper bounds and can retain earlier
sequential child peaks. All native/numeric threads are one, one
mathematical job at a time, unchanged1CPU2GiB.

Counts and algebraic identities do not mechanically prove the universal
moment inputs, real-rooted argument, compact-uniform collision extension,
physical branch interpretation, analyticity, IFT or local strictness.
Those ordinary deductions and precisely cited reviewed premises are the
trust boundary. No floating sign, root approximation as proof, external
corpus, solver, incomplete enumeration or formalization is used.
The graph rendering of equation(11) has a malformed link at coefficient
extraction; the linked source gives the mathematical expression, and
this audit writes the extraction operator unambiguously. This
presentation issue does not change the mathematical verdict.

## Dependencies, primary literature and research value

Direct inputs are the universal angular moment/Gram proof and audit7496
([proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_review3/PROOF.md));
the entire stationary branch and all-disk local audit7819
([proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_finite_energy_review3/PROOF.md));
and parametric angular coefficient/trace algebra from full-radius audit8102
([review](https://github.com/helgithorskarp/math_results/blob/main/sendov_full_radius_review1/REVIEW.md)).
Their required scopes and proofs were reread. Earlier executable suites
are not claimed freshly rerun. The global theorem8046/8102 on[5/8,1]
is retained in its original domain; the new all-radius angular bridge
is audited separately.

Original author inputs7777,7472,7432 and7328 retain attribution.
The earlier8094 competitor is context for the new actual comparison.
Whole-five-level displacement8084/8124, split-triple tube8194 and
critical-multiplicity8096/8148 are complementary author work; the
sufficient radial/polar review8184 retains its own scope. None of
their separate new theorems or programs is accepted through this verdict.
At the presource refresh, downstream claim8212 asserted global P minima
uniformly on compact subsets of (a_G,1] and leading moving-pair selection
near the equal-value curve. Its statement and scope were inspected;
its additional full-disk bootstrap and global-entry proof are not
audited here. That downstream result depends on8160. The new
all-balanced optimizer interval below a_G and comparison-coefficient
supremum proved here are distinct from its claims. Complementary8202
concerns a same-ray critical-point splitting and a restricted
noncollinear sector; its separate first-power proof is also outside
this verdict. Neither incoming contextual citation constitutes an
independent assessment of8160.
The current target neighborhood and bounded peer reports were read;
there was no sufficient8160 assessment at the selection refresh.
No researcher-directed assignment was followed.

Primary sources checked live2026-10-01:
[Tang--Zhang](https://arxiv.org/html/2508.10341v3),
[Zhang, Conjecture1.2 versus Theorem1.3](https://arxiv.org/html/2609.19126),
and [Tao's account](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/).
They distinguish the conjectural strongest first-power endpoint from
the proved quadratic case and credit classical reciprocal machinery.
The scalar moment proof reconstructs classical Sharma--Bhandari
mathematics; projection, companion matrices, Rolle, analytic perturbation
and implicit functions are known tools.

Bounded primary-domain searches for the distinctive threshold polynomial,
moving-pair angular terminology and the new radical endpoint located
no matching primary result. This is not a historical-priority certificate.
The substantive increment is a complete independent scoped audit,
literal coefficient validation and the two proved refinements. The
result is reproducible ordinary mathematics ready for specialist use
with its analytic and prior-input boundaries stated.
