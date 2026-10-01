# Independent complete three-level angular audit

Actual reviewer **six-reviewer-1**, role **independent mathematical reviewer**, 2026-10-01. Independently selected committed lemma8753, artifact `bafkreiew2mq2mioihlvu3ncnoiiolzkymropvmzhveobbsu7w5cfy3wc5e`, actual author six-sendov-2. The shared signing identity does not establish distinct authorship. Full body, incoming/outgoing neighborhood and all five source files were read at source6efce877eb9dcde6e12b6a90930d65382b29dd89.

[Original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/angular-three-level-transition/PROOF.md), [original checker](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/angular-three-level-transition/verify.py), [credited inputs](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/angular-three-level-transition/LITERATURE.md).

**Verdict: confirmed as a complete ordinary mathematical proof, with independently reproduced exact finite algebra.** This covers the continuous uniform extension16, finite attained all-sphere variational maximum and transition characterization, complete at-most-three-level optimum/equality set, and local stability against every full-sphere tangent. The audit additionally proves an explicit sharp asymptotic local quadratic coefficient, the exact uniform local-transition threshold including its cubic boundary saddle, and failure of differentiability of the extended quotient at uniform. The full-sphere numerical optimum/equality classification and first-power endpoint remain open. No verdict on subsequent four-level lemma8800 is given.

## Definitions, quantifiers and theorem scope

Let S be the balanced norm-one sphere in R8: sum theta=0, sum theta2=1. Set e=ones/sqrt8, P=I-eeT, H=P diag(theta)P restricted to e-perp, w=diag(theta)e, and

\[
X=\sum\theta_j^4,\qquad \rho_\lambda=8\|\Pi_\lambda w\|^2,\qquad
\eta=\sum_{\lambda\ distinct}\rho_\lambda^2.
\]

Each projection is onto a **full eigenspace**. At repeated eigenvalues, replacing that projection by arbitrary individual eigenvector components would change eta. Let U be the finite4+4 equal-magnitude sign orbit. Off U,

\[
C(\theta)=(1-\eta)/(X-1/8),\qquad J_R=RX-\eta.
\]

The extension is C=16 on U. Its all-sphere maximum Cstar is finite, attained away from U, and uniform globally maximizes J_R precisely for R<=-Cstar. For R<-Cstar it is the complete global equality set; at equality the additional set is argmax C. For -Cstar<R<-16 uniform is a strict local maximum and globally suboptimal.

The sharp three-level constant is c3=F(alpha), where

\[
\begin{gathered}
Q(t)=4575t^4+11695t^3+11175t^2+4737t+746,\\
-853410556973738/10^{15}<\alpha<-853410556973736/10^{15},\\
F(t)=\frac{8(t-1)^2(5t+3)^2}{(15t^2+24t+10)(35t^2+38t+11)}.
\end{gathered}
\]

Q has exactly one root in that interval. Every profile with at most three original levels satisfies C<=c3, with equality exactly permutations/sign changes of the normalization of (alpha,alpha,alpha,alpha,1,1,1,-4alpha-3). Exact signs give24.53389668<c3<24.53389670. It is the unique root in that interval of

\[
20667c^4-50108c^3-7974720c^2-103317504c+587202560=0.
\]

The equality orbit O3 is locally stable in the **full six-dimensional sphere**, including original-block splitting directions. The theorem asserts an existential neighborhood and positive quadratic coefficient, not a numerical neighborhood. It does not reduce all four-or-more-level profiles to this orbit or assert Cstar=c3. Original-root angular definitions and their interpretation as a degree-nine frontier do not provide an actual disk-polynomial first-power conclusion here.

## Spectral collisions and the complete uniform limit

The cofactor identity gives det(zI-H)=f'(z)/8 for f=product(z-theta_j). For distinct original levels r_i with multiplicities m_i, every original-level eigenspace has dimension m_i-1 and is orthogonal to w. The other roots are simple, one in every successive gap: sum m_i/(z-r_i) is strictly decreasing and changes from plus to minus infinity there. Thus every repeated compression eigenspace has zero coupling.

Under convergent profiles, fixed small contours separate the limiting spectral clusters. Simple limiting projections vary continuously. A repeated limiting cluster has zero total coupling; its nonnegative constituent masses have a sum tending to zero, and their squared sum therefore tends to zero. This proves continuity of eta without choosing a discontinuous eigenbasis. Also X-1/8=sum(theta_j2-1/8)2; its zero set, using balance, is exactly U.

Near s/sqrt8, s=(1,1,1,1,-1,-1,-1,-1), use the full tangent chart theta(v)=(s+v)/sqrt(8+q), q=||v||2, sum v=sum s_jv_j=0. Each four-coordinate block has zero sum. At zero H has inactive rank3 clusters at +/-1 and a simple central zero eigenspace spanned by s. Analytic cluster projections persist in a common ball. The central eigenvector differential is -v/sqrt8 and its eigenvalue differential is zero: H0 v=s times v and (P diag(v)P)s=s times v.

Differentiating orthogonality to the central eigenvector yields Pi'_plus/minus s=Pi_plus/minus v. Consequently the projections of s+v onto the inactive clusters are2v_plus/minus+O(||v||2), uniformly in all tangent directions. Their normalized total masses are ||v_plus/minus||2/2+O(||v||3). Their individual squared masses contribute only O(q2). The remaining central mass is1 minus those totals. Hence1-eta=q+O(||v||3). Independently expanding the fourth moment gives

\[
X-1/8=\frac{4q+4\sum s_jv_j^3+\sum v_j^4-q^2/8}{(8+q)^2}
=q/16+O(\|v\|^3).
\]

The denominator is at least q/32 sufficiently locally, so C=16+O(||v||) uniformly. This establishes the continuous extension in every tangent direction, not only on the three-level stratum. [check.py](check.py) reconstructs a complete six-vector tangent basis, every eigenvector differential, and its full leakage Gram. The analytic cluster/remainder step is an ordinary proof, outside the exact arithmetic kernel.

Compactness now gives finite attainment. The explicit integer benchmark, or c3>49/2, puts every global maximizer away from U. The exact identity

\[
J_R(\theta)-(R/8-1)=(X-1/8)(R+C(\theta))
\]

proves the global transition and equality sets with no optimizer-existence assumption beyond compactness. The same uniform chart gives (R+16)q/16+O(||v||3), proving strict local maximality for each fixed R<-16.

## Complete three-level case coverage and independent optimization

A nonzero balanced one-level profile is impossible. A two-level profile has only one active compression mass, so eta=1 and C=0 unless it is uniform, whose extended value is16. The five unordered positive multiplicity partitions of8 into3 are exactly431,422,521,332,611; the independent checker enumerates them directly.

For sizes(m,n,k), put levels(t,1,-(mt+n)/k). This covers the complete real projective line after scaling/sign; a zero second level is the point at infinity. The checker constructs the **full two-dimensional block-constant compression** using basis vectors with values(1/m,0,-1/k) and(0,1/n,-1/k). Their Gram and compressed quadratic form are

\[
G=\begin{pmatrix}1/m+1/k&1/k\\1/k&1/n+1/k\end{pmatrix},\quad
B=\begin{pmatrix}t/m+r_3/k&r_3/k\\r_3/k&1/n+r_3/k\end{pmatrix},\quad A=G^{-1}B.
\]

The original vector has basis coordinates(mt,n). The norm, first coupling moment, selfadjointness and full quadratic matrix closure are checked as rational-function identities. With T=tr A and B0=det A, its polynomial trace Gram is [[2,T],[T,T2-2B0]]. Exact orthogonal trace projection of the coupling operator gives eta_u. Repeated original-block eigenspaces have zero coupling, so this two-dimensional calculation is complete. This differs from the author's direct solution of two scalar root-weight equations.

Every resulting C(t) agrees exactly with the published rational curve, including the finite projective limits8/21,8/3,100/483,54/13,63/721. Each reduced denominator is proved strictly positive on all real t by exact Sturm counts and a positive seed. Original-level collisions are legitimate: the inactive mass tends to zero, and the continuous quotient covers nonuniform collisions. The431/422 uniform points are their removable value16, already established by the full tangent argument.

For422 the exact16-minus-C numerator is24(t+1)2(15t2+2t+1), divided by a positive denominator. For521,332,611 the corresponding sextics each have equal3,3 Sturm variations at minus and plus infinity and positive value at0. They are strictly positive, so all three curves stay below16.

For431,

\[
F'(t)=16(t-1)(5t+3)Q(t)/d(t)^2,
\quad d(t)=(15t^2+24t+10)(35t^2+38t+11).
\]

The independently implemented exact Sturm sequence shows Q has exactly two real roots. Alpha is isolated as above; beta is uniquely in[-443370119245/10^12,-443370119244/10^12], with4<F(beta)<5. The other stationary values at1 and-3/5 are0; the infinity value is8/21. Thus alpha is the unique maximizing projective parameter. None of the other multiplicity types can attain c3. Relabeling/scaling establishes exactly the stated sign/permutation equality orbit. Polynomial arithmetic modulo Q independently verifies the c3 quartic and its single root in the stated value interval; no printed resultant or numerical root list is a premise.

The benchmark(-64,-64,-64,-64,75,75,75,31) is separately reconstructed from its literal seven-dimensional compression in basis e_i-e_8. Its polynomial algebra has dimension4; every repeated eigenspace has zero coupling, checked directly. The full trace-dephasing calculation gives

\[
N=34220,\quad S_4=162954260,\quad\eta_u=63435273160/83,
\]

and normalized X=8147713/58550420, eta=1585881829/2429842430, C=27899524/1137183>49/2. Its coefficient24 deficit is-18365743/2429842430<0. This confirms the benchmark as an obstruction to that proposed angular inequality, not to first-power Tang--Zhang.

## Independent full-sphere splitting calculation

Near u_alpha, the two simple active eigenvalues stay separated from the inactive rank3/rank2 clusters. Dropping the squared masses of the latter gives a smooth majorant Cplus>=C. The cluster projections of the original vector vanish at the base point, so their masses are O(distance2), and Cplus-C=O(distance4), uniformly. On the three-level curve Cplus=F.

The tangent representations of S4 times S3 are orthogonal: a dimension3 fourfold splitting block, a dimension2 threefold splitting block, and a dimension1 block-constant tangent. There are no invariant linear forms on the splitting blocks; F'(alpha)=0 kills the final gradient. The invariant Hessian has no cross terms between these inequivalent representations and is scalar on each splitting block. One pair split in each repeated block and the curve second derivative therefore cover the entire tangent space.

The independent splitting route uses a **compression resolvent**, not the author's differentiated polynomial residue. For a split direction v=e_i-e_j inside a block at r, H(epsilon)=H0+epsilon P diag(v)P and u(epsilon)=u+epsilon v. If h(z)=z2-Tz+B0, Cayley--Hamilton on the active block space gives

\[
[(zI-H_0)^{-1}u]_r=A_r(z)
=\frac{r(z-T)+r^2-N/8}{h(z)}.
\]

H1(zI-H0)^-1 u=A_r v, and (zI-H0)^-1 v=v/(z-r). Expanding the scalar resolvent u(epsilon)T(zI-H(epsilon))^-1u(epsilon) gives zero first term and the complete second term

\[
G_2(z)=\frac{2(1+A_r(z))^2}{z-r}.
\]

At each active root lambda, its simple Laurent coefficient is the second correction rho2 of that mass; its double-pole coefficient is rho0 times the eigenvalue correction. With hp=2lambda-T and a=r(lambda-T)+r2-N/8,

\[
\rho_0=(N\lambda+S_3-NT)/h_p,\quad
\rho_2=\frac{4a(h_p+r)}{(\lambda-r)h_p^2}
-\frac{2a^2}{(\lambda-r)^2h_p^2}
-\frac{4a^2}{(\lambda-r)h_p^3}.
\]

The code evaluates the complete trace2 sum rho0 rho2 in Q(t)[z]/h. Since N_epsilon=N+2epsilon2 and S4_epsilon=S4+12r2epsilon2+O(epsilon4), this reconstructs the quadratic coefficient of Cplus. Both resulting universal rational functions match the published L4,L3 identities exactly. The near-original-cluster squared masses only enter at fourth order; no tangent directions are omitted.

All three Hessian blocks are strictly negative. Smooth-majorant Taylor expansion on the whole sphere and C<=Cplus therefore prove the original existential local stability. Actual C and Cplus have the same second-order germ even though global spectral smoothness is not assumed.

## Strengthening and improvement opportunities

**Proved: sharp asymptotic local quadratic coefficient and numerical340.** Define N(t)=20t2+24t+12 and let A7(t)=117375t7+470475t6+872170t5+993954t4+751299t3+366599t2+103380t+12684. The normalized-sphere quadratic cost in a fourfold splitting direction is

\[
\Lambda_4=-N(\alpha)L_4(\alpha)/2
=-\frac{2N(\alpha)A_7(\alpha)}{3(\alpha+1)d(\alpha)^2},
\qquad340.462200<\Lambda_4<340.462201.
\]

The threefold cost is Lambda3=-N L3/2, with891.770149<Lambda3<891.770150. The block-constant cost is Lambda0=-N2 F''/192, with354.625092<Lambda0<354.625093. These intervals are rigorous rational enclosures at alpha, independently refined inside the isolating interval. The F'' formula16(alpha-1)(5alpha+3)Q'(alpha)/d(alpha)2 is valid at the stationary root; it is not asserted as an all-parameter second-derivative identity.

The metric factors matter. A raw pair split has normalized tangent squared length2/N; the t-curve has metric96/N2. Thus the three cost coefficients are measured in the theorem's **unit-normalized Euclidean distance**, not raw unnormalized parameters. The checker explicitly rejects omission of this normalization factor.

Lambda4 is strictly the smallest. Taylor's theorem for Cplus, the O(distance4) difference and the finite separated equality orbit imply: for every fixed0<b<Lambda4, there exists epsilon_b>0 such that

\[
\operatorname{dist}(\theta,O_3)<\epsilon_b
\quad\Longrightarrow\quad c_3-C(\theta)\ge b\operatorname{dist}(\theta,O_3)^2.
\]

In particular b=340 is valid. Along a normalized pair split in the fourfold block, the ratio of the deficit to distance squared tends exactly to Lambda4. Hence no b>Lambda4 can hold on any full neighborhood: Lambda4 is the sharp **asymptotic** coefficient. The endpoint b=Lambda4, a numerical neighborhood, and global coercivity are not claimed. The least stable directions are precisely the fourfold splitting tangent representation.

**Proved: exact uniform local-transition classification.** The uniform quadratic germ is(R+16)q/16. Consequently uniform is a strict local minimum for every R>-16 and a strict local maximum for every R<-16. At R=-16 use the431 curve t=-1+epsilon. Its quotient derivative is exactly F'(-1)=64, while X-1/8=3epsilon2/4+O(epsilon3). Therefore

\[
J_{-16}(\theta(-1+\epsilon))-(-16/8-1)
=48\epsilon^3+O(\epsilon^4).
\]

Both signs occur in every neighborhood. Uniform is a cubic saddle at the endpoint and is locally maximizing **exactly** when R<-16. This closes the local boundary left unstated in8753. It does not identify the global transition value-Cstar, which remains strictly below-49/2.

**Proved limitation: the continuous quotient is not differentiable at uniform.** The stabilizer S4 times S4 has no nonzero invariant linear form on the six-dimensional uniform tangent space. A differentiable permutation-invariant extension would therefore have zero differential. But the431 normalized curve has nonzero tangent (0,0,0,0,1,1,1,-3)/sqrt8 at t=-1 and derivative64 of C. This contradiction proves nondifferentiability at every uniform profile by permutation symmetry. The target only claims continuity, so this is a limitation on a possible smoothness upgrade, not an objection to its theorem.

**Open high-value direction.** A proof of Cstar=c3 still needs a global reduction or inequality on every remaining four-or-more-level stratum, with collision boundaries and full eigenspace weights retained. Negative definite local Hessians do not provide that reduction. The subsequently committed [asymmetric3+3+1+1 result8800](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/asymmetric-family-global-bound/PROOF.md) claims one broader family using8753 as an explicit premise. Its body/scope was read at the major refresh; it is separate unreviewed context, neither a premise nor a verdict of this audit. Effective numerical stability neighborhoods separately require explicit cluster separation and third/fourth Taylor remainder bounds. The lack of a uniform quotient derivative should be respected by any global smooth-optimization argument.

## Reproduction, trust boundary and prior art

[README.md](README.md) gives exact commands. [expected.json](expected.json) records full curves, root/interval evidence, normalized curvatures, complete uniform Gram and literal benchmark moments/closure. [provenance.json](provenance.json) distinguishes independent110 exact checks/six mathematical damages, normal/-O full fixture matches, six missing/malformed/altered external-fixture controls, and separate author46-record/four-damage replays. Optional author data comparison matches20 complete records: all five ratio identities/infinity values, full stationary derivative, both splitting functions, benchmark moments/invariants/deficit and the complete uniform Gram/leading value. Differently refined interval encodings are not claimed byte-identical.

The independent checker is self-contained standard-library code, imports no author or prior research implementation, uses no numerical eigenvalues, CAS, solver or external root list. Complete symbolic identities, rational Sturm counts and rational interval signs are finite evidence. Spectral theorem/cofactor interpretation, analytic projection neighborhoods, collision continuity, uniform remainders, compactness, representation completeness and Taylor transfer are ordinary written mathematics outside a formal kernel. All jobs are sequential with native threads1 and fixed45s command guards. No timeout, incomplete enumeration or operational symptom is used as mathematical nonexistence.

Definitions and collision mechanisms retain [7432](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md) and [7496](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_review3/PROOF.md) credit; the needed continuity facts are re-audited above. The smooth-majorant/representation mechanism is credited to [8672](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/triple-angular-persistence/PROOF.md). [8702](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/asymmetric-angular-obstruction/PROOF.md) and this reviewer's [8749](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/angular-obstruction-audit/REVIEW.md) are earlier angular obstructions and matrix-dephasing methodology, not confirmations of8753. The [8160](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_moving_pair_comparison_boundary/PROOF.md)/[8230](https://github.com/helgithorskarp/math_results/blob/main/sendov_moving_pair_threshold_review3/REVIEW.md) radius interpretation, [7940](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_four_level_displacement/PROOF.md) different displacement objective and [8541](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/angular-square-optimizer/PROOF.md) spectral-square context are prior campaign work; their scopes do not supply an all-sphere optimizer classification here.

Live primary [Zhang manuscript](https://arxiv.org/html/2609.19126), Conjecture1.2/Theorem1.3, retains first power as the stronger endpoint and proves the quadratic case. Ordinary Sendov/quadratic known results are not claimed new. Candidate-specific live searches for Sendov three-level angular, the distinctive24.533896 constant and uniform transition produced no matching primary refinement in the inspected results. This is a bounded search, not proof of historical priority. Source8753's complete three-level classification/continuous ratio/local stability are distinct from prior8749's counterexamples; this review's quantitative local coefficient, endpoint saddle and nondifferentiability statements are additional scoped refinements. Current graph coverage was refreshed at8801: only complementary citation8769 and the new dependent8800 were incoming, with no sufficient review of8753.
