# Actual asymmetric family and sharp original-root motion scale

Actual **six-sendov-3 / researcher**, 2026-10-03. Complete ordinary
author proof, **unformalized and independently unreviewed**. The
construction and obstruction below are self-contained. The comparison
with the existing upper estimate explicitly credits that separate result.
Every collar for this construction is existential.

## 1. Statement and prior mathematics

Let

\[
 c=\cos(\pi/9),\quad d=2c^2-1,\quad
 y=\frac1{3(1+c)},\quad x=\frac23-y,\quad C=\frac83+y,
 \qquad \omega_k=e^{2\pi i k/9}.
 \tag{1}
\]

These constants, the balanced leading critical-profile sphere, and the
canonical first-order original motion

\[
 B_k(\eta)=\omega_k+\eta(-\omega_k/3-x-y\omega_k^{-1})
 \tag{2}
\]

are already established in
[8530](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/sharp-boundary-slope/PROOF.md)
and its scoped independent
[8608 review](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/sendov-boundary-audit/REVIEW.md).
They are credited prior results. Here all formulas needed for the
construction are checked directly.

**Theorem.** Define the explicit polynomial family in (5)-(7). There
exists \(\eta_0\in(0,1/12000]\) such that, for **every**
\(0<\eta<\eta_0\), this monic complex degree-nine polynomial has all
nine original roots **strictly** inside the unit disk, all nine originals
simple, and a marked original \(a=1-\eta\). Its eight critical points
consist of one point and seven copies of another. With all critical
multiplicities counted,

\[
 F_p(a)=\sum_{j=1}^8|a-\zeta_j|^{-1}
       =8+C\eta+K\eta^2+O(\eta^3),\qquad
 K=\frac{19935+47482c-62948c^2}{972},\quad 9<K<10.
 \tag{3}
\]

In particular the family satisfies **both** cuts

\[
 F_p(a)\le8+3\eta,\qquad
 F_p(a)\le8+C\eta+\epsilon\eta,
 \quad \epsilon=10\eta,\quad \Delta=\epsilon\eta+192\eta^2=202\eta^2.
 \tag{4}
\]

The unique original branches labeled near \(\omega_k\) obey, for
\(k=3,6\),

\[
 \lim_{\eta\downarrow0}\frac{Z_k(\eta)-B_k(\eta)}{\eta^{3/2}}
 =iA\omega_k,\qquad
 A=\frac{56(1+2c)}{[12(1+c)]^{3/2}}>0.
 \tag{4a}
\]

Consequently no finite uniform constant can bound all-original motion
by \(O(\Delta)\) on the class defined by both cuts. Even an additional
\(o(\sqrt{\eta\Delta})\) term cannot repair such a bound. The
\(\eta^{3/2}\) scale is necessary in this class: on this family
\(|Z_k-B_k|/\sqrt{\eta\Delta}\to A/\sqrt{202}>0\), and no uniform
\(O(\eta^q)\) bound with \(q>3/2\) is possible.

The existing ordinary
[9954 upper estimate](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/full-normal-receiving/PROOF.md)
gives, for all actual complex disk-root polynomials on its full numerical
window and both cuts,
\(|Z_k-B_k|<(19/2)\Delta+(7/2)\sqrt{\eta\Delta}\).
That statement and its separate175 objective/192 physical costs are
credited prior work. It supplies the complementary upper order on this
family; this packet neither re-proves that upper theorem nor gives it an
independent review. No optimal universal motion constant is asserted.
During the major-claim refresh,
[9988](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/full-receiving-audit/REVIEW.md)
independently confirmed the complete9954 theorem relative to its explicit
actual-entry premise. Its complete review and ordinary reconstruction
were read and agree verbatim with its committed signed body. That verdict
does not assess this new construction. Its numerical refinement is not
needed here; (4) preserves9954's original192 physical defect.

The earlier all-profile realization in8530 used a common inward
\(\eta^{3/2}\) repair with an objective cost of that order. The new
construction instead cancels the active odd normals while retaining
nonzero cubic *tangential* motion, then repairs disk containment at
order \(\eta^2\). The cancellation constant below is already the
mixed-moment constant and fourth-order Newton/root-curvature mechanism in
[8619](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/quartic-boundary/PROOF.md)
and its scoped
[8684 review](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/quartic-boundary-audit/REVIEW.md),
then used in
[8921](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/analytic-boundary/PROOF.md),
confirmed in the scoped
[8955 review](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/analytic-minimizer-audit/REVIEW.md).
Their exact6+2 minimizer and stronger fixed cubic-excess classes are
prior mathematics. This1+7 example concerns the broader leading-slope
class (4). It gives no new leading coefficient, optimal second objective
coefficient, critical-profile classification, or global first-power proof.

## 2. An explicit actual polynomial

Set

\[
 \lambda=12(1+c),\quad k=-7(1+2c)/18,\quad g=48k,
 \quad
 M_*=-\frac{512+1684c+1328c^2}{9},\quad
 \beta_* =\frac{86-261c-172c^2}{18}.
 \tag{5}
\]

First allow arbitrary finite real parameters \(M,\beta\). For a real
parameter \(s\), define

\[
\begin{aligned}
 \eta&=\lambda s^2,& a&=1-\lambda s^2,\\
 m&=-x\lambda s^2+ig s^3+Ms^4,\\
 \nu_L&=7is+42ks^2+7i\beta s^3,&
 \nu_S&=-is-6ks^2-i\beta s^3,\\
 \zeta_L&=m+\nu_L,& \zeta_S&=m+\nu_S.
\end{aligned}
 \tag{6}
\]

The final family uses \(M=M_*\), \(\beta=\beta_*\),
\(s=\sqrt{\eta/\lambda}>0\), and

\[
 p_s(z)=9\int_a^z(u-\zeta_L)(u-\zeta_S)^7\,du.
 \tag{7}
\]

This is a polynomial primitive difference, hence path independent and
fully explicit. It is monic of degree9, satisfies \(p_s(a)=0\), and
has the stated eight critical multiplicities exactly. For sufficiently
small nonzero \(s\), \(\zeta_L-\zeta_S=8is+O(s^2)\ne0\).
The centered critical sum is exactly zero:
\(\nu_L+7\nu_S=0\). At \(s=0\), \(p_0=z^9-1\).

All coefficients of (7) are polynomials in \(s,M,\beta\), with real
algebraic constants in \(\mathbb Q(c)\) and powers of \(i\).
Thus (7) is an actual family, rather than an inference of original-root
feasibility from hypothetical critical data. Feasibility is proved in
Section5 after every active radial term has been included.

## 3. Entire second and third jets

Put \(m_2=-x\lambda=-4(1+2c)\), and let
\(T=\nu_L^2+7\nu_S^2\), \(U_3=\nu_L^3+7\nu_S^3\). Direct multiplication gives

\[
 T=-56s^2+672ik s^3+(2016k^2-112\beta)s^4+O(s^5),
 \qquad U_3=-336is^3-6048ks^4+O(s^5).
 \tag{8}
\]

The sum of critical squares, including the mean, is
\(-56s^2+672ik s^3+(8m_2^2+2016k^2-112\beta)s^4+O(s^5)\).
The sum of critical cubes is
\(-336is^3+(-168m_2-6048k)s^4+O(s^5)\), and the fourth
sum is \(2408s^4+O(s^5)\). Newton identities therefore give the
**entire anchored polynomial jet**, coefficientwise in \(z\),

\[
 p_s(z)=z^9-1+s^2P_2(z)+s^3P_3(z)+s^4P_4(z)+O(s^5),
 \tag{9}
\]
\[
\begin{aligned}
 P_2(z)&=9\lambda-9m_2(z^8-1)+36(z^7-1),\\
 P_3(z)&=-9ig(z^8-1)-432ik(z^7-1)+168i(z^6-1),\\
 P_4(z)&=-36\lambda^2+\lambda(-72m_2+252)
              -9M(z^8-1)\\
 &\quad +(36m_2^2-1296k^2+72\beta)(z^7-1)
        +(-252m_2+3024k)(z^6-1)-378(z^5-1).
\end{aligned}
 \tag{10}
\]

All lower-degree terms through order4 are displayed, including the
\(z^5\) term and the constant from evaluating the primitive at the
moving anchor. The complete product/integral and (10) agree exactly in
the checker before any root calculation.

Every root \(\omega=\omega_k\) of \(p_0\) is simple. The analytic
implicit function theorem gives a unique original branch near it, with
convergent expansion

\[
 Z_k(s)=\omega+s^2L_k+s^3W_k+s^4V_k+O(s^5),
 \tag{11}
\]
\[
\begin{aligned}
 L_k&=\lambda(-\omega/3-x-y\omega^{-1}),\\
 W_k&=ig(1+\omega^{-1}-2\omega)
                     -\frac{56i}{3}(\omega^{-2}-\omega),\\
 V_k&=-\frac{P_4(\omega)+P_2'(\omega)L_k
                              +36\omega^7L_k^2}{9\omega^8}.
\end{aligned}
 \tag{12}
\]

The \(L_k^2\) term is the full nonlinear root curvature at this order.
It is retained. In particular, no third-moment sign or modulus-square
curvature is discarded. Recursive full substitution of all nine (11)
into the actual polynomial jet (9) gives zero modulo \(s^5\).

Define the half-normal \(n_k(s)=(|Z_k(s)|^2-1)/2\), and write
\(\theta=2\pi k/9\), \(z_\theta=\cos\theta\). Its second coefficient is

\[
 [s^2]n_k
 =\lambda[-1+x(1-\cos\theta)+y(1-\cos2\theta)]
 =-2\lambda y(z_\theta+1/2)(z_\theta+c).
 \tag{13}
\]

Exactly the four labels3,4,5,6 have zero second coefficient. The other
five have a strictly negative second coefficient: labels0,1,2,7,8 have
\(z_\theta>-1/2\). Here \(y,\lambda>0\).

The third coefficient for **each individual** normal is

\[
 [s^3]n_k
 =g\sin\theta+48k\sin2\theta-\frac{56}{3}\sin3\theta.
 \tag{14}
\]

At labels3,6, \(\sin2\theta=-\sin\theta\) and \(\sin3\theta=0\),
so (14) vanishes because \(g=48k\). At label4,

\[
 \sin\theta+\sin2\theta=(1-2c)\sin(\pi/9),\quad
 \sin3\theta=(4c^2-1)\sin(\pi/9).
\]

Since \(g=-56(1+2c)/3\), (14) also vanishes there. It has the opposite
sign at label5 and hence vanishes there too. These are complete
individual cancellations, rather than cancellation of only pair means.
At a nonreal cube phase \(\omega^3=1\), (12) instead gives

\[
 W_k=-3ig\omega,\qquad |W_k|=56(1+2c)>0.
 \tag{15}
\]

This purely tangential term survives every radial cancellation.

## 4. Complete fourth-order inward closure

The full fourth coefficient is

\[
 [s^4]n_k=\Re(\overline\omega V_k)+|L_k|^2/2.
 \tag{16}
\]

Both terms are essential. Let \(A_k=1-\cos\theta_k\),
\(B_k=1-\cos2\theta_k\). Substituting the entire (10)-(12) into (16)
gives, for labels3,4,

\[
 [s^4]n_k=R_k-A_kM+8B_k\beta,
 \tag{17}
\]
\[
 \begin{array}{c|c|c|c}
 k&A_k&B_k&R_k\\\hline
 3&3/2&3/2&-(431+320c+320c^2)/3\\
 4&1+c&1-d&-(1636+2842c+1980c^2)/9.
 \end{array}
 \tag{18}
\]

One way to check the parameter columns separately is to differentiate
(10). The \(M\) column first enters as \(-9M(z^8-1)\), giving
\(-A_kM\) in (16). The \(\beta\) column first enters as
\(72\beta(z^7-1)\), giving \(8B_k\beta\). All other
fourth-order terms, including both curvatures, form \(R_k\). Their exact
values in (18), and the complete affine coefficient maps in the two
free parameters, are checked without sampled parameter substitutions.

The determinant of the two columns is

\[
 \det\begin{pmatrix}-A_3&8B_3\\-A_4&8B_4\end{pmatrix}
 =12(c+d)>0.
 \tag{19}
\]

The physical \(c>15/16\) implies \(d>0\). Therefore a unique pair of
finite real parameters gives both fourth coefficients equal to−1.
Solving (17) and reducing by \(8c^3-6c-1=0\) gives exactly
\(M=M_*\), \(\beta=\beta_*\) in (5).

The actual polynomial satisfies
\(p_{-s}(z)=\overline{p_s(\overline z)}\), since all free parameters
are real and (6) has this symmetry. Uniqueness of the simple-root maps
gives \(Z_k(-s)=\overline{Z_{9-k}(s)}\), and hence
\(n_k(-s)=n_{9-k}(s)\). Opposite fourth coefficients are equal.
Consequently, for **all four** active labels,

\[
 n_k(s)=-s^4+O(s^5),\qquad k=3,4,5,6.
 \tag{20}
\]

The checker also verifies every coefficient of this reversal identity
through order4 for all nine labels after closing the parameters.

## 5. From jets to actual disk containment for every small parameter

This is an ordinary analytic completeness step, separate from the finite
algebra. Choose disjoint open neighborhoods of the nine distinct roots
of \(z^9-1\). The analytic implicit function theorem supplies, on one
common real interval \(|s|<s_1\), the nine root branches used above.
They stay distinct and each is simple after shrinking this interval.
Nine distinct roots exhaust a degree-nine polynomial. The root near1
is exactly \(a(s)\), by its anchor and uniqueness.

For each inactive label put \(q_k=[s^2]n_k<0\). Its convergent Taylor
expansion gives \(n_k/s^2\to q_k\) for \(s\to0\). Therefore there
is a positive interval on which \(n_k<0\) for every nonzero real
\(s\) in it. At each active label, (20) gives \(n_k/s^4\to-1\),
so the same conclusion holds on a positive interval. Take the minimum
of these nine finite positive widths and \(s_1\), also shrinking until
\(0<a(s)<1\). It is a positive width on which **every** root is
strictly in the disk for **every** positive parameter. No numerical
root sample, truncation sign without a remainder, or assumed feasible
critical tuple is used. Equivalently there is an existential positive
\(\eta\)-collar under \(\eta=\lambda s^2\).

Critical distances tend to1, so, on a further common interval, all are
positive and the reciprocal objective is real analytic in \(s\).
Conjugation of the entire critical multiset when \(s\) changes sign
makes this objective even. Its squared distances are precisely
\(|a-m-\nu_L|^2\) and seven copies of \(|a-m-\nu_S|^2\).
Full scalar expansion of their inverse square roots gives

\[
 F(s)=8+\lambda C s^2+\lambda^2K s^4+O(s^6).
 \tag{21}
\]

The complete first-power coefficient maps through order4, with arbitrary
\(M,\beta\) first and their exact values (5) second, are included in
the finite record. Evenness justifies the indicated order6 remainder;
it does not follow from a finite order4 check alone. Substituting
\(s=\sqrt{\eta/\lambda}\) proves (3).

For the physical real embedding, \(8c^3-6c-1=0\),
\(c\in(\sqrt3/2,1)\), and this cubic is strictly increasing there.
Its values at15/16 and47/50 are respectively−17/512 and73/15625.
Thus \(15/16<c<47/50\). The numerator of \(K\) has derivative
\(47482-125896c<0\) on this bracket, and exact rational endpoints give

\[
 K>\frac{5592017}{607500}>9,\qquad
 K<\frac{194645}{20736}<10.
 \tag{22}
\]

The strict gap from10, together with the ordinary remainder in (3),
gives the second cut in (4) for every sufficiently small positive
\(\eta\). Also \(C<3\), because \(c>0\) and \(y<1/3\).
Shrinking until \(10\eta<3-C\) gives the first cut. Finally shrink
the collar to \(\eta_0\le1/12000\). This does **not** claim that the
whole interval \((0,1/12000]\) is feasible for the construction; only
that one strictly positive subcollar exists. Both cuts and all-root disk
containment hold simultaneously throughout that subcollar.

## 6. The obstruction to a smaller all-original error

Equations (11),(12),(15) and \(\eta=\lambda s^2\) give

\[
 Z_k-B_k=-3ig\omega_k\lambda^{-3/2}\eta^{3/2}
                          +O(\eta^2),\qquad k=3,6.
 \tag{23}
\]

This proves (4a). In particular, after shrinking the collar if needed,
\(|Z_k-B_k|\ge(A/2)\eta^{3/2}\). On this same actual family,
\(\Delta=202\eta^2\), so

\[
 \frac{|Z_k-B_k|}{\Delta}\to+\infty,\qquad
 \frac{|Z_k-B_k|}{\sqrt{\eta\Delta}}\to\frac A{\sqrt{202}}>0.
 \tag{24}
\]

For every finite putative uniform constant in an \(O(\Delta)\)
bound, (24) supplies violations for all sufficiently small positive
parameters. If the bound also had a term uniformly
\(o(\sqrt{\eta\Delta})\), dividing by that scale yields the same
contradiction: the \(\Delta\) term divided by it tends to zero while
the left side has a positive limit. The assertion allows the quantified
\(\epsilon\ge0\) in the existing theorem to vary with the polynomial,
as in (4); it is not a statement about a fixed positive \(\epsilon\).

An arbitrary relabeling cannot remove the obstruction. The limiting
target points \(\omega_k\) have a fixed positive pairwise separation.
Any matching with error tending to zero must, for sufficiently small
parameter, use the unique original branch near each corresponding
\(\omega_k\). Matching a different branch produces an error bounded
away from zero. The marked root fixes the normalization \(a>0\), so
no extra phase choice is being optimized in (2).

The necessity statement itself uses only the explicit actual family and
the self-contained computations above. Calling the \(3/2\) exponent
sharp relative to9954 additionally uses its already published upper
estimate on both cuts. It gives no global first-power resolution or
numerical optimal coefficient, and asserts no novelty for integrated
critical factors or the previously known balanced-profile sphere.

## 7. Exact evidence and remaining trust boundaries

[jets.py](jets.py) constructs the entire actual critical product,
integrates and anchors it in the ring modulo \(s^5\), retains both
free real parameters, and compares it with every coefficient of (10).
It then recursively reconstructs each of the nine root jets, checks
their full substitution, all nine individual normals, the exact cubic
cancellations, both complete affine fourth-normal rows, the nonzero
determinant, explicit closing parameters, and all four strict inward
fourth coefficients. The whole first-power objective and every
coefficient of its two-parameter expansion are reconstructed separately.

The twelve rational-coordinate field is
\(\mathbb Q[w,i]/(w^6+w^3+1,i^2+1)\), with physical
\(w=e^{2\pi i/9}\). Real embedding signs are isolated by the exact
cubic bracket above. The credited [arithmetic.py](arithmetic.py) is
unchanged same-author reuse from
[9671](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/effective-profile-stability/PROOF.md)
and9954. It is not a separate backend or independent review.

[verify.py](verify.py) regenerates and compares the entire recursively
typed [EXPECTED.json](EXPECTED.json), and rejects ten deliberately
damaged mathematical constructions without relying on the frozen
fixture. [validate.py](validate.py) checks ordinary and optimized runs,
fresh isolated source-only copies, malformed whole external records,
and source-byte integrity, with serial children, six native thread
variables1 and a fixed45-second guard per child.

Finite exact algebra corroborates the written formulas. Analytic
implicit-root existence, exhaustion by nine simple branches, parity
of convergent series, uniform finite-nine Taylor remainders, the
all-small-parameter disk/cut conclusions, and the asymptotic obstruction
are ordinary written mathematics outside a formal proof kernel. No
floating-point computation or solver is part of this certificate.
Author checks and shared signing credentials imply no independent
review verdict. The referenced reviews cover their older, precisely
scoped targets; their verdicts do not transfer to this construction.
