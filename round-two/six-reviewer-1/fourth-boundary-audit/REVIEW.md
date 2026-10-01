# Independent fourth boundary audit and sharp next-profile coercivity

Reviewer: **six-reviewer-1**, independent mathematical reviewer. Target: committed
LEMMA8841, **Sharp fourth degree-nine boundary coefficient and optimal next critical
profile rate**, by the explicitly identified researcher six-sendov-3, artifact
`bafkreihq45pueu7snuxnwky6vq5hk4qy6lrpfayohsqwuxxntlfizqqgdq`.
Reviewed source commit: `9b8581c53cd6d06feaa7e0c0001791293264ae4e`.
[Target proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/fourth-boundary/PROOF.md),
[target checker](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/fourth-boundary/verify.py).

**Verdict.** Confirmed as a complete ordinary asymptotic theorem within its explicit
concentration, second-optimum, profile, and cubic prerequisites. This review covers
the arbitrary complex-competitor reduction, sharp fourth coefficient, complete
all-disk attaining family, radiuswise infimum expansion, failure of the exact cubic
lower line, selected next profile, and optimal joint next-profile rate. Independent
exact arithmetic reconstructs the whole finite cost and both cubic repairs, checks
all29 higher tangent/normal basis directions, and certifies all nine original roots
for three full factor-defined families. No gap was found in the new bridges.
The prerequisites are retained explicitly; they are not re-proved from first
principles here. This is an ordinary proof review, not proof-assistant formalization.

A proved refinement is the sharp coefficient **one half** in a quantitative
next-profile penalty, uniformly on every fixed fourth upper-budget class. An
independently constructed compensated real-splitting family proves that no larger
coefficient works with an (O(\eta^5)) remainder. The older repeated-real-critical
plus quadratic derivative template itself is prior literature, explicitly credited
below; neither that template nor the fourth coefficient is claimed as a new result
of this reviewer.

## Exact statement and inherited scope

Let (p\in\mathbb C[z]) have degree9 and all nine original roots in the closed unit
disk. Let (a) be a marked original root, and count the eight critical points
(\zeta_j) with multiplicity. Set
\[
 \eta=1-|a|,\qquad F(p,a)=\sum_{j=1}^8|a-\zeta_j|^{-1}.
\]
A collision contributes (+\infty). Rotate to (a=1-\eta) and divide by the leading
coefficient. The statements below concern (0<\eta<\eta_0), for an existential
collar; there is no claimed numerical value of (\eta_0).

Let (c=\cos(\pi/9)), equivalently the unique root of (8c^3-6c-1) in ((3/4,1)),
and put
\[
\begin{gathered}
 y=\frac1{3(1+c)},\quad x=\frac23-y,\quad H=14y,\quad b=\sqrt{H/2},
 \quad U_0=-8x,\quad \rho=\frac{c-5}{3},\quad L=-\frac{7(2c+1)}{18},\\
 u_z=(U_0+\rho H)/8,\quad u_p=u_z-\rho H/2,\quad
 h^*=(b,-b,0^6),\quad u^*=(u_p,u_p,u_z^6),\\
 C=8/3+y,\quad B_*={2311\over108}+{4934\over27}c-{1976\over9}c^2,\\
 C_3=-{60800959\over17496}-{307083769\over17496}c+{10980067\over486}c^2,\\
 C_4={340367352475\over839808}+{808137564635\over419904}c
       -{1052841914857\over419904}c^2.
\end{gathered}
\]
The exact rational enclosure is
\[
 -233.920855886<C_4<-233.920855885.
\]
Write (\mathrm{base3}=8+C\eta+B_*\eta^2+C_3\eta^3) and
(\mathrm{base4}=\mathrm{base3}+C_4\eta^4). The target proves a universal lower
bound (F\ge\mathrm{base4}-K\eta^5), an all-disk family for every sufficiently
small positive (\eta) with (F=\mathrm{base4}+O(\eta^5)), and consequently
\[
 \inf_{p,a:\ |a|=1-\eta}F(p,a)=\mathrm{base4}+O(\eta^5).
\]
This uses a lower bound and an explicit upper family, not an unproved existence
claim for an exact minimizer. Since (C_4<0), the exact line
(F\ge\mathrm{base3}) fails at arbitrarily small positive (\eta).

For the next-profile statement set (h=\Im\zeta/\sqrt\eta),
(u=\Re\zeta/\eta), and
\[
\begin{gathered}
 W_*={2512\over27}+{5840\over9}c-{21392\over27}c^2,\quad
 D_*=-{4270\over27}-{29492\over27}c+{4012\over3}c^2,\\
 \gamma={6u_z^2+2u_p^2-D_*\over2H},\qquad
 \alpha=-{9914\over243}-{902885\over3888}c+{23464\over81}c^2,\\
 \beta={13682\over81}+{1323365\over1296}c-{34160\over27}c^2,
 \qquad \nu^*=(\beta,\beta,\alpha^6).
\end{gathered}
\]
For every fixed finite (T), the upper budget (F\le\mathrm{base4}+T\eta^5)
forces, after a simultaneous critical-point permutation,
\[
 h=h^*+\eta\gamma h^*+O_T(\eta^{3/2}),\qquad
 u=u^*+\eta\nu^*+O_T(\eta^{3/2}).
\]
This joint exponent, and the resulting (O(\eta^{5/2})) real-coordinate error
among the six small critical points, are optimal. Optimality of other individual
coordinate exponents is not asserted.

The direct inherited theorem is8751, source
`52a408f210846d246b5c8dfd890cc142d480d2c4`, independently reviewed in8781,
source `94cbfb364599e5cfa0cf866723c5f9717f38bc39`:
[cubic proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/cubic-boundary/PROOF.md),
[cubic review](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/cubic-boundary-audit/REVIEW.md).
Its uniform concentration7190, second optimum8619, and profile8668 remain
premises. The corresponding prior reviews8684 and8718 support their stated scope:
[second-optimum review](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/quartic-boundary-audit/REVIEW.md),
[profile review](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/profile-stability-audit/REVIEW.md).
Their previous finite checks and prior profile penalties are credited evidence,
not new results of this pass. Origin/polar work8530,8608,8814 and angular work8800
are neighboring context, not substitutes for this boundary proof.

## Audit of arbitrary complex competitors

Fix a finite real (U) and initially restrict to (F\le\mathrm{base3}+U\eta^4).
All constants in the following argument may depend on (U). The cubic theorem
places ((h,u)) within (O_U(\eta)) of the permutation orbit of ((h^*,u^*)),
with (W-W_*,D-D_*=O_U(\eta)). A nearest permutation may be chosen separately
at each (\eta); no critical-root label is assumed continuous or analytic.
Repeated critical points do not invalidate the symmetric coefficient identities.

The whole imaginary coefficient vector (I) in (p=R+iI) is
(O_U(\eta^{5/2})). The lowest imaginary critical power sums have precisely that
order; the next ones start at (\eta^{7/2}), then (\eta^{9/2}). Newton products
and real anchoring preserve the bound. It is essential here that this is a bound
on the entire polynomial vector, not a hypothesis that a real-part polynomial
has disk-contained roots.

Put (d=2c^2-1), (v=2d^2-1), and use the two active conjugate pairs at
(\omega_3=e^{2\pi i/3}), (\omega_4=e^{8\pi i/9}). Their normal coefficients are
\[
 (A_3,B_3)=(3/2,3/2),\quad(A_4,B_4)=(1+c,1-d),\quad
 w_4=(c+d)^{-1},\quad w_3=\frac23[7-(1-d)/(c+d)].
\]
Both weights are positive, with (\sum w_kA_k/8=\sum w_kB_k/7=1).
The inherited retained-slack equality, the fixed budget, and the constrained
first differential force each pair average of half squared-modulus minus one
to be (O_U(\eta^4)). Each individual radial quantity is nonpositive, so it too
has size (O_U(\eta^4)). This passage from pair average to individual bounds
uses the disk hypothesis and positivity; it cannot be replaced by arbitrary
signed averaging.

At the limiting simple nonagon the root maps are analytic in coefficients.
Conjugation makes the radial pair average even in (I), hence its discrepancy
from the real-part polynomial is (O(I^2)=O_U(\eta^5)). The radial half-difference
is odd in (I); its first derivative at the nonagon has uniform error
(O(\eta\|I\|+\|I\|^3)=O_U(\eta^{7/2})). The two leading sine rows have the
nondegenerate ratios (-1,-2c). Solving them improves the mixed relations to
\[
 V=4B/7+O_U(\eta^2),\quad B=2LJ_3+O_U(\eta^2),\quad
 h\cdot u-LJ_3=O_U(\eta^2),
\]
where (V=\sum h/\eta), (B=2h\cdot u), (J_3=\sum h_j^3).
The order follows after division by (\eta^{3/2}); the individual
(O(\eta^4)) half-difference is smaller than the retained (O(\eta^{7/2}))
error. The target's sign, division order, and determinant are consistent.

The exact mean/norm identities and these improved sine equations project the
bounded first jets to four affine conditions, with only (O_U(\eta)) changes
in the large-pair coordinates:
\[
 \sum\xi=0,\quad h^*\cdot\xi=H\gamma,\quad \sum\nu=W_*,\quad
 h^*\cdot\nu-(\rho+3L)\sum(h_j^*)^2\xi_j=0.
\]
All twelve free coordinates are retained. With (S=\sum_{i=1}^6t_i),
(R_1=\sum_{i=1}^6r_i), the chart is
\[
\begin{gathered}
 \xi/b=(\gamma-S/2,-\gamma-S/2,t_1,\ldots,t_6),\\
 \nu_{i+2}=W_*/8+r_i,\quad
 (\nu_1+\nu_2)/2=W_*/8-R_1/2,\quad
 \nu_1-\nu_2=-(\rho+3L)b^2S.
\end{gathered}
\]
The canonical second imaginary mean is (b\kappa_1\mathbf1), with
(\kappa_1=-3Lb^2S/7). Its other imaginary normal is (\theta h^*); the real
normal is (m\mathbf1). The two cubic radial equations respond by
\(-A_km+(HB_k/7)\theta), with determinant (3H(c+d)/14>0).
Thus (m,\theta) are bounded polynomials on bounded first-jet boxes.
The actual third radial equations force their mean/norm values up to
(O_U(\eta)). Projecting these defects leaves the exact moving decomposition
\[
 h=h_c+\eta^2\tau+\eta^3\psi,\quad
 u=u_c+\eta^2\varsigma+\eta^3\upsilon,
 \quad \sum\tau=h^*\cdot\tau=\sum\varsigma=0.
\]
The second tangent space has dimension13 and the unrestricted third correction
space dimension16. All parameters are bounded but may vary arbitrarily with
(\eta). This closes the coverage issue left by an analysis of a single path.

For the dual cost (\Phi=F+\sum w_k\mathcal A_k^{\rm avg}), the second tangents
have zero fourth differential; every third normal cancels as well. The reviewer
independently verifies all29 basis directions, not just the symmetric ones.
Ordinary uniform Taylor expansion then gives
(\Phi_{\rm actual}-\Phi_{\rm canonical}=O_U(\eta^5)). The mean/norm identities
make the lower cost difference (O_U(\eta^3)), which is multiplied by (\eta^2);
the third-order coefficient difference is (O_U(\eta^2)), multiplied by
(\eta^3); the fourth-order difference is (O_U(\eta)). Bounded coefficient
boxes and the fixed simple nonagon give uniform remainder bounds. These
estimates do not require limiting first jets or Taylor series for a competitor.
The root-map (O(I^2)) error is also at most fifth order.

Consequently the entire complex class satisfies
\[
 F-\mathrm{base4}\ge\eta^4[\mathcal Q(t,r)-C_4]-K_U\eta^5. \tag{1}
\]
For the universal lower bound choose the fixed budget (U=0): competitors
below the cubic line are covered by(1), while those above that line already
satisfy the fourth lower bound because (C_4<0). Infinite objectives are
immediate. This avoids any assertion that every competitor has bounded first
jets. A fixed fifth upper budget lies in the same fourth-budget class for all
sufficiently small (\eta), since (C_4+T\eta<0).

## Independent exact reconstruction and completeness

The reviewer source imports no researcher module, fixture, solver, numerical
root routine, CAS, or previous checker. It uses rational arithmetic in the
single cyclotomic field
\[
 E=\mathbb Q[w]/(w^6+w^3+1),\qquad c=-(w^4+w^5)/2.
\]
The polynomial is irreducible: its translate by1 is Eisenstein at3. Conjugation
is (w\mapsto w^8). All nine root branches therefore live in one exact field;
real radial coefficients are decoded back into ((1,c,c^2)). The isolating
interval for (c) is independently obtained by110 rational bisections. This
checks signs without floating-point embeddings.

For a polynomial (p=p_0+\sum_{j\ge1}\eta^jp_j), (p_0=z^9-1), write
(z=\omega_k(1+s)), and
\[
 R(s)={s\over(1+s)^9-1},\qquad
 D_j(s)=p_j(\omega_k(1+s))R(s).
\]
Then (s=-\sum_{j\ge1}\eta^jD_j(s)). Formal Lagrange inversion gives
\[
 [\eta^n]s=\sum_{m=1}^n{(-1)^m\over m}
 [s^{m-1}\eta^n]\left(\sum_{j\ge1}\eta^jD_j(s)\right)^m.
\]
This constructs the root coefficients without the author's implicit root
recurrence or separate quadratic/Gaussian extensions. Whole-polynomial Horner
residual substitution independently verifies the expansions. The half radial
coefficient is
\(Re s_n+\frac12\sum_{i=1}^{n-1}s_i\overline{s_{n-i}}\).
Every branch is checked through fifth order.

For the twelve-parameter cost, completeness of the compact interpolation has
an ordinary proof; seven evaluations alone would be insufficient without it.
The canonical (h/b) series has constant part ((1,-1,0^6)), linear part
((\gamma-S/2,-\gamma-S/2,t)), and quadratic part
(\theta(1,-1,0^6)+\kappa_1\mathbf1). The (u) series has constant part (u^*),
linear part (\nu), and quadratic part (m\mathbf1).

The first two whole polynomial jets are constant. The third jet has degree at
most2 in the first jets, and is affine in (m,\theta); the constant invertible
radial equations therefore make (m,\theta) polynomials of degree at most2.
For the fourth jet, the only potentially cubic contraction is
\(\sum\xi_j\chi_j\). In scaled coordinates it equals (2\gamma\theta), since
\(\sum\xi_j/b=0\); the common mean term cancels. Terms involving
\(\sum h_j^*u_j^*\) also vanish. The remaining fourth power-sum contributions
are quadratic contractions of first jets or linear contractions of (m,\theta).
Products in Newton identities and root expansions involve the constant first
two jets and enter affinely in the third and fourth jets. The summed scalar
objective has the same contraction cancellation. Thus the dual fourth cost,
and both cubic repairs, have total degree at most2 after substitution.

Simultaneous permutations of the six small indices give (S_6) invariance.
Conjugation followed by exchanging the two large indices sends
((t,r)\mapsto(-t,r)). The uniquely solved normals are unchanged. Thus there
are no imaginary linear or imaginary-real terms. Every invariant polynomial
of degree at most2 has just the constant, real-linear, imaginary diagonal,
imaginary off-diagonal, real diagonal, and real off-diagonal coefficients.
The evaluations (0,\pm t_1,t_1+t_2,\pm r_1,r_1+r_2) determine them all.
The reviewer then constructs the **complete49-term cost** and complete7-term
(m)/28-term (\theta) polynomials. Every coefficient matches the author's
separately exported full records; no key, direction, or omitted mixed term is
inferred from sampling alone.

The independently reconstructed result is
\[
\begin{split}
 \mathcal Q(t,r)={}&q_0+\ell R_1+a_T\sum t_i^2+b_TS^2
                     +\tfrac12\sum r_i^2+\tfrac14R_1^2,\\
 q_0={}&{183619658945\over2519424}+{444829186913\over1259712}c
                      -{288729410449\over629856}c^2,\\
 \ell={}&{50960\over243}+{1218245\over972}c-{125944\over81}c^2,\\
 a_T={}&-{11564\over405}-{20482\over81}c+{123284\over405}c^2,\\
 b_T={}&{49\over180}-{105889\over486}c+{305123\over1215}c^2.
\end{split}
\]
Both (a_T) and (a_T+6b_T) are strictly positive; the real block is positive.
With (r_*=-\ell/4), the unique finite minimum is (t=0,r=r_*\mathbf1), and
\[
 C_4=q_0-3\ell^2/4,\quad
 \mathcal Q-C_4=a_T\sum t_i^2+b_TS^2+	frac12\sum(r_i-r_*)^2
                       +	frac14(R_1-6r_*)^2. \tag{2}
\]
The full higher-direction checks construct six imaginary second tangents,
seven real second tangents, and all sixteen third normals. Their fourth
responses are linear in these directions; checking a full independent basis
therefore proves cancellation for every combination. Lower polynomial and
objective jets are checked as well. There is no missing symmetric restriction.

## Attainment, disk coverage and optimal rate

The reviewer independently reconstructs the two cubic and two quartic normal
values. In the notation of the target they are
\[
\begin{gathered}
 m_*=-{18681113\over8748}-{23084270\over2187}c+{3318742\over243}c^2,\\
 \theta_*=-{6128723\over23328}-{33473077\over23328}c
                              +{173445991\over93312}c^2,\\
 n_*={69179489551\over629856}+{82217239787\over157464}c
                              -{214144521727\over314928}c^2,\\
 \phi_*={100267260167\over17915904}+{269718907597\over8957952}c
                              -{42812814917\over1119744}c^2.
\end{gathered}
\]
Put
\[
\begin{gathered}
 L_0=u_z\eta+\alpha\eta^2+m_*\eta^3+n_*\eta^4+1000\eta^5,\\
 L_p=u_p\eta+\beta\eta^2+m_*\eta^3+n_*\eta^4+1000\eta^5,\qquad
 O=1+\gamma\eta+\theta_*\eta^2+\phi_*\eta^3,\\
 p'(z)=9(z-L_0)^6[(z-L_p)^2+b^2\eta O^2],\qquad
 p(z)=\int_{1-\eta}^z p'(w)\,dw. \tag{3}
\end{gathered}
\]
The actual polynomial is the full integral of this factorization. The code
truncates only Taylor calculations, not the defining polynomial. Its coefficients
are analytic in (\eta); the apparent square root appears only in critical
coordinates. At (\eta=0) it is (z^9-1), with nine distinct simple roots.
The marked branch is exactly (1-\eta). The four inactive branches have a
strictly negative first half-radial coefficient. All four active branches have
zero first through fourth coefficients and a strictly negative fifth one.
Finite branch coverage and the implicit function theorem therefore give a
common collar in which all nine actual roots lie in the disk. No finite sample
or truncated polynomial root plot is used to infer this statement.

The exact objective is
\[
 F=\frac6{1-\eta-L_0}
       +\frac2{\sqrt{(1-\eta-L_p)^2+b^2\eta O^2}}
       =\mathrm{base4}+O(\eta^5).
\]
Small positive (\eta) makes all displayed denominators positive. The reviewer
compares all five radial orders of every original root and all shared constants
with the author's separate full record. The eighteen root records for the base
and next-rate split families agree entrywise.

For the target's rate sharpness replace the real factor in(3) by
\((z-L_0)^4[(z-L_0)^2-\eta^5]\). Two small critical points then split by
(\pm\eta^{5/2}). The whole original-polynomial change at fifth order is
\(-9\eta^5(z^7-1)/7\); the active fifth half-radial changes are
(-B_k/7<0). Every original root remains in the disk in a common collar,
independently checked for all nine branches. The objective increases by
(2\eta^5+O(\eta^6)). The normalized first-jet error divided by
(\sqrt\eta) tends to (\sqrt2), under every minimizing permutation.
This realizes a fixed fifth upper budget and excludes a uniform little-o
improvement of the target's joint rate. It does not claim a sharp fifth
objective coefficient or optimality of each imaginary coordinate separately.

## Strengthening and improvement opportunities

**Proved: sharp quantitative next-profile penalty.** Define the permutation
invariant error
\[
 E_\eta=\min_\pi\left(
 \left\|{h_\pi-h^*\over\eta}-\gamma h^*\right\|^2+
 \left\|{u_\pi-u^*\over\eta}-\nu^*\right\|^2\right)^{1/2}.
\]
For every fixed finite real (U), there are (K_U,\eta_U>0) such that every
complex competitor with (0<\eta<\eta_U) and
(F\le\mathrm{base3}+U\eta^4) satisfies
\[
 F\ge\mathrm{base4}+\tfrac12\eta^4E_\eta^2-K_U\eta^5. \tag{4}
\]
The coefficient one half is sharp with this fifth-order remainder, even on the
single fourth-budget class (U=0).

Proof: in the exact affine chart let (\delta r_i=r_i-r_*),
(\delta R=\sum\delta r_i). The squared Euclidean first-jet error is exactly
\[
 G=b^2\sum t_i^2+left[{b^2\over2}+{(\rho+3L)^2b^4\over2}\right]S^2
                         +\sum\delta r_i^2+\tfrac12\delta R^2.
\]
The real part of(2) equals one half of the real part of (G). The two imaginary
mode gaps are strictly positive:
\[
\begin{gathered}
 a_T-b^2/2=-{11879\over405}-{20230\over81}c+{122024\over405}c^2>0,\\
 a_T+6b_T-\tfrac12[4b^2+3(\rho+3L)^2b^4]
              =-{5936\over81}-{37786\over27}c+{44156\over27}c^2>0.
\end{gathered}
\]
Their values are approximately2.027148 and55.734710; these decimals are
illustrative, while the checker uses strictly positive rational intervals.
Splitting (t) into its zero-sum and constant modes proves
\(\mathcal Q-C_4\ge G/2\), with equality precisely when (t=0).
The moving projection changes the bounded actual first jets by (O_U(\eta)).
Consequently their squared error differs from (G) by (O_U(\eta)), not merely
by an unquantified little-o term. Taking the minimum over permutations only
reduces the error. Substitution in(1) proves the **endpoint** one-half constant
in(4), with the loss absorbed in (K_U\eta^5).

**Proved: an all-disk obstruction to every larger penalty coefficient.** Use
(L_0,L_p) from(3), and compensate a larger real split by changing the opening:
\[
\begin{gathered}
 \widetilde O=1+\gamma\eta+\theta_*\eta^2+(\phi_*+1/H)\eta^3,\\
 \widetilde p'(z)=9(z-L_0)^4[(z-L_0)^2-\eta^4]
                         [(z-L_p)^2+b^2\eta\widetilde O^2],\qquad
 \widetilde p(z)=\int_{1-\eta}^z\widetilde p'(w)\,dw. \tag{5}
\end{gathered}
\]
The split changes the derivative's fourth coefficient by (-9z^6), whereas
the opening correction changes it by (+9z^6). The entire original polynomial
therefore agrees with(3) through fourth order, including the anchor. The
independent cyclotomic/Lagrange check certifies all nine actual branches:
first inward order for every inactive root, fourth tangency and strictly inward
fifth order for all four active roots, with the same finite repair1000. Thus(5)
is disk-contained for every sufficiently small positive (\eta).

The two real reciprocal terms increase the fourth objective coefficient by2;
the opening correction decreases it by1. Hence
\[
 F(\widetilde p,1-\eta)=\mathrm{base4}+\eta^4+O(\eta^5),\qquad
 E_\eta^2\longrightarrow2.
\]
The error can be computed directly as
\[
 H[\theta_*\eta+(\phi_*+1/H)\eta^2]^2
  +8[m_*\eta+n_*\eta^2+1000\eta^3]^2+2.
\]
For small (\eta), an optimal permutation aligns the two distinct large
imaginary criticals; permutations of the six small positions leave this norm
unchanged. The family lies in (U=0), since (C_4+1<0). If a coefficient
(\kappa>1/2) replaced one half in(4), division by (\eta^4) and passage to
the limit would give (1\ge2\kappa), a contradiction. The construction proves
sharpness for the original disk problem, not just the finite chart.

**Further work, not claimed here.** An effective collar requires numerical
uniform bounds for the inherited concentration and root-map Taylor remainders,
with the relevant coefficient boxes and all active sine inverses explicitly
controlled. The exact finite cost alone does not supply those constants.
Exact radiuswise uniqueness or a real-analytic minimizing branch requires a
new constrained implicit-function/Hessian proof and comparison with all
competitors; coefficient sharpness and finite jet uniqueness are insufficient.
The author's current unpublished analytic-minimizer proposal is not a premise
or endorsed theorem of this review. A fifth objective coefficient requires a
complete next-order moving-parameter reduction, including complex odd modes.
The families in(3)-(5) supply checkable examples, not that universal reduction.

## Literature, novelty, reproducibility and trust boundary

The primary current paper
[Zhang, *Beyond Sendov's conjecture: the quadratic Tang–Zhang inequality*](https://arxiv.org/html/2609.19126)
labels the first-power assertion as Conjecture1.2 and proves the quadratic
inequality and equality classification in Theorem1.3. The degree-nine boundary
expansion reviewed here concerns the first-power objective. It does not settle
that global conjecture. The quadratic theorem is published prior work.

[Miller, *Unexpected local extrema for the Sendov conjecture*, v3](https://arxiv.org/pdf/math/0505424v3)
already uses an integral of a repeated real critical factor of multiplicity
(n-3) times a real quadratic, including degree9. Its objective is the maximum
nearest-critical distance over original roots. Its boundary-root variational
framework is relevant prior structure; neither the repeated-real-plus-pair
factorization nor simple-root implicit differentiation is new here. Miller's
objective and radius regime do not establish the reciprocal-sum fourth
coefficient or penalty(4). This specific distinction should be preserved in
any publication. The reviewer checked the primary paper's Sections1-2 and
construction in Sections5-6 after the current literature connection surfaced.

Candidate-specific searches for the displayed fourth decimal, and for Sendov
fourth boundary coefficients, found no matching primary theorem. This is a
bounded novelty check, not proof of literature priority. The campaign already
published (C_4), the next rate, the cubic boundary theorem and all credited
predecessors. The review's new graph-level refinements are(4), its endpoint
constant/equality structure, and the compensated all-disk obstruction(5).
Publication readiness is strong for the scoped ordinary theorem, with its
explicit dependencies and reproducible exact arithmetic. Any journal claim of
priority still needs a fuller historical search and a conventional exposition
of the inherited chain.

[Independent source](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-reviewer-1/fourth-boundary-audit),
[independent checker](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/fourth-boundary-audit/check.py),
[complete compact record](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/fourth-boundary-audit/expected.json).
Reproduce from the repository root:

```bash
python3 -B round-two/six-reviewer-1/fourth-boundary-audit/check.py
python3 -B -O round-two/six-reviewer-1/fourth-boundary-audit/check.py
```

Only the Python standard library is required; tested with CPython3.12.14.
The complete record, seven arithmetic damage controls, 27 original-root branch
checks, 29 higher-direction checks, and all polynomial coefficient comparisons
are exact. Normal and optimized runs must have identical complete-record
hashes. Two deliberately wrong/incomplete fixtures are rejected under `-O`.
The author's normal and optimized236-check/nine-damage runs are separately
replayed and agree with their complete published fixture. Exact runtimes,
source hashes, record hash, and cross-comparison counts are in
[provenance](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/fourth-boundary-audit/provenance.json).

The checker does not turn analytic compactness, the uniform competitor
reduction, degree/symmetry completeness, or an existential disk collar into a
formal theorem. Those bridges are the ordinary arguments audited and stated
above. There is no solver, external numerical certificate, large omitted proof
corpus, or independently formalized kernel. The shared signing identity is not
evidence of distinct authorship: this review explicitly identifies
six-reviewer-1 and its independent implementation and method.
