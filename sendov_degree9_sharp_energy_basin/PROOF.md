# The sharp all-disk energy basin at the degree-nine collapsed cutoff

Author **six-sendov-3**, role **researcher**, 2026-09-30.
Status: ordinary written proof, with exact author symbolic algebra controls;
independent review pending. The uniform spectral and completeness bridges
are not formalized. The reviewed angular theorem is credited below.

## 1. Statement and prior inputs

Let
\[
 p(z)=c(z-a)\prod_{j=1}^8(z-z_j),\qquad
 c\ne0,\quad 0<a<1,\quad |z_j|\le1,
\]
with a simple marked root \(a\). Critical points are counted with algebraic
multiplicity. Set
\[
 a_0=5/8,\quad d=1+a,\quad v=d^{-1},\quad
 \kappa=d(a-a_0),\quad C_*={560235\over8388608},
\]
\[
 u_j=(a-z_j)^{-1},\quad
 E_a=\sum_{j=1}^8|u_j-v|^2,\quad
 F_a=\sum_{p'(\zeta)=0}|a-\zeta|^{-1},\quad G_a=F_a-16v.
\]
All reciprocals in these definitions are finite: the marked root is simple,
and hence is not critical. Repeated other roots and repeated critical points
are allowed. A repeated marked root has \(F_a=+\infty\) under the standard
convention, but its original-root energy is undefined; it is excluded from
the quantifiers. Rotating the polynomial gives the equivalent statement for
a marked root of modulus \(a\), centered at its opposite unit point.

Define the **energy basin**
\[
 \mathcal R_E(a)=\sup\{\rho\ge0:
      G_a\ge0\text{ for every such }p\text{ with }E_a\le\rho\}.
                                                               \tag{1}
\]
This is a threshold in squared reciprocal displacement. Its square root is
the radius in the Euclidean reciprocal norm. It is a different metric from
\(\max_j|z_j+1|\); no optimal maximum-original-root basin is asserted.
Radius zero is admissible: it forces \(z_j=-1\), and then \(F_a=16v\).
Admissible radii form an initial interval, whether or not its endpoint is
admissible.

**Theorem 1 (sharp energy basin).** For \(a>a_0\) sufficiently close,
\(0<\mathcal R_E(a)<\infty\), and
\[
 \boxed{\lim_{a\downarrow5/8}{\mathcal R_E(a)\over(1+a)(a-5/8)}
       ={1\over C_*}={8388608\over560235}.}                    \tag{2}
\]
More precisely, for every \(\varepsilon>0\), some \(\eta_\varepsilon>0\)
has the following property:
\[
 a_0<a<a_0+\eta_\varepsilon,\quad
 E_a\le{\kappa\over C_*+\varepsilon}
                 \quad\Longrightarrow\quad G_a\ge0           \tag{3}
\]
for **every** disk-root polynomial above. There is also a single explicit
boundary family whose first small crossing energy is
\[
 E^*(a)={\kappa\over C_*}+O(\kappa^2),\qquad
                     \mathcal R_E(a)\le E^*(a).               \tag{4}
\]
No numerical size of these analytic neighborhoods is claimed.

The existing angular input is due to **six-sendov-2**, with the collision
bridge and optimizer independently audited by **six-reviewer-3**. On
\[
 \mathcal S_8=\{\theta\in\mathbb R^8:
                         \sum\theta_j=0,\ \sum\theta_j^2=1\},
\]
the fixed-cutoff boundary roots \(-e^{it\theta_j}\) satisfy uniformly
\[
 G_{a_0}=-K(\theta)v_0^8t^4+o(t^4),\quad v_0=8/13,
 \qquad K(\theta)\le C_*,                                  \tag{5}
\]
where \(K\) is continuous. Its maximum set is exactly
\[
 \mathcal O=\{\pm\text{permutations of }
                                (7,-1,\ldots,-1)/\sqrt{56}\}.
\]
These formulae and their optimizer are prior results, not claims of this
contribution. The author's preceding full-disk cutoff proof supplies the
spectral mechanism being extended here. Sections 2–4 repeat the needed
argument with the marked radius varying; a fixed-radius expansion alone
does not imply the joint estimate. Exact source provenance and status are
in LITERATURE.md.

## 2. A uniform varying-radius second-order reduction

Restrict \(a\) to one small closed interval about \(a_0\). Near collapse,
write the original roots uniquely as
\[
 z_j=-(1-\tau_j)e^{i\phi_j},\quad \tau_j\ge0,\quad
 T=\sum\tau_j,\quad M=\sum\phi_j,\quad L=\sum\phi_j^2.
\]
All estimates below are uniform on this interval and one fixed root
neighborhood, including collisions within the near critical cluster.
The inverse-map identity
\[
 |u_j-v|^2={v^2|z_j+1|^2\over|a-z_j|^2},\quad
 |z_j+1|^2=\tau_j^2+2(1-\tau_j)(1-\cos\phi_j)
\]
gives
\[
 E_a\asymp L+\sum\tau_j^2.                                 \tag{6}
\]
It also gives uniform localization: if \(a\to a_0\) and \(E_a\to0\),
every \(z_j\to-1\). Indeed
\(|z_j+1|=|u_j-v|\,|a-z_j|/v\), whose last two factors are
uniformly bounded for disk roots and these \(a\).

**Lemma 2.** Uniformly in this neighborhood,
\[
 \boxed{G_a=2v^2T+\kappa v^4L+{5v^3\over64}M^2
                               +O((T+L)^2).}                 \tag{7}
\]
Here is the spectral derivation. Let \(e=\mathbf1/\sqrt8\), \(Q=ee^*\),
\(P=I-Q\), \(H=I+J=P+9Q\), and \(S=P+3Q\).
The critical reciprocals are precisely the eigenvalues of
\[
 B=S\operatorname{diag}(u)S=vH+V.
\]
This classical reciprocal companion identity also follows directly from
\(e_k(q)=(k+1)e_k(u)\), obtained by differentiating the translated
polynomial. Every principal minor of \(\operatorname{diag}(u)H\) on a
\(k\)-element set is \((k+1)\prod u_j\); similarity by \(S\) gives
the displayed matrix. Its determinant is \(9\prod u_j\ne0\).

The near cluster of seven eigenvalues about \(v\) and the simple far
branch about \(9v\) are separated by \(8v\), bounded uniformly away
from zero. Contour resolvents centered at the moving \(v\) therefore
define jointly analytic symmetric moments
\(M_k=\sum_{\rm near}(q-v)^k\) and an analytic far root. No individual
near root labels are used. Expand
\[
 u_j=v-iv^2\phi_j+v^2\tau_j+c_2\phi_j^2+\cdots,
                    \qquad c_2=v^2/2-v^3.                   \tag{8}
\]
Conjugation sends all phases to their negatives and preserves real \(a\)
and radial variables. Thus real analytic traces have no Taylor monomials
of odd total phase degree. The resolvent expansion and this parity give
\[
 \Re M_2=-v^4\left({3\over4}L+{M^2\over64}\right)
                                          +O((T+L)^2),
\]
using \(\operatorname{tr}(P\Phi P\Phi)=3L/4+M^2/64\).
The stated error bounds radial squares, radial times two phases, and four
phases by \(T^2,TL,L^2\), respectively; the real cubic phase terms vanish.

For any normalized right near eigenvector \(h\), its projected equation
gives \(\|Qh\|=O(T+\sqrt L)\). The real and imaginary quadratic forms
then give, for \(q-v=x+iy\),
\[
 x=8v\|Qh\|^2+h^*\Re Vh=O(T+L),\qquad y=O(\sqrt L).
                                                               \tag{9}
\]
The matrices denoted by real and imaginary parts are their Hermitian
parts. These estimates require no eigenbasis or eigenvector conditioning.
Scalar modulus expansion consequently gives
\[
 \sum_{\rm near}(|q|-\Re q)=-\Re M_2/(2v)+O((T+L)^2).
\]
For the far root,
\[
 \Im q_f=-9v^2M/8+O(T\sqrt L+L^{3/2}),\quad
 |q_f|-\Re q_f=9v^3M^2/128+O((T+L)^2).
\]
Finally \(\sum q=2\sum u\). The coefficients are therefore
\[
 2v^2T,\qquad
 \left(2c_2+{3v^3\over8}\right)L
       =v^3(a-5/8)L=\kappa v^4L,\qquad
 {10v^3\over128}M^2.
\]
This proves (7). Unlike the fixed-cutoff cancellation, its angular
quadratic term is positive when \(a>a_0\).

**Corollary 3 (rates forced by failure).** If \(a\ge a_0\), \(G_a<0\),
and the roots are sufficiently near collapse, then \(L>0\) and
\[
 T=O(L^2),\qquad M^2=O(L^2),\qquad \kappa=O(L).              \tag{10}
\]
All constants are uniform in \(a\). The three displayed leading terms
in (7) are nonnegative with their \(T,M^2,L\kappa\) coefficients
bounded below by positive constants. Shrink the root neighborhood to
absorb \(CT^2+2CTL\) into half the positive radial term. It follows
that \(T\le C_1L^2\); substitution gives the other two inequalities,
the last after division by \(L>0\). If \(L=0<T\), the radial term
makes \(G_a>0\); if \(T=L=0\), the gap is zero.

## 3. The joint sharp expansion, including all collisions

Put
\[
 c_0=M/8,\quad t=\|\phi-c_0\mathbf1\|,
       \quad\theta=(\phi-c_0\mathbf1)/t\in\mathcal S_8.
\]
On negative-gap sequences approaching \(a_0\), (10) and
\(L=t^2+M^2/8\) imply \(t>0\),
\[
 T=O(t^4),\quad c_0=O(t^2),\quad a-a_0=O(t^2).               \tag{11}
\]
The following lemma holds under the controlled assumptions (11) even
without a negative gap, and permits either sign of \(a-a_0\).

**Lemma 4 (joint expansion).** Uniformly over sequences with (11),
\[
 \boxed{G_a=\kappa E_a+{128\over169}T+{40\over2197}M^2
                           -K(\theta)E_a^2+o(E_a^2).}        \tag{12}
\]
Uniformity means that the error divided by \(E_a^2\) tends to zero
when the three normalized quantities in (11) stay bounded. Directions
and normalized motions need not converge, and no smooth path is assumed.

To prove it, write \(x=\Re(q-v),y=\Im q\) for the near roots. By (9),
\(x=O(t^2),y=O(t)\). Their scalar modulus identity is
\[
 \sum_{\rm near}(|q|-\Re q)=
 -{\Re M_2\over2v}+{\sum x^2\over2v}
       +{\Re M_3\over6v^2}-{\Re M_4\over8v^3}+O(t^6).       \tag{13}
\]
Define the real analytic expression
\[
 \mathcal H=2\Re\sum u_j-\Re M_2/(2v)
                         +\Re M_3/(6v^2)-\Re M_4/(8v^3).
\]
Its constant is \(16v\), its radial linear part is \(2v^2T\), and
its phase quadratic is \(\kappa v^4L+v^3M^2/128\).
Its pure phase quartic is a homogeneous polynomial with coefficients
continuous in \(a\). Comparing to the balanced cutoff configuration
\(a=a_0,\tau=0,\phi=t\theta\), denote its expression by \(\mathcal H_b\).
Taylor expansion with (11) gives
\[
 \mathcal H-16v-(\mathcal H_b-16v_0)
     =2v_0^2T+\kappa v^4t^2+v_0^3M^2/128+o(t^4).            \tag{14}
\]
Indeed changing the quartic's coefficients costs \(O(|a-a_0|t^4)\);
changing its phases costs \(O(t^3|c_0|+|c_0|^4)\).
Radial-quadratic-phase and radial-square terms cost \(O(Tt^2+T^2)\).
The replacements of \(v\) by \(v_0\) in radial and mean coefficients,
and of \(L\) by \(t^2\) in its \(\kappa\) term, have order at least six.
All pure odd phase terms vanish by conjugation. These errors are uniform
on the compact angular sphere and on bounded normalized motions.
The far modulus contributes
\[
 (|q_f|-\Re q_f)-(|q_f^b|-\Re q_f^b)
                         =9v_0^3M^2/128+o(t^4).             \tag{15}
\]

For completeness the nonanalytic remaining assertion is
\[
 {1\over t^4}\left(\sum_{\rm near}x^2-
                         \sum_{\rm near}(x_b)^2\right)\to0. \tag{16}
\]
Analytic symmetric moments alone do not justify this. Let
\(\Theta=\operatorname{diag}(\theta)\),
\(A_\theta=P\Theta P|_{e^\perp}\), \(w=\Theta e\).
The separated near/far Riesz subspaces are analytic graphs with uniform
bounds. Their near effective matrix is
\[
 B_{\rm near}=vI-iv^2A_\theta t
     +t^2(C(a,\theta)-iv^2\beta I)+O(t^3),\quad\beta=c_0/t^2,
\]
\[
 C(a,\theta)=c_2A_\theta^2+c_Rww^*,\qquad c_R=c_2+9v^3/8.  \tag{17}
\]
The graph correction is
\(-PV_1QV_1P/(8v)=9v^3ww^*/8\), with
\(V_1=-iv^2S\Theta S\), and
\(P\Theta^2P=A_\theta^2+ww^*\). The radial perturbation is
\(O(t^4)\); changing \(a\) changes the moving base and the displayed
coefficients, without adding a real second-order mean term.

Every repeated eigenspace of the Hermitian \(A_\theta\) has zero
\(w\)-weight. In fact its eigen-equation is
\((\Theta-\lambda I)y=\sigma e\), \(y\perp e\). If \(\lambda\)
is a diagonal value, its coordinate forces \(\sigma=0\), and the
eigenspace is supported on that equal-value block, where
\(w^*y=\lambda e^*y=0\). If not, the solution space has dimension at
most one. Consequently \(C\) is the real scalar \(c_2\lambda^2I\)
on each repeated eigenspace.

Take any sequence satisfying (11). Pass to a subsequence
\(\theta_k\to\theta_0\), and group the eigenvalues of \(A_{\theta_k}\)
by the distinct limiting eigenvalues of \(A_{\theta_0}\).
Orthogonal spectral projections converge, and different groups have
positive limiting gaps. Removing the intergroup couplings in
\((B_{\rm near}-vI)/t\) through separated-subspace graphs gives each
group the matrix
\[
 -iv(a_k)^2A_{k,\rm group}
  +t_k(C_{k,\rm group}-iv(a_k)^2\beta_k I)+O(t_k^2).
\]
This uses only gaps **between** limiting groups. For a simple limiting
group its real second coefficient converges to the scalar compression of
\(C(a_0,\theta_0)\). For a repeated group it converges in operator
norm to \(c_2(a_0)\lambda_0^2I\).
The real quadratic form on a normalized right eigenvector kills the
leading anti-Hermitian matrix and the imaginary scalar mean correction.
Thus in each group \(x/t_k^2\) has the same limit as the balanced
cutoff configuration, for every eigenvalue in the group. Their
algebraic counts agree by the separated projections. This establishes
(16) on the subsequence; a sequence violating (16) would contradict the
same conclusion on one of its convergent angular subsequences.
No uniform gaps within a group, analytic root labels, or bounded
eigenvector condition numbers are assumed.

Combining (13)–(16) and the credited cutoff formula (5) gives
\[
 G_a=\kappa v^4t^2+2v_0^2T+10v_0^3M^2/128
                             -K(\theta)v_0^8t^4+o(t^4).
\]
The original-root metric gives \(E_a=v^4t^2+O(t^4)\).
Since \(\kappa=O(t^2)\) and \(a-a_0=O(t^2)\), its substitution
into the first and quartic terms changes them by \(o(t^4)\).
This proves (12), including its full joint uniformity.

## 4. The universal lower bound and the first-failure geometry

Suppose (3) failed for some \(\varepsilon>0\). There would be
\(a_k\downarrow a_0\) and disk-root polynomials with
\(0<E_k\le\kappa_k/(C_*+\varepsilon)\), \(G_k<0\).
Their energies tend to zero, so (6) localizes them. Corollary 3 puts
them in (11), and (12) gives
\[
 {G_k\over E_k^2}
 = {\kappa_k\over E_k}+{128\over169}{T_k\over E_k^2}
             +{40\over2197}{M_k^2\over E_k^2}-K(\theta_k)+o(1)
 \ge\varepsilon+o(1)>0,
\]
a contradiction. This proves (3) and
\(\liminf\mathcal R_E(a)/\kappa\ge1/C_*\).

It also classifies the geometry of failures at the sharp scale.
If \(a_k\downarrow a_0\), \(G_k<0\), and
\(E_k/\kappa_k\to1/C_*\), then
\[
 \boxed{T_k/E_k^2\to0,\quad M_k^2/E_k^2\to0,\quad
                     \operatorname{dist}(\theta_k,\mathcal O)\to0,}
                                                               \tag{18}
\]
and \(G_k/E_k^2\to0\). To see this, write the last display as
\(\kappa_k/E_k-C_*\) plus the sum of the nonnegative radial cost,
mean cost, and \(C_*-K(\theta_k)\), plus \(o(1)\). Negativity
forces this sum to zero. Continuity, compactness, and the credited
maximum set imply the angular conclusion. Equation (18) is necessary
for these near-threshold failures; it is not by itself a sign test at the
crossing, where higher-order terms decide the sign.

## 5. The actual singleton/seven polynomial and a genuine crossing

Use the explicit family
\[
 p_{a,t}(z)=(z-a)(z+e^{7it})(z+e^{-it})^7.                    \tag{19}
\]
All other roots lie on the unit circle, and their slopes are balanced.
Let \(u_A=(a+e^{7it})^{-1}\), \(u_B=(a+e^{-it})^{-1}\).
Six critical reciprocals are \(u_B\); the two remaining ones solve
\[
 q^2-(2u_A+8u_B)q+9u_Au_B=0.                              \tag{20}
\]
This accounts for all eight critical points, by differentiating (19).
At \(t=0\), the residual roots are \(v,9v\); the discriminant is
\(64v^2>0\), uniformly near \(a_0\). Its positive-base square-root
branch labels them analytically. All moduli have positive base, so
\(G(a,t)\) and \(E(a,t)\) are real analytic jointly in \(a,t\),
and even in \(t\) by conjugation. Their convergent series in
\(h=t^2\) define real analytic germs at \((a_0,0)\); no square-root
dependence on \(h\) is introduced in the sums.

Exact expansion of (20) gives, with \(d=1+a\),
\[
 E(a,t)=56v^4h+O(h^2),\quad
 \boxed{G(a,t)=\kappa E(a,t)-K_1(a)E(a,t)^2+O(E(a,t)^3),}
\]
\[
 \boxed{K_1(a)={d^3\over7168}(516d^2-528d-393),
                      \qquad K_1(a_0)=C_*.}                \tag{21}
\]
All remainders are joint analytic and uniform near \(a_0\).
The displayed coefficient is verified symbolically as an identity in
\(\mathbb Q[v,v^{-1}]\), rather than by sampling marked radii.
For explicit coefficient-level reproduction, the expansions in \(t\) are
\[
 E=56v^4t^2+\left(-{602\over3}v^4+2408v^5-2408v^6\right)t^4+O(t^6),
\]
\[
 G=56\left(v^2-{13\over8}v^3\right)t^2
    +\left(-{602\over3}v^2+{7525\over3}v^3
                         -6090v^4+{65359\over16}v^5\right)t^4+O(t^6).
\]
The first follows directly from
\(|u-v|^2=2v^2(1-\cos\phi)/(a^2+1+2a\cos\phi)\).
For the second, insert in (20)
\[
 (a+e^{i\phi})^{-1}=v-iv^2\phi+(v^2/2-v^3)\phi^2
       +i(v^2/6-v^3+v^4)\phi^3
       +(-v^2/24+7v^3/12-3v^4/2+v^5)\phi^4+O(\phi^5),
\]
expand the discriminant about \(64v^2\), and sum six copies of
\(|u_B|\) and the two residual moduli. Subtracting \(\kappa E\)
and dividing its quartic coefficient by \(-(56v^4)^2\) gives (21).
The standalone checker derives (20), also verifies it by direct
differentiation in the original \(z\) coordinate, expands both roots,
and expands their positive moduli. Its scope and trust boundary are in
section 6.

Since \(\partial_hE(a_0,0)=56v_0^4>0\), the analytic inverse-function
theorem gives \(h=H(a,E)\) near zero. Divide the analytic gap by \(E\)
through its removable zero, obtaining
\[
 g(a,E)=\kappa-K_1(a)E+O(E^2),\quad
                   \partial_Eg(a_0,0)=-C_*<0.
\]
The analytic implicit-function theorem gives one analytic crossing
\(E^*(a)\), positive for \(a>a_0\) close, satisfying (4). On one fixed
small positive energy interval, \(g\) is strictly decreasing; its sign
is positive below \(E^*(a)\), negative above it. Those positive energies
correspond to real \(t\) in (19), because the inverse has
\(H(a,E)>0\). Thus the sign change is realized by actual admissible
polynomials, not just by a formal quartic or a limiting direction.

For any \(\rho>E^*(a)\), choose an energy between \(E^*(a)\) and
\(\min(\rho,\text{the fixed neighborhood endpoint})\); the resulting
polynomial violates \(G_a\ge0\). Hence \(\mathcal R_E(a)\le E^*(a)\),
including the possible endpoint ambiguity in (1). Together with section
4 this proves (2), positivity, and finiteness.

## 6. Reproduction and limitations

`verify.py` uses only Python's standard library. Its arithmetic is exact
in \(\mathbb Q[v,v^{-1}][i][t]/(t^5)\), with real positive \(v\).
Every division checks that its denominator is a nonzero Laurent monomial;
every positive square-root constant checks an even monomial exponent and
a rational perfect square. The positive base choices coincide with the
actual branches in (20) for real \(0<a<1\).

There are seven balanced symbolic two-block profiles, twenty-eight
general radial/mean second-order profiles, twenty-one nonlinear mixed
joint profiles, a symbolic varying-base marked-motion control, and two
explicit sign controls bracketing the singleton crossing. All profiles
derive the actual derivative polynomial. The generic second-order
identities and (21) are polynomial identities in \(v\), not floating
fits. The mixed profiles are finite algebra controls; they do not prove
coverage of arbitrary original roots.

The all-disk coverage comes from sections 2–4, using the credited
angular theorem (5). The exact code does not independently verify the
spectral collision argument, uniform analytic estimates, completeness,
or the analytic implicit/inverse-function theorems. This is an ordinary
written proof with algebra verification, not a formally verified or
exhaustively enumerated theorem.

The target first-power inequality \(F_a\ge8\) for every degree-nine
disk-root polynomial remains outside the claim. Near collapse
\(F_{a_0}=128/13>8\), so a failure of \(F_a\ge16/(1+a)\) gives no
counterexample to that endpoint conjecture. The universal result here
concerns the exact scale and extremal geometry of the collapsed energy
basin. No optimal original-root maximum-displacement basin, explicit
neighborhood, or historical priority is claimed.
