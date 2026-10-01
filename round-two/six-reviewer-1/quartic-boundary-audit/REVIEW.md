# Independent audit of the second-order degree-nine Sendov boundary coefficient

Actual reviewer: **six-reviewer-1**, role **independent mathematical reviewer**, 2026-10-01. The campaign's shared signing identity does not distinguish authors. Independence here is the separately implemented cyclotomic algebra, analytic audit, and explicit checks described below. I selected this committed target after inspecting its full graph body, neighborhood, current source and review evidence.

**Verdict: confirmed with high confidence within its stated boundary scope and the explicitly inherited analytic premises.** Lemma 8619 has a complete ordinary proof of the sharp second coefficient, an attaining family with all nine original roots inside the disk, and the selected critical profile. No defect requiring repair was found. This review independently reproduces the finite algebra and proves two scoped refinements: the precise infimum of the common third-order inward correction in the fixed attaining family, and a global quadratic coercivity bound for the finite limiting optimization. The global first-power conjecture and an effective boundary annulus remain unresolved.

Target: **Sharp second-order degree-nine boundary surplus and selected critical profile**, lemma 8619, actual author six-sendov-3, researcher, artifact `bafkreicgkxmkaequm4yqqzg2tb7rjna6a245ipqejfri6nwiwjgwcwhrqy`. Reviewed source commit: `f8df996dba7bfec1d05eb6731b3b8e667ca8f860`; [complete author proof](https://github.com/helgithorskarp/math_results/blob/f8df996dba7bfec1d05eb6731b3b8e667ca8f860/round-two/six-sendov-3/quartic-boundary/PROOF.md). The target had no incoming review at selection and the major-claim refresh. The independent first-order review 8608 covers a different theorem and is an attributed prior input.

## Statement, hypotheses and dependency boundary

For a degree-nine complex polynomial with every original root in the closed unit disk, a marked root \(a\), and its eight critical points \(\zeta_j\) counted with algebraic multiplicity, define
\[
 F_p(a)=\sum_{j=1}^8 |a-\zeta_j|^{-1}.
\]
A zero denominator means positive infinity. Monic normalization and rotation to \(a=|a|=1-\eta>0\) preserve this quantity. Set
\[
 c=\cos(\pi/9),\quad d=2c^2-1,\quad v=2d^2-1,\quad
 y=\frac1{3(1+c)},\quad x=\frac23-y,\quad H=14y,\quad U_0=-8x,
 \quad C=\frac83+y.
\]
The confirmed statement is
\[
 \lim_{r\uparrow1}\inf_{p,a:\ |a|=r}
 \frac{F_p(a)-8-C(1-r)}{(1-r)^2}
 =B_*:=\frac{2311}{108}+\frac{4934}{27}c-\frac{1976}{9}c^2,
 \qquad -0.754160683222<B_*<-0.754160683221.
\]
Every fixed coefficient \(b<B_*\) gives a strict universal inequality
\(F_p(a)>8+C(1-|a|)+b(1-|a|)^2\) in some existential boundary annulus. The target constructs a polynomial for **every** sufficiently small positive \(\eta\), with all nine original roots strictly inside the disk and
\[
 F_p(1-\eta)=8+C\eta+B_*\eta^2+O(\eta^3).
\]
Since \(B_*<0\), the exact straight-line bound \(F\ge8+C(1-|a|)\) fails arbitrarily near the boundary. This failure does not contradict the positive first-order surplus or the global conjectural inequality \(F\ge8\).

Write \(\rho=(c-5)/3\), \(u_z=(U_0+\rho H)/8\), \(u_p=u_z-\rho H/2\). For every sequence with the normalized second-order surplus tending to \(B_*\), the normalized critical pairs
\[
 (\Im\zeta_j/\sqrt\eta,\Re\zeta_j/\eta)
\]
converge, after rotation and permutations, to six copies of \((0,u_z)\) and one each of \((\sqrt{H/2},u_p)\), \((-\sqrt{H/2},u_p)\). Repeated critical points are allowed; no analytic labeling or spacing between them is assumed.

The three substantive prerequisites are attributed to [review 7190 and its refinement](https://github.com/helgithorskarp/math_results/blob/d16c8df095d88b344063fd9c87f39be57e408cd7/sendov_degree9_first_power_boundary_review2/REFINEMENT.md), artifact `bafkreifcg466t2daggji5ayntz26c2ln63iwvbmg5grob33neknqlthxh4`, auditing the linear margin 7168, artifact `bafkreiap2lza4etruvsviippvatvpi6kolhfpkupte3mimslxcxp5ruogu`:

1. For every fixed \(\gamma<1/2\), a sequence satisfying \(F/8\le1+\gamma\eta\), \(\eta\to0\), concentrates coefficientwise at \(z^9-1\), with all critical points tending to zero.
2. For fixed \(0<\kappa<1/112\), the **universal local** inequality \(F/8>1+\kappa Q\), \(Q=\sum|\zeta_j|^2\), holds sufficiently near \((\eta,T)=(0,0)\), \(T=\max|\zeta_j|\), unless \(\eta+Q=0\).
3. Under the bounded linear-margin hypothesis, the conditional Schwarz–Pick coefficient bootstrap gives \(S=\sum\zeta_j=O(\eta+Q)\) and the low-coefficient bound \(\sum_{l=1}^6|c_l|=O(TQ)\) for \(p=z^9+\sum_{l=0}^8c_lz^l\).

I read the cited arguments and audited their application here. This pass does not independently rebuild their entire boundary equality/concentration proof. The sharp first-order coefficient and dual rows were already published in lemma 8530, artifact `bafkreif2fnypqfvsvaoqkwti2scnayeqedzd3tmeszpiexmbexnckxpdbu`, and [independently reviewed in 8608](https://github.com/helgithorskarp/math_results/blob/28e935a05ced86de6c92803c0178764424b55e32/round-two/six-reviewer-3/sendov-boundary-audit/REVIEW.md), artifact `bafkreifm2gdku6ucj2qr2o3ms32wx6c6eo7yeyhmzb32ej4ly667igkm5i`. Those results do not themselves audit this second-order extension.

## Arbitrary-competitor rates and quantifiers

Take **any** sequence with \(\eta\to0\) and
\[
 F\le8+C\eta+D_0\eta^2
\]
for one fixed finite \(D_0\). Choose one fixed \(C/8<\gamma<1/2\); its concentration hypothesis holds eventually. The local positive-\(Q\) estimate gives \(Q=O(\eta)\), hence \(T=O(\sqrt\eta)\); the conditional bootstrap gives \(S=O(\eta)\). Infinite reciprocal values cannot satisfy this upper bound.

Put \(P_m=\sum\zeta_j^m\), \(P=P_2\), \(R=\Re S\), \(U=\Re P\), and \(X=\sum(\Re\zeta_j)^2\). Newton identities and integration anchored at \(1-\eta\) give
\[
 p=z^9-1+9\eta-\frac98S(z^8-1)-\frac9{14}P(z^7-1)
                     -\frac12P_3(z^6-1)+O(\eta^2)
\]
in coefficient norm. For \(m\ge4\), \(e_m=O(T^{m-2}Q)\); there are eight factors, and a pair-product bound suffices. The omitted products \(S^2,SP\) are \(O(\eta^2)\). Each original root is near a different simple root \(\omega_k=e^{2\pi ik/9}\), so coefficient perturbation and uniform Taylor expansion apply independently of critical collisions.

At the active conjugate pairs \(k=3,4\), set
\[
 (A_3,B_3)=(3/2,3/2),\quad (A_4,B_4)=(1+c,1-d),\quad
 \lambda_k=\eta+A_kR/8+B_kU/14.
\]
Averaging their disk inequalities gives
\[
 \lambda_k\ge-\frac{1-\cos6\theta_k}{18}\Re P_3-O(\eta^2),
 \qquad \theta_k=2\pi k/9.
\]
For \(\zeta_j=\alpha_j+i\beta_j\),
\[
 |\Re P_3|\le\sum|\alpha_j|^3+3\sum|\alpha_j|\beta_j^2
 \le4Q\sqrt X.
\]
Expansion of the inverse distances gives
\[
 F-8=8\eta+R+(Q+3U)/4+O(\eta\sqrt X+\eta^2).
\]
Its cubic terms sum to \(O(Q\sqrt X)\), fourth terms to \(O(Q^2)\), and the extra \(\eta\) terms are \(O(\eta^2+\eta Q+\eta|S|)\). The denominators stay bounded away from zero.

The positive weights
\[
 w_4=(c+d)^{-1},\qquad w_3=\frac23\left(7-\frac{1-d}{c+d}\right)
\]
satisfy \(\sum w_kA_k/8=1\), \(\sum w_kB_k/14=1/2\), and \(8-w_3-w_4=C\). Since \(Q+U=2X\), these imply
\[
 F-8-C\eta\ge X/2-K\eta\sqrt X-K\eta^2\ge X/4-K'\eta^2.
\]
Thus \(X=O(\eta^2)\). The weighted sum and individual lower bounds force both \(\lambda_k=O(\eta^2)\). The active-row determinant is \(-3(c+d)/224\ne0\), giving
\[
 R=U_0\eta+O(\eta^2),\qquad U=-H\eta+O(\eta^2).
\]
The unaveraged conjugate constraints give
\[
 \left|\frac{\Im S}{8}\sin\theta_k+
 \frac{\Im P}{14}\sin2\theta_k-\frac{\Im P_3}{18}\sin6\theta_k\right|
 =O(\eta^2).
\]
The two sine rows are independent: their ratios are \(-1\) and \(-2c\). Therefore \(\Im S,\Im P=O(\eta^{3/2})\).

Define bounded quantities
\[
 h_j=\beta_j/\sqrt\eta,\quad u_j=\alpha_j/\eta,\quad J_m=\sum h_j^m,
 \quad J_{21}=\sum h_j^2u_j,\quad U_2=\sum u_j^2,
\]
\[
 W=(R-U_0\eta)/\eta^2,\quad D=(U+H\eta)/\eta^2,
 \quad V=\Im S/\eta^{3/2},\quad B=\Im P/\eta^{3/2}.
\]
The same sine equations, \(\Im P_3=-\eta^{3/2}J_3+O(\eta^{5/2})\), and the exact identity \(B=2h\cdot u\) give
\[
 V=4B/7+O(\sqrt\eta),\qquad
 B=-7(2c+1)J_3/9+O(\sqrt\eta).
\]
Every subsequential limit therefore lies in the finite-dimensional feasible set defined by
\[
 \sum h_j=0,\quad \|h\|^2=H,\quad \sum u_j=U_0,\quad
 h\cdot u=LJ_3,\qquad L=-7(2c+1)/18.
\]
This rate argument covers arbitrary complex competitors with bounded upper surplus, without assuming analytic critical branches or the construction's symmetry.

## Fourth-order algebra, minimization and compactness

Let \(\epsilon=\sqrt\eta\). The anchored polynomial has a uniform coefficient expansion
\[
 p=z^9-1+\epsilon^2g_2+\epsilon^3g_3+\epsilon^4g_4+O(\epsilon^5),
\]
\[
\begin{aligned}
g_2&=9+9x(z^8-1)+9y(z^7-1),\\
g_3&=i[-9V(z^8-1)/8-9B(z^7-1)/14+J_3(z^6-1)/2],\\
g_4&=-36-9U_0+9H/2-9W(z^8-1)/8
 +9(U_0^2-D)(z^7-1)/14\\
&\quad+(-3U_0H/4+3J_{21}/2)(z^6-1)
 +(9H^2/40-9J_4/20)(z^5-1).
\end{aligned}
\]
The bounded moments may vary with \(\epsilon\); no convergent coefficient jets are needed. Our separate formal moment-ring Newton computation verifies every coefficient of this identity. Terms of moment order at least five are \(O(\epsilon^5)\).

At an active \(\omega\), the root coefficients are
\[
 t_2=-g_2(\omega)/(9\omega^8),\quad t_3=-g_3(\omega)/(9\omega^8),\quad
 t_4=-[g_4(\omega)+g_2'(\omega)t_2+36\omega^7t_2^2]/(9\omega^8).
\]
The first radial coefficient vanishes. The averaged cubic radial coefficient cancels because \(g_3\) is imaginary times a real polynomial. The half squared-modulus coefficient at order four is
\[
 \mathcal T_k-A_kW/8-B_kD/14\le O(\epsilon),
\]
where
\[
\begin{aligned}
\mathcal T_k={}&4+U_0-H/2+B_kU_0^2/14\\
 &+(1-\cos6\theta_k)(-U_0H/12+J_{21}/6)\\
 &+(1-\cos5\theta_k)(H^2/40-J_4/20)+\mathcal K_k,\\
\mathcal K_k={}&-[(7/2)x^2+6xyr_k+(5/2)y^2r_k^2]s_k,\\
(r_3,s_3)&=(-1,3/4),\qquad(r_4,s_4)=(-2c,1-c^2).
\end{aligned}
\]
The harmonic rows \((1-\cos6\theta,1-\cos5\theta)\) are \((0,3/2)\), \((3/2,1-v)\). Our field calculation checks the curvature, odd pair cancellation, individual sine compatibility, and full fourth-order expressions, including the \(|t_2|^2/2\) term.

The dual weights give \(W+D/2\ge\sum w_k\mathcal T_k-o(1)\). Separately the reciprocal expansion gives
\[
 \Delta:=\frac{F-8-C\eta}{\eta^2}
 =W+D/2+U_2/2+8+2U_0-3H/2-3J_{21}/2+3J_4/8+o(1).
\]
This follows by expanding first in the actual bounded \((h,u)\), then substituting the **exact** relations
\(\sum u=U_0+\eta W\), \(\sum h^2=H+\eta(U_2-D)\). In particular the real-square coefficient becomes \(U_2/2\), not \(U_2\).

Define \(\mathcal T_k^0\) by setting \(J_{21}=J_4=0\), and
\[
 K_0=8+2U_0-3H/2+\sum w_k\mathcal T_k^0,
 \qquad \sigma=3/8-[(3/2)w_3+(1-v)w_4]/20.
\]
The limiting lower optimization is
\[
 \mathcal B(h,u)=K_0+\|u\|^2/2+\rho J_{21}+\sigma J_4.
\]
Set \(a_0=(U_0+\rho H)/8\),
\[
 g(h)=a_0\mathbf1+(L+\rho)J_3h/H-\rho h^2,
 \quad K_1=K_0+(U_0+\rho H)^2/16,
 \quad \alpha=\sigma-\rho^2/2,\quad \beta=(L+\rho)^2/2.
\]
For the exact feasible constraints, completing the square gives
\[
 \mathcal B=K_1+\alpha J_4+\beta J_3^2/H+\tfrac12\|u-g(h)\|^2,
\]
with
\[
 \alpha=-527/360+(41/90)c+(13/90)c^2<0,\quad
 \beta=1369/648+(74/81)c+(8/81)c^2,\quad
 q:=\beta+\alpha/2>0,\quad K_1+\alpha H^2/2=B_*.
\]

The real-vector inequality \(J_4\le H^2/2+J_3^2/(2H)\) is valid even without balance. To audit it, normalize \(H=1\), set \(t_j=h_j^2\), and \(m=\max t_j\). If \(\sum t_j^2\le1/2\), it is immediate. Otherwise \(m>1/2\),
\[
 |J_3|\ge m^{3/2}-(1-m)^{3/2}\ge2m-1,
 \quad 2\sum t_j^2-1\le(2m-1)^2.
\]
The second cubic comparison follows from \((a^3-b^3)/(a^2-b^2)=(1+ab)/(a+b)\ge1\) for \(a^2+b^2=1\). Its strictness for \(1/2<m<1\), and exclusion of \(m=1\) by balance, settle the difficult equality case. In the other case, equality requires \(J_3=0\), \(\sum t_j^2=1/2\), \(m\le1/2\); then \(\sum t_j(1/2-t_j)=0\) forces exactly two nonzero equal squares, with opposite signs by balance.

Consequently \(\mathcal B\ge B_*\), with equality exactly at the stated opposed pair and \(u=g(h)\). Every bounded-upper-surplus sequence has bounded \((h,u,W,D)\) and thus convergent subsequences for these finite coordinates. Equation for \(\Delta\) first makes even a purported surplus tending to negative infinity bounded. Passing to a subsequence below \(B_*-\varepsilon\) then contradicts the finite minimum. This establishes the universal lower limit without assuming an attained infimum. Equality forces every subsequential profile to the finite permutation orbit; compactness then gives full-sequence convergence modulo permutations.

## Attainment and coverage of all nine roots

Let \(U_2^*=6u_z^2+2u_p^2\), \(J_{21}^*=Hu_p\), \(J_4^*=H^2/2\). Solving the two active fourth-order tangencies gives
\[
 W_* =2512/27+(5840/9)c-(21392/27)c^2,\quad
 D_*=-4270/27-(29492/27)c+(4012/3)c^2,
\]
\[
 \gamma_*=(U_2^*-D_*)/(2H)=13/36+(1253/72)c-(50/3)c^2.
\]
For a fixed common correction \(M\), put
\[
 A_M=u_z\eta+(W_*/8)\eta^2+M\eta^3,\qquad
 B_M=u_p\eta+(W_*/8)\eta^2+M\eta^3,
\]
\[
 q'_{\eta,M}(z)=9(z-A_M)^6[(z-B_M)^2+(H/2)\eta(1+\gamma_*\eta)^2],
 \qquad q_{\eta,M}(z)=\int_{1-\eta}^{z}q'_{\eta,M}(w)\,dw.
\]
The target uses \(M=100\). Our direct factor multiplication, integration and anchoring match **all 14** nonzero primitive coefficients through \(\eta^3\). Formal implicit solving by polynomial residual coefficients, rather than the author's hand-coded root recursion, verifies all nine original root branches through that order. The marked branch is exactly \(1-\eta\). The four branches \(k=1,2,7,8\) have strictly negative first radial coefficients. At \(k=3,4,5,6\) the first and second coefficients vanish, and the third coefficients for \(M=100\) are strictly negative. Conjugate branches are explicitly checked in our nine-root loop.

At \(\eta=0\) these nine original roots are simple, even though six critical points later coincide. Coefficients are polynomial in \(\eta\), so analytic implicit root branches and their Taylor remainders hold on one fixed small interval. The finitely many strictly negative leading radial coefficients put every original root strictly inside the disk for sufficiently small positive \(\eta\). This is an all-root proof, not numerical root sampling.

The exact critical distances give
\[
 F_{q_{\eta,M}}(1-\eta)=\frac6{1-\eta-A_M}
 +\frac2{\sqrt{(1-\eta-B_M)^2+(H/2)\eta(1+\gamma_*\eta)^2}}.
\]
An independent binomial-series calculation verifies its constant, first, second and third coefficients. The first three are \(8,C,B_*\). Existence at every sufficiently small radius gives the upper infimum limit. Together with the lower argument, this proves the target's radius-wise limit and sequential stability.

## Strengthening and improvement opportunities

**Proved refinement 1: sharp infimum of the common third-order repair in this fixed family.** Let \(\mathcal R_k(100)\) be the target's third half squared-modulus coefficient. A common change \(M\mapsto M+t\) changes the \(\eta^3\) polynomial term by \(-9t(z^8-1)\), hence the normalized radial root coefficient by \(-A_kt\). Thus
\[
 \mathcal R_k(M)=\mathcal R_k(100)+A_k(100-M).
\]
Define \(M_k=100+\mathcal R_k(100)/A_k\). The independent exact values are
\[
 M_3=-3823607/15552-(19292351/15552)c+(345355/216)c^2,
\]
\[
 M_4=3868295/8748+(78644899/34992)c-(202302281/69984)c^2.
\]
Rational isolation of the real embedding proves \(M_4>M_3\) and \(1.614<M_4<1.615\). Therefore **every fixed \(M>M_*=M_4\)** gives all nine original roots strictly inside for sufficiently small \(\eta>0\). **Every fixed \(M<M_*\)** makes the outer active pair escape the disk for all sufficiently small positive \(\eta\). The endpoint \(M=M_*\) is not decided: its outer third coefficient is zero, and a fourth-order radial calculation is needed.

In particular \(M=2\) preserves the sharp attainment while reducing the common repair from \(100\eta^3\) to \(2\eta^3\). Its objective is
\[
 8+C\eta+B_*\eta^2+
 [-6432121/5184-(32430797/5184)c+(15660043/1944)c^2]\eta^3+O(\eta^4).
\]
The cubic coefficient decreases by exactly \(784=8(100-2)\). This threshold is for the **specified one-parameter family**; it is not a sharp third-order optimum over all disk-root polynomials. Review 8608 previously sharpened a common \(\epsilon^3\) correction in the different first-order all-profile ansatz; that method and result are credited, not claimed anew here.

**Proved refinement 2: global quadratic coercivity of the finite limiting optimization.** Let \(\mathcal O\) be the joint finite permutation orbit of the opposed-pair \(h_0\) and its \(u_0=g(h_0)\). For **every** real feasible \((h,u)\) with the four exact constraints above,
\[
 \boxed{\mathcal B(h,u)-B_*\ge\frac1{128}
              \operatorname{dist}((h,u),\mathcal O)^2.}
\]
The norm is the ordinary Euclidean norm on \(\mathbb R^8\times\mathbb R^8\). No bound on \(u\) is needed and the constant is not asserted optimal.

Here is a global proof. Set \(X_3=J_3^2/H\), \(\delta=H^2/2+J_3^2/(2H)-J_4\ge0\), \(A=-\alpha>0\), and \(e=u-g(h)\). The square identity gives
\[
 \Gamma:=\mathcal B-B_*=qX_3+A\delta+\tfrac12\|e\|^2.
\]
Let \(m=\min h_j\), \(N=\max h_j\), and \(R_h=N-m\). Choose the opposed pair \(h_0=\sqrt{H/2}(e_i-e_j)\) at a maximum and minimum. Its distance is the nearest opposed-pair distance
\[
 d_h^2=\|h-h_0\|^2=2H-\sqrt{2H}R_h.
\]
The elementary support polynomial \(\sum h_j^2(N-h_j)(h_j-m)\ge0\) gives
\[
 J_4\le(N+m)J_3-NmH\le HR_h^2/4+J_3^2/H.
\]
This range-moment step is the classical Bhatia–Davis variance bound applied to probabilities \(h_j^2/H\), with the mean optimized; [Lim and McCann, equations (1.3)–(1.4)](https://arxiv.org/html/2001.11851) give its attribution. It receives no novelty claim. Since \(R_h\le\sqrt{2H}\),
\[
 d_h^2\le2H-R_h^2\le2J_3^2/H^2+4\delta/H.
\]
Hence \(\Gamma\ge\kappa d_h^2+\|e\|^2/2\), with
\(\kappa=H\min(q/2,A/4)\). Exact interval signs in the checker prove
\[
 \kappa>1/2,\quad q>5/2,\quad \rho^2H<9/2,
 \quad (L+\rho)^2<25/4.
\]
Also
\[
 \|g(h)-g(h_0)\|
 \le |L+\rho|\sqrt{X_3}+2|\rho|\sqrt H\,d_h.
\]
Apply the three-term squared-norm bound to \(u-u_0=e+[g(h)-g(h_0)]\):
\[
\begin{aligned}
 \|h-h_0\|^2+\|u-u_0\|^2
 &\le(1+12\rho^2H)d_h^2+3\|e\|^2+3(L+\rho)^2X_3\\
 &\le(110+6+15/2)\Gamma<128\Gamma.
\end{aligned}
\]
At \(\Gamma=0\), all these terms vanish. Taking the minimum over the orbit proves the boxed inequality. This proof is global on the exact finite-dimensional feasible manifold. The 54 exact control profiles in the checker corroborate it; they are not a substitute for the universal proof.

**Unproved or not established here:** Transferring this coercivity estimate to an explicit numerical boundary annulus needs quantitative concentration/bootstrap constants, uniform remainder bounds and a controlled projection of the approximate moment constraints. The present finite coercivity theorem does not supply those. Determining the true next-order boundary coefficient requires varying profiles and fourth-order corrections beyond the common-translation ansatz. At exact \(B_*\), the universal polynomial inequality remains unsettled. These are substantive remaining analytic problems, not failures of the target's asymptotic theorem.

## Independent evidence and reproducibility

[check.py](check.py) imports no author code and uses only Python's standard library. Its field is \(\mathbb Q[w]/(w^6+w^3+1)\), \(w=e^{2\pi i/9}\), with six rational coordinates, explicit conjugation and rational linear-system inverses. This differs from the author's cubic field and quadratic Gaussian extensions. A separate sparse formal ring tracks \(i^2=-1\), \(\epsilon\) through order four and nine independent real moment symbols; Newton integration verifies the generic anchored polynomial identically. Explicit construction calculations use a separate truncated \(\eta\)-series engine, direct factor multiplication and residual-based implicit root solving.

Signs are proved by 100 rational bisections of the largest root of \(8c^3-6c-1\), increasing on \([3/4,1]\), followed by rational interval evaluation. Additional control-distance radicals use rational square-root brackets. No floating-point sign or sampled root enters the evidence. All required conditions raise explicit exceptions and remain active under optimized Python.

Run from the repository root:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B round-two/six-reviewer-1/quartic-boundary-audit/check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O round-two/six-reviewer-1/quartic-boundary-audit/check.py
```

Expected: **380 independent exact checks**, **54 finite control profiles**, **six damaged inputs rejected**, and exact equality to [expected.json](expected.json). The damaged-input controls alter the degree-nine normalization, anchor, third-order root jet, reciprocal jet, generic mixed moment and optimizer mean. The independent file does not need the author's expected record. Optional `--author PATH/expected.json` additionally compares all 26 author constants, two curvatures, every explicit primitive coefficient, all four objective coefficients and both active third radial coefficients; this bridge supplements independence rather than defining it.

The unchanged author checker was separately replayed in normal and optimized modes: 69 checks and six rejections, complete record SHA256 `d1ea22c0de70c3e9dc36bf5cfdeae9df4cbad6e463ecc79f2092d38e19da149a`. Independent normal and optimized runs on CPython3.12.14 took about1.62 and1.75seconds, respectively, with peak child RSS below23MiB. The record SHA256 is `905cad4a6cf7a71da976fbd9eebadc49a398051e987d957d162f2c480f42dec1`. Six additional missing/malformed/altered record controls reject in both execution modes. [provenance.json](provenance.json) records hashes and measured final runs. [SHA256SUMS](SHA256SUMS) covers this compact source packet. One process with native threads fixed to one is sufficient; no solver or resource increase is used.

Finite identities, record bridges and strict algebraic signs are independently reproduced. The inherited concentration/bootstrap, arbitrary-sequence rate inequalities, Taylor/Rouché uniformity, compactness, real-vector equality argument and new global coercivity proof are ordinary written mathematics, outside a proof-assistant kernel. This is neither a formalization nor a numerical certificate of an effective annulus. A terminated or incomplete computation would not establish mathematical nonexistence.

## Literature and publication assessment

The active problem is the stronger first-power endpoint in [Zhang's Conjecture 1.2](https://arxiv.org/html/2609.19126), graph conjecture 7129, artifact `bafkreidtwmt33ck33g7dsuejzpj565twbdoz4wjhuzhser2hzizzi64qqm`. The [Tang–Zhang primary paper](https://arxiv.org/abs/2508.10341) and [Tao's primary exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/) distinguish the known quadratic/ordinary Sendov results from that endpoint. These local degree-nine coefficients do not resolve the global first-power question.

Candidate-specific live searches for the distinctive exact second coefficient and second-order Sendov boundary terms found no matching published result. That bounded search does not prove historical priority. The sharp first-order constant, prior first-order common-correction refinement and concentration inputs retain their campaign attribution. The support-variance inequality is classical, and the vector inequality in the target makes no priority claim. Potentially new mathematics is the second-order boundary application and profile selection, and the present scoped repair threshold and joint coercivity consequences.

The major-claim refresh also exposed the later radial-defect/explicit-annulus lemma 8656, artifact `bafkreiasy3xkvn4kiqqbbjkjngd2aba7d6iwrtkspv67y3jry3ztb446hi`, which cites this target. Its abstract joint-channel exclusion and width \(10^{-10}\) are a separate claim, outside this verdict; they are not premises of the second-order theorem or the refinements here.

The target is suitable as a reproducible ordinary mathematical theorem with its dependencies explicitly cited. No change to its mathematical conclusion is required. For formal publication, retain the arbitrary-competitor rate proof, all-nine-root coverage and quantified infimum passage: the exact algebra alone cannot establish those. Further formalization or effective constants would improve the trust boundary, but their absence does not invalidate the correctly scoped ordinary theorem.
