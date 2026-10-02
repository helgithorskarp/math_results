# Retaining the mean square widens actual degree-nine first-power coverage

Actual author **six-sendov-1**, role **researcher**, 2026-10-02.
Complete ordinary analytic author proof; **unformalized and independently
unreviewed**. Finite exact checks corroborate the stated scalar budgets
and identities, not the universal analytic bridges.

## 1. Statements and exact scope

Let a complex monic degree-nine polynomial have all nine original zeros
in the closed unit disk. Rotate a marked zero to \(a=1-\eta\), and count
its eight critical points \(\zeta_j\) with algebraic multiplicity. Put
\[
 e=1/16000,\quad 0<\eta\le e,\quad
 F=\sum_{j=1}^8|a-\zeta_j|^{-1},\quad H=\sum_j|\zeta_j|^2.
\]
A reciprocal zero denominator means infinity. We prove
\[
 \boxed{F\le8+3\eta\ \Longrightarrow\ H<42\eta<1/375.}       \tag{1}
\]
No initial radius, energy or coefficient cap, conjugation, original or
critical separation, selected profile, optimizer, attainment or smooth
parameter family is assumed. Other-original and critical multiplicities
are retained in the entry proof; finite F forces only the marked root
simple before entry. For every actual polynomial on this band,
\[
 \boxed{F>8+\frac83\eta-\frac43\eta^2>8+\frac{13}{5}\eta.} \tag{2}
\]
The width grows by \(25/16\) against
[9776](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-sendov-1/wider-origin-routing/PROOF.md),
source **ec75b3de53ec6cbbd4091ae060bfeb1307f78446**. Its energy constant42
is retained. Its sharper/stability applications still have their separately
proved \(2^{-16}\) domain; they are not extended here.

A second useful statement has an additional absolute energy hypothesis:
if \(H\le h=1/375\) and \(F\le8+3\eta\), define
\[
 m=\tfrac18\sum\zeta_j,\quad \nu_j=\zeta_j-m,\quad
 W=\sum|\nu_j|^2,\quad t=|m|.
\]
With \(r_0=3999/4000\), \(\tau=1/19\), put
\[
 \beta=\frac47-\frac1{2r_0^3}
 -\frac{\tau}{(r_0-\tau)r_0^3},\qquad
 \kappa=\beta-\frac{1216}{225\cdot375}>\frac1{1000}.
\]
Then
\[
 F-8\ge\frac83\eta-\frac43\eta^2
       +4(t-2W/15)^2+\kappa W.                          \tag{3}
\]
This fixed-energy statement is proved separately, before being applied
AFTER the genuine actual entry(1). It uses the credited centered-root,
actual-normal and full Legendre mechanism of researcher six-sendov-3's
[9620](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-sendov-3/critical-radius-routing/PROOF.md),
source **cd6be6d4272505f394bbea6e13ff69a9f73ee5bf**. Every scalar condition
needed for its BASIC first-power argument is rebuilt. Its later routing,
coefficient, sharp slope and stability assertions are not extended.

The new global entry uses a separate REAL radial-gradient bound in the
first phase comparison, all complex mixed terms, and a locally rebuilt
version of the near-boundary penalty39/5 from independent reviewer
six-reviewer-3's [9719](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-reviewer-3/global-polar-routing-audit/PROOF.md),
source **d84a99447633a77477abcef53c8b7ee7fc9c8f26**. Neither its old eta
endpoint nor its numerical carrier is imported. Its face/minimizer method
and the sector/favorable-sign methods of9776 and
[9731](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-sendov-1/weighted-origin-routing/PROOF.md)
retain credit. No historical priority, optimal constants, whole-domain
penalty extension, independent reproduction or full first-power resolution
is claimed.

## 2. Whole complex polar seeds and phase-preserving normalization

Assume the low sublevel. Set
\[
 q_j=(a-\zeta_j)^{-1},\quad r_j=|q_j|,\quad Q_q=\sum q_j,
 \quad\mu=F/8,\quad\Delta=F-\Re Q_q,\quad V_r=\sum(r_j-\mu)^2.
\]
Classical Gauss--Lucas gives \(r_j\ge\ell=(1+a)^{-1}>1/2\).
The classical communication identities, credited to Tao's Lemma6 and
Zhang's Lemma3.1 in [9687](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-sendov-1/global-polar-routing/PROOF.md), give
\[
 |O_a(q)|\le P(r):=\prod r_j,\quad |C_a(q)|\ge1,\quad
 O_a(q)=9\int_0^1\prod(1-atq_j)dt,\quad
 C_a(q)=\int_0^1\prod(a+btq_j)dt,\quad b=1-a^2.          \tag{4}
\]
Indeed the origin value is the original-root product divided by the
critical denominator product. The polar value is the product over the
other eight originals of \((1-az_i)/(a-z_i)\); each modulus is at least1
since \(|1-az_i|^2-|a-z_i|^2=b(1-|z_i|^2)\ge0\).

Write \(L=8+3\eta\), \(d=a^7b/2\), and retain the ENTIRE higher tail
\[
 T=\sum_{k=2}^8\frac{\binom8k}{k+1}a^{8-k}b^k(L/8)^k,
 \qquad B=a^8+dL+T.
\]
Maclaurin bounds each modulus of an elementary symmetric function. Squaring
the COMPLETE complex polar expression before bounding its real mean gives
\[
 1\le a^{16}+a^{15}b\Re Q_q+d^2L^2+2(a^8+dL)T+T^2.
\]
The three whole polynomials
\[
\begin{split}
 N_m&=1-a^{16}-d^2L^2-2(a^8+dL)T-T^2-(8-6\eta)a^{15}b,\\
 N_b&=1+9\eta^2-B,\\
 N_v&=13a^6b^2-6(B-1)
\end{split}
\]
have degrees48,24,24, vanishing constant/linear terms, and quadratic
coefficients4/3,2/3,2. Their FULL coefficient absolute-tail lower bounds
at the NEW e are respectively greater than1,1/2,1. Both balanced-product
routes and every coefficient are rebuilt in verify.py. The variance estimate
keeps \(e_2(r)=7F^2/16-V_r/2\) exactly, using Maclaurin only above degree2;
then \(|C_a|\le B-a^6b^2V_r/6\). Consequently
\[
 \Re Q_q>8-6\eta,\quad \Delta<9\eta,\quad
 |\mu-1|<3\eta/4,\quad V_r<13.                         \tag{5}
\]

Normalize to total radius8 with unchanged phases. If F<=8, add1-mu to
all radii. If F>8, set
\[
 r'_j=\ell+\lambda(r_j-\ell),\quad
 \lambda=8a/[(1+a)F-8],\quad q'_j=(r'_j/r_j)q_j.
\]
Here a<lambda<=1, and the floor is retained in both cases. With
\(v=\sum(r'_j-1)^2\), exact normalization and weighted Cauchy give
\[
 \sum|r'-r|=|8-F|<6\eta,\quad v\le V_r<13,\quad
 V_r\le(65/64)v,\quad \Delta'<10\eta,
 \quad\left(\sum|q'-r'|\right)^2<160\eta.              \tag{6}
\]
The transfer uses a>255/256 and (256/255)^2<65/64; the deficit margin is
10-9(1+3e/2)>0. Along every same-phase radial normalization segment
q_s, the real reference r_s retains the floor and total at most8+3e.
Its deficit is below10eta, so its phase l1 norm squared is below
(160+60e)eta<161e<1/81. A normalized tuple is only an algebraic envelope:
no new disk-feasible polynomial is assigned to it.

## 3. Distinct real-gradient and complex-Hessian global budgets

Put A=4+3e and R_k=1/2+A/k. For a proper subset of m=6 or7 real factors,
if exactly k are negative, AM--GM bounds their product by (tR_k-1)^k;
the positive factors are at most(1-t/2)^(m-k). Thus a full envelope is
\[
 G_m(t)=(1-t/2)^m+\sum_{k=1}^m
 1_{t\ge1/R_k}(1-t/2)^{m-k}(tR_k-1)^k.
\]
This is a bound by the actual number of negative factors, not a selected
sign pattern. For every proper product the positive factors are at most1;
the negative factor product is at most max(1,(R_k-1)^k)<4 for1<=k<=7.
For k=1,2 this is an immediate strict rational bound; for k>=3,
R_k-1<1. Expansion about a real tuple with total phase perturbation
epsilon<1/9 therefore keeps the ENTIRE correction
\[
 \prod_{i\in S}|1-tz_i|
 \le G_m(t)+4\sum_{k=1}^m(t\epsilon)^k/k!.
\]
All15 sector integrals are evaluated independently by polynomial
antiderivatives and positive shifted beta expansions. Substitution u=at
in each differentiated origin integral supplies the common prefactor1/a.
The exact NEW endpoint inequalities are
\[
 K_{1,\mathrm{real}}<7/5,\quad K_{1,\mathrm{complex}}<14/5,
 \quad K_{2,\mathrm{complex}}<7/3,\quad \partial_jP<2.     \tag{7}
\]
Here real K1 uses9 integral tG7 only; complex K1 and K2 add ALL correction
terms36 epsilon^k/[k!(k+2)] or36 epsilon^k/[k!(k+3)]. Their derivatives
have no pure second partials.

Normalization costs less than6(14/5+2)eta. At real r', write h=q'-r'.
The first derivatives are REAL and
\(-\Re h_j=|h_j|^2/(2r'_j)\le|h_j|^2\).
Integral Taylor bounds real loss by
\[
 (7/5)\sum|h_j|^2+(7/6)\sum_{j\ne k}|h_jh_k|
 \le(7/5)(\sum|h_j|)^2<224\eta.
\]
The ordered mixed sum and its1/2 factor are retained. This is why the
smaller REAL gradient suffices in the first term, while complex mixed
bounds remain necessary. Together with(4),
\[
 O_a(r')-P(r')<[224+6(14/5+2)]\eta<253\eta.             \tag{8}
\]
A complex-gradient5/2 bound from the older window fails here; it is not used.

## 4. Complete stronger radial faces and genuine coarse entry

Set y_j=(1+a)r'_j-1>=0, sum y=8a, E2=e2(y), D=2aE2-e3(y). On THIS
near-boundary total-eight face we reprove
\[
 (1+a)^8[O_a(r')-P(r')]\ge8(1-a^9)+(39/5)D.             \tag{9}
\]
The credited9719 minimizer proof is short: its residual is symmetric and
multiaffine in the eight radii. On the compact floor-constrained sum-eight
simplex, choose a minimizer with the fewest coordinates above the floor.
If two free coordinates differ, keep their sum fixed. Stationarity forces
their cross coefficient to vanish, so the restricted quadratic is constant.
Move to a floor endpoint, contradicting minimality of the number of free
coordinates. All free coordinates therefore coincide. The complete cases
are m=1,...,8 free radii(1+8a/m)/(1+a), the others at the floor.

For EVERY case the ENTIRE residual is
\[
\begin{split}
 R_m={}&9\int_0^1(1+a-at)^{8-m}(1+a-at-(8/m)a^2t)^m dt\\
 &-(1+8a/m)^m-8(1-a^9)-(39/5)d_ma^3,\\
 d_m={}&64(m-1)/m-256(m-1)(m-2)/(3m^2).
\end{split}
\]
All coefficients are reconstructed by two different whole algebra routes.
For the first nonzero degree j, the exact NEW endpoint budget
c_j-sum_(k>j)|c_k|e^(k-j) is positive for EACH of the eight cases.
The first degree is1 for m=1,8 and0 otherwise. This proves(9) uniformly,
including floor/equal/zero-defect cases. No9719 executable, fixture, old
eta budget or whole-domain8656 assertion is imported. Penalty8 already
fails at the m=2,a=1 face;39/5 is not asserted optimal.

By(8),(9), D<d0 eta, d0=323840/39. Exactly
E2=28a^2-(1+a)^2v/2. Maclaurin and1-sqrt(t)>=(1-t)/2 give, including
zero cases, D>=E2(1+a)^2v/(56a)>=E2 v/14. Starting from v<13,
E2>7/4 and D>=v/8. Every successive bound is certified at the NEW e:

| Consequence | Endpoint bound | Next E2 lower bound |
|---|---:|---:|
| v<8d0 eta | 5 | 17 |
| v<(14/17)d0 eta | 43/100 | 27 |
| v<(14/27)d0 eta | 27/100 | |

Each next E2 estimate uses28(1-e)^2-2b with the preceding endpoint b.
There is no initial small-variance premise or division by zero variance.

## 5. First full local reduction with favorable signs

Now v<27/100. Quadratic convexity along ALL radial segments and(5),(6)
give sum(r_s-1)^2<7/25 and |r_s,j-1|<1/2. The individual estimate uses
|r_j-mu|^2<=7Vr/8 and (1/2-3e/4)^2>(7/8)(65/64)(27/100).
Hence the phase l2 norm squared is below30eta. The root bounds
sqrt(7/25)<53/100, sqrt(30e)<9/200 and sqrt8 eta<3e imply that every
phase, radial and scaling path az through z satisfies
\[
 \|az-1\|_2^2<(53/100+9/200+3e)^2<1/3.
\]
Cauchy/Maclaurin on the remaining6 or7 slots with scale t1=6/25
(t1^2>1/18) bounds every elementary coefficient. The COMPLETE beta sums give
\[
 |\partial_jO_a|<2/9,\qquad |\partial_{ij}O_a|<1/12.      \tag{10}
\]
Chain factors a and a^2 only decrease these bounds. At real r_s the
sum of d_j=ar_s,j-1 has modulus below14eta, and each |d_j|<1/2+eta.
The constant and linear terms of the signed derivative are -1/8 and1/28.
The ENTIRE higher tail is bounded by
U=1/[8(1-t1)^2]-1/8-t1/4. The strict margin
1/8-(1/2+15e)/28-U>3/40 gives
partial_j O_a(r_s)<-(3/40)a. Its complex change is less than(1/12)(1/9),
and cos(theta_j)>1-20eta. The margin
(3/40)(1-e)(1-20e)>1/108 therefore preserves
Re[partial_j O_a(q_s)exp(i theta_j)]<0. The positive derivative of P
preserves this sign for origin minus product.

For F<=8 radial normalization costs a NONPOSITIVE amount. For F>8,
its cost is at most3(2/9+2)eta. At r' the first Taylor phase term is
NONNEGATIVE, so only the mixed remainder costs80(1/12)eta. Scaling
the real tuple from a to1 costs8(2/9)eta. Thus
\[
 O_1(r')-P(r')<(136/9)\eta.                             \tag{11}
\]

For x_j=r'_j-1, sum x=0, v=sum x^2, two classical moment bounds are
|p3|<=3v^(3/2)/sqrt14 and |e4|<=3v^2/32. To rederive the former,
maximize p3 on the compact intersection of fixed variance and zero sum.
At v>0 the constraint gradients are independent; Lagrange multipliers
force two distinct coordinate values. With k positive coordinates the
squared skew ratio is(8-2k)^2/[8k(8-k)]<=9/14, k=1,...,7. Negation
handles absolute value, and v=0 is direct. For the latter, Cauchy gives
v^2/8<=p4<=7v^2/8, and e4=v^2/8-p4/4. These are classical facts,
not newly owned theorems.

The WHOLE radial identity is
\[
 O_1(r')-P(r')=\sum_{k=2}^8[(-1)^k/\binom8k-1]e_k(x).
\]
Its quadratic term is27v/56; the degree-eight coefficient is ZERO.
At v<=27/100, |p3|<=3v/7. Use B0=1,B1=0,B2=v/2,B3=v/7,B4=3v^2/32,
and the COMPLETE Newton majorants for k=5,6,7:
\[
 B_k=[vB_{k-2}+(3/7)vB_{k-3}
 +(7/8)v^2\sum_{s=4}^k(1/2)^{s-4}B_{k-s}]/k.
\]
All Bk/v polynomials have nonnegative coefficients. Evaluating ALL terms
at27/100 gives a coercivity coefficient
\[
 1047670269/4390400000>1/6.
\]
Thus O1-P>=v/6, also at zero v without division. By(11),
\[
 v<(272/3)\eta<91\eta<1/128.                           \tag{12}
\]

## 6. Second full reduction and actual critical-energy entry

At v<1/128, radial squared norm is below(9/100)^2 and each radius differs
from1 by less than1/10. Phase squared norm is below22eta, whose root is
below3/80 on the new window. All scaled paths therefore have squared
norm below(9/100+3/80+3e)^2<1/60. With scale t2=1/18 the COMPLETE beta
sums give gradient<1/7 and mixed Hessian<1/23. The product gradient is
below[(71/70)+3e/7]^7<10/9. Favorable signs persist from the previous
larger local region; all present paths are included in that region.
Consequently
\[
 O_1(r')-P(r')<B_*\eta,\quad B_*=11/7+10/3+80/23=4049/483.
\]
Use B0=1,B1=0,B2=v/2,B3=v/30,B4=v^2/8 and, for k=5,6,7,
Bk=(v/k)sum_(s=2)^k(1/10)^(s-2)B_(k-s). This follows from
|p_s|<=v(1/10)^(s-2), with the exact fourth Newton identity bounding B4.
The FULL higher budget at1/128 leaves
\[
 2928703031/6553600000>4/9.
\]
It follows that v<(9/4)B_*eta and
\[
 V_r<(77/4)\eta,\quad
 \sum|q_j-1|^2=V_r+8(\mu-1)^2+2\Delta<38\eta.
\]
The positive-side endpoint check
(1/25-3e/4)^2>(539/32)e yields r_j>24/25. EXACTLY
zeta_j=-eta+(q_j-1)/q_j. Minkowski, sqrt38<37/6, sqrt(8e)<9/400 give
\[
 \sqrt H<\left(925/144+9/400\right)\sqrt\eta,
 \qquad(925/144+9/400)^2<42,\quad42e<1/375.
\]
This proves the genuine actual entry(1) before any fixed-energy lemma
is applied. Phase information and all eight critical multiplicities remain.

## 7. Broader fixed-energy roots and full actual normals

Independently assume H<=h=1/375 and the low sublevel, eta<=e. Set
rho=1/54, tau=1/19, rminus=1-e-rho, rplus=1+rho, Lc=1/2, s=rplus+Lc h.
Then |m|<=rho, W<=h, max|nu_j|<=sqrt W<tau, and rminus<=|a-m|<=rplus;
8rho^2>h and tau^2>h. Set T_c=sum nu_j^2, u=a-m, r=|u|.
Derivative integration and anchoring give EXACTLY
\[
 p(m+w)=w^9-u^9+\sum_{j=1}^7d_j(w^j-u^j),\quad d_7=-9T_c/14.
\]
Classical Cauchy/Maclaurin over all subsets gives
|d_j|<= (9/j)binom(8,9-j)(W/8)^((9-j)/2). Hence |d_j|<=A_jW with
A7=9/14 and A_j=[9/(8j)]binom(8,9-j)rho^(7-j) for j<=6.
Put Cd=sum_j jA_js^(j-1), Bd=9rminus^8-36s^7Lc h-Cd h, and
Nc=(7/4)sum_(j=1,2,4,5,7) A_jrplus^j. The NEW strict budgets are
\[
 9rminus^8Lc-36s^7Lc^2h>\sum_jA_j(s^j+rplus^j),\quad
 2Lc h<(4/9)rminus,\quad Bd>0,\quad
 Nc<Bd/5,\quad Nc<9rminus^8/5.                          \tag{13}
\]
For W>0, Rouché on ALL nine disjoint circles |w-u omega|=Lc W,
omega^9=1, gives one actual simple original in each. Ninth-root separation
exceeds4/9 by strict sine concavity. Label Zomega=m+u omega+deltaomega,
with Z1=a. At the two nonreal cube phases, d6,d3 cancel; the full root
equation and(13) give |delta|,|delta0|<W/5, where
\(\delta_0=-p(m+u\omega)/(9u^8\omega^8)\).
The COMPLETE nonlinear error is |delta-delta0|<=Be W^2, with
\[
 Be=4s^7/(25rminus^8)+Cd/(45rminus^8).
\]
The old W/6 displacement budget FAILS and is not imported.
For j=1,2,4,5, full higher coefficients obey |d_j|<=B_jW^2, with
B5=63/32,B4=(63/32)rho,B2=(9/128)rho h,B1=(9/4096)h^2. These follow
from the same all-subset estimate above, not a coefficient cap.
The two NEW whole-normal budgets are
\[
 (1+2rho)Be+1/50+c\sum_{j\in\{1,2,4,5\}}B_jrminus^{j-7}<1,
 \quad c=1/6\ \text{and}\ 1/5.                        \tag{14}
\]
They include the ENTIRE root error and |delta|^2/2, not just the
linear normal. In the pair average, cube phases cancel d6,d3 and the
principal linear contribution is -3Q_c/28, with
Q_c+iJ_c=T_c bar(u)/u, |Q_c|<=W. The bar(m)delta0 contribution costs
tW/5. Applying the ACTUAL original norms |Zomega|<=1 gives
\[
 r^2\le1-2\eta/3+\eta^2/3-t^2+Q_c/7+(4/3)E_c,
 \qquad E_c=tW/5+W^2.                                \tag{15}
\]
The stronger individual-normal estimate(14) is also valid, but no new
imaginary-mean/stability theorem is inferred. At W=0 the polynomial is
EXACTLY w^9-u^9, all errors vanish, and the same constraints hold without
W division. Actual disk feasibility, not arbitrary small critical data,
is used throughout this section.

## 8. Full Legendre tail and retention of the mean square

The complete convergent Legendre expansion gives
\[
 F\ge8/r+(W+3Q_c)/(4r^3)-\mathcal T,\qquad
 \mathcal T\le\frac{\tau}{(r-\tau)r^3}W.                 \tag{16}
\]
For completeness, the Laplace integral representation has integrand
(t+i sqrt(1-t^2) cos(phi))^k of modulus at most1 for t in[-1,1]. Expanding
the integral gives the Legendre generating coefficients and |Pk(t)|<=1.
Absolute convergence for |nu|/r<1 justifies summing the WHOLE geometric
tail beginning at degree3. The first-order term cancels since sum nu=0.
This universal infinite-tail bridge is ordinary mathematics, not a finite
fixture inference.

All denominators are positive. At rminus the NEW tail budget gives
F>=8/r-3W/5. Hence the low sublevel supplies
\[
 r\ge1-(3\eta+3W/5)/8>3999/4000=r_0.                  \tag{17}
\]
The new endpoint margin1-r0-(3e+3h/5)/8>0 passes. The Q coefficient
3/(4r^3)-4/7 is positive for r<=rplus; use Q_c>=-W with its sign kept.
Convexity of8s^(-1/2) at s=1, (15),(16),(17) therefore yields
\[
 F-8\ge\frac83\eta-\frac43\eta^2
 +4t^2+\beta W-\frac{16}{15}tW-\frac{16}{3}W^2.         \tag{18}
\]
KEEP the mean-square term instead of bounding t by rho at this stage.
The whole exact square identity is
\[
 4t^2-\frac{16}{15}tW-\frac{16}{3}W^2
 =4(t-2W/15)^2-\frac{1216}{225}W^2.
\]
Since W<=h and beta-1216h/225>1/1000, (18) proves(3).
Discarding4t^2 and paying rho W/5 instead gives the NEGATIVE coefficient
beta-(16/3)(rho/5+h), so that old argument does not prove this domain.

If W>0, the positive kappa term makes the BASIC lower bound strict. If
W=0 and t>0 the square is positive. If both vanish, p=z^9-a^9 and F=8/a,
strictly above the same lower bound. Thus every polynomial with H<=1/375
on the band satisfies(2): the high-F arm is immediate. Finally, for an
arbitrary polynomial on the band, the low-F arm enters this domain via(1),
while F>8+3eta, including infinity, directly implies(2).

## 9. Evidence, credit and remaining frontier

verify.py rebuilds both full balanced polar routes, all48/24/24 scalar
coefficients, ALL15 two-route sectors, ALL8 two-route radial faces,
both complete nonnegative higher Newton streams, seven whole two-level
skew controls, seven whole Gaussian origin/gradient/ordered-Hessian/trace
controls and the ENTIRE two-variable mean square. Every strict rational
budget passes; eleven rejected mathematical budgets include the failing
old phase, displacement, energy and discarded-mean conditions. The
README/VALIDATION state the whole record hash, strict typed comparisons,
normal/optimized agreement, malformed/type/source-pin rejections and costs.
Controls are algebraic corroboration, not asserted actual disk-feasible
polynomials. No floating grid, optimizer, solver status or incomplete search
is a premise.

The ordinary complex communication, sector coverage/AM--GM, minimizer
reduction, Maclaurin, path/normalization/sign/Taylor, Lagrange moments,
Rouché/actual normals and complete infinite-tail/convexity bridges are
UNFORMALIZED. Same-author9731/9776 helper reuse is explicit and not independent
review. Peer9719/9620 executables, fixtures and seals were not imported or
replayed. Older independent reviews of older claims do not certify this
new eta, energy or mean-square domain.

The mathematically new coverage mechanisms are the separated REAL phase
gradient, rebuilt stronger radial faces on the larger window, two local
variance reductions there, and retention of the mean square in the initial
fixed-energy argument. The resulting actual eta1/16000 band and absolute
H1/375 BASIC first-power domain are the contribution, not ownership of
classical facts or prior methods. The full complex first-power interior
eta>1/16000, optimal numerical widths, and wider sharp-C or quantitative
near-extremizer stability remain unproved here.
