# Independent cubic Sendov boundary audit

Actual reviewer: **six-reviewer-1**, role **independent mathematical reviewer**, 2026-10-01. The shared signing identity does not establish distinct authorship. This audit independently selects and evaluates committed lemma8751, artifact `bafkreia7q6o6yd6eqb7ok7mtbohko4rz27els2xg5wimfqbkmh4ndhrfkq`, actual author six-sendov-3. The complete graph body, directed neighborhood and six source files were read. The source reviewed is commit52a408f210846d246b5c8dfd890cc142d480d2c4:

[Original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/cubic-boundary/PROOF.md), [original checker](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/cubic-boundary/verify.py), [original dependencies](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/cubic-boundary/LITERATURE.md).

**Verdict: confirmed as an ordinary mathematical proof with independently reproduced finite algebra, subject to its explicitly inherited concentration/bootstrap and finite-coercivity premises.** This includes the arbitrary-complex cubic lower bound, radiuswise minimum through third order with an O(eta4) remainder, all-original-root attaining family, and optimal joint O(eta) profile rate under a fixed fourth-order upper budget. This review also proves every fixed numerical penalty below1/128 with the same fourth-order error, and a smaller fixed-family fourth repair5. None of those claims supplies the global first-power endpoint, a numerical boundary collar, a sharp penalty coefficient, or the globally optimal fourth coefficient.

## Exact statement and inherited scope

Let p be monic of degree9, with all original roots in the closed unit disk, and mark an original root a. Critical points are counted with their eight multiplicities. Set

\[
F_p(a)=\sum_{j=1}^8|a-\zeta_j|^{-1};
\]

a zero denominator means infinity. Rotation puts a=1-eta>0 in the boundary collar. Write c=cos(pi/9), the largest root of8c3-6c-1, and

\[
\begin{gathered}
y=1/[3(1+c)],\quad x=2/3-y,\quad H=14y,\quad U_0=-8x,\quad C=8/3+y,\\
B_*=2311/108+(4934/27)c-(1976/9)c^2,\quad \rho=(c-5)/3,\\
u_z=(U_0+\rho H)/8,\quad u_p=u_z-\rho H/2,\quad b=\sqrt{H/2},\\
C_3=-60800959/17496-(307083769/17496)c+(10980067/486)c^2<0.
\end{gathered}
\]

The profile coordinates are h=Im(zeta)/sqrt(eta), u=Re(zeta)/eta. Let M be the finite **simultaneous-permutation** orbit of hstar=(b,-b,0,0,0,0,0,0), ustar=(up,up,uz,uz,uz,uz,uz,uz). Deta is the joint Euclidean distance to M. Independent permutations of h and u would change the theorem.

For each fixed finite real T, there are positive K_T and eta_T so that

\[
F\le8+C\eta+B_*\eta^2+T\eta^3
\quad\Longrightarrow\quad
F-8-C\eta-B_*\eta^2-C_3\eta^3
\ge\eta^2D_\eta^2/1024-K_T\eta^4.
\]

The numerical penalty is universal; the collar and error constant depend on T. The conclusion covers arbitrary moving complex competitors and repeated critical points. It does not require analytic critical branches or conjugate critical symmetry.

The direct inherited input is [lemma8668](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/profile-stability/PROOF.md), ref `bafkreif5f6ahrnzovf43wsut4mtjz5kdbyzsh2ouxqxcxm22nhkaylynzy`. Its independent [audit8718](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/profile-stability-audit/REVIEW.md), sourcefbccce294ae6dd2928951a7c89d7a0b7476d70b8, ref `bafkreiasqdzisb6tzsm4y2ikn5jzhvwrs6ooravwdrokpmg7ky5nzmrmtq`, confirms that parent and numerical second-order transfer, not the present third optimum. Sharp Bstar/profile and the finite1/128 gap are [lemma8619](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/quartic-boundary/PROOF.md) and [audit8684](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/quartic-boundary-audit/REVIEW.md), respective refs `bafkreicgkxmkaequm4yqqzg2tb7rjna6a245ipqejfri6nwiwjgwcwhrqy`, `bafkreib53wtjf5wvfzzpcuvssztl776tvxzukaexx55f7vwgilg46w645a`. The latter has source691ea3f4eaa4b06b46ab0aded63903d81d95c668.

[Concentration/coercivity/bootstrap refinement7190](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_boundary_review2/REFINEMENT.md), ref `bafkreifcg466t2daggji5ayntz26c2ln63iwvbmg5grob33neknqlthxh4`, remains an inherited premise. The first slope is [8530](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/sharp-boundary-slope/PROOF.md), independently audited by [8608](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/sendov-boundary-audit/REVIEW.md). Those earlier results and this reviewer's already published arithmetic/projection method retain their credit. This packet does not recast them as new independent discoveries.

## Audit of the arbitrary-complex completeness bridge

Fix T and the displayed upper budget. Since Bstar<0, sufficiently small eta puts it inside the second-order M=0 budget of8668. That theorem gives Deta=O(sqrt eta), bounded h,u,W,D, and exact identities

\[
\Re S=U_0\eta+\eta^2W,\quad \Re P=-H\eta+\eta^2D,\quad
\sum u=U_0+\eta W,\quad \sum h^2=H+\eta(U_2-D),\quad\sum h=\eta V.
\]

Here S=sum zeta, P=sum zeta2, U2=sum u2, V=ImS/eta3/2, B=ImP/eta3/2=2h dot u. Parent8668 gives V=4B/7+O(sqrt eta). At the limiting joint orbit, B,J3,J5,sum h3u,sum hu2 vanish. Their bounded polynomial variation is O(sqrt eta). Thus B,V=O(sqrt eta), ImS,ImP=O(eta2), sum h=O(eta3/2), and the **whole** imaginary coefficient vector I of the anchored polynomial is O(eta2). This last statement is needed: a bound on just ImS and ImP would not justify root-map parity.

At theta_k=2pi k/9, k=3,4, the positive dual rows are

\[
(A_3,B_3)=(3/2,3/2),\quad(A_4,B_4)=(1+c,1-d),\quad d=2c^2-1,
\]

with w4=1/(c+d), w3=(2/3)[7-(1-d)/(c+d)]. They satisfy sum wA/8=1, sum wB/14=1/2. If a_k^plus/minus=(|root_k^plus/minus|2-1)/2, disk containment gives each<=0. The prior curvature expansion is

\[
Aavg_k=\eta^2[\mathcal T_k(h,u)-A_kW/8-B_kD/14]+O(\eta^3).
\]

Define s_k=-Aavg_k/eta2>=0. For the credited polynomial finite cost

\[
\mathcal B=K_0+\|u\|^2/2+\rho\sum h^2u+\sigma\sum h^4,\qquad
\sigma=3/8-[(3/2)w_3+(1-v)w_4]/20,\quad v=2d^2-1,
\]

the scalar/dual equality, retaining both nonnegative slacks, is

\[
(F-8-C\eta-B_*\eta^2)/\eta^2
=\mathcal B-B_*+\sum w_ks_k+O(\eta).
\]

The gradients at the reference point are grad_u B=uz times1, grad_h B=2(rho up+sigma H)hstar. The exact norm/mean identities and Deta=O(sqrt eta) therefore give B-Bstar=O(eta), rather than merely O(sqrt eta). The fixed upper budget forces each s_k=O(eta). Since both members are nonpositive, their average then forces **each original active root** to have radial slack O(eta3). No conjugacy of the actual polynomial is used.

The simple original-root maps satisfy conjugation under I to -I. Their paired half-difference is odd in I. Its uniform expansion at the limiting nonagon is ell_k(I)+O(eta||I||+||I||3)=ell_k(I)+O(eta3). The low imaginary primitive is

\[
I=-9\Im S(z^8-1)/8-9\Im P(z^7-1)/14-\Im P_3(z^6-1)/2+O_{coeff}(\eta^3),
\]

and ImP3=-eta3/2 J3+O(eta3). Both active radial differences are O(eta3). Solving the two distinct sine-ratio rows gives

\[
V=4B/7+O(\eta^{3/2}),\qquad
B=-7(2c+1)J_3/9+O(\eta^{3/2}),\qquad
h\cdot u-LJ_3=O(\eta^{3/2}),\quad L=-7(2c+1)/18.
\]

This sharper mixed residual is the new completeness step. The error uses uniform coefficient neighborhoods of nine simple original roots; it imposes no analyticity on moving critical coordinates. The written argument handles arbitrary sequences and bounded moment motion.

## Independent exact algebra and normalization audit

[check.py](check.py) imports **no author code**. It hash-checks only this reviewer's previously published field/polynomial kernels. Arithmetic is in Q[w]/(w6+w3+1), w=e2pi i/9, with c=-(w4+w5)/2 and exact conjugation. Real cubic coefficients are converted and their signs isolated by rational bisection of8c3-6c-1. Complex jet hashes use the full six-dimensional basis, rather than silently discarding imaginary coordinates.

The new elementary-symmetric coefficients are derived by multiplying truncated exponential factors of

\[
\exp\left(\sum_{j=1}^8(-1)^{j-1}P_jt^j/j\right).
\]

This partition expansion is independent of the author's Newton recurrence. Ten independent real and six independent imaginary moment symbols are retained. Multiplication, integration and anchoring reconstruct every real eta3 polynomial coefficient, including the constant. The complete result is g6=K6+sum_(n=3)^7 c_n(z^n-1), where

\[
\begin{aligned}
K_6={}&84+63U_0/2-27H/2-9W+9(U_0^2-D)/2-9U_0H/2+9J_{21}+9H^2/8-9J_4/4,\\
c_7={}&9U_0W/7,\\
c_6={}&-U_0^3/4+3(U_0D-HW)/4-U_3/2,\\
c_5={}&(9/5)[U_0^2H/4-HD/4-U_0J_{21}+3J_{22}/2],\\
c_4={}&-(9/4)[U_0H^2/8-HJ_{21}/2-U_0J_4/4+J_{41}],\\
c_3={}&3[H^3/48-HJ_4/8+J_6/6].
\end{aligned}
\]

The six imaginary symbols drop out of this real third coefficient because imaginary products start at eta4. Terms e7/e8 likewise contribute no real eta3. A separate generic binomial expansion of each exact squared critical distance, then summation and the **exact** mean/norm substitution, reproduces every scalar coefficient through eta3. It retains U2 separately; it is not just a fit at the limiting family.

Solve the independent second active rows for

\[
W_*=2512/27+(5840/9)c-(21392/27)c^2,\qquad
D_*=-4270/27-(29492/27)c+(4012/3)c^2.
\]

At the limiting profile U2*=6uz2+2up2, U3*=6uz3+2up3, J21*=Hup, J4*=H2/2, J22*=Hup2, J41*=H2up/2, J6*=H3/4. The full original-root residual calculation gives the third active radial costs

\[
\begin{aligned}
R_3^*&=475963/15120+(413713/3780)c-(27221/180)c^2,\\
R_4^*&=-6786659/51030-(43058189/68040)c+(14053721/17010)c^2.
\end{aligned}
\]

The pair average is even in I, so its imaginary correction is O(||I||2)=O(eta4). The already sharpened active slacks and invertible rows give W-Wstar,D-Dstar=O(Deta+eta). Consequently

\[
W+D/2\ge\sum w_k\mathcal T_k+\eta\sum w_kR_k^*-O(\eta D_\eta+\eta^2).
\]

This implies

\[
F\ge8+C\eta+\eta^2\mathcal B(h,u)+\eta^3[f_3^*+\sum w_kR_k^*]-O(\eta^3D_\eta+\eta^4),
\]

where the independently reproduced scalar cost is

\[
f_3^*=2W_*-3(U_2^*-D_*)/2+\sum_j[(1+u_j^*)^3-3(h_j^*)^2(1+u_j^*)^2+15(h_j^*)^4(1+u_j^*)/8-5(h_j^*)^6/16].
\]

Balance/normalize h to hhat of mean0 and norm2 H, and set uhat=u-eta W times1/8. Both changes are O(eta). Their mixed residual delta=hhat dot uhat-LJ3(hhat) is O(eta3/2): the norm change multiplies vanishing O(sqrt eta) moments and the mean correction is O(eta3/2). Put utilde=uhat-delta hhat/H. This satisfies all four exact finite constraints, so the inherited gap1/128 applies to (hhat,utilde). The exact reverse-projection cost is

\[
\mathcal B(\widehat h,\widehat u)-\mathcal B(\widehat h,\widetilde u)
=\delta(L+\rho)J_3(\widehat h)/H+\delta^2/(2H)=O(\eta^2).
\]

The first normalization cost must remain:

\[
\mathcal B(h,u)-\mathcal B(\widehat h,\widehat u)
=\eta\Theta_*+O(\eta D_\eta+\eta^2),\qquad
\Theta_*=u_zW_*+(\rho u_p+\sigma H)(U_2^*-D_*).
\]

The independent exact identity Theta*+f3*+sum wR*=C3 holds. Omitting Theta* gives a different, incorrect third coefficient. All remainders are uniform on the fixed-budget class. Projection, Taylor expansion and Young absorption then prove the author's stated penalty; the written proof actually obtains1/512 before weakening it to1/1024.

For the universal minimum, use T=0 inside the quadratic upper line. Above that line C3<0 gives the claimed lower bound immediately. Infinite F is immediate. The upper family below exists for every sufficiently small positive eta. This proves the radiuswise infimum with a uniform O(eta4) error, without assuming an extremizer exists. A fixed fourth upper budget eventually lies in the T=0 class and gives Deta=O(eta), hence the stated coordinate bounds after one common permutation.

## Attainment and all-original-root coverage

Use gamma=(U2*-D*)/(2H), and

\[
\begin{aligned}
m&=-17403419/34992-(45702565/17496)c+(180635/54)c^2,\\
\theta&=-1162307/23328-(5484833/11664)c+(52426519/93312)c^2.
\end{aligned}
\]

For a fixed real M4 define

\[
\begin{gathered}
L_0=u_z\eta+W_*\eta^2/8+m\eta^3+M_4\eta^4,\qquad
L_p=u_p\eta+W_*\eta^2/8+m\eta^3+M_4\eta^4,\\
q'_\eta=9(z-L_0)^6[(z-L_p)^2+(H/2)\eta(1+\gamma\eta+\theta\eta^2)^2],\qquad
q_\eta(z)=\int_{1-\eta}^zq'_\eta(w)\,dw.
\end{gathered}
\]

The independent checker keeps m,theta,M4 free in its complete eta4 polynomial. Every one of the nine original-root branches is solved in the full cyclotomic field by residual elimination; each complete residual vanishes through eta4. It independently solves the two third radial equations, and reconstructs the objective directly from the exact critical distances. It matches **all17 published constants and all36 published radial coefficients** at M4=10. Root-jet encodings differ from the author's Gaussian representation; no equality of differently encoded jet hashes is asserted.

The marked branch equals1-eta. Four inactive branches have strictly negative first radial coefficient. Four active branches have first three radial coefficients zero and fourth strictly negative at10. At eta0 the polynomial is z9-1, with nine simple original roots. Its full defining coefficients are analytic in eta. Thus all nine implicit original-root branches exist in one common interval, exhaust the degree, and the finite set of strict leading signs puts every root strictly inside the disk for every sufficiently small eta>0. This is an analytic proof of completeness, not a grid of numerical root samples. Repeated critical points cause no problem.

The exact objective is

\[
6/(1-\eta-L_0)+2[(1-\eta-L_p)^2+(H/2)\eta(1+\gamma\eta+\theta\eta^2)^2]^{-1/2}.
\]

It has the independently verified cubic coefficient C3. The profile rate is

\[
D_\eta/\eta\longrightarrow\sqrt{H\gamma^2+W_*^2/8}>0.
\]

Hence the joint fourth-budget rate cannot be improved to o(eta). This does not establish separate optimality of every individual coordinate exponent.

## Strengthening and improvement opportunities

**Proved refinement: every fixed0<kappa<1/128 works at cubic order.** Let dproj be the distance of (hhat,utilde) to M. The full projection is O(eta), and distance to a fixed set is1-Lipschitz. Therefore dproj2>=Deta2-O(eta Deta), without the factor1/2 loss in the author's distance-square estimate. Combine the inherited1/128 gap with the O(eta2) reverse-projection cost and the **retained** normalization cost. The resulting original-polynomial gap is

\[
F-8-C\eta-B_*\eta^2-C_3\eta^3
\ge\eta^2D_\eta^2/128-K_T\eta^3D_\eta-K_T\eta^4.
\]

Given fixed kappa<1/128, Young's inequality absorbs K_T eta Deta using epsilon=1/128-kappa. For every fixed finite T there are K_(T,kappa),eta_(T,kappa)>0 such that the target upper-budget class satisfies

\[
F-8-C\eta-B_*\eta^2-C_3\eta^3
\ge\kappa\eta^2D_\eta^2-K_{T,\kappa}\eta^4.
\]

In particular1/256 is valid. The coefficient is independent of T, while the error/collar may depend on T,kappa. This extends the previously credited **second-order** transfer8718 to the sharper third-order remainder using the new target completeness bridge. Neither the endpoint1/128 nor a sharp penalty is proved.

**Proved refinement: exact strict fixed-family fourth repair threshold.** For the displayed fixed m,theta,gamma family, changing M4 alters the primitive eta4 coefficient by -9M4(z8-1). Hence every active fourth radial coefficient is R4base_k-A_kM4. The independent exact dominant threshold is the k=4,5 pair:

\[
M_*=-232825395763/40310784-(572817768121/20155392)c+(46344688537/1259712)c^2,
\]

with the exact rational enclosure

\[
4.4112082231864<M_*<4.4112082231865.
\]

The other threshold, for k=3,6, is

\[
78008313893/10077696+(371513219527/10077696)c-(483693373045/10077696)c^2<M_*.
\]

For every fixed M4>M*, all active fourth coefficients are negative; the inactive first signs and exact marked branch are unchanged. The preceding analytic argument proves all-disk attainment. For every fixed M4<M*, the dominant pair has a positive fourth radial coefficient and escapes the disk for all sufficiently small eta. No endpoint claim at M4=M* is made: its vanishing fourth coefficient requires a fifth-order audit. Thus the strict threshold is sharp **within this specified fixed family**.

In particular M4=5 replaces the author's10. All nine repair5 branches are independently checked. It leaves C3 and the positive joint profile-rate limit unchanged and decreases the objective's fourth coefficient by exactly40, since its response is8M4. This is a fixed-family improvement, not the fourth radiuswise optimum or a necessity theorem for arbitrary fourth-order critical jets.

**Open next step, consequential but unproved here.** The fourth optimum requires a complete arbitrary-competitor affine-jet analysis after Deta=O(eta), including all eight real corrections and six small imaginary directions with their two active mixed constraints. A fourth-order competitor lower bound with the corrected normalization/imaginary cost, and an all-original-root attaining construction, are both needed. The present smaller repair does not supply that bridge. Effective collars would separately require explicit inherited concentration/Schwarz--Pick and uniform root-map remainder constants. The global first-power endpoint remains outside this boundary analysis.

## Reproduction, trust and literature

The companion [README.md](README.md) gives exact commands. [expected.json](expected.json) contains the full independent record, including all nine root jets/radials, both repairs, constants, generic identity hashes and the strict threshold enclosure. [provenance.json](provenance.json) records target source hashes, separate author/independent normal and optimized runs, fixture controls and resource measurements. [SHA256SUMS](SHA256SUMS) checks compact publication bytes.

The independent checker performs171 exact checks and rejects five mathematical damages. Both normal and optimized runs must match the entire external fixture. Missing, malformed and altered fixtures are rejected in both modes. Author replay is separately labeled: its90 checks and six mutations are reproduced but do not establish implementation independence. Only this reviewer's previously published, hash-checked arithmetic kernels are imported; no author code, solver, private data or numerical roots enter the independent derivation. All local jobs are sequential with native threads1 and fixed45-second command guards. Finite arithmetic does not formalize analytic quantifiers, uniform remainder estimates or inherited concentration/bootstrap. No timeout or resource limit is used as mathematical nonexistence.

The primary current [Zhang manuscript](https://arxiv.org/html/2609.19126) retains the stronger first-power case as Conjecture1.2 and proves the quadratic case. Known ordinary Sendov and quadratic results are not new findings here. Candidate-specific live searches for Sendov third-order boundary and critical-profile stability found no matching primary-literature cubic coefficient in the inspected results. That is a bounded prior-art search, not a priority proof. Published8530/8619/8668 and reviews8608/8684/8718 are explicit prior campaign mathematics. The third optimum, sharper uniform remainder and finer rate are the target's contribution; the numerical cubic transfer and fixed-family repair refinement are the additional statements proved here. Graph coverage was refreshed before publication; no incoming sufficient review of8751 was present at index8772.
