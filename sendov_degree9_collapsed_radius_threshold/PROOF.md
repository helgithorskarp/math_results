# The sharp local radius threshold for the collapsed degree-nine family

Author: **six-sendov-2**, role **researcher**. Date: 2026-09-30.

Status: ordinary mathematical proof with an exact finite algebra checker.
The contour and norm arguments below are part of the written proof; the
checker is not a formal proof or an independent research review.

## 1. Statement and normalization

Let

\[
p(z)=C(z-a)\prod_{k=1}^8(z-z_k),\qquad C\ne0,
\quad 5/8<a\le1,\quad |z_k|\le1.
\]

Assume the marked root is simple and put

\[
v=\frac1{1+a},\quad u_k=\frac1{a-z_k},\quad
\delta_k=u_k-v,\quad E=\sum_{k=1}^8|\delta_k|^2,
\quad\epsilon=\max_k|\delta_k|,\quad
\kappa=(1+a)(a-5/8)>0.
\]

List all eight derivative zeros with multiplicity as \(\zeta_j\), and let
\(F(a)=\sum_j|a-\zeta_j|^{-1}\).

**Theorem 1 (quantitative local lower bound).** If
\(\epsilon\le\kappa/13000\), then

\[
\boxed{F(a)\ \ge\ \frac{16}{1+a}+\frac\kappa2 E.}\tag{1}
\]

Equality in the radial baseline \(F(a)=16/(1+a)\) holds exactly when
\(p(z)=C(z-a)(z+1)^8\). A sufficient hypothesis in original root
coordinates is

\[
\max_k|z_k+1|\le\kappa/5000.\tag{2}
\]

Thus every fixed marked radius greater than \(5/8\) has an explicit
neighborhood of its antipodal collapsed family with this stronger
first-power inequality. No upper bound on \(F\), surplus assumption,
reflection symmetry, or restriction on derivative arguments is required.
Other roots and derivative zeros may be repeated.

For a complex marked root \(\alpha\) of modulus \(a>5/8\), set
\(\omega=\alpha/a\) and rotate by \(\bar\omega\). In (1) use
\(u_k=\omega/(\alpha-z_k)\), and in (2) use
\(|z_k+\omega|\). The equality family is
\(C(z-\alpha)(z+\omega)^8\). Rotation preserves every distance and
multiplicity. The antipode is \(-\omega\).

**Theorem 2 (sharpness of the radius threshold).** For every
\(0\le a\le5/8\) and \(99/100\le c<1\), the degree-nine polynomial

\[
p_{a,c}(z)=(z-a)(z^2+2cz+1)^4\tag{3}
\]

has all roots in the closed unit disk and satisfies

\[
F_{a,c}(a)<\frac{16}{1+a}.\tag{4}
\]

As \(c\uparrow1\), its other roots tend to \(-1\). Hence no
neighborhood of the collapsed family at or below radius \(5/8\) can
satisfy the radial baseline for all disk-rooted perturbations. This is an
obstruction to that stronger baseline, not to the conjecture \(F\ge8\).

## 2. Exact disk geometry and a reciprocal matrix

Write \(b=1-a^2\), \(A=\sum\Re\delta_k\), and
\(\ell=\sum_j(|q_j|-\Re q_j)\ge0\), where
\(q_j=(a-\zeta_j)^{-1}\). The disk condition for a single other root is

\[
b|u_k|^2+2a\Re u_k-1\ge0.
\]

Indeed multiplying by \(|u_k|^{-2}\) gives
\(1-|a-u_k^{-1}|^2\ge0\). Since
\(bv^2+2av-1=0\) and \(2bv+2a=2\), it becomes exactly

\[
2\Re\delta_k+b|\delta_k|^2\ge0.\tag{5}
\]

Differentiating
\(p(a+w)=Cw\prod_k(a-z_k)\prod_k(1+u_kw)\) gives
\(e_k(q)=(k+1)e_k(u)\) for \(0\le k\le8\). In particular,

\[
\sum_jq_j=2\sum_ku_k=16v+2\sum_k\delta_k,
\qquad F-16v=2A+\ell.\tag{6}
\]

The marked root is simple, so \(p'(a)\ne0\); all these reciprocals are
finite. Let \(J\) be the eight by eight all-one matrix and define

\[
H=I+J,\qquad S=I+J/4,\qquad P=I-J/8,\qquad Q=J/8.
\]

Here \(S^2=H\), \(P,Q\) are orthogonal projections of ranks seven and
one, and \(SP=P\). With \(D_u=\operatorname{diag}(u_k)\), the
rank-one determinant identity gives

\[
\det(tI-D_uH)=\prod_k(t-u_k)
 \left(1-\sum_k\frac{u_k}{t-u_k}\right)
 =\sum_{k=0}^8(-1)^k(k+1)e_k(u)t^{8-k}.\tag{7}
\]

The displayed rational identity extends as a polynomial identity even
when some \(u_k\) coincide. It agrees with the reciprocal derivative
polynomial. Consequently the \(q_j\) are precisely the eigenvalues,
with algebraic multiplicity, of

\[
B=S D_u S=vH+V,\qquad V=S\operatorname{diag}(\delta_k)S.\tag{8}
\]

In fact \(S^{-1}BS=D_uH\). This use of a diagonal matrix plus a
rank-one perturbation is classical; the representation itself is not a
novelty claim. The Euclidean operator norm obeys
\(\|V\|\le9\epsilon\), since \(S\) has eigenvalues one and three.
The Hermitian matrix \(vH\) has eigenvalues \(v\) seven times and
\(9v\) once; their gap \(8v\) is at least four.

## 3. A squared moment for the seven-eigenvalue cluster

As \(0<\kappa\le3/4\), our hypothesis implies
\(\epsilon\le3/52000<1/10000\). On the positively oriented circle
\(|\lambda-v|=1\), put

\[
R_0(\lambda)=\frac{P}{\lambda-v}+\frac{Q}{\lambda-9v}.
\]

Its norm is at most one, because the two spectral distances are one and
at least three. For \(0\le s\le1\),
\(I-sR_0V\) is invertible by its norm-convergent geometric series.
Thus \(vH+sV\) has no eigenvalue on the circle. The winding number of
its determinant is constant in \(s\), so exactly seven eigenvalues of
\(B\) lie inside, counted with algebraic multiplicity.

Moreover, every eigenvalue of \(B\) is within \(9\epsilon\) of the
two-point spectrum of \(vH\). Otherwise
\(\|(\lambda I-vH)^{-1}V\|<1\), which makes
\(\lambda I-B\) invertible. Since the disk about \(9v\) lies outside
our circle, each of the seven clustered eigenvalues obeys

\[
|q_j-v|\le9\epsilon,\qquad |q_j|\le v+9\epsilon.\tag{9}
\]

Define the cluster moment

\[
T_2=\frac1{2\pi i}\int_{|\lambda-v|=1}
 (\lambda-v)^2\operatorname{tr}(\lambda I-B)^{-1}\,d\lambda
 =\sum_{\mathrm{cluster}}(q_j-v)^2.\tag{10}
\]

The trace resolvent identity follows by differentiating the determinant:
\(\operatorname{tr}(\lambda I-B)^{-1}=
\sum_j(\lambda-q_j)^{-1}\). It holds away from the spectrum, including
for nonnormal matrices and repeated eigenvalues. Thus (10) does not
require individually differentiable eigenvalue branches.

Expand the uniformly convergent resolvent series

\[
(\lambda I-B)^{-1}
 =\sum_{m\ge0}R_0(VR_0)^m.
\]

After multiplication by \((\lambda-v)^2\), the orders zero and one
have no residue at \(v\). At order two, expand the three resolvent
factors into \(P/(\lambda-v)\) and \(Q/(\lambda-9v)\).
Cyclicity of trace makes a word vanish when its first and last
projections differ. The word \(PPP\) contributes
\(\operatorname{tr}[(PVP)^2]\). The word \(PQP\) has denominator
\((\lambda-v)^2(\lambda-9v)\), so its cluster pole is canceled.
The words \(QPQ, QQQ\) are analytic at \(v\) after multiplication.
This lists every surviving word. The order-two residue is therefore
exactly \(\operatorname{tr}[(PVP)^2]\).

For the remaining orders, \(|\operatorname{tr}M|\le8\|M\|\)
and the contour radius is one. Since \(\epsilon^2\le E\),

\[
\left|T_2-\operatorname{tr}[(PVP)^2]\right|
 \le\frac{8(9\epsilon)^3}{1-9\epsilon}
 \le6000\epsilon E.\tag{11}
\]

The last constant follows already from \(\epsilon\le1/10000\).
All three estimates are exact bounds, not eigenvalue sampling.

Since \(SP=P\), elementary matrix multiplication gives

\[
\operatorname{tr}[(PVP)^2]
 =\frac34\sum_k\delta_k^2+
   \frac1{64}\left(\sum_k\delta_k\right)^2.\tag{12}
\]

For completeness, writing \(D=\operatorname{diag}(\delta_k)\),
cyclicity reduces the left side to \(\operatorname{tr}(DPDP)\).
Expand \(P=I-J/8\), use
\(\operatorname{tr}(D^2J)=\operatorname{tr}(DJD)=\sum\delta_k^2\)
and \(\operatorname{tr}(DJDJ)=(\sum\delta_k)^2\).

## 4. Coercivity from the disk constraint

The case \(E=0\) is the collapsed polynomial. Its derivative is
\(C(z+1)^7(9z+1-8a)\), so its critical reciprocals are
\(v\) seven times and \(9v\) once. It has \(F=16v\).
Assume now \(E>0\).

If \(A\ge\kappa E/4\), (6) immediately gives (1).
Otherwise let \(N\) be the sum of the negative parts of
\(\Re\delta_k\). By (5), \(N\le bE/2\), hence

\[
\sum_k|\Re\delta_k|=A+2N
 \le(\kappa/4+b)E\le E.\tag{13}
\]

For the last inequality it suffices that
\(b\le39/64\) and \(\kappa/4\le3/16\), whose sum is
\(51/64<1\). If \(R=\sum(\Re\delta_k)^2\) and
\(Y=\sum\Im\delta_k\), then (12) yields

\[
-\Re\operatorname{tr}[(PVP)^2]
 =\frac34E-\frac32R-\frac{A^2}{64}+\frac{Y^2}{64}
 \ge\frac34E-2E^2.\tag{14}
\]

Indeed \(R,A^2\le(\sum|\Re\delta_k|)^2\le E^2\), and
\(3/2+1/64=97/64<2\). Combining (10), (11), and (14),

\[
\sum_{\mathrm{cluster}}(\Im q_j)^2
 =\sum_{\mathrm{cluster}}(\Re(q_j-v))^2-\Re T_2
 \ge(3/4-6000\epsilon-2E)E.\tag{15}
\]

For every complex number \(q\),

\[
(\Im q)^2=(|q|-\Re q)(|q|+\Re q)
 \le2|q|(|q|-\Re q).
\]

This inequality also holds on the negative real axis without dividing
by \(|q|+\Re q\). Applying (9) and summing the seven nonnegative
angular losses gives

\[
\ell\ge\frac{3/4-6000\epsilon-2E}{2(v+9\epsilon)}E.\tag{16}
\]

The numerator is positive under our bounds; positivity is not needed
for the validity of the preceding inequality. Summing (5) gives
\(2A\ge-bE\). Thus

\[
F-16v\ge
 \left(\frac{3/4-6000\epsilon-2E}{2(v+9\epsilon)}-b\right)E.
\]

The leading coefficient is exactly

\[
\frac{3}{8v}-b=(1+a)(a-5/8)=\kappa.\tag{17}
\]

Since \(v\ge1/2\), \(E\le8\epsilon^2\), and
\(\epsilon<1\), the loss from that leading coefficient is at most

\[
\frac{27\epsilon}{8v(v+9\epsilon)}
 +\frac{6000\epsilon+2E}{2(v+9\epsilon)}
 \le\frac{27}{2}\epsilon+6000\epsilon+16\epsilon^2
 \le6030\epsilon\le\frac\kappa2.\tag{18}
\]

The last inequality uses \(6030/13000<1/2\). This proves (1).
It also proves the stated baseline equality classification: any
\(E>0\) gives a strictly positive gap.

To verify (2), put \(\rho=\kappa/5000\le3/20000\).
Then \(z_k\ne a\), and

\[
|u_k-v|=\frac{|z_k+1|}{(1+a)|a-z_k|}
 \le\frac{\rho}{(1+a)(1+a-\rho)}
 \le\frac{\kappa}{13000},
\]

because
\((13/8)(13/8-3/20000)>13/5\).
This completes Theorem 1.

## 5. An exact family violating the radial baseline

Let \(g(z)=z^2+2cz+1\) and use (3). Its other roots
\(-c\pm i\sqrt{1-c^2}\) are on the unit circle, four times each.
Direct differentiation gives

\[
p_{a,c}'(z)=g(z)^3
 \bigl(9z^2+(10c-8a)z+1-8ac\bigr).\tag{19}
\]

Set \(D=a^2+2ac+1\). The six critical points from \(g^3\)
each have distance \(\sqrt D\) from \(a\). If \(r_1,r_2\)
are the reciprocals of the distances with sign, namely
\(r_i=(a-\zeta_i)^{-1}\), for the two remaining critical points,
substitution in the quadratic in (19) gives

\[
D r^2-10(a+c)r+9=0.\tag{20}
\]

They are real and strictly positive: their product is \(9/D>0\),
their sum is \(10(a+c)/D>0\), and their discriminant is positive.
Indeed \(D\le(1+a)^2\) and
\(a+c\ge(99/100)(1+a)\), so
\(25(a+c)^2>9D\). Thus exactly, throughout the stated range,

\[
F_{a,c}(a)=\frac6{\sqrt D}+\frac{10(a+c)}D.\tag{21}
\]

View (21) as a function of \(c\). Its derivative is

\[
\frac{dF}{dc}=\frac{10(1-a^2)-6a\sqrt D}{D^2}.\tag{22}
\]

For \(0\le a\le5/8\),

\[
10(1-a^2)-6a(1+a)=(1+a)(10-16a)\ge0.
\]

If \(a<5/8\), this numerator lower bound is strictly positive.
If \(a=5/8\) and \(c<1\), then \(\sqrt D<1+a\), so the
actual numerator in (22) is again strictly positive. Consequently
\(F_{a,c}(a)<F_{a,1}(a)=16/(1+a)\), proving Theorem 2, including
the threshold value itself.

The same exact formula quantifies sharpness. With \(c=\cos t\),
for every fixed \(0\le a\le1\) as \(t\to0\),

\[
F_{a,\cos t}(a)=\frac{16}{1+a}
 +\frac{8(a-5/8)}{(1+a)^3}t^2+O(t^4).\tag{23}
\]

The corresponding reciprocal energy is exactly
\(E=16(1-c)/[D(1+a)^2]\). To see this, use the conjugate
reciprocals \((a+c\mp i\sqrt{1-c^2})/D\) and the identity
\[
 ((a+c)(1+a)-D)^2+(1+a)^2(1-c^2)=2(1-c)D.
\]
In particular \(E=8t^2/(1+a)^4+O(t^4)\). Thus for \(a>5/8\),
\((F-16/(1+a))/E\to\kappa\). In particular a uniformly valid
local coefficient of \(E\) cannot exceed \(\kappa\); (1) obtains
half that limiting coefficient with a coarse explicit radius.
At the threshold the next term is negative:

\[
F_{5/8,\cos t}(5/8)=\frac{128}{13}
 -\frac{9600}{13^5}t^4+O(t^6).\tag{24}
\]

Equations (23)--(24) follow by ordinary Taylor expansion of the explicit
positive-denominator expression (21), not by numerical root fitting.

## 6. Boundary equality and the quadratic theorem

At \(a=1\), Theorem 1 is the local quantitative strengthening
\(F\ge8+3E/8\) around \((z-1)(z+1)^8\). The known other
boundary first-power equality family \(z^9-\omega\),
\(|\omega|=1\), lies outside this collapsed neighborhood. We do not
claim a new global equality classification; see the cited team
[boundary classification](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_polar/PROOF.md)
and [two-family stability proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_two_family_boundary_stability/PROOF.md).
For \(a<1\), (1) implies \(F>8\) in the explicit neighborhood.

Zhang's [quadratic theorem](https://arxiv.org/html/2609.19126)
concerns \(\sum|q|^2\ge8\), with equality only for the regular
binomial family. It does not imply the first-power bound here.
For example, the collapsed model at \(a=1\) has
\(q=(1/2,\ldots,1/2,9/2)\), \(F=8\), and
\(\sum|q|^2=22\). Neither the quadratic equality statement nor
the all-degree Sendov theorem supplies (1) or the local threshold (4).

## 7. Optional routing from the earlier small-surplus reduction

Only this corollary uses the published
[interior surplus stability theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_interior_surplus_stability/PROOF.md),
source commit f50b95513b861e739eaf37de6d091d1e90850917, graph
bafkreibb4oxxoah7p6xb5xtvmsc66r7u4jeine3xwxwvcnip6nrinydk2e,
committed height 7260; its independent review was pending when this
proof was prepared. Theorems 1 and 2 are self-contained.

In that reduction, let \(a=1-\eta\), \(\sigma\ge0\),
\(F\le8+\sigma\), \(0<h=\eta+\sigma\le10^{-18}\), and take
the collapsed branch \(L=e_2(r_1-1/2,\ldots,r_8-1/2)<1\),
where \(r_j=|q_j|\). The earlier proof gives
\(\sum|u_k-1/2|^2\le11\cdot10^6h\). Hence

\[
E\le2\sum|u_k-1/2|^2+16(v-1/2)^2
 \le23\cdot10^6h.
\]

Here \(v-1/2=\eta/[2(2-\eta)]\le\eta/2\) and
\(\kappa\ge1/2\). Since
\(23\cdot10^6\cdot10^{-18}<1/26000^2\),
\(\epsilon\le\sqrt E<\kappa/13000\). Theorem 1 therefore gives
the exact necessary surplus

\[
\boxed{\sigma\ge\frac{8\eta}{2-\eta}+\frac\kappa2E.}\tag{25}
\]

For \(\eta>0\), the collapsed branch is excluded even when
\(\sigma\le4\eta\). This replaces the earlier collapsed radial
lower coefficient \(4-O(h)\) by the exact model baseline and a
positive energy term. It is a branch reduction for the complementary
analytic lane, not a proof of a global surplus slope four.

## 8. Evidence and remaining boundary

`verify.py` checks all small matrix identities, every low-order contour
word, the compressed complex trace, reciprocal characteristic
coefficients, the explicit obstruction's derivative factorization and
reciprocal quadratic, Taylor coefficients, and the rational constants.
It also rejects deliberately altered square-root, trace, radius and
threshold coefficients. It uses exact rational sparse polynomials and
standard-library Python; no external data or numerical eigenvalues.

The proof remains ordinary and unformalized. Independent review is
pending. The constants 13000 and 5000 are coarse and no optimal
neighborhood is asserted. At \(a\le5/8\), Theorem 2 blocks the exact
radial baseline, while the first-power endpoint \(F\ge8\) remains a
different question. Away from this explicit collapsed neighborhood and
the previously established regular branch, the general complex
first-power inequality remains unresolved by this contribution.
