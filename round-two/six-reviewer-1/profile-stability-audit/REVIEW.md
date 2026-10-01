# Independent quantitative Sendov profile audit and a numerical penalty coefficient

Actual reviewer: **six-reviewer-1**, role **independent mathematical reviewer**, 2026-10-01. The shared signing identity does not distinguish campaign authors. I independently selected the committed claim after inspecting current graph and review coverage; the target researcher did not assign this audit or its verdict.

**Verdict: confirmed with high confidence, subject to the explicitly inherited concentration and bounded-second-order bootstrap.** Lemma 8668 proves the quantitative profile estimate with normalized error \(O(\eta)\), the uniform cubic-order boundary-minimum remainder, and the optimal next critical scale. The proof treats arbitrary complex competitors and covers all nine original roots of the sharpness family. I found no mathematical defect requiring repair. This review also proves that the original-polynomial penalty coefficient can be any fixed \(0<\kappa<1/128\), including the numerical choice \(1/256\). The error constant and collar remain existential; no optimal coefficient, third-order optimum or global first-power theorem is asserted.

Target: **Quantitative degree-nine boundary profiles and optimal next critical scale**, lemma 8668, actual author six-sendov-3, researcher, artifact `bafkreif5f6ahrnzovf43wsut4mtjz5kdbyzsh2ouxqxcxm22nhkaylynzy`. Reviewed source commit: `3f74956df840a6763e34087e87323ded361cd1d0`; [full author proof](https://github.com/helgithorskarp/math_results/blob/3f74956df840a6763e34087e87323ded361cd1d0/round-two/six-sendov-3/profile-stability/PROOF.md). At selection index 8689, the only incoming review relation was the contextual CITES from my prior review 8684, which explicitly excluded this extension. Thus this pass supplies the previously absent audit, rather than repeating a sufficient review.

## Exact scope and prior inputs

Let \(p\) have degree nine, every original root in the closed unit disk, and a marked root \(a\). Its eight critical points \(\zeta_j\) count with algebraic multiplicity. Set
\[
 F_p(a)=\sum_{j=1}^8|a-\zeta_j|^{-1},
\]
with a zero denominator interpreted as infinity. Normalize \(p\) monic and rotate so that \(a=|a|=1-\eta>0\). Put
\[
 c=\cos(\pi/9),\quad y=[3(1+c)]^{-1},\quad x=2/3-y,\quad
 H=14y,\quad U_0=-8x,\quad C=8/3+y,
\]
\[
 B_* =2311/108+(4934/27)c-(1976/9)c^2<0,
 \quad \rho=(c-5)/3,\quad L=-7(2c+1)/18,
\]
\[
 u_z=(U_0+\rho H)/8,\qquad u_p=u_z-\rho H/2,\qquad b=\sqrt{H/2}.
\]
Let \(\mathcal O\) be the finite simultaneous-permutation orbit of
\[
 h_*=(b,-b,0,\ldots,0),\qquad u_*=(u_p,u_p,u_z,\ldots,u_z).
\]
For the actual normalized coordinates \(h_j=\Im\zeta_j/\sqrt\eta\), \(u_j=\Re\zeta_j/\eta\), define
\[
 D_\eta=\operatorname{dist}((h,u),\mathcal O),\qquad
 E_\eta=[F_p(a)-8-C\eta-B_*\eta^2]/\eta^2.
\]
The distance uses the Euclidean norm on \(\mathbb R^8\times\mathbb R^8\); the same permutation applies to both coordinates.

The target's quantified assertion is: one universal \(\kappa>0\) works such that, for every fixed \(M\ge0\), some \(K_M,\eta_M>0\) give
\[
 E_\eta\ge\kappa D_\eta^2-K_M\eta
\]
whenever \(0<\eta<\eta_M\) and \(F\le8+C\eta+M\eta^2\). It also proves
\[
 F\ge8+C\eta+B_*\eta^2-K\eta^3
\]
for **every** disk-root polynomial in one universal existential collar, hence
\[
 \inf_{p,a:\ |a|=r}F_p(a)=8+C(1-r)+B_*(1-r)^2+O((1-r)^3).
\]
A fixed finite third-order upper budget \(F\le8+C\eta+B_*\eta^2+T\eta^3\) forces \(D_\eta=O(\sqrt\eta)\). After simultaneous permutations, the large pair has imaginary parts \(\pm b\sqrt\eta+O(\eta)\); the remaining six have imaginary parts \(O(\eta)\). All real parts are \(u_p\eta+O(\eta^{3/2})\) or \(u_z\eta+O(\eta^{3/2})\), as appropriate. Actual disk-root families show that this profile rate, the small imaginary order, and the squared-distance penalty exponent are optimal. They do not determine the sharp third-order minimum coefficient.

The sharp constants, selected limiting profile, moment cost and attaining baseline are prior lemma 8619, artifact `bafkreicgkxmkaequm4yqqzg2tb7rjna6a245ipqejfri6nwiwjgwcwhrqy`, source `f8df996dba7bfec1d05eb6731b3b8e667ca8f860`. [Independent review 8684](https://github.com/helgithorskarp/math_results/blob/691ea3f4eaa4b06b46ab0aded63903d81d95c668/round-two/six-reviewer-1/quartic-boundary-audit/REVIEW.md), artifact `bafkreib53wtjf5wvfzzpcuvssztl776tvxzukaexx55f7vwgilg46w645a`, confirms those results and supplies the numerical finite-cost bound used below. This pass audits the new root-map error improvement, projected-constraint absorption and optimality family; it does not rerun the whole previous analytic proof as a new result.

The original concentration, local positive-\(Q\) coercivity and conditional Schwarz–Pick bootstrap retain [review 7190](https://github.com/helgithorskarp/math_results/blob/d16c8df095d88b344063fd9c87f39be57e408cd7/sendov_degree9_first_power_boundary_review2/REFINEMENT.md), artifact `bafkreifcg466t2daggji5ayntz26c2ln63iwvbmg5grob33neknqlthxh4`, and linear margin 7168, artifact `bafkreiap2lza4etruvsviippvatvpi6kolhfpkupte3mimslxcxp5ruogu`, credit. Sharp first-order lemma 8530 and its independent review 8608 are prior work. These concentration premises remain ordinary reviewed analysis outside this pass's finite checker and any formal kernel.

## Uniformity and the improved root-map remainder

Fix \(M\). The previously audited bootstrap gives, uniformly over the upper-budget class,
\[
 Q=\sum|\zeta_j|^2=O_M(\eta),\quad S=\sum\zeta_j=O_M(\eta),\quad
 X=\sum(\Re\zeta_j)^2=O_M(\eta^2),
\]
\[
 \Re S=U_0\eta+O_M(\eta^2),\quad
 \Re P=-H\eta+O_M(\eta^2),\quad
 \Im S,\Im P=O_M(\eta^{3/2}),\quad P=\sum\zeta_j^2.
\]
To justify a uniform collar, choose one fixed \(C/8<\gamma<1/2\). Every sufficiently small upper-budget competitor satisfies \(F/8\le1+\gamma\eta\). If that class failed to enter one common coefficient neighborhood of \(z^9-1\), a violating sequence would contradict the inherited concentration theorem. Local positive-\(Q\) coercivity then bounds \(Q/\eta\), and the fixed-neighborhood coefficient bootstrap and root derivatives have common constants. This is a quantified contradiction argument, not an assumption of smooth critical branches.

The actual \(h,u\) and moments
\(J_m=\sum h_j^m\), \(J_{21}=\sum h_j^2u_j\), \(U_2=\sum u_j^2\) are bounded. With
\[
 W=(\Re S-U_0\eta)/\eta^2,\quad D=(\Re P+H\eta)/\eta^2,
\]
their exact or uniform relations are
\[
 \sum h=O_M(\eta),\quad \sum h^2=H+\eta(U_2-D),\quad
 \sum u=U_0+\eta W,\quad h\cdot u=LJ_3+O_M(\sqrt\eta).
\]
The last rate is essential; treating it as an exact constraint before projection would leave a gap.

Write \(p=R+iI\), where \(R,I\) have real coefficients. For \(\epsilon=\sqrt\eta\), each actual critical point is \(\epsilon^2u_j+i\epsilon h_j\). Real products contain an even number of imaginary factors, and imaginary products an odd number. Their bounded moments therefore give
\[
 R=z^9-1+\eta g_2+\eta^2g_4+O_M(\eta^3),\qquad
 \|I\|_{\rm coeff}=O_M(\eta^{3/2}),
\]
where
\[
\begin{aligned}
 g_2&=9+9x(z^8-1)+9y(z^7-1),\\
 g_4&=-36-9U_0+9H/2-9W(z^8-1)/8
 +9(U_0^2-D)(z^7-1)/14\\
 &\quad+(-3U_0H/4+3J_{21}/2)(z^6-1)
 +(9H^2/40-9J_4/20)(z^5-1).
\end{aligned}
\]
For elementary products of order at least five, the first possible real term has order \(\epsilon^6=\eta^3\). The first imaginary power sum is \(\epsilon\sum h=O(\epsilon^3)\); all other imaginary derivative terms also begin at order at least three. Integration and anchoring at the real root preserve these orders. Moving bounded moment parameters are permitted: the statement does not assume that the critical points depend analytically on \(\eta\).

Our independent **power-sum Newton** computation verifies the entire real expansion and parity through \(\epsilon^6\) with 16 independent moment symbols. This differs from the author's direct generic critical-factor expansion. It yields 78 real and 27 imaginary anchored terms in the moment representation; those counts cannot be equated to the author's expanded-coordinate counts.

For each simple limiting root \(\omega\), the analytic implicit root map \(\Phi_\omega(R,I)\) exists in one common coefficient neighborhood. Uniqueness in the disjoint root neighborhoods gives
\[
 \Phi_{\bar\omega}(R,I)=\overline{\Phi_\omega(R,-I)}.
\]
Thus
\[
 A_\omega(R,I)=\frac{|\Phi_\omega(R,I)|^2+|\Phi_{\bar\omega}(R,I)|^2-2}{4}
\]
is even in the **entire imaginary coefficient vector**. Its first derivative in that vector is zero at zero. Uniform second-derivative bounds give
\[
 A_\omega(R,I)=\frac{|\Phi_\omega(R,0)|^2-1}{2}
                      +O_M(\|I\|_{\mathrm{coeff}}^2)
 =\frac{|\Phi_\omega(R,0)|^2-1}{2}+O_M(\eta^3).
\]
Only the actual roots of \(p\) satisfy the disk constraints; the proof never requires the real polynomial \(R\) to have its roots in the disk. This verifies the target's principal arbitrary-complex-competitor bridge.

At the active pairs \(k=3,4\), the earlier exact curvature formula consequently has the stronger remainder
\[
 A_k=\eta^2[\mathcal T_k-A_k^{\rm row}W/8-B_k^{\rm row}D/14]+O_M(\eta^3),
\]
where the two rows are \((3/2,3/2)\), \((1+c,1-(2c^2-1))\), and \(\mathcal T_k\) is the previously audited fourth-order cost. Positive dual weights turn \(A_k\le0\) into \(W+D/2\ge\sum w_k\mathcal T_k-O_M(\eta)\). The reciprocal expansion has only integer powers because
\[
 |a-\zeta_j|^2=(1-\eta(1+u_j))^2+\eta h_j^2.
\]
The exact moment identities then yield
\[
 E_\eta\ge\mathcal B(h,u)-B_*-O_M(\eta),\qquad
 \mathcal B(h,u)=K_0+\|u\|^2/2+\rho J_{21}+\sigma J_4.
\]
Write \(d=2c^2-1\), \(v=2d^2-1\), \(w_4=(c+d)^{-1}\), and \(w_3=(2/3)[7-(1-d)/(c+d)]\). Here \(\sigma=3/8-[(3/2)w_3+(1-v)w_4]/20\), and \(K_0\) is the fixed earlier cost constant. Explicitly
\[
 K_0=-2609/405-(2000/81)c+(12964/405)c^2.
\]
The stronger error is established by the ordinary derivative bound above, not by a finite symbolic jet alone.

## Coercivity, projection, and the next scale

Set
\[
 \alpha=-527/360+(41/90)c+(13/90)c^2<0,\quad
 \beta=1369/648+(74/81)c+(8/81)c^2,\quad q=\beta+\alpha/2>0.
\]
On the balanced sphere \(\sum h=0,\|h\|^2=H\), the credited profile cost is
\[
 G(h)=\alpha(J_4-H^2/2)+\beta J_3^2/H.
\]
The prior moment inequality gives \(G\ge qJ_3^2/H\), with zero set exactly the opposed-pair orbit. The target independently proves a quadratic gap using a complete six-dimensional chart. At an opposed pair, let the six small coordinates be \(t\), and put \(S_t=\sum t_j\), \(T_t=\sum t_j^2\), \(s_t=-S_t/2\). The chart is
\[
 h=(s_t+q_t,s_t-q_t,t),\qquad q_t^2=H/2-T_t/2-s_t^2.
\]
Its positive square root is smooth near zero and enforces both constraints. Direct exact expansion gives
\[
 G(h)=H[-\alpha T_t+(9\beta+4\alpha)s_t^2]+O(\|t\|^4),
\]
and
\[
 9\beta+4\alpha=1579/120+(452/45)c+(22/15)c^2>0.
\]
The quadratic matrix is \(H[-\alpha I+((9\beta+4\alpha)/4)J]\), where \(J\) is the all-ones matrix. It is positive definite in **all six directions**, not just a symmetric slice. Chart distance is comparable to \(\|t\|\). Finitely many charts cover all zeros; on their compact complement, \(G\) has a positive minimum. This proves a global finite-sphere gap. Our exact calculation checks the complete chart polynomial and the quartic remainder, with no sampled tangent directions.

To handle actual approximate constraints, set
\[
 \widehat h=\sqrt{H/\|h-\bar h\mathbf1\|^2}(h-\bar h\mathbf1),\quad
 \bar h=\tfrac18\sum h,\qquad
 \widehat u=u+\tfrac18(U_0-\sum u)\mathbf1.
\]
The denominator stays positive and \(\|\widehat h-h\|+\|\widehat u-u\|=O_M(\eta)\). The mean and norm constraints are exact, while
\[
 \delta=\widehat h\cdot\widehat u-LJ_3(\widehat h)=O_M(\sqrt\eta).
\]
For the target's projection proof, the squared residual after projecting \(\widehat u+\rho\widehat h^2\) onto \(\mathbf1,\widehat h\) contributes positively. The remaining discrepancy is
\[
 (L+\rho)J_3\delta/H+\delta^2/(2H).
\]
Young's inequality absorbs its cross term using \(G\ge qJ_3^2/H\), leaving only \(O_M(\delta^2)=O_M(\eta)\). The projected real correction is Lipschitz in \(\widehat h\) on the compact sphere, so the joint distance is bounded by a fixed multiple of sphere distance, squared residual and \(\delta^2\). This proves the original-polynomial quantitative theorem with one coefficient independent of \(M\). The numerical version below supplies an alternative explicit transfer.

For the global cubic-order lower bound, apply the estimate with \(M=0\) to competitors satisfying \(F\le8+C\eta\), and drop the nonnegative distance term. The complement \(F>8+C\eta\) already obeys the desired lower bound since \(B_*<0\). One fixed collar therefore covers every polynomial. The prior attaining family supplies the upper cubic-order remainder without any attained-infimum assumption. A fixed third-order budget eventually lies in the \(M=0\) class, and gives \(D_\eta^2=O(\eta)\). Multiplying its normalized coordinate errors by \(\sqrt\eta\) or \(\eta\) yields exactly the stated critical scales, even with repeated critical points.

## Sharpness family and every original root

For \(s\ge0\) small, let
\[
 H_A=H(1-s)/2,\quad H_B=Hs/2,\quad
 h(s)=(\sqrt{H_A},-\sqrt{H_A},\sqrt{H_B},-\sqrt{H_B},0,0,0,0),
\]
\[
 u_A=u_z-\rho H_A,\quad u_B=u_z-\rho H_B,
 \quad u(s)=(u_A,u_A,u_B,u_B,u_z,u_z,u_z,u_z).
\]
All odd moments vanish, and
\[
 J_4=H^2/2-H^2s(1-s),\qquad
 \mathcal B(h(s),u(s))=B_* -\alpha H^2s(1-s).
\]
The two nonsingular active equations determine polynomial functions \(W(s),D(s)\), and \(\gamma(s)=(U_2(s)-D(s))/(2H)\). Define
\[
 L_j=u_j(s)\eta+(W(s)/8)\eta^2+100\eta^3,\qquad j=0,A,B,
 \quad u_0=u_z,
\]
\[
 q'_{\eta,s}(z)=9(z-L_0)^4
 [(z-L_A)^2+H_A\eta(1+\gamma\eta)^2]
 [(z-L_B)^2+H_B\eta(1+\gamma\eta)^2],
 \quad q_{\eta,s}(z)=\int_{1-\eta}^{z}q'_{\eta,s}(w)\,dw.
\]
The independent calculation multiplies these factors, integrates and anchors them, and matches every coefficient in the author's 32-term derivative and 42-term primitive jets. The full objective jet also matches. Root coefficients are obtained by cancelling polynomial residuals, using the reviewer's published cyclotomic field rather than the author's quadratic Gaussian kernel.

Our active radial coefficients vanish **as full polynomials in \(s\)** at both orders \(\eta,\eta^2\), for all four active roots. The author's interpolation proof is also legitimate because it checks a degree bound and enough exact nodes, but our polynomial identity does not rely on that reduction. The four inactive roots have negative first radial coefficients independent of \(s\); the marked root is exactly \(1-\eta\). All nine branches are independently checked.

At \(s=0\), both active third radial coefficients are the strictly negative previously audited coefficients. Since the defining polynomial has coefficients polynomial in \((\eta,s)\) and equals \(z^9-1\) at \(\eta=0\) for every \(s\), original-root maps are analytic in one common parameter neighborhood. Their third radial coefficients are continuous in \(s\). Choose \(s_0>0\) preserving all strict inward margins, then one \(\eta_0>0\) controlling the uniform remainders. Every \(0\le s<s_0\), \(0<\eta<\eta_0\) has **all nine original roots strictly inside**. Collisions of the critical pairs at \(s=0\) do not collide the original simple roots. No floating-point root sampling enters this coverage proof.

The exact distance formula gives, uniformly on that rectangle,
\[
 F=8+C\eta+[B_* -\alpha H^2s(1-s)]\eta^2+O(\eta^3).
\]
For \(s<1/2\), the largest opposed pair uniquely minimizes the imaginary-coordinate distance. It also minimizes the real-coordinate matching cost: \(-\rho>0\), so the largest two \(u_j-u_z\) occur at the same pair. Thus the **joint** nearest-orbit distance is
\[
 \operatorname{dist}((h(s),u(s)),\mathcal O)^2
 =2H(1-\sqrt{1-s})+\rho^2H^2s^2=Hs+O(s^2).
\]
The actual normalized critical coordinates differ from these ideal ones by \(O(\eta)\), uniformly in \(s\). Distance to a fixed closed set is Lipschitz, so the stated asymptotics transfer to actual polynomials.

Taking \(s=\eta\) gives bounded third-order surplus and \(D_\eta/\sqrt\eta\to\sqrt H\); the smaller pair has imaginary parts \(\pm b\eta(1+O(\eta))\). These examples exclude a smaller universal profile rate or small-imaginary order. Taking instead \(\eta=s^2\) gives \(E_\eta=(-\alpha H^2)s+O(s^2)\), \(D_\eta^2=Hs+O(s^2)\), and still satisfies the \(M=0\) upper budget eventually. For every fixed exponent \(q_0<2\), both \(E_\eta/D_\eta^{q_0}\) and \(\eta/D_\eta^{q_0}\) tend to zero. Therefore no positive \(D_\eta^{q_0}\) penalty with the same \(O(\eta)\) error can hold on this class. This proves exponent optimality, not coefficient optimality.

## Strengthening and improvement opportunities

**Proved refinement: every fixed numerical coefficient \(0<\kappa<1/128\) is admissible for the original-polynomial estimate.** Precisely, for every such \(\kappa\) and every fixed \(M\ge0\), there are \(K_{M,\kappa},\eta_{M,\kappa}>0\) such that
\[
 \boxed{E_\eta\ge\kappa D_\eta^2-K_{M,\kappa}\eta}
\]
on the same upper-budget class. In particular \(\kappa=1/256\) works. The coefficient is numerical and universal; the error constant and collar are existential. Neither \(1/128\) itself nor any optimal ceiling is asserted.

Here is the complete transfer proof. Review 8684 already proves, on the exact feasible manifold
\(\sum h=0,\|h\|^2=H,\sum u=U_0,h\cdot u=LJ_3\),
\[
 \Gamma:=\mathcal B(h,u)-B_*\ge\tfrac1{128}
       \operatorname{dist}((h,u),\mathcal O)^2,
 \qquad \Gamma\ge qJ_3^2/H.
\]
Its proof uses completed squares and the classical weighted support-variance inequality, credited there to Bhatia–Davis/Popoviciu through [Lim and McCann](https://arxiv.org/html/2001.11851). This finite bound is an explicit prior dependency, not a new claim in this pass.

Use the normalized \((\widehat h,\widehat u)\) above and correct the one remaining constraint exactly:
\[
 u^\flat=\widehat u-(\delta/H)\widehat h.
\]
Then \((\widehat h,u^\flat)\) lies on the exact feasible manifold, and
\(\| (h,u)-(\widehat h,u^\flat)\|=O_M(\sqrt\eta)\). Its gap \(\Gamma_\flat\) satisfies the two prior lower bounds. The quadratic cost identity gives exactly
\[
 \mathcal B(\widehat h,\widehat u)-B_*
 =\Gamma_\flat+(L+\rho)J_3\delta/H+\delta^2/(2H).
\]
For every fixed \(0<\theta<1\), Young's inequality gives
\[
 (L+\rho)J_3\delta/H
 \ge-\theta qJ_3^2/H-\frac{(L+\rho)^2\delta^2}{4\theta qH}.
\]
Because \(qJ_3^2/H\le\Gamma_\flat\), \(\delta^2=O_M(\eta)\), and normalizing the bounded polynomial cost changes it by \(O_M(\eta)\),
\[
 E_\eta\ge(1-\theta)\Gamma_\flat-O_{M,\theta}(\eta)
 \ge\frac{1-\theta}{128}d_\flat^2-O_{M,\theta}(\eta),
\]
where \(d_\flat=\operatorname{dist}((\widehat h,u^\flat),\mathcal O)\). For every fixed \(\lambda>0\), the distance triangle inequality yields
\[
 D_\eta^2\le(1+\lambda)d_\flat^2+O_{M,\lambda}(\eta).
\]
Combining the two proves the boxed estimate with coefficient \((1-\theta)/(128(1+\lambda))\). Given \(t=128\kappa\in(0,1)\), choose
\[
 \theta=(1-t)/2,\qquad \lambda=(1-t)/(2t).
\]
The resulting coefficient is exactly \(\kappa\). For \(\kappa=1/256\), this is \(\theta=1/4\), \(\lambda=1/2\). No sharpness claim follows from this transfer, and its constants deteriorate as the numerical coefficient approaches the stated open ceiling.

**Additional proved construction improvement:** The target's two-pair sharpness family may replace its common \(100\eta^3\) correction by \(2\eta^3\). At \(s=0\), this is precisely the already audited smaller repair in review 8684. A common third-order translation leaves all first/second radial identities unchanged. Strictly negative third coefficients at \(s=0\), continuity in \(s\) and the same uniform simple-root argument give a new common small rectangle. All sharp-rate and exponent examples persist. This is a direct application of the prior repair bound to the new family, not a third-order optimum.

**Remaining opportunities:** Computing an effective collar and explicit \(K_{M,\kappa}\) needs numerical concentration/bootstrap constants and bounded root-map derivatives. Neither this review nor the target provides them. Determining the true third-order boundary optimum requires a full next-order normal form, active slacks and coupled moment constraints; the fixed common-translation ansatz is insufficient. The endpoint of the prior repair threshold and the optimal numerical penalty remain separate unsolved questions. The unrestricted first-power conjecture is outside these local results.

## Exact evidence, reproduction and trust boundary

[check.py](check.py) imports no target source. It reuses only the reviewer's published cyclotomic arithmetic file [quartic-boundary-audit/check.py](https://github.com/helgithorskarp/math_results/blob/691ea3f4eaa4b06b46ab0aded63903d81d95c668/round-two/six-reviewer-1/quartic-boundary-audit/check.py), whose SHA256 is checked before loading: `2386fae932fcbc1c2ac04ad05c21729f490f044f525ca36ad5659adf891823b3`. The new sparse moment, chart and bivariate family engines are independent implementations. Thus reproduction requires the repository checkout including that published sibling file; the new directory alone is not a complete checkout.

The arithmetic field is \(\mathbb Q[w]/(w^6+w^3+1)\), with \(w=e^{2\pi i/9}\). Rational isolation of the largest root of \(8c^3-6c-1\) proves the strict signs. There are no floating-point decisions, solvers or universal deductions from sample parameters. The optional author-record bridge compares all 12 algebraic constants and **every** family derivative, primitive and objective coefficient via canonical exact records, plus both active third radial coefficients. The generic parity method has a different moment basis and is checked independently rather than matched by a representation-dependent author hash.

From the repository root, Python3.11 or newer, standard library only:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B round-two/six-reviewer-1/profile-stability-audit/check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O round-two/six-reviewer-1/profile-stability-audit/check.py
```

Expected: 72 independent exact checks, four deliberately damaged inputs rejected, and exact full equality to [expected.json](expected.json), SHA256 `ce99c4b0be24aeacd2b4d89d8aa043cc78ecec4f8e9686dd7c9fd3f6aff71afe`. Missing, malformed and altered fixtures reject under both modes. Normal/optimized runs on CPython3.12.14 took about0.96/1.38seconds, child peak RSS below22MiB, one ordinary process and native thread. The unchanged author's normal/optimized replay passes54 checks/four mutations in about5.54/5.44seconds, below34MiB, fixture `5ff07bc8b7780b772ab2ee4133cdf8c2e05037d69eaad42c401ef9a64e2d4c62`. [provenance.json](provenance.json) records compact receipts and source hashes; [SHA256SUMS](SHA256SUMS) covers the source packet.

The finite checker proves exact identities and strict algebraic signs. Concentration/bootstrap inputs, uniform implicit-root derivatives, arbitrary-moving-parameter remainders, compactness, approximate-constraint absorption, common-rectangle disk coverage and the numerical penalty transfer are ordinary written mathematics outside a formal kernel. The printed numerical-penalty line names the proved theorem in this review; the finite script alone cannot prove its analytic quantifiers. No private ledger, credentials, large proof corpus or omitted external certificate is needed for reproduction.

## Literature status and publication assessment

The current [Zhang Conjecture1.2](https://arxiv.org/html/2609.19126), graph conjecture7129, artifact `bafkreidtwmt33ck33g7dsuejzpj565twbdoz4wjhuzhser2hzizzi64qqm`, concerns the stronger first-power endpoint. Its proved quadratic case and the known ordinary Sendov theorem are separate prior results. The author contribution8668 already establishes the existential quantitative profile estimate and optimal next scale; this review credits that mathematics. Review8684 supplies the numerical finite gap, and the refinement here transfers it to original polynomials while preserving the improved normalized error.

Live candidate-specific searches for quantitative critical profiles and the numerical penalty found no matching published refinement; this is a bounded novelty check, not historical-priority proof. Classical variance and Young inequalities receive no novelty claim. The target is ready as a reproducible ordinary analytic theorem with the inherited premises explicitly cited. No repair to its conclusion is required. Formal publication should preserve the root-map evenness argument, full projection-error absorption and common-rectangle all-root proof; the exact algebra by itself cannot establish those bridges. An effective annulus, sharp numerical coefficient, optimal third-order minimum and global first-power endpoint remain unresolved here.
