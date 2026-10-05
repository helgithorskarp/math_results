# A quarter-power residual modulus from two original-root sign groups

Actual author **six-sendov-2 / researcher**, 2026-10-05.
Complete ordinary author argument with new finite rational checks;
**unformalized and independently unreviewed**. No historical priority claim.

## 1. Statement and credited inputs

For a balanced unit \(x\in\mathbb R^8\) put \(\mu_k=\sum_i x_i^k\),
\(P=I-\mathbf1\mathbf1^T/8\), and
\(H=(P\operatorname{diag}(x)P)|_{\mathbf1^\perp}\).
At each distinct eigenvalue use its **full** mass
\(m_\lambda=\|\Pi_\lambda x\|^2\); put \(\eta=\sum m_\lambda^2\),
\(D=\mu_4-1/8\), and \(C=(1-\eta)/D\) for \(D>0\).
At the uniform four-positive/four-negative profiles the credited continuous
extension is \(\widetilde C=16\). Definitions and full grouped continuity
are [7432](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md)
and [8753](../angular-three-level-transition/PROOF.md).

**Theorem.** With \(R=\mu_3^2+\mu_5^2\), every such actual profile,
including all original and critical multiplicities, satisfies
\[
 \boxed{R\le10^{-96}\quad\Longrightarrow\quad
 \widetilde C\le208/9+4\cdot10^{27}R^{1/4}.}                       \tag{1}
\]
Consequently
\[
 R\le10^{-114}\implies\widetilde C<70/3,\qquad
 R\le10^{-116}\implies\widetilde C\le5209/225.                     \tag{2}
\]
The first collar is 34 decimal orders wider than the previous \(10^{-148}\)
collar, and 66 wider than the first explicit \(10^{-180}\) collar.
These conservative estimates do not resolve the unrestricted complex
degree-nine first-power inequality or the whole balanced real sphere.
The exact-locus value \(208/9\) is prior [8672](../triple-angular-persistence/PROOF.md)
and [the sharp odd-zero result](../sharp-odd-moment-angular-bound/PROOF.md).

The [published one-eighth modulus](../odd-moment-holder-modulus/PROOF.md),
source `e81cb9000b2ab8cab58af4f717e0737f80c28c77`, supplies the general
Gram, enlarged-band positive floor, arbitrary-time coefficient estimates,
cleared numerator estimate, exact-zero branch and closed-collar density.
We credit its [collar source](../explicit-odd-moment-collar/PROOF.md) too.
The new ingredient is an original-root **two-sign-group** licence at a new
variable heat time. All changed powers and scalar inequalities are checked
here; no parent mathematical executable is imported or replayed.

The extra published input is [8851, Theorem A and Section 3](../sign-count-angular-reduction/PROOF.md),
source `cc7d41fb91dc7c00f29baf1083fbfb1f575bf308`:
\[
 \min(\#\{z_i>0\},\#\{z_i<0\})\le3
       \quad\Longrightarrow\quad X(z):=\sum z_i^4\ge13/84        \tag{3}
\]
for every balanced unit real eight-vector. In particular this applies to
every such vector with a zero coordinate. The moment inequality is prior
work, not a new result here. Its angular bound with at most four levels is
not used, and no private earlier root-box proof is a premise.

## 2. Quantified distance from a zero-coordinate face

Let \(z\) be an actual balanced unit real eight-vector with
\[
                        X(z)\le103/672.                         \tag{4}
\]
Since \(103/672<13/84\), (3) forces exactly four strictly positive and
four strictly negative coordinates. Here is also an explicit lower bound
for every coordinate, without odd-moment hypotheses.

For coordinate \(j\), write \(a_j=e_j-\mathbf1/8\); then
\(\|a_j\|^2=7/8\) and \(z\cdot a_j=z_j\). Project orthogonally onto
the subspace of balanced vectors whose \(j\)th coordinate is zero:
\[
 w=z-\tfrac87z_j a_j,\qquad
 \beta^2=\tfrac87z_j^2,\qquad \|w\|^2=1-\beta^2.                 \tag{5}
\]
The inequality \(X(z)<1/4\) gives \(z_j^2\le\sqrt{X(z)}<1/2\),
so \(\beta^2<4/7<1\). In particular \(w\ne0\). The vector
\(v=w/\|w\|\) is balanced, unit and has a zero. Orthogonality gives
\[
 \|z-v\|^2=2(1-\sqrt{1-\beta^2})\le2\beta^2<4z_j^2.             \tag{6}
\]
On the unit ball the gradient of \(X\) has norm
\(4\sqrt{\sum t_i^6}\le4\). The segment joining \(z,v\) remains in
that ball, so \(|X(v)-X(z)|\le4\|v-z\|\le8|z_j|\).
By (3), \(X(v)\ge13/84=104/672\). Therefore
\[
                         |z_j|\ge1/5376.                        \tag{7}
\]
Every coordinate has four opposite-sign coordinates separated from it by
at least \(1/2688\). This bound concerns actual originals, not critical
square nodes or the unlicensed erased primitive.

## 3. Apply the geometry before erasing the odd coefficients

The credited [universal localization](../universal-angular-localization/PROOF.md)
gives \(C\le5560/243<208/9\) when \(0<D\le1/676\), and
\(C\le23<208/9\) when \(D\ge3/112\). The uniform value is 16.
Thus start with simple actual originals in
\(1/676<D<3/112\), with \(R>0\), and set
\[
               t=10^{10}R^{1/4},\quad t_*=10^{-14},
               K=1+112t,\quad r=\sqrt{t/8}.                     \tag{8}
\]
The domain in (1) gives \(0<t\le t_*\). Use the general monic chart
\[
 f=z^8-z^6/2-uz^5/3+2Ez^4+(u/6-v/5)z^3+4Gz^2+8Jz+c,
 \quad u=\mu_3, v=\mu_5, D=3/8-8E.                             \tag{9}
\]
Let \(Q_t=e^{-t\partial_z^2}\). The credited
[strict heat-preserver](../heat-hermite-angular-reduction/PROOF.md) makes
\(Q_tf\) real-rooted and simple. Its ordered actual roots \(b_i\) satisfy
\(\sum b_i=0\), \(\sum b_i^2=K\), and the published root-ODE mesh
\(b_{i+1}-b_i\ge\sqrt{2t}=4r\).

Normalize these **known real** roots to \(z=b/\sqrt K\), before any
erasure. Its even coefficient is
\[
 E_z=(E+15t/2+420t^2)/K^2,
 \quad |E_z-E|<24t,
 \quad |D_z-D|<192t.                                           \tag{10}
\]
The variable-time estimate in (10) is paid through \(t_*\) in the credited
source and involves no odd erasure or real-root assumption on \(f_0\).
The new comparison \(192t_*<1/672\) gives
\[
 X(z)=1/8+D_z<1/8+3/112+1/672=103/672.                          \tag{11}
\]
Thus Section 2 applies to the actual heated roots. Each \(b_i\) has four
opposite-sign roots at distance at least \(1/2688\), since \(\sqrt K\ge1\).

Erase only the \(z^5,z^3\) coefficients of \(f\), obtaining \(f_0\).
It is not assumed real-rooted. At either endpoint \(b_i\pm r\), four
opposite-sign-root distances are at least \(1/2688-r\ge1/5376\), using
the new inequality \(r\le1/5376\). The remaining three other-root
distances are at least \(3r\) by the mesh. The own-root distance is \(r\).
Consequently
\[
 |Q_tf(b_i\pm r)|\ge\frac{27r^4}{5376^4}
                         =\frac{27t^2}{64\cdot5376^4}.          \tag{12}
\]
The intervals \([b_i-r,b_i+r]\) are disjoint and their endpoint signs
are opposite. The credited \(K<9/4,r<1/2\) bounds put all endpoints in
\((-2,2)\). The entire discrepancy is
\[
 Q_t(f-f_0)=-\tfrac u3(z^5-20tz^3+60t^2z)
                     +(u/6-v/5)(z^3-6tz),                     \tag{13}
\]
whose magnitude there is at most \((334/3)\sqrt R<112\sqrt R\).
But \(t^2=10^{20}\sqrt R\), and the new rational inequality
\[
                         112<\frac{27\cdot10^{20}}{64\cdot5376^4} \tag{14}
\]
makes (12) strictly larger. Every endpoint sign survives. The intermediate
value theorem gives eight distinct real roots of \(Q_tf_0\), exhausting
its degree. After division by \(\sqrt K\), they form an actual simple
balanced unit profile \(y\) with exactly zero third and fifth moments.
The comparison uses no feasible even-centered primitive assumption.

## 4. The paid Gram bounds at the new time

The coefficient formulas for licensed \(y\) are
\(E_y=E_z\) and
\(G_y=(G-6Et-45t^2/2-840t^3)/K^3\).
The published brackets give \(|E_y-E|<24t\), \(|G_y-G|<44t\),
\(|D_y-D|<192t\). With \(192t_*<1/1352\) and \(192t_*<9/2800\),
\(y\) lies in the enlarged exact band \([1/1352,3/100]\).
Its actual three-row even Gram satisfies
\(\det A_y>1/20000000\), \(B_y\le208/9\). These are credited enlarged-band
lemmas, ultimately using [10105](../two-moment-parity-descent/PROOF.md)'s
critical-only horizontal continuation and the sharp exact envelope.

For clarity the same general matrix is
\(A=(\operatorname{tr}H^{2(i+j)})_{i,j=0}^2\),
\(w=(x^Tx,x^TH^2x,x^TH^4x)^T\), and, once \(A>0\),
\(B_x=(1-w^TA^{-1}w)/D\ge C(x)\).
The coefficient/determinant estimates only require \(t\le t_*\) and
\(R\le t\); they do not require the earlier relation \(R=t^8\).
Here \(R=(t/10^{10})^4\le t\), so the same budgets are
\[
 \|A_x-A_y\|_{\max}\le321t,\qquad
 \|w_x-w_y\|_{\max}\le1153t,
 \qquad \det A_x>1/40000000.                                  \tag{15}
\]
The determinant is positive before using any inverse: its loss is at most
\(882\cdot321t_*<1/40000000\), and both matrices are actual real Grams.
With \(T_0=208/9\), the cleared polynomial
\(\Psi=(T_0D-1)\det A+w^T\operatorname{adj}(A)w\)
satisfies \(\Psi(y)\ge0\) and
\[
 |\Psi(x)-\Psi(y)|\le11881170t<13000000t.                        \tag{16}
\]
The quoted budgets are explicit ordinary published inputs, with exact
source pins, rather than a replay of their closed checker. Dividing only
by \(D>1/676\) and the proved determinant floor yields
\[
 C(x)<208/9+351520000000000000t
       =208/9+351520000000000000\cdot10^{10}R^{1/4}
       <208/9+4\cdot10^{27}R^{1/4}.                             \tag{17}
\]
This proves (1) on the simple locus with positive residual.

## 5. Zero residual, every collision and evidence limits

For \(R=0\), the central profile itself is in the enlarged exact band;
the credited positive-Gram envelope gives \(C\le208/9\). Outside the
central band use the universal bounds. No division by \(R\) or heat time
is made at zero.

For a nonsimple original profile, normalized backward heat gives simple
balanced unit \(x(s)\to x\), with
\(u_s=u/(1+112s)^{3/2}\), \(v_s=(v+60su)/(1+112s)^{5/2}\).
Writing \(W=v+60su\), the credited identity is
\[
 R_s'=-\frac{60((1+112s)u-W)^2+276(1+112s)^2u^2+500W^2}
                  {(1+112s)^6}\le0.                           \tag{18}
\]
Thus \(R_s\le R\le10^{-96}\), including its equality boundary. Apply
the simple bound and \(R_s^{1/4}\le R^{1/4}\), then full grouped continuity
passes (1) to the limit. If \(R=0\), also \(R_s=0\). The uniform value16
is handled separately. No full eigenspace mass is split across a collision,
and no zero discriminant is cancelled.

For (2), the exact comparison
\((4\cdot10^{27})^4 10^{-114}<(2/9)^4\) gives the strict \(70/3\) bound.
At \(R\le10^{-116}\), the error is at most
\(4\cdot10^{27}10^{-29}=1/25\), giving \(208/9+1/25=5209/225\).

[check.py](check.py) validates the new rational projection constants,
quartic bands, radius/product licence, fourth-root time scaling and
corollaries. The entire external record is compared. It imports no parent
mathematics and does not formalize the ordinary projection, root ODE,
intermediate-value, Gram or continuity arguments. No parent review transfers.
The gain is a quarter-power dependence from four uniformly distant root
factors; constants and exponent optimality remain open here.
