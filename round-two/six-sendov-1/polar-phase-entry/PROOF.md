# Squared-polar phase control widens actual degree-nine entry

Actual author **six-sendov-1**, role **researcher**, 2026-10-03.
Complete ordinary analytic author proof, **unformalized and independently
unreviewed**. The exact checker verifies all finite coefficients and
receiving budgets stated below; the universal analytic arguments remain
ordinary written mathematics.

## 1. Actual statements and dependencies

Let a complex monic degree-nine polynomial have all nine original zeros
in the **closed** unit disk. Rotate a marked original to \(a=1-\eta\),
count the eight critical points \(\zeta_j\) with algebraic multiplicity,
and put
\[
 e=1/12000,\quad 0<\eta\le e,\qquad
 F=\sum_{j=1}^8|a-\zeta_j|^{-1},\qquad H=\sum_j|\zeta_j|^2.
\]
A zero reciprocal denominator means infinity. We prove
\[
 \boxed{F\le8+3\eta\ \Longrightarrow\ H<37\eta<1/320.}       \tag{1}
\]
There is no initial critical radius, energy or coefficient hypothesis,
conjugation, separation, selected profile, optimizer, attainment, smooth
family or critical-branch matching assumption. Finite F forces only the
marked original simple before entry. All other multiplicities persist
until an actual-root argument proves simplicity in its receiving domain.
For **every** actual polynomial on the band,
\[
 \boxed{F>8+\frac83\eta-\frac43\eta^2>8+\frac{13}{5}\eta.}    \tag{2}
\]
Multiplying by a nonzero leading coefficient changes neither statement.

Separately, assume \(H\le h=1/320\), the same eta band and the low cut.
Define
\[
 m=\tfrac18\sum\zeta_j,\quad t=|m|,\quad
 \nu_j=\zeta_j-m,\quad W=\sum|\nu_j|^2,
\]
\[
 r_0=9997/10000,\quad \tau=21/400,\quad
 \beta_c=\frac47-\frac1{2r_0^3}-\frac{\tau}{(r_0-\tau)r_0^3},
\]
\[
 \kappa=\beta_c-\frac{976}{225\cdot320}
 =\frac{2266385261714573}{1164451364653531500}>\frac1{600}.
\]
We prove the retained-square statement
\[
 \boxed{F-8\ge\frac83\eta-\frac43\eta^2
        +4(t-2W/15)^2+\kappa W.}                         \tag{3}
\]
This statement is proved under its separate fixed-energy hypothesis and
applied to arbitrary low-F polynomials **only after** the genuine entry(1).

The mathematical input used without extending its hypotheses is the
standalone derivative class in own
[9868](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/signed-origin-derivatives/PROOF.md),
source **aba6276ac4691eaf2cc267cc367717bab9de788c**:
for \(O_a(z)=9\int_0^1\prod(1-at z_j)dt\), every real base with
\(99/100\le a\le1\), \(r_j\ge1/2\), \(\sum r_j\le803/100\)
has \(|\partial_jO_a(r)|<9/16\); all complex perturbations of l1 norm
at most1/8 have gradient<2/3 and distinct mixed Hessian<3/4 throughout
intermediate segments. Its real phase loss is
\[
 O_a(r)-\Re O_a(q)\le(9/16)\Delta+(3/8)\epsilon^2,
 \quad\Delta=\sum r_j(1-\cos\theta_j),\quad
 \epsilon=\sum|q_j-r_j|.                                \tag{4}
\]
The full standalone class, including its analytic extremum proof and
complete tensor certificate, was independently **CONFIRMED** by
[9892](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/signed-derivative-audit/PROOF.md),
actual six-reviewer-3, source **a8ff9d4212667938d86ac13fa53a47516a8619d5**.
Its independent 69-eta actual comparison is on **eta<=1/16000**. We do
not import that numerical comparison or its old normalization constants.
Its universal off-diagonal7/8 improvement is credited but not needed for
the constants below. That review gives no verdict on this new entry leaf.

The communication, normalization, face-penalty and two-reduction method
credits own
[9818](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/mean-square-routing/PROOF.md),
source **b1df3a9250928ccf97593e3a55c2084a2bb4712e**, now independently
confirmed on its entire1/16000 band by
[9863](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/mean-square-audit/REVIEW.md),
six-reviewer-1, source **74977ee1d8f56f99f90fdd37e130160143310a8b**.
Its H40/H1/400 refinement and favorable retention of the full local gap
are credited context; those numerical hypotheses are not entry inputs.
The complete actual-root/paired-normal mechanism credits researcher
six-sendov-3's
[9857](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/wider-quadratic-stability/PROOF.md),
source **7b1b1f0b36c3a729d190f61b85d587eb4699d187**. Every numerical
root, nonlinear-normal, Legendre and retained-square budget needed here is
rebuilt; no old numerical domain is relabeled. The now committed independent
[9908 full assessment](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/wider-quadratic-audit/REVIEW.md),
actual six-reviewer-1, source **67a94723ed641ae7d0bc7f756948772e4890d6da**,
CONFIRMS the entire9857 theorem and improves its separate costs to238/268
on the SAME1/16000 band. That assessment gives no verdict on this leaf or
on the newer9894 result. Its newer
[9894](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/coupled-cubic-coercivity/PROOF.md),
source **79b0979dc2ac27d4ce64c3962f3d9c62180d3060**, has the separate
230 objective / **247 physical** result retaining E/4 and BOTH cuts on
eta<=1/16000. Neither those sharp/stability conclusions nor an independent
verdict are extended here. The new eta width is4/3 of9818/9863's band,
and H37 improves their H42/H40 entry bounds, with all receiving hypotheses
proved below. This is partial first-power progress, not a full endpoint,
optimal width/constant or historical priority claim.

## 2. Complete squared-polar estimate with a retained phase margin

Work first under the low cut. Set
\[
 q_j=(a-\zeta_j)^{-1},\quad r_j=|q_j|,\quad Q_q=\sum q_j,
 \quad\mu=F/8,\quad\Delta=F-\Re Q_q,\quad
 V_r=\sum(r_j-\mu)^2,\quad \ell=(1+a)^{-1}.
\]
Gauss--Lucas gives \(r_j\ge\ell>1/2\). The classical origin and polar
communication identities of Tao Lemma6 and Zhang Lemma3.1 give
\[
 |O_a(q)|\le P(r):=\prod r_j,\qquad
 |C_a(q)|\ge1,\quad C_a(q)=\int_0^1\prod(a+btq_j)dt,
 \quad b=1-a^2.                                        \tag{5}
\]
The origin value is the product of the other original zeros divided by
the critical denominator product. The polar value is
\(\prod_{i=1}^8(1-az_i)/(a-z_i)\). Each polar factor has modulus
at least1 because
\(|1-az_i|^2-|a-z_i|^2=b(1-|z_i|^2)\ge0\).
These are exact identities independent of any quadratic second-moment cap.

Put \(L=8+3\eta\), \(d=a^7b/2\), \(\sigma=11/2\), and retain
**every** higher term
\[
 T=\sum_{k=2}^8\frac{\binom8k}{k+1}a^{8-k}b^k(L/8)^k,
 \qquad B=a^8+dL+T.
\]
Maclaurin bounds \(|e_k(q)|\le e_k(r)\le\binom8k(F/8)^k\).
Writing the full polar expression as \(a^8+dQ_q+R\), \(|R|\le T\),
and squaring before discarding its real mean gives
\[
 1\le a^{16}+a^{15}b\Re Q_q+d^2L^2+2(a^8+dL)T+T^2.       \tag{6}
\]
The entire degree48 polynomial
\[
 N_\sigma=1-a^{16}-d^2L^2-2(a^8+dL)T-T^2
                  -(8-\sigma\eta)a^{15}b
             =1-B^2+(3+\sigma)\eta a^{15}b              \tag{7}
\]
has zero constant and linear coefficients and quadratic coefficient1/3.
Both whole routes agree in **all** coefficients. At e its quadratic
coefficient minus the complete absolute higher tail is positive. The
same reconstruction of the degree24 polynomials
\[
 N_b=1+9\eta^2-B,\qquad N_v=13a^6b^2-6(B-1)
\]
has heads2/3 and2, and complete tail lower bounds greater than1/2 and1,
respectively. For any polynomial \(N=\eta^j(c_j+\sum_{k>j}c_k\eta^{k-j})\)
these inequalities give strict positivity for **all**0<eta<=e, rather than
only at a tested point. All99 coefficients of these three streams and both
complete balanced-product constructions are in EXPECTED.json.

The quadratic coefficient in \(C_a\) is retained exactly:
\(e_2(r)=7F^2/16-V_r/2\). Bounding only higher degrees gives
\(|C_a|\le B-a^6b^2V_r/6\). Since \(a,b>0\), (5)--(7) imply
\[
 \Re Q_q>8-\sigma\eta,\quad \Delta<(17/2)\eta,
 \quad |\mu-1|<(11/16)\eta,\quad V_r<13.                \tag{8}
\]
No initially small critical data occurs in this argument.

## 3. All phase-preserving paths and the new global comparison

Normalize the real radii to total8 without altering phases.
For F<=8 add \(\delta=1-\mu\) to every radius. For F>8 put
\[
 r'_j=\ell+\lambda(r_j-\ell),\qquad
 \lambda=\frac{8a}{(1+a)F-8},\qquad q'_j=(r'_j/r_j)q_j.   \tag{9}
\]
The second denominator is positive; \(a<\lambda<1\) since
\(3(1+a)<8\). Both arms retain the floor; at F=8 the addition is zero.
With \(v=\sum(r'_j-1)^2\), the exact variance identities give
\[
 v=V_r\quad(F\le8),\qquad v=\lambda^2V_r\quad(F>8),
 \quad v\le V_r<13,\quad V_r\le(65/64)v.                \tag{10}
\]
Here a>255/256 and (256/255)^2<65/64. The normalization distance is
\(\sum|r'-r|=|8-F|<\sigma\eta\).

Write \(\beta=17/2\),
\[
 \beta'=\beta(1+\sigma e/4)=1632187/192000,
 \qquad S'=16\beta'=1632187/12000.
\]
In the addition arm, \(\delta<(\sigma/8)\eta\), hence
\(\Delta'\le(1+\delta/\ell)\Delta<(1+\sigma e/4)\beta\eta\).
In the shrinking arm \(r'\le r\), so \(\Delta'\le\Delta<\beta\eta\).
Every same-phase radial segment \(r_s e^{i\theta}\) has deficit
\(\Delta_s<\beta'\eta\), floor \(\ell\), and total at most8+3eta.
Weighted Cauchy proves, on **every** such segment,
\[
 \epsilon_s^2:=\Big(\sum|r_{s,j}(e^{i\theta_j}-1)|\Big)^2
 \le2\Big(\sum r_{s,j}\Big)\Delta_s
 <2(8+3e)\beta'\eta<1/64.                             \tag{11}
\]
For the normalized tuple specifically, \(\epsilon'^2<S'\eta\).
The real total is below803/100 and a>99/100. Thus (4), the entire
complex derivative bounds and **all intermediate points** apply before
any small-variance premise. By AM--GM every real product gradient is
less than \(G=(753/700)^7<2\). Starting from the ORIGINAL communication
inequality, the same-phase normalization costs at most
\(\sigma(2/3+2)\eta\), and (4) then yields
\[
 O_a(r')-P(r')<C_0\eta,\quad
 C_0=(9/16)\beta'+(3/8)S'+\sigma(2/3+2)
     =43287127/614400<71.                              \tag{12}
\]
This is the newly proved receiving-band budget. It is not described as
an improvement over9892's **69** on the smaller band. The normalized
complex tuple is an algebraic envelope, not a new disk-feasible polynomial.

## 4. All eight stronger real faces and genuine coarse entry

Let \(y_j=(1+a)r'_j-1\ge0\), \(\sum y=8a\),
\(E_2=e_2(y)\), \(D=2aE_2-e_3(y)\). We locally reprove on THIS band
\[
 (1+a)^8[O_a(r')-P(r')]
       \ge8(1-a^9)+(39/5)D.                            \tag{13}
\]
Credit independent reviewer six-reviewer-3's
[9719 minimizing-face argument](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/global-polar-routing-audit/PROOF.md),
source **d84a99447633a77477abcef53c8b7ee7fc9c8f26**.
The residual is symmetric and multiaffine in the eight real radii.
On the compact floor-constrained sum-eight simplex take a minimizer with
the fewest coordinates above the floor. For two unequal free coordinates
x,y, the restriction at fixed sum is Axy+B(x+y)+C. Interior stationarity
forces A(y-x)=0, so A=0. Moving along that constant interval to a floor
endpoint contradicts the minimal free count. Hence all free radii coincide.
All8 possible nonempty free sets are represented by m=1,...,8; all-floor
is impossible for a>0 and total8. Equal-free and zero cross-coefficient
cases are included, not excluded stationary degeneracies.

For each m the ENTIRE polynomial residual is
\[
 R_m=9\int_0^1(1+a-at)^{8-m}(1+a-at-(8/m)a^2t)^m dt
       -(1+8a/m)^m-8(1-a^9)-(39/5)d_ma^3,
\]
\[
 d_m=64(m-1)/m-256(m-1)(m-2)/(3m^2).
\]
Direct multiplication/integration and the complete binomial route agree
in all coefficients. Each leading coefficient minus its entire absolute
higher tail at the **new e** is strictly positive, proving(13) uniformly,
including zero-defect cases. No old fixture, verdict, numerical endpoint
or whole-domain radial penalty is imported.

Exactly \(E_2=28a^2-(1+a)^2v/2\). Maclaurin with
\(u=E_2/(28a^2)\in[0,1]\) gives
\(e_3(y)\le56a^3u^{3/2}\). Since1-sqrt(u)>=(1-u)/2,
\[
 D\ge E_2(1+a)^2v/(56a)\ge E_2v/14.                    \tag{14}
\]
This includes all zero cases without dividing by variance. By(12),(13),
\(D<d_0\eta\), \(d_0=256\cdot71/(39/5)=90880/39\).
Start with v<13, so \(E_2>28(1-e)^2-26>7/4\).
The full coarse implications, with each positive divisor established first,
are
\[
 v<8d_0\eta<8/5,\quad E_2>28(1-e)^2-16/5>99/4,
\]
\[
 v<(56/99)d_0\eta<11/100,\quad
 E_2>28(1-e)^2-22/100>111/4,
\]
\[
 \boxed{v<(56/111)d_0\eta<1/10.}                       \tag{15}
\]
For v=0 every implication is direct. This is genuine entry into the
first small region, rather than an assumed local critical configuration.

## 5. Whole first local balls, signed gradients and Newton gap

Write \(\mu_c=11/16\). Variance convexity on every real radial segment,
(8),(10), and zero sum imply
\[
 \sum(r_s-1)^2\le(65/64)v+8\mu_c^2\eta^2,
 \quad |r_{s,j}-1|\le\sqrt{(7/8)(65/64)v}+\mu_c\eta.      \tag{16}
\]
The individual estimate follows by Cauchy on the other seven centered
coordinates, valid for arbitrary collisions. With v<1/10, ALL receiving
rational budgets give
\[
 \|r_s-1\|_2<8/25,\quad |r_{s,j}-1|<3/10,
 \quad\|r_s\|_2<3.
\]
The phase l2 norm squared is at most \(2\max r_s\Delta_s\), and hence
its root is below9/200 on this band. By the triangle inequality EVERY
phase, radial and scaling path needed below, with factor c between a and1,
has
\[
 \|cz-1\|_2^2<(8/25+9/200+3e)^2<4/25.                 \tag{17}
\]
Linear phase segments are included by norm convexity. The same estimate
covers the two-arm radial normalization; no tuple is declared disk feasible.

For D=cz-1, Cauchy/Maclaurin bounds each elementary coefficient on the
remaining6 or7 coordinates by \(\binom mk t_1^k\), \(t_1=1/6\), because
\(t_1^2>(4/25)/6\). Complete beta integrals, including **all** remaining
orders, give
\[
 g_1=1/5>\sum_{k=0}^7(k+1)t_1^k/8,
 \quad h_1=1/16>\sum_{k=0}^6(k+1)(k+2)t_1^k/56.          \tag{18}
\]
These bound every gradient and distinct mixed Hessian; repeated-coordinate
second derivatives vanish. They also bound the unscaled origin polynomial
on the corresponding scaled paths; chain factors c and c^2 only decrease
coordinate derivative bounds.

At a real path the signed unscaled gradient has constant -1/8 and linear
term \(\sum_{i\ne j}(ar_{s,i}-1)/28\). The sum of all scaled deviations
has modulus below(8+sigma)eta, and removing one costs at most3/10+eta.
Thus the remaining sum has modulus below3/10+15eta. The ENTIRE higher
geometric majorant is
\[
 U(t_1)=1/[8(1-t_1)^2]-1/8-t_1/4.
\]
The strict receiving margin
\(1/8-(3/10+15e)/28-U(t_1)>1/10\)
proves \(\partial_jO_a(r_s)<-a/10\).
Also \(\cos\theta_j\ge1-\Delta_s/r_{s,j}>1-18\eta\).
The full complex gradient change is at most h1 epsilon_s, and
\[
 (1-e)(1-18e)/10>h_1/8.
\]
Therefore \(\Re[\partial_jO_a(q_s)e^{i\theta_j}]<0\)
on EVERY normalization segment. The product derivative is positive.

For F<=8 normalization thus has NONPOSITIVE cost for Re O minus P.
For F>8 its mass is F-8<=3eta and cost at most3(g1+2)eta.
At r' the first phase Taylor term is NONNEGATIVE for Re O(q')-O(r'),
so the full mixed remainder alone bounds loss by h1 epsilon'^2/2.
Scaling the normalized REAL tuple from a to1 costs8g1 eta, because
sum r'=8. Consequently
\[
 O_1(r')-P(r')<K_1\eta,\qquad
 K_1=11g_1+6+(S'/2)h_1=4780987/384000.                  \tag{19}
\]
No favorable global sign was used before the genuine small region(15).

For x_j=r'_j-1, sum x=0, v=sum x^2, let p_s=sum x_j^s and e_k=e_k(x).
Classical compact Lagrange multipliers show
\(|p_3|\le3v^{3/2}/\sqrt{14}\): at positive fixed v the independent
sum/variance constraint gradients force two coordinate values. At each
of the seven possible levels k, the squared skew ratio is
\((8-2k)^2/[8k(8-k)]\le9/14\). Negation covers the minimum; v=0 is direct.
The checker reconstructs every full two-level tuple, not just the maximum.
Cauchy and8x_j^2<=7v give
\(v^2/8\le p_4\le7v^2/8\); Newton's exact identity
\(e_4=v^2/8-p_4/4\) gives \(|e_4|\le3v^2/32\).
At v<=1/10, \(|p_3|<3v/11\). All these are credited classical facts.

The WHOLE exact radial identity is
\[
 O_1(r')-P(r')=\sum_{k=2}^8
             [(-1)^k/\binom8k-1]e_k(x).               \tag{20}
\]
Its quadratic term is27v/56 and its degree-eight coefficient is ZERO.
Define complete nonnegative majorant polynomials
\[
 B_0(v)=1,\ B_1(v)=0,\ B_2(v)=v/2,\ B_3(v)=v/11,
 \quad B_4(v)=3v^2/32,
\]
\[
 B_k(v)=\frac1k\left[vB_{k-2}+(3/11)vB_{k-3}
 +(7/8)v^2\sum_{s=4}^k(3/10)^{s-4}B_{k-s}\right]
 \quad(k=5,6,7).                                      \tag{21}
\]
Newton identities, the full fourth moment bound and
\(|p_s|\le(7/8)v^2(3/10)^{s-4}\) for s>=4 prove \(|e_k|\le B_k(v)\).
Every Bk/v has nonnegative coefficients. Therefore evaluating the ENTIRE
higher correction in(20) at v0=1/10 leaves the uniform full gap
\[
 c_1=\frac{14208849}{38720000}>0,\qquad
 O_1(r')-P(r')\ge c_1v.
\]
The exact margin **34c1-K1>0** proves
\[
 \boxed{v<34\eta<1/350.}                               \tag{22}
\]
The target33eta has NEGATIVE margin and is not used. No division by v
is made at zero. The entire Newton streams, not a selected high-degree
sample or an aggregate tail count, are retained.

## 6. Separate path radius, second whole gap and actual energy

The normalized moment bound and the radius along all actual normalization
paths are DISTINCT. From(22), zero sum gives
\(|x_j|^2\le7v/8<(7/8)(1/350)=(1/20)^2\).
Thus use \(\rho_x=1/20\) for normalized moments. Formula(16), with the
**actual** v<34eta, gives instead \(\rho_{\rm path}=51/1000\) for every
radial path coordinate. Substituting rho_x into that latter condition
would fail at this receiving endpoint; it is not done.

The complete receiving inequalities now give
\[
 \|r_s-1\|_2<11/200,\quad |r_{s,j}-1|<51/1000,
 \quad\|q_s-r_s\|_2<1/25,
\]
\[
 \|cz-1\|_2^2<(11/200+1/25+3e)^2<1/100.
\]
With t2=1/24, its square exceeds(1/100)/6. The complete gradient/Hessian
sums in(18) at t2 are below
\(g_2=1/7\), \(h_2=1/24\).
AM--GM on all seven remaining positive radii gives
\[
 \partial_jP(r_s)\le[(7+51/1000+3e)/7]^7<16/15=p_g.
\]
All these paths are inside the earlier signed region, so BOTH favorable
sign implications persist. Repeating the full argument of(19) gives
\[
 O_1(r')-P(r')<K_2\eta,\quad
 K_2=11g_2+3p_g+(S'/2)h_2=30663709/4032000.              \tag{23}
\]

Use the complete SECOND Newton stream
\[
 \widetilde B_0=1,\ \widetilde B_1=0,\ \widetilde B_2=v/2,
 \quad\widetilde B_3=\rho_xv/3,\quad
 \widetilde B_4=3v^2/32,
\]
\[
 \widetilde B_k(v)=\frac vk\sum_{s=2}^k
                       \rho_x^{s-2}\widetilde B_{k-s}(v)
 \quad(k=5,6,7).                                      \tag{24}
\]
Here \(|p_s|\le v\rho_x^{s-2}\) for all relevant s, and the stronger
fourth Newton identity is separately retained. Whole nonnegative coefficient
polynomials evaluated at1/350 leave
\[
 c_2=\frac{20409329741}{43904000000}>0,\quad
 v<A_v\eta,\quad A_v=\frac{3005043482000}{183683967669},
\]
\[
 V_r<A_r\eta,\quad A_r=(65/64)A_v
       =\frac{12207989145625}{734735870676}.             \tag{25}
\]
The closed equality7v2/8=rho_x^2 is handled correctly: actual v is
STRICTLY below34eta<=34e<1/350, so the actual normalized radius is strict.

Exact norm decomposition and(8) now give
\[
 \sum|q_j-1|^2=V_r+8(\mu-1)^2+2\Delta<34\eta.
\]
The positive-side squared endpoint margin
\[
 (1/28-\mu_ce)^2>(7/8)A_re
\]
gives every ACTUAL reciprocal radius r_j>27/28. Exactly
\(\zeta_j=-\eta+(q_j-1)/q_j\). Minkowski, sqrt34<35/6 and
sqrt(8e)<13/500 yield
\[
 \sqrt H<\left(490/81+13/500\right)\sqrt\eta,
 \quad (490/81+13/500)^2<37,\quad37e<1/320.
\]
This proves genuine entry(1), still with all8 critical multiplicities,
BEFORE any receiving fixed-energy root/normal/Legendre assertion.

## 7. Receiving all-nine original-root and whole paired-normal budgets

Independently assume H<=h=1/320 and low F on eta<=e. Let
\[
 \rho=1/50,\quad \tau=21/400,\quad L_c=1/2,
 \quad r_-=1-e-\rho,\quad r_+=1+\rho,\quad s=r_++L_ch.
\]
Since H=W+8t^2, t<=sqrt(h/8)<rho. Cauchy on the other seven centered
criticals gives8|nu_j|^2<=7W, hence max|nu|<tau because tau^2>7h/8.
Set u=a-m, r=|u| and T_c=sum nu_j^2. Initially r_-<=r<=r_+.
Derivative integration and anchoring at p(a)=0 give EXACTLY
\[
 p(m+w)=w^9-u^9+\sum_{j=1}^7d_j(w^j-u^j),
 \quad d_7=-9T_c/14,\quad d_6=-\tfrac12\sum\nu_j^3.      \tag{26}
\]
The exact degree-seven identity gives |d7|<=9W/14. For j=1,...,6,
all-subset Cauchy followed by nonnegative Maclaurin gives
\[
 |d_j|\le\frac9j\binom8{9-j}(W/8)^{(9-j)/2}\le A_jW,
\]
\[
 A_7=9/14,\quad
 A_j=\frac9{8j}\binom8{9-j}\rho^{7-j}\quad(j=1,...,6).
\]
Indeed (W/8)^(1/2)<=rho; this involves all coefficient subsets, arbitrary
complex phases and critical collisions. Define
\[
 C_d=\sum_{j=1}^7jA_js^{j-1},\quad
 B_d=9r_-^8-36s^7L_ch-C_dh,
\]
\[
 N_c=(7/4)\sum_{j\in\{1,2,4,5,7\}}A_jr_+^j.
\]
EVERY receiving inequality is strictly verified:
\[
 9r_-^8L_c-36s^7L_c^2h>\sum A_j(s^j+r_+^j),\quad
 2L_ch<(4/9)r_-,\quad B_d>0,
 \quad N_c<B_d/5,\quad N_c<9r_-^8/5.                    \tag{27}
\]
For W>0, on each of ALL9 circles |w-u omega|=Lc W, omega^9=1,
the principal polynomial is at least9r^8Lc W-36s^7Lc^2 W^2.
The ENTIRE lower polynomial is at mostW sum Aj(s^j+rplus^j).
Ninth-root separation exceeds4/9: strict concavity of sine on[0,pi/2]
gives2sin(pi/9)>4/9. Thus the circles are disjoint. Rouché gives exactly
one original counted with multiplicity in each, hence actual simplicity
and labels \(Z_\omega=m+u\omega+\delta_\omega\); Z1=a.

At the two nonreal cube phases d6,d3 cancel AT the base point. The
whole root equation, its full derivative correction Cd W, and(27) give
\[
 |\delta|,|\delta_0|<W/5,\qquad
 \delta_0=-p(m+u\omega)/(9u^8\omega^8),
\]
\[
 |\delta-\delta_0|\le B_eW^2,\quad
 B_e=4s^7/(25r_-^8)+C_d/(45r_-^8).                     \tag{28}
\]
For the first displacement the numerator is at mostNc W because
|omega^j-1|<=sqrt3<7/4, and the divisor is at leastBd.
The two terms in Be bound the COMPLETE principal Taylor remainder
36s^7 delta^2 and all lower-polynomial displacement terms. In particular,
d3,d6 still enter Cd; their base cancellation never deletes nonlinear drift.

For ALL remaining j=1,2,4,5, the full subset bound implies
\[
 |d_j|\le B_jW^2,\quad B_5=63/32,\ B_4=(63/32)\rho,
 \quad B_2=(9/128)\rho h,\quad B_1=(9/4096)h^2.
\]
Let
\[
 b_p=(1+2\rho)B_e+1/50+(1/6)\sum B_jr_-^{j-7}<4/5,
\]
\[
 b_i=(1+2\rho)B_e+1/50+(1/5)\sum B_jr_-^{j-7}<7/8.      \tag{29}
\]
These fresh full budgets are respectively about.774018 and.843756
(the decimals are display only). For clarity the universal paired-normal
bridge follows. Expand the ACTUAL half-normal
(|Zomega|^2-1)/2. Its error beyond the main d7 linear term is bounded by
bar(m)delta0 (cost tW/5), the full nonlinear term (cost(1+2rho)Be W^2),
|delta|^2/2 (cost W^2/50), and EVERY higher linear coefficient.
Multiplying delta0's j term by bar(u omega) gives
\(-d_j u^{j-8}\bar u(\omega^j-1)/9\).
The pair average of its cube coefficient is1/6 for j not divisible by3,
and zero for j=3,6. The individual norm is sqrt3/9<1/5.
Both facts are exact identities in Q[omega]/(omega^2+omega+1); the
checker retains all7 coefficient pairs, including the zeros, and the
principal d7 pair coefficient **-3/28**. Therefore for
\(Q_c+iJ_c=T_c\bar u/u\), |Qc|<=W, the averaged actual cube normal is
\[
 P_c=-\eta+\eta^2/2-(3a/2)\Re m+(3/2)t^2-3Q_c/28,
 \quad P_c\le E_c=tW/5+(4/5)W^2.                      \tag{30}
\]
This uses the ACTUAL original-disk inequalities |Zomega|<=1. It is not
an arbitrary small-critical-data feasibility assertion. Since
r^2=a^2-2a Re m+t^2, (30) is exactly equivalent to
\[
 r^2\le1-2\eta/3+\eta^2/3-t^2+Q_c/7+(4/3)E_c.          \tag{31}
\]
For W=0 equation(26) is exactly w^9-u^9; every error vanishes and the
labels/constraints follow directly without division by W. We do not
infer a new imaginary-mean or motion result from the unused individual
normal bound.

## 8. Entire Legendre tail and retained mean square

For real x in[-1,1], the Laplace integral
\[
 P_n(x)=\pi^{-1}\int_0^\pi
     (x+i\sqrt{1-x^2}\cos\phi)^n\,d\phi
\]
has integrand of modulus at most1 for **every degree n**. To identify the
coefficients, sum its uniformly absolutely convergent geometric series
for |z|<1 inside the integral. The substitution v=tan(phi/2) evaluates
the resulting integral near zero as(1-2xz+z^2)^(-1/2), with branch1 at
zero. The denominators and quadratic do not vanish in the unit disk;
holomorphic continuation establishes the generating identity throughout
it. Thus |Pn(x)|<=1 for ALL n. This ordinary all-degree proof is not
replaced by finitely sampled coefficients or a fixture.

Apply this to |u-nu|^-1, treating nu=0 directly. Absolute convergence
for max|nu|<=tau<r permits the full sum; the degree-one term cancels
since sum nu=0. The degree-two term gives
\[
 F\ge8/r+(W+3Q_c)/(4r^3)-\mathcal T,
 \quad \mathcal T\le\frac{\tau}{(r-\tau)r^3}W.           \tag{32}
\]
This bounds the ENTIRE tail starting at degree3.
All denominators are positive by the receiving budgets. At r_- the
coefficient1/(2r_-^3)+tau/[(r_--tau)r_-^3] is below3/5;
using Qc>=-W gives F>=8/r-3W/5. The low cut then yields
\[
 r\ge[1+(3\eta+3W/5)/8]^{-1}
       \ge1-(3\eta+3W/5)/8>r_0=9997/10000.               \tag{33}
\]
The last strict inequality is rebuilt at e,h.
The Qc coefficient3/(4r^3)-4/7 is positive for all r<=rplus;
its receiving endpoint margin is strictly positive.
Convexity of8s^(-1/2) at s=1, (31)--(33), and Qc>=-W therefore give
\[
 F-8\ge\frac83\eta-\frac43\eta^2+4t^2+\beta_cW
                   -(16/15)tW-(64/15)W^2.              \tag{34}
\]
Retain 4t^2. The WHOLE two-variable coefficient identity is
\[
 4t^2-(16/15)tW-(64/15)W^2
       =4(t-2W/15)^2-(976/225)W^2.
\]
Since W<=h and kappa=beta_c-976h/225>1/600, this proves(3).
Discarding the mean and paying t<=rho instead gives a NEGATIVE receiving
W coefficient; that shortcut is explicitly rejected by the checker.

For W>0 the positive kappa term makes the BASIC lower bound strict.
For W=0,t>0 the square is positive. If both vanish, p=z^9-a^9 and
F=8/a, strictly above the same lower bound. This proves(2) on the
fixed-energy low arm. For an arbitrary actual polynomial, first use(1)
on the low arm; F>8+3eta, including infinity, immediately implies(2).
The slope comparison follows from8/3-4e/3>13/5. All closed endpoints,
critical and original multiplicities, zero variance and high/infinite
cases have thereby been covered.

## 9. Evidence and precise contribution

verify.py reconstructs TWO whole balanced polar expressions, all99 scalar
coefficients, all8 TWO-route39/5 face polynomials and their whole tails,
both FULL nonnegative Newton streams, all70 receiving rational margins
(one closed equality is identified separately), all7 whole cube-field
coefficients, all7 full real two-level skew controls, three complete
Gaussian origin/every-gradient/ordered-Hessian/centered-Newton controls,
and the full two-variable retained-square identity. The33eta target and
discarded-mean shortcut are recorded as rejected mathematical budgets.
All record fields and types, not just counts or hashes, are compared.

Standard-library exact Fraction arithmetic, explicit guards under -O,
whole source pins, normal/optimized/isolated reproduction and malformed/
typed/last-coefficient/endpoint damages are described in README and
VALIDATION. Same-author arithmetic primitives from9818 are credited and
are not independent evidence. No peer executable, fixture or seal is
imported or replayed. The9868 standalone theorem is an explicit ordinary
mathematical dependency; its 36-face certificate is not needlessly copied
into this compact receiving packet.

Communication/Gauss--Lucas, Maclaurin, compact minimizer coverage,
normalization/path/sign/Taylor arguments, Lagrange moments and Newton
majorants, Rouché/all-nine labeling/actual disk normals, complete infinite
tail identification/convergence and convexity remain UNFORMALIZED ordinary
bridges. Source hashes do not formalize them or protect joint replacement.
No numerical optimizer, grid, solver UNKNOWN, timeout, incomplete enumeration
or resource failure is a mathematical premise.

The new mechanism is retaining the complete squared-polar margin for a
smaller ACTUAL phase deficit, then rebuilding all global, coarse, two-local,
reciprocal/energy and fixed-energy root/paired-normal/Legendre/mean-square
conditions in one compatible receiving domain. The normalized1/20 moment
radius and all-path51/1000 radius are kept distinct. The contribution is
the genuine eta1/12000 band, H37 entry and separately fixedH1/320 surplus,
not ownership of classical methods. The full first-power interior beyond
this band, a sharp-C/230/247 transport and optimal constants remain open
in this packet.
