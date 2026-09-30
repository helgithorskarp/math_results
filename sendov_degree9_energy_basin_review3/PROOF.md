# Independent audit of the sharp collapsed energy basin

Actual author **six-reviewer-3**, role **independent mathematical reviewer**,
2026-09-30. Ordinary analytic proof audit with independent exact algebra.
The shared signing identity does not establish distinct authorship; the
reviewer, selected scope and methodology are identified here explicitly.

## Definitions and the imported angular premise

Normalize the irrelevant leading coefficient to one and write
\[
p(z)=(z-a)\prod_{j=1}^8(z-z_j),\qquad 0<a<1,\quad |z_j|\le1,
\quad z_j\ne a.
\]
Thus the marked root is simple. Other roots and critical points may repeat;
all eight critical points are counted with algebraic multiplicity. Put
\[
a_0=5/8,\quad d=1+a,\quad v=1/d,\quad v_0=8/13,
\quad \kappa=d(a-a_0),\quad C_*={560235\over8388608},
\]
\[
u_j=(a-z_j)^{-1},\quad E=\sum|u_j-v|^2,\qquad
F=\sum_{p'(\zeta)=0}|a-\zeta|^{-1},\quad G=F-16v.
\]
The exclusion of a repeated marked root is essential to the definition of
\(E\). No simplicity hypothesis is imposed elsewhere.

We explicitly reuse the already reviewed angular theorem of
**six-sendov-2**. For
\[
\mathcal S=\{\theta\in\mathbb R^8:\sum\theta_j=0,\ \|\theta\|=1\},
\qquad z_j=-e^{it\theta_j},\quad a=a_0,
\]
its conclusion is
\[
G=-K(\theta)v_0^8t^4+o(t^4),                             \tag{1}
\]
uniformly on \(\mathcal S\), including collisions. The continuous
\(K\) has maximum \(C_*\), attained exactly on
\[
\mathcal O=\{\pm\text{permutations of }(7,-1,-1,-1,-1,-1,-1,-1)/\sqrt{56}\}.
\]
These are credited inputs, not new computations of this review. The
[prior independent angular audit](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_review3/PROOF.md)
also establishes, with \(p_8=10985/33554432\),
\[
\delta=C_*-K(\theta)\le14p_8/25
\quad\Longrightarrow\quad
\operatorname{dist}(\theta,\mathcal O)^2\le\delta/(64p_8).  \tag{2}
\]
Exact source and graph provenance appear in REVIEW.md and provenance.json.

## 1. Independent companion and second-order audit

Set \(\alpha_j=a-z_j\), and expand the original translated polynomial
\(p(a+y)=y\prod(y+\alpha_j)\). Then
\[
q^8p'(a-1/q)/p'(a)
=\sum_{k=0}^8(-1)^k(k+1)e_k(u)q^{8-k}.                  \tag{3}
\]
Its zeros are all critical reciprocals \(q=(a-\zeta)^{-1}\);
\(p'(a)=\prod\alpha_j\ne0\). This proves the elementary-symmetric
identity without assigning critical-root labels.

Let \(e=\mathbf1/\sqrt8\), \(Q=ee^*\), \(P=I-Q\),
\(S=P+3Q=I+J/4\). Every principal minor of
\(\operatorname{diag}(u)(I+J)\) of size \(k\) is
\((k+1)\prod u_j\). Similarity therefore realizes (3) as the
characteristic polynomial of
\[
B=S\operatorname{diag}(u)S=v(P+9Q)+V.                   \tag{4}
\]
This representation is classical. Our checker independently assembles
and differentiates the original translated polynomial, and compares all
nine coefficients with characteristic coefficients reconstructed from
exact matrix traces on five rational disk-root controls. Some controls
have repeated original roots. This finite check supplements (3), rather
than replacing its general derivation.

For roots sufficiently near \(-1\), use their unique small polar
coordinates
\[
z_j=-(1-\tau_j)e^{i\phi_j},\quad\tau_j\ge0,
\quad T=\sum\tau_j,\quad L=\sum\phi_j^2,\quad M=\sum\phi_j.
\]
Restrict \(a\) to a fixed closed neighborhood of \(a_0\). The identities
\[
|u_j-v|^2={v^2|z_j+1|^2\over|a-z_j|^2},\qquad
|z_j+1|^2=\tau_j^2+2(1-\tau_j)(1-\cos\phi_j)              \tag{5}
\]
give uniform localization as \(E\to0\), and locally
\(E\asymp L+\sum\tau_j^2\). All coefficients and denominators below
stay bounded uniformly on this neighborhood.

The near cluster of seven eigenvalues around \(v\) and the simple far
root around \(9v\) have a gap uniformly bounded away from zero. Riesz
moments \(M_k=\sum_{\mathrm{near}}(q-v)^k\) are jointly analytic in
the real parameters. No near-root labeling is required. Expansion gives
\[
u_j=v-iv^2\phi_j+v^2\tau_j+c_2\phi_j^2+\cdots,
\quad c_2=v^2/2-v^3,
\]
\[
\Re M_2=-v^4(3L/4+M^2/64)+O((T+L)^2).                  \tag{6}
\]
The trace identity behind (6) is
\(\operatorname{tr}(P\Phi P\Phi)=3L/4+M^2/64\).
Real analytic traces are even under simultaneous phase reversal, so
pure cubic phase terms vanish. Radial squares, radial-phase terms and
four phases have bounds \(T^2,TL,L^2\). Ten independently chosen rational
unbalanced-phase controls check the trace identity exactly.

For each near eigenvalue choose any normalized right eigenvector \(h\).
The far projected equation gives \(\|Qh\|=O(T+\sqrt L)\). The Hermitian
quadratic forms yield, for \(q-v=x+iy\),
\[
x=8v\|Qh\|^2+h^*\Re Vh=O(T+L),\qquad y=O(\sqrt L).
\]
Each eigenvalue has a right eigenvector, even at a defective collision;
we use these estimates separately and count algebraic multiplicities.
No eigenbasis or condition-number estimate enters. Consequently the
near moduli contribute \(-\Re M_2/(2v)+O((T+L)^2)\) beyond real parts.
The analytic far branch has
\[
\Im q_f=-9v^2M/8+O(T\sqrt L+L^{3/2}),
\quad |q_f|-\Re q_f=9v^3M^2/128+O((T+L)^2).
\]
Using \(\sum q=2\sum u_j\) gives the audited second-order formula
\[
G=2v^2T+\kappa v^4L+{5v^3\over64}M^2+O((T+L)^2).       \tag{7}
\]
Indeed \(2c_2+3v^3/8=v^3(a-5/8)=\kappa v^4\).
The far branch supplies nine of the ten units in the mean coefficient;
omitting it would invalidate the argument.

For \(a\ge a_0\), all three leading terms are nonnegative. If \(G<0\),
absorb the radial \(T^2,TL\) errors into the positive linear \(T\)
term. This forces \(L>0\), \(T=O(L^2)\), \(M^2=O(L^2)\), and
\(\kappa=O(L)\). The last assertion uses division by \(L\), which is
legitimate: \(L=0<T\) makes \(G>0\), and complete collapse has \(G=0\).

## 2. Audit of the collision-uniform joint quartic

Put \(c_0=M/8\), \(t=\|\phi-c_0\mathbf1\|\), and
\(\theta=(\phi-c_0\mathbf1)/t\). The controlled regime is
\[
t>0,\quad T=O(t^4),\quad c_0=O(t^2),\quad a-a_0=O(t^2).
                                                               \tag{8}
\]
Negative-gap sequences above satisfy it. We audit the lemma for every
configuration in (8), without imposing a negative gap.

For \(x=O(t^2),y=O(t)\), scalar expansion, followed by
\(y^2=x^2-\Re(x+iy)^2\), gives
\[
\sum_{\mathrm{near}}(|q|-\Re q)
=-{\Re M_2\over2v}+{\sum x^2\over2v}
  +{\Re M_3\over6v^2}-{\Re M_4\over8v^3}+O(t^6).        \tag{9}
\]
The third-moment factor is \(1/6\). Terms \(x^3,x^2y^2,y^6\) are
\(O(t^6)\); retaining their weights is needed for this remainder.

The analytic part
\(2\Re\sum u_j-\Re M_2/(2v)+\Re M_3/(6v^2)-\Re M_4/(8v^3)\)
has radial linear term \(2v^2T\), quadratic terms
\(\kappa v^4L+v^3M^2/128\), and a phase quartic continuous in \(a\).
Compare with \(a_0,\tau=0,\phi=t\theta\). Changing the marked radius
in the quartic costs \(O(|a-a_0|t^4)\), a mean phase costs
\(O(t^3|c_0|+|c_0|^4)\), and radial changes cost
\(O(Tt^2+T^2)\). All are \(o(t^4)\) under (8). Pure odd phase terms
vanish. The far modulus adds \(9v_0^3M^2/128+o(t^4)\).

The remaining term \(\sum x^2\) is not an analytic symmetric moment.
The following argument is the decisive audited trust boundary. Write
\(\Theta=\operatorname{diag}(\theta)\),
\(A=P\Theta P|_{e^\perp}\), and \(w=\Theta e\in e^\perp\).
The separated near/far graph construction gives
\[
B_{\mathrm{near}}=vI-iv^2At+t^2(C-iv^2\beta I)+O(t^3),
\quad\beta=c_0/t^2,
\]
\[
C=c_2A^2+(c_2+9v^3/8)ww^*.                            \tag{10}
\]
In particular \(P\Theta^2P=A^2+ww^*\), and the graph correction is
\(-PV_1QV_1P/(8v)=9v^3ww^*/8\), with
\(V_1=-iv^2S\Theta S\). Our rational matrix checks reproduce both
identities directly; the projection uses the entire far cluster, not an
assumed near eigenbasis.

For an \(A\)-eigenvector \(y\perp e\),
\((\Theta-\lambda I)y=\sigma e\). If \(\lambda\) is a diagonal value,
the corresponding coordinate forces \(\sigma=0\). Then \(y\) is
supported on that equal-value block, and
\(w^*y=\lambda e^*y=0\). If \(\lambda\) is not a diagonal value,
the solution space has dimension at most one. Thus every repeated
\(A\)-eigenspace has zero \(w\)-weight, and \(C\) compresses to the
scalar \(c_2\lambda^2I\) on it. This also proves continuity of the
needed real second coefficients at angular collisions.

More explicitly, take any sequence in (8), pass to
\(\theta_k\to\theta_0\), and group the eigenvalues of \(A_k\) by
distinct limiting eigenvalues of \(A_0\). Orthogonal group projections
converge. Only gaps between limiting groups are used to eliminate
intergroup couplings in \((B_{\mathrm{near}}-vI)/t\). Within a group,
the resulting matrix is
\[
-iv_k^2A_{k,\mathrm{group}}
 +t_k(C_{k,\mathrm{group}}-iv_k^2\beta_k I)+O(t_k^2).
\]
The leading matrix is anti-Hermitian. The real quadratic form of any
normalized right eigenvector kills that matrix and the imaginary mean
scalar. For a simple limiting group the real second coefficient has the
unique scalar compression limit. For a repeated group its limit is
\(c_2(a_0)\lambda_0^2\) for every eigenvalue in the group. This is
the same limit in the balanced cutoff configuration. Algebraic counts
agree by the separated group projections. Hence
\[
\sum x^2-\sum(x^{\mathrm{balanced}})^2=o(t^4)             \tag{11}
\]
on every subsequence, and therefore uniformly on bounded normalized
motions. There is no within-group gap assumption and no inference from
analytic traces alone. Finite equal-coordinate controls in the checker
exercise 135 pairs, but the preceding eigenspace argument covers all
collisions.

Finally \(E=v^4t^2+O(t^4)\). Combining (1), (9)--(11), with
\(\kappa=O(t^2)\), proves the audited joint expansion
\[
\boxed{G=\kappa E+{128\over169}T+{40\over2197}M^2
                      -K(\theta)E^2+o(E^2).}             \tag{12}
\]
Uniformity holds when the three normalized quantities in (8) are
bounded; directions and paths need not converge or be differentiable.

## 3. Sharp basin, actual crossing, and its quantifiers

Define \(R_E(a)\) as the supremum of the energies \(\rho\ge0\) such
that every admissible polynomial with \(E\le\rho\) has \(G\ge0\).
If the lower bound \(E\le\kappa/(C_*+\varepsilon)\Rightarrow G\ge0\)
failed for arbitrarily small \(a-a_0>0\), (5) would localize a violating
sequence, (7) would put it in (8), and (12) would give
\[
G/E^2\ge\kappa/E-C_*+o(1)\ge\varepsilon+o(1)>0,
\]
a contradiction. This proves the universal lower bound with an
existential neighborhood for every fixed \(\varepsilon>0\).

For the upper bound use the actual boundary-root polynomial
\[
p_{a,t}(z)=(z-a)(z+e^{7it})(z+e^{-it})^7.                \tag{13}
\]
Our independent calculation differentiates it in
\(y=\zeta-a\), setting \(\alpha=a+e^{7it},\beta=a+e^{-it}\).
Six critical points have \(y=-\beta\), and the remaining two solve
\[
9y^2+(8\alpha+2\beta)y+\alpha\beta=0.                  \tag{14}
\]
Their bases are \(-d\) and \(-d/9\); their implicit derivatives are
\(-8d\) and \(8d\), both nonzero. Recursively solving (14), taking
positive moduli and reciprocals, gives
\[
E=56v^4t^2+(-602v^4/3+2408v^5-2408v^6)t^4+O(t^6),
\]
\[
G=56(v^2-13v^3/8)t^2+
(-602v^2/3+7525v^3/3-6090v^4+65359v^5/16)t^4+O(t^6).
\]
These are exact Laurent identities in \(d\), not sampled radii. The
checker also derives the energy independently from (5), using
\(2v^2(1-\cos\phi)/(a^2+1+2a\cos\phi)\).
Consequently
\[
G=\kappa E-K_1(a)E^2+O(E^3),\qquad
K_1(a)={d^3\over7168}(516d^2-528d-393),\quad K_1(a_0)=C_*.
                                                               \tag{15}
\]

The two simple residual branches and their positive moduli are analytic
in \((a,t)\). Conjugation makes the sums even in \(t\), hence analytic
in \(h=t^2\). Since \(E_h(a_0,0)=56v_0^4>0\), the analytic inverse
theorem gives \(h=H(a,E)>0\) for small positive \(E\). Dividing the
gap by its removable factor \(E\) gives
\(g(a,E)=\kappa-K_1(a)E+O(E^2)\), with
\(g_E(a_0,0)=-C_*<0\). The analytic implicit theorem and local strict
monotonicity yield a positive crossing
\(E^*(a)=\kappa/C_*+O(\kappa^2)\), with \(G<0\) immediately above it.
Every such energy is attained by an actual (13). For any \(\rho>E^*\),
choose an attained energy between \(E^*\) and \(\rho\) in this small
neighborhood. Thus \(R_E(a)\le E^*(a)\), without assuming its supremum
is itself admissible. Together with the lower bound this confirms
\[
R_E(a)>0,\quad R_E(a)<\infty,\qquad
R_E(a)/\kappa\longrightarrow {8388608\over560235}.       \tag{16}
\]
For negative-gap sequences with \(E/\kappa\to1/C_*\), (12) is a
vanishing base term plus nonnegative radial, mean and angular losses.
Therefore \(T/E^2\to0\), \(M^2/E^2\to0\),
\(\operatorname{dist}(\theta,\mathcal O)\to0\), and \(G/E^2\to0\).
This is necessary failure geometry, not a finite-energy sign test.

## 4. Proved refinement: the minimum at every fixed energy scale

For \(\lambda>0\) and \(a>a_0\) close define
\[
V(a,\lambda)=\min_{E=\lambda\kappa}{G\over E^2},         \tag{17}
\]
where the minimum ranges over all admissible ordered disk-root tuples.
For every compact interval \(J\subset(0,\infty)\), the levels are
nonempty for all \(\lambda\in J\) and all sufficiently small \(a-a_0>0\),
the minima are attained, and
\[
\boxed{\sup_{\lambda\in J}
 \left|V(a,\lambda)-\left({1\over\lambda}-C_*\right)\right|
 \longrightarrow0.}                                    \tag{18}
\]
This applies below and above the sharp threshold, including positive-gap
minimizers. It is a refinement of the audited leading-order theorem.

**Existence and upper bound.** The analytic inverse in (15) realizes
each level \(E=\lambda\kappa\), uniformly for \(\lambda\in J\), in
the family (13). It gives
\[
V(a,\lambda)\le1/\lambda-K_1(a)+O(\lambda\kappa)
                  =1/\lambda-C_*+O(\kappa).             \tag{19}
\]
To see attainment, an energy level bounds
\(|u_j|\le v+\sqrt E\), so
\(|a-z_j|\ge(v+\sqrt E)^{-1}\). The level is therefore a closed
subset of the compact disk product, separated from every forbidden
\(z_j=a\). The critical multiset is continuous in polynomial
coefficients; alternatively (4) expresses \(F\) as a continuous sum
of eigenvalue moduli, even at collisions. Thus \(G\) attains its minimum.

**An extension of the failure-rate reduction.** In place of \(G<0\),
assume \(G\le C_0E^2\), where \(C_0\) is any fixed nonnegative
constant. By (5), \(E\le C(L+T^2)\), hence
\(E^2\le C'(L^2+T^4)\). For \(a\ge a_0\), (7) and the
positivity of its leading terms imply
\[
cT+c'M^2\le C_0E^2+C''(T+L)^2\le C'''(L^2+T^2).
\]
Shrink the neighborhood to absorb the \(T^2\) term into \(cT/2\).
This proves \(T=O(L^2)\) and \(M^2=O(L^2)\). If \(E>0\), then
\(L>0\), because \(L=0\) forces \(T=0\) in this inequality.
Now \(t^2=L-M^2/8\sim L\). On a fixed level with \(\lambda\in J\),
\(\kappa=E/\lambda=O(L)\); the constants are uniform on \(J\).
Thus all configurations with a bounded normalized gap on these levels
satisfy (8). This step is the extra lemma needed beyond a negative-gap
argument.

**Lower bound and uniformity.** By (19), actual minimizers have
\(G/E^2\le C_0\) for a single \(C_0\) uniform on \(J\). The
preceding reduction applies. Formula (12), with \(E=\lambda\kappa\),
then gives
\[
G/E^2=1/\lambda-C_*+
 {128\over169}{T\over E^2}+{40\over2197}{M^2\over E^2}
 +(C_*-K(\theta))+o(1)\ge1/\lambda-C_*+o(1).             \tag{20}
\]
Its remainder is uniform: every sequence of such minimizers, even with
varying \(\lambda\in J\), has bounded normalized motions. Failure of
uniform convergence would select a sequence contradicting (12) and
(19). This proves (18). No new cubic remainder estimate is used.

**Near-minimizer geometry.** Suppose \(a_k\downarrow a_0\),
\(\lambda_k\in J\), \(E_k=\lambda_k\kappa_k\), and
\[
G_k/E_k^2-(1/\lambda_k-C_*)\longrightarrow0.
\]
The same bounded-gap reduction and (20) show
\[
T_k/E_k^2\to0,\qquad M_k^2/E_k^2\to0,
\qquad \operatorname{dist}(\theta_k,\mathcal O)\to0.     \tag{21}
\]
In particular these conclusions hold for exact minimizers. Once the
angular loss is in the window of (2), the credited quantitative bound
also gives
\[
{128\over169}{T_k\over E_k^2}+{40\over2197}{M_k^2\over E_k^2}
 +64p_8\operatorname{dist}(\theta_k,\mathcal O)^2
\le {G_k\over E_k^2}-{1\over\lambda_k}+C_*+o(1).         \tag{22}
\]
The \(o(1)\) has no certified numerical rate here. This is asymptotic
coercivity, not an explicit finite neighborhood or a higher-order basin
coefficient.

## Trust boundary

The uniform estimates, spectral grouping, variational compactness and
inverse/implicit-function steps above are ordinary mathematics; they are
not checked by a proof assistant or by finite matrix controls. The
credited angular theorem is explicitly imported from an earlier
independent review. The new checker imports no author modules and uses
only exact Python standard-library rational arithmetic. It checks the
actual singleton family symbolically for every positive \(d\), seven
independently chosen nonlinear profiles, and the stated rational matrix
controls. These establish exact algebra, not an enumeration of all disk
polynomials. The global first-power inequality \(F\ge8\), an optimal
maximum original-root displacement basin, and the exact second-order
coefficient of the universal energy basin remain outside this review.
