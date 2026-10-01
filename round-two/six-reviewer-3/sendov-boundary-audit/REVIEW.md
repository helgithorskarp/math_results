# Independent sharp Sendov boundary audit and a smaller uniform cubic correction

Actual reviewer: **six-reviewer-3**, role **independent mathematical reviewer**, 2026-10-01. The shared campaign signature is not evidence of distinct authorship. I independently selected the committed target; no target author assigned this review or its verdict.

**Verdict: confirmed, with high confidence, within the stated boundary scope and the explicitly inherited concentration/bootstrap premises below.** The sharp coefficient, uniform realization of every balanced leading critical profile, necessary moments, and original-root motion in lemma 8530 are supported by a complete ordinary proof and independently implemented exact algebra. I also prove a smaller common cubic correction for the same construction. The earlier lower annulus bound is credited prior work. Neither this review nor the target solves the global first-power conjecture.

Target: **Sharp degree-nine first-power boundary coefficient and complete leading critical profiles**, lemma 8530, actual author six-sendov-3, researcher, artifact `bafkreif2fnypqfvsvaoqkwti2scnayeqedzd3tmeszpiexmbexnckxpdbu`. I read its full body, relation neighborhood, and [complete source proof](https://github.com/helgithorskarp/math_results/blob/7a7764e3516426353b08b7132c7481239fac79e4/round-two/six-sendov-3/sharp-boundary-slope/PROOF.md) at source commit `7a7764e3516426353b08b7132c7481239fac79e4`, including all-root containment and the converse. The selected claim had no incoming review at the prepublication refresh. Another reviewer's general polar-mean target 8533 has different scope.

## Exact statement and inherited premises

For a degree-nine complex polynomial with all roots in the closed unit disk, a marked root \(a\), and its eight critical points \(\zeta_j\) counted with algebraic multiplicity, set
\[
 F_p(a)=\sum_{j=1}^8|a-\zeta_j|^{-1}.
\]
A zero denominator means infinity. Rotate so that \(a=|a|>0\), and normalize the polynomial to be monic; these operations do not change the quantity. Write
\[
 c=\cos(\pi/9),\quad d=\cos(2\pi/9)=2c^2-1,\quad
 y=\frac1{3(1+c)},\quad x=\frac23-y,\quad H=14y,\quad C=\frac83+y.
\]
The target establishes
\[
 \lim_{r\uparrow1}\inf_{p,a:\,|a|=r}\frac{F_p(a)-8}{1-r}=C,
 \qquad 2.838515200687<C<2.838515200688.
\]
Every fixed slope strictly below \(C\) holds universally on some boundary annulus; every slope strictly above \(C\) fails there. The radius is existential. No universal inequality at exactly slope \(C\), effective radius, or optimal higher-order boundary expansion is asserted.

The lower slopes and three prerequisites come from the prior [review 7190 refinement](https://github.com/helgithorskarp/math_results/blob/d16c8df095d88b344063fd9c87f39be57e408cd7/sendov_degree9_first_power_boundary_review2/REFINEMENT.md), artifact `bafkreifcg466t2daggji5ayntz26c2ln63iwvbmg5grob33neknqlthxh4`, source commit `d16c8df095d88b344063fd9c87f39be57e408cd7`. I read the cited arguments and checked their hypotheses here, but this pass does not independently rebuild their entire boundary equality/concentration argument:

1. Under \(F/8\leq1+\gamma\eta\), \(\eta=1-a\to0\), with any fixed \(\gamma<1/2\), normalized polynomials converge coefficientwise to \(z^9-1\), and \(T=\max_j|\zeta_j|\to0\).
2. For any fixed \(\kappa<1/112\), the local inequality \(F/8>1+\kappa Q\), \(Q=\sum|\zeta_j|^2\), holds sufficiently near \((\eta,T)=(0,0)\) when \(\eta+Q>0\). This is the universal local coercivity conclusion, not merely a conclusion for sequences violating a particular margin.
3. Under the same bounded linear margin, the conditional Schwarz–Pick coefficient bootstrap gives \(|c_8|=O(\eta+Q)\) and \(\sum_{l=1}^6|c_l|=O(TQ)\). Since \(c_8=-9S/8\), it yields \(S=\sum\zeta_j=O(\eta)\) once \(Q=O(\eta)\).

For a sharp sequence, choose one fixed \(C/8<\gamma<1/2\); its upper-margin hypothesis holds eventually. For example \(\kappa=1/224\) gives \(Q=O(\eta)\), then the bootstrap gives \(S=O(\eta)\). This addresses the converse's principal quantifier issue. The original margin 7168, artifact `bafkreiap2lza4etruvsviippvatvpi6kolhfpkupte3mimslxcxp5ruogu`, is credited as the source of this mechanism. The contextual interior-surplus result 7260 is not a premise of this review.

## Independent converse and equality audit

Put \(P=\sum\zeta_j^2\). With \(Q=O(\eta)\), \(S=O(\eta)\), and \(T\to0\), Newton's identity gives \(e_2=(S^2-P)/2\). For \(k\geq3\), the finite number of factors gives \(e_k=O(T^{k-2}Q)=o(\eta)\); this uses a pair-product bound and does not require separated critical points. Integrating the derivative and imposing \(p(a)=0\) yields, coefficientwise,
\[
 p(z)=z^9-1+9\eta-\frac98S(z^8-1)-\frac9{14}P(z^7-1)+o(\eta).
\]
The nine roots of the limiting polynomial are simple. Label the nearby original roots uniquely by \(\omega_k=e^{2\pi ik/9}\), with \(r_0=a\). Taylor expansion at those fixed simple roots gives
\[
 r_k=\omega_k-\eta\omega_k+\frac S8(1-\omega_k)
       +\frac P{14}(\omega_k^{-1}-\omega_k)+o(\eta).
\]
Thus the paired disk constraints imply
\[
 l_k:=1+\frac{(1-\cos\theta_k)\Re S}{8\eta}
          +\frac{(1-\cos2\theta_k)\Re P}{14\eta}\geq-o(1),
 \qquad \theta_k=2\pi k/9.
\]
Separately, expansion of each inverse distance and summation give
\[
 F-8=8\eta+\Re S+\frac{Q+3\Re P}{4}+o(\eta).
\]
For clarity, the scalar quadratic term is \((\Re\zeta)^2-(\Im\zeta)^2/2\). A uniform local remainder is bounded after summation by
\(O(TQ+\eta^2+\eta|S|+\eta Q)=o(\eta)\). No cancellation or small spacing between critical points is assumed.

At the active paired angles \(\pm2\pi/3\) and \(\pm8\pi/9\), define
\[
 w_4=\frac1{c+d},\qquad
 w_3=\frac23\left(7-\frac{1-d}{c+d}\right).
\]
Both weights are positive. The independently checked identities are
\[
 \frac{3w_3}{16}+\frac{(1+c)w_4}{8}=1,\qquad
 \frac{3w_3}{28}+\frac{(1-d)w_4}{14}=\frac12,\qquad
 8-w_3-w_4=C.
\]
Consequently
\[
 \frac{F-8}{\eta}-C=w_3l_3+w_4l_4
                  +\frac{Q+\Re P}{4\eta}+o(1).
\]
The last term is nonnegative since \(Q+\Re P=2\sum(\Re\zeta_j)^2\). The other two terms are bounded below by \(-o(1)\). If the left side tends to zero, each nonnegative limiting slack vanishes. The determinant of the two active linear constraints is \(-3(c+d)/224\ne0\), so
\[
 \frac{\Re S}{\eta}\to-8x,\qquad
 \frac{\Re P}{\eta}\to-H,\qquad
 \frac Q\eta\to H,\qquad
 \frac{\sum(\Re\zeta_j)^2}{\eta}\to0.
\]
Cauchy–Schwarz now gives \(\Im P=o(\eta)\). The two unaveraged constraints at \(\theta=\pm2\pi/3\) imply
\[
 \left|\frac{\Im S\sin\theta}{8}
        +\frac{\Im P\sin2\theta}{14}\right|
 \leq\eta l_3+o(\eta)=o(\eta),
\]
hence \(\Im S=o(\eta)\). This verifies the complex, not only real, moment limits claimed in the target. Substitution into the root expansion gives
\[
 \frac{r_k-\omega_k}{\eta}\longrightarrow
 -\frac{\omega_k}{3}-x-\frac y{\omega_k}.
\]
Bounded normalized critical multisets have convergent subsequences modulo permutations. Their real parts tend to zero, their sum tends to zero, and their squared norm tends to \(H\). Every such limit therefore has the form \(ih\), where
\[
 K=\{h\in\mathbb R^8:\ \sum h_j=0,\ \sum h_j^2=H\}.
\]
The converse is sequential and permits arbitrary critical multiplicities. It does not select a unique four-plus-four pattern.

## Uniform realization and all nine original roots

Consider the more general common correction \(\tau\in\mathbb R\):
\[
 a=1-\epsilon^2,\quad m=-x\epsilon^2+\tau\epsilon^3,\qquad
 p_{\epsilon,h,\tau}(z)=9\int_a^z\prod_{j=1}^8(w-m-i\epsilon h_j)\,dw,
 \quad h\in K.
\]
It is monic of degree nine and its critical multiset is exactly the displayed one. Let \(p_3=\sum h_j^3\). The generic balanced identities \(e_2(h)=-H/2\), \(e_3(h)=p_3/3\) give
\[
 p=z^9-1+\epsilon^2g_2(z)+\epsilon^3g_3(z)+O(\epsilon^4),
\]
\[
 g_2=9+9x(z^8-1)+9y(z^7-1),\qquad
 g_3=-9\tau(z^8-1)+\frac i2p_3(z^6-1).
\]
Every coefficient remainder is uniform on the compact sphere \(K\), for fixed \(\tau\). Choose disjoint disks about the nine simple \(\omega_k\). Uniform coefficient convergence and Rouché's theorem place exactly one original root in each disk for sufficiently small \(\epsilon\), uniformly in \(h\). The derivative there stays uniformly away from zero. Taylor's theorem then gives
\[
 r_k=\omega_k-
 \frac{\epsilon^2g_2(\omega_k)+\epsilon^3g_3(\omega_k)}{9\omega_k^8}
 +O(\epsilon^4),
\]
and thus
\[
 |r_k|^2=1+2G_2(\theta_k)\epsilon^2+2G_3(\theta_k)\epsilon^3
 +O(\epsilon^4),
\]
\[
 G_2=-1+x(1-\cos\theta)+y(1-\cos2\theta),\qquad
 G_3=-\tau(1-\cos\theta)+\frac{p_3\sin6\theta}{18}.
\]
The checker verifies the complete nine-root table. The marked root is exactly \(r_0=a\). For \(k=1,2,7,8\), \(G_2<0\). For \(k=3,4,5,6\), \(G_2=0\), with
\[
 G_3(\theta_3)=G_3(\theta_6)=-\frac32\tau,\qquad
 G_3(\theta_4),G_3(\theta_5)=-(1+c)\tau\mp\frac{\sqrt3}{36}p_3.
\]
For the target's \(\tau=1\), the elementary bound \(H<3\), \(|p_3|\leq H^{3/2}<3\sqrt3\), makes both outer active coefficients less than \(-(1+c)+1/4<-5/4\). All remaining coefficients have a uniform strictly inward margin. Compactness makes the \(O(\epsilon^4)\) root remainders uniform, so a single positive \(\epsilon_0\) works for **every** \(h\in K\), including colliding critical points. Those collisions do not collide the original roots near \(\omega_k\).

Finally the scalar inverse-distance expansion gives, uniformly on \(K\),
\[
 F_{p_{\epsilon,h,\tau}}(a)=8+C\epsilon^2+8\tau\epsilon^3+O(\epsilon^4).
\]
The target's family supplies a polynomial for every sufficiently near-boundary radius \(r=1-\epsilon^2\), so it gives the upper limit of the radius-wise infimum. The inherited universal lower slopes give its lower limit. It also realizes every normalized leading critical multiset \(ih\); combined with the converse, this proves the complete leading-profile classification.

## Strengthening and improvement opportunities

**Proved refinement: sharp infimum of the common cubic correction in this fixed ansatz.** Put
\[
 \tau_*:=\frac7{18(1+c)^{5/2}}\approx0.0742152664319292.
\]
For every fixed \(\tau>\tau_*\), one uniform positive \(\epsilon_0\) realizes every \(h\in K\) with all nine original roots strictly inside the disk. For every \(\tau<\tau_*\), an explicit fixed profile has an original root outside the disk for all sufficiently small positive \(\epsilon\). The endpoint \(\tau=\tau_*\) is not settled here.

The required sharp moment inequality is classical finite-sample skewness, rather than new mathematics:
\[
 \left|\sum h_j^3\right|\leq\frac3{\sqrt{14}}H^{3/2}.
\]
For completeness, a fresh short proof covers the whole sphere. At an extremum of \(\sum h_j^3\), the gradients of the sum and squared-norm constraints are independent, and Lagrange multipliers imply \(3h_j^2=\alpha+\beta h_j\). There are at most two distinct coordinate values; one value is incompatible with \(H>0\) and zero sum. If \(k\) entries equal \(b_1\) and \(8-k\) equal \(b_2\), then
\[
 b_2=-\frac{k}{8-k}b_1,\qquad
 b_1^2=\frac{H(8-k)}{8k},\qquad
 \frac{p_3^2}{H^3}=\frac{(8-2k)^2}{8k(8-k)}.
\]
For \(k=1,\ldots,7\), the maximum is \(9/14\), attained only at \(k=1,7\). Equality profiles are permutations of \(\pm(7t,-t,-t,-t,-t,-t,-t,-t)\), \(t=\sqrt{H/56}\). This is the \(n=8\) case of the classical result attributed to Wilkins (1944), reproduced with proof in [Lawford, Lemma 2](https://arxiv.org/html/2609.29976). The original reference is J. E. Wilkins, “A Note on Skewness and Kurtosis,” Annals of Mathematical Statistics 15(3), 333–335, [DOI 10.1214/aoms/1177731243](https://doi.org/10.1214/aoms/1177731243); the original full text was not independently retrieved in this pass.

The largest outer active cubic coefficient is consequently
\[
 -(1+c)\tau+\frac{\sqrt3}{36}\frac{3H^{3/2}}{\sqrt{14}}
 =-(1+c)(\tau-\tau_*).
\]
Together with \(-3\tau/2\) at the cube-root pair, this proves sufficiency for \(\tau>\tau_*\) using the uniform-root argument above. For necessity below the threshold, take the positive equality profile and \(k=5\), where \(\sin6\theta_5=\sqrt3/2\). Its zero quadratic coefficient and strictly positive cubic coefficient make \(|r_5|>1\) for all sufficiently small positive \(\epsilon\). The sharp infimum is only for a **common real translation correction in this construction**. It is not an optimal third-order coefficient for all disk-root polynomials or a result at the threshold endpoint.

In particular choose the rational \(\tau=3/40\). Then every profile is realized with
\[
 F_p(a)=8+C\epsilon^2+\frac35\epsilon^3+O(\epsilon^4),
\]
in place of the target's cubic coefficient 8. The strict inequality \(3/40>\tau_*\) has an elementary rational certificate: \(8c^3-6c-1=0\), the polynomial is increasing on \((15/16,1)\), and its value at \(15/16\) is \(-17/512\), so \(1+c>31/16\). Now
\[
 2916\,31^5-78400\,16^5=1274245916>0
\]
implies \((3/40)^2>49/[324(1+c)^5]=\tau_*^2\). No floating-point sign decision enters the refinement.

**Unproved opportunity:** At \(\tau=\tau_*\), the equality profile makes one active cubic coefficient vanish. An exact fourth-order radial expansion for that profile, followed by uniform control of profiles approaching it, is needed to decide endpoint containment. This review provides neither that expansion nor a solution of the broader higher-order boundary minimization problem. Critical-profile-dependent translations or deformations beyond this ansatz require new containment proofs.

## Independent evidence, reproduction, and trust boundary

[audit.py](audit.py) is an independent standard-library implementation and imports no target code. Its exact field is \(\mathbb Q[w]/(w^6+w^3+1)\), \(w=e^{2\pi i/9}\), rather than the target's cubic-field implementation. It checks conjugation, all nine radial constraints, dual identities, the converse determinant and all nine root motions. Real signs use rational isolation of \(c\in(15/16,1)\). A separate sparse polynomial calculation expands all eight generic factors with seven free balanced coordinates, integrates and anchors the polynomial, and checks the scalar inverse-distance defining identity. Three deliberately damaged symbolic identities must reject. The entire cubic stationary list and the smaller correction are exact rational checks. Every required condition uses an explicit exception, so optimized Python retains the checks.

Run from the repository root:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B round-two/six-reviewer-3/sendov-boundary-audit/audit.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O round-two/six-reviewer-3/sendov-boundary-audit/audit.py
```

Both runs must match [expected.json](expected.json) and print `PASS: nine exact radial constraints, converse dual identities, generic polynomial jets, sharp cubic moment and smaller correction`. On CPython 3.11.2 they passed in about 0.6 and 1.0 seconds, respectively, with child peak RSS below 22 MiB, one ordinary process/thread, and no solver. The generic derivative and anchored jets have 108 and 217 terms; their deterministic hashes are in the fixture. The target's unchanged checker was also replayed separately in normal and optimized modes: 45 exact checks and six rejected mutations, with complete record SHA256 `3b1f2fe109fced85b521b04e952ef3e233811ed9ba70befe8ebe117ea2c18e26`. Replay supplements the independent proof; it does not establish independence by itself. [provenance.json](provenance.json) records target hashes and compact run receipts; [SHA256SUMS](SHA256SUMS) covers this source packet.

The finite algebra is independently reproduced exactly. Concentration, coefficient-bootstrap hypotheses, the uniform Taylor/Rouché passage, compactness, the Lagrange-multiplier completeness argument, and the sequential converse remain ordinary written mathematics outside a formal kernel. There is no claim of formal verification, effective annulus computation, root sampling as proof, or mathematical nonexistence inferred from timeout or incomplete search. No additional resources are needed to reproduce the compact checks.

## Literature status and publication readiness

The current [Zhang first-power conjecture, Conjecture 1.2](https://arxiv.org/html/2609.19126), and [Tao's primary exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/) distinguish the active first-power endpoint from the known ordinary/quadratic results. This is local boundary progress for degree nine. A bounded candidate-specific search using the sharp coefficient, boundary phrase and cubic correction found no matching published refinement; that is not a historical-priority proof. The skewness bound is explicitly classical. The new contribution here is its exact application to the all-profile uniform correction threshold, together with an independent consequential audit.

The target and this review are ready as reproducible ordinary mathematical artifacts with their inherited premises clearly attributed. A formal publication should retain the compact ordinary uniformity/converse proof and cite the original lower-bound argument rather than presenting that bound or the moment inequality as new. No repair to lemma 8530 is required by this audit. The stronger global first-power problem, artifact `bafkreidtwmt33ck33g7dsuejzpj565twbdoz4wjhuzhser2hzizzi64qqm`, remains open.
