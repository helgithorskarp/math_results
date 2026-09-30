# The degree-nine maximum-displacement basin as an angular maximum

Author **six-sendov-2**, role **researcher**, 2026-09-30.
Status: complete ordinary written author proof using explicitly credited
angular and joint-motion inputs. Independent review of this extension and
of the cited joint-motion extension is pending. The asymptotic bridges are
not formalized; the accompanying exact algebra checks do not formalize them.

## 1. Statement, metrics and credited inputs

Let
\[
 p(z)=c(z-a)\prod_{j=1}^8(z-z_j),\qquad c\ne0,\quad
 0<a<1,\quad |z_j|\le1,
\]
with a simple marked zero \(a\). Critical points are counted with algebraic
multiplicity, and repeated other zeros are permitted. Define
\[
 a_0=5/8,\quad d=1+a,\quad d_0=13/8,\quad v=d^{-1},
 \quad\kappa=d(a-a_0),\quad p_0={10985\over33554432},
\]
\[
 F_a=\sum_{p'(\zeta)=0}|a-\zeta|^{-1},\quad
 G_a=F_a-16/d,\quad \rho(p)=\max_j|z_j+1|,
\]
\[
 E_a=\sum_j|(a-z_j)^{-1}-v|^2.
\]
The simple marked-zero convention makes all reciprocals finite. A repeated
marked zero would give \(F_a=+\infty\) but undefined original-root energy;
it is excluded from these quantifiers. Rotation gives the equivalent
statement about a complex marked zero of modulus \(a\), centered at its
opposite unit point.

The maximum-original-root basin is
\[
 R_8(a)=\sup\{r\ge0:G_a\ge0\text{ for every such }p
                                      \text{ with }\rho(p)\le r\}.
                                                               \tag{1}
\]
Radius zero is admissible, because \(z_j=-1\) gives \(F_a=16/d\).
Admissible radii form an initial interval; its endpoint need not be
admissible. This is the metric of the preceding displacement-basin work,
rather than the sum of squared reciprocal displacements \(E_a\).

For a nonzero balanced real direction \(\theta\), put
\[
 \mu_k=\sum_j\theta_j^k,\quad
 e=\mathbf1/\sqrt8,\quad P=I-ee^*,\quad
 A=P\operatorname{diag}(\theta)P|_{e^\perp},\quad
 w=\operatorname{diag}(\theta)e,
\]
\[
 \Psi(\theta)=\sum_{\lambda}\|\Pi_\lambda w\|^4,\qquad
 K(\theta)=p_0\left(122+{224\mu_4-5760\Psi(\theta)\over\mu_2^2}\right).
                                                               \tag{2}
\]
The sum uses full spectral projections at distinct eigenvalues, including
collisions. The [credited angular theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md)
and [optimizer](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_optimizer/PROOF.md),
independently audited in the [angular review](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_review3/REVIEW.md),
give continuity and scale invariance of \(K\), and
\(60p_0\le K\le204p_0\). We import these results.

On the compact sphere
\[
 \mathcal S_8=\{\theta\in\mathbb R^8:\sum\theta_j=0,\ \mu_2=1\},
 \quad q(\theta)=\max_j\theta_j^2,
\]
define the positive, finite, attained variational constant
\[
 \boxed{\Lambda_8=\max_{\mathcal S_8}{K(\theta)\over q(\theta)},
 \quad \mathcal M_\infty=\operatorname*{argmax}_{\mathcal S_8}K/q.} \tag{3}
\]
Here \(q\ge1/8\). Equivalently, on the compact set of balanced directions
with \(\max|\theta_j|=1\), let \(J=\mu_2K/p_0\); then
\(\Lambda_8=p_0\max J\).

**Theorem 1 (the full displacement reduction).** For \(a>a_0\) sufficiently
close, \(0<R_8(a)<\infty\), and
\[
 \boxed{\lim_{a\downarrow5/8}{R_8(a)^2\over\kappa}
                       ={d_0^4\over\Lambda_8}=:B_\infty.}     \tag{4}
\]
More precisely, for every \(\varepsilon>0\), some
\(\eta_\varepsilon>0\) gives, for **every** disk-root polynomial above,
\[
 a_0<a<a_0+\eta_\varepsilon,\quad
 \rho(p)^2\le {\kappa d_0^4\over\Lambda_8+\varepsilon}
                     \quad\Longrightarrow\quad G_a\ge0.    \tag{5}
\]
For each \(\lambda>1\), a maximizing direction in (3) produces actual
boundary-root polynomials with negative gap for every sufficiently small
positive \(a-a_0\), at squared displacement
\(\lambda\kappa d_0^4/\Lambda_8+O(\kappa^2)\).
No numerical size of these neighborhoods or analytic first-crossing
uniqueness for arbitrary directions is claimed.

**Theorem 2 (a global angular displacement bound).** Without any conjugate
symmetry assumption,
\[
 \boxed{\max_{\sum\theta=0,\ \max|\theta|=1}J(\theta)
       \le H_0:={2113776-5040\sqrt{80045}\over847}<813.}        \tag{6}
\]
This is a sufficient bound, not an asserted optimal angular constant.
Together with the already published four-block profile, it yields
\[
 \boxed{ {106496\over5H_0}\le B_\infty
       \le B_*={106496\over5j(u_*)},}                         \tag{7}
\]
where the [credited four-block theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_four_block_basin/PROOF.md)
defines
\[
 j(u)={2058+21912u-15876u^2+19224u^3+3402u^4
                                  \over(3+u)(1+3u)^2}
\]
and its unique maximizer \(2/25<u_*<9/100\). That predecessor proves
\(27.106707<B_*<27.106708\); its optimum is not claimed new here.
The new lower endpoint satisfies
\[
 26.2273440907 < {106496\over5H_0}<26.2273440908.              \tag{8}
\]
The exact interval is reproduced using integer-square-root enclosures.

**Corollary 3 (near-threshold failure geometry).** Suppose
\(a_k\downarrow a_0\), \(G_{a_k}<0\), and
\(\rho(p_k)^2/\kappa_k\to B_\infty\). In the angular decomposition
defined below,
\[
 \boxed{T_k/E_k^2\to0,\quad M_k^2/E_k^2\to0,\quad
             \operatorname{dist}(\theta_k,\mathcal M_\infty)\to0,}
                                                               \tag{9}
\]
and \(G_{a_k}/E_k^2\to0\). The maximum set remains unidentified;
this is a qualitative necessity for sharp-scale failures, not a sign
test at a crossing or an explicit distance-to-orbit estimate.

The primary new input making (4) possible is **six-sendov-3**'s
[all-disk joint-motion proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_sharp_energy_basin/PROOF.md),
source e0f007cfc02f9cf519eb00acab3b963e03f8cb8b, graph
bafkreidfppq3cl6kblyzctun2z7hstapk6krsrggtsmdrmetb4vxi2yz2i,
height7534. We use its Corollary3 and Lemma4, including their uniformity
over collisions, and do not infer that joint statement from a fixed-radius
angular expansion. Its independent review remains pending.

## 2. The joint input and the metric conversion

For all roots near \(-1\), write uniquely
\[
 z_j=-(1-\tau_j)e^{i\phi_j},\quad \tau_j\ge0,\quad
 T=\sum\tau_j,\quad M=\sum\phi_j,\quad L=\sum\phi_j^2.
\]
On any negative-gap sequence with \(a\ge a_0\) and these roots converging
to \(-1\), the cited bootstrap gives, uniformly,
\[
 L>0,\quad T=O(L^2),\quad M^2=O(L^2),\quad\kappa=O(L).       \tag{10}
\]
Put \(c_0=M/8\), \(t=\|\phi-c_0\mathbf1\|\), and
\(\theta=(\phi-c_0\mathbf1)/t\). Since
\(t^2=L-M^2/8\), (10) implies \(t>0\), \(\theta\in\mathcal S_8\),
and
\[
 T=O(t^4),\quad c_0=O(t^2),\quad a-a_0=O(t^2).              \tag{11}
\]
The cited joint lemma states, uniformly when these three normalized
quantities stay bounded, even without a negative gap,
\[
 G_a=\kappa E_a+{128\over169}T+{40\over2197}M^2
                         -K(\theta)E_a^2+o(E_a^2).          \tag{12}
\]
Directions and their spectral collision types may vary. The premise
includes the joint near-critical spectral grouping argument; our exact
checker does not certify that analytic argument.

The original-root identities are
\[
 |z_j+1|^2=\tau_j^2+2(1-\tau_j)(1-\cos\phi_j),\qquad
 |(a-z_j)^{-1}-v|^2={v^2|z_j+1|^2\over|a-z_j|^2}.
\]
Under (11), uniformly over directions,
\[
 \rho(p)^2=t^2q(\theta)+O(t^3),\qquad
 E_a=d_0^{-4}t^2+O(t^4).                                  \tag{13}
\]
For the first estimate, \(\phi_j=t\theta_j+c_0\), so
\(\max\phi_j^2=t^2q+O(t^3)\), while the radial and cosine errors
are \(O(t^4)\) or smaller. For the second, the original-root inverse
is analytic; its squared distance has quadratic term \(v^4\phi_j^2\).
The sum has no odd total phase terms by conjugation. Its radial-square,
radial times two phases and pure phase-four errors are \(O(t^4)\) under
(11). Replacing \(L\) by \(t^2\) and \(v\) by \(d_0^{-1}\) costs
\(O(t^4)\). This also follows from the original-root metric estimate
in the cited joint proof. Since \(q\ge1/8\), inversion is uniform:
\[
 {\rho(p)^2\over E_a}=d_0^4q(\theta)+O(t).                  \tag{14}
\]

## 3. Proof of the full displacement reduction

On a negative-gap sequence, the radial and mean terms in (12) are
nonnegative, hence
\[
 0<\kappa/E_a\le K(\theta)+o(1).
\]
This bounds the multiplier \(\kappa/E_a\), so (14) gives
\[
 {\kappa d_0^4\over\rho(p)^2}
       ={\kappa/E_a\over q(\theta)}+o(1)
       \le {K(\theta)\over q(\theta)}+o(1)\le\Lambda_8+o(1).\tag{15}
\]
If (5) were false for a fixed \(\varepsilon>0\), choose counterexamples
with \(a\downarrow a_0\). Their displacements tend to zero, so every
other root converges to \(-1\). Displacement zero cannot be a failure.
The bootstrap, joint lemma and (15) apply, contradicting
\(\kappa d_0^4/\rho(p)^2\ge\Lambda_8+\varepsilon\).
Thus (5) holds, \(R_8(a)>0\), and
\(\liminf R_8(a)^2/\kappa\ge d_0^4/\Lambda_8\).

For the reverse inequality choose a maximizer \(\theta\) in (3), fix
\(\lambda>1\), and set
\[
 t^2={\lambda\kappa d_0^4\over K(\theta)},\qquad
 p_a(z)=(z-a)\prod_j(z+e^{it\theta_j}).                     \tag{16}
\]
These are actual disk-root polynomials with a simple marked zero.
They have \(T=M=0\) and \(a-a_0=O(t^2)\); (12) applies by construction.
Equation (13) yields \(E_a=\lambda\kappa/K+O(\kappa^2)\), and
\[
 G_a={\lambda(1-\lambda)\over K}\kappa^2+o(\kappa^2)<0.
\]
For these mean-zero paths the displacement error improves to \(O(t^4)\),
so
\[
 \rho(p_a)^2={\lambda\kappa d_0^4q\over K}+O(\kappa^2)
            ={\lambda\kappa d_0^4\over\Lambda_8}+O(\kappa^2).
\]
A violating polynomial at this radius implies \(R_8(a)\le\rho(p_a)\),
regardless of endpoint admissibility. In particular the basin is finite.
Take the limsup and then \(\lambda\downarrow1\). This proves (4).
No individual critical-root labeling or analytic crossing assertion is
used in the construction.

For Corollary3 put \(h_k=\kappa_kd_0^4/\rho(p_k)^2\to\Lambda_8\).
Equations (12)–(14) give
\[
 {G_k\over E_k^2}
 =q(\theta_k)\left(\Lambda_8-{K(\theta_k)\over q(\theta_k)}\right)
     +{128\over169}{T_k\over E_k^2}
     +{40\over2197}{M_k^2\over E_k^2}+o(1).
\]
Each displayed term is nonnegative. Negativity forces their sum to zero.
Continuity and compactness imply approach to \(\mathcal M_\infty\), and
also yield the claimed vanishing gap. This proves (9).

## 4. A moment bound for the different angular objective

Normalize \(\max|\theta_j|=1\), and put
\[
 \alpha=\mu_2\le8,\qquad x={\mu_4\over\alpha^2},\qquad
 s={\mu_3\over\alpha^{3/2}},\qquad z=s^2,\qquad
 \eta={64\Psi\over\alpha^2}.
\]
Then \(x\ge1/8\), \(\mu_4\le\alpha\), and
\[
 J=\alpha(122+224x-90\eta).                                \tag{17}
\]
The [credited optimizer proof, Section3](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_optimizer/PROOF.md)
supplies the orthogonal spectral moment bound, not just its final maximum
of \(K\). In its unit-\(\mu_2\) normalization,
\[
 \eta\ge {1\over7}+{4z\over3}+{N^2\over D}\quad(D>0),
\]
\[
 N=x-{13\over56}-{5z\over6},\qquad
 D={x\over2}-{11\over224}-{25z\over48}\ge0.                 \tag{18}
\]
If \(D=0\), necessarily \(N=0\). These are the squared projections of
the normalized spectral weights onto \(1,\lambda,\lambda^2\) after
orthogonalization. Repeated compression spaces have zero \(w\)-weight;
listing their eigenvalues with multiplicity is therefore legitimate.
The simple consequence \(\eta\ge1/7\) holds everywhere.

If \(\alpha\le5\), (17) immediately gives
\[
 J\le224\mu_4/\alpha+{764\over7}\alpha
     \le224+{3820\over7}={5388\over7}.                      \tag{19}
\]
For \(5\le\alpha\le8\),
\(1/8\le x\le1/\alpha\le1/5<13/56\). Thus
\(N_0=x-13/56<0\) and \(D_0=x/2-11/224>0\).
The alternative \(D=0\) would contradict \(N=0\), since
\(N=N_0-5z/6<0\). Also \(D\le D_0\) and \(|N|\ge|N_0|\), so (18)
implies
\[
 K/p_0\le H(x):={764\over7}+224x-90{(x-13/56)^2\over x/2-11/224}.
\]
On this entire interval \(H'(x)>224\), because
\((N_0^2/D_0)'=2N_0/D_0-N_0^2/(2D_0^2)<0\). Consequently
\[
 J\le\alpha H(1/\alpha)
 ={764\over7}\alpha+224
              -{45\over7}{(56-13\alpha)^2\over112-11\alpha}.
                                                               \tag{20}
\]
With \(h=112-11\alpha>0\), the last expression is exactly
\[
 {2113776-16009h-31752000/h\over847}
 \le {2113776-2\sqrt{16009\cdot31752000}\over847}=H_0,       \tag{21}
\]
by the arithmetic–geometric mean inequality. The radical simplifies to
\(2\sqrt{16009\cdot31752000}=5040\sqrt{80045}\).
The low-regime bound (19) is smaller than (20) at \(\alpha=6\), whose
value is \(18658/23\), and this is at most \(H_0\).
This proves the global inequality (6).

An alternative wholly rational bound is \(J<813\). Clearing its positive
denominator in (20) leaves
\[
 16009\alpha^2-196441\alpha+602896
 =16009\left(\alpha-{196441\over32018}\right)^2
                       +{17981775\over64036}>0.              \tag{22}
\]
The checker verifies (20)–(22), the radical reduction and (8) exactly.
No sharpness of this moment relaxation is asserted.

Finally \(d_0^4/p_0=106496/5\), and the credited three-unit-pair profile
has \(J=j(u_*)\), hence \(p_0j(u_*)\le\Lambda_8\le p_0H_0\).
Equations (4) and (7) follow. The energy optimizer itself is not a
displacement optimizer: its max-slope normalization
\((1,-1/7,\ldots,-1/7)\) has \(J=1632/7\), whereas the actual balanced
profile with three unit pairs and one pair at \(\pm1/3\) has
\(J=j(1/9)=5472/7\). The distinct energy-normalized and displacement-
normalized optimization problems cannot be identified.

## 5. Scope and reproducibility

The global complex exponent-one Tang–Zhang conjecture asks \(F_a\ge8\).
Here the comparison is the stronger local collapsed baseline \(16/(1+a)\);
at the cutoff it is \(128/13>8\). Equations (4)–(9) describe its failure
scale and angular reduction. They do not prove the unrestricted endpoint,
the optimal numerical displacement constant, a globally sharp angular
profile, or a finite explicit neighborhood. The known unit-marked-zero
regular/collapsed equality classification and quadratic equality theorem
are separate statements.

[SPECTRAL_REDUCTION.md](SPECTRAL_REDUCTION.md) gives an additional exact
15-term rational squared-weight formula for the complete four-pair centrally
symmetric angular family on its generic domain. This is an algebraic oracle
for the remaining optimization, not a certificate of its optimizer.
Singular faces are explicitly excluded from division and have credited
continuous limits.

Run `python3 verify.py --expected expected.json` from this directory.
The standard-library checker verifies the global-bound rational identities,
integer radical enclosures, generic cubic quotient and adjugate identities,
their discriminant cancellation, exact recovery of the preceding face,
and definition-level rational compression controls. The controls and
matrix calculations are author checks; independent peer review is pending.
The output manifest records checks and a canonical coefficient digest.
Exact algebra verifies the explicit finite identities, while the written
sequential proof and imported uniform analytic lemma remain outside that
checker's trust boundary.
