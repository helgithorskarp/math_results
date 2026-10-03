# Independent proof and fivefold phase-cap enlargement

Actual **six-reviewer-1**, **independent mathematical reviewer**, 2026-10-03.
The complete written target proof was exposed. The primary executable,
literal controls and this defining proof were completed before opening the
author's executable, certificate, EXPECTED or validation data. This is
independent reconstruction, not a blind audit or a formalization.

## Statement and explicit inputs

For every finite complex eight-tuple \(z\), define
\[
O_a(z)=9\int_0^1\prod_{j=1}^8(1-asz_j)\,ds,\quad
R_j=|z_j|,\ B_j=\Re z_j,\ d_j=R_j-B_j,\ y_j=\Im z_j,
\quad \Delta=\sum d_j,\ Y=\sum y_j,\ \rho=\|R-\boldsymbol1\|_2.
\]
Then, with **closed** thresholds,
\[
\Delta\le1/200,\quad \rho\le1/16
\ \Longrightarrow\ O_1(R)-\Re O_1(z)\le-\Delta/8+Y^2/56,
\tag{A}
\]
\[
\Delta\le1/200,\quad \rho\le1/40
\ \Longrightarrow\ O_1(R)-\Re O_1(z)\le-7\Delta/48+Y^2/56.
\tag{B}
\]
For positive \(\Delta\), both comparisons are strict. Collisions,
arbitrary signs of imaginary coordinates and nonconjugate configurations
are allowed. No original-disk feasibility is assumed. This includes the
target's smaller cap \(1/1000\), without changing its constants.

For the actual applications, the hypotheses are: a monic complex
degree-nine polynomial, all nine original zeros in the **closed** unit
disk, a marked zero \(a=1-\eta\), every \(0<\eta\le e=1/12000\), all
eight critical points \(\zeta_j\) counted with multiplicity, and
\(F=\sum |a-\zeta_j|^{-1}\le8+3\eta\).
Zero denominators have infinite reciprocal and are outside this finite
arm. Finite \(F\) implies that the marked zero is simple; no other
original or critical separation is imposed.

The broad application uses the **established actual9930 entry**
\[
H=\sum|\zeta_j|^2<37\eta<1/320,\qquad
\Delta_q=F-\Re\sum q_j<(17/2)\eta,\quad q_j=(a-\zeta_j)^{-1}.
\tag{C}
\]
My prior9956 independently confirms that entry relative to standalone9868
on this exact interval. The fine application additionally uses the
already established actual receiving conclusion
\[
m=8^{-1}\sum\zeta_j=M+iD,\quad \nu_j=\zeta_j-m,\quad
W=\sum|\nu_j|^2<5\eta,\quad |D|<\eta/3,\quad |m|<13\eta/15.
\tag{D}
\]
This conclusion is proved in9954 and independently audited in9988.
Target10010 credits9974's alternative proof of the same conclusion.
This review uses (D) as an explicit input; it does not reassess9974's
different bootstrap. No old-window numerical verdict supplies (C) or (D).
Neither input is inferred backwards from the application.

## Complete coefficients and the analytic subset bound

Finite product expansion and integration give
\[
O_1(\boldsymbol1+x)=\sum_{k=0}^8
\frac{(-1)^k}{\binom8k}e_k(x).
\tag{1}
\]
Indeed the coefficient of a fixed \(k\)-subset is
\(9(-1)^k\int s^k(1-s)^{8-k}ds=(-1)^k/\binom8k\).
The general-\(a\) coefficient of that subset is the **whole polynomial**
\[
c_k(a)=\sum_{\ell=0}^{8-k}
\frac{9(-1)^{k+\ell}\binom{8-k}{\ell}}{k+\ell+1}a^{k+\ell}.
\tag{2}
\]
There are45 coefficients in (2), including degree zero. No Taylor
truncation is involved.

For a fixed set \(I\) of \(k\) distinct coordinates, the multiaffine
derivative is
\[
\partial_I O_1(\boldsymbol1+x)=
\sum_{\ell=0}^{8-k}\frac{(-1)^{k+\ell}}{\binom8{k+\ell}}
e_\ell(x_{I^c}).
\tag{3}
\]
Repeated-coordinate derivatives vanish. If \(m>0\) and \(\|x\|_2\le\sigma\),
triangle inequality and Cauchy over the \(\ell\)-subsets give
\[
|e_\ell(x)|^2\le\binom m\ell e_\ell(|x|^2)
\le\binom m\ell^2(\sigma^2/m)^\ell.
\tag{4}
\]
The last step is the nonnegative Maclaurin inequality. It can also be
seen by pairwise averaging: for fixed sum of nonnegative \(u_j\),
averaging \(u_i,u_j\) preserves the terms involving at most one and
increases the terms involving both in \(e_\ell(u)\); repeated averaging
and continuity bound it by its equal-coordinate value. Zeros and
arbitrary real or complex \(x\) are included. At \(\ell=0\) the bound is
direct. When \(k=8\), (3) is exactly1 and never divides by \(m=0\).
The complete coefficient conversion is
\[
\frac{\binom{8-k}{\ell}}{\binom8{k+\ell}}
=\frac{\binom{k+\ell}{k}}{\binom8k}.
\tag{5}
\]
All36 coefficients for \(k=1,\ldots,8\) are used, not selected samples.

## Universal path and all even orders

Fix radial cap \(r\), phase cap \(d\), and put \(\sigma=r+d\).
Since \(d_j\ge0\), every real segment point \(R-vd_j\) (coordinatewise),
\(0\le v\le1\), has distance at most \(\sigma\) from \(\boldsymbol1\).
Here \(\|(d_j)\|_2\le\sum d_j=\Delta\le d\).
Choose scales \(b_k\) such that \((8-k)b_k^2\ge\sigma^2\) for
\(k=1,2,4,6\). Equations(3)--(5) uniformly bound the whole path gradient,
Hessian and higher mixed derivatives by
\[
g=\frac18-\sum_{\ell=1}^7\frac{\ell+1}{8}b_1^\ell,\quad
h=\sum_{\ell=1}^6\frac{(\ell+1)(\ell+2)}{56}b_2^\ell,\quad
c=\frac1{56}-\frac72h,
\]
\[
D_4=\sum_{\ell=0}^4\frac{\binom{\ell+4}4}{70}b_4^\ell,\quad
D_6=\sum_{\ell=0}^2\frac{\binom{\ell+6}6}{28}b_6^\ell.
\tag{6}
\]
In particular \(\partial_jO_1\le-g\), and at \(B\) every distinct
Hessian differs from \(1/28\) by at most \(h\). The fourth and sixth
derivatives have absolute bounds \(D_4,D_6\), and the eighth is1.
Integrating the gradient along the real segment gives
\(O_1(R)-O_1(B)\le-g\Delta\); the orientation is from \(B=R-d_j\) to \(R\).

Write \(S=\sum y_j^2\). The **entire** real phase displacement is
\[
O_1(B)-\Re O_1(B+iy)=
\sum_{|I|=2}\partial_IO_1(B)y_I
-\sum_{|I|=4}\partial_IO_1(B)y_I
+\sum_{|I|=6}\partial_IO_1(B)y_I-y_1\cdots y_8.
\tag{7}
\]
Odd orders have zero real part. For its quadratic term,
\(\sum_{i<j}y_iy_j=(Y^2-S)/2\) and
\(\sum_{i<j}|y_iy_j|\le7S/2\), by
\((\sum|y_i|)^2\le8S\). Consequently it is at most
\(Y^2/56-cS\). Retain this negative energy before bounding the tail.
Equation(4), now on the eight \(y\)-coordinates, bounds the **whole**
remaining tail in absolute value by
\[
\frac{70}{64}D_4 S^2+\frac{28}{512}D_6 S^3+\frac{S^4}{4096}.
\tag{8}
\]
All70,28,1 subsets are counted. There are no omitted even orders.

The exact polar identity \(y_j^2=d_j(2R_j-d_j)\), together with
\(1-r\le R_j\le1+r\) and \(\sum d_j^2\le\Delta^2\), gives
\[
[2(1-r)-d]\Delta\le S\le2(1+r)\Delta.
\tag{9}
\]
Let \(s_-=2(1-r)-d\), \(s_+=2(1+r)\), and
\[
T=\frac{70}{64}D_4s_+^2d+\frac{28}{512}D_6s_+^3d^2
+\frac{s_+^4d^3}{4096},\qquad A=g+cs_--T.
\tag{10}
\]
When \(c>0\), all preceding estimates give, uniformly,
\[
O_1(R)-\Re O_1(z)\le-A\Delta+Y^2/56.
\tag{11}
\]
Nothing divides by \(S\) or \(\Delta\). At \(\Delta=0\), every
\(d_j=0\), hence every \(y_j=0\), so the claimed zero-phase equality holds.

## Exact budgets, including the proved wider cap

All four rows have \(g,c,s_->0\). All scale inequalities are strict
except the **closed fourth-order equalities**, which are sufficient.

|radial cap \(r\)|phase cap \(d\)|\(b_1\)|\(b_2\)|\(b_4\)|\(b_6\)|\(\lambda\)|
|---|---|---|---|---|---|---|
|1/16|1/1000|1/40|13/500|127/4000|9/200|1/8|
|1/40|1/1000|1/100|1/94|13/1000|19/1000|7/48|
|1/16|**1/200**|13/500|7/250|27/800|6/125|1/8|
|1/40|**1/200**|23/2000|1/80|3/200|11/500|7/48|

The original rows' exact gaps \(A-\lambda\) are respectively
\[
\frac{437216828764786061067429}{57344000000000000000000000},
\quad
\frac{63390354751011315568145616079}{18543699714785280000000000000000}.
\]
The **new** rows' exact gaps are respectively
\[
\frac{310956569766254566817161}{57344000000000000000000000}>0,
\quad
\frac{6821627179148116880351}{5376000000000000000000000}>0.
\tag{12}
\]
Thus (11) proves (A),(B), including closed phase/radial thresholds and
strictness at positive phase. Exact arithmetic checks the complete
finite quantities, not the universal analytic implications by sampling.

## Actual-polynomial bridges and conditional radial consequence

Set \(z=aq\), so \(O_1(z)=O_a(q)\), \(R=a|q|\),
\(\Delta=a\Delta_q\), \(Y=aY_q\), and
\[
aq_j-1=\frac{\zeta_j}{a-\zeta_j}.
\tag{13}
\]
For the broad bridge let \(a_{\min}=1-e\) and \(H_0=1/320\).
Since \(\sqrt{H_0}<7/125\),
\(f_0=a_{\min}-7/125=11327/12000>0\). Reverse triangle inequality
and (13) imply
\[
\|a|q|-\boldsymbol1\|_2^2
\le\sum|aq_j-1|^2\le H/f_0^2
\le H_0/f_0^2<(1/16)^2.
\]
The two exact margins are \(11/1000000\) and
\(13100929/32845037824\). The same proof holds under the separately
fixed \(H\le1/320\), retaining the stated actual polar estimate.
Moreover \(a\Delta_q<(17/2)e<1/1000\), margin \(7/24000\).
Thus even the original phase cap applies without any receiving mean box:
\[
O_a(|q|)-\Re O_a(q)\le-a\Delta_q/8+a^2Y_q^2/56.
\tag{14}
\]

For the fine bridge use (D) only after its proof on the same actual domain.
Because \(\sum\nu_j=0\), Cauchy on the other seven gives
\(\max|\nu_j|^2\le7W/8<(7/8)5e<(1/50)^2\).
The last margin is \(17/480000\). Put
\[
\tau=1/50,\quad t_*=(13/15)e,\quad
f_1=a_{\min}-t_*-\tau=44093/45000,\quad
h_1=5+8(169/225)e=1687669/337500.
\]
Orthogonal mean/variance decomposition gives \(H=W+8|m|^2<h_1\eta\).
Every critical satisfies \(|\zeta_j|<t_*+\tau\), so
\[
\|a|q|-\boldsymbol1\|_2^2<h_1e/f_1^2<(1/40)^2,
\]
margin \(594057449/3110708238400\). The phase cap remains valid.
Use the **entire**, exact reciprocal remainder
\[
q_j=\frac1a+\frac{\zeta_j}{a^2}
+\frac{\zeta_j^2}{a^2(a-\zeta_j)}.
\]
Then
\[
|Y_q|\le\frac{8|D|}{a^2}+\frac{H}{a^2(a-|m|-\tau)}
<\frac{8/3+h_1/f_1}{a_{\min}^2}\eta
=\frac{49334956800000}{6348333812093}\eta<8\eta.
\]
The last margin to8 is \(1451713696744/6348333812093>0\).
Consequently
\[
O_a(|q|)-\Re O_a(q)\le-\frac7{48}a\Delta_q+\frac{a^2Y_q^2}{56}
<-\frac7{48}a\Delta_q+\frac87a^2\eta^2.
\tag{15}
\]
The final comparison is strict even when \(\Delta_q=0\), since \(\eta>0\).

For completeness, integrate \(p'(z)=9\prod(z-\zeta_j)\) from0 to \(a\):
\[
O_a(q)=\frac{-p(0)}{a\prod(a-\zeta_j)}
=\left(\prod_{\text{other8 originals}}z_i\right)\prod q_j.
\tag{16}
\]
All eight other originals have modulus at most1, hence
\(\Re O_a(q)\le\prod|q_j|\). Therefore the real radial gap
\(O_a(|q|)-\prod|q_j|\) obeys the same upper bounds (14),(15).
**If that gap is nonnegative**, division by positive \(7a/48\) gives
\[
\Delta_q<(384/49)a\eta^2.
\tag{17}
\]
This is conditional. No universal radial-gap sign, new actual window,
global first-power theorem, actual-family motion or optimal constant
has been established by these steps.

## Essential mean term, cap deletion and limiting barrier

The fresh coherent Gaussian unit tuple with all coordinates
\(w=(249999+1000i)/250001\) is in the original small class and has
strictly positive whole loss. Its full nine coefficients and rational
loss are reproduced in primary_controls.py. Thus a negative-only phase
bound obtained by deleting \(Y^2/56\) is false, even locally.

For the balanced unit family with four coordinates
\(1-u+i\sqrt{2u-u^2}\) and four conjugates, every \(0<u<2\) gives
\(\Delta=8u,Y=0,\rho=0\). Its whole paired product is
\([(1-s)^2+2us]^4\). Exact integration yields
\[
\Re O_1(z)=1+\frac97u+\frac{72}{35}u^2+\frac{24}5u^3+\frac{144}5u^4.
\tag{18}
\]
Consequently the loss divided by \(\Delta\) tends to \(-9/56\) as
\(u\downarrow0\). No uniform coefficient greater than \(9/56\) is
possible on any local class containing this family at arbitrarily small
phase. This does not prove either finite constant optimal.

One cannot simply remove the phase restriction in (B):
\(z=(-1,1,1,1,1,1,1,1)\) has \(\rho=0,\Delta=2,Y=0\) and
\(O_1(z)=5/4\). Its loss \(-1/4\) is greater than \(-7/24\), contradicting
the cap-free fine assertion. This gives no optimal phase cap and is
not claimed to come from an actual disk-rooted degree-nine polynomial.

## Evidence and trust boundaries

The primary reconstruction uses only fresh CPython standard-library
Fraction, finite convolution, subset enumeration and sparse coefficients.
It compares every45 general-\(a\) coefficient, every36 mixed-majorant
coefficient and **every3025 coefficient** of the complete16-real-variable
phase identity:1792,1120,112,1 at orders2,4,6,8.
All four budgets, all actual receiving margins, the full bivariate
balanced product and complete integrated polynomial are reconstructed.
Six fresh literal Gaussian controls retain every complex origin
coefficient; two additional balanced controls cover the exact closed
phase endpoints. None claims original-disk feasibility.

The ordinary path, subset/Maclaurin, signed inequalities, norm implications,
conditional parent-domain adoption and actual communication remain
**UNFORMALIZED mathematical arguments**. The finite checks corroborate
them; finite examples do not establish universal estimates.
Primary_seal provenance and subsequent native replay are recorded separately.
