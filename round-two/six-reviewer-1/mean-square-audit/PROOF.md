# Independent mean-square boundary audit and stronger actual energy

Actual author **six-reviewer-1**, role **independent mathematical reviewer**,
2026-10-02. Target LEMMA9818/0, researcher six-sendov-1, source
**b1df3a9250928ccf97593e3a55c2084a2bb4712e**,
[complete defining proof](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-sendov-1/mean-square-routing/PROOF.md).
Verdict: **CONFIRMS** its whole actual-polynomial domain, global entry,
fixed-energy mean-square surplus and unconditional basic first-power bound.
The proof below remains ordinary and **unformalized**.

## 1. Exact scope and strengthened statements

For every actual complex monic degree-nine polynomial with all nine original
zeros in the closed unit disk, rotate a marked original to \(a=1-\eta\).
For every \(0<\eta\le e=1/16000\), count all eight critical points
\(\zeta_j\) with algebraic multiplicity, and put
\[
 F=\sum|a-\zeta_j|^{-1},\qquad H=\sum|\zeta_j|^2.
\]
A zero denominator means infinity. We confirm
\[
 F\le8+3\eta\Longrightarrow H<42\eta<1/375,\qquad
 F>8+\frac83\eta-\frac43\eta^2
 \ge8+\frac{31999}{12000}\eta>8+\frac{13}{5}\eta.        \tag{1}
\]
The new refinement on the same actual domain and low objective cut is
\[
 \boxed{H<40\eta\le1/400},                            \tag{2}
\]
so \(H<1/400\), including at the endpoint. No optimality of40 is asserted.
No initial critical energy/radius/coefficient, conjugation, separation,
template, attained optimizer or smooth-family assumption is used.
Finite \(F\) forces only the marked original simple. Other multiplicities
remain until the actual root-counting argument proves simplicity.
Normalized reciprocal tuples are algebraic envelopes, not actual polynomials.

Independently assume \(H\le1/375\) and the same low \(F\) cut. Set
\[
 m=\frac18\sum\zeta_j,\quad t=|m|,\quad \nu_j=\zeta_j-m,\quad
 W=\sum|\nu_j|^2,\quad r_0=3999/4000,\quad \tau=1/19,
\]
\[
 \beta=\frac47-\frac1{2r_0^3}
       -\frac{\tau}{(r_0-\tau)r_0^3}.
\]
The target's separate fixed-energy statement is confirmed:
\[
 F-8\ge\frac83\eta-\frac43\eta^2+
 4(t-2W/15)^2+\kappa_{375}W,\quad
 \kappa_{375}=\beta-\frac{1216}{225\cdot375}>\frac1{1000}. \tag{3}
\]
After the genuine entry (2), the same proof strengthens this to
\[
 F-8\ge\frac83\eta-\frac43\eta^2+
 4(t-2W/15)^2+\kappa_{400}W,\quad
 \kappa_{400}=\frac{5553785913936784}{2877081109812511875}
             >\frac1{600}.                           \tag{4}
\]
All root/normal/tail budgets retain the independently certified
\(H\le1/375\) region; only absorption of \(W^2\) uses \(W<1/400\).

## 2. Whole polar communication and normalization

In the finite low sublevel put \(q_j=(a-\zeta_j)^{-1}\),
\(r_j=|q_j|\), \(Q_q=\sum q_j\), \(\mu=F/8\),
\(\Delta=F-\Re Q_q\), \(V_r=\sum(r_j-\mu)^2\).
Gauss--Lucas gives \(r_j\ge\ell=1/(1+a)>1/2\).
Integrating the derivative from the marked original and taking products
over the other eight originals gives classical reciprocal communication:
\[
 |O_a(q)|\le P(r),\quad |C_a(q)|\ge1,\quad
 O_a(q)=9\int_0^1\prod(1-atq_j)\,dt,\quad
 C_a(q)=\int_0^1\prod(a+btq_j)\,dt,\quad b=1-a^2,\quad P=\prod r_j.
\]
For the polar factors,
\(|1-az_i|^2-|a-z_i|^2=b(1-|z_i|^2)\ge0\).
Products and integration preserve all multiplicities.

Let \(L=8+3\eta,d=a^7b/2\),
\[
 T=\sum_{k=2}^8\frac{\binom8k}{k+1}a^{8-k}b^k(L/8)^k,\quad
 B=a^8+dL+T.
\]
Squaring the entire complex polar expression before estimating the real
mean, Maclaurin gives
\[
 1\le a^{16}+a^{15}b\Re Q_q+d^2L^2+2(a^8+dL)T+T^2.
\]
The whole polynomials
\[
 N_m=1-a^{16}-d^2L^2-2(a^8+dL)T-T^2-(8-6\eta)a^{15}b,
\]
\[
 N_b=1+9\eta^2-B,\qquad N_v=13a^6b^2-6(B-1)
\]
have degrees48,24,24, zero constant/linear coefficients, and quadratic
coefficients \(4/3,2/3,2\). Direct full product integration and the full
binomial route agree. Complete absolute-tail coefficient budgets at \(e\)
exceed \(1,1/2,1\). Retaining
\(e_2(r)=7F^2/16-V_r/2\) gives
\[
 \Re Q_q>8-6\eta,\quad\Delta<9\eta,\quad
 |\mu-1|<3\eta/4,\quad V_r<13.                         \tag{5}
\]

Preserve phases and normalize total radius to8. For \(F\le8\) add
\(1-\mu\) to every radius. For \(F>8\), set
\[
 r'_j=\ell+\lambda(r_j-\ell),\quad
 \lambda=8a/[(1+a)F-8],\quad q'_j=(r'_j/r_j)q_j.
\]
Then \(a<\lambda\le1\), the floor persists, and, with
\(v=\sum(r'_j-1)^2\), weighted Cauchy proves
\[
 \sum|r'-r|=|8-F|<6\eta,\quad v\le V_r<13,\quad
 V_r\le(65/64)v,\quad\Delta'<10\eta,\quad
 (\sum|q'-r'|)^2<160\eta.                             \tag{6}
\]
Explicit margins use \(a>255/256,a^{-2}<65/64\) and
\(10-9(1+3e/2)>0\). Every same-phase radial segment keeps floor, total
at most \(8+3e\), deficit \(<10\eta\), and phase norm squared
\(<(160+60e)\eta<161e<1/81\).

## 3. Separate real/complex derivatives and complete stronger faces

Put \(A=4+3e,R_k=1/2+A/k\). If a proper product of \(m=6\) or7 real
factors has exactly \(k\) negative factors, AM--GM bounds their product
by \((uR_k-1)^k\), while each positive factor is at most \(1-u/2\).
The nonnegative envelope covering every sign pattern is
\[
 G_m(u)=(1-u/2)^m+\sum_{k=1}^m
 {\bf1}_{u\ge1/R_k}(1-u/2)^{m-k}(uR_k-1)^k.
\]
A single product has a single negative count, so no extra binomial
multiplicity is required. All proper residual products, including the
empty product, are \(<4\) or at most1: explicit \(k=1,2\) margins pass,
and \(R_k-1<1\) for \(k\ge3\).
The entire finite complex correction for \(\epsilon<1/9\) is
\[
 \prod_{i\in S}|1-uz_i|\le G_m(u)+
 4\sum_{k=1}^m(u\epsilon)^k/k!.
\]
Substitute \(u=at\) in either derivative integral, giving prefactor \(1/a\).
All15 sector integrals are evaluated by whole polynomial antiderivatives
and positive shifted-beta expansions, coefficient/support/integral complete.
The full bounds are
\[
 K_{1,\mathrm{real}}<7/5,\quad
 K_{1,\mathrm{complex}}<14/5,\quad
 K_{2,\mathrm{complex}}<7/3,\quad\partial_jP<2.
\]
Complex corrections retain all
\(36\epsilon^k/[k!(k+2)]\) or \(36\epsilon^k/[k!(k+3)]\).
The real first derivative does not require this correction.
There are no pure second partials.

At real \(r'\), \(h=q'-r'\) has
\(-\Re h_j=|h_j|^2/(2r'_j)\le|h_j|^2\).
Retaining the ordered mixed sum and \(1/2\) Taylor factor, the loss is
\[
 (7/5)\sum|h_j|^2+(7/6)\sum_{j\ne k}|h_jh_k|
 \le(7/5)(\sum|h_j|)^2<224\eta.
\]
Full normalization cost gives
\[
 O_a(r')-P(r')<[224+6(14/5+2)]\eta<253\eta.             \tag{7}
\]
The old complex-gradient bound5/2 fails on the larger endpoint.

Set \(y_j=(1+a)r'_j-1\ge0,\sum y=8a,E_2=e_2(y)\),
\(D=2aE_2-e_3(y)\). On this total-eight face,
\[
 (1+a)^8(O_a(r')-P(r'))\ge8(1-a^9)+(39/5)D.           \tag{8}
\]
To prove full coverage, choose a compact-simplex minimizer of the
symmetric multiaffine residual with fewest free coordinates.
If two unequal free coordinates vary at fixed sum, stationarity forces
their cross coefficient zero; the restriction is constant. Moving to a
floor endpoint contradicts minimality. Thus every free coordinate agrees.
The eight complete cases are \(m=1,\ldots,8\) free radii
\((1+8a/m)/(1+a)\). Their entire residuals are
\[
 R_m=9\int_0^1(1+a-at)^{8-m}(1+a-at-(8/m)a^2t)^m\,dt
 -(1+8a/m)^m-8(1-a^9)-(39/5)d_ma^3,
\]
\[
 d_m=64(m-1)/m-256(m-1)(m-2)/(3m^2).
\]
Full factor multiplication in \((\eta,t)\) and full binomial expansion
in \(a\), followed by substitution, agree. Every first nonzero coefficient
minus its whole endpoint absolute-tail cost is positive. First order is
one for \(m=1,8\), zero otherwise. All floor/equal/zero-defect cases are
covered. Penalty8 fails at \(m=2,a=1\);39/5 is not asserted optimal.

Equations(7)--(8) give \(D<d_0\eta,d_0=323840/39\).
Exactly \(E_2=28a^2-(1+a)^2v/2\). Maclaurin and
\(1-\sqrt x\ge(1-x)/2\) give
\[
 D\ge E_2(1+a)^2v/(56a)\ge E_2v/14.
\]
Starting \(v<13\) gives \(E_2>7/4,D\ge v/8\).
Successive proved bounds are
\[
 v<8d_0\eta<5,\ E_2>17;\quad
 v<(14/17)d_0\eta<43/100,\ E_2>27;\quad
 v<(14/27)d_0\eta<27/100.                             \tag{9}
\]
Each \(E_2\) bound uses the preceding endpoint; no initial small variance
or division by zero is hidden.

## 4. Entire local paths, moments and both variance reductions

Convexity of squared norm along every radial segment gives
\(\sum(r_s-1)^2<7/25\), each \(|r_{s,j}-1|<1/2\);
use \(|r_j-\mu|^2\le7V_r/8\) and the strict endpoint margin.
Phase squared norm is \(<30\eta\). Thus all radial, phase and scaling
paths satisfy
\[
 \|az-1\|_2^2<(53/100+9/200+3e)^2<1/3,
\]
using \(\sqrt{7/25}<53/100,\sqrt{30e}<9/200\).
Cauchy/Maclaurin on all remaining6 or7 slots with scale6/25 bounds
every coefficient of the complete derivative integrals:
\[
 |\partial_jO_a|<2/9,\qquad|\partial_{ij}O_a|<1/12.
\]
On real radial segments, \(d_j=ar_{s,j}-1\) have sum modulus \(<14\eta\)
and individual modulus \(<1/2+\eta\). The signed derivative constant and
linear terms are \(-1/8,1/28\); the entire higher tail is bounded by
\[
 U=1/[8(1-6/25)^2]-1/8-(6/25)/4.
\]
The endpoint margin gives \(\partial_jO_a(r_s)<-(3/40)a\).
Complex change is \(<1/108\), and \(\cos\theta_j>1-20\eta\);
\((3/40)(1-e)(1-20e)>1/108\) preserves
\(\Re[\partial_jO_a(q_s)e^{i\theta_j}]<0\).
Subtracting the positive radial derivative of \(P\) preserves this sign.
For \(F\le8\) normalization cost is nonpositive. For \(F>8\) it is at
most \(3(2/9+2)\eta\). At real \(r'\), the first phase Taylor term is
nonnegative, leaving mixed cost \(80\eta/12\). Scaling \(a\) to1 costs
\(16\eta/9\). Hence the full upper bound is
\[
 O_1(r')-P(r')<(136/9)\eta.                            \tag{10}
\]

For \(x_j=r'_j-1,\sum x=0,v=\sum x^2\), the classical bound
\(|p_3|\le3v^{3/2}/\sqrt{14}\) follows by compact maximization:
at \(v>0\), independent constraint gradients and Lagrange multipliers
force two distinct values. All \(k=1,\ldots,7\) positive counts give
squared ratio \((8-2k)^2/[8k(8-k)]\le9/14\); negation handles absolute
value and \(v=0\) is direct. Cauchy and the zero-sum individual bound give
\(v^2/8\le p_4\le7v^2/8\), so
\(e_4=v^2/8-p_4/4\) implies \(|e_4|\le3v^2/32\).
The whole radial identity is
\[
 O_1(r')-P(r')=\sum_{k=2}^8[(-1)^k/\binom8k-1]e_k(x).
\]
Its quadratic term is \(27v/56\), degree-eight coefficient zero.
At \(v\le27/100\), \(|p_3|\le3v/7\). Full Newton majorants are
\(B_0=1,B_1=0,B_2=v/2,B_3=v/7,B_4=3v^2/32\) and, for \(k=5,6,7\),
\[
 B_k=[vB_{k-2}+(3/7)vB_{k-3}
 +(7/8)v^2\sum_{s=4}^k(1/2)^{s-4}B_{k-s}]/k.
\]
All coefficients of \(B_k/v\) are nonnegative. The entire cost at27/100
leaves \(1047670269/4390400000>1/6\). Thus the gap is at least \(v/6\),
including \(v=0\), and (10) gives
\[
 v<(272/3)\eta<91\eta<1/128.                           \tag{11}
\]

Now radial squared norm is \(<(9/100)^2\), every coordinate differs
from1 by \(<1/10\), and phase squared norm \(<22\eta\) has root \(<3/80\).
Every scaled path lies in
\(\|az-1\|_2^2<(9/100+3/80+3e)^2<1/60\).
Scale1/18 in the complete coefficient bounds gives gradient \(<1/7\),
mixed Hessian \(<1/23\), product gradient
\(<[(71/70)+3e/7]^7<10/9\). These paths lie inside the preceding
favorable-sign region. The complete new upper cost is
\[
 O_1(r')-P(r')<B_*\eta,\quad
 B_*=\frac{11}{7}+\frac{10}{3}+\frac{80}{23}=\frac{4049}{483}.
\]
Use \(|p_s|\le v(1/10)^{s-2}\), the full fourth Newton identity, and
\(B_0=1,B_1=0,B_2=v/2,B_3=v/30,B_4=v^2/8\),
\[
 B_k=(v/k)\sum_{s=2}^k(1/10)^{s-2}B_{k-s},\quad k=5,6,7.
\]
The entire higher-degree budget at1/128 leaves
\[
 c_2=2928703031/6553600000>4/9.
\]
Replacing \(c_2\) by4/9 confirms target
\(V_r<(77/4)\eta,\sum|q_j-1|^2<38\eta,r_j>24/25\).
The exact identity \(\zeta_j=-\eta+(q_j-1)/q_j\), Minkowski,
\(\sqrt{38}<37/6,\sqrt{8e}<9/400\) yields the original \(H<42\eta\).

Retain the full \(c_2\) instead:
\[
 A_v=B_*/c_2=\frac{26535526400000}{1414563563973},\quad
 A_r=(65/64)A_v=\frac{26950144000000}{1414563563973}.
\]
Then \(v<A_v\eta,V_r<A_r\eta\), and
\[
 \sum|q_j-1|^2=V_r+8(\mu-1)^2+2\Delta
 <[A_r+18+(9/2)e]\eta
 =\frac{1677205951920523757}{45266034047136000}\eta
 <(609/100)^2\eta.
\]
The strict endpoint margin
\((1/30-3e/4)^2-(7/8)A_re>0\) gives every \(r_j>29/30\).
Since \((609/100)/(29/30)=63/10\),
\[
 H<(63/10+9/400)^2\eta
 =\frac{6395841}{160000}\eta<40\eta,\qquad
 40-\frac{6395841}{160000}=\frac{4159}{160000}>0.
\]
This proves (2) before any fixed-energy premise is applied.

## 5. Complete actual roots, normals and fixed-energy region

Independently assume \(H\le h=1/375\) and the low \(F\) cut.
Take \(\rho=1/54,\tau=1/19,L_c=1/2\),
\[
 r_-=1-e-\rho,\quad r_+=1+\rho,\quad s=r_++L_ch,\quad
 u=a-m,\quad r=|u|.
\]
Then \(t\le\rho,W\le h,\max|\nu_j|\le\sqrt W<\tau\);
\(8\rho^2>h,\tau^2>h,r_-\le r\le r_+\).
Derivative integration and anchoring at the marked original give exactly
\[
 p(m+w)=w^9-u^9+\sum_{j=1}^7d_j(w^j-u^j),\quad
 d_7=-9T_c/14,\quad T_c=\sum\nu_j^2.
\]
All-subset Cauchy/Maclaurin gives
\[
 |d_j|\le(9/j)\binom8{9-j}(W/8)^{(9-j)/2}\le A_jW,\quad
 A_7=9/14,\quad A_j=[9/(8j)]\binom8{9-j}\rho^{7-j}\ (j\le6).
\]
Put
\[
 C_d=\sum jA_js^{j-1},\quad
 B_d=9r_-^8-36s^7L_ch-C_dh,\quad
 N_c=(7/4)\sum_{j=1,2,4,5,7}A_jr_+^j.
\]
Entire new endpoint budgets verify
\[
 9r_-^8L_c-36s^7L_c^2h>\sum_jA_j(s^j+r_+^j),\quad
 2L_ch<(4/9)r_-,\quad B_d>0,\quad
 N_c<B_d/5,\quad N_c<9r_-^8/5.
\]
For \(W>0\), Rouché on all nine disjoint circles
\(|w-u\omega|=L_cW,\omega^9=1\), gives one actual simple original
in each. Ninth-root separation exceeds4/9 by strict sine concavity.
Label \(Z_\omega=m+u\omega+\delta_\omega\), with \(Z_1=a\).
At the two nonreal cube phases \(d_6,d_3\) cancel. The complete root
equation gives
\[
 |\delta|,|\delta_0|<W/5,\quad
 \delta_0=-p(m+u\omega)/(9u^8\omega^8),\quad
 |\delta-\delta_0|\le B_eW^2,\quad
 B_e=4s^7/(25r_-^8)+C_d/(45r_-^8).
\]
Old displacement \(W/6\) fails and is not imported.
All-subset bounds further give \(|d_j|\le B_jW^2\), where
\[
 B_5=63/32,\quad B_4=(63/32)\rho,\quad
 B_2=(9/128)\rho h,\quad B_1=(9/4096)h^2.
\]
Both whole normal error estimates satisfy
\[
 (1+2\rho)B_e+1/50+c\sum_{j=1,2,4,5}B_jr_-^{j-7}<1,
 \qquad c=1/6,\ 1/5.
\]
These retain all nonlinear error and \(|\delta|^2/2\).
The credited universal cube-field pair identity has principal normal
\(-3Q_c/28\), with \(Q_c+iJ_c=T_c\bar u/u,\ |Q_c|\le W\).
The full \(\bar m\delta_0\) term costs \(tW/5\).
Using actual original norms \(|Z_\omega|\le1\) yields
\[
 r^2\le1-2\eta/3+\eta^2/3-t^2+Q_c/7+(4/3)E_c,\quad
 E_c=tW/5+W^2.                                      \tag{12}
\]
The individual normal is covered, without claiming new imaginary-mean
or profile motion stability. At \(W=0\), the polynomial is exactly
\(w^9-u^9\), all errors vanish, and the same disk constraints hold
without division by \(W\).

## 6. Whole Legendre tail, square completion and strict cases

The complete convergent Legendre expansion gives
\[
 F\ge8/r+(W+3Q_c)/(4r^3)-\mathcal T,\qquad
 \mathcal T\le\frac{\tau}{(r-\tau)r^3}W.                \tag{13}
\]
The Laplace representation integrand
\((x+i\sqrt{1-x^2}\cos\phi)^k\) has modulus at most1 for
\(-1\le x\le1\); its finite expansion gives the generating coefficients
and \(|P_k(x)|\le1\). Absolute convergence since \(|\nu|/r<1\)
justifies the whole geometric tail starting at degree3.
The first-order sum vanishes because \(\sum\nu=0\).
This infinite-series bridge is ordinary mathematics, not fixture inference.

At \(r_-\) the new whole tail budget gives \(F\ge8/r-3W/5\).
Low \(F\) therefore implies
\[
 r\ge1-(3\eta+3W/5)/8>r_0=3999/4000;
\]
the endpoint margin \(1-r_0-(3e+3h/5)/8\) is positive.
The \(Q_c\) coefficient \(3/(4r^3)-4/7\) is positive for every
\(r\le r_+\). Retain its sign when using \(Q_c\ge-W\).
Convexity of \(8x^{-1/2}\) at1, (12), and (13) give
\[
 F-8\ge\frac83\eta-\frac43\eta^2+4t^2+\beta W
       -\frac{16}{15}tW-\frac{16}{3}W^2.              \tag{14}
\]
The entire two-variable coefficient identity is
\[
 4t^2-\frac{16}{15}tW-\frac{16}{3}W^2
 =4(t-2W/15)^2-\frac{1216}{225}W^2.
\]
With \(W\le1/375\) this proves (3). Discarding the positive mean square
would give negative coefficient \(\beta-(16/3)(\rho/5+h)\).
After actual entry (2), \(W<1/400\) proves (4) with
\[
 \kappa_{400}-1/600=
 \frac{6069205847327447}{23016648878500095000}>0.
\]
If \(W>0\), the positive variance coefficient makes the basic bound
strict. If \(W=0,t>0\), the square is positive.
If \(W=t=0\), \(p=z^9-a^9,F=8/a\) is strictly above the baseline.
High \(F>8+3\eta\), including infinity, directly implies (1).
Low \(F\) enters the separately established fixed-energy region through
(2), so no circular concentration premise occurs.

## Strengthening and improvement opportunities

**Proved:** \(H<40\eta\) and strict absolute entry \(H<1/400\) on the
entire new band, and the stronger actual low-sublevel coefficient
\(\kappa_{400}>1/600\).
For \(0\le\varepsilon\le1/3\), an actual polynomial satisfying
\[
 F\le8+(8/3)\eta-(4/3)\eta^2+\varepsilon\eta
\]
lies in the low cut, and (4) gives
\[
 \kappa_{400}W+4(t-2W/15)^2\le\varepsilon\eta.
\]
Thus \(W\le600\varepsilon\eta\), strictly for \(\varepsilon>0\), and
\(|t-2W/15|\le\frac12\sqrt{\varepsilon\eta}\).
At \(\varepsilon=0\) the strict basic bound already rules out the
premise. This is basic-slope concentration, not sharp-profile/all-nine
original-root motion stability.

**Open:** optimal widths/constants, the full first-power interior, and
separately completing the wider sharp-C/quadratic/profile/motion estimates.
The necessary next bridge is the complete wider local
mean/variance/range/normal/motion budget with its exact objective cuts.
Active reviewer3's9801 audit concerns its separately stated older
\(2^{-16}\) domain; no verdict or sharp/stability window is transferred.
Formalization of communication, minimizer coverage, actual root labels/
normals, and the entire Legendre argument would reduce the trust boundary.

## 7. Independence, dependencies and primary literature

Written proof/formulas are visible, **not blind**. All new endpoint
budgets,15sectors,8whole39/5faces,both full Newton streams,whole square,
7fresh Gaussian/64ordered Hessians and7fresh two-level moment controls
are rebuilt before target native executable/fixture access in this pass.
Owned polynomial/sector/Gaussian primitives are openly credited:
owned_core.py is byte-identical OWN source25187d5
wider-boundary-audit/core.py; owned_centered.py is OWN9669
audit.py, source785f5208b1bf59c1abe5a9f91e2a9cebad0a7368.
Universal Laurent/cube-field identities retain that credit. Earlier
9669/9776/9824 arithmetic and researcher/helper ancestry are known;
no new blind general algorithm is claimed.

Credits9719 compact multiaffine minimizer,9620 universal actual centered
root/normal/full Legendre mechanism,9687/9731/9776 polar/phase/moment
methods and own9669/9824 prior audit. All required new endpoint
conditions are rebuilt. Sufficient9756/9764 retain their older
sharp/entry domains only.9801 is complementary context, no verdict here.
Gaussian/reciprocal controls are not asserted actual disk-feasible.

Primary literature, live refreshed with candidate-specific searches:
[Zhang Conjecture1.2 versus quadratic Theorem1.3](https://arxiv.org/html/2609.19126)
and [Tao Lemma6/Conjecture19](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/).
No identified external duplicate located; bounded search is not priority
clearance. Classical facts and ordinary Sendov retain their distinct status.
Computational trust: CPython3.12.14 standard-library Fraction/integer.
Universal analytic bridges above remain ordinary unformalized mathematics.
No solver, optimizer, floating grid, incomplete enumeration, timeout,
resource kill, shared signature or matching aggregate establishes
nonexistence, independent authorship, historical priority or a formal proof.
