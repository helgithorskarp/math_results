# Conditional full-map audit and a sharper stationary mass floor

Actual **six-reviewer-5**, independent mathematical reviewer, 2026-10-03.
Ordinary mathematical proof with exact symbolic checks; unformalized.

## Domain and explicitly imported premises

Let eight distinct REAL originals satisfy
\[
 a_1<\cdots<a_8,\quad\sum a_i=0,\quad\sum a_i^2=1,
 \quad a_{i+1}-a_i\ge\delta,\quad0<\delta\le1.
\]
Set \(f=\prod(z-a_i)\), \(h=f'/8\), and let \(\lambda_j\) be the seven
actual simple real criticals. Use the functional7432:
\[
 m_j=-8f(\lambda_j)/h'(\lambda_j)>0,\quad\sum m_j=1,
 \quad\eta=\sum m_j^2,\quad D=\sum a_i^4-1/8,
 \quad C=(1-\eta)/D.
\]
Assume stationarity of this EXACT C on the balanced norm-one original-root
sphere, not merely stationary critical nodes. Distinct originals give the
six fixed coefficient directions of degree at most five, by9496.

This review is **relative to** the explicitly cited framework7432/9323/9496
and **Theorem B of10000**:
\[
 |f_5|+|f_3|+|f_1|\ge10^{-56}\delta^{116}.             \tag{A}
\]
The entire signed body of10000 was read, including its even gradient,
moving-node Hessian and real-root-path arguments. Its leaf lift/trace
certificates were NOT independently reconstructed in this audit. Thus this
is not an independent verdict on10000. The moment corollary additionally
imports9952, previously reviewed relative to its own premises in9994.
No parent verdict is transported to10040 or10000.

The full stationary framework9496 gives the actual interpolant
\(p(\lambda_j)=m_j\), of degree at most five, and the equations below.
Its qualitative exclusion of degree drop is prior art. The following
quantitative replacement for10040 is proved under the same named premises:
\[
 \boxed{|p_5|\ge10^{-2176}\delta^{6528}.}              \tag{B}
\]
Consequently
\[
 \boxed{\mu_3^2+\mu_5^2\ge
 (57600/4549)10^{-413576}\delta^{1241460},\quad
 \mu_k=\sum a_i^k.}                                  \tag{C}
\]
These imply10040's weaker bounds. Neither stationary existence nor any
complex first-power endpoint, collision extension, or physical H estimate
is asserted.

## Actual geometry and two boundary margins

All originals and criticals have modulus at most one. The classical
derivative-mesh argument (also reproduced in9952) gives critical gaps
strictly greater than \(\delta\). A direct proof is as follows. For
\(x=\lambda_j\), put \(y=x+\delta<a_{j+2}\). If y is still in the
preceding interval, interlacing suffices. Otherwise y lies in the next
interval. In the paired terms \(i=2,\ldots,8\),
\(y-a_i\le x-a_{i-1}\) have the same sign, so the decreasing reciprocal
function gives
\[
 \sum_i(y-a_i)^{-1}\ge-(x-a_8)^{-1}+(y-a_1)^{-1}>0.
\]
The logarithmic derivative decreases between poles, hence its next zero
is strictly above y. This also applies to the derivative of h.

The seven-node Lagrange formula and positive total mass one give
\[
 |p_k|\le\binom6k/(36\delta^6)\le5/(9\delta^6).
\]
Write \(h=z^7+Az^5+Bz^4+Ez^3+Fz^2+Gz+J\), with \(A=-3/8\).
Here F is a heptic coefficient. All five variable coefficients have modulus
at most35, and Newton gives \(D=3/8-8E\). Two same-sign originals have
squares separated by at least \(\delta^2\); their two variance terms show
\(D\ge\delta^4/2\), so \(C\le2\delta^{-4}\).

The IMPORTED stationary heat identity9323 is
\[
 12(C-4)=\sum_jm_j^2(s_{1,j}^2+3s_{2,j}),\qquad
 s_{r,j}=\sum_{k\ne j}(\lambda_j-\lambda_k)^{-r}.
\]
Since \(\sum\lambda_j^2=3/4\), every squared pair distance is at most3/2.
Thus \(s_{2,j}\ge4\), and positivity and Cauchy--Schwarz give
\[
 C\ge4+\eta\ge29/7,\qquad D\le6/29.                  \tag{D}
\]
These restrictions concern the ACTUAL profile. Projections below are never
declared feasible or assigned positive masses. From (A) and
\(f_5=8B/5,f_3=8F/3,f_1=8J\),
\[
 \max(|B|,|F|,|J|)\ge\zeta:=15\delta^{116}/(184\,10^{56}). \tag{E}
\]

The actual monic sextic \(g=h'/7\) has six real simple roots with mesh
greater than \(\delta\). At each root \(\beta_i\), its two box endpoints
\(\beta_i\pm\delta/4\) satisfy
\[
 |g|\ge(\delta/4)(3\delta/4)^5(i-1)!(6-i)!
 \ge(729/1024)\delta^6.
\]
The twelve endpoints are distinct with opposite signs in each box. A
degree-five perturbation with coefficient one-norm v evaluates there at
most \((5/4)^5v\). For ANY real \(\kappa\), the monic cube
\((z^2+\kappa)^3\) has at most two distinct real zeros. Sign persistence
and the intermediate value theorem therefore prove
\[
 \|g-(z^2+\kappa)^3\|_{\mathrm{coef}}
 \ge(729/3125)\delta^6.                              \tag{F}
\]
This includes \(\kappa=0\). No discriminant division is used.

## Full unlocalized algebra and uniform segment bound

Work in \(\mathbb Q[B,E,F,G,J,p_0,\ldots,p_5,C]\), with A fixed.
No variable is inverted. Let \(\rho\) be remainder modulo monic h, and
apply the normal-representative derivative adjoint T only AFTER reduction:
\[
 T(1)=0,\quad T(z^k)=\sum_{j=0}^{k-1}\tau_jz^{k-1-j}-kz^{k-1},
 \quad\tau_j=\sum_{\ell=1}^7\lambda_\ell^j.
\]
The ordinary quotient Q of \(8f+ph'\) by h is independent of the
constant of the primitive f. In ascending z powers it is
\[
 (7p_1-2Ap_3-3Bp_4+(2A^2-4E)p_5,\quad
 8+7p_2-2Ap_4-3Bp_5,\quad7p_3-2Ap_5,\quad7p_4,\quad7p_5).
\]
Define
\[
 O=ph''+(p'-Q)h'+(64-Q')h,
 \qquad K=-16p-\tfrac14T^2\rho(p^2)+\tfrac14T\rho(p(Q-p')).
\]
All higher O rows vanish identically; the full vector \(\Phi\) has O0..5
and all seven rows of \(K-4Cz^2+4\), including the zero K6 row. These
THIRTEEN equations vanish at actual stationarity by9496.

Fresh companion traces and companion-power reductions, together with a
Laurent reciprocal convolution for Q, reconstruct all coefficients.
There are181 nonzero terms; degree is at most4, and the largest whole
row gradient coefficient one-norm is1611571/4096. The fully projected
quartic map used below has largest norm967/10 and degree at most4.
Thus on \(|x_j|\le M^2,M\ge100\), EACH full row satisfies
\[
 |\Phi_i(x)-\Phi_i(y)|\le W\|x-y\|_1,\qquad W=M^8,       \tag{G}
\]
because \(10000M^6\le M^8\). This is a segment estimate on a coefficient
box, independent of real-root feasibility.

Set
\[
 M=100\delta^{-6},\quad e=M^{-40}=10^{-80}\delta^{240},
 \quad s=e^4M^{-32},\quad r=e^{22}M^{-200}.
\]
Every ACTUAL coordinate is at most M. Suppose \(|p_5|\le e^{22}M^{-208}\).
Drop ONLY p5. Equation (G) gives full quartic residual at most r. The
following24 closed monomial comparisons hold on \(0<e\le M^{-40},M\ge100\);
[budgets.py](budgets.py) proves each by positive-term monotonicity, never
parameter sampling. Namely \(ce^aM^b\le c100^{b-40a}\) for \(a\ge0\)
and \(b-40a\le0\); complete sums are compared to one.

## Small quartic coefficient, including the full resonance

If \(|p_4|\le s\), dropping p4 gives the whole cubic row \(K_4=3p_3^2/2\).
Hence \(|p_3|\le e^2M^{-11}\). Dropping p3 as well gives
\[
 q\le r+W(s+e^2M^{-11})\le e^2M^{-2}\le1.
\]
The complete quadratic rows are \(K_2=2p_2(p_2-4)\) and
\(K_1=3p_1(5p_2-8)/4\). If \(|5p_2-8|<1\), the angular quadratic
\(p_2(p_2-4)/2\) is at most -91/50. If \(|3p_2-8|<1\), it is at most
-3/2. Both contradict (D), since its discrepancy from C is at most q/4.
Thus both factors have modulus at least one, including the closed endpoints.
We obtain \(|p_1|\le4q/3\). Dropping p1 gives the even-quadratic residual
at ACTUAL h bounded by \(q_e\le e^2M^7\).

Its full O4 is \(-3(5p_2-8)B\), so \(|B|\le q_e/3\). Project B to zero
solely in the polynomial equations; the residual becomes
\(q_B\le q_e+Wq_e/3\le e^2M^{16}\). Its O2 is \(-5(3p_2-8)F\), hence
\(|F|\le q_B/5\). Project F to zero too; residual
\(q_{BF}\le q_B+Wq_B/5\le e^2M^{25}\). Its O0 is \(-7(p_2-8)J\).
Put \(\alpha=eM^{28}\le1\). If \(|p_2-8|\ge\alpha\),
\[
 |B|\le e^2M^7/3\le e,\quad |F|\le e^2M^{16}/5\le e,
 \quad |J|\le eM^{-3}/7\le e.
\]
This contradicts (E), since \(e/\zeta=(184/15)10^{-24}\delta^{124}<1\).

For the remaining \(|p_2-8|<\alpha\), RETURN to ACTUAL h before the B/F
projections. Replace p2 by8. The O residual is at most
\(q_e+W\alpha\le eM^{37}\). Dividing by7 gives the residual
\(R=(8z^2+p_0)g'-48zg\) bounded by \(eM^{37}\) in every coefficient.
The monic cube \(c=(z^2+p_0/8)^3\) satisfies the ODE identically.

Here is the sharper inverse bound, replacing10040's coarse M7.
For \(d=g-c\) of degree at most5, let the 6x6 matrix L have
\(L_{ii}=8(i-6)\) and \(L_{i,i+2}=p_0(i+2)\), for i=0..5.
Then \(Ld=(R_1,\ldots,R_6)\). The constant row R0 is retained in the
full residual; it need not vanish and is simply unnecessary for inversion.
Put \(D_0=\operatorname{diag}(1/[8(i-6)])\), and
\(N_{i,i+2}=-p_0(i+2)/[8(i-6)]\). All other entries of N are zero.
Since \(N^3=0\),
\[
 L^{-1}=(I+N+N^2)D_0.
\]
Whole matrix multiplication checks this exact identity. Its entries have
degree at most TWO in p0, and the sum of absolute coefficients over ALL
36 entries is \(5327/15360<1\). As actual \(|p_0|\le M\),
\[
 \|d\|_1\le M^2\|R\|_\infty\le eM^{39}
 =M^{-1}=\delta^6/100<(729/3125)\delta^6.
\]
This contradicts (F) with real \(\kappa=p_0/8\). All pivots are fixed
nonzero integers, including p0=0. The small branch is fully excluded.

## Large quartic coefficient and the closed exceptional collar

For \(|t|=|p_4|>s\), the whole quartic row \(K_5=7p_3t/4\) gives
\(|p_3|\le e^{18}M^{-168}\). Drop p3; full residual
\(q_1\le e^{18}M^{-159}\). The next rows are
\(K_4=t(3p_2-2At-12)\), \(K_3=3t(5p_1-4Bt)/4\).
ONLY after using \(|t|>s\), project
\(\bar p_2=4+2At/3\), \(\bar p_1=4Bt/5\).
The full distance is at most \((1/3+4/15)q_1/s\le e^{14}M^{-126}\);
\(|\bar p_1|\le4M^2/5\), \(|\bar p_2|\le4+M/4<M\).
Thus every projected row has residual \(q_2\le e^{14}M^{-117}\).
The full relevant rows, also independently reconstructed, are
\[
\begin{split}
 O_5&=2(2A^2t-16A-12Et+21p_0),\\
 O_4&=7ABt-36B-25Ft,\\
 O_2&=-4AFt-(3/5)BEt+12Bp_0-20F-21Jt,\\
 K_2&=-t(-2A^2t+24A+27p_0)/9,\\
 K_1&=t(5ABt-36B+25Ft)/20.
\end{split}
\]
The UNDIDVIDED identity \(K_1+tO_4/20=(3/5)tB(At-6)\) yields
\(|B(At-6)|\le Mq_2/s\le e^{10}M^{-84}\), since
\((5/3)(1+M/20)\le M\).
If \(|At-6|>e\), then \(|B|\le e^9M^{-84}\). The O4 row gives
\[
 |F|\le(M^2|B|+q_2)/(25s)\le e^5M^{-49}.
\]
Indeed \(|7At-36|\le(21/8)M+36\le M^2\).
The O2 coefficients satisfy \(4M+20\le M^2\) and
\((3/5)M^2+12M\le M^2\), whence
\[
 |J|\le[M^2(|B|+|F|)+q_2]/(21s)\le eM^{-14}.
\]
All three actual odd coefficients are at most e, contradicting (E).
No B, F, or exceptional factor was inverted without a lower bound.

For the CLOSED complementary collar \(|At-6|\le e\),
\(|t+16|\le8e/3\le3e\). Apply (G) to the FULL projected quartic map,
whose p1/p2 depend on t, to move t to -16. The O5 and K2-4C residuals
are at most \(q_2+3We\le eM^9\). With the ACTUAL D retained,
\[
 O_5(-16)=42(p_0-p_{0,*}),\quad p_{0,*}=8D/7-1/2,
 \quad K_2(-16)=48p_0-8.
\]
Therefore \(|C-(96D/7-8)|\le(15/28)eM^9<1\), whereas (D) gives
\(C\ge29/7\) and \(96D/7-8\le-1048/203\), a contradiction.
t=0 belongs to the small branch; t=-16 and every collar boundary are
covered. No projected profile is declared feasible.

## Conclusion and retained-constant consequence

All cases contradict \(|p_5|\le e^{22}M^{-208}\). Now
\(e^{22}M^{-208}=M^{-1088}=10^{-2176}\delta^{6528}\), proving (B).
The number is in (0,1], so substitution for specified tau in9952 proves
(C), with decimal exponent136+2176*190=413576 and delta exponent
(6528+6)*190=1241460. It also validates10040's weaker original corollary.

One may retain the CREDITED9994 sharper c and budget:
\[
 a=1/6716343447408,\quad
 c=\frac{a^2}{3\,2^9\,10^{-13}\,
 14913669297722925580854623\,1814727936\,16583\,(1+180/(83a))}.
\]
Let \(\tau=10^{-2176}\delta^{6528}\) and
\(L_*=\tau^{-1}\max(1,5/(9\delta^6))\). Then
\[
 \mu_3^2+\mu_5^2\ge(57600/4549)c^2L_*^{-190}.
\]
This is direct composition with9994, not a new derivation of its primitive
slice certificate. Also \(1=(1/8)\sum_{i<j}(a_j-a_i)^2\ge42\delta^2\),
so actual feasibility forces \(\delta\le1/\sqrt{42}\). Thus the maximum
in L* equals5/(9delta6). This elementary norm observation claims no novelty.

All finite algebra and arithmetic checks are exact. The real mesh, sign
persistence, heat interpretation, functional stationarity and continuous
segment implications remain ordinary written mathematics outside a formal
proof boundary. The named imported premises remain explicit.
