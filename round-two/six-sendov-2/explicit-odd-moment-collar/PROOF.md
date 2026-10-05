# An explicit two-odd-moment angular collar

Actual author **six-sendov-2**, role **researcher**, 2026-10-05.
Complete ordinary author proof with exact polynomial and rational checks;
**unformalized and independently unreviewed**. No historical priority is
claimed. The very small collar below is an explicit quantitative statement,
not a practical estimate of the largest possible neighborhood.

## 1. Statement, full masses and credited inputs

Let (x\in\mathbb R^8) satisfy \(\sum x_i=0\) and \(\sum x_i^2=1\).
Put \(\mu_k=\sum x_i^k\), \(P=I-\mathbf1\mathbf1^T/8\), and
\(H=(P\operatorname{diag}(x)P)|_{\mathbf1^\perp}\).
At each **distinct** eigenvalue use the full projection mass
\(m_\lambda=\|\Pi_\lambda x\|^2\), and put
\[
 \eta=\sum_\lambda m_\lambda^2,\quad D=\mu_4-1/8,\quad
 C=(1-\eta)/D\quad(D>0).
\]
At the uniform four-positive/four-negative profiles, (D=0), use the
continuous value \(\widetilde C=16\); elsewhere \(\widetilde C=C\).
These definitions and the full-sphere continuity are credited to
[7432](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md),
[8753](../angular-three-level-transition/PROOF.md), and the independent
[8806 audit](../../six-reviewer-1/three-level-angular-audit/REVIEW.md).

**Theorem.** Including every original-root and compression multiplicity,
\[
 \boxed{\quad \mu_3^2+\mu_5^2\le10^{-180}
             \quad\Longrightarrow\quad \widetilde C\le70/3.\quad}       \tag{1}
\]
The threshold is \(47/2-1/6\). This is a real original-root angular
stability lemma auxiliary to degree-nine complex first power; it does
not establish the unrestricted complex first-power inequality.

The source-published
[universal localization](../universal-angular-localization/PROOF.md)
gives, without odd-moment hypotheses,
\[
 C\le5560/243\quad(0<D\le1/676),\qquad
 C\le23\quad(D\ge3/112).                                  \tag{2}
\]
Both values are below (70/3). Its proof is an explicit ordinary input,
not an inferred numerical search outcome. We therefore need only
\[
                 1/676<D<3/112.                            \tag{3}
\]
The [heat/Hermite reduction](../heat-hermite-angular-reduction/PROOF.md)
supplies real-root preservation, strict separation for positive backward
heat time, and density **inside closed residual collars**. The new
quantitative separation and sign licence appear below. The exact-locus
Gram polynomial and boundary square are credited to the
[sharp two-odd-zero proof](../sharp-odd-moment-angular-bound/PROOF.md);
the value and attaining family already occur in
[8672](../triple-angular-persistence/PROOF.md).
No review of a credited input is transferred to this theorem.

## 2. Entire general even Gram and its valid inequality

Write (u=\mu_3,v=\mu_5). The complete chart is
\[
 f(z)=z^8-\tfrac12z^6-\tfrac u3z^5+2Ez^4
 +(\tfrac u6-\tfrac v5)z^3+4Gz^2+8Jz+c,
 \qquad D=3/8-8E.                                        \tag{4}
\]
For simple real originals, (h=f'/8) has seven distinct real zeros.
Newton's recurrence for (h) gives
\[
\begin{split}
 \tau_0&=7,\qquad \tau_2=3/4,\qquad \tau_4=9/32-4E,\\
 \tau_6&=27/256-9E/4-6G+25u^2/192,\\
 \tau_8&=81/2048-9E/8+4E^2-3G+5u^2/192+uv/8,
\end{split}                                               \tag{5}
\]
where \(\tau_k=\operatorname{tr}H^k\).
The credited resolvent \(x^T(zI-H)^{-1}x=8z-8f/h\) gives
\[
 w=(\nu_0,\nu_2,\nu_4)^T
   =(1,3/8-8E,9/64-4E-24G+5u^2/24)^T.                    \tag{6}
\]
As a separate derivation, \(\nu_2=\mu_4-1/8\), and
\(\nu_4=\mu_6-\mu_4/4+1/64-u^2/8\), the squared norm of
the projected vector \((x_i^3-x_i/8)_i\).
Newton gives \(\mu_6=1/4-6E+u^2/3-24G\), verifying (6).
All entries of the three-row matrix
\[
                  A=(\tau_{2(i+j)})_{i,j=0}^2              \tag{7}
\]
are thus specified for the **general** chart. They depend on the residual
moments through (u^2,uv), and not on (J,c).

Let (V_{ij}=\lambda_j^{2i}). Then (A=VV^T) and (Vm=w).
Whenever (A>0), least squares gives
\[
 \eta\ge w^TA^{-1}w,\qquad
 C\le B_x:=\frac{1-w^TA^{-1}w}{D}.                       \tag{8}
\]
We will prove the positive determinant for the actual profile before
using an inverse. Define the polynomial numerator, with (T=70/3),
\[
 \Psi_T(x)=(TD-1)\det A+w^T\operatorname{adj}(A)w
          =D\det A\,(T-B_x).                            \tag{9}
\]
The last equality is used only on a positive determinant domain.

## 3. Quantitative determinant and envelope on an enlarged exact band

Consider a simple real original profile (y) with third and fifth
moments zero and
\[
                 1/1352\le D_y\le3/100.                  \tag{10}
\]
Its (h_J=z^7-3z^5/8+Ez^3+Gz+J) has simple real zeros.
The horizontal-level continuation proved in
[10105, Section4](../two-moment-parity-descent/PROOF.md) makes its **critical**
polynomial (h_0) simple and real-rooted. This does not assert that a
centered primitive is real-rooted. Write
\[
 h_0=zq(z^2),\quad q(Y)=Y^3-3Y^2/8+EY+G,\quad
 b=1/8,\ a^2=D_y/24,\ p=\prod_{i=1}^3(Y_i-b).
\]
The three (Y_i) are positive real roots. Their centered sums are zero,
their squared sum is (6a^2), and their discriminant gives
\[
 -2a^3\le p\le2a^3,\quad
 E=3/64-D_y/8,\quad G=-1/512+D_y/64-p.                  \tag{11}
\]
Here (a^2\le1/800<1/784), so (a<1/28). From (5)--(6),
\[
A_y=\begin{pmatrix}
7&3/4&3/32+D_y/2\\
3/4&3/32+D_y/2&3/256+3D_y/16+6p\\
3/32+D_y/2&3/256+3D_y/16+6p&3/2048+3D_y/64+D_y^2/16+3p
\end{pmatrix},\quad w_y=(1,D_y,D_y/8+24p)^T.             \tag{12}
\]
This is the Gram at the actual profile (y), even when (J\ne0).
The critical-only continuation licenses (11); no feasible even primitive
is being substituted for (y).

As a polynomial in (p), its determinant has coefficient (-252) of
(p^2), and hence is concave. At the two endpoints,
\[
 \det A_y\big|_{D_y=24a^2,\ p=\pm2a^3}
       =72a^2(b\mp a)^2(b\pm2a)^2.                      \tag{13}
\]
Concavity, (10), and (a<1/28) therefore give the explicit floor
\[
 \det A_y\ge\frac{72}{32448}(5/56)^2(3/56)^2
             >\delta:=1/20000000.                      \tag{14}
\]
The matrix is a real Gram, so this positive determinant makes it positive
definite. Formula (13) also handles limiting double square nodes without
cancelling their discriminant.

For a formal threshold (R), literal determinant and cofactor expansion
of (12) yields the credited full polynomial
\[
\begin{split}
\Phi_R={}&3(R+2)D_y^4/32+3(4-R)D_y^3/512
          +3(R-16)D_y^2/4096\\
 &+pD_y(9R/64-3(R+26)D_y/4)+p^2(486-252RD_y).           \tag{15}
\end{split}
\]
It equals (D_y\det A_y(R-B_y)). For (R=208/9), the coefficient
of (p^2) on (10) is at least (7782/25>300).
Thus its derivative in (p) is bounded below by the value at (-2a^3):
\[
 \partial_p\Phi_{208/9}(24a^2,-2a^3)=24a^2 L(a),\quad
 L(a)=13/4-81a-884a^2+23296a^3.                          \tag{16}
\]
On (0<a<1/28),
\[
 L'(a)=-55+(a-1/28)(69888a+728)<0,\quad L(1/28)=57/196>0.
\]
Consequently (Phi) is increasing in (p), and its lower endpoint is
\[
 \Phi_{208/9}(24a^2,-2a^3)
       =192a^4(a+1/8)^2(34a-1)^2\ge0.                  \tag{17}
\]
We have proved on the enlarged band
\[
 B_y\le208/9,\qquad
 \Psi_{70/3}(y)\ge(2/9)D_y\det A_y
                    > (2/9)(1/1352)\delta=:M.           \tag{18}
\]
This strengthens the quantitative denominator control needed here; the
sharp value, polynomial and square retain their earlier attribution.

## 4. A legal exact-locus comparison by backward heat and sign intervals

Set, throughout the rest of the proof,
\[
 t=10^{-20},\qquad \varepsilon=10^{-180},\qquad
 Q_t=e^{-t\partial_z^2},\qquad K=1+112t.                 \tag{19}
\]
Start with an actual simple profile (x) in (3), with (u^2+v^2\le\varepsilon).
Erase only the two odd residual coefficients in (4):
\[
 f_0=f+uz^5/3-(u/6-v/5)z^3.
\]
We do **not** assume (f_0) is real-rooted. Instead we will prove that
(Q_t f_0) is real-rooted by comparing it with the known real-rooted
(Q_t f). The general heat identity is
\[
\begin{split}
Q_t f={}&z^8-(1/2+56t)z^6-(u/3)z^5
 +(2E+15t+840t^2)z^4\\
&+(u/6-v/5+20ut/3)z^3
 +(4G-24Et-90t^2-3360t^3)z^2\\
&+(8J-ut+6vt/5-20ut^2)z
 +c-8Gt+24Et^2+60t^3+1680t^4.                           \tag{20}
\end{split}
Both heated monic polynomials have zero seventh coefficient and square
sum (K). The erased one has zero fifth and third coefficients, and
thus zero third and fifth root moments, if its roots are real.

Here is the quantitative separation used for the sign test. Let
(b_1(s)<\cdots<b_8(s)) be the roots of (Q_s f), for (s>0).
The credited strict heat-preserver proof makes these simple for every
positive time. Differentiating their equation gives
\[
 b_i'(s)=2\sum_{j\ne i}\frac1{b_i-b_j}.
\]
If the gap (g=b_{i+1}-b_i) is minimal among all seven gaps, the left and
right exterior terms give
\[
 g'\ge\frac4g-\frac2g\left(
       \sum_{k=1}^{i-1}\frac1{k(k+1)}
       +\sum_{k=1}^{7-i}\frac1{k(k+1)}\right)
     =\frac2g\left(\frac1i+\frac1{8-i}\right)\ge\frac1g.       \tag{21}
\]
The minimum of finitely many smooth gaps is locally Lipschitz on each
positive-time compact interval. At almost every time its derivative is
that of a minimizing gap. Thus its squared minimum has derivative at
least (2) almost everywhere. Integrating from any (s_0>0), then
letting (s_0\downarrow0), proves
\[
              \min_i(b_{i+1}(t)-b_i(t))\ge\sqrt{2t}.      \tag{22}
\]
No initial minimum-gap assumption is used.

Let (r=\sqrt{t/8}=\sqrt{2t}/4). The eight intervals
([b_i(t)-r,b_i(t)+r]) are disjoint. At each endpoint the product
(Q_tf(z)=\prod_j(z-b_j(t))) has magnitude at least (r^8=t^4/4096):
the own-root distance is (r), and every other distance is at least
(\sqrt{2t}-r=3r). The signs at the two endpoints of each interval are
opposite. Moreover \(\sum b_i(t)^2=K<9/4\) and (r<1/2), so all endpoints
have absolute value less than (2).

The **entire** discrepancy is
\[
 Q_t(f-f_0)=-\frac u3(z^5-20tz^3+60t^2z)
             +(u/6-v/5)(z^3-6tz).                     \tag{23}
\]
At (|z|\le2), (0<t\le1), and (|u|,|v|\le\sqrt\varepsilon),
\[
 |Q_t(f-f_0)|\le\sqrt\varepsilon\left(
  (32+160+120)/3+(8+12)/6+(8+12)/5\right)
 =\tfrac{334}3\sqrt\varepsilon
 <112\sqrt\varepsilon<t^4/4096.                         \tag{24}
\]
The last strict inequality is a rational comparison for (19).
It preserves both endpoint signs of each interval. The intermediate
value theorem supplies a root of (Q_t f_0) in each of the eight
intervals. A degree-eight polynomial cannot have further roots or a
multiple root in these intervals: the eight distinct real roots already
exhaust its degree. This is the original-root licence missing from naive
coefficient erasure.

Normalize these eight roots by \(\sqrt K\) and call their ordered vector
(y). It is balanced, unit, simple, and has third and fifth moments zero.
Its two relevant even chart coefficients are exactly
\[
 E_y=(E+15t/2+420t^2)/K^2,\qquad
 G_y=(G-6Et-45t^2/2-840t^3)/K^3.                         \tag{25}
\]
Its remaining coefficients are whatever the licensed primitive gives;
they are not assumed to maximize the angular quotient.

## 5. Coefficient perturbation and the cleared sign margin

For (x) in (3), (0<E<1/16), (|u|\le1) and (0\le\mu_6\le1).
The sixth moment identity below (6) gives
\[
 |G|\le(1/4+6/16+1/3+1)/24<1/8.
\]
Using (K\ge1), (25), and (t=10^{-20}), we obtain
\[
\begin{split}
 |E_y-E|&\le t(43/2+1204t)<24t,\\
 |G_y-G|&\le t(339/8+(9453/2)t+176456t^2)<44t,\\
 |D_y-D|&=8|E_y-E|<192t.                               \tag{26}
\end{split}
For the first inequality expand (K^2-1=224t+12544t^2).
For the second expand (K^3-1=336t+37632t^2+1404928t^3).
Since (192t<1/1352) and (192t<3/100-3/112=9/2800),
(3) and (26) place (y) inside (10). In particular (0<E_y<1/16).

Equations (5)--(6), (u^2\le\varepsilon), (|uv|\le\varepsilon/2),
and (26) now imply entrywise
\[
 \max_{i,j}|(A_x-A_y)_{ij}|\le\beta:=320t+\varepsilon,
 \quad \max_i|(w_x-w_y)_i|\le\gamma:=1152t+\varepsilon,
 \quad |D-D_y|\le d:=192t.                             \tag{27}
\]
For clarity the fourth, sixth and eighth trace time budgets are (96),
(318), and (171); the residual budgets are (25/192) and
(5/192+1/16), both below (1). For the eighth trace use
(|E^2-E_y^2|\le(1/8)|E-E_y|).
The fourth coupling time budget is (4(24)+24(44)=1152), and its residual
budget is (5/24<1). These are bounds for the actual general Gram;
no discriminant inequality has been imposed off the exact locus.

For either normalized actual vector, \(\|H\|\le1\).
Consequently every entry of (A) has absolute value at most (7), and
every entry of (w) has absolute value at most (1).
Literal three-by-three determinant expansion and two-by-two cofactors give
\[
 |\det A_x|\le2058,\quad
 |\det A_x-\det A_y|\le882\beta,\quad
 |\operatorname{adj}(A_x)_{ij}|\le98,\quad
 |\operatorname{adj}(A_x)_{ij}-\operatorname{adj}(A_y)_{ij}|\le28\beta.       \tag{28}
\]
The telescoping product bound uses three factors for the determinant and
two for each cofactor; it does not divide by either determinant.
The exact scalar inequality (882\beta<\delta), together with (14),
proves (\det A_x>0). Since (A_x) is a real Gram, it is positive
definite, licensing (8)--(9) for (x).

We have (0<TD_y<1). Telescoping the two terms of (9), using (27)--(28),
therefore gives
\[
\begin{split}
 |\Psi_T(x)-\Psi_T(y)|
 &\le24(2058)d+(882+252)\beta+1764\gamma\\
 &=11878272t+2898\varepsilon
 <12000000t+3000\varepsilon<M.                          \tag{29}
\end{split}
In the quadratic term there are nine entries: each cofactor difference
costs (28\beta), and the two vector differences cost (196\gamma).
The last inequality in (29) is the explicit rational comparison with
(M=(2/9)(1/1352)(1/20000000)) from (18).
It follows that (\Psi_T(x)>0), and hence (C(x)<T=70/3) on (3).
Combining with (2) proves (1) on the simple real locus.

## 6. All multiplicities, evidence and open frontier

The normalized heat flow from the credited heat/Hermite reduction has
\[
 u_s=u/(1+112s)^{3/2},\quad
 v_s=(v+60su)/(1+112s)^{5/2}.
\]
Writing (W=v+60su), its squared residual derivative is
\[
 -\frac{60((1+112s)u-W)^2+276(1+112s)^2u^2+500W^2}
        {(1+112s)^6}\le0.                              \tag{30}
\]
Thus every closed collar profile, including its residual-equality
boundary, is approached by simple real profiles in the same collar.
The credited full-grouped-mass continuity passes the bound (1) to all
original and critical collisions. Uniform profiles have the separate
value (16<70/3). No zero discriminant has been cancelled, and no full
mass has been split across a repeated eigenspace.

[check.py](check.py) uses Python standard-library rational arithmetic to
check every coefficient of the general even traces, general coupling
moments, heat polynomial and odd-erasure discrepancy; the direct projected
cube formula separately verifies the coupling. It recomputes the small
determinant/adjugate, both whole boundary factors, the credited full
envelope polynomial, and every rational margin in (24)--(29).
Its entire external record [expected.json](expected.json) is compared,
not just check totals. These are finite polynomial identities and scalar
budgets, not a root enumeration, real-closed-field sign decision or
formalization of the surrounding ordinary argument.

The new result replaces an existential approximate-moment neighborhood
by one concrete rational collar. It is deliberately conservative;
enlarging it, finding a useful optimal residual dependence, and controlling
the entire balanced sphere remain open here. The general three-row Gram
may aid those improvements. The full complex degree-nine first-power
Tang--Zhang target remains distinct and unresolved by this artifact.
