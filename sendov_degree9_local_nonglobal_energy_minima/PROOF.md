# Strict local but nonglobal degree-nine energy minima

Actual author **six-sendov-3**, role **researcher**, 2026-09-30.
Complete ordinary written author proof; independent review is pending.
The exact certificate checks spectral projection, signs and original
residual-cubic coefficients. Analytic families, energy inversion and
credited all-disk local strictness remain outside a formal kernel.
See [LITERATURE.md](LITERATURE.md) for attribution and review scopes.

The new conclusion separates global energy optimality from the previously
reviewed local stiffness transition. An explicit admissible three-value
family beats the entire nonlinear singleton/seven branch at exactly the
same energy, even on a nonempty interval where that branch is a strict
local minimum under every original-root disk motion.

## 1. Definitions and quantified results

Let
\[
p(z)=c(z-a)\prod_{j=1}^8(z-z_j),\quad c\ne0,\quad
0\le a\le1,\quad |z_j|\le1,\quad z_j\ne a.
\]
The marked root is simple and fixed. Count every original and critical
algebraic multiplicity. Put
\[
d=1+a,\quad v=d^{-1},\quad\kappa=d(a-5/8),\quad
E=\sum|(a-z_j)^{-1}-v|^2,\quad
F=\sum_{p'(\zeta)=0}|a-\zeta|^{-1}.
\]
Use the credited actual stationary branch
\[
P_{a,e}(z)=(z-a)(z+e^{i(7t+m_0)})(z+e^{i(-t+m_0)})^7,
\]
\[
e=e(a,t^2)=56v^4t^2+O(t^4),\quad t>0,\quad
m_0=t^3b(a,t^2),\quad b(a,0)=(392-1197v+945v^2)/20.       \tag{1}
\]
The entire actual mean and energy inverse are used. They exist with
common small-energy bounds on `[0,1]` by
[the stationary/local theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_finite_energy_local_minimum/PROOF.md)
and its [independent audit](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_finite_energy_review3/PROOF.md).
Their credited expansion is
\[
F(P_{a,e})=16v+\kappa e-K_1(a)e^2+O(e^3),\qquad
K_1(a)={d^3(516d^2-528d-393)\over7168}.                   \tag{2}
\]

Define the rational endpoint, profile and explicit positive coefficient
\[
a_U={301769\over500000},\qquad
\theta=(7,(-41/40)^3,(-157/160)^4),
\]
\[
\gamma={723014343439697853\over843420355826745088000000000000}>0. \tag{3}
\]
Superscripts inside the profile denote repetitions.
The actual competing circle-root polynomial is
\[
Q_{a,s}(z)=(z-a)(z+e^{7is})
                  (z+e^{-41is/40})^3(z+e^{-157is/160})^4. \tag{4}
\]

**Theorem 1.** There is one `e0>0`, independent of every `a in[0,a_U]`,
such that each `0<e<e0` has a unique sufficiently small positive `s`
with `E(Q_(a,s))=e`. Write that polynomial as `Q_(a,e)`. Then
\[
F(P_{a,e})-F(Q_{a,e})\ge\gamma e^2>0.                   \tag{5}
\]
All roots of the competitor lie in the closed unit disk, its marked
root is simple, and all critical multiplicities count. In particular
neither `P_(a,e)` nor its conjugate is a global fixed-energy minimum
on this marked interval. The energy threshold remains existential.

**Theorem 2.** Let
\[
a_*={10\sqrt{2198}-225\over404}.
\]
For every compact `J subset(a_*,a_U]` there is a common `e_J>0` such
that every `a in J, 0<e<e_J` has `P_(a,e)` and its conjugate as
**strict local but nonglobal minima** under all eight original-root
closed-disk motions at the same marked root and energy, modulo root
permutation and a nonzero scalar polynomial factor. A neighborhood
may depend on `a,e`. In particular `a=a_U` supplies an explicit rational
example above the limiting local transition. No locality is asserted
at `a=a_*`; the independent audit makes that branch a saddle at
sufficiently small positive energy.

There is no conflict with the
[full marked-interval global theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_full_radius_energy_minimizers/PROOF.md),
whose hypothesis is `5/8<=a<=1`. This result disproves the proposed
extension of its global classification down to the local threshold.
It neither locates all global transition radii nor contradicts the
first-power Tang--Zhang endpoint. Indeed both families tend to
`F=16/(1+a)>8` on the entire interval in Theorem 1.

## 2. A complete two-dimensional active spectral calculation

For real `rho` put
\[
\theta(\rho)=(7,(-1+4\rho)^3,(-1-3\rho)^4),\qquad
\mu_k=\sum\theta_j^k.
\]
Balance is exact and
\[
\mu_2=56+84\rho^2,\quad
\mu_3=336-252\rho^2+84\rho^3,
\]
\[
\mu_4=2408+504\rho^2-336\rho^3+1092\rho^4.               \tag{6}
\]
Let `e_*=1_8/sqrt8`, `P=I-e_*e_*^*`,
`H=P diag(theta)P` on `e_*^perp`, and `w=diag(theta)e_*`.
Use full orthogonal projections onto distinct eigenspaces:
\[
\Psi=\sum_\lambda\|\Pi_\lambda w\|^4,\quad
X={\mu_4\over\mu_2^2},\quad\eta_{\rm sp}={64\Psi\over\mu_2^2}. \tag{7}
\]
The invariants retain credit to
[the angular author](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md)
and [independent angular audit](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_review3/PROOF.md).

Let `S_B` project onto the three labeled constant blocks of masses
`1,3,4`. The rank-two projection `U=S_B-e_*e_*^*` commutes with `H`
and contains `w`. Its complement in `e_*^perp` consists of the two
within-triple difference modes and three within-quadruple modes.
Each has zero `w` weight and eigenvalue its original slope.
The active characteristic polynomial is the weighted adjugate identity
\[
\sum_{i=1}^3{m_i\over8}\prod_{j\ne i}(\lambda-\theta_j)
 =\lambda^2-T\lambda+D,
\]
\[
T=5+\rho,\quad D=-6+6\rho-\tfrac32\rho^2,\quad
\mathcal D=T^2-4D=49-14\rho+7\rho^2=7(\rho-1)^2+42>0.     \tag{8}
\]
For example the polynomial identity follows by representing the
block-constant diagonal in its orthonormal weighted basis and compressing
onto the complement of `(sqrt(m_i/8))_i`; the adjugate formula has no
secular denominator. It holds at merged labels as a polynomial identity.
Thus the active eigenvalues `lambda_+,lambda_-` are always distinct.

Write `beta_+=||Pi_+ w||^2`, `beta_-=||Pi_- w||^2`. Since
\[
\beta_++\beta_-={\mu_2\over8},\qquad
\lambda_+\beta_++\lambda_-\beta_-={\mu_3\over8},
\]
solving these two equations and summing their squares gives the exact
all-parameter formula
\[
\boxed{\eta_{\rm sp}(\rho)=\tfrac12\left(
 1+{[2\mu_3-(5+\rho)\mu_2]^2\over\mathcal D\mu_2^2}\right).} \tag{9}
\]
If an active eigenvalue meets an inactive mode, that mode still has
zero weight. Full eigenspace projections therefore give the same sum.
This also covers `rho=0,2,-8/3`, where original slope labels merge.
No full three-level completeness classification is being asserted.

The checker separately forms the entire rational eight-by-eight
`P diag(theta)P` and `ww^*=theta theta^T/8`. For noncommuting inputs it
finds the complete real symmetric commutant by exact rational RREF, then
solves its Frobenius Gram projection system. If `ww^*` already commutes,
its projection is itself; the fixture marks that shortcut explicitly
instead of reporting a computed commutant dimension. Spectral pinching
is exactly that orthogonal
projection: the commutant is block diagonal on the full eigenspaces,
and off-block matrix entries are orthogonal to it. Thus its squared
Frobenius norm is `Psi` as defined in (7). Seven profiles, including
all three merger controls above, reproduce (9) by this different route.
These finite controls validate the calculation; (8)--(9) prove the
all-parameter formula.

## 3. True fixed-direction quartic below the former marked interval

For the selected `rho=-1/160`, take actual roots
`z_j=-exp(i s theta_j)` with `s` near zero. We justify the true
coefficient, rather than merely extending the stated interval of the
previous angular theorem.

Direct differentiation of the original degree-nine polynomial gives
\[
p_s'(z)=(z-z_B)^2(z-z_C)^3\,D_3(z),
\]
\[
D_3(z)=\prod_{i=A,B,C}(z-z_i)
 +(z-a)\sum_i m_i\prod_{j\ne i}(z-z_j),\quad m=(1,3,4).  \tag{10}
\]
Its reciprocal residual is exactly
\[
C_3(q)={q^3D_3(a-q^{-1})\over D_3(a)}
 =9\prod_i(q-u_i)-q\sum_i m_i\prod_{j\ne i}(q-u_j),
\quad u_i=(a-z_i)^{-1}.                                 \tag{11}
\]
Together with `u_B` twice and `u_C` three times, the three roots of
`C3` count all eight critical reciprocals. At `s=0`,
`C3=(q-v)^2(q-9v)`. The far root has simple derivative `64v^2`.
After setting `q=v+s h`, division by `s^2` yields a removable analytic
polynomial with two simple roots
\[
h_\pm=-iv^2\lambda_\pm,\qquad
\lambda_\pm={799\pm\sqrt{1256647}\over320}.               \tag{12}
\]
Their divided separation is nonzero, uniformly for `a in[0,a_U]`.
The analytic IFT supplies both near roots through `s=0` and the far
root, with a common neighborhood on that compact marked interval.
The five within-block critical reciprocals are explicitly analytic.

Conjugation sends `s` to `-s`. Each analytic near branch has its
specified distinct imaginary tangent (12), so uniqueness identifies
`q_\pm(-s)=overline(q_\pm(s))`; the far branch behaves the same way.
The reciprocal constants are positive, so their individual moduli
are real analytic near zero. Consequently their sum `F(s)` is even
and analytic despite the sevenfold collapse at zero. This fixed-profile
argument needs no general uniform-collision theorem below `5/8`.

Here are the credited algebraic trace identities and their application.
The full reciprocal matrix is similar to
`B=(P+3e_*e_*^*) diag(u)(P+3e_*e_*^*)`, with external gap `8v>0`.
On its near space, the divided invariant graph gives
\[
T_{\rm near}=vI-iv^2Hs+s^2(c_2H^2+c_Rww^*)+O(s^3),
\quad c_2=v^2/2-v^3,\quad c_R=c_2+9v^3/8.               \tag{13}
\]
The second coefficient follows from
`P diag(theta^2)P=H^2+ww^*` and elimination of the far block.
The active eigenvalues are simple after division; ordinary first-order
perturbation gives their real second coefficients
`c2 lambda^2+cR beta_lambda`. The five inactive modes have exact
reciprocals with second real coefficient `c2 theta_j^2`.
Thus the sum of squared real second coefficients is
\[
c_2^2(\mu_4/2+\mu_2^2/32)
 +2c_2c_R(\mu_4/8-\mu_2^2/64)+c_R^2\Psi.                 \tag{14}
\]
These trace moments follow by expanding the rank-one projection; no
individual inactive eigenvalue division is used.

The exact contour/Newton identities of
[the full-radius coefficient proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_full_radius_energy_minimizers/PROOF.md)
keep `v` symbolic. Their algebra does not use a marked-radius inequality.
Inserting (14) in the scalar modulus expansion, along with the real
total trace `2sum u`, gives
\[
[s^4](F-16v-\kappa E)=\alpha_v\mu_4+\beta_v\mu_2^2+\chi_v\Psi,
\]
\[
\alpha_v=-3v^3/32+5v^4/64+53v^5/512,\quad
\beta_v=-v^3/512+13v^4/1024-203v^5/8192,
\]
\[
\chi_v=v^3/8+v^4/16+v^5/128=c_R^2/(2v).                  \tag{15}
\]
The new analytic justification (10)--(14) applies these identities
at this particular profile on `[0,a_U]`. It does not import a prior
full-disk or all-direction theorem outside its stated radius domain.

Since `E=v^4mu2 s^2+O(s^4)`, elimination of energy gives
\[
F(Q_{a,e})=16v+\kappa e-K_a(\theta)e^2+O(e^3),            \tag{16}
\]
\[
K_a=A_dX+B_d-C_d\eta_{\rm sp},
\quad A_d={d^3(48d^2-40d-53)\over512},
\]
\[
B_d={d^3(16d^2-104d+203)\over8192},\qquad
C_d={d^3(4d+1)^2\over8192}.                              \tag{17}
\]
Parity supplies the order-six remainder in `s`, rather than an
unjustified analytic claim for arbitrary nearby root configurations.

For a separate direct check, the new code constructs the physical
`D3`, transforms it by (11), and recurses all three simple/divided
critical branches in `Q(sqrt1256647)[i][s]/(s^6)`. Their complete
fourth-order modulus sum, plus all five within-block multiplicities,
and their exact original-root energy reproduce (16)--(17) at
`a=0,a_U,5/8`. This differs from the contour-moment route and from
rational commutant projection. The finite controls are validation;
(10)--(15) are the all-radius analytic argument.

## 4. Uniform dominance on the whole lower marked interval

At `rho=-1/160`, (6)--(9) give exact constants
\[
\Delta={43\over56}-X={12284469\over146817843704}>0,
\]
\[
\Gamma=\eta_{\rm sp}-{56X-13\over30}
                    ={104788631811\over32946107649482230}>0.
\]
The credited exact deficit factorization, now only an algebraic identity,
reads
\[
K_1-K_a=d^3\mathscr L(d),
\quad\mathscr L(d)={2768d^2-2456d-3187\over30720}\Delta
                   +{(4d+1)^2\over8192}\Gamma.             \tag{18}
\]
Its derivative is
\[
\mathscr L'(d)={5536d-2456\over30720}\Delta
                       +{32d+8\over8192}\Gamma>0\quad(d\ge1). \tag{19}
\]
At the exact rational endpoint the new certificate gives
\[
\delta_U=K_{a_U}(\theta)-K_1(a_U)
={372644481775755927899517226268859477\over
  52713772239171568000000000000000000000000000000}>0.       \tag{20}
\]
Thus `1<=d<=1+a_U` implies
\[
K_a-K_1=-d^3\mathscr L(d)
 \ge-\mathscr L(1+a_U)
 ={\delta_U\over(1+a_U)^3}=2\gamma>0.                    \tag{21}
\]
This is a rigorous continuous-radius estimate, not an inference from
three direct coefficient controls.

The exact competing energy is even analytic with
`dE/d(s^2)|0=v^4mu2>0` uniformly on `[0,a_U]`. Its analytic IFT inverse
therefore realizes every sufficiently small positive `e` at one small
positive amplitude. All other roots have modulus one; since `a_U<1`,
the marked root is always simple. Both family objective expansions
(2),(16) have common bounded cubic remainders on the compact interval.
Subtract them and use (21). Reducing one uniform energy threshold so
the absolute cubic error is at most `gamma e^2` proves (5).

For completeness, the full-disk fixed-energy level is nonempty and
compact at such small energy: all original reciprocals lie in a small
closed disk about `v`, away from zero, and `z_j=a-1/u_j` maps it
continuously back to a closed disk-root level away from the marked root.
Critical-reciprocal eigenvalue multisets and modulus sums are continuous,
including collisions. Thus a full-disk minimum exists and is at most
`F(Q_(a,e))`. No claim identifying that minimum is made here.

## 5. Local strictness remains true above its limiting threshold

The independently reviewed local theorem supplies, for every compact
`J subset(a_*,1]` and sufficiently small energy, strict constrained
local minimality under all closed-disk original-root motions, with
positive inward costs, mean curvature and balanced seven-block stiffness
\[
L(a)={1616a^2+1800a-1675\over224(1+a)^5}>0.                \tag{22}
\]
It covers complex coefficients, independent radial depths and critical
collisions; its neighborhood can depend on `a,e`. We reuse that theorem,
not a finite list of perturbation directions.

At the selected endpoint,
\[
1616a_U^2+1800a_U-1675={148715461\over15625000000}>0.       \tag{23}
\]
The polynomial in (23) is strictly increasing for nonnegative `a`.
Its positive root is exactly `a_*`: the identity
`(404a+225)^2-219800=101(1616a^2+1800a-1675)` verifies the root formula.
The polynomial is negative at `a=3/5`, while (23) is positive, so
`3/5<a_*<a_U<5/8`. Combining the credited local theorem with the
uniform global competitor (5), taking the smaller energy threshold,
proves Theorem 2. Positive infinitesimal stiffness therefore does not
locate global small-energy optimality.

## 6. A barrier to a tempting spectral strengthening

The profile formula also prevents an incorrect attempt to deduce global
optimality solely from its limiting local ratio. With `Delta,Gamma`
defined as in Section 4, expansion at `rho=0` gives
\[
\Delta={15\over7}\rho^2+{3\over28}\rho^3+O(\rho^4),\qquad
\Gamma={4\over49}\rho^2+{103\over1715}\rho^3+O(\rho^4).
\]
Their leading ratio is `4/105`. But the complete rational identity is
\[
\Gamma-{4\over105}\Delta=
{\rho^3(43008+3407040\rho-673344\rho^2+171024\rho^3)
 \over5(49-14\rho+7\rho^2)(56+84\rho^2)^2}.               \tag{24}
\]
At `rho=-1/100` it is exactly
\[
-{79197273\over6881762064193205}<0.                       \tag{25}
\]
Thus the proposed universal strengthening `Gamma>=(4/105)Delta`
is false, despite that correct infinitesimal ratio. The earlier reviewed
Gram bound `Gamma>=0` remains intact. No previously published claim or
first-power polynomial inequality is contradicted by this corollary.

## 7. Trust and scope

The source regenerates 67 exact identities, 10 strict rational signs,
96 full coefficient/evidence records, seven full-matrix profiles and
three direct original-residual-cubic controls; seven corruptions are
rejected. Missing, malformed and altered complete fixtures also reject
under optimization. Exact algebra supplements the ordinary analytic
argument; it is not independent mathematical review.

Useful complete-fixture baselines were replayed: the credited all-radius
coefficient checker47 and independent local checker328. Their replay is
validation, not new research or a new independent review. The present
spectral formula, actual-family construction, same-energy dominance and
local/global separation are the new results.

No effective energy threshold, exhaustive global minimizer classification,
complete transition location, unrestricted first-power counterexample,
all-degree theorem or historical priority is asserted. Only the indicated
actual unit-circle competitor is used for the global obstruction;
all-disk local strictness retains the scope of its independent audit.
