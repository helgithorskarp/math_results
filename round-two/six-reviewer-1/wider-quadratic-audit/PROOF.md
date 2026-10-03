# Independent wider boundary audit and retained-budget improvements

Actual author **six-reviewer-1**, role **independent mathematical reviewer**,
2026-10-03. This is an ordinary, unformalized mathematical proof relative to
the precisely scoped entry lemma below. Written formulas were exposed.
The new target executable and fixture had not been opened when this proof
and its independent complete arithmetic record were prepared.

## Domain, conclusions and dependency

Let p be complex monic of degree nine, with ALL nine original zeros in the
CLOSED unit disk. Rotate a marked zero to a=1−η, where EVERY
0<η≤e=1/16000 is allowed. Count ALL eight critical points ζ with algebraic
multiplicity. Put F=Σ|a−ζ|⁻¹, with zero denominator interpreted as infinity.
No cap on the initial critical energy, radius or coefficients, no
conjugation, separation, chosen profile, optimizer, attainment, smooth path
or branch matching is assumed.

We independently reconstruct the ENTIRE assertion of LEMMA9857 and prove
the following modest improvements on its SAME domain:

\[
 F>8+C\eta-238\eta^2>8+(141/50)\eta.                 \tag{A}
\]

Under F≤8+3η, define
\[
 m=M+iD=\tfrac18\sum\zeta,\quad \nu_j=\zeta_j-m,\quad
 V=\sum|\nu_j|^2,\quad T=\sum\nu_j^2,\quad t=|m|,
 \quad u=a-m,\quad r=|u|,
\]
\[
 \xi_j=\nu_j\bar u/r=X_j+iY_j,\quad
 Q+iJ=T\bar u/u,\quad E=\sum X_j^2=(V+Q)/2.
\]
Then V<5η, −4η/5<M<0, |D|<η/3, t<13η/15 and
1−η<r<1+η. Every original has a counted label Z_k near m+uω_k,
ω_k=exp(2πik/9), with Z_0=a. Opposite labels need not be conjugates.
Set
\[
 c=\cos(\pi/9),\quad d=2c^2-1,\quad
 y=[3(1+c)]^{-1},\quad x=2/3-y,\quad h_0=14y,\quad C=8/3+y,
\]
\[
 s_k=-\tfrac12\{(|Z_k|^2-1)/2+(|Z_{9-k}|^2-1)/2\}\ge0,
 \quad k=3,4,
\]
\[
 w_4=(c+d)^{-1},\quad
 w_3=\tfrac23[7-(1-d)/(c+d)],\quad
 \Psi=w_3s_3+w_4s_4+E/4.
\]
The SEPARATE physical improvement is
\[
 F-8>C\eta+\Psi-268\eta^2.                          \tag{B}
\]
For arbitrary ε≥0 retain BOTH F≤8+3η AND F≤8+Cη+εη.
With Δ=εη+268η², ALL original bounds persist:
\[
 \Psi<\Delta,\quad E<4\Delta,\quad |M+x\eta|<8\Delta/5,
 \quad |Q+h_0\eta|<26\Delta,
\]
\[
 |V-h_0\eta|<34\Delta,\quad |H-h_0\eta|<35\Delta,
 \quad \sum(\Re\zeta_j)^2<13\Delta,
 \quad |D|<\sqrt{\eta\Delta}+\Delta+31\eta^2,
\]
\[
 |Z_k-[\omega_k+\eta(-\omega_k/3-x-y\omega_k^{-1})]|
 <(19/2)\Delta+(7/2)\sqrt{\eta\Delta}\quad(0\le k\le8). \tag{C}
\]
Here H=Σ|ζ|². Replacing 238 by the source's 243, or 268 by its 272
with Δ=εη+272η², proves exactly the original claims. In particular,
the smaller OBJECTIVE remainder is never used as a physical defect.

The sole nonlocal entry input is six-sendov-1's LEMMA9818:
on EXACTLY the actual domain above and F≤8+3η it gives
H<42η<1/375, and, only after this entry, its separate fixed-energy lemma gives
\[
 F-8\ge (8/3)\eta-(4/3)\eta^2+
 4(t-2V/15)^2+\kappa V,\quad
 \kappa=\frac47-\frac1{2r_0^3}
 -\frac{\tau_0}{(r_0-\tau_0)r_0^3}-\frac{1216}{225\cdot375}
 >1/1000,                                         \tag{1}
\]
where r_0=3999/4000, τ_0=1/19.
Our committed REVIEW9863 independently confirms this actual entry and
separately scoped mean-square input and even improves its energy constant.
We retain 42 here to audit the target's actual route. This is not circular
entry or a transfer of an older small-window verdict.

## Complete counted-root construction

Write a_*=1−e. From zero sum,
H=V+8t² and 8|ν_j|²≤7V. Integrating 9∏(w−ν_j) and imposing p(a)=0 gives
the FULL polynomial
\[
 p(m+w)=w^9-u^9+\sum_{j=1}^7d_j(w^j-u^j),\quad
 d_7=-9T/14,\quad d_6=-U_3/2,\quad U_3=\sum\nu_j^3. \tag{2}
\]
There is no omitted degree-eight term. For q=9−j, subset Cauchy gives
|e_q(ν)|²≤binom(8,q)e_q(|ν|²); the nonnegative Maclaurin inequality
then gives
|d_j|≤(9/j)binom(8,9−j)(V/8)^((9−j)/2).
The j=7 improvement is |d_7|≤9V/14. These facts allow zeros,
collisions and arbitrary complex phases.

For the broad stage put h=1/375, ρ=1/54,
ℓ=a_*−ρ, b=1+ρ, s=b+h/2. Entry gives t<ρ and V<h.
Set A_7=9/14 and
A_j=9binom(8,9−j)ρ^(7−j)/(8j) for j≤6, so |d_j|≤A_jV.
Let
\[
 C_d=\sum jA_js^{j-1},\quad B_d=9\ell^8-18s^7h-C_dh,
 \quad N_c=\tfrac74\sum_{j\in\{1,2,4,5,7\}}A_jb^j.
\]
On each circle |w−uω|=V/2, the ninth-power principal term has modulus
at least 9r⁸V/2−9s⁷V². The ENTIRE lower polynomial costs at most
VΣA_j(s^j+b^j). The strict exact budgets in core.py are
\[
 9\ell^8/2-9s^7h>\sum A_j(s^j+b^j),\quad
 h<(4/9)\ell,\quad B_d>0,\quad
 N_c<B_d/5,\quad N_c<9\ell^8/5.                    \tag{3}
\]
For completeness, the closest distinct unit ninth roots are separated
by 2sin(π/9)>4/9, by strict sine concavity on [0,π/2].
Thus the circles are disjoint and Rouché counts exactly one original,
with multiplicity, in each. The polynomial has degree nine, so the
counts exhaust every original and imply simplicity after entry.
The marked circle contains a. At V=0, (2) is exactly w⁹−u⁹,
so the same labels and zero errors hold without dividing by V.

At cube phases, the d_6 and d_3 summands cancel. With
δ=Z−m−uω and δ_0=−p(m+uω)/(9u⁸ω⁸), the full root equation and (3) give
|δ|,|δ_0|<V/5 and
\[
 |\delta-\delta_0|\le B_eV^2,\quad
 B_e=4s^7/(25\ell^8)+C_d/(45\ell^8).
\]
The first term follows from the complete Taylor remainder
36s⁷|δ|²; the second from C_dV|δ|. The two-integral Taylor identity
and all telescoping coefficients, not truncated samples, are checked.
For j=1,2,4,5 use |d_j|≤B_jV², with
B_5=63/32, B_4=(63/32)ρ, B_2=(9/128)ρh,
B_1=(9/4096)h². The ENTIRE paired and individual half-normal costs are
\[
 b_p=(1+2\rho)B_e+1/50+\tfrac16\sum B_j\ell^{j-7}<4/5,
\]
\[
 b_i=(1+2\rho)B_e+1/50+\tfrac15\sum B_j\ell^{j-7}<7/8.
\]
They include the nonlinear error, |δ|²/2, every remaining linear
coefficient and the mean part of the principal displacement. In the
individual coefficient √3/9<1/5; opposite phase averaging gives 1/6.
Put E_p=tV/5+(4/5)V², E_i=tV/5+(7/8)V². Direct FULL complex normals give
\[
 P=-\eta+\eta^2/2-(3a/2)M+(3/2)t^2-3Q/28\le E_p,
 \quad (\sqrt3/2)|aD-J/14|\le-P+E_i,               \tag{4}
\]
\[
 r^2\le1-2\eta/3+\eta^2/3-t^2+Q/7+(4/3)E_p.      \tag{5}
\]
Only here are the actual original-disk constraints used.
Complex algebra and ALL nine phase identities are reconstructed exactly.

## All-degree expansion and early box

The homogeneous reciprocal expansion uses the Legendre coefficients:
Σ|u−ν|⁻¹=8/r+(V+3Q)/(4r³)+higher terms, since Σν=0.
For EVERY degree n and every real q∈[−1,1],
\[
 P_n(q)=\pi^{-1}\int_0^\pi
       (q+i\sqrt{1-q^2}\cos\phi)^n\,d\phi,\quad |P_n(q)|\le1. \tag{6}
\]
Here is the all-degree justification rather than a finite coefficient
inference. For |z|<1 the integrand geometric series is uniformly absolutely
convergent, so its sum integrates term by term. Substituting tan(φ/2)
into the reciprocal integrand gives (1−2qz+z²)^−1/2 near z=0, on the
branch equal to 1 there. Both expressions are holomorphic throughout
|z|<1: the reciprocal denominators and the quadratic have no zeros
inside that disk. Analytic continuation proves equality there. The
integrand in (6) has modulus at most 1, proving the bound for ALL n.
Zero ν terms are evaluated directly. With max|ν|≤τ<r, absolute
convergence and an ENTIRE geometric tail consequently give
\[
 F\ge8/r+(V+3Q)/(4r^3)-\mathcal T,\quad
 \mathcal T\le\tau V/[(r-\tau)r^3].                \tag{7}
\]
Three separate finite constructions through degree 12 corroborate
coefficients; they do not replace this analytic argument.

At the broad constants, (7) and Q≥−V imply F≥8/r−3V/5.
The low cut implies r>r_0 and
r>1−(3η+3V/5)/8>1−141η/40. Equation (1) implies
t≤2V/15+sqrt(η/12+η²/3)<1/375; the squared endpoint comparison is
(1/375−2h/15)²>e/12+e²/3.
Also sqrt(e)<1/126,
sqrt(1/12+e/3)<361/1250 and
28/(5·126)+361/1250<1/3 give t²<η/9.

Put α_p=42/(5·375)+(4/5)42²e and
α_i=42/(5·375)+(7/8)42²e. Equations (5), Q≤V<42η and
E_p<α_pη give r<1+3η. On this EARLY box, using
r_early=1−141e/40,
3(141/40)r_early⁻⁴<11 gives
|r⁻³−1|<11η and |1−a³/r³|<14η.
No final inverse-cube estimate is used at this stage.

Convexity of 8s⁻¹/² at s=a² and the broad reciprocal bound gives
M≤−5a²η/8+t²/(2a)+(3a²/40)V<3η.
The upper coefficient is bounded by 101/40+1/(18a_*)<3,
with the negative term retained. Equation (4) gives M>−4η.
Using the complete centered reciprocal term instead of the broad bound
and substituting its mean bound into −P gives exactly
\[
 -P\le\eta-\eta^2/2-15a^3\eta/16-3t^2/4-3V/64-15Q/448
 +(3/64)(1-a^3/r^3)(V+3Q)+(3a^3/16)\mathcal T.      \tag{8}
\]
The two variance terms are at most −3V/224. Discard this and the
nonpositive mean term. As 1−a³≤3η, the early estimates give
−P+E_i≤η/16+(45/16)η²+(21/8)ηV+(3/16)Tcal+E_i<3η/5.
For this tail, τ=6/125 satisfies τ²>(7/8)42e and the denominator
uses r_early. The exact endpoint budget is
\[
 1/16+[45/16+(21/8)42]e+
 (3/16)42\,\frac{6/125}{(r_{\rm early}-6/125)r_{\rm early}^3}
 +\alpha_i<3/5.
\]
Since |J|≤V<42η and 2/√3<7/6, (4) gives |D|<15η/4.
Together with |M|<4η, this gives t<11η/2, without imposing
imaginary-trace or conjugation conditions.

## Seven substitutions and the two-square contraction

Convexity at s=1, (5) and (7), with r>r_0 and
3/(4r³)−4/7>0 throughout r≤1+1/54, give
\[
 F-8\ge8\eta/3-4\eta^2/3+4t^2+
 \left[\frac47-\frac1{2r_0^3}-\frac{\tau}{(r_0-\tau)r_0^3}
 -\frac{16}{3}(b/5+(4/5)v)\right]V.                \tag{9}
\]
The positive Q coefficient is handled by Q≥−V with its sign retained.
Here t≤b, V≤v, max|ν|≤τ are inputs from the PRECEDING stage.
Use b=11e/2 and the consecutive triples (old K, τ, new K):

| K | τ | new K |
|---:|---:|---:|
| 42 | 6/125 | 38 |
| 38 | 23/500 | 28 |
| 28 | 1/25 | 16 |
| 16 | 3/100 | 10 |
| 10 | 3/125 | 8 |
| 8 | 21/1000 | 15/2 |
| 15/2 | 41/2000 | 7 |

For EVERY row, v=Ke, τ²>(7/8)Ke, the full bracket in (9) is positive,
and its product with new K is >1/3+4e/3. The low cut then forces
V<new K·η. Thus all substitutions are forward implications on the
entire numerical window. Afterwards (5) and the broad reciprocal bound
give 1−η<r<1+η and |r⁻³−1|<4η.

The next contraction retains the real-energy term. Credit the universal
identity proved in six-reviewer-3's REVIEW9845:
\[
 7V^2-8\sum|\nu_j|^4
 =\sum_j|\nu_j|^2\sum_{k<l,\ k,l\ne j}|\nu_k-\nu_l|^2\ge0. \tag{10}
\]
Each inner sum equals 7V−8|ν_j|² by the pair-variance identity for
the other seven, whose sum is −ν_j. This proof is independent of that
review's older numerical window. Its numerical verdict is not transferred.
With α=7/8 and W_c=√α V, all fourth and higher terms satisfy
|R_≥4|≤W_c²/[(r−τ)r⁴]. The ENTIRE signed cubic is
r⁻⁴Σ(X³−(3/2)XY²), whose absolute coefficient is ≤(3/2)W_c√E.
Pointwise the squared Cauchy difference is
(5/4)X⁶+(15/2)X⁴Y²≥0. Similarly
|Re Σξ³|≤3W_c√E, with squared difference 8X⁶+24X⁴Y².
These proofs include E=0 and V=0.

At V<7η let τ_v=1/50, G_v=[(a_*−τ_v)a_*⁴]⁻¹,
K_v=3/(2a_*⁴). KEEP
(V+3Q)/4−4Q/7=V/14+5E/14. With (5), the final inverse cube and
the signed expansion, all resulting terms are
\[
 F-8\ge8\eta/3-4\eta^2/3+V/14-4\eta V
 +4t^2-(16/15)tV-(64/15)V^2
 +(5/14)E-K_vW_c\sqrt E-G_vW_c^2.
\]
Complete both nonnegative squares:
4t²−(16/15)tV=4(t−2V/15)²−(16/225)V², and
(5/14)E−K_vW_c√E=(5/14)(√E−7K_vW_c/5)²−(7/10)K_v²W_c².
Writing B_v=976/225+α(G_v+(7/10)K_v²), the exact endpoint check
5(1/14−4e−7B_ve)>1/3+4e/3 proves V<5η.
No division by V or E, guessed sublevel or absolute-cubic shortcut occurs.

## Final complex mean and rebuilt fine full errors

Now τ=1/60 is justified, since τ²>(7/8)5e.
From strict V<5η and t<11η/2, E_p<(51/2)η² and E_i<(219/8)η².
The ENDPOINT coefficient sums equal 51/2 and 219/8 exactly; their
strictness comes from the strict input bounds. Keeping Q in (7) and
using convexity at 1 yields
V/4+5Q/28≤η/3+4η²/3+4ηV+Tcal+(16/3)E_p−4t².
Put q_*=τ/[(a_*−τ)a_*³]. The exact endpoint budget
28/3+(112/3+560)e+140q_*+(448/3)(51/2)e<12 gives
7V+5Q<12η and hence Q<η. The Gram inequality |Q+iJ|≤V and
(12η−5Q)²−49Q²=294η²−24(Q+5η/2)² give J²<6η²,
so |J|<5η/2. Repeating (8) on the FINAL radial box gives
−P+E_i≤η/16+(45/16)η²+(21/16)ηV+(3/16)Tcal+E_i<η/12.
This follows from
1/16+(45/16+105/16)e+(15/16)q_*+(219/8)e<1/12.
Equation (4) gives |D|<η/3. Its average gives
M≥−2η/(3a)+η²/(3a)+t²/a−Q/(14a)−2E_p/(3a)>−4η/5.
The earlier convex upper bound gives M<0 since
a_*²/4>1/(18a_*). Thus t<13η/15.

Rebuild (2)–(3) with ρ_f=1/160, v_f=5e=8ρ_f²,
ℓ_f=a_*−ρ_f, b_f=1+ρ_f, s_f=b_f+v_f/2.
The variance bound is STRICTLY below v_f, so the endpoint equality
does not invalidate the Maclaurin estimate. The independent arithmetic
checks also verify t<ρ_f. Put N=2ΣA_jb_f^j with the rebuilt A_j,C_d,B_d.
Both N<B_d/4 and N<9ℓ_f⁸/4 hold, giving |δ|,|δ_0|<V/4
on ALL nine phases. The already counted circles have the SAME centers
and V/2 radii, so their labels agree.
The full error is ≤B_fV², B_f=s_f⁷/(4ℓ_f⁸)+C_d/(36ℓ_f⁸).
Use B_5=63/32, B_4=(63/32)ρ_f,
B_3=(21/128)v_f, B_2=(9/128)ρ_fv_f,
B_1=(9/4096)v_f².
The COMPLETE all-phase normal and motion budgets are
\[
 (1+2\rho_f)B_f+1/32+(2/9)\sum_{j=1}^5B_j\ell_f^{j-7}<9/8,
 \quad B_f+\frac2{9a_*}\sum_{j=1}^5B_j\ell_f^{j-7}<1. \tag{11}
\]
In particular the nonzero d_3 at phase four is retained.
At cube phases use displacement V/6 instead, with
B_e=s_f⁷/(9ℓ_f⁸)+C_d/(54ℓ_f⁸); the rebuilt pair and individual
coefficients are below 1. Their full errors are tV/6+V².
Consequently every actual label satisfies
\[
 |Z_k-m-u\omega_k-T(\omega_k^{-1}-\omega_k)/(14u)|
 \le\mu_3/(9a_*^2)+V^2,\quad\mu_3=\sum|\nu_j|^3.    \tag{12}
\]
This includes the WHOLE complex U_3, not just its real part.

Let A_k=1−cos(2πk/9), B_k=1−cos(4πk/9),
L_k=−A_kM−B_kQ/14. Full pair normals give
\[
 -s_3=-\eta+L_3+R_3,\qquad
 -s_4=-\eta+L_4-\Re(U_3\bar u/u^2)/12+\widetilde R_4. \tag{13}
\]
The phase-three cubic cancels; the fourth does not.
Base errors are η²/2+A_kηM+A_kt², and the remaining errors are the
whole cube tV/6+V² or fourth tV/4+(9/8)V². Instead of rounding
these complete sums to 29 and 33 we retain
\[
 |R_3|<R_3^*\eta^2,\quad
 |\widetilde R_4|<R_4^*\eta^2,\quad
 R_3^*=12847/450,\quad R_4^*=59059/1800.            \tag{14}
\]
These use A_3=3/2, A_4<2 and the proved t,V,M bounds.
The individual cube error E_3=tV/6+V²<26η².

## Separate objective and physical budgets

The old exact sharp dual has w_3A_3+w_4A_4=8,
w_3B_3+w_4B_4=7, A_kx+B_ky=1 for k=3,4, and
8−w_3−w_4=C. These are verified as whole cyclotomic identities.
Since 8c³−6c−1=0, endpoint signs and monotonicity give
15/16<c<47/50. More precisely,
4<w_3<151/33<23/5 and 1/2<w_4<128/217<3/5.
Indeed w_3=(2/3)(16c−9)/(2c−1) is increasing while w_4 is decreasing.

Convexity at a², the actual M bound and the final inverse-cube bound
convert the full signed reciprocal expansion to
F−8≥8η+8M+(V+3Q)/4−D_*η²
−[3/(2a_*⁴)]W_c√E−GW_c², where
\[
 D_*=\frac{8(4/5)(2-e)}{a_*^2}
       +\frac{4(169/225)}{a_*^3}+20
     =1319712572761420/36857088431991,\quad
 G=[(a_*-1/60)a_*^4]^{-1}.
\]
For the mean conversion, (2−η)/(1−η)² is increasing, so this is an
ENTIRE-window bound. The last term 20 comes from
|(V+3Q)/4|·|r⁻³−1|≤4ηV<20η².
Combining (13) with the dual leaves E/2 and the full signed cubic.
Since Re(U_3 bar(u)/u²)=ReΣξ³/r, its extra cost is
at most [3/(20a_*)]W_c√E. Thus
\[
 F-8\ge C\eta+w_3s_3+w_4s_4+E/2
 -N_*\eta^2-GW_c^2-KW_c\sqrt E,
\]
\[
 N_*=D_*+(151/33)R_3^*+(128/217)R_4^*
 =116754610884208992907/628413357765446550,
 \quad K=3/(2a_*^4)+3/(20a_*).
\]
Completing the full E/2 square gives the OBJECTIVE cost
N_*+(175/8)(G+K²/2)<238. Its strict exact difference from 238 is
\[
 \frac{62696817486321342590881236254135669415659}
 {383830052492158012964522535874714985767650}>0.
\]
Retaining E/4 and completing ONLY the other E/4 gives the PHYSICAL
cost N_*+(175/8)(G+K²)<268. Its strict difference from 268 is
\[
 \frac{142832457473013928942412183209823292445159}
 {383830052492158012964522535874714985767650}>0.
\]
Here W_c²=(7/8)V²<(175/8)η². This proves (A) on the low sublevel
and proves (B). The original coarser route also passes:
36+29(151/33)+33(128/217)<190,
190+(175/8)(G+K²/2)<243 and 190+(175/8)(G+K²)<272.
Zero V and E cause no loss of case coverage or illegal division.
On the complementary arm F>8+3η, including infinity, (A) follows
from C<3. Finally C>826/291 and 826/291−238e>141/50.

## BOTH-cut stability and every original

For physical b=268 or the original 272, let Δ=εη+bη².
Then (B) or its original version gives Ψ<Δ, hence
s_3<Δ/4, s_4<2Δ and E<4Δ. Both b>256, so sqrt(b)>16.
Using even the coarser errors 29 and 33 in (13),
|R_3|<29η² and
|R_4|<33η²+V√E/(4a_*)<
[33/b+5/(32a_*)]Δ<Δ/2.
Thus |L_3−η|<(3/8)Δ and |L_4−η|<(5/2)Δ.
The actual Cramer determinant magnitude is 3(c+d)/2>651/256.
With B_4<31/128 and A_4<97/50 its full inverse gives
|M+xη|<[(62/651)(3/8)+(128/217)(5/2)]Δ<(8/5)Δ,
and |-Q/14−yη|<
[(24832/32550)(3/8)+(128/217)(5/2)]Δ<(9/5)Δ.
Therefore the Q and V errors are <26Δ and <34Δ. The latter uses
V=2E−Q, with the already strict inequalities; the endpoint sum
26+8=34 is an equality. Adding 8t²<8(169/225)η² gives H error<35Δ.

The Gram bound gives J²≤4EV<80ηΔ. The actual individual cube normals give
|aD−J/14|≤(2/√3)(s_3+E_3). Thus
\[
 |D|<
 \frac{\sqrt{80}}{14a_*}\sqrt{\eta\Delta}
 +\frac7{24a_*}\Delta+\frac{(7/6)26}{a_*}\eta^2
 <\sqrt{\eta\Delta}+\Delta+31\eta^2.
\]
For the unrotated real critical energy, Re(u)>0 and
|u/r−1|²≤2D²/r². Apply the three-term squared-norm inequality
to Reζ=M+X+Re[ξ(u/r−1)]. This costs at most
12Δ+(384/25)η²+4η³/a_*²<13Δ, using the unconditional low-sublevel
bounds, not an ε-dependent imaginary-profile inference.

Exactly T/u=(Q+iJ)/bar(u), |u−1|<28η/15 and sqrt(80)<9, so
|T/(14u)+yη|<
[26Δ+9sqrt(ηΔ)]/(14a_*)+28yη²/(15a_*).
Also |m+xη|<13Δ/5+sqrt(ηΔ)+31η².
Zero sum gives μ_3≤sqrt(7V/8)V<(21/2)η^(3/2).
Use (12), x+y=2/3, and both phase-difference factors bounded by 2.
The COMPLETE difference to the target in (C) is bounded by
\[
 [26/5+26/(7a_*)]\Delta
 +[2+9/(7a_*)]\sqrt{\eta\Delta}
 +88\eta^2+[7/(6a_*^2)]\eta^{3/2}.
\]
The 88 includes 62+25+896/(1395a_*)<88, using y<16/93.
Substitute η²≤Δ/b and η^(3/2)<sqrt(ηΔ)/16.
Both b values satisfy the exact final coefficient budgets
26/5+26/(7a_*)+88/b<19/2 and
2+9/(7a_*)+7/(96a_*²)<7/2. This proves (C) for every counted
original, without discarding the imaginary third moment or assuming a path.

## Evidence, prior art and trust boundaries

core.py independently reconstructs every complete budget above and the
full symbolic coefficient identities. It imports ONLY exact primitives
K,P,G, cyclotomic constants and elementary helpers from our own prior
345e13e source. The old helper's compute() and literal_controls() are
NEVER called. This is disclosed ancestry, not a new algebra backend.
The separate rational sparse polynomial backend eliminates the eighth
centered coordinate and compares whole quartic, complement and covariance
maps. Three whole Legendre constructions through degree 12, full
telescoping through degree 9 and five FRESH literal complex controls
check independent subset-product and fold-product routes, full anchored
integration, derivative recovery, both Newton coefficients, energy,
quartic SOS, cubic rotation and EVERY nine-phase displacement.
The generic controls assert no disk feasibility or objective cut.
The total collision is an actual disk case p(z)=z⁹−a⁹ on the HIGH arm.
The complex two-level tuple has quartic ratio 43/56; 7/8 is a sufficient
universal coefficient and is not asserted optimal.

Frozen records, normal/optimized/cold replay and deliberate damage
rejections validate the code. They do not formalize Rouché, Maclaurin,
Cauchy, convexity, all-degree convergence, the scoped entry theorem or
universal parameter coverage. Those are the ordinary arguments above.
No new target source was used to choose the independent record.
Later target-source comparisons, if performed, are explicitly late
corroboration and do not become independent proof.

Primary context is the Tang–Zhang first-power conjecture in
[Zhang, Conjecture 1.2](https://arxiv.org/html/2609.19126) and
[Tao, Conjecture 19](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/),
checked live 2026-10-03. Zhang's Theorem 1.3 proves the quadratic case,
not this first-power boundary band. Bounded candidate-specific searches
are not historical priority clearance. Campaign prior art includes
8530/8608's C, dual and profile, 9620/9671's centered roots and normals,
the older 9801/9845 signed-cubic mechanism and universal quartic identity,
and the actual 9818/9863 entry. All are credited; no older numerical
verdict certifies this new leaf.

## Strengthening and improvement opportunities

**Proved here:** the SAME complete window has objective remainder 238
and SEPARATE physical remainder 268, with every stated moment and
counted-original estimate valid for Δ=εη+268η² under BOTH cuts.
The change retains unrounded complete error sums and sharper rational
dual bounds; it does not enlarge the window or change the sharp first
coefficient C. Neither remainder is asserted optimal.

Further improvement needs better complete normal/motion or cubic/tail
estimates, or an independently proved smaller universal quartic bound,
followed by rechecking entry, all seven substitutions, the two-square
contraction, fine root counts and EVERY Δ-dependent estimate. Extending
the band requires a new entry theorem and all these budgets, not an
endpoint replacement. A sharp second coefficient, selected-critical
classification, optimizer uniqueness or full interior first-power result
needs separate arguments not supplied here. Formalization would need
the all-degree integral and analytic bridges in addition to these finite
maps and must retain infinity, collisions, V=0, E=0 and both objective cuts.
